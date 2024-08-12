#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.passwordauthentication.interface
:brief: ``PasswordAuthentication`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
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
class SharedPasswordAuthenticationInterfaceTestCase(SharedPasswordAuthenticationTestCase, ABC):
    """
    Validates ``PasswordAuthentication`` interface test cases
    """

    @features("PasswordAuthentication")
    @level("Interface")
    @services("Debugger")
    def test_start_session(self):
        """
        Validate ``StartSession`` interface
        """
        self.post_requisite_reload_nvs = True
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartSession request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=account_name)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
        check_map = checker.get_default_check_map(self)
        if not isinstance(self.current_channel, UsbReceiverChannel):
            feature_1602_index, _, device_index, _ = self.PasswordAuthenticationTestUtils.HIDppHelper.\
                get_parameters(self)
            check_map.update({
                "device_index": (checker.check_device_index, HexList(device_index)),
                "feature_index": (checker.check_feature_index, HexList(feature_1602_index))
            })
        # end if
        checker.check_fields(self, response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).start_session_response_cls, check_map)

        self.testCaseChecked("INT_PWD_AUTH_0001", _AUTHOR)
    # end def test_start_session

    @features("PasswordAuthentication")
    @features("NoPasswordAuthenticationLongPassword")
    @level("Interface")
    @services("Debugger")
    def test_passwd0(self):
        """
        Validate ``Passwd0`` interface for short password
        """
        self.post_requisite_reload_nvs = True
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        passwd0 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(account_name=account_name)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartSession request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(test_case=self, account_name=account_name)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Passwd0 request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(test_case=self, passwd=HexList(passwd0))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Passwd0Response fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
        check_map = checker.get_default_check_map(self)
        if not isinstance(self.current_channel, UsbReceiverChannel):
            feature_1602_index, _, device_index, _ = self.PasswordAuthenticationTestUtils.HIDppHelper.\
                get_parameters(self)
            check_map.update({
                "device_index": (checker.check_device_index, HexList(device_index)),
                "feature_index": (checker.check_feature_index, HexList(feature_1602_index))
            })
        # end if
        checker.check_fields(self, response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).passwd0_response_cls, check_map)

        self.testCaseChecked("INT_PWD_AUTH_0002", _AUTHOR)
    # end def test_passwd0
# end class SharedPasswordAuthenticationInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
