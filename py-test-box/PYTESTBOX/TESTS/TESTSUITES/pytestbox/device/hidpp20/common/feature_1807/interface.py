#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1807.interface
:brief: HID++ 2.0 ``ConfigurableProperties`` interface test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.hidpp20.common.feature_1807.configurableproperties import ConfigurablePropertiesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ConfigurablePropertiesInterfaceTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` interface test cases
    """

    @features("Feature1807")
    @level("Interface")
    def test_get_property_info(self):
        """
        Validate ``GetPropertyInfo`` normal processing

        [0] getPropertyInfo(propertyId) -> flags, size
        """
        property_id = ConfigurableProperties.PropertyId.MIN

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetPropertyInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.get_property_info(
            test_case=self,
            property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPropertyInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.GetPropertyInfoResponseChecker
        check_map = checker.get_check_map_by_property(test_case=self, property_id=property_id)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1807_index))
        })
        checker.check_fields(self, response, self.feature_1807.get_property_info_response_cls, check_map)

        self.testCaseChecked("INT_1807_0001", _AUTHOR)
    # end def test_get_property_info

    @features("Feature1807")
    @level("Interface")
    def test_select_property(self):
        """
        Validate ``SelectProperty`` normal processing

        [1] selectProperty(propertyId, rdOffset, wrOffset) -> None
        """
        property_id, _ = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SelectProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
            test_case=self,
            property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1807_index))
        }
        checker.check_fields(self, response, self.feature_1807.select_property_response_cls, check_map)

        self.testCaseChecked("INT_1807_0002", _AUTHOR)
    # end def test_select_property

    @features("Feature1807")
    @level("Interface")
    def test_read_property(self):
        """
        Validate ``ReadProperty`` normal processing

        [2] readProperty() -> data
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first present property")
        # --------------------------------------------------------------------------------------------------------------
        property_id = ConfigurablePropertiesTestUtils.HIDppHelper.get_first_property_present(
            self, write_data_if_none=0xAA)
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        # Skip check of field data
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1807_index)),
            "data": None
        })
        checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map)

        self.testCaseChecked("INT_1807_0003", _AUTHOR)
    # end def test_read_property

    @features("Feature1807")
    @level("Interface")
    @services('Debugger')
    def test_write_property(self):
        """
        Validate ``WriteProperty`` normal processing

        [3] writeProperty(data) -> None
        """
        self.post_requisite_reload_nvs = True
        data = 0xAA

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first supported property")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(self)
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.write_property(
            test_case=self,
            data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WritePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1807_index))
        }
        checker.check_fields(self, response, self.feature_1807.write_property_response_cls, check_map)

        self.testCaseChecked("INT_1807_0004", _AUTHOR)
    # end def test_write_property

    @features("Feature1807")
    @level("Interface")
    @services('Debugger')
    def test_delete_property(self):
        """
        Validate ``DeleteProperty`` normal processing

        [4] deleteProperty(propertyId) -> None
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first supported property")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.delete_property(
            test_case=self,
            property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DeletePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1807_index))
        }
        checker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map)

        self.testCaseChecked("INT_1807_0005", _AUTHOR)
    # end def test_delete_property
# end class ConfigurablePropertiesInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
