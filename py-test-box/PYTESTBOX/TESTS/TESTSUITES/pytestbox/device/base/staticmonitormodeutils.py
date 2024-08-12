#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.staticmonitormodeutils
:brief: Helpers for ``StaticMonitorMode`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import MouseModeEvent
from pyhid.hidpp.features.common.staticmonitormode import SetMonitorModeResponse
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorMode
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorModeFactory
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class StaticMonitorModeTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``StaticMonitorMode`` feature
    """

    class SetMonitorModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetMonitorModeResponse``
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
            return {
                "mode": (
                    cls.check_mode,
                    StaticMonitorMode.OFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_mode(test_case, response, expected):
            """
            Check mode field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetMonitorModeResponse to check
            :type response: ``SetMonitorModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert mode that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Mode shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.mode),
                msg="The mode parameter differs from the one expected")
        # end def check_mode
    # end class SetMonitorModeResponseChecker

    class KeyboardModeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeyboardModeEvent``
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
            return {
                "row_col_code": (cls.check_row_col_code, HexList(0x0)),
                "break_or_make_info": (cls.check_break_or_make_info, HexList(0x0))
            }
        # end get_default_check_map

        @staticmethod
        def check_row_col_code(test_case, event, expected):
            """
            Check row_col_code field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyboardModeEvent to check
            :type event: ``KeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code),
                msg="The row_col_code parameter differs from the one expected")
        # end def check_row_col_code

        @staticmethod
        def check_break_or_make_info(test_case, event, expected):
            """
            Check break_or_make_info field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyboardModeEvent to check
            :type event: ``KeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert break_or_make_info that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The break_or_make_info shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.break_or_make_info),
                msg="The break_or_make_info parameter differs from the one expected")
        # end def check_break_or_make_info
    # end class KeyboardModeEventChecker

    class MouseModeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``MouseModeEvent``
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
            return {
                "x_value": (cls.check_x_value, HexList(0x0)),
                "y_value": (cls.check_y_value, HexList(0x0)),
                "tilt_left_or_right_analog_value": (cls.check_tilt_left_or_right_analog_value, HexList(0x0)),
                "back_and_forward_analog_values": (cls.check_back_and_forward_analog_values, HexList(0x0)),
                "roller_value": (cls.check_roller_value, HexList(0x0)),
                "time_between_ratchets": (cls.check_time_between_ratchets, HexList(0x0)),
                "switches": (cls.check_switches, HexList(0x0)),
            }
        # end def get_default_check_map

        @staticmethod
        def check_x_value(test_case, event, expected):
            """
            Check x_value field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MouseModeEvent to check
            :type event: ``MouseModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert x_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The x_value shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.x_value),
                msg="The x_value parameter differs from the one expected")
        # end def check_x_value

        @staticmethod
        def check_y_value(test_case, event, expected):
            """
            Check y_value field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MouseModeEvent to check
            :type event: ``MouseModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert y_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The y_value shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.y_value),
                msg="The y_value parameter differs from the one expected")
        # end def check_y_value

        @staticmethod
        def check_tilt_left_or_right_analog_value(test_case, event, expected):
            """
            Check tilt_left_or_right_analog_value field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MouseModeEvent to check
            :type event: ``MouseModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert tilt_left_or_right_analog_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The tilt_left_or_right_analog_value shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.tilt_left_or_right_analog_value),
                msg="The tilt_left_or_right_analog_value parameter differs from the one expected")
        # end def check_tilt_left_or_right_analog_value

        @staticmethod
        def check_back_and_forward_analog_values(test_case, event, expected):
            """
            Check back_and_forward_analog_values field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MouseModeEvent to check
            :type event: ``MouseModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert back_and_forward_analog_values that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The back_and_forward_analog_values shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.back_and_forward_analog_values),
                msg="The back_and_forward_analog_values parameter differs from the one expected")
        # end def check_back_and_forward_analog_values

        @staticmethod
        def check_roller_value(test_case, event, expected):
            """
            Check roller_value field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MouseModeEvent to check
            :type event: ``MouseModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert roller_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The roller_value shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.roller_value),
                msg="The roller_value parameter differs from the one expected")
        # end def check_roller_value

        @staticmethod
        def check_time_between_ratchets(test_case, event, expected):
            """
            Check time_between_ratchets field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MouseModeEvent to check
            :type event: ``MouseModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert time_between_ratchets that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The time_between_ratchets shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.time_between_ratchets),
                msg="The time_between_ratchets parameter differs from the one expected")
        # end def check_time_between_ratchets

        @staticmethod
        def check_switches(test_case, event, expected):
            """
            Check switches field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MouseModeEvent to check
            :type event: ``MouseModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert switches that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The switches shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.switches),
                msg="The switches parameter differs from the one expected")
        # end def check_switches
    # end class MouseModeEventChecker

    class EnhancedKeyboardModeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``EnhancedKeyboardModeEvent``
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
            return {"row_col_code_0": (cls.check_row_col_code_0, HexList(0xFF)),
                    "row_col_code_1": (cls.check_row_col_code_1, HexList(0xFF)),
                    "row_col_code_2": (cls.check_row_col_code_2, HexList(0xFF)),
                    "row_col_code_3": (cls.check_row_col_code_3, HexList(0xFF)),
                    "row_col_code_4": (cls.check_row_col_code_4, HexList(0xFF)),
                    "row_col_code_5": (cls.check_row_col_code_5, HexList(0xFF)),
                    "row_col_code_6": (cls.check_row_col_code_5, HexList(0xFF)),
                    "row_col_code_7": (cls.check_row_col_code_7, HexList(0xFF)),
                    }
        # end def get_default_check_map

        @staticmethod
        def check_row_col_code_0(test_case, event, expected):
            """
            Check row_col_code_0 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_0 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_0),
                msg="The row_col_code_0 parameter differs from the one expected")
        # end def check_row_col_code_0

        @staticmethod
        def check_row_col_code_1(test_case, event, expected):
            """
            Check row_col_code_1 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_ shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_1),
                msg="The row_col_code_1 parameter differs from the one expected")
        # end def check_row_col_code_1

        @staticmethod
        def check_row_col_code_2(test_case, event, expected):
            """
            Check row_col_code_2 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_2 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_2),
                msg="The row_col_code_2 parameter differs from the one expected")
        # end def check_row_col_code_2

        @staticmethod
        def check_row_col_code_3(test_case, event, expected):
            """
            Check row_col_code_3 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_3 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_3 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_3),
                msg="The row_col_code_3 parameter differs from the one expected")
        # end def check_row_col_code_3

        @staticmethod
        def check_row_col_code_4(test_case, event, expected):
            """
            Check row_col_code_4 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_4 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_4 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_4),
                msg="The row_col_code_4 parameter differs from the one expected")
        # end def check_row_col_code_4

        @staticmethod
        def check_row_col_code_5(test_case, event, expected):
            """
            Check row_col_code_5 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_5 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_5 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_5),
                msg="The row_col_code_5 parameter differs from the one expected")
        # end def check_row_col_code_5

        @staticmethod
        def check_row_col_code_6(test_case, event, expected):
            """
            Check row_col_code_6 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_6 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_6 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_6),
                msg="The row_col_code_6 parameter differs from the one expected")
        # end def check_row_col_code_6

        @staticmethod
        def check_row_col_code_7(test_case, event, expected):
            """
            Check row_col_code_7 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardModeEvent to check
            :type event: ``EnhancedKeyboardModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_col_code_7 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_col_code_7 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_col_code_7),
                msg="The row_col_code_7 parameter differs from the one expected")
        # end def check_row_col_code_7
    # end class EnhancedKeyboardModeEventChecker

    class KeyboardWithLargerMatrixModeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeyboardWithLargerMatrixModeEvent``
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
            return {
                "row_code": (cls.check_row_code, (HexList(0xFF))),
                "col_code": (cls.check_col_code, (HexList(0xFF))),
                "break_or_make_info": (cls.check_break_or_make_info, (HexList(0x0)))
            }
        # end def get_default_check_map

        @staticmethod
        def check_row_code(test_case, event, expected):
            """
            Check row_code field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyboardWithLargerMatrixModeEvent to check
            :type event: ``KeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code),
                msg="The row_code parameter differs from the one expected")
        # end def check_row_code

        @staticmethod
        def check_col_code(test_case, event, expected):
            """
            Check col_code field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyboardWithLargerMatrixModeEvent to check
            :type event: ``KeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code),
                msg="The col_code parameter differs from the one expected")
        # end def check_col_code

        @staticmethod
        def check_break_or_make_info(test_case, event, expected):
            """
            Check break_or_make_info field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyboardWithLargerMatrixModeEvent to check
            :type event: ``KeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert break_or_make_info that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The break_or_make_info shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.break_or_make_info),
                msg="The break_or_make_info parameter differs from the one expected")
        # end def check_break_or_make_info
    # end class KeyboardWithLargerMatrixModeEventChecker

    class EnhancedKeyboardWithLargerMatrixModeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``EnhancedKeyboardWithLargerMatrixModeEvent``
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
            return {
                "row_code_0": (cls.check_row_code_0, HexList(0xFF)),
                "col_code_0": (cls.check_col_code_0, HexList(0xFF)),
                "row_code_1": (cls.check_row_code_1, HexList(0xFF)),
                "col_code_1": (cls.check_col_code_1, HexList(0xFF)),
                "row_code_2": (cls.check_row_code_2, HexList(0xFF)),
                "col_code_2": (cls.check_col_code_2, HexList(0xFF)),
                "row_code_3": (cls.check_row_code_3, HexList(0xFF)),
                "col_code_3": (cls.check_col_code_3, HexList(0xFF)),
                "row_code_4": (cls.check_row_code_4, HexList(0xFF)),
                "col_code_4": (cls.check_col_code_4, HexList(0xFF)),
                "row_code_5": (cls.check_row_code_5, HexList(0xFF)),
                "col_code_5": (cls.check_col_code_5, HexList(0xFF)),
                "row_code_6": (cls.check_row_code_6, HexList(0xFF)),
                "col_code_6": (cls.check_col_code_6, HexList(0xFF)),
                "row_code_7": (cls.check_row_code_7, HexList(0xFF)),
                "col_code_7": (cls.check_col_code_7, HexList(0xFF))
            }
        # end def get_default_check_map

        @staticmethod
        def check_row_code_0(test_case, event, expected):
            """
            Check row_code_0 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_0 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_0),
                msg="The row_code_0 parameter differs from the one expected")
        # end def check_row_code_0

        @staticmethod
        def check_col_code_0(test_case, event, expected):
            """
            Check col_code_0 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_0 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_0),
                msg="The col_code_0 parameter differs from the one expected")
        # end def check_col_code_0

        @staticmethod
        def check_row_code_1(test_case, event, expected):
            """
            Check row_code_1 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_1 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_1),
                msg="The row_code_1 parameter differs from the one expected")
        # end def check_row_code_1

        @staticmethod
        def check_col_code_1(test_case, event, expected):
            """
            Check col_code_1 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_1 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_1),
                msg="The col_code_1 parameter differs from the one expected")
        # end def check_col_code_1

        @staticmethod
        def check_row_code_2(test_case, event, expected):
            """
            Check row_code_2 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_2 shall passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_2),
                msg="The row_code_2 parameter differs from the one expected")
        # end def check_row_code_2

        @staticmethod
        def check_col_code_2(test_case, event, expected):
            """
            Check col_code_2 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_2 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_2),
                msg="The col_code_2 parameter differs from the one expected")
        # end def check_col_code_2

        @staticmethod
        def check_row_code_3(test_case, event, expected):
            """
            Check row_code_3 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_3 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_3 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_3),
                msg="The row_code_3 parameter differs from the one expected")
        # end def check_row_code_3

        @staticmethod
        def check_col_code_3(test_case, event, expected):
            """
            Check col_code_3 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_3 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_3 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_3),
                msg="The col_code_3 parameter differs from the one expected")
        # end def check_col_code_3

        @staticmethod
        def check_row_code_4(test_case, event, expected):
            """
            Check row_code_4 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_4 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_4 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_4),
                msg="The row_code_4 parameter differs from the one expected")
        # end def check_row_code_4

        @staticmethod
        def check_col_code_4(test_case, event, expected):
            """
            Check col_code_4 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_4 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_4 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_4),
                msg="The col_code_4 parameter differs from the one expected")
        # end def check_col_code_4

        @staticmethod
        def check_row_code_5(test_case, event, expected):
            """
            Check row_code_5 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_5 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_5 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_5),
                msg="The row_code_5 parameter differs from the one expected")
        # end def check_row_code_5

        @staticmethod
        def check_col_code_5(test_case, event, expected):
            """
            Check col_code_5 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_5 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_5 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_5),
                msg="The col_code_5 parameter differs from the one expected")
        # end def check_col_code_5

        @staticmethod
        def check_row_code_6(test_case, event, expected):
            """
            Check row_code_6 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_6 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_6 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_6),
                msg="The row_code_6 parameter differs from the one expected")
        # end def check_row_code_6

        @staticmethod
        def check_col_code_6(test_case, event, expected):
            """
            Check col_code_6 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_6 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_6 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_6),
                msg="The col_code_6 parameter differs from the one expected")
        # end def check_col_code_6

        @staticmethod
        def check_row_code_7(test_case, event, expected):
            """
            Check row_code_7 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert row_code_7 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The row_code_7 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.row_code_7),
                msg="The row_code_7 parameter differs from the one expected")
        # end def check_row_code_7

        @staticmethod
        def check_col_code_7(test_case, event, expected):
            """
            Check col_code_7 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: EnhancedKeyboardWithLargerMatrixModeEvent to check
            :type event: ``EnhancedKeyboardWithLargerMatrixModeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert col_code_7 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The col_code_7 shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.col_code_7),
                msg="The col_code_7 parameter differs from the one expected")
        # end def check_col_code_7
    # end class EnhancedKeyboardWithLargerMatrixModeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):

        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=StaticMonitorMode.FEATURE_ID, factory=StaticMonitorModeFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def set_monitor_mode(cls, test_case, mode, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``SetMonitorMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param mode: Mode
            :type mode: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetMonitorModeResponse
            :rtype: ``SetMonitorModeResponse``
            """
            feature_18b0_index, feature_18b0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_18b0.set_monitor_mode_cls(
                device_index=device_index,
                feature_index=feature_18b0_index,
                mode=HexList(mode))

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
                response_class_type=feature_18b0.set_monitor_mode_response_cls)
        # end def set_monitor_mode

        @classmethod
        def monitor_mode_broadcast_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                         check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``MonitorModeBroadcastEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: MonitorModeBroadcastEvent
            :rtype: ``MonitorModeBroadcastEvent``
            """
            _, feature_18b0, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_18b0.monitor_mode_broadcast_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def monitor_mode_broadcast_event
    # end class HIDppHelper

    @classmethod
    def get_kbd_row_col_code(cls, test_case, key_id, combined=True):
        """
        Get row, column code of key from keyboard layout

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: The key ID
        :type key_id: ``KEY_ID | int``
        :param combined: If row and col code should be returned combined (default is True) -OPTIONAL
        :type combined: ``bool``

        :return: Row, Column indexes of key
        :rtype: ``str | tuple[str]``
        """
        row_index, col_index = test_case.button_stimuli_emulator.get_row_col_indexes(key_id)
        if combined:
            return "{:01X}{:01X}".format(row_index, col_index)
        else:
            return "{:02X}".format(row_index), "{:02X}".format(col_index)
        # end if
    # end def get_kbd_row_col_code

    @classmethod
    def update_switch(cls, switch, button, set_bit=False, clear_bit=False):
        """
        Update switch using set bit or clear bit according to the button pressed or released

        :param switch: The current switch value
        :type switch: ``HexList``
        :param button: The button pressed or released
        :type button: ``KEY_ID``
        :param set_bit: Set the bit - OPTIONAL
        :type set_bit: ``bool``
        :param clear_bit: Clear the bit - OPTIONAL
        :type clear_bit: ``bool``

        :return: The updated switch value
        :rtype: ``HexList``
        """
        switch = HexList(switch)
        if set_bit:
            switch.setBit(button - 1)
        elif clear_bit:
            switch.clearBit(button - 1)
        # end if

        return switch
    # def update_switch

    @classmethod
    def get_non_ghosted_keys(cls, test_case, number_of_keys):
        """
        Return a list of non-ghosted keys by picking one key per column or row (depending on the number of row and
        column)

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param number_of_keys: The number of non-ghosted keys to return
        :type number_of_keys: ``int``

        return: The list of non-ghosted keys
        rtype: ``list[int]``
        """
        non_ghosted_keys = []
        supported_key_id_list = test_case.button_stimuli_emulator.get_key_id_list()

        # Find the maximum and minimum indexes for rows and columns
        minimum_row_index, minimum_col_index, maximum_row_index, maximum_col_index = None, None, None, None
        for key_id in supported_key_id_list:
            row_index, col_index = test_case.button_stimuli_emulator.get_row_col_indexes(key_id=key_id)
            minimum_row_index = min(minimum_row_index, row_index) if minimum_row_index is not None else row_index
            minimum_col_index = min(minimum_col_index, col_index) if minimum_col_index is not None else col_index
            maximum_row_index = max(maximum_row_index, row_index) if maximum_row_index is not None else row_index
            maximum_col_index = max(maximum_col_index, col_index) if maximum_col_index is not None else col_index
        # end for

        if (maximum_col_index - minimum_col_index) > (maximum_row_index - minimum_row_index):
            # Select one key per column
            for single_col_index in range(minimum_col_index, maximum_col_index + 1):
                for key_id in supported_key_id_list:
                    row_index, col_index = test_case.button_stimuli_emulator.get_row_col_indexes(key_id=key_id)
                    if col_index == single_col_index:
                        non_ghosted_keys.append(key_id)
                        break
                    # end if
                # end for
                if len(non_ghosted_keys) == number_of_keys:
                    break
                # end if
            # end for
        else:
            # Select one key per row
            for single_row_index in range(minimum_row_index, maximum_row_index + 1):
                for key_id in supported_key_id_list:
                    row_index, col_index = test_case.button_stimuli_emulator.get_row_col_indexes(key_id=key_id)
                    if row_index == single_row_index:
                        non_ghosted_keys.append(key_id)
                        break
                    # end if
                # end for
                if len(non_ghosted_keys) == number_of_keys:
                    break
                # end if
            # end for
        # end if

        test_case.assertTrue(len(non_ghosted_keys) == number_of_keys,
                             msg=f"Not enough non-ghosted keys expected: {number_of_keys} "
                                 f"obtained: {len(non_ghosted_keys)}")
        return non_ghosted_keys
    # end def get_non_ghosted_keys
# end class StaticMonitorModeTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
