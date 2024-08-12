#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.keyboard.test.keyboardinternationallayouts_test
:brief: HID++ 2.0 ``KeyboardInternationalLayouts`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import GetKeyboardLayout
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import GetKeyboardLayoutResponse
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayoutsFactory
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayoutsV0
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayoutsV1
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardInternationalLayoutsInstantiationTestCase(TestCase):
    """
    Test ``KeyboardInternationalLayouts`` testing classes instantiations
    """

    @staticmethod
    def test_keyboard_international_layouts():
        """
        Test ``KeyboardInternationalLayouts`` class instantiation
        """
        my_class = KeyboardInternationalLayouts(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = KeyboardInternationalLayouts(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_keyboard_international_layouts

    @staticmethod
    def test_get_keyboard_layout():
        """
        Test ``GetKeyboardLayout`` class instantiation
        """
        my_class = GetKeyboardLayout(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetKeyboardLayout(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_keyboard_layout

    @staticmethod
    def test_get_keyboard_layout_response():
        """
        Test ``GetKeyboardLayoutResponse`` class instantiation
        """
        my_class = GetKeyboardLayoutResponse(device_index=0, feature_index=0,
                                             keyboard_layout=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetKeyboardLayoutResponse(device_index=0xff, feature_index=0xff,
                                             keyboard_layout=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_keyboard_layout_response
# end class KeyboardInternationalLayoutsInstantiationTestCase


class KeyboardInternationalLayoutsTestCase(TestCase):
    """
    Test ``KeyboardInternationalLayouts`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            KeyboardInternationalLayoutsV0.VERSION: {
                "cls": KeyboardInternationalLayoutsV0,
                "interfaces": {
                    "get_keyboard_layout_cls": GetKeyboardLayout,
                    "get_keyboard_layout_response_cls": GetKeyboardLayoutResponse,
                },
                "max_function_index": 0
            },
            KeyboardInternationalLayoutsV1.VERSION: {
                "cls": KeyboardInternationalLayoutsV1,
                "interfaces": {
                    "get_keyboard_layout_cls": GetKeyboardLayout,
                    "get_keyboard_layout_response_cls": GetKeyboardLayoutResponse,
                },
                "max_function_index": 0
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``KeyboardInternationalLayoutsFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(KeyboardInternationalLayoutsFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``KeyboardInternationalLayoutsFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                KeyboardInternationalLayoutsFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``KeyboardInternationalLayoutsFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = KeyboardInternationalLayoutsFactory.create(version)
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
            obj = KeyboardInternationalLayoutsFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class KeyboardInternationalLayoutsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
