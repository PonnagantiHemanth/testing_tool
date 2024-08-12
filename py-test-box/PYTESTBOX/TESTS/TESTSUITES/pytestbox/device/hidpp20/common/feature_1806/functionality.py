#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1806.functionality
:brief: HID++ 2.0 ConfigurableDeviceProperties functionality test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/04/28
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from string import ascii_uppercase
from string import digits
from random import choices

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_1806.configurabledeviceproperties import \
    ConfigurableDevicePropertiesTestCase
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurableDevicePropertiesFunctionalityTestCase(ConfigurableDevicePropertiesTestCase):
    """
    Validates ConfigurableDeviceProperties functionality test cases
    """
    @features("Feature1806")
    @features("Feature1802")
    @level("Functionality")
    def test_set_device_name_api_reset_verify(self):
        """
        Validates SetDeviceName
        """
        self.post_requisite_reload_nvs = True
        name_chunk = "Testing"
        Utils.SetDeviceNameHelper.HIDppHelper.write(self, char_index=0, device_name=name_chunk)
        Utils.HIDppHelper.force_device_reset_and_activate_features(self)
        output_value = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
                self, device_name_max_count=len(name_chunk))
        self.assertNotEqual(unexpected=name_chunk,
                            obtained=output_value,
                            msg="The unexpected device_name is same as obtained")
        self.testCaseChecked("FUN_1806_0001", _AUTHOR)
    # end def test_set_device_name_api_reset_verify

    @features("Feature1806")
    @level("Functionality")
    def test_supported_property_ids(self):
        """
        Validate Supported Property Ids
        """
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.validate_supported_property_ids(self)
        self.testCaseChecked("FUN_1806_0002_TO_FUN_1806_0013", _AUTHOR)
    # end def test_supported_property_ids

    @features("Feature1806")
    @features("Feature1802")
    @level("Functionality")
    def test_supported_property_ids_after_reset_by_feature(self):
        """
        Validate Supported Property Ids
        """
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.validate_supported_property_ids(self, device_reset="byFeature")
        self.testCaseChecked("FUN_1806_0014_TO_FUN_1806_0027", _AUTHOR)
    # end def test_supported_property_ids_after_reset_by_feature

    @features("Feature1806")
    @level("Functionality")
    @services("PowerSupply")
    def test_supported_property_ids_after_reset_by_power_supply(self):
        """
        Validate Supported Property Ids
        """
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.validate_supported_property_ids(self, device_reset="byPowerSupply")
        self.testCaseChecked("FUN_1806_0028_TO_FUN_1806_0041", _AUTHOR)
    # end def test_supported_property_ids_after_reset_by_power_supply

    @features("Feature1806")
    @features("Feature1802")
    @features("Feature0005")
    @level("Functionality")
    def test_set_device_name_max_count_validation(self):
        """
        Validates SetDeviceProperties value
        """
        self.set_feature_1802()
        self.post_requisite_reload_nvs = True

        response = Utils.GetDeviceNameMaxCountHelper.HIDppHelper.read(self)
        device_name_max_count = int(Numeral(response.device_name_max_count))
        # generating a random string matching the device name max count
        name_chunk = ''.join(choices(ascii_uppercase + digits, k=device_name_max_count))
        for index in range(device_name_max_count // 15 + 1):
            Utils.SetDeviceNameHelper.HIDppHelper.write(
                self, char_index=index * 0x0F, device_name=name_chunk[index * 0x0F:(index+1) * 0x0F])
        # end for
        Utils.SetDeviceNameCommitHelper.HIDppHelper.write(self, length=len(name_chunk))
        output_value_before = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
                self, device_name_max_count=device_name_max_count)

        # generating a random string greater than the device name max count
        second_name_chunk = ''.join(choices(ascii_uppercase + digits, k=device_name_max_count+1))
        Utils.SetDeviceNameHelper.HIDppHelper.write(
            self, char_index=device_name_max_count, device_name=second_name_chunk[device_name_max_count:])
        Utils.SetDeviceNameCommitHelper.HIDppHelper.write(self, length=len(second_name_chunk))
        output_value_after = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
                self, device_name_max_count=device_name_max_count)
        self.assertEqual(expected=output_value_before,
                         obtained=output_value_after,
                         msg="The name set is not as expected")
        self.testCaseChecked("FUN_1806_0042", _AUTHOR)
    # end def test_set_device_name_max_count_validation

    @features("Feature1806")
    @features("Feature0005")
    @level("Functionality")
    def test_set_device_name_greater_than_max_count_validation(self):
        """
        Validates DeviceName value
        """
        self.post_requisite_reload_nvs = True
        response = Utils.GetDeviceNameMaxCountHelper.HIDppHelper.read(self)
        max_count = int(Numeral(response.device_name_max_count))
        # 15 bytes to write + 1 byte char_index
        size = 15
        name_chunks = ["This is line 01", "This is line 02", "This is line 03", "This is line 04", "This is line 05"]
        offset_list = [0 * size, 1 * size, 2 * size, 3 * size, 4 * size]
        # -----------------------------------------------------------------------
        LogHelper.log_check(self, "issuing SetDeviceName to write 75 characters")
        # -----------------------------------------------------------------------
        given_name = ""
        for index in range(len(offset_list)):
            given_name = f"{given_name}{name_chunks[index]}"
            Utils.SetDeviceNameHelper.HIDppHelper.write(self,
                                                        char_index=offset_list[index],
                                                        device_name=name_chunks[index])
        # end for

        Utils.SetDeviceNameCommitHelper.HIDppHelper.write(self, length=max_count)

        full_name = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(self, max_count)

        self.assertEqual(expected=given_name[0:max_count],
                         obtained=full_name,
                         msg="The name set is not as expected")
        self.testCaseChecked("FUN_1806_0043", _AUTHOR)
    # end def test_set_device_name_greater_than_max_count_validation

    @features("Feature1806")
    @level("Functionality")
    def test_set_device_properties_invalid_sub_data_index(self):
        """
        Validates SetDeviceProperties/GetDeviceProperties value
        """
        self.post_requisite_reload_nvs = True
        property_id = 1
        flag = 0
        invalid_sub_data_index = 1
        property_data = RandHexList(1)
        Utils.SetDevicePropertiesHelper.HIDppHelper.write(
                self,
                property_id=property_id,
                flag=flag,
                sub_data_index=invalid_sub_data_index,
                property_data=property_data)

        response = Utils.GetDevicePropertiesHelper.HIDppHelper.read(
                self,
                property_id=property_id,
                flag=flag,
                sub_data_index=invalid_sub_data_index)

        # reading invalid sub_data_index should return a successful response but without any data fields.
        # ------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate GetDeviceProperties.property_data == {property_data}')
        # ------------------------------------------------------------------------------------------------
        self.assertEqual(expected=property_data,
                         obtained=response.property_data,
                         msg="The property_data should be empty")
        self.testCaseChecked("FUN_1806_0044", _AUTHOR)
    # end def test_set_device_properties_invalid_sub_data_index

    @features("Feature1806")
    @level("Functionality")
    def test_get_device_properties_invalid_sub_data_index(self):
        """
        Validates SetDeviceProperties/GetDeviceProperties value
        """
        self.post_requisite_reload_nvs = True
        property_id = 1
        flag = 0
        valid_sub_data_index = 0
        invalid_sub_data_index = 1
        property_data = RandHexList(1)
        Utils.SetDevicePropertiesHelper.HIDppHelper.write(
                self,
                property_id=property_id,
                flag=flag,
                sub_data_index=valid_sub_data_index,
                property_data=property_data)

        response = Utils.GetDevicePropertiesHelper.HIDppHelper.read(
                self,
                property_id=property_id,
                flag=flag,
                sub_data_index=invalid_sub_data_index)

        # reading invalid sub_data_index should return a successful response but without any data fields.
        # ------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate GetDeviceProperties.property_data == {property_data}')
        # ------------------------------------------------------------------------------------------------
        self.assertEqual(expected=property_data,
                         obtained=response.property_data,
                         msg="The property_data should be empty")
        self.testCaseChecked("FUN_1806_0045", _AUTHOR)
    # end def test_get_device_properties_invalid_sub_data_index

    @features("Feature1806")
    @features("Feature1802")
    @level("Functionality")
    def test_set_device_extended_model_id_reset_verify(self):
        """
        Validates SetDeviceName value
        """
        self.post_requisite_reload_nvs = True
        input_value = 3
        Utils.SetDeviceExtendModelIDHelper.HIDppHelper.write(self, extended_model_id=input_value)
        Utils.HIDppHelper.force_device_reset_and_activate_features(self)
        # -----------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceInfo request")
        # -----------------------------------------------------------------------------
        output_value = DeviceInformationTestUtils.HIDppHelper.get_extended_model_id(self)
        self.assertEqual(expected=HexList(input_value),
                         obtained=output_value,
                         msg="The extended model id obtained is not as expected")
        self.testCaseChecked("FUN_1806_0046", _AUTHOR)
    # end def test_set_device_extended_model_id_reset_verify

    @features("Feature1806")
    @features("Feature1802")
    @features("Feature0005")
    @level("Functionality")
    def test_set_device_name_and_commit_and_reset_verify(self):
        """
        Validates SetDeviceName value
        """
        self.post_requisite_reload_nvs = True
        name_chunk = "Testing"
        Utils.SetDeviceNameHelper.HIDppHelper.write(self, char_index=0, device_name=name_chunk)
        Utils.SetDeviceNameCommitHelper.HIDppHelper.write(self, length=len(name_chunk))
        Utils.HIDppHelper.force_device_reset_and_activate_features(self)
        output_value = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
                self, device_name_max_count=len(name_chunk))
        self.assertEqual(expected=name_chunk,
                         obtained=output_value,
                         msg="The name set is not as expected")
        self.testCaseChecked("FUN_1806_0047", _AUTHOR)
    # end def test_set_device_name_and_commit_and_reset_verify
# end class ConfigurableDevicePropertiesFunctionalityTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
