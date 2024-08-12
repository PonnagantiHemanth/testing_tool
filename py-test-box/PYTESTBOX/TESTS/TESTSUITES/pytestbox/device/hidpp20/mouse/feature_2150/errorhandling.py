#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2150.errorhandling
:brief: HID++ 2.0 ``Thumbwheel`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/14
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
from pytestbox.device.base.thumbwheelutils import ThumbwheelTestUtils
from pytestbox.device.hidpp20.mouse.feature_2150.thumbwheel import ThumbwheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ThumbwheelErrorHandlingTestCase(ThumbwheelTestCase):
    """
    Validate ``Thumbwheel`` errorhandling test cases
    """

    @features("Feature2150")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_2150.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetThumbwheelInfo request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2150.get_thumbwheel_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2150_index)
            report.function_index = function_index

            ThumbwheelTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_2150_0001", _AUTHOR)
    # end def test_wrong_function_index
# end class ThumbwheelErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
