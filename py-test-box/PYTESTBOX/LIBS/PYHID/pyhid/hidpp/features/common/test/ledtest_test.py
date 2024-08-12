#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.ledtest_test
:brief: HID++ 2.0 ``LEDTest`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.ledtest import GetLEDList
from pyhid.hidpp.features.common.ledtest import GetLEDListResponse
from pyhid.hidpp.features.common.ledtest import GetLEDTestMode
from pyhid.hidpp.features.common.ledtest import GetLEDTestModeResponse
from pyhid.hidpp.features.common.ledtest import LEDTest
from pyhid.hidpp.features.common.ledtest import LEDTestFactory
from pyhid.hidpp.features.common.ledtest import LEDTestV0
from pyhid.hidpp.features.common.ledtest import SetLEDTestMode
from pyhid.hidpp.features.common.ledtest import SetLEDTestModeResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LEDTestInstantiationTestCase(TestCase):
    """
    Test ``LEDTest`` testing classes instantiations
    """

    @staticmethod
    def test_led_test():
        """
        Test ``LEDTest`` class instantiation
        """
        my_class = LEDTest(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = LEDTest(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_led_test

    @staticmethod
    def test_get_led_list():
        """
        Test ``GetLEDList`` class instantiation
        """
        my_class = GetLEDList(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetLEDList(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_led_list

    @staticmethod
    def test_get_led_test_mode():
        """
        Test ``GetLEDTestMode`` class instantiation
        """
        my_class = GetLEDTestMode(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetLEDTestMode(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_led_test_mode

    @staticmethod
    def test_set_led_test_mode():
        """
        Test ``SetLEDTestMode`` class instantiation
        """
        my_class = SetLEDTestMode(device_index=0, feature_index=0,
                                  battery_green_led=0,
                                  battery_red_led=0,
                                  roller_led=0,
                                  capslock_led=0,
                                  backlight_led=0,
                                  rgb=0,
                                  reserved=0,
                                  led_mask_presence_2=0,
                                  product_specific_led_0=0,
                                  product_specific_led_1=0,
                                  product_specific_led_2=0,
                                  product_specific_led_3=0,
                                  product_specific_led_4=0,
                                  product_specific_led_5=0,
                                  product_specific_led_6=0,
                                  product_specific_led_7=0,
                                  product_specific_led_8=0,
                                  product_specific_led_9=0,
                                  product_specific_led_10=0,
                                  product_specific_led_11=0,
                                  product_specific_led_12=0,
                                  product_specific_led_13=0,
                                  product_specific_led_14=0,
                                  product_specific_led_15=0,
                                  product_specific_led_16=0,
                                  product_specific_led_17=0,
                                  product_specific_led_18=0,
                                  product_specific_led_19=0,
                                  product_specific_led_20=0,
                                  product_specific_led_21=0,
                                  product_specific_led_22=0,
                                  product_specific_led_23=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLEDTestMode(device_index=0xFF, feature_index=0xFF,
                                  battery_green_led=0x1,
                                  battery_red_led=0x1,
                                  roller_led=0x1,
                                  capslock_led=0x1,
                                  backlight_led=0x1,
                                  rgb=0x1,
                                  reserved=0x3,
                                  led_mask_presence_2=0xFF,
                                  product_specific_led_0=0x1,
                                  product_specific_led_1=0x1,
                                  product_specific_led_2=0x1,
                                  product_specific_led_3=0x1,
                                  product_specific_led_4=0x1,
                                  product_specific_led_5=0x1,
                                  product_specific_led_6=0x1,
                                  product_specific_led_7=0x1,
                                  product_specific_led_8=0x1,
                                  product_specific_led_9=0x1,
                                  product_specific_led_10=0x1,
                                  product_specific_led_11=0x1,
                                  product_specific_led_12=0x1,
                                  product_specific_led_13=0x1,
                                  product_specific_led_14=0x1,
                                  product_specific_led_15=0x1,
                                  product_specific_led_16=0x1,
                                  product_specific_led_17=0x1,
                                  product_specific_led_18=0x1,
                                  product_specific_led_19=0x1,
                                  product_specific_led_20=0x1,
                                  product_specific_led_21=0x1,
                                  product_specific_led_22=0x1,
                                  product_specific_led_23=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_led_test_mode

    @staticmethod
    def test_get_led_list_response():
        """
        Test ``GetLEDListResponse`` class instantiation
        """
        my_class = GetLEDListResponse(device_index=0, feature_index=0,
                                      battery_green_led=0,
                                      battery_red_led=0,
                                      roller_led=0,
                                      capslock_led=0,
                                      backlight_led=0,
                                      rgb=0,
                                      reserved=0,
                                      led_mask_presence_2=0,
                                      product_specific_led_0=0,
                                      product_specific_led_1=0,
                                      product_specific_led_2=0,
                                      product_specific_led_3=0,
                                      product_specific_led_4=0,
                                      product_specific_led_5=0,
                                      product_specific_led_6=0,
                                      product_specific_led_7=0,
                                      product_specific_led_8=0,
                                      product_specific_led_9=0,
                                      product_specific_led_10=0,
                                      product_specific_led_11=0,
                                      product_specific_led_12=0,
                                      product_specific_led_13=0,
                                      product_specific_led_14=0,
                                      product_specific_led_15=0,
                                      product_specific_led_16=0,
                                      product_specific_led_17=0,
                                      product_specific_led_18=0,
                                      product_specific_led_19=0,
                                      product_specific_led_20=0,
                                      product_specific_led_21=0,
                                      product_specific_led_22=0,
                                      product_specific_led_23=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetLEDListResponse(device_index=0xFF, feature_index=0xFF,
                                      battery_green_led=0x1,
                                      battery_red_led=0x1,
                                      roller_led=0x1,
                                      capslock_led=0x1,
                                      backlight_led=0x1,
                                      rgb=0x1,
                                      reserved=0x3,
                                      led_mask_presence_2=0xFF,
                                      product_specific_led_0=0x1,
                                      product_specific_led_1=0x1,
                                      product_specific_led_2=0x1,
                                      product_specific_led_3=0x1,
                                      product_specific_led_4=0x1,
                                      product_specific_led_5=0x1,
                                      product_specific_led_6=0x1,
                                      product_specific_led_7=0x1,
                                      product_specific_led_8=0x1,
                                      product_specific_led_9=0x1,
                                      product_specific_led_10=0x1,
                                      product_specific_led_11=0x1,
                                      product_specific_led_12=0x1,
                                      product_specific_led_13=0x1,
                                      product_specific_led_14=0x1,
                                      product_specific_led_15=0x1,
                                      product_specific_led_16=0x1,
                                      product_specific_led_17=0x1,
                                      product_specific_led_18=0x1,
                                      product_specific_led_19=0x1,
                                      product_specific_led_20=0x1,
                                      product_specific_led_21=0x1,
                                      product_specific_led_22=0x1,
                                      product_specific_led_23=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_led_list_response

    @staticmethod
    def test_get_led_test_mode_response():
        """
        Test ``GetLEDTestModeResponse`` class instantiation
        """
        my_class = GetLEDTestModeResponse(device_index=0, feature_index=0,
                                          battery_green_led=0,
                                          battery_red_led=0,
                                          roller_led=0,
                                          capslock_led=0,
                                          backlight_led=0,
                                          rgb=0,
                                          reserved=0,
                                          led_mask_presence_2=0,
                                          product_specific_led_0=0,
                                          product_specific_led_1=0,
                                          product_specific_led_2=0,
                                          product_specific_led_3=0,
                                          product_specific_led_4=0,
                                          product_specific_led_5=0,
                                          product_specific_led_6=0,
                                          product_specific_led_7=0,
                                          product_specific_led_8=0,
                                          product_specific_led_9=0,
                                          product_specific_led_10=0,
                                          product_specific_led_11=0,
                                          product_specific_led_12=0,
                                          product_specific_led_13=0,
                                          product_specific_led_14=0,
                                          product_specific_led_15=0,
                                          product_specific_led_16=0,
                                          product_specific_led_17=0,
                                          product_specific_led_18=0,
                                          product_specific_led_19=0,
                                          product_specific_led_20=0,
                                          product_specific_led_21=0,
                                          product_specific_led_22=0,
                                          product_specific_led_23=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetLEDTestModeResponse(device_index=0xFF, feature_index=0xFF,
                                          battery_green_led=0x1,
                                          battery_red_led=0x1,
                                          roller_led=0x1,
                                          capslock_led=0x1,
                                          backlight_led=0x1,
                                          rgb=0x1,
                                          reserved=0x3,
                                          led_mask_presence_2=0xFF,
                                          product_specific_led_0=0x1,
                                          product_specific_led_1=0x1,
                                          product_specific_led_2=0x1,
                                          product_specific_led_3=0x1,
                                          product_specific_led_4=0x1,
                                          product_specific_led_5=0x1,
                                          product_specific_led_6=0x1,
                                          product_specific_led_7=0x1,
                                          product_specific_led_8=0x1,
                                          product_specific_led_9=0x1,
                                          product_specific_led_10=0x1,
                                          product_specific_led_11=0x1,
                                          product_specific_led_12=0x1,
                                          product_specific_led_13=0x1,
                                          product_specific_led_14=0x1,
                                          product_specific_led_15=0x1,
                                          product_specific_led_16=0x1,
                                          product_specific_led_17=0x1,
                                          product_specific_led_18=0x1,
                                          product_specific_led_19=0x1,
                                          product_specific_led_20=0x1,
                                          product_specific_led_21=0x1,
                                          product_specific_led_22=0x1,
                                          product_specific_led_23=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_led_test_mode_response

    @staticmethod
    def test_set_led_test_mode_response():
        """
        Test ``SetLEDTestModeResponse`` class instantiation
        """
        my_class = SetLEDTestModeResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLEDTestModeResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_led_test_mode_response
# end class LEDTestInstantiationTestCase


class LEDTestTestCase(TestCase):
    """
    Test ``LEDTest`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            LEDTestV0.VERSION: {
                "cls": LEDTestV0,
                "interfaces": {
                    "get_led_list_cls": GetLEDList,
                    "get_led_list_response_cls": GetLEDListResponse,
                    "get_led_test_mode_cls": GetLEDTestMode,
                    "get_led_test_mode_response_cls": GetLEDTestModeResponse,
                    "set_led_test_mode_cls": SetLEDTestMode,
                    "set_led_test_mode_response_cls": SetLEDTestModeResponse,
                },
                "max_function_index": 2
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``LEDTestFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(LEDTestFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``LEDTestFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                LEDTestFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``LEDTestFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = LEDTestFactory.create(version)
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
            obj = LEDTestFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class LEDTestTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
