#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.ledtestutils
:brief: Helpers for ``LEDTest`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.ledtest import GetLEDListResponse
from pyhid.hidpp.features.common.ledtest import GetLEDTestModeResponse
from pyhid.hidpp.features.common.ledtest import LEDTest
from pyhid.hidpp.features.common.ledtest import LEDTestFactory
from pyhid.hidpp.features.common.ledtest import SetLEDTestModeResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LEDTestTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``LEDTest`` feature
    """

    class LEDMaskPresence1BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDMaskPresence1BitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "battery_green_led": (cls.check_battery_green_led, int(config.F_BatteryGreenLED)),
                "battery_red_led": (cls.check_battery_red_led, int(config.F_BatteryRedLED)),
                "roller_led": (cls.check_roller_led, int(config.F_RollerLED)),
                "caps_lock_led": (cls.check_caps_lock_led, int(config.F_CapsLockLED)),
                "backlight_led": (cls.check_backlight_led, int(config.F_BacklightLED)),
                "rgb": (cls.check_rgb, int(config.F_RGB)),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_battery_green_led(test_case, bitmap, expected):
            """
            Check battery_green_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert battery_green_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The battery_green_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.battery_green_led),
                msg="The battery_green_led parameter differs from the one expected")
        # end def check_battery_green_led

        @staticmethod
        def check_battery_red_led(test_case, bitmap, expected):
            """
            Check battery_red_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert battery_red_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The battery_red_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.battery_red_led),
                msg="The battery_red_led parameter differs from the one expected")
        # end def check_battery_red_led

        @staticmethod
        def check_roller_led(test_case, bitmap, expected):
            """
            Check roller_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert roller_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The roller_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.roller_led),
                msg="The roller_led parameter differs from the one expected")
        # end def check_roller_led

        @staticmethod
        def check_caps_lock_led(test_case, bitmap, expected):
            """
            Check caps_lock_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert caps_lock_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The caps_lock_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.caps_lock_led),
                msg="The caps_lock_led parameter differs from the one expected")
        # end def check_caps_lock_led

        @staticmethod
        def check_backlight_led(test_case, bitmap, expected):
            """
            Check backlight_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert backlight_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The backlight_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.backlight_led),
                msg="The backlight_led parameter differs from the one expected")
        # end def check_backlight_led

        @staticmethod
        def check_rgb(test_case, bitmap, expected):
            """
            Check rgb field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert rgb that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The rgb shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.rgb),
                msg="The rgb parameter differs from the one expected")
        # end def check_rgb

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class LEDMaskPresence1BitMapChecker

    class LEDGenericMaskPresence1BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDGenericMaskPresence1BitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "product_specific_led_0": (cls.check_product_specific_led_0, int(config.F_ProductSpecificLED0)),
                "product_specific_led_1": (cls.check_product_specific_led_1, int(config.F_ProductSpecificLED1)),
                "product_specific_led_2": (cls.check_product_specific_led_2, int(config.F_ProductSpecificLED2)),
                "product_specific_led_3": (cls.check_product_specific_led_3, int(config.F_ProductSpecificLED3)),
                "product_specific_led_4": (cls.check_product_specific_led_4, int(config.F_ProductSpecificLED4)),
                "product_specific_led_5": (cls.check_product_specific_led_5, int(config.F_ProductSpecificLED5)),
                "product_specific_led_6": (cls.check_product_specific_led_6, int(config.F_ProductSpecificLED6)),
                "product_specific_led_7": (cls.check_product_specific_led_7, int(config.F_ProductSpecificLED7))
            }
        # end def get_default_check_map

        @staticmethod
        def check_product_specific_led_0(test_case, bitmap, expected):
            """
            Check product_specific_led_0 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_0 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_0),
                msg="The product_specific_led_0 parameter differs from the one expected")
        # end def check_product_specific_led_0

        @staticmethod
        def check_product_specific_led_1(test_case, bitmap, expected):
            """
            Check product_specific_led_1 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_1 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_1),
                msg="The product_specific_led_1 parameter differs from the one expected")
        # end def check_product_specific_led_1

        @staticmethod
        def check_product_specific_led_2(test_case, bitmap, expected):
            """
            Check product_specific_led_2 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_2 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_2),
                msg="The product_specific_led_2 parameter differs from the one expected")
        # end def check_product_specific_led_2

        @staticmethod
        def check_product_specific_led_3(test_case, bitmap, expected):
            """
            Check product_specific_led_3 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_3 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_3 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_3),
                msg="The product_specific_led_3 parameter differs from the one expected")
        # end def check_product_specific_led_3

        @staticmethod
        def check_product_specific_led_4(test_case, bitmap, expected):
            """
            Check product_specific_led_4 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_4 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_4 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_4),
                msg="The product_specific_led_4 parameter differs from the one expected")
        # end def check_product_specific_led_4

        @staticmethod
        def check_product_specific_led_5(test_case, bitmap, expected):
            """
            Check product_specific_led_5 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_5 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_5 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_5),
                msg="The product_specific_led_5 parameter differs from the one expected")
        # end def check_product_specific_led_5

        @staticmethod
        def check_product_specific_led_6(test_case, bitmap, expected):
            """
            Check product_specific_led_6 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_6 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_6 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_6),
                msg="The product_specific_led_6 parameter differs from the one expected")
        # end def check_product_specific_led_6

        @staticmethod
        def check_product_specific_led_7(test_case, bitmap, expected):
            """
            Check product_specific_led_7 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_7 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_7 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_7),
                msg="The product_specific_led_7 parameter differs from the one expected")
        # end def check_product_specific_led_7
    # end class LEDGenericMaskPresence1BitMapChecker

    class LEDGenericMaskPresence2BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDGenericMaskPresence2BitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "product_specific_led_8": (cls.check_product_specific_led_8, int(config.F_ProductSpecificLED8)),
                "product_specific_led_9": (cls.check_product_specific_led_9, int(config.F_ProductSpecificLED9)),
                "product_specific_led_10": (cls.check_product_specific_led_10, int(config.F_ProductSpecificLED10)),
                "product_specific_led_11": (cls.check_product_specific_led_11, int(config.F_ProductSpecificLED11)),
                "product_specific_led_12": (cls.check_product_specific_led_12, int(config.F_ProductSpecificLED12)),
                "product_specific_led_13": (cls.check_product_specific_led_13, int(config.F_ProductSpecificLED13)),
                "product_specific_led_14": (cls.check_product_specific_led_14, int(config.F_ProductSpecificLED14)),
                "product_specific_led_15": (cls.check_product_specific_led_15, int(config.F_ProductSpecificLED15))
            }
        # end def get_default_check_map

        @staticmethod
        def check_product_specific_led_8(test_case, bitmap, expected):
            """
            Check product_specific_led_8 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_8 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_8 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_8),
                msg="The product_specific_led_8 parameter differs from the one expected")
        # end def check_product_specific_led_8

        @staticmethod
        def check_product_specific_led_9(test_case, bitmap, expected):
            """
            Check product_specific_led_9 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_9 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_9 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_9),
                msg="The product_specific_led_9 parameter differs from the one expected")
        # end def check_product_specific_led_9

        @staticmethod
        def check_product_specific_led_10(test_case, bitmap, expected):
            """
            Check product_specific_led_10 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_10 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_10 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_10),
                msg="The product_specific_led_10 parameter differs from the one expected")
        # end def check_product_specific_led_10

        @staticmethod
        def check_product_specific_led_11(test_case, bitmap, expected):
            """
            Check product_specific_led_11 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_11 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_11 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_11),
                msg="The product_specific_led_11 parameter differs from the one expected")
        # end def check_product_specific_led_11

        @staticmethod
        def check_product_specific_led_12(test_case, bitmap, expected):
            """
            Check product_specific_led_12 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_12 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_12 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_12),
                msg="The product_specific_led_12 parameter differs from the one expected")
        # end def check_product_specific_led_12

        @staticmethod
        def check_product_specific_led_13(test_case, bitmap, expected):
            """
            Check product_specific_led_13 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_13 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_13 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_13),
                msg="The product_specific_led_13 parameter differs from the one expected")
        # end def check_product_specific_led_13

        @staticmethod
        def check_product_specific_led_14(test_case, bitmap, expected):
            """
            Check product_specific_led_14 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_14 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_14 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_14),
                msg="The product_specific_led_14 parameter differs from the one expected")
        # end def check_product_specific_led_14

        @staticmethod
        def check_product_specific_led_15(test_case, bitmap, expected):
            """
            Check product_specific_led_15 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_15 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_15 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_15),
                msg="The product_specific_led_15 parameter differs from the one expected")
        # end def check_product_specific_led_15
    # end class LEDGenericMaskPresence2BitMapChecker

    class LEDGenericMaskPresence3BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDGenericMaskPresence3BitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "product_specific_led_16": (cls.check_product_specific_led_16, int(config.F_ProductSpecificLED16)),
                "product_specific_led_17": (cls.check_product_specific_led_17, int(config.F_ProductSpecificLED17)),
                "product_specific_led_18": (cls.check_product_specific_led_18, int(config.F_ProductSpecificLED18)),
                "product_specific_led_19": (cls.check_product_specific_led_19, int(config.F_ProductSpecificLED19)),
                "product_specific_led_20": (cls.check_product_specific_led_20, int(config.F_ProductSpecificLED20)),
                "product_specific_led_21": (cls.check_product_specific_led_21, int(config.F_ProductSpecificLED21)),
                "product_specific_led_22": (cls.check_product_specific_led_22, int(config.F_ProductSpecificLED22)),
                "product_specific_led_23": (cls.check_product_specific_led_23, int(config.F_ProductSpecificLED23))
            }
        # end def get_default_check_map

        @staticmethod
        def check_product_specific_led_16(test_case, bitmap, expected):
            """
            Check product_specific_led_16 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_16 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_16 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_16),
                msg="The product_specific_led_16 parameter differs from the one expected")
        # end def check_product_specific_led_16

        @staticmethod
        def check_product_specific_led_17(test_case, bitmap, expected):
            """
            Check product_specific_led_17 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_17 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_17 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_17),
                msg="The product_specific_led_17 parameter differs from the one expected")
        # end def check_product_specific_led_17

        @staticmethod
        def check_product_specific_led_18(test_case, bitmap, expected):
            """
            Check product_specific_led_18 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_18 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_18 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_18),
                msg="The product_specific_led_18 parameter differs from the one expected")
        # end def check_product_specific_led_18

        @staticmethod
        def check_product_specific_led_19(test_case, bitmap, expected):
            """
            Check product_specific_led_19 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_19 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_19 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_19),
                msg="The product_specific_led_19 parameter differs from the one expected")
        # end def check_product_specific_led_19

        @staticmethod
        def check_product_specific_led_20(test_case, bitmap, expected):
            """
            Check product_specific_led_20 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_20 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_20 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_20),
                msg="The product_specific_led_20 parameter differs from the one expected")
        # end def check_product_specific_led_20

        @staticmethod
        def check_product_specific_led_21(test_case, bitmap, expected):
            """
            Check product_specific_led_21 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_21 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_21 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_21),
                msg="The product_specific_led_21 parameter differs from the one expected")
        # end def check_product_specific_led_21

        @staticmethod
        def check_product_specific_led_22(test_case, bitmap, expected):
            """
            Check product_specific_led_22 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_22 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_22 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_22),
                msg="The product_specific_led_22 parameter differs from the one expected")
        # end def check_product_specific_led_22

        @staticmethod
        def check_product_specific_led_23(test_case, bitmap, expected):
            """
            Check product_specific_led_23 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskPresence3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskPresence3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_23 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_23 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_23),
                msg="The product_specific_led_23 parameter differs from the one expected")
        # end def check_product_specific_led_23
    # end class LEDGenericMaskPresence3BitMapChecker

    class GetLEDListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetLEDListResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "led_mask_presence_1": (
                    cls.check_led_mask_presence_1,
                    LEDTestTestUtils.LEDMaskPresence1BitMapChecker.get_default_check_map(test_case)),
                "reserved_led_mask_presence_2": (cls.check_reserved_led_mask_presence_2, 0),
                "led_generic_mask_presence_1": (
                    cls.check_led_generic_mask_presence_1,
                    LEDTestTestUtils.LEDGenericMaskPresence1BitMapChecker.get_default_check_map(test_case)),
                "led_generic_mask_presence_2": (
                    cls.check_led_generic_mask_presence_2,
                    LEDTestTestUtils.LEDGenericMaskPresence2BitMapChecker.get_default_check_map(test_case)),
                "led_generic_mask_presence_3": (
                    cls.check_led_generic_mask_presence_3,
                    LEDTestTestUtils.LEDGenericMaskPresence3BitMapChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_led_mask_presence_1(test_case, message, expected):
            """
            Check ``led_mask_presence_1``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDListResponse to check
            :type message: ``GetLEDListResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDMaskPresence1BitMapChecker.check_fields(
                test_case, message.led_mask_presence_1, LEDTest.LEDMaskPresence1BitMap, expected)
        # end def check_led_mask_presence_1

        @staticmethod
        def check_reserved_led_mask_presence_2(test_case, response, expected):
            """
            Check reserved_led_mask_presence_2 field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetLEDListResponse to check
            :type response: ``GetLEDListResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved_led_mask_presence_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved_led_mask_presence_2 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved_led_mask_presence_2),
                msg="The reserved_led_mask_presence_2 parameter differs from the one expected")
        # end def check_reserved_led_mask_presence_2

        @staticmethod
        def check_led_generic_mask_presence_1(test_case, message, expected):
            """
            Check ``led_generic_mask_presence_1``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDListResponse to check
            :type message: ``GetLEDListResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDGenericMaskPresence1BitMapChecker.check_fields(
                test_case, message.led_generic_mask_presence_1, LEDTest.LEDGenericMaskPresence1BitMap, expected)
        # end def check_led_generic_mask_presence_1

        @staticmethod
        def check_led_generic_mask_presence_2(test_case, message, expected):
            """
            Check ``led_generic_mask_presence_2``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDListResponse to check
            :type message: ``GetLEDListResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDGenericMaskPresence2BitMapChecker.check_fields(
                test_case, message.led_generic_mask_presence_2, LEDTest.LEDGenericMaskPresence2BitMap, expected)
        # end def check_led_generic_mask_presence_2

        @staticmethod
        def check_led_generic_mask_presence_3(test_case, message, expected):
            """
            Check ``led_generic_mask_presence_3``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDListResponse to check
            :type message: ``GetLEDListResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDGenericMaskPresence3BitMapChecker.check_fields(
                test_case, message.led_generic_mask_presence_3, LEDTest.LEDGenericMaskPresence3BitMap, expected)
        # end def check_led_generic_mask_presence_3
    # end class GetLEDListResponseChecker

    class LEDMaskState1BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDMaskState1BitMap``
        """

        @classmethod
        def get_check_map(cls, test_case, battery_green_led=0, battery_red_led=0, roller_led=0, caps_lock_led=0,
                          backlight_led=0, rgb=0, **kwargs):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param battery_green_led: 0=> Turn Battery Green LED to OFF state
                1=> Battery Green LED to ON state - OPTIONAL.
            :type battery_green_led: ``bool | int``
            :param battery_red_led: 0=> Turn Battery Red LED to off state. 1=> Battery Red LED to ON state - OPTIONAL.
            :type battery_red_led: ``bool | int``
            :param roller_led: 0=> Turn Roller LED to OFF state. 1=> Turn Roller LED to ON state - OPTIONAL.
            :type roller_led: ``bool | int``
            :param caps_lock_led: 0=> Turn Caps Lock LED to OFF state. 1=> Turn Caps Lock LED to ON state - OPTIONAL.
            :type caps_lock_led: ``bool | int``
            :param backlight_led: 0=> Turn Backlight LED to OFF state. 1=> Turn Backlight LED to ON state - OPTIONAL.
            :type backlight_led: ``bool | int``
            :param rgb: 0=> Turn RGB LED to OFF state. 1=> Turn RGB LED to ON state - OPTIONAL.
            :type rgb: ``bool | int``
            :param kwargs: Keyword arguments
            :type kwargs: ``dict``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "battery_green_led": (cls.check_battery_green_led, battery_green_led),
                "battery_red_led": (cls.check_battery_red_led, battery_red_led),
                "roller_led": (cls.check_roller_led, roller_led),
                "caps_lock_led": (cls.check_caps_lock_led, caps_lock_led),
                "backlight_led": (cls.check_backlight_led, backlight_led),
                "rgb": (cls.check_rgb, rgb),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_check_map

        @staticmethod
        def check_battery_green_led(test_case, bitmap, expected):
            """
            Check battery_green_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert battery_green_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The battery_green_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.battery_green_led),
                msg="The battery_green_led parameter differs from the one expected")
        # end def check_battery_green_led

        @staticmethod
        def check_battery_red_led(test_case, bitmap, expected):
            """
            Check battery_red_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert battery_red_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The battery_red_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.battery_red_led),
                msg="The battery_red_led parameter differs from the one expected")
        # end def check_battery_red_led

        @staticmethod
        def check_roller_led(test_case, bitmap, expected):
            """
            Check roller_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert roller_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The roller_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.roller_led),
                msg="The roller_led parameter differs from the one expected")
        # end def check_roller_led

        @staticmethod
        def check_caps_lock_led(test_case, bitmap, expected):
            """
            Check caps_lock_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert caps_lock_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The caps_lock_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.caps_lock_led),
                msg="The caps_lock_led parameter differs from the one expected")
        # end def check_caps_lock_led

        @staticmethod
        def check_backlight_led(test_case, bitmap, expected):
            """
            Check backlight_led field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert backlight_led that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The backlight_led shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.backlight_led),
                msg="The backlight_led parameter differs from the one expected")
        # end def check_backlight_led

        @staticmethod
        def check_rgb(test_case, bitmap, expected):
            """
            Check rgb field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert rgb that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The rgb shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.rgb),
                msg="The rgb parameter differs from the one expected")
        # end def check_rgb

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class LEDMaskState1BitMapChecker

    class LEDGenericMaskState1BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDGenericMaskState1BitMap``
        """

        @classmethod
        def get_check_map(cls, test_case, product_specific_led_0=0, product_specific_led_1=0, product_specific_led_2=0,
                          product_specific_led_3=0, product_specific_led_4=0, product_specific_led_5=0,
                          product_specific_led_6=0, product_specific_led_7=0, **kwargs):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param product_specific_led_0: 0=> Turn Product Specific LED 0 to OFF state.
                                           1=> Turn Product Specific LED 0 to ON state - OPTIONAL.
            :type product_specific_led_0: ``bool | int``
            :param product_specific_led_1: 0=> Turn Product Specific LED 1 to OFF state.
                                           1=> Turn Product Specific LED 1 to ON state - OPTIONAL.
            :type product_specific_led_1: ``bool | int``
            :param product_specific_led_2: 0=> Turn Product Specific LED 2 to OFF state.
                                           1=> Turn Product Specific LED 2 to ON state - OPTIONAL.
            :type product_specific_led_2: ``bool | int``
            :param product_specific_led_3: 0=> Turn Product Specific LED 3 to OFF state.
                                           1=> Turn Product Specific LED 3 to ON state - OPTIONAL.
            :type product_specific_led_3: ``bool | int``
            :param product_specific_led_4: 0=> Turn Product Specific LED 4 to OFF state.
                                           1=> Turn Product Specific LED 4 to ON state - OPTIONAL.
            :type product_specific_led_4: ``bool | int``
            :param product_specific_led_5: 0=> Turn Product Specific LED 5 to OFF state.
                                           1=> Turn Product Specific LED 5 to ON state - OPTIONAL.
            :type product_specific_led_5: ``bool | int``
            :param product_specific_led_6: 0=> Turn Product Specific LED 6 to OFF state.
                                           1=> Turn Product Specific LED 6 to ON state - OPTIONAL.
            :type product_specific_led_6: ``bool | int``
            :param product_specific_led_7: 0=> Turn Product Specific LED 7 to OFF state.
                                           1=> Turn Product Specific LED 7 to ON state - OPTIONAL.
            :type product_specific_led_7: ``bool | int``
            :param kwargs: Keyword arguments
            :type kwargs: ``dict``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "product_specific_led_0": (cls.check_product_specific_led_0, product_specific_led_0),
                "product_specific_led_1": (cls.check_product_specific_led_1, product_specific_led_1),
                "product_specific_led_2": (cls.check_product_specific_led_2, product_specific_led_2),
                "product_specific_led_3": (cls.check_product_specific_led_3, product_specific_led_3),
                "product_specific_led_4": (cls.check_product_specific_led_4, product_specific_led_4),
                "product_specific_led_5": (cls.check_product_specific_led_5, product_specific_led_5),
                "product_specific_led_6": (cls.check_product_specific_led_6, product_specific_led_6),
                "product_specific_led_7": (cls.check_product_specific_led_7, product_specific_led_7)
            }
        # end def get_default_check_map

        @staticmethod
        def check_product_specific_led_0(test_case, bitmap, expected):
            """
            Check product_specific_led_0 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_0 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_0),
                msg="The product_specific_led_0 parameter differs from the one expected")
        # end def check_product_specific_led_0

        @staticmethod
        def check_product_specific_led_1(test_case, bitmap, expected):
            """
            Check product_specific_led_1 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_1 shall be be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_1),
                msg="The product_specific_led_1 parameter differs from the one expected")
        # end def check_product_specific_led_1

        @staticmethod
        def check_product_specific_led_2(test_case, bitmap, expected):
            """
            Check product_specific_led_2 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_2 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_2),
                msg="The product_specific_led_2 parameter differs from the one expected")
        # end def check_product_specific_led_2

        @staticmethod
        def check_product_specific_led_3(test_case, bitmap, expected):
            """
            Check product_specific_led_3 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_3 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_3 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_3),
                msg="The product_specific_led_3 parameter differs from the one expected")
        # end def check_product_specific_led_3

        @staticmethod
        def check_product_specific_led_4(test_case, bitmap, expected):
            """
            Check product_specific_led_4 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_4 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_4 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_4),
                msg="The product_specific_led_4 parameter differs from the one expected")
        # end def check_product_specific_led_4

        @staticmethod
        def check_product_specific_led_5(test_case, bitmap, expected):
            """
            Check product_specific_led_5 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_5 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_5 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_5),
                msg="The product_specific_led_5 parameter differs from the one expected")
        # end def check_product_specific_led_5

        @staticmethod
        def check_product_specific_led_6(test_case, bitmap, expected):
            """
            Check product_specific_led_6 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_6 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_6 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_6),
                msg="The product_specific_led_6 parameter differs from the one expected")
        # end def check_product_specific_led_6

        @staticmethod
        def check_product_specific_led_7(test_case, bitmap, expected):
            """
            Check product_specific_led_7 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState1BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState1BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_7 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_7 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_7),
                msg="The product_specific_led_7 parameter differs from the one expected")
        # end def check_product_specific_led_7
    # end class LEDGenericMaskState1BitMapChecker

    class LEDGenericMaskState2BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDGenericMaskState2BitMap``
        """

        @classmethod
        def get_check_map(cls, test_case, product_specific_led_8=0, product_specific_led_9=0, product_specific_led_10=0,
                          product_specific_led_11=0, product_specific_led_12=0, product_specific_led_13=0,
                          product_specific_led_14=0, product_specific_led_15=0, **kwargs):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :type product_specific_led_8: ``bool | int``
            :param product_specific_led_9: 0=> Turn Product Specific LED 9 to OFF state.
                                           1=> Turn Product Specific LED 9 to ON state - OPTIONAL.
            :type product_specific_led_9: ``bool | int``
            :param product_specific_led_10: 0=> Turn Product Specific LED 10 to OFF state.
                                            1=> Turn Product Specific LED 10 to ON state - OPTIONAL.
            :type product_specific_led_10: ``bool | int``
            :param product_specific_led_11: 0=> Turn Product Specific LED 11 to OFF state.
                                            1=> Turn Product Specific LED 11 to ON state - OPTIONAL.
            :type product_specific_led_11: ``bool | int``
            :param product_specific_led_12: 0=> Turn Product Specific LED 12 to OFF state.
                                            1=> Turn Product Specific LED 12 to ON state - OPTIONAL.
            :type product_specific_led_12: ``bool | int``
            :param product_specific_led_13: 0=> Turn Product Specific LED 13 to OFF state.
                                            1=> Turn Product Specific LED 13 to ON state - OPTIONAL.
            :type product_specific_led_13: ``bool | int``
            :param product_specific_led_14: 0=> Turn Product Specific LED 14 to OFF state.
                                            1=> Turn Product Specific LED 14 to ON state - OPTIONAL.
            :type product_specific_led_14: ``bool | int``
            :param product_specific_led_15: 0=> Turn Product Specific LED 15 to OFF state.
                                            1=> Turn Product Specific LED 15 to ON state - OPTIONAL.
            :type product_specific_led_15: ``bool | int``
            :param kwargs: Keyword arguments
            :type kwargs: ``dict``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "product_specific_led_8": (cls.check_product_specific_led_8, product_specific_led_8),
                "product_specific_led_9": (cls.check_product_specific_led_9, product_specific_led_9),
                "product_specific_led_10": (cls.check_product_specific_led_10, product_specific_led_10),
                "product_specific_led_11": (cls.check_product_specific_led_11, product_specific_led_11),
                "product_specific_led_12": (cls.check_product_specific_led_12, product_specific_led_12),
                "product_specific_led_13": (cls.check_product_specific_led_13, product_specific_led_13),
                "product_specific_led_14": (cls.check_product_specific_led_14, product_specific_led_14),
                "product_specific_led_15": (cls.check_product_specific_led_15, product_specific_led_15)
            }
        # end def get_default_check_map

        @staticmethod
        def check_product_specific_led_8(test_case, bitmap, expected):
            """
            Check product_specific_led_8 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_8 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_8 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_8),
                msg="The product_specific_led_8 parameter differs from the one expected")
        # end def check_product_specific_led_8

        @staticmethod
        def check_product_specific_led_9(test_case, bitmap, expected):
            """
            Check product_specific_led_9 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_9 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_9 shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_9),
                msg="The product_specific_led_9 parameter differs from the one expected")
        # end def check_product_specific_led_9

        @staticmethod
        def check_product_specific_led_10(test_case, bitmap, expected):
            """
            Check product_specific_led_10 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_10 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_10 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_10),
                msg="The product_specific_led_10 parameter differs from the one expected")
        # end def check_product_specific_led_10

        @staticmethod
        def check_product_specific_led_11(test_case, bitmap, expected):
            """
            Check product_specific_led_11 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_11 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_11 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_11),
                msg="The product_specific_led_11 parameter differs from the one expected")
        # end def check_product_specific_led_11

        @staticmethod
        def check_product_specific_led_12(test_case, bitmap, expected):
            """
            Check product_specific_led_12 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_12 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_12 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_12),
                msg="The product_specific_led_12 parameter differs from the one expected")
        # end def check_product_specific_led_12

        @staticmethod
        def check_product_specific_led_13(test_case, bitmap, expected):
            """
            Check product_specific_led_13 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_13 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_13 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_13),
                msg="The product_specific_led_13 parameter differs from the one expected")
        # end def check_product_specific_led_13

        @staticmethod
        def check_product_specific_led_14(test_case, bitmap, expected):
            """
            Check product_specific_led_14 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_14 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_14 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_14),
                msg="The product_specific_led_14 parameter differs from the one expected")
        # end def check_product_specific_led_14

        @staticmethod
        def check_product_specific_led_15(test_case, bitmap, expected):
            """
            Check product_specific_led_15 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState2BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState2BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_15 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_15 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_15),
                msg="The product_specific_led_15 parameter differs from the one expected")
        # end def check_product_specific_led_15
    # end class LEDGenericMaskState2BitMapChecker

    class LEDGenericMaskState3BitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LEDGenericMaskState3BitMap``
        """

        @classmethod
        def get_check_map(cls, test_case, product_specific_led_16=0, product_specific_led_17=0,
                          product_specific_led_18=0, product_specific_led_19=0, product_specific_led_20=0,
                          product_specific_led_21=0, product_specific_led_22=0, product_specific_led_23=0, **kwargs):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param product_specific_led_16: 0=> Turn Product Specific LED 16 to OFF state.
                                            1=> Turn Product Specific LED 16 to ON state - OPTIONAL.
            :type product_specific_led_16: ``bool | int``
            :param product_specific_led_17: 0=> Turn Product Specific LED 17 to OFF state.
                                            1=> Turn Product Specific LED 17 to ON state - OPTIONAL.
            :type product_specific_led_17: ``bool | int``
            :param product_specific_led_18: 0=> Turn Product Specific LED 18 to OFF state.
                                            1=> Turn Product Specific LED 18 to ON state - OPTIONAL.
            :type product_specific_led_18: ``bool | int``
            :param product_specific_led_19: 0=> Turn Product Specific LED 19 to OFF state.
                                            1=> Turn Product Specific LED 19 to ON state - OPTIONAL.
            :type product_specific_led_19: ``bool | int``
            :param product_specific_led_20: 0=> Turn Product Specific LED 20 to OFF state.
                                            1=> Turn Product Specific LED 20 to ON state - OPTIONAL.
            :type product_specific_led_20: ``bool | int``
            :param product_specific_led_21: 0=> Turn Product Specific LED 21 to OFF state.
                                            1=> Turn Product Specific LED 21 to ON state - OPTIONAL.
            :type product_specific_led_21: ``bool | int``
            :param product_specific_led_22: 0=> Turn Product Specific LED 22 to OFF state.
                                            1=> Turn Product Specific LED 22 to ON state - OPTIONAL.
            :type product_specific_led_22: ``bool | int``
            :param product_specific_led_23: 0=> Turn Product Specific LED 23 to OFF state.
                                            1=> Turn Product Specific LED 23 to ON state - OPTIONAL.
            :type product_specific_led_23: ``bool | int``
            :param kwargs: Keyword arguments
            :type kwargs: ``dict``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "product_specific_led_16": (cls.check_product_specific_led_16, product_specific_led_16),
                "product_specific_led_17": (cls.check_product_specific_led_17, product_specific_led_17),
                "product_specific_led_18": (cls.check_product_specific_led_18, product_specific_led_18),
                "product_specific_led_19": (cls.check_product_specific_led_19, product_specific_led_19),
                "product_specific_led_20": (cls.check_product_specific_led_20, product_specific_led_20),
                "product_specific_led_21": (cls.check_product_specific_led_21, product_specific_led_21),
                "product_specific_led_22": (cls.check_product_specific_led_22, product_specific_led_22),
                "product_specific_led_23": (cls.check_product_specific_led_23, product_specific_led_23)
            }
        # end def get_default_check_map

        @staticmethod
        def check_product_specific_led_16(test_case, bitmap, expected):
            """
            Check product_specific_led_16 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_16 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_16 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_16),
                msg="The product_specific_led_16 parameter differs from the one expected")
        # end def check_product_specific_led_16

        @staticmethod
        def check_product_specific_led_17(test_case, bitmap, expected):
            """
            Check product_specific_led_17 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_17 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_17 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_17),
                msg="The product_specific_led_17 parameter differs from the one expected")
        # end def check_product_specific_led_17

        @staticmethod
        def check_product_specific_led_18(test_case, bitmap, expected):
            """
            Check product_specific_led_18 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_18 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_18 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_18),
                msg="The product_specific_led_18 parameter differs from the one expected")
        # end def check_product_specific_led_18

        @staticmethod
        def check_product_specific_led_19(test_case, bitmap, expected):
            """
            Check product_specific_led_19 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_19 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_19 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_19),
                msg="The product_specific_led_19 parameter differs from the one expected")
        # end def check_product_specific_led_19

        @staticmethod
        def check_product_specific_led_20(test_case, bitmap, expected):
            """
            Check product_specific_led_20 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_20 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_20 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_20),
                msg="The product_specific_led_20 parameter differs from the one expected")
        # end def check_product_specific_led_20

        @staticmethod
        def check_product_specific_led_21(test_case, bitmap, expected):
            """
            Check product_specific_led_21 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_21 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_21 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_21),
                msg="The product_specific_led_21 parameter differs from the one expected")
        # end def check_product_specific_led_21

        @staticmethod
        def check_product_specific_led_22(test_case, bitmap, expected):
            """
            Check product_specific_led_22 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_22 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_22 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_22),
                msg="The product_specific_led_22 parameter differs from the one expected")
        # end def check_product_specific_led_22

        @staticmethod
        def check_product_specific_led_23(test_case, bitmap, expected):
            """
            Check product_specific_led_23 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LEDGenericMaskState3BitMap to check
            :type bitmap: ``LEDTest.LEDGenericMaskState3BitMap``
            :param expected: Expected value
            :type expected: ``bool | int``

            :raise ``AssertionError``: Assert product_specific_led_23 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The product_specific_led_23 shall be passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.product_specific_led_23),
                msg="The product_specific_led_23 parameter differs from the one expected")
        # end def check_product_specific_led_23
    # end class LEDGenericMaskState3BitMapChecker

    class LEDTestModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define common Helper to check ``GetLEDTestModeResponse`` and ``SetLEDTestModeResponse``
        """

        @classmethod
        def get_check_map(cls, test_case, **kwargs):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST
            return {
                "led_mask_state_1": (
                    cls.check_led_mask_state_1,
                    LEDTestTestUtils.LEDMaskState1BitMapChecker.get_check_map(test_case, **kwargs)),
                "reserved_led_mask_state_2": (cls.check_reserved_led_mask_state_2, 0),
                "led_generic_mask_state_1": (
                    cls.check_led_generic_mask_state_1,
                    LEDTestTestUtils.LEDGenericMaskState1BitMapChecker.get_check_map(test_case, **kwargs)),
                "led_generic_mask_state_2": (
                    cls.check_led_generic_mask_state_2,
                    LEDTestTestUtils.LEDGenericMaskState2BitMapChecker.get_check_map(test_case, **kwargs)),
                "led_generic_mask_state_3": (
                    cls.check_led_generic_mask_state_3,
                    LEDTestTestUtils.LEDGenericMaskState3BitMapChecker.get_check_map(test_case, **kwargs))
            }
        # end def get_check_map

        @staticmethod
        def check_led_mask_state_1(test_case, message, expected):
            """
            Check ``led_mask_state_1``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDTestModeResponse or SetLEDTestModeResponse to check
            :type message: ``GetLEDTestModeResponse | SetLEDTestModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDMaskState1BitMapChecker.check_fields(
                test_case, message.led_mask_state_1, LEDTest.LEDMaskState1BitMap, expected)
        # end def check_led_mask_state_1

        @staticmethod
        def check_reserved_led_mask_state_2(test_case, response, expected):
            """
            Check reserved_led_mask_state_2 field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetLEDTestModeResponse or SetLEDTestModeResponse to check
            :type response: ``GetLEDTestModeResponse | SetLEDTestModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved_led_mask_state_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved_led_mask_state_2 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved_led_mask_state_2),
                msg="The reserved_led_mask_state_2 parameter differs from the one expected")
        # end def check_reserved_led_mask_state_2

        @staticmethod
        def check_led_generic_mask_state_1(test_case, message, expected):
            """
            Check ``led_generic_mask_state_1``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDTestModeResponse or SetLEDTestModeResponse to check
            :type message: ``GetLEDTestModeResponse | SetLEDTestModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDGenericMaskState1BitMapChecker.check_fields(
                test_case, message.led_generic_mask_state_1, LEDTest.LEDGenericMaskState1BitMap, expected)
        # end def check_led_generic_mask_state_1

        @staticmethod
        def check_led_generic_mask_state_2(test_case, message, expected):
            """
            Check ``led_generic_mask_state_2``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDTestModeResponse or SetLEDTestModeResponse to check
            :type message: ``GetLEDTestModeResponse | SetLEDTestModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDGenericMaskState2BitMapChecker.check_fields(
                test_case, message.led_generic_mask_state_2, LEDTest.LEDGenericMaskState2BitMap, expected)
        # end def check_led_generic_mask_state_2

        @staticmethod
        def check_led_generic_mask_state_3(test_case, message, expected):
            """
            Check ``led_generic_mask_state_3``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLEDTestModeResponse or SetLEDTestModeResponse to check
            :type message: ``GetLEDTestModeResponse | SetLEDTestModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LEDTestTestUtils.LEDGenericMaskState3BitMapChecker.check_fields(
                test_case, message.led_generic_mask_state_3, LEDTest.LEDGenericMaskState3BitMap, expected)
        # end def check_led_generic_mask_state_3
    # end class GetLEDTestModeResponseChecker

    class GetLEDTestModeResponseChecker(LEDTestModeResponseChecker):
        """
        Define Helper to check ``SetLEDTestModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case)
        # end def get_default_check_map
    # end class GetLEDTestModeResponseChecker

    class SetLEDTestModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetLEDTestModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {}
        # end def get_default_check_map
    # end class SetLEDTestModeResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):

        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=LEDTest.FEATURE_ID, factory=LEDTestFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(test_case, feature_id, factory, device_index, port_index, update_test_case,
                                          skip_not_found)
        # end def get_parameters

        @classmethod
        def get_led_list(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetLEDList``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetLEDListResponse
            :rtype: ``GetLEDListResponse``
            """
            feature_18a1_index, feature_18a1, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_18a1.get_led_list_cls(
                device_index=device_index,
                feature_index=feature_18a1_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_18a1.get_led_list_response_cls)
        # end def get_led_list

        @classmethod
        def get_led_test_mode(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetLEDTestMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetLEDTestModeResponse
            :rtype: ``GetLEDTestModeResponse``
            """
            feature_18a1_index, feature_18a1, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_18a1.get_led_test_mode_cls(
                device_index=device_index,
                feature_index=feature_18a1_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_18a1.get_led_test_mode_response_cls)
        # end def get_led_test_mode

        @classmethod
        def set_led_test_mode(cls, test_case, battery_green_led=0, battery_red_led=0, roller_led=0, caps_lock_led=0,
                              backlight_led=0, rgb=0, product_specific_led_0=0, product_specific_led_1=0,
                              product_specific_led_2=0, product_specific_led_3=0, product_specific_led_4=0,
                              product_specific_led_5=0, product_specific_led_6=0, product_specific_led_7=0,
                              product_specific_led_8=0, product_specific_led_9=0, product_specific_led_10=0,
                              product_specific_led_11=0, product_specific_led_12=0, product_specific_led_13=0,
                              product_specific_led_14=0, product_specific_led_15=0, product_specific_led_16=0,
                              product_specific_led_17=0, product_specific_led_18=0, product_specific_led_19=0,
                              product_specific_led_20=0, product_specific_led_21=0, product_specific_led_22=0,
                              product_specific_led_23=0, device_index=None, port_index=None, software_id=None,
                              padding=None, reserved=None, **kwargs):
            """
            Process ``SetLEDTestMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param battery_green_led: 0=> Turn Battery Green LED to OFF state.
                                      1=> Battery Green LED to ON state - OPTIONAL.
            :type battery_green_led: ``bool | int``
            :param battery_red_led: 0=> Turn Battery Red LED to off state. 1=> Battery Red LED to ON state - OPTIONAL.
            :type battery_red_led: ``bool | int``
            :param roller_led: 0=> Turn Roller LED to OFF state. 1=> Turn Roller LED to ON state - OPTIONAL.
            :type roller_led: ``bool | int``
            :param caps_lock_led: 0=> Turn Caps Lock LED to OFF state. 1=> Turn Caps Lock LED to ON state - OPTIONAL.
            :type caps_lock_led: ``bool | int``
            :param backlight_led: 0=> Turn Backlight LED to OFF state. 1=> Turn Backlight LED to ON state - OPTIONAL.
            :type backlight_led: ``bool | int``
            :param rgb: 0=> Turn RGB LED to OFF state. 1=> Turn RGB LED to ON state - OPTIONAL.
            :type rgb: ``bool | int``
            :param product_specific_led_0: 0=> Turn Product Specific LED 0 to OFF state.
                                           1=> Turn Product Specific LED 0 to ON state - OPTIONAL.
            :type product_specific_led_0: ``bool | int``
            :param product_specific_led_1: 0=> Turn Product Specific LED 1 to OFF state.
                                           1=> Turn Product Specific LED 1 to ON state - OPTIONAL.
            :type product_specific_led_1: ``bool | int``
            :param product_specific_led_2: 0=> Turn Product Specific LED 2 to OFF state.
                                           1=> Turn Product Specific LED 2 to ON state - OPTIONAL.
            :type product_specific_led_2: ``bool | int``
            :param product_specific_led_3: 0=> Turn Product Specific LED 3 to OFF state.
                                           1=> Turn Product Specific LED 3 to ON state - OPTIONAL.
            :type product_specific_led_3: ``bool | int``
            :param product_specific_led_4: 0=> Turn Product Specific LED 4 to OFF state.
                                           1=> Turn Product Specific LED 4 to ON state - OPTIONAL.
            :type product_specific_led_4: ``bool | int``
            :param product_specific_led_5: 0=> Turn Product Specific LED 5 to OFF state.
                                           1=> Turn Product Specific LED 5 to ON state - OPTIONAL.
            :type product_specific_led_5: ``bool | int``
            :param product_specific_led_6: 0=> Turn Product Specific LED 6 to OFF state.
                                           1=> Turn Product Specific LED 6 to ON state - OPTIONAL.
            :type product_specific_led_6: ``bool | int``
            :param product_specific_led_7: 0=> Turn Product Specific LED 7 to OFF state.
                                           1=> Turn Product Specific LED 7 to ON state - OPTIONAL.
            :type product_specific_led_7: ``bool | int``
            :param product_specific_led_8: 0=> Turn Product Specific LED 8 to OFF state.
                                           1=> Turn Product Specific LED 8 to ON state - OPTIONAL.
            :type product_specific_led_8: ``bool | int``
            :param product_specific_led_9: 0=> Turn Product Specific LED 9 to OFF state.
                                           1=> Turn Product Specific LED 9 to ON state - OPTIONAL.
            :type product_specific_led_9: ``bool | int``
            :param product_specific_led_10: 0=> Turn Product Specific LED 10 to OFF state.
                                            1=> Turn Product Specific LED 10 to ON state - OPTIONAL.
            :type product_specific_led_10: ``bool | int``
            :param product_specific_led_11: 0=> Turn Product Specific LED 11 to OFF state.
                                            1=> Turn Product Specific LED 11 to ON state - OPTIONAL.
            :type product_specific_led_11: ``bool | int``
            :param product_specific_led_12: 0=> Turn Product Specific LED 12 to OFF state.
                                            1=> Turn Product Specific LED 12 to ON state - OPTIONAL.
            :type product_specific_led_12: ``bool | int``
            :param product_specific_led_13: 0=> Turn Product Specific LED 13 to OFF state.
                                            1=> Turn Product Specific LED 13 to ON state - OPTIONAL.
            :type product_specific_led_13: ``bool | int``
            :param product_specific_led_14: 0=> Turn Product Specific LED 14 to OFF state.
                                            1=> Turn Product Specific LED 14 to ON state - OPTIONAL.
            :type product_specific_led_14: ``bool | int``
            :param product_specific_led_15: 0=> Turn Product Specific LED 15 to OFF state.
                                            1=> Turn Product Specific LED 15 to ON state - OPTIONAL.
            :type product_specific_led_15: ``bool | int``
            :param product_specific_led_16: 0=> Turn Product Specific LED 16 to OFF state.
                                            1=> Turn Product Specific LED 16 to ON state - OPTIONAL.
            :type product_specific_led_16: ``bool | int``
            :param product_specific_led_17: 0=> Turn Product Specific LED 17 to OFF state.
                                            1=> Turn Product Specific LED 17 to ON state - OPTIONAL.
            :type product_specific_led_17: ``bool | int``
            :param product_specific_led_18: 0=> Turn Product Specific LED 18 to OFF state.
                                            1=> Turn Product Specific LED 18 to ON state - OPTIONAL.
            :type product_specific_led_18: ``bool | int``
            :param product_specific_led_19: 0=> Turn Product Specific LED 19 to OFF state.
                                            1=> Turn Product Specific LED 19 to ON state - OPTIONAL.
            :type product_specific_led_19: ``bool | int``
            :param product_specific_led_20: 0=> Turn Product Specific LED 20 to OFF state.
                                            1=> Turn Product Specific LED 20 to ON state - OPTIONAL.
            :type product_specific_led_20: ``bool | int``
            :param product_specific_led_21: 0=> Turn Product Specific LED 21 to OFF state.
                                            1=> Turn Product Specific LED 21 to ON state - OPTIONAL.
            :type product_specific_led_21: ``bool | int``
            :param product_specific_led_22: 0=> Turn Product Specific LED 22 to OFF state.
                                            1=> Turn Product Specific LED 22 to ON state - OPTIONAL.
            :type product_specific_led_22: ``bool | int``
            :param product_specific_led_23: 0=> Turn Product Specific LED 23 to OFF state.
                                            1=> Turn Product Specific LED 23 to ON state - OPTIONAL.
            :type product_specific_led_23: ``bool | int``
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
            :param kwargs: Keyword arguments
            :type kwargs: ``dict``

            :return: SetLEDTestModeResponse
            :rtype: ``SetLEDTestModeResponse``
            """
            feature_18a1_index, feature_18a1, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_18a1.set_led_test_mode_cls(
                device_index=device_index,
                feature_index=feature_18a1_index,
                battery_green_led=battery_green_led,
                battery_red_led=battery_red_led,
                roller_led=roller_led,
                caps_lock_led=caps_lock_led,
                backlight_led=backlight_led,
                rgb=rgb,
                product_specific_led_0=product_specific_led_0,
                product_specific_led_1=product_specific_led_1,
                product_specific_led_2=product_specific_led_2,
                product_specific_led_3=product_specific_led_3,
                product_specific_led_4=product_specific_led_4,
                product_specific_led_5=product_specific_led_5,
                product_specific_led_6=product_specific_led_6,
                product_specific_led_7=product_specific_led_7,
                product_specific_led_8=product_specific_led_8,
                product_specific_led_9=product_specific_led_9,
                product_specific_led_10=product_specific_led_10,
                product_specific_led_11=product_specific_led_11,
                product_specific_led_12=product_specific_led_12,
                product_specific_led_13=product_specific_led_13,
                product_specific_led_14=product_specific_led_14,
                product_specific_led_15=product_specific_led_15,
                product_specific_led_16=product_specific_led_16,
                product_specific_led_17=product_specific_led_17,
                product_specific_led_18=product_specific_led_18,
                product_specific_led_19=product_specific_led_19,
                product_specific_led_20=product_specific_led_20,
                product_specific_led_21=product_specific_led_21,
                product_specific_led_22=product_specific_led_22,
                product_specific_led_23=product_specific_led_23)

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
                response_class_type=feature_18a1.set_led_test_mode_response_cls)
        # end def set_led_test_mode
    # end class HIDppHelper

    @classmethod
    def get_led_presence_map(cls, test_case):
        """
        Return led presence information in a dictionary form

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :return: The dictionary of led presence
        :rtype: ``dict``
        """
        config = test_case.f.PRODUCT.FEATURES.COMMON.LED_TEST

        return {
            "battery_green_led": int(config.F_BatteryGreenLED),
            "battery_red_led": int(config.F_BatteryRedLED),
            "roller_led": int(config.F_RollerLED),
            "caps_lock_led": int(config.F_CapsLockLED),
            "backlight_led": int(config.F_BacklightLED),
            "rgb": int(config.F_RGB),
            "product_specific_led_0": int(config.F_ProductSpecificLED0),
            "product_specific_led_1": int(config.F_ProductSpecificLED1),
            "product_specific_led_2": int(config.F_ProductSpecificLED2),
            "product_specific_led_3": int(config.F_ProductSpecificLED3),
            "product_specific_led_4": int(config.F_ProductSpecificLED4),
            "product_specific_led_5": int(config.F_ProductSpecificLED5),
            "product_specific_led_6": int(config.F_ProductSpecificLED6),
            "product_specific_led_7": int(config.F_ProductSpecificLED7),
            "product_specific_led_8": int(config.F_ProductSpecificLED8),
            "product_specific_led_9": int(config.F_ProductSpecificLED9),
            "product_specific_led_10": int(config.F_ProductSpecificLED10),
            "product_specific_led_11": int(config.F_ProductSpecificLED11),
            "product_specific_led_12": int(config.F_ProductSpecificLED12),
            "product_specific_led_13": int(config.F_ProductSpecificLED13),
            "product_specific_led_14": int(config.F_ProductSpecificLED14),
            "product_specific_led_15": int(config.F_ProductSpecificLED15),
            "product_specific_led_16": int(config.F_ProductSpecificLED16),
            "product_specific_led_17": int(config.F_ProductSpecificLED17),
            "product_specific_led_18": int(config.F_ProductSpecificLED18),
            "product_specific_led_19": int(config.F_ProductSpecificLED19),
            "product_specific_led_20": int(config.F_ProductSpecificLED20),
            "product_specific_led_21": int(config.F_ProductSpecificLED21),
            "product_specific_led_22": int(config.F_ProductSpecificLED22),
            "product_specific_led_23": int(config.F_ProductSpecificLED23)
        }
    # end def get_led_presence_map

    @classmethod
    def get_led_state_map(cls):
        """
        Return LED state information in a dictionary form with all LEDs inactive

        :return: The dictionary of LED presence
        :rtype: ``dict``
        """
        return {
            "battery_green_led": 0,
            "battery_red_led": 0,
            "roller_led": 0,
            "caps_lock_led": 0,
            "backlight_led": 0,
            "rgb": 0,
            "product_specific_led_0": 0,
            "product_specific_led_1": 0,
            "product_specific_led_2": 0,
            "product_specific_led_3": 0,
            "product_specific_led_4": 0,
            "product_specific_led_5": 0,
            "product_specific_led_6": 0,
            "product_specific_led_7": 0,
            "product_specific_led_8": 0,
            "product_specific_led_9": 0,
            "product_specific_led_10": 0,
            "product_specific_led_11": 0,
            "product_specific_led_12": 0,
            "product_specific_led_13": 0,
            "product_specific_led_14": 0,
            "product_specific_led_15": 0,
            "product_specific_led_16": 0,
            "product_specific_led_17": 0,
            "product_specific_led_18": 0,
            "product_specific_led_19": 0,
            "product_specific_led_20": 0,
            "product_specific_led_21": 0,
            "product_specific_led_22": 0,
            "product_specific_led_23": 0
        }
    # end def get_led_state_map
# end class LEDTestTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
