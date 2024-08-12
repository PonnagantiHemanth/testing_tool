#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1602.functionality
:brief: HID++ 2.0 ``PasswordAuthentication`` functionality test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/11/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1602.passwordauthentication import DevicePasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.functionality import \
    SharedPasswordAuthenticationFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_LONG_PWD_WARNING = "Long password must be supported for this device. Check the settings or decorator"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DevicePasswordAuthenticationFunctionalityTestCase(SharedPasswordAuthenticationFunctionalityTestCase,
                                                        DevicePasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` functionality test cases
    """

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @level("Functionality")
    def test_open_all_sessions_long_password(self):
        """
        Validate Open, Authenticate and Close all the possible session.
        Also check passwd1 API return SUCCESS (for long_password=1)
        """
        self.post_requisite_reload_nvs = True
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
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

            if not response.long_password:
                warnings.warn(_LONG_PWD_WARNING)
                return
            # end if

            passwd0, passwd1 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_and_password1_from_name(
                account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
                test_case=self, passwd=HexList(passwd0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.IN_PROGRESS.value)
            checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd0_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd1 request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd1(
                test_case=self, passwd=HexList(passwd1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd1Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.SUCCESS.value)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd1_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send EndSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check EndSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1602.end_session_response_cls, {})
        # end for

        self.testCaseChecked("FUN_PWD_AUTH_0002", _AUTHOR)
    # end def test_open_all_sessions_long_password
# end class DevicePasswordAuthenticationFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
