#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.test.passwordauthentication_test
:brief: HID++ 2.0 ``PasswordAuthentication`` test module
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choices
from string import ascii_uppercase
from string import digits
from unittest import TestCase

from pyhid.hidpp.features.common.passwordauthentication import EndSession
from pyhid.hidpp.features.common.passwordauthentication import EndSessionResponse
from pyhid.hidpp.features.common.passwordauthentication import Passwd0
from pyhid.hidpp.features.common.passwordauthentication import Passwd0Response
from pyhid.hidpp.features.common.passwordauthentication import Passwd1
from pyhid.hidpp.features.common.passwordauthentication import Passwd1Response
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationFactory
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationV0
from pyhid.hidpp.features.common.passwordauthentication import StartSession
from pyhid.hidpp.features.common.passwordauthentication import StartSessionResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PasswordAuthenticationInstantiationTestCase(TestCase):
    """
    Test ``PasswordAuthentication`` testing classes instantiations
    """

    @staticmethod
    def test_password_authentication():
        """
        Test ``PasswordAuthentication`` class instantiation
        """
        my_class = PasswordAuthentication(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = PasswordAuthentication(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_password_authentication

    @staticmethod
    def test_start_session():
        """
        Test ``StartSession`` class instantiation
        """
        my_class = StartSession(device_index=0, feature_index=0,
                                account_name=''.join(choices(ascii_uppercase + digits, k=1)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartSession(device_index=0xFF, feature_index=0xFF,
                                account_name=''.join(choices(ascii_uppercase + digits, k=16)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_session

    @staticmethod
    def test_end_session():
        """
        Test ``EndSession`` class instantiation
        """
        my_class = EndSession(device_index=0, feature_index=0,
                              account_name=''.join(choices(ascii_uppercase + digits, k=1)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = EndSession(device_index=0xFF, feature_index=0xFF,
                              account_name=''.join(choices(ascii_uppercase + digits, k=16)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_end_session

    @staticmethod
    def test_passwd0():
        """
        Test ``Passwd0`` class instantiation
        """
        my_class = Passwd0(device_index=0, feature_index=0,
                           passwd=''.join(choices(ascii_uppercase + digits, k=1)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = Passwd0(device_index=0xFF, feature_index=0xFF,
                           passwd=''.join(choices(ascii_uppercase + digits, k=16)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_passwd0

    @staticmethod
    def test_passwd1():
        """
        Test ``Passwd1`` class instantiation
        """
        my_class = Passwd1(device_index=0, feature_index=0,
                           passwd=''.join(choices(ascii_uppercase + digits, k=1)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = Passwd1(device_index=0xFF, feature_index=0xFF,
                           passwd=''.join(choices(ascii_uppercase + digits, k=16)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_passwd1

    @staticmethod
    def test_start_session_response():
        """
        Test ``StartSessionResponse`` class instantiation
        """
        my_class = StartSessionResponse(device_index=0, feature_index=0,
                                        long_password=False,
                                        full_authentication=False,
                                        constant_credentials=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartSessionResponse(device_index=0xFF, feature_index=0xFF,
                                        long_password=True,
                                        full_authentication=True,
                                        constant_credentials=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_session_response

    @staticmethod
    def test_end_session_response():
        """
        Test ``EndSessionResponse`` class instantiation
        """
        my_class = EndSessionResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EndSessionResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_end_session_response

    @staticmethod
    def test_passwd0_response():
        """
        Test ``Passwd0Response`` class instantiation
        """
        my_class = Passwd0Response(device_index=0, feature_index=0,
                                   status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = Passwd0Response(device_index=0xFF, feature_index=0xFF,
                                   status=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_passwd0_response

    @staticmethod
    def test_passwd1_response():
        """
        Test ``Passwd1Response`` class instantiation
        """
        my_class = Passwd1Response(device_index=0, feature_index=0,
                                   status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = Passwd1Response(device_index=0xFF, feature_index=0xFF,
                                   status=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_passwd1_response
# end class PasswordAuthenticationInstantiationTestCase


class PasswordAuthenticationTestCase(TestCase):
    """
    Test ``PasswordAuthentication`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            PasswordAuthenticationV0.VERSION: {
                "cls": PasswordAuthenticationV0,
                "interfaces": {
                    "start_session_cls": StartSession,
                    "start_session_response_cls": StartSessionResponse,
                    "end_session_cls": EndSession,
                    "end_session_response_cls": EndSessionResponse,
                    "passwd0_cls": Passwd0,
                    "passwd0_response_cls": Passwd0Response,
                    "passwd1_cls": Passwd1,
                    "passwd1_response_cls": Passwd1Response,
                },
                "max_function_index": 3
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``PasswordAuthenticationFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(PasswordAuthenticationFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``PasswordAuthenticationFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                PasswordAuthenticationFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``PasswordAuthenticationFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = PasswordAuthenticationFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = PasswordAuthenticationFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class PasswordAuthenticationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
