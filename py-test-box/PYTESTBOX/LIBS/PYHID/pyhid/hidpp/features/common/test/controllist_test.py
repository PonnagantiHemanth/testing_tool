#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.controllist_test
:brief: HID++ 2.0 ``ControlList`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.controllist import ControlList
from pyhid.hidpp.features.common.controllist import ControlListFactory
from pyhid.hidpp.features.common.controllist import ControlListV0
from pyhid.hidpp.features.common.controllist import GetControlList
from pyhid.hidpp.features.common.controllist import GetControlListResponse
from pyhid.hidpp.features.common.controllist import GetCount
from pyhid.hidpp.features.common.controllist import GetCountResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ControlListInstantiationTestCase(TestCase):
    """
    Test ``ControlList`` testing classes instantiations
    """

    @staticmethod
    def test_control_list():
        """
        Test ``ControlList`` class instantiation
        """
        my_class = ControlList(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ControlList(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_control_list

    @staticmethod
    def test_get_count():
        """
        Test ``GetCount`` class instantiation
        """
        my_class = GetCount(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCount(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_count

    @staticmethod
    def test_get_control_list():
        """
        Test ``GetControlList`` class instantiation
        """
        my_class = GetControlList(device_index=0, feature_index=0,
                                  offset=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetControlList(device_index=0xFF, feature_index=0xFF,
                                  offset=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_control_list

    @staticmethod
    def test_get_count_response():
        """
        Test ``GetCountResponse`` class instantiation
        """
        my_class = GetCountResponse(device_index=0, feature_index=0,
                                    count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCountResponse(device_index=0xFF, feature_index=0xFF,
                                    count=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_count_response

    @staticmethod
    def test_get_control_list_response():
        """
        Test ``GetControlListResponse`` class instantiation
        """
        my_class = GetControlListResponse(device_index=0, feature_index=0,
                                          cid_0=0,
                                          cid_1=0,
                                          cid_2=0,
                                          cid_3=0,
                                          cid_4=0,
                                          cid_5=0,
                                          cid_6=0,
                                          cid_7=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetControlListResponse(device_index=0xFF, feature_index=0xFF,
                                          cid_0=HexList("FF" * (GetControlListResponse.LEN.CID_0 // 8)),
                                          cid_1=HexList("FF" * (GetControlListResponse.LEN.CID_1 // 8)),
                                          cid_2=HexList("FF" * (GetControlListResponse.LEN.CID_2 // 8)),
                                          cid_3=HexList("FF" * (GetControlListResponse.LEN.CID_3 // 8)),
                                          cid_4=HexList("FF" * (GetControlListResponse.LEN.CID_4 // 8)),
                                          cid_5=HexList("FF" * (GetControlListResponse.LEN.CID_5 // 8)),
                                          cid_6=HexList("FF" * (GetControlListResponse.LEN.CID_6 // 8)),
                                          cid_7=HexList("FF" * (GetControlListResponse.LEN.CID_7 // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_control_list_response
# end class ControlListInstantiationTestCase


class ControlListTestCase(TestCase):
    """
    Test ``ControlList`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ControlListV0.VERSION: {
                "cls": ControlListV0,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_count_response_cls": GetCountResponse,
                    "get_control_list_cls": GetControlList,
                    "get_control_list_response_cls": GetControlListResponse,
                },
                "max_function_index": 1
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ControlListFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ControlListFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ControlListFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                ControlListFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ControlListFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ControlListFactory.create(version)
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
            obj = ControlListFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ControlListTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
