#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pychannel.throughreceiverchannel
:brief: Through BLE receiver communication channel classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/08/06
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import weakref
from enum import IntEnum
from enum import auto
from time import perf_counter_ns

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.channelinterfaceclasses import MessageFilter
from pychannel.usbchannel import LogitechReportType
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import BLEProReceiverInformation
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.deviceconnection import EQuadReceiverInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformationModel
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegisterResponse
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueWithFilter
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pytransport.usb.usbmessage import UsbMessage

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

# Configure all transports traces verbosity
#  - None: disable all traces (Default)
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for packets only
#  - TraceLevel.DEBUG: Debug level will be for every context actions
FORCE_AT_CREATION_ALL_THROUGH_BLE_RECEIVER_CHANNEL_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_THROUGH_BLE_RECEIVER_CHANNEL_TRACE_FILE_NAME = None

# This flag is used to activate/deactivate the automatic clear of untreated messages in the queues when
# closing a ThroughReceiverChannel
AUTOMATIC_MESSAGE_CLEAR_IN_CLOSE = False


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ThroughReceiverChannel(BaseCommunicationChannel):
    """
    Common implementation of a communication channel through a receiver.
    """
    DEVICE_INFORMATION_CLASS = None
    DEVICE_PAIRING_INFORMATION_MIN_R0 = None
    DEVICE_NAME_MIN_R0 = None

    class DeviceInformationOffset(IntEnum):
        DEVICE_PAIRING_INFORMATION = 0
        DEVICE_NAME = auto()
    # end class DeviceInformationOffset

    def __init__(self, receiver_channel, device_index, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param receiver_channel: Channel to communicate to the receiver itself
        :type receiver_channel: ``UsbReceiverChannel``
        :param device_index: Index of the device in the receiver
        :type device_index: ``int``
        :param trace_level: Trace level of the transport context - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the transport context - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        """
        if FORCE_AT_CREATION_ALL_THROUGH_BLE_RECEIVER_CHANNEL_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_THROUGH_BLE_RECEIVER_CHANNEL_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_THROUGH_BLE_RECEIVER_CHANNEL_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_THROUGH_BLE_RECEIVER_CHANNEL_TRACE_FILE_NAME
        # end if

        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        self.device_index = device_index
        self.receiver_channel = receiver_channel
        self.connected = None
        self._device_information = [None, None]
        self.hidpp_time_stamped_msg_queue = None
        self.hidpp_link_enabled = False

        self.subscribe_to_receiver_multi_queue()
    # end def __init__

    def __str__(self):
        str_to_return = f"{self.__class__.__name__}(port: {self.get_channel_usb_port_path_str()}, " \
                        f"device index: {self.device_index}"

        if self._device_information[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION] is not \
                None:
            str_to_return += f", transport ID: {self.get_transport_id():04X}"
        # end if

        if self.connected is not None:
            connected = "connected" if self.is_device_connected() else "not connected"
            str_to_return += f", {connected})"
        else:
            str_to_return += ")"
        # end if

        return str_to_return
    # end def __str__

    def __del__(self):
        try:
            if self.is_open:
                self.close()
            # end if

            if self.is_subscribed_to_receiver_multi_queue():
                self.unsubscribe_from_receiver_multi_queue()
            # end if
        finally:
            TRACE_LOGGER.unsubscribe(subscription_owner=self)
        # end try
    # end def __del__

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self, link_enabler=LinkEnablerInfo.HID_PP_MASK):
        """
        Open the channel. As it is a channel through a receiver, only a HID++ link can be done in this structure.
        All HID messages do not have a device index information, making it impossible to know which device triggered
        said message. The receiver channel has to be opened prior to the call of this method.

        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo``. However, only ``LinkEnablerInfo.HID_PP_MASK`` matters
        :type link_enabler: ``int`` or ``BitStruct``

        :raise ``ChannelException``: If the receiver channel is not open or if the HID++ link is not enable on the
                                     receiver channel, and it is asked to be on this one or the hardware device is off
        """
        if not self.receiver_channel.is_open:
            raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
        # end if

        if not self.is_open:
            if not self._is_hardware_device_on():
                raise ChannelException(ChannelException.Cause.HARDWARE_DEVICE_OFF)
            # end if

            # Check if the cache shows the device as connected
            if not self.connected:
                # If the cache says that it is not connected, retry by refreshing the cache
                if not self.is_device_connected(force_refresh_cache=True):
                    raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
                # end if
            # end if

            if isinstance(link_enabler, int):
                link_enabler = BitStruct(Numeral(link_enabler))
            # end if

            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Opening (link enable = {link_enabler})...",
                trace_level=TraceLevel.DEBUG)

            if link_enabler.testBit(LinkEnablerInfo.HID_PP_POSITION):
                if LogitechReportType.HIDPP not in self.receiver_channel.report_type_time_stamped_msg_queue:
                    raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT)
                # end if
                self.hidpp_link_enabled = True
            # end if

            with self.receiver_channel.associated_channels_weak_ref:
                self.receiver_channel.associated_channels_weak_ref[self.device_index] = weakref.ref(self)
            # end with

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

            with self.receiver_channel.associated_channels_weak_ref:
                self.receiver_channel.associated_channels_weak_ref.pop(self.device_index, None)
            # end with

            if AUTOMATIC_MESSAGE_CLEAR_IN_CLOSE:
                if self.hidpp_time_stamped_msg_queue is not None:
                    while not self.hidpp_time_stamped_msg_queue.event_empty.is_set():
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Untreated message in {LogitechReportType.HIDPP} queue: "
                                    f"{self.hidpp_time_stamped_msg_queue.get()}",
                            trace_level=TraceLevel.WARNING)
                    # end while
                # end if
                self._device_information = [None, None]
                untreated_messages = self.hid_dispatcher.clear_all_queues()

                for untreated_message in untreated_messages:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Untreated message in HID dispatcher: {untreated_message}",
                        trace_level=TraceLevel.WARNING)
                # end for
            # end if

            self.hidpp_link_enabled = False

            self.is_open = False
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Channel already closed", trace_level=TraceLevel.DEBUG)
        # end if
    # end def close

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def mute(self):
        """
        Mute the through receiver channel.

        :raise ``ChannelException``: If the receiver channel is not open
        """
        if not self.receiver_channel.is_open:
            raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
        # end if

        if self.is_open:
            self.receiver_channel.mute()
        # end if
    # end def mute

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def unmute(self):
        """
        Unmute the through receiver channel.

        :raise ``ChannelException``: If the receiver channel is not open
        """
        if not self.receiver_channel.is_open:
            raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
        # end if

        if self.is_open:
            self.receiver_channel.unmute()
        # end if
    # end def unmute

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def update_callback(self, targeted_report_types, callback=None):
        # See ``BaseCommunicationChannel.update_callback``
        if not self.receiver_channel.is_open:
            raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
        # end if

        self.receiver_channel.update_callback(targeted_report_types=targeted_report_types, callback=callback)
    # end def update_callback

    def send_data(self, data, timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT):
        """
        Send data through the receiver channel. It should be a HID++ that have the device index field. This method
        will set this field to the correct one.

        :param data: Data to send
        :type data: ``TimestampedBitFieldContainerMixin`` or ``HexList`` or ``UsbMessage``
        :param timeout: The timeout of this action in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``

        :raise ``ChannelException``: If channel is not open, or if the device index of the
                                     message does not match the channel's device index
        :raise ``TypeError``: If the parameter ``data`` is not the right type
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self.hidpp_link_enabled:
            raise ChannelException(ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT)
        # end if

        if (isinstance(data, HexList) and len(data) not in HidppMessage.HIDPP_REPORT_LEN_LIST) or \
                (isinstance(data, UsbMessage) and len(data.data) not in HidppMessage.HIDPP_REPORT_LEN_LIST):
            raise ChannelException(ChannelException.Cause.WRONG_PARAMETER,
                                   f"Packet length: {len(data)}, it should be either 7, 20 or 64")
        # end if

        if isinstance(data, TimestampedBitFieldContainerMixin):
            data_device_index = to_int(data.deviceIndex)
        elif isinstance(data, HexList):
            data_device_index = data[HidppMessage.OFFSET.DEVICE_INDEX]
        elif isinstance(data, UsbMessage):
            data_device_index = data.data[HidppMessage.OFFSET.DEVICE_INDEX]
        else:
            raise TypeError(f"Parameter data should be HidppMessage or HexList, {data} is a {type(data)}")
        # end if

        if data_device_index != self.device_index:
            raise ChannelException(
                ChannelException.Cause.WRONG_PARAMETER, f"Wrong device index {data_device_index} in data")
        # end if

        if not isinstance(data, UsbMessage):
            # Create a USBMessage object
            usb_message = UsbMessage(message_class=type(data), data=HexList(data), timestamp=perf_counter_ns())
        else:
            usb_message = data
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Sending {usb_message}...", trace_level=TraceLevel.DEBUG)
        try:
            self.receiver_channel.send_data(data=usb_message, timeout=timeout)
        except ChannelException as e:
            if e.get_cause() == ChannelException.Cause.CHANNEL_NOT_OPEN:
                raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
            elif e.get_cause() == ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT:
                raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT)
            else:
                raise
            # end if
        # end try

        if isinstance(data, TimestampedBitFieldContainerMixin):
            data.timestamp = usb_message.timestamp
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {data}", trace_level=TraceLevel.INFO)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {usb_message}", trace_level=TraceLevel.INFO)
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
        :rtype: ``UsbMessage`` or ``TimestampedBitFieldContainerMixin``

        :raise ``ChannelException``: If channel is not open, HID++ link not present
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if dispatcher_queue is not None and raw_filters is not None:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"When dispatcher_queue is not None (right now it is {dispatcher_queue}), the raw_filters is "
                        f"also ignored (right now it is {raw_filters})",
                trace_level=TraceLevel.WARNING)
        elif dispatcher_queue is None and message_class is not None:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"When dispatcher_queue is None (right now it is None), the message_class is also ignored "
                        f"(right now it is {message_class})",
                trace_level=TraceLevel.WARNING)
        # end if

        if report_type != LogitechReportType.HIDPP:
            if dispatcher_queue is not None:
                dispatcher_queue = self.receiver_channel.hid_dispatcher.get_queue_by_name(name=dispatcher_queue.name)
            # end if
            try:
                message = self.receiver_channel.get_message(
                    report_type=report_type,
                    dispatcher_queue=dispatcher_queue,
                    raw_filters=raw_filters,
                    message_class=message_class,
                    timeout=timeout,
                    skip_error=skip_error)
            except ChannelException as e:
                if e.get_cause() == ChannelException.Cause.CHANNEL_NOT_OPEN:
                    raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
                elif e.get_cause() == ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT:
                    raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT)
                else:
                    raise
                # end if
            # end try
        else:
            if not self.hidpp_link_enabled:
                raise ChannelException(ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT)
            # end if

            message = self._common_get_message(
                report_type=report_type,
                time_stamped_msg_queue=self.hidpp_time_stamped_msg_queue,
                dispatcher_queue=dispatcher_queue,
                raw_filters=raw_filters,
                message_class=message_class,
                timeout=timeout,
                skip_error=skip_error)
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Received message {message}", trace_level=TraceLevel.INFO)

        return message
    # end def get_message

    def process_all_report_type_in_dispatcher(self, report_type=LogitechReportType.HIDPP):
        # See ``BaseCommunicationChannel.process_all_report_type_in_dispatcher``
        self.receiver_channel.process_all_report_type_in_dispatcher(report_type=report_type)
        if report_type == LogitechReportType.HIDPP:
            while not self.hidpp_time_stamped_msg_queue.event_empty.is_set():
                transport_message = self.hidpp_time_stamped_msg_queue.get_nowait()
                self._report_type_to_process_message_callback[report_type](transport_message=transport_message)
            # end while
        # end if
    # end def process_all_report_type_in_dispatcher

    def get_descriptors(self):
        # See ``BaseCommunicationChannel.get_descriptors``
        descriptor_messages = self.receiver_channel.get_descriptors()

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message="Associated receiver channel's descriptors gotten",
            trace_level=TraceLevel.INFO)

        return descriptor_messages
    # end def get_descriptors

    def get_interface_descriptor(self, interface):
        # See ``BaseCommunicationChannel.get_interface_descriptor``
        descriptor_message = self.receiver_channel.get_interface_descriptor(interface=interface)

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message="Associated receiver channel's descriptor gotten",
            trace_level=TraceLevel.INFO)

        return descriptor_message
    # end def get_interface_descriptor

    def get_transport_id(self, force_refresh_cache=False):
        # See ``BaseCommunicationChannel.get_transport_id``
        raise NotImplementedError("get_transport_id() method should be implemented by child class")
    # end def get_transport_id

    def is_device_connected(self, force_refresh_cache=False):
        """
        Check if the device is connected using fake arrival mechanism. If the device is not connected, the channel
        will be automatically closed. The channel does not need to be open to use this method. If the associated
        receiver channel is not open, it will open it and close it at the end. The result will be cached.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: Flag indicating if the device is connected or not
        :rtype: ``bool``

        :raise ``ChannelException``: If receiver channel is not open, HID++ link not present
        """
        if self.connected is None or force_refresh_cache:
            # Open the receiver channel if needed
            if not self.receiver_channel.is_open:
                self.receiver_channel.open(link_enabler=LinkEnablerInfo.HID_PP_MASK)
                close_receiver_channel = True
            else:
                close_receiver_channel = False
            # end if

            try:
                self.receiver_channel.process_all_report_type_in_dispatcher()

                self.receiver_channel.perform_fake_arrival()

                filters = [MessageFilter(index_in_message=Hidpp1Data.Offset.SUB_ID,
                                         value=Hidpp1Data.Hidpp1NotificationSubId.DEVICE_CONNECTION)]
                self.connected = False

                queue_to_use = self.receiver_channel.report_type_time_stamped_msg_queue[
                        LogitechReportType.HIDPP].queues[Hidpp1Data.DeviceIndex.TRANSCEIVER]

                while not queue_to_use.event_empty.is_set():
                    message = queue_to_use.get(timeout=.1)

                    if self._is_expected_message(message=message, filters=filters):
                        device_connection = DeviceConnection.fromHexList(HexList(message.data))
                        if to_int(device_connection.device_index) == self.device_index:
                            device_information = self.DEVICE_INFORMATION_CLASS.fromHexList(
                                HexList(device_connection.information))
                            self.connected = (to_int(device_information.device_info_link_status) ==
                                              DeviceConnection.LinkStatus.LINK_ESTABLISHED)
                            self.protocol = LogitechProtocol(to_int(device_connection.protocol_type))
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message=f"Received DeviceConnection ({message}) with device_info_link_status = "
                                        f"{self.connected}",
                                trace_level=TraceLevel.INFO)
                        else:
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message=f"Received message DeviceConnection from another device: {message}",
                                trace_level=TraceLevel.INFO)
                        # end if
                    else:
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Received message other than DeviceConnection: {message}",
                            trace_level=TraceLevel.INFO)
                    # end if
                # end while

                if not self.connected and self.is_open:
                    self.close()
                # end if
            except ChannelException as e:
                if e.get_cause() == ChannelException.Cause.CHANNEL_NOT_OPEN:
                    raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
                elif e.get_cause() == ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT:
                    raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT)
                else:
                    raise
                # end if
            finally:
                # Close the receiver channel if needed
                if close_receiver_channel:
                    self.receiver_channel.close()
                # end if
            # end try
        # end if

        return self.connected
    # end def is_device_connected

    def wait_device_connection_state(self, connected, timeout):
        # See ``BaseCommunicationChannel.wait_device_connection_state``
        raise RuntimeError("wait_device_connection_state() method is not implemented yet")
    # end def wait_device_connection_state

    def is_link_enabled(self, link_report_type):
        """
        Check if a link is enabled. It returns ``False`` if the channel is closed.

        :param link_report_type: Report type of the link to check.
        :type link_report_type: ``LogitechReportType``

        :return: Flag indicating if the link is enabled
        :rtype: ``bool``
        """
        if link_report_type != LogitechReportType.HIDPP:
            return self.is_open and self.receiver_channel.is_link_enabled(link_report_type=link_report_type)
        # end if

        return self.is_open and self.hidpp_time_stamped_msg_queue is not None
    # end def is_link_enabled

    def get_device_info(self, force_refresh_cache=False):
        """
        Getting device information by calling the receiver 0xB5 register. The result will be cached and returned next
        call to this method (except if ``force_refresh_cache`` is True). The channel does not need to be opened to
        use this method. If the associated receiver channel is not open, it will open it and close it at the end.
        The result will be cached.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: List of structure for device pairing information and device name
        :rtype: ``list[GetLongRegisterResponse]``

        :raise ``ChannelException``: If receiver channel is not open, HID++ link not present
        """
        if (self._device_information[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION] is None
                and self._device_information[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_NAME] is None) or \
                force_refresh_cache:
            # Open the receiver channel if needed
            if not self.receiver_channel.is_open:
                self.receiver_channel.open(link_enabler=LinkEnablerInfo.HID_PP_MASK)
                close_receiver_channel = True
            else:
                close_receiver_channel = False
            # end if

            previously_enabled = True
            try:
                # Get pairing information
                self._fill_in_device_info_by_r0(
                    r0=self.DEVICE_PAIRING_INFORMATION_MIN_R0 + self.device_index - 1,
                    index_in_cache=ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION)

                # Get device name
                self._fill_in_device_info_by_r0(
                    r0=self.DEVICE_NAME_MIN_R0 + self.device_index - 1,
                    index_in_cache=ThroughReceiverChannel.DeviceInformationOffset.DEVICE_NAME)
            except ChannelException as e:
                if e.get_cause() == ChannelException.Cause.CHANNEL_NOT_OPEN:
                    raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN)
                elif e.get_cause() == ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT:
                    raise ChannelException(ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT)
                else:
                    raise
                # end if
            finally:
                if not previously_enabled:
                    self.receiver_channel.enable_hidpp_reporting(enable=False)
                # end if

                # Close the receiver channel if needed
                if close_receiver_channel:
                    self.receiver_channel.close()
                # end if
            # end try
        # end if

        return self._device_information
    # end def get_device_info

    def get_channel_usb_port_path_list(self):
        """
        Wrapper method to get the associated receiver USB device port path as a list.

        :return: The port path to the device
        :rtype: ``list[int]``
        """
        return self.receiver_channel.get_channel_usb_port_path_list()
    # end def get_channel_usb_port_path_list

    def get_channel_usb_port_path_str(self):
        """
        Wrapper method to get the associated receiver USB device port path as a string.

        :return: The port path to the device
        :rtype: ``str``
        """
        return self.receiver_channel.get_channel_usb_port_path_str()
    # end def get_channel_usb_port_path_str

    def subscribe_to_receiver_multi_queue(self):
        """
        Subscribe this channel's HID++ queue to the receiver multi queue.
        """
        if not self.is_subscribed_to_receiver_multi_queue():
            self.hidpp_time_stamped_msg_queue = QueueWithFilter()
            multi_queue = self.receiver_channel.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP]
            multi_queue.add_device_index_queue(
                device_index=self.device_index, associated_queue=self.hidpp_time_stamped_msg_queue)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message="Already subscribed to the receiver multi queue",
                trace_level=TraceLevel.DEBUG)
        # end if
    # end def subscribe_to_receiver_multi_queue

    def unsubscribe_from_receiver_multi_queue(self):
        """
        Unsubscribe this channel's HID++ queue from the receiver multi queue.

        :raise ``ChannelException``: If the channel is open, it is impossible to unsubscribe
        """
        if self.is_subscribed_to_receiver_multi_queue():
            # Sanity check
            if self.is_open:
                raise ChannelException(
                    ChannelException.Cause.CONFIGURATION_ERROR,
                    "Channel should not be opened when unsubscribing from the receiver multi queue")
            # end if

            multi_queue = self.receiver_channel.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP]
            multi_queue.remove_device_index_queue(device_index=self.device_index)
            while not self.hidpp_time_stamped_msg_queue.event_empty.is_set():
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Untreated message in {LogitechReportType.HIDPP} queue: "
                            f"{self.hidpp_time_stamped_msg_queue.get()}",
                    trace_level=TraceLevel.WARNING)
            # end while
            self.hidpp_time_stamped_msg_queue = None
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message="Already unsubscribed from the receiver multi queue",
                trace_level=TraceLevel.DEBUG)
        # end if
    # end def unsubscribe_from_receiver_multi_queue

    def is_subscribed_to_receiver_multi_queue(self):
        """
        Indicate if the channel is subscribed to its receiver multi queue.

        :return: Flag indicating if the channel is subscribed to its receiver multi queue
        :rtype: ``bool``
        """
        multi_queue = self.receiver_channel.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP]
        return self.hidpp_time_stamped_msg_queue is not None and self.device_index in multi_queue.queues
    # end def is_subscribed_to_receiver_multi_queue

    def _fill_in_device_info_by_r0(self, r0, index_in_cache):
        """
        Fill in the device information variable with a specific device info using the r0 parameter.

        :param r0: r0 parameter of the HID++ request
        :type r0: ``int``
        :param index_in_cache: Index in the cache to put the result structure
        :type index_in_cache: ``ThroughReceiverChannel.DeviceInformationOffset``
        """
        get_info_class = NonVolatilePairingInformationModel.get_message_cls(
            sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER, message_type="request", r0=r0)
        get_info_response_class = NonVolatilePairingInformationModel.get_message_cls(
            sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER, message_type="response", r0=r0)

        get_info = get_info_class(r0=r0)
        filters = [MessageFilter(index_in_message=Hidpp1Data.Offset.SUB_ID, value=get_info.sub_id),
                   MessageFilter(index_in_message=Hidpp1Data.Offset.REGISTER_ADDRESS, value=get_info.address),
                   MessageFilter(index_in_message=Hidpp1Data.Offset.REGISTER_R0, value=r0)]
        get_info_response = self.receiver_channel.send_data_wait_response(data=get_info, raw_filters=filters)

        self._device_information[index_in_cache] = get_info_response_class.fromHexList(HexList(get_info_response.data))
    # end def _fill_in_device_info_by_r0
