#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8060.business
:brief: HID++ 2.0 ``ReportRate`` business test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/08/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils
from pytestbox.device.hidpp20.gaming.feature_8060.reportrate import ReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReportRateBusinessTestCase(ReportRateTestCase):
    """
    Validate ``ReportRate`` business test cases
    """

    @features("Feature8060")
    @features("Feature8100")
    @level('Business', 'SmokeTests')
    def test_set_report_rate(self):
        """
        Validate ``SetReportRate`` business test case
        """
        self.post_requisite_reload_nvs = True
        host_mode = OnboardProfiles.Mode.HOST_MODE
        onboard_mode = OnboardProfiles.Mode.ONBOARD_MODE

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8100 index")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_8100, _, _ = OnboardProfilesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {host_mode} (host mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=host_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no error returned")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=self, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over reportRate in reportRateList ")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in ReportRateTestUtils.get_default_report_rate_list(self):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            response = ReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate no error returned")
            # ----------------------------------------------------------------------------------------------------------
            ReportRateTestUtils.MessageChecker.check_fields(
                test_case=self, message=response,
                expected_cls=self.feature_8060.set_report_rate_response_cls, check_map={})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            response = ReportRateTestUtils.HIDppHelper.get_report_rate(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate GetReportRate.reportRate shall be equal to {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ReportRateTestUtils.GetReportRateResponseChecker.check_report_rate(
                test_case=self, response=response, expected=report_rate)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self,
                                     f"Send SetOnboardMode request with onboardMode = {onboard_mode} (onboard mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=self, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        self.testCaseChecked("BUS_8060_0001", _AUTHOR)
    # end def test_set_report_rate
# end class ReportRateBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
