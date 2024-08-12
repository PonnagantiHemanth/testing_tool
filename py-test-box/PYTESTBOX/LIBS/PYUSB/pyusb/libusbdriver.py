#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyusb.libusbdriver
:brief: Device libusb1 interface
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from os import R_OK
from os import access
from os.path import dirname
from os.path import join
from sys import stdout
from threading import Lock
from threading import RLock
from time import sleep
from time import time

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pychannel.throughreceiverchannel import ThroughGotthardReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import GotthardReceiverChannel
from pychannel.usbchannel import UsbChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pylibrary.system.device import BaseSmartDevice
from pylibrary.system.device import SmartDeviceFactory
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import synchronized
from pylibrary.tools.util import ContainsIntEnumMeta
from pytransport.ble.blecontext import BleContext
from pytransport.ble.nrfblelibblecontext.nrfblelibblecontext import NrfBleLibBleContext
# Next line is kept to be able to easily switch between Logiusb and Libusb
# noinspection PyUnresolvedReferences
from pytransport.usb.libusbcontext.libusbdriverusbcontext import LibusbUsbContext
# Next line is kept to be able to easily switch between Logiusb and Libusb
# noinspection PyUnresolvedReferences
from pytransport.usb.logiusbcontext.logiusbcontext import LogiusbUsbContext
from pytransport.usb.usbconstants import LogitechReceiverProductId
from pytransport.usb.usbconstants import ProductId
from pytransport.usb.usbconstants import RequestType
from pytransport.usb.usbconstants import VendorId
from pytransport.usb.usbcontext import UsbContext
from pytransport.usb.usbhub.smartusbhub import SmartUsbHub
from pytransport.usb.usbhub.usbhubconstants import UsbHubAction
from pytransport.usb.usbhub.usbhubconstants import UsbHubUtils


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
DEVICE = RequestType.Recipient.DEVICE
INTERFACE = RequestType.Recipient.INTERFACE

# Receivers PID (0xC500-0xC5FF)
RECEIVERS_PID = 0xC500
RECEIVERS_MASK = 0xFF00
RECEIVERS_CONNECTION_COUNT = 6

VERBOSE = False
TRACE_LOGGER = TraceLogger.get_instance()

# To force USB Context, comment or uncomment following lines as needed
FORCE_USB_CONTEXT_CLASS = None
# FORCE_USB_CONTEXT_CLASS = LibusbUsbContext
# FORCE_USB_CONTEXT_CLASS = LogiusbUsbContext

# This flag is to be able to force the generation of the USB config file in the ``LibusbDriver.configure`` method
FORCE_REGENERATE_USB_CONFIG_FILE = False

# A global lock, that guarantees that 2 hub API calls could not occur at the same time
HUB_LOCK = Lock()


class BleContextClassId(IntEnum, metaclass=ContainsIntEnumMeta):
    """
    BLE Context Class ID to use to update its hardware firmware (DK)
    """
    NO_CONTEXT = 0
    NRF_BLE_LIB = auto()
