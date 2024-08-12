#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8061.business
:brief: HID++ 2.0 ``ExtendedAdjustableReportRate`` business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8061.extendedadjustablereportrate import \
    ExtendedAdjustableReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableReportRateBusinessTestCase(ExtendedAdjustableReportRateTestCase):
    """
    Validate ``ExtendedAdjustableReportRate`` business test cases
    """

    @features("Feature8061")
    @features("Feature8100")
    @level('Business', 'SmokeTests')
    def test_report_rate_info_change_event(self):
        """
        Validate that event is sent whenever the report rate is changed by setReportRate request
        """
        onboard_mode = OnboardProfiles.Mode.HOST_MODE
        supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over report_rate in range {supported_report_rate_list}')
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in supported_report_rate_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReportRateInfoEvent response inputs fields are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate)
            })
            checker.check_fields(self, response, self.feature_8061.report_rate_info_event_cls, check_map)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8061_0001", _AUTHOR)
    # end def test_report_rate_info_change_event

    @features("Feature8061")
    @features("Feature8100")
    @features("Wireless")
    @features("USB")
    @level("Business")
    @bugtracker('ReportRateInfo_EventLost')
    def test_report_rate_info_change_event_after_plug_unplug_usb(self):
        """
        Validate that event is sent whenever the report rate is changed by plugin USB cable and unplug USB cable
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        report_rate_wireless = ExtendedAdjustableReportRateTestUtils.get_none_default_wireless_report_rate(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a software profile from the default OOB profile and change the "
                                 f"wireless report rate to {report_rate_wireless}.")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_software_profile_with_attributes(
            test_case=self, modifiers={"report_rate_wireless": report_rate_wireless})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power ON the USB cable and switch to the channel then update the feature mapping")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unpluging_usb_cable = True
        ProtocolManagerUtils.switch_to_usb_channel(test_case=self)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=ExtendedAdjustableReportRate.FEATURE_ID)

        # TODO: Simplify following procedure, if there is any better way.
        #  Because the reportRateInfoEvent will be sent within 10ms after powering on the USB channel. It's not
        #  enough for updating the feature mapping and the reportRateInfoEvent will be dropped. So currently, I decided
        #  to repeat the POWER ON -> OFF procedure after updating feature mapping that can make the reportRateInfoEvent
        #  got as expected.
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF the USB cable and switch to the receiver channel")
        # --------------------------------------------------------------------------------------------------------------
        ProtocolManagerUtils.exit_usb_channel(test_case=self)
        self.post_requisite_unpluging_usb_cable = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power ON the USB cable and switch to the channel")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unpluging_usb_cable = True
        ProtocolManagerUtils.switch_to_usb_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
        # --------------------------------------------------------------------------------------------------------------
        report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
            self, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the received report rate {report_rate_info_event.report_rate} equals "
                                  f"{ExtendedAdjustableReportRateTestUtils.get_highest_report_rate(self)}")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker.check_fields(
            self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF the USB cable")
        # --------------------------------------------------------------------------------------------------------------
        ProtocolManagerUtils.exit_usb_channel(test_case=self)
        self.post_requisite_unpluging_usb_cable = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
        # --------------------------------------------------------------------------------------------------------------
        report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check the received report rate {report_rate_info_event.report_rate} equals {report_rate_wireless}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "report_rate": (checker.check_report_rate, report_rate_wireless)
        })
        ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker.check_fields(
            self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)

        self.testCaseChecked("BUS_8061_0002", _AUTHOR)
    # end def test_report_rate_info_change_event_after_plug_unplug_usb
# end class ExtendedAdjustableReportRateBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
