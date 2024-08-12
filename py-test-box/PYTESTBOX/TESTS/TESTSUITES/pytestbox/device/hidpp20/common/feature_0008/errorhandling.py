#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0008.errorhandling
:brief: HID++ 2.0 ``KeepAlive`` error handling test suite
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keepaliveutils import KeepAliveTestUtils
from pytestbox.device.hidpp20.common.feature_0008.keepalive import KeepAliveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "HARISH KUMAR D"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class KeepAliveErrorHandlingTestCase(KeepAliveTestCase):
    """
    Validate ``KeepAlive`` errorhandling test cases
    """

    @features("Feature0008")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_0008.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetTimeoutRange request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestUtils.HIDppHelper.get_timeout_range_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_0008_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature0008")
    @level("ErrorHandling")
    def test_validate_invalid_keep_alive_request(self):
        """
        Validate INVALID ARGUMENT is received when keepAlive is called without of range values
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting values between 1..timeoutMin and"
                                 "timeoutMax..0xFFFF")
        # --------------------------------------------------------------------------------------------------------------
        high_requested_timeouts = KeepAliveTestCase.generate_random_times(
            self, number_of_requested_timeout=10, minimum=self.config.F_TimeoutMax, maximum=0xFFFF)

        low_requested_timeouts = KeepAliveTestCase.generate_random_times(
            self, number_of_requested_timeout=10, minimum=1, maximum=self.config.F_TimeoutMin)

        for timeout in high_requested_timeouts + low_requested_timeouts:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={timeout} and check error code = "
                                     f"INVALID ARGUMENT.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestUtils.HIDppHelper.keep_alive_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                requested_timeout=timeout)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_0008_0002", _AUTHOR)
    # end def test_validate_invalid_keep_alive_request
# end class KeepAliveErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
