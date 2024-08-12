#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2250.analysismode
:brief: Validate HID++ 2.0 ``AnalysisMode`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/08/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analysismodeutils import AnalysisModeTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisModeTestCase(DeviceBaseTestCase):
    """
    Validate ``AnalysisMode`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2250 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2250_index, self.feature_2250, self.device_index, _ = \
            AnalysisModeTestUtils.HIDppHelper.get_parameters(self)

        self.compute_cumulative_displacement = AnalysisModeTestUtils.compute_cumulative_displacement
        self.config = self.f.PRODUCT.FEATURES.MOUSE.ANALYSIS_MODE
        self.emulate_continuous_motion = AnalysisModeTestUtils.emulate_continuous_motion
        self.negative_clamped_value = AnalysisMode.MaxClampedValues.NEGATIVE_CLAMPED_VALUE
        self.positive_clamped_value = AnalysisMode.MaxClampedValues.POSITIVE_CLAMPED_VALUE
        self.twos_complement = AnalysisModeTestUtils.twos_complement
        if self.motion_emulator is not None:
            self.delta_signed_max = self.motion_emulator.module.ll_ctrl.reg_map.Limits.DELTA_SIGNED_MAX
            self.delta_signed_min = self.motion_emulator.module.ll_ctrl.reg_map.Limits.DELTA_SIGNED_MIN
        # end if
    # end def setUp

    def set_analysis_mode_on(self):
        """
        Send SetAnalysisMode request with mode set to On
        """
        on = AnalysisMode.MODE.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as ON')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)
    # end def set_analysis_mode_on

    def set_highest_reporting_rate(self):
        """
        Request the highest reporting rate supported by the device to reduce the test duration
        """
        if self.f.PRODUCT.F_IsGaming:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send SetOnboardMode request with onboardMode = host mode")
            # ----------------------------------------------------------------------------------------------------------
            self.set_host_mode()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set the highest report rate supported by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.set_report_rate()
        # end if
    # end def set_highest_reporting_rate

    def set_host_mode(self):
        """
        Set Host mode for DUT using feature 0x8100 or 0x8101 depending on which one is supported by the device
        """
        if self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_Enabled:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetOnboardMode request using feature 0x8100 with mode = Host Mode")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(
                test_case=self, onboard_mode=OnboardProfiles.Mode.HOST_MODE)

        elif self.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_Enabled:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetSetMode request using feature 0x8101 with mode = Host Mode")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.get_set_mode(
                test_case=self, onboard_mode=ProfileManagement.Mode.HOST_MODE,
                set_onboard_mode=ProfileManagementTestUtils.RequestType.SET)
        # end if
    # end def set_host_mode

    def set_report_rate(self):
        """
        Set the highest report rate for DUT using feature 0x8060 or 0x8061 depending on which one is supported by the
        device
        """
        if self.f.PRODUCT.FEATURES.GAMING.REPORT_RATE.F_Enabled:
            highest_report_rate = int(self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRate[0])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get feature 0x8060 index")
            # ----------------------------------------------------------------------------------------------------------
            _, feature_8060, _, _ = ReportRateTestUtils.HIDppHelper.get_parameters(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request using feature 0x8060 "
                                     f"with highest report rate = {highest_report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            response = ReportRateTestUtils.HIDppHelper.set_report_rate(self, highest_report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate no error returned")
            # ----------------------------------------------------------------------------------------------------------
            ReportRateTestUtils.MessageChecker.check_fields(
                test_case=self, message=response,
                expected_cls=feature_8060.set_report_rate_response_cls, check_map={})

        elif self.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE.F_Enabled:
            highest_report_rate = ExtendedAdjustableReportRateTestUtils.get_highest_report_rate(self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get feature 0x8061 index")
            # ----------------------------------------------------------------------------------------------------------
            self.feature_8061_index, self.feature_8061, _, _ = \
                ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_parameters(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request using feature 0x8061 "
                                     f"with highest report rate = {highest_report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(
                test_case=self, report_rate=highest_report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetReportRateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.SetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8061.set_report_rate_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
                test_case=self, check_first_message=False)
        # end if
    # end def set_report_rate
# end class AnalysisModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
