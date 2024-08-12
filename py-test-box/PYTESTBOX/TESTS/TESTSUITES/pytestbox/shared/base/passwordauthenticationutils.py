#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.passwordauthenticationutils
:brief:  Helpers for Password Authentication feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum

from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pytestbox.base.basetestutils import CommonBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class SharedPasswordAuthenticationTestUtils(CommonBaseTestUtils):
    """
    Provide helpers for common checks on ``PasswordAuthentication`` feature
    """

    class Status(IntEnum):
        """
        Status type supported
        """
        INVALID = 0
        IN_PROGRESS = 1
        SUCCESS = 2
        FAILURE = 3
        RESERVED = 4  # 4..255
    # end class Status

    class Flags:
        """
        Flags type supported
        """
        UPGRADEABLE_CREDENTIALS = 0x00
        CONSTANT_CREDENTIALS = 0x01
        SEMI_AUTHENTICATION = 0x00
        FULL_AUTHENTICATION = 0x01
        SHORT_PASSWORD_SUPPORT = 0x00
        LONG_PASSWORD_SUPPORT = 0x01
    # end class Flags

    @classmethod
    def is_supported(cls, test_case, account_name):
        """
        Check if account is supported

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param account_name: Account name
        :type account_name: ``AccountNames``

        :return: True if account is supported
        :rtype: ``bool``
        """
        return NotImplementedAbstractMethodError
    # end def is_supported

    @classmethod
    def get_all_account_name_values(cls, account_name):
        """
        Get all account name values

        :param account_name: Account name
        :type account_name: ``str``

        :return: Account name values in order
        :rtype: ``tuple[bool, bool, bool]``

        :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
        """
        return NotImplementedAbstractMethodError
    # end def get_all_account_name_values

    class StartSessionResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        Check ``StartSessionResponse``
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``StartSessionResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            return NotImplementedAbstractMethodError
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, message, expected):
            """
            Check reserved bits value

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``BitFieldContainerMixin``
            :param expected: StartSession flags reserved bits value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(obtained=to_int(message.reserved),
                                  expected=to_int(expected),
                                  msg="The reserved bits are not as expected")
        # end def check_reserved

        @staticmethod
        def check_long_password(test_case, message, expected):
            """
            Check long password bit value

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``BitFieldContainerMixin``
            :param expected: StartSession long password bit value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(obtained=to_int(message.long_password),
                                  expected=to_int(expected),
                                  msg="The long password bit is not as expected")
        # end def check_long_password

        @staticmethod
        def check_full_authentication(test_case, message, expected):
            """
            Check full authentication bit value

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``BitFieldContainerMixin``
            :param expected: StartSession full authentication bit value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(obtained=to_int(message.full_authentication),
                                  expected=to_int(expected),
                                  msg="The full authentication bit is not as expected")
        # end def check_full_authentication

        @staticmethod
        def check_constant_credentials(test_case, message, expected):
            """
            Check constant credentials bit value

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``BitFieldContainerMixin``
            :param expected: StartSession constant credentials bit value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(obtained=to_int(message.constant_credentials),
                                  expected=to_int(expected),
                                  msg="The constant credentials bit is not as expected")
        # end def check_constant_credentials
    # end class StartSessionResponseChecker

    class PasswordResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        Check ``PasswordResponse``
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``PasswordResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "status": (cls.check_status, HexList(SharedPasswordAuthenticationTestUtils.Status.SUCCESS.value))
            }
        # end def get_default_check_map

        @staticmethod
        def check_status(test_case, response, expected):
            """
            Check status field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: PasswordResponse to check
            :type response: ``BitFieldContainerMixin``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(expected=to_int(expected),
                                  obtained=to_int(response.status),
                                  msg=f"The status parameter is not as expected")
        # end def check_status
    # end class PasswordResponseChecker

    class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
        # See ``CommonBaseTestUtils.HIDppHelper``
        @classmethod
        def start_session(cls, test_case, account_name, device_index=None, port_index=None, software_id=None,
                          padding=None, reserved=None):
            """
            Send ``StartSession`` Request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param account_name: Account name, expressed as a UTF-8 string (except 0)
            :type account_name: ``str``
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

            :return: StartSession response
            :rtype: ``BitFieldContainerMixin``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def start_session

        @classmethod
        def passwd0(cls, test_case, passwd, device_index=None, port_index=None, software_id=None, padding=None,
                    reserved=None):
            """
            Send ``Passwd0`` Request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param passwd: Password
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

            :return: Passwd0 response
            :rtype: ``BitFieldContainerMixin``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def passwd0

        @classmethod
        def get_password0_from_name(cls, account_name):
            """
            Get password for given account name

            :param account_name: Account name
            :type account_name: ``str``

            :return: The password of account name
            :rtype: ``str | HexList``

            :raise ``AssertionError``: Assert passwd0 that raise an exception
            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def get_password0_from_name

        @classmethod
        def authenticate_and_validate(cls, test_case, start_session_response, account_name):
            """
            Check the password response sequence by sending the passwd0
            and also passwd1 (if long password is set)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param start_session_response: StartSessionResponse to check
            :type start_session_response: ``BitFieldContainerMixin``
            :param account_name: Account name
            :type account_name: ``str``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def authenticate_and_validate

        @classmethod
        def get_feature_interface(cls, test_case):
            """
            Get interface for ``PasswordAuthentication`` request and response classes

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Password Authentication interface
            :rtype: ``FeatureInterface``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def get_feature_interface

        @classmethod
        def get_passwd0_cls_req(cls, test_case, passwd):
            """
            Get password0 request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param passwd: Password
            :type passwd: ``str | HexList``

            :return: Password0 request class
            :rtype: ``BitFieldContainerMixin``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def get_passwd0_cls_req

        @classmethod
        def get_start_session_cls_req(cls, test_case, account_name):
            """
            Get start session request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param account_name: Account name
            :type account_name: ``str | HexList``

            :return: Start session request
            :rtype: ``BitFieldContainerMixin``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def get_start_session_cls_req

        @classmethod
        def start_session_and_authenticate(cls, test_case, account_name):
            """
            Start session with given account name and authenticate

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param account_name: Account name
            :type account_name: ``str``

            :raise ``NotImplementedAbstractMethodError``: Throw error if child does not implement
            """
            raise NotImplementedAbstractMethodError()
        # end def start_session_and_authenticate
    # end class HIDppHelper
# end class SharedPasswordAuthenticationTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
