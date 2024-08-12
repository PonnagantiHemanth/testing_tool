#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.device_information.interface
:brief: Validate BLE GATT Device Information service interface test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/01/31
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import itertools

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_endian_list
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.gatt.device_information.device_information import \
    GattDeviceInformationServiceApplicationTestCases
from pytestbox.device.ble.gatt.device_information.device_information import \
    GattDeviceInformationServiceBootloaderTestCases
from pytestbox.device.ble.gatt.device_information.device_information import GattDeviceInformationServiceTestCases
from pytransport.ble.bleconstants import BlePnPIdVendorSrc
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleCharacteristicProperties
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.bleinterfaceclasses import PnPId
from pytransport.usb.usbconstants import VendorId

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------

_AUTHOR = "Sylvana Ieri"

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class GattDeviceInformationServiceInterfaceTestCase(GattDeviceInformationServiceTestCases):
    """
    BLE DIS Interface Test Cases application class
    """

    def _check_dis_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics
        of the GATT service in all mode

        Note: Expected value for serial number only defined for NRF52 devices
        Note: Expected value for software revision only defined for devices with Nordic "SoftDevices"
        source: https://spaces.logitech.com/x/6x9HCQ
        """
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.DEVICE_INFORMATION))

        string = HexList.fromString(self.f.SHARED.DEVICES.F_Name[0])
        serial_number = map(HexList.fromString, self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_UnitId)

        def firmware_revision_hexlist(arguments):
            prefix, number, revision, build = arguments
            return HexList.fromString(f"{prefix}{number}.{revision}_{build}")
        # end def firmware_revision_hexlist

        firmware_revision = map(firmware_revision_hexlist, itertools.product(*(
            self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_FwPrefix, self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_FwNumber,
            self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_Revision, self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_Build,)))

        self.assertNotNone(self.f.PRODUCT.PROTOCOLS.BLE.F_Software_Revision, "Software revision need to be included "
                                                                             "in settings")
        software_revision = map(HexList.fromString, self.f.PRODUCT.PROTOCOLS.BLE.F_Software_Revision)

        pid = int(self.f.PRODUCT.F_BluetoothPID, 16)

        def pnp_id_hex_list(build):
            build = int(build, 16)
            return HexList(PnPId(vendor_id_src=BlePnPIdVendorSrc.USB_IMPL_FORUM,
                                 vendor_id=HexList(
                                     to_endian_list(VendorId.LOGITECH_INC.value, little_endian=True, byte_count=2)),
                                 # dummy values to fill in the pid
                                 product_id=HexList(to_endian_list(pid, little_endian=True, byte_count=2)),
                                 fw_build=HexList(to_endian_list(build, little_endian=True, byte_count=2))))
        # end def pnp_id_hex_list

        pnp_id = map(pnp_id_hex_list, self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_Build)
        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING):
                (BleCharacteristicProperties(read=True), None, HexList.fromString("Logitech")),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING):
                (BleCharacteristicProperties(read=True), None, string),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SERIAL_NUMBER_STRING):
                (BleCharacteristicProperties(read=True), None, serial_number),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.FIRMWARE_REVISION_STRING):
                (BleCharacteristicProperties(read=True), None, firmware_revision),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SOFTWARE_REVISION_STRING):
                (BleCharacteristicProperties(read=True), None, software_revision),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID):
                (BleCharacteristicProperties(read=True), None, pnp_id),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)
    # end def _check_dis_characteristics
# end class GattDeviceInformationServiceInterfaceTestCase


class GattDeviceInformationServiceApplicationInterfaceTestCase(GattDeviceInformationServiceApplicationTestCases,
                                                               GattDeviceInformationServiceInterfaceTestCase):
    """
    BLE DIS Interface Test Cases Application class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get whole gatt table")
        # --------------------------------------------------------------------------------------------------------------
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
    # end def setUp

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_dis_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics
        of the GATT service in application mode
        """
        self._check_dis_characteristics()

        self.testCaseChecked("INT_BLE_GATT_DIS_0001")
    # end def test_dis_characteristics

# end class GattDeviceInformationServiceApplicationInterfaceTestCase
        
        
class GattDeviceInformationServiceBootloaderInterfaceTestCase(GattDeviceInformationServiceBootloaderTestCases,
                                                              GattDeviceInformationServiceInterfaceTestCase):
    """
    BLE DIS Interface Test Cases Bootloader class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get whole gatt table")
        # --------------------------------------------------------------------------------------------------------------
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
        self._get_feature_0003_index()
    # end def setUp

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_dis_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics
        of the GATT service in application mode
        """
        self._check_dis_characteristics()

        self.testCaseChecked("INT_BLE_GATT_DIS_0001")
    # end def test_dis_characteristics
# end class GattDeviceInformationServiceBootloaderInterfaceTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
