#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.hids.interface
:brief: Validate BLE GATT human interface device service interfaces test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/03/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.blereportmap import HidReportHidppLongReportDescriptor
from pyhid.hid.blereportmap import HidReportHidppLongReportDescriptorLegacy
from pyhid.hiddata import HidData
from pylibrary.tools.hexlist import HexList
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.mlx90393multisensorutils import LogHelper
from pytestbox.device.ble.gatt.hids.hids import GattHIDSApplicationTestCases
from pytestbox.device.ble.gatt.hids.hids import GattHIDSBootloaderTestCases
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleCharacteristicProperties
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.bleinterfaceclasses import HIDInformation


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class GattHIDSApplicationInterfaceTestCase(GattHIDSApplicationTestCases):
    """
    BLE HIDS Interface Test Cases Application class
    """
    
    def setUp(self):
        # See GattHIDSApplicationTestCases,setUp
        super().setUp()
        self._prerequisite_gatt_table()
    # end def setUp

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_hids_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics
        of the GATT HIDS in application mode
        """

        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE))

        hid_information = [
            HexList(HIDInformation(bcd_hid=0x1101, country_code=0x00, flags=0x03)),  # TODO add japan, korean layouts
        ]

        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_INFORMATION):
                (BleCharacteristicProperties(read=True), None, hid_information),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT_MAP):
                (BleCharacteristicProperties(read=True), None, None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_CONTROL_POINT):
                (BleCharacteristicProperties(write_wo_resp=True), None, None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PROTOCOL_MODE):
                (BleCharacteristicProperties(read=True, write_wo_resp=True), None,
                 [HexList(HidData.Protocol.REPORT)]),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_OUTPUT_REPORT):
                (BleCharacteristicProperties(read=True, write_wo_resp=True, write=True), None, None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_INPUT_REPORT):
                (BleCharacteristicProperties(read=True, notify=True), None, None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_MOUSE_INPUT_REPORT):
                (BleCharacteristicProperties(read=True, notify=True), None, None),

        }
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the HIDS characteristics properties and default value")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_HIDS_0001", _AUTHOR)
    # end def test_hids_characteristics
# end class GattHIDSApplicationInterfaceTestCase


@features.class_decorator("BootloaderBLESupport")
class GattHIDSBootloaderInterfaceTestCase(GattHIDSBootloaderTestCases):
    """
    BLE HIDS Interface Test Cases Bootloader class
    """
    
    def setUp(self):
        # See GattHIDSBootloaderTestCases.setUp
        super().setUp()
        self._prerequisite_gatt_table()
    # end def setUp

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_hids_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics
        of the GATT HIDS in bootloader mode
        """

        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE))

        hid_information = [
            HexList(HIDInformation(bcd_hid=0x1101, country_code=0x00, flags=0x03))
        ]

        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_INFORMATION):
                (BleCharacteristicProperties(read=True), None, hid_information),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT_MAP):
                (BleCharacteristicProperties(read=True), None, [HexList(HidReportHidppLongReportDescriptor()),
                                                                HexList(HidReportHidppLongReportDescriptorLegacy())]),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_CONTROL_POINT):
                (BleCharacteristicProperties(write_wo_resp=True), None, None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_OUTPUT_REPORT):
                (BleCharacteristicProperties(read=True, write_wo_resp=True, write=True), None, None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_INPUT_REPORT):
                (BleCharacteristicProperties(read=True, notify=True), None, None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_MOUSE_INPUT_REPORT):
                (BleCharacteristicProperties(read=True, notify=True), None, None),

        }
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the HIDS characteristics properties and default value")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_HIDS_0002", _AUTHOR)
    # end def test_hids_characteristics
# end class GattHIDSBootloaderInterfaceTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