# end class BleContextClassId


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ChannelIdentifier(object):
    """
    Channel characteristics enabling to select the correct one
    """
    def __init__(self,
                 port_index=None,
                 device_index=None,
                 transport_id=None,
                 protocol=None,
                 vendor_id=None,
                 product_id=None,
                 unit_id=None):
        """
        Initialize a ChannelIdentifier instance.

        :param port_index: Port index identifier - OPTIONAL
        :type port_index: ``int`` or ``None``
        :param device_index: Device index identifier - OPTIONAL
        :type device_index: ``int`` or ``None``
        :param transport_id: USB, BLE or eQuad Product identifier - OPTIONAL
        :type transport_id: ``str`` or ``None``
        :param protocol: Protocol identifier - OPTIONAL
        :type protocol: ``LogitechProtocol`` or ``None``
        :param vendor_id: Device Vendor identifier (for USB) DEPRECATED - OPTIONAL
        :type vendor_id: ``str`` or ``None``
        :param product_id: Device Product identifier (for USB) - OPTIONAL
        :type product_id: ``str`` or ``None``
        :param unit_id: Device Product identifier - OPTIONAL
        :type unit_id: ``str`` or ``None``
        """
        # Initial parameters.
        self.port_index = port_index
        self.device_index = device_index
        self.transport_id = transport_id
        self.protocol = protocol
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.unit_id = unit_id

        assert (self.port_index is not None or
                self.device_index is not None or
                self.transport_id is not None or
                self.protocol is not None or
                self.vendor_id is not None or
                self.product_id is not None or
                self.unit_id is not None), \
            "At least one element to identify the device should be given"
    # end def __init__

    def __str__(self):
        """
        Obtains a string representation of the current object.

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"port_index({self.port_index}), " \
               f"device_index({self.device_index}), " \
               f"transport_id({self.transport_id}), " \
               f"protocol({self.protocol}), " \
               f"vendor_id({self.vendor_id}), " \
               f"product_id({self.product_id}), " \
               f"unit_id({self.unit_id})"
    # end def __str__

    __repr__ = __str__
# end class ChannelIdentifier


class LibusbError(ValueError):
    """
    Allow the filtering of specific LibUsb error
    """
# end class LibusbError


class LibusbDriver(BaseSmartDevice):
    """
    Allow the manipulation of a USB Device via libusb1.

    Usage:
    @code
    sc = LibusbDriver(device_number)
    @endcode
    where device_number is the index of the device in the config file [RUNTIME] section

    After the declaration of a LibusbDriver, a getDeviceList request is sent via libusb

    USB context is cleaned at the destruction of the instance.
    """
    # Logitech vendor identifier
    LOGI_VENDOR_ID = 0x046d
    GRAVITON_EMULATOR_PRODUCT_ID = 0x555A  # USB Tools PID (0x5500-0x55FF)
    USB_PID_GOTTHARD = 0xF013
    # YEPKIT Board Identifier
    YEPKIT_VENDOR_ID = 0x04D8
    # D-Link USB 2.0 Hub (7 ports) Identifier
    DLINK_VENDOR_ID = 0x05E3
    # Phidgets USB 2.0 Hub (7 ports) Identifier
    PHIDGETS_VENDOR_ID = 0x1A40
    USB_CHARGING_CABLE_ENABLE = True
    CRUSH_PAD_CHARGING_EMULATOR_ENABLE = True
    MAX_USB_PORT_COUNT = 1
    # SEGGER Identifier
    SEGGER_VENDOR_ID = 0x1366
    SEGGER_PRODUCT_ID = 0x0101

    # Cache result of USB Hub discovery to get rid of duplicate discovery
    USB_HUB_LIST = None
    # Cache number of JLink discovered
    PROBE_COUNT = None
    GOTTHARD_DETECTED = None
    BLE_PRO_RECEIVER_DETECTED = None
    CRUSH_RECEIVER_DETECTED = None
    BEAGLE_480_DETECTED = None

    # USB context attributes
    USB_CONTEXT_CLASS = None
    USB_CONTEXT = None

    # BLE context attributes
    BLE_CONTEXT = None
    BLE_CONTEXT_MCU_NAME = 'NRF52840_XXAA'  # Graviton DK used for all current BLE contexts hardware

    # The different mappings for the channels.
    USB_CHANNEL_MAPPING = {}
    THROUGH_RECEIVER_CHANNEL_MAPPING = {}
    BLE_CHANNEL_MAPPING = {}
    IS_CONFIGURED = False

    # This is the value of self.port_index when the USB communication is not on a USB hub
    NON_HUB_USB_PORT_INDEX = 0
    # This is the value of self.port_index when the direct BLE communication is used
    BLE_PORT_INDEX = -1
    GOTTHARD = 4
    CHARGING_PORT_NUMBER = 5
    CRUSH_PAD_EMULATOR_PORT_NUMBER = 6
    # USB Port 6 default state: True (disabled) or False (enabled)
    IS_PORT6_DISABLED = None
    FTDI_CABLE_PORT_NUMBER = 7
    MAX_NUMBER_OF_DEVICE_IN_RECEIVER = 6
    # This is a dictionary to cache the 0x1D4B and 0x1004 features index, id and version
    FEATURE_CACHE = {}

    ACCEPTED_VID = [VendorId.LOGITECH_INC]

    # Maximum delay to wait to ensure the arrival or departure of USB devices
    ASYNCHRONOUS_CONNECTION_DISCONNECTION_DELAY = 1.0

    def __init__(self, device_number):
        """
        Initialize a LibusbDriver instance.

        :param device_number: Local device's number (1, 2 or 3)
        :type device_number: ``int``
        """
        super(LibusbDriver, self).__init__(device_number)

        # Queue
        self.time_stamped_msg_queue = None

        self._is_allocated = False
        # RLock on device allocation
        self._allocation_lock = RLock()
    # end def __init__

    def __del__(self):
        """
        Close the LibusbDriver instance.
        Unallocate the device
        Close the USB context
        """
        # The delete method of this object is called at the end of the testsuite, the USB charging cable is turned on
        self.turn_on_usb_charging_cable()
        self.unallocate()
    # end def __del__

    @classmethod
    def discover_product(cls, pid, vid=None):
        """
        Try to find a product with matching PID and VID

        :param pid: Product ID
        :type pid: ``int``
        :param vid: Vendor ID
        :type vid: ``int``
        :return: True if found
        :rtype: ``bool``
        """
        vid = vid if vid is not None else VendorId.LOGITECH_INC
        found = False
        if cls.USB_CONTEXT_CLASS is not None and len(cls.USB_CONTEXT_CLASS.get_plugged_devices(vid=vid, pid=pid)) > 0:
            found = True
        # end if
        return found
    # end def discover_product

    @classmethod
    def discover_emulator(cls):
        """
        The scan function of this module tries to find a graviton emulator board.

        :return: True if a Graviton Emulator board is found
        :rtype: ``bool``
        """
        """
        CRO: 
            discover_emulator shall be removed.
            FYI: graviton emulator will be replaced by the Kosmos at a given time.
        """
        return cls.discover_product(pid=ProductId.LOGITECH_GRAVITON_EMULATOR)
    # end def discover_emulator

    @classmethod
    def discover_gotthard(cls):
        """
        Try to find a Gotthard receiver on the current setup

        :return: True if a Gotthard receiver is found
        :rtype: ``bool``
        """
        if cls.GOTTHARD_DETECTED is None:
            cls.GOTTHARD_DETECTED = cls.discover_product(pid=ProductId.LOGITECH_GOTTHARD_RECEIVER)
        # end if
        return cls.GOTTHARD_DETECTED
    # end def discover_gotthard

    @classmethod
    def discover_ble_pro_receiver(cls):
        """
        Try to find a BLE Pro receiver on the current setup

        :return: Flag indicating if a BLE Pro receiver is found
        :rtype: ``bool``
        """
        if cls.BLE_PRO_RECEIVER_DETECTED is None:
            iter_pids = iter(LogitechReceiverProductId.ble_pro_pids())
            pid = next(iter_pids, False)
            while not cls.BLE_PRO_RECEIVER_DETECTED and pid:
                cls.BLE_PRO_RECEIVER_DETECTED = cls.discover_product(pid=pid)
                pid = next(iter_pids, False)
            # end while
        # end if
        return cls.BLE_PRO_RECEIVER_DETECTED
    # end def discover_ble_pro_receiver

    @classmethod
    def discover_crush_receiver(cls):
        """
        Try to find a Crush receiver on the current setup

        :return: True if a Crush receiver is found
        :rtype: ``bool``
        """
        if cls.CRUSH_RECEIVER_DETECTED is None:
            cls.CRUSH_RECEIVER_DETECTED = cls.discover_product(pid=ProductId.LOGITECH_CRUSH_RECEIVER)
        # end if
        return cls.CRUSH_RECEIVER_DETECTED
    # end def discover_crush_receiver

    @classmethod
    def discover_usb_hub(cls):
        """
        The scan function of this module tries to find usb hubs as HUB boards.

        :return: The usb hub list is discovered during the first method execution than cached for all following calls
        :rtype: ``list[SmartUsbHub]``
        """
        if LibusbDriver.USB_HUB_LIST is not None:
            return LibusbDriver.USB_HUB_LIST
        # end if

        usb_hub_list = []
        # noinspection PyBroadException
        try:
            usb_hub_id_list = SmartUsbHub.get_smart_usb_hub_location()
        except Exception:
            LibusbDriver.USB_HUB_LIST = usb_hub_list
            return usb_hub_list
        # end try

        for hub_id in usb_hub_id_list:
            hub = SmartUsbHub(hub_id=hub_id, port_count=UsbHubUtils.PHIDGETS_HUB0003_NUMBER_PORTS)
            for p in range(1, UsbHubUtils.PHIDGETS_HUB0003_NUMBER_PORTS + 1):
                # Disable only charging port
                action = UsbHubAction.ON \
                    if p not in [LibusbDriver.CHARGING_PORT_NUMBER,
                                 LibusbDriver.CRUSH_PAD_EMULATOR_PORT_NUMBER if cls.IS_PORT6_DISABLED else None] \
                    else UsbHubAction.OFF
                hub.set_usb_ports_status(port_index=p, status=action)
            # end for
            usb_hub_list.append(hub)
            # end if
        # end for

        LibusbDriver.USB_HUB_LIST = usb_hub_list
        LibusbDriver.USB_CHARGING_CABLE_ENABLE = False
        LibusbDriver.CRUSH_PAD_CHARGING_EMULATOR_ENABLE = False

        return usb_hub_list
    # end def discover_usb_hub

    @classmethod
    def discover_debug_probe(cls):
        """
        This scanning function counts the number of connected flashing module.

        :return: The number of connected flashing module
        :rtype: ``int``
        """
        if LibusbDriver.PROBE_COUNT is not None:
            return LibusbDriver.PROBE_COUNT
        # end if

        if cls.USB_CONTEXT_CLASS is not None:
            LibusbDriver.PROBE_COUNT = len(cls.USB_CONTEXT_CLASS.get_plugged_devices(
                vid=[VendorId.SEGGER_MICROCONTROLLER_SYSTEM_GMBH, VendorId.MAAXTER, VendorId.ST_MICROELECTRONICS],
                pid=[ProductId.SEGGER_J_LINK,
                     ProductId.SEGGER_J_LINK_PLUS,
                     ProductId.NRF52_DK_V1,
                     ProductId.NRF52_DK_V2,
                     ProductId.NRF52_DK_V3,
                     ProductId.TELINK_MAXXTER,
                     ProductId.ST_LINK_V2_PROBE]))
        # end if

        return LibusbDriver.PROBE_COUNT
    # end def discover_debug_probe

    @classmethod
    def discover_beagle_480(cls):
        """
        Check if a Beagle 480 USB analyser is connected on the test setup.

        :return: Flag indicating that a Beagle 480 is present
        :rtype: ``bool``
        """
        if LibusbDriver.BEAGLE_480_DETECTED is not None:
            return LibusbDriver.BEAGLE_480_DETECTED
        # end if

        if cls.USB_CONTEXT_CLASS is not None:
            LibusbDriver.BEAGLE_480_DETECTED = len(cls.USB_CONTEXT_CLASS.get_plugged_devices(
                vid=[VendorId.TOTAL_PHASE], pid=[ProductId.BEAGLE_USB_480]))
        # end if

        return LibusbDriver.BEAGLE_480_DETECTED
    # end def discover_beagle_480

    @staticmethod
    def is_usb_channel(channel):
        """
        Check if a channel is USB or not.

        :param channel: Channel to check
        :type channel: ``BaseCommunicationChannel``

        :return: Flag indicating if the channel is USB
        :rtype: ``bool``
        """
        return channel.protocol == LogitechProtocol.USB
    # end def is_usb_channel

    @staticmethod
    def is_usb_channel_on_hub(channel):
        """
        Check if a channel is on a hub.

        :param channel: Channel to check
        :type channel: ``BaseCommunicationChannel``

        :return: Flag indicating if the channel is on a hub
        :rtype: ``bool``
        """
        if isinstance(channel, (UsbChannel, ThroughReceiverChannel)):
            return len(channel.get_channel_usb_port_path_list()) >= UsbHubUtils.DEVICE_ON_HUB_PORT_PATH_DEPTH
        # end if

        return False
    # end def is_usb_channel_on_hub

    @staticmethod
    def is_hub_port_associated_to_channel(channel, port_index):
        """
        Check if a channel is associated with a port index on a hub.

        :param channel: Channel to check
        :type channel: ``BaseCommunicationChannel``
        :param port_index: Port index to check
        :type port_index: ``int``

        :return: Flag indicating if the channel is associated with the port index
        :rtype: ``bool``
        """
        if isinstance(channel, (UsbChannel, ThroughReceiverChannel)):
            port_path = channel.get_channel_usb_port_path_list()

            if len(port_path) < UsbHubUtils.DEVICE_ON_HUB_PORT_PATH_DEPTH:
                # Channel not on a hub
                return False
            # end if

            return port_path[-1] == port_index
        # end if

        return False
    # end def is_hub_port_associated_to_channel

    @classmethod
    def generate_usb_config_file(cls, full_path=None):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.configure
        From those arguments are extracted:
        - path: The path where the @c Libusb.ini configuration file should be generated.
        """
        if LibusbDriver.USB_CONTEXT is not None and full_path is None:
            if cls.USB_CONTEXT.CONFIG_DIRECTORY_PATH is None:
                raise ValueError('Missing argument for configuration: full-path')
            # end if

            full_path = cls.USB_CONTEXT.CONFIG_DIRECTORY_PATH
        # end if

        # All USB port should be ON to generate a configuration file with all devices
        usb_hub_list = cls.discover_usb_hub()
        hub_port_states = {}
        for usb_hub in usb_hub_list:
            hub_port_states[usb_hub] = {}
            for port in range(1, usb_hub.port_count + 1):
                # Save current usb port state
                current_status = usb_hub.get_usb_ports_status(port_index=port)
                if current_status != UsbHubAction.ON:
                    # If the port is not ON, save the current state
                    hub_port_states[usb_hub][port] = current_status
                    # Then change its state to ON
                    usb_hub.set_usb_ports_status(port_index=port, status=UsbHubAction.ON)
                # end if
            # end for
        # end for

        # Add a small waiting period to let libusb to recognize that all port
        sleep(1)

        # Generate the configuration file
        if cls.USB_CONTEXT_CLASS is not None:
            cls.USB_CONTEXT_CLASS.generate_configuration_file(path=dirname(full_path), vid=cls.ACCEPTED_VID)
        # end if

        # All USB port for which the state was changed should be set back to the state saved previously
        for usb_hub in usb_hub_list:
            for port in hub_port_states[usb_hub]:
                usb_hub.set_usb_ports_status(port_index=port, status=hub_port_states[usb_hub][port])
            # end for
        # end for
    # end def generate_usb_config_file

    @classmethod
    def configure(cls, **kwargs):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.configure

        From those arguments are extracted:
        - path: The path where the current @c Libusb.ini configuration file can be found.
        - usb_context_class: The usb context class to use.
        - force_reconfigure: Flag indicating to force the reconfiguration if already done
        - feature: Context features used for kosmos (or standalone power supply emulator) initialization
        """
        if "force_reconfigure" in kwargs:
            force_reconfigure = kwargs["force_reconfigure"]
        else:
            force_reconfigure = False
        # end if

        if cls.IS_CONFIGURED and not force_reconfigure:
            return
        # end if

        if "features" in kwargs:
            features = kwargs["features"]
            if features is not None:
                # The imports are local because configurationmanager and emulatorsmanager import LibusbDriver, so we
                # need to avoid mutual import at the global level
                from pytestbox.base.configurationmanager import ConfigurationManager
                from pytestbox.base.emulatorsmanager import EmulatorsManager
                configuration_manager = ConfigurationManager(features=features)
                emulators_manager = EmulatorsManager.get_instance(features=features)

                # Initialize kosmos and all emulators
                emulators_manager.init_kosmos()
                emulators_manager.init_power_supply()
                emulators_manager.init_power_slider_emulator()
                emulators_manager.init_button_emulator(configuration_manager.current_device_type)
                emulators_manager.init_ambient_light_sensor_emulator()
                emulators_manager.init_proximity_sensor_emulator()
                emulators_manager.init_led_monitoring_service()
                emulators_manager.init_led_spy_over_i2c_monitoring_service()
                emulators_manager.init_motion_emulator()
                # No need to turn on the switch because it will already be on after the initialization method
                emulators_manager.init_jlink_io_switch()

                # Turn on the device before the channel device manager cache initialization
                if emulators_manager.power_supply_emulator is not None:
                    emulators_manager.power_supply_emulator.turn_on()
                # end if
                if emulators_manager.power_slider_emulator is not None:
                    emulators_manager.power_slider_emulator.power_on()
                # end if
            # end if
            # Port 6 is disabled by default when DUT supports wireless charging tests
            cls.IS_PORT6_DISABLED = features.PRODUCT.DEVICE.BATTERY.F_WirelessCharging
        # end if

        if FORCE_USB_CONTEXT_CLASS is not None:
            cls.USB_CONTEXT_CLASS = FORCE_USB_CONTEXT_CLASS
        elif "usb_context_class" in kwargs:
            usb_context_class = kwargs["usb_context_class"]
            if isinstance(usb_context_class, type) and issubclass(usb_context_class, UsbContext):
                cls.USB_CONTEXT_CLASS = usb_context_class
            elif usb_context_class is not None:
                raise ValueError(f"usb_context_class parameter should be a type to be used as a USB "
                                 f"context, {usb_context_class} is not")
            # end if
        # end if

        if "path" not in kwargs and cls.USB_CONTEXT_CLASS is not None:
            if cls.USB_CONTEXT_CLASS.CONFIG_DIRECTORY_PATH is None:
                raise ValueError('Missing argument for first configuration: path')
            # end if

            path = cls.USB_CONTEXT_CLASS.CONFIG_DIRECTORY_PATH
        else:
            path = kwargs["path"]

            if cls.USB_CONTEXT_CLASS is not None:
                if path is None and cls.USB_CONTEXT_CLASS.CONFIG_DIRECTORY_PATH is None:
                    raise ValueError('Argument path should not be None for the first configuration')
                # end if
            # end if
        # end if

        if VERBOSE:
            start_time = time()
        else:
            start_time = 0
        # end if

        ###########################
        #           BLE           #
        ###########################
        if len(NrfBleLibBleContext.get_bt_stack_devices_com_ports()) > 0:
            if cls.BLE_CONTEXT is None:
                cls.BLE_CONTEXT = NrfBleLibBleContext()
            # end if

            stdout.write("BLE context in use: NrfBleLibBleContext\n")

            # For now the path is the same as the USB context
            BleContext.CONFIG_DIRECTORY_PATH = path
            stdout.write("\tNo BLE channel found\n")
        else:
            stdout.write("No BLE context hardware found\n")
        # end if

        ###########################
        #           USB           #
        ###########################
        if cls.USB_CONTEXT_CLASS is not None:
            if cls.USB_CONTEXT is None:
                cls.USB_CONTEXT = cls.USB_CONTEXT_CLASS()
            # end if

            stdout.write(f"USB context in use: {cls.USB_CONTEXT_CLASS.__name__}\n")

            cls.USB_CHANNEL_MAPPING.clear()
            usb_config_file_path = join(path, cls.USB_CONTEXT_CLASS.CONFIG_FILE_NAME)
            if FORCE_REGENERATE_USB_CONFIG_FILE or not access(usb_config_file_path, R_OK):
                cls.generate_usb_config_file(usb_config_file_path)
            # end if

            cls.USB_CONTEXT.CONFIG_DIRECTORY_PATH = path

            cls.USB_CONTEXT_CLASS.configure_device_cache(path=path, vid=cls.ACCEPTED_VID)
            cls.USB_CONTEXT.open()

            try:
                usb_devices = cls.USB_CONTEXT.get_devices(vid=cls.ACCEPTED_VID)
                receiver_channels = []
                usb_hub_list = cls.discover_usb_hub()
                disable_usb_after = False
                log_to_print = ""
                for usb_device in usb_devices:
                    # Gothard PID has been excluded of LogitechReceiverProductId for now because it is not a user
                    # receiver and in our tests it will not be used as primary receiver for now
                    if LogitechReceiverProductId.has_value(usb_device.pid):
                        # For now, we use 6 device for all receiver because this is the specification for BLE pro and
                        # eQuad step 4 DJ. In the device manager this will be done differently by reading the register
                        # 0xB5 at 0x02 or 0x03 to know the actual value
                        usb_channel = UsbReceiverChannel(
                            max_number_of_paired_devices=cls.MAX_NUMBER_OF_DEVICE_IN_RECEIVER,
                            usb_context=cls.USB_CONTEXT,
                            usb_context_device=usb_device)
                        receiver_channels.append(usb_channel)
                    elif usb_device.pid == ProductId.LOGITECH_GOTTHARD_RECEIVER:
                        usb_channel = GotthardReceiverChannel(
                            max_number_of_paired_devices=cls.MAX_NUMBER_OF_DEVICE_IN_RECEIVER,
                            usb_context=cls.USB_CONTEXT,
                            usb_context_device=usb_device)
                    else:
                        usb_channel = UsbChannel(usb_context=cls.USB_CONTEXT, usb_context_device=usb_device)
                    # end if
                    if cls.is_usb_channel_on_hub(usb_channel):
                        port_index = usb_channel.get_channel_usb_port_path_list()[-1]
                    else:
                        port_index = cls.NON_HUB_USB_PORT_INDEX
                        assert port_index not in cls.USB_CHANNEL_MAPPING, \
                            "Cannot have more than one device not on USB hub"
                    # end if

                    cls.USB_CHANNEL_MAPPING[port_index] = usb_channel
                    # Get the device descriptors of each USB channel to initialize the HID dispatcher data collections
                    # and report id list
                    # The USB device open close operation also seems to unlock libusb driver polling mechanism when
                    # locked because of too many devices plugged in
                    if port_index > cls.NON_HUB_USB_PORT_INDEX and len(usb_hub_list) > 0 and \
                            usb_hub_list[0].get_usb_ports_status(port_index=port_index) != UsbHubAction.ON:
                        disable_usb_after = True
                        # Enable the USB port before configuration
                        cls.enable_usb_port(port_index=port_index)
                    # end if
                    usb_channel.open()
                    usb_channel.get_descriptors()
                    usb_channel.close()
                    if disable_usb_after:
                        # Disable the USB port after configuration if it was disabled before configuration
                        cls.disable_usb_port(port_index=port_index)
                        disable_usb_after = False
                    # end if

                    log_to_print += f"\t\t{usb_channel}\n"
                # end for

                if log_to_print == "":
                    stdout.write("\tNo USB channel found\n")
                else:
                    stdout.write(f"\tUSB channel(s) found:\n{log_to_print}")
                # end if

                ###########################
                #     Through receiver    #
                ###########################
                cls.THROUGH_RECEIVER_CHANNEL_MAPPING.clear()
                log_to_print = ""
                for receiver_channel in receiver_channels:
                    # For now there are the BLE Pro receiver and the others are eQuad
                    # TODO For now we use some default protocol, we need to find a better way of specifying this, maybe
                    #  the transport ID of the paired device or the product ID of the receiver can help us find the
                    #  right one
                    if receiver_channel.get_usb_pid() in [LogitechReceiverProductId.GRAVITY_BLE_PRO,
                                                          LogitechReceiverProductId.MEZZY_BLE_PRO,
                                                          LogitechReceiverProductId.QBERT_BLE_PRO,
                                                          LogitechReceiverProductId.COILY_BLE_PRO]:
                        channel_class = ThroughBleProReceiverChannel
                        default_protocol = LogitechProtocol.BLE_PRO
                    else:
                        channel_class = ThroughEQuadReceiverChannel
                        default_protocol = LogitechProtocol.EQUAD_STEP_4_DJ
                    # end if

                    receiver_channel.open()
                    # Set IDLE to 0 on keyboard interface
                    receiver_channel.hid_class_specific_request(
                        interface_id=receiver_channel.report_type_to_interface.get(LogitechReportType.KEYBOARD, None),
                        w_value=0)
                    receiver_channel.enable_hidpp_reporting(enable=True)
                    if cls.is_usb_channel_on_hub(receiver_channel):
                        port_index = receiver_channel.get_channel_usb_port_path_list()[-1]
                    else:
                        port_index = cls.NON_HUB_USB_PORT_INDEX
                        # No need to check if multiple device not on hub as it was done previously
                    # end if

                    try:
                        for device_index in range(1, cls.MAX_NUMBER_OF_DEVICE_IN_RECEIVER + 1):
                            through_receiver_channel = channel_class(
                                receiver_channel=receiver_channel, device_index=device_index)
                            through_receiver_channel.protocol = default_protocol

                            # noinspection PyBroadException
                            try:
                                through_receiver_channel.get_device_info(force_refresh_cache=True)
                                through_receiver_channel.is_device_connected(force_refresh_cache=True)
                                cls.THROUGH_RECEIVER_CHANNEL_MAPPING[(port_index, device_index)] = \
                                    through_receiver_channel
                                log_to_print += f"\t{through_receiver_channel}\n"
                            except Exception:
                                pass
                            # end try
                        # end for
                    finally:
                        receiver_channel.close()
                    # end try
                # end for

                if log_to_print == "":
                    stdout.write("No channel through receiver found\n")
                else:
                    stdout.write(f"Channel(s) through receiver found:\n{log_to_print}")
                # end if
            finally:
                cls.USB_CONTEXT.close()
            # end try
        else:
            stdout.write("No USB context configured\n")
        # end if

        cls.IS_CONFIGURED = True

        if VERBOSE:
            stdout.write(f"\nDevice manager configuration took {time() - start_time}\n")
        else:
            stdout.write("\n")
        # end if
    # end def configure

    @classmethod
    def is_ble_context_present(cls):
        """
        Check if the BLE context hardware is present

        :return: Flag indicating if there is a BLE context hardware
        :rtype: ``bool``
        """
        return len(NrfBleLibBleContext.get_bt_stack_devices_com_ports()) > 0
    # end def is_ble_context_present

    @classmethod
    def reset_ble_context_hardware(cls, debugger):
        """
        Update the BLE context hardware

        :param debugger: JLink to use to update the firmware
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        """
        if isinstance(cls.BLE_CONTEXT, (NrfBleLibBleContext, )):
            cls.BLE_CONTEXT.reset_context_hardware(debugger=debugger)
        # end if
    # end def reset_ble_context_hardware

    @classmethod
    def update_ble_context_hardware(cls, ble_context_class_id, debugger, jlink_connection_control, force):
        """
        Update the BLE context hardware

        :param ble_context_class_id: The BLE context class ID to choose the right firmware to load on the DK, valid
                                     values can be found in ``BleContextClassId`` (it can be the item in the enum, the
                                     value in the enum or the name in the enum)
        :type ble_context_class_id: ``BleContextClassId`` or ``int`` or ``str``
        :param debugger: JLink to use to update the firmware
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        :param jlink_connection_control: JLink connection control to use to select the DK
        :type jlink_connection_control: ``pyraspi.services.jlinkconnectioncontrol.JlinkConnectionControl``
        :param force: Flag indicating to force the update, even if the hardware is already up-to-date - OPTIONAL
        :type force: ``bool``
        """
        assert ble_context_class_id in BleContextClassId, f"Unknown ble_context_class_id = {ble_context_class_id}"

        ble_context_class_id = BleContextClassId(ble_context_class_id)

        if not force and (ble_context_class_id == BleContextClassId.NO_CONTEXT and cls.BLE_CONTEXT is None) or \
                (ble_context_class_id == BleContextClassId.NRF_BLE_LIB and
                 isinstance(cls.BLE_CONTEXT, NrfBleLibBleContext)):
            return
        # end if

        if cls.BLE_CONTEXT is not None:
            cls.BLE_CONTEXT.close()
            cls.BLE_CONTEXT = None
        # end if

        with debugger.closed():
            with jlink_connection_control.disconnected():
                if ble_context_class_id == BleContextClassId.NRF_BLE_LIB:
                    NrfBleLibBleContext.update_context_hardware(debugger=debugger, force=force)
                else:
                    assert ble_context_class_id == BleContextClassId.NO_CONTEXT
                    if cls.is_ble_context_present() or force:
                        # BleContextClassId.NO_CONTEXT
                        with debugger.opened_with_mcu_name(mcu_name=cls.BLE_CONTEXT_MCU_NAME, unlock_device=True):
                            debugger.erase_firmware()
                        # end with
                    # end if
                # end if
            # end with
        # end with

        # The creation and open/close of the BLE context were done outside the jlink switch to improve connection
        # stability.
        if ble_context_class_id == BleContextClassId.NRF_BLE_LIB:
            cls.BLE_CONTEXT = NrfBleLibBleContext()
        # end if

        if cls.BLE_CONTEXT is not None:
            cls.BLE_CONTEXT.open()
            cls.BLE_CONTEXT.close()
        # end if
    # end def update_ble_context_hardware

    # ------------------------------------------------------------------------------
    #                           Public interface
    # ------------------------------------------------------------------------------
    def is_allocated(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.is_allocated
        """
        with self._allocation_lock:
            return self._is_allocated
        # end with
    # end def is_allocated

    def allocate(self):
        # See ``BaseSmartDevice.allocate``
        with self._allocation_lock:
            if not self._is_allocated and LibusbDriver.USB_CONTEXT is not None:
                try:
                    LibusbDriver.USB_CONTEXT.open()
                except Exception:
                    if LibusbDriver.USB_CONTEXT.is_open:
                        LibusbDriver.USB_CONTEXT.close()
                    # end if
                    raise
                # end try

                self._is_allocated = True
            # end if
        # end with
    # end def allocate

    def unallocate(self):
        """
        Disconnection from real devices.
        """
        with self._allocation_lock:
            if self._is_allocated:
                for channel in self.get_all_cached_channels_in_list():
                    channel.close()
                # end for

                if LibusbDriver.BLE_CONTEXT is not None and LibusbDriver.BLE_CONTEXT.is_open:
                    LibusbDriver.BLE_CONTEXT.close()
                # end if
                if LibusbDriver.USB_CONTEXT is not None:
                    LibusbDriver.USB_CONTEXT.close()
                # end if

                self._is_allocated = False
            # end if
        # end with
    # end def unallocate

    @staticmethod
    def _set_usb_ports_status(port_index, status):
        LibusbDriver.USB_HUB_LIST[0].set_usb_ports_status(port_index=port_index, status=status)
        sleep(1)

        if LibusbDriver.USB_CONTEXT is not None and not \
                LibusbDriver.USB_CONTEXT.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
            LibusbDriver.USB_CONTEXT.update_device_list()
        # end if
        return LibusbDriver.USB_HUB_LIST[0].get_usb_ports_status(port_index=port_index) == status
    # end def _set_usb_ports_status

    @staticmethod
    @synchronized(HUB_LOCK)
    def enable_usb_port(port_index):
        """
        Enable an usb port located on a HUB board

        :param port_index: USB port position
        :type port_index: ``int``

        :return: True if port enabled False otherwise
        :rtype: ``bool``
        """
        assert len(LibusbDriver.discover_usb_hub()) > 0, "No HUB present"

        return LibusbDriver._set_usb_ports_status(port_index=port_index, status=UsbHubAction.ON)
    # end def enable_usb_port

    @staticmethod
    @synchronized(HUB_LOCK)
    def disable_usb_port(port_index):
        """
        Disable an usb port located on a HUB board

        :param port_index: USB port position
        :type port_index: ``int``

        :return: True if port disabled False otherwise
        :rtype: ``bool``
        """
        assert len(LibusbDriver.discover_usb_hub()) > 0, "No HUB present"

        if port_index in LibusbDriver.USB_CHANNEL_MAPPING:
            LibusbDriver.USB_CHANNEL_MAPPING[port_index].close()
        # end if

        return LibusbDriver._set_usb_ports_status(port_index=port_index, status=UsbHubAction.OFF)
    # end def disable_usb_port

    @classmethod
    def enable_all_usb_ports(cls, enable_charging=False):
        """
        Enable all usb ports located on a HUB board. The port used for charging is treated on its own using the
        ``enable_charging`` parameter.

        :param enable_charging: Flag indicating to enable the charging port
        :type enable_charging: ``bool``
        """
        assert len(LibusbDriver.discover_usb_hub()) > 0, "No HUB present"

        ports_on_off_config = {}
        for p in range(1, UsbHubUtils.PHIDGETS_HUB0003_NUMBER_PORTS + 1):
            if enable_charging:
                ports_on_off_config[p] = True
            else:
                if p in [cls.CHARGING_PORT_NUMBER,
                         cls.CRUSH_PAD_EMULATOR_PORT_NUMBER if cls.IS_PORT6_DISABLED else None]:
                    ports_on_off_config[p] = False
                else:
                    ports_on_off_config[p] = True
                # end if
            # end if
        # end for

        return cls.set_usb_ports_status(ports_on_off_config=ports_on_off_config)
    # end def enable_all_usb_ports

    @classmethod
    def disable_all_usb_ports(cls, disable_charging=False):
        """
        Disable all usb ports located on a HUB board. The port used for charging is treated on its own using the
        ``disable_charging`` parameter.

        :param disable_charging: Flag indicating to disable the charging port
        :type disable_charging: ``bool``
        """
        assert len(LibusbDriver.discover_usb_hub()) > 0, "No HUB present"

        ports_on_off_config = {}
        for p in range(1, UsbHubUtils.PHIDGETS_HUB0003_NUMBER_PORTS + 1):
            if p != cls.CHARGING_PORT_NUMBER or disable_charging:
                ports_on_off_config[p] = False
            # end if
        # end for

        return cls.set_usb_ports_status(ports_on_off_config=ports_on_off_config)
    # end def disable_all_usb_ports

    @staticmethod
    def get_usb_ports_status():
        """
        Get the usb port enable/disable status for DLink USB Hub

        :return: ports,  looks like below
            {1: False, 2: True, 3: False, 4: False, 5: False, 6: False, 7: False}
        :rtype: ``dict[int, bool]``
        """
        assert len(LibusbDriver.discover_usb_hub()) > 0, "No HUB present"

        ports = {}
        for port in range(1, LibusbDriver.USB_HUB_LIST[0].port_count + 1):
            ports[port] = LibusbDriver.USB_HUB_LIST[0].get_usb_ports_status(port_index=port) == UsbHubAction.ON
        # end for
        return ports
    # end def get_usb_ports_status

    @staticmethod
    @synchronized(HUB_LOCK)
    def set_usb_ports_status(ports_on_off_config, loops=10):
        """
        Set the usb port enable/disable status for DLink USB Hub

        :param ports_on_off_config: looks like below
            {1: False, 2: True, 3: False, 4: False, 5: False, 6: False, 7: False}
        :type ports_on_off_config: ``dict[int, bool]``

        :param loops: retry times
        :type loops: ``int``

        :return: status, True if success, False otherwise
                 loop_retry_counter, how many loops to make the ports status as wished
        :rtype: ``bool, int``
        """
        assert len(LibusbDriver.discover_usb_hub()) > 0, "No HUB present"

        counter = 0
        success = False
        while not success and counter < loops:
            # noinspection PyBroadException
            try:
                for port in ports_on_off_config:
                    status = UsbHubAction.ON if ports_on_off_config[port] else UsbHubAction.OFF
                    LibusbDriver.USB_HUB_LIST[0].set_usb_ports_status(port_index=port, status=status)
                # end for
                success = True
            except Exception:
                counter += 1
            # end try
        # end while

        sleep(LibusbDriver.ASYNCHRONOUS_CONNECTION_DISCONNECTION_DELAY)
        if LibusbDriver.USB_CONTEXT is not None and not \
                LibusbDriver.USB_CONTEXT.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
            LibusbDriver.USB_CONTEXT.update_device_list()
        # end if

        return success, counter+1
    # end def set_usb_ports_status

    @staticmethod
    @synchronized(HUB_LOCK)
    def turn_on_usb_charging_cable(force=False):
        """
        Turn on power for USB charging cable on Phidgets USB Hub
            - Logical port number = 5

        :param force:  Set True to force turning on port
        :type force: ``bool``
        """
        if len(LibusbDriver.discover_usb_hub()) == 0:
            return
        elif LibusbDriver.USB_CHARGING_CABLE_ENABLE and not force:
            return
        # end if

        LibusbDriver.USB_HUB_LIST[0].set_usb_ports_status(
            port_index=LibusbDriver.CHARGING_PORT_NUMBER, status=UsbHubAction.ON)

        if LibusbDriver.USB_CONTEXT is not None and not \
                LibusbDriver.USB_CONTEXT.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
            sleep(LibusbDriver.ASYNCHRONOUS_CONNECTION_DISCONNECTION_DELAY)
            LibusbDriver.USB_CONTEXT.update_device_list()
        elif LibusbDriver.CHARGING_PORT_NUMBER in LibusbDriver.USB_CHANNEL_MAPPING:
            LibusbDriver.USB_CHANNEL_MAPPING[LibusbDriver.CHARGING_PORT_NUMBER].wait_device_connection_state(
                connected=True, timeout=LibusbDriver.ASYNCHRONOUS_CONNECTION_DISCONNECTION_DELAY)
        # end if
        LibusbDriver.USB_CHARGING_CABLE_ENABLE = True
    # end def turn_on_usb_charging_cable

    @staticmethod
    @synchronized(HUB_LOCK)
    def turn_off_usb_charging_cable(force=False):
        """
        Turn off power for USB charging cable on Phidgets USB Hub
            - Logical port number = 5

        :param force:  Set True to force turning off port
        :type force: ``bool``
        """
        if len(LibusbDriver.discover_usb_hub()) == 0:
            return
        elif not LibusbDriver.USB_CHARGING_CABLE_ENABLE and not force:
            return
        # end if

        if LibusbDriver.CHARGING_PORT_NUMBER in LibusbDriver.USB_CHANNEL_MAPPING:
            LibusbDriver.USB_CHANNEL_MAPPING[LibusbDriver.CHARGING_PORT_NUMBER].close()
        # end if

        LibusbDriver.USB_HUB_LIST[0].set_usb_ports_status(
            port_index=LibusbDriver.CHARGING_PORT_NUMBER, status=UsbHubAction.OFF)

        if not LibusbDriver.USB_CONTEXT.ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY:
            sleep(LibusbDriver.ASYNCHRONOUS_CONNECTION_DISCONNECTION_DELAY)
            LibusbDriver.USB_CONTEXT.update_device_list()
        elif LibusbDriver.CHARGING_PORT_NUMBER in LibusbDriver.USB_CHANNEL_MAPPING:
            LibusbDriver.USB_CHANNEL_MAPPING[LibusbDriver.CHARGING_PORT_NUMBER].wait_device_connection_state(
                connected=False, timeout=LibusbDriver.ASYNCHRONOUS_CONNECTION_DISCONNECTION_DELAY)
        # end if
        LibusbDriver.USB_CHARGING_CABLE_ENABLE = False
    # end def turn_off_usb_charging_cable

    @staticmethod
    @synchronized(HUB_LOCK)
    def turn_on_crush_pad_charging_emulator(force=False, delay=1):
        """
        Turn on power for Crush Pad charging emulator on Phidgets USB hub
            - Logical port number = 6

        :param force: Set True to force turning on the port
        :type force: ``bool``
        :param delay: The delay time which ensures the device is entering wireless charging mode
        :type delay: ``bool``
        """
        if len(LibusbDriver.discover_usb_hub()) == 0:
            return
        # end if
        if LibusbDriver.CRUSH_PAD_CHARGING_EMULATOR_ENABLE and not force:
            return
        # end if

        LibusbDriver.USB_HUB_LIST[0].set_usb_ports_status(port_index=LibusbDriver.CRUSH_PAD_EMULATOR_PORT_NUMBER,
                                                          status=UsbHubAction.ON)
        if delay:
            sleep(delay)
        # end if

        LibusbDriver.CRUSH_PAD_CHARGING_EMULATOR_ENABLE = True
    # end def turn_on_crush_pad_charging_emulator

    @staticmethod
    @synchronized(HUB_LOCK)
    def turn_off_crush_pad_charging_emulator(force=False):
        """
        Turn off power for Crush Pad charging emulator on Phidgets USB hub
            - Logical port number = 6

        :param force: Set True to force turning off the port
        :type force: ``bool``
        """
        if len(LibusbDriver.discover_usb_hub()) == 0:
            return
        # end if
        if not LibusbDriver.CRUSH_PAD_CHARGING_EMULATOR_ENABLE and not force:
            return
        # end if

        if LibusbDriver.CRUSH_PAD_EMULATOR_PORT_NUMBER in LibusbDriver.USB_CHANNEL_MAPPING:
            LibusbDriver.USB_CHANNEL_MAPPING[LibusbDriver.CRUSH_PAD_EMULATOR_PORT_NUMBER].close()
        # end if

        LibusbDriver.USB_HUB_LIST[0].set_usb_ports_status(port_index=LibusbDriver.CRUSH_PAD_EMULATOR_PORT_NUMBER,
                                                          status=UsbHubAction.OFF)

        LibusbDriver.CRUSH_PAD_CHARGING_EMULATOR_ENABLE = False
    # end def turn_off_crush_pad_charging_emulator

    def powerUp(self, port=0):
        """
        Get device's vendor identifier and product identifier inserted in a given port

        :param port: Index of the device:
                     - 0 on mono-host configuration (default value)
                     - 1, 2, 3, etc... on multi-host configuration (HUB board)
        :type port: ``int``
        """
        device = self.USB_CHANNEL_MAPPING[port]
        return HexList(f"{device.get_usb_vid():04X}{device.get_usb_pid():04X}")
    # end def powerUp

    def isPoweredUp(self):
        # See ``BaseSmartDevice.isPoweredUp``
        return self.is_allocated()
    # end def isPoweredUp

    def init(self, port=None, claim_all=False):
        """
        Take the control over a USB device

        :param  port: index of the device.
            - None: stay on the same host (default value)
            - 0: on mono-host configuration
            - 0, 1 or 2: on multi-host configuration (HUB board)
        :type port: ``int``
        :param claim_all: Flag indicating to claim the interfaces from all the connected receivers
        :type claim_all: ``bool``
        """
        # Useless
        pass
    # end def init

    def powerDown(self):
        # See ``BaseSmartDevice.powerDown``
        pass
    # end def powerDown

    def getDriverInfo(self):
        # See ``BaseSmartDevice.getDriverInfo``
        if self.USB_CONTEXT_CLASS is not None:
            return type(self).USB_CONTEXT_CLASS.get_driver_info()
        else:
            return None
        # end if
    # end def getDriverInfo

    def setTearing(self, tearing_time):
        # See ``BaseSmartDevice.setTearing``
        raise NotImplementedError
    # end def setTearing

    def getElapsedTime(self):
        # See ``BaseSmartDevice.sendRaw``
        return 0
    # end def getElapsedTime

    def sendRaw(self, *data):
        # See ``BaseSmartDevice.sendRaw``
        raise NotImplementedError
    # end def sendRaw

    def reset(self):
        # See ``BaseSmartDevice.reset``
        raise NotImplementedError
    # end def reset

    @classmethod
    def get_all_cached_channels_in_list(cls):
        """
        Get all the cached channels in a list.

        :return: The list of all cached channels
        :rtype: ``list[BaseCommunicationChannel]``
        """
        all_channels = []
        all_channels.extend(list(cls.USB_CHANNEL_MAPPING.values()))
        all_channels.extend(list(cls.THROUGH_RECEIVER_CHANNEL_MAPPING.values()))
        all_channels.extend(list(cls.BLE_CHANNEL_MAPPING.values()))
        return all_channels
    # end def get_all_cached_channels_in_list

    def get_channels(self, channel_ids, check_connected=False):
        """
        Get a list of channels from the cache matching the wanted channel identifier.

        :param channel_ids: The wanted channel identifier
        :type channel_ids: ``list[ChannelIdentifier]``
        :param check_connected: The wanted channel should be a connected one - OPTIONAL
        :type check_connected: ``bool``

        :return: A list of channels from the cache matching the given identifier
        :rtype: ``list[BaseCommunicationChannel]``
        """
        channels_to_return = []

        for channel_id in channel_ids:
            cache_list_to_use = self._get_cache_based_on_channel_identifier(channel_id=channel_id)

            for channel in cache_list_to_use:
                if self.is_channel_a_match(channel=channel, channel_id=channel_id, check_connected=check_connected):
                    channels_to_return.append(channel)
                # end if
            # end for
        # end for

        return channels_to_return
    # end def get_channels

    def get_channel(self, channel_ids, check_connected=False):
        """
        Get the first channel from the cache matching the wanted channel identifier. ``None`` is returned if nothing
        is found.

        :param channel_ids: The wanted channel identifier(s)
        :type channel_ids: ``list[ChannelIdentifier]``
        :param check_connected: The wanted channel should be a connected one - OPTIONAL
        :type check_connected: ``bool``

        :return: A list of channels from the cache matching the given identifier
        :rtype: ``BaseCommunicationChannel`` or ``None``
        """
        for channel_id in channel_ids:
            cache_list_to_use = self._get_cache_based_on_channel_identifier(channel_id=channel_id)

            for channel in cache_list_to_use:
                if self.is_channel_a_match(channel=channel, channel_id=channel_id, check_connected=check_connected):
                    return channel
                # end if
            # end for
        # end for

        return None
    # end def get_channel

    @classmethod
    def is_channel_a_match(cls, channel, channel_id, check_connected=False):
        """
        Check if a channel is matching a channel identifier. If no parameters are checked, it returns ``False``.

        :param channel: Channel to use
        :type channel: ``BaseCommunicationChannel``
        :param channel_id: Channel identifier to use
        :type channel_id: ``ChannelIdentifier``
        :param check_connected: The wanted channel should be a connected one - OPTIONAL
        :type check_connected: ``bool``

        :return: Flag indicating if the channel match the identifier
        :rtype: ``bool``
        """
        is_match = True
        at_least_one_parameter_check = False

        if channel_id.transport_id is not None:
            is_match &= (f"{channel.get_transport_id():04X}" == channel_id.transport_id)
            at_least_one_parameter_check = True
        # end if

        if channel_id.protocol is not None:
            is_match &= (channel.protocol == channel_id.protocol)
            at_least_one_parameter_check = True
        # end if

        if channel_id.port_index is not None:
            if isinstance(channel, (UsbChannel, ThroughReceiverChannel)):
                if LibusbDriver.is_usb_channel_on_hub(channel=channel):
                    is_match &= (channel.get_channel_usb_port_path_list()[-1] == channel_id.port_index)
                else:
                    is_match &= (cls.NON_HUB_USB_PORT_INDEX == channel_id.port_index)
                # end if
                at_least_one_parameter_check = True
            # end if
        # end if

        if channel_id.device_index is not None:
            if isinstance(channel, ThroughReceiverChannel):
                is_match &= (channel.device_index == channel_id.device_index)
                at_least_one_parameter_check = True
            # end if
        # end if

        if channel_id.vendor_id is not None:
            if isinstance(channel, UsbChannel):
                is_match &= (f"{channel.get_usb_vid():04X}" == channel_id.vendor_id)
                at_least_one_parameter_check = True
            elif isinstance(channel, ThroughReceiverChannel):
                is_match &= (f"{channel.receiver_channel.get_usb_vid():04X}" == channel_id.vendor_id)
                at_least_one_parameter_check = True
            # end if
        # end if

        if channel_id.product_id is not None:
            if isinstance(channel, UsbChannel):
                is_match &= (f"{channel.get_usb_pid():04X}" == channel_id.product_id)
                at_least_one_parameter_check = True
            elif isinstance(channel, ThroughReceiverChannel):
                is_match &= (f"{channel.receiver_channel.get_usb_pid():04X}" == channel_id.product_id)
                at_least_one_parameter_check = True
            # end if
        # end if

        if check_connected:
            is_match &= channel.is_device_connected()
        # end if

        return is_match and at_least_one_parameter_check
    # end def is_channel_a_match

    @classmethod
    def refresh_through_receiver_channel_cache(cls):
        """
        Refresh the through receiver channel cache. It will only delete the one in the cache that are not existing
        anymore. It will not add new ones.
        """
        cache_key_list = list(cls.THROUGH_RECEIVER_CHANNEL_MAPPING.keys())
        close_receiver_channel = False

        for cache_key in cache_key_list:
            through_receiver_channel = cls.THROUGH_RECEIVER_CHANNEL_MAPPING[cache_key]

            # noinspection PyBroadException
            try:
                if not through_receiver_channel.receiver_channel.is_open:
                    through_receiver_channel.receiver_channel.open()
                    close_receiver_channel = True
                # end if
                through_receiver_channel.get_device_info(force_refresh_cache=True)
                through_receiver_channel.is_device_connected(force_refresh_cache=True)
            except Exception:
                cls._remove_channel_from_temporary_cache(cache_key=cache_key)
            # end try

            if close_receiver_channel:
                through_receiver_channel.receiver_channel.close()
                close_receiver_channel = False
            # end if
        # end for
    # end def refresh_through_receiver_channel_cache

    @classmethod
    def add_channel_to_cache(cls, channel):
        """
        Add a channel to the cache. For now only ThroughReceiverChannel are accepted. If the channel is already in
        cache, nothing is done. This method cannot be used to replace an existing channel in the cache by another
        channel with the same port index and device index.

        :param channel: Channel to add
        :type channel: ``ThroughReceiverChannel``

        :raise ``AssertionError``: If a channel with the same port index and device index as the one given is already
                                   in cache
        """
        assert isinstance(channel, ThroughReceiverChannel), \
            f"Can only add ThroughReceiverChannel with this method, given {channel}"

        if cls.is_usb_channel_on_hub(channel=channel):
            port_index = channel.get_channel_usb_port_path_list()[-1]
        else:
            port_index = cls.NON_HUB_USB_PORT_INDEX
        # end if

        if (port_index, channel.device_index) in cls.THROUGH_RECEIVER_CHANNEL_MAPPING:
            assert cls.THROUGH_RECEIVER_CHANNEL_MAPPING[(port_index, channel.device_index)] == channel, \
                f"Channel on port index {port_index} and device index {channel.device_index} already cached"
            return
        # end if

        cls.THROUGH_RECEIVER_CHANNEL_MAPPING[(port_index, channel.device_index)] = channel
    # end def add_channel_to_cache

    @classmethod
    def remove_channel_from_cache(cls, port_index, device_index=None):
        """
        Remove a channel from the cache. For now only ThroughReceiverChannel are affected by this method. If no
        channel with the given port index and device index is in cache, nothing is done.

        :param port_index: Port index of the channel to remove
        :type port_index: ``int``
        :param device_index: Device index of the device to remove. If ``None``, all device indexes for the receiver
                             on ``port_index`` are removed - OPTIONAL
        :type device_index: ``int`` or ``None``
        """
        if device_index is None:
            for dev_index in range(1, cls.MAX_NUMBER_OF_DEVICE_IN_RECEIVER + 1):
                if cls.THROUGH_RECEIVER_CHANNEL_MAPPING.get((port_index, dev_index), None) is not None:
                    cls._remove_channel_from_temporary_cache(cache_key=(port_index, dev_index))
                # end if
            # end for
        else:
            if cls.THROUGH_RECEIVER_CHANNEL_MAPPING.get((port_index, device_index), None) is not None:
                cls._remove_channel_from_temporary_cache(cache_key=(port_index, device_index))
            # end if
        # end if
    # end def remove_channel_from_cache

    @classmethod
    def remove_all_channel_through_gotthard_from_cache(cls):
        """
        Remove all channel through a Gotthard receiver from the cache.
        """

        for cache_key in cls.THROUGH_RECEIVER_CHANNEL_MAPPING:
            if isinstance(cls.THROUGH_RECEIVER_CHANNEL_MAPPING[cache_key], ThroughGotthardReceiverChannel):
                cls._remove_channel_from_temporary_cache(cache_key=cache_key)
            # end if
        # end for
    # end def remove_all_channel_through_gotthard_from_cache

    @classmethod
    def _remove_channel_from_temporary_cache(cls, cache_key):
        """
        Internal method to remove a channel from the temporary cache.

        :param cache_key: The key in the cache, its format should be: ``(port_index, device_index)``
        :type cache_key: ``tuple[int, int]``
        """
        channel_to_remove = cls.THROUGH_RECEIVER_CHANNEL_MAPPING.pop(cache_key)
        if channel_to_remove.is_open:
            channel_to_remove.close()
        # end if
        if channel_to_remove.is_subscribed_to_receiver_multi_queue():
            channel_to_remove.unsubscribe_from_receiver_multi_queue()
        # end if
    # end def _remove_channel_from_temporary_cache

    @classmethod
    def _get_cache_based_on_protocol(cls, protocol):
        """
        Get a list of all channel matching a protocol. If unknown protocol, the whole cache is returned.

        :param protocol: Protocol identifier
        :type protocol: ``LogitechProtocol``

        :return: The wanted list of cached channel
        :rtype: ``list[BaseCommunicationChannel]``
        """
        if protocol == LogitechProtocol.USB:
            return list(cls.USB_CHANNEL_MAPPING.values())
        elif protocol == LogitechProtocol.BLE:
            return list(cls.BLE_CHANNEL_MAPPING.values())
        elif protocol > LogitechProtocol.UNKNOWN:
            cache_list = list(cls.THROUGH_RECEIVER_CHANNEL_MAPPING.values())
            return cache_list
        # end if

        return cls.get_all_cached_channels_in_list()
    # end def _get_cache_based_on_protocol

    @classmethod
    def _get_cache_based_on_channel_identifier(cls, channel_id):
        """
        Get a list of all channel matching a channel identifier.

        :param channel_id: Channel identifier
        :type channel_id: ``ChannelIdentifier``

        :return: The wanted list of cached channel
        :rtype: ``list[BaseCommunicationChannel]``
        """
        if channel_id.device_index is not None and channel_id.device_index != Hidpp1Data.DeviceIndex.TRANSCEIVER:
            cache_list_to_use = list(cls.THROUGH_RECEIVER_CHANNEL_MAPPING.values())
        elif channel_id.device_index == Hidpp1Data.DeviceIndex.TRANSCEIVER:
            cache_list_to_use = list(cls.USB_CHANNEL_MAPPING.values())
        elif channel_id.protocol is not None:
            cache_list_to_use = cls._get_cache_based_on_protocol(protocol=channel_id.protocol)
        else:
            cache_list_to_use = cls.get_all_cached_channels_in_list()
        # end if

        return cache_list_to_use
    # end def _get_cache_based_on_channel_identifier
