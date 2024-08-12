#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8100.errorhandling
:brief: HID++ 2.0 ``OnboardProfiles`` error handling test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/01/04
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
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8100.onboardprofiles import OnboardProfilesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OnboardProfilesErrorHandlingTestCase(OnboardProfilesTestCase):
    """
    Validate ``OnboardProfiles`` error handling test cases
    """

    @features("Feature8100")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over functionIndex invalid range (typical wrong values)")
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_8100.get_max_function_index() + 1)),
                max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetOnboardProfilesInfo request with a "
                                     f"wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8100.get_onboard_profiles_info_cls(
                ChannelUtils.get_device_index(test_case=self), self.feature_8100_index)
            report.functionIndex = function_index
            OnboardProfilesTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8100_0001", _AUTHOR)
    # end def test_wrong_function_index
# end class OnboardProfilesErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
