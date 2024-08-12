#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.transportcontext
:brief: Transport (BLE, USB, etc...) context interface classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from functools import wraps
from inspect import signature
from threading import Event
from threading import RLock
# For some reason pycharm decided not to see it while being used in a docstring (it normally does)
# noinspection PyUnresolvedReferences
from typing import Callable

from pylibrary.system.device import ReadOnlyDeviceCacheMetaClass
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.threadutils import RLockedDict
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.tracebacklog import TracebackLogWrapper

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

# Configure all transports traces verbosity
#  - None: disable all traces (Default)
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for packets only
#  - TraceLevel.DEBUG: Debug level will be for every context actions
FORCE_AT_CREATION_ALL_TRANSPORT_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_TRANSPORT_TRACE_FILE_NAME = None


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TransportContextException(Exception):
    """
    Common class for transport context exceptions.
    """

    class Cause(IntEnum):
        """
        Transport context exception causes used in a transport context.
        """
        UNKNOWN = 0
        CONTEXT_NOT_OPEN = auto()
        CONTEXT_INVALID_STATE = auto()
        DEVICE_NOT_CONNECTED = auto()
        DEVICE_NOT_FOUND = auto()
        DEVICE_NOT_OPEN = auto()
        DEVICE_UNKNOWN = auto()
        TIMEOUT = auto()
        CONTEXT_ERROR_PIPE = auto()
        CONTEXT_ERROR_IO = auto()
        CONTEXT_ERROR_NO_DEVICE = auto()
        CONTEXT_CONFIG_UNKNOWN = auto()
        DATA_ERROR = auto()
        ACTION_ALREADY_DONE = auto()
        CONTEXT_INTERNAL_ERROR = auto()
        PARAMETER_ERROR = auto()
        CONTEXT_DOOMED_ERROR = auto()
        INSUFFICIENT_AUTHENTICATION = auto()
        CONTEXT_INVALID_PARAMETER = auto()
        DEVICE_DISCONNECTION_DURING_OPERATION = auto()
        AUTHENTICATION_FAILED = auto()
    # end class Cause

    def __init__(self, *args):
        """
        Take its parameters from the constants in ``TransportContextException.Cause``, and may optionally
        provide a message.

        :param args: Arguments passed to the parent constructor
        :type args: ``TransportContextException.Cause`` or ``str`` or ``object``
        """
        super().__init__(*args)
    # end def __init__

    def get_cause(self):
        """
        Obtain the exception cause.

        This is the first int argument.

        :return: The exception cause, as an int from ``TransportContextException.Cause``
        :rtype: ``TransportContextException.Cause``
        """
        causes = [x for x in self.args if isinstance(x, TransportContextException.Cause)]
        if len(causes) > 0:
            return causes[0]
        # end if
        return TransportContextException.Cause.UNKNOWN
    # end def get_cause

    def get_message(self):
        """
        Get the messages for this exception.

        :return: The message embedded within this exception.
        :rtype: ``str``
        """
        string_messages = [x for x in self.args if isinstance(x, str)]
        return ", ".join(string_messages)
    # end def get_message

    def add_message(self, message):
        """
        Extend the message list for this exception.

        :param message: The message to add to this exception.
        :type message: ``str``
        """
        self.args += (message,)
    # end def add_message
# end class TransportContextException


def internal_exception_wrapper(exception_types):
    """
    Wrap a method to except some exception types and put them in a generic ``TransportContextException`` with cause
    ``CONTEXT_INTERNAL_ERROR`` and the trace of the exception as message.

    :param exception_types: The type(s) of exception to wrap
    :type exception_types: ``type`` or ``tuple[type]``

    :return: An inner decorator that will wrap the wanted exceptions and put it in a generic
    :rtype: ``callable type``
    """

    def synchronize(wrapped):
        """
        Wrapper around the given function

        :param wrapped: The function to decorate
        :type wrapped: ``callable type``

        :return: An inner decorator on the function
        :rtype: ``callable type``
        """

        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            """
            The exception wrapping on the decorated function

            :param args: The decorated function arguments
            :type args: ``tuple``
            :param kwargs: The decorated function keyword arguments
            :type kwargs: ``dict``

            :return: The decorated function return value
            :rtype: ``object`` or ``None``
            """
            try:
                return wrapped(*args, **kwargs)
            except exception_types:
                raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                                f"Internal error:\n{TracebackLogWrapper.get_exception_stack()}")
            # end try
        # end def wrapper

        try:
            # Copy signature of the source method to the wrapper one
            wrapper.__signature__ = signature(wrapped)
        except ValueError:
            # Value error is raised when source_method signature does not exist, it should therefore not be a problem
            pass
        # end try
        return wrapper
    # end def synchronize
    return synchronize
