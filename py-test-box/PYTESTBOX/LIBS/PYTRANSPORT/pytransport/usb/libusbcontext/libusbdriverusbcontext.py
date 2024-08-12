#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.usb.libusbcontext.libusbdriverusbcontext
:brief: LibUSB driver USB context classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/04/28
"""
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from atexit import register
from binascii import hexlify
from ctypes import c_long
from ctypes import py_object
from ctypes import pythonapi
from os import environ
from sys import platform
from threading import RLock
from threading import Thread
from time import perf_counter_ns
from time import sleep
# For some reason pycharm decided not to see it while being used in a docstring (it normally does)
# noinspection PyUnresolvedReferences
from typing import Callable
from typing import List

from pylibrary.system.tracelogger import DummyOwner
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import RLockedDict
from pylibrary.tools.threadutils import ThreadedExecutor
from pylibrary.tools.threadutils import WeakMethod
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pytransport.transportcontext import TransportContextException
from pytransport.usb.libusbcontext.usbtasks import ContextEventHandleTask
from pytransport.usb.libusbcontext.usbtasks import InterruptPollingTask
from pytransport.usb.libusbcontext.usbtasks import MAX_THREADS
from pytransport.usb.libusbcontext.usbtasks import USB_TIMEOUT
from pytransport.usb.usbcontext import StringDescriptor
from pytransport.usb.usbcontext import UsbContext
from pytransport.usb.usbcontext import UsbContextDevice
from pytransport.usb.usbmessage import UsbMessage

# Import libusb python wrapper through pysetup
try:
    # noinspection PyUnresolvedReferences
    import pysetup
    # noinspection PyUnresolvedReferences
    environ['PATH'] = "%s;%s" % (pysetup.LIBUSB, environ['PATH'])
    # noinspection PyUnresolvedReferences
    import usb1
except ImportError:
    pass
# end try


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
HOT_PLUG_EVENT_TO_STR = {
    usb1.HOTPLUG_EVENT_DEVICE_ARRIVED: 'arrived',
    usb1.HOTPLUG_EVENT_DEVICE_LEFT: 'left'
}

TRACE_LOGGER = TraceLogger.get_instance()

USB_TASK_LOCK = RLock()

# Reattach or not the kernel driver when closing a device, by default it is set to False to gain time after
# the first open
REATTACH_KERNEL_DRIVER = False


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------
class LibusbUsbContextDevice(UsbContextDevice):
    """
    USB device structure used in a USB context.
    """

    def __init__(self, reader_name, vid, pid, connected=False,
                 transfer_callbacks=None, libusb_device=None, libusb_device_handle=None):
        """
        :param reader_name: The bus ID and port number as read in the config file, format: Bus X Device Y
        :type reader_name: ``str``
        :param vid: The VID of the device
        :type vid: ``int``
        :param vid: The PID of the device
        :type pid: ``int``
        :param connected: Flag indicating if the device is connected - OPTIONAL
        :type connected: ``bool``
        :param transfer_callbacks: The callbacks that will be used when a transfer is received for each transfer type
                                   (HID mouse, HID keyboard, HID++, etc...), its format is a thread safe dictionary
                                   (the keys are endpoint IDs). If ``None``, it will be set as an
                                   empty thread safe dictionary - OPTIONAL
        :type transfer_callbacks: ``RLockedDict`` or ``None``
        :param libusb_device: Handle of the device after being opened - OPTIONAL
        :type libusb_device: ``usb1.USBDevice`` or ``None``
        :param libusb_device_handle: Handle of the device after being opened - OPTIONAL
        :type libusb_device_handle: ``usb1.USBDeviceHandle`` or ``None``
        """
        super().__init__(
            reader_name=reader_name, vid=vid, pid=pid, connected=connected, transfer_callbacks=transfer_callbacks)

        self._libusb_device = libusb_device
        self._libusb_device_lock = RLock()
        self._libusb_device_handle = libusb_device_handle
        self._libusb_device_handle_lock = RLock()
        self.interface_list = None
    # end def __init__

    @property
    @synchronize_with_object_inner_lock("_libusb_device_lock")
    def libusb_device(self):
        """
        Property getter of ``libusb_device``.

        :return: ``libusb_device`` object
        :rtype: ``usb1.USBDevice`` or ``None``
        """
        return self._libusb_device
    # end def property getter libusb_device

    @libusb_device.setter
    @synchronize_with_object_inner_lock("_libusb_device_lock")
    def libusb_device(self, libusb_device):
        """
        Property setter of ``libusb_device``.

        :param libusb_device: ``libusb_device`` object
        :type libusb_device: ``usb1.USBDevice`` or ``None``
        """
        self._libusb_device = libusb_device
    # end def property setter libusb_device

    @property
    @synchronize_with_object_inner_lock("_libusb_device_handle_lock")
    def libusb_device_handle(self):
        """
        Property getter of ``libusb_device_handle``.

        :return: ``libusb_device_handle`` object
        :rtype: ``usb1.USBDeviceHandle`` or ``None``
        """
        return self._libusb_device_handle
    # end def property getter libusb_device_handle

    @libusb_device_handle.setter
    @synchronize_with_object_inner_lock("_libusb_device_handle_lock")
    def libusb_device_handle(self, libusb_device_handle):
        """
        Property setter of ``libusb_device_handle``.

        :param libusb_device_handle: ``libusb_device_handle`` object
        :type libusb_device_handle: ``usb1.USBDeviceHandle`` or ``None``
        """
        self._libusb_device_handle = libusb_device_handle
    # end def property setter libusb_device_handle

    def get_manufacturer_string(self):
        # See ``UsbContextDevice.get_manufacturer_string``
        return self.libusb_device.getManufacturer()
    # end def get_manufacturer_string

    def get_product_string(self):
        # See ``UsbContextDevice.get_product_string``
        return self.libusb_device.getProduct()
    # end def get_product_string

    def get_serial_number_string(self):
        # See ``UsbContextDevice.get_serial_number_string``
        return NotImplementedError("LibusbUsbContextDevice.get_serial_number_string not implemented yet")
    # end def get_serial_number_string

    def get_device_address(self):
        # See ``UsbContextDevice.get_device_address``
        return self.libusb_device.getDeviceAddress()
    # end def get_device_address
# end class LibusbUsbContextDevice


class LibusbUsbContext(UsbContext):
    """
    Allow the manipulation of a USB Context via libusb1.

    USB context is cleaned at the destruction of the instance (see ``TransportContext.__del__``).
    """
    USB_CONTEXT_DEVICE_CLASS = LibusbUsbContextDevice
    # Hotplug capability is not supported by Libusb Driver
    ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY = False

    def __init__(self, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        # See ``UsbContext.__init__``
        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        self._usb_context_devices = None
        self._libusb_context = None
        self._hotplug_opaque_handle = None  # This handle is only to be used to unregister the hotplug callback
        self._hotplug_callback = WeakMethod(self._hotplug_callback)
        self._hotplug_task = None
        self._threaded_executor = None
        self._executor_thread = None
        self._device_endpoint_task_dict = RLockedDict()

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

        if self._libusb_context is not None:
            # Close (destroy) the USB context
            self._libusb_context.close()
            self._libusb_context = None
        # end if
    # end def __del__

    @staticmethod
    def get_driver_info():
        # See ``UsbContext.get_driver_info``
        return str(usb1.getVersion())
    # end def get_driver_info

    @classmethod
    def get_plugged_devices(cls, vid=None, pid=None):
        # See ``UsbContext.get_plugged_devices``
        log_owner = DummyOwner()
        TRACE_LOGGER.subscribe(subscription_owner=log_owner, trace_level=cls.CLASS_METHOD_TRACE_LEVEL,
                               trace_file_name=cls.CLASS_METHOD_TRACE_FILE_NAME,
                               trace_name="LibusbUsbContext.get_plugged_devices")
        try:
            vid, pid, str_vid, str_pid = cls._get_str_vid_pid(vid, pid)
            TRACE_LOGGER.log_trace(subscription_owner=log_owner,
                                   message=f"Listing all plugged devices according to filter "
                                           f"vid({str_vid}) and pid({str_pid})...",
                                   trace_level=TraceLevel.DEBUG)

            devices_found = []
            with usb1.USBContext() as usb_context:
                for device in reversed(usb_context.getDeviceList()):
                    found = True

                    if vid is not None and device.getVendorID() not in vid:
                        found = False
                    # end if

                    if pid is not None and device.getProductID() not in pid:
                        found = False
                    # end if

                    if found:
                        # Get device's bus number .
                        bus_id = device.getBusNumber()
                        # Get device's port on its bus.
                        port_list = '->'.join(str(x) for x in device.getPortNumberList())
                        device_found = LibusbUsbContextDevice(reader_name=f'Bus {bus_id} Device {port_list}',
                                                              vid=device.getVendorID(), pid=device.getProductID(),
                                                              connected=True, libusb_device=device)
                        TRACE_LOGGER.log_trace(subscription_owner=log_owner,
                                               message=f"Found device on {device_found.reader_name}, "
                                                       f"VID(0x{device_found.vid:04X}) and "
                                                       f"PID(0x{device_found.pid:04X})",
                                               trace_level=TraceLevel.DEBUG)
                        devices_found.append(device_found)
                    # end if
                # end for
            # end with
            TRACE_LOGGER.log_trace(subscription_owner=log_owner,
                                   message=f"Found {len(devices_found)} plugged devices according to "
                                           f"filter vid({str_vid}) and pid({str_pid})",
                                   trace_level=TraceLevel.DEBUG)
            return devices_found
        finally:
            TRACE_LOGGER.unsubscribe(subscription_owner=log_owner)
        # end try
    # end def get_plugged_devices

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self):
        # See ``TransportContext.open``
        if self.is_open:
            return
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Opening {self.__class__.__name__}...", trace_level=TraceLevel.DEBUG)

        try:
            self._libusb_context = usb1.USBContext()
            # Get a deep copy of the device cache using device_cache read only property
            self._usb_context_devices = self.__class__.device_cache

            tasks = []
            if self.__class__.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
                self._hotplug_task = ContextEventHandleTask(
                    libusb_context=self._libusb_context,
                    trace_level=TRACE_LOGGER.get_trace_level(subscription_owner=self),
                    trace_file_name=self.trace_file_name, trace_name="LibusbUsbContext Hotplug")
                self._hotplug_opaque_handle = self._libusb_context.hotplugRegisterCallback(
                    callback=self._hotplug_callback)
                tasks.append(self._hotplug_task)
            # end if

            self._threaded_executor = ThreadedExecutor(
                tasks=tasks, max_threads=MAX_THREADS, name="Libusb Driver USB Context Executor",
                run_until_stop=True)
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
            if self._hotplug_task is not None:
                self._hotplug_task.stop_event.set()
                self._hotplug_task = None
            # end if
            if self._hotplug_opaque_handle is not None:
                # noinspection PyBroadException
                try:
                    self._libusb_context.hotplugDeregisterCallback(self._hotplug_opaque_handle)
                except Exception:
                    pass
                # end try
                self._hotplug_opaque_handle = None
            # end if
            self._force_kill_executor_thread()
            self._threaded_executor = None
            self._executor_thread = None
            self._libusb_context = None
            self._usb_context_devices = None
            raise
        # end try

        self.is_open = True

        self.update_device_list()
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See TransportContext.close
        if not self.is_open:
            return
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Closing {self.__class__.__name__}...", trace_level=TraceLevel.DEBUG)

        try:
            if self._hotplug_task is not None:
                self._hotplug_task.stop_event.set()
            # end if

            for device in self._usb_context_devices:
                self.close_device(usb_context_device=device)
                if device.libusb_device is not None:
                    device.libusb_device.close()
                # end if
            # end for

            if self._executor_thread is not None and self._executor_thread.is_alive():
                self._threaded_executor.stop()
                self._executor_thread.join(USB_TIMEOUT + 1)
                if self._executor_thread.is_alive():
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Executor thread failed to join, Force kill",
                        trace_level=TraceLevel.ERROR)
                    self._force_kill_executor_thread()
                # end if
            # end if

            self._libusb_context.close()

            if self._hotplug_opaque_handle is not None:
                # noinspection PyBroadException
                try:
                    self._libusb_context.hotplugDeregisterCallback(self._hotplug_opaque_handle)
                except Exception:
                    pass
                # end try
            # end if

            for device in self._usb_context_devices:
                device.libusb_device = None
                device.connected = False
            # end for
            self._usb_context_devices.clear()
        except Exception:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Exception while closing. Clean attributes. Exception:\n"
                        f"{TracebackLogWrapper.get_exception_stack()}",
                trace_level=TraceLevel.ERROR)
            for device in self._usb_context_devices:
                device.clear_transfer_callbacks()
                device.interface_list = None
                device.libusb_device_handle = None
                device.libusb_device = None
                device.connected = False
            # end for
            self._force_kill_executor_thread()
            raise
        finally:
            self._threaded_executor = None
            self._executor_thread = None
            self._hotplug_task = None
            self._hotplug_opaque_handle = None
            self._libusb_context = None
            self._usb_context_devices = None
            self.is_open = False
        # end try
    # end def close

    def reset(self):
        # See TransportContext.reset
        self.close()
        sleep(.5)
        self.open()
    # end def reset

    def open_device(self, usb_context_device):
        """
        Open a context device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LibusbUsbContextDevice``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        with usb_context_device.lock_opening_closing:
            if not self.__class__.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
                self.update_device_list()
            # end if

            if usb_context_device.libusb_device_handle is not None:
                return
            # end if

            libusb_device = usb_context_device.libusb_device

            self._sanity_check(usb_context_device=usb_context_device)

            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Opening {usb_context_device.reader_name}...",
                trace_level=TraceLevel.DEBUG)

            libusb_device_handle = libusb_device.open()
            usb_context_device.libusb_device_handle = libusb_device_handle

            try:
                usb_context_device.interface_list = []
                if platform == 'linux':
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Detach the kernel driver from all interfaces (if needed)",
                        trace_level=TraceLevel.DEBUG)

                    for cfg in libusb_device:
                        # Configuration Descriptor
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self, message=f"Configuration Descriptor: {cfg.getConfigurationValue()}",
                            trace_level=TraceLevel.DEBUG)
                        for i in cfg:
                            # Interface Descriptor
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message=f"Interface Descriptor (NumSettings= {i.getNumSettings()})",
                                trace_level=TraceLevel.DEBUG)

                            # Start with detaching the kernel driver for all interfaces
                            for i_set in i:
                                #  Check whether a Kernel driver is active
                                if libusb_device_handle.kernelDriverActive(i_set.getNumber()):
                                    # Ask Kernel driver to detach
                                    libusb_device_handle.detachKernelDriver(i_set.getNumber())
                                    TRACE_LOGGER.log_trace(
                                        subscription_owner=self,
                                        message=f"Detach kernel driver for Interface ID {i_set.getNumber()}",
                                        trace_level=TraceLevel.DEBUG)
                                else:
                                    TRACE_LOGGER.log_trace(
                                        subscription_owner=self,
                                        message=f"Kernel driver for Interface ID {i_set.getNumber()} already detached",
                                        trace_level=TraceLevel.DEBUG)
                                # end if
                            # end for
                        # end for
                    # end for

                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"The kernel driver is detached from all interfaces",
                        trace_level=TraceLevel.DEBUG)
                # end if

                for cfg in libusb_device:
                    # Configuration Descriptor
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Configuration Descriptor: {cfg.getConfigurationValue()}",
                        trace_level=TraceLevel.DEBUG)
                    for i in cfg:
                        # Interface Descriptor
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Interface Descriptor (NumSettings= {i.getNumSettings()})",
                            trace_level=TraceLevel.DEBUG)

                        # Iterate over USBInterfaceSetting instances
                        for i_set in i:
                            # Interface Descriptor
                            protocol = i_set.getProtocol() if i_set.getNumber() <= 2 else i_set.getNumber()
                            endpoints = []
                            for endpoint in i_set:
                                endpoints.append((endpoint.getAddress(), endpoint.getMaxPacketSize()))
                            # end for
                            usb_context_device.interface_list.append((i_set.getNumber(), protocol, endpoints))

                            # Claim (= get exclusive access to) given interface number.
                            # Required to receive/send data.
                            libusb_device_handle.claimInterface(i_set.getNumber())
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self, message=f"Claim Interface ID {i_set.getNumber()}",
                                trace_level=TraceLevel.DEBUG)
                        # end for
                    # end for
                # end for

                with self._device_endpoint_task_dict:
                    self._device_endpoint_task_dict[usb_context_device.reader_name] = {}
                # end with

                if usb_context_device.libusb_device is None:
                    raise TransportContextException(
                        TransportContextException.Cause.DEVICE_NOT_CONNECTED, "Device disconnected during opening")
                # end if
            except Exception:
                # noinspection PyBroadException
                try:
                    self.close_device(usb_context_device=usb_context_device)
                except Exception:
                    usb_context_device.libusb_device_handle = None
                    usb_context_device.interface_list.clear()
                    usb_context_device.interface_list = None
                    with self._device_endpoint_task_dict:
                        self._device_endpoint_task_dict.pop(usb_context_device.reader_name, None)
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
        :type usb_context_device: ``LibusbUsbContextDevice``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        with usb_context_device.lock_opening_closing:
            if usb_context_device.libusb_device_handle is None:
                return
            # end if

            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Closing {usb_context_device.reader_name}...",
                trace_level=TraceLevel.DEBUG)

            self._sanity_check_device_open(usb_context_device=usb_context_device)

            self._stop_all_polling_thread_of_device(usb_context_device=usb_context_device)

            usb_context_device.clear_transfer_callbacks()

            libusb_device_handle = usb_context_device.libusb_device_handle

            for interfaceId, _, _ in usb_context_device.interface_list:
                # noinspection PyBroadException
                try:
                    libusb_device_handle.releaseInterface(interfaceId)
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Release Interface ID {interfaceId}",
                        trace_level=TraceLevel.DEBUG)
                except Exception as e:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self, message=f"Could not release Interface ID {interfaceId}: {e}",
                        trace_level=TraceLevel.ERROR)
                # end try
            # end for

            if platform == 'linux' and REATTACH_KERNEL_DRIVER:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self, message=f"Attach the kernel driver from all interfaces (if needed)",
                    trace_level=TraceLevel.DEBUG)

                for interfaceId, _, _ in usb_context_device.interface_list:
                    # Check whether a Kernel driver was previously active
                    # noinspection PyBroadException
                    try:
                        kernel_active = libusb_device_handle.kernelDriverActive(interfaceId)
                    except Exception:
                        kernel_active = True
                    # end try
                    if not kernel_active:
                        # noinspection PyBroadException
                        try:
                            # Ask Kernel driver to attach
                            libusb_device_handle.attachKernelDriver(interfaceId)
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self, message=f"Attach kernel driver for Interface ID {interfaceId}",
                                trace_level=TraceLevel.DEBUG)
                        except Exception as e:
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message=f"Could not attach kernel driver for Interface ID {interfaceId}: {e}",
                                trace_level=TraceLevel.ERROR)
                        # end try
                    # end if
                # end for

                TRACE_LOGGER.log_trace(
                    subscription_owner=self, message=f"The kernel driver is detached from all interfaces",
                    trace_level=TraceLevel.DEBUG)
            # end if

            usb_context_device.interface_list.clear()
            usb_context_device.interface_list = None

            # noinspection PyBroadException
            try:
                libusb_device_handle.close()
            except Exception as e:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Could not close device handle {usb_context_device.vid}:{usb_context_device.pid}: {e}",
                    trace_level=TraceLevel.ERROR)
            # end try
            usb_context_device.libusb_device_handle = None
            with self._device_endpoint_task_dict:
                self._device_endpoint_task_dict.pop(usb_context_device.reader_name, None)
            # end with

            if not self.__class__.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
                self.update_device_list()
            # end if

            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"{usb_context_device.reader_name} closed",
                trace_level=TraceLevel.INFO)
        # end with
    # end def close_device

    def control_write(self, usb_context_device, bm_request_type, b_request, w_value, w_index, data,
                      timeout=UsbContext.GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        """
        Perform a control write on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LibusbUsbContextDevice``
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

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        self._sanity_check_device_open(usb_context_device)

        if trace_owner is None:
            trace_owner = self
        # end if

        try:
            TRACE_LOGGER.log_trace(
                subscription_owner=trace_owner,
                message=f"{usb_context_device.reader_name}, Control write on interface 0x{w_index:02X} started",
                trace_level=TraceLevel.DEBUG)

            data_length = usb_context_device.libusb_device_handle.controlWrite(
                request_type=bm_request_type, request=b_request, value=w_value, index=w_index,
                data=bytes(list(data.data)), timeout=int(timeout*1000))

            # Update the timestamp of the message sent
            data.timestamp = perf_counter_ns()

            TRACE_LOGGER.log_trace(
                subscription_owner=trace_owner,
                message=f"{usb_context_device.reader_name}, Control write on interface 0x{w_index:02X}: {data.data} "
                        f"at {data.timestamp}ns",
                trace_level=TraceLevel.INFO)

            return data_length
        except usb1.libusb1.USBError as e:
            TRACE_LOGGER.log_trace(
                subscription_owner=trace_owner,
                message=f"{usb_context_device.reader_name}, Control write on interface 0x{w_index:02X} exception: "
                        f"{str(e)}; for packet {data.data}",
                trace_level=TraceLevel.ERROR)
            if str(e) == 'LIBUSB_ERROR_PIPE [-9]':
                raise TransportContextException(TransportContextException.Cause.CONTEXT_ERROR_PIPE, str(e))
            elif str(e) == 'LIBUSB_ERROR_IO [-1]':
                raise TransportContextException(TransportContextException.Cause.CONTEXT_ERROR_IO, str(e))
            elif str(e) == 'LIBUSB_ERROR_NO_DEVICE [-4]':
                raise TransportContextException(TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE, str(e))
            elif str(e) == 'LIBUSB_ERROR_TIMEOUT [-7]':
                raise TransportContextException(TransportContextException.Cause.TIMEOUT, str(e))
            # end if
            raise
        # end try
    # end def control_write

    def control_read(self, usb_context_device, bm_request_type, b_request, w_value, w_index, w_length,
                     timeout=UsbContext.GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        """
        Perform a control read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LibusbUsbContextDevice``
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

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        self._sanity_check_device_open(usb_context_device)

        if trace_owner is None:
            trace_owner = self
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Control read on interface 0x{w_index:02X} started",
            trace_level=TraceLevel.DEBUG)

        control_data = usb_context_device.libusb_device_handle.controlRead(
            request_type=bm_request_type, request=b_request, value=w_value, index=w_index, length=w_length,
            timeout=int(timeout*1000))

        control_data = UsbMessage(data=HexList(control_data.hex()), timestamp=perf_counter_ns())
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
        :type usb_context_device: ``LibusbUsbContextDevice``
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

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("bulk_write() method should be implemented before use")
    # end def bulk_write

    def bulk_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        """
        Perform a bulk read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LibusbUsbContextDevice``
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
        :type usb_context_device: ``LibusbUsbContextDevice``
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
            trace_level=TraceLevel.EXTRA_DEBUG)

        data_length = usb_context_device.libusb_device_handle.interruptWrite(
            endpoint=endpoint, data=bytes(list(data.data)), timeout=int(timeout*1000))

        # Update the timestamp of the message sent
        data.timestamp = perf_counter_ns()

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Interrupt write on endpoint 0x{endpoint:02X}: "
                    f"{HexList(data.data)} at {data.timestamp}ns",
            trace_level=TraceLevel.INFO)

        return data_length
    # end def interrupt_write

    def interrupt_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        """
        Perform an interrupt read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LibusbUsbContextDevice``
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
        with USB_TASK_LOCK:
            self._sanity_check_device_open(usb_context_device)

            if trace_owner is None:
                trace_owner = self
            # end if

            device_handle = usb_context_device.libusb_device_handle
        # end with

        TRACE_LOGGER.log_trace(
            subscription_owner=trace_owner,
            message=f"{usb_context_device.reader_name}, Interrupt read on endpoint 0x{endpoint:02X} started",
            trace_level=TraceLevel.EXTRA_DEBUG)

        interrupt_data = device_handle.interruptRead(
            endpoint=endpoint, length=w_length, timeout=int(timeout*1000))
        # Perform the time
        timestamp = perf_counter_ns()

        interrupt_data = UsbMessage(
            data=HexList(hexlify(interrupt_data).decode('utf8')), timestamp=timestamp)
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
        :type usb_context_device: ``LibusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from
        :type endpoint: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param time_stamped_msg_queue: Queue to get all USB message received - OPTIONAL
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
        self._sanity_check_device_open(usb_context_device=usb_context_device)

        assert not discard_report, 'LibusbUsbContext does not support the option to discard the report callback'

        if callback is not None:
            usb_context_device.set_transfer_callback(transfer_type_key=endpoint, callback=callback)
        # end if

        task = InterruptPollingTask(libusb_usb_context=self, usb_context_device=usb_context_device,
                                    endpoint_number=endpoint, data_size=w_length,
                                    time_stamped_msg_queue=time_stamped_msg_queue, trace_name=trace_name)

        self._threaded_executor.add_task(task)
        task.polling_started_event.wait()

        with self._device_endpoint_task_dict:
            self._device_endpoint_task_dict[usb_context_device.reader_name][endpoint] = task
        # end with
    # end def start_interrupt_read_polling

    def stop_interrupt_read_polling(self, usb_context_device, endpoint=None):
        """
        Stop a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LibusbUsbContextDevice``
        :param endpoint: Endpoint to get the data from, if None stop all interrupt polling for the device - OPTIONAL
        :type endpoint: ``int`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if endpoint is None:
            self._stop_all_polling_thread_of_device(usb_context_device=usb_context_device)
        else:
            with self._device_endpoint_task_dict:
                interface_tasks = self._device_endpoint_task_dict.get(usb_context_device.reader_name, None)

                if interface_tasks is None:
                    return
                # end if

                task = interface_tasks.pop(endpoint, None)

                if task is None:
                    return
                # end if

                task.stop_event.set()

                task.end_event.wait(USB_TIMEOUT * 1.01)
            # end with
        # end if
    # end def stop_interrupt_read_polling

    def get_ascii_string_descriptor(self, usb_context_device, descriptor):
        """
        Get the string description of the USB device defined descriptor.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``LibusbUsbContextDevice``
        :param descriptor: String descriptor (values can be found in ``StringDescriptor``):

                             * 1 : Manufacturer
                             * 2 : Product
                             * 3 : Serial Number
        :type descriptor: ``int``

        :return: The descriptor string
        :rtype: ``str``
        """
        self._sanity_check_device_open(usb_context_device=usb_context_device)
        string_descriptor = str(usb_context_device.libusb_device_handle.getASCIIStringDescriptor(descriptor))
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
        :type usb_context_device: ``LibusbUsbContextDevice``

        :return: The descriptor string
        :rtype: ``str``
        """
        self._sanity_check_device_open(usb_context_device=usb_context_device)
        device_info = ""
        device_info += f"USB.VendorID     : 0x{usb_context_device.libusb_device.getVendorID():04X}\n"
        device_info += f"USB.ProductID    : 0x{usb_context_device.libusb_device.getProductID():04X}\n"
        device_info += f"USB.bcdDevice    : 0x{usb_context_device.libusb_device.getbcdDevice():04X}\n"
        if usb_context_device.libusb_device_handle is not None:
            manufacturer = str(self.get_ascii_string_descriptor(usb_context_device, StringDescriptor.MANUFACTURER))
        else:
            manufacturer = str(usb_context_device.libusb_device.getManufacturer())
        # end if
        device_info += f"Manufacturer     : {manufacturer}\n"
        if usb_context_device.libusb_device_handle is not None:
            product = str(self.get_ascii_string_descriptor(usb_context_device, StringDescriptor.PRODUCT))
        else:
            product = str(usb_context_device.libusb_device.getProduct())
        # end if
        device_info += f"Product          : {product}"
        # Serial number has been removed because it was raising errors
        # if usb_context_device.libusb_device_handle is not None:
        #     serial_number = str(self.get_ascii_string_descriptor(usb_context_device, StringDescriptor.SERIAL_NUMBER))
        # else:
        #     serial_number = str(usb_context_device.libusb_device.getSerialNumber())
        # # end if
        # device_info += f"Serial Number    : 0x{serial_number.replace(' ', '')}"

        return device_info
    # end def get_device_info

    def update_device_list(self):
        # See ``UsbContext.update_device_list``
        if not self.is_open:
            return
        # end if

        self._sanity_check()

        with USB_TASK_LOCK:
            # Put all devices back to not connected and not context specific device structure associated
            usb_context_devices = {}
            for usb_context_device in self._usb_context_devices:
                usb_context_device.libusb_device = None
                usb_context_device.connected = False
                usb_context_devices[usb_context_device.reader_name] = usb_context_device
            # end for

            # Update all connected devices
            for usb_context_device in reversed(self._libusb_context.getDeviceList()):
                port_list = '->'.join(str(x) for x in usb_context_device.getPortNumberList())
                reader_name = f'Bus {usb_context_device.getBusNumber()} Device {port_list}'
                if reader_name in usb_context_devices:
                    usb_context_devices[reader_name].vid = usb_context_device.getVendorID()
                    usb_context_devices[reader_name].pid = usb_context_device.getProductID()
                    usb_context_devices[reader_name].libusb_device = usb_context_device
                    usb_context_devices[reader_name].connected = True
                # end if
            # end for

            for usb_context_device in self._usb_context_devices:
                assert isinstance(usb_context_device, LibusbUsbContextDevice), \
                    f"usb_context_device should be a LibusbUsbContextDevice, {usb_context_device} is not"
                if not usb_context_device.connected:
                    if usb_context_device.libusb_device_handle is not None:
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Lost connection on an open device: {usb_context_device.reader_name}",
                            trace_level=TraceLevel.WARNING)
                    # end if

                    try:
                        self._stop_all_polling_thread_of_device(usb_context_device=usb_context_device)
                        self._device_endpoint_task_dict.pop(usb_context_device.reader_name, None)
                    finally:
                        usb_context_device.libusb_device_handle = None
                        usb_context_device.interface_list = None
                    # end try
                # end if
            # end for
        # end with
    # end def update_device_list

    def _sanity_check(self, usb_context_device=None):
        """
        Check if the context is open and if a context device (if given) is connected.

        :param usb_context_device: The USB device to check - OPTIONAL
        :type usb_context_device: ``LibusbUsbContextDevice``

        :raise ``TransportContextException``: If the context is not open or if the device is not connected nor found
        """
        super()._sanity_check(usb_context_device=usb_context_device)

        if usb_context_device is not None and usb_context_device.libusb_device is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_FOUND)
        # end if
    # end def _sanity_check

    def _sanity_check_device_open(self, usb_context_device):
        """
        Check if the context is open and if a context device is connected and found.

        :param usb_context_device: The USB device to check
        :type usb_context_device: ``LibusbUsbContextDevice``

        :raise ``TransportContextException``: If the context is not open or if the device is not connected nor found
        """
        self._sanity_check(usb_context_device=usb_context_device)

        if usb_context_device.libusb_device_handle is None or \
                self._device_endpoint_task_dict.get(usb_context_device.reader_name, None) is None or \
                usb_context_device.interface_list is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_OPEN)
        # end if
    # end def _sanity_check_device_open

    def _stop_all_polling_thread_of_device(self, usb_context_device):
        """
        Stop all polling threads associated to a context device. If this method is called by a thread while already
        called in another thread, it will not be done.

        :param usb_context_device: Context device to use
        :type usb_context_device: ``LibusbUsbContextDevice``
        """
        # The first part of the method should not be blocked but should be able to block other calls of
        # ``with self._device_endpoint_task_dict``, that is why
        # ``with self._device_endpoint_task_dict.try_lock_do_anyway()`` is used.
        with self._device_endpoint_task_dict.try_lock_do_anyway():
            interface_tasks = self._device_endpoint_task_dict.get(usb_context_device.reader_name, None)

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
                    # All stop event are set to avoid having to wait for all timeout sequentially. This way, all
                    # timeout done by the libusb methods in the threads will be awaited parallely
                    for interface_task in interface_tasks.values():
                        interface_task.stop_event.set()
                    # end for

                    # All the wait should then be done here but because their stops are done in parallel just the
                    # first one should be blocking for a long time
                    for interface_task in interface_tasks.values():
                        interface_task.end_event.wait(USB_TIMEOUT * 1.01)
                    # end for

                    interface_tasks.clear()
                # end with
            finally:
                usb_context_device.stopping_all_polling_threads.release()
            # end try
        # end with
    # end def _stop_all_polling_thread_of_device

    def _hotplug_callback(self, context, device, event):
        """

        :param context: The USB context associated with the event
        :type context: ``usb1.USBContext``
        :param device: The USB device associated with the event
        :type device: ``usb1.USBDevice``
        :param event: Event received
        :type event: ``int``
        :return:
        """
        if context != self._libusb_context:
            return
        # end if

        event_str = HOT_PLUG_EVENT_TO_STR[event] if event in HOT_PLUG_EVENT_TO_STR else str(event)
        # Get device's bus number .
        bus_id = device.getBusNumber()
        # Get device's port on its bus.
        port_list = '->'.join(str(x) for x in device.getPortNumberList())
        reader_name = f'Bus {bus_id} Device {port_list}'

        usb_context_device = None
        try:
            usb_context_devices = self.get_devices(
                reader_name=reader_name, vid=device.getVendorID(), pid=device.getProductID())
            assert len(usb_context_devices) <= 1, \
                f"There is more than one device with reader_name({reader_name}), vid(0x{device.getVendorID():04X}) " \
                f"and pid(0x{device.getProductID():04X}): \n{usb_context_devices}"
            if len(usb_context_devices) == 1:
                usb_context_device = usb_context_devices[0]
            # end if
        except (AssertionError, TransportContextException):
            TRACE_LOGGER.log_trace(
                subscription_owner=self._hotplug_task, message=f"Exception while getting device in callback ",
                trace_level=TraceLevel.WARNING)
        # end try

        if usb_context_device is None:
            TRACE_LOGGER.log_trace(
                subscription_owner=self._hotplug_task,
                message=f"Event on unknown device [Bus {bus_id} Device {port_list}]: {event_str}",
                trace_level=TraceLevel.DEBUG)
            return
        # end if

        assert isinstance(usb_context_device, LibusbUsbContextDevice), \
            f"usb_context_device should be a LibusbUsbContextDevice, {usb_context_device} is not"

        # The part of the method should not be blocked but should be able to block other calls of
        # ``with self._device_endpoint_task_dict``, that is why
        # ``with self._device_endpoint_task_dict.try_lock_do_anyway()`` is used.
        with self._device_endpoint_task_dict.try_lock_do_anyway():
            # noinspection PyUnresolvedReferences
            if event != usb1.HOTPLUG_EVENT_DEVICE_ARRIVED:
                try:
                    self._stop_all_polling_thread_of_device(usb_context_device=usb_context_device)
                    self._device_endpoint_task_dict.pop(usb_context_device.reader_name, None)
                finally:
                    usb_context_device.libusb_device_handle = None
                    usb_context_device.libusb_device = None
                    usb_context_device.interface_list = None
                    usb_context_device.connected = False
                # end try
            else:
                usb_context_device.libusb_device = device
                usb_context_device.connected = True
            # end if
        # end with

        TRACE_LOGGER.log_trace(
            subscription_owner=self._hotplug_task,
            message=f"Event on device [{usb_context_device.reader_name}]: {event_str}",
            trace_level=TraceLevel.INFO)
    # end def _hotplug_callback

    def _force_kill_executor_thread(self):
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
# end class LibusbUsbContext

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