# end class ThroughReceiverChannel


class ThroughEQuadReceiverChannel(ThroughReceiverChannel):
    """
    Implementation of a communication channel through an eQuad receiver.
    """
    DEVICE_INFORMATION_CLASS = EQuadReceiverInformation
    DEVICE_PAIRING_INFORMATION_MIN_R0 = NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_PAIRING_INFO_MIN
    DEVICE_NAME_MIN_R0 = NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN

    def __init__(self, receiver_channel, device_index, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        # See ``ThroughReceiverChannel.__init__``
        super().__init__(receiver_channel=receiver_channel,
                         device_index=device_index,
                         trace_level=trace_level,
                         trace_file_name=trace_file_name)

        TRACE_LOGGER.update_trace_name(
            subscription_owner=self,
            trace_name=f"Channel through eQuad receiver ({self.receiver_channel.get_channel_usb_port_path_str()}) "
                       f"on device index {self.device_index}")
    # end def __init__

    def get_transport_id(self, force_refresh_cache=False):
        """
        Get the transport ID of the device, this mean eQuad PID for eQuad devices.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``
        """
        device_pairing_information = self.get_device_info(force_refresh_cache=force_refresh_cache)[
            ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION]

        return to_int(device_pairing_information.device_quid)
    # end def get_transport_id
# end class ThroughEQuadReceiverChannel


class ThroughBleProReceiverChannel(ThroughReceiverChannel):
    """
    Implementation of a communication channel through a BLE Pro receiver.
    """
    DEVICE_INFORMATION_CLASS = BLEProReceiverInformation
    DEVICE_PAIRING_INFORMATION_MIN_R0 = NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN
    DEVICE_NAME_MIN_R0 = NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN

    def __init__(self, receiver_channel, device_index, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        # See ``ThroughReceiverChannel.__init__``
        super().__init__(receiver_channel=receiver_channel,
                         device_index=device_index,
                         trace_level=trace_level,
                         trace_file_name=trace_file_name)

        TRACE_LOGGER.update_trace_name(
            subscription_owner=self,
            trace_name=f"Channel through BLE Pro receiver ({self.receiver_channel.get_channel_usb_port_path_str()}) "
                       f"on device index {self.device_index}")
    # end def __init__

    def get_transport_id(self, force_refresh_cache=False):
        """
        Get the transport ID of the device, this mean Bluetooth PID for BLE Pro devices.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: The transport ID
        :rtype: ``int``
        """
        device_pairing_information = self.get_device_info(force_refresh_cache=force_refresh_cache)[
            ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION]

        bluetooth_pid = to_int(device_pairing_information.bluetooth_pid)

        return ((bluetooth_pid & 0xFF00) >> 8) + ((bluetooth_pid & 0x00FF) << 8)
    # end def get_transport_id
# end class ThroughBleProReceiverChannel


class ThroughGotthardReceiverChannel(ThroughReceiverChannel):
    """
    Implementation of a communication channel through a Gotthard receiver.
    """
    DEVICE_INFORMATION_CLASS = None
    DEVICE_PAIRING_INFORMATION_MIN_R0 = None
    DEVICE_NAME_MIN_R0 = None

    def __init__(self, receiver_channel, device_index, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        # See ``ThroughReceiverChannel.__init__``
        super().__init__(receiver_channel=receiver_channel,
                         device_index=device_index,
                         trace_level=trace_level,
                         trace_file_name=trace_file_name)

        # By default, we consider the device connected
        self.connected = True
        self.protocol = LogitechProtocol.GOTTHARD
        self.subscribe_to_receiver_multi_queue()

        TRACE_LOGGER.update_trace_name(
            subscription_owner=self,
            trace_name=f"Channel through Gotthard receiver ({self.receiver_channel.get_channel_usb_port_path_str()}) "
                       f"on device index {self.device_index}")
    # end def __init__

    def __str__(self):
        return f"{self.__class__.__name__}(port: {self.get_channel_usb_port_path_str()}, " \
               f"device index: {self.device_index})"
    # end def __str__

    def get_transport_id(self, force_refresh_cache=False):
        # See ``ThroughReceiverChannel.get_transport_id``
        raise RuntimeError("Cannot get transport ID on a Gotthard receiver")
    # end def get_transport_id

    def get_device_info(self, force_refresh_cache=False):
        # See ``ThroughReceiverChannel.get_device_info``
        raise RuntimeError("Cannot get device info on a Gotthard receiver")
    # end def get_device_info

    def is_device_connected(self, force_refresh_cache=False):
        # See ``ThroughReceiverChannel.is_device_connected``
        return self.connected
    # end def is_device_connected
# end class ThroughGotthardReceiverChannel

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
