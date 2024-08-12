#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.bleprotocolutils
:brief:  Helpers for BLE Protocol (applicable to device targets only)
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/07/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import sys
from contextlib import contextmanager
from enum import Enum
from enum import IntEnum
from statistics import mean
from time import perf_counter_ns
from time import sleep

import numpy as np
from math import inf

from pychannel.blechannel import BASE_UUID_TO_ADD
from pychannel.blechannel import BleChannel
from pychannel.logiconstants import BleAdvertisementModelSpecificFields
from pychannel.logiconstants import BleAdvertisingDataConstants
from pychannel.logiconstants import BleAdvertisingInterval
from pychannel.logiconstants import BleAdvertisingSeries
from pychannel.logiconstants import LogitechBleConnectionParameters
from pychannel.logiconstants import LogitechBleConstants
from pyharness.core import TestException
from pyharness.extensions import WarningLevel
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndName
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_endian_list
from pylibrary.tools.threadutils import QueueWithEvents
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.emulatorsmanager import EmulatorsManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytransport.ble.bleadvertisingparser import BleAdvertisingParser
from pytransport.ble.bleconstants import AncsUuids
from pytransport.ble.bleconstants import BleAdvertisingAppearance
from pytransport.ble.bleconstants import BleAdvertisingDataType
from pytransport.ble.bleconstants import BleAdvertisingFlagBitIndex
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.bleconstants import BleChromePNPID
from pytransport.ble.bleconstants import BleContextEventType
from pytransport.ble.bleconstants import BlePnPIdVendorSrc
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleconstants import ManufacturerDataCompanyId
from pytransport.ble.bleconstants import ManufacturerDataName
from pytransport.ble.blecontext import BleContext
from pytransport.ble.blecontext import BleContextDevice
from pytransport.ble.bleinterfaceclasses import BleAdvertisingData
from pytransport.ble.bleinterfaceclasses import BleCharacteristic
from pytransport.ble.bleinterfaceclasses import BleCharacteristicProperties
from pytransport.ble.bleinterfaceclasses import BleDescriptor
from pytransport.ble.bleinterfaceclasses import BleGapAddress
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters
from pytransport.ble.bleinterfaceclasses import BleService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.bleinterfaceclasses import PnPId
from pytransport.ble.blemessage import BleMessage
from pytransport.transportcontext import TransportContextException

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

EXTRA_SCAN_TIME = 2  # in seconds
# margin added to asynchronous scan time to take into account the delay to trigger the advertising.
# based on empiric measurements on the longer one, entering ble pairing mode
SCAN_TRIGGER_TIME = 4 # in seconds
MS_TO_S_DIVIDER = 1e3
SCAN_DURATION_FOR_INTERVAL_CHECKING = 100  # in number of interval
ADVERTISING_PAIRING_SUB_WINDOW_TOLERANCE = 10  # in number of interval
ADVERTISING_PREPAIRING_SUB_WINDOW_TOLERANCE = 100  # in number of interval
ADVERTISING_DURATION_TOLERANCE = 5  # in percent
# The advDelay as defined in specification (Bluetooth Core Spec v5.3 Vol 6 Part B Section 4.4.2.2.1)
ADV_DELAY = 10
# The average advertising interval tolerance is plus or minus 2.88ms
# chosen due to being the standard deviation of advertising delay
AVERAGE_ADVERTISING_INTERVAL_TOLERANCE = 2.88  # in milliseconds
# Minimum number of advertising packet lost
MIN_PACKET_LOST = 1
# Maximum number of undirected advertising packet lost
# This value was decided considering the limitation of the current BLE context solution: pc-ble-driver-py. It is not
# as strong against BLE noise as a sniffer. Therefore, there can be advertising intervals 2 to 10 times more than the
# expected one representing multiple packets that were lost.
MAX_PACKET_LOST_UNDIRECTED_OR_DIRECTED_LDC = 10
# Maximum advertising packet length according to BLE core specification
MAX_ADVERTISING_LENGTH = 31
WRONG_NUMBER_OF_ADVERTISING_INTERVAL_TOLERANCE = 3
# High Duty Cycle timing (Bluetooth Core Spec v5.3 Vol 6 Part B Section 4.4.2.4.3)
MAX_ADVERTISING_DURATION_DIRECTED_HDC = 1.28  # in seconds
# High Duty Cycle timing (Bluetooth Core Spec v5.3 Vol 6 Part B Section 4.4.2.4.3)
MAX_ADVERTISING_INTERVAL_DIRECTED_HDC = 3.75  # in milliseconds
# Low Duty Cycle timing (Bluetooth Core Spec v5.3 Vol 6 Part B Section 4.4.2.2.1)
MIN_ADVERTISING_INTERVAL_DIRECTED_LDC = 20  # in milliseconds
# Maximum number of directed advertising (High Duty Cycle) packet lost
# The next 3 values were decided considering the limitation of the current BLE context solution: pc-ble-driver-py. It
# is not as strong against BLE noise as a sniffer. It also has a scanning window limited to 10s, over that it has
# to restart scanning, which can induce the loss of a lot of package in High Duty Cycle
MAX_PACKET_LOST_DIRECTED_HDC = 100
# Maximum of consecutive packet loss. This means when multiple consecutive advertising intervals showing packet loss.
MAX_CONSECUTIVE_PACKET_LOSS_DIRECTED_HDC = 15
# Maximum of consecutive packet loss. This means when multiple consecutive advertising intervals showing packet loss.
MAX_CONSECUTIVE_PACKET_LOSS_UNDIRECTED_OR_DIRECTED_LDC = 10
# Key size for the encryption, found in the BLE connection security parameters
LOGITECH_ENCRYPTION_KEY_SIZE = 16


# Common values specified by logitech, see:
# https://spaces.logitech.com/x/7gPTBw
ADVERTISING_FLAG_FIELD = (1 << BleAdvertisingFlagBitIndex.LE_LIMITED_DISC_MODE) + \
                         (1 << BleAdvertisingFlagBitIndex.BR_EDR_NOT_SUPPORTED)
DEVICE_TYPE_TO_BLE_APPEARANCE = {  # only three appearance are now allowed Keyboard, Mouse, Generic HID
    DeviceTypeAndName.TYPE.KEYBOARD: BleAdvertisingAppearance.KEYBOARD,
    DeviceTypeAndName.TYPE.MOUSE: BleAdvertisingAppearance.MOUSE,
    DeviceTypeAndName.TYPE.PRESENTER: BleAdvertisingAppearance.GENERIC_HUMAN_INTERFACE_DEVICE,
    DeviceTypeAndName.TYPE.TRACKBALL: BleAdvertisingAppearance.MOUSE,
    DeviceTypeAndName.TYPE.TRACKPAD: BleAdvertisingAppearance.GENERIC_HUMAN_INTERFACE_DEVICE,
    DeviceTypeAndName.TYPE.DIAL: BleAdvertisingAppearance.GENERIC_HUMAN_INTERFACE_DEVICE,
}
LENGTH_OF_SWIFT_PAIR_DATA_IN_ADVERTISING = 7
SWIFT_PAIR_MANUFACTURER_SPECIFIC_DATA = [0x06, 0x00, 0x03, 0x00, 0x80]
LENGTH_OF_SERVICE_DATA_IN_SCAN_RESPONSE = 12

FIRST_TIMESTAMP_SUB_WINDOW_INDEX = 0
LAST_TIMESTAMP_SUB_WINDOW_INDEX = 1


class OsXModelName(Enum):
    """
    Some model names were documented in the following patchset:
    https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/8806/4/lble/lble_os_detection.c#57
    """
    EMAC = "eMac"
    IBOOK = "iBook"
    IMAC = "iMac"
    MAC_MINI = "Mac mini"
    MAC_PRO = "Mac Pro"
    MAC_SERVER = "Mac Server"
    MAC_BOOK = "MacBook"
    POWER_MAC = "Power Mac"
    POWER_BOOK = "PowerBook"
    X_SERVE = "Xserve"
    MAC_STUDIO = "Mac13,1"
    MAC_BOOK_PRO_2022 = "MacBookPro18,4"
    MAC_BOOK_AIR_2022 = "MacBookAir5,2"
    MAC_BOOK_2022 = "MacBook9,1"
    MAC_PRO_2022 = "MacPro5,1"
    MAC_MINI_2022 = "Macmini6,2"
# end class OsXModelName


class IosModelName(Enum):
    IPHONE = "iPhone"
    IPAD = "iPad"
# end class IosModelName


class BleProPid(IntEnum):
    RANGE_START = 0xB600
    RANGE_END = 0xB61F
# end class BleProPid


class AppServiceDataSubFieldLength(IntEnum):
    """
    Length of the subfields in the Service data field in the scan response for application or bootloader
    reconnection.

    Source: https://spaces.logitech.com/x/7gPTBw
    """
    UUID = 2
    BLE_PRO_SERVICE_PROTOCOL_TYPE = 1
    BLE_PRO_SERVICE_VERSION = 1
    DEVICE_STATE = 1
    DEVICE_BLUETOOTH_PID = 2
    AUTHENTICATION_TYPE = 1
    DEVICE_TYPE_RFU = 1
    PRODUCT_SPECIFIC_DATA = 1
# end class AppServiceDataSubFieldLength


class AppServiceDataSubFieldIndex(IntEnum):
    """
    Index of the subfields in the Service data field in the scan response for application or bootloader
    reconnection.

    Source: https://spaces.logitech.com/x/7gPTBw
    """
    UUID = 0
    BLE_PRO_SERVICE_PROTOCOL_TYPE = UUID + AppServiceDataSubFieldLength.UUID
    BLE_PRO_SERVICE_VERSION = BLE_PRO_SERVICE_PROTOCOL_TYPE + AppServiceDataSubFieldLength.BLE_PRO_SERVICE_PROTOCOL_TYPE
    DEVICE_STATE = BLE_PRO_SERVICE_VERSION + AppServiceDataSubFieldLength.BLE_PRO_SERVICE_VERSION
    DEVICE_BLUETOOTH_PID = DEVICE_STATE + AppServiceDataSubFieldLength.DEVICE_STATE
    AUTHENTICATION_TYPE = DEVICE_BLUETOOTH_PID + AppServiceDataSubFieldLength.DEVICE_BLUETOOTH_PID
    DEVICE_TYPE_RFU = AUTHENTICATION_TYPE + AppServiceDataSubFieldLength.AUTHENTICATION_TYPE
    PRODUCT_SPECIFIC_DATA = DEVICE_TYPE_RFU + AppServiceDataSubFieldLength.DEVICE_TYPE_RFU
# end class AppServiceDataSubFieldIndex


class AppServiceDataSubFieldDefault(IntEnum):
    """
    Default values of the subfields in the Service data field in the scan response for application or bootloader
    reconnection.

    Source: https://spaces.logitech.com/x/7gPTBw
    """
    UUID = BleUuidStandardService.LOGITECH_BLE_PRO
    BLE_PRO_SERVICE_PROTOCOL_TYPE = 0x10
    DEVICE_STATE = NonVolatilePairingInformation.DeviceState.APPLICATION_BOOTLOADER_RECONNECTION
# end class AppServiceDataSubFieldDefault


class ReportReferences:
    """
    Report references
    source: https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/view#heading=h.apf33or5gxto
    """
    MOUSE_INPUT = HexList("0201")
    MOUSE_16BITS_INPUT = HexList("1501")
    LED_OUTPUT = HexList("0102")
    KEYBOARD_INPUT = HexList("0101")
    GAMING_LED_OUTPUT = HexList("1802")
    GAMING_KEYBOARD_INPUT = HexList("1801")
    GENERIC_CONSUMER_INPUT = HexList("0301")
    GENERIC_DESKTOP_SYSTEM_CONTROL = HexList("0401")
    PRODUCT_SPECIFIC_CONSUMER_INPUT = HexList("0501")
    DESKTOP_CALL_STATE_MANAGEMENT = HexList("1101")
    TOP_ROW_FEATURE = HexList("0903")
    HIDPP_INPUT = HexList("1101")
    HIDPP_OUTPUT = HexList("1102")
