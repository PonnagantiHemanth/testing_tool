#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pychannel.blechannel
:brief: BLE communication channel classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/09/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from queue import Empty
from sys import stdout
from time import perf_counter_ns
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.logiconstants import LogitechBleConnectionParameters
from pychannel.logiconstants import LogitechBleConstants
from pychannel.logiconstants import LogitechVendorUuid
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueWithFilter
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pytransport.ble.bleconstants import BleContextEventType
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.blecontext import BleContext
from pytransport.ble.blecontext import BleContextDevice
from pytransport.ble.bleinterfaceclasses import BleCharacteristic
from pytransport.ble.bleinterfaceclasses import BleGapAddress
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.blemessage import BleMessage
from pytransport.transportcontext import TransportContextException
from pytransport.transportmessage import TransportMessage

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

# Configure all transports traces verbosity
#  - None: disable all traces (Default)
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for packets only
#  - TraceLevel.DEBUG: Debug level will be for every context actions
FORCE_AT_CREATION_ALL_BLE_CHANNEL_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_BLE_CHANNEL_TRACE_FILE_NAME = None


class ReportReferenceIndex:
    """
    Indexes in the HID report characteristic descriptor value
    """
    REPORT_ID = 0
    REPORT_TYPE = 1
# end class ReportReferenceIndex


class HidReportType:
    """
    HID report types that can be found in a HID Report characteristic Report Reference descriptor value
    """
    INPUT_REPORT = 1
    OUTPUT_REPORT = 2
    FEATURE_REPORT = 3
# end class HidReportType


class HidReportId:
    """
    Report IDs that can be found in a HID Report characteristic Report Reference descriptor value
    """
    KEYBOARD = 0x01
    MOUSE = 0x02
    CONSUMER_CONTROL = 0x03
    SYSTEM_CONTROL = 0x04
    CONSUMER_SPECIFIC = 0x05
    TOP_ROW = 0x09
    CALL_STATE_MGT = 0x0B
    MOUSE_WIRELESS = 0x0F
    SHORT_HID_PP = 0x10
    LONG_HID_PP = 0x11
    GAMING_MOUSE = 0x15
    GAMING_KEYBOARD = 0x18
    WIN_DIGITIZER = 0x1E
    WIN_DEV_CAP = 0x1F
    WIN_DEV_CER = 0x20
    IPAD_DIGITIZER = 0x21
    IPAD_FAKE_KBD = 0x22
# end class HidReportId


class HidppPipe(IntEnum):
    """
    Constants to use to chose which pipe to use for the HID++ exchanges
    """
    HID_SERVICE = 1
    BLEPP_SERVICE = 2
# end class HidppPipe


BASE_UUID_TO_ADD = [
    LogitechVendorUuid.BLE_PRO_CHAR_BASE, LogitechVendorUuid.BLEPP_APP_BASE, LogitechVendorUuid.BLEPP_BOOT_BASE]


REPORT_ID_TO_LINK_ENABLER = {
    HidReportId.KEYBOARD: LinkEnablerInfo.KEYBOARD_POSITION,
    HidReportId.GAMING_KEYBOARD: LinkEnablerInfo.KEYBOARD_POSITION,
    HidReportId.MOUSE: LinkEnablerInfo.MOUSE_POSITION,
    HidReportId.GAMING_MOUSE: LinkEnablerInfo.MOUSE_POSITION,
    HidReportId.SHORT_HID_PP: LinkEnablerInfo.HID_PP_POSITION,
    HidReportId.LONG_HID_PP: LinkEnablerInfo.HID_PP_POSITION,
    HidReportId.WIN_DIGITIZER: LinkEnablerInfo.DIGITIZER_POSITION
}

