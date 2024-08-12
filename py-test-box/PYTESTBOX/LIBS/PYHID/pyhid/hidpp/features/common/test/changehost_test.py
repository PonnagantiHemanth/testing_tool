#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.test.changehost_test
:brief: HID++ 2.0 ``ChangeHost`` test module
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.changehost import ChangeHost
from pyhid.hidpp.features.common.changehost import ChangeHostFactory
from pyhid.hidpp.features.common.changehost import ChangeHostV0
from pyhid.hidpp.features.common.changehost import ChangeHostV1
from pyhid.hidpp.features.common.changehost import GetCookies
from pyhid.hidpp.features.common.changehost import GetCookiesResponse
from pyhid.hidpp.features.common.changehost import GetHostInfoV0
from pyhid.hidpp.features.common.changehost import GetHostInfoV1
from pyhid.hidpp.features.common.changehost import GetHostInfoV0Response
from pyhid.hidpp.features.common.changehost import GetHostInfoV1Response
from pyhid.hidpp.features.common.changehost import SetCookie
from pyhid.hidpp.features.common.changehost import SetCookieResponse
from pyhid.hidpp.features.common.changehost import SetCurrentHost
from pyhid.hidpp.features.common.changehost import SetCurrentHostResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostInstantiationTestCase(TestCase):
    """
    Test ``ChangeHost`` testing classes instantiations
    """

    @staticmethod
    def test_change_host():
        """
        Test ``ChangeHost`` class instantiation
        """
        my_class = ChangeHost(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ChangeHost(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_change_host

    @staticmethod
    def test_get_host_info_v0():
        """
        Test ``GetHostInfoV0`` class instantiation
        """
        my_class = GetHostInfoV0(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostInfoV0(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_host_info_v0

    @staticmethod
    def test_get_host_info_v0_response():
        """
        Test ``GetHostInfoV0Response`` class instantiation
        """
        my_class = GetHostInfoV0Response(device_index=0,
                                         feature_index=0,
                                         nb_host=0,
                                         curr_host=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostInfoV0Response(device_index=0xff,
                                         feature_index=0xff,
                                         nb_host=0xff,
                                         curr_host=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_info_v0_response

    @staticmethod
    def test_get_host_info_v1():
        """
        Test ``GetHostInfoV1`` class instantiation
        """
        my_class = GetHostInfoV1(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostInfoV1(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_host_info_v1

    @staticmethod
    def test_get_host_info_v0_response():
        """
        Test ``GetHostInfoV1Response`` class instantiation
        """
        my_class = GetHostInfoV1Response(device_index=0,
                                         feature_index=0,
                                         nb_host=0,
                                         curr_host=0,
                                         rsv=0,
                                         flags=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostInfoV1Response(device_index=0xff,
                                         feature_index=0xff,
                                         nb_host=0xff,
                                         curr_host=0xff,
                                         rsv=0x7f,
                                         flags=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_info_v1_response

    @staticmethod
    def test_set_current_host():
        """
        Test ``SetCurrentHost`` class instantiation
        """
        my_class = SetCurrentHost(device_index=0, feature_index=0,
                                  host_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetCurrentHost(device_index=0xff, feature_index=0xff,
                                  host_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_current_host

    @staticmethod
    def test_set_current_host_response():
        """
        Test ``SetCurrentHostResponse`` class instantiation
        """
        my_class = SetCurrentHostResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCurrentHostResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_current_host_response

    @staticmethod
    def test_get_cookies():
        """
        Test ``GetCookies`` class instantiation
        """
        my_class = GetCookies(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCookies(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_cookies

    @staticmethod
    def test_get_cookies_response():
        """
        Test ``GetCookiesResponse`` class instantiation
        """
        my_class = GetCookiesResponse(device_index=0, feature_index=0,
                                      cookies=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCookiesResponse(device_index=0xff, feature_index=0xff,
                                      cookies=0xffffffffffffffffffffffffffffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cookies_response

    @staticmethod
    def test_set_cookie():
        """
        Test ``SetCookie`` class instantiation
        """
        my_class = SetCookie(device_index=0, feature_index=0,
                             host_index=0,
                             cookie=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetCookie(device_index=0xff, feature_index=0xff,
                             host_index=0xff,
                             cookie=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_cookie

    @staticmethod
    def test_set_cookie_response():
        """
        Test ``SetCookieResponse`` class instantiation
        """
        my_class = SetCookieResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCookieResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cookie_response
# end class ChangeHostInstantiationTestCase


class ChangeHostTestCase(TestCase):
    """
    Test ``ChangeHost`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            ChangeHostV0.VERSION: {
                "cls": ChangeHostV0,
                "interfaces": {
                    "get_host_info_cls": GetHostInfoV0,
                    "get_host_info_response_cls": GetHostInfoV0Response,
                    "set_current_host_cls": SetCurrentHost,
                    "set_current_host_response_cls": SetCurrentHostResponse,
                    "get_cookies_cls": GetCookies,
                    "get_cookies_response_cls": GetCookiesResponse,
                    "set_cookie_cls": SetCookie,
                    "set_cookie_response_cls": SetCookieResponse,
                },
                "max_function_index": 3
            },
            ChangeHostV1.VERSION: {
                "cls": ChangeHostV1,
                "interfaces": {
                    "get_host_info_cls": GetHostInfoV1,
                    "get_host_info_response_cls": GetHostInfoV1Response,
                    "set_current_host_cls": SetCurrentHost,
                    "set_current_host_response_cls": SetCurrentHostResponse,
                    "get_cookies_cls": GetCookies,
                    "get_cookies_response_cls": GetCookiesResponse,
                    "set_cookie_cls": SetCookie,
                    "set_cookie_response_cls": SetCookieResponse,
                },
                "max_function_index": 3
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ChangeHostFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ChangeHostFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ChangeHostFactory`` with out of range versions
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                ChangeHostFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ChangeHostFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = ChangeHostFactory.create(version)
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
        """
        for version, expected in self.expected.items():
            obj = ChangeHostFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ChangeHostTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
