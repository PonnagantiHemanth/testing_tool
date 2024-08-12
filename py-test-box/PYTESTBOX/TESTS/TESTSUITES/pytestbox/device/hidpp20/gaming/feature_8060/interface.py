#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.gaming.feature_8060.interface
:brief: HID++ 2.0 ``ReportRate`` interface test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/08/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils
from pytestbox.device.hidpp20.gaming.feature_8060.reportrate import ReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReportRateInterfaceTestCase(ReportRateTestCase):
    """
    Validate ``ReportRate`` interface test cases
    """

    @features("Feature8060")
    @level("Interface")
    def test_get_report_rate_list(self):
        """
        Validate ``GetReportRateList`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetReportRateList request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8060.get_report_rate_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8060_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8060.get_report_rate_list_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetReportRateListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ReportRateTestUtils.GetReportRateListResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_8060.get_report_rate_list_response_cls, check_map)

        self.testCaseChecked("INT_8060_0001", _AUTHOR)
    # end def test_get_report_rate_list

    @features("Feature8060")
    @level("Interface")
    def test_get_report_rate(self):
        """
        Validate ``GetReportRate`` interface
        """
        report_rate = int(self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRate[0])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetReportRate request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8060.get_report_rate_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8060_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8060.get_report_rate_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetReportRateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ReportRateTestUtils.GetReportRateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "report_rate": (checker.check_report_rate, report_rate),
        })
        checker.check_fields(self, response, self.feature_8060.get_report_rate_response_cls, check_map)

        self.testCaseChecked("INT_8060_0002", _AUTHOR)
    # end def test_get_report_rate

    @features("Feature8060")
    @features("Feature8100")
    @level("Interface")
    def test_set_report_rate(self):
        """
        Validate ``SetReportRate`` interface
        """
        self.post_requisite_reload_nvs = True
        report_rate = int(self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRate[0])
        host_mode = OnboardProfiles.Mode.HOST_MODE

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {host_mode} (Host Mode)")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=host_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetReportRate request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8060.set_report_rate_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8060_index,
            report_rate=report_rate)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8060.set_report_rate_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetReportRateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ReportRateTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex)
        }
        checker.check_fields(self, response, self.feature_8060.set_report_rate_response_cls, check_map)

        self.testCaseChecked("INT_8060_0003", _AUTHOR)
    # end def test_set_report_rate
# end class ReportRateInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
