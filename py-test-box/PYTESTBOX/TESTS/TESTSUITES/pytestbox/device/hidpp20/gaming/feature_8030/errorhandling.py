#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8030.errorhandling
:brief: HID++ 2.0 ``MacroRecordkey`` error handling test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.macrorecordkeyutils import MacroRecordkeyTestUtils
from pytestbox.device.hidpp20.gaming.feature_8030.macrorecordkey import MacroRecordkeyTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyErrorHandlingTestCase(MacroRecordkeyTestCase):
    """
    Validate ``MacroRecordkey`` errorhandling test cases
    """

    @features("Feature8030")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        enabled = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8030.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetLED request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            MacroRecordkeyTestUtils.HIDppHelper.set_led_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                enabled=enabled,
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8030_0001", _AUTHOR)
    # end def test_wrong_function_index
# end class MacroRecordkeyErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
