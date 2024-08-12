#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b10.business
:brief: HID++ 2.0 ``ControlList`` business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/09/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.controllist import GetControlListResponse
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
class ControlListBusinessTestCase(ControlListTestCase):
    """
    Validate ``ControlList`` business test cases
    """

    @features("Feature1B10")
    @level('Business', 'SmokeTests')
    def test_get_control_list(self):
        """
        Verify the whole CID list is as expected
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over offset in range(0, {self.config.F_Count}, 8)")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range(0, self.config.F_Count, GetControlListResponse.NUM_OF_CID_PER_PACKET):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getControlList request with offset={offset}")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_control_list(
                test_case=self,
                offset=offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getControlList response and check the partial_tag_list is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ControlListTestUtils.GetControlListResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b10.get_control_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1B10_0001", _AUTHOR)
    # end def test_get_control_list

    @features("Feature1B10")
    @level("Business")
    def test_get_control_list_in_order(self):
        """
        Verify the getControlList function with all valid offset parameters
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over offset in range(0, {self.config.F_Count})")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range(0, self.config.F_Count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getControlList request with offset={offset}")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_control_list(
                test_case=self,
                offset=offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getControlList response and check the partial_tag_list is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ControlListTestUtils.GetControlListResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b10.get_control_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1B10_0002", _AUTHOR)
    # end def test_get_control_list_in_order

    @features("Feature1B10")
    @level("Business")
    def test_get_control_list_in_reversed_order(self):
        """
        Verify the getControlList function with all valid offset parameters in reversed order
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over offset in range({self.config.F_Count - 1}, -1, -1)")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range(self.config.F_Count - 1, -1, -1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getControlList request with offset={offset}")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_control_list(
                test_case=self,
                offset=offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getControlList response and check the partial_tag_list is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ControlListTestUtils.GetControlListResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b10.get_control_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1B10_0003", _AUTHOR)
    # end def test_get_control_list_in_reversed_order
# end class ControlListBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
