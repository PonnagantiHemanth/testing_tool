#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.passwordauthentication.business
:brief: ``PasswordAuthentication`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.hidpp.passwordauthentication.passwordauthentication import SharedPasswordAuthenticationTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class SharedPasswordAuthenticationBusinessTestCase(SharedPasswordAuthenticationTestCase, ABC):
    """
    Validates Shared Password Authentication Business Test Case
    """

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("Business")
    @services("Debugger")
    def test_service_requiring_authentication(self):
        """
        Validate that service requiring authentication can be used after authentication
        """
        self.post_requisite_reload_nvs = True
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enable respective feature for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)
            self.ManageUtils.HIDppHelper.enable_features(
                test_case=self, manufacturing=manufacturing, compliance=compliance, gotthard=gotthard)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check deactivatable features state for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(
                manufacturing=manufacturing, compliance=compliance, gothard=gotthard)
            self.ManageUtils.HIDppHelper.check_state(self, expected_state)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Disable features")
            # ----------------------------------------------------------------------------------------------------------
            self.ManageUtils.HIDppHelper.disable_features(self, disable_all=True)
        # end for

        self.testCaseChecked("BUS_PWD_AUTH_0001", _AUTHOR)
    # end def test_service_requiring_authentication

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @features("ManageDeactivatableFeaturesSupportCompliance")
    @level("Business")
    @services("Debugger")
    def test_starting_a_session_does_not_end_any_already_authenticated_open_session(self):
        """
        Validate that starting a session does not end any already authenticated open session for different accounts
        """
        self.post_requisite_reload_nvs = True
        account_name_manf = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        account_name_compl = self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value

        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
            test_case=self, account_name=account_name_manf)

        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
            test_case=self, account_name=account_name_compl)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send EnableFeatures to enable manufacturing feature")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        self.ManageUtils.HIDppHelper.enable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check 0x1E02 state")
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True)
        self.ManageUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send EndSession request for {account_name_manf}")
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
            test_case=self, account_name=account_name_manf)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send EndSession request for {account_name_compl}")
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
            test_case=self, account_name=account_name_compl)

        self.testCaseChecked("BUS_PWD_AUTH_0002", _AUTHOR)
    # end def test_starting_a_session_does_not_end_any_already_authenticated_open_session
# end class SharedPasswordAuthenticationBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
