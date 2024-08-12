#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.usb.usbcontext
:brief: USB context interface classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from configparser import ConfigParser
from inspect import getmembers
from inspect import ismethod
from os import R_OK
from os import access
from os import remove
from os.path import join
from threading import RLock
from time import time
# For some reason pycharm decided not to see it while being used in a docstring (it normally does)
# noinspection PyUnresolvedReferences
from typing import Callable

from pylibrary.system.tracelogger import DummyOwner
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pytransport.transportcontext import TRACE_LOGGER
from pytransport.transportcontext import TransportContext
from pytransport.transportcontext import TransportContextDevice
from pytransport.transportcontext import TransportContextException
from pytransport.usb.usbconstants import HidClassSpecificRequest
from pytransport.usb.usbconstants import RequestType
from pytransport.usb.usbconstants import StandardDeviceRequest
from pytransport.usb.usbmessage import UsbMessage

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# Configure USB traces verbosity
#  - None: disable all traces (Default)
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for packets only
#  - TraceLevel.DEBUG: Debug level will be for every context actions
FORCE_AT_CREATION_ALL_USB_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_USB_TRACE_FILE_NAME = None

# Change this to True to have all non-private methods information and timing
# It will be added to the USB context trace at level = TraceLevel.INFO so if the level of the USB context is under
# that, it will not be traced
TRACE_METHOD_INFO_AND_TIMING = False


class StringDescriptor:
    """
    ASCII string descriptor
    """
    MANUFACTURER = 1
    PRODUCT = 2
    SERIAL_NUMBER = 3
