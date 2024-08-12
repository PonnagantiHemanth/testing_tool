#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b10.interface
:brief: HID++ 2.0 ``ControlList`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.hidpp20.common.feature_1b10.controllist import ControlListTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ControlListInterfaceTestCase(ControlListTestCase):
    """
    Validate ``ControlList`` interface test cases
    """

    @features("Feature1B10")
    @level("Interface")
    def test_get_count_api(self):
        """
        Validate ``GetCount`` normal processing

        [0] getCount() -> count
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCount request")
        # --------------------------------------------------------------------------------------------------------------
        response = ControlListTestUtils.HIDppHelper.get_count(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCountResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ControlListTestUtils.GetCountResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b10_index))
        })
        checker.check_fields(self, response, self.feature_1b10.get_count_response_cls, check_map)

        self.testCaseChecked("INT_1B10_0001", _AUTHOR)
    # end def test_get_count_api

    @features("Feature1B10")
    @level("Interface")
    def test_get_control_list_api(self):
        """
        Validate ``GetControlList`` normal processing

        [1] getControlList(offset) -> cid0, cid1, cid2, cid3, cid4, cid5, cid6, cid7
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetControlList request")
        # --------------------------------------------------------------------------------------------------------------
        response = ControlListTestUtils.HIDppHelper.get_control_list(
            test_case=self,
            offset=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetControlListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ControlListTestUtils.GetControlListResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b10_index)),
        })
        checker.check_fields(self, response, self.feature_1b10.get_control_list_response_cls, check_map)

        self.testCaseChecked("INT_1B10_0002", _AUTHOR)
    # end def test_get_control_list_api
# end class ControlListInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
