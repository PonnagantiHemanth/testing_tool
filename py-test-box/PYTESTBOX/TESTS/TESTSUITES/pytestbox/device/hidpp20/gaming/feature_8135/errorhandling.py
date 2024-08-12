#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8135.errorhandling
:brief: HID++ 2.0 ``PedalStatus`` error handling test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.gaming.feature_8135.pedalstatus import PedalStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PedalStatusErrorHandlingTestCase(PedalStatusTestCase):
    """
    Validate ``PedalStatus`` errorhandling test cases
    """

    @features("Feature8135")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_8135.get_max_function_index() + 1)),
                max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPedalStatus request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8135.get_pedal_status_cls(self.deviceIndex, self.feature_8135_index)
            report.functionIndex = function_index

            error_response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate ErrorCode ({ErrorCodes.INVALID_FUNCTION_ID})")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=ErrorCodes.INVALID_FUNCTION_ID,
                             msg="The error_code parameter differs from the one expected")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8135_0001", _AUTHOR)
    # end def test_wrong_function_index
# end class PedalStatusErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
