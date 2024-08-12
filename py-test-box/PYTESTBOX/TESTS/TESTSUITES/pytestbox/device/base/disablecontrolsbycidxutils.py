#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.disablecontrolsbycidxutils
:brief: Helpers for ``DisableControlsByCIDX`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDX
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDXFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``DisableControlsByCIDX`` feature
    """

    class GameModeFullStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GameModeFullState``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_CONTROLS_BY_CIDX
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "lock_supported": (
                    cls.check_lock_supported,
                    config.F_GameModeLockSupported),
                "supported": (
                    cls.check_supported,
                    config.F_GameModeSupported),
                "locked": (
                    cls.check_locked,
                    config.F_GameModeLocked),
                "enabled": (
                    cls.check_enabled,
                    config.F_GameModeEnabled)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: GameModeFullState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeFullState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_lock_supported(test_case, bitmap, expected):
            """
            Check lock_supported field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: GameModeFullState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeFullState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert lock_supported that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.lock_supported),
                msg="The lock_supported parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.lock_supported})")
        # end def check_lock_supported

        @staticmethod
        def check_supported(test_case, bitmap, expected):
            """
            Check supported field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: GameModeFullState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeFullState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert supported that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.supported),
                msg="The supported parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.supported})")
        # end def check_supported

        @staticmethod
        def check_locked(test_case, bitmap, expected):
            """
            Check locked field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: GameModeFullState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeFullState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert locked that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.locked),
                msg="The locked parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.locked})")
        # end def check_locked

        @staticmethod
        def check_enabled(test_case, bitmap, expected):
            """
            Check enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: GameModeFullState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeFullState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert enabled that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.enabled),
                msg="The enabled parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.enabled})")
        # end def check_enabled
    # end class GameModeFullStateChecker

    class GetGameModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetGameModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "game_mode_full_state": (
                    cls.check_game_mode_full_state,
                    DisableControlsByCIDXTestUtils.GameModeFullStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_game_mode_full_state(test_case, message, expected):
            """
            Check ``game_mode_full_state``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetGameModeResponse to check
            :type message: ``pyhid.hidpp.features.keyboard.disablecontrolsbycidx.GetGameModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            DisableControlsByCIDXTestUtils.GameModeFullStateChecker.check_fields(
                test_case, message.game_mode_full_state, DisableControlsByCIDX.GameModeFullState, expected)
        # end def check_game_mode_full_state
    # end class GetGameModeResponseChecker

    class GetValueChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetValue``
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
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_CONTROLS_BY_CIDX
            return {
                "reserved": (cls.check_reserved, 0),
                "poweron_game_mode_lock": (cls.check_poweron_game_mode_lock, config.F_PowerOnGameModeLock),
                "poweron_game_mode": (cls.check_poweron_game_mode, config.F_PowerOnGameMode)
            }

        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GetValue to check
            :type bitmap: ``DisableControlsByCIDX.GetValue``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")

        # end def check_reserved

        @staticmethod
        def check_poweron_game_mode_lock(test_case, bitmap, expected):
            """
            Check poweron_game_mode_lock field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GetValue to check
            :type bitmap: ``DisableControlsByCIDX.GetValue``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert poweron_game_mode_lock that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The poweron_game_mode_lock shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.poweron_game_mode_lock),
                msg="The poweron_game_mode_lock parameter differs from the one expected")

        # end def check_poweron_game_mode_lock

        @staticmethod
        def check_poweron_game_mode(test_case, bitmap, expected):
            """
            Check poweron_game_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GetValue to check
            :type bitmap: ``DisableControlsByCIDX.GetValue``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert poweron_game_mode that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The poweron_game_mode shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.poweron_game_mode),
                msg="The poweron_game_mode parameter differs from the one expected")
        # end def check_poweron_game_mode
    # end class GetValueChecker

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
                "get_value": (
                    cls.check_get_value,
                    DisableControlsByCIDXTestUtils.GetValueChecker.get_default_check_map(test_case))
            }

        # end def get_default_check_map

        @staticmethod
        def check_get_value(test_case, message, expected):
            """
            Check ``get_value``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetSetPowerOnParamsResponse to check
            :type message: ``GetSetPowerOnParamsResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            DisableControlsByCIDXTestUtils.GetValueChecker.check_fields(
                test_case, message.get_value, DisableControlsByCIDX.GetValue, expected)
        # end def check_get_value
    # end class GetSetPowerOnParamsResponseChecker

    class SupportedPowerOnParamsChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SupportedPowerOnParams``
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
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_CONTROLS_BY_CIDX
            return {
                "reserved": (cls.check_reserved, 0),
                "poweron_game_mode_lock": (cls.check_poweron_game_mode_lock, config.F_PowerOnGameModeLockSupported),
                "poweron_game_mode": (cls.check_poweron_game_mode, config.F_PowerOnGameModeSupported)
            }

        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: SupportedPowerOnParams to check
            :type bitmap: ``DisableControlsByCIDX.SupportedPowerOnParams``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")

        # end def check_reserved

        @staticmethod
        def check_poweron_game_mode_lock(test_case, bitmap, expected):
            """
            Check poweron_game_mode_lock field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: SupportedPowerOnParams to check
            :type bitmap: ``DisableControlsByCIDX.SupportedPowerOnParams``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert poweron_game_mode_lock that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The poweron_game_mode_lock shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.poweron_game_mode_lock),
                msg="The poweron_game_mode_lock parameter differs from the one expected")

        # end def check_poweron_game_mode_lock

        @staticmethod
        def check_poweron_game_mode(test_case, bitmap, expected):
            """
            Check poweron_game_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: SupportedPowerOnParams to check
            :type bitmap: ``DisableControlsByCIDX.SupportedPowerOnParams``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert poweron_game_mode that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The poweron_game_mode shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.poweron_game_mode),
                msg="The poweron_game_mode parameter differs from the one expected")
        # end def check_poweron_game_mode
    # end class SupportedPowerOnParamsChecker

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
                "supported_power_on_params": (
                    cls.check_supported_power_on_params,
                    DisableControlsByCIDXTestUtils.SupportedPowerOnParamsChecker.get_default_check_map(test_case))
            }

        # end def get_default_check_map

        @staticmethod
        def check_supported_power_on_params(test_case, message, expected):
            """
            Check ``supported_power_on_params``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            DisableControlsByCIDXTestUtils.SupportedPowerOnParamsChecker.check_fields(
                test_case, message.supported_power_on_params, DisableControlsByCIDX.SupportedPowerOnParams, expected)
        # end def check_supported_power_on_params
    # end class GetCapabilitiesResponseChecker

    class GameModeStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GameModeState``
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
                "locked": (cls.check_locked, 0),
                "enabled": (cls.check_enabled, DisableControlsByCIDX.GameMode.DISABLE)
            }

        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GameModeState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")

        # end def check_reserved

        @staticmethod
        def check_locked(test_case, bitmap, expected):
            """
            Check locked field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GameModeState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert locked that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The locked shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.locked),
                msg="The locked parameter differs from the one expected")

        # end def check_locked

        @staticmethod
        def check_enabled(test_case, bitmap, expected):
            """
            Check enabled field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GameModeState to check
            :type bitmap: ``DisableControlsByCIDX.GameModeState``
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
    # end class GameModeStateChecker

    class GameModeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GameModeEvent``
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
                "game_mode_state": (
                    cls.check_game_mode_state,
                    DisableControlsByCIDXTestUtils.GameModeStateChecker.get_default_check_map(test_case))
            }

        # end def get_default_check_map

        @staticmethod
        def check_game_mode_state(test_case, message, expected):
            """
            Check ``game_mode_state``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GameModeEvent to check
            :type message: ``GameModeEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            DisableControlsByCIDXTestUtils.GameModeStateChecker.check_fields(
                test_case, message.game_mode_state, DisableControlsByCIDX.GameModeState, expected)
        # end def check_game_mode_state
    # end class GameModeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=DisableControlsByCIDX.FEATURE_ID,
                           factory=DisableControlsByCIDXFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def set_disabled_controls(
                cls, test_case, cidx_7=0, cidx_6=0, cidx_5=0, cidx_4=0, cidx_3=0, cidx_2=0, cidx_1=0, cidx_0=0,
                cidx_15=0, cidx_14=0, cidx_13=0, cidx_12=0, cidx_11=0, cidx_10=0, cidx_9=0, cidx_8=0, cidx_23=0,
                cidx_22=0, cidx_21=0, cidx_20=0, cidx_19=0, cidx_18=0, cidx_17=0, cidx_16=0, cidx_31=0, cidx_30=0,
                cidx_29=0, cidx_28=0, cidx_27=0, cidx_26=0, cidx_25=0, cidx_24=0, cidx_39=0, cidx_38=0, cidx_37=0,
                cidx_36=0, cidx_35=0, cidx_34=0, cidx_33=0, cidx_32=0, cidx_47=0, cidx_46=0, cidx_45=0, cidx_44=0,
                cidx_43=0, cidx_42=0, cidx_41=0, cidx_40=0, cidx_55=0, cidx_54=0, cidx_53=0, cidx_52=0, cidx_51=0,
                cidx_50=0, cidx_49=0, cidx_48=0, cidx_63=0, cidx_62=0, cidx_61=0, cidx_60=0, cidx_59=0, cidx_58=0,
                cidx_57=0, cidx_56=0, cidx_71=0, cidx_70=0, cidx_69=0, cidx_68=0, cidx_67=0, cidx_66=0, cidx_65=0,
                cidx_64=0, cidx_79=0, cidx_78=0, cidx_77=0, cidx_76=0, cidx_75=0, cidx_74=0, cidx_73=0, cidx_72=0,
                cidx_87=0, cidx_86=0, cidx_85=0, cidx_84=0, cidx_83=0, cidx_82=0, cidx_81=0, cidx_80=0, cidx_95=0,
                cidx_94=0, cidx_93=0, cidx_92=0, cidx_91=0, cidx_90=0, cidx_89=0, cidx_88=0, cidx_103=0, cidx_102=0,
                cidx_101=0, cidx_100=0, cidx_99=0, cidx_98=0, cidx_97=0, cidx_96=0, cidx_111=0, cidx_110=0, cidx_109=0,
                cidx_108=0, cidx_107=0, cidx_106=0, cidx_105=0, cidx_104=0, cidx_119=0, cidx_118=0, cidx_117=0,
                cidx_116=0, cidx_115=0, cidx_114=0, cidx_113=0, cidx_112=0, cidx_127=0, cidx_126=0, cidx_125=0,
                cidx_124=0, cidx_123=0, cidx_122=0, cidx_121=0, cidx_120=0, device_index=None, port_index=None,
                software_id=None):
            """
            Process ``SetDisabledControls``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cidx_7: Cidx 7
            :type cidx_7: ``int | HexList``
            :param cidx_6: Cidx 6
            :type cidx_6: ``int | HexList``
            :param cidx_5: Cidx 5
            :type cidx_5: ``int | HexList``
            :param cidx_4: Cidx 4
            :type cidx_4: ``int | HexList``
            :param cidx_3: Cidx 3
            :type cidx_3: ``int | HexList``
            :param cidx_2: Cidx 2
            :type cidx_2: ``int | HexList``
            :param cidx_1: Cidx 1
            :type cidx_1: ``int | HexList``
            :param cidx_0: Cidx 0
            :type cidx_0: ``int | HexList``
            :param cidx_15: Cidx 15
            :type cidx_15: ``int | HexList``
            :param cidx_14: Cidx 14
            :type cidx_14: ``int | HexList``
            :param cidx_13: Cidx 13
            :type cidx_13: ``int | HexList``
            :param cidx_12: Cidx 12
            :type cidx_12: ``int | HexList``
            :param cidx_11: Cidx 11
            :type cidx_11: ``int | HexList``
            :param cidx_10: Cidx 10
            :type cidx_10: ``int | HexList``
            :param cidx_9: Cidx 9
            :type cidx_9: ``int | HexList``
            :param cidx_8: Cidx 8
            :type cidx_8: ``int | HexList``
            :param cidx_23: Cidx 23
            :type cidx_23: ``int | HexList``
            :param cidx_22: Cidx 22
            :type cidx_22: ``int | HexList``
            :param cidx_21: Cidx 21
            :type cidx_21: ``int | HexList``
            :param cidx_20: Cidx 20
            :type cidx_20: ``int | HexList``
            :param cidx_19: Cidx 19
            :type cidx_19: ``int | HexList``
            :param cidx_18: Cidx 18
            :type cidx_18: ``int | HexList``
            :param cidx_17: Cidx 17
            :type cidx_17: ``int | HexList``
            :param cidx_16: Cidx 16
            :type cidx_16: ``int | HexList``
            :param cidx_31: Cidx 31
            :type cidx_31: ``int | HexList``
            :param cidx_30: Cidx 30
            :type cidx_30: ``int | HexList``
            :param cidx_29: Cidx 29
            :type cidx_29: ``int | HexList``
            :param cidx_28: Cidx 28
            :type cidx_28: ``int | HexList``
            :param cidx_27: Cidx 27
            :type cidx_27: ``int | HexList``
            :param cidx_26: Cidx 26
            :type cidx_26: ``int | HexList``
            :param cidx_25: Cidx 25
            :type cidx_25: ``int | HexList``
            :param cidx_24: Cidx 24
            :type cidx_24: ``int | HexList``
            :param cidx_39: Cidx 39
            :type cidx_39: ``int | HexList``
            :param cidx_38: Cidx 38
            :type cidx_38: ``int | HexList``
            :param cidx_37: Cidx 37
            :type cidx_37: ``int | HexList``
            :param cidx_36: Cidx 36
            :type cidx_36: ``int | HexList``
            :param cidx_35: Cidx 35
            :type cidx_35: ``int | HexList``
            :param cidx_34: Cidx 34
            :type cidx_34: ``int | HexList``
            :param cidx_33: Cidx 33
            :type cidx_33: ``int | HexList``
            :param cidx_32: Cidx 32
            :type cidx_32: ``int | HexList``
            :param cidx_47: Cidx 47
            :type cidx_47: ``int | HexList``
            :param cidx_46: Cidx 46
            :type cidx_46: ``int | HexList``
            :param cidx_45: Cidx 45
            :type cidx_45: ``int | HexList``
            :param cidx_44: Cidx 44
            :type cidx_44: ``int | HexList``
            :param cidx_43: Cidx 43
            :type cidx_43: ``int | HexList``
            :param cidx_42: Cidx 42
            :type cidx_42: ``int | HexList``
            :param cidx_41: Cidx 41
            :type cidx_41: ``int | HexList``
            :param cidx_40: Cidx 40
            :type cidx_40: ``int | HexList``
            :param cidx_55: Cidx 55
            :type cidx_55: ``int | HexList``
            :param cidx_54: Cidx 54
            :type cidx_54: ``int | HexList``
            :param cidx_53: Cidx 53
            :type cidx_53: ``int | HexList``
            :param cidx_52: Cidx 52
            :type cidx_52: ``int | HexList``
            :param cidx_51: Cidx 51
            :type cidx_51: ``int | HexList``
            :param cidx_50: Cidx 50
            :type cidx_50: ``int | HexList``
            :param cidx_49: Cidx 49
            :type cidx_49: ``int | HexList``
            :param cidx_48: Cidx 48
            :type cidx_48: ``int | HexList``
            :param cidx_63: Cidx 63
            :type cidx_63: ``int | HexList``
            :param cidx_62: Cidx 62
            :type cidx_62: ``int | HexList``
            :param cidx_61: Cidx 61
            :type cidx_61: ``int | HexList``
            :param cidx_60: Cidx 60
            :type cidx_60: ``int | HexList``
            :param cidx_59: Cidx 59
            :type cidx_59: ``int | HexList``
            :param cidx_58: Cidx 58
            :type cidx_58: ``int | HexList``
            :param cidx_57: Cidx 57
            :type cidx_57: ``int | HexList``
            :param cidx_56: Cidx 56
            :type cidx_56: ``int | HexList``
            :param cidx_71: Cidx 71
            :type cidx_71: ``int | HexList``
            :param cidx_70: Cidx 70
            :type cidx_70: ``int | HexList``
            :param cidx_69: Cidx 69
            :type cidx_69: ``int | HexList``
            :param cidx_68: Cidx 68
            :type cidx_68: ``int | HexList``
            :param cidx_67: Cidx 67
            :type cidx_67: ``int | HexList``
            :param cidx_66: Cidx 66
            :type cidx_66: ``int | HexList``
            :param cidx_65: Cidx 65
            :type cidx_65: ``int | HexList``
            :param cidx_64: Cidx 64
            :type cidx_64: ``int | HexList``
            :param cidx_79: Cidx 79
            :type cidx_79: ``int | HexList``
            :param cidx_78: Cidx 78
            :type cidx_78: ``int | HexList``
            :param cidx_77: Cidx 77
            :type cidx_77: ``int | HexList``
            :param cidx_76: Cidx 76
            :type cidx_76: ``int | HexList``
            :param cidx_75: Cidx 75
            :type cidx_75: ``int | HexList``
            :param cidx_74: Cidx 74
            :type cidx_74: ``int | HexList``
            :param cidx_73: Cidx 73
            :type cidx_73: ``int | HexList``
            :param cidx_72: Cidx 72
            :type cidx_72: ``int | HexList``
            :param cidx_87: Cidx 87
            :type cidx_87: ``int | HexList``
            :param cidx_86: Cidx 86
            :type cidx_86: ``int | HexList``
            :param cidx_85: Cidx 85
            :type cidx_85: ``int | HexList``
            :param cidx_84: Cidx 84
            :type cidx_84: ``int | HexList``
            :param cidx_83: Cidx 83
            :type cidx_83: ``int | HexList``
            :param cidx_82: Cidx 82
            :type cidx_82: ``int | HexList``
            :param cidx_81: Cidx 81
            :type cidx_81: ``int | HexList``
            :param cidx_80: Cidx 80
            :type cidx_80: ``int | HexList``
            :param cidx_95: Cidx 95
            :type cidx_95: ``int | HexList``
            :param cidx_94: Cidx 94
            :type cidx_94: ``int | HexList``
            :param cidx_93: Cidx 93
            :type cidx_93: ``int | HexList``
            :param cidx_92: Cidx 92
            :type cidx_92: ``int | HexList``
            :param cidx_91: Cidx 91
            :type cidx_91: ``int | HexList``
            :param cidx_90: Cidx 90
            :type cidx_90: ``int | HexList``
            :param cidx_89: Cidx 89
            :type cidx_89: ``int | HexList``
            :param cidx_88: Cidx 88
            :type cidx_88: ``int | HexList``
            :param cidx_103: Cidx 103
            :type cidx_103: ``int | HexList``
            :param cidx_102: Cidx 102
            :type cidx_102: ``int | HexList``
            :param cidx_101: Cidx 101
            :type cidx_101: ``int | HexList``
            :param cidx_100: Cidx 100
            :type cidx_100: ``int | HexList``
            :param cidx_99: Cidx 99
            :type cidx_99: ``int | HexList``
            :param cidx_98: Cidx 98
            :type cidx_98: ``int | HexList``
            :param cidx_97: Cidx 97
            :type cidx_97: ``int | HexList``
            :param cidx_96: Cidx 96
            :type cidx_96: ``int | HexList``
            :param cidx_111: Cidx 111
            :type cidx_111: ``int | HexList``
            :param cidx_110: Cidx 110
            :type cidx_110: ``int | HexList``
            :param cidx_109: Cidx 109
            :type cidx_109: ``int | HexList``
            :param cidx_108: Cidx 108
            :type cidx_108: ``int | HexList``
            :param cidx_107: Cidx 107
            :type cidx_107: ``int | HexList``
            :param cidx_106: Cidx 106
            :type cidx_106: ``int | HexList``
            :param cidx_105: Cidx 105
            :type cidx_105: ``int | HexList``
            :param cidx_104: Cidx 104
            :type cidx_104: ``int | HexList``
            :param cidx_119: Cidx 119
            :type cidx_119: ``int | HexList``
            :param cidx_118: Cidx 118
            :type cidx_118: ``int | HexList``
            :param cidx_117: Cidx 117
            :type cidx_117: ``int | HexList``
            :param cidx_116: Cidx 116
            :type cidx_116: ``int | HexList``
            :param cidx_115: Cidx 115
            :type cidx_115: ``int | HexList``
            :param cidx_114: Cidx 114
            :type cidx_114: ``int | HexList``
            :param cidx_113: Cidx 113
            :type cidx_113: ``int | HexList``
            :param cidx_112: Cidx 112
            :type cidx_112: ``int | HexList``
            :param cidx_127: Cidx 127
            :type cidx_127: ``int | HexList``
            :param cidx_126: Cidx 126
            :type cidx_126: ``int | HexList``
            :param cidx_125: Cidx 125
            :type cidx_125: ``int | HexList``
            :param cidx_124: Cidx 124
            :type cidx_124: ``int | HexList``
            :param cidx_123: Cidx 123
            :type cidx_123: ``int | HexList``
            :param cidx_122: Cidx 122
            :type cidx_122: ``int | HexList``
            :param cidx_121: Cidx 121
            :type cidx_121: ``int | HexList``
            :param cidx_120: Cidx 120
            :type cidx_120: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: SetDisabledControlsResponse
            :rtype: ``SetDisabledControlsResponse``
            """
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.set_disabled_controls_cls(
                device_index=device_index,
                feature_index=feature_4523_index,
                cidx_7=cidx_7,
                cidx_6=cidx_6,
                cidx_5=cidx_5,
                cidx_4=cidx_4,
                cidx_3=cidx_3,
                cidx_2=cidx_2,
                cidx_1=cidx_1,
                cidx_0=cidx_0,
                cidx_15=cidx_15,
                cidx_14=cidx_14,
                cidx_13=cidx_13,
                cidx_12=cidx_12,
                cidx_11=cidx_11,
                cidx_10=cidx_10,
                cidx_9=cidx_9,
                cidx_8=cidx_8,
                cidx_23=cidx_23,
                cidx_22=cidx_22,
                cidx_21=cidx_21,
                cidx_20=cidx_20,
                cidx_19=cidx_19,
                cidx_18=cidx_18,
                cidx_17=cidx_17,
                cidx_16=cidx_16,
                cidx_31=cidx_31,
                cidx_30=cidx_30,
                cidx_29=cidx_29,
                cidx_28=cidx_28,
                cidx_27=cidx_27,
                cidx_26=cidx_26,
                cidx_25=cidx_25,
                cidx_24=cidx_24,
                cidx_39=cidx_39,
                cidx_38=cidx_38,
                cidx_37=cidx_37,
                cidx_36=cidx_36,
                cidx_35=cidx_35,
                cidx_34=cidx_34,
                cidx_33=cidx_33,
                cidx_32=cidx_32,
                cidx_47=cidx_47,
                cidx_46=cidx_46,
                cidx_45=cidx_45,
                cidx_44=cidx_44,
                cidx_43=cidx_43,
                cidx_42=cidx_42,
                cidx_41=cidx_41,
                cidx_40=cidx_40,
                cidx_55=cidx_55,
                cidx_54=cidx_54,
                cidx_53=cidx_53,
                cidx_52=cidx_52,
                cidx_51=cidx_51,
                cidx_50=cidx_50,
                cidx_49=cidx_49,
                cidx_48=cidx_48,
                cidx_63=cidx_63,
                cidx_62=cidx_62,
                cidx_61=cidx_61,
                cidx_60=cidx_60,
                cidx_59=cidx_59,
                cidx_58=cidx_58,
                cidx_57=cidx_57,
                cidx_56=cidx_56,
                cidx_71=cidx_71,
                cidx_70=cidx_70,
                cidx_69=cidx_69,
                cidx_68=cidx_68,
                cidx_67=cidx_67,
                cidx_66=cidx_66,
                cidx_65=cidx_65,
                cidx_64=cidx_64,
                cidx_79=cidx_79,
                cidx_78=cidx_78,
                cidx_77=cidx_77,
                cidx_76=cidx_76,
                cidx_75=cidx_75,
                cidx_74=cidx_74,
                cidx_73=cidx_73,
                cidx_72=cidx_72,
                cidx_87=cidx_87,
                cidx_86=cidx_86,
                cidx_85=cidx_85,
                cidx_84=cidx_84,
                cidx_83=cidx_83,
                cidx_82=cidx_82,
                cidx_81=cidx_81,
                cidx_80=cidx_80,
                cidx_95=cidx_95,
                cidx_94=cidx_94,
                cidx_93=cidx_93,
                cidx_92=cidx_92,
                cidx_91=cidx_91,
                cidx_90=cidx_90,
                cidx_89=cidx_89,
                cidx_88=cidx_88,
                cidx_103=cidx_103,
                cidx_102=cidx_102,
                cidx_101=cidx_101,
                cidx_100=cidx_100,
                cidx_99=cidx_99,
                cidx_98=cidx_98,
                cidx_97=cidx_97,
                cidx_96=cidx_96,
                cidx_111=cidx_111,
                cidx_110=cidx_110,
                cidx_109=cidx_109,
                cidx_108=cidx_108,
                cidx_107=cidx_107,
                cidx_106=cidx_106,
                cidx_105=cidx_105,
                cidx_104=cidx_104,
                cidx_119=cidx_119,
                cidx_118=cidx_118,
                cidx_117=cidx_117,
                cidx_116=cidx_116,
                cidx_115=cidx_115,
                cidx_114=cidx_114,
                cidx_113=cidx_113,
                cidx_112=cidx_112,
                cidx_127=cidx_127,
                cidx_126=cidx_126,
                cidx_125=cidx_125,
                cidx_124=cidx_124,
                cidx_123=cidx_123,
                cidx_122=cidx_122,
                cidx_121=cidx_121,
                cidx_120=cidx_120)

            if software_id is not None:
                report.software_id = software_id
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4523.set_disabled_controls_response_cls)
            return response
        # end def set_disabled_controls

        @classmethod
        def set_disabled_controls_and_check_error(
                cls, test_case, error_codes,
                cidx_7=0, cidx_6=0, cidx_5=0, cidx_4=0, cidx_3=0, cidx_2=0, cidx_1=0, cidx_0=0,
                cidx_15=0, cidx_14=0, cidx_13=0, cidx_12=0, cidx_11=0, cidx_10=0, cidx_9=0, cidx_8=0,
                cidx_23=0, cidx_22=0, cidx_21=0, cidx_20=0, cidx_19=0, cidx_18=0, cidx_17=0, cidx_16=0,
                cidx_31=0, cidx_30=0, cidx_29=0, cidx_28=0, cidx_27=0, cidx_26=0, cidx_25=0, cidx_24=0,
                cidx_39=0, cidx_38=0, cidx_37=0, cidx_36=0, cidx_35=0, cidx_34=0, cidx_33=0, cidx_32=0,
                cidx_47=0, cidx_46=0, cidx_45=0, cidx_44=0, cidx_43=0, cidx_42=0, cidx_41=0, cidx_40=0,
                cidx_55=0, cidx_54=0, cidx_53=0, cidx_52=0, cidx_51=0, cidx_50=0, cidx_49=0, cidx_48=0,
                cidx_63=0, cidx_62=0, cidx_61=0, cidx_60=0, cidx_59=0, cidx_58=0, cidx_57=0, cidx_56=0,
                cidx_71=0, cidx_70=0, cidx_69=0, cidx_68=0, cidx_67=0, cidx_66=0, cidx_65=0, cidx_64=0,
                cidx_79=0, cidx_78=0, cidx_77=0, cidx_76=0, cidx_75=0, cidx_74=0, cidx_73=0, cidx_72=0,
                cidx_87=0, cidx_86=0, cidx_85=0, cidx_84=0, cidx_83=0, cidx_82=0, cidx_81=0, cidx_80=0,
                cidx_95=0, cidx_94=0, cidx_93=0, cidx_92=0, cidx_91=0, cidx_90=0, cidx_89=0, cidx_88=0,
                cidx_103=0, cidx_102=0, cidx_101=0, cidx_100=0, cidx_99=0, cidx_98=0, cidx_97=0, cidx_96=0,
                cidx_111=0, cidx_110=0, cidx_109=0, cidx_108=0, cidx_107=0, cidx_106=0, cidx_105=0, cidx_104=0,
                cidx_119=0, cidx_118=0, cidx_117=0, cidx_116=0, cidx_115=0, cidx_114=0, cidx_113=0, cidx_112=0,
                cidx_127=0, cidx_126=0, cidx_125=0, cidx_124=0, cidx_123=0, cidx_122=0, cidx_121=0, cidx_120=0,
                function_index=None, device_index=None, port_index=None):
            """
            Process ``SetDisabledControls``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param cidx_7: Cidx 7
            :type cidx_7: ``int | HexList``
            :param cidx_6: Cidx 6
            :type cidx_6: ``int | HexList``
            :param cidx_5: Cidx 5
            :type cidx_5: ``int | HexList``
            :param cidx_4: Cidx 4
            :type cidx_4: ``int | HexList``
            :param cidx_3: Cidx 3
            :type cidx_3: ``int | HexList``
            :param cidx_2: Cidx 2
            :type cidx_2: ``int | HexList``
            :param cidx_1: Cidx 1
            :type cidx_1: ``int | HexList``
            :param cidx_0: Cidx 0
            :type cidx_0: ``int | HexList``
            :param cidx_15: Cidx 15
            :type cidx_15: ``int | HexList``
            :param cidx_14: Cidx 14
            :type cidx_14: ``int | HexList``
            :param cidx_13: Cidx 13
            :type cidx_13: ``int | HexList``
            :param cidx_12: Cidx 12
            :type cidx_12: ``int | HexList``
            :param cidx_11: Cidx 11
            :type cidx_11: ``int | HexList``
            :param cidx_10: Cidx 10
            :type cidx_10: ``int | HexList``
            :param cidx_9: Cidx 9
            :type cidx_9: ``int | HexList``
            :param cidx_8: Cidx 8
            :type cidx_8: ``int | HexList``
            :param cidx_23: Cidx 23
            :type cidx_23: ``int | HexList``
            :param cidx_22: Cidx 22
            :type cidx_22: ``int | HexList``
            :param cidx_21: Cidx 21
            :type cidx_21: ``int | HexList``
            :param cidx_20: Cidx 20
            :type cidx_20: ``int | HexList``
            :param cidx_19: Cidx 19
            :type cidx_19: ``int | HexList``
            :param cidx_18: Cidx 18
            :type cidx_18: ``int | HexList``
            :param cidx_17: Cidx 17
            :type cidx_17: ``int | HexList``
            :param cidx_16: Cidx 16
            :type cidx_16: ``int | HexList``
            :param cidx_31: Cidx 31
            :type cidx_31: ``int | HexList``
            :param cidx_30: Cidx 30
            :type cidx_30: ``int | HexList``
            :param cidx_29: Cidx 29
            :type cidx_29: ``int | HexList``
            :param cidx_28: Cidx 28
            :type cidx_28: ``int | HexList``
            :param cidx_27: Cidx 27
            :type cidx_27: ``int | HexList``
            :param cidx_26: Cidx 26
            :type cidx_26: ``int | HexList``
            :param cidx_25: Cidx 25
            :type cidx_25: ``int | HexList``
            :param cidx_24: Cidx 24
            :type cidx_24: ``int | HexList``
            :param cidx_39: Cidx 39
            :type cidx_39: ``int | HexList``
            :param cidx_38: Cidx 38
            :type cidx_38: ``int | HexList``
            :param cidx_37: Cidx 37
            :type cidx_37: ``int | HexList``
            :param cidx_36: Cidx 36
            :type cidx_36: ``int | HexList``
            :param cidx_35: Cidx 35
            :type cidx_35: ``int | HexList``
            :param cidx_34: Cidx 34
            :type cidx_34: ``int | HexList``
            :param cidx_33: Cidx 33
            :type cidx_33: ``int | HexList``
            :param cidx_32: Cidx 32
            :type cidx_32: ``int | HexList``
            :param cidx_47: Cidx 47
            :type cidx_47: ``int | HexList``
            :param cidx_46: Cidx 46
            :type cidx_46: ``int | HexList``
            :param cidx_45: Cidx 45
            :type cidx_45: ``int | HexList``
            :param cidx_44: Cidx 44
            :type cidx_44: ``int | HexList``
            :param cidx_43: Cidx 43
            :type cidx_43: ``int | HexList``
            :param cidx_42: Cidx 42
            :type cidx_42: ``int | HexList``
            :param cidx_41: Cidx 41
            :type cidx_41: ``int | HexList``
            :param cidx_40: Cidx 40
            :type cidx_40: ``int | HexList``
            :param cidx_55: Cidx 55
            :type cidx_55: ``int | HexList``
            :param cidx_54: Cidx 54
            :type cidx_54: ``int | HexList``
            :param cidx_53: Cidx 53
            :type cidx_53: ``int | HexList``
            :param cidx_52: Cidx 52
            :type cidx_52: ``int | HexList``
            :param cidx_51: Cidx 51
            :type cidx_51: ``int | HexList``
            :param cidx_50: Cidx 50
            :type cidx_50: ``int | HexList``
            :param cidx_49: Cidx 49
            :type cidx_49: ``int | HexList``
            :param cidx_48: Cidx 48
            :type cidx_48: ``int | HexList``
            :param cidx_63: Cidx 63
            :type cidx_63: ``int | HexList``
            :param cidx_62: Cidx 62
            :type cidx_62: ``int | HexList``
            :param cidx_61: Cidx 61
            :type cidx_61: ``int | HexList``
            :param cidx_60: Cidx 60
            :type cidx_60: ``int | HexList``
            :param cidx_59: Cidx 59
            :type cidx_59: ``int | HexList``
            :param cidx_58: Cidx 58
            :type cidx_58: ``int | HexList``
            :param cidx_57: Cidx 57
            :type cidx_57: ``int | HexList``
            :param cidx_56: Cidx 56
            :type cidx_56: ``int | HexList``
            :param cidx_71: Cidx 71
            :type cidx_71: ``int | HexList``
            :param cidx_70: Cidx 70
            :type cidx_70: ``int | HexList``
            :param cidx_69: Cidx 69
            :type cidx_69: ``int | HexList``
            :param cidx_68: Cidx 68
            :type cidx_68: ``int | HexList``
            :param cidx_67: Cidx 67
            :type cidx_67: ``int | HexList``
            :param cidx_66: Cidx 66
            :type cidx_66: ``int | HexList``
            :param cidx_65: Cidx 65
            :type cidx_65: ``int | HexList``
            :param cidx_64: Cidx 64
            :type cidx_64: ``int | HexList``
            :param cidx_79: Cidx 79
            :type cidx_79: ``int | HexList``
            :param cidx_78: Cidx 78
            :type cidx_78: ``int | HexList``
            :param cidx_77: Cidx 77
            :type cidx_77: ``int | HexList``
            :param cidx_76: Cidx 76
            :type cidx_76: ``int | HexList``
            :param cidx_75: Cidx 75
            :type cidx_75: ``int | HexList``
            :param cidx_74: Cidx 74
            :type cidx_74: ``int | HexList``
            :param cidx_73: Cidx 73
            :type cidx_73: ``int | HexList``
            :param cidx_72: Cidx 72
            :type cidx_72: ``int | HexList``
            :param cidx_87: Cidx 87
            :type cidx_87: ``int | HexList``
            :param cidx_86: Cidx 86
            :type cidx_86: ``int | HexList``
            :param cidx_85: Cidx 85
            :type cidx_85: ``int | HexList``
            :param cidx_84: Cidx 84
            :type cidx_84: ``int | HexList``
            :param cidx_83: Cidx 83
            :type cidx_83: ``int | HexList``
            :param cidx_82: Cidx 82
            :type cidx_82: ``int | HexList``
            :param cidx_81: Cidx 81
            :type cidx_81: ``int | HexList``
            :param cidx_80: Cidx 80
            :type cidx_80: ``int | HexList``
            :param cidx_95: Cidx 95
            :type cidx_95: ``int | HexList``
            :param cidx_94: Cidx 94
            :type cidx_94: ``int | HexList``
            :param cidx_93: Cidx 93
            :type cidx_93: ``int | HexList``
            :param cidx_92: Cidx 92
            :type cidx_92: ``int | HexList``
            :param cidx_91: Cidx 91
            :type cidx_91: ``int | HexList``
            :param cidx_90: Cidx 90
            :type cidx_90: ``int | HexList``
            :param cidx_89: Cidx 89
            :type cidx_89: ``int | HexList``
            :param cidx_88: Cidx 88
            :type cidx_88: ``int | HexList``
            :param cidx_103: Cidx 103
            :type cidx_103: ``int | HexList``
            :param cidx_102: Cidx 102
            :type cidx_102: ``int | HexList``
            :param cidx_101: Cidx 101
            :type cidx_101: ``int | HexList``
            :param cidx_100: Cidx 100
            :type cidx_100: ``int | HexList``
            :param cidx_99: Cidx 99
            :type cidx_99: ``int | HexList``
            :param cidx_98: Cidx 98
            :type cidx_98: ``int | HexList``
            :param cidx_97: Cidx 97
            :type cidx_97: ``int | HexList``
            :param cidx_96: Cidx 96
            :type cidx_96: ``int | HexList``
            :param cidx_111: Cidx 111
            :type cidx_111: ``int | HexList``
            :param cidx_110: Cidx 110
            :type cidx_110: ``int | HexList``
            :param cidx_109: Cidx 109
            :type cidx_109: ``int | HexList``
            :param cidx_108: Cidx 108
            :type cidx_108: ``int | HexList``
            :param cidx_107: Cidx 107
            :type cidx_107: ``int | HexList``
            :param cidx_106: Cidx 106
            :type cidx_106: ``int | HexList``
            :param cidx_105: Cidx 105
            :type cidx_105: ``int | HexList``
            :param cidx_104: Cidx 104
            :type cidx_104: ``int | HexList``
            :param cidx_119: Cidx 119
            :type cidx_119: ``int | HexList``
            :param cidx_118: Cidx 118
            :type cidx_118: ``int | HexList``
            :param cidx_117: Cidx 117
            :type cidx_117: ``int | HexList``
            :param cidx_116: Cidx 116
            :type cidx_116: ``int | HexList``
            :param cidx_115: Cidx 115
            :type cidx_115: ``int | HexList``
            :param cidx_114: Cidx 114
            :type cidx_114: ``int | HexList``
            :param cidx_113: Cidx 113
            :type cidx_113: ``int | HexList``
            :param cidx_112: Cidx 112
            :type cidx_112: ``int | HexList``
            :param cidx_127: Cidx 127
            :type cidx_127: ``int | HexList``
            :param cidx_126: Cidx 126
            :type cidx_126: ``int | HexList``
            :param cidx_125: Cidx 125
            :type cidx_125: ``int | HexList``
            :param cidx_124: Cidx 124
            :type cidx_124: ``int | HexList``
            :param cidx_123: Cidx 123
            :type cidx_123: ``int | HexList``
            :param cidx_122: Cidx 122
            :type cidx_122: ``int | HexList``
            :param cidx_121: Cidx 121
            :type cidx_121: ``int | HexList``
            :param cidx_120: Cidx 120
            :type cidx_120: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.set_disabled_controls_cls(
                device_index=device_index, feature_index=feature_4523_index, cidx_7=cidx_7, cidx_6=cidx_6,
                cidx_5=cidx_5, cidx_4=cidx_4, cidx_3=cidx_3, cidx_2=cidx_2, cidx_1=cidx_1, cidx_0=cidx_0,
                cidx_15=cidx_15, cidx_14=cidx_14, cidx_13=cidx_13, cidx_12=cidx_12,
                cidx_11=cidx_11, cidx_10=cidx_10, cidx_9=cidx_9, cidx_8=cidx_8,
                cidx_23=cidx_23, cidx_22=cidx_22, cidx_21=cidx_21, cidx_20=cidx_20,
                cidx_19=cidx_19, cidx_18=cidx_18, cidx_17=cidx_17, cidx_16=cidx_16,
                cidx_31=cidx_31, cidx_30=cidx_30, cidx_29=cidx_29, cidx_28=cidx_28,
                cidx_27=cidx_27, cidx_26=cidx_26, cidx_25=cidx_25, cidx_24=cidx_24,
                cidx_39=cidx_39, cidx_38=cidx_38, cidx_37=cidx_37, cidx_36=cidx_36,
                cidx_35=cidx_35, cidx_34=cidx_34, cidx_33=cidx_33, cidx_32=cidx_32,
                cidx_47=cidx_47, cidx_46=cidx_46, cidx_45=cidx_45, cidx_44=cidx_44,
                cidx_43=cidx_43, cidx_42=cidx_42, cidx_41=cidx_41, cidx_40=cidx_40,
                cidx_55=cidx_55, cidx_54=cidx_54, cidx_53=cidx_53, cidx_52=cidx_52,
                cidx_51=cidx_51, cidx_50=cidx_50, cidx_49=cidx_49, cidx_48=cidx_48,
                cidx_63=cidx_63, cidx_62=cidx_62, cidx_61=cidx_61, cidx_60=cidx_60,
                cidx_59=cidx_59, cidx_58=cidx_58, cidx_57=cidx_57, cidx_56=cidx_56,
                cidx_71=cidx_71, cidx_70=cidx_70, cidx_69=cidx_69, cidx_68=cidx_68,
                cidx_67=cidx_67, cidx_66=cidx_66, cidx_65=cidx_65, cidx_64=cidx_64,
                cidx_79=cidx_79, cidx_78=cidx_78, cidx_77=cidx_77, cidx_76=cidx_76,
                cidx_75=cidx_75, cidx_74=cidx_74, cidx_73=cidx_73, cidx_72=cidx_72,
                cidx_87=cidx_87, cidx_86=cidx_86, cidx_85=cidx_85, cidx_84=cidx_84,
                cidx_83=cidx_83, cidx_82=cidx_82, cidx_81=cidx_81, cidx_80=cidx_80,
                cidx_95=cidx_95, cidx_94=cidx_94, cidx_93=cidx_93, cidx_92=cidx_92,
                cidx_91=cidx_91, cidx_90=cidx_90, cidx_89=cidx_89, cidx_88=cidx_88,
                cidx_103=cidx_103, cidx_102=cidx_102, cidx_101=cidx_101, cidx_100=cidx_100,
                cidx_99=cidx_99, cidx_98=cidx_98, cidx_97=cidx_97, cidx_96=cidx_96,
                cidx_111=cidx_111, cidx_110=cidx_110, cidx_109=cidx_109, cidx_108=cidx_108,
                cidx_107=cidx_107, cidx_106=cidx_106, cidx_105=cidx_105, cidx_104=cidx_104,
                cidx_119=cidx_119, cidx_118=cidx_118, cidx_117=cidx_117, cidx_116=cidx_116,
                cidx_115=cidx_115, cidx_114=cidx_114, cidx_113=cidx_113, cidx_112=cidx_112,
                cidx_127=cidx_127, cidx_126=cidx_126, cidx_125=cidx_125, cidx_124=cidx_124,
                cidx_123=cidx_123, cidx_122=cidx_122, cidx_121=cidx_121, cidx_120=cidx_120)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_disabled_controls_and_check_error

        @classmethod
        def get_game_mode(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetGameMode``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetGameModeResponse
            :rtype: ``GetGameModeResponse``
            """
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.get_game_mode_cls(
                device_index=device_index,
                feature_index=feature_4523_index)

            if software_id is not None:
                report.software_id = software_id
                # end if

            if padding is not None:
                report.padding = padding
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4523.get_game_mode_response_cls)
            return response
        # end def get_game_mode

        @classmethod
        def get_game_mode_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetGameMode``

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
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.get_game_mode_cls(
                device_index=device_index,
                feature_index=feature_4523_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_game_mode_and_check_error

        @classmethod
        def get_set_power_on_params(cls, test_case, poweron_game_mode_lock_valid, poweron_game_mode_valid,
                                    poweron_game_mode_lock, poweron_game_mode, device_index=None, port_index=None,
                                    software_id=None, padding=None):
            """
            Process ``GetSetPowerOnParams``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param poweron_game_mode_lock_valid: poweron game mode lock valid
            :type poweron_game_mode_lock_valid: ``int | HexList``
            :param poweron_game_mode_valid: poweron game mode valid
            :type poweron_game_mode_valid: ``int | HexList``
            :param poweron_game_mode_lock: poweron game mode lock
            :type poweron_game_mode_lock: ``int | HexList``
            :param poweron_game_mode: poweron game mode
            :type poweron_game_mode: ``int | HexList``
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
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.get_set_power_on_params_cls(
                device_index=device_index,
                feature_index=feature_4523_index,
                poweron_game_mode_lock_valid=poweron_game_mode_lock_valid,
                poweron_game_mode_valid=poweron_game_mode_valid,
                poweron_game_mode_lock=poweron_game_mode_lock,
                poweron_game_mode=poweron_game_mode)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4523.get_set_power_on_params_response_cls)
        # end def get_set_power_on_params

        @classmethod
        def get_set_power_on_params_and_check_error(
                cls, test_case, error_codes, poweron_game_mode_lock_valid, poweron_game_mode_valid,
                poweron_game_mode_lock, poweron_game_mode, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetSetPowerOnParams``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param poweron_game_mode_lock_valid: poweron game mode lock valid
            :type poweron_game_mode_lock_valid: ``int | HexList``
            :param poweron_game_mode_valid: poweron game mode valid
            :type poweron_game_mode_valid: ``int | HexList``
            :param poweron_game_mode_lock: poweron game mode lock
            :type poweron_game_mode_lock: ``int | HexList``
            :param poweron_game_mode: poweron game mode
            :type poweron_game_mode: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.get_set_power_on_params_cls(
                device_index=device_index,
                feature_index=feature_4523_index,
                poweron_game_mode_lock_valid=poweron_game_mode_lock_valid,
                poweron_game_mode_valid=poweron_game_mode_valid,
                poweron_game_mode_lock=poweron_game_mode_lock,
                poweron_game_mode=poweron_game_mode)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_set_power_on_params_and_check_error

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
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_4523_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4523.get_capabilities_response_cls)
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
            feature_4523_index, feature_4523, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4523.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_4523_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def game_mode_event(cls, test_case, timeout=2,
                            check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``GameModeEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: GameModeEvent
            :rtype: ``GameModeEvent``
            """
            _, feature_4523, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_4523.game_mode_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def game_mode_event
    # end class HIDppHelper

    @classmethod
    def convert_to_hexlist(cls, disabled_cidx_list):
        """
        Convert disabled cidx list to 0x4523 raw settings

        :param disabled_cidx_list: Disabled control id list
        :type disabled_cidx_list: ``List[int]``

        :return: The raw settings of disable keys
        :rtype: ``HexList``
        """
        raw_settings = [HexList('00') for _ in range(16)]
        for cidx in disabled_cidx_list:
            index = cidx // 8
            pos = cidx % 8
            raw_settings[index].setBit(pos=pos)
        # end for
        return HexList(raw_settings)
    # end def convert_to_hexlist
# end class DisableControlsByCIDXTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
