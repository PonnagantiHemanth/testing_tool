#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1805.errorhandling
:brief: HID++ 2.0 ``OobState`` error handling test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/03/13
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
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.device.hidpp20.common.feature_1805.oobstate import OobStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateErrorHandlingTestCase(OobStateTestCase):
    """
    Validate ``OobState`` errorhandling test cases
    """

    @features("Feature1805")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1805.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOobState request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1805.set_oob_state_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1805_index)
            report.function_index = function_index

            OobStateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1805_0001", _AUTHOR)
    # end def test_wrong_function_index
# end class OobStateErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
