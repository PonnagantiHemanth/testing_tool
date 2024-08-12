#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1806.interface
:brief: HID++ 2.0 ConfigurableDeviceProperties interface test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/04/28
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import RandHexList
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_1806.configurabledeviceproperties import \
    ConfigurableDevicePropertiesTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurableDevicePropertiesInterfaceTestCase(ConfigurableDevicePropertiesTestCase):
    """
    Validates ConfigurableDeviceProperties interface test cases
    """
    @features("Feature1806")
    @level("Interface")
    def test_get_device_name_max_count_api(self):
        """
        Validates GetDeviceNameMaxCount interface
        """
        Utils.GetDeviceNameMaxCountHelper.HIDppHelper.read(self)
        self.testCaseChecked("INT_1806_0001", _AUTHOR)
    # end def test_get_device_name_max_count_api

    @features("Feature1806")
    @level("Interface")
    def test_set_device_name_api_and_set_device_name_commit_api(self):
        """
        Validates SetDeviceName and SetDeviceNameCommit interfaces
        """
        # These two api are interconnected. Can be tested together for nvs load/reload purpose.
        self.post_requisite_reload_nvs = True
        Utils.SetDeviceNameHelper.HIDppHelper.write(self, char_index=0, device_name="TEST_NAME_1806")
        Utils.SetDeviceNameCommitHelper.HIDppHelper.write(self, length=len("TEST_NAME_1806"))
        self.testCaseChecked("INT_1806_0002_and_INT_1806_0003", _AUTHOR)
    # end def test_set_device_name_api_and_set_device_name_commit_api

    @features("Feature1806")
    @level("Interface")
    def test_set_device_extend_model_id_api(self):
        """
        Validates SetDeviceExtendModelID interface
        """
        self.post_requisite_reload_nvs = True
        Utils.SetDeviceExtendModelIDHelper.HIDppHelper.write(self, extended_model_id=1)
        self.testCaseChecked("INT_1806_0004", _AUTHOR)
    # end def test_set_device_extend_model_id_api

    @features("Feature1806")
    @level("Interface")
    def test_set_and_get_device_properties_api(self):
        """
        Validates SetDeviceProperties interface

        Set/Get can be tested together.
        Otherwise, get will return error if property id is not available.
        """
        self.post_requisite_reload_nvs = True
        Utils.SetDevicePropertiesHelper.HIDppHelper.write(
                self,
                property_id=1,
                flag=0,
                sub_data_index=0,
                property_data=RandHexList(1))
        Utils.GetDevicePropertiesHelper.HIDppHelper.read(
                self,
                property_id=1,
                flag=0,
                sub_data_index=0)
        self.testCaseChecked("INT_1806_0005", _AUTHOR)
        self.testCaseChecked("INT_1806_0006", _AUTHOR)
    # end def test_set_device_properties_api
# end class ConfigurableDevicePropertiesInterfaceTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
