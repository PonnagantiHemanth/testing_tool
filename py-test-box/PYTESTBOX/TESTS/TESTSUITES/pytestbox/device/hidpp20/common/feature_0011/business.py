#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.common.feature_0011.business
:brief: HID++ 2.0 ``PropertyAccess`` business test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.features.common.propertyaccess import PropertyAccess
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.keyboardinternationallayoutsutils import KeyboardInternationalLayoutsTestUtils
from pytestbox.device.base.propertyaccessutils import PropertyAccessTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_0011.propertyaccess import PropertyAccessTestCase
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_RE_INIT_USB = "Perform required hardware reset to re-init USB with the new data"
_JUMP_ON_BOOTLOADER = "Jump on bootloader"
_AUTHOR = "Kevin Dayet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class PropertyAccessBusinessTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` business test cases
    """

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.EXTENDED_MODEL_ID)
    @level('Business', 'SmokeTests')
    @services('Debugger')
    def test_configure_property_extended_model_id(self):
        """
        Test extended model id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check 0x0003.getDeviceInfo matches
        """
        property_id = PropertyAccess.PropertyId.EXTENDED_MODEL_ID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Extended Model Id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        extended_model_id = DeviceInformationTestUtils.HIDppHelper.get_extended_model_id(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check extended model id matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=extended_model_id,
                         msg="Extended Model Id obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_0011_0001", _AUTHOR)
    # end def test_configure_property_extended_model_id

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature4540")
    @level("Business")
    @services('Debugger')
    def test_configure_property_keyboard_layout(self):
        """
        Test keyboard layout business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check layout value through the getKeyboardLayout function (x4540 Keyboard international layouts feature)
        """
        property_id = PropertyAccess.PropertyId.KEYBOARD_LAYOUT
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # Check layout value through the getKeyboardLayout function (x4540 Keyboard international layouts feature)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetKeyboardLayout request")
        # --------------------------------------------------------------------------------------------------------------
        response = KeyboardInternationalLayoutsTestUtils.HIDppHelper.get_keyboard_layout(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetKeyboardLayoutResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_4540, _, _ = KeyboardInternationalLayoutsTestUtils.HIDppHelper.get_parameters(test_case=self)
        checker = KeyboardInternationalLayoutsTestUtils.GetKeyboardLayoutResponseChecker
        check_map = checker.get_default_check_map(self)
        # Set unsupported layout id, gaming keyboard will change it to United States (US).
        # Note: Gaming keyboards applied the patch at 2024/05/08
        # https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/mpk25_cinderella_tkl/+/e592acff88024b5689fd1942d0ae6242cb20fe8f
        check_map.update({
            "keyboard_layout": (checker.check_keyboard_layout,
                                test_data if not self.f.PRODUCT.F_IsGaming else KeyboardInternationalLayouts.LAYOUT.US)
        })
        checker.check_fields(self, response, feature_4540.get_keyboard_layout_response_cls, check_map)

        self.testCaseChecked("BUS_0011_0002", _AUTHOR)
    # end def test_configure_property_keyboard_layout

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone0(self):
        """
        Test RGB LED bin information business case:
        Check the property id zone 0 is supported and not present, select the property, write it with load NVS, read it
        back and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_0011_0003#1", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone0

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone1(self):
        """
        Test RGB LED bin information business case:
        Check the property id zone 1 is supported and not present, select the property, write it with load NVS, read it
        back and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_0011_0003#2", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone1

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone2(self):
        """
        Test RGB LED bin information business case:
        Check the property id zone 2 is supported and not present, select the property, write it with load NVS, read it
        back and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_0011_0003#3", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone2

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone3(self):
        """
        Test RGB LED bin information business case:
        Check the property id zone 3 is supported and not present, select the property, write it with load NVS, read it
        back and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_0011_0003#4", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone3

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone4(self):
        """
        Test RGB LED bin information business case:
        Check the property id zone 4 is supported and not present, select the property, write it with load NVS, read it
        back and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_0011_0003#5", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone4

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.SERIAL_NUMBER)
    @level("Business")
    @services('Debugger')
    def test_configure_property_serial_number(self):
        """
        Test serial number business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check 0x0003.getDeviceSerialNumber matches
        """
        property_id = PropertyAccess.PropertyId.SERIAL_NUMBER
        # Serial number format is a base-34 alphanumeric scheme (I and O are not used and all letters are upper cases)
        test_data = HexList("35" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Read Serial Number with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        serial_number = DeviceInformationTestUtils.HIDppHelper.get_device_serial_number(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Serial Number matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=serial_number,
                         msg="Serial Number obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_0011_0007", _AUTHOR)
    # end def test_configure_property_serial_number

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.CAR_SIMULATOR_PEDALS_TYPES)
    @level("Business")
    @services('Debugger')
    def test_configure_property_car_simulator_pedals_types(self):
        """
        Test car-simulator pedal types business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.CAR_SIMULATOR_PEDALS_TYPES
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0008", _AUTHOR)
    # end def test_configure_property_car_simulator_pedals_types

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.HIDPP_DEVICE_NAME)
    @level("Business")
    @services('Debugger')
    def test_configure_property_hidpp_device_name(self):
        """
        Test HID++ device name business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check 0x0005.getDeviceName matches
        """
        property_id = PropertyAccess.PropertyId.HIDPP_DEVICE_NAME
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Read Device Name with feature 0x0005")
        # --------------------------------------------------------------------------------------------------------------
        device_name = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(self,
                                                                                  device_name_max_count=len(test_data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Device Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=device_name,
                         msg="Device Name obtained from feature 0x0005 should match written data")

        self.testCaseChecked("BUS_0011_0009", _AUTHOR)
        self.testCaseChecked("FUN_0011_0002", _AUTHOR)
    # end def test_configure_property_hidpp_device_name

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.HW_VERSION)
    @level("Business")
    @services('Debugger')
    def test_configure_property_hw_version(self):
        """
        Test hardware version business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.HW_VERSION
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0028", _AUTHOR)
    # end def test_configure_property_hw_version

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.SOFTWARE_EXTRA_INFORMATION)
    @level("Business")
    @services('Debugger')
    def test_configure_property_software_extra_information(self):
        """
        Test software extra information business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.SOFTWARE_EXTRA_INFORMATION
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0029", _AUTHOR)
        self.testCaseChecked("FUN_0011_0004", _AUTHOR)
    # end def test_configure_property_software_extra_information

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.RGB_LED_ZONE_INTENSITY)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_zone_intensity(self):
        """
        Test RGB LED zone intensity business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.RGB_LED_ZONE_INTENSITY
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0034", _AUTHOR)
    # end def test_configure_property_rgb_led_zone_intensity

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.RGB_LED_DRIVER_ID)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_driver_id(self):
        """
        Test RGB LED driver id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.RGB_LED_DRIVER_ID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0035", _AUTHOR)
    # end def test_configure_property_rgb_led_driver_id

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.PART_NUMBER)
    @level("Business")
    @services('Debugger')
    def test_configure_property_part_number(self):
        """
        Test part number business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.PART_NUMBER
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0036", _AUTHOR)
    # end def test_configure_property_part_number

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.REGULATORY_MODEL_NUMBER)
    @level("Business")
    @services('Debugger')
    def test_configure_property_regulatory_model_number(self):
        """
        Test regulatory model number business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.REGULATORY_MODEL_NUMBER
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0037", _AUTHOR)
    # end def test_configure_property_regulatory_model_number

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.DISABLE_EASY_PAIRING)
    @level("Business")
    @services('Debugger')
    def test_configure_property_disable_easy_pairing(self):
        """
        Test disable easy pairing business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.DISABLE_EASY_PAIRING
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0038", _AUTHOR)
    # end def test_configure_property_disable_easy_pairing