# end class LibusbDriver


smartDeviceFactory = SmartDeviceFactory(LibusbDriver)


class DeviceManagerMock(BaseSmartDevice):
    """
    Define a Device Manager Mock instance.
    """

    def __init__(self, device_number):
        """
        :param device_number: Local device's number (1, 2 or 3)
        :type device_number: ``int``
        """
        super().__init__(device_number)

        self._is_allocated = False
        self._is_power_up = False
    # end def __init__

    def is_allocated(self):
        # See ``pylibrary.system.device.BaseSmartDevice.is_allocated``
        return self._is_allocated
    # end def is_allocated

    def allocate(self):
        # See ``pylibrary.system.device.BaseSmartDevice.allocate``
        self._is_allocated = True
    # end def allocate

    def unallocate(self):
        # See ``pylibrary.system.device.BaseSmartDevice.unallocate``
        self._is_allocated = False
    # end def unallocate

    def powerUp(self):
        # See ``pylibrary.system.device.BaseSmartDevice.powerUp``
        self._is_power_up = True
    # end def powerUp

    def isPoweredUp(self):
        # See ``pylibrary.system.device.BaseSmartDevice.powerUp``
        return self._is_power_up
    # end def isPoweredUp

    def reset(self):
        # See ``pylibrary.system.device.BaseSmartDevice.reset``
        pass
    # end def reset

    def powerDown(self):
        # See ``pylibrary.system.device.BaseSmartDevice.powerDown``
        self._is_power_up = False
    # end def powerDown

    def sendRaw(self, *data):
        # See ``pylibrary.system.device.BaseSmartDevice.sendRaw``
        pass
    # end def sendRaw

    def getElapsedTime(self):
        # See ``pylibrary.system.device.BaseSmartDevice.getElapsedTime``
        return 0
    # end def getElapsedTime
# end class DeviceManagerMock

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
