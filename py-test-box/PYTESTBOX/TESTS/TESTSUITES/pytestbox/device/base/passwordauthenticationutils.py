#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.passwordauthenticationutils
:brief: Helpers for device ``PasswordAuthentication`` feature
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from enum import Enum

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.passwordauthentication import EndSessionResponse
from pyhid.hidpp.features.common.passwordauthentication import Passwd1Response
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.passwordfileparser import PasswordFileParser
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.passwordauthenticationutils import SharedPasswordAuthenticationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DevicePasswordAuthenticationTestUtils(SharedPasswordAuthenticationTestUtils, DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``PasswordAuthentication`` feature
    """
    class AccountNames(Enum):
        """
        Account types supported
        """
        MANUFACTURING = "x1E02_Manuf"
        COMPLIANCE = "x1E02_Compl"
        GOTHARD = "x1E02_Gothard"
        GOTTHARD = GOTHARD
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
            cls.AccountNames.COMPLIANCE:
                test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportCompliance,
            cls.AccountNames.GOTTHARD:
                test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard,
        }
        return account_support[account_name]
    # end def is_supported

    @classmethod
    def get_all_account_name_values(cls, account_name):
        # See ``SharedPasswordAuthenticationTestUtils.get_all_account_name_values``
        manufacturing = account_name == DevicePasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        compliance = account_name == DevicePasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value
        gothard = account_name == DevicePasswordAuthenticationTestUtils.AccountNames.GOTHARD.value

        return manufacturing, compliance, gothard
    # end def get_all_account_name_values

    class StartSessionResponseChecker(SharedPasswordAuthenticationTestUtils.StartSessionResponseChecker):
        # See ``SharedPasswordAuthenticationTestUtils.StartSessionResponseChecker``
        @classmethod
        def get_default_check_map(cls, test_case):
            # See ``SharedPasswordAuthenticationTestUtils.StartSessionResponseChecker.get_default_check_map``
            config = test_case.f.PRODUCT.FEATURES.COMMON.PASSWORD_AUTHENTICATION
            return {
                "reserved": (cls.check_reserved, 0),
                "long_password": (cls.check_long_password, HexList(config.F_SupportLongPassword)),
                "full_authentication": (cls.check_full_authentication, HexList(config.F_FullAuthentication)),
                "constant_credentials": (cls.check_constant_credentials, HexList(config.F_ConstantCredentials))
            }
        # end def get_default_check_map
    # end class StartSessionResponseChecker

    class HIDppHelper(SharedPasswordAuthenticationTestUtils.HIDppHelper, DeviceBaseTestUtils.HIDppHelper):
        # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=PasswordAuthentication.FEATURE_ID,
                           factory=PasswordAuthenticationFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def start_session(cls, test_case, account_name, device_index=None, port_index=None, software_id=None,
                          padding=None, reserved=None):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.start_session``
            feature_1602_index, feature_1602, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1602.start_session_cls(
                device_index=device_index,
                feature_index=feature_1602_index,
                account_name=account_name)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1602.start_session_response_cls)
        # end def start_session

        @classmethod
        def end_session(cls, test_case, account_name, device_index=None, port_index=None, software_id=None,
                        padding=None, reserved=None):
            """
            Process ``EndSession``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param account_name: Account name, expressed as UTF-8 string (except 0)
            :type account_name: ``str | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: EndSessionResponse
            :rtype: ``EndSessionResponse``
            """
            feature_1602_index, feature_1602, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1602.end_session_cls(
                device_index=device_index,
                feature_index=feature_1602_index,
                account_name=account_name)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1602.end_session_response_cls)
        # end def end_session

        @classmethod
        def passwd0(cls, test_case, passwd, device_index=None, port_index=None, software_id=None, padding=None,
                    reserved=None):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.passwd0``
            feature_1602_index, feature_1602, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1602.passwd0_cls(
                device_index=device_index,
                feature_index=feature_1602_index,
                passwd=passwd)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1602.passwd0_response_cls)
        # end def passwd0

        @classmethod
        def passwd1(cls, test_case, passwd, device_index=None, port_index=None, software_id=None, padding=None,
                    reserved=None):
            """
            Process ``Passwd1``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param passwd: Password. This parameter shall be a random binary string, except 0.
            :type passwd: ``str | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: Passwd1Response
            :rtype: ``Passwd1Response``
            """
            feature_1602_index, feature_1602, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1602.passwd1_cls(
                device_index=device_index,
                feature_index=feature_1602_index,
                passwd=passwd)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1602.passwd1_response_cls)
        # end def passwd1

        @classmethod
        def get_password0_from_name(cls, account_name):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_password_from_name``
            passwd0 = None
            password_file_parser = PasswordFileParser()
            if account_name == DevicePasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value:
                passwd0 = password_file_parser.get_password(PasswordFileParser.Accounts.MANUFACTURING)
            elif account_name == DevicePasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value:
                passwd0 = password_file_parser.get_password(PasswordFileParser.Accounts.COMPLIANCE)
            elif account_name == DevicePasswordAuthenticationTestUtils.AccountNames.GOTHARD.value:
                passwd0 = password_file_parser.get_password(PasswordFileParser.Accounts.GOTHARD)
            # end if
            assert passwd0 is not None
            return passwd0
        # end def get_password0_from_name

        @classmethod
        def get_password0_and_password1_from_name(cls, account_name):
            """
            Get passwd0 and passwd1 for given account name

            :param account_name: Account name
            :type account_name: ``str``

            :return: The password of account name
            :rtype: ``tuple[str, str]``

            :raise ``AssertionError``: Assert password size that raise an exception
            """
            passwd = "0102030405060708091011121314151617181920212223242526272829303132"
            warnings.warn(f"TODO: implement passwd properly when Long password is supported for {account_name}")

            password_size = 16 * 2  # Hex size for 16
            assert len(passwd) > password_size
            passwd0 = passwd[:password_size]
            passwd1 = passwd[password_size:]

            return passwd0, passwd1
        # end def get_password0_and_password1_from_name

        @classmethod
        def authenticate_and_validate(cls, test_case, start_session_response, account_name):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.authenticate_and_validate``
            if start_session_response.long_password:
                passwd0, passwd1 = cls.get_password0_and_password1_from_name(account_name=account_name)
            else:
                passwd0 = cls.get_password0_from_name(account_name=account_name)
                passwd1 = None
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, f"Send Passwd0 request for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            response = cls.passwd0(test_case=test_case, passwd=HexList(passwd0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, f"Check Passwd0Response fields for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            checker = DevicePasswordAuthenticationTestUtils.PasswordResponseChecker
            check_map = checker.get_default_check_map(test_case)
            if start_session_response.long_password:
                # long password
                status = HexList(DevicePasswordAuthenticationTestUtils.Status.IN_PROGRESS.value)
                check_map.update({
                    "status": (checker.check_status, status)
                })
                checker.check_fields(
                    test_case, response, cls.get_feature_interface(test_case).passwd0_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f"Send Passwd1 request for {account_name}")
                # ------------------------------------------------------------------------------------------------------
                response = cls.passwd1(test_case=test_case, passwd=HexList(passwd1))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Check Passwd1Response fields for {account_name}")
                # ------------------------------------------------------------------------------------------------------
                status = HexList(DevicePasswordAuthenticationTestUtils.Status.SUCCESS.value)
                check_map.update({
                    "status": (checker.check_status, status)
                })
                checker.check_fields(
                    test_case, response, cls.get_feature_interface(test_case).passwd1_response_cls, check_map)
            else:
                # short password
                status = HexList(DevicePasswordAuthenticationTestUtils.Status.SUCCESS.value)
                check_map.update({
                    "status": (checker.check_status, status)
                })
                checker.check_fields(
                    test_case, response, cls.get_feature_interface(test_case).passwd0_response_cls, check_map)
            # end if
        # end def authenticate_and_validate

        @classmethod
        def get_feature_interface(cls, test_case):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_feature_interface``
            _, feature_1602, _, _ = cls.get_parameters(test_case)
            return feature_1602
        # end def get_feature_interface

        @classmethod
        def get_passwd0_cls_req(cls, test_case, passwd):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_passwd0_cls_req``
            feature_1602_index, feature_1602, device_index, _ = cls.get_parameters(test_case=test_case)
            return feature_1602.passwd0_cls(device_index=device_index,
                                            feature_index=feature_1602_index,
                                            passwd=passwd)
        # end def get_passwd0_cls_req

        @classmethod
        def get_start_session_cls_req(cls, test_case, account_name):
            # See ``SharedPasswordAuthenticationTestUtils.HIDppHelper.get_start_session_cls_req``
            feature_1602_index, feature_1602, device_index, port_index = cls.get_parameters(test_case=test_case)
            return feature_1602.start_session_cls(device_index=device_index,
                                                  feature_index=feature_1602_index,
                                                  account_name=account_name)
        # def get_start_session_cls_req

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
            checker = DevicePasswordAuthenticationTestUtils.StartSessionResponseChecker
            check_map = checker.get_default_check_map(test_case)
            checker.check_fields(
                test_case, response, cls.get_feature_interface(test_case).start_session_response_cls, check_map)

            cls.authenticate_and_validate(test_case=test_case,
                                          start_session_response=response,
                                          account_name=account_name)
        # end def start_session_and_authenticate
    # end class HIDppHelper
# end class DevicePasswordAuthenticationTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