# end class PropertyAccessBusinessTestCase


# noinspection DuplicatedCode
class PropertyAccessBLEProBusinessTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` BLE Pro specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE_PRO

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_APP_NAME)
    @features("BLEProProtocol")
    @level("Business")
    @services("BLEProReceiver")
    @services('Debugger')
    def test_configure_property_ble_gap_app_name(self):
        """
        BLE GAP application name Business case with BLE Pro receiver:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check the BLE Pro Device Discovery 0x4F Notification
        Check the pairing data stored in the BLE PRo receiver NVS.
        """
        if self.last_ble_address is None and self.device_debugger is not None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            self.device_memory_manager.read_nvs()
            self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=self, memory_manager=self.device_memory_manager)
        # end if

        property_id = PropertyAccess.PropertyId.BLE_GAP_APP_NAME
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id), minVal=0x30, maxVal=0x7E)
        self._write_check_supported_property(property_id, test_data)
        # Save the crafted BLE device name to correctly filter the discovery notifications
        DiscoveryTestUtils.set_ble_device_name(test_case=self, device_name=bytearray.fromhex(str(test_data)).decode())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        backup_channel = self.current_channel
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.current_channel.receiver_channel)
        DiscoveryTestUtils.start_discovery(self)
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')
        DiscoveryTestUtils.cancel_discovery(self)

        DevicePairingTestUtils.change_host_by_link_state(self)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=backup_channel)

        self._activate_features()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check property: read request and NVS')
        # ---------------------------------------------------------------------------
        Utils.check_property(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Device Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        device_name = DiscoveryTestUtils.get_name(device_discovery)
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=device_name,
                         msg="Device Name in Device Discovery Notifications should match written data")

        self.testCaseChecked("BUS_0011_0018", _AUTHOR)
        self.testCaseChecked("FUN_0011_0003", _AUTHOR)
    # end def test_configure_property_ble_gap_app_name
# end class PropertyAccessBLEProBusinessTestCase


# noinspection DuplicatedCode
class PropertyAccessBLEBusinessTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` BLE specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_ADV_SERVICE_DATA)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_adv_service_data(self):
        """
        Test BLE GAP advertising service data business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_ADV_SERVICE_DATA
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0006", _AUTHOR)
    # end def test_configure_property_ble_gap_adv_service_data

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_ADV_OUTPUT_POWER)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_adv_output_power(self):
        """
        Test BLE GAP advertising output power business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_ADV_OUTPUT_POWER
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0007", _AUTHOR)
    # end def test_configure_property_ble_gap_adv_output_power

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_BL_NAME)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_bl_name(self):
        """
        Test BLE GAP bootloader name business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_BL_NAME
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO :
        #  * enter bootloader mode
        #  * check the characteristic Device Name in the GAP of the device that can be read after connection (no need
        #  for advertising then)

        self.testCaseChecked("BUS_0011_0017", _AUTHOR)
    # end def test_configure_property_ble_gap_bl_name

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_APP_NAME)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_app_name(self):
        """
        BLE GAP application name Business case with BLE direct:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check Advertising message received by the BLE stack emulator
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_APP_NAME
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO : check Advertising message:
        #  * enter advertising mode
        #  The name information can be found in discoverable advertising (short name in advertising packet and
        #  complete name in scan response) so you will need to change host to an unconnected one.
        #  Or it should be in the characteristic Device Name in the GAP of the device that can be read after
        #  connection (no need for advertising then)

        self.testCaseChecked("BUS_0011_0019", _AUTHOR)
    # end def test_configure_property_ble_gap_app_name

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_DIS_VID)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_vid(self):
        """
        Test BLE DIS vendor id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check Device Information Service.PnP ID.USB_VID
        """
        property_id = PropertyAccess.PropertyId.BLE_DIS_VID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO : check Device Information Service.PnP ID.USB_VID
        #  See https://spaces.logitech.com/pages/viewpage.action?pageId=81631905

        self.testCaseChecked("BUS_0011_0021", _AUTHOR)
    # end def test_configure_property_ble_dis_vid

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_DIS_BL_PID)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_bl_pid(self):
        """
        Test BLE DIS bootloader Product id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check Device Information Service.PnP ID.BT_PID in bootloader mode
        """
        property_id = PropertyAccess.PropertyId.BLE_DIS_BL_PID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO : check Device Information Service.PnP ID.BT_PIT in bootloader mode
        #  * enter bootloader mode
        #  See https://spaces.logitech.com/pages/viewpage.action?pageId=81631905

        self.testCaseChecked("BUS_0011_0022", _AUTHOR)
    # end def test_configure_property_ble_dis_bl_pid

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_DIS_APP_PID)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_app_pid(self):
        """
        Test BLE DIS application product id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check 0x0003.getDeviceInfo matches
        Check Device Information Service.PnP ID.BT_PID in application mode
        """
        property_id = PropertyAccess.PropertyId.BLE_DIS_APP_PID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO : check 0x0003.getDeviceInfo matches
        #        check Device Information Service.PnP ID.BT_PID in application mode
        #  See https://spaces.logitech.com/pages/viewpage.action?pageId=81631905

        self.testCaseChecked("BUS_0011_0023", _AUTHOR)
    # end def test_configure_property_ble_dis_app_pid

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_DIS_MANUFACTURER_NAME)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_manufacturer_name(self):
        """
        Test BLE DIS manufacturer name business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check Device Information Service Manufacturer Name String
        """
        property_id = PropertyAccess.PropertyId.BLE_DIS_MANUFACTURER_NAME
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO : check Device Information Service Manufacturer Name String
        #  See https://spaces.logitech.com/pages/viewpage.action?pageId=81631905

        self.testCaseChecked("BUS_0011_0024", _AUTHOR)
    # end def test_configure_property_ble_dis_manufacturer_name

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_DIS_BL_MODEL_NUMBER)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_bl_model_number(self):
        """
        Test BLE DIS bootloader model number business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check Device Information Service model number in bootloader mode
        """
        property_id = PropertyAccess.PropertyId.BLE_DIS_BL_MODEL_NUMBER
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO : check Device Information Service model number in bootloader mode
        #  * enter bootloader mode
        #  See https://spaces.logitech.com/pages/viewpage.action?pageId=81631905

        self.testCaseChecked("BUS_0011_0025", _AUTHOR)
    # end def test_configure_property_ble_dis_bl_model_number

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_DIS_APP_MODEL_NUMBER)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_app_model_number(self):
        """
        Test BLE DIS application model number business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check Device Information Service model number in application mode
        """
        property_id = PropertyAccess.PropertyId.BLE_DIS_APP_MODEL_NUMBER
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # TODO : check Device Information Service model number in application mode
        #  See https://spaces.logitech.com/pages/viewpage.action?pageId=81631905

        self.testCaseChecked("BUS_0011_0026", _AUTHOR)
    # end def test_configure_property_ble_dis_app_model_number

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_BL_ADV_NAME_SIZE)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_bl_adv_name_size(self):
        """
        Test BLE GAP bootloader advertisement name size business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_BL_ADV_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0030", _AUTHOR)
    # end def test_configure_property_ble_bl_adv_name_size

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_APP_ADV_NAME_SIZE)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_app_adv_name_size(self):
        """
        Test BLE GAP application advertisement name size business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_APP_ADV_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0031", _AUTHOR)
    # end def test_configure_property_ble_app_adv_name_size

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_BL_SR_NAME_SIZE)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_bl_sr_name_size(self):
        """
        Test BLE GAP bootloader scan response name size business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_BL_SR_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0032", _AUTHOR)
    # end def test_configure_property_ble_bl_sr_name_size

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.BLE_GAP_APP_SR_NAME_SIZE)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_app_sr_name_size(self):
        """
        Test BLE GAP application scan response name size business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.BLE_GAP_APP_SR_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_0011_0033", _AUTHOR)
    # end def test_configure_property_ble_app_sr_name_size
