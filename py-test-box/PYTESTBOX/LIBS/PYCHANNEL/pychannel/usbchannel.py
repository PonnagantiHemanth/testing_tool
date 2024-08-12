#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pychannel.usbchannel
:brief: USB communication channel classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/08/06
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from queue import Empty
from time import perf_counter_ns
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.channelinterfaceclasses import MessageFilter
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.hiddispatcher import HidMessageQueue
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingRequest
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingResponse
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import SetEnableHidppReportingRequest
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.tools.hidppthreadutils import ReceiverMultiHidppQueue
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueWithFilter
from pylibrary.tools.threadutils import RLockedDict
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pytransport.usb.usbconstants import EndpointDirection
from pytransport.usb.usbconstants import HidClassSpecificRequest
from pytransport.usb.usbconstants import RequestType
from pytransport.usb.usbcontext import UsbContext
from pytransport.usb.usbcontext import UsbContextDevice
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
FORCE_AT_CREATION_ALL_USB_CHANNEL_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_USB_CHANNEL_TRACE_FILE_NAME = None


class LogitechReportId(IntEnum):
    """
    USB Protocol descriptor
    """
    REPORT_ID_SHORT_MESSAGE = 0x10
    REPORT_ID_LONG_MESSAGE = 0x11
    REPORT_ID_VERY_LONG_MESSAGE = 0x12
    REPORT_ID_NORMAL_VLP_MESSAGE = 0x13
    REPORT_ID_EXTENDED_VLP_MESSAGE = 0x14
