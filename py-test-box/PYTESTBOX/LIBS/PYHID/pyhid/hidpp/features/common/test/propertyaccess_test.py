#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.propertyaccess_test
:brief: HID++ 2.0 ``PropertyAccess`` test module
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.propertyaccess import GetPropertyInfo
from pyhid.hidpp.features.common.propertyaccess import GetPropertyInfoResponse
from pyhid.hidpp.features.common.propertyaccess import PropertyAccess
from pyhid.hidpp.features.common.propertyaccess import PropertyAccessFactory
from pyhid.hidpp.features.common.propertyaccess import PropertyAccessV0
from pyhid.hidpp.features.common.propertyaccess import ReadProperty
from pyhid.hidpp.features.common.propertyaccess import ReadPropertyResponse
from pyhid.hidpp.features.common.propertyaccess import SelectProperty
from pyhid.hidpp.features.common.propertyaccess import SelectPropertyResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PropertyAccessInstantiationTestCase(TestCase):
    """
    Test ``PropertyAccess`` testing classes instantiations
    """

    @staticmethod
    def test_property_access():
        """
        Test ``PropertyAccess`` class instantiation
        """
        my_class = PropertyAccess(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = PropertyAccess(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_property_access

    @staticmethod
    def test_get_property_info():
        """
        Test ``GetPropertyInfo`` class instantiation
        """
        my_class = GetPropertyInfo(device_index=0, feature_index=0,
                                   property_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetPropertyInfo(device_index=0xFF, feature_index=0xFF,
                                   property_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_property_info

    @staticmethod
    def test_select_property():
        """
        Test ``SelectProperty`` class instantiation
        """
        my_class = SelectProperty(device_index=0, feature_index=0,
                                  property_id=0,
                                  rd_offset=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SelectProperty(device_index=0xFF, feature_index=0xFF,
                                  property_id=0xFF,
                                  rd_offset=0xFFFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_select_property

    @staticmethod
    def test_read_property():
        """
        Test ``ReadProperty`` class instantiation
        """
        my_class = ReadProperty(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadProperty(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_property

    @staticmethod
    def test_get_property_info_response():
        """
        Test ``GetPropertyInfoResponse`` class instantiation
        """
        my_class = GetPropertyInfoResponse(device_index=0, feature_index=0,
                                           corrupted=False,
                                           present=False,
                                           supported=False,
                                           size=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPropertyInfoResponse(device_index=0xFF, feature_index=0xFF,
                                           corrupted=True,
                                           present=True,
                                           supported=True,
                                           size=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_property_info_response

    @staticmethod
    def test_select_property_response():
        """
        Test ``SelectPropertyResponse`` class instantiation
        """
        my_class = SelectPropertyResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SelectPropertyResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_select_property_response

    @staticmethod
    def test_read_property_response():
        """
        Test ``ReadPropertyResponse`` class instantiation
        """
        my_class = ReadPropertyResponse(device_index=0, feature_index=0,
                                        data=HexList("00" * (ReadPropertyResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadPropertyResponse(device_index=0xFF, feature_index=0xFF,
                                        data=HexList("FF" * (ReadPropertyResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_property_response
# end class PropertyAccessInstantiationTestCase


class PropertyAccessTestCase(TestCase):
    """
    Test ``PropertyAccess`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            PropertyAccessV0.VERSION: {
                "cls": PropertyAccessV0,
                "interfaces": {
                    "get_property_info_cls": GetPropertyInfo,
                    "get_property_info_response_cls": GetPropertyInfoResponse,
                    "select_property_cls": SelectProperty,
                    "select_property_response_cls": SelectPropertyResponse,
                    "read_property_cls": ReadProperty,
                    "read_property_response_cls": ReadPropertyResponse,
                },
                "max_function_index": 2
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``PropertyAccessFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(PropertyAccessFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``PropertyAccessFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                PropertyAccessFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``PropertyAccessFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = PropertyAccessFactory.create(version)
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
            obj = PropertyAccessFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class PropertyAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
