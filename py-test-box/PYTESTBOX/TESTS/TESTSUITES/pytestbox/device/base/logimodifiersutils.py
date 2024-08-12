#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.logimodifiersutils
:brief: Helpers for ``LogiModifiers`` feature
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.logimodifiers import GetCapabilitiesResponse
from pyhid.hidpp.features.gaming.logimodifiers import GetLocallyPressedStateResponse
from pyhid.hidpp.features.gaming.logimodifiers import LogiModifiers
from pyhid.hidpp.features.gaming.logimodifiers import LogiModifiersFactory
from pyhid.hidpp.features.gaming.logimodifiers import PressEvent
from pyhid.hidpp.features.gaming.logimodifiers import SetForcedPressedStateResponse
from pyhid.hidpp.features.gaming.logimodifiers import SetPressEventsResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiModifiersTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``LogiModifiers`` feature
    """

    class GettableModifiersChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GettableModifiers``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.LOGI_MODIFIERS
            return {
                "reserved": (cls.check_reserved, 0),
                "g_shift": (cls.check_gm_g_shift, config.F_GM_GShift),
                "fn": (cls.check_gm_fn, config.F_GM_Fn),
                "right_gui": (cls.check_gm_right_gui, config.F_GM_RightGui),
                "right_alt": (cls.check_gm_right_alt, config.F_GM_RightAlt),
                "right_shift": (cls.check_gm_right_shift, config.F_GM_RightShift),
                "right_ctrl": (cls.check_gm_right_ctrl, config.F_GM_RightCtrl),
                "left_gui": (cls.check_gm_left_gui, config.F_GM_LeftGui),
                "left_alt": (cls.check_gm_left_alt, config.F_GM_LeftAlt),
                "left_shift": (cls.check_gm_left_shift, config.F_GM_LeftShift),
                "left_ctrl": (cls.check_gm_left_ctrl, config.F_GM_LeftCtrl),
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_gm_g_shift(test_case, bitmap, expected):
            """
            Check gm_g_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_g_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.g_shift),
                msg="The gm_g_shift parameter differs from the one expected")
        # end def check_gm_g_shift

        @staticmethod
        def check_gm_fn(test_case, bitmap, expected):
            """
            Check gm_fn field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_fn that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fn),
                msg="The gm_fn parameter differs from the one expected")
        # end def check_gm_fn

        @staticmethod
        def check_gm_right_gui(test_case, bitmap, expected):
            """
            Check gm_right_gui field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_right_gui that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_gui),
                msg="The gm_right_gui parameter differs from the one expected")
        # end def check_gm_right_gui

        @staticmethod
        def check_gm_right_alt(test_case, bitmap, expected):
            """
            Check gm_right_alt field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_right_alt that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_alt),
                msg="The gm_right_alt parameter differs from the one expected")
        # end def check_gm_right_alt

        @staticmethod
        def check_gm_right_shift(test_case, bitmap, expected):
            """
            Check gm_right_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_right_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_shift),
                msg="The gm_right_shift parameter differs from the one expected")
        # end def check_gm_right_shift

        @staticmethod
        def check_gm_right_ctrl(test_case, bitmap, expected):
            """
            Check gm_right_ctrl field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_right_ctrl that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_ctrl),
                msg="The gm_right_ctrl parameter differs from the one expected")
        # end def check_gm_right_ctrl

        @staticmethod
        def check_gm_left_gui(test_case, bitmap, expected):
            """
            Check gm_left_gui field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_left_gui that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_gui),
                msg="The gm_left_gui parameter differs from the one expected")
        # end def check_gm_left_gui

        @staticmethod
        def check_gm_left_alt(test_case, bitmap, expected):
            """
            Check gm_left_alt field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_left_alt that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_alt),
                msg="The gm_left_alt parameter differs from the one expected")
        # end def check_gm_left_alt

        @staticmethod
        def check_gm_left_shift(test_case, bitmap, expected):
            """
            Check gm_left_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_left_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_shift),
                msg="The gm_left_shift parameter differs from the one expected")
        # end def check_gm_left_shift

        @staticmethod
        def check_gm_left_ctrl(test_case, bitmap, expected):
            """
            Check gm_left_ctrl field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GettableModifiers to check
            :type bitmap: ``LogiModifiers.GettableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gm_left_ctrl that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_ctrl),
                msg="The gm_left_ctrl parameter differs from the one expected")
        # end def check_gm_left_ctrl
    # end class GettableModifiersChecker

    class ForceableModifiersChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ForceableModifiers``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.LOGI_MODIFIERS
            return {
                "reserved1": (cls.check_reserved1, 0),
                "g_shift": (cls.check_fm_g_shift, config.F_FM_GShift),
                "fn": (cls.check_fm_fn, config.F_FM_Fn),
                "reserved2": (cls.check_reserved2, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved1(test_case, bitmap, expected):
            """
            Check reserved1 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForceableModifiers to check
            :type bitmap: ``LogiModifiers.ForceableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved1),
                msg="The reserved1 parameter differs from the one expected")
        # end def check_reserved1

        @staticmethod
        def check_fm_g_shift(test_case, bitmap, expected):
            """
            Check fm_g_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForceableModifiers to check
            :type bitmap: ``LogiModifiers.ForceableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fm_g_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.g_shift),
                msg="The fm_g_shift parameter differs from the one expected")
        # end def check_fm_g_shift

        @staticmethod
        def check_fm_fn(test_case, bitmap, expected):
            """
            Check fm_fn field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForceableModifiers to check
            :type bitmap: ``LogiModifiers.ForceableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fm_fn that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fn),
                msg="The fm_fn parameter differs from the one expected")
        # end def check_fm_fn

        @staticmethod
        def check_reserved2(test_case, bitmap, expected):
            """
            Check reserved2 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForceableModifiers to check
            :type bitmap: ``LogiModifiers.ForceableModifiers``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved2),
                msg="The reserved2 parameter differs from the one expected")
        # end def check_reserved2
    # end class ForceableModifiersChecker

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
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
                "gettable_modifiers": (
                    cls.check_gettable_modifiers,
                    LogiModifiersTestUtils.GettableModifiersChecker.get_default_check_map(test_case)),
                "forceable_modifiers": (
                    cls.check_forceable_modifiers,
                    LogiModifiersTestUtils.ForceableModifiersChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_gettable_modifiers(test_case, message, expected):
            """
            Check ``gettable_modifiers``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LogiModifiersTestUtils.GettableModifiersChecker.check_fields(
                test_case, message.gettable_modifiers, LogiModifiers.GettableModifiers, expected)
        # end def check_gettable_modifiers

        @staticmethod
        def check_forceable_modifiers(test_case, message, expected):
            """
            Check ``forceable_modifiers``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LogiModifiersTestUtils.ForceableModifiersChecker.check_fields(
                test_case, message.forceable_modifiers, LogiModifiers.ForceableModifiers, expected)
        # end def check_forceable_modifiers
    # end class GetCapabilitiesResponseChecker

    class LocallyPressedStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LocallyPressedState``
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
                "reserved": (cls.check_reserved, 0),
                "g_shift": (cls.check_g_shift, False),
                "fn": (cls.check_fn, False),
                "right_gui": (cls.check_right_gui, False),
                "right_alt": (cls.check_right_alt, False),
                "right_shift": (cls.check_right_shift, False),
                "right_ctrl": (cls.check_right_ctrl, False),
                "left_gui": (cls.check_left_gui, False),
                "left_alt": (cls.check_left_alt, False),
                "left_shift": (cls.check_left_shift, False),
                "left_ctrl": (cls.check_left_ctrl, False)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_g_shift(test_case, bitmap, expected):
            """
            Check g_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert g_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.g_shift),
                msg="The g_shift parameter differs from the one expected")
        # end def check_g_shift

        @staticmethod
        def check_fn(test_case, bitmap, expected):
            """
            Check fn field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fn that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fn),
                msg="The fn parameter differs from the one expected")
        # end def check_fn

        @staticmethod
        def check_right_gui(test_case, bitmap, expected):
            """
            Check right_gui field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_gui that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_gui),
                msg="The right_gui parameter differs from the one expected")
        # end def check_right_gui

        @staticmethod
        def check_right_alt(test_case, bitmap, expected):
            """
            Check right_alt field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_alt that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_alt),
                msg="The right_alt parameter differs from the one expected")
        # end def check_right_alt

        @staticmethod
        def check_right_shift(test_case, bitmap, expected):
            """
            Check right_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_shift),
                msg="The right_shift parameter differs from the one expected")
        # end def check_right_shift

        @staticmethod
        def check_right_ctrl(test_case, bitmap, expected):
            """
            Check right_ctrl field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_ctrl that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_ctrl),
                msg="The right_ctrl parameter differs from the one expected")
        # end def check_right_ctrl

        @staticmethod
        def check_left_gui(test_case, bitmap, expected):
            """
            Check left_gui field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_gui that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_gui),
                msg="The left_gui parameter differs from the one expected")
        # end def check_left_gui

        @staticmethod
        def check_left_alt(test_case, bitmap, expected):
            """
            Check left_alt field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_alt that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_alt),
                msg="The left_alt parameter differs from the one expected")
        # end def check_left_alt

        @staticmethod
        def check_left_shift(test_case, bitmap, expected):
            """
            Check left_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_shift),
                msg="The left_shift parameter differs from the one expected")
        # end def check_left_shift

        @staticmethod
        def check_left_ctrl(test_case, bitmap, expected):
            """
            Check left_ctrl field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: LocallyPressedState to check
            :type bitmap: ``LogiModifiers.LocallyPressedState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_ctrl that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_ctrl),
                msg="The left_ctrl parameter differs from the one expected")
        # end def check_left_ctrl
    # end class LocallyPressedStateChecker

    class GetLocallyPressedStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetLocallyPressedStateResponse``
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
                "locally_pressed_state": (
                    cls.check_locally_pressed_state,
                    LogiModifiersTestUtils.LocallyPressedStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_locally_pressed_state(test_case, message, expected):
            """
            Check ``locally_pressed_state``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetLocallyPressedStateResponse to check
            :type message: ``GetLocallyPressedStateResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LogiModifiersTestUtils.LocallyPressedStateChecker.check_fields(
                test_case, message.locally_pressed_state, LogiModifiers.LocallyPressedState, expected)
        # end def check_locally_pressed_state
    # end class GetLocallyPressedStateResponseChecker

    class ForcedPressedStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ForcedPressedStateRsp``
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
                "reserved1": (cls.check_reserved1, 0),
                "g_shift": (cls.check_g_shift, False),
                "fn": (cls.check_fn, False),
                "reserved2": (cls.check_reserved2, 0)
            }

        # end def get_default_check_map

        @staticmethod
        def check_reserved1(test_case, bitmap, expected):
            """
            Check reserved1 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForcedPressedStateRsp to check
            :type bitmap: ``LogiModifiers.ForcedPressedStateRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved1),
                msg="The reserved1 parameter differs from the one expected")

        # end def check_reserved1

        @staticmethod
        def check_g_shift(test_case, bitmap, expected):
            """
            Check g_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForcedPressedStateRsp to check
            :type bitmap: ``LogiModifiers.ForcedPressedStateRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert g_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.g_shift),
                msg="The g_shift parameter differs from the one expected")

        # end def check_g_shift

        @staticmethod
        def check_fn(test_case, bitmap, expected):
            """
            Check fn field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForcedPressedStateRsp to check
            :type bitmap: ``LogiModifiers.ForcedPressedStateRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fn that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fn),
                msg="The fn parameter differs from the one expected")

        # end def check_fn

        @staticmethod
        def check_reserved2(test_case, bitmap, expected):
            """
            Check reserved2 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ForcedPressedStateRsp to check
            :type bitmap: ``LogiModifiers.ForcedPressedStateRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved2),
                msg="The reserved2 parameter differs from the one expected")
        # end def check_reserved2
    # end class ForcedPressedStateResponseChecker

    class GetForcedPressedStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetForcedPressedStateResponse``
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
                "forced_pressed_state": (
                    cls.check_forced_pressed_state_rsp,
                    LogiModifiersTestUtils.ForcedPressedStateResponseChecker.get_default_check_map(test_case))
            }

        # end def get_default_check_map

        @staticmethod
        def check_forced_pressed_state_rsp(test_case, message, expected):
            """
            Check ``forced_pressed_state_rsp``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetForcedPressedStateResponse to check
            :type message: ``GetForcedPressedStateResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LogiModifiersTestUtils.ForcedPressedStateResponseChecker.check_fields(
                test_case, message.forced_pressed_state, LogiModifiers.ForcedPressedState, expected)
        # end def check_forced_pressed_state_rsp
    # end class GetForcedPressedStateResponseChecker

    class ReportedModifiersRspChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReportedModifiersRsp``
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
                "reserved": (cls.check_reserved, 0),
                "g_shift": (cls.check_g_shift, False),
                "fn": (cls.check_fn, False),
                "right_gui": (cls.check_right_gui, False),
                "right_alt": (cls.check_right_alt, False),
                "right_shift": (cls.check_right_shift, False),
                "right_ctrl": (cls.check_right_ctrl, False),
                "left_gui": (cls.check_left_gui, False),
                "left_alt": (cls.check_left_alt, False),
                "left_shift": (cls.check_left_shift, False),
                "left_ctrl": (cls.check_left_ctrl, False)
            }

        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")

        # end def check_reserved

        @staticmethod
        def check_g_shift(test_case, bitmap, expected):
            """
            Check g_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert g_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.g_shift),
                msg="The g_shift parameter differs from the one expected")

        # end def check_g_shift

        @staticmethod
        def check_fn(test_case, bitmap, expected):
            """
            Check fn field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fn that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fn),
                msg="The fn parameter differs from the one expected")

        # end def check_fn

        @staticmethod
        def check_right_gui(test_case, bitmap, expected):
            """
            Check right_gui field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_gui that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_gui),
                msg="The right_gui parameter differs from the one expected")

        # end def check_right_gui

        @staticmethod
        def check_right_alt(test_case, bitmap, expected):
            """
            Check right_alt field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_alt that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_alt),
                msg="The right_alt parameter differs from the one expected")

        # end def check_right_alt

        @staticmethod
        def check_right_shift(test_case, bitmap, expected):
            """
            Check right_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_shift),
                msg="The right_shift parameter differs from the one expected")

        # end def check_right_shift

        @staticmethod
        def check_right_ctrl(test_case, bitmap, expected):
            """
            Check right_ctrl field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert right_ctrl that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.right_ctrl),
                msg="The right_ctrl parameter differs from the one expected")

        # end def check_right_ctrl

        @staticmethod
        def check_left_gui(test_case, bitmap, expected):
            """
            Check left_gui field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_gui that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_gui),
                msg="The left_gui parameter differs from the one expected")

        # end def check_left_gui

        @staticmethod
        def check_left_alt(test_case, bitmap, expected):
            """
            Check left_alt field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_alt that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_alt),
                msg="The left_alt parameter differs from the one expected")

        # end def check_left_alt

        @staticmethod
        def check_left_shift(test_case, bitmap, expected):
            """
            Check left_shift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_shift that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_shift),
                msg="The left_shift parameter differs from the one expected")

        # end def check_left_shift

        @staticmethod
        def check_left_ctrl(test_case, bitmap, expected):
            """
            Check left_ctrl field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ReportedModifiersRsp to check
            :type bitmap: ``LogiModifiers.ReportedModifiersRsp``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert left_ctrl that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.left_ctrl),
                msg="The left_ctrl parameter differs from the one expected")
        # end def check_left_ctrl

    # end class ReportedModifiersRspChecker

    class GetPressEventsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetPressEventsResponse``
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
                "reported_modifiers": (
                    cls.check_reported_modifiers_rsp,
                    LogiModifiersTestUtils.ReportedModifiersRspChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_reported_modifiers_rsp(test_case, message, expected):
            """
            Check ``reported_modifiers_rsp``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetPressEventsResponse to check
            :type message: ``GetPressEventsResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LogiModifiersTestUtils.ReportedModifiersRspChecker.check_fields(
                test_case, message.reported_modifiers, LogiModifiers.ReportedModifiers, expected)
        # end def check_reported_modifiers_rsp
    # end class GetPressEventsResponseChecker

    class PressEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``PressEvent``
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
                "locally_pressed_state": (
                    cls.check_locally_pressed_state,
                    LogiModifiersTestUtils.LocallyPressedStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_locally_pressed_state(test_case, message, expected):
            """
            Check ``locally_pressed_state``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: PressEvent to check
            :type message: ``PressEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LogiModifiersTestUtils.LocallyPressedStateChecker.check_fields(
                test_case, message.locally_pressed_state, LogiModifiers.LocallyPressedState, expected)
        # end def check_locally_pressed_state
    # end class PressEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=LogiModifiers.FEATURE_ID,
                           factory=LogiModifiersFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCapabilities``

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

            :return: GetCapabilitiesResponse
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_8051_index, feature_8051, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8051.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_8051_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8051.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_locally_pressed_state(cls, test_case, device_index=None, port_index=None, software_id=None,
                                      padding=None):
            """
            Process ``GetLocallyPressedState``

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

            :return: GetLocallyPressedStateResponse
            :rtype: ``GetLocallyPressedStateResponse``
            """
            feature_8051_index, feature_8051, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8051.get_locally_pressed_state_cls(
                device_index=device_index,
                feature_index=feature_8051_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8051.get_locally_pressed_state_response_cls)
        # end def get_locally_pressed_state

        @classmethod
        def set_forced_pressed_state(cls, test_case, g_shift, fn, device_index=None, port_index=None,
                                     software_id=None, padding=None):
            """
            Process ``SetForcedPressedState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param g_shift: G Shift
            :type g_shift: ``int | HexList``
            :param fn: Fn
            :type fn: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetForcedPressedStateResponse
            :rtype: ``SetForcedPressedStateResponse``
            """
            feature_8051_index, feature_8051, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8051.set_forced_pressed_state_cls(
                device_index=device_index,
                feature_index=feature_8051_index,
                g_shift=g_shift,
                fn=fn)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8051.set_forced_pressed_state_response_cls)
        # end def set_forced_pressed_state

        @classmethod
        def set_press_events(cls, test_case, g_shift=False, fn=False,
                             right_gui=False, right_alt=False, right_shift=False, right_ctrl=False,
                             left_gui=False, left_alt=False, left_shift=False, left_ctrl=False,
                             device_index=None, port_index=None, software_id=None,
                             padding=None):
            """
            Process ``SetPressEvents``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param g_shift: G Shift
            :type g_shift: ``int | HexList``
            :param fn: Fn
            :type fn: ``int | HexList``
            :param right_gui: Right Gui
            :type right_gui: ``int | HexList``
            :param right_alt: Right Alt
            :type right_alt: ``int | HexList``
            :param right_shift: Right Shift
            :type right_shift: ``int | HexList``
            :param right_ctrl: Right Ctrl
            :type right_ctrl: ``int | HexList``
            :param left_gui: Left Gui
            :type left_gui: ``int | HexList``
            :param left_alt: Left Alt
            :type left_alt: ``int | HexList``
            :param left_shift: Left Shift
            :type left_shift: ``int | HexList``
            :param left_ctrl: Left Ctrl
            :type left_ctrl: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetPressEventsResponse
            :rtype: ``SetPressEventsResponse``
            """
            feature_8051_index, feature_8051, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8051.set_press_events_cls(
                device_index=device_index,
                feature_index=feature_8051_index,
                g_shift=g_shift,
                fn=fn,
                right_gui=right_gui,
                right_alt=right_alt,
                right_shift=right_shift,
                right_ctrl=right_ctrl,
                left_gui=left_gui,
                left_alt=left_alt,
                left_shift=left_shift,
                left_ctrl=left_ctrl)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8051.set_press_events_response_cls)
        # end def set_press_events

        @classmethod
        def get_forced_pressed_state(cls, test_case, device_index=None, port_index=None, software_id=None,
                                     padding=None):
            """
            Process ``GetForcedPressedState``

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

            :return: GetForcedPressedStateResponse
            :rtype: ``GetForcedPressedStateResponse``
            """
            feature_8051_index, feature_8051, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8051.get_forced_pressed_state_cls(
                device_index=device_index,
                feature_index=feature_8051_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8051.get_forced_pressed_state_response_cls)

        # end def get_forced_pressed_state

        @classmethod
        def get_press_events(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetPressEvents``

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

            :return: GetPressEventsResponse
            :rtype: ``GetPressEventsResponse``
            """
            feature_8051_index, feature_8051, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8051.get_press_events_cls(
                device_index=device_index,
                feature_index=feature_8051_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8051.get_press_events_response_cls)

        # end def get_press_events

        @classmethod
        def press_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``PressEvent``: get notification from event queue

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

            :return: PressEvent
            :rtype: ``PressEvent``
            """
            _, feature_8051, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8051.press_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def press_event
    # end class HIDppHelper
# end class LogiModifiersTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
