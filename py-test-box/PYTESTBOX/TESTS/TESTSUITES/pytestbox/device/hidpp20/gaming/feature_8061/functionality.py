#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8061.functionality
:brief: HID++ 2.0 ``ExtendedAdjustableReportRate`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.powermodes import PowerModes
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8061.extendedadjustablereportrate import \
    ExtendedAdjustableReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableReportRateFunctionalityTestCase(ExtendedAdjustableReportRateTestCase):
    """
    Validate ``ExtendedAdjustableReportRate`` functionality test cases
    """

    @features("Feature8061")
    @features("Feature8100")
    @features("Wireless")
    @level("Functionality")
    def test_set_report_rate_wireless(self):
        """
        Validate the wireless report rate can be changed by setReportRate request
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
            report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReportRateInfoEvent response inputs fields are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate)
            })
            checker.check_fields(self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetReportRate response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate),
            })
            checker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8061_0001", _AUTHOR)
    # end def test_set_report_rate_wireless

    @features("Feature8061")
    @features("Feature8100")
    @features("USB")
    @level("Functionality")
    def test_set_report_rate_wired(self):
        """
        Validate the wired report rate can be changed by setReportRate request
        """
        onboard_mode = OnboardProfiles.Mode.HOST_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Power ON the USB cable and switch to the channel")
        # --------------------------------------------------------------------------------------------------------------
        if self.config_manager.current_protocol != LogitechProtocol.USB:
            self.post_requisite_unpluging_usb_cable = True
            ProtocolManagerUtils.switch_to_usb_channel(test_case=self)
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=ExtendedAdjustableReportRate.FEATURE_ID)
        # end if
        supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over report_rate in {supported_report_rate_list}")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in supported_report_rate_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReportRateInfoEvent response inputs fields are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate)
            })
            checker.check_fields(self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=ExtendedAdjustableReportRate.ConnectionType.WIRED)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetReportRate response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate),
            })
            checker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8061_0002", _AUTHOR)
    # end def test_set_report_rate_wired

    @features("Feature8061")
    @features("USB")
    @level("Functionality")
    def test_get_device_capabilities_functionality(self):
        """
        Validate the supportedReportRateList for each connectionTypes are valid
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        report = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_device_capabilities(
            test_case=self, connection_type=int(self.config_manager.current_protocol != LogitechProtocol.USB))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetDeviceCapabilities response fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.GetDeviceCapabilitiesResponseChecker.check_fields(
            self, report, self.feature_8061.get_device_capabilities_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Power ON the USB cable and switch to the channel")
        # --------------------------------------------------------------------------------------------------------------
        if self.config_manager.current_protocol != LogitechProtocol.USB:
            self.post_requisite_unpluging_usb_cable = True
            ProtocolManagerUtils.switch_to_usb_channel(test_case=self)
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=ExtendedAdjustableReportRate.FEATURE_ID)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        report = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_device_capabilities(
            test_case=self, connection_type=int(self.config_manager.current_protocol != LogitechProtocol.USB))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetDeviceCapabilities response fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.GetDeviceCapabilitiesResponseChecker.check_fields(
            self, report, self.feature_8061.get_device_capabilities_response_cls)

        self.testCaseChecked("FUN_8061_0003", _AUTHOR)
    # end def test_get_device_capabilities_functionality

    @features("Feature8061")
    @features("Wireless")
    @level("Functionality")
    def test_get_actual_report_rate_wireless(self):
        """
        Validate the actualReportRateList response fields are valid when the connection type is wireless
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetActualReportRateList request")
        # --------------------------------------------------------------------------------------------------------------
        report = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_actual_report_rate_list(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetActualReportRateList response fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.GetActualReportRateListResponseChecker.check_fields(
            self, report, self.feature_8061.get_actual_report_rate_list_response_cls)

        self.testCaseChecked("FUN_8061_0004", _AUTHOR)
    # end def test_get_actual_report_rate_wireless

    @features("Feature8061")
    @features("USB")
    @level("Functionality")
    def test_get_actual_report_rate_wired(self):
        """
        Validate the actualReportRateList response fields are valid when the connection type is wired
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Power ON the USB cable and switch to the channel")
        # --------------------------------------------------------------------------------------------------------------
        if self.config_manager.current_protocol != LogitechProtocol.USB:
            self.post_requisite_unpluging_usb_cable = True
            ProtocolManagerUtils.switch_to_usb_channel(test_case=self)
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=ExtendedAdjustableReportRate.FEATURE_ID)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetActualReportRateList request")
        # --------------------------------------------------------------------------------------------------------------
        report = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_actual_report_rate_list(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetActualReportRateList response fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.GetActualReportRateListResponseChecker.check_fields(
            self, report, self.feature_8061.get_actual_report_rate_list_response_cls)

        self.testCaseChecked("FUN_8061_0005", _AUTHOR)
    # end def test_get_actual_report_rate_wired

    @features("Feature8061")
    @features("Feature8100")
    @features("Wireless")
    @level("Functionality")
    @services('PowerSupply')
    def test_report_rate_reset_after_restart(self):
        """
        Validate the setting report rate will be reset to the OOB profile setting when the DUT restarts
        """
        onboard_mode = OnboardProfiles.Mode.HOST_MODE
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x8100)")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8100_index = ChannelUtils.update_feature_mapping(test_case=self,
                                                                      feature_id=OnboardProfiles.FEATURE_ID)

        report_rate_wireless = ExtendedAdjustableReportRateTestUtils.get_none_default_wireless_report_rate(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a software profile from the default OOB profile and change the "
                                 f"wireless report rate to {report_rate_wireless}.")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_software_profile_with_attributes(
            test_case=self, modifiers={"report_rate_wireless": report_rate_wireless})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over report_rate in range {supported_report_rate_list}")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in supported_report_rate_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetReportRate response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate),
            })
            checker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power OFF -> ON the DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)
            ChannelUtils.clean_messages(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=WirelessDeviceStatusBroadcastEvent,
                channel=self.current_channel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check reportRate is reset to OOB profile setting's value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate_wireless)
            })
            ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker.check_fields(
                self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait GetReportRate response and check reportRate is reset to OOB profile "
                                      "setting's value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate_wireless)
            })
            ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8061_0006", _AUTHOR)
    # end def test_report_rate_reset_after_restart

    @features("Feature8061")
    @features("Feature8100")
    @features("Wireless")
    @level("Functionality")
    @services('PowerSupply')
    @services('PowerSwitch')
    def test_report_rate_reset_after_restart_by_power_switch(self):
        """
        Validate the setting report rate will be reset to the OOB profile setting when the DUT is restarted by the power
        switch.
        """
        onboard_mode = OnboardProfiles.Mode.HOST_MODE
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x8100)")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8100_index = ChannelUtils.update_feature_mapping(test_case=self,
                                                                      feature_id=OnboardProfiles.FEATURE_ID)

        report_rate_wireless = ExtendedAdjustableReportRateTestUtils.get_none_default_wireless_report_rate(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a software profile from the default OOB profile and change the "
                                 f"wireless report rate to {report_rate_wireless}.")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_software_profile_with_attributes(
            test_case=self, modifiers={"report_rate_wireless": report_rate_wireless})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over report_rate in range {supported_report_rate_list}")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in supported_report_rate_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetReportRate response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate),
            })
            checker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power switch OFF -> ON the DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.power_slider_emulator.reset()
            ChannelUtils.clean_messages(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=WirelessDeviceStatusBroadcastEvent,
                channel=self.current_channel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check reportRate is reset to OOB profile setting's value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate_wireless)
            })
            ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker.check_fields(
                self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait GetReportRate response and check reportRate is reset to OOB profile "
                                      "setting's value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate_wireless)
            })
            ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8061_0007", _AUTHOR)
    # end def test_report_rate_reset_after_restart_by_power_switch

    @features("Feature8061")
    @features("Feature8100")
    @level("Functionality")
    def test_report_rate_reset_after_leaving_host_mode(self):
        """
        Validate the setting report rate will be reset to the OOB profile setting when the DUT leaving host mode
        """
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x8100)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8100_index = ChannelUtils.update_feature_mapping(test_case=self,
                                                                      feature_id=OnboardProfiles.FEATURE_ID)

        report_rate_wireless = ExtendedAdjustableReportRateTestUtils.get_none_default_wireless_report_rate(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a software profile from the default OOB profile and change the "
                                 f"wireless report rate to {report_rate_wireless}.")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_software_profile_with_attributes(
            test_case=self, modifiers={"report_rate_wireless": report_rate_wireless})
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over report_rate in range {supported_report_rate_list}")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in supported_report_rate_list:
            onboard_mode = OnboardProfiles.Mode.HOST_MODE
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
                self, allow_no_message=True, check_first_message=False)

            if report_rate != report_rate_wireless:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check the received report rate {report_rate_info_event.report_rate} equals {report_rate}")
                # ------------------------------------------------------------------------------------------------------
                checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
                check_map = checker.get_default_check_map(test_case=self)
                check_map.update({
                    "report_rate": (checker.check_report_rate, report_rate),
                })
                checker.check_fields(
                    self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check the received report rate {get_report_rate_response.report_rate} equals {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate),
            })
            checker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)

            onboard_mode = OnboardProfiles.Mode.ONBOARD_MODE
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Onboard Mode)")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
                                                                                        self, allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check reportRate is reset to OOB profile setting's value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate_wireless)
            })
            ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker.check_fields(
                self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait GetReportRate response and check reportRate is reset to OOB profile "
                                      "setting's value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate_wireless)
            })
            ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8061_0008", _AUTHOR)
    # end def test_report_rate_reset_after_leaving_host_mode

    @features("Feature8061")
    @features("Feature8100")
    @features("Feature1830")
    @level("Functionality")
    def test_report_rate_reset_after_leaving_depp_sleep_mode(self):
        """
        Validate the setting report rate will be reset to the OOB profile setting when the DUT leaving deep-sleep mode
        """
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1830)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=PowerModes.FEATURE_ID)

        report_rate_wireless = ExtendedAdjustableReportRateTestUtils.get_none_default_wireless_report_rate(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a software profile from the default OOB profile and change the "
                                 f"wireless report rate to {report_rate_wireless}.")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_software_profile_with_attributes(
            test_case=self, modifiers={"report_rate_wireless": report_rate_wireless})
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over report_rate in range {supported_report_rate_list}")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in supported_report_rate_list:
            onboard_mode = OnboardProfiles.Mode.HOST_MODE
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            report_rate_info_event = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
                self, allow_no_message=True, check_first_message=False)

            if report_rate != report_rate_wireless:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check the received report rate {report_rate_info_event.report_rate} equals {report_rate}")
                # ------------------------------------------------------------------------------------------------------
                checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
                check_map = checker.get_default_check_map(test_case=self)
                check_map.update({
                    "report_rate": (checker.check_report_rate, report_rate),
                })
                checker.check_fields(
                    self, report_rate_info_event, self.feature_8061.report_rate_info_event_cls, check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check the received report rate {get_report_rate_response.report_rate} equals {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate),
            })
            checker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setPowerMode request with powerMode = {PowerModes.DEEP_SLEEP}")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform an user action to wake-up the DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            get_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                test_case=self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait GetReportRate response and check reportRate is reset to the OOB profile "
                                      "setting's value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate_wireless)
            })
            ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker.check_fields(
                self, get_report_rate_response, self.feature_8061.get_report_rate_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8061_0009", _AUTHOR)
    # end def test_report_rate_reset_after_leaving_depp_sleep_mode
# end class ExtendedAdjustableReportRateFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
