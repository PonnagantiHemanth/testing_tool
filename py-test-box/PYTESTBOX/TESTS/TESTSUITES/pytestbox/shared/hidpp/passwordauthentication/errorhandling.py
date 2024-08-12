#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.passwordauthentication.errorhandling
:brief: ``PasswordAuthentication`` errorhandling test suite
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
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
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
class SharedPasswordAuthenticationErrorHandlingTestCase(SharedPasswordAuthenticationTestCase, ABC):
    """
    Validates Shared Password Authentication errorhandling TestCases
    """
    _test_sending_password_without_started_session_expected_error_codes = None
    _test_session_if_no_authentication_expected_error_codes = None
    _test_session_is_closed_when_device_is_reset_expected_error_codes = None
    _test_start_session_request_for_an_already_open_session_expected_error_codes = None
    _test_start_session_with_wrong_authentication_expected_error_codes = None
    _test_start_session_with_wrong_name_expected_error_codes = None

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    @services("HardwareReset")
    def test_session_is_closed_when_device_is_reset(self):
        """
        Validate that session is closed when the DUT is reset

        :raise ``AssertionError``: Assert account name that raise an exception
        """
        self.post_requisite_reload_nvs = True
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform a DUT hardware reset")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.ResetHelper.hardware_reset(self)
            self.PasswordAuthenticationTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable respective features")
            # ----------------------------------------------------------------------------------------------------------
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)
            report = self.ManageUtils.HIDppHelper.get_enable_features_req(
                test_case=self, manufacturing=manufacturing, compliance=compliance, gotthard=gotthard)
            self.ManageUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=self._test_session_is_closed_when_device_is_reset_expected_error_codes)
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0001", _AUTHOR)
    # end def test_session_is_closed_when_device_is_reset

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_start_session_request_for_an_already_open_session(self):
        """
        Validate that sending start session request for an already open session closes the session
        """
        self.post_requisite_reload_nvs = True
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING

        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
            test_case=self, account_name=account_name.value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=account_name.value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
        checker.check_fields(self, response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).start_session_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send EnableFeatures to enable manufacturing feature")
        # --------------------------------------------------------------------------------------------------------------
        report = self.ManageUtils.HIDppHelper.get_enable_features_req(test_case=self, manufacturing=True)

        self.ManageUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=self._test_start_session_request_for_an_already_open_session_expected_error_codes)

        self.testCaseChecked("ERR_PWD_AUTH_0002", _AUTHOR)
    # end def test_start_session_request_for_an_already_open_session

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_session_if_no_authentication(self):
        """
        Validate that session is not considered opened if the authentication protocol does not
        complete successfully (no authentication done)
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
        checker.check_fields(self, start_session_response,  self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).start_session_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send EnableFeatures to enable manufacturing feature")
        # --------------------------------------------------------------------------------------------------------------
        report = self.ManageUtils.HIDppHelper.get_enable_features_req(test_case=self, manufacturing=True)

        self.ManageUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=self._test_start_session_with_wrong_authentication_expected_error_codes)

        self.testCaseChecked("ERR_PWD_AUTH_0003", _AUTHOR)
    # end def test_session_if_no_authentication

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_start_session_with_wrong_authentication(self):
        """
        Validate that session is not considered opened if the authentication protocol does not
        complete successfully (wrong authentication done)
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
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, start_session_response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).start_session_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Passwd0 request for {account_name} with wrong password")
        # --------------------------------------------------------------------------------------------------------------
        passwd0 = "34567887612345678900112233445566"

        manuf_password = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(
            account_name=account_name)

        assert passwd0 != manuf_password
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
            test_case=self, passwd=HexList(passwd0))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        status = HexList(self.PasswordAuthenticationTestUtils.Status.FAILURE.value)
        checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "status": (checker.check_status, status)
        })
        checker.check_fields(self, response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).passwd0_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable respective features")
        # --------------------------------------------------------------------------------------------------------------
        report = self.ManageUtils.HIDppHelper.get_enable_features_req(test_case=self, manufacturing=True)

        self.ManageUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=self._test_start_session_with_wrong_authentication_expected_error_codes)

        self.testCaseChecked("ERR_PWD_AUTH_0004", _AUTHOR)
    # end def test_start_session_with_wrong_authentication

    @features("PasswordAuthentication")
    @level("ErrorHandling")
    def test_start_session_with_wrong_name(self):
        """
        Validate that start session with invalid account names (including 0) return INVALID_ARGUMENT error
        """
        account_name = "x1E02_Invalid"
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartSession request for wrong account_name {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.PasswordAuthenticationTestUtils.HIDppHelper.get_start_session_cls_req(
            test_case=self, account_name=account_name)
        self.PasswordAuthenticationTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=self._test_start_session_with_wrong_name_expected_error_codes)

        self.testCaseChecked("ERR_PWD_AUTH_0005", _AUTHOR)
    # end def test_start_session_with_wrong_name

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_sending_wrong_password(self):
        """
        Validate that sending a wrong password (including 0) returns a failure
        """
        values = ["00000000000000000000000000000000", "00112233445566778899114455667700",
                  "FFFFFFFF00000000FFFFFFFF00000000", "0000000000000000FFFFFFFFFFFFFFFF"]
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        manuf_passwd = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(
            account_name=account_name)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over account wrong password values")
        # --------------------------------------------------------------------------------------------------------------
        for passwd0 in values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            start_session_response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(
                self, start_session_response,
                self.PasswordAuthenticationTestUtils.HIDppHelper.get_feature_interface(
                    test_case=self).start_session_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name} with wrong password")
            # ----------------------------------------------------------------------------------------------------------
            assert passwd0 != manuf_passwd
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
                test_case=self, passwd=HexList(passwd0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.FAILURE.value)
            checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                                 get_feature_interface(test_case=self).passwd0_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_PWD_AUTH_0006", _AUTHOR)
    # end def test_sending_wrong_password

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_sending_password_without_started_session(self):
        """
        Validate that sending a passwd without started session returns NOT_ALLOWED error
        """
        self.post_requisite_reload_nvs = True
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Passwd0 request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        passwd0 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(
            account_name=account_name)
        report = self.PasswordAuthenticationTestUtils.HIDppHelper.get_passwd0_cls_req(
            test_case=self, passwd=HexList(passwd0))

        self.PasswordAuthenticationTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=self._test_sending_password_without_started_session_expected_error_codes)

        self.testCaseChecked("ERR_PWD_AUTH_0007", _AUTHOR)
    # end def test_sending_password_without_started_session
# end class SharedPasswordAuthenticationErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
