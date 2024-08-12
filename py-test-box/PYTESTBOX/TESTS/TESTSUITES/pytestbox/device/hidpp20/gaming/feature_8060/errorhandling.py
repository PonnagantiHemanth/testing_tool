#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8060.errorhandling
:brief: HID++ 2.0 ``ReportRate`` error handling test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/08/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils
from pytestbox.device.hidpp20.gaming.feature_8060.reportrate import ReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReportRateErrorHandlingTestCase(ReportRateTestCase):
    """
    Validate ``ReportRate`` errorhandling test cases
    """

    @features("Feature8060")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8060.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetReportRateList request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_request = self.feature_8060.get_report_rate_list_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8060_index)
            get_report_rate_request.functionIndex = function_index

            ReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=get_report_rate_request,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8060_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature8060")
    @features("Feature8100")
    @level("ErrorHandling")
    def test_set_unsupported_report_rate(self):
        """
        Validate ``SetReportRate`` with unsupported report rate
        """
        self.post_requisite_reload_nvs = True
        host_mode = OnboardProfiles.Mode.HOST_MODE
        onboard_mode = OnboardProfiles.Mode.ONBOARD_MODE
        unsupported_report_rate_list = [report_rate for report_rate in [1, 2, 3, 4, 5, 6, 7, 8]
                                        if report_rate not in ReportRateTestUtils.get_default_report_rate_list(self)]

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
        LogHelper.log_info(self, "Test Loop over reportRate in unsupported report rate list")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in unsupported_report_rate_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate={report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            set_report_rate_request = self.feature_8060.set_report_rate_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8060_index,
                report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the InvalidArgument(2) error returned")
            # ----------------------------------------------------------------------------------------------------------
            ReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=set_report_rate_request,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode}")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=self, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        self.testCaseChecked("ERR_8060_0002", _AUTHOR)
    # end def test_set_unsupported_report_rate

    @features("Feature8060")
    @features("Feature8100")
    @level("ErrorHandling")
    def test_set_invalid_report_rate(self):
        """
        Validate ``SetReportRate`` with invalid report rate
        """
        self.post_requisite_reload_nvs = True
        host_mode = OnboardProfiles.Mode.HOST_MODE
        onboard_mode = OnboardProfiles.Mode.ONBOARD_MODE
        all_report_rate_list = [1, 2, 3, 4, 5, 6, 7, 8]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8100 index")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_8100, _, _ = OnboardProfilesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {host_mode}")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=host_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no error returned")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=self, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over reportRate in invalid range (several interesting values)")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in compute_wrong_range(value=list(all_report_rate_list), max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate={report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            set_report_rate_request = self.feature_8060.set_report_rate_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8060_index,
                report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the InvalidArgument(2) error returned")
            # ----------------------------------------------------------------------------------------------------------
            ReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=set_report_rate_request,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode}")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=self, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        self.testCaseChecked("ERR_8060_0003", _AUTHOR)
    # end def test_set_invalid_report_rate

    @features("Feature8060")
    @level("ErrorHandling")
    def test_set_report_rate_in_onboard_mode(self):
        """
        Validate ``SetReportRate`` while in onboard mode
        """
        report_rate = int(self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRate[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetReportRate request with reportRate={report_rate}")
        # --------------------------------------------------------------------------------------------------------------
        set_report_rate_request = self.feature_8060.set_report_rate_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8060_index,
            report_rate=report_rate)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the InvalidArgument(2) error returned")
        # --------------------------------------------------------------------------------------------------------------
        ReportRateTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=set_report_rate_request,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_8060_0004", _AUTHOR)
    # end def test_set_report_rate_in_onboard_mode
# end class ReportRateErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
