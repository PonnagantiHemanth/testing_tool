#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.base.passwordauthenticationutils
:brief:  Helpers for receiver ``PasswordAuthentication`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import Enum

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.registers.passwd import PasswordRequest
from pyhid.hidpp.hidpp1.registers.passwd import PasswordResponse
from pyhid.hidpp.hidpp1.registers.startsession import StartSessionRequest
from pyhid.hidpp.hidpp1.registers.startsession import StartSessionResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.passwordfileparser import PasswordFileParser
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils
from pytestbox.shared.base.passwordauthenticationutils import SharedPasswordAuthenticationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class ReceiverPasswordAuthenticationTestUtils(SharedPasswordAuthenticationTestUtils, ReceiverBaseTestUtils):
    """
    Provide helpers for common checks on ``PasswordAuthentication`` feature
    """
    class AccountNames(Enum):
        """
        Account types supported
        """
        MANUFACTURING = "x1E02_Manuf"
    # end class AccountNames

    @classmethod
    def is_supported(cls, test_case, account_name):
        """
        Check if account is supported

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param account_name: Account name
        :type account_name: ``AccountNames``

        :return: True if account is supported
        :rtype: ``bool``
        """
        account_support = {
            cls.AccountNames.MANUFACTURING:
                test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportManufacturing,
        }
        return account_support[account_name]
    # end def is_supported

    @classmethod
    def get_all_account_name_values(cls, account_name):
        # See ``SharedPasswordAuthenticationTestUtils.get_all_account_name_values``
        manufacturing = account_name == ReceiverPasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        compliance = False
        gothard = False

        return manufacturing, compliance, gothard
    # end def get_all_account_name_values

    class StartSessionResponseChecker(SharedPasswordAuthenticationTestUtils.StartSessionResponseChecker):
        # See ``SharedPasswordAuthenticationTestUtils.StartSessionResponseChecker``
        @classmethod
        def get_default_check_map(cls, test_case):
            # See ``SharedPasswordAuthenticationTestUtils.StartSessionResponseChecker.get_default_check_map``
            return {
                "reserved": (cls.check_reserved, 0),
                "long_password": (
                    cls.check_long_password, ReceiverPasswordAuthenticationTestUtils.Flags.SHORT_PASSWORD_SUPPORT),
                "full_authentication": (
                    cls.check_full_authentication, ReceiverPasswordAuthenticationTestUtils.Flags.SEMI_AUTHENTICATION),
                "constant_credentials": (
                    cls.check_constant_credentials, ReceiverPasswordAuthenticationTestUtils.Flags.CONSTANT_CREDENTIALS),
            }
        # end def get_default_check_map
    # end class StartSessionResponseChecker

    class HIDppHelper(SharedPasswordAuthenticationTestUtils.HIDppHelper, ReceiverBaseTestUtils.HIDppHelper):
        # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper``
        @classmethod
        def start_session(cls, test_case, account_name, device_index=None, port_index=None, software_id=None,
                          padding=None, reserved=None):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.start_session``
            return ChannelUtils.send(
                test_case=test_case,
                report=StartSessionRequest(account_name),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=StartSessionResponse)
        # end def start_session

        @classmethod
        def passwd0(cls, test_case, passwd, device_index=None, port_index=None, software_id=None, padding=None,
                    reserved=None):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.passwd0``
            return ChannelUtils.send(
                test_case=test_case,
                report=PasswordRequest(password=passwd),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=PasswordResponse
            )
        # end def passwd0

        @classmethod
        def get_password0_from_name(cls, account_name):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_password_from_name``
            passwd0 = None
            password_file_parser = PasswordFileParser()
            if account_name == ReceiverPasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value:
                passwd0 = password_file_parser.get_password(PasswordFileParser.Accounts.MANUFACTURING)
            # end if
            assert passwd0 is not None
            return passwd0
        # end def get_password0_from_name

        @classmethod
        def authenticate_and_validate(cls, test_case, start_session_response, account_name):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.authenticate_and_validate``
            passwd0 = cls.get_password0_from_name(account_name=account_name)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, f"Send Passwd0 request for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            response = cls.passwd0(test_case=test_case, passwd=HexList(passwd0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, f"Check Passwd0Response fields for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(ReceiverPasswordAuthenticationTestUtils.Status.SUCCESS.value)
            checker = ReceiverPasswordAuthenticationTestUtils.PasswordResponseChecker
            check_map = checker.get_default_check_map(test_case)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(
                test_case, response, cls.get_feature_interface(test_case).passwd0_response_cls, check_map)
        # end def authenticate_and_validate

        @classmethod
        def get_feature_interface(cls, test_case):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_feature_interface``
            class FeatureInterface:
                """
                Feature interface
                """
                start_session_cls = StartSessionRequest
                start_session_response_cls = StartSessionResponse
                passwd0_cls = PasswordRequest
                passwd0_response_cls = PasswordResponse
            # end class FeatureInterface
            return FeatureInterface
        # end def get_feature_interface

        @classmethod
        def get_passwd0_cls_req(cls, test_case, passwd):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_passwd0_cls_req``
            return PasswordRequest(password=passwd)
        # end def get_passwd0_cls_req

        @classmethod
        def get_start_session_cls_req(cls, test_case, account_name):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_start_session_cls_req``
            return StartSessionRequest(account_name=account_name)
        # end def get_start_session_cls_req

        @classmethod
        def start_session_and_authenticate(cls, test_case, account_name):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate``
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, f"Send StartSession request for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            response = cls.start_session(test_case=test_case, account_name=account_name)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, f"Validate the StartSession response for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            checker = ReceiverPasswordAuthenticationTestUtils.StartSessionResponseChecker
            check_map = checker.get_default_check_map(test_case)
            checker.check_fields(
                test_case, response, cls.get_feature_interface(test_case).start_session_response_cls, check_map)

            cls.authenticate_and_validate(test_case=test_case,
                                          start_session_response=response,
                                          account_name=account_name)
        # end def start_session_and_authenticate
    # end class HIDppHelper
# end class ReceiverPasswordAuthenticationTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