# end class PropertyAccessBLEBusinessTestCase


# noinspection DuplicatedCode
class PropertyAccessEQuadBusinessTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` EQuad specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.unifying_protocols()

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.EQUAD_DEVICE_NAME)
    @features("Unifying")
    @level("Business")
    @services('Debugger')
    def test_configure_property_equad_device_name(self):
        """
        eQuad device name Business case with pairing:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get device unit id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.unit_id = DeviceInformationTestUtils.HIDppHelper.get_device_info(test_case=self).unit_id

        property_id = PropertyAccess.PropertyId.EQUAD_DEVICE_NAME
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        self.post_requisite_new_equad_connection = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform new device connection (to get new pairing info)')
        # --------------------------------------------------------------------------------------------------------------
        EQuadDeviceConnectionUtils.new_device_connection_and_pre_pairing(
            test_case=self, unit_ids=[self.unit_id], disconnect=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get device name in pairing info')
        # --------------------------------------------------------------------------------------------------------------
        device_name_req = GetEQuadDeviceNameRequest(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN +
                                                    self.original_device_index - 1)
        device_name_resp = ChannelUtils.send(
            test_case=self,
            channel=self.current_channel.receiver_channel,
            report=device_name_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetEQuadDeviceNameResponse
        )
        equad_device_name = device_name_resp.name_string.toString()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check EQuad device name matches written data')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=equad_device_name,
                         msg="EQuad device name should match written data")

        self.testCaseChecked("BUS_0011_0004", _AUTHOR)
        self.testCaseChecked("FUN_0011_0001", _AUTHOR)
    # end def test_configure_property_equad_device_name

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.EQUAD_ID)
    @features("Unifying")
    @level("Business")
    @services('Debugger')
    def test_configure_property_equad_id(self):
        """
        Test eQuad id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check 0x0003.getDeviceInfo matches
        """
        property_id = PropertyAccess.PropertyId.EQUAD_ID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Read EQuad Id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        equad_id = DeviceInformationTestUtils.HIDppHelper.get_device_info(self).model_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check EQuad Id matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertIn(member=test_data,
                      container=equad_id,
                      msg="Model Id obtained from feature 0x0003 should contain written data for EQuad Id")

        self.testCaseChecked("BUS_0011_0010", _AUTHOR)
    # end def test_configure_property_equad_id
# end class PropertyAccessEQuadBusinessTestCase


# noinspection DuplicatedCode
class PropertyAccessUSBBusinessTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` USB specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.USB_VID)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_vid(self):
        """
        Test USB vendor id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check VendorId in USB Core Device Descriptor during USB enumeration
        """
        property_id = PropertyAccess.PropertyId.USB_VID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _RE_INIT_USB)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB VID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=int(Numeral(test_data)),
                         obtained=self.current_channel.get_usb_vid(),
                         msg="USB VID should match written data")

        self.testCaseChecked("BUS_0011_0011", _AUTHOR)
    # end def test_configure_property_usb_vid

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.USB_BL_PID)
    @features("USB")
    @features("BootloaderAvailable")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_bl_pid(self):
        """
        Test USB bootloader product id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check 0x0003.getDeviceInfo matches
        """
        property_id = PropertyAccess.PropertyId.USB_BL_PID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _RE_INIT_USB)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _JUMP_ON_BOOTLOADER)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Bootloader PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=int(Numeral(test_data)),
                         obtained=self.current_channel.get_usb_pid(),
                         msg="USB Bootloader PID should match written data")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Read Bootloader PID with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(self)
        btldr_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(self.feature_0003.entity_types.BOOTLOADER)))
        btldr_pid = DeviceInformationTestUtils.HIDppHelper.get_fw_info(self, entity_index=btldr_entity_idx).transport_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Bootloader PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=btldr_pid,
                         msg="Bootloader PID obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_0011_0012", _AUTHOR)
    # end def test_configure_property_usb_bl_pid

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.USB_APP_PID)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_app_pid(self):
        """
        Test USB application product id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check ProductId in USB Core Device Descriptor during USB enumeration
        Check 0x0003.getDeviceInfo matches
        """
        property_id = PropertyAccess.PropertyId.USB_APP_PID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _RE_INIT_USB)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Application PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=int(Numeral(test_data)),
                         obtained=self.current_channel.get_usb_pid(),
                         msg="USB Application PID should match written data")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Read Application PID with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(self)
        fw_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(self.feature_0003.entity_types.MAIN_APP)))
        app_pid = DeviceInformationTestUtils.HIDppHelper.get_fw_info(self, entity_index=fw_entity_idx).transport_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Application PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=app_pid,
                         msg="Application PID obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_0011_0013", _AUTHOR)
    # end def test_configure_property_usb_app_pid

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.USB_MANUFACTURER_STRING)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_manufacturer_string_app(self):
        """
        Test USB manufacturer string business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check manufacturer string in USB Core Device Descriptor during USB enumeration
        """
        property_id = PropertyAccess.PropertyId.USB_MANUFACTURER_STRING
        test_data = HexList("55" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _RE_INIT_USB)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Manufacturer string matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=self.current_channel.get_manufacturer_string(),
                         msg="USB Manufacturer string should match written data")

        self.testCaseChecked("BUS_0011_0014", _AUTHOR)
    # end def test_configure_property_usb_manufacturer_string_app

    @features("Feature0011")
    @features("BootloaderAvailable")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.USB_MANUFACTURER_STRING)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_manufacturer_string_bl(self):
        """
        Test USB manufacturer string business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        Check manufacturer string in USB Core Device Descriptor during USB enumeration

        USB manufacturer string shall be shared between bootloader and application
        """
        property_id = PropertyAccess.PropertyId.USB_MANUFACTURER_STRING
        test_data = HexList("55" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _RE_INIT_USB)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _JUMP_ON_BOOTLOADER)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Manufacturer string matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=self.current_channel.get_manufacturer_string(),
                         msg="USB Manufacturer string should match written data")

        self.testCaseChecked("BUS_0011_0014", _AUTHOR)
    # end def test_configure_property_usb_manufacturer_string_bl

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.USB_BL_PRODUCT_STRING)
    @features("USB")
    @features("BootloaderAvailable")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_bl_product_string(self):
        """
        Test USB bootloader product string business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.USB_BL_PRODUCT_STRING
        test_data = HexList("55" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _RE_INIT_USB)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _JUMP_ON_BOOTLOADER)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Product string matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=self.current_channel.get_product_string(),
                         msg="USB Product string should match written data")

        self.testCaseChecked("BUS_0011_0015", _AUTHOR)
    # end def test_configure_property_usb_bl_product_string

    @features("Feature0011")
    @features("Feature0011AccessiblePropertyId", PropertyAccess.PropertyId.USB_APP_PRODUCT_STRING)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_app_product_string(self):
        """
        Test USB application product string business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = PropertyAccess.PropertyId.USB_APP_PRODUCT_STRING
        test_data = HexList("55" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _RE_INIT_USB)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Product string matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=self.current_channel.get_product_string(),
                         msg="USB Product string should match written data")

        self.testCaseChecked("BUS_0011_0016", _AUTHOR)
    # end def test_configure_property_usb_app_product_string
# end class PropertyAccessUSBBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
