#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.fullkeycustomizationutils
:brief: Helpers for ``FullKeyCustomization`` feature
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from random import randint
from random import randrange
from random import sample
from time import sleep

# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hid import HidMouse
from pyhid.hid import HidMouseNvidiaExtension
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE_TO_KEY_ID_MAP
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hiddata import HidData
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import BaseLayerTriggerAsBitmapEvent
from pyhid.hidpp.features.common.fullkeycustomization import BaseLayerTriggerAsListEvent
from pyhid.hidpp.features.common.fullkeycustomization import EnableDisableEvent
from pyhid.hidpp.features.common.fullkeycustomization import FNLayerTriggerAsBitmapEvent
from pyhid.hidpp.features.common.fullkeycustomization import FNLayerTriggerAsListEvent
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomizationFactory
from pyhid.hidpp.features.common.fullkeycustomization import GShiftLayerTriggerAsBitmapEvent
from pyhid.hidpp.features.common.fullkeycustomization import GShiftLayerTriggerAsListEvent
from pyhid.hidpp.features.common.fullkeycustomization import GetCapabilitiesResponseV0
from pyhid.hidpp.features.common.fullkeycustomization import GetCapabilitiesResponseV1
from pyhid.hidpp.features.common.fullkeycustomization import GetSetEnabledResponse
from pyhid.hidpp.features.common.fullkeycustomization import GetSetPowerOnParamsResponse
from pyhid.hidpp.features.common.fullkeycustomization import GetToggleKeyListResponse
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import FkcProfileButton
from pylibrary.mcu.fkcprofileformat import KEY_ID_TO_MODIFIER_BITFIELD
from pylibrary.mcu.fkcprofileformat import MODIFIER_BITFIELD_TO_KEY_ID
from pylibrary.mcu.fkcprofileformat import MODIFIER_KEY_LIST
from pylibrary.mcu.fkcprofileformat import Macro
from pylibrary.mcu.fkcprofileformat import NOT_REMAPPABLE_KEY_LIST
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.profileformat import AcPanCommand
from pylibrary.mcu.profileformat import ConsumerKeyCommand
from pylibrary.mcu.profileformat import KeyAction
from pylibrary.mcu.profileformat import MacroCommand0
from pylibrary.mcu.profileformat import MacroCommand1
from pylibrary.mcu.profileformat import MacroCommand2
from pylibrary.mcu.profileformat import MacroCommand4
from pylibrary.mcu.profileformat import MouseButtonCommand
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.mcu.profileformat import ProfileMacro
from pylibrary.mcu.profileformat import RollerCommand
from pylibrary.mcu.profileformat import StandardKeyCommand
from pylibrary.mcu.profileformat import XYCommand
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FullKeyCustomizationTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``FullKeyCustomization`` feature
    """

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponseV0 | GetCapabilitiesResponseV1``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION

            return {
                "fkc_config_file_ver": (cls.check_fkc_config_file_ver, config.F_FkcConfigFileVer),
                "macro_def_file_ver": (cls.check_macro_def_file_ver, config.F_MacroDefFileVer),
                "fkc_config_file_maxsize": (cls.check_fkc_config_file_maxsize, config.F_FkcConfigFileMaxsize),
                "macro_def_file_maxsize": (cls.check_macro_def_file_maxsize, config.F_MacroDefFileMaxsize),
                "fkc_config_max_triggers": (cls.check_fkc_config_max_triggers, config.F_FkcConfigMaxTriggers),
                "reserved": (cls.check_reserved, 0),
                "sw_config_capabilities": (cls.check_sw_config_capabilities, config.F_SwConfigCapabilities)
            }
        # end def get_default_check_map

        @staticmethod
        def check_fkc_config_file_ver(test_case, response, expected):
            """
            Check fkc_config_file_ver field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0 | GetCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_config_file_ver that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The fkc_config_file_ver shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fkc_config_file_ver),
                msg="The fkc_config_file_ver parameter differs from the one expected")
        # end def check_fkc_config_file_ver

        @staticmethod
        def check_macro_def_file_ver(test_case, response, expected):
            """
            Check macro_def_file_ver field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0 | GetCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert macro_def_file_ver that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The macro_def_file_ver shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.macro_def_file_ver),
                msg="The macro_def_file_ver parameter differs from the one expected")
        # end def check_macro_def_file_ver

        @staticmethod
        def check_fkc_config_file_maxsize(test_case, response, expected):
            """
            Check fkc_config_file_maxsize field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0 | GetCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_config_file_maxsize that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The fkc_config_file_maxsize shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fkc_config_file_maxsize),
                msg="The fkc_config_file_maxsize parameter differs from the one expected")
        # end def check_fkc_config_file_maxsize

        @staticmethod
        def check_macro_def_file_maxsize(test_case, response, expected):
            """
            Check macro_def_file_maxsize field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0 | GetCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert macro_def_file_maxsize that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The macro_def_file_maxsize shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.macro_def_file_maxsize),
                msg="The macro_def_file_maxsize parameter differs from the one expected")
        # end def check_macro_def_file_maxsize

        @staticmethod
        def check_fkc_config_max_triggers(test_case, response, expected):
            """
            Check fkc_config_max_triggers field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0 | GetCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_config_max_triggers that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The fkc_config_max_triggers shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fkc_config_max_triggers),
                msg="The fkc_config_max_triggers parameter differs from the one expected")
        # end def check_fkc_config_max_triggers
    # end class GetCapabilitiesResponseChecker

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_sw_config_capabilities(test_case, response, expected):
            """
            Check sw_config_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert sw_config_capabilities that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The sw_config_capabilities shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sw_config_capabilities),
                msg="The sw_config_capabilities parameter differs from the one expected")
        # end def check_sw_config_capabilities
    # end class GetCapabilitiesResponseChecker

    class PowerOnFkcStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``PowerOnFkcState``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION
            return {
                "reserved": (cls.check_reserved, 0),
                "power_on_fkc_enable": (cls.check_power_on_fkc_enable, config.F_PowerOnFkcEnable)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: PowerOnFkcState to check
            :type bitmap: ``FullKeyCustomization.PowerOnFkcState``
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
        def check_power_on_fkc_enable(test_case, bitmap, expected):
            """
            Check power_on_fkc_enable field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: PowerOnFkcState to check
            :type bitmap: ``FullKeyCustomization.PowerOnFkcState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert power_on_fkc_enable that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The power_on_fkc_enable shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.power_on_fkc_enable),
                msg="The power_on_fkc_enable parameter differs from the one expected")
        # end def check_power_on_fkc_enable
    # end class PowerOnFkcStateChecker

    class GetSetPowerOnParamsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSetPowerOnParamsResponse``
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
                "power_on_fkc_state": (
                    cls.check_power_on_fkc_state,
                    FullKeyCustomizationTestUtils.PowerOnFkcStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_power_on_fkc_state(test_case, message, expected):
            """
            Check ``power_on_fkc_state``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetSetPowerOnParamsResponse to check
            :type message: ``GetSetPowerOnParamsResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            FullKeyCustomizationTestUtils.PowerOnFkcStateChecker.check_fields(
                test_case, message.power_on_fkc_state, FullKeyCustomization.PowerOnFkcState, expected)
        # end def check_power_on_fkc_state
    # end class GetSetPowerOnParamsResponseChecker

    class GetToggleKeyListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetToggleKeyListResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION
            return {
                "toggle_key_0_cidx": (cls.check_toggle_key_0_cidx, config.F_ToggleKey0Cidx),
                "toggle_key_1_cidx": (cls.check_toggle_key_1_cidx, config.F_ToggleKey1Cidx),
                "toggle_key_2_cidx": (cls.check_toggle_key_2_cidx, config.F_ToggleKey2Cidx),
                "toggle_key_3_cidx": (cls.check_toggle_key_3_cidx, config.F_ToggleKey3Cidx),
                "toggle_key_4_cidx": (cls.check_toggle_key_4_cidx, config.F_ToggleKey4Cidx),
                "toggle_key_5_cidx": (cls.check_toggle_key_5_cidx, config.F_ToggleKey5Cidx),
                "toggle_key_6_cidx": (cls.check_toggle_key_6_cidx, config.F_ToggleKey6Cidx),
                "toggle_key_7_cidx": (cls.check_toggle_key_7_cidx, config.F_ToggleKey7Cidx)
            }
        # end def get_default_check_map

        @staticmethod
        def check_toggle_key_0_cidx(test_case, response, expected):
            """
            Check toggle_key_0_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_0_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_0_cidx),
                msg="The toggle_key_0_cidx parameter differs from the one expected")
        # end def check_toggle_key_0_cidx

        @staticmethod
        def check_toggle_key_1_cidx(test_case, response, expected):
            """
            Check toggle_key_1_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_1_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_1_cidx),
                msg="The toggle_key_1_cidx parameter differs from the one expected")
        # end def check_toggle_key_1_cidx

        @staticmethod
        def check_toggle_key_2_cidx(test_case, response, expected):
            """
            Check toggle_key_2_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_2_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_2_cidx),
                msg="The toggle_key_2_cidx parameter differs from the one expected")
        # end def check_toggle_key_2_cidx

        @staticmethod
        def check_toggle_key_3_cidx(test_case, response, expected):
            """
            Check toggle_key_3_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_3_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_3_cidx),
                msg="The toggle_key_3_cidx parameter differs from the one expected")
        # end def check_toggle_key_3_cidx

        @staticmethod
        def check_toggle_key_4_cidx(test_case, response, expected):
            """
            Check toggle_key_4_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_4_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_4_cidx),
                msg="The toggle_key_4_cidx parameter differs from the one expected")
        # end def check_toggle_key_4_cidx

        @staticmethod
        def check_toggle_key_5_cidx(test_case, response, expected):
            """
            Check toggle_key_5_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_5_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_5_cidx),
                msg="The toggle_key_5_cidx parameter differs from the one expected")
        # end def check_toggle_key_5_cidx

        @staticmethod
        def check_toggle_key_6_cidx(test_case, response, expected):
            """
            Check toggle_key_6_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_6_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_6_cidx),
                msg="The toggle_key_6_cidx parameter differs from the one expected")
        # end def check_toggle_key_6_cidx

        @staticmethod
        def check_toggle_key_7_cidx(test_case, response, expected):
            """
            Check toggle_key_7_cidx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetToggleKeyListResponse to check
            :type response: ``GetToggleKeyListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert toggle_key_7_cidx that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.toggle_key_7_cidx),
                msg="The toggle_key_7_cidx parameter differs from the one expected")
        # end def check_toggle_key_7_cidx
    # end class GetToggleKeyListResponseChecker

    class FkcStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``FkcState``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION
            return {
                "reserved": (cls.check_reserved, 0),
                "fkc_enabled": (cls.check_fkc_enabled, config.F_FkcEnabled)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FkcState to check
            :type bitmap: ``FullKeyCustomization.FkcState``
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
        def check_fkc_enabled(test_case, bitmap, expected):
            """
            Check fkc_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FkcState to check
            :type bitmap: ``FullKeyCustomization.FkcState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_enabled that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The fkc_enabled shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_enabled),
                msg="The fkc_enabled parameter differs from the one expected")
        # end def check_fkc_enabled
    # end class FkcStateChecker

    class ToggleKeysStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ToggleKeysState``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION
            return {
                "toggle_key_7_enabled": (cls.check_toggle_key_7_enabled, config.F_ToggleKey7Enabled),
                "toggle_key_6_enabled": (cls.check_toggle_key_6_enabled, config.F_ToggleKey6Enabled),
                "toggle_key_5_enabled": (cls.check_toggle_key_5_enabled, config.F_ToggleKey5Enabled),
                "toggle_key_4_enabled": (cls.check_toggle_key_4_enabled, config.F_ToggleKey4Enabled),
                "toggle_key_3_enabled": (cls.check_toggle_key_3_enabled, config.F_ToggleKey3Enabled),
                "toggle_key_2_enabled": (cls.check_toggle_key_2_enabled, config.F_ToggleKey2Enabled),
                "toggle_key_1_enabled": (cls.check_toggle_key_1_enabled, config.F_ToggleKey1Enabled),
                "toggle_key_0_enabled": (cls.check_toggle_key_0_enabled, config.F_ToggleKey0Enabled)
            }
        # end def get_default_check_map

        @staticmethod
        def check_toggle_key_7_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_7_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_7_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_7_enabled),
                msg="The toggle_key_7_enabled parameter differs from the one expected")
        # end def check_toggle_key_7_enabled

        @staticmethod
        def check_toggle_key_6_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_6_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_6_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_6_enabled),
                msg="The toggle_key_6_enabled parameter differs from the one expected")
        # end def check_toggle_key_6_enabled

        @staticmethod
        def check_toggle_key_5_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_5_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_5_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_5_enabled),
                msg="The toggle_key_5_enabled parameter differs from the one expected")
        # end def check_toggle_key_5_enabled

        @staticmethod
        def check_toggle_key_4_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_4_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_4_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_4_enabled),
                msg="The toggle_key_4_enabled parameter differs from the one expected")
        # end def check_toggle_key_4_enabled

        @staticmethod
        def check_toggle_key_3_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_3_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_3_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_3_enabled),
                msg="The toggle_key_3_enabled parameter differs from the one expected")
        # end def check_toggle_key_3_enabled

        @staticmethod
        def check_toggle_key_2_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_2_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_2_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_2_enabled),
                msg="The toggle_key_2_enabled parameter differs from the one expected")
        # end def check_toggle_key_2_enabled

        @staticmethod
        def check_toggle_key_1_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_1_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_1_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_1_enabled),
                msg="The toggle_key_1_enabled parameter differs from the one expected")
        # end def check_toggle_key_1_enabled

        @staticmethod
        def check_toggle_key_0_enabled(test_case, bitmap, expected):
            """
            Check toggle_key_0_enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ToggleKeysState to check
            :type bitmap: ``FullKeyCustomization.ToggleKeysState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert toggle_key_0_enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.toggle_key_0_enabled),
                msg="The toggle_key_0_enabled parameter differs from the one expected")
        # end def check_toggle_key_0_enabled
    # end class ToggleKeysStateChecker

    class GetSetEnabledResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSetEnabledResponse``
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
                "fkc_state": (
                    cls.check_fkc_state,
                    FullKeyCustomizationTestUtils.FkcStateChecker.get_default_check_map(test_case)),
                "toggle_keys_state": (
                    cls.check_toggle_keys_state,
                    FullKeyCustomizationTestUtils.ToggleKeysStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_fkc_state(test_case, message, expected):
            """
            Check ``fkc_state``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetSetEnabledResponse to check
            :type message: ``GetSetEnabledResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            FullKeyCustomizationTestUtils.FkcStateChecker.check_fields(
                test_case, message.fkc_state, FullKeyCustomization.FkcState, expected)
        # end def check_fkc_state

        @staticmethod
        def check_toggle_keys_state(test_case, message, expected):
            """
            Check ``toggle_keys_state``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetSetEnabledResponse to check
            :type message: ``GetSetEnabledResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            FullKeyCustomizationTestUtils.ToggleKeysStateChecker.check_fields(
                test_case, message.toggle_keys_state, FullKeyCustomization.ToggleKeysState, expected)
        # end def check_toggle_keys_state
    # end class GetSetEnabledResponseChecker

    class GetSetSWConfigurationCookieResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSetSWConfigurationCookieResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION
            return {
                "sw_configuration_cookie": (cls.check_sw_configuration_cookie, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sw_configuration_cookie(test_case, response, expected):
            """
            Check sw_configuration_cookie field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetSetSWConfigurationCookieResponse to check
            :type response: ``GetSetSWConfigurationCookieResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert sw_configuration_cookie that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The sw_configuration_cookie shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sw_configuration_cookie),
                msg="The sw_configuration_cookie parameter differs from the one expected")
        # end def check_sw_configuration_cookie
    # end class GetSetSWConfigurationCookieResponseChecker

    class BaseLayerTriggerAsListEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``BaseLayerTriggerAsListEvent``
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
                "key_trigger_0": (cls.check_key_trigger_0, 0),
                "key_trigger_1": (cls.check_key_trigger_1, 0),
                "key_trigger_2": (cls.check_key_trigger_2, 0),
                "key_trigger_3": (cls.check_key_trigger_3, 0),
                "key_trigger_4": (cls.check_key_trigger_4, 0),
                "key_trigger_5": (cls.check_key_trigger_5, 0),
                "key_trigger_6": (cls.check_key_trigger_6, 0),
                "key_trigger_7": (cls.check_key_trigger_7, 0),
                "key_trigger_8": (cls.check_key_trigger_8, 0),
                "key_trigger_9": (cls.check_key_trigger_9, 0),
                "key_trigger_10": (cls.check_key_trigger_10, 0),
                "key_trigger_11": (cls.check_key_trigger_11, 0),
                "key_trigger_12": (cls.check_key_trigger_12, 0),
                "key_trigger_13": (cls.check_key_trigger_13, 0),
                "key_trigger_14": (cls.check_key_trigger_14, 0),
                "key_trigger_15": (cls.check_key_trigger_15, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_trigger_0(test_case, event, expected):
            """
            Check key_trigger_0 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_0 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_0),
                msg="The key_trigger_0 parameter differs from the one expected")
        # end def check_key_trigger_0

        @staticmethod
        def check_key_trigger_1(test_case, event, expected):
            """
            Check key_trigger_1 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_1),
                msg="The key_trigger_1 parameter differs from the one expected")
        # end def check_key_trigger_1

        @staticmethod
        def check_key_trigger_2(test_case, event, expected):
            """
            Check key_trigger_2 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_2),
                msg="The key_trigger_2 parameter differs from the one expected")
        # end def check_key_trigger_2

        @staticmethod
        def check_key_trigger_3(test_case, event, expected):
            """
            Check key_trigger_3 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_3 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_3),
                msg="The key_trigger_3 parameter differs from the one expected")
        # end def check_key_trigger_3

        @staticmethod
        def check_key_trigger_4(test_case, event, expected):
            """
            Check key_trigger_4 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_4 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_4),
                msg="The key_trigger_4 parameter differs from the one expected")
        # end def check_key_trigger_4

        @staticmethod
        def check_key_trigger_5(test_case, event, expected):
            """
            Check key_trigger_5 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_5 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_5),
                msg="The key_trigger_5 parameter differs from the one expected")
        # end def check_key_trigger_5

        @staticmethod
        def check_key_trigger_6(test_case, event, expected):
            """
            Check key_trigger_6 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_6 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_6),
                msg="The key_trigger_6 parameter differs from the one expected")
        # end def check_key_trigger_6

        @staticmethod
        def check_key_trigger_7(test_case, event, expected):
            """
            Check key_trigger_7 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_7 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_7),
                msg="The key_trigger_7 parameter differs from the one expected")
        # end def check_key_trigger_7

        @staticmethod
        def check_key_trigger_8(test_case, event, expected):
            """
            Check key_trigger_8 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_8 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_8),
                msg="The key_trigger_8 parameter differs from the one expected")
        # end def check_key_trigger_8

        @staticmethod
        def check_key_trigger_9(test_case, event, expected):
            """
            Check key_trigger_9 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_9 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_9),
                msg="The key_trigger_9 parameter differs from the one expected")
        # end def check_key_trigger_9

        @staticmethod
        def check_key_trigger_10(test_case, event, expected):
            """
            Check key_trigger_10 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_10 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_10),
                msg="The key_trigger_10 parameter differs from the one expected")
        # end def check_key_trigger_10

        @staticmethod
        def check_key_trigger_11(test_case, event, expected):
            """
            Check key_trigger_11 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_11 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_11),
                msg="The key_trigger_11 parameter differs from the one expected")
        # end def check_key_trigger_11

        @staticmethod
        def check_key_trigger_12(test_case, event, expected):
            """
            Check key_trigger_12 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_12 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_12),
                msg="The key_trigger_12 parameter differs from the one expected")
        # end def check_key_trigger_12

        @staticmethod
        def check_key_trigger_13(test_case, event, expected):
            """
            Check key_trigger_13 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_13 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_13),
                msg="The key_trigger_13 parameter differs from the one expected")
        # end def check_key_trigger_13

        @staticmethod
        def check_key_trigger_14(test_case, event, expected):
            """
            Check key_trigger_14 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_14 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_14),
                msg="The key_trigger_14 parameter differs from the one expected")
        # end def check_key_trigger_14

        @staticmethod
        def check_key_trigger_15(test_case, event, expected):
            """
            Check key_trigger_15 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BaseLayerTriggerAsListEvent to check
            :type event: ``BaseLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_15 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_15),
                msg="The key_trigger_15 parameter differs from the one expected")
        # end def check_key_trigger_15
    # end class BaseLayerTriggerAsListEventChecker

    class KeyTriggerBitmapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeyTriggerBitmap``
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
                "fkc_idx_7": (cls.check_fkc_idx_7, 0),
                "fkc_idx_6": (cls.check_fkc_idx_6, 0),
                "fkc_idx_5": (cls.check_fkc_idx_5, 0),
                "fkc_idx_4": (cls.check_fkc_idx_4, 0),
                "fkc_idx_3": (cls.check_fkc_idx_3, 0),
                "fkc_idx_2": (cls.check_fkc_idx_2, 0),
                "fkc_idx_1": (cls.check_fkc_idx_1, 0),
                "fkc_idx_0": (cls.check_fkc_idx_0, 0),
                "fkc_idx_15": (cls.check_fkc_idx_15, 0),
                "fkc_idx_14": (cls.check_fkc_idx_14, 0),
                "fkc_idx_13": (cls.check_fkc_idx_13, 0),
                "fkc_idx_12": (cls.check_fkc_idx_12, 0),
                "fkc_idx_11": (cls.check_fkc_idx_11, 0),
                "fkc_idx_10": (cls.check_fkc_idx_10, 0),
                "fkc_idx_9": (cls.check_fkc_idx_9, 0),
                "fkc_idx_8": (cls.check_fkc_idx_8, 0),
                "fkc_idx_23": (cls.check_fkc_idx_23, 0),
                "fkc_idx_22": (cls.check_fkc_idx_22, 0),
                "fkc_idx_21": (cls.check_fkc_idx_21, 0),
                "fkc_idx_20": (cls.check_fkc_idx_20, 0),
                "fkc_idx_19": (cls.check_fkc_idx_19, 0),
                "fkc_idx_18": (cls.check_fkc_idx_18, 0),
                "fkc_idx_17": (cls.check_fkc_idx_17, 0),
                "fkc_idx_16": (cls.check_fkc_idx_16, 0),
                "fkc_idx_31": (cls.check_fkc_idx_31, 0),
                "fkc_idx_30": (cls.check_fkc_idx_30, 0),
                "fkc_idx_29": (cls.check_fkc_idx_29, 0),
                "fkc_idx_28": (cls.check_fkc_idx_28, 0),
                "fkc_idx_27": (cls.check_fkc_idx_27, 0),
                "fkc_idx_26": (cls.check_fkc_idx_26, 0),
                "fkc_idx_25": (cls.check_fkc_idx_25, 0),
                "fkc_idx_24": (cls.check_fkc_idx_24, 0),
                "fkc_idx_39": (cls.check_fkc_idx_39, 0),
                "fkc_idx_38": (cls.check_fkc_idx_38, 0),
                "fkc_idx_37": (cls.check_fkc_idx_37, 0),
                "fkc_idx_36": (cls.check_fkc_idx_36, 0),
                "fkc_idx_35": (cls.check_fkc_idx_35, 0),
                "fkc_idx_34": (cls.check_fkc_idx_34, 0),
                "fkc_idx_33": (cls.check_fkc_idx_33, 0),
                "fkc_idx_32": (cls.check_fkc_idx_32, 0),
                "fkc_idx_47": (cls.check_fkc_idx_47, 0),
                "fkc_idx_46": (cls.check_fkc_idx_46, 0),
                "fkc_idx_45": (cls.check_fkc_idx_45, 0),
                "fkc_idx_44": (cls.check_fkc_idx_44, 0),
                "fkc_idx_43": (cls.check_fkc_idx_43, 0),
                "fkc_idx_42": (cls.check_fkc_idx_42, 0),
                "fkc_idx_41": (cls.check_fkc_idx_41, 0),
                "fkc_idx_40": (cls.check_fkc_idx_40, 0),
                "fkc_idx_55": (cls.check_fkc_idx_55, 0),
                "fkc_idx_54": (cls.check_fkc_idx_54, 0),
                "fkc_idx_53": (cls.check_fkc_idx_53, 0),
                "fkc_idx_52": (cls.check_fkc_idx_52, 0),
                "fkc_idx_51": (cls.check_fkc_idx_51, 0),
                "fkc_idx_50": (cls.check_fkc_idx_50, 0),
                "fkc_idx_49": (cls.check_fkc_idx_49, 0),
                "fkc_idx_48": (cls.check_fkc_idx_48, 0),
                "fkc_idx_63": (cls.check_fkc_idx_63, 0),
                "fkc_idx_62": (cls.check_fkc_idx_62, 0),
                "fkc_idx_61": (cls.check_fkc_idx_61, 0),
                "fkc_idx_60": (cls.check_fkc_idx_60, 0),
                "fkc_idx_59": (cls.check_fkc_idx_59, 0),
                "fkc_idx_58": (cls.check_fkc_idx_58, 0),
                "fkc_idx_57": (cls.check_fkc_idx_57, 0),
                "fkc_idx_56": (cls.check_fkc_idx_56, 0),
                "fkc_idx_71": (cls.check_fkc_idx_71, 0),
                "fkc_idx_70": (cls.check_fkc_idx_70, 0),
                "fkc_idx_69": (cls.check_fkc_idx_69, 0),
                "fkc_idx_68": (cls.check_fkc_idx_68, 0),
                "fkc_idx_67": (cls.check_fkc_idx_67, 0),
                "fkc_idx_66": (cls.check_fkc_idx_66, 0),
                "fkc_idx_65": (cls.check_fkc_idx_65, 0),
                "fkc_idx_64": (cls.check_fkc_idx_64, 0),
                "fkc_idx_79": (cls.check_fkc_idx_79, 0),
                "fkc_idx_78": (cls.check_fkc_idx_78, 0),
                "fkc_idx_77": (cls.check_fkc_idx_77, 0),
                "fkc_idx_76": (cls.check_fkc_idx_76, 0),
                "fkc_idx_75": (cls.check_fkc_idx_75, 0),
                "fkc_idx_74": (cls.check_fkc_idx_74, 0),
                "fkc_idx_73": (cls.check_fkc_idx_73, 0),
                "fkc_idx_72": (cls.check_fkc_idx_72, 0),
                "fkc_idx_87": (cls.check_fkc_idx_87, 0),
                "fkc_idx_86": (cls.check_fkc_idx_86, 0),
                "fkc_idx_85": (cls.check_fkc_idx_85, 0),
                "fkc_idx_84": (cls.check_fkc_idx_84, 0),
                "fkc_idx_83": (cls.check_fkc_idx_83, 0),
                "fkc_idx_82": (cls.check_fkc_idx_82, 0),
                "fkc_idx_81": (cls.check_fkc_idx_81, 0),
                "fkc_idx_80": (cls.check_fkc_idx_80, 0),
                "fkc_idx_95": (cls.check_fkc_idx_95, 0),
                "fkc_idx_94": (cls.check_fkc_idx_94, 0),
                "fkc_idx_93": (cls.check_fkc_idx_93, 0),
                "fkc_idx_92": (cls.check_fkc_idx_92, 0),
                "fkc_idx_91": (cls.check_fkc_idx_91, 0),
                "fkc_idx_90": (cls.check_fkc_idx_90, 0),
                "fkc_idx_89": (cls.check_fkc_idx_89, 0),
                "fkc_idx_88": (cls.check_fkc_idx_88, 0),
                "fkc_idx_103": (cls.check_fkc_idx_103, 0),
                "fkc_idx_102": (cls.check_fkc_idx_102, 0),
                "fkc_idx_101": (cls.check_fkc_idx_101, 0),
                "fkc_idx_100": (cls.check_fkc_idx_100, 0),
                "fkc_idx_99": (cls.check_fkc_idx_99, 0),
                "fkc_idx_98": (cls.check_fkc_idx_98, 0),
                "fkc_idx_97": (cls.check_fkc_idx_97, 0),
                "fkc_idx_96": (cls.check_fkc_idx_96, 0),
                "fkc_idx_111": (cls.check_fkc_idx_111, 0),
                "fkc_idx_110": (cls.check_fkc_idx_110, 0),
                "fkc_idx_109": (cls.check_fkc_idx_109, 0),
                "fkc_idx_108": (cls.check_fkc_idx_108, 0),
                "fkc_idx_107": (cls.check_fkc_idx_107, 0),
                "fkc_idx_106": (cls.check_fkc_idx_106, 0),
                "fkc_idx_105": (cls.check_fkc_idx_105, 0),
                "fkc_idx_104": (cls.check_fkc_idx_104, 0),
                "fkc_idx_119": (cls.check_fkc_idx_119, 0),
                "fkc_idx_118": (cls.check_fkc_idx_118, 0),
                "fkc_idx_117": (cls.check_fkc_idx_117, 0),
                "fkc_idx_116": (cls.check_fkc_idx_116, 0),
                "fkc_idx_115": (cls.check_fkc_idx_115, 0),
                "fkc_idx_114": (cls.check_fkc_idx_114, 0),
                "fkc_idx_113": (cls.check_fkc_idx_113, 0),
                "fkc_idx_112": (cls.check_fkc_idx_112, 0),
                "fkc_idx_127": (cls.check_fkc_idx_127, 0),
                "fkc_idx_126": (cls.check_fkc_idx_126, 0),
                "fkc_idx_125": (cls.check_fkc_idx_125, 0),
                "fkc_idx_124": (cls.check_fkc_idx_124, 0),
                "fkc_idx_123": (cls.check_fkc_idx_123, 0),
                "fkc_idx_122": (cls.check_fkc_idx_122, 0),
                "fkc_idx_121": (cls.check_fkc_idx_121, 0),
                "fkc_idx_120": (cls.check_fkc_idx_120, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_fkc_idx_7(test_case, bitmap, expected):
            """
            Check fkc_idx_7 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_7 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_7),
                msg="The fkc_idx_7 parameter differs from the one expected")
        # end def check_fkc_idx_7

        @staticmethod
        def check_fkc_idx_6(test_case, bitmap, expected):
            """
            Check fkc_idx_6 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_6 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_6),
                msg="The fkc_idx_6 parameter differs from the one expected")
        # end def check_fkc_idx_6

        @staticmethod
        def check_fkc_idx_5(test_case, bitmap, expected):
            """
            Check fkc_idx_5 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_5 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_5),
                msg="The fkc_idx_5 parameter differs from the one expected")
        # end def check_fkc_idx_5

        @staticmethod
        def check_fkc_idx_4(test_case, bitmap, expected):
            """
            Check fkc_idx_4 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_4 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_4),
                msg="The fkc_idx_4 parameter differs from the one expected")
        # end def check_fkc_idx_4

        @staticmethod
        def check_fkc_idx_3(test_case, bitmap, expected):
            """
            Check fkc_idx_3 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_3 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_3),
                msg="The fkc_idx_3 parameter differs from the one expected")
        # end def check_fkc_idx_3

        @staticmethod
        def check_fkc_idx_2(test_case, bitmap, expected):
            """
            Check fkc_idx_2 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_2),
                msg="The fkc_idx_2 parameter differs from the one expected")
        # end def check_fkc_idx_2

        @staticmethod
        def check_fkc_idx_1(test_case, bitmap, expected):
            """
            Check fkc_idx_1 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_1),
                msg="The fkc_idx_1 parameter differs from the one expected")
        # end def check_fkc_idx_1

        @staticmethod
        def check_fkc_idx_0(test_case, bitmap, expected):
            """
            Check fkc_idx_0 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_0 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_0),
                msg="The fkc_idx_0 parameter differs from the one expected")
        # end def check_fkc_idx_0

        @staticmethod
        def check_fkc_idx_15(test_case, bitmap, expected):
            """
            Check fkc_idx_15 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_15 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_15),
                msg="The fkc_idx_15 parameter differs from the one expected")
        # end def check_fkc_idx_15

        @staticmethod
        def check_fkc_idx_14(test_case, bitmap, expected):
            """
            Check fkc_idx_14 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_14 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_14),
                msg="The fkc_idx_14 parameter differs from the one expected")
        # end def check_fkc_idx_14

        @staticmethod
        def check_fkc_idx_13(test_case, bitmap, expected):
            """
            Check fkc_idx_13 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_13 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_13),
                msg="The fkc_idx_13 parameter differs from the one expected")
        # end def check_fkc_idx_13

        @staticmethod
        def check_fkc_idx_12(test_case, bitmap, expected):
            """
            Check fkc_idx_12 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_12 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_12),
                msg="The fkc_idx_12 parameter differs from the one expected")
        # end def check_fkc_idx_12

        @staticmethod
        def check_fkc_idx_11(test_case, bitmap, expected):
            """
            Check fkc_idx_11 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_11 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_11),
                msg="The fkc_idx_11 parameter differs from the one expected")
        # end def check_fkc_idx_11

        @staticmethod
        def check_fkc_idx_10(test_case, bitmap, expected):
            """
            Check fkc_idx_10 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_10 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_10),
                msg="The fkc_idx_10 parameter differs from the one expected")
        # end def check_fkc_idx_10

        @staticmethod
        def check_fkc_idx_9(test_case, bitmap, expected):
            """
            Check fkc_idx_9 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_9 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_9),
                msg="The fkc_idx_9 parameter differs from the one expected")
        # end def check_fkc_idx_9

        @staticmethod
        def check_fkc_idx_8(test_case, bitmap, expected):
            """
            Check fkc_idx_8 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_8 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_8),
                msg="The fkc_idx_8 parameter differs from the one expected")
        # end def check_fkc_idx_8

        @staticmethod
        def check_fkc_idx_23(test_case, bitmap, expected):
            """
            Check fkc_idx_23 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_23 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_23),
                msg="The fkc_idx_23 parameter differs from the one expected")
        # end def check_fkc_idx_23

        @staticmethod
        def check_fkc_idx_22(test_case, bitmap, expected):
            """
            Check fkc_idx_22 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_22 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_22),
                msg="The fkc_idx_22 parameter differs from the one expected")
        # end def check_fkc_idx_22

        @staticmethod
        def check_fkc_idx_21(test_case, bitmap, expected):
            """
            Check fkc_idx_21 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_21 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_21),
                msg="The fkc_idx_21 parameter differs from the one expected")
        # end def check_fkc_idx_21

        @staticmethod
        def check_fkc_idx_20(test_case, bitmap, expected):
            """
            Check fkc_idx_20 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_20 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_20),
                msg="The fkc_idx_20 parameter differs from the one expected")
        # end def check_fkc_idx_20

        @staticmethod
        def check_fkc_idx_19(test_case, bitmap, expected):
            """
            Check fkc_idx_19 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_19 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_19),
                msg="The fkc_idx_19 parameter differs from the one expected")
        # end def check_fkc_idx_19

        @staticmethod
        def check_fkc_idx_18(test_case, bitmap, expected):
            """
            Check fkc_idx_18 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_18 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_18),
                msg="The fkc_idx_18 parameter differs from the one expected")
        # end def check_fkc_idx_18

        @staticmethod
        def check_fkc_idx_17(test_case, bitmap, expected):
            """
            Check fkc_idx_17 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_17 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_17),
                msg="The fkc_idx_17 parameter differs from the one expected")
        # end def check_fkc_idx_17

        @staticmethod
        def check_fkc_idx_16(test_case, bitmap, expected):
            """
            Check fkc_idx_16 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_16 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_16),
                msg="The fkc_idx_16 parameter differs from the one expected")
        # end def check_fkc_idx_16

        @staticmethod
        def check_fkc_idx_31(test_case, bitmap, expected):
            """
            Check fkc_idx_31 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_31 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_31),
                msg="The fkc_idx_31 parameter differs from the one expected")
        # end def check_fkc_idx_31

        @staticmethod
        def check_fkc_idx_30(test_case, bitmap, expected):
            """
            Check fkc_idx_30 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_30 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_30),
                msg="The fkc_idx_30 parameter differs from the one expected")
        # end def check_fkc_idx_30

        @staticmethod
        def check_fkc_idx_29(test_case, bitmap, expected):
            """
            Check fkc_idx_29 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_29 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_29),
                msg="The fkc_idx_29 parameter differs from the one expected")
        # end def check_fkc_idx_29

        @staticmethod
        def check_fkc_idx_28(test_case, bitmap, expected):
            """
            Check fkc_idx_28 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_28 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_28),
                msg="The fkc_idx_28 parameter differs from the one expected")
        # end def check_fkc_idx_28

        @staticmethod
        def check_fkc_idx_27(test_case, bitmap, expected):
            """
            Check fkc_idx_27 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_27 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_27),
                msg="The fkc_idx_27 parameter differs from the one expected")
        # end def check_fkc_idx_27

        @staticmethod
        def check_fkc_idx_26(test_case, bitmap, expected):
            """
            Check fkc_idx_26 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_26 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_26),
                msg="The fkc_idx_26 parameter differs from the one expected")
        # end def check_fkc_idx_26

        @staticmethod
        def check_fkc_idx_25(test_case, bitmap, expected):
            """
            Check fkc_idx_25 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_25 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_25),
                msg="The fkc_idx_25 parameter differs from the one expected")
        # end def check_fkc_idx_25

        @staticmethod
        def check_fkc_idx_24(test_case, bitmap, expected):
            """
            Check fkc_idx_24 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_24 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_24),
                msg="The fkc_idx_24 parameter differs from the one expected")
        # end def check_fkc_idx_24

        @staticmethod
        def check_fkc_idx_39(test_case, bitmap, expected):
            """
            Check fkc_idx_39 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_39 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_39),
                msg="The fkc_idx_39 parameter differs from the one expected")
        # end def check_fkc_idx_39

        @staticmethod
        def check_fkc_idx_38(test_case, bitmap, expected):
            """
            Check fkc_idx_38 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_38 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_38),
                msg="The fkc_idx_38 parameter differs from the one expected")
        # end def check_fkc_idx_38

        @staticmethod
        def check_fkc_idx_37(test_case, bitmap, expected):
            """
            Check fkc_idx_37 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_37 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_37),
                msg="The fkc_idx_37 parameter differs from the one expected")
        # end def check_fkc_idx_37

        @staticmethod
        def check_fkc_idx_36(test_case, bitmap, expected):
            """
            Check fkc_idx_36 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_36 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_36),
                msg="The fkc_idx_36 parameter differs from the one expected")
        # end def check_fkc_idx_36

        @staticmethod
        def check_fkc_idx_35(test_case, bitmap, expected):
            """
            Check fkc_idx_35 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_35 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_35),
                msg="The fkc_idx_35 parameter differs from the one expected")
        # end def check_fkc_idx_35

        @staticmethod
        def check_fkc_idx_34(test_case, bitmap, expected):
            """
            Check fkc_idx_34 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_34 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_34),
                msg="The fkc_idx_34 parameter differs from the one expected")
        # end def check_fkc_idx_34

        @staticmethod
        def check_fkc_idx_33(test_case, bitmap, expected):
            """
            Check fkc_idx_33 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_33 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_33),
                msg="The fkc_idx_33 parameter differs from the one expected")
        # end def check_fkc_idx_33

        @staticmethod
        def check_fkc_idx_32(test_case, bitmap, expected):
            """
            Check fkc_idx_32 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_32 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_32),
                msg="The fkc_idx_32 parameter differs from the one expected")
        # end def check_fkc_idx_32

        @staticmethod
        def check_fkc_idx_47(test_case, bitmap, expected):
            """
            Check fkc_idx_47 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_47 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_47),
                msg="The fkc_idx_47 parameter differs from the one expected")
        # end def check_fkc_idx_47

        @staticmethod
        def check_fkc_idx_46(test_case, bitmap, expected):
            """
            Check fkc_idx_46 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_46 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_46),
                msg="The fkc_idx_46 parameter differs from the one expected")
        # end def check_fkc_idx_46

        @staticmethod
        def check_fkc_idx_45(test_case, bitmap, expected):
            """
            Check fkc_idx_45 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_45 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_45),
                msg="The fkc_idx_45 parameter differs from the one expected")
        # end def check_fkc_idx_45

        @staticmethod
        def check_fkc_idx_44(test_case, bitmap, expected):
            """
            Check fkc_idx_44 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_44 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_44),
                msg="The fkc_idx_44 parameter differs from the one expected")
        # end def check_fkc_idx_44

        @staticmethod
        def check_fkc_idx_43(test_case, bitmap, expected):
            """
            Check fkc_idx_43 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_43 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_43),
                msg="The fkc_idx_43 parameter differs from the one expected")
        # end def check_fkc_idx_43

        @staticmethod
        def check_fkc_idx_42(test_case, bitmap, expected):
            """
            Check fkc_idx_42 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_42 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_42),
                msg="The fkc_idx_42 parameter differs from the one expected")
        # end def check_fkc_idx_42

        @staticmethod
        def check_fkc_idx_41(test_case, bitmap, expected):
            """
            Check fkc_idx_41 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_41 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_41),
                msg="The fkc_idx_41 parameter differs from the one expected")
        # end def check_fkc_idx_41

        @staticmethod
        def check_fkc_idx_40(test_case, bitmap, expected):
            """
            Check fkc_idx_40 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_40 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_40),
                msg="The fkc_idx_40 parameter differs from the one expected")
        # end def check_fkc_idx_40

        @staticmethod
        def check_fkc_idx_55(test_case, bitmap, expected):
            """
            Check fkc_idx_55 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_55 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_55),
                msg="The fkc_idx_55 parameter differs from the one expected")
        # end def check_fkc_idx_55

        @staticmethod
        def check_fkc_idx_54(test_case, bitmap, expected):
            """
            Check fkc_idx_54 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_54 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_54),
                msg="The fkc_idx_54 parameter differs from the one expected")
        # end def check_fkc_idx_54

        @staticmethod
        def check_fkc_idx_53(test_case, bitmap, expected):
            """
            Check fkc_idx_53 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_53 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_53),
                msg="The fkc_idx_53 parameter differs from the one expected")
        # end def check_fkc_idx_53

        @staticmethod
        def check_fkc_idx_52(test_case, bitmap, expected):
            """
            Check fkc_idx_52 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_52 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_52),
                msg="The fkc_idx_52 parameter differs from the one expected")
        # end def check_fkc_idx_52

        @staticmethod
        def check_fkc_idx_51(test_case, bitmap, expected):
            """
            Check fkc_idx_51 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_51 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_51),
                msg="The fkc_idx_51 parameter differs from the one expected")
        # end def check_fkc_idx_51

        @staticmethod
        def check_fkc_idx_50(test_case, bitmap, expected):
            """
            Check fkc_idx_50 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_50 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_50),
                msg="The fkc_idx_50 parameter differs from the one expected")
        # end def check_fkc_idx_50

        @staticmethod
        def check_fkc_idx_49(test_case, bitmap, expected):
            """
            Check fkc_idx_49 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_49 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_49),
                msg="The fkc_idx_49 parameter differs from the one expected")
        # end def check_fkc_idx_49

        @staticmethod
        def check_fkc_idx_48(test_case, bitmap, expected):
            """
            Check fkc_idx_48 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_48 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_48),
                msg="The fkc_idx_48 parameter differs from the one expected")
        # end def check_fkc_idx_48

        @staticmethod
        def check_fkc_idx_63(test_case, bitmap, expected):
            """
            Check fkc_idx_63 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_63 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_63),
                msg="The fkc_idx_63 parameter differs from the one expected")
        # end def check_fkc_idx_63

        @staticmethod
        def check_fkc_idx_62(test_case, bitmap, expected):
            """
            Check fkc_idx_62 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_62 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_62),
                msg="The fkc_idx_62 parameter differs from the one expected")
        # end def check_fkc_idx_62

        @staticmethod
        def check_fkc_idx_61(test_case, bitmap, expected):
            """
            Check fkc_idx_61 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_61 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_61),
                msg="The fkc_idx_61 parameter differs from the one expected")
        # end def check_fkc_idx_61

        @staticmethod
        def check_fkc_idx_60(test_case, bitmap, expected):
            """
            Check fkc_idx_60 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_60 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_60),
                msg="The fkc_idx_60 parameter differs from the one expected")
        # end def check_fkc_idx_60

        @staticmethod
        def check_fkc_idx_59(test_case, bitmap, expected):
            """
            Check fkc_idx_59 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_59 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_59),
                msg="The fkc_idx_59 parameter differs from the one expected")
        # end def check_fkc_idx_59

        @staticmethod
        def check_fkc_idx_58(test_case, bitmap, expected):
            """
            Check fkc_idx_58 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_58 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_58),
                msg="The fkc_idx_58 parameter differs from the one expected")
        # end def check_fkc_idx_58

        @staticmethod
        def check_fkc_idx_57(test_case, bitmap, expected):
            """
            Check fkc_idx_57 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_57 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_57),
                msg="The fkc_idx_57 parameter differs from the one expected")
        # end def check_fkc_idx_57

        @staticmethod
        def check_fkc_idx_56(test_case, bitmap, expected):
            """
            Check fkc_idx_56 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_56 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_56),
                msg="The fkc_idx_56 parameter differs from the one expected")
        # end def check_fkc_idx_56

        @staticmethod
        def check_fkc_idx_71(test_case, bitmap, expected):
            """
            Check fkc_idx_71 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_71 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_71),
                msg="The fkc_idx_71 parameter differs from the one expected")
        # end def check_fkc_idx_71

        @staticmethod
        def check_fkc_idx_70(test_case, bitmap, expected):
            """
            Check fkc_idx_70 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_70 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_70),
                msg="The fkc_idx_70 parameter differs from the one expected")
        # end def check_fkc_idx_70

        @staticmethod
        def check_fkc_idx_69(test_case, bitmap, expected):
            """
            Check fkc_idx_69 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_69 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_69),
                msg="The fkc_idx_69 parameter differs from the one expected")
        # end def check_fkc_idx_69

        @staticmethod
        def check_fkc_idx_68(test_case, bitmap, expected):
            """
            Check fkc_idx_68 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_68 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_68),
                msg="The fkc_idx_68 parameter differs from the one expected")
        # end def check_fkc_idx_68

        @staticmethod
        def check_fkc_idx_67(test_case, bitmap, expected):
            """
            Check fkc_idx_67 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_67 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_67),
                msg="The fkc_idx_67 parameter differs from the one expected")
        # end def check_fkc_idx_67

        @staticmethod
        def check_fkc_idx_66(test_case, bitmap, expected):
            """
            Check fkc_idx_66 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_66 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_66),
                msg="The fkc_idx_66 parameter differs from the one expected")
        # end def check_fkc_idx_66

        @staticmethod
        def check_fkc_idx_65(test_case, bitmap, expected):
            """
            Check fkc_idx_65 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_65 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_65),
                msg="The fkc_idx_65 parameter differs from the one expected")
        # end def check_fkc_idx_65

        @staticmethod
        def check_fkc_idx_64(test_case, bitmap, expected):
            """
            Check fkc_idx_64 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_64 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_64),
                msg="The fkc_idx_64 parameter differs from the one expected")
        # end def check_fkc_idx_64

        @staticmethod
        def check_fkc_idx_79(test_case, bitmap, expected):
            """
            Check fkc_idx_79 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_79 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_79),
                msg="The fkc_idx_79 parameter differs from the one expected")
        # end def check_fkc_idx_79

        @staticmethod
        def check_fkc_idx_78(test_case, bitmap, expected):
            """
            Check fkc_idx_78 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_78 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_78),
                msg="The fkc_idx_78 parameter differs from the one expected")
        # end def check_fkc_idx_78

        @staticmethod
        def check_fkc_idx_77(test_case, bitmap, expected):
            """
            Check fkc_idx_77 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_77 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_77),
                msg="The fkc_idx_77 parameter differs from the one expected")
        # end def check_fkc_idx_77

        @staticmethod
        def check_fkc_idx_76(test_case, bitmap, expected):
            """
            Check fkc_idx_76 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_76 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_76),
                msg="The fkc_idx_76 parameter differs from the one expected")
        # end def check_fkc_idx_76

        @staticmethod
        def check_fkc_idx_75(test_case, bitmap, expected):
            """
            Check fkc_idx_75 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_75 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_75),
                msg="The fkc_idx_75 parameter differs from the one expected")
        # end def check_fkc_idx_75

        @staticmethod
        def check_fkc_idx_74(test_case, bitmap, expected):
            """
            Check fkc_idx_74 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_74 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_74),
                msg="The fkc_idx_74 parameter differs from the one expected")
        # end def check_fkc_idx_74

        @staticmethod
        def check_fkc_idx_73(test_case, bitmap, expected):
            """
            Check fkc_idx_73 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_73 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_73),
                msg="The fkc_idx_73 parameter differs from the one expected")
        # end def check_fkc_idx_73

        @staticmethod
        def check_fkc_idx_72(test_case, bitmap, expected):
            """
            Check fkc_idx_72 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_72 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_72),
                msg="The fkc_idx_72 parameter differs from the one expected")
        # end def check_fkc_idx_72

        @staticmethod
        def check_fkc_idx_87(test_case, bitmap, expected):
            """
            Check fkc_idx_87 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_87 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_87),
                msg="The fkc_idx_87 parameter differs from the one expected")
        # end def check_fkc_idx_87

        @staticmethod
        def check_fkc_idx_86(test_case, bitmap, expected):
            """
            Check fkc_idx_86 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_86 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_86),
                msg="The fkc_idx_86 parameter differs from the one expected")
        # end def check_fkc_idx_86

        @staticmethod
        def check_fkc_idx_85(test_case, bitmap, expected):
            """
            Check fkc_idx_85 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_85 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_85),
                msg="The fkc_idx_85 parameter differs from the one expected")
        # end def check_fkc_idx_85

        @staticmethod
        def check_fkc_idx_84(test_case, bitmap, expected):
            """
            Check fkc_idx_84 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_84 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_84),
                msg="The fkc_idx_84 parameter differs from the one expected")
        # end def check_fkc_idx_84

        @staticmethod
        def check_fkc_idx_83(test_case, bitmap, expected):
            """
            Check fkc_idx_83 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_83 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_83),
                msg="The fkc_idx_83 parameter differs from the one expected")
        # end def check_fkc_idx_83

        @staticmethod
        def check_fkc_idx_82(test_case, bitmap, expected):
            """
            Check fkc_idx_82 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_82 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_82),
                msg="The fkc_idx_82 parameter differs from the one expected")
        # end def check_fkc_idx_82

        @staticmethod
        def check_fkc_idx_81(test_case, bitmap, expected):
            """
            Check fkc_idx_81 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_81 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_81),
                msg="The fkc_idx_81 parameter differs from the one expected")
        # end def check_fkc_idx_81

        @staticmethod
        def check_fkc_idx_80(test_case, bitmap, expected):
            """
            Check fkc_idx_80 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_80 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_80),
                msg="The fkc_idx_80 parameter differs from the one expected")
        # end def check_fkc_idx_80

        @staticmethod
        def check_fkc_idx_95(test_case, bitmap, expected):
            """
            Check fkc_idx_95 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_95 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_95),
                msg="The fkc_idx_95 parameter differs from the one expected")
        # end def check_fkc_idx_95

        @staticmethod
        def check_fkc_idx_94(test_case, bitmap, expected):
            """
            Check fkc_idx_94 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_94 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_94),
                msg="The fkc_idx_94 parameter differs from the one expected")
        # end def check_fkc_idx_94

        @staticmethod
        def check_fkc_idx_93(test_case, bitmap, expected):
            """
            Check fkc_idx_93 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_93 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_93),
                msg="The fkc_idx_93 parameter differs from the one expected")
        # end def check_fkc_idx_93

        @staticmethod
        def check_fkc_idx_92(test_case, bitmap, expected):
            """
            Check fkc_idx_92 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_92 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_92),
                msg="The fkc_idx_92 parameter differs from the one expected")
        # end def check_fkc_idx_92

        @staticmethod
        def check_fkc_idx_91(test_case, bitmap, expected):
            """
            Check fkc_idx_91 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_91 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_91),
                msg="The fkc_idx_91 parameter differs from the one expected")
        # end def check_fkc_idx_91

        @staticmethod
        def check_fkc_idx_90(test_case, bitmap, expected):
            """
            Check fkc_idx_90 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_90 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_90),
                msg="The fkc_idx_90 parameter differs from the one expected")
        # end def check_fkc_idx_90

        @staticmethod
        def check_fkc_idx_89(test_case, bitmap, expected):
            """
            Check fkc_idx_89 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_89 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_89),
                msg="The fkc_idx_89 parameter differs from the one expected")
        # end def check_fkc_idx_89

        @staticmethod
        def check_fkc_idx_88(test_case, bitmap, expected):
            """
            Check fkc_idx_88 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_88 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_88),
                msg="The fkc_idx_88 parameter differs from the one expected")
        # end def check_fkc_idx_88

        @staticmethod
        def check_fkc_idx_103(test_case, bitmap, expected):
            """
            Check fkc_idx_103 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_103 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_103),
                msg="The fkc_idx_103 parameter differs from the one expected")
        # end def check_fkc_idx_103

        @staticmethod
        def check_fkc_idx_102(test_case, bitmap, expected):
            """
            Check fkc_idx_102 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_102 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_102),
                msg="The fkc_idx_102 parameter differs from the one expected")
        # end def check_fkc_idx_102

        @staticmethod
        def check_fkc_idx_101(test_case, bitmap, expected):
            """
            Check fkc_idx_101 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_101 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_101),
                msg="The fkc_idx_101 parameter differs from the one expected")
        # end def check_fkc_idx_101

        @staticmethod
        def check_fkc_idx_100(test_case, bitmap, expected):
            """
            Check fkc_idx_100 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_100 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_100),
                msg="The fkc_idx_100 parameter differs from the one expected")
        # end def check_fkc_idx_100

        @staticmethod
        def check_fkc_idx_99(test_case, bitmap, expected):
            """
            Check fkc_idx_99 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_99 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_99),
                msg="The fkc_idx_99 parameter differs from the one expected")
        # end def check_fkc_idx_99

        @staticmethod
        def check_fkc_idx_98(test_case, bitmap, expected):
            """
            Check fkc_idx_98 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_98 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_98),
                msg="The fkc_idx_98 parameter differs from the one expected")
        # end def check_fkc_idx_98

        @staticmethod
        def check_fkc_idx_97(test_case, bitmap, expected):
            """
            Check fkc_idx_97 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_97 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_97),
                msg="The fkc_idx_97 parameter differs from the one expected")
        # end def check_fkc_idx_97

        @staticmethod
        def check_fkc_idx_96(test_case, bitmap, expected):
            """
            Check fkc_idx_96 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_96 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_96),
                msg="The fkc_idx_96 parameter differs from the one expected")
        # end def check_fkc_idx_96

        @staticmethod
        def check_fkc_idx_111(test_case, bitmap, expected):
            """
            Check fkc_idx_111 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_111 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_111),
                msg="The fkc_idx_111 parameter differs from the one expected")
        # end def check_fkc_idx_111

        @staticmethod
        def check_fkc_idx_110(test_case, bitmap, expected):
            """
            Check fkc_idx_110 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_110 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_110),
                msg="The fkc_idx_110 parameter differs from the one expected")
        # end def check_fkc_idx_110

        @staticmethod
        def check_fkc_idx_109(test_case, bitmap, expected):
            """
            Check fkc_idx_109 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_109 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_109),
                msg="The fkc_idx_109 parameter differs from the one expected")
        # end def check_fkc_idx_109

        @staticmethod
        def check_fkc_idx_108(test_case, bitmap, expected):
            """
            Check fkc_idx_108 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_108 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_108),
                msg="The fkc_idx_108 parameter differs from the one expected")
        # end def check_fkc_idx_108

        @staticmethod
        def check_fkc_idx_107(test_case, bitmap, expected):
            """
            Check fkc_idx_107 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_107 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_107),
                msg="The fkc_idx_107 parameter differs from the one expected")
        # end def check_fkc_idx_107

        @staticmethod
        def check_fkc_idx_106(test_case, bitmap, expected):
            """
            Check fkc_idx_106 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_106 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_106),
                msg="The fkc_idx_106 parameter differs from the one expected")
        # end def check_fkc_idx_106

        @staticmethod
        def check_fkc_idx_105(test_case, bitmap, expected):
            """
            Check fkc_idx_105 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_105 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_105),
                msg="The fkc_idx_105 parameter differs from the one expected")
        # end def check_fkc_idx_105

        @staticmethod
        def check_fkc_idx_104(test_case, bitmap, expected):
            """
            Check fkc_idx_104 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_104 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_104),
                msg="The fkc_idx_104 parameter differs from the one expected")
        # end def check_fkc_idx_104

        @staticmethod
        def check_fkc_idx_119(test_case, bitmap, expected):
            """
            Check fkc_idx_119 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_119 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_119),
                msg="The fkc_idx_119 parameter differs from the one expected")
        # end def check_fkc_idx_119

        @staticmethod
        def check_fkc_idx_118(test_case, bitmap, expected):
            """
            Check fkc_idx_118 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_118 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_118),
                msg="The fkc_idx_118 parameter differs from the one expected")
        # end def check_fkc_idx_118

        @staticmethod
        def check_fkc_idx_117(test_case, bitmap, expected):
            """
            Check fkc_idx_117 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_117 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_117),
                msg="The fkc_idx_117 parameter differs from the one expected")
        # end def check_fkc_idx_117

        @staticmethod
        def check_fkc_idx_116(test_case, bitmap, expected):
            """
            Check fkc_idx_116 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_116 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_116),
                msg="The fkc_idx_116 parameter differs from the one expected")
        # end def check_fkc_idx_116

        @staticmethod
        def check_fkc_idx_115(test_case, bitmap, expected):
            """
            Check fkc_idx_115 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_115 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_115),
                msg="The fkc_idx_115 parameter differs from the one expected")
        # end def check_fkc_idx_115

        @staticmethod
        def check_fkc_idx_114(test_case, bitmap, expected):
            """
            Check fkc_idx_114 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_114 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_114),
                msg="The fkc_idx_114 parameter differs from the one expected")
        # end def check_fkc_idx_114

        @staticmethod
        def check_fkc_idx_113(test_case, bitmap, expected):
            """
            Check fkc_idx_113 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_113 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_113),
                msg="The fkc_idx_113 parameter differs from the one expected")
        # end def check_fkc_idx_113

        @staticmethod
        def check_fkc_idx_112(test_case, bitmap, expected):
            """
            Check fkc_idx_112 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_112 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_112),
                msg="The fkc_idx_112 parameter differs from the one expected")
        # end def check_fkc_idx_112

        @staticmethod
        def check_fkc_idx_127(test_case, bitmap, expected):
            """
            Check fkc_idx_127 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_127 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_127),
                msg="The fkc_idx_127 parameter differs from the one expected")
        # end def check_fkc_idx_127

        @staticmethod
        def check_fkc_idx_126(test_case, bitmap, expected):
            """
            Check fkc_idx_126 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_126 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_126),
                msg="The fkc_idx_126 parameter differs from the one expected")
        # end def check_fkc_idx_126

        @staticmethod
        def check_fkc_idx_125(test_case, bitmap, expected):
            """
            Check fkc_idx_125 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_125 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_125),
                msg="The fkc_idx_125 parameter differs from the one expected")
        # end def check_fkc_idx_125

        @staticmethod
        def check_fkc_idx_124(test_case, bitmap, expected):
            """
            Check fkc_idx_124 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_124 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_124),
                msg="The fkc_idx_124 parameter differs from the one expected")
        # end def check_fkc_idx_124

        @staticmethod
        def check_fkc_idx_123(test_case, bitmap, expected):
            """
            Check fkc_idx_123 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_123 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_123),
                msg="The fkc_idx_123 parameter differs from the one expected")
        # end def check_fkc_idx_123

        @staticmethod
        def check_fkc_idx_122(test_case, bitmap, expected):
            """
            Check fkc_idx_122 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_122 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_122),
                msg="The fkc_idx_122 parameter differs from the one expected")
        # end def check_fkc_idx_122

        @staticmethod
        def check_fkc_idx_121(test_case, bitmap, expected):
            """
            Check fkc_idx_121 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_121 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_121),
                msg="The fkc_idx_121 parameter differs from the one expected")
        # end def check_fkc_idx_121

        @staticmethod
        def check_fkc_idx_120(test_case, bitmap, expected):
            """
            Check fkc_idx_120 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTriggerBitmap to check
            :type bitmap: ``FullKeyCustomization.KeyTriggerBitmap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fkc_idx_120 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.fkc_idx_120),
                msg="The fkc_idx_120 parameter differs from the one expected")
        # end def check_fkc_idx_120
    # end class KeyTriggerBitmapChecker

    class BaseLayerTriggerAsBitmapEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``BaseLayerTriggerAsBitmapEvent``
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
                "key_trigger_bitmap": (
                    cls.check_key_trigger_bitmap,
                    FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_trigger_bitmap(test_case, message, expected):
            """
            Check ``key_trigger_bitmap``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: BaseLayerTriggerAsBitmapEvent to check
            :type message: ``BaseLayerTriggerAsBitmapEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker.check_fields(
                test_case, message.key_trigger_bitmap, FullKeyCustomization.KeyTriggerBitmap, expected)
        # end def check_key_trigger_bitmap
    # end class BaseLayerTriggerAsBitmapEventChecker

    class FNLayerTriggerAsListEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``FNLayerTriggerAsListEvent``
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
                "key_trigger_0": (cls.check_key_trigger_0, 0),
                "key_trigger_1": (cls.check_key_trigger_1, 0),
                "key_trigger_2": (cls.check_key_trigger_2, 0),
                "key_trigger_3": (cls.check_key_trigger_3, 0),
                "key_trigger_4": (cls.check_key_trigger_4, 0),
                "key_trigger_5": (cls.check_key_trigger_5, 0),
                "key_trigger_6": (cls.check_key_trigger_6, 0),
                "key_trigger_7": (cls.check_key_trigger_7, 0),
                "key_trigger_8": (cls.check_key_trigger_8, 0),
                "key_trigger_9": (cls.check_key_trigger_9, 0),
                "key_trigger_10": (cls.check_key_trigger_10, 0),
                "key_trigger_11": (cls.check_key_trigger_11, 0),
                "key_trigger_12": (cls.check_key_trigger_12, 0),
                "key_trigger_13": (cls.check_key_trigger_13, 0),
                "key_trigger_14": (cls.check_key_trigger_14, 0),
                "key_trigger_15": (cls.check_key_trigger_15, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_trigger_0(test_case, event, expected):
            """
            Check key_trigger_0 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_0 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_0),
                msg="The key_trigger_0 parameter differs from the one expected")
        # end def check_key_trigger_0

        @staticmethod
        def check_key_trigger_1(test_case, event, expected):
            """
            Check key_trigger_1 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_1),
                msg="The key_trigger_1 parameter differs from the one expected")
        # end def check_key_trigger_1

        @staticmethod
        def check_key_trigger_2(test_case, event, expected):
            """
            Check key_trigger_2 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_2),
                msg="The key_trigger_2 parameter differs from the one expected")
        # end def check_key_trigger_2

        @staticmethod
        def check_key_trigger_3(test_case, event, expected):
            """
            Check key_trigger_3 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_3 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_3),
                msg="The key_trigger_3 parameter differs from the one expected")
        # end def check_key_trigger_3

        @staticmethod
        def check_key_trigger_4(test_case, event, expected):
            """
            Check key_trigger_4 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_4 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_4),
                msg="The key_trigger_4 parameter differs from the one expected")
        # end def check_key_trigger_4

        @staticmethod
        def check_key_trigger_5(test_case, event, expected):
            """
            Check key_trigger_5 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_5 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_5),
                msg="The key_trigger_5 parameter differs from the one expected")
        # end def check_key_trigger_5

        @staticmethod
        def check_key_trigger_6(test_case, event, expected):
            """
            Check key_trigger_6 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_6 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_6),
                msg="The key_trigger_6 parameter differs from the one expected")
        # end def check_key_trigger_6

        @staticmethod
        def check_key_trigger_7(test_case, event, expected):
            """
            Check key_trigger_7 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_7 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_7),
                msg="The key_trigger_7 parameter differs from the one expected")
        # end def check_key_trigger_7

        @staticmethod
        def check_key_trigger_8(test_case, event, expected):
            """
            Check key_trigger_8 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_8 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_8),
                msg="The key_trigger_8 parameter differs from the one expected")
        # end def check_key_trigger_8

        @staticmethod
        def check_key_trigger_9(test_case, event, expected):
            """
            Check key_trigger_9 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_9 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_9),
                msg="The key_trigger_9 parameter differs from the one expected")
        # end def check_key_trigger_9

        @staticmethod
        def check_key_trigger_10(test_case, event, expected):
            """
            Check key_trigger_10 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_10 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_10),
                msg="The key_trigger_10 parameter differs from the one expected")
        # end def check_key_trigger_10

        @staticmethod
        def check_key_trigger_11(test_case, event, expected):
            """
            Check key_trigger_11 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_11 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_11),
                msg="The key_trigger_11 parameter differs from the one expected")
        # end def check_key_trigger_11

        @staticmethod
        def check_key_trigger_12(test_case, event, expected):
            """
            Check key_trigger_12 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_12 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_12),
                msg="The key_trigger_12 parameter differs from the one expected")
        # end def check_key_trigger_12

        @staticmethod
        def check_key_trigger_13(test_case, event, expected):
            """
            Check key_trigger_13 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_13 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_13),
                msg="The key_trigger_13 parameter differs from the one expected")
        # end def check_key_trigger_13

        @staticmethod
        def check_key_trigger_14(test_case, event, expected):
            """
            Check key_trigger_14 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_14 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_14),
                msg="The key_trigger_14 parameter differs from the one expected")
        # end def check_key_trigger_14

        @staticmethod
        def check_key_trigger_15(test_case, event, expected):
            """
            Check key_trigger_15 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FNLayerTriggerAsListEvent to check
            :type event: ``FNLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_15 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_15),
                msg="The key_trigger_15 parameter differs from the one expected")
        # end def check_key_trigger_15
    # end class FNLayerTriggerAsListEventChecker

    class FNLayerTriggerAsBitmapEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``FNLayerTriggerAsBitmapEvent``
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
                "key_trigger_bitmap": (
                    cls.check_key_trigger_bitmap,
                    FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_trigger_bitmap(test_case, message, expected):
            """
            Check ``key_trigger_bitmap``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: FNLayerTriggerAsBitmapEvent to check
            :type message: ``FNLayerTriggerAsBitmapEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker.check_fields(
                test_case, message.key_trigger_bitmap, FullKeyCustomization.KeyTriggerBitmap, expected)
        # end def check_key_trigger_bitmap
    # end class FNLayerTriggerAsBitmapEventChecker

    class GShiftLayerTriggerAsListEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GShiftLayerTriggerAsListEvent``
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
                "key_trigger_0": (cls.check_key_trigger_0, 0),
                "key_trigger_1": (cls.check_key_trigger_1, 0),
                "key_trigger_2": (cls.check_key_trigger_2, 0),
                "key_trigger_3": (cls.check_key_trigger_3, 0),
                "key_trigger_4": (cls.check_key_trigger_4, 0),
                "key_trigger_5": (cls.check_key_trigger_5, 0),
                "key_trigger_6": (cls.check_key_trigger_6, 0),
                "key_trigger_7": (cls.check_key_trigger_7, 0),
                "key_trigger_8": (cls.check_key_trigger_8, 0),
                "key_trigger_9": (cls.check_key_trigger_9, 0),
                "key_trigger_10": (cls.check_key_trigger_10, 0),
                "key_trigger_11": (cls.check_key_trigger_11, 0),
                "key_trigger_12": (cls.check_key_trigger_12, 0),
                "key_trigger_13": (cls.check_key_trigger_13, 0),
                "key_trigger_14": (cls.check_key_trigger_14, 0),
                "key_trigger_15": (cls.check_key_trigger_15, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_trigger_0(test_case, event, expected):
            """
            Check key_trigger_0 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_0 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_0),
                msg="The key_trigger_0 parameter differs from the one expected")
        # end def check_key_trigger_0

        @staticmethod
        def check_key_trigger_1(test_case, event, expected):
            """
            Check key_trigger_1 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_1),
                msg="The key_trigger_1 parameter differs from the one expected")
        # end def check_key_trigger_1

        @staticmethod
        def check_key_trigger_2(test_case, event, expected):
            """
            Check key_trigger_2 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_2),
                msg="The key_trigger_2 parameter differs from the one expected")
        # end def check_key_trigger_2

        @staticmethod
        def check_key_trigger_3(test_case, event, expected):
            """
            Check key_trigger_3 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_3 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_3),
                msg="The key_trigger_3 parameter differs from the one expected")
        # end def check_key_trigger_3

        @staticmethod
        def check_key_trigger_4(test_case, event, expected):
            """
            Check key_trigger_4 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_4 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_4),
                msg="The key_trigger_4 parameter differs from the one expected")
        # end def check_key_trigger_4

        @staticmethod
        def check_key_trigger_5(test_case, event, expected):
            """
            Check key_trigger_5 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_5 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_5),
                msg="The key_trigger_5 parameter differs from the one expected")
        # end def check_key_trigger_5

        @staticmethod
        def check_key_trigger_6(test_case, event, expected):
            """
            Check key_trigger_6 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_6 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_6),
                msg="The key_trigger_6 parameter differs from the one expected")
        # end def check_key_trigger_6

        @staticmethod
        def check_key_trigger_7(test_case, event, expected):
            """
            Check key_trigger_7 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_7 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_7),
                msg="The key_trigger_7 parameter differs from the one expected")
        # end def check_key_trigger_7

        @staticmethod
        def check_key_trigger_8(test_case, event, expected):
            """
            Check key_trigger_8 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_8 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_8),
                msg="The key_trigger_8 parameter differs from the one expected")
        # end def check_key_trigger_8

        @staticmethod
        def check_key_trigger_9(test_case, event, expected):
            """
            Check key_trigger_9 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_9 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_9),
                msg="The key_trigger_9 parameter differs from the one expected")
        # end def check_key_trigger_9

        @staticmethod
        def check_key_trigger_10(test_case, event, expected):
            """
            Check key_trigger_10 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_10 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_10),
                msg="The key_trigger_10 parameter differs from the one expected")
        # end def check_key_trigger_10

        @staticmethod
        def check_key_trigger_11(test_case, event, expected):
            """
            Check key_trigger_11 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_11 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_11),
                msg="The key_trigger_11 parameter differs from the one expected")
        # end def check_key_trigger_11

        @staticmethod
        def check_key_trigger_12(test_case, event, expected):
            """
            Check key_trigger_12 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_12 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_12),
                msg="The key_trigger_12 parameter differs from the one expected")
        # end def check_key_trigger_12

        @staticmethod
        def check_key_trigger_13(test_case, event, expected):
            """
            Check key_trigger_13 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_13 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_13),
                msg="The key_trigger_13 parameter differs from the one expected")
        # end def check_key_trigger_13

        @staticmethod
        def check_key_trigger_14(test_case, event, expected):
            """
            Check key_trigger_14 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_14 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_14),
                msg="The key_trigger_14 parameter differs from the one expected")
        # end def check_key_trigger_14

        @staticmethod
        def check_key_trigger_15(test_case, event, expected):
            """
            Check key_trigger_15 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: GShiftLayerTriggerAsListEvent to check
            :type event: ``GShiftLayerTriggerAsListEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_trigger_15 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_trigger_15),
                msg="The key_trigger_15 parameter differs from the one expected")
        # end def check_key_trigger_15
    # end class GShiftLayerTriggerAsListEventChecker

    class GShiftLayerTriggerAsBitmapEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GShiftLayerTriggerAsBitmapEvent``
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
                "key_trigger_bitmap": (
                    cls.check_key_trigger_bitmap,
                    FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_trigger_bitmap(test_case, message, expected):
            """
            Check ``key_trigger_bitmap``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GShiftLayerTriggerAsBitmapEvent to check
            :type message: ``GShiftLayerTriggerAsBitmapEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker.check_fields(
                test_case, message.key_trigger_bitmap, FullKeyCustomization.KeyTriggerBitmap, expected)
        # end def check_key_trigger_bitmap
    # end class GShiftLayerTriggerAsBitmapEventChecker

    class FkcFailureEnabledStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``FkcFailureEnabledState``
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
                "failure": (cls.check_failure, 0),
                "enabled": (cls.check_enabled, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FkcFailureEnabledState to check
            :type bitmap: ``FullKeyCustomization.FkcFailureEnabledState``
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
        def check_failure(test_case, bitmap, expected):
            """
            Check failure field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FkcFailureEnabledState to check
            :type bitmap: ``FullKeyCustomization.FkcFailureEnabledState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert failure that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.failure),
                msg="The failure parameter differs from the one expected")
        # end def check_failure

        @staticmethod
        def check_enabled(test_case, bitmap, expected):
            """
            Check enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FkcFailureEnabledState to check
            :type bitmap: ``FullKeyCustomization.FkcFailureEnabledState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert enabled that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The enabled shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.enabled),
                msg="The enabled parameter differs from the one expected")
        # end def check_enabled
    # end class FkcFailureEnabledStateChecker

    class EnableDisableEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``EnableDisableEvent``
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
                "fkc_failure_enabled_state": (
                    cls.check_fkc_failure_enabled_state,
                    FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_fkc_failure_enabled_state(test_case, message, expected):
            """
            Check ``fkc_failure_enabled_state``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: EnableDisableEvent to check
            :type message: ``EnableDisableEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker.check_fields(
                test_case, message.fkc_failure_enabled_state, FullKeyCustomization.FkcFailureEnabledState, expected)
        # end def check_fkc_failure_enabled_state
    # end class EnableDisableEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=FullKeyCustomization.FEATURE_ID,
                           factory=FullKeyCustomizationFactory,
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

            :return: GetCapabilitiesResponse (if not error)
            :rtype: ``GetCapabilitiesResponseV0 | GetCapabilitiesResponseV1``
            """
            feature_1b05_index, feature_1b05, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b05.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_1b05_index)

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
                response_class_type=feature_1b05.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1b05_index, feature_1b05, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b05.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_1b05_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def get_set_power_on_params(cls, test_case, set_power_on_fkc_enable,
                                    power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.DISABLE,
                                    device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetSetPowerOnParams``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param set_power_on_fkc_enable: Set Power On Fkc Enable
            :type set_power_on_fkc_enable: ``int | HexList``
            :param power_on_fkc_enable: Power On Fkc Enable
            :type power_on_fkc_enable: ``int | FullKeyCustomization.PowerOnFKCStatus``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetSetPowerOnParamsResponse (if not error)
            :rtype: ``GetSetPowerOnParamsResponse``
            """
            feature_1b05_index, feature_1b05, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b05.get_set_power_on_params_cls(
                device_index=device_index,
                feature_index=feature_1b05_index,
                set_power_on_fkc_enable=set_power_on_fkc_enable,
                power_on_fkc_enable=power_on_fkc_enable)

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
                response_class_type=feature_1b05.get_set_power_on_params_response_cls)
        # end def get_set_power_on_params

        @classmethod
        def get_toggle_key_list(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetToggleKeyList``

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

            :return: GetToggleKeyListResponse (if not error)
            :rtype: ``GetToggleKeyListResponse``
            """
            feature_1b05_index, feature_1b05, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b05.get_toggle_key_list_cls(
                device_index=device_index,
                feature_index=feature_1b05_index)

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
                response_class_type=feature_1b05.get_toggle_key_list_response_cls)
        # end def get_toggle_key_list

        @classmethod
        def get_set_enabled(cls, test_case, set_toggle_keys_enabled, set_fkc_enabled, fkc_enabled=0,
                            toggle_keys_enabled=0, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetSetEnabled``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param set_toggle_keys_enabled: Set Toggle Keys Enabled
            :type set_toggle_keys_enabled: ``int | HexList``
            :param set_fkc_enabled: Set Fkc Enabled
            :type set_fkc_enabled: ``int | HexList``
            :param fkc_enabled: Fkc Enabled - OPTIONAL
            :type fkc_enabled: ``int | HexList``
            :param toggle_keys_enabled: Toggle hotkeys enabled byte - OPTIONAL
            :type toggle_keys_enabled: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetSetEnabledResponse (if not error)
            :rtype: ``GetSetEnabledResponse``
            """
            feature_1b05_index, feature_1b05, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b05.get_set_enabled_cls(
                device_index=device_index,
                feature_index=feature_1b05_index,
                set_toggle_keys_enabled=set_toggle_keys_enabled,
                set_fkc_enabled=set_fkc_enabled,
                fkc_enabled=fkc_enabled,
                toggle_key_7_enabled=(toggle_keys_enabled & 0x80) >> 7,
                toggle_key_6_enabled=(toggle_keys_enabled & 0x40) >> 6,
                toggle_key_5_enabled=(toggle_keys_enabled & 0x20) >> 5,
                toggle_key_4_enabled=(toggle_keys_enabled & 0x10) >> 4,
                toggle_key_3_enabled=(toggle_keys_enabled & 0x8) >> 3,
                toggle_key_2_enabled=(toggle_keys_enabled & 0x4) >> 2,
                toggle_key_1_enabled=(toggle_keys_enabled & 0x2) >> 1,
                toggle_key_0_enabled=(toggle_keys_enabled & 0x1) >> 0)

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
                response_class_type=feature_1b05.get_set_enabled_response_cls)
        # end def get_set_enabled

        @classmethod
        def get_set_enabled_and_check_error(cls, test_case, error_codes, set_toggle_keys_enabled, set_fkc_enabled,
                                            fkc_enabled=0, toggle_keys_enabled=0, device_index=None, port_index=None):
            """
            Process ``GetSetEnabled``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param set_toggle_keys_enabled: Set Toggle Keys Enabled
            :type set_toggle_keys_enabled: ``int | HexList``
            :param set_fkc_enabled: Set Fkc Enabled
            :type set_fkc_enabled: ``int | HexList``
            :param fkc_enabled: Fkc Enabled - OPTIONAL
            :type fkc_enabled: ``int | HexList``
            :param toggle_keys_enabled: Toggle hotkeys enabled byte - OPTIONAL
            :type toggle_keys_enabled: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """

            feature_1b05_index, feature_1b05, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b05.get_set_enabled_cls(
                device_index=device_index,
                feature_index=feature_1b05_index,
                set_toggle_keys_enabled=set_toggle_keys_enabled,
                set_fkc_enabled=set_fkc_enabled,
                fkc_enabled=fkc_enabled,
                toggle_key_7_enabled=(toggle_keys_enabled & 0x80) >> 7,
                toggle_key_6_enabled=(toggle_keys_enabled & 0x40) >> 6,
                toggle_key_5_enabled=(toggle_keys_enabled & 0x20) >> 5,
                toggle_key_4_enabled=(toggle_keys_enabled & 0x10) >> 4,
                toggle_key_3_enabled=(toggle_keys_enabled & 0x8) >> 3,
                toggle_key_2_enabled=(toggle_keys_enabled & 0x4) >> 2,
                toggle_key_1_enabled=(toggle_keys_enabled & 0x2) >> 1,
                toggle_key_0_enabled=(toggle_keys_enabled & 0x1) >> 0)

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_set_enabled_and_check_error

        @classmethod
        def get_set_sw_configuration_cookie(cls, test_case, set_sw_configuration_cookie, sw_configuration_cookie=0,
                                            device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetSetSWConfigurationCookie``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param set_sw_configuration_cookie: Set SW Configuration Cookie
            :type set_sw_configuration_cookie: ``int | HexList``
            :param sw_configuration_cookie: SW Configuration Cookie - OPTIONAL
            :type sw_configuration_cookie: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetSetSWConfigurationCookieResponse (if not error)
            :rtype: ``GetSetSWConfigurationCookieResponseV1``
            """
            feature_1b05_index, feature_1b05, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b05.get_set_sw_configuration_cookie_cls(
                device_index=device_index,
                feature_index=feature_1b05_index,
                set_sw_configuration_cookie=set_sw_configuration_cookie,
                sw_configuration_cookie=HexList(sw_configuration_cookie))

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
                response_class_type=feature_1b05.get_set_sw_configuration_cookie_response_cls)
        # end def get_set_sw_configuration_cookie

        @classmethod
        def base_layer_trigger_as_list_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``BaseLayerTriggerAsListEvent``: get notification from event queue

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

            :return: BaseLayerTriggerAsListEvent
            :rtype: ``BaseLayerTriggerAsListEvent``
            """
            _, feature_1b05, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b05.base_layer_trigger_as_list_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def base_layer_trigger_as_list_event

        @classmethod
        def base_layer_trigger_as_bitmap_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``BaseLayerTriggerAsBitmapEvent``: get notification from event queue

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

            :return: BaseLayerTriggerAsBitmapEvent
            :rtype: ``BaseLayerTriggerAsBitmapEvent``
            """
            _, feature_1b05, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b05.base_layer_trigger_as_bitmap_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def base_layer_trigger_as_bitmap_event

        @classmethod
        def fn_layer_trigger_as_list_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``FNLayerTriggerAsListEvent``: get notification from event queue

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

            :return: FNLayerTriggerAsListEvent
            :rtype: ``FNLayerTriggerAsListEvent``
            """
            _, feature_1b05, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b05.fn_layer_trigger_as_list_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def fn_layer_trigger_as_list_event

        @classmethod
        def fn_layer_trigger_as_bitmap_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``FNLayerTriggerAsBitmapEvent``: get notification from event queue

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

            :return: FNLayerTriggerAsBitmapEvent
            :rtype: ``FNLayerTriggerAsBitmapEvent``
            """
            _, feature_1b05, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b05.fn_layer_trigger_as_bitmap_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def fn_layer_trigger_as_bitmap_event

        @classmethod
        def gshift_layer_trigger_as_list_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``GShiftLayerTriggerAsListEvent``: get notification from event queue

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

            :return: GShiftLayerTriggerAsListEvent
            :rtype: ``GShiftLayerTriggerAsListEvent``
            """
            _, feature_1b05, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b05.gshift_layer_trigger_as_list_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def gshift_layer_trigger_as_list_event

        @classmethod
        def gshift_layer_trigger_as_bitmap_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``GShiftLayerTriggerAsBitmapEvent``: get notification from event queue

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

            :return: GShiftLayerTriggerAsBitmapEvent
            :rtype: ``GShiftLayerTriggerAsBitmapEvent``
            """
            _, feature_1b05, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b05.gshift_layer_trigger_as_bitmap_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def gshift_layer_trigger_as_bitmap_event

        @classmethod
        def enable_disable_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=False, allow_no_message=False, skip_error_message=False):
            """
            Process ``EnableDisableEvent``: get notification from event queue

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

            :return: EnableDisableEvent
            :rtype: ``EnableDisableEvent``
            """
            _, feature_1b05, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b05.enable_disable_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def enable_disable_event
    # end class HIDppHelper

    class FkcTableHelper:
        """
        FKC main, modifier and Fn Table Helper
        """

        class KeyProvider:
            """
            Provide remappable/non-remappable keys for trigger and action key

                   Remapping          |   Trigger (Key Pool)   |   Action (Key Pool)
            --------------------------|------------------------|----------------------
            Trigger -> Key            |  All remappable keys   |  Standard keys
            --------------------------|------------------------|----------------------
            Trigger -> nM + Key       |  All remappable keys   |  Non-modifier keys
            --------------------------|------------------------|----------------------
            nM + Trigger -> Key       |  Non-modifier keys     |  Standard keys
            --------------------------|------------------------|----------------------
            nM + Trigger -> nM + Key  |  Non-modifier keys     |  Non-modifier keys

            Note: For Fn + Trigger remapping, the all remappable keys might be less than the other layers (FKC toggle,
                  game mode and immersive lighting keys might be defined in OOB Fn layer). Therefore the key pool shall
                  be from
                  1. get_all_remappable_fn_keys
                  2. get_all_standard_fn_keys
                  3. get_all_non_modifier_fn_keys
            """

            @classmethod
            def get_all_remappable_keys(cls, test_case):
                """
                Get all remappable keys from the key matrix

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All remappable keys
                :rtype: ``list[KEY_ID]``
                """
                key_id_list = list(test_case.button_stimuli_emulator.get_key_id_list())
                return [key for key in key_id_list if key not in NOT_REMAPPABLE_KEY_LIST]
            # end def get_all_remappable_keys

            @classmethod
            def get_all_standard_keys(cls, test_case):
                """
                Get all standard keys that in the all remappable keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All supported standard keys
                :rtype: ``list[KEY_ID]``
                """
                all_remappable_keys = cls.get_all_remappable_keys(test_case=test_case)
                return [key for key in all_remappable_keys if key in list(STANDARD_KEYS.keys())]
            # end def get_all_standard_keys

            @classmethod
            def get_all_non_modifier_keys(cls, test_case):
                """
                Get all supported non-modifier keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All supported non-modifier keys
                :rtype: ``list[KEY_ID]``
                """
                all_standard_keys = cls.get_all_standard_keys(test_case=test_case)
                return [key for key in all_standard_keys if key not in MODIFIER_KEY_LIST]
            # end def get_all_non_modifier_keys

            @classmethod
            def get_all_modifier_keys(cls, test_case):
                """
                Get all supported modifier keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All supported modifier keys
                :rtype: ``list[KEY_ID]``
                """
                all_standard_keys = cls.get_all_standard_keys(test_case=test_case)
                return [key for key in all_standard_keys if key in MODIFIER_KEY_LIST]
            # end def get_all_modifier_keys

            @classmethod
            def get_non_remappable_oob_fn_keys(cls, test_case):
                """
                Get the non-remappable OOB Fn Keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Non-remappable OOB Fn keys
                :rtype: ``list[KEY_ID]``
                """
                fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=test_case, excluded_keys=[])
                return [fn_keys[key] for key in list(fn_keys.keys()) if key in NOT_REMAPPABLE_KEY_LIST]
            # end def get_non_remappable_oob_fn_keys

            @classmethod
            def get_remappable_oob_fn_keys(cls, test_case):
                """
                Get the remappable OOB Fn Keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Remappable OOB Fn keys
                :rtype: ``list[KEY_ID]``
                """
                fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=test_case, excluded_keys=NOT_REMAPPABLE_KEY_LIST)
                return list(fn_keys.values())
            # end def get_remappable_oob_fn_keys

            @classmethod
            def get_all_remappable_fn_keys(cls, test_case):
                """
                Get all remappable Fn Keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All remappable Fn keys
                :rtype: ``list[KEY_ID]``
                """
                all_remappable_keys = cls.get_all_remappable_keys(test_case=test_case)
                non_remappable_oob_fn_keys = cls.get_non_remappable_oob_fn_keys(test_case=test_case)
                return [key for key in all_remappable_keys if key not in non_remappable_oob_fn_keys]
            # end def get_all_remappable_fn_keys

            @classmethod
            def get_all_non_modifier_fn_keys(cls, test_case):
                """
                Get all supported non-modifier fn keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All supported non-modifier fn keys
                :rtype: ``list[KEY_ID]``
                """
                all_remappable_fn_keys = cls.get_all_remappable_fn_keys(test_case=test_case)
                return [key for key in all_remappable_fn_keys if key not in MODIFIER_KEY_LIST]
            # end def get_all_non_modifier_fn_keys

            @classmethod
            def get_all_modifier_fn_keys(cls, test_case):
                """
                Get all supported modifier fn keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All supported modifier fn keys
                :rtype: ``list[KEY_ID]``
                """
                all_remappable_fn_keys = cls.get_all_remappable_fn_keys(test_case=test_case)
                return [key for key in all_remappable_fn_keys if key in MODIFIER_KEY_LIST]
            # end def get_all_modifier_fn_keys

            @classmethod
            def get_all_standard_fn_keys(cls, test_case):
                """
                Get all supported standard fn keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: All supported standard fn keys
                :rtype: ``list[KEY_ID]``
                """
                all_remappable_fn_keys = cls.get_all_remappable_fn_keys(test_case=test_case)
                return [key for key in all_remappable_fn_keys if key in list(STANDARD_KEYS.keys())]
            # end def get_all_standard_fn_keys

            @classmethod
            def trigger_key_get_key_list(cls, test_case, key_type, fn_trigger_remapping=False):
                """
                Get the supported keys by key type for Trigger key

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param key_type: The key type if trigger or action key
                :type key_type: ``RemappedKey.RandomKey``
                :param fn_trigger_remapping: The flag indicating the remapping is Fn + Trigger that might has less
                                             remappable keys (shall consider keys in FN_KEYS that defined in key
                                             matrix layout). - OPTIONAL
                :type fn_trigger_remapping: ``bool``

                :return: The supported keys by key type
                :rtype: ``list[KEY_ID]``

                :raise ``ValueError``: If input unsupported keyboard key type or FKC layer
                """
                if not fn_trigger_remapping:
                    if key_type == RemappedKey.RandomKey.NON_MODIFIER_KEY:
                        return cls.get_all_non_modifier_keys(test_case=test_case)
                    elif key_type == RemappedKey.RandomKey.ALL_REMAPPABLE_KEY:
                        return cls.get_all_remappable_keys(test_case=test_case)
                    else:
                        raise ValueError(f'Wrong key type: {key_type!s}. Only allowed keyboard key type')
                    # end if
                else:
                    if key_type == RemappedKey.RandomKey.NON_MODIFIER_KEY:
                        return cls.get_all_non_modifier_fn_keys(test_case=test_case)
                    elif key_type == RemappedKey.RandomKey.MODIFIER_KEY:
                        return cls.get_all_modifier_fn_keys(test_case=test_case)
                    elif key_type == RemappedKey.RandomKey.ALL_REMAPPABLE_KEY:
                        return cls.get_all_remappable_fn_keys(test_case=test_case)
                    else:
                        raise ValueError(f'Unsupported key type: {key_type!s} in Fn layer')
                    # end if
                # end if
            # end def trigger_key_get_key_list

            @classmethod
            def is_fn_trigger_remapping(cls, layer, trigger_modifier_count):
                """
                Check if the remapping is Fn + Trigger

                :param layer: The layer of FKC main table
                :type layer: ``FkcMainTable.Layer``
                :param trigger_modifier_count: The number if trigger modifiers
                :type trigger_modifier_count: ``int``

                :return: Indicating the remapping is Fn + Trigger or not
                :rtype: ``bool``
                """
                return True if layer == FkcMainTable.Layer.FN and trigger_modifier_count == 0 else False
            # end def is_fn_trigger_remapping
        # end class KeyProvider

        class RandomParameters:
            """
            Parameters for FKC remapped keys generation
            """

            class Button:
                """
                Parameters for key remapping generation
                """
                def __init__(self, full_keys=False, count=0, action_types=(RemappedKey.ActionType.KEYBOARD,),
                             trigger_modifiers=(0,), action_modifiers=(0,),
                             trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                             action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY):
                    """
                    :param full_keys: Indicate to remap full keys on the keyboard - OPTIONAL
                    :type full_keys: ``bool``
                    :param count: The number of remapping to be generated - OPTIONAL
                    :type count: ``int``
                    :param action_types: Allowed action types - OPTIONAL
                    :type action_types: ``tuple[RemappedKey.ActionType]``
                    :param trigger_modifiers: Trigger modifier count in the list - OPTIONAL
                    :type trigger_modifiers: ``tuple[int]``
                    :param action_modifiers: Action modifier count in the list - OPTIONAL
                    :type action_modifiers: ``tuple[int]``
                    :param trigger_key_type: The trigger key type
                    :type trigger_key_type: ``RemappedKey.RandomKey``
                    :param action_key_type: The action key type. It'll affect the remapping result if action_types
                                            includes RemappedKey.ActionType.KEYBOARD
                    :type action_key_type: ``RemappedKey.RandomKey``
                    """
                    self.full_keys = full_keys
                    self.count = count
                    self.action_types = action_types
                    self.trigger_modifiers = trigger_modifiers
                    self.action_modifiers = action_modifiers
                    self.trigger_key_type = trigger_key_type
                    self.action_key_type = action_key_type
                # end def __init__

                def __str__(self):
                    return f'Full keys remapping: {self.full_keys}, Count={self.count}, Action types: ' \
                           f'{self.action_types}, Trigger modifier count={self.trigger_modifiers}, ' \
                           f'Action modifier count={self.action_modifiers}, Trigger_key_type: ' \
                           f'{self.trigger_key_type}, Action_key_type: {self.action_key_type}'
                # end def __str__

                def __repr__(self):
                    return self.__str__()
                # end def __repr__
            # end class Button

            class Macro:
                """
                Parameters for Macro generation
                """
                def __init__(self, entry_count=0, command_count=0, command_types=(StandardKeyCommand,)):
                    """
                    :param entry_count: The number of Macro entry to be generated - OPTIONAL
                    :type entry_count: ``int``
                    :param command_count: The number of macro commands will be generated in Macro - OPTIONAL
                    :type command_count: ``int``
                    :param command_types: Selected macro command types - OPTIONAL
                    :type command_types: ``tuple[object]``
                    """
                    self.entry_count = entry_count
                    self.command_count = command_count
                    self.command_types = command_types
                # end def __init__

                def __str__(self):
                    return f'Macro entry count={self.entry_count}, ' \
                           f'Macro command_count count={self.command_count}, ' \
                           f'Macro command types: {self.command_types}\n'
                # end def __str__

                def __repr__(self):
                    return self.__str__()
                # end def __repr__
            # end class Macro

            def __init__(self, layer=FkcMainTable.Layer.BASE, button=None, macro=None, profile_count=1,
                         remove_used_keys=True):
                """
                :param layer: The FKC main table layer for the random generation - OPTIONAL
                :type layer: ``FkcMainTable.Layer``
                :param button: Button parameters - OPTIONAL
                :type button: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters.RandomParameters.Button``
                :param macro: Macro parameters - OPTIONAL
                :type macro: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters.RandomParameters.Macro``
                :param profile_count: Create the number of profiles - OPTIONAL
                :type profile_count: ``int``
                :param remove_used_keys: For all remappable keys,
                                         remove keys that been used in the preset remapped keys - OPTIONAL
                :type remove_used_keys: ``bool``
                """
                self.layer = layer
                self.button = button if button else self.Button()
                self.macro = macro if macro else self.Macro()
                self.profile_count = profile_count
                self.remove_used_keys = remove_used_keys
            # end def __init__

            def get_action_type(self):
                """
                Get the action type by random selection

                :return: The action type
                :rtype: ``RemappedKey.ActionType``
                """
                return choice(self.button.action_types)
            # end def get_action_type

            def get_trigger_modifier_count(self):
                """
                Get the trigger modifier count by random selection

                :return: The trigger modifier count
                :rtype: ``int``
                """
                return choice(self.button.trigger_modifiers)
            # end def get_trigger_modifier_count

            def get_action_modifier_count(self):
                """
                Get the action modifier count by random selection

                :return: The action modifier count
                :rtype: ``int``
                """
                return choice(self.button.action_modifiers)
            # end def get_action_modifier_count

            def get_macro_command(self):
                """
                Get the supported macro command by random selection

                :return: The supported macro command
                :rtype: ``StandardKeyCommand | MouseButtonCommand | ConsumerKeyCommand``
                """
                return choice(self.macro.command_types)
            # end def get_macro_command

            def __str__(self):
                return f'Random Parameters: {self.layer}, {self.button}, {self.macro}, ' \
                       f'profile count: {self.profile_count}, remove used keys: {self.remove_used_keys}\n'
            # end def __str__

            def __repr__(self):
                return self.__str__()
            # end def __repr__
        # end class RandomParameters

        class RandomGenerationHelper:
            """
            Random generation of FKC remapping helper
            """

            @classmethod
            def get_random_non_modifier_key(cls, test_case):
                """
                Get a non-modifier key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Non-Modifier key
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_non_modifier_keys(
                    test_case=test_case))
            # end def get_random_non_modifier_key

            @classmethod
            def get_random_modifier_key(cls, test_case):
                """
                Get a modifier key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Modifier key
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_modifier_keys(
                    test_case=test_case))
            # end def get_random_modifier_key

            @classmethod
            def get_random_standard_key(cls, test_case):
                """
                Get a standard key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Standard key
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_standard_keys(
                    test_case=test_case))
            # end def get_random_standard_key

            @classmethod
            def get_random_remappable_key(cls, test_case):
                """
                Get a remappable key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Remappable key id
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_remappable_keys(
                    test_case=test_case))
            # end def get_random_remappable_key

            @classmethod
            def get_random_key(cls, test_case, key_type):
                """
                Get a modifier or non-modifier or standard key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param key_type: The key type if trigger or action key
                :type key_type: ``RemappedKey.RandomKey``

                :return: A supported key by the key type
                :rtype: ``KEY_ID``

                :raise ``ValueError``: If input unsupported key type
                """
                if key_type == RemappedKey.RandomKey.NON_MODIFIER_KEY:
                    # Available for trigger and action key
                    return cls.get_random_non_modifier_key(test_case=test_case)
                elif key_type == RemappedKey.RandomKey.MODIFIER_KEY:
                    # Available for trigger and action key
                    return cls.get_random_modifier_key(test_case=test_case)
                elif key_type == RemappedKey.RandomKey.STANDARD_KEY:
                    # Available for action key
                    return cls.get_random_standard_key(test_case=test_case)
                elif key_type == RemappedKey.RandomKey.ALL_REMAPPABLE_KEY:
                    # Available for trigger key
                    return cls.get_random_remappable_key(test_case=test_case)
                else:
                    raise ValueError(
                        f'Unsupported key type: {key_type!s}! Check the settings for random key generation')
                # end if
            # end def get_random_key

            @classmethod
            def get_random_remappable_fn_key(cls, test_case):
                """
                Get a remappable Fn Key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Remappable Fn key
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_remappable_fn_keys(
                    test_case=test_case))
            # end def get_random_remappable_fn_key

            @classmethod
            def get_random_standard_fn_key(cls, test_case):
                """
                Get a remappable standard Fn Key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Remappable standard Fn key
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_standard_fn_keys(
                    test_case=test_case))
            # end def get_random_standard_fn_key

            @classmethod
            def get_random_non_modifier_fn_key(cls, test_case):
                """
                Get a remappable non-modifier Fn Key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Remappable non-modifier Fn key
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_non_modifier_fn_keys(
                    test_case=test_case))
            # end def get_random_non_modifier_fn_key

            @classmethod
            def get_random_modifier_fn_key(cls, test_case):
                """
                Get a remappable modifier Fn Key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

                :return: Remappable modifier Fn key
                :rtype: ``KEY_ID``
                """
                return choice(FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_modifier_fn_keys(
                    test_case=test_case))
            # end def get_random_modifier_fn_key

            @classmethod
            def get_random_fn_key(cls, test_case, key_type):
                """
                Get a modifier or non-modifier or standard fn key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param key_type: The key type if trigger or action key
                :type key_type: ``RemappedKey.RandomKey``

                :return: A supported fn key by the key type
                :rtype: ``KEY_ID``

                :raise ``ValueError``: If input unsupported key type
                """
                if key_type == RemappedKey.RandomKey.NON_MODIFIER_KEY:
                    return cls.get_random_non_modifier_fn_key(test_case=test_case)
                elif key_type == RemappedKey.RandomKey.MODIFIER_KEY:
                    return cls.get_random_modifier_fn_key(test_case=test_case)
                elif key_type == RemappedKey.RandomKey.STANDARD_KEY:
                    return cls.get_random_standard_fn_key(test_case=test_case)
                elif key_type == RemappedKey.RandomKey.ALL_REMAPPABLE_KEY:
                    return cls.get_random_remappable_fn_key(test_case=test_case)
                else:
                    raise ValueError(
                        f'Unsupported key type: {key_type!s}! Check the settings for random key generation')
                # end if
            # end def get_random_fn_key

            @classmethod
            def get_random_unused_key(cls, test_case, key_type, fn_trigger_remapping=False, excluded_keys=()):
                """
                Get a modifier or non-modifier or standard key randomly

                Note: While manually assign random keys to preset_remapped_keys, add excluded keys could avoid the
                      duplicated key returned by the random key generation!

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param key_type: The key type of trigger or action key
                :type key_type: ``RemappedKey.RandomKey``
                :param fn_trigger_remapping: The flag indicating the remapping is Fn + Trigger that might has less
                                             remappable keys (shall consider keys in FN_KEYS that defined in key
                                             matrix layout).  - OPTIONAL
                :type fn_trigger_remapping: ``bool``
                :param excluded_keys: The excluded key id list - OPTIONAL
                :type excluded_keys: ``list[KEY_ID]``

                :return: A supported key by the key type
                :rtype: ``KEY_ID``

                :raise ``AssertionError``: If input an unknown FKC layer
                :raise ``Exception``: Cannot find a random key is not in the excluded_keys in 10 times!
                """
                random_key_func = cls.get_random_fn_key if fn_trigger_remapping else cls.get_random_key

                try_count = 10
                while try_count > 0:
                    # noinspection PyArgumentList
                    random_key = random_key_func(test_case=test_case, key_type=key_type)
                    if random_key not in excluded_keys:
                        return random_key
                    else:
                        try_count -= 1
                    # end if
                # end while
                raise Exception('Cannot find a random key is not in the excluded_keys in 10 times!')
            # end def get_random_unused_key

            @classmethod
            def get_random_trigger_key(cls, test_case, key_type, fn_trigger_remapping=False, excluded_keys=()):
                """
                Get a remappable trigger randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param key_type: The key type of trigger key
                :type key_type: ``RemappedKey.RandomKey``
                :param fn_trigger_remapping: The flag indicating the remapping is Fn + Trigger that might has less
                                             remappable keys (shall consider keys in FN_KEYS that defined in key
                                             matrix layout).  - OPTIONAL
                :type fn_trigger_remapping: ``bool``
                :param excluded_keys: The excluded key id list - OPTIONAL
                :type excluded_keys: ``list[KEY_ID]``

                :return: A supported key by the key type
                :rtype: ``KEY_ID``
                """
                return cls.get_random_unused_key(test_case=test_case, key_type=key_type,
                                                 fn_trigger_remapping=fn_trigger_remapping, excluded_keys=excluded_keys)
            # end def get_random_trigger_key

            @classmethod
            def get_random_action_key(cls, test_case, key_type, excluded_keys=()):
                """
                Get a remappable action key randomly

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param key_type: The key type of action key
                :type key_type: ``RemappedKey.RandomKey``
                :param excluded_keys: The excluded key id list - OPTIONAL
                :type excluded_keys: ``list[KEY_ID]``

                :return: A supported key by the key type
                :rtype: ``KEY_ID``
                """
                return cls.get_random_unused_key(test_case=test_case, key_type=key_type, excluded_keys=excluded_keys)
            # end def get_random_action_key

            @classmethod
            def get_random_mouse_button_mask(cls):
                """
                Get a mouse button mask randomly

                :return: Mouse button mask
                :rtype: ``FkcProfileButton.ButtonMask``
                """
                return choice([button_mask for button_mask in FkcProfileButton.ButtonMask])
            # end def get_random_mouse_button_mask

            @classmethod
            def get_random_consumer_key(cls, os_variant):
                """
                Get a consumer key id randomly

                :param os_variant: OS variant
                :type os_variant: ``OS | str``

                :return: Consumer key id
                :rtype: ``KEY_ID``
                """
                consumer_keys = {}
                for key_id, consumer_usage_in_os in HidData.CONSUMER_KEYS.items():
                    consumer_usage = consumer_usage_in_os.get(os_variant)
                    if consumer_usage:
                        consumer_keys[key_id] = consumer_usage
                    else:
                        # If there is no information about the specified OS, then try to get it from OS.ALL
                        consumer_usage = consumer_usage_in_os.get(OS.ALL)
                        if consumer_usage:
                            consumer_keys[key_id] = consumer_usage
                        # end if
                    # end if
                # end for

                return choice(list(consumer_keys.keys()))
            # end def get_random_consumer_key

            @classmethod
            def get_random_xy_movement(cls):
                """
                Get a mouse XY movement randomly

                :return: XY movement
                :rtype: ``tuple[int, int]``
                """
                return randrange(start=-16384, stop=16384), randrange(start=-16384, stop=16384)
            # end def get_random_xy_movement

            @classmethod
            def get_random_wheel_movement(cls):
                """
                Get a mouse vertical/horizontal wheel movement randomly

                :return: vertical/horizontal wheel
                :rtype: ``int``
                """
                return randrange(start=-128, stop=128)
            # end def get_random_wheel_movement

            @classmethod
            def get_random_function_key(cls):
                """
                Get a function key randomly
                Note: Supports Tilt left and right function only

                :return: Function key
                :rtype: ``KEY_ID``
                """
                return choice([KEY_ID.TILT_LEFT, KEY_ID.TILT_RIGHT])
            # end def get_random_function_key

            @classmethod
            def get_random_action_type(cls):
                """
                Get a action type randomly

                :return: Action type
                :rtype: ``RemappedKey.ActionType | int``
                """
                return choice([RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                               RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO])
            # end def get_random_action_type

            @classmethod
            def _generate_modifier_bitfield(cls, test_case, modifier_bitfields, count):
                """
                Generate trigger bitfield by random select modifiers from the modifier_list

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param modifier_bitfields: The list of modifiers are defined in ``FullKeyCustomization.TriggerBitField``
                                           or ``FullKeyCustomization.ActionBitField``
                :type modifier_bitfields: ``list[int]``
                :param count: The number of modifiers to be triggered
                :type count: ``int``

                :return: The selected trigger modifier bitfields
                :rtype: ``int``
                """
                supported_modifier_keys = \
                    FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_modifier_keys(test_case=test_case)
                supported_modifiers_in_bitfield = [x for x in modifier_bitfields
                                                   if MODIFIER_BITFIELD_TO_KEY_ID[x] in supported_modifier_keys]

                modifier_bitfield = 0
                random_count = count if count <= len(supported_modifiers_in_bitfield) else \
                    len(supported_modifiers_in_bitfield)
                random_modifiers = sample(supported_modifiers_in_bitfield, random_count)
                for random_modifier in random_modifiers:
                    modifier_bitfield |= random_modifier
                # end for

                return modifier_bitfield
            # end def _generate_modifier_bitfield

            @classmethod
            def generate_trigger_bitfield(cls, test_case, count):
                """
                Generate trigger bitfield by random select modifiers in ``FullKeyCustomization.TriggerBitField``

                Note: Exclude SingleKeyMatch in the selection

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param count: The number of modifiers to be triggered
                :type count: ``int``

                return: The selected trigger modifier bitfields
                :rtype: ``int``
                """
                modifier_bitfields = [x for x in FullKeyCustomization.TriggerBitField if x !=
                                      FullKeyCustomization.TriggerBitField.SINGLE_KEY_MATCH]
                # noinspection PyTypeChecker
                return cls._generate_modifier_bitfield(test_case=test_case, modifier_bitfields=modifier_bitfields,
                                                       count=count)
            # end def generate_trigger_bitfield

            @classmethod
            def generate_action_bitfield(cls, test_case, count):
                """
                Generate trigger bitfield by random select modifiers in ``FullKeyCustomization.ActionBitField``

                Note: Exclude NotifySW and UpdateModifiers in the selection

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param count: The number of modifiers in the remapped action
                :type count: ``int``

                return: The selected action modifier bitfields
                :rtype: ``int``
                """
                modifier_bitfields = [x for x in FullKeyCustomization.ActionBitField if x not in
                                      [FullKeyCustomization.ActionBitField.NOTIFY_SW,
                                       FullKeyCustomization.ActionBitField.UPDATE_MODIFIERS]]
                # noinspection PyTypeChecker
                return cls._generate_modifier_bitfield(test_case=test_case, modifier_bitfields=modifier_bitfields,
                                                       count=count)
            # end def generate_action_bitfield

            @classmethod
            def generate_key_remapping(cls, test_case, os_variant, random_parameters, trigger_key=None, macro=None,
                                       notify_sw=False):
                """
                Generate a single line group for the FKC main table with a random selection of the trigger and action
                keys

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param os_variant: OS variant
                :type os_variant: ``OS | str``
                :param random_parameters: Parameters for the random remapped key generation
                :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters``
                :param trigger_key: The key id of trigger - OPTIONAL
                :type trigger_key: ``KEY_ID | None``
                :param macro: Macro object - OPTIONAL
                :type macro: ``Macro``
                :param notify_sw: Combine NotifySW in the action_bitfield - OPTIONAL
                :type notify_sw: ``bool``

                :return: The ``FkcMainTable.Group`` instance or None if the trigger_cid is a non-remappable key
                :rtype: ``FkcMainTable.Group | None``

                :raise ``AssertionError``: If cannot convert trigger_key to trigger_cidx
                """
                trigger_modifier_count = random_parameters.get_trigger_modifier_count()
                trigger_bitfield = cls.generate_trigger_bitfield(test_case=test_case, count=trigger_modifier_count)
                action_bitfield = cls.generate_action_bitfield(test_case=test_case,
                                                               count=random_parameters.get_action_modifier_count())
                if notify_sw:
                    action_bitfield |= FullKeyCustomization.ActionBitField.NOTIFY_SW
                # end if

                if not trigger_bitfield:
                    trigger_bitfield |= FullKeyCustomization.TriggerBitField.SINGLE_KEY_MATCH
                # end if

                action_type = random_parameters.get_action_type()
                if action_type == RemappedKey.ActionType.KEYBOARD:
                    action_key = cls.get_random_action_key(test_case=test_case,
                                                           key_type=random_parameters.button.action_key_type)
                    if action_key in MODIFIER_KEY_LIST:
                        action_bitfield |= FullKeyCustomization.ActionBitField.UPDATE_MODIFIERS | \
                                           KEY_ID_TO_MODIFIER_BITFIELD[action_key]
                        button_setting = FkcProfileButton.create_empty_button()
                    else:
                        button_setting = FkcProfileButton.create_standard_key(key_id=action_key)
                    # end if
                elif action_type == RemappedKey.ActionType.MOUSE:
                    button_setting = FkcProfileButton.create_mouse_button(
                        button_mask=cls.get_random_mouse_button_mask())
                elif action_type == RemappedKey.ActionType.CONSUMER:
                    button_setting = FkcProfileButton.create_consumer_button(
                        key_id=cls.get_random_consumer_key(os_variant=os_variant), os_variant=os_variant)
                elif action_type == RemappedKey.ActionType.MACRO:
                    random_entry = choice(macro.entries)
                    button_setting = FkcProfileButton.create_execute_macro(sector_id=macro.first_sector_id_lsb,
                                                                           address=random_entry.start_address)
                elif action_type == RemappedKey.ActionType.FUNCTION:
                    function_type = FkcProfileButton.convert_key_id_to_function_type(
                        key_id=cls.get_random_function_key())
                    button_setting = FkcProfileButton.create_function_button(function_type=function_type)
                elif action_type == RemappedKey.ActionType.VIRTUAL_MODIFIER:
                    button_setting = choice([FkcProfileButton.create_fn_key(), FkcProfileButton.create_gshift_key()])
                else:
                    raise ValueError(f'Unknown action type: {action_type}')
                # end if
                row = FkcMainTable.Group.Row(trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                                             button_setting=button_setting)
                if not trigger_key:
                    fn_trigger_remapping = \
                        FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.is_fn_trigger_remapping(
                            layer=random_parameters.layer,
                            trigger_modifier_count=trigger_modifier_count)
                    trigger_key = cls.get_random_trigger_key(test_case=test_case,
                                                             key_type=random_parameters.button.trigger_key_type,
                                                             fn_trigger_remapping=fn_trigger_remapping)
                # end if
                trigger_cidx = ControlListTestUtils.key_id_to_cidx(test_case=test_case, key_id=trigger_key)
                assert trigger_cidx is not None, f'Cannot get trigger_cidx by trigger_key: {trigger_key!s}'

                return FkcMainTable.Group(trigger_cidx=trigger_cidx, rows=[row])
            # end def generate_key_remapping

            @classmethod
            def generate_macro(cls, test_case, os_variant, directory, random_parameters, raise_buffer_overflow=True):
                """
                Generate Macro. For each macro entry contains several standard keys by random selection

                :param test_case: Current test case
                :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
                :param os_variant: OS variant
                :type os_variant: ``OS | str``
                :param directory: ``DirectoryFile`` instance
                :type directory: ``DirectoryFile``
                :param random_parameters: Parameters for the random remapped key generation
                :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters``
                :param raise_buffer_overflow: Flag indicating to raise FKC table overflow RAM buffer error - OPTIONAL
                :type raise_buffer_overflow: ``bool``

                :return: ``Macro`` instance
                :rtype: ``Macro``

                :raise ``ValueError``: If macro size > ram_buffer_size or unsupported macro command
                """
                start_address = 0
                entries = []
                for _ in range(random_parameters.macro.entry_count):
                    commands = []
                    count = random_parameters.macro.command_count
                    while count > 0:
                        command_cls = random_parameters.get_macro_command()
                        if command_cls == StandardKeyCommand:
                            key_down, key_up = ProfileMacro.create_std_key_stroke(
                                key_id=cls.get_random_standard_key(test_case=test_case))
                            commands.append(key_down)
                            commands.append(key_up)
                        elif command_cls == MouseButtonCommand:
                            button_down, button_up = ProfileMacro.create_button_stroke(
                                button_mask=cls.get_random_mouse_button_mask())
                            commands.append(button_down)
                            commands.append(button_up)
                        elif command_cls == ConsumerKeyCommand:
                            consumer_down, consumer_up = ProfileMacro.create_cons_key_stroke(
                                key_id=cls.get_random_consumer_key(os_variant=os_variant), os_variant=os_variant)
                            commands.append(consumer_down)
                            commands.append(consumer_up)
                        elif command_cls == XYCommand:
                            x, y = cls.get_random_xy_movement()
                            commands.append(ProfileMacro.create_xy_movement(x_pos=x, y_pos=y))
                        elif command_cls == RollerCommand:
                            commands.append(ProfileMacro.create_roller(v_wheel=cls.get_random_wheel_movement()))
                        elif command_cls == AcPanCommand:
                            commands.append(ProfileMacro.create_ac_pan(h_wheel=cls.get_random_wheel_movement()))
                        else:
                            raise ValueError(f'Unsupported macro command: {command_cls}')
                        # end if
                        count -= 1
                    # end while

                    # noinspection PyTypeChecker
                    commands.append(ProfileMacro.create_macro_end())
                    entry = Macro.Entry(commands=commands, start_address=start_address)
                    entries.append(entry)

                    # Update start address
                    for command in commands:
                        start_address += len(command)
                    # end for
                # end for
                macro = Macro(entries=entries)
                if raise_buffer_overflow:
                    FullKeyCustomizationTestUtils.FkcTableHelper.check_size(test_case=test_case,
                                                                            table_size=macro.n_bytes)
                # end if
                macro.register(directory=directory)
                return macro
            # end def generate_macro
        # end class RandomGenerationHelper

        @classmethod
        def create_key_remapping(cls, test_case, preset_remapped_key, os_variant, macro=None, notify_sw=False):
            """
            Create a key remapping

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param preset_remapped_key: Remapped key object
            :type preset_remapped_key: ``RemappedKey``
            :param os_variant: OS variant
            :type os_variant: ``OS | str``
            :param macro: Macro object - OPTIONAL
            :type macro: ``Macro``
            :param notify_sw: Combine NotifySW in the action_bitfield - OPTIONAL
            :type notify_sw: ``bool``

            :return: ``FkcMainTable.Group`` instance
            :rtype: ``FkcMainTable.Group``

            :raise ``AssertionError``: If trigger_cidx is None or set trigger_key/action_key to an unexpected RandomKey
                                       or profile_number is None while action key = switch to a specific onboard profile
            """
            trigger_bitfield = 0
            for modifier_key in preset_remapped_key.trigger_modifier_keys:
                if modifier_key in [RemappedKey.RandomKey.MODIFIER_KEY]:
                    modifier_key = cls.RandomGenerationHelper.get_random_modifier_key(test_case=test_case)
                # end if
                trigger_bitfield |= KEY_ID_TO_MODIFIER_BITFIELD[modifier_key]
            # end for

            if preset_remapped_key.trigger_key in [RemappedKey.RandomKey.STANDARD_KEY,
                                                   RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                                   RemappedKey.RandomKey.MODIFIER_KEY,
                                                   RemappedKey.RandomKey.ALL_REMAPPABLE_KEY]:
                fn_trigger_remapping = cls.KeyProvider.is_fn_trigger_remapping(
                    layer=preset_remapped_key.layer,
                    trigger_modifier_count=len(preset_remapped_key.trigger_modifier_keys))
                trigger_key = cls.RandomGenerationHelper.get_random_trigger_key(
                    test_case=test_case, key_type=preset_remapped_key.trigger_key,
                    fn_trigger_remapping=fn_trigger_remapping)
            else:
                assert preset_remapped_key.trigger_key not in [RemappedKey.RandomKey.MOUSE_BUTTON,
                                                               RemappedKey.RandomKey.CONSUMER_KEY]
                trigger_key = preset_remapped_key.trigger_key
            # end if
            trigger_cidx = ControlListTestUtils.key_id_to_cidx(test_case=test_case, key_id=trigger_key)
            assert trigger_cidx is not None, f'Cannot get trigger_cidx by trigger_key: {trigger_key!s}'

            action_bitfield = 0
            for modifier_key in preset_remapped_key.action_modifier_keys:
                if modifier_key in [RemappedKey.RandomKey.MODIFIER_KEY]:
                    modifier_key = cls.RandomGenerationHelper.get_random_modifier_key(test_case=test_case)
                # end if
                action_bitfield |= KEY_ID_TO_MODIFIER_BITFIELD[modifier_key]
            # end for

            if notify_sw:
                action_bitfield |= FullKeyCustomization.ActionBitField.NOTIFY_SW
            # end if

            if not trigger_bitfield:
                trigger_bitfield |= FullKeyCustomization.TriggerBitField.SINGLE_KEY_MATCH
            # end if

            if preset_remapped_key.action_type == RemappedKey.ActionType.RANDOM:
                preset_remapped_key.action_type = cls.RandomGenerationHelper.get_random_action_type()
            # end if

            if preset_remapped_key.action_type == RemappedKey.ActionType.KEYBOARD:
                if preset_remapped_key.action_key == RemappedKey.RandomKey.RANDOM:
                    preset_remapped_key.action_key = choice([RemappedKey.RandomKey.STANDARD_KEY,
                                                             RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                                             RemappedKey.RandomKey.MODIFIER_KEY])
                # end if
                if preset_remapped_key.action_key in [RemappedKey.RandomKey.STANDARD_KEY,
                                                      RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                                      RemappedKey.RandomKey.MODIFIER_KEY]:
                    action_key = cls.RandomGenerationHelper.get_random_action_key(
                        test_case=test_case, key_type=preset_remapped_key.action_key)
                else:
                    assert preset_remapped_key.action_key not in [RemappedKey.RandomKey.MOUSE_BUTTON,
                                                                  RemappedKey.RandomKey.CONSUMER_KEY]
                    action_key = preset_remapped_key.action_key
                # end if

                if action_key in MODIFIER_KEY_LIST:
                    action_bitfield |= FullKeyCustomization.ActionBitField.UPDATE_MODIFIERS | \
                                       KEY_ID_TO_MODIFIER_BITFIELD[action_key]
                    button_setting = FkcProfileButton.create_empty_button()
                else:
                    button_setting = FkcProfileButton.create_standard_key(key_id=action_key)
                # end if

                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                    button_setting=button_setting)
            elif preset_remapped_key.action_type == RemappedKey.ActionType.MOUSE:
                if preset_remapped_key.action_key in [RemappedKey.RandomKey.MOUSE_BUTTON, RemappedKey.RandomKey.RANDOM]:
                    button_mask = cls.RandomGenerationHelper.get_random_mouse_button_mask()
                else:
                    assert preset_remapped_key.action_key not in [RemappedKey.RandomKey.STANDARD_KEY,
                                                                  RemappedKey.RandomKey.MODIFIER_KEY,
                                                                  RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                                                  RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                                                                  RemappedKey.RandomKey.CONSUMER_KEY]
                    button_mask = FkcProfileButton.convert_key_id_to_button_mask(key_id=preset_remapped_key.action_key)
                # end if
                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                    button_setting=FkcProfileButton.create_mouse_button(button_mask=button_mask))
            elif preset_remapped_key.action_type == RemappedKey.ActionType.CONSUMER:
                if preset_remapped_key.action_key in [RemappedKey.RandomKey.CONSUMER_KEY, RemappedKey.RandomKey.RANDOM]:
                    action_key = cls.RandomGenerationHelper.get_random_consumer_key(os_variant=os_variant)
                else:
                    assert preset_remapped_key.action_key not in [RemappedKey.RandomKey.STANDARD_KEY,
                                                                  RemappedKey.RandomKey.MODIFIER_KEY,
                                                                  RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                                                  RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                                                                  RemappedKey.RandomKey.MOUSE_BUTTON]
                    action_key = preset_remapped_key.action_key
                # end if
                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                    button_setting=FkcProfileButton.create_consumer_button(
                        key_id=action_key, os_variant=os_variant))
            elif preset_remapped_key.action_type == RemappedKey.ActionType.MACRO:
                if preset_remapped_key.action_key == RemappedKey.RandomKey.RANDOM:
                    preset_remapped_key.macro_entry_index = randint(0, len(macro.entries) - 1)
                # end if
                macro_entry = macro.entries[preset_remapped_key.macro_entry_index]
                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                    button_setting=FkcProfileButton.create_execute_macro(sector_id=macro.first_sector_id_lsb,
                                                                         address=macro_entry.start_address))
            elif preset_remapped_key.action_type == RemappedKey.ActionType.STOP_MACRO:
                macro_entry = macro.entries[preset_remapped_key.macro_entry_index]
                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                    button_setting=FkcProfileButton.create_stop_macro(sector_id=macro.first_sector_id_lsb,
                                                                      address=macro_entry.start_address))
            elif preset_remapped_key.action_type == RemappedKey.ActionType.STOP_ALL_MACRO:
                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                    button_setting=FkcProfileButton.create_stop_all_macros())
            elif preset_remapped_key.action_type == RemappedKey.ActionType.FUNCTION:
                if preset_remapped_key.action_key in [RemappedKey.RandomKey.RANDOM]:
                    preset_remapped_key.action_key = cls.RandomGenerationHelper.get_random_function_key()
                # end if
                if preset_remapped_key.action_key == KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE:
                    assert preset_remapped_key.profile_number is not None
                # end if
                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield,
                    button_setting=FkcProfileButton.create_function_button(
                        function_type=FkcProfileButton.convert_key_id_to_function_type(
                            key_id=preset_remapped_key.action_key),
                        profile_number=preset_remapped_key.profile_number))
            elif preset_remapped_key.action_type == RemappedKey.ActionType.VIRTUAL_MODIFIER:
                if preset_remapped_key.action_key == KEY_ID.FN_KEY:
                    button_settings = FkcProfileButton.create_fn_key()
                elif preset_remapped_key.action_key == KEY_ID.G_SHIFT:
                    button_settings = FkcProfileButton.create_gshift_key()
                else:
                    raise ValueError(f'the action key is not Fn or GShift key! {preset_remapped_key.action_key}')
                # end if
                row = FkcMainTable.Group.Row(
                    trigger_bitfield=trigger_bitfield, action_bitfield=action_bitfield, button_setting=button_settings)
            else:
                raise ValueError(f'Unsupported action type: {preset_remapped_key.action_type}')
            # end if

            return FkcMainTable.Group(trigger_cidx=trigger_cidx, rows=[row])
        # end def create_key_remapping

        @classmethod
        def create_main_tables(
                cls, test_case, os_variant, directory, random_parameters, preset_remapped_keys=None,
                macro=None, notify_sw=False, raise_buffer_overflow=True, oversize_fkc_table=False):
            """
            Create a FKC main tables by the preset and random remapped keys

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param os_variant: OS variant
            :type os_variant: ``OS | str``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param random_parameters: Random parameters
            :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters``
            :param preset_remapped_keys: The preset remapped keys - OPTIONAL
            :type preset_remapped_keys: ``list[RemappedKey] | None``
            :param macro: Macro object
            :type macro: ``Macro``
            :param notify_sw: Combine NotifySW in the action_bitfield - OPTIONAL
            :type notify_sw: ``bool``
            :param raise_buffer_overflow: Flag indicating to raise FKC table overflow RAM buffer error - OPTIONAL
            :type raise_buffer_overflow: ``bool``
            :param oversize_fkc_table: Flag indicating to create oversize FKC profiles - OPTIONAL
            :type oversize_fkc_table: ``bool``

            :return: ``FkcMainTable`` instances for BASE, FN and GSHIFT layers
            :rtype: ``list[FkcMainTable]``

            :raise ``ValueError``: If main table size > ram_buffer_size
            :raise ``AssertionError``: If assigned predefined remapped keys but set full_keys as True. Or
                                       random_parameters.button.count is not 0
            :raise ``Exception``: If found a duplicated item in the preset remapped keys or cannot find an unused
                                  trigger key in 10 times
            """
            # Create empty FKC main tables for BASE(index=0), Fn(index=1) and GShift(index=2) layers
            main_tables = [FkcMainTable(groups=[]), FkcMainTable(groups=[]), FkcMainTable(groups=[])]

            if preset_remapped_keys:
                preset_remapped_keys = RemappedKey.sort(preset_remapped_keys=preset_remapped_keys)
                for remapped_key in preset_remapped_keys:
                    success = False
                    retry_count = 10
                    while not success:
                        new_group = cls.create_key_remapping(test_case=test_case, preset_remapped_key=remapped_key,
                                                             macro=macro, os_variant=os_variant)
                        success = main_tables[remapped_key.layer].append(new_group=new_group)
                        if not success:
                            if remapped_key.trigger_key in [RemappedKey.RandomKey.MODIFIER_KEY,
                                                            RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                                            RemappedKey.RandomKey.STANDARD_KEY,
                                                            RemappedKey.RandomKey.ALL_REMAPPABLE_KEY]:
                                retry_count -= 1
                                if retry_count == 0:
                                    raise Exception('Cannot find an unused trigger key in 10 times.')
                                # end if
                            else:
                                raise Exception('Find a duplicated remapped key in the preset list.')
                            # end if
                        # end if
                    # end while
                # end for
            # end if

            if random_parameters.button.full_keys:
                assert random_parameters.button.count == 0
                fn_trigger_remapping = cls.KeyProvider.is_fn_trigger_remapping(
                    layer=random_parameters.layer, trigger_modifier_count=random_parameters.button.trigger_modifiers[0])
                all_remappable_keys = cls.KeyProvider.trigger_key_get_key_list(
                    test_case=test_case,
                    key_type=random_parameters.button.trigger_key_type,
                    fn_trigger_remapping=fn_trigger_remapping)

                if random_parameters.remove_used_keys and preset_remapped_keys:
                    for remapped_key in preset_remapped_keys:
                        for modifier_key_id in remapped_key.trigger_modifier_keys:
                            if modifier_key_id in all_remappable_keys:
                                all_remappable_keys.remove(modifier_key_id)
                            # end if
                        # end for
                        if remapped_key.trigger_key in all_remappable_keys:
                            all_remappable_keys.remove(remapped_key.trigger_key)
                        # end if
                    # end for
                # end if

                for trigger_key in all_remappable_keys:
                    new_group = cls.RandomGenerationHelper.generate_key_remapping(
                        test_case=test_case,
                        os_variant=os_variant,
                        random_parameters=random_parameters,
                        trigger_key=trigger_key,
                        macro=macro,
                        notify_sw=notify_sw)
                    if new_group:
                        main_tables[random_parameters.layer].append(new_group=new_group)
                    # end if
                # end for
            else:
                random_count = random_parameters.button.count
                retry_count = 10
                while (oversize_fkc_table and main_tables[random_parameters.layer].n_bytes <=
                       test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION.F_FkcConfigFileMaxsize) or \
                        random_count > 0:
                    new_group = cls.RandomGenerationHelper.generate_key_remapping(
                        test_case=test_case,
                        os_variant=os_variant,
                        random_parameters=random_parameters,
                        macro=macro,
                        notify_sw=notify_sw)
                    success = main_tables[random_parameters.layer].append(new_group=new_group) \
                        if new_group else False

                    if success:
                        retry_count = 10
                        random_count -= 1
                    else:
                        retry_count -= 1
                        if retry_count == 0:
                            raise Exception('Cannot find an unused trigger key in 10 times.')
                        # end if
                    # end if
                # end while
            # end if

            if raise_buffer_overflow and not oversize_fkc_table:
                for layer in FkcMainTable.Layer:
                    cls.check_size(test_case=test_case, table_size=main_tables[layer].n_bytes)
                # end for
            # end if

            for layer in FkcMainTable.Layer:
                if not main_tables[layer].is_empty():
                    main_tables[layer].register(directory=directory,
                                                file_type_id=FkcMainTable.Layer.to_file_type_id(layer=layer))
                # end if
            # end for

            return main_tables
        # end def create_main_tables

        @classmethod
        def _convert_to_macro_commands(cls, test_case, preset_macro_entry):
            """
            Convert preset macro entry to Macro commands

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param preset_macro_entry: Preset macro entry
            :type preset_macro_entry: ``PresetMacroEntry``

            :return: ``Macro.Entry`` instance
            :rtype: ``list[MacroCommand0 | MacroCommand1 | MacroCommand2 | MacroCommand4]``
            """
            commands = []
            for preset_command in preset_macro_entry.commands:
                if preset_command.TYPE == ProfileMacro.Opcode.KEY_DOWN:
                    if preset_command.key_id in [RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                                 RemappedKey.RandomKey.MODIFIER_KEY,
                                                 RemappedKey.RandomKey.STANDARD_KEY]:
                        key_id = cls.RandomGenerationHelper.get_random_key(test_case=test_case,
                                                                           key_type=preset_command.key_id)
                    else:
                        key_id = preset_command.key_id
                    # end if
                    if preset_command.action == KeyAction.PRESS:
                        commands.append(ProfileMacro.create_std_key_down(key_id=key_id))
                    elif preset_command.action == KeyAction.RELEASE:
                        commands.append(ProfileMacro.create_std_key_up(key_id=key_id))
                    else:
                        key_down, key_up = ProfileMacro.create_std_key_stroke(key_id=key_id)
                        commands.append(key_down)
                        commands.append(key_up)
                    # end if
                elif preset_command.TYPE == ProfileMacro.Opcode.BUTTON_DOWN:
                    mouse_button = FkcProfileButton.convert_key_id_to_button_mask(key_id=preset_command.key_id)
                    if preset_command.action == KeyAction.PRESS:
                        commands.append(ProfileMacro.create_button_down(button_mask=mouse_button))
                    elif preset_command.action == KeyAction.RELEASE:
                        commands.append(ProfileMacro.create_button_up(button_mask=mouse_button))
                    else:
                        button_down, button_up = ProfileMacro.create_button_stroke(button_mask=mouse_button)
                        commands.append(button_down)
                        commands.append(button_up)
                    # end if
                elif preset_command.TYPE == ProfileMacro.Opcode.CONS_DOWN:
                    if preset_command.action == KeyAction.PRESS:
                        commands.append(ProfileMacro.create_cons_key_down(key_id=preset_command.key_id,
                                                                          os_variant=preset_command.os_variant))
                    elif preset_command.action == KeyAction.RELEASE:
                        commands.append(ProfileMacro.create_cons_key_up(key_id=preset_command.key_id,
                                                                        os_variant=preset_command.os_variant))
                    else:
                        consumer_down, consumer_up = ProfileMacro.create_cons_key_stroke(
                            key_id=preset_command.key_id, os_variant=preset_command.os_variant)
                        commands.append(consumer_down)
                        commands.append(consumer_up)
                    # end if
                elif preset_command.TYPE == ProfileMacro.Opcode.XY:
                    commands.append(ProfileMacro.create_xy_movement(x_pos=preset_command.x, y_pos=preset_command.y))
                elif preset_command.TYPE == ProfileMacro.Opcode.ROLLER:
                    commands.append(ProfileMacro.create_roller(v_wheel=preset_command.wheel))
                elif preset_command.TYPE == ProfileMacro.Opcode.AC_PAN:
                    commands.append(ProfileMacro.create_ac_pan(h_wheel=preset_command.ac_pan))
                elif preset_command.TYPE == ProfileMacro.Opcode.WAIT_FOR_X_MS:
                    commands.append(ProfileMacro.create_delay(time_ms=preset_command.ms))
                elif preset_command.TYPE == ProfileMacro.Opcode.MACRO_END:
                    commands.append(ProfileMacro.create_macro_end())
                elif preset_command.TYPE == ProfileMacro.Opcode.REPEAT_WHILE_PRESSED:
                    commands.append(ProfileMacro.create_repeat_while_pressed())
                elif preset_command.TYPE == ProfileMacro.Opcode.REPEAT_UNTIL_CANCEL:
                    commands.append(ProfileMacro.create_repeat_until_cancel())
                elif preset_command.TYPE == ProfileMacro.Opcode.WAIT_FOR_RELEASE:
                    commands.append(ProfileMacro.create_wait_for_release())
                elif preset_command.TYPE == ProfileMacro.Opcode.JUMP:
                    commands.append(ProfileMacro.create_jump(sector_id=preset_command.sector_id,
                                                             address=preset_command.address))
                elif preset_command.TYPE == ProfileMacro.Opcode.NO_OPERATION:
                    commands.append(ProfileMacro.create_no_operation())
                # end if
            # end for

            return commands
        # end def _convert_to_macro_commands

        @classmethod
        def create_macro(cls, test_case, directory, preset_macro_entries, raise_buffer_overflow=True):
            """
            Create Macro by preset macro entries

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param preset_macro_entries: Preset macro entry list
            :type preset_macro_entries: ``list[PresetMacroEntry]``
            :param raise_buffer_overflow: Flag indicating to raise FKC table overflow RAM buffer error - OPTIONAL
            :type raise_buffer_overflow: ``bool``

            :return: ``Macro`` instance
            :rtype: ``Macro``

            :raise ``ValueError``: If macro table size > ram_buffer_size or input an unknown end command
            """
            start_address = 0
            entries = []
            for preset_macro_entry in preset_macro_entries:
                commands = cls._convert_to_macro_commands(test_case=test_case, preset_macro_entry=preset_macro_entry)
                entries.append(Macro.Entry(commands=commands, start_address=start_address))
                # Update start address
                for command in commands:
                    start_address += len(command)
                # end for
            # end for

            macro = Macro(entries=entries)
            if raise_buffer_overflow:
                cls.check_size(test_case=test_case, table_size=macro.n_bytes)
            # end if
            macro.register(directory=directory)

            return macro
        # end def create_macro

        @classmethod
        def update_macro(cls, test_case, directory, macro, preset_macro_entries, raise_buffer_overflow=True):
            """
            Update Macro with preset macro entries

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param macro: ``Macro`` instance
            :type macro: ``Macro``
            :param preset_macro_entries: Preset macro entry list
            :type preset_macro_entries: ``list[PresetMacroEntry]``
            :param raise_buffer_overflow: Flag indicating to raise FKC table overflow RAM buffer error - OPTIONAL
            :type raise_buffer_overflow: ``bool``

            :raise ``ValueError``: If macro table size > ram_buffer_size or input an unknown end command
            """
            # Compute start address
            if len(macro.entries) > 0:
                start_address = macro.entries[-1].start_address
                for command in macro.entries[-1].commands:
                    start_address += len(command)
                # end for
            else:
                start_address = 0
            # end if
            entries = []
            for preset_macro_entry in preset_macro_entries:
                commands = cls._convert_to_macro_commands(test_case=test_case, preset_macro_entry=preset_macro_entry)
                entries.append(Macro.Entry(commands=commands, start_address=start_address))
                # Update start address
                for command in commands:
                    start_address += len(command)
                # end for
            # end for

            macro.append(directory=directory, entries=entries)
            if raise_buffer_overflow:
                cls.check_size(test_case=test_case, table_size=macro.n_bytes)
            # end if
        # end def update_macro

        @classmethod
        def convert_to_remapped_keys(cls, test_case, fkc_main_tables, os_variant, macro=None):
            """
            Convert ``FKCMainTable`` to trigger and action key id list

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param fkc_main_tables: ``FKCMainTable`` instances for BASE, Fn and GSHIFT layers
            :type fkc_main_tables: ``list[FkcMainTable]``
            :param os_variant: OS variant
            :type os_variant: ``OS | str``
            :param macro: Macro object - OPTIONAL
            :type macro: ``Macro``

            :return: Trigger and action key id list
            :rtype: ``list[RemappedKey]``

            :raise ``AssertionError``: If the macro is None while remapping macro or the action type is unknown
            """
            remapped_keys = []
            for layer, fkc_main_table in enumerate(fkc_main_tables):
                if fkc_main_table.is_empty():
                    continue
                # end if
                fkc_idx = 0
                for group in fkc_main_table.groups:
                    trigger_key_id = ControlListTestUtils.cidx_to_key_id(test_case=test_case,
                                                                         cid_index=group.trigger_cidx)
                    for row in group.rows:
                        trigger_modifier_keys = [] if not to_int(row.trigger_bitfield) else cls.convert_to_key_ids(
                                modifier_bitfield=to_int(row.trigger_bitfield))
                        action_modifier_keys = [] if not to_int(row.action_bitfield) else cls.convert_to_key_ids(
                            modifier_bitfield=to_int(row.action_bitfield))

                        action_type = RemappedKey.get_action_type(button_settings=row.button_setting)
                        if action_type == RemappedKey.ActionType.KEYBOARD:
                            hid_usage = to_int(row.button_setting.param_4)
                            if hid_usage:
                                action_key_id = KEYBOARD_HID_USAGE_TO_KEY_ID_MAP[hid_usage]
                            else:
                                # The case of remapping Key -> Modifier
                                action_key_id = None
                            # end if

                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.KEYBOARD,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             action_modifier_keys=action_modifier_keys,
                                                             action_key=action_key_id,
                                                             trigger_cidx=group.trigger_cidx,
                                                             action_hid_usage=row.button_setting.param_4,
                                                             fkc_idx=fkc_idx))
                        elif action_type == RemappedKey.ActionType.MACRO:
                            assert macro
                            macro_entry_index, macron_commands = Macro.convert_to_macro_commands(
                                macro=macro, first_sector_id_lsb=to_int(row.button_setting.param_2),
                                start_address=(to_int(row.button_setting.param_3) << 8) +
                                               to_int(row.button_setting.param_4), os_variant=os_variant)
                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.MACRO,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             trigger_cidx=group.trigger_cidx,
                                                             action_modifier_keys=action_modifier_keys,
                                                             macro_entry_index=macro_entry_index,
                                                             macro_commands=macron_commands,
                                                             fkc_idx=fkc_idx))
                        elif action_type == RemappedKey.ActionType.STOP_MACRO:
                            assert macro
                            macro_entry_index, macron_commands = Macro.convert_to_macro_commands(
                                macro=macro, first_sector_id_lsb=to_int(row.button_setting.param_2),
                                start_address=(to_int(row.button_setting.param_3) << 8) +
                                               to_int(row.button_setting.param_4), os_variant=os_variant)
                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.STOP_MACRO,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             trigger_cidx=group.trigger_cidx,
                                                             action_modifier_keys=action_modifier_keys,
                                                             macro_entry_index=macro_entry_index,
                                                             macro_commands=macron_commands,
                                                             fkc_idx=fkc_idx))
                        elif action_type == RemappedKey.ActionType.STOP_ALL_MACRO:
                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.STOP_ALL_MACRO,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             trigger_cidx=group.trigger_cidx,
                                                             action_modifier_keys=action_modifier_keys,
                                                             fkc_idx=fkc_idx))
                        elif action_type == RemappedKey.ActionType.MOUSE:
                            button_mask = to_int(row.button_setting.param_3) << 8 | to_int(row.button_setting.param_4)
                            action_key_id = FkcProfileButton.convert_button_mask_to_key_id(button_mask=button_mask)
                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.MOUSE,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             action_modifier_keys=action_modifier_keys,
                                                             action_key=action_key_id,
                                                             trigger_cidx=group.trigger_cidx,
                                                             button_mask=button_mask,
                                                             fkc_idx=fkc_idx))
                        elif action_type == RemappedKey.ActionType.CONSUMER:
                            consumer_hid_usage = to_int(row.button_setting.param_3) << 8 | \
                                                 to_int(row.button_setting.param_4)
                            action_key_id = FkcProfileButton.get_consumer_key_id(consumer_usage=consumer_hid_usage,
                                                                                 os_variant=os_variant)
                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.CONSUMER,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             action_modifier_keys=action_modifier_keys,
                                                             action_key=action_key_id,
                                                             trigger_cidx=group.trigger_cidx,
                                                             consumer_hid_usage=consumer_hid_usage,
                                                             fkc_idx=fkc_idx))
                        elif action_type == RemappedKey.ActionType.FUNCTION:
                            function_type = FkcProfileButton.FunctionExecution(to_int(row.button_setting.param_2))
                            action_key = FkcProfileButton.convert_function_type_to_key_id(function_type=function_type)
                            profile_number = to_int(row.button_setting.param_3) \
                                if function_type == FkcProfileButton.FunctionExecution.SWITCH_TO_SPECIFIC_PROFILE \
                                else None
                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.FUNCTION,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             action_modifier_keys=action_modifier_keys,
                                                             action_key=action_key,
                                                             trigger_cidx=group.trigger_cidx,
                                                             profile_number=profile_number,
                                                             fkc_idx=fkc_idx))
                        elif action_type == RemappedKey.ActionType.VIRTUAL_MODIFIER:
                            action_key = KEY_ID.FN_KEY if to_int(row.button_setting.param_4) == 1 else KEY_ID.G_SHIFT
                            remapped_keys.append(RemappedKey(layer=FkcMainTable.Layer(layer),
                                                             action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                                                             trigger_modifier_keys=trigger_modifier_keys,
                                                             trigger_key=trigger_key_id,
                                                             action_modifier_keys=action_modifier_keys,
                                                             action_key=action_key,
                                                             trigger_cidx=group.trigger_cidx,
                                                             fkc_idx=fkc_idx))
                        else:
                            raise ValueError(f'Unknown action type: {action_type}')
                        # end if
                        fkc_idx += 1
                    # end for
                # end for
            # end for
            return remapped_keys
        # end def convert_to_remapped_keys

        @classmethod
        def convert_to_key_ids(cls, modifier_bitfield):
            """
            Convert Modifier Bitfield to ``KEY_ID`` list

            :param modifier_bitfield: Modifier bitfield
            :type modifier_bitfield: ``int``

            :return: The ``KEY)ID`` list
            :rtype: ``list[KEY_ID]``
            """
            key_ids = []

            if modifier_bitfield & FullKeyCustomization.TriggerBitField.R_GUI:
                key_ids.append(KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION)
            # end if
            if modifier_bitfield & FullKeyCustomization.TriggerBitField.R_ALT:
                key_ids.append(KEY_ID.KEYBOARD_RIGHT_ALT)
            # end if
            if modifier_bitfield & FullKeyCustomization.TriggerBitField.R_SHIFT:
                key_ids.append(KEY_ID.KEYBOARD_RIGHT_SHIFT)
            # end if
            if modifier_bitfield & FullKeyCustomization.TriggerBitField.R_CTRL:
                key_ids.append(KEY_ID.KEYBOARD_RIGHT_CONTROL)
            # end if
            if modifier_bitfield & FullKeyCustomization.TriggerBitField.L_GUI:
                key_ids.append(KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION)
            # end if
            if modifier_bitfield & FullKeyCustomization.TriggerBitField.L_ALT:
                key_ids.append(KEY_ID.KEYBOARD_LEFT_ALT)
            # end if
            if modifier_bitfield & FullKeyCustomization.TriggerBitField.L_SHIFT:
                key_ids.append(KEY_ID.KEYBOARD_LEFT_SHIFT)
            # end if
            if modifier_bitfield & FullKeyCustomization.TriggerBitField.L_CTRL:
                key_ids.append(KEY_ID.KEYBOARD_LEFT_CONTROL)
            # end if
            return key_ids
        # end def convert_to_key_ids

        @classmethod
        def check_size(cls, test_case, table_size):
            """
            Check the table size doesn't exceed ram_buffer_size

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param table_size: The table sizd
            :type table_size: ``int``

            :raise ``ValueError``: If table size > ram_buffer_size
            """
            ram_buffer_size = to_int(test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_RamBufferSize) - \
                              (FkcMainTable.Group.ROW_LENGTH * 2)
            if table_size >= ram_buffer_size:
                raise ValueError(f'Too many records in the table! size: {table_size} bytes')
            # end if
        # end def check_size

        @classmethod
        def find_key(cls, remapped_keys, preset_remapped_key):
            """
            Find the preset remapped key in the converted remapped keys

            :param remapped_keys: Converted remapped keys
            :type remapped_keys: ``list[RemappedKey]``
            :param preset_remapped_key: Preset remapped key
            :type preset_remapped_key: ``RemappedKey``

            :raise ``Exception``: If cannot find preset remapped key in the converted remapped keys
            """
            for remapped_key in remapped_keys:
                if remapped_key.layer == preset_remapped_key.layer and \
                   remapped_key.action_type == preset_remapped_key.action_type and \
                   remapped_key.trigger_modifier_keys == preset_remapped_key.trigger_modifier_keys and \
                   remapped_key.trigger_key == preset_remapped_key.trigger_key:
                    return remapped_key
                # end if
            # end for
            raise Exception(f'Cannot find the preset remapped key {preset_remapped_key} '
                            'in the converted remapped keys.')
    # end class FkcTableHelper

    class FkcKeyMatrixHelper:
        """
        FKC Key Matrix Helper
        """

        @classmethod
        def build_key_sequence(cls, test_case, remapped_key, fn_key=None, gshift_key=None, key_interval=0):
            """
            Build the key remapping test sequence

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            :param fn_key: The combined Fn key id
            :type fn_key: ``KEY_ID``
            :param gshift_key: The combined GShift key id
            :type gshift_key: ``KEY_ID``
            :param key_interval: timing between keystroke - OPTIONAL
            :type key_interval: ``float``
            """
            if remapped_key.layer == FkcMainTable.Layer.FN:
                assert fn_key is not None
                test_case.button_stimuli_emulator.multiple_keys_press(key_ids=[fn_key], delay=.05)
            elif remapped_key.layer == FkcMainTable.Layer.GSHIFT:
                assert gshift_key is not None
                test_case.button_stimuli_emulator.multiple_keys_press(key_ids=[gshift_key], delay=.05)
            # end if

            if not remapped_key.trigger_modifier_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Send the keystroke of trigger key: {remapped_key.trigger_key!s}")
                # ------------------------------------------------------------------------------------------------------
                test_case.button_stimuli_emulator.keystroke(key_id=remapped_key.trigger_key)
            else:
                combination_keys = remapped_key.trigger_modifier_keys + [remapped_key.trigger_key]
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Press then release the combination keys {combination_keys} properly")
                # ------------------------------------------------------------------------------------------------------
                test_case.button_stimuli_emulator.multiple_keys_press(key_ids=combination_keys, delay=0.05)
                test_case.button_stimuli_emulator.multiple_keys_release(key_ids=list(reversed(combination_keys)),
                                                                        delay=0.05)
            # end if
            if remapped_key.layer == FkcMainTable.Layer.FN:
                test_case.button_stimuli_emulator.multiple_keys_release(key_ids=[fn_key], delay=.05)
            elif remapped_key.layer == FkcMainTable.Layer.GSHIFT:
                test_case.button_stimuli_emulator.multiple_keys_release(key_ids=[gshift_key], delay=.05)
            # end if

            sleep(key_interval)
        # end def build_key_sequence

        @staticmethod
        def get_custom_key_expected_actions(key, os_variant):
            """
            Get the expected actions for input keys

            :param key: The action key with its make or break state
            :type key: ``RemappedKey``
            :param os_variant: OS detected by the firmware - OPTIONAL
            :type os_variant: ``str``

            :return: Expected actions
            :rtype: ``list[HIDReport]``, ``list[list[str]]``, ``list[list[int]]``
            """
            custom_response_class = None
            custom_field_name = []
            custom_field_value = []
            if key.trigger_modifier_keys:
                if key.state == MAKE:
                    # Suppressed modifier keys
                    for key_id in key.trigger_modifier_keys:
                        if os_variant not in iter(HidData.KEY_ID_TO_HID_MAP[key_id]):
                            # If we have no information about the detected OS, we select the first available variant
                            os_variant = next(iter(HidData.KEY_ID_TO_HID_MAP[key_id]))
                        # end if
                        fields_name = HidData.KEY_ID_TO_HID_MAP[key_id][os_variant][BREAK]['Fields_name']
                        fields_value = HidData.KEY_ID_TO_HID_MAP[key_id][os_variant][BREAK]['Fields_value']

                        custom_field_name.append(fields_name[0][0])
                        custom_field_value.append(fields_value[0][0])
                    # end for
                elif key.state == BREAK:
                    # FKC UX Guideline No. 1.11
                    # Keep modifiers in MAKE state
                    for key_id in key.trigger_modifier_keys:
                        if os_variant not in iter(HidData.KEY_ID_TO_HID_MAP[key_id]):
                            # If we have no information about the detected OS, we select the first available variant
                            os_variant = next(iter(HidData.KEY_ID_TO_HID_MAP[key_id]))
                        # end if
                        fields_name = HidData.KEY_ID_TO_HID_MAP[key_id][os_variant][MAKE]['Fields_name']
                        fields_value = HidData.KEY_ID_TO_HID_MAP[key_id][os_variant][MAKE]['Fields_value']

                        custom_field_name.append(fields_name[0][0])
                        custom_field_value.append(fields_value[0][0])
                    # end for
                # end if
            # end if

            custom_key_list = key.action_modifier_keys + [key.action_key]
            for key_id in custom_key_list:
                if key_id is None:
                    continue
                # end if
                if os_variant not in iter(HidData.KEY_ID_TO_HID_MAP[key_id]):
                    # If we have no information about the detected OS, we select the first available variant
                    os_variant = next(iter(HidData.KEY_ID_TO_HID_MAP[key_id]))
                # end if
                responses_class = HidData.KEY_ID_TO_HID_MAP[key_id][os_variant][key.state]['Responses_class']
                fields_name = HidData.KEY_ID_TO_HID_MAP[key_id][os_variant][key.state]['Fields_name']
                fields_value = HidData.KEY_ID_TO_HID_MAP[key_id][os_variant][key.state]['Fields_value']
                if not custom_response_class:
                    custom_response_class = responses_class
                # end if
                custom_field_name.append(fields_name[0][0])
                custom_field_value.append(fields_value[0][0])
            # end for

            return custom_response_class, [custom_field_name], [custom_field_value]
        # end def get_custom_key_expected_actions

        @classmethod
        def check_hid_report_by_remapped_key(cls, test_case, key, raise_exception=True, variant=None):
            """
            Check the HID report associated to a key pressed or released stimulus.

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param key: The action key with its make or break state
            :type key: ``RemappedKey``
            :param raise_exception: Flag enabling to raise an exception when a failure occurs - OPTIONAL
            :type raise_exception: ``bool``
            :param variant: OS detected by the firmware - OPTIONAL
            :type variant: ``str`` or ``None``

            :raise ``NoMessageReceived``: Exception thrown by ``HidMessageQueue`` when the expected message hasn't been
            received.
            """
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=test_case, key=key, raise_exception=raise_exception, variant=variant,
                get_expected_action_func=cls.get_custom_key_expected_actions)
        # end def check_hid_report_by_remapped_key

        @classmethod
        def check_hid_report(cls, test_case, remapped_key):
            """
            Check the HID report for FKC remapped key

            Note: This verification method is valid if there is a delay between the modifier and the trigger keypress.

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``

            :raise ``NotImplementedError``: Cannot find the check method for the remapping!
            """
            trigger_modifier = '' if not remapped_key.trigger_modifier_keys else 'n_modifiers_and_'
            action_modifier = '' if not remapped_key.action_modifier_keys else 'm_modifiers_and_'
            if remapped_key.action_type == RemappedKey.ActionType.KEYBOARD:
                action = 'key'
            elif remapped_key.action_type in [RemappedKey.ActionType.MOUSE, RemappedKey.ActionType.CONSUMER]:
                action = 'mouse_or_consumer'
            elif remapped_key.action_type == RemappedKey.ActionType.MACRO:
                action = 'macro'
            else:
                assert remapped_key.action_key in [KEY_ID.NO_ACTION, KEY_ID.TILT_LEFT, KEY_ID.TILT_RIGHT]
                if remapped_key.action_key == KEY_ID.NO_ACTION:
                    # Fixme: Just ignore NO_ACTION key here. Could support it with modifier bitfield in the future
                    #        if needed.
                    return
                # end if
                action = 'tilt_function'
            # end if

            if trigger_modifier == '' and action_modifier != '' and action == 'macro':
                raise NotImplementedError('Not support the check method: Trigger -> Modifiers + Macro')
            elif trigger_modifier != '' and action_modifier != '' and action == 'macro':
                raise NotImplementedError('Not support the check method: Modifiers + Trigger -> Modifiers + Macro')
            elif trigger_modifier != '' and action_modifier != '' and action == 'tilt_function':
                raise NotImplementedError('Not support the check method: Modifiers + Trigger -> Modifiers + Tilt')
            else:
                check_function = getattr(cls, f'check_{trigger_modifier}trigger_remap_to_{action_modifier}{action}')
            # end if
            check_function(test_case=test_case, remapped_key=remapped_key)
        # end def check_hid_report

        @classmethod
        def check_key(cls, test_case, remapped_key):
            """
            Check HID report for the Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=remapped_key.action_key, state=MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=remapped_key.action_key, state=BREAK))
        # end def check_key

        @classmethod
        def check_trigger_remap_to_key(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: Trigger -> Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_key(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_trigger_remap_to_key

        @classmethod
        def check_n_modifiers_and_trigger_remap_to_key(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: N x Modifiers + Trigger -> Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            for modifier_key in remapped_key.trigger_modifier_keys:
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=modifier_key, state=MAKE))
            # end for
            if remapped_key.action_key not in remapped_key.trigger_modifier_keys:
                cls.check_hid_report_by_remapped_key(
                    test_case=test_case,
                    key=RemappedKey(
                        trigger_modifier_keys=remapped_key.trigger_modifier_keys,  # Suppress trigger modifiers
                        action_key=remapped_key.action_key,
                        state=MAKE))
            else:
                different_modifiers = [key for key in remapped_key.trigger_modifier_keys
                                       if key != remapped_key.action_key]
                if different_modifiers:
                    cls.check_hid_report_by_remapped_key(
                        test_case=test_case,
                        key=RemappedKey(
                            action_modifier_keys=different_modifiers,
                            state=BREAK))
                # end if
            # end if
            cls.check_hid_report_by_remapped_key(
                test_case=test_case, key=RemappedKey(action_key=remapped_key.action_key, state=BREAK))
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_n_modifiers_and_trigger_remap_to_key

        @classmethod
        def check_trigger_remap_to_m_modifiers_and_key(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: Trigger -> M x Modifiers + Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_hid_report_by_remapped_key(test_case=test_case,
                                                 key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                                                 action_key=remapped_key.action_key,
                                                                 state=MAKE))
            cls.check_hid_report_by_remapped_key(test_case=test_case,
                                                 key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                                                 action_key=remapped_key.action_key,
                                                                 state=BREAK))
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_trigger_remap_to_n_modifiers_and_key

        @classmethod
        def check_n_modifiers_and_trigger_remap_to_m_modifiers_and_key(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: N x Modifiers + Trigger -> M x Modifiers + Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            for modifier_key in remapped_key.trigger_modifier_keys:
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=modifier_key, state=MAKE))
            # end for

            if any(key in remapped_key.trigger_modifier_keys for key in remapped_key.action_modifier_keys):
                # FKC Guideline No.1_11:
                # No temporary release of modifier when a remap trigger and target include the same modifier
                same_modifiers = [key for key in remapped_key.action_modifier_keys
                                  if key in remapped_key.trigger_modifier_keys]
                new_modifiers = [key for key in remapped_key.action_modifier_keys
                                 if key not in remapped_key.trigger_modifier_keys]
                suppressed_modifiers = [key for key in remapped_key.trigger_modifier_keys
                                        if key not in remapped_key.action_modifier_keys]
                if remapped_key.trigger_modifier_keys != remapped_key.action_modifier_keys:
                    cls.check_hid_report_by_remapped_key(
                        test_case=test_case, key=RemappedKey(
                            trigger_modifier_keys=suppressed_modifiers,
                            action_modifier_keys=new_modifiers,
                            action_key=remapped_key.action_key,
                            state=MAKE))
                else:
                    if remapped_key.action_key:
                        cls.check_hid_report_by_remapped_key(
                            test_case=test_case, key=RemappedKey(action_key=remapped_key.action_key,
                                                                 state=MAKE))
                    # end if
                # end if
                if remapped_key.action_key:
                    cls.check_hid_report_by_remapped_key(
                        test_case=test_case,
                        key=RemappedKey(action_modifier_keys=new_modifiers,
                                        action_key=remapped_key.action_key,
                                        state=BREAK))
                    for modifier_key in reversed(same_modifiers):
                        cls.check_hid_report_by_remapped_key(
                            test_case=test_case,
                            key=RemappedKey(action_key=modifier_key,
                                            state=BREAK))
                    # end for
                else:
                    cls.check_hid_report_by_remapped_key(
                        test_case=test_case,
                        key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                        state=BREAK))
                # end if
            else:
                cls.check_hid_report_by_remapped_key(
                    test_case=test_case, key=RemappedKey(
                        trigger_modifier_keys=remapped_key.trigger_modifier_keys,  # Suppress trigger modifiers
                        action_modifier_keys=remapped_key.action_modifier_keys,
                        action_key=remapped_key.action_key,
                        state=MAKE))
                cls.check_hid_report_by_remapped_key(
                    test_case=test_case,
                    key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                    action_key=remapped_key.action_key,
                                    state=BREAK))
            # end if
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_n_modifiers_and_trigger_remap_to_m_modifiers_and_key

        @classmethod
        def check_trigger_remap_to_mouse_or_consumer(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: Trigger -> Mouse Button or Consumer Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_key(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_trigger_remap_to_mouse_or_consumer

        @classmethod
        def check_n_modifiers_and_trigger_remap_to_mouse_or_consumer(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: N x Modifiers + Trigger -> Mouse Button or Consumer Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            for modifier_key in remapped_key.trigger_modifier_keys:
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=modifier_key, state=MAKE))
            # end for
            cls.check_hid_report_by_remapped_key(
                test_case=test_case,
                key=RemappedKey(action_modifier_keys=remapped_key.trigger_modifier_keys,  # Suppress trigger modifiers
                                state=BREAK))
            cls.check_key(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_n_modifiers_and_trigger_remap_to_mouse_or_consumer

        @classmethod
        def check_trigger_remap_to_m_modifiers_and_mouse_or_consumer(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: Trigger -> M x Modifiers + Mouse Button or Consumer Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_hid_report_by_remapped_key(
                test_case=test_case,
                key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                state=MAKE))
            cls.check_key(test_case=test_case, remapped_key=remapped_key)
            cls.check_hid_report_by_remapped_key(
                test_case=test_case,
                key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                state=BREAK))
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_trigger_remap_to_n_modifiers_and_mouse_or_consumer

        @classmethod
        def check_n_modifiers_and_trigger_remap_to_m_modifiers_and_mouse_or_consumer(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: N x Modifiers + Trigger -> M x Modifiers + Mouse Button or Consumer Key

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            for modifier_key in remapped_key.trigger_modifier_keys:
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=modifier_key, state=MAKE))
            # end for
            if any(key in remapped_key.trigger_modifier_keys for key in remapped_key.action_modifier_keys):
                # FKC Guideline No.1_11:
                # No temporary release of modifier when a remap trigger and target include the same modifier
                same_modifiers = [key for key in remapped_key.action_modifier_keys
                                  if key in remapped_key.trigger_modifier_keys]
                new_modifiers = [key for key in remapped_key.action_modifier_keys
                                 if key not in remapped_key.trigger_modifier_keys]
                suppressed_modifiers = [key for key in remapped_key.trigger_modifier_keys
                                        if key not in remapped_key.action_modifier_keys]
                if new_modifiers:
                    cls.check_hid_report_by_remapped_key(
                        test_case=test_case,
                        key=RemappedKey(trigger_modifier_keys=suppressed_modifiers,
                                        action_modifier_keys=new_modifiers,
                                        state=MAKE))
                else:
                    if suppressed_modifiers:
                        cls.check_hid_report_by_remapped_key(
                             test_case=test_case,
                             key=RemappedKey(action_modifier_keys=suppressed_modifiers,
                                             state=BREAK))
                    # end if
                # end if
                cls.check_key(test_case=test_case, remapped_key=remapped_key)
                if new_modifiers:
                    cls.check_hid_report_by_remapped_key(
                            test_case=test_case,
                            key=RemappedKey(action_modifier_keys=new_modifiers,
                                            state=BREAK))
                # end if
                if same_modifiers:
                    cls.check_hid_report_by_remapped_key(
                        test_case=test_case,
                        key=RemappedKey(action_modifier_keys=same_modifiers,
                                        state=BREAK))
                # end if
            else:
                cls.check_hid_report_by_remapped_key(
                    test_case=test_case, key=RemappedKey(
                        trigger_modifier_keys=remapped_key.trigger_modifier_keys,  # Suppress trigger modifiers
                        action_modifier_keys=remapped_key.action_modifier_keys,
                        state=MAKE))
                cls.check_key(test_case=test_case, remapped_key=remapped_key)
                cls.check_hid_report_by_remapped_key(
                    test_case=test_case,
                    key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                    state=BREAK))
            # end if
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_n_modifiers_and_trigger_remap_to_m_modifiers_and_mouse_or_consumer(

        @classmethod
        def check_xy_movement(cls, test_case, x, y):
            """
            Check HID report for xy movement

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param x: The x movement
            :type x: ``int``
            :param y: The y movement
            :type y: ``int``
            """
            mouse_report = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                 class_type=(HidMouse, HidMouseNvidiaExtension))
            test_case.assertEqual(expected=x, obtained=to_int(mouse_report.x),
                                  msg=f'Unexpected X movement: {mouse_report.x}')
            test_case.assertEqual(expected=y, obtained=to_int(mouse_report.y),
                                  msg=f'Unexpected Y movement: {mouse_report.y}')
        # end def check_xy_movement

        @classmethod
        def check_vertical_wheel(cls, test_case, wheel):
            """
            Check HID report for vertical wheel

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param wheel: The movement of vertical wheel
            :type wheel: ``int``
            """
            mouse_report = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                 class_type=(HidMouse, HidMouseNvidiaExtension))
            test_case.assertEqual(expected=HexList(Numeral(wheel, byteCount=1)), obtained=mouse_report.wheel,
                                  msg=f'Unexpected Vertical Wheel: {mouse_report.wheel}')
        # end def check_vertical_wheel

        @classmethod
        def check_horizontal_wheel(cls, test_case, ac_pan):
            """
            Check HID report for horizontal wheel

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param ac_pan: The movement of horizontal wheel
            :type ac_pan: ``int``
            """
            mouse_report = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                 class_type=(HidMouse, HidMouseNvidiaExtension))
            test_case.assertEqual(expected=HexList(Numeral(ac_pan, byteCount=1)), obtained=mouse_report.ac_pan,
                                  msg=f'Unexpected AC Pan: {mouse_report.ac_pan}')
        # end def check_horizontal_wheel

        @classmethod
        def check_macro(cls, test_case, remapped_key):
            """
            Check HID report for the Macro

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The remapped key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            for command in remapped_key.macro_commands:
                if command.TYPE in [ProfileMacro.Opcode.KEY_DOWN, ProfileMacro.Opcode.BUTTON_DOWN,
                                    ProfileMacro.Opcode.CONS_DOWN]:
                    if command.action == KeyAction.PRESS:
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=command.key_id, state=MAKE))
                    elif command.action == KeyAction.RELEASE:
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=command.key_id, state=BREAK))
                    # end if
                elif command.TYPE == ProfileMacro.Opcode.XY:
                    cls.check_xy_movement(test_case=test_case, x=command.x, y=command.y)
                elif command.TYPE == ProfileMacro.Opcode.ROLLER:
                    cls.check_vertical_wheel(test_case=test_case, wheel=command.wheel)
                elif command.TYPE == ProfileMacro.Opcode.AC_PAN:
                    cls.check_horizontal_wheel(test_case=test_case, ac_pan=command.ac_pan)
                # end if
            # end for
        # end def check_macro

        @classmethod
        def check_trigger_remap_to_macro(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: Trigger -> Macro

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The remapped key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_macro(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_trigger_remap_to_macro

        @classmethod
        def check_n_modifiers_and_trigger_remap_to_macro(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: N x Modifiers + Trigger -> Macro

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            for trigger_modifier in remapped_key.trigger_modifier_keys:
                cls.check_hid_report_by_remapped_key(
                    test_case=test_case, key=RemappedKey(action_modifier_keys=[trigger_modifier], state=MAKE))
            # end for
            cls.check_hid_report_by_remapped_key(
                test_case=test_case,
                key=RemappedKey(action_modifier_keys=remapped_key.trigger_modifier_keys, state=BREAK))
            cls.check_macro(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_n_modifiers_trigger_remap_to_macro

        @classmethod
        def check_tilt_function(cls, test_case, remapped_key):
            """
            Check HID report for the Function (Tilt)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_hid_report_by_remapped_key(
                test_case=test_case, key=RemappedKey(action_key=remapped_key.action_key, state=MAKE))
        # end def check_tilt_function

        @classmethod
        def check_trigger_remap_to_tilt_function(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: Trigger -> Function (Tilt)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_tilt_function(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_trigger_remap_to_tilt_function

        @classmethod
        def check_n_modifiers_and_trigger_remap_to_tilt_function(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: N x Modifiers + Trigger -> Function (Tilt)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            for trigger_modifier in remapped_key.trigger_modifier_keys:
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=test_case, key=KeyMatrixTestUtils.Key(key_id=trigger_modifier, state=MAKE))
            # end for
            # Suppress trigger modifiers
            cls.check_hid_report_by_remapped_key(
                test_case=test_case,
                key=RemappedKey(action_modifier_keys=remapped_key.trigger_modifier_keys, state=BREAK))
            cls.check_tilt_function(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_n_modifiers_and_trigger_remap_to_tilt_function

        @classmethod
        def check_trigger_remap_to_m_modifiers_and_tilt_function(cls, test_case, remapped_key):
            """
            Check HID report for the remapping: Trigger -> M x Modifiers + Function (Tilt)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param remapped_key: The action key with its make or break state
            :type remapped_key: ``RemappedKey``
            """
            cls.check_hid_report_by_remapped_key(
                test_case=test_case,
                key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                state=MAKE))
            cls.check_hid_report_by_remapped_key(
                test_case=test_case,
                key=RemappedKey(action_modifier_keys=remapped_key.action_modifier_keys,
                                state=BREAK))
            cls.check_tilt_function(test_case=test_case, remapped_key=remapped_key)
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end def check_trigger_remap_to_n_modifiers_and_tilt_function
    # end class FkcKeyMatrixHelper

    @classmethod
    def set_fkc_state_by_toggle_key(cls, test_case, enable, toggle_key_index=0):
        """
        Set FKC enable state by toggle key

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param enable: Indicate the required FKC state
        :type enable: ``bool``
        :param toggle_key_index: The toggle key index (0 ~ 7) - OPTIONAL
        :type toggle_key_index: ``int``
        """
        get_enabled = cls.HIDppHelper.get_set_enabled(test_case=test_case, set_fkc_enabled=0,
                                                      fkc_enabled=0, set_toggle_keys_enabled=0)
        if enable != bool(get_enabled.fkc_state.fkc_enabled):
            test_case.post_requisite_reload_nvs = True
            toggle_key_setting = getattr(test_case.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION,
                                         f'F_ToggleKey{toggle_key_index}Cidx')
            toggle_key_1 = ControlListTestUtils.cidx_to_key_id(test_case=test_case,
                                                               cid_index=to_int(toggle_key_setting[0]))
            toggle_key_2 = ControlListTestUtils.cidx_to_key_id(test_case=test_case,
                                                               cid_index=to_int(toggle_key_setting[1]))
            test_case.button_stimuli_emulator.multiple_keys_press(key_ids=[toggle_key_1, toggle_key_2], delay=0.05)
            test_case.button_stimuli_emulator.multiple_keys_release(key_ids=[toggle_key_2, toggle_key_1], delay=0.05)

            # Check the FKC enable state
            ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=(FNLayerTriggerAsListEvent, FNLayerTriggerAsBitmapEvent))
            enable_disable_event = cls.HIDppHelper.enable_disable_event(test_case=test_case)
            test_case.assertEqual(expected=False,
                                  obtained=bool(enable_disable_event.fkc_failure_enabled_state.failure))
            test_case.assertEqual(expected=enable,
                                  obtained=bool(enable_disable_event.fkc_failure_enabled_state.enabled))
        # end if
    # end def toggle_fkc_enable
# end class FullKeyCustomizationTestUtils
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
