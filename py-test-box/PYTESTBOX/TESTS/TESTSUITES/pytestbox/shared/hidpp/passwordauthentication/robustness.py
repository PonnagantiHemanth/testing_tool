#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.passwordauthentication.robustness
:brief: ``PasswordAuthentication`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from abc import ABC

from pychannel.usbchannel import UsbChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pylibrary.tools.hexlist import HexList
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.hidpp.passwordauthentication.passwordauthentication import SharedPasswordAuthenticationTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class SharedPasswordAuthenticationRobustnessTestCase(SharedPasswordAuthenticationTestCase, ABC):
    """
    Validates Shared Password Authentication Robustness Test Case
    """
    _test_service_is_closed_when_underlying_transport_channel_is_terminated_err_codes = None

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("Robustness")
    @services("Debugger")
    def test_service_is_closed_when_underlying_transport_channel_is_terminated(self):
        """
        Validate that session is closed when the underlying transport channel is terminated
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reset the device/receiver if DUT is receiver/device")
            # ----------------------------------------------------------------------------------------------------------
            if isinstance(self.current_channel, UsbChannel):
                self.PasswordAuthenticationTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=self)
            else:
                ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)
                ReceiverTestUtils.reset_receiver(test_case=self)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_prerequisite(self, "Enable hidden features")
                # ------------------------------------------------------------------------------------------------------
                self.ManageUtils.HIDppHelper.enable_hidden_features(self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable respective features")
            # ----------------------------------------------------------------------------------------------------------
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)
            report = self.ManageUtils.HIDppHelper.get_enable_features_req(
                test_case=self, manufacturing=manufacturing, compliance=compliance, gotthard=gotthard)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate response")
            # ----------------------------------------------------------------------------------------------------------
            self.ManageUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=self._test_service_is_closed_when_underlying_transport_channel_is_terminated_err_codes)
        # end for

        self.testCaseChecked("ROB_PWD_AUTH_0001", _AUTHOR)
    # end def test_service_is_closed_when_underlying_transport_channel_is_terminated

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("Robustness")
    @services("Debugger")
    def test_start_session_account_names(self):
        """
        Validate start session for each known account name
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Start session with {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            start_session_response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check start session response")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(self, start_session_response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                                 get_feature_interface(test_case=self).start_session_response_cls)
        # end for

        self.testCaseChecked("ROB_PWD_AUTH_0002", _AUTHOR)
    # end def test_start_session_account_names

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationSmallerPassword")
    @features("ManageDeactivatableFeaturesAuth")
    @level("Robustness")
    @services("Debugger")
    def test_smaller_password(self):
        """
        Validate that bytes following 0 are ignored if password is smaller than 16/32 bytes
        """
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartSession request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        start_session_response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=account_name)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
        checker.check_fields(self, start_session_response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).start_session_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Passwd0 request for {account_name} with additional bytes")
        # --------------------------------------------------------------------------------------------------------------
        warnings.warn("TODO: Once the smaller password is implemented, send the extra bytes accordingly. Also check "
                      "the account to use")
        extra = "0123456789"
        passwd0 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(
            account_name=account_name)
        passwd0 += extra
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
            test_case=self, passwd=HexList(passwd0))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).passwd0_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Enable features for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        self.ManageUtils.HIDppHelper.enable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check 0x1E02 state")
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True)
        self.ManageUtils.HIDppHelper.check_state(self, expected_state)

        self.testCaseChecked("ROB_PWD_AUTH_0003", _AUTHOR)
    # end def test_smaller_password
# end class SharedPasswordAuthenticationRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
