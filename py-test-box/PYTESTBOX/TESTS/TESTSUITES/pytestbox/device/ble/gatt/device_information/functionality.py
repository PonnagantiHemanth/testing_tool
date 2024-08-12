#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.device_information.functionality
:brief: Validates BLE Device Information service of the GATT functionalities test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/01/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pylibrary.tools.hexlist import HexList
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.ble.gatt.device_information.device_information import \
    GattDeviceInformationServiceApplicationTestCases
from pytestbox.device.ble.gatt.device_information.device_information import \
    GattDeviceInformationServiceBootloaderTestCases
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.bleinterfaceclasses import PnPId


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattDeviceInformationServiceApplicationFunctionalityTestCase(GattDeviceInformationServiceApplicationTestCases):
    """
    BLE DIS Functionality Test Cases application class
    """
    @features('BLEProtocol')
    @features('Feature1807')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME)
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_manufacturer_name_change_with_1807(self):
        """
        Verify that the DIS Manufacturer Name String characteristic value is changed using the feature 0x1807
        """
        self.prerequisite_feature1807()

        dis_service = BleUuid(BleUuidStandardService.DEVICE_INFORMATION)
        manufacturer_name_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS Manufacturer Name String characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_name = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=dis_service,
                                                                            characteristic_uuid=manufacturer_name_char)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Name read: {original_name}")
        LogHelper.log_step(self, "Generate a different name from the read name")
        # --------------------------------------------------------------------------------------------------------------
        new_name_to_set = original_name.swapcase()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"New name to set: {new_name_to_set}")
        LogHelper.log_step(self, "Change the manufacturer name with with HID++ feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self,
                                                                    ConfigurableProperties.PropertyId.BLE_DIS_MANUFACTURER_NAME)
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList.fromString(new_name_to_set))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset device")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS Manufacturer Name String characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_name_read = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=dis_service,
                                                                            characteristic_uuid=manufacturer_name_char)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's the new name")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=original_name,
                            obtained=new_name_read,
                            msg="Current manufacturer name in the DIS is still the old one after writing with feature 0x1807")
        self.assertEqual(expected=new_name_to_set,
                         obtained=new_name_read,
                         msg="Current manufacturer name in the DIS doesn't match with name set with feature 0x1807")

        self.testCaseChecked("FUN_BLE_GATT_DIS_0001", _AUTHOR)
    # end def test_manufacturer_name_change_with_1807

    @features('BLEProtocol')
    @features('Feature1807')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_APP_MODEL_NUMBER)
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_model_number_string_change_with_1807(self):
        """
        Verify that the DIS Model Number String characteristic value is changed using the feature 0x1807
        """
        self.prerequisite_feature1807()

        dis_service = BleUuid(BleUuidStandardService.DEVICE_INFORMATION)
        model_number_string_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS Model Number String characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_model = BleProtocolTestUtils.read_characteristics_as_string(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=model_number_string_char)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Model number string read: {original_model}")
        LogHelper.log_step(self, "Generate a different model number string from the read model number string")
        # --------------------------------------------------------------------------------------------------------------
        new_model_to_set = original_model.swapcase()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"New model number to set: {new_model_to_set}")
        LogHelper.log_step(self, "Change the model number with with HID++ feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
            self, ConfigurableProperties.PropertyId.BLE_DIS_APP_MODEL_NUMBER)
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList.fromString(new_model_to_set))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset device")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS Model Number String characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_model_read = BleProtocolTestUtils.read_characteristics_as_string(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=model_number_string_char)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's the new model number")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=original_model,
                            obtained=new_model_read,
                            msg="Current model number in the DIS is still the old one after writing with feature 0x1807")
        self.assertEqual(expected=new_model_to_set,
                         obtained=new_model_read,
                         msg="Current model number in the DIS doesn't match with name set with feature 0x1807")

        self.testCaseChecked("FUN_BLE_GATT_DIS_0002", _AUTHOR)
    # end def test_model_number_string_change_with_1807

    @features('BLEProtocol')
    @features('Feature0003')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_firmware_revision_match(self):
        """
        Verify the firmware revision string matches the one obtained with hid++ feature 0003
        """
        self._get_feature_0003_index()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the DIS Firmware Revision String characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        dis_firmware_revision_string = BleProtocolTestUtils.read_characteristics_as_string(
            self, ble_context_device=self.current_ble_device,
            service_uuid=BleUuid(BleUuidStandardService.DEVICE_INFORMATION),
            characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.FIRMWARE_REVISION_STRING))[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Firmware revision in DIS {dis_firmware_revision_string}")
        LogHelper.log_step(self, "Get the corresponding value using the feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        fw_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(self.feature_0003.entity_types.MAIN_APP)))
        fw_info = DeviceInformationTestUtils.HIDppHelper.get_fw_info(test_case=self, entity_index=fw_entity_idx)
        hidpp_firmware_revision_string = f"{fw_info.fw_prefix.toString()}{fw_info.fw_number.toLong():02X}." \
                                         f"{fw_info.fw_revision.toLong():02X}_{fw_info.fw_build.toLong():04X}"
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Firmware revision from 0x0003 {hidpp_firmware_revision_string}")
        LogHelper.log_check(self, "Check that the values are the same")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=hidpp_firmware_revision_string,
                         obtained=dis_firmware_revision_string,
                         msg="The firmware revision string from the DIS service doesn't match "
                             "the one obtained through feature 0x0003")

        self.testCaseChecked("FUN_BLE_GATT_DIS_0004", _AUTHOR)
    # end def test_firmware_revision_match

    @features('BLEProtocol')
    @features('Feature1807')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_APP_PID)
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_pnp_id_pid_change_with_1807(self):
        """
        Verify that the DIS PNP ID characteristic value is changed using the feature 0x1807
        """
        self.prerequisite_feature1807()

        dis_service = BleUuid(BleUuidStandardService.DEVICE_INFORMATION)
        pnp_id_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS PNP ID characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_pnp = PnPId.fromHexList(BleProtocolTestUtils.read_characteristics(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=pnp_id_char)[0].data)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"PNP ID read: {original_pnp}")
        LogHelper.log_step(self, "Generate a different pnp id from the read pnp id")
        # --------------------------------------------------------------------------------------------------------------
        new_pid = original_pnp.product_id.toLong() ^ 0xFFFF
        new_pnp_id_pid_to_check = HexList.fromLong(new_pid, 2, littleEndian=False)
        new_pnp_id_pid_to_set = HexList.fromLong(new_pid, 2, littleEndian=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"New PNP Id to set: {new_pnp_id_pid_to_set}")
        LogHelper.log_step(self, "Change the pnp id with with HID++ feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self,
                                                                    ConfigurableProperties.PropertyId.BLE_DIS_APP_PID)
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, new_pnp_id_pid_to_set)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset device")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS PNP ID characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_pnp_id_pid_read = PnPId.fromHexList(BleProtocolTestUtils.read_characteristics(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=pnp_id_char)[0].data).product_id
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's the new pnp id")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=original_pnp.product_id,
                            obtained=new_pnp_id_pid_read,
                            msg="Current pnp id pid in the DIS is still the old one after writing with feature 0x1807")
        self.assertEqual(expected=new_pnp_id_pid_to_check,
                         obtained=new_pnp_id_pid_read,
                         msg="Current pnp id pid in the DIS doesn't match with name set with feature 0x1807")

        self.testCaseChecked("FUN_BLE_GATT_DIS_0005", _AUTHOR)
    # end def test_pnp_id_pid_change_with_1807
