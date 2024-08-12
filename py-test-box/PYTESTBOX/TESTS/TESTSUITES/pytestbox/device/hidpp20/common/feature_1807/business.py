#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1807.business
:brief: HID++ 2.0 ``ConfigurableProperties`` business test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils as Utils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.keyboardinternationallayoutsutils import KeyboardInternationalLayoutsTestUtils
from pytestbox.device.hidpp20.common.feature_1807.configurableproperties import ConfigurablePropertiesTestCase
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils
from pytransport.ble.bleconstants import BlePnPIdVendorSrc
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.bleinterfaceclasses import PnPId
from pytransport.usb.usbconstants import VendorId

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"
_READ_DIS = "Get PnP ID characteristic in the Device Information Service"
_HARDWARE_RESET = "Perform required hardware reset to force firmware to re-init BLE with the new data"
_JUMP_ON_BOOTLOADER = "Jump on bootloader"
_MANUFACTURING_FEATURES = "Enable manufacturing features"
_DELETE_CHUNK_IN_NVS = "Delete chunk in NVS"

MIN_SPECIAL_CHARACTER_VALUE = 0x20
MIN_LETTER_CHARACTER_VALUE = 0x30
MAX_CHARACTER_VALUE = 0x7E


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class ConfigurablePropertiesBusinessTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` business test cases
    """

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.EXTENDED_MODEL_ID)
    @level('Business', 'SmokeTests')
    @services('Debugger')
    def test_configure_property_extended_model_id(self):
        """
        Test extended model id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check 0x0003.getDeviceInfo matches
        """
        property_id = ConfigurableProperties.PropertyId.EXTENDED_MODEL_ID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))

        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Extended Model Id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        extended_model_id = DeviceInformationTestUtils.HIDppHelper.get_extended_model_id(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check extended model id matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=extended_model_id,
                         msg="Extended Model Id obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_1807_0001", _AUTHOR)
    # end def test_configure_property_extended_model_id

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature4540")
    @level("Business")
    @services('Debugger')
    def test_configure_property_keyboard_layout(self):
        """
        Test keyboard layout business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check layout value through the getKeyboardLayout function (x4540 Keyboard international layouts feature)
        """
        property_id = ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=min(KeyboardInternationalLayouts.LAYOUT).value,
                                maxVal=max(KeyboardInternationalLayouts.LAYOUT).value)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Check layout value through the getKeyboardLayout function (x4540 Keyboard "
                                 "international layouts feature")
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset to force re-init")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

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
        check_map.update({
            "keyboard_layout": (checker.check_keyboard_layout, test_data)
        })
        checker.check_fields(self, response, feature_4540.get_keyboard_layout_response_cls, check_map)

        self.testCaseChecked("BUS_1807_0002", _AUTHOR)
    # end def test_configure_property_keyboard_layout

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone0(self):
        """
        Test RGB LED bin information business case:
        Check the 3 property ids are supported and not present, select the property one by one, write them,
        read them back
        """
        property_id = ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_1807_0003#1", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone0

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone1(self):
        """
        Test RGB LED bin information business case:
        Check the 3 property ids are supported and not present, select the property one by one, write them,
        read them back
        """
        property_id = ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_1807_0003#2", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone1

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone2(self):
        """
        Test RGB LED bin information business case:
        Check the 3 property ids are supported and not present, select the property one by one, write them,
        read them back
        """
        property_id = ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_1807_0003#3", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone2

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone3(self):
        """
        Test RGB LED bin information business case:
        Check the 3 property ids are supported and not present, select the property one by one, write them,
        read them back
        """
        property_id = ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_1807_0003#4", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone3

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_bin_information_zone4(self):
        """
        Test RGB LED bin information business case:
        Check the 3 property ids are supported and not present, select the property one by one, write them,
        read them back
        """
        property_id = ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        # TODO : Check LEDs behavior
        self.testCaseChecked("BUS_1807_0003#5", _AUTHOR)
    # end def test_configure_property_rgb_led_bin_information_zone4

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.SERIAL_NUMBER)
    @level("Business")
    @services('Debugger')
    def test_configure_property_serial_number(self):
        """
        Test serial number business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check 0x0003.getDeviceSerialNumber matches
        """
        property_id = ConfigurableProperties.PropertyId.SERIAL_NUMBER
        # Serial number format is a base-34 alphanumeric scheme (I and O are not used and all letters are upper cases)
        test_data = HexList("35" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Serial Number with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        serial_number = DeviceInformationTestUtils.HIDppHelper.get_device_serial_number(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Serial Number matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=serial_number,
                         msg="Serial Number obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_1807_0008", _AUTHOR)
    # end def test_configure_property_serial_number

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.CAR_SIMULATOR_PEDALS_TYPES)
    @level("Business")
    @services('Debugger')
    def test_configure_property_car_simulator_pedals_types(self):
        """
        Test car-simulator pedal types business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.CAR_SIMULATOR_PEDALS_TYPES
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0009", _AUTHOR)
    # end def test_configure_property_car_simulator_pedals_types

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.HIDPP_DEVICE_NAME)
    @level("Business")
    @services('Debugger')
    def test_configure_property_hidpp_device_name(self):
        """
        Test HID++ device name business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check 0x0005.getDeviceName matches
        """
        property_id = ConfigurableProperties.PropertyId.HIDPP_DEVICE_NAME
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(
            self, property_id), minVal=MIN_SPECIAL_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Device Name with feature 0x0005")
        # --------------------------------------------------------------------------------------------------------------
        device_name = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(self,
                                                                                  device_name_max_count=len(test_data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=device_name,
                         msg="Device Name obtained from feature 0x0005 should match written data")

        self.testCaseChecked("BUS_1807_0010", _AUTHOR)
    # end def test_configure_property_hidpp_device_name

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.HW_VERSION)
    @level("Business")
    @services('Debugger')
    def test_configure_property_hw_version(self):
        """
        Test hardware version business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.HW_VERSION
        test_data = HexList('')
        for _ in range(Utils.ConfigurationHelper.get_size(self, property_id)):
            test_data += HexList((randint(0, 9) << 4) | (randint(0, 9)))
        # end for
        LogHelper.log_info(self,
                           f"HW Version should be in BCD format (see feature 0x0003 specifications), got {test_data}")
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read FW Info for HW entity with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        if (str(HexList(DeviceInformation.EntityTypeV1.HARDWARE)) in
                self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE)):
            hw_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
                str(HexList(DeviceInformation.EntityTypeV1.HARDWARE)))
            fw_info = DeviceInformationTestUtils.HIDppHelper.get_fw_info(self, entity_index=hw_entity_idx)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FW number matches written data")
            # --------------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(test_data[0]),
                             obtained=to_int(fw_info.fw_number),
                             msg="FW number obtained from feature 0x0003 should match the most significant byte of "
                                 "the written data")

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FW revision matches written data")
            # --------------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(test_data[1]),
                             obtained=to_int(fw_info.fw_revision),
                             msg="FW revision obtained from feature 0x0003 should match the least significant byte of "
                                 "the written data")
        # end if

        self.testCaseChecked("BUS_1807_0028", _AUTHOR)
    # end def test_configure_property_hw_version

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.SOFTWARE_EXTRA_INFORMATION)
    @level("Business")
    @services('Debugger')
    def test_configure_property_software_extra_information(self):
        """
        Test software extra information business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.SOFTWARE_EXTRA_INFORMATION
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0029", _AUTHOR)
    # end def test_configure_property_software_extra_information

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.RGB_LED_ZONE_INTENSITY)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_zone_intensity(self):
        """
        Test RGB LED zone intensity business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = ConfigurableProperties.PropertyId.RGB_LED_ZONE_INTENSITY
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0034", _AUTHOR)
    # end def test_configure_property_rgb_led_zone_intensity

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.RGB_LED_DRIVER_ID)
    @level("Business")
    @services('Debugger')
    def test_configure_property_rgb_led_driver_id(self):
        """
        Test RGB LED driver id business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = ConfigurableProperties.PropertyId.RGB_LED_DRIVER_ID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0035", _AUTHOR)
    # end def test_configure_property_rgb_led_driver_id

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.PART_NUMBER)
    @level("Business")
    @services('Debugger')
    def test_configure_property_part_number(self):
        """
        Test part number business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = ConfigurableProperties.PropertyId.PART_NUMBER
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0036", _AUTHOR)
    # end def test_configure_property_part_number

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.REGULATORY_MODEL_NUMBER)
    @level("Business")
    @services('Debugger')
    def test_configure_property_regulatory_model_number(self):
        """
        Test regulatory model number business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = ConfigurableProperties.PropertyId.REGULATORY_MODEL_NUMBER
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0037", _AUTHOR)
    # end def test_configure_property_regulatory_model_number

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.DISABLE_EASY_PAIRING)
    @level("Business")
    @services('Debugger')
    def test_configure_property_disable_easy_pairing(self):
        """
        Test disable easy pairing business case:
        Check the property id is supported and not present, select the property, write it with load NVS, read it back
        and check read value matches the written value with load NVS.
        """
        property_id = ConfigurableProperties.PropertyId.DISABLE_EASY_PAIRING
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0038", _AUTHOR)
    # end def test_configure_property_disable_easy_pairing
# end class ConfigurablePropertiesBusinessTestCase


# noinspection DuplicatedCode
class ConfigurablePropertiesBLEProBusinessTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` BLE Pro specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE_PRO

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
    @features("BLEProProtocol")
    @level("Business")
    @services("BLEProReceiver")
    @services('AtLeastOneKey', (KEY_ID.HOST_1, KEY_ID.CONNECT_BUTTON, KEY_ID.LS2_CONNECTION))
    @services('Debugger')
    def test_configure_property_ble_gap_app_name(self):
        """
        BLE GAP application name Business case with BLE Pro receiver:
        Check the property id is supported and not present, select the property, write it, read it back
        Check the BLE Pro Device Discovery 0x4F Notification
        Check the pairing data stored in the BLE PRo receiver NVS.
        """
        if self.last_ble_address is None and self.device_debugger is not None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            self.device_memory_manager.read_nvs()
            self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=self, memory_manager=self.device_memory_manager)
        # end if

        property_id = ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_LETTER_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _MANUFACTURING_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check property: read request and NVS')
        # ---------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.check_property(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        device_name = DiscoveryTestUtils.get_name(device_discovery)
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=device_name,
                         msg="Device Name in Device Discovery Notifications should match written data")

        self.testCaseChecked("BUS_1807_0019", _AUTHOR)
    # end def test_configure_property_ble_gap_app_name