# end class ReportReferences

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleProtocolTestUtils(DeviceBaseTestUtils):
    """
    Test utils for BLE Protocol (applicable to device targets only)
    """
    MAX_TRIES = 4

    @classmethod
    @contextmanager
    def manage_verbosity_ble_context(cls, test_case, trace_level):
        """
        Change the trace level of the BLE context for a given section. If the level is the same as the current one,
        nothing is done.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param trace_level: The wanted trace level requested for the BLE context
        :type trace_level: ``TraceLevel``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        current_trace_level = TRACE_LOGGER.get_trace_level(subscription_owner=ble_context)
        assert current_trace_level is not None, "The BLE context is not subscribed to the trace logger"

        if current_trace_level == trace_level:
            yield
            return
        # end if

        TRACE_LOGGER.update_trace_level(subscription_owner=ble_context, trace_level=trace_level)
        try:
            yield
        finally:
            TRACE_LOGGER.update_trace_level(subscription_owner=ble_context, trace_level=current_trace_level)
        # end try
    # end def manage_verbosity_ble_context

    @classmethod
    def get_ble_context(cls, test_case):
        """
        Get the BLE context

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The BLE context or ``None`` if it is not present and the sanity check is not requested
        :rtype: ``BleContext`` or ``None``

        :raise ``AssertionError``: if the sanity check fails or if it still failed to open after multiple tries
        """
        assert test_case.device.BLE_CONTEXT is not None, "Test case should have a BLE context to use this method"

        retry_count = 0
        while not test_case.device.BLE_CONTEXT.is_open and retry_count < cls.MAX_TRIES:
            try:
                test_case.device.BLE_CONTEXT.open()
            except TransportContextException as e:
                if e.get_cause() != TransportContextException.Cause.CONTEXT_DOOMED_ERROR or \
                        EmulatorsManager.is_jlink_io_switch_present(features=test_case.f) or \
                        test_case.device_debugger is None:
                    raise
                # end if

                retry_count += 1

                if retry_count < cls.MAX_TRIES:
                    # TODO: remove the ``force_console_print=True``. We keep it for now to be able to quickly know if
                    #  this happens a lot
                    test_case.log_traceback_as_warning(
                        supplementary_message="BLE context is doomed, force update of the hardware and retry",
                        warning_level=WarningLevel.ROBUSTNESS,
                        force_console_print=True)

                    if retry_count == 1:
                        # For the first retry, just a simple reset is tried
                        test_case.reset_ble_context_hardware()
                    else:
                        test_case.update_ble_context_hardware(force=True)
                    # end if
                # end if
            # end try
        # end while

        assert retry_count < cls.MAX_TRIES, f"Opening BLE context still failed after {cls.MAX_TRIES} try(ies)"

        return test_case.device.BLE_CONTEXT
    # end def get_ble_context

    @classmethod
    def get_ble_context_central_address(cls, test_case):
        """
        Get central address of the BLE context.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The central address
        :rtype: ``BleGapAddress``
        """
        return cls.get_ble_context(test_case=test_case).get_central_address()
    # end def get_ble_context_central_address

    @classmethod
    def get_current_device_ble_gap_address(cls, test_case):
        """
        Get the DUT BLE GAP address.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The DUT BLE GAP address
        :rtype: ``BleGapAddress``
        """
        address_current_device = cls.NvsHelper.get_last_gap_address(
            test_case=test_case, memory_manager=test_case.memory_manager)
        # The address found is in little endian while our interface asks for big endian
        address_current_device.reverse()
        # To get the next address to advertise, it should be incremented
        address_current_device = address_current_device[:1] + HexList('00' * (len(address_current_device) - 1)) if \
            address_current_device[1:] == HexList('FF' * (len(address_current_device) - 1)) else \
            address_current_device[:1] + HexList(
                Numeral(address_current_device[1:], len(address_current_device) - 1) + 1)
        return BleGapAddress(address_type=LogitechBleConstants.ADDRESS_TYPE, address=str(address_current_device))
    # end def get_current_device_ble_gap_address

    @classmethod
    def increment_address(cls, test_case, address=None):
        """
        Increment a ble address by 1

        example of use :
        When device advertise in prepairing and undirected pairing, the address of the regular pairing mode undirected
        advertising is done by incrementing the current address by one because the current one is
        used for the prepairing advertising

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param address: Address to increment, otherwise use the current device ble address if None
        :type address: ``BleGapAddress`` or ``None``
        :return: the incremented address
        :rtype: ``BleGapAddress``
        """
        if address is None:
            address = cls.get_current_device_ble_gap_address(test_case=test_case)
        # end if
        incremented_address = HexList(address.address)

        # increment address with byte overflow, case of full FF is not a valid ble address so not an issue
        for index in range(-1, -len(incremented_address), -1):
            if incremented_address[index] != 0xFF:
                incremented_address[index] += 1
                break
            else:
                incremented_address[index] = 0
            # end if
        # end for
        address.address = str(incremented_address)
        return address
    # end def increment_address

    @classmethod
    def read_characteristics(cls, test_case, ble_context_device, service_uuid, characteristic_uuid):
        """
        Read characteristics matching a given UUID in a given service. Note that multiple characteristics can match a
        same UUID, even within a single service, so a list of characteristics is read.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_context_device: Context device to read from
        :type ble_context_device: ``BleContextDevice``
        :param service_uuid: UUID of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: UUID of the characteristic to read
        :type characteristic_uuid: ``BleUuid``

        :return: List of characteristics' data
        :rtype: ``list[BleMessage]``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        service = ble_context.get_service(ble_context_device=ble_context_device, uuid=service_uuid)
        characteristics = service.get_characteristics(characteristic_uuid=characteristic_uuid)
        read_characteristics = []
        for characteristic in characteristics:
            read_characteristics.append(ble_context.attribute_read(ble_context_device=ble_context_device,
                                                                   attribute=characteristic))
        # end for
        return read_characteristics
    # end def read_characteristics

    @classmethod
    def write_characteristic(cls, test_case, ble_context_device, service_uuid, characteristic_uuid, value):
        """
        Write characteristic matching a given UUID in a given service and convert the values to string.
        Note that even if multiple characteristics can match same UUID, whatever the service, this function asserts that
        only one exists.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_context_device: Context device to read from
        :type ble_context_device: ``BleContextDevice``
        :param service_uuid: UUID of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: UUID of the characteristic to write to
        :type characteristic_uuid: ``BleUuid``
        :param value: The value to write to the characteristic
        :type value: ``HexList`` or ``BleMessage``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        message = value if isinstance(value, BleMessage) else BleMessage(message_class=HexList, data=value,
                                                                         timestamp=perf_counter_ns())
        service = ble_context.get_service(ble_context_device=ble_context_device, uuid=service_uuid)
        characteristics = service.get_characteristics(characteristic_uuid=characteristic_uuid)

        test_case.assertEqual(expected=1,
                              obtained=len(characteristics),
                              msg=f"Only one instance of {characteristic_uuid} should exist in {service_uuid}")

        ble_context.characteristic_write(ble_context_device=ble_context_device,
                                         characteristic=characteristics[0],
                                         data=message)
    # end def write_characteristic

    @classmethod
    def write_wo_resp_characteristic(cls, test_case, ble_context_device, service_uuid, characteristic_uuid, value):
        """
        Write without response characteristic matching a given UUID in a given service and convert the values to string.
        Note that even if multiple characteristics can match same UUID, whatever the service, this function asserts that
        only one exists.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_context_device: Context device to read from
        :type ble_context_device: ``BleContextDevice``
        :param service_uuid: UUID of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: UUID of the characteristic to write to
        :type characteristic_uuid: ``BleUuid``
        :param value: The value to write to the characteristic
        :type value: ``HexList`` or ``BleMessage``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        message = value if isinstance(value, BleMessage) else BleMessage(message_class=HexList, data=value,
                                                                         timestamp=perf_counter_ns())
        service = ble_context.get_service(ble_context_device=ble_context_device, uuid=service_uuid)
        characteristics = service.get_characteristics(characteristic_uuid=characteristic_uuid)

        test_case.assertEqual(expected=1,
                              obtained=len(characteristics),
                              msg=f"Only one instance of {characteristic_uuid} should exist in {service_uuid}")

        ble_context.characteristic_write_without_response(ble_context_device=ble_context_device,
                                                          characteristic=characteristics[0],
                                                          data=message)
    # end def write_wo_resp_characteristic

    @classmethod
    def read_characteristics_as_string(cls, test_case, ble_context_device, service_uuid, characteristic_uuid):
        """
        Read characteristics matching a given UUID in a given service and convert the values to string.
        Note that the conversion can produce gibberish if used on the wrong characteristics, and looses timestamp
        information
        Note that multiple characteristics can match same UUID, even within a single service,
        so a list of characteristics is read.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_context_device: Context device to read from
        :type ble_context_device: ``BleContextDevice``
        :param service_uuid: UUID of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: UUID of the characteristic to read
        :type characteristic_uuid: ``BleUuid``

        :return: List of characteristics' texts
        :rtype: ``list[str]``
        """
        data = cls.read_characteristics(test_case, ble_context_device, service_uuid, characteristic_uuid)
        texts = []
        for characteristic in data:
            text = characteristic.data.toString()
            texts.append(text)
        # end for
        return texts
    # end def read_characteristics_as_string

    @classmethod
    def read_descriptor(cls, test_case, ble_context_device, characteristic, descriptor_uuid):
        """
        Read a descroptor of a characteristic filtered by the descriptor UUID

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_context_device: Context device to read from
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: The characteristic to check the descriptor
        :type characteristic: ``BleCharacteristic``
        :param descriptor_uuid: The UUID of the descriptor to read
        :type descriptor_uuid: ``BleUuid``

        :return: The data of the descriptor
        :rtype: ``BleMessage``
        """
        ble_context = cls.get_ble_context(test_case)
        descriptor = \
            [descriptor for descriptor in characteristic.descriptors if
             descriptor.uuid == descriptor_uuid][0]
        return ble_context.attribute_read(ble_context_device=ble_context_device, attribute=descriptor)

    # end def read_descriptor

    @classmethod
    def scan_for_logitech_devices(cls, test_case, scan_time, send_scan_request):
        """
        Scan for logitech devices that has the logitech BLE Pro UUID in the advertising packet and the wanted device
        name found in settings.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param scan_time: The scan time in seconds
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag to indicate that a scan response is requested for each advertising
                                           packet
        :type send_scan_request: ``bool``

        :return: The list of found logitech devices
        :rtype: ``list[BleContextDevice]``
        """
        ble_devices = cls.get_ble_context(test_case=test_case).scan(
            scan_time=scan_time, send_scan_request=send_scan_request)

        logitech_ble_devices = []
        for ble_device in ble_devices:
            adv_data = ble_device.advertising_data
            if ble_device.advertising_type == BleAdvertisingPduType.CONNECTABLE_UNDIRECTED and \
                    cls.is_logitech_ble_uuid_in_record(advertising_data=adv_data[0]) and \
                    cls.is_short_name_in_settings_name(test_case=test_case, advertising_data=adv_data[0]):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Found Logitech device: {ble_device.advertising_data}")
                # ------------------------------------------------------------------------------------------------------
                logitech_ble_devices.append(ble_device)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Found device: {ble_device.advertising_data}")
                # ------------------------------------------------------------------------------------------------------
            # end if
        # end for

        return logitech_ble_devices
    # end def scan_for_logitech_devices

    @classmethod
    def scan_for_current_device(cls, test_case, scan_timeout, send_scan_request, force_scan_for_all_timeout=False):
        """
        Scan for the current DUT.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param scan_timeout: The scan timeout in seconds
        :type scan_timeout: ``int`` or ``float``
        :param send_scan_request: Flag to indicate that a scan response is requested for each advertising
                                           packet
        :type send_scan_request: ``bool``
        :param force_scan_for_all_timeout: Flag to indicate to scan for the whole timeout, even if the device is found
                                           before the end
        :type force_scan_for_all_timeout: ``bool``

        :return: The current device
        :rtype: ``BleContextDevice``
        """
        try:
            address_current_device = cls.get_current_device_ble_gap_address(test_case=test_case)
        except TestException:
            DeviceBaseTestUtils.NvsHelper.force_last_gap_address(test_case=test_case)
            address_current_device = cls.get_current_device_ble_gap_address(test_case=test_case)
        # end try
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, f'Current device address: {address_current_device}')
        # --------------------------------------------------------------------------------------------------------------

        return cls.scan_for_devices(
            test_case=test_case, ble_addresses=[address_current_device], scan_timeout=scan_timeout,
            send_scan_request=send_scan_request, force_scan_for_all_timeout=force_scan_for_all_timeout)[0]
    # end def scan_for_current_device

    @classmethod
    def scan_for_devices(cls, test_case, ble_addresses, scan_timeout, send_scan_request,
                         force_scan_for_all_timeout=False):
        """
        Scan for one or multiple devices based on their address.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_addresses: The list of bluetooth addresses to consider
        :type ble_addresses: ``list[BleGapAddress]``
        :param scan_timeout: The scan timeout in seconds
        :type scan_timeout: ``int`` or ``float``
        :param send_scan_request: Flag to indicate that a scan response is requested for each advertising packet
        :type send_scan_request: ``bool``
        :param force_scan_for_all_timeout: Flag to indicate to scan for the whole timeout, even if the device is found
                                           before the end
        :type force_scan_for_all_timeout: ``bool``

        :return: The list of found devices
        :rtype: ``list[BleContextDevice]``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        if force_scan_for_all_timeout:
            devices = ble_context.scan_for_devices(
                ble_addresses=ble_addresses,
                scan_time=scan_timeout,
                send_scan_request=send_scan_request)

            if len(devices) == 0:
                raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_FOUND,
                                                f"Could not find the device with param: {ble_addresses}")
            # end if
            return devices
        else:
            return [ble_context.scan_for_first_device_found(
                ble_addresses=ble_addresses,
                scan_timeout=scan_timeout,
                send_scan_request=send_scan_request)]
        # end if
    # end def scan_for_devices

    @classmethod
    def start_scan_for_devices(cls, test_case, ble_addresses, scan_timeout, send_scan_request,
                               force_scan_for_all_timeout=False):
        """
        Start asynchronous scan for one or multiple devices based on their address.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_addresses: The list of bluetooth addresses to consider
        :type ble_addresses: ``list[BleGapAddress]``
        :param scan_timeout: The scan timeout in seconds
        :type scan_timeout: ``int`` or ``float``
        :param send_scan_request: Flag to indicate that a scan response is requested for each advertising packet
        :type send_scan_request: ``bool``
        :param force_scan_for_all_timeout: Flag to indicate to scan for the whole timeout, even if the device is found
                                           before the end
        :type force_scan_for_all_timeout: ``bool``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        if force_scan_for_all_timeout:
            ble_context.start_scan_for_device(
                ble_addresses=ble_addresses,
                scan_time=scan_timeout,
                send_scan_request=send_scan_request)
        else:
            ble_context.start_scan_for_first_device_found(
                ble_addresses=ble_addresses,
                scan_timeout=scan_timeout,
                send_scan_request=send_scan_request)
        # end if
    # end def start_scan_for_devices

    @classmethod
    def get_scanning_result(cls, test_case, timeout):
        """
        Read the result of asynchronous scanning started earlier. It will block until they are ready

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param timeout: Timeout to get the response in seconds
        :type timeout: ``float``

        :return: The list of found devices
        :rtype: ``list[BleContextDevice]``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        try:
            return ble_context.get_scanning_result(timeout)
        except TransportContextException as e:
            test_case.fail(f"Transport context exception on getting scan results:\n {e.get_cause().name}")
        # end try
    # end def get_scanning_result

    @classmethod
    def scan_for_current_device_with_entering_pairing_mode_during_scan(cls, test_case, scan_timeout, send_scan_request,
                                                                       force_scan_for_all_timeout=False):
        """
        Scan for the current DUT, that will be asked to start advertising after the scanning starts to ensure
        reading the first packet

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param scan_timeout: The scan timeout in seconds
        :type scan_timeout: ``int`` or ``float``
        :param send_scan_request: Flag to indicate that a scan response is requested for each advertising
                                           packet
        :type send_scan_request: ``bool``
        :param force_scan_for_all_timeout: Flag to indicate to scan for the whole timeout, even if the device is found
                                           before the end - OPTIONAL
        :type force_scan_for_all_timeout: ``bool``

        :return: The current device
        :rtype: ``BleContextDevice``
        """
        try:
            address_current_device = cls.get_current_device_ble_gap_address(test_case=test_case)
        except TestException:
            DeviceBaseTestUtils.NvsHelper.force_last_gap_address(test_case=test_case)
            address_current_device = cls.get_current_device_ble_gap_address(test_case=test_case)
        # end try
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, f'Current device address: {address_current_device}')
        # --------------------------------------------------------------------------------------------------------------

        return cls.scan_for_devices_with_entering_pairing_mode_during_scan(test_case, [address_current_device],
                                                                           scan_timeout, send_scan_request,
                                                                           force_scan_for_all_timeout)[0]
    # end def scan_for_current_device_with_entering_pairing_mode_during_scan

    @classmethod
    def scan_for_devices_with_entering_pairing_mode_during_scan(cls, test_case, ble_addresses, scan_timeout,
                                                                send_scan_request, force_scan_for_all_timeout=False):
        """
        Scan for the a list of device, the DUT will be asked to start advertising after the scanning starts to ensure
        reading the first packet

        :param ble_addresses: The list of bluetooth addresses to consider
        :type ble_addresses: ``list[BleGapAddress]``
        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param scan_timeout: The scan timeout in seconds
        :type scan_timeout: ``int`` or ``float``
        :param send_scan_request: Flag to indicate that a scan response is requested for each advertising
                                           packet
        :type send_scan_request: ``bool``
        :param force_scan_for_all_timeout: Flag to indicate to scan for the whole timeout, even if the device is found
                                           before the end - Optional
        :type force_scan_for_all_timeout: ``bool``

        :return: The scanned device
        :rtype: ``list[BleContextDevice]``
        """
        cls.start_scan_for_devices(
            test_case=test_case, ble_addresses=ble_addresses,
            scan_timeout=scan_timeout + SCAN_TRIGGER_TIME,
            send_scan_request=send_scan_request, force_scan_for_all_timeout=force_scan_for_all_timeout)
        cls.enter_pairing_mode_ble(test_case)
        return cls.get_scanning_result(test_case, scan_timeout + SCAN_TRIGGER_TIME)
    # end def scan_for_devices_with_entering_pairing_mode_during_scan

    @staticmethod
    def get_pairing_sub_window_duration_acceptance_range(test_case):
        """
        Get the acceptance range in nanoseconds of the regular pairing advertising duration when unused
        prepairing data is present.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``

        :return: Accepted range as a tuple of min and max values in nanoseconds
        :rtype: ``list[int]``
        """
        accepted_regular_sub_window_ns_min = \
            test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_UnusedPrepairingInfoRegularAdvertisingSubWindowS * \
            TIMESTAMP_UNIT_DIVIDER_MAP['s'] - \
            (ADVERTISING_PAIRING_SUB_WINDOW_TOLERANCE *
             max(test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_FirstAdvertisingIntervalMs,
                 test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_SecondAdvertisingIntervalMs)) * \
            TIMESTAMP_UNIT_DIVIDER_MAP['ms']
        accepted_regular_sub_window_ns_max = \
            test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_UnusedPrepairingInfoRegularAdvertisingSubWindowS * \
            TIMESTAMP_UNIT_DIVIDER_MAP['s'] + \
            (ADVERTISING_PAIRING_SUB_WINDOW_TOLERANCE *
             max(test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_FirstAdvertisingIntervalMs,
                 test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_SecondAdvertisingIntervalMs)) * \
            TIMESTAMP_UNIT_DIVIDER_MAP['ms']
        return accepted_regular_sub_window_ns_min, accepted_regular_sub_window_ns_max
    # end def get_pairing_sub_window_duration_acceptance_range

    @staticmethod
    def get_prepairing_sub_window_duration_acceptance_range(test_case):
        """
        Get the acceptance range in nanoseconds of the prepairing advertising duration when unused
        prepairing data is present.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``

        :return: Accepted range as a tuple of min and max values in nanoseconds
        :rtype: ``list[int]``
        """
        accepted_prepairing_sub_window_ns_min = \
            test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_UnusedPrepairingInfoPrepairingAdvertisingSubWindowS * \
            TIMESTAMP_UNIT_DIVIDER_MAP['s'] - \
            ADVERTISING_PREPAIRING_SUB_WINDOW_TOLERANCE * \
            MAX_ADVERTISING_INTERVAL_DIRECTED_HDC * TIMESTAMP_UNIT_DIVIDER_MAP['ms']
        accepted_prepairing_sub_window_ns_max = \
            test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_UnusedPrepairingInfoPrepairingAdvertisingSubWindowS * \
            TIMESTAMP_UNIT_DIVIDER_MAP['s'] + \
            ADVERTISING_PREPAIRING_SUB_WINDOW_TOLERANCE * \
            MAX_ADVERTISING_INTERVAL_DIRECTED_HDC * TIMESTAMP_UNIT_DIVIDER_MAP['ms']
        return accepted_prepairing_sub_window_ns_min, accepted_prepairing_sub_window_ns_max
    # end def get_prepairing_sub_window_duration_acceptance_range

    @classmethod
    def get_sub_windows_timestamps(cls, test_case, timestamps, is_prepairing):
        """
        Get the first and last timestamp of each sub window (prepairing or pairing).

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param timestamps: List of timestamps in nanoseconds to use
        :type timestamps: ``list[int]``
        :param is_prepairing: Flag indicating for prepairing sub windows (``True``) or for regular pairing (``False``)
        :type is_prepairing: ``bool``

        :return: The list of couple of first and last timestamp of each sub window
        :rtype: ``list[tuple[int]]``
        """
        if is_prepairing:
            accepted_other_sub_window_ns_min, accepted_other_sub_window_ns_max = \
                cls.get_pairing_sub_window_duration_acceptance_range(test_case=test_case)
        else:
            accepted_other_sub_window_ns_min, accepted_other_sub_window_ns_max = \
                cls.get_prepairing_sub_window_duration_acceptance_range(test_case=test_case)
        # end if

        sub_windows_timestamps = []
        first_sub_window_timestamp = timestamps[0]
        for i in range(len(timestamps) - 1):
            interval = timestamps[i + 1] - timestamps[i]
            if accepted_other_sub_window_ns_min <= interval <= accepted_other_sub_window_ns_max:
                sub_windows_timestamps.append((first_sub_window_timestamp, timestamps[i]))
                first_sub_window_timestamp = timestamps[i + 1]
            # end if
        # end for

        # If first_sub_window_timestamp is neither the last sub window first timestamp nor the last timestamp in the
        # complete list, then the last sub window should be added
        if first_sub_window_timestamp not in [sub_windows_timestamps[-1][0], timestamps[-1]]:
            sub_windows_timestamps.append((first_sub_window_timestamp, timestamps[-1]))
        # end if

        return sub_windows_timestamps
    # end def get_sub_windows_timestamps

    @classmethod
    def check_advertising_interval_undirected_or_directed_ldc(cls, test_case, filtered_values, wrong_interval,
                                                              expected_interval_ms, check_all=False):
        """
        Check the advertising interval from all the timestamps measured from the scan for an undirected advertising.
        Either checks that all values are within the accepted range or if the average is the middle value of
        the tolerance range.

        This method is for undirected advertising and directed advertising in Low Duty Cycle (LDC).

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param filtered_values: list of filtered interval values
        :type filtered_values: ``list[int]``
        :param wrong_interval: list of the subset of filtered values outside the accepted range
        :type wrong_interval: ``list[int]``
        :param expected_interval_ms: The expected theoretical interval value
        :type expected_interval_ms: ``int``
        :param check_all: Flag indicating to check all interval value and not just the average - OPTIONAL
        :type check_all: ``bool``

        :raise ``AssertionError``: If more than half the values were filtered
        """

        if check_all:
            test_case.assertAlmostEqual(first=len(wrong_interval),
                                        second=0,
                                        delta=WRONG_NUMBER_OF_ADVERTISING_INTERVAL_TOLERANCE,
                                        msg=f"Wrong advertising intervals: {wrong_interval}")
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, "Check that the average is the value in the middle of the accepted error range "
                           f"for an expected interval of {expected_interval_ms}")
            # ----------------------------------------------------------------------------------------------------------
            average_interval = round(mean(filtered_values) / TIMESTAMP_UNIT_DIVIDER_MAP['ms'])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Average interval in ms: {average_interval}")
            # ----------------------------------------------------------------------------------------------------------
            test_case.assertAlmostEqual(first=average_interval,
                                        second=expected_interval_ms + int(ADV_DELAY // 2),
                                        delta=AVERAGE_ADVERTISING_INTERVAL_TOLERANCE,
                                        msg=f"Wrong advertising interval: {average_interval}")
        # end if
    # end def check_advertising_interval_undirected_or_directed_ldc

    @classmethod
    def filter_ldc_advertising(cls, test_case, intervals, expected_interval_ms):
        """
        Apply a filter to the intervals from a batch of advertising removing interval values representing missed packets

        This method is for undirected advertising and directed advertising in Low Duty Cycle (LDC).

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param intervals: list of intervals to filter
        :type intervals: ``list``
        :param expected_interval_ms: expected interval in milliseconds
        :type expected_interval_ms: ``int``

        :return: list of filtered intervals and list of intervals outside the expected range in the filtered value
        :rtype: ``tuple[list[int], list[int]]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            test_case,
            "Advertising measured interval in ms: "
            f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in intervals]}")
        LogHelper.log_info(test_case,
                           "Filter out the value that represent a packet lost, aka the values that is a multiple of "
                           "the expected one (in the valid error range)")
        # --------------------------------------------------------------------------------------------------------------
        expected_interval_ns = expected_interval_ms * TIMESTAMP_UNIT_DIVIDER_MAP['ms']
        filtered_values = []
        filtered_out_values = []
        consecutive_packet_loss = []
        # Remove all values representing loss of packets
        for interval in intervals:
            is_packet_loss = False
            for i in range(1 + MIN_PACKET_LOST, 1 + MAX_PACKET_LOST_UNDIRECTED_OR_DIRECTED_LDC):
                min_interval, max_interval = cls._get_interval_range_for_missed_packets(
                    expected_interval_ns=expected_interval_ns, number_of_missed_packets=i)
                if min_interval <= interval <= max_interval:
                    is_packet_loss = True
                    break
                # end if
            # end for

            if is_packet_loss:
                consecutive_packet_loss.append(interval)

                if len(consecutive_packet_loss) > MAX_CONSECUTIVE_PACKET_LOSS_UNDIRECTED_OR_DIRECTED_LDC:
                    # If there is more consecutive values that could represent packet loss, then in this filter we
                    # consider them not as packet loss but as possible wrong values that should not be filtered out.
                    filtered_values.extend(consecutive_packet_loss)
                    consecutive_packet_loss.clear()
                # end if
            else:
                filtered_values.append(interval)
                if len(consecutive_packet_loss) > 0:
                    # Filter out the values that were representing packet loss
                    filtered_out_values.extend(consecutive_packet_loss)
                    consecutive_packet_loss.clear()
                # end if
            # end if
        # end for
        if len(consecutive_packet_loss) > 0:
            # Filter out the last values that were representing packet loss
            filtered_out_values.extend(consecutive_packet_loss)
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Values filtered out (in ms): "
                                      f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in filtered_out_values]}")
        LogHelper.log_info(
            test_case,
            "Filtered advertising measured interval in ms: "
            f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in filtered_values]}")
        LogHelper.log_info(test_case, "Make some stats to log")
        # --------------------------------------------------------------------------------------------------------------
        wrong_interval = []
        for interval in filtered_values:
            interval_ms = interval / TIMESTAMP_UNIT_DIVIDER_MAP['ms']
            if not (expected_interval_ms - 1 < interval_ms < expected_interval_ms + ADV_DELAY + 1):
                wrong_interval.append(interval)
            # end if
        # end for
        if len(filtered_values) > 0:
            error_percentage = 100 * len(wrong_interval) / len(filtered_values)
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, f"Intervals out of the accepted range ({error_percentage:.2f}%): "
                           f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in wrong_interval]}")
            # --------------------------------------------------------------------------------------------------------------
        else:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "All intervals filtered out, no statistics can be established")
            # --------------------------------------------------------------------------------------------------------------
        # end if
        if len(wrong_interval) > 0 and intervals[0] == wrong_interval[0]:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "First value out of accepted range. Specification "
                                          "is less strict on this specific interval.\n"
                                          "Removed first value from list")
            # ------------------------------------------------------------------------------------------------------
            filtered_values.pop(0)
            wrong_interval.pop(0)
        # end if
        return filtered_values, wrong_interval
    # end def filter_ldc_advertising

    @classmethod
    def check_advertising_interval_directed_hdc(cls, test_case, filtered_values, wrong_interval, check_all=False):
        """
        Check the advertising interval from all the timestamps measured from the scan for an undirected advertising.
        Either checks that all values are within the accepted range or if the average is the middle value of
        the tolerance range.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param filtered_values: list of filtered interval values
        :type filtered_values: ``list[int]``
        :param wrong_interval: list of the subset of filtered values outside the accepted range
        :type wrong_interval: ``list[int]``
        :param check_all: Flag indicating to check all interval value and not just the average - OPTIONAL
        :type check_all: ``bool``
        """
        if check_all:
            test_case.assertAlmostEqual(first=len(wrong_interval),
                                        second=0,
                                        delta=WRONG_NUMBER_OF_ADVERTISING_INTERVAL_TOLERANCE,
                                        msg=f"Wrong advertising intervals: {wrong_interval}")
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, "Check that the average is the value in the middle of the accepted error range "
                           "for High duty cycle")
            # ----------------------------------------------------------------------------------------------------------
            average_interval = mean(filtered_values) / TIMESTAMP_UNIT_DIVIDER_MAP['ms']
            test_case.assertLessEqual(
                a=average_interval,
                b=MAX_ADVERTISING_INTERVAL_DIRECTED_HDC,
                msg="The high cycle timeing for advertising should be less or equal "
                    f"to {MAX_ADVERTISING_INTERVAL_DIRECTED_HDC}ms")
        # end if
    # end def check_advertising_interval_directed_hdc

    @classmethod
    def filter_hdc_intervals(cls, test_case, intervals):
        """
        Apply a filter to the intervals from a batch of advertising removing interval values representing missed packets

        This method is for undirected advertising and directed advertising in High Duty Cycle (HDC).


        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param intervals: list of intervals to filter
        :type intervals: ``list``

        :return: list of filtered intervals and list of intervals outside the expected range in the filtered value
        :rtype: ``tuple[list[int], list[int]]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            test_case,
            "Advertising measured interval in ms: "
            f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in intervals]}")
        # --------------------------------------------------------------------------------------------------------------

        max_advertising_interval_ns = MAX_ADVERTISING_INTERVAL_DIRECTED_HDC * TIMESTAMP_UNIT_DIVIDER_MAP['ms']

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Filter out the potential missed packet values")
        # --------------------------------------------------------------------------------------------------------------
        new_filtered_values = []
        filtered_out_values = []
        consecutive_packet_loss = []
        # Remove all values representing loss of packets
        for interval in intervals:
            if max_advertising_interval_ns * MIN_PACKET_LOST <= interval <= \
                    max_advertising_interval_ns * MAX_PACKET_LOST_DIRECTED_HDC:
                # This represents packet loss
                consecutive_packet_loss.append(interval)

                if len(consecutive_packet_loss) > MAX_CONSECUTIVE_PACKET_LOSS_DIRECTED_HDC:
                    # If there is more consecutive values that could represent packet loss, then in this filter we
                    # consider them not as packet loss but as possible wrong values that should not be filtered out.
                    new_filtered_values.extend(consecutive_packet_loss)
                    consecutive_packet_loss.clear()
                # end if
            else:
                new_filtered_values.append(interval)
                if len(consecutive_packet_loss) > 0:
                    # Filter out the values that were representing packet loss
                    filtered_out_values.extend(consecutive_packet_loss)
                    consecutive_packet_loss.clear()
                # end if
            # end if
        # end for
        if len(consecutive_packet_loss) > 0:
            # Filter out the last values that were representing packet loss
            filtered_out_values.extend(consecutive_packet_loss)
        # end if
        filtered_values = new_filtered_values
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Values filtered out (in ms): "
                                      f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in filtered_out_values]}")
        LogHelper.log_info(
            test_case,
            "Filtered advertising measured interval in ms: "
            f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in filtered_values]}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Make some stats to log")
        # --------------------------------------------------------------------------------------------------------------
        wrong_interval = []
        for interval in filtered_values:
            if not interval <= max_advertising_interval_ns:
                wrong_interval.append(interval)
            # end if
        # end for
        if len(filtered_values) > 0:
            error_percentage = 100 * len(wrong_interval) / len(filtered_values)
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, f"Intervals out of the accepted range ({error_percentage:.2f}%): "
                           f"{[a / TIMESTAMP_UNIT_DIVIDER_MAP['ms'] for a in wrong_interval]}")
            # --------------------------------------------------------------------------------------------------------------
        else:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "All intervals filtered out, no statistics can be established")
            # --------------------------------------------------------------------------------------------------------------
        # end if
        return filtered_values, wrong_interval
    # end def filter_hdc_intervals

    @classmethod
    def get_expected_series_application_pairing(cls, test_case, prepairing=False):
        """
        Get the expected advertisement series for the device configuration in application pairing.

        source and reference:
        https://spaces.logitech.com/x/gwAnDQ 2.1.1.1 pairing

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :return: A tuple of series in order from lowest to highest priority
        :param prepairing: Flag indicating if prepairing
        :type prepairing:
        :rtype:
        """
        swift_pair = test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_SwiftPairCapability
        ble_pro = test_case.f.PRODUCT.PROTOCOLS.BLE_PRO.F_Enabled
        fast_pair = test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_FastPairCapability
        if swift_pair:
            if ble_pro:
                if fast_pair:
                    series = [BleAdvertisingSeries.A, BleAdvertisingSeries.B, BleAdvertisingSeries.C]
                else:  # no fast pair
                    series = [BleAdvertisingSeries.E, BleAdvertisingSeries.F]
                # end if
            else:  # no ble_pro
                if fast_pair:
                    series = [BleAdvertisingSeries.A, BleAdvertisingSeries.B, BleAdvertisingSeries.P]
                else:  # no fast pair
                    series = [BleAdvertisingSeries.Q, BleAdvertisingSeries.R]
                # end if
            # end if
        else:  # no swift pair
            if ble_pro:
                if fast_pair:
                    series = [BleAdvertisingSeries.S, BleAdvertisingSeries.C]
                else:  # no fast pair
                    series = [BleAdvertisingSeries.T,]
                # end if
            else:  # no ble_pro
                if fast_pair:
                    test_case.fail("Advertisement series expected for device with Fast Pair "
                                   "but no Swift Pair and BLE Pro is not yet defined")
                    series = None # done to not have a usage before attribution error in Pycharm
                else:  # no fast pair
                    series = [BleAdvertisingSeries.U,]
                # end if
            # end if
        # end if
        if prepairing:
            series.append(BleAdvertisingSeries.D)
        # end if

        # Check asked pairing series is compatible with Mezzi 1.0
        # Changes of specifications can cause this error.
        # For reasons of simplicity of implementation this check only look
        # if there is service data before the ble pro service data.
        # If an explicit decision to put a longer service data chunk before BLE PRO,
        # it will need to be handled in the check.
        # Idem if explicit decision to break compatibility with Mezzi 1.0
        # https://jira.logitech.io/browse/MZI-115
        if ble_pro:
            for looked_at_series in series:
                service_data = []
                for key, value in looked_at_series.value.scan_response.items():
                    if key == BleAdvertisingDataType.SERVICE_DATA:
                        if value is BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD:
                            if len(service_data) > 0:
                                test_case.fail("Asked advertising packet may cause an incompatibility with Mezzy 1.0.\n"
                                               "Verify that the field(s) before BLE Pro are shorter than "
                                               "the BLE PRO one.\n If not this reproduces the condition of "
                                               "https://jira.logitech.io/browse/MZI-115")
                            # end if
                        else:
                            service_data.append(series)
                        # end if
                    # end if
                # end for
            # end for
        # end if

        return series
    # end def get_expected_series_application_pairing

    @classmethod
    def get_scan_time(cls, expected_series, max_scan_time=None):
        """
        return the duration of advertisement in a set of series, capped to ``max_scan_time``

        :param expected_series: List of expected series definition
        :type expected_series: ``list[BleAdvertisingSeries]``
        :param max_scan_time: Maximum time to scan, if omited scan for the whole advertising duration - OPTIONAL
        :type max_scan_time: ``int`` or ``float`` or ``None``

        :return: duration in seconds
        :rtype: ``int`` or ``float``
        """
        if max_scan_time is None:
            max_scan_time = inf
        # end if

        duration = 0
        for s in expected_series:
            series = s.value
            if series.start.value >= max_scan_time:
                continue  # this series start is after the max scan, so ignored
            # end if

            duration = max(duration, min(max_scan_time, series.stop.value))  # get new duration if applicable
        # end for
        return duration
    # end def get_scan_time

    @classmethod
    def get_scan_time_one_window_each_series(cls, expected_series, max_scan_time=None):
        """
        return the duration to get one window of each series in a set of series, capped to ``max_scan_time``

        :param expected_series: List of expected series definition
        :type expected_series: ``list[BleAdvertisingSeries]``
        :param max_scan_time: Maximum time to scan, if omitted scan until one window is expected to be found - OPTIONAL
        :type max_scan_time: ``int`` or ``float`` or ``None``

        :return: duration in seconds
        :rtype: ``int`` or ``float``
        """
        if max_scan_time is None:
            max_scan_time = inf
        # end if

        duration = 0
        for s in expected_series:
            series = s.value
            if series.start.value >= max_scan_time:
                continue  # this series start is after the max scan, so ignored
            # end if
            window = series.window.value
            if window is not None:
                first_window = series.start.value + window[1]
            else:
                first_window = series.stop.value
            # end if
            duration = max(duration, min(max_scan_time, first_window))  # get new duration if applicable
        # end for
        return duration
    # end def get_scan_time_one_window_each_series

    @classmethod
    def get_scan_time_number_of_interval_for_each_series(cls, expected_series, number_of_interval, max_scan_time=None):
        """
        return the duration to get N interval of each series in a set of series, capped to ``max_scan_time``

        :param expected_series: List of expected series definition
        :type expected_series: ``list[BleAdvertisingSeries]``
        :param number_of_interval: the number of interval for each series
        :type number_of_interval: ``int``
        :param max_scan_time: Maximum time to scan, if omitted scan until one window is expected to be found - OPTIONAL
        :type max_scan_time: ``int`` or ``float`` or ``None``

        :return: duration in seconds
        :rtype: ``int`` or ``float``
        """
        if max_scan_time is None:
            max_scan_time = inf
        # end if
        timings = BleAdvertisingParser.get_expected_series_timing(expected_series)

        num_interval_for_each_series = {series: 0 for series in expected_series}

        duration = 0
        for timing in timings:
            series, start, stop = timing
            window_duration = stop-start

            if start >= max_scan_time:
                break  # this serie is ignored because its start is after the max scan timing
            # end if

            interval_ms = series.value.interval if (series.value.interval!= BleAdvertisingInterval.HIGH_DUTY_CYCLE) \
                else MAX_ADVERTISING_INTERVAL_DIRECTED_HDC

            num_interval_for_each_series[series] += window_duration * 1e3 / interval_ms

            duration += window_duration
            if num_interval_for_each_series[series] >= number_of_interval:
                # check all series done
                if np.all(np.array(list(num_interval_for_each_series.values())) >= number_of_interval):
                    # remove excess time in the last window
                    number_to_reduce = num_interval_for_each_series[series]-number_of_interval
                    duration -= number_to_reduce * interval_ms/ 1e3
                    # end search
                    break
                # end if
            # end if
        # end for

        return duration
    # end def get_scan_time_number_of_interval_for_each_series

    @classmethod
    def check_advertising_content(cls, test_case, advertising_packet, expected_series=None):
        """
        Check the advertising packet content. It will build the expected one from the test case settings.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param advertising_packet: Advertising packet to check
        :type advertising_packet: ``BleAdvertisingData``
        :param expected_series: The series this packet is part of, if none specified,
            use the first series of the pairing advertising of the current DUT  - Optional
        :type expected_series: ``BleAdvertisingSeries`` or ``None``
        """

        if expected_series is None:
            expected_series = cls.get_expected_series_application_pairing(test_case)[0]
        # end if
        expected_advertising_packet = cls.build_expected_advertising_data(test_case, expected_series.value.packet)

        cls._check_packet_content(test_case=test_case, expected_packet=expected_advertising_packet,
                                  obtained_packet=advertising_packet.records)
    # end def check_advertising_content

    @classmethod
    def build_expected_advertising_data(cls, test_case, packet_format):
        """
        Build an advertising packet from the expected values for a given format
        # The advertising dictionary follows the format for BleAdvertisingData

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param packet_format: definition of the packet format, a dictionary from a ``BleAdvertisingSeriesDefinition``
        :type packet_format: ``dict``

        :return: a dictionary of each fields in the packet's data. it follows the format for BleAdvertisingData
        :rtype: ``dict``
        """
        current_length = 0  # decide if used, currently unused
        expected_advertising_packet = dict()
        for data_type, content in packet_format.items():

            if isinstance(content, BleAdvertisementModelSpecificFields):
                if content.value <= BleAdvertisementModelSpecificFields.NAME_FULL.value:
                    max_name_length = content.value
                    data = HexList(list(bytes(test_case.f.SHARED.DEVICES.F_Name[0][:max_name_length], 'utf-8')))
                elif content == BleAdvertisementModelSpecificFields.TX_POWER:
                    data = HexList(test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_TxPower)
                elif content == BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE:
                    data = HexList(to_endian_list(value=DEVICE_TYPE_TO_BLE_APPEARANCE[
                        test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType],
                                                  byte_count=2, little_endian=True))
                elif content == BleAdvertisementModelSpecificFields.BOOTLOADER_APPEARANCE:
                    data = HexList("0000")
                elif content == BleAdvertisementModelSpecificFields.FAST_PAIR_DATA_FIELD:
                    data = HexList("2CFE") + HexList(test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_FastPairModelId)
                elif content == BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD:
                    data = to_endian_list(
                        value=BleUuidStandardService.LOGITECH_BLE_PRO, byte_count=2, little_endian=True)
                    data.append(AppServiceDataSubFieldDefault.BLE_PRO_SERVICE_PROTOCOL_TYPE)
                    data.append(
                        test_case.config_manager.get_feature_version(test_case.f.PRODUCT.PROTOCOLS.BLE_PRO))
                    data.append(AppServiceDataSubFieldDefault.DEVICE_STATE)
                    data.extend(to_endian_list(
                        value=int(test_case.f.PRODUCT.F_BluetoothPID, 16), byte_count=2, little_endian=True))
                    data.append(test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_AuthenticationType)
                    # Sanity check for Device type: it should only be on 4 bits
                    assert test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_DeviceType < 0x10, \
                        "Device type in setting on more than 4 bits: " \
                        f"{test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_DeviceType}"
                    data.append(test_case.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_DeviceType)
                    data.append(test_case.config_manager.get_feature(ConfigurationManager.ID.EXTENDED_MODEL_ID))
                else:
                    raise ValueError(f"{content} is unsupported")
                # end if
            elif isinstance(content, tuple):
                data = HexList()
                for part in content:
                    data.extend(HexList(to_endian_list(part, little_endian=True)))
                # end for
            elif isinstance(content, int):
                data = HexList(to_endian_list(content, little_endian=True))
            elif isinstance(content, BleAdvertisingDataConstants):
                data = content.value
            elif isinstance(content, HexList):
                data = content
            else:
                raise TypeError(f"{type(content)} is unsupported")
            # end if

            # append the data in the expected packet

            length = len(data)
            expected_advertising_packet[data_type] = [data]
            current_length += length + 2
        # end for
        return expected_advertising_packet
    # end def build_expected_advertising_data

    @staticmethod
    def advertising_dictionary_to_raw_bytes(advertising_dictionary):
        """
        concatenate an advertising dictionary into raw bytes

        :param advertising_dictionary: an advertising dictionary. it follows the format for BleAdvertisingData
        :type advertising_dictionary: ``dict``
        :return:
        :rtype:
        """
        raw_packet =[]
        for key, value in advertising_dictionary.items():
            length = 1 + len(value[0])
            raw_packet.extend([length, key])
            raw_packet.extend(value[0])
        # end for
        return raw_packet
    # end def advertising_dictionary_to_raw_bytes

    @staticmethod
    def check_characteristics(test_case, service, expected_characteristics):
        """
        Check a service has all its characteristics with all their expected properties,
        security level and default values

        Note: the security level is not readable by current back end, so value for its position is currently ignored

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param service: The service to check
        :type service: ``BleService``
        :param expected_characteristics: A dictionary of tuples of expected value, keyed on characteristics uuids
        :type expected_characteristics: ``dict[BleUuid, tuple[BleCharacteristicProperties, any, HexList]]``
        """
        # ------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, f"Test Loop on service {service.uuid}'s characteristics")
        # ------------------------------------------------------------------------------------------------------
        for characteristic in service.characteristics:
            # TODO: Read security level or remove variable

            if characteristic.uuid not in expected_characteristics.keys():
                continue
            # end if

            expected_properties, expected_security_level, expected_default = expected_characteristics[
                characteristic.uuid]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Check if characteristic {characteristic.uuid} has the expected properties")
            # ----------------------------------------------------------------------------------------------------------
            test_case.assertEqual(expected=expected_properties,
                                  obtained=characteristic.properties,
                                  msg=f"Properties in {characteristic.uuid} differ from expected")

            if expected_properties.read and expected_default is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case,
                                   f"Check if characteristic {characteristic.uuid} has the expected default value")
                # ------------------------------------------------------------------------------------------------------
                value = test_case.ble_context.attribute_read(ble_context_device=test_case.current_ble_device,
                                                             attribute=characteristic)
                if isinstance(expected_default, (map, list)):
                    test_case.assertIn(member=value.data,
                                       container=expected_default,
                                       msg=f"Default value in {characteristic.uuid} differ from expected values")
                else:
                    test_case.assertEqual(expected=expected_default,
                                          obtained=value.data,
                                          msg=f"Default value in {characteristic.uuid} differs from the expected one")
                # end if
            # end if
        # end for

    # end def check_characteristics

    @classmethod
    def check_scan_response_content(cls, test_case, scan_response, expected_series=None):
        """
        Check the scan response content. It will build the expected one from the test case settings.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param scan_response: Scan response to check
        :type scan_response: ``BleAdvertisingData``
        :param expected_series: the advertising series definition that will be matched against,
            if omitted will use the first of the device pairing mode sequence
        :type expected_series: ``BleAdvertisingSeries``
        """
        if expected_series is None:
            expected_series = cls.get_expected_series_application_pairing(test_case)[0]
        # end if

        expected_scan_response = cls.build_expected_advertising_data(test_case, expected_series.value.scan_response)


        cls._check_packet_content(test_case=test_case, expected_packet=expected_scan_response,
                                  obtained_packet=scan_response.records)
    # end def check_scan_response_content

    @staticmethod
    def is_logitech_ble_uuid_in_record(advertising_data):
        """
        Verify if a Logitech BLE UUID is part of the record for ``BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE``
        in advertising packet.

        :param advertising_data: Advertising data object
        :type advertising_data: ``BleAdvertisingData``

        :return: Flag indicating if a Logitech BLE UUID is present
        :rtype: ``bool``
        """
        if BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE not in advertising_data.records:
            return False
        # end if

        for elements in advertising_data.records[BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE]:
            for index in range(0, len(elements) - 1, 2):
                uuid = elements[index] + (elements[index + 1] << 8)
                if uuid in [BleUuidStandardService.LOGITECH_BLE_PRO,
                            BleUuidStandardService.LOGITECH_GENERIC_BLE]:
                    return True
                # end if
            # end for
        # end for
        return False
    # end def is_logitech_ble_uuid_in_record

    @staticmethod
    def is_short_name_in_settings_name(test_case, advertising_data):
        """
        Verify if the short local name in the record for ``BleAdvertisingDataType.SHORT_LOCAL_NAME`` in advertising
        packet is a substring of the complete name in settings.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param advertising_data: Advertising data object
        :type advertising_data: ``BleAdvertisingData``

        :return: Flag indicating if the short local name is as expected
        :rtype: ``bool``
        """
        if BleAdvertisingDataType.SHORT_LOCAL_NAME not in advertising_data.records:
            return False
        # end if

        for element in advertising_data.records[BleAdvertisingDataType.SHORT_LOCAL_NAME]:
            name = bytes(element)
            if name in bytes(test_case.f.SHARED.DEVICES.F_Name[0], 'utf-8'):
                return True
            # end if
        # end for
        return False
    # end def is_short_name_in_settings_name

    @classmethod
    def connect_device(cls, test_case, ble_context_device, confirm_connect=False, connection_parameters=None):
        """
        Connect to a device. It will not perform a service discovery.

        WARNING: This will not implement any retry mechanism (see https://jira.logitech.io/browse/PTB-1850).

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device to connect and bond to
        :type ble_context_device: ``BleContextDevice``
        :param confirm_connect: Flag indicating if the connection shall be verified - OPTIONAL
        :type confirm_connect: ``bool``
        :param connection_parameters: Connection parameters. If ``None``, the BLE Pro nominal values for Logitech will
                                      be used, see ``LogitechBleConnectionParameters`` - OPTIONAL
        :type connection_parameters: ``BleGapConnectionParameters`` or ``None``

        :return: Flag indicating if the connection worked
        :rtype: ``bool``
        """
        if connection_parameters is None:
            connection_parameters = BleGapConnectionParameters(
                min_connection_interval=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_CONNECTION_INTERVAL_MS,
                max_connection_interval=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_CONNECTION_INTERVAL_MS,
                supervision_timeout=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_SUPERVISION_TIMEOUT_MS,
                slave_latency=LogitechBleConnectionParameters.BLE_PRO_RECEIVER_SLAVE_LATENCY)
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, f"Connect with connection parameters = {connection_parameters}")
        # --------------------------------------------------------------------------------------------------------------

        return cls.get_ble_context(test_case=test_case).connect(
            ble_context_device=ble_context_device,
            connection_parameters=connection_parameters,
            service_discovery=False, confirm_connect=confirm_connect)
    # end def connect_device

    @classmethod
    def disconnect_device(cls, test_case, ble_context_device):
        """
        Disconnect from  a device.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device to connect and bond to
        :type ble_context_device: ``BleContextDevice``
        """
        cls.get_ble_context(test_case=test_case).disconnect(
            ble_context_device=ble_context_device)
    # end def disconnect_device

    @classmethod
    def connect_and_bond_device(cls, test_case, ble_context_device, connection_parameters=None, lesc=False,
                                log_gatt_table=True):
        """
        Connect and bond (or encrypt connection if already bonded) to a device. If the device was not already bonded,
        this method will save the host credentials to a pickle file.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device to connect and bond to
        :type ble_context_device: ``BleContextDevice``
        :param connection_parameters: Connection parameters. If ``None``, the BLE Pro nominal values for Logitech will
                                      be used, see ``LogitechBleConnectionParameters`` - OPTIONAL
        :type connection_parameters: ``BleGapConnectionParameters`` or ``None``
        :param lesc: Flag indicating to permit LE secure connection - OPTIONAL
        :type lesc: ``bool``
        :param log_gatt_table: Flag indicating if the gatt table is added to the log - OPTIONAL
        :type log_gatt_table: ``bool``
        """
        ble_context = cls.get_ble_context(test_case=test_case)

        counter = 0
        while counter < cls.MAX_TRIES:
            try:
                ble_context_device.wait_for_disconnection_event.clear()
                connected = cls.connect_device(test_case=test_case, ble_context_device=ble_context_device,
                                               confirm_connect=counter > 0,
                                               connection_parameters=connection_parameters)
                assert connected, "Connection failed"

                ble_context.perform_service_discovery(
                    ble_context_device=ble_context_device, vendor_uuid_bases_to_add=BASE_UUID_TO_ADD)
                ble_context.authenticate_just_works(ble_context_device=ble_context_device, lesc=lesc)

                if counter > BleChannel.RETRY_THRESHOLD_TO_LOG:
                    to_log = f"[BLE channel] Connection to device ({ble_context_device.address}) had to be retried " \
                             f"{counter} time(s)"
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case=test_case, msg=to_log)
                    # --------------------------------------------------------------------------------------------------
                    # TODO: This is to be removed when we do not want the statistics anymore.
                    #  See https://jira.logitech.io/browse/PTB-1850
                    sys.stdout.write(to_log + "\n")
                # end if

                break
            except AssertionError as e:
                test_case.log_traceback_as_warning(
                    supplementary_message="AssertionError while trying to connect and bond a BLE device")
                counter += 1
                if str(e) in ("No response from device", "Connection failed") and counter < cls.MAX_TRIES:
                    cls.wait_for_disconnection(test_case=test_case, ble_context_device=ble_context_device)
                    continue
                # end if
                e.args += (f"after {counter} tries",)
                raise
            except TransportContextException as e:
                test_case.log_traceback_as_warning(
                    supplementary_message="TransportContextException while trying to connect and bond a BLE device")
                counter += 1
                if e.get_cause() in [TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                     TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION] and \
                        counter < cls.MAX_TRIES:
                    cls.wait_for_disconnection(test_case=test_case, ble_context_device=ble_context_device)
                    continue
                # end if
                e.add_message(f"after {counter} tries")
                raise
            # end try
        # end while
        if log_gatt_table:
            gatt_table = ble_context.get_gatt_table(ble_context_device)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"GATT Table of device {ble_context_device.address.address}\n"
                                          f"{cls.gatt_table_to_string_with_handles(gatt_table)}")
            # ----------------------------------------------------------------------------------------------------------
        # end if
    # end def connect_and_bond_device

    @classmethod
    def connect_no_encryption(cls, test_case, ble_context_device, connection_parameters=None, lesc=False):
        """
        Connect to a device without encryption and perform service discovery.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device to connect and bond to
        :type ble_context_device: ``BleContextDevice``
        :param connection_parameters: Connection parameters. If ``None``, the BLE Pro nominal values for Logitech will
                                      be used, see ``LogitechBleConnectionParameters`` - OPTIONAL
        :type connection_parameters: ``BleGapConnectionParameters`` or ``None``
        """
        ble_context = cls.get_ble_context(test_case=test_case)

        counter = 0
        while counter < cls.MAX_TRIES:
            try:
                ble_context_device.wait_for_disconnection_event.clear()
                connected = cls.connect_device(test_case=test_case, ble_context_device=ble_context_device,
                                               confirm_connect=counter > 0, connection_parameters=connection_parameters)
                assert connected, "Connection failed"

                ble_context.perform_service_discovery(
                    ble_context_device=ble_context_device, vendor_uuid_bases_to_add=BASE_UUID_TO_ADD)

                if counter > BleChannel.RETRY_THRESHOLD_TO_LOG:
                    to_log = f"[BLE channel] Connection to device ({ble_context_device.address}) had to be retried " \
                             f"{counter} time(s)"
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case=test_case, msg=to_log)
                    # --------------------------------------------------------------------------------------------------
                    # TODO: This is to be removed when we do not want the statistics anymore.
                    #  See https://jira.logitech.io/browse/PTB-1850
                    sys.stdout.write(to_log + "\n")
                # end if

                break
            except AssertionError as e:
                test_case.log_traceback_as_warning(
                    supplementary_message="AssertionError while trying to connect a BLE device")
                counter += 1
                if str(e) in ("No response from device", "Connection failed") and counter < cls.MAX_TRIES:
                    cls.wait_for_disconnection(test_case=test_case, ble_context_device=ble_context_device)
                    continue
                # end if
                e.args += (f"after {counter} tries",)
                raise
            except TransportContextException as e:
                test_case.log_traceback_as_warning(
                    supplementary_message="Exception while trying to connect a BLE device")
                counter += 1
                if e.get_cause() in [TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                     TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION] and \
                        counter < cls.MAX_TRIES:
                    cls.wait_for_disconnection(test_case=test_case, ble_context_device=ble_context_device)
                    continue
                # end if
                e.add_message(f"after {counter} tries")
                raise
            # end try
        # end while
    # end def connect_no_encryption

    @classmethod
    def wait_for_disconnection(cls, test_case, ble_context_device):
        """
        Wait for the disconnection event to be propagated to the BLE context

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device to connect and bond to
        :type ble_context_device: ``BleContextDevice``
        """
        # Add a large wait time to let the internal state of the BLE context to be the right one
        if not ble_context_device.wait_for_disconnection_event.wait(
                timeout=BleContext.DISCONNECTION_STATE_SYNC_UP):
            try:
                test_case.logInfo("BLE context disconnection propagation timeout. Call disconnect device "
                                  f"at {perf_counter_ns()}")
                cls.disconnect_device(test_case=test_case, ble_context_device=ble_context_device)
            except TransportContextException:
                test_case.logTrace("TransportContextException while trying to disconnect a device")
            # end try
        else:
            test_case.logInfo(f"BLE context disconnection. Clear event queue at {perf_counter_ns()}")
            ble_context_device.ble_context_event_queue.clear_all_events_of_a_type(
                event_type=BleContextEventType.DISCONNECTION_EVENT)
            sleep(.1)
        # end if
    # end def wait_for_disconnection

    @classmethod
    def create_new_ble_channel(cls, test_case, ble_context_device, connection_parameters=None, log_gatt_table=True):
        """
        Connect, bond (or encrypt connection if already bonded) and create a new BLE channel around a device. The
        descriptors are read and the HID dispatcher of the new BLE channel is initialized with the Root feature 0x0000.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device to use
        :type ble_context_device: ``BleContextDevice``
        :param connection_parameters: Connection parameters. If ``None``, the BLE Pro nominal values for Logitech will
                                      be used, see ``LogitechBleConnectionParameters`` - OPTIONAL
        :type connection_parameters: ``BleGapConnectionParameters`` or ``None``
        :param log_gatt_table: Flag indicating if the gatt table is added to the log - OPTIONAL
        :type log_gatt_table: ``bool``

        :return: The newly created BLE Channel
        :rtype: ``BleChannel``
        """
        cls.connect_and_bond_device(
            test_case=test_case, ble_context_device=ble_context_device, connection_parameters=connection_parameters,
            log_gatt_table=log_gatt_table)
        ble_channel = BleChannel(
            ble_context=cls.get_ble_context(test_case=test_case), ble_context_device=ble_context_device)
        # Open the channel on the HID packets only for the last part of the test
        ble_channel.open()
        ChannelUtils.get_descriptors(test_case=test_case, channel=ble_channel)
        _, root_version = test_case.current_channel.hid_dispatcher.get_feature_entry_by_index(
            feature_index=Root.FEATURE_INDEX)
        ble_channel.hid_dispatcher.add_feature_entry(
            feature_index=Root.FEATURE_INDEX, feature_id=Root.FEATURE_ID, feature_version=root_version)

        return ble_channel
    # end def create_new_ble_channel

    @classmethod
    def delete_device_bond(cls, test_case, ble_context_device):
        """
        Delete the pickle file used for the host credentials (if there is one).

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device concerned by the pickle file
        :type ble_context_device: ``BleContextDevice``
        """
        cls.get_ble_context(test_case=test_case).delete_bond(ble_context_device=ble_context_device)
    # end def delete_device_bond

    @classmethod
    def customize_service_read(cls, service, characteristics):
        """
        Add a list of read characteristic to the given service

        :param service: the service to customize
        :type service: ``BleService``
        :param characteristics: List of characteristics to add, each characteristic as a tuple of the UUID and the value
        :type characteristics: ``list[tuple(BleUuid, HexList)]``
        """
        for uuid, value in characteristics:
            characteristic = BleCharacteristic(
                uuid=uuid,
                properties=BleCharacteristicProperties(read=True),
                value=value)
            service.characteristics.append(characteristic)
        # end for
    # end def customize_service_read

    @classmethod
    def customize_service_write(cls, service, characteristics):
        """
        Add a list of write characteristic with responses to the given service

        :param service: the service to customize
        :type service: ``BleService``
        :param characteristics: List of characteristics to add, each characteristic as the UUID
        :type characteristics: ``list[BleUuid]``
        """
        for uuid in characteristics:
            characteristic = BleCharacteristic(
                uuid=uuid,
                properties=BleCharacteristicProperties(write=True))
            service.characteristics.append(characteristic)
        # end for
    # end def customize_service_write

    @classmethod
    def customize_service_write_wo_resp(cls, service, characteristics):
        """
        Add a list of write characteristic without responses to the given service
        :param service: the service to customize
        :type service: ``BleService``
        :param characteristics: List of characteristics to add, each characteristic as the UUID
        :type characteristics: ``list[BleUuid]``
        """
        for uuid in characteristics:
            characteristic = BleCharacteristic(
                uuid=uuid,
                properties=BleCharacteristicProperties(write_wo_resp=True))
            service.characteristics.append(characteristic)
        # end for
    # end def customize_service_write_wo_resp

    @classmethod
    def customize_service_notify(cls, service, characteristics):
        """
        Add a list of notify characteristic to the given service
        :param service: the service to customize
        :type service: ``BleService``
        :param characteristics: List of characteristics to add, each characteristic as the UUID
        :type characteristics: ``list[BleUuid]``
        """
        for uuid in characteristics:
            characteristic = BleCharacteristic(
                uuid=uuid,
                properties=BleCharacteristicProperties(notify=True))
            characteristic.descriptors.append(
                BleDescriptor(uuid=BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION)))
            service.characteristics.append(characteristic)
        # end for
    # end def customize_service_notify

    @classmethod
    def change_host_os_emulation(cls, test_case, os_emulation_type=BleNvsChunks.OsDetectedType.UNDETERMINED, name=None,
                                 ble_pro_pid=None):
        """
        Change the GATT table of the host to emulate a specific OS.

        WARNING: It can trigger a reset of the host hardware.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param os_emulation_type: Type of the OS emulated by the host - OPTIONAL
        :type os_emulation_type: ``BleNvsChunks.OsDetectedType``
        :param name: Name to set in the Model Number String BLE characteristic - OPTIONAL
        :type name: ``OsXModelNames`` or ``IOSModelNames`` or ``None``
        :param ble_pro_pid: Name to set in the Model Number String BLE characteristic - OPTIONAL
        :type ble_pro_pid: ``int`` or ``None``

        :raise ``ValueError``: If OS emulation type is not supported
        """
        ble_context = cls.get_ble_context(test_case=test_case)

        if os_emulation_type in [BleNvsChunks.OsDetectedType.OSX, BleNvsChunks.OsDetectedType.IOS]:
            cls._change_host_os_emulation_apple(ble_context, os_emulation_type, name)
        elif os_emulation_type == BleNvsChunks.OsDetectedType.CHROME:
            cls._change_host_os_emulation_chrome(ble_context)
        elif os_emulation_type in [BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO, BleNvsChunks.OsDetectedType.LINUX,
                                   BleNvsChunks.OsDetectedType.UNDETERMINED]:
            cls._change_host_os_emulation_other(ble_context, os_emulation_type, ble_pro_pid)
        else:
            raise ValueError(f"Unsupported OS emulation type: {os_emulation_type}")
        # end if
    # end def change_host_os_emulation

    @classmethod
    def direct_subscribe_notification(cls, test_case, ble_context_device, characteristic, notification_queue=None):
        """
        Enable the notification on a given characteristic and return a queue with just that notification
        or add it to an existing queue

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device concerned by the characteristic
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to enable notification from
        :type characteristic: ``BleCharacteristic``
        :param notification_queue: queue to use. by default create a new one - OPTIONAL
        :type notification_queue: ``QueueWithEvents``

        :return: the queue collecting the notifications
        :rtype: ``QueueWithEvents``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        if notification_queue is None:
            notification_queue = QueueWithEvents()
        # end if
        if not ble_context.get_notification_status(ble_context_device=ble_context_device,
                                                   characteristic=characteristic):
            ble_context.enable_notification(
                ble_context_device=ble_context_device,
                characteristic=characteristic,
                time_stamped_queue=notification_queue
            )
        else:
            ble_context.update_notification_queue(
                ble_context_device=ble_context_device,
                characteristic=characteristic,
                time_stamped_queue=notification_queue)
        # end if
        return notification_queue
    # end def direct_subscribe_notification

    @classmethod
    def direct_subscribe_indication(cls, test_case, ble_context_device, characteristic, indication_queue=None):
        """
        enable indication on a given characteristic and return a queue with just that indication
        or add it to an existing queue


        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device concerned by the characteristic
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to enable indication from
        :type characteristic: ``BleCharacteristic``
        :param indication_queue: queue to use. by default create a new one - OPTIONAL
        :type indication_queue: ``QueueWithEvents``

        :return: the queue collecting the indication
        :rtype: ``QueueWithEvents``
        """

        ble_context = cls.get_ble_context(test_case=test_case)
        if indication_queue is None:
            indication_queue = QueueWithEvents()
        # end if
        if not ble_context.get_indication_status(ble_context_device=ble_context_device,
                                                 characteristic=characteristic):
            ble_context.enable_indication(
                ble_context_device=ble_context_device,
                characteristic=characteristic,
                time_stamped_queue=indication_queue
            )
        else:
            ble_context.update_indication_queue(
                ble_context_device=ble_context_device,
                characteristic=characteristic,
                time_stamped_queue=indication_queue)
        # end if
        return indication_queue
    # end def direct_subscribe_indication

    @classmethod
    def subscribe_notification(cls, test_case, ble_context_device, service_uuid, characteristic_uuid):
        """
        Enable the notification on all characteristics matching the given uuid and return the notification queue.
        If multiple characteristic correspond to this characteristic, only one queue with all notifications is created

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device concerned by the characteristic
        :type ble_context_device: ``BleContextDevice``
        :param characteristic_uuid: Characteristic UUID to enable notification from
        :type characteristic_uuid: ``BleUuid``
        :param service_uuid: Service UUID containing the characterisitc
        :type service_uuid: ``BleUuid``

        :return: the queue
        :rtype: ``QueueWithEvents``
        """
        ble_context = cls.get_ble_context(test_case=test_case)
        gatt_table = ble_context.get_gatt_table(ble_context_device)
        service = cls.get_service_in_gatt(gatt_table, service_uuid)
        notification_queue = QueueWithEvents()

        for characteristic in service.get_characteristics(characteristic_uuid):
            cls.direct_subscribe_notification(test_case, ble_context_device, characteristic, notification_queue)
        # end for

        return notification_queue
    # end def subscribe_notification

    @classmethod
    def subscribe_indication(cls, test_case, ble_context_device, service_uuid, characteristic_uuid):
        """
        Enable the indication on all characteristics matching the given uuid and return the indication queue.
        If multiple characteristic correspond to this characteristic, only one queue with all indications is created

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device concerned by the characteristic
        :type ble_context_device: ``BleContextDevice``
        :param characteristic_uuid: Characteristic UUID to enable notification from
        :type characteristic_uuid: ``BleUuid``
        :param service_uuid: Service UUID containing the characterisitc
        :type service_uuid: ``BleUuid``

        :return: the queue
        :rtype: ``QueueWithEvents``
        """

        ble_context = cls.get_ble_context(test_case=test_case)
        gatt_table = ble_context.get_gatt_table(ble_context_device)
        service = cls.get_service_in_gatt(gatt_table, service_uuid)
        indication_queue = QueueWithEvents()

        for characteristic in service.get_characteristics(characteristic_uuid):
            cls.direct_subscribe_indication(test_case, ble_context_device, characteristic, indication_queue)
        # end for

        return indication_queue
    # end def subscribe_indication

    @staticmethod
    def check_presence_attribute(test_case, gatt_table, service_uuid, characteristic_uuid, service_name,
                                 characteristic_name):
        """
        Check that the given attribute is present in the given gatt_table

        :param test_case: The current test case
        :type test_case: ``DeviceBaseTestCase``
        :param gatt_table: the gatt table to check in
        :type gatt_table: ``list``
        :param service_uuid: the UUID of the service the characteristic should be in
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: the UUID of the characteristic to check
        :type characteristic_uuid: ``BleUuid``
        :param service_name: Service name in human-readable form for the error printing
        :type service_name: ``str``
        :param characteristic_name: Characteristic name in human-readable form for the error printing
        :type characteristic_name: ``str``
        """
        service_to_check = BleProtocolTestUtils.get_service_in_gatt(gatt_table, service_uuid)
        test_case.assertNotNone(service_to_check,
                                msg=f"{service_name} service not in the GATT table")
        for characteristic in service_to_check.characteristics:
            if characteristic.uuid == characteristic_uuid:
                return
            # end if
        # end for
        test_case.fail(msg=f"{characteristic_name} not in {service_name} Service")
    # end def check_presence_attribute

    @classmethod
    def encrypt_connection(cls, test_case, ble_context_device, lesc=False, log_gatt_table=False):
        """
        Encrypt the connection ( or bond if not done) to a device. If the device was not already bonded,
        this method will save the host credentials to a pickle file.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param ble_context_device: Context device to connect and bond to
        :type ble_context_device: ``BleContextDevice``
        :param lesc: Flag indicating to permit LE secure connection - OPTIONAL
        :type lesc: ``bool``
        :param log_gatt_table: Flag indicating if the gatt table is added to the log - OPTIONAL
        :type log_gatt_table: ``bool``
        """
        ble_context = cls.get_ble_context(test_case=test_case)

        counter = 0
        while counter < cls.MAX_TRIES:
            try:
                ble_context.perform_service_discovery(
                    ble_context_device=ble_context_device, vendor_uuid_bases_to_add=BASE_UUID_TO_ADD)
                ble_context.authenticate_just_works(ble_context_device=ble_context_device, lesc=lesc)

                if counter > BleChannel.RETRY_THRESHOLD_TO_LOG:
                    to_log = f"[BLE channel] Connection to device ({ble_context_device.address}) had to be retried " \
                             f"{counter} time(s)"
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case=test_case, msg=to_log)
                    # --------------------------------------------------------------------------------------------------
                    # TODO: This is to be removed when we do not want the statistics anymore.
                    #  See https://jira.logitech.io/browse/PTB-1850
                    sys.stdout.write(to_log + "\n")
                # end if

                break
            except AssertionError as e:
                test_case.log_traceback_as_warning(
                    supplementary_message="Error while trying to encrypt a BLE device")
                counter += 1
                if str(e) in ("No response from device", "Connection failed") and counter < cls.MAX_TRIES:
                    # Add a small wait time to let the internal state of the BLE context to be the right one
                    ble_context_device.wait_for_disconnection_event.wait(
                        timeout=BleContext.BLOCKING_DEFAULT_TIMEOUT)
                    continue
                # end if
                e.args += (f"after {counter} tries",)
                raise
            except TransportContextException as e:
                test_case.log_traceback_as_warning(
                    supplementary_message="Error while trying to encrypt a BLE device")
                counter += 1
                if e.get_cause() in [TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                     TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION] and \
                        counter < cls.MAX_TRIES:
                    # Add a small wait time to let the internal state of the BLE context to be the right one
                    ble_context_device.wait_for_disconnection_event.wait(
                        timeout=BleContext.BLOCKING_DEFAULT_TIMEOUT)
                    continue
                # end if
                e.add_message(f"after {counter} tries")
                raise
            # end try
        # end while
        if log_gatt_table:
            gatt_table = ble_context.get_gatt_table(ble_context_device)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"GATT Table of device {ble_context_device.address.address}\n"
                                          f"{cls.gatt_table_to_string_with_handles(gatt_table)}")
            # ----------------------------------------------------------------------------------------------------------
        # end if
    # end def encrypt_connection

    @staticmethod
    def get_service_in_gatt(gatt_table, service_uuid):
        """
        Search for a service matching the given UUID in the provided gatt table and return the first instance matching,
        otherwise return ``None`` if not found

        :param gatt_table: the gatt table to check in
        :type gatt_table: ``list``
        :param service_uuid: the UUID of the service to find
        :type service_uuid: ``BleUuid``

        :return: the service matching the given UUID, or None if not found
        :rtype: ``BleService`` or None
        """
        for service in gatt_table:
            if service.uuid == service_uuid:
                return service
            # end if
        # end for
        return None
    # end def get_service_in_gatt

    @staticmethod
    def get_services_list_in_gatt(gatt_table, service_uuid):
        """
        Search for all services matching the given UUID in the provided gatt table and return them,
        empty list if none are found

        :param gatt_table: the gatt table to check in
        :type gatt_table: ``list``
        :param service_uuid: the UUID of the service to find
        :type service_uuid: ``BleUuid``

        :return: the services matching the given UUID
        :rtype: ``list[BleService]``
        """
        return [service for service in gatt_table if service.uuid == service_uuid]
    # end def get_services_list_in_gatt

    @staticmethod
    def gatt_table_to_string(gatt_table):
        """
        return a string representation of a gatt table
        :param gatt_table: the gatt table to use
        :type gatt_table: ``list``

        :return: a representation of the gatt table
        :rtype: ''str''
        """
        representation = ""
        for service in gatt_table:
            representation += f"|{'-':-<128}|\n"
            representation += f"|{str(service.uuid):<128}|\n"
            for characteristic in service.characteristics:
                representation += f"|{'':<32}{str(characteristic.uuid):<96}|\n"
                for descriptor in characteristic.descriptors:
                    representation += f"|{str(descriptor.uuid):>128}|\n"
                # end for
            # end for
        # end for
        representation += f"|{'-':-<128}|"
        return representation
    # end def gatt_table_to_string

    @staticmethod
    def gatt_table_to_string_with_handles(gatt_table):
        """
        Provide a string representation of a gatt table including the handles

        :param gatt_table: the gatt table to use
        :type gatt_table: ``list``

        :return: a representation of the gatt table
        :rtype: ''str''
        """
        representation = ""
        for service in gatt_table:
            representation += f"|{'-':-<160}|\n"
            service_string = f"{str(service.uuid)}[{service.handle}]"
            representation += f"|{service_string :<160}|\n"
            for characteristic in service.characteristics:
                characteristic_string = f"{str(characteristic.uuid)}[{characteristic.declaration.handle}] " \
                                        f"(value handle=[{characteristic.handle}]) "
                representation += f"|{'':<32}{characteristic_string :<128}|\n"
                for descriptor in characteristic.descriptors:
                    descriptor_string = f"{str(descriptor.uuid)}[{descriptor.handle}]"
                    representation += f"|{descriptor_string :>160}|\n"
                # end for
            # end for
        # end for
        representation += f"|{'-':-<160}|"
        return representation
    # end def gatt_table_to_string_with_handles

    @classmethod
    def check_write_permission(cls, test_case, service_uuid, characteristic_uuid, value):
        """
        Check if the write operation is rejected when the authentication level is too low

        :param test_case: The current test case
        :type test_case: ``DeviceBaseTestCase``
        :param service_uuid: The uuid of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: The uuid of the characteristic to use
        :type characteristic_uuid: ``BleUuid``
        :param value: the value to try to write on, it normally shouldn't be accepted
        :type value: ``HexList``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        except INSUFFICIENT_AUTHENTICATION which is filtered out
        """
        try:
            cls.write_characteristic(test_case,
                                     ble_context_device=test_case.current_ble_device,
                                     service_uuid=service_uuid,
                                     characteristic_uuid=characteristic_uuid,
                                     value=value)
            # fail the test if no exception was raised
            test_case.fail("Writing with too low of a permission was accepted")
        except TransportContextException as e:
            if e.get_cause() == TransportContextException.Cause.INSUFFICIENT_AUTHENTICATION:
                pass
            else:
                raise
            # end if
        # end try
    # end def check_write_permission

    @classmethod
    def check_write_wo_resp_permission(cls, test_case, service_uuid, characteristic_uuid, value):
        """
        Check if the write without responce operation is rejected when the authentication level is too low

        :param test_case: The current test case
        :type test_case: ``DeviceBaseTestCase``
        :param service_uuid: The uuid of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: The uuid of the characteristic to use
        :type characteristic_uuid: ``BleUuid``
        :param value: the value to try to write on, it normally shouldn't be accepted
        :type value: ``HexList``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        except INSUFFICIENT_AUTHENTICATION which is filtered out
        """
        try:
            cls.write_characteristic(test_case,
                                     ble_context_device=test_case.current_ble_device,
                                     service_uuid=service_uuid,
                                     characteristic_uuid=characteristic_uuid,
                                     value=value)
            # fail the test if no exception was raised
            test_case.fail("Writing with too low of a permission was accepted")
        except TransportContextException as e:
            if e.get_cause() == TransportContextException.Cause.INSUFFICIENT_AUTHENTICATION:
                pass
            else:
                raise
            # end if
        # end try
    # end def check_write_wo_resp_permission

    @classmethod
    def check_read_permission(cls, test_case, service_uuid, characteristic_uuid):
        """
        Check if the read operation is rejected when the authentication level is too low

        :param test_case: The current test case
        :type test_case: ``DeviceBaseTestCase``
        :param service_uuid: The uuid of the service containing the characteristic
        :type service_uuid:   ``BleUuid``
        :param characteristic_uuid: The uuid of the characteristic to use
        :type characteristic_uuid: ``BleUuid``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        except INSUFFICIENT_AUTHENTICATION which is filtered out
        """
        try:
            result = cls.read_characteristics(test_case,
                                              ble_context_device=test_case.current_ble_device,
                                              service_uuid=service_uuid,
                                              characteristic_uuid=characteristic_uuid)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Returned value from the read {result}")
            # ----------------------------------------------------------------------------------------------------------
            # fail the test if no exception was raised
            test_case.fail("Reading without a proper permission level shall trigger an error")
        except TransportContextException as e:
            if e.get_cause() == TransportContextException.Cause.INSUFFICIENT_AUTHENTICATION:
                pass
            else:
                raise
            # end if
        # end try
    # end def check_read_permission

    @classmethod
    def check_notification_permission(cls, test_case, service_uuid, characteristic_uuid):
        """
        Check if the notification subscribe operation is rejected when the authentication level is too low

        :param test_case: The current test case
        :type test_case: ``DeviceBaseTestCase``
        :param service_uuid:The uuid of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: The uuid of the characteristic to use
        :type characteristic_uuid:   ``BleUuid``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        except INSUFFICIENT_AUTHENTICATION which is filtered out
        """
        service = test_case.ble_context.get_service(ble_context_device=test_case.current_ble_device,
                                                    uuid=service_uuid)
        characteristics = service.get_characteristics(characteristic_uuid=characteristic_uuid)[0]
        try:
            cls.direct_subscribe_notification(test_case=test_case, ble_context_device=test_case.current_ble_device,
                                              characteristic=characteristics)
            # fail the test if no exception was raised
            test_case.fail("Subscribing to indication with too low of a permission was accepted")
        except TransportContextException as e:
            if e.get_cause() == TransportContextException.Cause.INSUFFICIENT_AUTHENTICATION:
                pass
            else:
                raise
            # end if
        # end try
    # end def check_notification_permission

    @classmethod
    def check_indication_permission(cls, test_case, service_uuid, characteristic_uuid):
        """
        Check if the indication subscribe operation is rejected when the authentication level is too low

        :param test_case: The current test case
        :type test_case: ``DeviceBaseTestCase``
        :param service_uuid:The uuid of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        :param characteristic_uuid: The uuid of the characteristic to use
        :type characteristic_uuid:   ``BleUuid``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        except INSUFFICIENT_AUTHENTICATION which is filtered out
        """
        service = test_case.ble_context.get_service(ble_context_device=test_case.current_ble_device,
                                                    uuid=service_uuid)
        characteristics = service.get_characteristics(characteristic_uuid=characteristic_uuid)[0]
        try:
            cls.direct_subscribe_indication(test_case, ble_context_device=test_case.current_ble_device,
                                            characteristic=characteristics)
            # fail the test if no exception was raised
            test_case.fail("Subscribing to indication with too low of a permission was accepted")
        except TransportContextException as e:
            if e.get_cause() == TransportContextException.Cause.INSUFFICIENT_AUTHENTICATION:
                pass
            else:
                raise
            # end if
        # end try
    # end def check_indication_permission

    @classmethod
    def get_hid_report(cls, test_case, gatt_table, current_ble_device, report_reference):
        """
        Get the report corresponding to the given report reference in a GATT Table

        :param test_case: Test case using this method
        :type test_case: ``DeviceBaseTestCase``
        :param gatt_table: The gatt table to search
        :type gatt_table: ``list``
        :param current_ble_device: the corresponding device
        :type current_ble_device: ``BleContextDevice``
        :param report_reference: The report reference to find see ``ReportReferences``
        :type report_reference: ``HexList``

        :return: Ble characteristic of the report
        :rtype: ``BleCharacteristic``
        """
        hids = BleProtocolTestUtils.get_service_in_gatt(gatt_table,
                                                        BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE))
        reports = [char for char in hids.characteristics if
                   char.uuid == BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT)]
        for report in reports:
            report_reference_read = BleProtocolTestUtils.read_descriptor(
                test_case, current_ble_device,
                report, BleUuid(BleUuidStandardDescriptor.REPORT_REFERENCE)).data
            if report_reference_read == report_reference:
                return report
            # end if
        # end for
        return None
    # end def get_hid_report

    @classmethod
    def _change_host_os_emulation_other(cls, ble_context, os_emulation_type, ble_pro_pid=None):
        """
        Change the GATT table of the host to emulate a specific OS for BLE Pro, linux and Windows.

        WARNING: It can trigger a reset of the host hardware.

        :param ble_context: the ble context of the current test case
        :type ble_context: ``BleContext``
        :param os_emulation_type: Type of the OS emulated by the host
        :type os_emulation_type: ``BleNvsChunks.OsDetectedType``
        :param ble_pro_pid: Name to set in the Model Number String BLE characteristic - OPTIONAL
        :type ble_pro_pid: ``BleProPid`` or ``None``

        :raise ``ValueError``: If OS emulation type is not supported
        """
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            ble_context.reset_central_gatt_table()
        # end if

        dis = BleService(uuid=dis_uuid)
        pnp_id = PnPId(vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG)

        if os_emulation_type == BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO:
            if ble_pro_pid is None:
                ble_pro_pid = BleProPid.RANGE_START
            # end if
            pnp_id.vendor_id = HexList(to_endian_list(ManufacturerDataCompanyId.LOGITECH_INTERNATIONAL_SA.value,
                                                      little_endian=True, byte_count=2))
            pnp_id.product_id = HexList(to_endian_list(ble_pro_pid, little_endian=True, byte_count=2))
            # dummy value needed to fill in the pnp_id field completely
            pnp_id.fw_build = HexList(to_endian_list(0x00, little_endian=True, byte_count=2))
            name = HexList(bytes(ManufacturerDataName.LOGITECH_INTERNATIONAL_SA.value, "utf-8"))
        elif BleNvsChunks.OsDetectedType.LINUX:
            pnp_id.vendor_id = HexList(to_endian_list(ManufacturerDataCompanyId.LINUX_FOUNDATION.value,
                                                      little_endian=True, byte_count=2))
            pnp_id.product_id = HexList(to_endian_list(0x00, little_endian=True, byte_count=2))
            # dummy values needed to fill in the pnp_id field completely
            pnp_id.fw_build = HexList(to_endian_list(0x00, little_endian=True, byte_count=2))
            name = HexList(bytes(ManufacturerDataName.LINUX_FOUNDATION.value, "utf-8"))
        elif os_emulation_type == BleNvsChunks.OsDetectedType.UNDETERMINED:  # windows
            pnp_id.vendor_id = HexList(to_endian_list(ManufacturerDataCompanyId.MICROSOFT.value,
                                                      little_endian=True, byte_count=2))
            # dummy values needed to fill in the pnp_id field completely
            pnp_id.product_id = HexList(to_endian_list(0x00, little_endian=True, byte_count=2))
            pnp_id.fw_build = HexList(to_endian_list(0x00, little_endian=True, byte_count=2))
            name = HexList(bytes(ManufacturerDataName.MICROSOFT.value, "utf-8"))
        else:
            raise ValueError(f"Unsupported OS emulation type: {os_emulation_type}")
        # end if

        characteristic = BleCharacteristic(
            uuid=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
            properties=BleCharacteristicProperties(read=True),
            value=HexList(pnp_id))
        dis.characteristics.append(characteristic)

        characteristic = BleCharacteristic(
            uuid=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
            properties=BleCharacteristicProperties(read=True),
            value=name)

        dis.characteristics.append(characteristic)
        ble_context.add_service_to_central_gatt_table(service=dis)
    # end def _change_host_os_emulation_other

    @classmethod
    def _change_host_os_emulation_chrome(cls, ble_context):
        """
        Change the GATT table of the host to emulate a specific OS to Chrome.

        WARNING: It can trigger a reset of the host hardware.

        :param ble_context: the ble context of the current test case
        :type ble_context: ``BleContext``
        """
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            ble_context.reset_central_gatt_table()
        # end if
        dis = BleService(uuid=dis_uuid)

        pnp_id = PnPId(
            vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
            vendor_id=HexList(to_endian_list(ManufacturerDataCompanyId.GOOGLE.value, little_endian=True, byte_count=2)),
            product_id=HexList(to_endian_list(BleChromePNPID.PRODUCT_ID, little_endian=True, byte_count=2)),
            fw_build=HexList(to_endian_list(BleChromePNPID.FW_BUILD, little_endian=True, byte_count=2))
        )
        characteristic = BleCharacteristic(
            uuid=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
            properties=BleCharacteristicProperties(read=True),
            value=HexList(pnp_id))
        dis.characteristics.append(characteristic)
        ble_context.add_service_to_central_gatt_table(service=dis)
    # end def _change_host_os_emulation_chrome

    @classmethod
    def _change_host_os_emulation_apple(cls, ble_context, os_emulation_type, name=None):
        """
        Change the GATT table of the host to emulate a specific OS from Apple.

        WARNING: It can trigger a reset of the host hardware.

        :param ble_context: the ble context of the current test case
        :type ble_context: ``BleContext``
        :param os_emulation_type: Type of the OS emulated by the host
        :type os_emulation_type: ``BleNvsChunks.OsDetectedType``
        :param name: Name to set in the Model Number String BLE characteristic - OPTIONAL
        :type name: ``OsXModelNames`` or ``IOSModelNames`` or ``None``
        """
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ancs_uuid = BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.ANCS)

        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid) or \
                ble_context.is_service_in_central_gatt_table(service_uuid=ancs_uuid):
            ble_context.reset_central_gatt_table()
        # end if
        dis = BleService(uuid=dis_uuid)

        characteristic = BleCharacteristic(
            uuid=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
            properties=BleCharacteristicProperties(read=True),
            value=HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8")))
        dis.characteristics.append(characteristic)

        characteristic = BleCharacteristic(
            uuid=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
            properties=BleCharacteristicProperties(read=True),
            value=HexList(PnPId(
                vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                vendor_id=HexList(
                    to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                # dummy values to fill in the pid
                product_id=HexList(to_endian_list(0x00, little_endian=True, byte_count=2)),
                fw_build=HexList(to_endian_list(0x00, little_endian=True, byte_count=2))
            )))
        dis.characteristics.append(characteristic)

        if name is None:
            if os_emulation_type == BleNvsChunks.OsDetectedType.IOS:
                name = IosModelName.IPHONE
            elif os_emulation_type == BleNvsChunks.OsDetectedType.OSX:
                name = OsXModelName.MAC_BOOK
            # end if
        # end if

        characteristic = BleCharacteristic(
            uuid=BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
            properties=BleCharacteristicProperties(read=True),
            value=HexList(bytes(name.value, "utf-8")))
        dis.characteristics.append(characteristic)
        ble_context.add_service_to_central_gatt_table(service=dis)

        if os_emulation_type == BleNvsChunks.OsDetectedType.IOS:
            ancs = BleService(uuid=ancs_uuid)
            ble_context.add_service_to_central_gatt_table(service=ancs)
        # end if
    # end def _change_host_os_emulation_apple

    @staticmethod
    def _check_packet_content(test_case, expected_packet, obtained_packet):
        """
        Internal method to check the content of a packet (advertising or scan response) in a dictionary format.

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param expected_packet: Expected packet
        :type expected_packet: ``dict``
        :param obtained_packet: Obtained packet
        :type obtained_packet: ``dict``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg=f"\nExpected packet:")
        # --------------------------------------------------------------------------------------------------------------
        for key in expected_packet.keys():
            key_to_print = key.name if isinstance(key, BleAdvertisingDataType) else key
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f"\t{key_to_print}: {expected_packet[key]}")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg=f"\nObtained packet:")
        # --------------------------------------------------------------------------------------------------------------
        for key in obtained_packet.keys():
            key_to_print = key.name if isinstance(key, BleAdvertisingDataType) else key
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f"\t{key_to_print}: {obtained_packet[key]}")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        test_case.assertEqual(
            obtained=len(obtained_packet.keys()), expected=len(expected_packet.keys()),
            msg="Not the same number of fields between the expected packet and the one obtained")

        for key in expected_packet.keys():
            test_case.assertTrue(
                expr=key in obtained_packet.keys(), msg=f"{key.name} field is not in the packet")
            for element in expected_packet[key]:
                test_case.assertTrue(expr=element in obtained_packet[key],
                                     msg=f"{element} data for {key.name} field is not in the packet")
            # end for
        # end for

        test_case.assertEqual(obtained=obtained_packet.keys(), expected=expected_packet.keys(),
                              msg="Obtained packet is not in the expected order")
    # end def _check_packet_content

    @staticmethod
    def _get_interval_range_for_missed_packets(expected_interval_ns, number_of_missed_packets):
        """
        Return the range of advertising interval representing a loss of packet. A small error of 2 milliseconds
        is added.

        :param expected_interval_ns: The expected interval in nanoseconds
        :param number_of_missed_packets: The number of missed packets
        :return:
        """
        accepted_error_ns = 2 * TIMESTAMP_UNIT_DIVIDER_MAP['ms']  # 2ms
        min_interval = (expected_interval_ns * number_of_missed_packets) - accepted_error_ns
        max_interval = ((expected_interval_ns + ADV_DELAY * TIMESTAMP_UNIT_DIVIDER_MAP['ms']) *
                        number_of_missed_packets) + accepted_error_ns

        return min_interval, max_interval
    # end def _get_interval_range_for_missed_packets

    @staticmethod
    def build_128_bits_uuid(uuid_list):
        """
        Build a ``BleUuid`` from a list of its bytes
        :param uuid_list: list of the bytes
        :type uuid_list: ``[int]``
        :return: The new BleUuid
        :rtype: ``BleUuid``
        """
        return BleUuid(value=(uuid_list[2] << 8) + uuid_list[3],
                       is_16_bits_uuid=False, uuid_base=uuid_list)
    # end def build_128_bits_uuid
# end class BleProtocolTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
