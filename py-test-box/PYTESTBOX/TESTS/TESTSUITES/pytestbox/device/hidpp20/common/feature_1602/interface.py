#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1602.interface
:brief: HID++ 2.0 ``PasswordAuthentication`` interface test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2022/02/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1602.passwordauthentication import DevicePasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.interface import SharedPasswordAuthenticationInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_LONG_PWD_WARNING = "Long password must be supported for this device. Check the settings or decorator"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DevicePasswordAuthenticationInterfaceTestCase(SharedPasswordAuthenticationInterfaceTestCase,
                                                    DevicePasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` interface test cases
    """

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @features("ManageDeactivatableFeaturesSupportManufacturing")
    @level("Interface")
    @services("Debugger")
    def test_passwd1(self):
        """
        Validate ``Passwd1`` interface for long password
        """
        self.post_requisite_reload_nvs = True
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        feature_1602_index, _, device_index, _ = self.PasswordAuthenticationTestUtils.HIDppHelper.get_parameters(self)

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
        check_map.update({
            "device_index": (checker.check_device_index, HexList(device_index)),
            "feature_index": (checker.check_feature_index, HexList(feature_1602_index))
        })
        checker.check_fields(self, response, self.feature_1602.start_session_response_cls, check_map)

        if not response.long_password:
            warnings.warn(_LONG_PWD_WARNING)
            return
        # end if

        passwd0, passwd1 = self.PasswordAuthenticationTestUtils.HIDppHelper.\
            get_password0_and_password1_from_name(account_name=account_name)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Passwd0 request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(test_case=self, passwd=HexList(passwd0))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Passwd0Response fields {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        status = HexList(self.PasswordAuthenticationTestUtils.Status.IN_PROGRESS.value)
        checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(device_index)),
            "feature_index": (checker.check_feature_index, HexList(feature_1602_index)),
            "status": (checker.check_status, status)
        })
        checker.check_fields(self, response, self.feature_1602.passwd0_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Passwd1 request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd1(test_case=self, passwd=HexList(passwd1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Passwd1Response fields for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        status = HexList(self.PasswordAuthenticationTestUtils.Status.SUCCESS.value)
        # update the existing check_map which already has device_index and feature_index
        check_map.update({
            "status": (checker.check_status, status)
        })
        checker.check_fields(self, response, self.feature_1602.passwd1_response_cls, check_map)

        self.testCaseChecked("INT_PWD_AUTH_0003", _AUTHOR)
    # end def test_passwd1

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesSupportManufacturing")
    @level("Interface")
    @services("Debugger")
    def test_end_session(self):
        """
        Validate ``EndSession`` interface
        """
        self.post_requisite_reload_nvs = True
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        feature_1602_index, _, device_index, _ = self.PasswordAuthenticationTestUtils.HIDppHelper.get_parameters(self)

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
        check_map.update({
            "device_index": (checker.check_device_index, HexList(device_index)),
            "feature_index": (checker.check_feature_index, HexList(feature_1602_index))
        })
        checker.check_fields(self, response, self.feature_1602.start_session_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send EndSession request for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
            test_case=self, account_name=account_name)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check EndSessionResponse fields for {account_name}")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(device_index)),
            "feature_index": (checker.check_feature_index, HexList(feature_1602_index))
        }
        checker.check_fields(self, response, self.feature_1602.end_session_response_cls, check_map)

        self.testCaseChecked("INT_PWD_AUTH_0004", _AUTHOR)
        # end def test_end_session
    # end class DevicePasswordAuthenticationInterfaceTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
