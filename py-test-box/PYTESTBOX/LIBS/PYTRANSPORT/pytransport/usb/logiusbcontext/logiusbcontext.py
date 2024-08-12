#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytransport.usb.logiusbcontext.logiusbcontext
:brief: Logiusb USB context classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/12/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from atexit import register
from ctypes import c_long
from ctypes import py_object
from ctypes import pythonapi
from queue import Queue
from sys import platform
from threading import RLock
from threading import Thread
from time import perf_counter_ns
from time import sleep
# For some reason pycharm decided not to see it while being used in a docstring (it normally does)
# noinspection PyUnresolvedReferences
from typing import Callable
from warnings import warn
from weakref import ref

from logiusb_py.logiusb import LogiusbContext
from logiusb_py.logiusb import LogiusbDevice
from logiusb_py.logiusb import LogiusbTransfer
from logiusb_py.logiusb_constants import LogiusbDefines
from logiusb_py.logiusb_constants import LogiusbDeviceSpeed
from logiusb_py.logiusb_constants import LogiusbLogLevel
from logiusb_py.logiusb_constants import LogiusbPacketIndex
from logiusb_py.logiusb_constants import LogiusbUtilsConstant
from logiusb_py.logiusb_stuctures import LogiusbDeviceDescriptor
from logiusb_py.logiusb_utils import LogiusbException
from pylibrary.system.tracelogger import DummyOwner
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import RLockedDict
from pylibrary.tools.threadutils import ThreadedExecutor
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pytransport.transportcontext import TRACE_LOGGER
from pytransport.transportcontext import TransportContextException
from pytransport.usb.logiusbcontext.logiusbtasks import InterruptPollingTask
from pytransport.usb.logiusbcontext.logiusbtasks import MAX_THREADS
from pytransport.usb.usbcontext import UsbContext
from pytransport.usb.usbcontext import UsbContextDevice
from pytransport.usb.usbmessage import UsbMessage

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
# Reattach or not the kernel driver when closing a device, by default it is set to False to gain time after
# the first open
REATTACH_KERNEL_DRIVER = False
READER_NAME_ADDON_FOR_DOOMED_DEVICE = " (logiusb device doomed)"