# end class ConfigurablePropertiesBLEProBusinessTestCase


# noinspection DuplicatedCode
class ConfigurablePropertiesBLEBusinessTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` BLE specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_ADV_SERVICE_DATA)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_adv_service_data(self):
        """
        Test BLE GAP advertising service data business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_ADV_SERVICE_DATA
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0006", _AUTHOR)
    # end def test_configure_property_ble_gap_adv_service_data

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_ADV_OUTPUT_POWER)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_adv_output_power(self):
        """
        Test BLE GAP advertising output power business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_ADV_OUTPUT_POWER
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0007", _AUTHOR)
    # end def test_configure_property_ble_gap_adv_output_power

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_BL_NAME)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_bl_name(self):
        """
        Test BLE GAP bootloader name business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_BL_NAME
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _JUMP_ON_BOOTLOADER)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Device Name characteristic in the GAP of the device")
        # --------------------------------------------------------------------------------------------------------------
        read_device_name_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.GENERIC_ACCESS),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME))
        assert len(read_device_name_characteristics) == 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=ascii_converter(read_device_name_characteristics[0].data),
                         msg="Device Name in GAP should match written data")

        self.testCaseChecked("BUS_1807_0018", _AUTHOR)
    # end def test_configure_property_ble_gap_bl_name

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_gap_app_name(self):
        """
        BLE GAP application name Business case with BLE direct:
        Check the property id is supported and not present, select the property, write it, read it back
        Check Advertising message received by the BLE stack emulator
        """
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_LETTER_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Device Name characteristic in the GAP of the device")
        # --------------------------------------------------------------------------------------------------------------
        read_device_name_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.GENERIC_ACCESS),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME))
        assert len(read_device_name_characteristics) == 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=ascii_converter(read_device_name_characteristics[0].data),
                         msg="Device Name in GAP should match written data")

        self.testCaseChecked("BUS_1807_0020", _AUTHOR)
    # end def test_configure_property_ble_gap_app_name

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_VID)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_vid(self):
        """
        Test BLE DIS vendor id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check Device Information Service.PnP ID.USB_VID : See
        https://spaces.logitech.com/pages/viewpage.action?pageId=81631905
        """
        property_id = ConfigurableProperties.PropertyId.BLE_DIS_VID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _READ_DIS)
        # --------------------------------------------------------------------------------------------------------------
        read_pnp_id_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID))
        assert len(read_pnp_id_characteristics) == 1
        pnp_id = PnPId.fromHexList(read_pnp_id_characteristics[0].data)

        if to_int(pnp_id.vendor_id_src) == BlePnPIdVendorSrc.BLUETOOTH_SIG:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Vendor Id matches written data")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(test_data),
                             obtained=to_int(pnp_id.vendor_id, little_endian=True),
                             msg="Vendor Id in PnP Id characteristic in DIS should match written data")
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Vendor Id does not change")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=VendorId.LOGITECH_INC,
                             obtained=to_int(pnp_id.vendor_id, little_endian=True),
                             msg="Vendor Id in PnP Id characteristic in DIS should not be changed")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check property is well written in NVS")
            # ----------------------------------------------------------------------------------------------------------
            Utils.check_property(self, property_id=property_id, data=test_data, hidpp_check=False, nvs_check=True)
        # end if

        self.testCaseChecked("BUS_1807_0021#1", _AUTHOR)
    # end def test_configure_property_ble_dis_vid

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_VID)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_usb_vid(self):
        """
        Test USB Vendor id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check Device Information Service.PnP ID.USB_VID : See
        https://spaces.logitech.com/pages/viewpage.action?pageId=81631905
        """
        property_id = ConfigurableProperties.PropertyId.USB_VID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _READ_DIS)
        # --------------------------------------------------------------------------------------------------------------
        read_pnp_id_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID))
        assert len(read_pnp_id_characteristics) == 1
        pnp_id = PnPId.fromHexList(read_pnp_id_characteristics[0].data)

        if to_int(pnp_id.vendor_id_src) == BlePnPIdVendorSrc.USB_IMPL_FORUM:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Vendor Id matches written data")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(test_data),
                             obtained=to_int(pnp_id.vendor_id, little_endian=True),
                             msg="Vendor Id in PnP Id characteristic in DIS should match written data")
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Vendor Id does not change")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=VendorId.LOGITECH_INC,
                             obtained=to_int(pnp_id.vendor_id, little_endian=True),
                             msg="Vendor Id in PnP Id characteristic in DIS should not be changed")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check property is well written in NVS")
            # ----------------------------------------------------------------------------------------------------------
            Utils.check_property(self, property_id=property_id, data=test_data, hidpp_check=False, nvs_check=True)
        # end if

        self.testCaseChecked("BUS_1807_0021#2", _AUTHOR)
    # end def test_configure_property_usb_vid

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_BL_PID)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_bl_pid(self):
        """
        Test BLE DIS bootloader product id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check Device Information Service.PnP ID.BT_PID in bootloader mode
        """
        property_id = ConfigurableProperties.PropertyId.BLE_DIS_BL_PID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _JUMP_ON_BOOTLOADER)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _READ_DIS)
        # --------------------------------------------------------------------------------------------------------------
        read_pnp_id_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID))
        assert len(read_pnp_id_characteristics) == 1
        pnp_id = PnPId.fromHexList(read_pnp_id_characteristics[0].data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Product Id matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(test_data),
                         obtained=to_int(pnp_id.pid, little_endian=True),
                         msg="Product Id in PnP Id characteristic in DIS should match written data")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Bootloader PID with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(self)
        btldr_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(self.feature_0003.entity_types.BOOTLOADER)))
        btldr_pid = DeviceInformationTestUtils.HIDppHelper.get_fw_info(self, entity_index=btldr_entity_idx).transport_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Bootloader PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=btldr_pid,
                         msg="Bootloader PID obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_1807_0022", _AUTHOR)
    # end def test_configure_property_ble_dis_bl_pid

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_APP_PID)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_app_pid(self):
        """
        Test BLE DIS application product id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check 0x0003.getDeviceInfo matches
        Check Device Information Service.PnP ID.BT_PID in application mode
        """
        property_id = ConfigurableProperties.PropertyId.BLE_DIS_APP_PID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _READ_DIS)
        # --------------------------------------------------------------------------------------------------------------
        read_pnp_id_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID))
        assert len(read_pnp_id_characteristics) == 1
        pnp_id = PnPId.fromHexList(read_pnp_id_characteristics[0].data)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Product Id matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(test_data),
                         obtained=to_int(pnp_id.pid, little_endian=True),
                         msg="Product Id in PnP Id characteristic in DIS should match written data")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Application PID with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(self)
        fw_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(self.feature_0003.entity_types.MAIN_APP)))
        app_pid = DeviceInformationTestUtils.HIDppHelper.get_fw_info(self, entity_index=fw_entity_idx).transport_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Application PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=app_pid,
                         msg="Application PID obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_1807_0023", _AUTHOR)
    # end def test_configure_property_ble_dis_app_pid

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    @bugtracker('SoftDeviceOverflowOnPropertyChange')
    def test_configure_property_ble_dis_manufacturer_name(self):
        """
        Test BLE DIS manufacturer name business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check Device Information Service Manufacturer Name String
        """
        property_id = ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_LETTER_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Manufacturer Name characteristic in the Device Information Service")
        # --------------------------------------------------------------------------------------------------------------
        read_manufacturer_name_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING))
        assert len(read_manufacturer_name_characteristics) == 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Manufacturer Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=ascii_converter(read_manufacturer_name_characteristics[0].data),
                         msg="Manufacturer Name in DIS should match written data")

        self.testCaseChecked("BUS_1807_0024", _AUTHOR)
    # end def test_configure_property_ble_dis_manufacturer_name

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_BL_MODEL_NUMBER)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_property_ble_dis_bl_model_number(self):
        """
        Test BLE DIS bootloader model number business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check Device Information Service model number in bootloader mode
        """
        property_id = ConfigurableProperties.PropertyId.BLE_DIS_BL_MODEL_NUMBER
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_SPECIAL_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _JUMP_ON_BOOTLOADER)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Model Number characteristic in the Device Information Service")
        # --------------------------------------------------------------------------------------------------------------
        read_model_number_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING))
        assert len(read_model_number_characteristics) == 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Model Number matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=ascii_converter(read_model_number_characteristics[0].data),
                         msg="Model Number in DIS should match written data")

        self.testCaseChecked("BUS_1807_0025", _AUTHOR)
    # end def test_configure_property_ble_dis_bl_model_number

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_APP_MODEL_NUMBER)
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    @bugtracker('SoftDeviceOverflowOnPropertyChange')
    def test_configure_property_ble_dis_app_model_number(self):
        """
        Test BLE DIS application model number business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check Device Information Service model number in application mode
        """
        property_id = ConfigurableProperties.PropertyId.BLE_DIS_APP_MODEL_NUMBER
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_SPECIAL_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Model Number characteristic in the Device Information Service")
        # --------------------------------------------------------------------------------------------------------------
        read_model_number_characteristics = BleProtocolTestUtils.read_characteristics(
            self,
            self.ble_context_device_used,
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING))
        assert len(read_model_number_characteristics) == 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Model Number matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ascii_converter(test_data),
                         obtained=ascii_converter(read_model_number_characteristics[0].data),
                         msg="Model Number in DIS should match written data")

        self.testCaseChecked("BUS_1807_0026", _AUTHOR)
    # end def test_configure_property_ble_dis_app_model_number

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_BL_ADV_NAME_SIZE)
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
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_BL_ADV_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0030", _AUTHOR)
    # end def test_configure_property_ble_bl_adv_name_size

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_APP_ADV_NAME_SIZE)
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
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_APP_ADV_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0031", _AUTHOR)
    # end def test_configure_property_ble_app_adv_name_size

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_BL_SR_NAME_SIZE)
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
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_BL_SR_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0032", _AUTHOR)
    # end def test_configure_property_ble_bl_sr_name_size

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_APP_SR_NAME_SIZE)
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
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_APP_SR_NAME_SIZE
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)
        self.testCaseChecked("BUS_1807_0033", _AUTHOR)
    # end def test_configure_property_ble_app_sr_name_size

    @features("Feature1807")
    @features("BLEProtocol")
    @level("Business")
    @services("BleContext")
    @services('Debugger')
    def test_configure_gatt_table_variable_length_properties_without_length_change(self):
        """
        Test all supported properties that lead to a variable length in the ble GATT table without changing the current
        length to avoid running in the issues of https://jira.logitech.io/browse/BT-555
        """
        property_ids_raw = [
            ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME,
            ConfigurableProperties.PropertyId.BLE_DIS_APP_MODEL_NUMBER,
        ]

        property_ids = list(filter(
            lambda x: x.name in self.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_PROPERTIES.F_SupportedProperties,
            property_ids_raw))

        test_data_list = {}

        for property_id in property_ids:
            match property_id:
                case ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Get Manufacturer Name characteristic in the Device Information Service")
                    # --------------------------------------------------------------------------------------------------
                    read_manufacturer_name_characteristics = BleProtocolTestUtils.read_characteristics(
                        self,
                        self.ble_context_device_used,
                        BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
                        BleUuid(BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING))
                    assert len(read_manufacturer_name_characteristics) == 1
                    size_data = len(read_manufacturer_name_characteristics[0].data)
                case ConfigurableProperties.PropertyId.BLE_DIS_APP_MODEL_NUMBER:
                    # ----------------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Get Model Number characteristic in the Device Information Service")
                    # ----------------------------------------------------------------------------------------------------------
                    read_model_number_characteristics = BleProtocolTestUtils.read_characteristics(
                        self,
                        self.ble_context_device_used,
                        BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
                        BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING))
                    assert len(read_model_number_characteristics) == 1
                    size_data = len(read_model_number_characteristics[0].data)
                case _:
                    raise ValueError(f"Unexpected property id {property_id!r}")
            # end match
            size_payload = Utils.ConfigurationHelper.get_size(self, property_id)
            test_data = RandHexList(size_data, minVal=MIN_SPECIAL_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
            test_data.addPadding(size=size_payload, fromLeft=False)
            self._write_check_supported_property(property_id, test_data)
            test_data_list[property_id] = test_data
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        if ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME in property_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get Manufacturer Name characteristic in the Device Information Service")
            # ----------------------------------------------------------------------------------------------------------
            read_manufacturer_name_characteristics = BleProtocolTestUtils.read_characteristics(
                self,
                self.ble_context_device_used,
                BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
                BleUuid(BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING))
            assert len(read_manufacturer_name_characteristics) == 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Manufacturer Name matches written data")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ascii_converter(test_data_list[
                                                          ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME]),
                             obtained=ascii_converter(read_manufacturer_name_characteristics[0].data),
                             msg="Manufacturer Name in DIS should match written data")
        # end if

        if ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME in property_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get Model Number characteristic in the Device Information Service")
            # ----------------------------------------------------------------------------------------------------------
            read_model_number_characteristics = BleProtocolTestUtils.read_characteristics(
                self,
                self.ble_context_device_used,
                BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
                BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING))
            assert len(read_model_number_characteristics) == 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Model Number matches written data")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ascii_converter(test_data_list[
                                                          ConfigurableProperties.PropertyId.BLE_DIS_APP_MODEL_NUMBER]),
                             obtained=ascii_converter(read_model_number_characteristics[0].data),
                             msg="Model Number in DIS should match written data")
        # end if
        self.testCaseChecked("BUS_1807_0039", "Sylvana Ieri")
    # end def test_configure_gatt_table_variable_length_properties_without_length_change
# end class ConfigurablePropertiesBLEBusinessTestCase


# noinspection DuplicatedCode
class ConfigurablePropertiesEQuadBusinessTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` EQuad specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.unifying_protocols()

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.EQUAD_DEVICE_NAME)
    @features("Unifying")
    @level("Business")
    @services('Debugger')
    def test_configure_property_equad_device_name(self):
        """
        eQuad device name Business case with pairing:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get device unit id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.unit_id = DeviceInformationTestUtils.HIDppHelper.get_device_info(test_case=self).unit_id

        property_id = ConfigurableProperties.PropertyId.EQUAD_DEVICE_NAME
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
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
                                                    ChannelUtils.get_device_index(test_case=self) - 1)
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

        self.testCaseChecked("BUS_1807_0004", _AUTHOR)
    # end def test_configure_property_equad_device_name

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.EQUAD_ID)
    @features("Unifying")
    @level("Business")
    @services('Debugger')
    def test_configure_property_equad_id(self):
        """
        Test eQuad id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check 0x0003.getDeviceInfo matches
        """
        property_id = ConfigurableProperties.PropertyId.EQUAD_ID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read EQuad Id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        equad_id = DeviceInformationTestUtils.HIDppHelper.get_device_info(self).model_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check EQuad Id matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertIn(member=test_data,
                      container=equad_id,
                      msg="Model Id obtained from feature 0x0003 should contain written data for EQuad Id")

        self.testCaseChecked("BUS_1807_0011", _AUTHOR)
    # end def test_configure_property_equad_id
# end class ConfigurablePropertiesEQuadBusinessTestCase


# noinspection DuplicatedCode
class ConfigurablePropertiesUSBBusinessTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` USB specific properties business test cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_VID)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_vid(self):
        """
        Test USB vendor id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check VendorId in USB Core Device Descriptor during USB enumeration
        """
        property_id = ConfigurableProperties.PropertyId.USB_VID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB VID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=int(Numeral(test_data)),
                         obtained=self.current_channel.get_usb_vid(),
                         msg="USB VID should match written data")

        self.testCaseChecked("BUS_1807_0012", _AUTHOR)
    # end def test_configure_property_usb_vid

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_BL_PID)
    @features("USB")
    @features("BootloaderAvailable")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_bl_pid(self):
        """
        Test USB bootloader product id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check 0x0003.getDeviceInfo matches
        """
        property_id = ConfigurableProperties.PropertyId.USB_BL_PID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
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
        LogHelper.log_step(self, "Read Bootloader PID with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(self)
        btldr_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(self.feature_0003.entity_types.BOOTLOADER)))
        btldr_pid = DeviceInformationTestUtils.HIDppHelper.get_fw_info(self, entity_index=btldr_entity_idx).transport_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Bootloader PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data,
                         obtained=btldr_pid,
                         msg="Bootloader PID obtained from feature 0x0003 should match written data")

        self.testCaseChecked("BUS_1807_0013", _AUTHOR)
    # end def test_configure_property_usb_bl_pid

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_APP_PID)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_app_pid(self):
        """
        Test USB application product id business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check ProductId in USB Core Device Descriptor during USB enumeration
        Check 0x0003.getDeviceInfo matches
        """
        property_id = ConfigurableProperties.PropertyId.USB_APP_PID
        test_data = RandHexList(Utils.ConfigurationHelper.get_size(self, property_id))
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Application PID matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=int(Numeral(test_data)),
                         obtained=self.current_channel.get_usb_pid(),
                         msg="USB Application PID should match written data")

        if self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_Enabled:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Read Application PID with feature 0x0003")
            # ----------------------------------------------------------------------------------------------------------
            self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
                self)
            fw_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
                str(HexList(self.feature_0003.entity_types.MAIN_APP)))
            app_pid = DeviceInformationTestUtils.HIDppHelper.get_fw_info(self, entity_index=fw_entity_idx).transport_id

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Application PID matches written data")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=test_data,
                             obtained=app_pid,
                             msg="Application PID obtained from feature 0x0003 should match written data")
        # end if

        self.testCaseChecked("BUS_1807_0014", _AUTHOR)
    # end def test_configure_property_usb_app_pid

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_MANUFACTURER_STRING)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_manufacturer_string_app(self):
        """
        Test USB manufacturer string business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check manufacturer string in USB Core Device Descriptor during USB enumeration
        """
        property_id = ConfigurableProperties.PropertyId.USB_MANUFACTURER_STRING
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_LETTER_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Manufacturer string matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=self.current_channel.get_manufacturer_string(),
                         msg="USB Manufacturer string should match written data")

        self.testCaseChecked("BUS_1807_0015", _AUTHOR)
    # end def test_configure_property_usb_manufacturer_string_app

    @features("Feature1807")
    @features("BootloaderAvailable")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_MANUFACTURER_STRING)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_manufacturer_string_bl(self):
        """
        Test USB manufacturer string business case:
        Check the property id is supported and not present, select the property, write it, read it back
        Check manufacturer string in USB Core Device Descriptor during USB enumeration

        USB manufacturer string shall be shared between bootloader and application
        """
        property_id = ConfigurableProperties.PropertyId.USB_MANUFACTURER_STRING
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_LETTER_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
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

        self.testCaseChecked("BUS_1807_0015", _AUTHOR)
    # end def test_configure_property_usb_manufacturer_string_bl

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_BL_PRODUCT_STRING)
    @features("USB")
    @features("BootloaderAvailable")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_bl_product_string(self):
        """
        Test USB bootloader product string business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.USB_BL_PRODUCT_STRING
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_LETTER_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
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

        self.testCaseChecked("BUS_1807_0016", _AUTHOR)
    # end def test_configure_property_usb_bl_product_string

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.USB_APP_PRODUCT_STRING)
    @features("USB")
    @level("Business")
    @services('Debugger')
    def test_configure_property_usb_app_product_string(self):
        """
        Test USB application product string business case:
        Check the property id is supported and not present, select the property, write it, read it back
        """
        property_id = ConfigurableProperties.PropertyId.USB_APP_PRODUCT_STRING
        test_data = RandHexList(size=Utils.ConfigurationHelper.get_size(self, property_id),
                                minVal=MIN_LETTER_CHARACTER_VALUE, maxVal=MAX_CHARACTER_VALUE)
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _HARDWARE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB Product string matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=self.current_channel.get_product_string(),
                         msg="USB Product string should match written data")

        self.testCaseChecked("BUS_1807_0017", _AUTHOR)
    # end def test_configure_property_usb_app_product_string
# end class ConfigurablePropertiesUSBBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
