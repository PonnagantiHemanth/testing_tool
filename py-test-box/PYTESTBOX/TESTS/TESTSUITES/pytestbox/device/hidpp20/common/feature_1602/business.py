#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1602.business
:brief: HID++ 2.0 ``PasswordAuthentication`` business test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1602.passwordauthentication import DevicePasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.business import SharedPasswordAuthenticationBusinessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_DISABLE_FEATURES = "Send DisableFeatures request"
_ENABLE_HIDDEN_FEATURES = "Enable hidden features"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DevicePasswordAuthenticationBusinessTestCase(SharedPasswordAuthenticationBusinessTestCase,
                                                   DevicePasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` business test cases
    """

    @features("PasswordAuthentication")
    @features("Feature1004")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("Business")
    @services("Debugger")
    @services("PowerSupply")
    def test_service_requiring_authentication_when_battery_at_critical_level(self):
        """
        Validate that service requiring authentication can be used after authentication, when battery is at
        critical level
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _ENABLE_HIDDEN_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, "critical"))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set voltage to critical level {critical_voltage}")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(critical_voltage)

        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send EnableFeatures with {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)
            self.ManageUtils.HIDppHelper.enable_features(
                test_case=self, manufacturing=manufacturing, compliance=compliance, gotthard=gotthard)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check deactivatable features state")
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(
                manufacturing=manufacturing, compliance=compliance, gothard=gotthard)
            self.ManageUtils.HIDppHelper.check_state(self, expected_state)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send EndSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _DISABLE_FEATURES)
            # ----------------------------------------------------------------------------------------------------------
            self.ManageUtils.HIDppHelper.disable_features(self, disable_all=True)
        # end for

        self.testCaseChecked("BUS_PWD_AUTH_0003", _AUTHOR)
    # end def test_service_requiring_authentication_when_battery_at_critical_level

    @features("PasswordAuthentication")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level('Business', 'SmokeTests')
    @services("Debugger")
    def test_session_open_when_hidden_feature_is_enable_at_any_time(self):
        """
        Validate that a session can be opened while the hidden features are not yet enabled.
        Rationale: The 0x1602 feature is always active and has not the hidden attribute. It does not require the
        0x1E00 feature to enable it.
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _ENABLE_HIDDEN_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls)

            if compliance:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, _ENABLE_HIDDEN_FEATURES)
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.HIDppHelper.enable_hidden_features(self)
            # end if

            self.PasswordAuthenticationTestUtils.HIDppHelper.authenticate_and_validate(
                test_case=self, start_session_response=response, account_name=account_name.value)

            if gotthard:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, _ENABLE_HIDDEN_FEATURES)
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.HIDppHelper.enable_hidden_features(self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enable feature for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            self.ManageUtils.HIDppHelper.enable_features(
                test_case=self, manufacturing=manufacturing, compliance=compliance, gotthard=gotthard)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check enabled feature for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(
                manufacturing=manufacturing, compliance=compliance, gothard=gotthard)
            self.ManageUtils.HIDppHelper.check_state(self, expected_state)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send EndSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _DISABLE_FEATURES)
            # ----------------------------------------------------------------------------------------------------------
            self.ManageUtils.HIDppHelper.disable_features(self, disable_all=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Disable hidden features")
            # ----------------------------------------------------------------------------------------------------------
            self.enable_hidden_feature_id = ChannelUtils.update_feature_mapping(test_case=self,
                                                                                feature_id=EnableHidden.FEATURE_ID)
            report = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(test_case=self),
                                             feature_index=self.enable_hidden_feature_id,
                                             enable_byte=EnableHidden.DISABLED)
            ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=SetEnableHiddenFeaturesResponse)
        # end for

        self.testCaseChecked("BUS_PWD_AUTH_0004", _AUTHOR)
    # end def test_session_open_when_hidden_feature_is_enable_at_any_time
# end class DevicePasswordAuthenticationBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