# ----------------------------------------------------------------------------------------------------------------------
# Implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiusbUsbContextDevice(UsbContextDevice):
    """
    USB device structure used in a Logiusb USB context.
    """

    def __init__(self, reader_name="", vid=0, pid=0, connected=False, transfer_callbacks=None, logiusb_device=None):
        """
        :param reader_name: The bus ID and port number read in the config file, format: Bus X Device Y, it is ignored
                            when ``logiusb_device`` is not ``None`` - OPTIONAL
        :type reader_name: ``str``
        :param vid: The VID of the device, it is ignored when ``logiusb_device`` is not ``None`` - OPTIONAL
        :type vid: ``int``
        :param pid: The PID of the device, it is ignored when ``logiusb_device`` is not ``None`` - OPTIONAL
        :type pid: ``int``
        :param connected: Flag indicating if the device is connected, it is ignored when ``logiusb_device`` is not
                          ``None`` - OPTIONAL
        :type connected: ``bool``
        :param transfer_callbacks: The callbacks that will be used when a transfer is received for each transfer type
                                   (HID mouse, HID keyboard, HID++, etc...), its format is a thread safe dictionary
                                   (the keys are endpoint IDs). If ``None``, it will be set as an
                                   empty thread safe dictionary - OPTIONAL
        :type transfer_callbacks: ``RLockedDict`` or ``None``
        :param logiusb_device: Logiusb device associated to this device - OPTIONAL
        :type logiusb_device: ``LogiusbDevice`` or ``None``
        """
        self._property_lock = RLock()
        self._reader_name = reader_name
        self._vid = vid
        self._pid = pid
        self._speed = None
        self._address = None
        self._device_descriptor = None
        self._active_configuration = None
        self._logiusb_device_key = LogiusbUtilsConstant.UNKNOWN_DEVICE_KEY

        if logiusb_device is not None:
            with logiusb_device:
                if logiusb_device.is_doomed:
                    self._reader_name += READER_NAME_ADDON_FOR_DOOMED_DEVICE
                else:
                    ports = "->".join([str(i) for i in logiusb_device.get_device_port_list()])
                    self._reader_name = f"Bus {logiusb_device.bus} Device {ports}"
                    self._vid = logiusb_device.vid
                    self._pid = logiusb_device.pid
                    self._speed = logiusb_device.speed
                    self._device_descriptor = logiusb_device.device_descriptor
                    self._active_configuration = logiusb_device.active_config
                    self._logiusb_device_key = logiusb_device.get_device_key()
                    # After calling value.attached, it can doom the device if it is not attached
                    if logiusb_device.is_doomed:
                        self._reader_name += READER_NAME_ADDON_FOR_DOOMED_DEVICE
                    # end if
                # end if
            # end with
        # end if
        super().__init__(
            reader_name=reader_name, vid=vid, pid=pid, connected=connected, transfer_callbacks=transfer_callbacks)

        self._logiusb_device = logiusb_device
    # end def __init__

    @property
    @synchronize_with_object_inner_lock("_property_lock")
    def logiusb_device(self):
        """
        Property getter of ``logiusb_device``.

        :return: ``logiusb_device`` value
        :rtype: ``LogiusbDevice`` or ``None``
        """
        return self._logiusb_device
    # end def property getter logiusb_device

    @logiusb_device.setter
    def logiusb_device(self, logiusb_device):
        """
        Property setter of ``logiusb_device``. This will change the value of some other properties that are related
        to the device.

        :param logiusb_device: ``logiusb_device`` value
        :type logiusb_device: ``LogiusbDevice`` or ``None``

        :raise ``AssertionError``: If ``value`` is not a ``LogiusbDevice`` or ``None``
        """
        assert isinstance(logiusb_device, (LogiusbDevice, type(None))), \
            f"{self.__class__.__name__} _logiusb_device attribute is a LogiusbDevice or None, {logiusb_device} is not"

        with self._property_lock:
            self._logiusb_device = logiusb_device
        # end with

        reader_name = None
        vid = None
        pid = None
        speed = None
        device_descriptor = None
        active_configuration = None
        logiusb_device_key = None
        if logiusb_device is not None:
            # To avoid calling locks inside of locks, changing the associated properties values is done in using
            # local variables for transiting the information
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    ports = "->".join([str(i) for i in logiusb_device.get_device_port_list()])
                    reader_name = f"Bus {logiusb_device.bus} Device {ports}"
                    vid = logiusb_device.vid
                    pid = logiusb_device.pid
                    speed = logiusb_device.speed
                    device_descriptor = logiusb_device.device_descriptor
                    active_configuration = logiusb_device.active_config
                    logiusb_device_key = logiusb_device.get_device_key()
                    # After calling value.attached, it can doom the device if it is not attached
                    if logiusb_device.is_doomed:
                        reader_name += READER_NAME_ADDON_FOR_DOOMED_DEVICE
                    # end if
                # end if
            # end with

            if reader_name is not None:
                with self._property_lock:
                    self._reader_name = reader_name
                    self._vid = vid
                    self._pid = pid
                    self._speed = speed
                    self._device_descriptor = device_descriptor
                    self._active_configuration = active_configuration
                    self._logiusb_device_key = logiusb_device_key
                # end with
            else:
                # LogiusbDevice doomed
                with self._property_lock:
                    self._logiusb_device_key = LogiusbUtilsConstant.UNKNOWN_DEVICE_KEY
                    if READER_NAME_ADDON_FOR_DOOMED_DEVICE not in self._reader_name:
                        self._reader_name += READER_NAME_ADDON_FOR_DOOMED_DEVICE
                    # end if
                # end with
            # end if
        else:
            with self._property_lock:
                self._logiusb_device_key = LogiusbUtilsConstant.UNKNOWN_DEVICE_KEY
                # Remove the potential doomed information from the name
                if READER_NAME_ADDON_FOR_DOOMED_DEVICE in self._reader_name:
                    self._reader_name = self._reader_name[:-len(READER_NAME_ADDON_FOR_DOOMED_DEVICE)]
                # end if
            # end with
        # end if
    # end def property setter logiusb_device

    @property
    def logiusb_device_key(self):
        """
        Property getter of ``logiusb_device_key``. This attribute is changed to a property to be computed with the
        ``LogiusbDevice``. If the ``LogiusbDevice`` is not accessible, the last saved value is returned.
        This attribute is read-only.

        :return: ``logiusb_device_key`` value
        :rtype: ``tuple[int]``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        logiusb_device_key = None
        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    logiusb_device_key = logiusb_device.get_device_key()
                # end if
            # end with

            if logiusb_device_key is not None:
                with self._property_lock:
                    self._logiusb_device_key = logiusb_device_key
                # end with
                return logiusb_device_key
            # end if
        # end if

        with self._property_lock:
            return self._logiusb_device_key
        # end with
    # end def property getter logiusb_device_key

    @property
    def reader_name(self):
        """
        Property getter of ``reader_name``. This attribute is changed to a property to be computed with the
        ``LogiusbDevice``. If the ``LogiusbDevice`` is not accessible, the last saved value is returned.

        :return: ``reader_name`` value
        :rtype: ``str``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    ports = "->".join([str(i) for i in logiusb_device.get_device_port_list()])
                    reader_name = f"Bus {logiusb_device.bus} Device {ports}"
                else:
                    reader_name = None
                # end if
            # end with

            if reader_name is not None:
                with self._property_lock:
                    self._reader_name = reader_name
                # end with
                return reader_name
            else:
                with self._property_lock:
                    if READER_NAME_ADDON_FOR_DOOMED_DEVICE not in self._reader_name:
                        self._reader_name += READER_NAME_ADDON_FOR_DOOMED_DEVICE
                        return self._reader_name
                    # end if
                # end with
            # end if
        # end if

        with self._property_lock:
            return self._reader_name
        # end with
    # end def property getter reader_name

    @reader_name.setter
    def reader_name(self, reader_name):
        """
        DEPRECATED

        Property setter of ``reader_name``. This attribute is changed to a property to be computed with the
        ``LogiusbDevice``. This property is then read only but to be backward compatible, the setter is created but
        does nothing.

        :param reader_name: ``reader_name`` value
        :type reader_name: ``str``
        """
        warn('This property is then read only but to be backward compatible, the setter is created but does nothing. '
             f'reader_name is NOT set to {reader_name}', DeprecationWarning)
    # end def property setter reader_name

    @property
    def vid(self):
        """
        Property getter of ``vid``. This attribute is changed to a property to have it coincide with the
        attribute ``vid`` of the ``LogiusbDevice``. If the ``LogiusbDevice`` is not accessible, the last saved
        value is returned.

        :return: ``vid`` value
        :rtype: ``int``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    vid = logiusb_device.vid
                else:
                    vid = None
                # end if
            # end with

            if vid is not None:
                with self._property_lock:
                    self._vid = vid
                # end with
                return vid
            # end if
        # end if

        with self._property_lock:
            return self._vid
        # end with
    # end def property getter vid

    @vid.setter
    def vid(self, vid):
        """
        DEPRECATED

        Property setter of ``vid``. This attribute is changed to a property to have it coincide with the
        attribute ``vid`` of the ``LogiusbDevice``. This property is then read only but to be backward compatible,
        the setter is created but does nothing.

        :param vid: ``vid`` value
        :type vid: ``int``
        """
        warn('This property is then read only but to be backward compatible, the setter is created but does nothing. '
             f'vid is NOT set to {vid}', DeprecationWarning)
    # end def property setter vid

    @property
    def pid(self):
        """
        Property getter of ``pid``. This attribute is changed to a property to have it coincide with the
        attribute ``pid`` of the ``LogiusbDevice``. If the ``LogiusbDevice`` is not accessible, the last saved
        value is returned.

        :return: ``pid`` value
        :rtype: ``int``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    pid = logiusb_device.pid
                else:
                    pid = None
                # end if
            # end with

            if pid is not None:
                with self._property_lock:
                    self._pid = pid
                # end with
                return pid
            # end if
        # end if

        with self._property_lock:
            return self._pid
        # end with
    # end def property getter pid

    @pid.setter
    def pid(self, pid):
        """
        DEPRECATED

        Property setter of ``pid``. This attribute is changed to a property to have it coincide with the
        attribute ``pid`` of the ``LogiusbDevice``. This property is then read only but to be backward compatible,
        the setter is created but does nothing.

        :param pid: ``pid`` value
        :type pid: ``int``
        """
        warn('This property is then read only but to be backward compatible, the setter is created but does nothing. '
             f'pid is NOT set to {pid}', DeprecationWarning)
    # end def property setter pid

    @property
    def connected(self):
        """
        Property getter of ``connected``. This attribute is changed to a property to have it coincide with the
        attribute ``attached`` of the ``LogiusbDevice``. If the ``LogiusbDevice`` is not accessible, the last saved
        value is returned.

        :return: ``connected`` value
        :rtype: ``bool``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    connected = logiusb_device.attached
                else:
                    connected = False
                # end if
            # end with

            if not connected:
                self.logiusb_device = None
            # end if
        else:
            connected = False
        # end if

        return connected
    # end def property getter connected

    @connected.setter
    def connected(self, connected):
        """
        DEPRECATED

        Property setter of ``connected``. This attribute is changed to a property to have it coincide with the
        attribute ``attached`` of the ``LogiusbDevice``. This property is then read only but to be backward compatible,
        the setter is created but does nothing.

        :param connected: ``connected`` value
        :type connected: ``bool``
        """
        warn('This property is then read only but to be backward compatible, the setter is created but does nothing. '
             f'connected is NOT set to {connected}', DeprecationWarning)
    # end def property setter connected

    @property
    def speed(self):
        """
        Property getter of ``speed``. This attribute is changed to a property to have it coincide with the
        attribute ``speed`` of the ``LogiusbDevice``. This property is read-only (meaning it has no setter function).
        This is the same as the value ``logiusb_device.speed``.

        :return: ``speed`` value
        :rtype: ``LogiusbDeviceSpeed`` or ``int``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    speed = logiusb_device.speed
                else:
                    speed = None
                # end if
            # end with

            if speed is not None:
                with self._property_lock:
                    self._speed = speed
                # end with
                return speed
            # end if
        # end if

        with self._property_lock:
            return self._speed
        # end with
    # end def property getter speed

    @property
    def address(self):
        """
        Property getter of ``address``. This attribute is changed to a property to have it coincide with the
        attribute ``address`` of the ``LogiusbDevice``. This property is read-only (meaning it has no setter function).
        This is the same as the value ``logiusb_device.address``.

        :return: ``address`` value
        :rtype: ``int``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    address = logiusb_device.address
                else:
                    address = None
                # end if
            # end with

            if address is not None:
                with self._property_lock:
                    self._address = address
                # end with
                return address
            # end if
        # end if

        with self._property_lock:
            return self._address
        # end with
    # end def property getter address

    @property
    def device_descriptor(self):
        """
        Property getter of ``device_descriptor``. This attribute is changed to a property to have it coincide with the
        attribute ``device_descriptor`` of the ``LogiusbDevice``. If the ``LogiusbDevice`` is not accessible, the last
        saved value is returned.

        :return: ``device_descriptor`` value
        :rtype: ``LogiusbDeviceDescriptor`` or ``None``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    device_descriptor = logiusb_device.device_descriptor
                else:
                    device_descriptor = None
                # end if
            # end with

            if device_descriptor is not None:
                with self._property_lock:
                    self._device_descriptor = device_descriptor
                # end with
                return device_descriptor
            # end if
        # end if

        with self._property_lock:
            return self._device_descriptor
        # end with
    # end def property getter device_descriptor

    @property
    def active_configuration(self):
        """
        Property getter of ``active_configuration``. This attribute is changed to a property to have it coincide with
        the attribute ``active_config`` of the ``LogiusbDevice``. If the ``LogiusbDevice`` is not accessible, the last
        saved value is returned.

        :return: ``active_configuration`` value
        :rtype: ``LogiusbDeviceDescriptor``
        """
        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed:
                    active_configuration = logiusb_device.active_config
                else:
                    active_configuration = None
                # end if
            # end with

            if active_configuration is not None:
                with self._property_lock:
                    self._active_configuration = active_configuration
                # end with
                return active_configuration
            # end if
        # end if

        with self._property_lock:
            return self._active_configuration
        # end with
    # end def property getter active_configuration

    def get_manufacturer_string(self):
        """
        Get USB Manufacturer String. The default value if it has never been read and/or it cannot be read on the
        device (no capability or unplugged for example) is "NOT FOUND".

        :return: USB Manufacturer String
        :rtype: ``str``
        """
        i_manufacturer = None

        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed and logiusb_device.is_open and \
                        logiusb_device.device_descriptor.i_manufacturer != 0:
                    i_manufacturer = logiusb_device.device_descriptor.i_manufacturer
                # end if
            # end with
        # end if

        if i_manufacturer is not None:
            return logiusb_device.get_ascii_string_descriptor(i_manufacturer)
        else:
            return LogiusbUtilsConstant.NOT_FOUND_STRING
        # end if
    # end def get_manufacturer_string

    def get_product_string(self):
        """
        Get USB Product String. The default value if it has never been read and/or it cannot be read on the
        device (no capability or unplugged for example) is "NOT FOUND".

        :return: USB Product String
        :rtype: ``str``
        """
        i_product = None

        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed and logiusb_device.is_open and \
                        logiusb_device.device_descriptor.i_product != 0:
                    i_product = logiusb_device.device_descriptor.i_product
                # end if
            # end with
        # end if

        if i_product is not None:
            return logiusb_device.get_ascii_string_descriptor(i_product)
        else:
            return LogiusbUtilsConstant.NOT_FOUND_STRING
        # end if
    # end def get_product_string

    def get_serial_number_string(self):
        """
        Get USB Serial number String. The default value if it has never been read and/or it cannot be read on the
        device (no capability or unplugged for example) is "NOT FOUND".

        :return: USB Product String
        :rtype: ``str``
        """
        i_serial_number = None

        with self._property_lock:
            logiusb_device = self._logiusb_device
        # end with

        if logiusb_device is not None:
            with logiusb_device:
                if not logiusb_device.is_doomed and logiusb_device.is_open and \
                        logiusb_device.device_descriptor.i_serial_number != 0:
                    i_serial_number = logiusb_device.device_descriptor.i_serial_number
                # end if
            # end with
        # end if

        if i_serial_number is not None:
            return logiusb_device.get_ascii_string_descriptor(i_serial_number)
        else:
            return LogiusbUtilsConstant.NOT_FOUND_STRING
        # end if
    # end def get_serial_number_string

    def get_basic_reader_name(self):
        # See ``UsbContextDevice.get_basic_reader_name``
        with self._property_lock:
            reader_name = self._reader_name
        # end with

        # Remove the potential doomed information from the name
        if READER_NAME_ADDON_FOR_DOOMED_DEVICE in reader_name:
            return reader_name[:-len(READER_NAME_ADDON_FOR_DOOMED_DEVICE)]
        # end if

        return reader_name
        # end with
    # end def get_basic_reader_name

    def get_device_address(self):
        # See ``UsbContextDevice.get_device_address``
        with self._property_lock:
            return self.address
        # end with
    # end def get_device_address
