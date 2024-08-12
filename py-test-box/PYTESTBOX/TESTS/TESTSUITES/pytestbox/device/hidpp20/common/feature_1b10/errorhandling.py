#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b10.errorhandling
:brief: HID++ 2.0 ``ControlList`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.hidpp20.common.feature_1b10.controllist import ControlListTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ControlListErrorHandlingTestCase(ControlListTestCase):
    """
    Validate ``ControlList`` errorhandling test cases
    """

    @features("Feature1B10")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1b10.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCount request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1b10.get_count_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1b10_index)
            report.function_index = function_index

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_FUNCTION_ID error code")
            # ----------------------------------------------------------------------------------------------------------
            ControlListTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self, report=report, error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B10_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1B10")
    @level("ErrorHandling")
    def test_get_control_list_with_invalid_offset(self):
        """
        Validate that sending getControlList request with an invalid offset raises an error INVALID_ARGUMENT(0x02)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: invalid_offset in range({self.config.F_Count}, 0xFF + 1)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_offset in range(self.config.F_Count, 0xFF + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getControlList request with offset = {invalid_offset}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1b10.get_control_list_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1b10_index,
                offset=invalid_offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ControlListTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self, report=report, error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B10_0002", _AUTHOR)
    # end def test_get_control_list_with_invalid_offset
# end class ControlListErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