# end def internal_exception_wrapper


class TransportContextDevice:
    """
    Transport device used in a transport context.
    """

    def __init__(self, connected=False, transfer_callbacks=None):
        """
        :param connected: Flag indicating if the device is connected - OPTIONAL
        :type connected: ``bool``
        :param transfer_callbacks: The callbacks that will be used when a transfer is received for each transfer type
                                   (HID mouse, HID keyboard, HID++, etc...), its format is a thread safe dictionary
                                   (the keys are dependent on the type of context). If ``None``, it will be set as an
                                   empty thread safe dictionary - OPTIONAL
        :type transfer_callbacks: ``RLockedDict`` or ``None``
        """
        self._lock_connected = RLock()
        self._connected = connected
        self._transfer_callbacks = transfer_callbacks if transfer_callbacks is not None else RLockedDict()

        # This event is there only for contexts with asynchronous event for connection of a device (see
        # ``TransportContext.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY``).
        # It can be used to wait for a connection to happen. It is set when not used
        self.wait_for_connection_event = Event()
        self.wait_for_connection_event.set()
        # This event is there only for contexts with asynchronous event for disconnection of a device (see
        # ``TransportContext.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY``).
        # It can be used to wait for a disconnection to happen. It is set when not used
        self.wait_for_disconnection_event = Event()
        self.wait_for_disconnection_event.set()
    # end def __init__

    @property
    @synchronize_with_object_inner_lock("_lock_connected")
    def connected(self):
        """
        Property getter of ``connected``.

        :return: ``connected`` value
        :rtype: ``bool``
        """
        return self._connected
    # end def property getter connected

    @connected.setter
    @synchronize_with_object_inner_lock("_lock_connected")
    def connected(self, connected):
        """
        Property setter of ``connected``.

        :param connected: ``connected`` value
        :type connected: ``bool``
        """
        assert isinstance(connected, bool), \
            f"{self.__class__.__name__} connected attribute is a bool, {connected} is not"

        self._connected = connected
    # end def property setter connected

    @synchronize_with_object_inner_lock("_transfer_callbacks")
    def set_transfer_callback(self, transfer_type_key, callback):
        """
        Set a transfer callback

        :param transfer_type_key: The key in the internal thread safe dictionary to set the callback (its type
                                  dependent on the type of context)
        :type transfer_type_key: ``object``
        :param callback: The callback to use for the type of transfer, it should have the argument
                         ``transport_message`` in its signature. If ``None``, the associated entry in the thread
                         safe dictionary will be removed (if present)
        :type callback: ``Callable`` or ``None``
        """
        if callback is not None:
            self._transfer_callbacks[transfer_type_key] = callback
        else:
            self._transfer_callbacks.pop(transfer_type_key, None)
        # end if
    # end def set_transfer_callback

    @synchronize_with_object_inner_lock("_transfer_callbacks")
    def get_transfer_callback(self, transfer_type_key):
        """
        Get a transfer callback

        :param transfer_type_key: The key in the internal thread safe dictionary to get the callback (its type
                                  dependent on the type of context)
        :type transfer_type_key: ``object``

        :return: The callback for the type of transfer
        :rtype: ``Callable`` or ``None``
        """
        return self._transfer_callbacks.get(transfer_type_key, None)
    # end def get_transfer_callback

    @synchronize_with_object_inner_lock("_transfer_callbacks")
    def clear_transfer_callbacks(self):
        """
        Clear all transfer callbacks
        """
        self._transfer_callbacks.clear()
    # end def clear_transfer_callbacks