# end class LogiusbUsbContextDevice


class LogiusbUsbContext(UsbContext):
    """
    Allow the manipulation of a USB Context via Logiusb.

    USB context is cleaned at the destruction of the instance (see ``TransportContext.__del__``).
    """
    USB_CONTEXT_DEVICE_CLASS = LogiusbUsbContextDevice
    ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY = True  # Hotplug capability
    TRANSFER_TIMEOUT = 1  # In seconds

    def __init__(self, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        # See ``UsbContext.__init__``
        self._logiusb_context = None
        self._usb_context_devices = None
        self._threaded_executor = None
        self._executor_thread = None
        self._device_endpoint_task_dict = RLockedDict()
        self._hotplug_callback = None

        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        trace_level = TRACE_LOGGER.get_trace_level(subscription_owner=self)

        if trace_level == TraceLevel.EXTRA_DEBUG:
            log_level = LogiusbLogLevel.LOG_LEVEL_MAX_SIZE
        elif trace_level > TraceLevel.NO_TRACE:
            log_level = LogiusbLogLevel.LOG_LEVEL_ERROR
        else:
            log_level = LogiusbLogLevel.LOG_LEVEL_NONE
        # end if
        LogiusbUsbContext.CLASS_METHOD_TRACE_LEVEL = trace_level

        self._logiusb_context = LogiusbContext(log_level=log_level)
        self._hotplug_callback = self.get_hotplug_callback()

        # atexit register
        register(self.clean_up)
    # end def __init__

    def clean_up(self):
        """
        Clean up callback for when python is exiting
        """
        try:
            self._force_kill_executor_thread()
        finally:
            self._usb_context_devices = None
            self._threaded_executor = None
            self._executor_thread = None
            self.is_open = False
        # end try
    # end def clean_up

    def __del__(self):
        # noinspection PyBroadException
        try:
            # See ``TransportContext.__del__``
            super().__del__()
        except Exception:
            pass
        # end try

        if self._logiusb_context is not None:
            # Close (destroy) the USB context
            self._logiusb_context.external_hotplug_callback = None
            self._logiusb_context.close()
            self._logiusb_context = None
        # end if
    # end def __del__

    @classmethod
    def get_logiusb_log_level_from_class_log_level(cls):
        """
        Get the Logiusb log level from the value of the class variable ``CLASS_METHOD_TRACE_LEVEL``
        """
        if cls.CLASS_METHOD_TRACE_LEVEL == TraceLevel.EXTRA_DEBUG:
            return LogiusbLogLevel.LOG_LEVEL_MAX_SIZE
        elif cls.CLASS_METHOD_TRACE_LEVEL > TraceLevel.NO_TRACE:
            return LogiusbLogLevel.LOG_LEVEL_ERROR
        else:
            return LogiusbLogLevel.LOG_LEVEL_NONE
        # end if
    # end def get_logiusb_log_level_from_class_log_level

    @staticmethod
    def get_driver_info():
        # See ``UsbContext.get_driver_info``
        return str(LogiusbContext(
            log_level=LogiusbUsbContext.get_logiusb_log_level_from_class_log_level()).get_version())
    # end def get_driver_info

    @classmethod
    def get_plugged_devices(cls, vid=None, pid=None):
        # See ``UsbContext.get_plugged_devices``
        log_owner = DummyOwner()
        TRACE_LOGGER.subscribe(
            subscription_owner=log_owner, trace_level=cls.CLASS_METHOD_TRACE_LEVEL,
            trace_file_name=cls.CLASS_METHOD_TRACE_FILE_NAME, trace_name=f"{cls.__name__}.get_plugged_devices")

        context = LogiusbContext(log_level=cls.get_logiusb_log_level_from_class_log_level())

        with context.opened():
            vid, pid, str_vid, str_pid = cls._get_str_vid_pid(vid, pid)

            vid = [None] if vid is None else vid
            pid = [None] if pid is None else pid

            already_added_devices = []
            devices_found = []
            for vendor_id in vid:
                for product_id in pid:
                    context_devices = context.get_device_list(vid=vendor_id, pid=product_id)
                    for device in context_devices:
                        if device.attached and device not in already_added_devices:
                            with device.opened():
                                device_found = LogiusbUsbContextDevice(logiusb_device=device)
                                TRACE_LOGGER.log_trace(subscription_owner=log_owner,
                                                       message=f"Found device on {device_found.reader_name}, "
                                                               f"VID(0x{device_found.vid:04X}) and "
                                                               f"PID(0x{device_found.pid:04X})",
                                                       trace_level=TraceLevel.DEBUG)
                                devices_found.append(device_found)
                            # end with
                            already_added_devices.append(device)
                        # end if
                    # end for
                # end for
            # end for

            TRACE_LOGGER.log_trace(subscription_owner=log_owner,
                                   message=f"Found {len(devices_found)} plugged devices according to "
                                           f"filter vid({str_vid}) and pid({str_pid})",
                                   trace_level=TraceLevel.DEBUG)

            return devices_found
        # end with
    # end def get_plugged_devices

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self):
        # See ``TransportContext.open``
        if self.is_open:
            return
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Opening {self.__class__.__name__}...", trace_level=TraceLevel.DEBUG)

        # Get a copy of the device cache using device_cache read only property
        self._usb_context_devices = self.__class__.device_cache
        try:
            self._logiusb_context.external_hotplug_callback = self._hotplug_callback
            self._logiusb_context.open()
            self._threaded_executor = ThreadedExecutor(
                tasks=[], max_threads=MAX_THREADS, name="Logiusb USB Context Executor", run_until_stop=True)
            self._executor_thread = Thread(target=ThreadedExecutor.execute, args=(self._threaded_executor,))
            # The thread is a daemon: It will NOT prevent the main thread from dying
            self._executor_thread.setDaemon(True)
            self._executor_thread.start()
        except Exception:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Exception while opening. Clean attributes. Exception:\n"
                        f"{TracebackLogWrapper.get_exception_stack()}",
                trace_level=TraceLevel.ERROR)
            self._usb_context_devices = None
            self._force_kill_executor_thread()
            self._threaded_executor = None
            self._executor_thread = None
            raise
        # end try

        self.is_open = True

        self.update_device_list()
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See ``TransportContext.close``
        if not self.is_open or self._usb_context_devices is None:
            return
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Closing {self.__class__.__name__}...", trace_level=TraceLevel.DEBUG)

        try:
            for device in self._usb_context_devices:
                # noinspection PyBroadException
                try:
                    self.close_device(usb_context_device=device)
                except Exception:
                    pass
                finally:
                    self._stop_all_polling_thread_of_device(usb_context_device=device)
                    with self._device_endpoint_task_dict.try_lock_do_anyway():
                        self._device_endpoint_task_dict.pop(device.get_basic_reader_name(), None)
                    # end with
                    device.logiusb_device = None
                # end try
            # end for
            if self._executor_thread.is_alive():
                self._threaded_executor.stop()
                self._executor_thread.join(1)
            # end if
        finally:
            try:
                self._logiusb_context.close()
            finally:
                self._logiusb_context.external_hotplug_callback = None
                self._usb_context_devices = None
                self._force_kill_executor_thread()
                self._threaded_executor = None
                self._executor_thread = None
                self.is_open = False
            # end try
        # end try
    # end def close

    def reset(self):
        # See ``TransportContext.reset``
        self.close()
        self.open()
    # end def reset

    def open_device(self, usb_context_device):
        """
        Open a context device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        """
        with usb_context_device.lock_opening_closing:
            if usb_context_device.logiusb_device is not None and usb_context_device.logiusb_device.is_open:
                return
            # end if

            self._sanity_check(usb_context_device=usb_context_device)

            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Opening {usb_context_device.reader_name}...",
                trace_level=TraceLevel.DEBUG)

            with self._device_endpoint_task_dict:
                self._device_endpoint_task_dict[usb_context_device.get_basic_reader_name()] = {}
            # end with

            usb_context_device.logiusb_device.open()

            try:
                # Configuration Descriptor
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Active Configuration Descriptor: {usb_context_device.logiusb_device.active_config}",
                    trace_level=TraceLevel.EXTRA_DEBUG)

                kernel_driver_was_detached = False
                if platform == 'linux':
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Detach the kernel driver from all interfaces (if needed)",
                        trace_level=TraceLevel.DEBUG)

                    # Start with detaching the kernel driver for all interfaces
                    for interface in usb_context_device.logiusb_device.active_config.interfaces:
                        descriptor = interface.interface_descriptor
                        #  Check whether a Kernel driver is active
                        if usb_context_device.logiusb_device.is_kernel_driver_attached(
                                interface_number=descriptor.b_interface_number):
                            # Ask Kernel driver to detach
                            usb_context_device.logiusb_device.detach_kernel_driver(
                                interface_number=descriptor.b_interface_number)
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message=f"Detach kernel driver for Interface ID {descriptor.b_interface_number}",
                                trace_level=TraceLevel.DEBUG)
                            kernel_driver_was_detached = True
                        # end if
                    # end for

                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"The kernel driver is detached from all interfaces",
                        trace_level=TraceLevel.DEBUG)
                # end if

                if kernel_driver_was_detached:
                    # Workaround: For Wakanda device, the soft usb reset creates an issue on HIDpp and HID report
                    if usb_context_device.speed != LogiusbDeviceSpeed.DEVICE_SPEED_HIGH:
                        usb_context_device.logiusb_device.reset()
                        # Give time to the USB connection to be back online, this number is random and should maybe
                        # be improved
                        sleep(.2)
                    # end if
                # end if

                usb_context_device.interface_list = []
                for interface in usb_context_device.logiusb_device.active_config.interfaces:
                    descriptor = interface.interface_descriptor
                    protocol = descriptor.b_interface_protocol if descriptor.b_interface_number <= 2 \
                        else descriptor.b_interface_number
                    endpoints = []
                    for endpoint in interface.endpoint_descriptors:
                        endpoints.append((endpoint.b_endpoint_address, endpoint.w_max_packet_size))
                    # end for
                    usb_context_device.interface_list.append((descriptor.b_interface_number, protocol, endpoints))

                    # Claim (= get exclusive access to) given interface number.
                    # Required to receive/send data.
                    usb_context_device.logiusb_device.claim_interface(interface_number=descriptor.b_interface_number)
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Claim Interface ID {descriptor.b_interface_number}",
                        trace_level=TraceLevel.DEBUG)
                # end for
            except Exception:
                # noinspection PyBroadException
                try:
                    if usb_context_device.logiusb_device.is_open:
                        usb_context_device.logiusb_device.close()
                    # end if
                finally:
                    if usb_context_device.interface_list is not None:
                        usb_context_device.interface_list.clear()
                        usb_context_device.interface_list = None
                    # end if
                    with self._device_endpoint_task_dict:
                        self._device_endpoint_task_dict.pop(usb_context_device.get_basic_reader_name(), None)
                    # end with
                # end try
                raise
            # end try

            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"{usb_context_device.reader_name} open", trace_level=TraceLevel.INFO)
        # end with
    # end def open_device

    def close_device(self, usb_context_device):
        """
        Close a context device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        """
        with usb_context_device.lock_opening_closing:
            if usb_context_device.logiusb_device is None or not usb_context_device.logiusb_device.is_open:
                return
            # end if

            try:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self, message=f"Closing {usb_context_device.reader_name}...",
                    trace_level=TraceLevel.DEBUG)

                self._sanity_check_device_open(usb_context_device=usb_context_device)

                # Stop all transfers
                self.stop_interrupt_read_polling(usb_context_device=usb_context_device)

                if usb_context_device.interface_list is not None:
                    for interface_number, _, _ in usb_context_device.interface_list:
                        # noinspection PyBroadException
                        try:
                            usb_context_device.logiusb_device.release_interface(interface_number=interface_number)
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self, message=f"Release Interface ID {interface_number}",
                                trace_level=TraceLevel.DEBUG)
                        except Exception as e:
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message=f"Could not release Interface ID {interface_number}: {e}",
                                trace_level=TraceLevel.ERROR)
                        # end try
                    # end for

                    if platform == 'linux' and REATTACH_KERNEL_DRIVER:
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Attach the kernel driver from all interfaces (if needed)",
                            trace_level=TraceLevel.DEBUG)

                        for interface_number, _, _ in usb_context_device.interface_list:
                            # Check whether a Kernel driver was previously active
                            # noinspection PyBroadException
                            try:
                                kernel_active = usb_context_device.logiusb_device.is_kernel_driver_attached(
                                    interface_number=interface_number)
                            except Exception:
                                kernel_active = True
                            # end try
                            if not kernel_active:
                                # noinspection PyBroadException
                                try:
                                    # Ask Kernel driver to attach
                                    usb_context_device.logiusb_device.attach_kernel_driver(
                                        interface_number=interface_number)
                                    TRACE_LOGGER.log_trace(
                                        subscription_owner=self,
                                        message=f"Attach kernel driver for Interface ID {interface_number}",
                                        trace_level=TraceLevel.DEBUG)
                                except Exception as e:
                                    TRACE_LOGGER.log_trace(
                                        subscription_owner=self,
                                        message="Could not attach kernel driver for Interface ID "
                                                f"{interface_number}: {e}",
                                        trace_level=TraceLevel.ERROR)
                                # end try
                            # end if
                        # end for

                        TRACE_LOGGER.log_trace(
                            subscription_owner=self, message=f"The kernel driver is detached from all interfaces",
                            trace_level=TraceLevel.DEBUG)
                    # end if
                # end if
            finally:
                # noinspection PyBroadException
                try:
                    usb_context_device.logiusb_device.close()
                except Exception as e:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Could not close device handle {usb_context_device.vid}:{usb_context_device.pid}: {e}",
                        trace_level=TraceLevel.ERROR)
                # end try

                if usb_context_device.interface_list is not None:
                    usb_context_device.interface_list.clear()
                    usb_context_device.interface_list = None
                # end if

                with self._device_endpoint_task_dict:
                    self._device_endpoint_task_dict.pop(usb_context_device.get_basic_reader_name(), None)
                # end with
            # end try
        # end with

        TRACE_LOGGER.log_trace(subscription_owner=self, message=f"{usb_context_device.reader_name} closed",
                               trace_level=TraceLevel.INFO)
    # end def close_device

    def control_write(self, usb_context_device, bm_request_type, b_request, w_value, w_index, data,
                      timeout=UsbContext.GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        """
        Perform a control write on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param bm_request_type: Request type bitmask
        :type bm_request_type: ``int``
        :param b_request: The meaning of this parameter is request type dependent
        :type b_request: ``int``
        :param w_value: The meaning of this parameter is request type dependent
        :type w_value: ``int``
        :param w_index: The meaning of this parameter is request type dependent
        :type w_index: ``int``
        :param data: Data to write
        :type data: ``UsbMessage``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Is the action blocking or not, UNUSED IN THIS TYPE OF CONTEXT (BLOCKING BY DEFAULT) - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The number of bytes sent
        :rtype: ``int``
        """
        self._sanity_check_device_open(usb_context_device)

        if trace_owner is None:
            trace_owner = self
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Control write on interface 0x{w_index:02X} started",
            trace_level=TraceLevel.DEBUG)

        try:
            transfer = usb_context_device.logiusb_device.create_control_write_transfer(
                bm_request_type=bm_request_type, b_request=b_request, w_value=w_value, w_index=w_index,
                data=list(data.data))
            transfer.synchronous_submit(timeout=LogiusbTransfer.GENERIC_1S_TIMEOUT)
        except LogiusbException as logiusb_exception:
            self.transfer_exception_treatment(logiusb_exception=logiusb_exception)
        # end try

        # Update the timestamp of the message sent
        data.timestamp = perf_counter_ns()

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Control write on interface 0x{w_index:02X}: {data.data} "
                    f"at {data.timestamp}ns",
            trace_level=TraceLevel.INFO)

        return len(data.data)
    # end def control_write

    def control_read(self, usb_context_device, bm_request_type, b_request, w_value, w_index, w_length,
                     timeout=UsbContext.GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        """
        Perform a control read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param bm_request_type: Request type bitmask
        :type bm_request_type: ``int``
        :param b_request: The meaning of this parameter is request type dependent
        :type b_request: ``int``
        :param w_value: The meaning of this parameter is request type dependent
        :type w_value: ``int``
        :param w_index: The meaning of this parameter is request type dependent
        :type w_index: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Is the action blocking or not, UNUSED IN THIS TYPE OF CONTEXT (BLOCKING BY DEFAULT) - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The message read
        :rtype: ``UsbMessage``
        """
        self._sanity_check_device_open(usb_context_device)

        if trace_owner is None:
            trace_owner = self
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Control read on interface 0x{w_index:02X} started",
            trace_level=TraceLevel.DEBUG)

        receiving_queue = Queue()
        try:
            transfer = usb_context_device.logiusb_device.create_control_read_transfer(
                bm_request_type=bm_request_type, b_request=b_request, w_value=w_value, w_index=w_index,
                w_length=w_length, receiving_queue=receiving_queue)

            transfer.synchronous_submit(timeout=LogiusbTransfer.GENERIC_1S_TIMEOUT)
        except LogiusbException as logiusb_exception:
            self.transfer_exception_treatment(logiusb_exception=logiusb_exception)
        # end try

        control_data = receiving_queue.get(timeout=timeout)
        control_data = UsbMessage(
            data=HexList(control_data[LogiusbPacketIndex.MESSAGE_INDEX][LogiusbDefines.TRANSFER_CONTROL_SETUP_SIZE:]),
            timestamp=int(control_data[LogiusbPacketIndex.TIMESTAMP_INDEX]))

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Control read on interface 0x{w_index:02X}: {control_data.data} "
                    f"at {control_data.timestamp}ns",
            trace_level=TraceLevel.INFO)

        return control_data
    # end def control_read

    def bulk_write(self, usb_context_device, endpoint, data, timeout=0, blocking=False, trace_owner=None):
        """
        Perform a bulk write on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to send the data to
        :type endpoint: ``int``
        :param data: Data to write
        :type data: ``UsbMessage``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Is the action blocking or not, UNUSED IN THIS TYPE OF CONTEXT (BLOCKING BY DEFAULT) - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The number of bytes sent
        :rtype: ``int``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("bulk_write() method should be implemented before use")
    # end def bulk_write

    def bulk_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        """
        Perform a bulk read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from
        :type endpoint: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Is the action blocking or not, UNUSED IN THIS TYPE OF CONTEXT (BLOCKING BY DEFAULT) - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The message read
        :rtype: ``UsbMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("bulk_read() method should be implemented before use")
    # end def bulk_read

    def interrupt_write(self, usb_context_device, endpoint, data, timeout=0, blocking=False, trace_owner=None):
        """
        Perform an interrupt write on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to send the data to
        :type endpoint: ``int``
        :param data: Data to write
        :type data: ``UsbMessage``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Is the action blocking or not, UNUSED IN THIS TYPE OF CONTEXT (BLOCKING BY DEFAULT) - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The number of bytes sent
        :rtype: ``int``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        self._sanity_check_device_open(usb_context_device)

        if trace_owner is None:
            trace_owner = self
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Interrupt write on endpoint 0x{endpoint:02X} started",
            trace_level=TraceLevel.DEBUG)

        try:
            transfer = usb_context_device.logiusb_device.create_interrupt_write_transfer(
                endpoint_address=endpoint, data=bytes(list(data.data)))
            transfer.synchronous_submit(timeout=LogiusbTransfer.GENERIC_1S_TIMEOUT)
        except LogiusbException as logiusb_exception:
            self.transfer_exception_treatment(logiusb_exception=logiusb_exception)
        # end try

        # Update the timestamp of the message sent
        data.timestamp = perf_counter_ns()

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Interrupt write on endpoint 0x{endpoint:02X}: {data.data} "
                    f"at {data.timestamp}ns",
            trace_level=TraceLevel.INFO)

        return len(data.data)
    # end def interrupt_write

    def interrupt_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        """
        Perform an interrupt read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from
        :type endpoint: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Is the action blocking or not, UNUSED IN THIS TYPE OF CONTEXT (BLOCKING BY DEFAULT) - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The message read
        :rtype: ``UsbMessage``
        """
        self._sanity_check_device_open(usb_context_device)

        if trace_owner is None:
            trace_owner = self
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Interrupt read on endpoint 0x{endpoint:02X} started",
            trace_level=TraceLevel.EXTRA_DEBUG)

        receiving_queue = Queue()
        try:
            transfer = usb_context_device.logiusb_device.create_interrupt_read_transfer(
                packet_maximum_length=w_length, endpoint_address=endpoint, receiving_queue=receiving_queue)

            transfer.synchronous_submit(timeout=LogiusbTransfer.GENERIC_1S_TIMEOUT)
        except LogiusbException as logiusb_exception:
            self.transfer_exception_treatment(logiusb_exception=logiusb_exception)
        # end try

        interrupt_data = receiving_queue.get(timeout=timeout)
        interrupt_data = UsbMessage(
            data=HexList(interrupt_data[LogiusbPacketIndex.MESSAGE_INDEX]),
            timestamp=int(interrupt_data[LogiusbPacketIndex.TIMESTAMP_INDEX]))

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Interrupt read on endpoint 0x{endpoint:02X}: "
                    f"{interrupt_data.data} at {interrupt_data.timestamp}ns",
            trace_level=TraceLevel.INFO)
        return interrupt_data
    # end def interrupt_read

    def start_interrupt_read_polling(self, usb_context_device, endpoint, w_length, time_stamped_msg_queue=None,
                                     trace_name=None, callback=None, discard_report=False):
        """
        Start a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from
        :type endpoint: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param time_stamped_msg_queue: Queue to get all USB message received, the same queue can only be used for
                                       one endpoint - OPTIONAL
        :type time_stamped_msg_queue: ``Queue`` or ``None``
        :param trace_name: Trace name for this action, if ``None`` the trace name or ``self`` will be used - OPTIONAL
        :type trace_name: ``str`` or ``None``
        :param callback: Callback to use, it will change add it in the ``usb_context_device``.
                         If ``None``, it will be ignored - OPTIONAL
        :type callback: ``Callable`` or ``None``
        :param discard_report: Flag indicating to discard any message received on this endpoint - OPTIONAL
        :type discard_report: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        with self._device_endpoint_task_dict:
            self._sanity_check_device_open(usb_context_device=usb_context_device)

            if callback is not None:
                usb_context_device.set_transfer_callback(transfer_type_key=endpoint, callback=callback)
            # end if

            endpoint_task_dict = self._device_endpoint_task_dict[usb_context_device.get_basic_reader_name()]

            if endpoint in endpoint_task_dict.keys():
                raise TransportContextException(TransportContextException.Cause.ACTION_ALREADY_DONE,
                                                f"Polling task on endpoint 0x{endpoint:02X} is already started")
            # end if

            task = InterruptPollingTask(
                logiusb_context=self, logiusb_context_device=usb_context_device, packet_maximum_length=w_length,
                endpoint_address=endpoint, time_stamped_msg_queue=time_stamped_msg_queue,
                trace_name=trace_name, discard_report=discard_report)
            self._threaded_executor.add_task(task)

            endpoint_task_dict[endpoint] = task
        # end with
    # end def start_interrupt_read_polling

    def stop_interrupt_read_polling(self, usb_context_device, endpoint=None):
        """
        Stop a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from, if None stop all interrupt polling for the device - OPTIONAL
        :type endpoint: ``int`` or ``None``
        """
        with self._device_endpoint_task_dict:
            if endpoint is None:
                self._stop_all_polling_thread_of_device(usb_context_device=usb_context_device)
            else:
                interface_tasks = self._device_endpoint_task_dict.get(usb_context_device.get_basic_reader_name(), None)

                if interface_tasks is None:
                    return
                # end if

                task = interface_tasks.pop(endpoint, None)

                if task is not None:
                    task.stop_task()
                # end if
            # end if
        # end with
    # end def stop_interrupt_read_polling

    def mute_interrupt_read_polling(self, usb_context_device, endpoint):
        """
        Mute a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from, if None stop all interrupt polling for the device - OPTIONAL
        :type endpoint: ``int`` or ``None``
        """
        with self._device_endpoint_task_dict:
            interface_tasks = self._device_endpoint_task_dict.get(usb_context_device.get_basic_reader_name(), None)

            if interface_tasks is None:
                return
            # end if

            if endpoint in interface_tasks.keys():
                interface_tasks[endpoint].mute_task()
            # end if
        # end with
    # end def mute_interrupt_read_polling

    def unmute_interrupt_read_polling(self, usb_context_device, endpoint):
        """
        Unmute a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from, if None stop all interrupt polling for the device - OPTIONAL
        :type endpoint: ``int`` or ``None``
        """
        with self._device_endpoint_task_dict:
            interface_tasks = self._device_endpoint_task_dict.get(usb_context_device.get_basic_reader_name(), None)

            if interface_tasks is None:
                return
            # end if

            if endpoint in interface_tasks.keys():
                interface_tasks[endpoint].unmute_task()
            # end if
        # end with
    # end def unmute_interrupt_read_polling

    def get_ascii_string_descriptor(self, usb_context_device, descriptor):
        """
        Get the string description of the USB device defined descriptor.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        :param descriptor: String descriptor (values can be found in ``StringDescriptor``):

                             * 1 : Manufacturer
                             * 2 : Product
                             * 3 : Serial Number
        :type descriptor: ``int``

        :return: The descriptor string
        :rtype: ``str``
        """
        self._sanity_check_device_open(usb_context_device=usb_context_device)
        string_descriptor = usb_context_device.logiusb_device.get_ascii_string_descriptor(descriptor=descriptor)
        return string_descriptor
    # end def get_ascii_string_descriptor

    def get_device_info(self, usb_context_device):
        """
        Get the string description of the Device info, containing:

        * USB.VendorID     : 0x....
        * USB.ProductID    : 0x....
        * USB.bcdDevice    : 0x....
        * Manufacturer     : ...
        * Product          : ...
        * Serial Number    : 0x........

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``

        :return: The descriptor string
        :rtype: ``str``
        """
        self._sanity_check_device_open(usb_context_device=usb_context_device)

        device_info = ""
        device_info += f"USB.VendorID     : 0x{usb_context_device.vid:04X}\n"
        device_info += f"USB.ProductID    : 0x{usb_context_device.pid:04X}\n"
        device_info += f"USB.bcdDevice    : 0x{usb_context_device.device_descriptor.bcd_device:04X}\n"
        device_info += f"Manufacturer     : {usb_context_device.get_manufacturer_string()}\n"
        device_info += f"Product          : {usb_context_device.get_product_string()}\n"
        device_info += f"Product          : {usb_context_device.get_product_string()}\n"
        device_info += f"Serial Number    : 0x{usb_context_device.get_serial_number_string().replace(' ', '')}"

        return device_info
    # end def get_device_info

    def update_device_list(self):
        # See ``UsbContext.update_device_list``
        if not self.is_open:
            return
        # end if

        self._sanity_check()

        current_plugged_in_device = self._logiusb_context.get_device_list()

        # Put all devices back to not connected and not context specific device structure associated
        usb_context_devices = {}
        for usb_context_device in self._usb_context_devices:
            # The connected = False is done inside the property setter of logiusb_device
            usb_context_device.logiusb_device = None
            usb_context_devices[usb_context_device.reader_name] = usb_context_device
        # end for

        # Update all connected devices
        for logiusb_device in current_plugged_in_device:
            with logiusb_device:
                if logiusb_device.is_doomed:
                    continue
                # end if
                ports = "->".join([str(i) for i in logiusb_device.get_device_port_list()])
                reader_name = f"Bus {logiusb_device.bus} Device {ports}"
                if reader_name in usb_context_devices.keys():
                    usb_context_devices[reader_name].logiusb_device = logiusb_device
                # end if
            # end with
        # end for
    # end def update_device_list

    def get_hotplug_callback(self):
        weak_self = ref(self)

        def hotplug_callback(logiusb_device_popped_key, logiusb_device_found):
            context_python_object = weak_self()
            if context_python_object is None:
                return
            # end if

            if logiusb_device_popped_key is not None:
                # noinspection PyProtectedMember
                for device in context_python_object._usb_context_devices:
                    if device.logiusb_device_key == logiusb_device_popped_key:
                        # noinspection PyProtectedMember
                        with self._device_endpoint_task_dict.try_lock_do_anyway():
                            context_python_object._stop_all_polling_thread_of_device(usb_context_device=device)
                            # noinspection PyProtectedMember
                            context_python_object._device_endpoint_task_dict.pop(device.get_basic_reader_name(), None)
                        # end with
                        device.logiusb_device = None
                        device.wait_for_disconnection_event.set()
                        break
                    # end if
                # end for
            # end if

            if logiusb_device_found is not None:
                ports = "->".join([str(i) for i in logiusb_device_found.get_device_port_list()])
                reader_name = f"Bus {logiusb_device_found.bus} Device {ports}"
                # noinspection PyProtectedMember
                for device in context_python_object._usb_context_devices:
                    if device.get_basic_reader_name() == reader_name:
                        device.logiusb_device = logiusb_device_found
                        device.wait_for_connection_event.set()
                        break
                    # end if
                # end for
            # end if
        # end def hotplug_callback

        return hotplug_callback
    # end def get_hotplug_callback

    def _sanity_check(self, usb_context_device=None):
        """
        Check if the context is open and if a context device (if given) is connected.

        :param usb_context_device: The USB device to check - OPTIONAL
        :type usb_context_device: ``LogiusbUsbContextDevice``

        :raise ``TransportContextException``: If the context is not open or if the device is not connected nor found
        """
        super()._sanity_check(usb_context_device=usb_context_device)

        if usb_context_device is not None:
            if usb_context_device.logiusb_device is None:
                raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_FOUND)
            # end if
            if usb_context_device.logiusb_device.is_doomed:
                raise TransportContextException(
                    TransportContextException.Cause.DEVICE_NOT_FOUND, "Logiusb device is doomed")
            # end if
        # end if
    # end def _sanity_check

    def _sanity_check_device_open(self, usb_context_device):
        """
        Check if the context is open and if a context device is connected and found.

        :param usb_context_device: The USB device to check
        :type usb_context_device: ``LogiusbUsbContextDevice``

        :raise ``TransportContextException``: If the context is not open or if the device is not connected nor found
        """
        self._sanity_check(usb_context_device=usb_context_device)

        if not usb_context_device.logiusb_device.is_open:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_OPEN)
        # end if

        if self._device_endpoint_task_dict.get(usb_context_device.get_basic_reader_name(), None) is None:
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                "The device is open but it seems that the dictionary with its submitted transfers was not created")
        # end if

        if usb_context_device.interface_list is None:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                            "The device is open but it seems that its interface list was not created")
        # end if
    # end def _sanity_check_device_open

    def _stop_all_polling_thread_of_device(self, usb_context_device):
        """
        Stop all polling threads associated to a context device. If this method is called by a thread while already
        called in another thread, it will not be done.

        :param usb_context_device: Context device to use
        :type usb_context_device: ``LogiusbUsbContextDevice``
        """
        # The first part of the method should not be blocked but should be able to block other calls of
        # ``with self._device_endpoint_task_dict``, that is why
        # ``with self._device_endpoint_task_dict.try_lock_do_anyway()`` is used.
        with self._device_endpoint_task_dict.try_lock_do_anyway():
            interface_tasks = self._device_endpoint_task_dict.get(usb_context_device.get_basic_reader_name(), None)

            if not usb_context_device.stopping_all_polling_threads.acquire(blocking=False):
                return
            # end if

            try:
                if interface_tasks is None or len(interface_tasks) == 0:
                    return
                # end if

                # The second part of the method should always block if ``self._device_endpoint_task_dict`` is used
                # somewhere else, that is why ``with self._device_endpoint_task_dict`` is used.
                with self._device_endpoint_task_dict:
                    for task in interface_tasks.values():
                        task.stop_task()
                    # end for
                # end with
            finally:
                usb_context_device.stopping_all_polling_threads.release()
            # end try
        # end with
    # end def _stop_all_polling_thread_of_device

    def _force_kill_executor_thread(self):
        """
        Kill the threaded executor forcefully.
        """
        if self._executor_thread is None or not self._executor_thread.is_alive():
            return
        # end if

        self._threaded_executor.force_kill_all_threads()

        result = pythonapi.PyThreadState_SetAsyncExc(c_long(self._executor_thread.ident), py_object(SystemExit))
        if result == 0:
            raise ValueError("Invalid thread ID")
        elif result > 1:
            pythonapi.PyThreadState_SetAsyncExc(c_long(self._executor_thread.ident), 0)
            raise SystemError('Force kill thread failure: Exception raise failure')
        # end if
    # end def _force_kill_executor_thread

    @staticmethod
    def transfer_exception_treatment(logiusb_exception):
        """
        Encapsulate a ``LogiusbException`` in a ``TransportContextException``.

        :param logiusb_exception: The ``LogiusbException`` to encapsulate
        :type logiusb_exception: ``LogiusbException``

        :raise ``TransportContextException``: The ``TransportContextException`` encapsulating the ``LogiusbException``
        """
        str_exp = str(logiusb_exception)
        if logiusb_exception.get_cause() == LogiusbException.Cause.DOOMED:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE, str(str_exp))
        elif logiusb_exception.get_cause() == LogiusbException.Cause.NOT_OPEN:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_OPEN, str(str_exp))
        elif logiusb_exception.get_cause() == LogiusbException.Cause.TRANSFER_ALREADY_SUBMITTED:
            raise TransportContextException(TransportContextException.Cause.ACTION_ALREADY_DONE, str(str_exp))
        elif logiusb_exception.get_cause() == LogiusbException.Cause.TRANSFER_NOT_SUBMITTED:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INVALID_STATE, str(str_exp))
        elif logiusb_exception.get_cause() == LogiusbException.Cause.TIMEOUT:
            raise TransportContextException(TransportContextException.Cause.TIMEOUT, str(str_exp))
        elif logiusb_exception.get_cause() == LogiusbException.Cause.INVALID_PARAMETER:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INVALID_PARAMETER, str(str_exp))
        elif logiusb_exception.get_cause() == LogiusbException.Cause.LOGIUSB_C_ERROR:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR, str(str_exp))
        else:
            raise
        # end if
    # end def transfer_exception_treatment
# end class LogiusbUsbContext

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
