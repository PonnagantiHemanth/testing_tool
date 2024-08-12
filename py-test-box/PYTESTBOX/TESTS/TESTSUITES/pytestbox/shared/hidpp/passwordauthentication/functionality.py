#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.passwordauthentication.functionality
:brief: ``PasswordAuthentication`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
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
class SharedPasswordAuthenticationFunctionalityTestCase(SharedPasswordAuthenticationTestCase, ABC):
    """
    Validates Shared Password Authentication Functionality Test Cases
    """

    @features("PasswordAuthentication")
    @features("NoPasswordAuthenticationLongPassword")
    @level("Functionality")
    @services("Debugger")
    def test_open_all_sessions_short_password(self):
        """
        Validate Open, Authenticate and Close all the possible session. Also check passwd0 API return
        SUCCESS (for long_password=0)
        """
        self.post_requisite_reload_nvs = True
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                test_case=self, account_name=account_name.value)

            if not isinstance(self.current_channel, UsbReceiverChannel):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send EndSession request for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
                    test_case=self, account_name=account_name.value)
            # end if
        # end for

        self.testCaseChecked("FUN_PWD_AUTH_0001", _AUTHOR)
    # end def test_open_all_sessions_short_password
# end class SharedPasswordAuthenticationFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
