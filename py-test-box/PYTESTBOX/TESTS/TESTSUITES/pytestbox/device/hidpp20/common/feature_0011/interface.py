#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0011.interface
:brief: HID++ 2.0 ``PropertyAccess`` interface test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.propertyaccess import PropertyAccess
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.propertyaccessutils import PropertyAccessTestUtils
from pytestbox.device.hidpp20.common.feature_0011.propertyaccess import PropertyAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Kevin Dayet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class PropertyAccessInterfaceTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` interface test cases
    """

    @features("Feature0011")
    @level("Interface")
    def test_get_property_info(self):
        """
        Validate ``GetPropertyInfo`` normal processing

        [0] getPropertyInfo(propertyId) -> flags, size
        """
        property_id = PropertyAccess.PropertyId.MIN
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetPropertyInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.get_property_info(
            test_case=self,
            property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPropertyInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.GetPropertyInfoResponseChecker
        check_map = checker.get_check_map_by_property(self, property_id=property_id)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0011_index))
        })
        checker.check_fields(self, response, self.feature_0011.get_property_info_response_cls, check_map)

        self.testCaseChecked("INT_0011_0001", _AUTHOR)
    # end def test_get_property_info

    @features("Feature0011")
    @level("Interface")
    def test_select_property(self):
        """
        Validate ``SelectProperty`` normal processing

        [1] selectProperty(propertyId, rdOffset) -> None
        """
        property_id, _ = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SelectProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.select_property(
            test_case=self,
            property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0011_index))
        }
        checker.check_fields(self, response, self.feature_0011.select_property_response_cls, check_map)

        self.testCaseChecked("INT_0011_0002", _AUTHOR)
    # end def test_select_property

    @features("Feature0011")
    @level("Interface")
    def test_read_property(self):
        """
        Validate ``ReadProperty`` normal processing

        [2] readProperty() -> data
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first present property")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(
            self, write_data_if_none=0xAA)
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.read_property(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        # Skip check of field data
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0011_index)),
            "data": None
        })
        checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map)

        self.testCaseChecked("INT_0011_0003", _AUTHOR)
    # end def test_read_property
# end class PropertyAccessInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
