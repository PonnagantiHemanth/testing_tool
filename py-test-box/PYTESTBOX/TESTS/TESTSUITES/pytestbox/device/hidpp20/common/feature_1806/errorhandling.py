#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1806.errorhandling
:brief: HID++ 2.0 ConfigurableDeviceProperties errorhandling test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/04/28
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_1806.configurabledeviceproperties import \
    ConfigurableDevicePropertiesTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"
LogHelper = CommonBaseTestUtils.LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurableDevicePropertiesErrorHandlingTestCase(ConfigurableDevicePropertiesTestCase):
    """
    Validates ConfigurableDeviceProperties error handling test cases
    """
    @features("Feature1806")
    @level("ErrorHandling")
    def test_set_device_name_commit_wrong_length(self):
        """
        Validates SetDeviceNameCommit with wrong length
        """
        self.post_requisite_reload_nvs = True
        Utils.SetDeviceNameHelper.HIDppHelper.write(self, char_index=0, device_name="TEST_NAME_1806")
        Utils.SetDeviceNameCommitHelper.HIDppHelper.write_with_wrong_length(self, length=0)
        self.testCaseChecked("ERR_1806_0001", _AUTHOR)
    # end def test_set_device_name_commit_wrong_length

    @features("Feature1806")
    @level("ErrorHandling")
    def test_set_device_properties_api_invalid_property_id(self):
        """
        Validates SetDeviceProperties invalid property id
        """
        self.post_requisite_reload_nvs = True
        for invalid_property_id in [0, self.feature_1806.property_id.get_max_id() + 1]:
            Utils.SetDevicePropertiesHelper.HIDppHelper.write_with_invalid_argument(
                    self,
                    property_id=invalid_property_id,
                    flag=0,
                    sub_data_index=0,
                    property_data=1)
        # end for
        self.testCaseChecked("ERR_1806_0002", _AUTHOR)
    # end def test_set_device_properties_api_invalid_property_id

    @features("Feature1806")
    @level("ErrorHandling")
    def test_get_device_properties_invalid_property_id(self):
        """
        Validates GetDeviceProperties invalid property id
        """
        for invalid_property_id in [0, self.feature_1806.property_id.get_max_id() + 1]:
            Utils.GetDevicePropertiesHelper.HIDppHelper.read_with_invalid_argument(
                    self,
                    property_id=invalid_property_id,
                    flag=0,
                    sub_data_index=0)
        # end for
        self.testCaseChecked("ERR_1806_0003", _AUTHOR)
    # end def test_get_device_properties_invalid_property_id

    @features("Feature1806")
    @level("ErrorHandling")
    def test_set_device_properties_api_invalid_sub_data_index(self):
        """
        Validates SetDeviceProperties invalid sub data index
        """
        self.post_requisite_reload_nvs = True
        property_id_list = self.feature_1806.property_id.get_all_ids()
        property_size_list = self.feature_1806.property_size.get_all_sizes()
        for index in range(len(property_id_list)):
            pid = property_id_list[index]
            size = property_size_list[index]
            if size < 14:
                continue
            # end if
            Utils.SetDevicePropertiesHelper.HIDppHelper.write_with_invalid_argument(
                    self,
                    property_id=pid,
                    flag=1,
                    sub_data_index=size,
                    property_data=0)
        # end for
        self.testCaseChecked("ERR_1806_0004", _AUTHOR)
    # end def test_set_device_properties_api_invalid_sub_data_index

    @features("Feature1806")
    @level("ErrorHandling")
    def test_get_device_properties_invalid_sub_data_index(self):
        """
        Validates GetDeviceProperties invalid sub data index
        """
        property_id_list = self.feature_1806.property_id.get_all_ids()
        property_size_list = self.feature_1806.property_size.get_all_sizes()
        for index in range(len(property_id_list)):
            Utils.GetDevicePropertiesHelper.HIDppHelper.read_with_invalid_argument(
                    self,
                    property_id=property_id_list[index],
                    flag=1,
                    sub_data_index=property_size_list[index])
        # end for
        self.testCaseChecked("ERR_1806_0005", _AUTHOR)
    # end def test_get_device_properties_invalid_sub_data_index

    @features("Feature1806")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validates function index
        """
        wrong_index = self.feature_1806.get_max_function_index() + 1
        # ------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetDeviceNameMaxCount request with function index: {wrong_index}")
        # ------------------------------------------------------------------------------------------------
        report = self.feature_1806.get_device_name_max_count_cls(self.deviceIndex, self.feature_1806_index)
        report.functionIndex = wrong_index
        error_response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)
        # ---------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate error code: {ErrorCodes.INVALID_FUNCTION_ID}")
        # ---------------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                         expected=ErrorCodes.INVALID_FUNCTION_ID,
                         msg="The error_code parameter differs from the one expected")
        self.testCaseChecked("ERR_1806_0006", _AUTHOR)
    # end def test_wrong_function_index
# end class ConfigurableDevicePropertiesErrorHandlingTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
