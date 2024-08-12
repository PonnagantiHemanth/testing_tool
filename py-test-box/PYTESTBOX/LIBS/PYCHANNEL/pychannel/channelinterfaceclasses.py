#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pychannel.channelinterfaceclasses
:brief: Communication channel interface classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/08/03
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from queue import Empty
from threading import RLock
from time import sleep, time

from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.hid.interfacedescriptors import ReportDescriptor
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hiddispatcher import HidMessageQueue
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueWithFilter
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.util import ContainsIntEnumMeta
from pylibrary.tools.util import NotImplementedAbstractMethodError
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
FORCE_AT_CREATION_ALL_CHANNEL_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_CHANNEL_TRACE_FILE_NAME = None


class LogitechReportType(IntEnum):
    """
    Logitech report types
    """
    HIDPP = 0
    KEYBOARD = 1
    MOUSE = 2
    DIGITIZER = 3
# end class LogitechReportType


class LinkEnablerInfo:
    """
    Link enabler information
    """
    # Position
    HID_PP_POSITION = 0
    KEYBOARD_POSITION = 1
    MOUSE_POSITION = 2
    DIGITIZER_POSITION = 3
    # Mask
    HID_PP_MASK = 0x01
    KEYBOARD_MASK = 0x02
    MOUSE_MASK = 0x04
    DIGITIZER_MASK = 0x08
    ALL_MASK = 0x0F
    # Disable callback
    # Position
    DISABLE_HID_PP_CB_POSITION = 4
    DISABLE_KEYBOARD_CB_POSITION = 5
    DISABLE_MOUSE_CB_POSITION = 6
    DISABLE_DIGITIZER_CB_POSITION = 7
    # Mask
    DISABLE_HID_PP_CB_MASK = 0x10
    DISABLE_KEYBOARD_CB_MASK = 0x20
    DISABLE_MOUSE_CB_MASK = 0x40
    DISABLE_DIGITIZER_CB_MASK = 0x80
# end class LinkEnablerInfo


class LogitechProtocol(IntEnum, metaclass=ContainsIntEnumMeta):
    """
    Protocol value for Logitech devices. All values >= 0 can be found in the specification (section
    "Protocol types definition"):
    https://docs.google.com/document/d/11LzttOQP5EgmbbKCIkzBd1qCc5O9c7xiFqyRgHtq15c/edit

    (Those values are redundant with DeviceConnection.ProtocolTypes in
    pyhid.hidpp.hidpp1.notifications.deviceconnection)

    All values < 0 are added for consistency and do not belong to a specification.
    """
    BLE = -2
    USB = -1

    # Specified values (can also be found in DeviceConnection.ProtocolTypes)
    UNKNOWN = 0x00
    BLUETOOTH = 0x01
    MHZ_27 = 0x02
    QUAD_EQUAD = 0x03
    EQUAD_STEP_4_DJ = 0x04
    DFU_LITE = 0x05
    EQUAD_STEP_4_LITE = 0x06
    EQUAD_STEP_4_GAMING = 0x07
    EQUAD_STEP_4_GAMEPADS = 0x08
    GOTTHARD = 0x09
    DAGGER_ROM = 0x0A
    UNIFYING_V2 = 0x0B
    LS1_0 = 0x0C
    LS1_1 = 0x0D
    LS2_LLPM = 0x0E
    LS2_CA = 0x0F
    BLE_PRO = 0x10
    LS2_CA_CRC24 = 0x11
    # The actual protocol of crush receiver is LS2_CA_CRC24. The constant CRUSH(0x91) is only for switching
    # current protocol to Crush receiver by set PROTOCOL_TO_CHANGE_TO = LogitechProtocol.LS2_CA_CRC24_FOR_CRUSH
    LS2_CA_CRC24_FOR_CRUSH = 0x91

    @classmethod
    def unifying_protocols(cls):
        """
        Get the list of Unifying protocols

        :return: List of Unifying protocols
        :rtype: ``tuple[LogitechProtocol]``
        """
        return (
            cls.QUAD_EQUAD,
            cls.EQUAD_STEP_4_DJ,
            cls.EQUAD_STEP_4_LITE,
            cls.EQUAD_STEP_4_GAMING,
            cls.EQUAD_STEP_4_GAMEPADS,
            cls.DAGGER_ROM,
            cls.UNIFYING_V2,
            cls.LS1_0,
            cls.LS1_1,
            cls.LS2_LLPM,
            cls.LS2_CA,
            cls.LS2_CA_CRC24
        )
    # end def unifying_protocols

    @classmethod
    def gaming_protocols(cls):
        """
        Get the list of Gaming protocols

        :return: List of Gaming protocols
        :rtype: ``tuple[LogitechProtocol]``
        """
        return (
            cls.EQUAD_STEP_4_GAMING,
            cls.EQUAD_STEP_4_GAMEPADS,
            cls.LS1_0,
            cls.LS1_1,
            cls.LS2_LLPM,
            cls.LS2_CA,
            cls.LS2_CA_CRC24
        )
    # end def gaming_protocols
