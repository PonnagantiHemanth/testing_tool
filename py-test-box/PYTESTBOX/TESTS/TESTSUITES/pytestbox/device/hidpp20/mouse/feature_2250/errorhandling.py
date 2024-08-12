#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2250.errorhandling
:brief: HID++ 2.0 ``AnalysisMode`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/08/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analysismodeutils import AnalysisModeTestUtils
from pytestbox.device.hidpp20.mouse.feature_2250.analysismode import AnalysisModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisModeErrorHandlingTestCase(AnalysisModeTestCase):
    """
    Validate ``AnalysisMode`` errorhandling test cases
    """

    @features("Feature2250")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_2250.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAnalysisMode request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            AnalysisModeTestUtils.HIDppHelper.get_analysis_mode_and_check_error(
                test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID], function_index=function_index)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_2250_0001")
    # end def test_wrong_function_index

    @features('Feature2250')
    @level('ErrorHandling')
    def test_wrong_mode(self):
        """
        Validate SetAnalysisMode mode error range

        Check boundary values (2 and 0xFF) plus all bits in the byte [0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with a chosen list of wrong mode value')
        # --------------------------------------------------------------------------------------------------------------
        for wrong_mode in compute_wrong_range([AnalysisMode.MODE.ON, AnalysisMode.MODE.OFF], max_value=0xFF):
            AnalysisModeTestUtils.HIDppHelper.set_analysis_mode_and_check_error(
                test_case=self, mode=wrong_mode, error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for
        self.testCaseChecked("ERR_2250_0002")
    # end def test_wrong_mode
# end class AnalysisModeErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