# end class LogitechReportId


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class UsbChannel(BaseCommunicationChannel):
    """
    Implementation of a USB communication channel.
    """
    HIDPP_QUEUE_TYPE = QueueWithFilter

    def __init__(self, usb_context, usb_context_device, trace_level=TraceLevel.NO_TRACE,
                 trace_file_name=None):
        """
        :param usb_context: USB context to use for this channel
        :type usb_context: ``UsbContext``
        :param usb_context_device: USB context device to use for this channel
        :type usb_context_device: ``UsbContextDevice``
        :param trace_level: Trace level of the channel - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the channel - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        """
        if FORCE_AT_CREATION_ALL_USB_CHANNEL_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_USB_CHANNEL_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_USB_CHANNEL_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_USB_CHANNEL_TRACE_FILE_NAME
        # end if

        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        self._usb_context = usb_context
        self._usb_context_device = usb_context_device
        self.report_type_to_interface = {}
        self.report_type_to_endpoint = {}
        self.report_type_time_stamped_msg_queue = {}
        self.protocol = LogitechProtocol.USB
        self.interrupt_out_endpoint = None
        self.send_data = self.send_data_control_write

        for report_type in LogitechReportType:
            if report_type == LogitechReportType.HIDPP:
                queue_type = self.HIDPP_QUEUE_TYPE
            else:
                queue_type = QueueWithFilter
            # end if

            self.report_type_time_stamped_msg_queue[report_type] = queue_type()
        # end for

        TRACE_LOGGER.update_trace_name(
            subscription_owner=self,
            trace_name=f"USB Channel on {self._usb_context_device.get_basic_reader_name()} "
                       f"{self._usb_context_device.vid:04X}:{self._usb_context_device.pid:04X}")
    # end def __init__

    def __str__(self):
        return f"{self.__class__.__name__}(port: {self.get_channel_usb_port_path_str()}, " \
               f"VID: {self._usb_context_device.vid:04X}, PID: {self._usb_context_device.pid:04X})"
    # end def __str__

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self, link_enabler=LinkEnablerInfo.ALL_MASK):
        """
        Open the channel.

        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo`` - OPTIONAL
        :type link_enabler: ``int`` or ``BitStruct``

        :raise ``ChannelException``: If the hardware device is off or if the USB device is not connected
        """
        if not self.is_open:
            if not self._is_hardware_device_on():
                raise ChannelException(ChannelException.Cause.HARDWARE_DEVICE_OFF)
            # end if

            if not self.is_device_connected(
                    force_refresh_cache=not self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY):
                raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
            # end if

            if isinstance(link_enabler, int):
                link_enabler = BitStruct(HexList(Numeral(link_enabler, 2)))
            # end if

            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Opening (link enable = {link_enabler})...",
                trace_level=TraceLevel.DEBUG)

            self._usb_context.open_device(usb_context_device=self._usb_context_device)

            try:
                for interface_id, protocol, endpoints in self._usb_context_device.interface_list:
                    for ep_id, size in endpoints:
                        if (ep_id & EndpointDirection.IN) != EndpointDirection.IN:
                            # See https://www.usb.org/sites/default/files/hid1_11.pdf :
                            # Device Class Definition for Human Interface Devices (HID)
                            # 4.4
                            # "The Interrupt Out pipe is optional. If a device declares an Interrupt Out endpoint then
                            # Output reports are transmitted by the host to the device through the Interrupt Out
                            # endpoint. If no Interrupt Out endpoint is declared then Output reports are transmitted to
                            # a device through the Control endpoint, using Set_Report(Output) requests."
                            self.interrupt_out_endpoint = ep_id
                            self.send_data = self.send_data_interrupt_write
                            # Assign interrupt polling only to IN endpoint
                            continue
                        # end if
                        # The link enabler is only used to put the time stamped message queue or not, the polling has to
                        # be started to avoid problems in the sending queues on the device part
                        if protocol == LogitechReportType.HIDPP:
                            # HID++ Interface
                            self._start_interrupt_polling_on_interface(
                                link_enabler=link_enabler,
                                link_enabler_info_position=LinkEnablerInfo.HID_PP_POSITION,
                                report_type=LogitechReportType.HIDPP,
                                interface_id=interface_id,
                                ep_id=ep_id,
                                size=size,
                                trace_name="HID++ polling",
                                discard_report=link_enabler.testBit(LinkEnablerInfo.DISABLE_HID_PP_CB_POSITION) == 1)
                        elif protocol == LogitechReportType.MOUSE:
                            # Mouse Interface
                            self._start_interrupt_polling_on_interface(
                                link_enabler=link_enabler,
                                link_enabler_info_position=LinkEnablerInfo.MOUSE_POSITION,
                                report_type=LogitechReportType.MOUSE,
                                interface_id=interface_id,
                                ep_id=ep_id,
                                size=size,
                                trace_name="HID Mouse polling",
                                discard_report=link_enabler.testBit(LinkEnablerInfo.DISABLE_MOUSE_CB_POSITION) == 1)
                        elif protocol == LogitechReportType.KEYBOARD:
                            # Keyboard Interface
                            self._start_interrupt_polling_on_interface(
                                link_enabler=link_enabler,
                                link_enabler_info_position=LinkEnablerInfo.KEYBOARD_POSITION,
                                report_type=LogitechReportType.KEYBOARD,
                                interface_id=interface_id,
                                ep_id=ep_id,
                                size=size,
                                trace_name="HID Keyboard polling",
                                discard_report=link_enabler.testBit(LinkEnablerInfo.DISABLE_KEYBOARD_CB_POSITION) == 1)
                        elif protocol == LogitechReportType.DIGITIZER:
                            # Digitizer interface
                            self._start_interrupt_polling_on_interface(
                                link_enabler=link_enabler,
                                link_enabler_info_position=LinkEnablerInfo.DIGITIZER_POSITION,
                                report_type=LogitechReportType.DIGITIZER,
                                interface_id=interface_id,
                                ep_id=ep_id,
                                size=size,
                                trace_name="HID Digitizer polling",
                                discard_report=link_enabler.testBit(LinkEnablerInfo.DISABLE_DIGITIZER_CB_POSITION) == 1)
                        # end if
                    # end for
                # end for
            except Exception:
                # This try catch is to cleanly close the device if anything went wrong, therefore we do not specify
                # which exception because it does not matter.
                try:
                    self._usb_context.close_device(usb_context_device=self._usb_context_device)
                except Exception:
                    # This try catch is to cleanly close all threads if anything went wrong, therefore we do not specify
                    # which exception because it does not matter.
                    self._usb_context.stop_interrupt_read_polling(usb_context_device=self._usb_context_device)
                    raise
                # end try
                raise
            # end try
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

            if not self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
                self._usb_context.update_device_list()
            # end if

            if self._usb_context_device.connected:
                # noinspection PyBroadException
                try:
                    self._usb_context.stop_interrupt_read_polling(usb_context_device=self._usb_context_device)
                    self._usb_context.close_device(usb_context_device=self._usb_context_device)
                except Exception:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Could not stop context device: {TracebackLogWrapper.get_exception_stack()}",
                        trace_level=TraceLevel.ERROR)
                # end try
            # end if

            for report_type in self.report_type_time_stamped_msg_queue:
                receiver_queue = self.report_type_time_stamped_msg_queue[report_type]
                if isinstance(receiver_queue, ReceiverMultiHidppQueue):
                    receiver_queue = receiver_queue.queues[Hidpp1Data.DeviceIndex.TRANSCEIVER]
                # end if

                while not receiver_queue.event_empty.is_set():
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Untreated message in {report_type} timestamped queue: "
                                f"{receiver_queue.get_nowait()}",
                        trace_level=TraceLevel.WARNING)
                # end while
            # end for
            self.report_type_to_interface.clear()
            untreated_messages = self.hid_dispatcher.clear_all_queues()
            for untreated_message in untreated_messages:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Untreated message in HID dispatcher: {untreated_message}",
                    trace_level=TraceLevel.WARNING)
            # end for
            self.is_open = False
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Channel already closed", trace_level=TraceLevel.DEBUG)
        # end if
    # end def close

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def mute(self):
        """
        Mute the USB channel i.e. the transfer queue is unchecked.
        """
        if self.is_open:
            for interface_id, protocol, endpoints in self._usb_context_device.interface_list:
                for ep_id, size in endpoints:
                    self._usb_context.mute_interrupt_read_polling(
                        usb_context_device=self._usb_context_device, endpoint=ep_id)
                # end for
            # end for
        # end if
    # end def mute

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def unmute(self):
        """
        Unmute the USB channel.
        """
        if self.is_open:
            for interface_id, protocol, endpoints in self._usb_context_device.interface_list:
                for ep_id, size in endpoints:
                    self._usb_context.unmute_interrupt_read_polling(
                        usb_context_device=self._usb_context_device, endpoint=ep_id)
                # end for
            # end for
        # end if
    # end def unmute

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def update_callback(self, targeted_report_types, callback=None):
        # See ``BaseCommunicationChannel.update_callback``
        if self.is_open:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Updating callbacks...", trace_level=TraceLevel.DEBUG)

            if not self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
                self._usb_context.update_device_list()
            # end if

            if self._usb_context_device.connected:
                targeted_report_types_left = targeted_report_types.copy()
                for targeted_report_type in targeted_report_types:
                    targeted_endpoint = self.report_type_to_endpoint.get(targeted_report_type, None)
                    if targeted_endpoint is None:
                        continue
                    else:
                        targeted_report_types_left.remove(targeted_report_type)
                    # end if
                    self._usb_context_device.set_transfer_callback(
                        transfer_type_key=targeted_endpoint, callback=callback)
                # end for
                if len(targeted_report_types_left) > 0:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Targeted report types {targeted_report_types_left} "
                                                         "not in the DUT open links",
                        trace_level=TraceLevel.DEBUG)
                # end if

                TRACE_LOGGER.log_trace(
                    subscription_owner=self, message="Callbacks updated", trace_level=TraceLevel.DEBUG)
            else:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self, message="UsbChannel.update_callback skipped: Device not connected",
                    trace_level=TraceLevel.DEBUG)
            # end if
        else:
            TRACE_LOGGER.log_trace(
                    subscription_owner=self, message="UsbChannel.update_callback skipped: Channel closed",
                    trace_level=TraceLevel.DEBUG)
        # end if
    # end def update_callback

    def send_data_control_write(self, data, timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT):
        """
        Send data through the channel, using Control Endpoint

        :param data: Data to send
        :type data: ``TimestampedBitFieldContainerMixin`` or ``HexList`` or ``UsbMessage``
        :param timeout: The timeout of this action in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``

        :raise ``ChannelException``: If channel is not open, HID++ link not present, not all bytes are sent or if the
                                     USB device is not connected
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self.is_device_connected(
                force_refresh_cache=not self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY):
            raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        if LogitechReportType.HIDPP not in self.report_type_to_interface:
            raise ChannelException(
                ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT, f"Report type = {LogitechReportType.HIDPP}")
        # end if

        if not isinstance(data, UsbMessage):
            # Create a USBMessage object
            usb_message = UsbMessage(message_class=type(data), data=HexList(data), timestamp=perf_counter_ns())
        else:
            usb_message = data
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Sending {usb_message}...", trace_level=TraceLevel.DEBUG)

        # Setup request
        # bRequest:                   SET_REPORT
        # bmRequestType.Recipient:    Interface
        # bmRequestType.Type:         Class
        # bmRequestType.Direction:    Host-to-device
        request_type = RequestType.TransferDirection.HOST_TO_DEVICE << RequestType.TRANSFER_DIRECTION_BITWISE_LEFT_SHIFT
        request_type |= RequestType.Type.CLASS << RequestType.TYPE_BITWISE_LEFT_SHIFT
        request_type |= RequestType.Recipient.INTERFACE
        # Compute reportId value
        if len(usb_message.data) == 0:
            raise ChannelException(ChannelException.Cause.WRONG_PARAMETER, "No data in USB message")
        # end if
        report_id = usb_message.data[0]
        report_sizes = {
            LogitechReportId.REPORT_ID_SHORT_MESSAGE: HidppMessage.SHORT_MSG_SIZE,
            LogitechReportId.REPORT_ID_LONG_MESSAGE: HidppMessage.LONG_MSG_SIZE,
            LogitechReportId.REPORT_ID_VERY_LONG_MESSAGE: HidppMessage.VERY_LONG_MSG_SIZE
        }
        # Check report size for HID++, but not for VLP as size may vary
        if report_id in report_sizes and len(usb_message.data) != report_sizes[report_id]:
            raise ChannelException(
                ChannelException.Cause.WRONG_PARAMETER,
                f"Packet length {len(usb_message.data)} should be {report_sizes[report_id]} for report id {report_id}")
        # end if

        # wValue:                     Output Report x
        w_value = 0x200 | report_id  # hid report, report ID x
        # wIndex:                     Interface 0, 1 or 2
        # wLength:                    len(data)

        bytes_sent = self._usb_context.control_write(usb_context_device=self._usb_context_device,
                                                     bm_request_type=request_type,
                                                     b_request=HidClassSpecificRequest.SET_REPORT,
                                                     w_value=w_value,
                                                     w_index=self.report_type_to_interface[LogitechReportType.HIDPP],
                                                     data=usb_message,
                                                     timeout=timeout)
        usb_message.timestamp = perf_counter_ns()

        if bytes_sent != len(data):
            raise ChannelException(ChannelException.Cause.ERROR_BYTES_ARE_SENT,
                                   f"Sent {bytes_sent} bytes when expecting {len(data)}")
        # end if

        if isinstance(data, TimestampedBitFieldContainerMixin):
            data.timestamp = usb_message.timestamp
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {data}", trace_level=TraceLevel.INFO)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {usb_message}", trace_level=TraceLevel.INFO)
        # end if
    # end def send_data_control_write

    def send_data_interrupt_write(self, data, timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT):
        """
        Send data through the channel, using Out Endpoint

        :param data: Data to send
        :type data: ``TimestampedBitFieldContainerMixin`` or ``HexList`` or ``UsbMessage``
        :param timeout: The timeout of this action in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``

        :raise ``ChannelException``: If channel is not open, HID++ link not present, not all bytes are sent or if the
                                     USB device is not connected
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self.is_device_connected(
                force_refresh_cache=not self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY):
            raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        if LogitechReportType.HIDPP not in self.report_type_to_interface:
            raise ChannelException(
                ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT, f"Report type = {LogitechReportType.HIDPP}")
        # end if

        if self.interrupt_out_endpoint is None:
            raise ChannelException(
                ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT, "No interrupt OUT endpoint")
        # end if

        if not isinstance(data, UsbMessage):
            # Create a USBMessage object
            usb_message = UsbMessage(message_class=type(data), data=HexList(data), timestamp=perf_counter_ns())
        else:
            usb_message = data
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Sending {usb_message}...", trace_level=TraceLevel.DEBUG)

        bytes_sent = self._usb_context.interrupt_write(
            usb_context_device=self._usb_context_device,
            data=usb_message,
            endpoint=self.interrupt_out_endpoint,
            timeout=timeout
        )

        usb_message.timestamp = perf_counter_ns()

        if bytes_sent != len(data):
            raise ChannelException(ChannelException.Cause.ERROR_BYTES_ARE_SENT,
                                   f"Sent {bytes_sent} bytes when expecting {len(data)}")
        # end if

        if isinstance(data, TimestampedBitFieldContainerMixin):
            data.timestamp = usb_message.timestamp
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {data}", trace_level=TraceLevel.INFO)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Message sent {usb_message}", trace_level=TraceLevel.INFO)
        # end if
    # end def send_data_interrupt_write

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
        :type dispatcher_queue: ``HidMessageQueue`` or ``None``
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

        :raise ``ChannelException``: If channel is not open, HID++ link not present, a part of the code should
                                     not have been reached with no message found or if the USB device is not connected
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if report_type not in self.report_type_to_interface:
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
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self.is_device_connected(
                force_refresh_cache=not self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY):
            raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        self._usb_context.get_descriptor(
            usb_context_device=self._usb_context_device,
            recipient=RequestType.Recipient.DEVICE,
            descriptor_type=0x02,
            descriptor_index=0x00,
            descriptor_size=0x54)

        # Call self.hid_dispatcher.process_control_read_get_descriptor only when recipient is an ood number
        # RequestType.Recipient.DEVICE = 0 is not, so it should not be called

        # Interface descriptor
        descriptor_messages = []
        for interface, _, _ in self._usb_context_device.interface_list:
            descriptor_messages.append(self.get_interface_descriptor(interface=interface))
        # end for

        TRACE_LOGGER.log_trace(subscription_owner=self, message="Descriptors gotten", trace_level=TraceLevel.INFO)

        return descriptor_messages
    # end def get_descriptors

    def get_interface_descriptor(self, interface):
        # See ``BaseCommunicationChannel.get_interface_descriptor``
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if not self.is_device_connected(
                force_refresh_cache=not self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY):
            raise ChannelException(ChannelException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        descriptor_message = None
        # Interface descriptor
        descriptor = self._usb_context.get_descriptor(
            usb_context_device=self._usb_context_device,
            recipient=RequestType.Recipient.INTERFACE,
            descriptor_type=0x22,
            descriptor_index=0x00,
            descriptor_size=0x1FF,
            w_index=interface)
        # Call self.hid_dispatcher.process_control_read_get_descriptor only when recipient is an ood number
        # RequestType.Recipient.INTERFACE = 1 is not, so it should not be called
        self.hid_dispatcher.process_control_read_get_descriptor(transport_message=descriptor)
        try:
            descriptor_message = self.hid_dispatcher.interface_descriptor_queue.get(timeout=.01)
        except Empty:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="A descriptor is missing", trace_level=TraceLevel.WARNING)
        # end try

        TRACE_LOGGER.log_trace(subscription_owner=self, message="Descriptor gotten", trace_level=TraceLevel.INFO)

        return descriptor_message
    # end def get_interface_descriptor

    def get_transport_id(self, force_refresh_cache=False):
        """
        Get the transport ID of the device, this mean PID for USB devices.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: The transport ID
        :rtype: ``int``
        """
        if force_refresh_cache:
            self._usb_context.update_device_list()
        # end if

        return self._usb_context_device.pid
    # end def get_transport_id

    def is_device_connected(self, force_refresh_cache=False):
        """
        Check if the USB device is connected. If the device is not connected, the channel will be automatically closed.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        if force_refresh_cache:
            self._usb_context.update_device_list()
        # end if

        connected = self._usb_context_device.connected

        if not connected and self.is_open:
            self.close()
        # end if

        return connected
    # end def is_device_connected

    def wait_device_connection_state(self, connected, timeout):
        # See ``BaseCommunicationChannel.wait_device_connection_state``
        if self._usb_context.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
            event_to_use = self._usb_context_device.wait_for_connection_event if connected \
                else self._usb_context_device.wait_for_disconnection_event

            event_to_use.clear()
            try:
                if self.is_device_connected() is not connected:
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

            # A delay is added because it seems that libusb give the information that the device is connected but
            # its structure in libusb does not seem to be complete. This is an empirical value, it is not standard.
            # As libusb does not have hotplug currently activated, this sleep is added based on the
            # ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY value of the USB context used
            sleep(.5)
            return self.is_device_connected(force_refresh_cache=True) is connected
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
        return self.is_open and link_report_type not in self.report_type_to_interface
    # end def is_link_enabled

    def get_channel_usb_port_path_list(self):
        """
        Wrapper method to get the USB device port path as a list.

        :return: The port path to the device
        :rtype: ``list[int]``
        """
        return self._usb_context_device.get_usb_port_path()
    # end def get_channel_usb_port_path_list

    def get_channel_usb_port_path_str(self):
        """
        Wrapper method to get the USB device port path as a string.

        :return: The port path to the device
        :rtype: ``str``
        """
        return self._usb_context_device.get_basic_reader_name()
    # end def get_channel_usb_port_path_str

    def get_usb_vid(self):
        """
        Wrapper method to get the USB VID.

        :return: The device VID
        :rtype: ``int``
        """
        return self._usb_context_device.vid
    # end def get_usb_vid

    def get_usb_pid(self):
        """
        Wrapper method to get the USB PID.

        :return: The device PID
        :rtype: ``int``
        """
        return self._usb_context_device.pid
    # end def get_usb_pid

    def get_manufacturer_string(self):
        """
        Get USB Manufacturer String

        :return: USB Manufacturer String
        :rtype: ``str``
        """
        return self._usb_context_device.get_manufacturer_string()
    # end def get_manufacturer_string

    def get_product_string(self):
        """
        Get USB Product String

        :return: USB Product String
        :rtype: ``str``
        """
        return self._usb_context_device.get_product_string()
    # end def get_product_string

    def get_device_address(self):
        # See ``UsbContextDevice.get_device_address``
        return self._usb_context_device.get_device_address()
    # end def get_device_address

    def hid_class_specific_request(
            self,
            interface_id,
            b_request=HidClassSpecificRequest.SET_IDLE,
            w_value=0,
            data=UsbMessage(data=HexList()),
            w_length=0,
            timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT,
            blocking=False):
        """
        Wrapper method to performs a HID class specific request on a USB device.

        :param interface_id: Number of the interface that supports this request
        :type interface_id: ``int``
        :param b_request: Request to perform, values can be found in ``HidClassSpecificRequest`` - OPTIONAL
        :type b_request: ``int``
        :param w_value: The meaning of this parameter is request type dependent - OPTIONAL
        :type w_value: ``int``
        :param data: Data to write if a SET request is used - OPTIONAL
        :type data: ``UsbMessage``
        :param w_length: Length of the buffer to receive data if a GET request is used - OPTIONAL
        :type w_length: ``int``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``float``
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``

        :return: Either the data received if it is a GET request or the length of data sent if it is a SET request
        :rtype: ``UsbMessage`` or ``int``
        """
        return self._usb_context.hid_class_specific_request(
            usb_context_device=self._usb_context_device,
            interface_id=interface_id,
            b_request=b_request,
            w_value=w_value,
            data=data,
            w_length=w_length,
            timeout=timeout,
            blocking=blocking)
    # end def hid_class_specific_request

    def _start_interrupt_polling_on_interface(
            self,
            link_enabler,
            link_enabler_info_position,
            report_type,
            interface_id,
            ep_id,
            size,
            trace_name,
            discard_report=False):
        """
        Internal method to use to start a polling on an interface with or without a time stamped message queue
        depending on the link enabler.

        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo``
        :type link_enabler: ``BitStruct``
        :param link_enabler_info_position: The position to test in the parameter ``link_enabler``, values can be
                                           found in ``LinkEnablerInfo``
        :type link_enabler_info_position: ``int``
        :param report_type: The associated report type
        :type report_type: ``LogitechReportType``
        :param interface_id: The interface ID
        :type interface_id: ``int``
        :param ep_id: The end point ID
        :type ep_id: ``int``
        :param size: The maximum length of the end point interface
        :type size: ``int``
        :param trace_name: Trace name of the polling actions
        :type trace_name: ``str``
        :param discard_report: Flag indicating to discard any message received on this endpoint - OPTIONAL
        :type discard_report: ``bool``
        """
        if link_enabler.testBit(link_enabler_info_position):
            self.report_type_to_interface[report_type] = interface_id
            self.report_type_to_endpoint[report_type] = ep_id
            msg_queue = self.report_type_time_stamped_msg_queue[report_type]
        else:
            msg_queue = None
        # end if
        self._usb_context.start_interrupt_read_polling(
            usb_context_device=self._usb_context_device,
            endpoint=ep_id,
            w_length=size,
            time_stamped_msg_queue=msg_queue,
            trace_name=trace_name,
            discard_report=discard_report)
        # end if
    # end def _start_interrupt_polling_on_interface
# end class UsbChannel


class UsbReceiverChannel(UsbChannel):
    """
    Implementation of a USB communication channel representing a receiver. This type of channel has associated channels
    that depend on it to be open.
    """
    HIDPP_QUEUE_TYPE = ReceiverMultiHidppQueue
    SUPERVISION_TIMEOUT = 3.5  # In seconds

    def __init__(self, max_number_of_paired_devices, usb_context, usb_context_device, trace_level=TraceLevel.NO_TRACE,
                 trace_file_name=None):
        """
        :param max_number_of_paired_devices: Maximum number of device paired to this receiver, it has to be more than 0
        :type max_number_of_paired_devices: ``int``
        :param usb_context: USB context to use for this channel
        :type usb_context: ``UsbContext``
        :param usb_context_device: USB context device to use for this channel
        :type usb_context_device: ``UsbContextDevice``
        :param trace_level: Trace level of the channel - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the channel - OPTIONAL
        :type trace_file_name: ``str`` or ``None``

        :raise ``ChannelException``: If ``max_number_of_paired_devices`` is less or equal to 0
        """
        super().__init__(usb_context=usb_context,
                         usb_context_device=usb_context_device,
                         trace_level=trace_level,
                         trace_file_name=trace_file_name)

        if max_number_of_paired_devices <= 0:
            raise ChannelException(
                ChannelException.Cause.WRONG_PARAMETER,
                f"Wrong max_number_of_paired_devices ({max_number_of_paired_devices}), should be more than 0")
        # end if

        # The associated channels are weak reference to avoid deadlock
        self.associated_channels_weak_ref = RLockedDict()
        self._max_number_of_paired_devices = max_number_of_paired_devices

        TRACE_LOGGER.update_trace_name(
            subscription_owner=self,
            trace_name=f"Receiver Channel on {self._usb_context_device.get_basic_reader_name()} "
                       f"{self._usb_context_device.vid:04X}:{self._usb_context_device.pid:04X}")
    # end def __init__

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See ``UsbChannel.close``
        if self.is_open:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Closing all associated channels...", trace_level=TraceLevel.DEBUG)

            counter = 0
            with self.associated_channels_weak_ref:
                while len(self.associated_channels_weak_ref) > 0 and counter <= self._max_number_of_paired_devices:
                    device_index = next(iter(self.associated_channels_weak_ref))
                    channel_to_close = self.associated_channels_weak_ref.pop(device_index)()
                    if channel_to_close is None:
                        # This associated channel does not exist anymore, every data for it in this structure
                        # should be cleared
                        # Noqa is used because an element in a dictionary is too vague for the indexer to know that
                        # is has attributes named queues and remove_device_index_queue
                        if device_index in \
                                self.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP].queues:  # noqa
                            queue = \
                                self.report_type_time_stamped_msg_queue[  # noqa
                                    LogitechReportType.HIDPP].remove_device_index_queue(device_index=device_index)
                            while not queue.empty():
                                TRACE_LOGGER.log_trace(
                                    subscription_owner=self,
                                    message=f"Untreated message in device index {device_index} "
                                            f"queue: {queue.get_nowait()}",
                                    trace_level=TraceLevel.WARNING)
                            # end while
                        # end if
                    else:
                        channel_to_close.close()
                    # end if
                    counter += 1
                # end while
            # end with

            assert counter < self._max_number_of_paired_devices, \
                "Something wrong happened while closing associated channels, " \
                "tried to close more than the maximum number of channels"

            super().close()
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="Channel already closed", trace_level=TraceLevel.DEBUG)
        # end if
    # end def close

    def get_message(
            self,
            report_type=LogitechReportType.HIDPP,
            dispatcher_queue=None,
            raw_filters=None,
            message_class=None,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            skip_error=False):
        # See ``UsbChannel.get_message``
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if report_type not in self.report_type_to_interface:
            raise ChannelException(ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT, f"Report type = {report_type}")
        # end if

        if report_type == LogitechReportType.HIDPP:
            # Noqa is used because an element in a dictionary is too vague for the indexer to know that is has
            # an attribute named queues
            receiver_queue = self.report_type_time_stamped_msg_queue[report_type].queues[  # noqa
                Hidpp1Data.DeviceIndex.TRANSCEIVER]
        else:
            receiver_queue = self.report_type_time_stamped_msg_queue[report_type]
        # end if

        message = self._common_get_message(
            report_type=report_type,
            time_stamped_msg_queue=receiver_queue,
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
        # See ``UsbChannel.process_all_report_type_in_dispatcher``
        if report_type not in self.report_type_time_stamped_msg_queue:
            return
        # end if

        if report_type == LogitechReportType.HIDPP:
            # Noqa is used because an element in a dictionary is too vague for the indexer to know that is has
            # an attribute named queues
            receiver_queue = self.report_type_time_stamped_msg_queue[report_type].queues[  # noqa
                Hidpp1Data.DeviceIndex.TRANSCEIVER]
        else:
            receiver_queue = self.report_type_time_stamped_msg_queue[report_type]
        # end if
        while not receiver_queue.event_empty.is_set():
            transport_message = receiver_queue.get_nowait()
            self._report_type_to_process_message_callback[report_type](transport_message=transport_message)
        # end while
    # end def process_all_report_type_in_dispatcher

    def enable_hidpp_reporting(self, enable):
        """
        Enable the HID++ reporting flag of the receiver.

        :param enable: Flag indication the enable status the HID++ reporting
        :type enable: ``bool``

        :return: Previous reporting flag state
        :rtype: ``bool``

        :raise ``ChannelException``: If channel is not open, HID++ link not present or not all bytes are sent
        """
        # Sanity check
        if not self.is_open:
            raise ChannelException(ChannelException.Cause.CHANNEL_NOT_OPEN)
        # end if

        if LogitechReportType.HIDPP not in self.report_type_to_interface:
            raise ChannelException(
                ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT, f"Report type = {LogitechReportType.HIDPP}")
        # end if

        get_register = GetEnableHidppReportingRequest()
        filters = [MessageFilter(index_in_message=Hidpp1Data.Offset.SUB_ID, value=get_register.sub_id),
                   MessageFilter(index_in_message=Hidpp1Data.Offset.REGISTER_ADDRESS, value=get_register.address)]
        response = self.send_data_wait_response(data=get_register, raw_filters=filters)
        get_register_response = GetEnableHidppReportingResponse.fromHexList(HexList(response.data))

        if int(enable) != get_register_response.receiver_reporting_flag_wireless_notifications:
            set_register = SetEnableHidppReportingRequest(receiver_reporting_flag_wireless_notifications=int(enable))
            filters = [MessageFilter(index_in_message=Hidpp1Data.Offset.SUB_ID, value=set_register.sub_id),
                       MessageFilter(index_in_message=Hidpp1Data.Offset.REGISTER_ADDRESS, value=set_register.address)]
            self.send_data_wait_response(data=set_register, raw_filters=filters)

            return not enable
        # end if

        return enable
    # end def enable_hidpp_reporting

    def perform_fake_arrival(self):
        """
        Perform a fake arrival on the receiver.
        """
        previously_enabled = self.enable_hidpp_reporting(enable=True)
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        filters = [MessageFilter(index_in_message=Hidpp1Data.Offset.SUB_ID, value=set_register.sub_id),
                   MessageFilter(index_in_message=Hidpp1Data.Offset.REGISTER_ADDRESS, value=set_register.address)]
        self.send_data_wait_response(data=set_register, raw_filters=filters)

        if not previously_enabled:
            self.enable_hidpp_reporting(enable=False)
        # end if
    # end def perform_fake_arrival
# end class UsbReceiverChannel


class GotthardReceiverChannel(UsbReceiverChannel):
    """
    Implementation of a USB communication channel representing a Gotthard receiver. This type of channel has
    associated channels that depend on it to be open. It is the same as ``UsbReceiverChannel`` but deactivating the
    method ``perform_fake_arrival`` that cannot be used for that kind of receiver.
    """

    def __init__(self, max_number_of_paired_devices, usb_context, usb_context_device, trace_level=TraceLevel.NO_TRACE,
                 trace_file_name=None):
        # See ``UsbReceiverChannel.__init__``
        super().__init__(
            max_number_of_paired_devices=max_number_of_paired_devices,
            usb_context=usb_context,
            usb_context_device=usb_context_device,
            trace_level=trace_level,
            trace_file_name=trace_file_name)

        TRACE_LOGGER.update_trace_name(
            subscription_owner=self,
            trace_name=f"Gotthard Receiver Channel on {self._usb_context_device.get_basic_reader_name()} "
                       f"{self._usb_context_device.vid:04X}:{self._usb_context_device.pid:04X}")
    # end def __init__

    def perform_fake_arrival(self):
        # See ``UsbReceiverChannel.perform_fake_arrival``
        raise RuntimeError("Cannot perform fake arrival on a Gotthard receiver")
    # end def perform_fake_arrival
# end class GotthardReceiverChannel

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