# end class LogitechProtocol


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ChannelException(Exception):
    """
    Common class for channel exceptions.
    """

    class Cause(IntEnum):
        """
        Channel exception causes used in a transport context.
        """
        UNKNOWN = 0
        CONTEXT_NOT_OPEN = auto()
        CHANNEL_NOT_OPEN = auto()
        HARDWARE_DEVICE_OFF = auto()
        WRONG_PARAMETER = auto()
        ERROR_BYTES_ARE_SENT = auto()
        EXPECTED_LINK_NOT_PRESENT = auto()
        ASSOCIATED_RECEIVER_CHANNEL_NOT_OPEN = auto()
        ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT = auto()
        DEVICE_NOT_CONNECTED = auto()
        DEVICE_NOT_PRESENT = auto()
        CONFIGURATION_ERROR = auto()
        ERROR_MESSAGE_RECEIVED = auto()
    # end class Cause

    def __init__(self, *args):
        """
        It takes its parameters from the constants in ``ChannelException.Cause``, and may optionally
        provide a message.

        :param args: Arguments passed to the parent constructor
        :type args: ``ChannelException.Cause`` or ``str`` or ``object``
        """
        super().__init__(*args)
    # end def __init__

    def get_cause(self):
        """
        Obtains the exception cause.

        This is the first int argument.

        :return: The exception cause, as an int from ``ChannelException.Cause``
        :rtype: ``ChannelException.Cause``
        """
        causes = [x for x in self.args if isinstance(x, ChannelException.Cause)]
        if len(causes) > 0:
            return causes[0]
        # end if
        return ChannelException.Cause.UNKNOWN
    # end def get_cause

    def get_message(self):
        """
        Get the messages for this exception.

        :return: The message embedded within this exception.
        :rtype: ``str``
        """
        string_messages = [x for x in self.args if isinstance(x, str)]
        return ', '.join(string_messages)
    # end def get_message

    def get_error_message_object(self):
        """
        Get the error message objects for this exception (if any).

        :return: The error message object embedded within this exception (if any)
        :rtype: ``TransportMessage`` or ``TimestampedBitFieldContainerMixin`` or ``None``
        """
        for x in self.args:
            if isinstance(x, (TransportMessage, TimestampedBitFieldContainerMixin)):
                return x
            # end if
        # end for
        return None
    # end def get_error_message_object
# end class ChannelException


class MessageFilter:
    """
    Filter structure to use for a message. It has the index and the value of an element to check in a message.
    """

    def __init__(self, index_in_message, value):
        """
        :param index_in_message: Index of the element to check
        :type index_in_message: ``int`` or ``HexList``
        :param value: Value of the element to check
        :type value: ``int`` or ``HexList``
        """
        self.index_in_message = int(Numeral(index_in_message))
        self.value = int(Numeral(value))
    # end def __init__

    def __str__(self):
        return f"(index: {self.index_in_message} - value: 0x{self.value:02X})"
    # end def __str__

    def __repr__(self):
        return str(self)
    # end def __repr__
# end class MessageFilter