HID_REPORT_ID_TO_LOGITECH_REPORT_TYPE = {
    HidReportId.KEYBOARD: LogitechReportType.KEYBOARD,
    HidReportId.GAMING_KEYBOARD: LogitechReportType.KEYBOARD,
    HidReportId.MOUSE: LogitechReportType.MOUSE,
    HidReportId.GAMING_MOUSE: LogitechReportType.MOUSE,
    HidReportId.SHORT_HID_PP: LogitechReportType.HIDPP,
    HidReportId.LONG_HID_PP: LogitechReportType.HIDPP,
    HidReportId.WIN_DIGITIZER: LogitechReportType.DIGITIZER
}


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleChannel(BaseCommunicationChannel):
    """
    Implementation of a Ble communication channel.
    """
    MAX_RETRY = 4
    # Define the number of retry that will trigger a log on console
    RETRY_THRESHOLD_TO_LOG = 1

    def __init__(self, ble_context, ble_context_device, trace_level=TraceLevel.NO_TRACE,
                 trace_file_name=None):
        """
        :param ble_context: BLE context to use for this channel
        :type ble_context: ``BleContext``
        :param ble_context_device: BLE context device to use for this channel
        :type ble_context_device: ``BleContextDevice``
        :param trace_level: Trace level of the channel - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the channel - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        """
        if FORCE_AT_CREATION_ALL_BLE_CHANNEL_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_BLE_CHANNEL_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_BLE_CHANNEL_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_BLE_CHANNEL_TRACE_FILE_NAME
        # end if

        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        self._report_type_to_process_message_callback[LogitechReportType.HIDPP] = self._hidpp_process_wrapper

        self._ble_context = ble_context
        self._ble_context_device = ble_context_device
        self._services = None
        self.report_type_in_to_characteristic = {}
        self.report_type_out_to_characteristic = {}
        self.report_type_time_stamped_msg_queue = {}
        self.protocol = LogitechProtocol.BLE
        self._current_hidpp_pipe = HidppPipe.HID_SERVICE

        for report_type in LogitechReportType:
            self.report_type_time_stamped_msg_queue[report_type] = QueueWithFilter()
        # end for

        TRACE_LOGGER.update_trace_name(
            subscription_owner=self, trace_name=f"BLE Channel with address {self._ble_context_device.address}")
    # end def __init__

    def __str__(self):
        return f"{self.__class__.__name__}(address: {self._ble_context_device.address})"
    # end def __str__

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self, link_enabler=LinkEnablerInfo.ALL_MASK, hidpp_pipe=None):
        """
        Open the channel.

        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo``
        :type link_enabler: ``int`` or ``BitStruct``
        :param hidpp_pipe: Pipe tu use for the HID++ communication. If ``None``, the value used in the precedent open
                           will be used, if it is the first open by default it is on the HID service - OPTIONAL
        :type hidpp_pipe: ``HidppPipe`` or ``None``

        :raise ``ChannelException``: If the BLE context is not open, or hardware device is off, or the configuration of
                                     characteristic is not as expected
        """
        if not self.is_open:
            if not self._ble_context.is_open:
                raise ChannelException(ChannelException.Cause.CONTEXT_NOT_OPEN)
            # end if

            if not self._is_hardware_device_on():
                raise ChannelException(ChannelException.Cause.HARDWARE_DEVICE_OFF)
            # end if

            if not self._ble_context_device.connected:
                self.connect_encrypt_to_device()
            # end if

            if isinstance(link_enabler, int):
                link_enabler = BitStruct(Numeral(link_enabler))
            # end if

            if hidpp_pipe is None:
                hidpp_pipe = self._current_hidpp_pipe
            # end if

            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Opening (link enable = {link_enabler})...",
                trace_level=TraceLevel.DEBUG)

            self._services = self._ble_context.get_gatt_table(ble_context_device=self._ble_context_device)
            hid_report_characteristics = self._get_hid_report_characteristics_and_descriptors(
                services=self._services,
                uuid_characteristic=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.REPORT,
                                            is_16_bits_uuid=True),
                uuid_descriptor=BleUuid(value=BleUuidStandardDescriptor.REPORT_REFERENCE, is_16_bits_uuid=True))

            for characteristic, descriptors in hid_report_characteristics:
                for descriptor in descriptors:
                    ble_message = self._ble_context.attribute_read(
                        ble_context_device=self._ble_context_device, attribute=descriptor)
                    report_id = ble_message.data[ReportReferenceIndex.REPORT_ID]
                    if report_id in REPORT_ID_TO_LINK_ENABLER and \
                            link_enabler.testBit(REPORT_ID_TO_LINK_ENABLER[report_id]):
                        hid_report_type = ble_message.data[ReportReferenceIndex.REPORT_TYPE]
                        logitech_report_type = HID_REPORT_ID_TO_LOGITECH_REPORT_TYPE[report_id]

                        if logitech_report_type == LogitechReportType.HIDPP:
                            if hidpp_pipe != HidppPipe.HID_SERVICE:
                                # Skip this characteristic if the pipe for HID++ was not chosen on the HID service
                                continue
                            elif self._current_hidpp_pipe != HidppPipe.HID_SERVICE:
                                self._current_hidpp_pipe = HidppPipe.HID_SERVICE
                            # end if
                        # end if

                        if hid_report_type == HidReportType.INPUT_REPORT:
                            if logitech_report_type in self.report_type_in_to_characteristic:
                                raise ChannelException(ChannelException.Cause.CONFIGURATION_ERROR,
                                                       f"Input Report ID present multiple times {logitech_report_type}")
                            # end if

                            if not self._ble_context.get_notification_status(
                                    ble_context_device=self._ble_context_device, characteristic=characteristic):
                                self._ble_context.enable_notification(
                                    ble_context_device=self._ble_context_device,
                                    characteristic=characteristic,
                                    time_stamped_queue=self.report_type_time_stamped_msg_queue[logitech_report_type])
                            else:
                                self._ble_context.update_notification_queue(
                                    ble_context_device=self._ble_context_device,
                                    characteristic=characteristic,
                                    time_stamped_queue=self.report_type_time_stamped_msg_queue[logitech_report_type])
                            # end if
                            self.report_type_in_to_characteristic[logitech_report_type] = characteristic
                        elif hid_report_type == HidReportType.OUTPUT_REPORT:
                            if logitech_report_type in self.report_type_out_to_characteristic:
                                raise ChannelException(ChannelException.Cause.CONFIGURATION_ERROR,
                                                       f"Out Report ID present multiple times {logitech_report_type}")
                            # end if
                            self.report_type_out_to_characteristic[logitech_report_type] = characteristic
                        else:
                            raise ChannelException(ChannelException.Cause.CONFIGURATION_ERROR,
                                                   f"Unknown HID report type ({hid_report_type}) for a wanted link")
                        # end if
                    # end if
                # end for
            # end for

            # If not Report for HID++ was found (or the pipe chosen was BLE++) but link is enable, try to
            # find BLE++ service
            if link_enabler.testBit(LinkEnablerInfo.HID_PP_MASK) and \
                    (LogitechReportType.HIDPP not in self.report_type_in_to_characteristic or
                     LogitechReportType.HIDPP not in self.report_type_out_to_characteristic):
                self._enable_blepp_pipe()
            # end if

            self.is_open = True
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Channel already open", trace_level=TraceLevel.DEBUG)
        # end if
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See ``BaseCommunicationChannel.close``
        if self.is_open:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Closing...", trace_level=TraceLevel.DEBUG)
            try:
                for logitech_report_type in self.report_type_in_to_characteristic:
                    if self._ble_context_device.connected:
                        # noinspection PyBroadException
                        try:
                            self._ble_context.disable_notification(
                                ble_context_device=self._ble_context_device,
                                characteristic=self.report_type_in_to_characteristic[logitech_report_type])
                        except Exception:
                            # The connection could be lost during the disabling, therefore it is important not to stop
                            # there
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message="Exception while disabling notification of the BLE device: "
                                        f"{TracebackLogWrapper.get_traceback_stack()}",
                                trace_level=TraceLevel.WARNING)
                        # end try
                    # end if
                    while not self.report_type_time_stamped_msg_queue[logitech_report_type].event_empty.is_set():
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message="Untreated message in queue: "
                                    f"{self.report_type_time_stamped_msg_queue[logitech_report_type].get()}",
                            trace_level=TraceLevel.WARNING)
                    # end while
                # end for
                untreated_messages = self.hid_dispatcher.clear_all_queues()
                for untreated_message in untreated_messages:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Untreated message in HID dispatcher: {untreated_message}",
                        trace_level=TraceLevel.WARNING)
                # end for
            finally:
                self.is_open = False
                self.report_type_in_to_characteristic.clear()
                self.report_type_out_to_characteristic.clear()
                self._services = None
            # end try
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Channel already closed", trace_level=TraceLevel.DEBUG)
        # end if
    # end def close

    def set_hidpp_pipe(self, hidpp_pipe):
        """
        Set the HID++ pipe.

        :param hidpp_pipe: Pipe to use for the HID++ communication
        :type hidpp_pipe: ``HidppPipe``
        """
        # Sanity check
        if not self.is_open or self._services is None:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self._ble_context_device.connected:
            raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        if LogitechReportType.HIDPP not in self.report_type_in_to_characteristic or \
                LogitechReportType.HIDPP not in self.report_type_out_to_characteristic:
            raise ChannelException(ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT)
        # end if

        if self._current_hidpp_pipe == hidpp_pipe:
            return
        # end if

        # Disable the current pipe
        self._ble_context.disable_notification(
            ble_context_device=self._ble_context_device,
            characteristic=self.report_type_in_to_characteristic[LogitechReportType.HIDPP])

        # Enable the wanted pipe
        if hidpp_pipe == HidppPipe.HID_SERVICE:
            hid_report_characteristics = self._get_hid_report_characteristics_and_descriptors(
                services=self._services,
                uuid_characteristic=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.REPORT,
                                            is_16_bits_uuid=True),
                uuid_descriptor=BleUuid(value=BleUuidStandardDescriptor.REPORT_REFERENCE, is_16_bits_uuid=True))

            for characteristic, descriptors in hid_report_characteristics:
                for descriptor in descriptors:
                    ble_message = self._ble_context.attribute_read(
                        ble_context_device=self._ble_context_device, attribute=descriptor)
                    report_id = ble_message.data[ReportReferenceIndex.REPORT_ID]
                    hid_report_type = ble_message.data[ReportReferenceIndex.REPORT_TYPE]

                    if HID_REPORT_ID_TO_LOGITECH_REPORT_TYPE[report_id] != LogitechReportType.HIDPP:
                        continue
                    elif self._current_hidpp_pipe != HidppPipe.HID_SERVICE:
                        self._current_hidpp_pipe = HidppPipe.HID_SERVICE
                    # end if

                    if hid_report_type == HidReportType.INPUT_REPORT:
                        if not self._ble_context.get_notification_status(
                                ble_context_device=self._ble_context_device, characteristic=characteristic):
                            self._ble_context.enable_notification(
                                ble_context_device=self._ble_context_device,
                                characteristic=characteristic,
                                time_stamped_queue=self.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP])
                        else:
                            self._ble_context.update_notification_queue(
                                ble_context_device=self._ble_context_device,
                                characteristic=characteristic,
                                time_stamped_queue=self.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP])
                        # end if
                        self.report_type_in_to_characteristic[LogitechReportType.HIDPP] = characteristic
                    elif hid_report_type == HidReportType.OUTPUT_REPORT:
                        self.report_type_out_to_characteristic[LogitechReportType.HIDPP] = characteristic
                    else:
                        raise ChannelException(ChannelException.Cause.CONFIGURATION_ERROR,
                                               f"Unknown HID report type ({hid_report_type}) for HID++ link")
                    # end if
                # end for
            # end for
        elif hidpp_pipe == HidppPipe.BLEPP_SERVICE:
            self._enable_blepp_pipe()
        else:
            raise ChannelException(ChannelException.Cause.WRONG_PARAMETER,
                                   f"Unknown HID++ pipe ({hidpp_pipe}), only {HidppPipe.HID_SERVICE} and "
                                   f"{HidppPipe.BLEPP_SERVICE} are implemented")
        # end if
    # end def set_hidpp_pipe

    def get_hidpp_pipe(self):
        """
        Get the HID++ pipe.

        :return: Pipe used for the HID++ communication
        :rtype: ``HidppPipe``
        """
        return self._current_hidpp_pipe
    # end def get_hidpp_pipe

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def update_callback(self, targeted_report_types, callback=None):
        # See ``BaseCommunicationChannel.update_callback``
        if self.is_open:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Updating callbacks...", trace_level=TraceLevel.DEBUG)

            if not self._ble_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
                self._ble_context.update_device_list()
            # end if

            if self._ble_context_device.connected:
                targeted_report_types_left = targeted_report_types.copy()
                for targeted_report_type in targeted_report_types:
                    targeted_characteristic: BleCharacteristic = self.report_type_in_to_characteristic.get(
                        targeted_report_type, None)
                    if targeted_characteristic is None:
                        continue
                    else:
                        targeted_report_types_left.remove(targeted_report_type)
                    # end if
                    self._ble_context_device.set_transfer_callback(
                        transfer_type_key=targeted_characteristic.handle, callback=callback)
                # end for
                if len(targeted_report_types_left) > 0:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Targeted report types {targeted_report_types_left} "
                                                         "not in the DUT open links",
                        trace_level=TraceLevel.DEBUG)
                # end if
            else:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self, message="BleChannel.update_callback skipped: Device not connected",
                    trace_level=TraceLevel.DEBUG)
            # end if
        else:
            TRACE_LOGGER.log_trace(
                    subscription_owner=self, message="BleChannel.update_callback skipped: Channel closed",
                    trace_level=TraceLevel.DEBUG)
        # end if
    # end def update_callback

    def send_data(self, data, timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT):
        """
        Send data through the channel.

        :param data: Data to send
        :type data: ``TimestampedBitFieldContainerMixin`` or ``HexList`` or ``BleMessage``
        :param timeout: The timeout of this action in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``

        :raise ``ChannelException``: If channel is not open, device not connected, HID++ link not present or not all
                                     bytes are sent
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self._ble_context_device.connected:
            raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        if LogitechReportType.HIDPP not in self.report_type_out_to_characteristic:
            raise ChannelException(ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT)
        # end if

        if not isinstance(data, BleMessage):
            # Create a BleMessage object
            ble_message = BleMessage(message_class=type(data), timestamp=perf_counter_ns())
            data_list = list(HexList(data))
        else:
            ble_message = data
            data_list = list(data.data)
        # end if

        characteristic = self.report_type_out_to_characteristic[LogitechReportType.HIDPP]
        if characteristic.uuid == BleUuid(value=BleUuidStandardCharacteristicAndObjectType.REPORT):
            # The report type needs to be removed for data on HID++ report characteristic.
            number_of_bytes_to_remove = 1
        elif characteristic.uuid == BleUuid.from_array(uuid_array=LogitechVendorUuid.BOOTLOADER_CHARACTERISTIC) or \
                characteristic.uuid == BleUuid.from_array(uuid_array=LogitechVendorUuid.APPLICATION_CHARACTERISTIC):
            # The report type and the device number needs to be removed for data on HID++ proprietary service
            # characteristic.
            number_of_bytes_to_remove = 2
        else:
            raise ChannelException(ChannelException.Cause.CONFIGURATION_ERROR, "Output characteristic unknown")
        # end if

        # Regardless of if it is a short or a long report, the size of the data should be of long report
        # minus number_of_bytes_to_remove because it is the size of the characteristic's data.
        data_list = data_list[number_of_bytes_to_remove:] + [0] * \
            (HidppMessage.LONG_MSG_SIZE - len(data_list[number_of_bytes_to_remove:]) - number_of_bytes_to_remove)
        ble_message.data = HexList(data_list)

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Sending {ble_message}...", trace_level=TraceLevel.DEBUG)

        self._ble_context.characteristic_write(
            ble_context_device=self._ble_context_device, characteristic=characteristic, data=ble_message)
        ble_message.timestamp = perf_counter_ns()

        if isinstance(data, TimestampedBitFieldContainerMixin):
            data.timestamp = ble_message.timestamp
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {data}", trace_level=TraceLevel.INFO)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {ble_message}", trace_level=TraceLevel.INFO)
        # end if
    # end def send_data

    def get_message(
            self,
            report_type=LogitechReportType.HIDPP,
            dispatcher_queue=None,
            raw_filters=None,
            message_class=None,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            skip_error=False):
        """
        Get message received through the channel. The parameters are used this way:

        * If NO ``dispatcher_queue`` is given, ``raw_filters`` is taken into account and ``message_class`` is ignored
        * If A ``dispatcher_queue`` is given, ``message_class`` is taken into account and ``raw_filters`` is ignored

        This method has an error message catching mechanism that can be skipped with the parameter ``skip_error``. If
        no filters are given in the parameters (``raw_filters``, ``message_class``), the mechanism will be automatically
        skipped and ``skip_error`` will be ignored. The mechanism will work as follows (when filters are given):

        * It checks if the error message types (HID++ 1 and HID++ 2) are present in the filters
        * Each type of error that IS NOT present in the filters is added and an exception is raised if it is the type
          of message that is returned
        * Each type of error that IS present in the filters will be returned by this method if it is the type
          of message that is returned

        :param report_type: The report type of message to get - OPTIONAL
        :type report_type: ``LogitechReportType``
        :param dispatcher_queue: Queue in the dispatcher to find the message in. If None, the dispatcher step is not
                                 performed - OPTIONAL
        :type dispatcher_queue: ``hid_message_queue`` or ``None``
        :param raw_filters: A list of filter for the message. If ``None``, the message is not checked. This parameter is
                            only relevant if ``dispatcher_queue`` IS ``None``, otherwise it is ignored - OPTIONAL
        :type raw_filters: ``list[MessageFilter]`` or ``tuple[list[MessageFilter]]`` or ``None``
        :param message_class: The class(es) of the message to get during the dispatcher step. If ``None``, the message
                              class is not checked. This parameter is only relevant if ``dispatcher_queue`` IS NOT
                              ``None``, otherwise it is ignored - OPTIONAL
        :type message_class: ``type`` or ``tuple[type]`` or ``None``
        :param timeout: The timeout of this action in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``
        :param skip_error: Flag indicating if the automatic error catching mechanism should be skipped or not
        :type skip_error: ``bool``

        :return: The first message received on this channel
        :rtype: ``BleMessage`` or ``TimestampedBitFieldContainerMixin``

        :raise ``ChannelException``: If channel is not open, device not connected, HID++ link not present or not all
                                     bytes are sent
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if report_type not in self.report_type_in_to_characteristic:
            raise ChannelException(ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT, f"Report type = {report_type}")
        # end if

        message = self._common_get_message(
            report_type=report_type,
            time_stamped_msg_queue=self.report_type_time_stamped_msg_queue[report_type],
            dispatcher_queue=dispatcher_queue,
            raw_filters=raw_filters,
            message_class=message_class,
            timeout=timeout,
            skip_error=skip_error)

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Received message {message}", trace_level=TraceLevel.INFO)

        return message
    # end def get_message

    def process_all_report_type_in_dispatcher(self, report_type=LogitechReportType.HIDPP):
        # See ``BaseCommunicationChannel.process_all_report_type_in_dispatcher``
        while not self.report_type_time_stamped_msg_queue[report_type].event_empty.is_set():
            transport_message = self.report_type_time_stamped_msg_queue[report_type].get_nowait()
            self._report_type_to_process_message_callback[report_type](transport_message=transport_message)
        # end while
    # end def process_all_report_type_in_dispatcher

    def get_descriptors(self):
        # See ``BaseCommunicationChannel.get_descriptors``
        # The value of the parameter interface does not matter so 0 is given
        return [self.get_interface_descriptor(interface=0)]
    # end def get_descriptors

    def get_interface_descriptor(self, interface):
        # See ``BaseCommunicationChannel.get_interface_descriptor``
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self._ble_context_device.connected:
            raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        hid_report_map_characteristic = self._get_hid_report_characteristics_and_descriptors(
            services=self._services,
            uuid_characteristic=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.REPORT_MAP,
                                        is_16_bits_uuid=True))[0][0]

        descriptor = self._ble_context.attribute_read(
            ble_context_device=self._ble_context_device, attribute=hid_report_map_characteristic)

        self.hid_dispatcher.process_control_read_get_descriptor(descriptor)

        try:
            descriptor_message = self.hid_dispatcher.interface_descriptor_queue.get(timeout=.01)
        except Empty:
            descriptor_message = None
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="A descriptor is missing", trace_level=TraceLevel.WARNING)
        # end try
        return descriptor_message
    # end def get_interface_descriptor

    def get_transport_id(self, force_refresh_cache=False):
        """
        Get the transport ID of the device, this mean Bluetooth ID in advertising packet for BLE devices.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: The transport ID
        :rtype: ``int``
        """
        # TODO: It will be done with the device manager as currently the BLE context is not working properly

        return 0
    # end def get_transport_id

    def is_device_connected(self, force_refresh_cache=False):
        """
        Check if the BLE device is connected. If the device is not connected, the channel will be automatically closed.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        if force_refresh_cache:
            self._ble_context.update_device_list()
        # end if

        connected = self._ble_context_device.connected

        if not connected:
            self.close()
        # end if

        return connected
    # end def is_device_connected

    def wait_device_connection_state(self, connected, timeout):
        # See ``BaseCommunicationChannel.wait_device_connection_state``
        if connected and not self._ble_context_device.connected:
            try:
                self.connect_encrypt_to_device(timeout=timeout)
                return True
            except ChannelException as e:
                if e.get_cause() != ChannelException.Cause.DEVICE_NOT_PRESENT:
                    raise
                # end if
                return False
            # end try
        else:
            if self._ble_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
                event_to_use = self._ble_context_device.wait_for_connection_event if connected \
                    else self._ble_context_device.wait_for_disconnection_event

                event_to_use.clear()
                try:
                    if self._ble_context_device.connected is not connected:
                        return event_to_use.wait(timeout=timeout)
                    else:
                        return True
                    # end if
                finally:
                    event_to_use.set()
                # end try
            else:
                remaining_time = timeout
                while self.is_device_connected(force_refresh_cache=True) is not connected and remaining_time > 0:
                    # For now the only option we have is to wait some time and test check the state again
                    sleep(self.WAIT_CONNECTION_STATE_PERIOD if remaining_time > self.WAIT_CONNECTION_STATE_PERIOD
                          else remaining_time)

                    remaining_time -= self.WAIT_CONNECTION_STATE_PERIOD
                # end while

                return self.is_device_connected(force_refresh_cache=True) is connected
            # end if
        # end if
    # end def wait_device_connection_state

    def is_link_enabled(self, link_report_type):
        """
        Check if a link is enabled. It returns ``False`` if the channel is closed.

        :param link_report_type: Report type of the link to check.
        :type link_report_type: ``LogitechReportType``

        :return: Flag indicating if the link is enabled
        :rtype: ``bool``
        """
        return self.is_open and (link_report_type not in self.report_type_out_to_characteristic or
                                 link_report_type not in self.report_type_in_to_characteristic)
    # end def is_link_enabled

    def connect_encrypt_to_device(self, timeout=BleContext.GENERIC_SCAN_TIME):
        """
        Scan for the already bonded device, connect to it and encrypt the communication. Nothing is done if the device
        is already connected.

        :param timeout: Timeout to scan for the device advertising in directed mode - OPTIONAL
        :type timeout: ``int`` or ``float``

        :raise ``ChannelException``: If device not present during scanning
        """
        if not self._ble_context_device.connected:
            if self.hardware_device is not None:
                self.hardware_device.wake_up_device()
            else:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message="No hardware device associated to the channel, cannot wake device up",
                    trace_level=TraceLevel.DEBUG)
            # end if

            if not self._ble_context.is_direct_advertising_device_present(
                    ble_context_device=self._ble_context_device, scan_time=timeout):
                raise ChannelException(
                    ChannelException.Cause.DEVICE_NOT_PRESENT,
                    f"Device with address {self._ble_context_device.address} is not advertising")
            # end if

            counter = 0
            while counter < self.MAX_RETRY:
                try:
                    # We add the connection confirmation mechanism only if it fails the first time as it adds a delay
                    connection_parameters = BleGapConnectionParameters(
                        min_connection_interval=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_CONNECTION_INTERVAL_MS,
                        max_connection_interval=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_CONNECTION_INTERVAL_MS,
                        supervision_timeout=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_SUPERVISION_TIMEOUT_MS,
                        slave_latency=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_SLAVE_LATENCY)
                    self._ble_context_device.wait_for_disconnection_event.clear()
                    connected = self._ble_context.connect(
                        ble_context_device=self._ble_context_device, connection_parameters=connection_parameters,
                        service_discovery=False, confirm_connect=counter > 0)
                    assert connected, "Connection failed"

                    self._ble_context.perform_service_discovery(
                        ble_context_device=self._ble_context_device, vendor_uuid_bases_to_add=BASE_UUID_TO_ADD)
                    self._ble_context.authenticate_just_works(ble_context_device=self._ble_context_device)

                    if counter > self.RETRY_THRESHOLD_TO_LOG:
                        to_log = f"[BLE channel] Connection to device ({self._ble_context_device.address}) had to be " \
                                 f"retried {counter} time(s)"
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self, message=to_log, trace_level=TraceLevel.WARNING)
                        # TODO: This is to be removed when we do not want the statistics anymore.
                        #  See https://jira.logitech.io/browse/PTB-1850
                        stdout.write(to_log + "\n")
                    # end if
                    break
                except AssertionError as e:
                    counter += 1
                    if str(e) in ("No response from device", "Connection failed") and counter < self.MAX_RETRY:
                        self.wait_for_disconnection(ble_context_device=self._ble_context_device)
                        continue
                    # end if
                    e.args += (f"after {counter} tries",)
                    raise
                except TransportContextException as e:
                    counter += 1
                    if e.get_cause() in [TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                         TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION] and \
                            counter < self.MAX_RETRY:
                        self.wait_for_disconnection(ble_context_device=self._ble_context_device)
                        continue
                    # end if
                    e.add_message(f"after {counter} tries")
                    raise
                finally:
                    self._ble_context_device.wait_for_disconnection_event.set()
                # end try
            # end while
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Device already connected", trace_level=TraceLevel.DEBUG)
        # end if
    # end def connect_encrypt_to_device

    def wait_for_disconnection(self, ble_context_device):
        """
        Wait for the disconnection event to be propagated to the BLE context

        :param ble_context_device: Context device to connect and bond to
        :type ble_context_device: ``BleContextDevice``
        """
        # Add a large wait time to let the internal state of the BLE context to be the right one
        if not ble_context_device.wait_for_disconnection_event.wait(
                timeout=BleContext.DISCONNECTION_STATE_SYNC_UP):
            try:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message="BLE context disconnection propagation timeout. "
                            f"Call disconnect device at {perf_counter_ns()}",
                    trace_level=TraceLevel.INFO)
                self.disconnect_from_device()
            except TransportContextException:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message="TransportContextException while trying to disconnect a device",
                    trace_level=TraceLevel.DEBUG)
            # end try
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"BLE context disconnection. Clear event queue at {perf_counter_ns()}",
                trace_level=TraceLevel.INFO)
            ble_context_device.ble_context_event_queue.clear_all_events_of_a_type(
                event_type=BleContextEventType.DISCONNECTION_EVENT)
            sleep(.1)
        # end if
    # end def wait_for_disconnection

    def disconnect_from_device(self):
        """
        Close the channel if open and disconnect from the device.
        """
        if self._ble_context_device.connected:
            if self.is_open:
                self.close()
            # end if

            self._ble_context.disconnect(ble_context_device=self._ble_context_device)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Device already disconnected", trace_level=TraceLevel.DEBUG)
        # end if
    # end def disconnect_from_device

    def get_device_ble_address(self):
        """
        Get the BLE GAP address of the device associated to this channel.

        :return: The BLE GAP address
        :rtype: ``BleGapAddress``
        """
        return self._ble_context_device.address
    # end def get_device_ble_address

    def get_ble_context_device(self):
        """
        Get the BLE context device associated to this channel.

        :return: The BLE context device
        :rtype: ``BleContextDevice``
        """
        return self._ble_context_device
    # end def get_ble_context_device

    def _hidpp_process_wrapper(self, transport_message):
        """
        Wrapper around ``self.__hid_dispatcher.process_interrupt_hidpp`` to add the necessary report ID byte at the
        beginning of the message as it is not given on a BLE packet.

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The queue where the message has been put in or None if the given message could not be treated
        :rtype: ``HidMessageQueue`` or ``None``
        """
        if len(transport_message.data) == LogitechBleConstants.BLEPP_MESSAGE_SIZE:
            transport_message.data = HexList(Hidpp1Data.DeviceIndex.TRANSCEIVER) + transport_message.data
        # end if
        transport_message.data = HexList(HidReportId.LONG_HID_PP) + transport_message.data
        return self.hid_dispatcher.process_interrupt_hidpp(transport_message=transport_message)
    # end def _hidpp_process_wrapper

    @staticmethod
    def _get_hid_report_characteristics_and_descriptors(services, uuid_characteristic, uuid_descriptor=None):
        """
        Get the list of all the HID characteristics and their REPORT_REFERENCE descriptors.

        :param services: This gatt table to parse
        :type services: ``list[BleService]``
        :param uuid_characteristic: UUID of the characteristic to get
        :type uuid_characteristic: ``BleUuid``
        :param uuid_descriptor: UUID of the descriptor to get - OPTIONAL
        :type uuid_descriptor: ``BleUuid`` or ``None``

        :return: A list of tuple of a characteristic and its REPORT_REFERENCE descriptors
        :rtype: ``list[tuple[BleCharacteristic, list[BleDescriptor]]]``
        """
        descriptors_to_return = []
        for service in services:
            if service.uuid == BleUuid(value=BleUuidStandardService.HUMAN_INTERFACE_DEVICE):
                characteristics = service.get_characteristics(characteristic_uuid=uuid_characteristic)
                for characteristic in characteristics:
                    if uuid_descriptor is not None:
                        descriptors = characteristic.get_descriptors(
                            descriptor_uuid=BleUuid(value=BleUuidStandardDescriptor.REPORT_REFERENCE))
                        descriptors_to_return.append((characteristic, descriptors))
                    else:
                        descriptors_to_return.append((characteristic, None))
                    # end if
                # end for

                break
            # end if
        # end for
        return descriptors_to_return
    # end def _get_hid_report_characteristics_and_descriptors

    def _enable_blepp_pipe(self):
        """
        Enable the BLE++ pipe.
        """
        for service in self._services:
            if service.uuid == BleUuid.from_array(uuid_array=LogitechVendorUuid.BOOTLOADER_SERVICE):
                uuid_array_characteristic = LogitechVendorUuid.BOOTLOADER_CHARACTERISTIC
            elif service.uuid == BleUuid.from_array(uuid_array=LogitechVendorUuid.APPLICATION_SERVICE):
                uuid_array_characteristic = LogitechVendorUuid.APPLICATION_CHARACTERISTIC
            else:
                continue
            # end if

            characteristic = service.get_characteristics(
                characteristic_uuid=BleUuid.from_array(uuid_array=uuid_array_characteristic))[0]
            if not self._ble_context.get_notification_status(
                    ble_context_device=self._ble_context_device, characteristic=characteristic):
                self._ble_context.enable_notification(
                    ble_context_device=self._ble_context_device,
                    characteristic=characteristic,
                    time_stamped_queue=self.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP])
            else:
                self._ble_context.update_notification_queue(
                    ble_context_device=self._ble_context_device,
                    characteristic=characteristic,
                    time_stamped_queue=self.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP])
            # end if
            self.report_type_in_to_characteristic[LogitechReportType.HIDPP] = characteristic
            self.report_type_out_to_characteristic[LogitechReportType.HIDPP] = characteristic
            self._current_hidpp_pipe = HidppPipe.BLEPP_SERVICE
            break
        # end for
    # end def _enable_blepp_pipe
# end class BleChannel

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