# end class GattDeviceInformationServiceApplicationFunctionalityTestCase


@features.class_decorator("BootloaderBLESupport")
class GattDeviceInformationServiceBootloaderFunctionalityTestCase(GattDeviceInformationServiceBootloaderTestCases):
    """
    BLE DIS Functionality Test Cases bootloader class
    """

    @features('BLEProtocol')
    @features('Feature1807')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_BL_PID)
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_model_number_string_change_with_1807(self):
        """
        Verify that the DIS PNP ID characteristic value is changed using the feature 0x1807
        """

        dis_service = BleUuid(BleUuidStandardService.DEVICE_INFORMATION)
        model_number_string_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS PNP ID characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_model = BleProtocolTestUtils.read_characteristics_as_string(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=model_number_string_char)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Model number string read: {original_model}")
        LogHelper.log_step(self, "Generate a different model number string from the read model number string")
        # --------------------------------------------------------------------------------------------------------------
        new_model_to_set = original_model.swapcase()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"New model number to set: {new_model_to_set}")
        LogHelper.log_step(self, "jump on application")
        # --------------------------------------------------------------------------------------------------------------
        DfuTestUtils.force_target_on_application(self, check_required=False)
        self.post_requisite_restart_in_main_application = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1807_index, self.feature_1807, _, _ = ConfigurablePropertiesTestUtils.HIDppHelper.get_parameters(
            test_case=self,
            feature_id=ConfigurableProperties.FEATURE_ID,
            factory=ConfigurablePropertiesFactory)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the pnp id with with HID++ feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
            self, ConfigurableProperties.PropertyId.BLE_DIS_BL_MODEL_NUMBER)
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList.fromString(new_model_to_set))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "jump on bootloader")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=True)
        self.post_requisite_restart_in_main_application = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS Model Number String characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_model_read = BleProtocolTestUtils.read_characteristics_as_string(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=model_number_string_char)[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's the new model number")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=original_model,
                            obtained=new_model_read,
                            msg="Current model number in the DIS is still the old one after writing with feature 0x1807")
        self.assertEqual(expected=new_model_to_set,
                         obtained=new_model_read,
                         msg="Current model number in the DIS doesn't match with name set with feature 0x1807")

        self.testCaseChecked("FUN_BLE_GATT_DIS_0003", _AUTHOR)

    # end def test_model_number_string_change_with_1807

    @features('BLEProtocol')
    @features('Feature1807')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_DIS_BL_PID)
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_pnp_id_pid_change_with_1807(self):
        """
        Verify that the DIS PNP ID characteristic value is changed using the feature 0x1807
        """
        dis_service = BleUuid(BleUuidStandardService.DEVICE_INFORMATION)
        pnp_id_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS PNP ID characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_pnp = PnPId.fromHexList(BleProtocolTestUtils.read_characteristics(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=pnp_id_char)[0].data)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"PNP ID read: {original_pnp}")
        LogHelper.log_step(self, "Generate a different pnp id bootloader pid from the read pnp id bootloader pid")
        # --------------------------------------------------------------------------------------------------------------
        new_pid = original_pnp.product_id.toLong() ^ 0xFFFF
        new_pnp_id_pid_to_check = HexList.fromLong(new_pid, 2, littleEndian=False)
        new_pnp_id_pid_to_set = HexList.fromLong(new_pid, 2, littleEndian=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"New PNP Id to set: {new_pnp_id_pid_to_set}")
        LogHelper.log_step(self, "jump on application")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restart_in_main_application = False
        DfuTestUtils.force_target_on_application(self, check_required=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1807_index, self.feature_1807, _, _ = ConfigurablePropertiesTestUtils.HIDppHelper.get_parameters(
            test_case=self,
            feature_id=ConfigurableProperties.FEATURE_ID,
            factory=ConfigurablePropertiesFactory)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the pnp id with with HID++ feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self,
                                                                    ConfigurableProperties.PropertyId.BLE_DIS_BL_PID)
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, new_pnp_id_pid_to_set)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "jump on bootloader")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=True)
        self.post_requisite_restart_in_main_application = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get DIS PNP ID characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_pnp_id_pid_read = PnPId.fromHexList(BleProtocolTestUtils.read_characteristics(
            test_case=self, ble_context_device=self.current_ble_device, service_uuid=dis_service,
            characteristic_uuid=pnp_id_char)[0].data).product_id
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's the new pnp id")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=original_pnp.product_id,
                            obtained=new_pnp_id_pid_read,
                            msg="Current pnp id pid in the DIS is still the old one after writing with feature 0x1807")
        self.assertEqual(expected=new_pnp_id_pid_to_check,
                         obtained=new_pnp_id_pid_read,
                         msg="Current pnp id pid in the DIS doesn't match with name set with feature 0x1807")

        self.testCaseChecked("FUN_BLE_GATT_DIS_0006", _AUTHOR)
    # end def test_pnp_id_pid_change_with_1807
# end class GattDeviceInformationServiceBootloaderFunctionalityTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