# end class TransportContextDevice


class TransportContext(metaclass=ReadOnlyDeviceCacheMetaClass):
    """
    Common implementation of a transport context.
    """
    CONFIG_DIRECTORY_PATH = None  # Path to find the config files and the key files
    CONFIG_FILE_NAME = None  # Name of the configuration file
    # Flag to indicate that the type of Transport context has an asynchronous way of handling connection and
    # disconnection of a device
    ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY = False

    def __init__(self, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param trace_level: Trace level of the transport context
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the transport context
        :type trace_file_name: ``str`` or ``None``
        """
        if FORCE_AT_CREATION_ALL_TRANSPORT_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_TRANSPORT_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_TRANSPORT_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_TRANSPORT_TRACE_FILE_NAME
        # end if

        # Since this will not be saved as a file name in the trace logger, it is saved here
        self.trace_file_name = trace_file_name

        TRACE_LOGGER.subscribe(subscription_owner=self, trace_level=trace_level, trace_file_name=trace_file_name)

        self._is_open_lock = RLock()
        self.__is_open = False
        self._opening_closing_lock = RLock()
    # end def __init__

    def __del__(self):
        """
        Close the context before its destruction.
        """
        self.close()
        TRACE_LOGGER.unsubscribe(subscription_owner=self)
    # end def __del__

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

        :raise ``AssertionError``: If ``value`` is not a boolean
        """
        assert isinstance(value, bool), f"{self.__class__.__name__} is_open attribute is a boolean, " \
                                        f"{value} is not"
        self.__is_open = value
        if value:
            log_str = f"{self.__class__.__name__} open"
        else:
            log_str = f"{self.__class__.__name__} closed"
        # end if
        TRACE_LOGGER.log_trace(subscription_owner=self, message=log_str, trace_level=TraceLevel.DEBUG)
    # end def property setter is_open

    @classmethod
    def generate_configuration_file(cls, path, *args, **kwargs):
        """
        Generate the configuration file for the context.

        :param path: The path where the configuration file will be generated
        :type path: ``str``
        :param args: Potential child argument - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword argument - OPTIONAL
        :type kwargs: ``object``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("generate_configuration_file() method should be implemented by child class")
    # end def generate_configuration_file

    @classmethod
    def configure_device_cache(cls, path, force_reconfiguration=False, *args, **kwargs):
        """
        Configure the transport context device cache.

        :param path: The path where the current configuration file can be found
        :type path: ``str``
        :param force_reconfiguration: Flag indicating if the reconfiguration should be forced if the cache was already
                                      configured - OPTIONAL
        :type force_reconfiguration: ``bool``
        :param args: Potential child argument - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword argument - OPTIONAL
        :type kwargs: ``object``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        :raise ``ValueError``: If the ``path`` parameter is not an accessible file
        """
        raise NotImplementedError("configure_device_cache() method should be implemented by child class")
    # end def configure_device_cache

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self):
        """
        Open the transport context.

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        # This method should be setting is_open property to True at the end if it was successful
        raise NotImplementedError("open() method should be implemented by child class, and use property is_open")
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        """
        Close the transport context.

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        # This method should be setting is_open property to False at the end if it was successful
        raise NotImplementedError("close() method should be implemented by child class, and use property is_open")
    # end def close

    def reset(self):
        """
        Reset the transport context.

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("reset() method should be implemented by child class")
    # end def reset

    def get_devices(self, index_in_cache=None, *args, **kwargs):
        """
        Get a list of context devices. Multiple filters can be used as parameters:

        * If ``index_in_cache`` is given, other filters are ignored and the index in the cache is used to get the device
        * Child class can add new filters as parameters

        :param index_in_cache: The index in the cache of the device to get - OPTIONAL
        :type index_in_cache: ``int`` or ``None``
        :param args: Potential child parameters - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword parameters - OPTIONAL
        :type kwargs: ``object``

        :return: The list of found device with the given filters (empty list if no device found)
        :rtype: ``list[TransportContextDevice]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("get_devices() method should be implemented by child class")
    # end def get_devices
# end class TransportContext

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