class BaseCommunicationChannel:
    """
    Common implementation of a communication channel.
    """
    MAX_MESSAGE_COUNTER = 20
    RETRY_COUNT = 5

    HIDPP_1_ERROR_FILTERS = [MessageFilter(index_in_message=Hidpp1ErrorCodes.OFFSET.SUB_ID,
                                           value=Hidpp1ErrorCodes.ERROR_TAG)]
    HIDPP_2_ERROR_FILTERS = [MessageFilter(index_in_message=Hidpp2ErrorCodes.OFFSET.ERROR_TAG,
                                           value=Hidpp2ErrorCodes.ERROR_TAG)]
    GENERIC_SEND_TIMEOUT = .6  # in seconds
    GENERIC_GET_TIMEOUT = 2  # in seconds
    WAIT_CONNECTION_STATE_PERIOD = 0.1  # in seconds

    def __init__(self, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param trace_level: Trace level of the channel - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the channel - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        """
        if FORCE_AT_CREATION_ALL_CHANNEL_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_CHANNEL_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_CHANNEL_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_CHANNEL_TRACE_FILE_NAME
        # end if

        # Since this will not be saved as a file name in the trace logger, it is saved here
        self.trace_file_name = trace_file_name

        TRACE_LOGGER.subscribe(subscription_owner=self, trace_level=trace_level, trace_file_name=trace_file_name)

        self._is_open_lock = RLock()
        self.__is_open = False
        self._opening_closing_lock = RLock()

        self.__hardware_device = None
        self.__protocol = LogitechProtocol.UNKNOWN
        self.__hid_dispatcher = HIDDispatcher()

        self._report_type_to_process_message_callback = {
            LogitechReportType.HIDPP: self.__hid_dispatcher.process_interrupt_hidpp,
            LogitechReportType.MOUSE: self.__hid_dispatcher.process_interrupt_hid_mouse,
            LogitechReportType.KEYBOARD: self.__hid_dispatcher.process_interrupt_hid_keyboard,
            LogitechReportType.DIGITIZER: self.__hid_dispatcher.process_interrupt_hid_digitizer,
        }
    # end def __init__

    def __del__(self):
        try:
            if self.is_open:
                self.close()
            # end if
        finally:
            TRACE_LOGGER.unsubscribe(subscription_owner=self)
        # end try
    # end def __del__

    def __str__(self):
        raise NotImplementedAbstractMethodError()
    # end def __str__

    def __repr__(self):
        return str(self)
    # end def __repr__

    @property
    @synchronize_with_object_inner_lock("_is_open_lock")
    def is_open(self):
        """
        Property getter of ``is_open``.

        :return: ``is_open`` value
        :rtype: ``bool``
        """
        return self.__is_open
    # end def property getter is_open

    @is_open.setter
    @synchronize_with_object_inner_lock("_is_open_lock")
    def is_open(self, value):
        """
        Property setter of ``is_open``.

        :param value: ``is_open`` value
        :type value: ``bool``

        :raise ``AssertionError``: If ``value`` is not a ``bool``
        """
        assert isinstance(value, bool), f"{self.__class__.__name__} is_open attribute is a boolean, " \
                                        f"{value} is not"
        self.__is_open = value
        TRACE_LOGGER.log_trace(
            subscription_owner=self, message="open" if value else "closed", trace_level=TraceLevel.DEBUG)
    # end def property setter is_open

    @property
    def hardware_device(self):
        """
        Property getter of ``hardware_device``.

        :return: ``hardware_device`` value
        :rtype: ``HardwareDevice`` or ``None``
        """
        return self.__hardware_device
    # end def property getter hardware_device

    @hardware_device.setter
    def hardware_device(self, value):
        """
        Property setter of ``hardware_device``.

        :param value: ``hardware_device`` value
        :type value: ``HardwareDevice`` or ``None``

        :raise ``AssertionError``: If ``value`` is not a ``HardwareDevice`` or ``None``
        """
        # TODO uncomment when HardwareDevice is implemented
        # assert isinstance(value, (HardwareDevice, type(None))), \
        #     f"{self.__class__.__name__} hardware_device attribute is a HardwareDevice or None, {value} is not"
        self.__hardware_device = value
    # end def property setter hardware_device

    @property
    @synchronize_with_object_inner_lock("_is_open_lock")
    def protocol(self):
        """
        Property getter of ``protocol``.

        :return: ``protocol`` value
        :rtype: ``LogitechProtocol``
        """
        return self.__protocol
    # end def property getter protocol

    @protocol.setter
    @synchronize_with_object_inner_lock("_is_open_lock")
    def protocol(self, value):
        """
        Property setter of ``protocol``.

        :param value: ``protocol`` value
        :type value: ``LogitechProtocol``

        :raise ``AssertionError``: If ``value`` is not a ``LogitechProtocol``
        """
        assert isinstance(value, LogitechProtocol), \
            f"{self.__class__.__name__} protocol attribute is a LogitechProtocol, {value} is not"
        self.__protocol = value
    # end def property setter protocol

    @property
    def hid_dispatcher(self):
        """
        Property getter of ``hid_dispatcher``.

        :return: ``hid_dispatcher`` value
        :rtype: ``HIDDispatcher``
        """
        return self.__hid_dispatcher
    # end def property getter hid_dispatcher

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self, link_enabler):
        """
        Open the channel.

        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo``
        :type link_enabler: ``int`` or ``BitStruct``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        # This method should be setting is_open property to True at the end if it was successful
        raise NotImplementedAbstractMethodError()
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        """
        Close the channel.

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        # This method should be setting is_open property to False at the end if it was successful
        raise NotImplementedAbstractMethodError()
    # end def close

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def update_callback(self, targeted_report_types, callback=None):
        """
        Update the callback method which is called when receiving reports from the DUT.

        :param targeted_report_types: List of report types for which to change the task configuration. Note that
                                      unsupported report types will be ignored.
        :type targeted_report_types: ``list[LogitechReportType]``
        :param callback: Callback when receiving data - OPTIONAL
        :type callback: ``Callable type`` or ``None``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def update_callback

    def turn_on_hardware_device(self):
        """
        Turn on associated hardware device. This operation WILL NOT open all associated ``BaseCommunicationChannel``.

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        :raise ``AssertionError``: If ``hardware_device`` is ``None``
        """
        assert self.hardware_device is not None, "Cannot turn off hardware device if it is None"

        self.hardware_device.turn_on()
    # end def turn_on_hardware_device

    def turn_off_hardware_device(self):
        """
        Turn off associated hardware device. This operation WILL close all associated ``BaseCommunicationChannel``.

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        :raise ``AssertionError``: If ``hardware_device`` is ``None``
        """
        assert self.hardware_device is not None, "Cannot turn off hardware device if it is None"

        self.close()
        self.hardware_device.turn_off()
    # end def turn_off_hardware_device

    def send_data(self, data, timeout=GENERIC_SEND_TIMEOUT):
        """
        Send data through the channel.

        :param data: Data to send
        :type data: ``TimestampedBitFieldContainerMixin`` or ``HexList`` or ``TransportMessage``
        :param timeout: The timeout of this action in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def send_data

    def get_message(
            self,
            report_type=LogitechReportType.HIDPP,
            dispatcher_queue=None,
            raw_filters=None,
            message_class=None,
            timeout=GENERIC_GET_TIMEOUT,
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
        :rtype: ``TransportMessage`` or ``TimestampedBitFieldContainerMixin``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_message

    def process_all_report_type_in_dispatcher(self, report_type=LogitechReportType.HIDPP):
        """
        Process all message of a report type in the dispatcher, freeing the time stamped message queue.

        :param report_type: The report type of message to use - OPTIONAL
        :type report_type: ``LogitechReportType``
        """
        raise NotImplementedAbstractMethodError()
    # end def process_all_report_type_in_dispatcher

    def get_descriptors(self):
        """
        Get descriptors and put them in the HID dispatcher.

        :return: The list of descriptor messages gotten
        :rtype: ``list[ReportDescriptor|None]``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_descriptors

    def get_interface_descriptor(self, interface):
        """
        Get the interface descriptor and put it in the HID dispatcher.

        :param interface: The interface index
        :type interface: ``int``

        :return: The received interface descriptor message
        :rtype: ``ReportDescriptor|None``

        :raise ``ChannelException``: If channel is not open or if the USB device not connected
        """
        raise NotImplementedAbstractMethodError()
    # end def get_interface_descriptor

    def get_transport_id(self, force_refresh_cache=False):
        """
        Get the transport ID of the device, this can mean different IDs depending on the device.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: The transport ID
        :rtype: ``int``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_transport_id

    def send_data_wait_response(
            self,
            data,
            send_timeout=GENERIC_SEND_TIMEOUT,
            reply_timeout=GENERIC_GET_TIMEOUT,
            dispatcher_queue=None,
            raw_filters=None,
            message_class=None,
            skip_error=False):
        """
        Send a request and get the reply through the channel. It can be done without the dispatcher using raw filters
        or with the dispatcher using message class. This means:

        * If NO ``dispatcher_queue`` is given, ``raw_filters`` is taken into account and ``message_class`` is ignored
        * If A ``dispatcher_queue`` is given, ``message_class`` is taken into account and ``raw_filters`` is ignored

        This method has been included to be robust against lost replies. It sends again the request a certain amount
        of time (``BaseCommunicationChannel.RETRY_COUNT``) if the response is not received. Therefore, the timeout can
        be repeated to remove potential repeated messages that were not lost but just to fast to get.

        The error catching mechanism is explained in the description of the method ``get_message``.

        :param data: Data to send
        :type data: ``TimestampedBitFieldContainerMixin`` or ``HexList`` or ``TransportMessage``
        :param send_timeout: The timeout of the send action in seconds (0 disable it) - OPTIONAL
        :type send_timeout: ``float``
        :param reply_timeout: The timeout of the received action in seconds (0 disable it) - OPTIONAL
        :type reply_timeout: ``float``
        :param dispatcher_queue: Queue in the dispatcher to find the message in. If None, the dispatcher step is not
                                 performed - OPTIONAL
        :type dispatcher_queue: ``HidMessageQueue`` or ``None``
        :param raw_filters: A list of filter for the message, or ``None`` to disable it - OPTIONAL
        :type raw_filters: ``list[MessageFilter]`` or ``tuple[list[MessageFilter]]`` or ``None``
        :param message_class: The class(es) of the message to get during the dispatcher step. If None, the message
                              class is not checked. This parameter is only relevant if ``dispatcher_queue`` is not
                              None, otherwise it is ignored - OPTIONAL
        :type message_class: ``type`` or ``tuple[type]`` or ``None``
        :param skip_error: Flag indicating if the automatic error catching mechanism should be skipped or not
        :type skip_error: ``bool``

        :return: The wanted message received on this channel
        :rtype: ``TransportMessage``

        :raise ``AssertionError``: If too many unwanted message are received before receiving the expected one
        """
        for retry_index in range(BaseCommunicationChannel.RETRY_COUNT):
            try:
                self.send_data(data=data, timeout=send_timeout)
                message = self.get_message(
                    dispatcher_queue=dispatcher_queue,
                    raw_filters=raw_filters,
                    message_class=message_class,
                    timeout=reply_timeout,
                    skip_error=skip_error)

                if retry_index > 0:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Missed packets: {retry_index}",
                        trace_level=TraceLevel.WARNING)
                    # Since there were retries, we might receive more responses
                    for _ in range(retry_index):
                        try:
                            self.get_message(
                                dispatcher_queue=dispatcher_queue,
                                raw_filters=raw_filters,
                                message_class=message_class,
                                timeout=reply_timeout)
                        except Empty:
                            break
                        except ChannelException as e:
                            if e.get_cause() == ChannelException.Cause.ERROR_MESSAGE_RECEIVED:
                                # Error messages could have been received for previous sent packets and ignored
                                # because of skip_error
                                continue
                            # end if
                            raise
                        # end try
                    # end for
                # end if

                return message
            except Empty:
                if retry_index < BaseCommunicationChannel.RETRY_COUNT - 1:
                    sleep(.01)
                    continue
                # end if
                raise
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.TIMEOUT,
                                     TransportContextException.Cause.CONTEXT_ERROR_PIPE) and \
                        retry_index < BaseCommunicationChannel.RETRY_COUNT - 1:
                    sleep(.01)
                    continue
                # end if
                raise
            # end try
        # end for
    # end def send_data_wait_response

    def is_device_connected(self, force_refresh_cache=False):
        """
        Check if the device is connected, this can mean different IDs depending on the device. If the device is not
        connected, the channel will be automatically closed. The result will be cached.

        :param force_refresh_cache: Flag indicating if the cache should be ignored - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: Flag indicating if the device is connected or not
        :rtype: ``bool``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_device_connected

    def wait_device_connection_state(self, connected, timeout):
        """
        Wait for a connection state on the device. If the device is not connected at the end of this method, the
        channel will be automatically closed. The result will be cached.

        :param connected: Flag indicating to wait for a connected state if ``True`` or disconnected state otherwise.
        :type connected: ``bool``
        :param timeout: Time to wait for the expected connection state to happen [seconds]
        :type timeout: ``float`` or ``int``

        :return: Flag indicating if the device is in the wanted connection state after the wait
        :rtype: ``bool``

        :raise ``ChannelException``: It can raise for any causes in ``ChannelException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def wait_device_connection_state

    def is_link_enabled(self, link_report_type):
        """
        Check if a link is enabled. It returns ``False`` if the channel is closed.

        :param link_report_type: Report type of the link to check.
        :type link_report_type: ``LogitechReportType``

        :return: Flag indicating if the link is enabled
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_link_enabled

    def _is_hardware_device_on(self):
        """
        Check if the hardware device (if any) is on. Raise an exception if not.

        :return: Flag indicating if hardware device (if present) is on.
        :rtype: ``bool``
        """
        return self.hardware_device is None or self.hardware_device.is_on
    # end def _is_hardware_device_on

    def _common_get_message(
            self,
            report_type,
            time_stamped_msg_queue,
            dispatcher_queue, raw_filters,
            message_class,
            timeout,
            skip_error):
        """
        Common part for get message for all BaseCommunicationChannel. The error catching mechanism is explained in the
        description of the method ``get_message``.

        :param report_type: The report type of message to get
        :type report_type: ``LogitechReportType``
        :param time_stamped_msg_queue: Time stamped message queue of the structure to use
        :type time_stamped_msg_queue: ``QueueWithFilter``
        :param dispatcher_queue: Queue in the dispatcher to find the message in. If None, the dispatcher step is not
                                 performed
        :type dispatcher_queue: ``HidMessageQueue`` or ``None``
        :param raw_filters: A list of filter for the message. If ``None``, the message is not checked. This parameter is
                            only relevant if ``dispatcher_queue`` IS ``None``, otherwise it is ignored
        :type raw_filters: ``list[MessageFilter]`` or ``tuple[list[MessageFilter]]`` or ``None``
        :param message_class: The class(es) of the message to get during the dispatcher step. If None, the message
                              class is not checked. This parameter is only relevant if ``dispatcher_queue`` is not
                              None, otherwise it is ignored
        :type message_class: ``type`` or ``tuple[type]`` or ``None``
        :param timeout: The timeout of this action in seconds (0 disable it)
        :type timeout: ``float``
        :param skip_error: Flag indicating if the automatic error catching mechanism should be skipped or not
        :type skip_error: ``bool``

        :return: The first message received on this channel
        :rtype: ``TransportMessage`` or ``TimestampedBitFieldContainerMixin``
        """
        if dispatcher_queue is None:
            message = self._common_get_message_without_dispatcher(
                report_type=report_type,
                time_stamped_msg_queue=time_stamped_msg_queue,
                raw_filters=raw_filters,
                timeout=timeout,
                skip_error=skip_error)
        else:
            message = self._common_get_message_with_dispatcher(
                report_type=report_type,
                time_stamped_msg_queue=time_stamped_msg_queue,
                dispatcher_queue=dispatcher_queue,
                message_class=message_class,
                timeout=timeout,
                skip_error=skip_error)
        # end if

        return message
    # end def _common_get_message

    def _common_get_message_without_dispatcher(
            self, report_type, time_stamped_msg_queue, raw_filters, timeout, skip_error):
        """
        Common part for get message without using the HID dispatcher. The error catching mechanism is explained in the
        description of the method ``get_message``.

        :param report_type: The report type of message to get
        :type report_type: ``LogitechReportType``
        :param time_stamped_msg_queue: Time stamped message queue of the structure to use
        :type time_stamped_msg_queue: ``QueueWithFilter``
        :param raw_filters: A list of filter for the message. If ``None``, the message is not checked
        :type raw_filters: ``list[MessageFilter]`` or ``tuple[list[MessageFilter]]`` or ``None``
        :param timeout: The timeout of this action in seconds (0 disable it)
        :type timeout: ``float`` or ``int``
        :param skip_error: Flag indicating if the automatic error catching mechanism should be skipped or not. It will
                           be forced to ``True`` if ``raw_filters`` is ``None``
        :type skip_error: ``bool``

        :return: The first message received on this channel
        :rtype: ``TransportMessage`` or ``TimestampedBitFieldContainerMixin``

        :raise ``ChannelException``: If a part of the code should not have been reached with no message found
        """
        is_error_1_in_filters = True
        is_error_2_in_filters = True

        if report_type != LogitechReportType.HIDPP:
            skip_error = True
        # end if

        if raw_filters is None:
            filter_method = None
            skip_error = True
        else:
            if not isinstance(raw_filters, tuple):
                raw_filters = (raw_filters,)
            # end if

            if not skip_error:
                is_error_1_in_filters, is_error_2_in_filters = self._are_hidpp_errors_in_filters(filters=raw_filters)

                for is_error_in_filters, error_filters in [(is_error_1_in_filters, self.HIDPP_1_ERROR_FILTERS),
                                                           (is_error_2_in_filters, self.HIDPP_2_ERROR_FILTERS)]:
                    if not is_error_in_filters:
                        raw_filters = tuple(list(raw_filters) + [error_filters])
                    # end if
                # end for
            # end if

            def filter_method(message_gotten):
                """
                Filter method to give to the queue when getting a message.

                :param message_gotten: The message to check
                :type message_gotten: ``TransportMessage``

                :return: Flag indicating if the message follow the filter
                :rtype:``bool``
                """
                return self._is_expected_message(message=message_gotten, filters=raw_filters)
            # end def filter_method
        # end if

        message = time_stamped_msg_queue.get_first_message_filter(
            timeout=timeout if timeout > 0 else None, filter_method=filter_method)

        if not skip_error:
            for is_error_in_filters, error_filters in [(is_error_1_in_filters, self.HIDPP_1_ERROR_FILTERS),
                                                       (is_error_2_in_filters, self.HIDPP_2_ERROR_FILTERS)]:
                if not is_error_in_filters and self._is_expected_message(message=message, filters=error_filters):
                    raise ChannelException(
                        ChannelException.Cause.ERROR_MESSAGE_RECEIVED, f"Received unexpected error message", message)
                # end if
            # end for
        # end if

        return message
    # end def _common_get_message_without_dispatcher

    def _common_get_message_with_dispatcher(
            self, report_type, time_stamped_msg_queue, dispatcher_queue, message_class, timeout, skip_error):
        """
        Common part for get message using the HID dispatcher. The error catching mechanism is explained in the
        description of the method ``get_message``.

        :param report_type: The report type of message to get
        :type report_type: ``LogitechReportType``
        :param time_stamped_msg_queue: Time stamped message queue of the structure to use
        :type time_stamped_msg_queue: ``QueueWithFilter``
        :param dispatcher_queue: Queue in the dispatcher to find the message in
        :type dispatcher_queue: ``HidMessageQueue``
        :param message_class: The class(es) of the message to get during the dispatcher step. If ``None``, the message
                              class is not checked and ``skip_error`` is forced to ``True``.
        :type message_class: ``type`` or ``tuple[type]`` or ``None``
        :param timeout: The timeout of this action in seconds (0 disable it)
        :type timeout: ``float`` or ``int``
        :param skip_error: Flag indicating if the automatic error catching mechanism should be skipped or not. It will
                           be forced to ``True`` if ``report_type`` is not ``LogitechReportType.HIDPP`` or if
                           ``message_class`` is ``None``
        :type skip_error: ``bool``

        :return: The first message received on this channel
        :rtype: ``TransportMessage`` or ``TimestampedBitFieldContainerMixin``

        :raise ``ChannelException``: If a part of the code should not have been reached with no message found
        """
        is_error_1_in_filters = True
        is_error_2_in_filters = True

        if not skip_error:
            # TODO: For now always deactivate error catching, it will be reactivated in another pull request
            skip_error = True
        # end if

        if report_type != LogitechReportType.HIDPP:
            skip_error = True
        # end if

        if message_class is None:
            filter_method = None
            skip_error = True
        else:
            if not skip_error:
                if not isinstance(message_class, tuple):
                    message_class = (message_class,)
                # end if

                is_error_1_in_filters = Hidpp1ErrorCodes in message_class
                is_error_2_in_filters = Hidpp2ErrorCodes in message_class
            # end if

            def filter_method(message_gotten):
                """
                 Filter method to give to the queue when getting a message.

                :param message_gotten: The message to check
                :type message_gotten: ``TransportMessage``

                :return: Flag indicating if the message follow the filter
                :rtype:``bool``
                """
                return isinstance(message_gotten, message_class)
            # end def filter_method
        # end if

        self.process_all_report_type_in_dispatcher(report_type=report_type)

        message = None

        if not dispatcher_queue.event_empty.is_set():
            message = dispatcher_queue.get_no_wait_first_message_filter(
                filter_method=filter_method, skip_error=True)
        # end if

        if message is None:
            end_time = time() + timeout
            remaining_time = timeout
            while message is None and remaining_time >= 0:
                transport_message = time_stamped_msg_queue.get(block=remaining_time > 0, timeout=remaining_time)
                if not skip_error:
                    for is_error_in_filters, error_filters in [(is_error_1_in_filters, self.HIDPP_1_ERROR_FILTERS),
                                                               (is_error_2_in_filters, self.HIDPP_2_ERROR_FILTERS)]:
                        if not is_error_in_filters and self._is_expected_message(message=transport_message,
                                                                                 filters=error_filters):
                            raise ChannelException(ChannelException.Cause.ERROR_MESSAGE_RECEIVED,
                                                   f"Received unexpected error message",
                                                   message)
                        # end if
                    # end for
                # end if
                self._report_type_to_process_message_callback[report_type](transport_message=transport_message)
                remaining_time = end_time - time()
                # This could add a small drift to the computation of the timeout, but it should be small enough to
                # be accepted
                message = dispatcher_queue.get_no_wait_first_message_filter(
                    filter_method=filter_method, skip_error=remaining_time > 0)
            # end while

            if message is None:
                raise ChannelException(
                    ChannelException.Cause.UNKNOWN,
                    "Critical error, this part should not have been reached if no message was found")
            # end if
        # end if

        return message
    # end def _common_get_message_with_dispatcher

    @staticmethod
    def _are_hidpp_errors_in_filters(filters):
        """
        Check if the HID++ errors (1 and 2) are present in the filters.

        :param filters: A list of filter for the message
        :type filters: ``tuple[list[MessageFilter]]``

        :return: Flag indicating if the HID++ errors (1 and 2) are present in the filters or not
        :rtype: ``tuple[bool]``
        """
        is_error_1_in_filters = False
        is_error_2_in_filters = False
        for message_filters in filters:
            for byte_filter in message_filters:
                if byte_filter.index_in_message == Hidpp1ErrorCodes.OFFSET.SUB_ID and \
                        byte_filter.value == Hidpp1ErrorCodes.ERROR_TAG:
                    is_error_1_in_filters = True
                elif byte_filter.index_in_message == Hidpp2ErrorCodes.OFFSET.ERROR_TAG and \
                        byte_filter.value == Hidpp2ErrorCodes.ERROR_TAG:
                    is_error_2_in_filters = True
                # end if

                if is_error_1_in_filters and is_error_2_in_filters:
                    break
                # end if
            # end for
            if is_error_1_in_filters and is_error_2_in_filters:
                break
            # end if
        # end for

        return is_error_1_in_filters, is_error_2_in_filters
    # end def _are_hidpp_errors_in_filters

    def _is_expected_message(self, message, filters):
        """
        Check if a message matches the expected filters.

        :param message: Data to send
        :type message: ``TransportMessage``
        :param filters: A list of filter for the message
        :type filters: ``list[MessageFilter]`` or ``tuple[list[MessageFilter]]``

        :return: Flag indicating if this is the expected message or not
        :rtype: ``bool``
        """
        if not isinstance(filters, tuple):
            filters = (filters,)
        # end if

        for message_filters in filters:
            is_expected_message = True
            for byte_filter in message_filters:
                to_check = int(Numeral(message.data[byte_filter.index_in_message]))
                if to_check != byte_filter.value:
                    is_expected_message = False
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Wrong element in message at index {byte_filter.index_in_message}: "
                                f"expected {byte_filter.value}, received {to_check}",
                        trace_level=TraceLevel.DEBUG)
                # end if
            # end for
            if is_expected_message:
                return True
            # end if
        # end for
        return False
    # end def _is_expected_message
# end class BaseCommunicationChannel

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
