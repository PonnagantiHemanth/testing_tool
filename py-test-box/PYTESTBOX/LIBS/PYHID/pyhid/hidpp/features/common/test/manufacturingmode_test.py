#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.manufacturingmode_test
:brief: HID++ 2.0 ``ManufacturingMode`` test module
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/06/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.manufacturingmode import GetManufacturingMode
from pyhid.hidpp.features.common.manufacturingmode import GetManufacturingModeResponse
from pyhid.hidpp.features.common.manufacturingmode import ManufacturingMode
from pyhid.hidpp.features.common.manufacturingmode import ManufacturingModeFactory
from pyhid.hidpp.features.common.manufacturingmode import ManufacturingModeV0
from pyhid.hidpp.features.common.manufacturingmode import SetManufacturingMode
from pyhid.hidpp.features.common.manufacturingmode import SetManufacturingModeResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ManufacturingModeInstantiationTestCase(TestCase):
    """
    Test ``ManufacturingMode`` testing classes instantiations
    """

    @staticmethod
    def test_manufacturing_mode():
        """
        Test ``ManufacturingMode`` class instantiation
        """
        my_class = ManufacturingMode(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ManufacturingMode(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_manufacturing_mode

    @staticmethod
    def test_set_manufacturing_mode():
        """
        Test ``SetManufacturingMode`` class instantiation
        """
        my_class = SetManufacturingMode(device_index=0, feature_index=0,
                                        manufacturing_mode=False)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetManufacturingMode(device_index=0xFF, feature_index=0xFF,
                                        manufacturing_mode=True)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_manufacturing_mode

    @staticmethod
    def test_get_manufacturing_mode():
        """
        Test ``GetManufacturingMode`` class instantiation
        """
        my_class = GetManufacturingMode(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetManufacturingMode(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_manufacturing_mode

    @staticmethod
    def test_set_manufacturing_mode_response():
        """
        Test ``SetManufacturingModeResponse`` class instantiation
        """
        my_class = SetManufacturingModeResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetManufacturingModeResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_manufacturing_mode_response

    @staticmethod
    def test_get_manufacturing_mode_response():
        """
        Test ``GetManufacturingModeResponse`` class instantiation
        """
        my_class = GetManufacturingModeResponse(device_index=0, feature_index=0,
                                                manufacturing_mode=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetManufacturingModeResponse(device_index=0xFF, feature_index=0xFF,
                                                manufacturing_mode=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_manufacturing_mode_response
# end class ManufacturingModeInstantiationTestCase


class ManufacturingModeTestCase(TestCase):
    """
    Test ``ManufacturingMode`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ManufacturingModeV0.VERSION: {
                "cls": ManufacturingModeV0,
                "interfaces": {
                    "set_manufacturing_mode_cls": SetManufacturingMode,
                    "set_manufacturing_mode_response_cls": SetManufacturingModeResponse,
                    "get_manufacturing_mode_cls": GetManufacturingMode,
                    "get_manufacturing_mode_response_cls": GetManufacturingModeResponse,
                },
                "max_function_index": 1
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ManufacturingModeFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ManufacturingModeFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ManufacturingModeFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                ManufacturingModeFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ManufacturingModeFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ManufacturingModeFactory.create(version)
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
            obj = ManufacturingModeFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ManufacturingModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