# end class StringDescriptor


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class UsbContextDevice(TransportContextDevice):
    """
    USB device structure used in a USB context.
    """
    def __init__(self, reader_name, vid, pid, connected=False, transfer_callbacks=None):
        """
        :param reader_name: The bus ID and port number read in the config file, format: Bus X Device Y
        :type reader_name: ``str``
        :param vid: The VID of the device
        :type vid: ``int``
        :param pid: The PID of the device
        :type pid: ``int``
        :param connected: Flag indicating if the device is connected - OPTIONAL
        :type connected: ``bool``
        :param transfer_callbacks: The callbacks that will be used when a transfer is received for each transfer type
                                   (HID mouse, HID keyboard, HID++, etc...), its format is a thread safe dictionary
                                   (the keys are endpoint IDs). If ``None``, it will be set as an
                                   empty thread safe dictionary - OPTIONAL
        :type transfer_callbacks: ``RLockedDict`` or ``None``
        """
        super().__init__(connected=connected, transfer_callbacks=transfer_callbacks)

        self.reader_name = reader_name
        self.vid = vid
        self.pid = pid
        self.interface_list = None
        self.lock_opening_closing = RLock()

        # This RLock is used to know if stopping all polling threads is already being performed
        self.stopping_all_polling_threads = RLock()
    # end def __init__

    def get_usb_port_path(self):
        """
        Get a list of int of the port path to the device. It is found in the reader name.

        :return: The port path to the device
        :rtype: ``list[int]``
        """
        split_reader_name = self.get_basic_reader_name().split(" ")
        usb_port_path = split_reader_name[split_reader_name.index("Device") + 1]
        return [int(x) for x in usb_port_path.split("->")]
    # end def get_usb_port_path

    def get_manufacturer_string(self):
        """
        Get USB Manufacturer String

        :return: USB Manufacturer String
        :rtype: ``str``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_manufacturer_string

    def get_product_string(self):
        """
        Get USB Product String

        :return: USB Product String
        :rtype: ``str``
        """
        return NotImplementedAbstractMethodError()
    # end def get_product_string

    def get_serial_number_string(self):
        """
        Get USB Serial number String

        :return: USB Product String
        :rtype: ``str``
        """
        return NotImplementedAbstractMethodError()
    # end def get_serial_number_string

    def get_basic_reader_name(self):
        """
        Get the basic reader name. Some USB context might add additional information in the reader_name (see Logiusb
        for example), this method is to force getting only the format "Bus X Device Y".

        :return: USB Product String
        :rtype: ``str``
        """
        return self.reader_name
    # end def get_basic_reader_name

    def get_device_address(self):
        """
        Get USB Device Address

        :return: USB Device Address
        :rtype: ``int``
        """
        return NotImplementedAbstractMethodError()
    # end def get_device_address
# end class UsbContextDevice


class UsbContext(TransportContext):
    """
    Common implementation of a USB context.
    """
    CONFIG_FILE_NAME = "usb_context.ini"  # Name of the configuration file
    # Class to use for configuring the class cache, it should be UsbContextDevice or its child class
    USB_CONTEXT_DEVICE_CLASS = UsbContextDevice
    CLASS_METHOD_TRACE_LEVEL = FORCE_AT_CREATION_ALL_USB_TRACE_LEVEL if \
        FORCE_AT_CREATION_ALL_USB_TRACE_LEVEL is not None else TraceLevel.NO_TRACE
    CLASS_METHOD_TRACE_FILE_NAME = FORCE_AT_CREATION_ALL_USB_TRACE_FILE_NAME
    GENERIC_CONTROL_TIMEOUT = 1  # In seconds

    def __init__(self, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param trace_level: Trace level of the USB context - OPTIONAL
        :type trace_level: ``TraceLevel``
        :param trace_file_name: Trace output of the transport context - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        """

        self._threaded_executor = None

        if FORCE_AT_CREATION_ALL_USB_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_USB_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_USB_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_USB_TRACE_FILE_NAME
        # end if

        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        # This cache attribute should be updated in child class to have the device cache
        self._usb_context_devices = None

        if TRACE_METHOD_INFO_AND_TIMING:
            for method_name, method_object in [x for x in getmembers(self, predicate=ismethod) if x[0][0] != '_']:
                setattr(self, method_name, self._method_info_and_timing(method_object, method_name))
            # end for
        # end if
    # end def __init__

    def _method_info_and_timing(self, method_object, method_name):
        def wrapped(*args, **kwargs):
            start_time = None
            try:
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f"Entering {method_name} with args = {args} and kwargs = {kwargs}",
                                       trace_level=TraceLevel.INFO)
                try:
                    start_time = time()
                    return method_object(*args, **kwargs)
                except Exception:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Exception in {method_name}. Exception:\n"
                                f"{TracebackLogWrapper.get_exception_stack()}",
                        trace_level=TraceLevel.ERROR)
                    raise
                # end try
            finally:
                if start_time is not None:
                    str_to_add = f", it took {time() - start_time}s"
                else:
                    str_to_add = ""
                # end if

                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f"Exiting {method_name}{str_to_add}",
                                       trace_level=TraceLevel.INFO)
            # end try
        # end def wrapped
        return wrapped
    # end def _method_info_and_timing

    @staticmethod
    def get_driver_info():
        """
        Obtain driver information.

        :return: Driver info
        :rtype: ``str``
        """
        raise NotImplementedError("get_driver_info() method should be implemented by child class")
    # end def get_driver_info

    @classmethod
    def get_plugged_devices(cls, vid=None, pid=None):
        """
        Find the devices plugged in with the wanted VIDs and PIDs (if given).

        :param vid: The VID list of the devices to find. If None, no filter on VID will be applied - OPTIONAL
        :type vid: ``list[int]`` or ``int`` or ``None``
        :param pid: The PID list of the devices to find. If None, no filter on PID will be applied - OPTIONAL
        :type pid: ``list[int]`` or ``int`` or ``None``

        :return: List of devices plugged in that match the wanted PID/VID filters
        :rtype: ``list[UsbContextDevice]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextExceptionCause``
        """
        raise NotImplementedError("get_plugged_devices() method should be implemented by child class")
    # end def get_plugged_devices

    @classmethod
    def generate_configuration_file(cls, path, vid=None, pid=None, *args, **kwargs):
        """
        Generate the configuration file for the context.

        :param path: The path where the configuration file will be generated
        :type path: ``str``
        :param vid: The VID list of the devices to find. If None, no filter on VID will be applied - OPTIONAL
        :type vid: ``list[int]`` or ``int`` or ``None``
        :param pid: The PID list of the devices to find. If None, no filter on PID will be applied - OPTIONAL
        :type pid: ``list[int]`` or ``int`` or ``None``
        :param args: Potential child argument - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword argument - OPTIONAL
        :type kwargs: ``object``

        :return: Number of device plugged in that match the wanted PID/VID filters
        :rtype: ``list[UsbContextDevice]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        log_owner = DummyOwner()
        TRACE_LOGGER.subscribe(subscription_owner=log_owner,
                               trace_level=cls.CLASS_METHOD_TRACE_LEVEL,
                               trace_file_name=cls.CLASS_METHOD_TRACE_FILE_NAME,
                               trace_name=f"{cls.__name__}.generate_configuration_file")

        vid, pid, str_vid, str_pid = cls._get_str_vid_pid(vid, pid)
        TRACE_LOGGER.log_trace(subscription_owner=log_owner,
                               message=f"Generate cache file with all plugged devices according to "
                                       f"filter vid({str_vid}) and pid({str_pid})...",
                               trace_level=TraceLevel.DEBUG)

        full_path = join(path, cls.CONFIG_FILE_NAME)

        # Delete previously-generated file (might be available from an old run)
        try:
            remove(full_path)
        except OSError:
            # no file to be removed
            pass
        # end try

        device_found = False
        with open(full_path, 'w+') as config_file:
            config_file.writelines(
                ('# ----------------------------------------------------------------------------\n',
                 f'# This is the USB configuration file. (Generated with {cls.__name__})\n',
                 '# \n',
                 '# This file contains a section per USB device, mapping a given index to a USB Device '
                 '(Bus Id and Port Nb).\n',
                 '# This file is optional:\n',
                 '# - It will be re-created each time the project is run\n',
                 '# \n',
                 '# The [READERS_X] sections.\n',
                 '# This section contains the reader name (bus id, port numbers), the VID and the PID of a USB '
                 'device\n',
                 '# \n',
                 '# Example (second example is typically a mezzy receiver on the first port of a hub):\n',
                 '# [READERS_0]\n',
                 '# reader_name = Bus 3 Device 1->1\n'
                 '# vid = 046D\n'
                 '# pid = C548\n'
                 '# or\n',
                 '# [READERS_1]\n',
                 '# reader_name = Bus 3 Device 1->2->1\n'
                 '# vid = 046D\n'
                 '# pid = C548\n'
                 '# \n',
                 '# ----------------------------------------------------------------------------\n',
                 ))
            index = 0
            config = ConfigParser()
            # Retrieve the list of all wanted USB devices currently plugged in
            TRACE_LOGGER.log_trace(subscription_owner=log_owner,
                                   message=f"Call {cls.__name__}.get_plugged_devices...",
                                   trace_level=TraceLevel.DEBUG)
            devices = cls.get_plugged_devices(vid=vid, pid=pid)
            if len(devices) > 0:
                device_found = True
                for device in devices:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=log_owner,
                        message=f"Add section READER_{index}: {device.get_basic_reader_name()} "
                                f"{device.vid:04X}:{device.pid:04X}",
                        trace_level=TraceLevel.DEBUG)
                    config.add_section(section=f'READER_{index}')
                    config.set(section=f'READER_{index}', option='reader_name', value=device.get_basic_reader_name())
                    config.set(section=f'READER_{index}', option='vid', value=f'{device.vid:04X}')
                    config.set(section=f'READER_{index}', option='pid', value=f'{device.pid:04X}')
                    index += 1
                # end for
                config.write(fp=config_file)
            # end if
        # end with

        if not device_found:
            TRACE_LOGGER.log_trace(
                subscription_owner=log_owner,
                message=f"No device found to put in cache",
                trace_level=TraceLevel.ERROR)
            # delete the invalid config file
            try:
                # removing the invalid libusb.ini file and raising an exception
                remove(full_path)
                raise ValueError("No USB Device Found! Could NOT generate a valid configuration file")
            except OSError:
                pass
            # end try
        # end if
        TRACE_LOGGER.log_trace(
            subscription_owner=log_owner,
            message=f"Cache file generated: {full_path}",
            trace_level=TraceLevel.DEBUG)
    # end def generate_configuration_file

    @classmethod
    def configure_device_cache(cls, path, force_reconfiguration=False, vid=None, pid=None, *args, **kwargs):
        """
        Configure the transport context device cache. If the configuration file is not present (or
        ``force_reconfiguration`` is ``True``), the configuration file will be generated with the wanted filters
        (VID/PID).

        :param path: The path where the configuration file will be generated
        :type path: ``str``
        :param force_reconfiguration: Flag indicating if the reconfiguration should be forced if the cache was already
                                      configured - OPTIONAL
        :type force_reconfiguration: ``bool``
        :param vid: The VID list of the devices to find if generating the cache file is done. If None, no filter on
                    VID will be applied - OPTIONAL
        :type vid: ``list[int]`` or ``int`` or ``None``
        :param pid: The PID list of the devices to find if generating the cache file is done. If None, no filter on
                    PID will be applied - OPTIONAL
        :type pid: ``list[int]`` or ``int`` or ``None``
        :param args: Potential child argument - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword argument - OPTIONAL
        :type kwargs: ``object``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        :raise ``ValueError``: If the ``path`` parameter is not an accessible file
        """
        if len(cls._DEVICE_CACHE) != 0:
            if force_reconfiguration:
                cls._DEVICE_CACHE.clear()
            else:
                return
            # end if
        # end if

        full_path = join(path, cls.CONFIG_FILE_NAME)

        if not access(full_path, R_OK):
            cls.generate_configuration_file(path=path, vid=vid, pid=pid)
        # end if

        config = ConfigParser()
        config.read([full_path])

        index = 0
        while config.has_section(f'READER_{index}'):
            reader_name = config.get(f'READER_{index}', 'reader_name').strip("\"'")
            vid = int(config.get(f'READER_{index}', 'vid').strip("\"'"), 16)
            pid = int(config.get(f'READER_{index}', 'pid').strip("\"'"), 16)
            if reader_name is not None and reader_name != 'None':
                cls._DEVICE_CACHE.append(cls.USB_CONTEXT_DEVICE_CLASS(reader_name=reader_name, vid=vid, pid=pid))
            # end if
            index += 1
        # end while

        if index == 0:
            raise ValueError('Empty config file: %s' % (full_path,))
        # end if
    # end def configure_device_cache

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self):
        # See TransportContext.open
        raise NotImplementedError("open() method should be implemented by child class, and use property is_open")
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See TransportContext.close
        raise NotImplementedError("close() method should be implemented by child class, and use property is_open")
    # end def close

    def reset(self):
        # See TransportContext.reset
        raise NotImplementedError("reset() method should be implemented by child class")
    # end def reset

    def get_devices(self, index_in_cache=None, reader_name=None, vid=None, pid=None, *args, **kwargs):
        """
        Get a list of context devices. Multiple filters can be used:

        * If ``index_in_cache`` is given, all other filters are ignored and the index in the cache is used to get
          the device
        * If ``reader_name`` is given, the list of devices with this reader name (format of
          ``UsbContextDevice.reader_name``) is returned
        * If ``vid`` is given, the list of devices with this VID is returned
        * If ``pid`` is given, the list of devices with this PID is returned
        * Child class can add new filters as parameters

        :param index_in_cache: The index in the cache of the device to get - OPTIONAL
        :type index_in_cache: ``int`` or ``None``
        :param reader_name: The bus ID and port number read in the config file, format: Bus X Device Y - OPTIONAL
        :type reader_name: ``str`` or ``None``
        :param vid: The list possible VID of the device - OPTIONAL
        :type vid: ``list[int]`` or ``int`` or ``None``
        :param vid: The list possible PID of the device - OPTIONAL
        :type pid: ``list[int]`` or ``int`` or ``None``
        :param args: Potential future parameters - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential future keyword parameters - OPTIONAL
        :type kwargs: ``object``

        :return: The list of found device with the given filters (empty list if no device found)
        :rtype: ``list[UsbContextDevice]``

        :raise ``TransportContextException``: If the context cache has not been created (typically if the context
                                              is not open)
        """
        if self._usb_context_devices is None:
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INVALID_STATE,
                "The context cache has not been created (typically if the context is not open)")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Getting device with filters index_in_cache({index_in_cache}), reader_name({reader_name}), "
                    f"vid({vid}) and pid({pid})...",
            trace_level=TraceLevel.DEBUG)

        devices_found = []

        try:
            if index_in_cache is not None and index_in_cache < len(self._usb_context_devices):
                devices_found.append(self._usb_context_devices[index_in_cache])
                return devices_found
            # end if

            if isinstance(vid, int):
                vid = [vid]
            # end if

            if isinstance(pid, int):
                pid = [pid]
            # end if

            for device in self._usb_context_devices:
                found = True

                if reader_name is not None and device.get_basic_reader_name() != reader_name:
                    found = False
                # end if

                if vid is not None and device.vid not in vid:
                    found = False
                # end if

                if pid is not None and device.pid not in pid:
                    found = False
                # end if

                if found:
                    devices_found.append(device)
                # end if
            # end for

            return devices_found
        finally:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Found {len(devices_found)} device(s) with filters index_in_cache({index_in_cache}), "
                        f"reader_name({reader_name}), vid({vid}) and pid({pid})",
                trace_level=TraceLevel.DEBUG)
        # end try
    # end def get_devices

    def open_device(self, usb_context_device):
        """
        Open a context device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("open_device() method should be implemented by child class")
    # end def open_device

    def close_device(self, usb_context_device):
        """
        Close a context device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("close_device() method should be implemented by child class")
    # end def close_device

    def control_write(self, usb_context_device, bm_request_type, b_request, w_value, w_index, data,
                      timeout=GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        """
        Perform a control write on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
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
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The number of bytes sent
        :rtype: ``int``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("control_write() method should be implemented by child class")
    # end def control_write

    def control_read(self, usb_context_device, bm_request_type, b_request, w_value, w_index, w_length,
                     timeout=GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        """
        Perform a control read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
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
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The message read
        :rtype: ``UsbMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("control_read() method should be implemented by child class")
    # end def control_read

    def bulk_write(self, usb_context_device, endpoint, data, timeout=0, blocking=False, trace_owner=None):
        """
        Perform a bulk write on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to send the data to
        :type endpoint: ``int``
        :param data: Data to write
        :type data: ``UsbMessage``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The number of bytes sent
        :rtype: ``int``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("bulk_write() method should be implemented by child class")
    # end def bulk_write

    def bulk_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        """
        Perform a bulk read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to get the data from
        :type endpoint: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The message read
        :rtype: ``UsbMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("bulk_read() method should be implemented by child class")
    # end def bulk_read

    def interrupt_write(self, usb_context_device, endpoint, data, timeout=0, blocking=False, trace_owner=None):
        """
        Perform an interrupt write on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to send the data to
        :type endpoint: ``int``
        :param data: Data to write
        :type data: ``UsbMessage``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The number of bytes sent
        :rtype: ``int``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("interrupt_write() method should be implemented by child class")
    # end def interrupt_write

    def interrupt_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        """
        Perform an interrupt read on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to get the data from
        :type endpoint: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``
        :param trace_owner: Owner of the trace for this action, if ``None``, ``self`` will be used - OPTIONAL
        :type trace_owner: ``object`` or ``None``

        :return: The message read
        :rtype: ``UsbMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("interrupt_read() method should be implemented by child class")
    # end def interrupt_read

    def start_interrupt_read_polling(self, usb_context_device, endpoint, w_length, time_stamped_msg_queue=None,
                                     trace_name=None, callback=None, discard_report=False):
        """
        Start a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to get the data from
        :type endpoint: ``int``
        :param w_length: Length of the buffer to receive data
        :type w_length: ``int``
        :param time_stamped_msg_queue: Queue to get all USB message received - OPTIONAL
        :type time_stamped_msg_queue: ``Queue`` or ``None``
        :param trace_name: Trace's name for this action, if ``None`` the trace name or ``self`` will be used - OPTIONAL
        :type trace_name: ``str`` or ``None``
        :param callback: Callback to use, it will change add it in the ``usb_context_device``.
                         If ``None``, it will be ignored - OPTIONAL
        :type callback: ``Callable`` or ``None``
        :param discard_report: Flag indicating to discard any message received on this endpoint - OPTIONAL
        :type discard_report: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("start_interrupt_read_polling() method should be implemented by child class")
    # end def start_interrupt_read_polling

    def stop_interrupt_read_polling(self, usb_context_device, endpoint=None):
        """
        Stop a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to get the data from, if None stop all interrupt polling for the device - OPTIONAL
        :type endpoint: ``int`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("stop_interrupt_read_polling() method should be implemented by child class")
    # end def stop_interrupt_read_polling

    def mute_interrupt_read_polling(self, usb_context_device, endpoint=None):
        """
        Mute a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to get the data from, if None stop all interrupt polling for the device - OPTIONAL
        :type endpoint: ``int`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("mute_interrupt_read_polling() method should be implemented by child class")
    # end def mute_interrupt_read_polling

    def unmute_interrupt_read_polling(self, usb_context_device, endpoint=None):
        """
        Unmute a task that performs interrupt read continuous polling on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint: Endpoint to get the data from, if None stop all interrupt polling for the device - OPTIONAL
        :type endpoint: ``int`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("unmute_interrupt_read_polling() method should be implemented by child class")
    # end def unmute_interrupt_read_polling

    def get_ascii_string_descriptor(self, usb_context_device, descriptor):
        """
        Get the string description of the USB device defined descriptor.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param descriptor: String descriptor (values can be found in ``StringDescriptor``):

                             * 1 : Manufacturer
                             * 2 : Product
                             * 3 : Serial Number
        :type descriptor: ``int``

        :return: The descriptor string
        :rtype: ``str``
        """
        raise NotImplementedError("get_ascii_string_descriptor() method should be implemented by child class")
    # end def get_ascii_string_descriptor

    def update_device_list(self):
        """
        Update the device list. For example when a hardware change has been performed and the context do not have any
        hot-plug capabilities.

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedError("update_device_list() method should be implemented by child class")
    # end def update_device_list

    def get_descriptor(self, usb_context_device, recipient, descriptor_type, descriptor_index, descriptor_size,
                       w_index=0, timeout=0, blocking=False):
        """
        Get a descriptor of a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
        :param recipient: USB recipient to use, values can be found in RequestType.Recipient
        :type recipient: ``int``
        :param descriptor_type: Descriptor type
        :type recipient: ``int``
        :param descriptor_index: Descriptor type index
        :type recipient: ``int``
        :param descriptor_size: Descriptor size
        :type recipient: ``int``
        :param w_index: The meaning of this parameter is recipient dependent
        :type w_index: ``int``
        :param timeout: The timeout of this action in seconds - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``

        :return: The descriptor message read
        :rtype: ``UsbMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        request_type = RequestType.TransferDirection.DEVICE_TO_HOST << RequestType.TRANSFER_DIRECTION_BITWISE_LEFT_SHIFT
        request_type |= RequestType.Type.STANDARD << RequestType.TYPE_BITWISE_LEFT_SHIFT
        request_type |= recipient

        return self.control_read(usb_context_device=usb_context_device,
                                 bm_request_type=request_type,
                                 b_request=StandardDeviceRequest.GET_DESCRIPTOR,
                                 w_value=descriptor_index | (descriptor_type << 8),
                                 w_index=w_index,
                                 w_length=descriptor_size,
                                 timeout=timeout,
                                 blocking=blocking)
    # end def get_descriptor

    def hid_class_specific_request(
            self,
            usb_context_device,
            interface_id,
            b_request=HidClassSpecificRequest.SET_IDLE,
            w_value=0,
            data=UsbMessage(data=HexList()),
            w_length=0,
            timeout=0,
            blocking=False):
        """
        Perform a HID class specific request on a USB device.

        :param usb_context_device: The USB device to use
        :type usb_context_device: ``UsbContextDevice``
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
        :type timeout: ``int`` or ``float``
        :param blocking: Flag indicating if the action is blocking or not - OPTIONAL
        :type blocking: ``bool``

        :return: Either the data received if it is a GET request or the length of data sent if it is a SET request
        :rtype: ``UsbMessage`` or ``int``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        request_type = RequestType.Type.CLASS << RequestType.TYPE_BITWISE_LEFT_SHIFT
        request_type |= RequestType.Recipient.INTERFACE

        # Get values are below 0x09 which is the value of SET_REPORT
        if 0 < b_request < HidClassSpecificRequest.SET_REPORT:
            request_type |= \
                RequestType.TransferDirection.DEVICE_TO_HOST << RequestType.TRANSFER_DIRECTION_BITWISE_LEFT_SHIFT
            return self.control_read(usb_context_device=usb_context_device,
                                     bm_request_type=request_type,
                                     b_request=b_request,
                                     w_value=w_value,
                                     w_index=interface_id,
                                     w_length=w_length,
                                     timeout=timeout,
                                     blocking=blocking)
        elif b_request >= HidClassSpecificRequest.SET_REPORT:
            request_type |= \
                RequestType.TransferDirection.HOST_TO_DEVICE << RequestType.TRANSFER_DIRECTION_BITWISE_LEFT_SHIFT
            return self.control_write(usb_context_device=usb_context_device,
                                      bm_request_type=request_type,
                                      b_request=b_request,
                                      w_value=w_value,
                                      w_index=interface_id,
                                      data=data,
                                      timeout=timeout,
                                      blocking=blocking)
        else:
            raise TransportContextException(TransportContextException.Cause.DATA_ERROR,
                                            f"b_request parameter should be > 0, received {b_request}")
        # end if
    # end def hid_class_specific_request

    def _sanity_check(self, usb_context_device=None):
        """
        Check if the context is open and if a context device (if given) is connected.

        :param usb_context_device: The USB device to check - OPTIONAL
        :type usb_context_device: ``UsbContextDevice``

        :raise ``TransportContextException``: If the context is not open or if the device is not connected
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if usb_context_device is not None and not usb_context_device.connected:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED)
        # end if
    # end def _sanity_check

    @staticmethod
    def _get_str_vid_pid(vid, pid):
        """
        Get vid and pid in list format and string format.

        :param vid: The VID to change
        :type vid: ``list[int]`` or ``int`` or ``None``
        :param pid: The PID to change
        :type pid: ``list[int]`` or ``int`` or ``None``

        :return: The VID and PID in string format (and list format if needed)
        :rtype: ``tuple[list[int] | None, list[int] | None, list[str] | str, list[str] | str]``
        """
        if isinstance(vid, int):
            vid = [vid]
        # end if

        if isinstance(pid, int):
            pid = [pid]
        # end if

        str_vid = [f"{_vid:04X}" for _vid in vid] if vid is not None else "None"
        str_pid = [f"{_pid:04X}" for _pid in pid] if pid is not None else "None"

        return vid, pid, str_vid, str_pid
    # end def _get_str_vid_pid
# end class UsbContext

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
