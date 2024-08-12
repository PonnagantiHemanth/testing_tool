#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.keepalive_test
:brief: HID++ 2.0 ``KeepAlive`` test module
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.keepalive import GetTimeoutRangeRequest
from pyhid.hidpp.features.common.keepalive import GetTimeoutRangeResponse
from pyhid.hidpp.features.common.keepalive import KeepAliveRequest
from pyhid.hidpp.features.common.keepalive import KeepAliveFactory
from pyhid.hidpp.features.common.keepalive import KeepAliveResponse
from pyhid.hidpp.features.common.keepalive import KeepAliveTimeoutEventV1
from pyhid.hidpp.features.common.keepalive import KeepAliveV0
from pyhid.hidpp.features.common.keepalive import KeepAliveV1
from pyhid.hidpp.features.common.keepalive import TerminateRequest
from pyhid.hidpp.features.common.keepalive import TerminateResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeepAliveInstantiationTestCase(TestCase):
    """
    Test ``KeepAlive`` testing classes instantiations
    """

    @staticmethod
    def test_keep_alive_feature():
        """
        Test ``KeepAlive`` class instantiation
        """
        my_class = KeepAliveRequest(device_index=0, feature_index=0, requested_timeout=HexList(0))

        RootTestCase._top_level_class_checker(my_class)

        my_class = KeepAliveRequest(device_index=0xFF, feature_index=0xFF, requested_timeout=HexList(0xFF))

        RootTestCase._top_level_class_checker(my_class)
    # end def test_keep_alive_feature

    @staticmethod
    def test_get_timeout_range():
        """
        Test ``GetTimeoutRangeRequest`` class instantiation
        """
        my_class = GetTimeoutRangeRequest(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetTimeoutRangeRequest(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_timeout_range

    @staticmethod
    def test_keep_alive():
        """
        Test ``KeepAlive`` class instantiation
        """
        my_class = KeepAliveRequest(device_index=0, feature_index=0, requested_timeout=HexList(0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = KeepAliveRequest(
            device_index=0xFF, feature_index=0xFF,
            requested_timeout=HexList("FF" * (KeepAliveRequest.LEN.REQUESTED_TIMEOUT // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_keep_alive

    @staticmethod
    def test_terminate():
        """
        Test ``TerminateRequest`` class instantiation
        """
        my_class = TerminateRequest(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = TerminateRequest(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_terminate

    @staticmethod
    def test_get_timeout_range_response():
        """
        Test ``GetTimeoutRangeResponse`` class instantiation
        """
        my_class = GetTimeoutRangeResponse(
            device_index=0, feature_index=0,
            timeout_minimum=HexList(0), timeout_maximum=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetTimeoutRangeResponse(
            device_index=0xFF, feature_index=0xFF,
            timeout_minimum=HexList("FF" * (GetTimeoutRangeResponse.LEN.TIMEOUT_MINIMUM // 8)),
            timeout_maximum=HexList("FF" * (GetTimeoutRangeResponse.LEN.TIMEOUT_MAXIMUM // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_timeout_range_response

    @staticmethod
    def test_keep_alive_response():
        """
        Test ``KeepAliveResponse`` class instantiation
        """
        my_class = KeepAliveResponse(device_index=0, feature_index=0, final_timeout=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = KeepAliveResponse(
            device_index=0xFF, feature_index=0xFF,
            final_timeout=HexList("FF" * (KeepAliveResponse.LEN.FINAL_TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_keep_alive_response

    @staticmethod
    def test_terminate_response():
        """
        Test ``TerminateResponse`` class instantiation
        """
        my_class = TerminateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = TerminateResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_terminate_response

    @staticmethod
    def test_keep_alive_timeout_event_v1():
        """
        Test ``KeepAliveTimeoutEventV1`` class instantiation
        """
        my_class = KeepAliveTimeoutEventV1(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = KeepAliveTimeoutEventV1(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_keep_alive_timeout_event_v1
# end class KeepAliveInstantiationTestCase


class KeepAliveTestCase(TestCase):
    """
    Test ``KeepAlive`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            KeepAliveV0.VERSION: {
                "cls": KeepAliveV0,
                "interfaces": {
                    "get_timeout_range_cls": GetTimeoutRangeRequest,
                    "get_timeout_range_response_cls": GetTimeoutRangeResponse,
                    "keep_alive_cls": KeepAliveRequest,
                    "keep_alive_response_cls": KeepAliveResponse,
                    "terminate_cls": TerminateRequest,
                    "terminate_response_cls": TerminateResponse,
                },
                "max_function_index": 2
            },
            KeepAliveV1.VERSION: {
                "cls": KeepAliveV1,
                "interfaces": {
                    "get_timeout_range_cls": GetTimeoutRangeRequest,
                    "get_timeout_range_response_cls": GetTimeoutRangeResponse,
                    "keep_alive_cls": KeepAliveRequest,
                    "keep_alive_response_cls": KeepAliveResponse,
                    "terminate_cls": TerminateRequest,
                    "terminate_response_cls": TerminateResponse,
                    "keep_alive_timeout_event_cls": KeepAliveTimeoutEventV1,
                },
                "max_function_index": 2
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``KeepAliveFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(KeepAliveFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``KeepAliveFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                KeepAliveFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``KeepAliveFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = KeepAliveFactory.create(version)
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
            obj = KeepAliveFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class KeepAliveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
