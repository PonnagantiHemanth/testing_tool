#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1807.robustness
:brief: HID++ 2.0 ``ConfigurableProperties`` robustness test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import sample
from random import choice

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.hidpp20.common.feature_1807.configurableproperties import ConfigurablePropertiesTestCase
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class ConfigurablePropertiesRobustnessTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` robustness test cases
    """

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.EQUAD_DEVICE_NAME)
    @level("Robustness")
    @services('Debugger')
    def test_equad_name_longer_than_max_size(self):
        """
        Goal: Check eQuad device name could not be longer than 14 bytes
        If the property’s maximum size is reached, the remaining bytes are meaningless and shall be ignored.
        """
        property_id = ConfigurableProperties.PropertyId.EQUAD_DEVICE_NAME
        test_data = HexList("AA" * ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(self, property_id))
        longer_test_data = HexList(test_data + HexList("55"))

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, longer_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.check_property(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check new chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        final_parser = self.memory_manager.nvs_parser
        ConfigurablePropertiesTestUtils.NvsHelper.check_new_chunks_after_write_data(
            self, initial_parser, final_parser, property_id, test_data)

        self.testCaseChecked("ROB_1807_0001", _AUTHOR)
    # end def test_equad_name_longer_than_max_size

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.HIDPP_DEVICE_NAME)
    @level("Robustness")
    @services('Debugger')
    def test_device_name_longer_than_max_size(self):
        """
        Goal: Check device name could not be longer than maximum size
        If the property’s maximum size is reached, the remaining bytes are meaningless and shall be ignored.
        """
        property_id = ConfigurableProperties.PropertyId.HIDPP_DEVICE_NAME
        test_data = HexList("AA" * ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(self, property_id))
        longer_test_data = HexList(test_data + HexList("55"))

        initial_parser = self._get_initial_parser()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, longer_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.check_property(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check new chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        final_parser = self.memory_manager.nvs_parser
        ConfigurablePropertiesTestUtils.NvsHelper.check_new_chunks_after_write_data(
            self, initial_parser, final_parser, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Device Name with feature 0x0005")
        # --------------------------------------------------------------------------------------------------------------
        device_name = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(self,
                                                                                  device_name_max_count=len(test_data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Device Name matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(ascii_converter(test_data),
                         device_name,
                         "Device Name obtained from feature 0x0005 should match written data")

        self.testCaseChecked("ROB_1807_0002", _AUTHOR)
    # end def test_device_name_longer_than_max_size

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_BL_NAME)
    @level("Robustness")
    @services('Debugger')
    def test_ble_gap_bl_name_longer_than_max_size(self):
        """
        Goal: Check BLE GAP adv. name could not be longer than maximum size
        If the property’s maximum size is reached, the remaining bytes are meaningless and shall be ignored.
        """
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_BL_NAME
        test_data = HexList("AA" * ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(self, property_id))
        longer_test_data = HexList(test_data + HexList("55"))

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, longer_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.check_property(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check new chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        final_parser = self.memory_manager.nvs_parser
        ConfigurablePropertiesTestUtils.NvsHelper.check_new_chunks_after_write_data(
            self, initial_parser, final_parser, property_id, test_data)

        self.testCaseChecked("ROB_1807_0003#1", _AUTHOR)
    # end def test_ble_gap_bl_name_longer_than_max_size

    @features("Feature1807")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
    @level("Robustness")
    @services('Debugger')
    def test_ble_gap_app_name_longer_than_max_size(self):
        """
        Goal: Check BLE GAP adv. name could not be longer than maximum size
        If the property’s maximum size is reached, the remaining bytes are meaningless and shall be ignored.
        """
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME
        test_data = HexList("AA" * ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(self, property_id))
        longer_test_data = HexList(test_data + HexList("55"))

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, longer_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.check_property(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check new chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        final_parser = self.memory_manager.nvs_parser
        ConfigurablePropertiesTestUtils.NvsHelper.check_new_chunks_after_write_data(
            self, initial_parser, final_parser, property_id, test_data)

        self.testCaseChecked("ROB_1807_0003#2", _AUTHOR)
    # end def test_ble_gap_app_name_longer_than_max_size

    @features("Feature1807")
    @level("Robustness")
    def test_get_property_info_software_id(self):
        """
        Validate ``GetPropertyInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.0xPP.0xPP

        SwID boundary values [0..F]
        """
        property_id = ConfigurableProperties.PropertyId.MIN
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ConfigurableProperties.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPropertyInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.get_property_info(
                test_case=self,
                property_id=property_id,
                software_id=software_id
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPropertyInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurablePropertiesTestUtils.GetPropertyInfoResponseChecker
            check_map = checker.get_check_map_by_property(test_case=self, property_id=property_id)
            checker.check_fields(
                self, response, self.feature_1807.get_property_info_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0005#1", _AUTHOR)
    # end def test_get_property_info_software_id

    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_select_property_software_id(self):
        """
        Validate ``SelectProperty`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.Offset

        SwID boundary values [0..F]
        """
        property_id, _ = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ConfigurableProperties.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectProperty request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
                test_case=self,
                property_id=property_id,
                software_id=software_id
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SelectPropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1807.select_property_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0005#2", _AUTHOR)
    # end def test_select_property_software_id

    @features("Feature1807")
    @level("Robustness")
    def test_read_property_software_id(self):
        """
        Validate ``ReadProperty`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first present property")
        # --------------------------------------------------------------------------------------------------------------
        property_id = ConfigurablePropertiesTestUtils.HIDppHelper.get_first_property_present(
            test_case=self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ConfigurableProperties.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Select first supported property with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadProperty request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(
                test_case=self,
                software_id=software_id
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadPropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
            check_map = checker.get_default_check_map(self)
            # Skip check of field data
            check_map["data"] = None

            checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0005#3", _AUTHOR)
    # end def test_read_property_software_id

    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_write_property_software_id(self):
        """
        Validate ``WriteProperty`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Data

        SwID boundary values [0..F]
        """
        property_id, _ = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(self)
        data = 0xAA

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        for software_id in compute_inf_values(ConfigurableProperties.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Select first supported property")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteProperty request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.write_property(
                test_case=self,
                data=data,
                software_id=software_id
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WritePropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1807.write_property_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0005#4", _AUTHOR)
    # end def test_write_property_software_id

    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_delete_property_software_id(self):
        """
        Validate ``DeleteProperty`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.0xPP.0xPP

        SwID boundary values [0..F]
        """
        property_id, _ = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        for software_id in compute_inf_values(ConfigurableProperties.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send DeleteProperty request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.delete_property(
                test_case=self,
                property_id=property_id,
                software_id=software_id
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check DeletePropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1807.delete_property_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0005#5", _AUTHOR)
    # end def test_delete_property_software_id

    @features("Feature1807")
    @level("Robustness")
    def test_get_property_info_padding(self):
        """
        Validate ``GetPropertyInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        property_id = ConfigurableProperties.PropertyId.MIN
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1807.get_property_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPropertyInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.get_property_info(
                test_case=self,
                property_id=property_id,
                padding=padding
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPropertyInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurablePropertiesTestUtils.GetPropertyInfoResponseChecker
            check_map = checker.get_check_map_by_property(test_case=self, property_id=property_id)
            checker.check_fields(self, response, self.feature_1807.get_property_info_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0006#1", _AUTHOR)
    # end def test_get_property_info_padding

    @features("Feature1807")
    @level("Robustness")
    def test_read_property_padding(self):
        """
        Validate ``ReadProperty`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first present property")
        # --------------------------------------------------------------------------------------------------------------
        property_id = ConfigurablePropertiesTestUtils.HIDppHelper.get_first_property_present(
            test_case=self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1807.read_property_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Select first supported property")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadProperty request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(
                test_case=self,
                padding=padding
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadPropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
            check_map = checker.get_default_check_map(self)
            # Skip check of field data
            check_map["data"] = None
            checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0006#2", _AUTHOR)
    # end def test_read_property_padding

    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_delete_property_padding(self):
        """
        Validate ``DeleteProperty`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        property_id, _ = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        request_cls = self.feature_1807.delete_property_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send DeleteProperty request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.delete_property(
                test_case=self,
                property_id=property_id,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check DeletePropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1807.delete_property_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1807_0006#3", _AUTHOR)
    # end def test_delete_property_padding

    def _perform_nvs_chunk_stress_test(self, loop_count=10, property_count=8, deletion=False):
        """
        Perform steps for NVS chunk stress test:
            - loop for the specific count
            -   choose candidates randomly from the supported properties
            -   loop candidates
            -       write random data for a candidate
            -       read data for the candidate
            -       check data consistency
            -   delete one of candidates if requested
            cf Lexend NVS chunk test document:
            https://docs.google.com/document/d/1OAYjV3o4SiR0R2470QTP3qHTmsZmoX2AXUQdbkc8KEM/view

        :param loop_count: the number of loops executed during the stess test - OPTIONAL
        :type loop_count: ``int``
        :param property_count: the number of properties selected for the test - OPTIONAL
        :type property_count: ``int``
        :param deletion: Flag indicating to delete the chunk - OPTIONAL
        :type deletion: ``bool``
        """
        supported_properties = self.config_manager.get_feature(ConfigurationManager.ID.SUPPORTED_PROPERTIES)
        num_properties = len(supported_properties)

        self.post_requisite_reload_nvs = True

        for _ in range(0, loop_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Randomly select properties from supported list")
            # ----------------------------------------------------------------------------------------------------------
            candidates = sample(supported_properties, min(property_count, num_properties))

            for property_id in candidates:
                test_data = RandHexList(ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(self, property_id))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Select property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Write property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, test_data)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Re-Select property {repr(property_id)} at offset 0")
                # ------------------------------------------------------------------------------------------------------
                ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Read property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                read_data = ConfigurablePropertiesTestUtils.HIDppHelper.read_data(self, data_size=len(test_data))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check property {repr(property_id)} data")
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(test_data, read_data, "Read data should match the written data")
            # end for

            if deletion:
                ConfigurablePropertiesTestUtils.HIDppHelper.delete_property(self, choice(candidates))
            # end if
        # end for
    # end def _perform_nvs_chunk_stress_test

    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_data_consistency_for_properties_writing_and_reading(self):
        """
        Goal: Check the data consistency for the properties writing and reading
        """
        self._perform_nvs_chunk_stress_test(deletion=False)
        self.testCaseChecked("ROB_1807_0007", _AUTHOR)
    # end def test_data_consistency_for_properties_writing_and_reading

    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_data_consistency_for_properties_writing_reading_and_deletion(self):
        """
        Goal: Check the data consistency for the properties writing and reading
        """
        self._perform_nvs_chunk_stress_test(deletion=True)
        self.testCaseChecked("ROB_1807_0008", _AUTHOR)
    # end def test_data_consistency_for_properties_writing_reading_and_deletion
# end class ConfigurablePropertiesRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
