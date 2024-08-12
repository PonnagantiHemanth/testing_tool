#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.rgbeffectsutils
:brief: Helpers for ``RGBEffects`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import F_OK
from os import access
from os import makedirs
from os.path import join
from pickle import HIGHEST_PROTOCOL
from pickle import dump
from warnings import warn

# noinspection PyUnresolvedReferences
from pysetup import LIBS_PATH

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pyhid.hidpp.features.gaming.rgbeffects import EffectSyncEvent
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutCustomOnboardStoredEffect0
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutCustomOnboardStoredEffect1
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutCustomOnboardStoredEffect2
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutCustomOnboardStoredEffect3
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutCustomOnboardStoredEffect4
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutCustomOnboardStoredEffect5
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutCustomOnboardStoredEffect6
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutDeviceV0ToV1
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutDeviceV2ToV4
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutEffectGeneralInfo
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutRGBClusterV0
from pyhid.hidpp.features.gaming.rgbeffects import InfoAboutRGBClusterV1ToV4
from pyhid.hidpp.features.gaming.rgbeffects import ManageNvConfigResponseV0ToV2
from pyhid.hidpp.features.gaming.rgbeffects import ManageNvConfigResponseV3ToV4
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbLedBinInfoResponse
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbPowerModeConfigResponse
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbPowerModeResponse
from pyhid.hidpp.features.gaming.rgbeffects import ManageSWControlResponse
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsFactory
from pyhid.hidpp.features.gaming.rgbeffects import SetEffectSyncCorrectionResponse
from pyhid.hidpp.features.gaming.rgbeffects import SetMultiLedRgbClusterPatternResponse
from pyhid.hidpp.features.gaming.rgbeffects import SetRgbClusterEffectResponse
from pyhid.hidpp.features.gaming.rgbeffects import UserActivityEvent
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pyhid.hidpp.features.root import Root
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.config.ledlayout import GET_LED_LAYOUT_BY_ID
from pyraspi.services.kosmos.i2c.rgbparser import LedDataRgbParser
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RGBEffectsTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on ``RGBEffects`` feature
    """
    class RGBClusterId:
        """
        RGB cluster ID
        """
        PRIMARY = 0x00
        EDGE = 0x01
        MULTI_CLUSTER = 0xFF
    # end def class RGBClusterId

    class WavePattern:
        """
        Direction of Wave effect
        """
        DEFAULT = 0  # all play
        HORIZONTAL = 1
        VERTICAL = 2
        CENTER_OUT = 3
        INWARD = 4
        OUTWARD = 5
        REVERSE_HORIZONTAL = 6
        REVERSE_VERTICAL = 7
        CENTER_IN = 8
    # end def class WavePattern

    class NvCapabilities:
        """
        ID list for effect in NV capabilities
        """
        BOOT_UP_EFFECT = 0x0001
        DEMO = 0x0002
        USER_DEMO_MODE = 0x0004
        EVENTS_DISPLAY = 0x0008
        ACTIVE_DIMMING = 0x0010
        RAMP_DOWN_TO_OFF = 0x0020
        SHUTDOWN_EFFECT = 0x0040
    # end class NvCapabilities

    class GetOrSet:
        """
        Access mode of function with get or set
        """
        GET = 0x00
        SET = 0x01
    # end class GetOrSet

    class NvCapabilityState:
        """
        Non volatile capabilty possible state
        """
        NO_CHANGE = 0
        ENABLE = 1
        DISABLE = 2
        ENABLE_DURING_TIMEOUT = 4
    # end class NvCapabilityState

    class SlotInfoType:
        """
        Slot Info Type for custom onboard stored effect
        """
        SLOT_STATE = 0
        DEFAULTS = 1
        UUID_0_10 = 2
        UUID_11_16 = 3
        EFFECT_NAME_0_10 = 4
        EFFECT_NAME_11_21 = 5
        EFFECT_NAME_22_31 = 6
    # end class SlotInfoType

    class LedBinIndex:
        """
        LED Bin Index
        """
        BIN_VALUE_BRIGHTNESS = 0x00
        BIN_VALUE_COLOR = 0x01
        CALIBRATION_FACTORS = 0x02
        BRIGHTNESS = 0x03
        COLOR_METRIC_X = 0x04
        COLOR_METRIC_Y = 0x05
    # end class LedBinIndex

    class SwControlFlags:
        """
        SW Control Flags
        """
        ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS = 0x01
        ENABLE_SW_CONTROL_OF_POWER_MODES = 0x02
    # end class SwControlFlags

    class Persistence:
        """
        RGB settings persistence through power cycle
        """
        VOLATILE = 0x01  # RAM
        NON_VOLATILE = 0x02  # EEPROM
    # end class Persistence

    class EventNotificationFlags:
        ENABLE_EFFECTS_SYNC_NOTIFICATION = 0x01
        ENABLE_USER_ACTIVITY_TIMEOUT_NOTIFICATION = 0x02
        ENABLE_NO_USER_ACTIVITY_TIMEOUT_NOTIFICATION = 0x03
    # end class EventNotificationFlags

    class FixedRGBEffectMode:
        """
        Ramp up/down mode for fixed rgb effect
        """
        DEFAULT = 0
        RAMP_UP_DOWN = 1
        NO_EFFECT = 2
    # end class FixedRGBEffectMode

    class PulsingBreathingWaveformEffect:
        """
        Waveform for pulsing breathing rgb effect
        """
        DEFAULT = 0
        SINE = 1
        SQUARE = 2
        TRIANGLE = 3
        SAW_TOOTH = 4
        SHARK_FIN = 5
        EXPONENTIAL = 6
    # end class PulsingBreathingWaveformEffect

    class PowerMode:
        """
        RGB powermode to which the effect will be applied
        """
        FULL_POWER_MODE = 0
        POWER_SAVE_MODE = 1
    # end class PowerMode

    class GetInfoAboutDeviceResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutDevice`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutDevice`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, 0xFF),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, 0),
                "rgb_cluster_count": (cls.check_rgb_cluster_count, config.F_RgbClusterCount),
                "nv_capabilities": (cls.check_nv_capabilities, config.F_NvCapabilities),
                "ext_capabilities": (cls.check_ext_capabilities, config.F_ExtCapabilities),
                "reserved": (cls.check_reserved, 0),
                # V2
                'number_of_multi_cluster_effects': (cls.check_number_of_multi_cluster_effects,
                                                    config.F_NumberOfMultiClusterEffects)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutDevice to check
            :type response: ``InfoAboutDeviceV0ToV1`` or ``InfoAboutDeviceV2ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg=f"The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutDevice to check
            :type response: ``InfoAboutDeviceV0ToV1`` or ``InfoAboutDeviceV2ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg=f"The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_rgb_cluster_count(test_case, response, expected):
            """
            Check rgb_cluster_count field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutDevice to check
            :type response: ``InfoAboutDeviceV0ToV1`` or ``InfoAboutDeviceV2ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_count),
                msg=f"The rgb_cluster_count parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_count})")
        # end def check_rgb_cluster_count

        @staticmethod
        def check_nv_capabilities(test_case, response, expected):
            """
            Check nv_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutDevice to check
            :type response: ``InfoAboutDeviceV0ToV1`` or ``InfoAboutDeviceV2ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nv_capabilities),
                msg=f"The nv_capabilities parameter differs "
                    f"(expected:{expected}, obtained:{response.nv_capabilities})")
        # end def check_nv_capabilities

        @staticmethod
        def check_ext_capabilities(test_case, response, expected):
            """
            Check ext_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutDevice to check
            :type response: ``InfoAboutDeviceV0ToV1`` or ``InfoAboutDeviceV2ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.ext_capabilities),
                msg=f"The ext_capabilities parameter differs "
                    f"(expected:{expected}, obtained:{response.ext_capabilities})")
        # end def check_ext_capabilities

        @staticmethod
        def check_number_of_multi_cluster_effects(test_case, response, expected):
            """
            Check number_of_multi_cluster_effects field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutDevice to check
            :type response: ``InfoAboutDeviceV2ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.number_of_multi_cluster_effects),
                msg=f"The number_of_multi_cluster_effects parameter differs "
                    f"(expected:{expected}, obtained:{response.number_of_multi_cluster_effects})")
        # end def check_number_of_multi_cluster_effects

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutDevice to check
            :type response: ``InfoAboutDeviceV0ToV1`` or ``InfoAboutDeviceV2ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetInfoAboutDeviceResponseChecker

    class GetInfoAboutRGBClusterResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutRGBCluster`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutRGBCluster`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CLUSTER_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, int(config.F_ClusterIndex[0], 16)),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, 0),
                "location_effect": (cls.check_location_effect, int(config.F_LocationEffect[0], 16)),
                "effects_number": (cls.check_effects_number, int(config.F_EffectsNumber[0], 16)),
                "display_persistency_capabilities": (cls.check_display_persistency_capabilities,
                                                     int(config.F_DisplayPersistencyCapabilities[0], 16)),
                "reserved": (cls.check_reserved, 0),
                # V1+
                'effect_persistency_capabilities': (cls.check_effect_persistency_capabilities,
                                                    int(config.F_EffectPersistencyCapabilities[0], 16)),
                'multi_led_pattern_capabilities': (cls.check_multi_led_pattern_capabilities,
                                                   int(config.F_MultiLedPatternCapabilities[0], 16))
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV0`` or ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV0`` or ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_location_effect(test_case, response, expected):
            """
            Check location_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV0`` or ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.location_effect),
                msg="The location_effect parameter differs "
                    f"(expected:{expected}, obtained:{response.location_effect})")
        # end def check_location_effect

        @staticmethod
        def check_effects_number(test_case, response, expected):
            """
            Check effects_number field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV0`` or ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effects_number),
                msg="The effects_number parameter differs "
                    f"(expected:{expected}, obtained:{response.effects_number})")
        # end def check_effects_number

        @staticmethod
        def check_display_persistency_capabilities(test_case, response, expected):
            """
            Check display_persistency_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV0`` or ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.display_persistency_capabilities),
                msg="The display_persistency_capabilities parameter differs "
                    f"(expected:{expected}, obtained:{response.display_persistency_capabilities})")
        # end def check_display_persistency_capabilities

        @staticmethod
        def check_effect_persistency_capabilities(test_case, response, expected):
            """
            Check effect_persistency_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effect_persistency_capabilities),
                msg="The effect_persistency_capabilities parameter differs "
                    f"(expected:{expected}, obtained:{response.effect_persistency_capabilities})")
        # end def check_effect_persistency_capabilities

        @staticmethod
        def check_multi_led_pattern_capabilities(test_case, response, expected):
            """
            Check multi_led_pattern_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.multi_led_pattern_capabilities),
                msg="The multi_led_pattern_capabilities parameter differs "
                    f"(expected:{expected}, obtained:{response.multi_led_pattern_capabilities})")
        # end def check_multi_led_pattern_capabilities

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutRGBCluster to check
            :type response: ``InfoAboutRGBClusterV0`` or ``InfoAboutRGBClusterV1ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetInfoAboutRGBClusterResponseChecker

    class GetInfoAboutEffectGeneralInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutEffectGeneralInfo`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutEffectGeneralInfo`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.EFFECT_INFO_TABLE
            fields_to_check = {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, int(config.F_ClusterIndex[0], 16)),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, int(config.F_EffectIndex[0], 16)),
                "effect_id": (cls.check_effect_id, int(config.F_EffectId[0], 16)),
                "effect_capabilities": (cls.check_effect_capabilities, int(config.F_EffectCapabilities[0], 16)),
                "effect_period": (cls.check_effect_period, int(config.F_EffectPeriod[0], 16)),
                "reserved": (cls.check_reserved, 0)
            }

            return fields_to_check
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutEffectGeneralInfo to check
            :type response: ``InfoAboutEffectGeneralInfo``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutEffectGeneralInfo to check
            :type response: ``InfoAboutEffectGeneralInfo``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_effect_id(test_case, response, expected):
            """
            Check effect_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutEffectGeneralInfo to check
            :type response: ``InfoAboutEffectGeneralInfo``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effect_id),
                msg="The effect_id parameter differs "
                    f"(expected:{expected}, obtained:{response.effect_id})")
        # end def check_effect_id

        @staticmethod
        def check_effect_capabilities(test_case, response, expected):
            """
            Check effect_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutEffectGeneralInfo to check
            :type response: ``InfoAboutEffectGeneralInfo``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effect_capabilities),
                msg="The effect_capabilities parameter differs "
                    f"(expected:{expected}, obtained:{response.effect_capabilities})")
        # end def check_effect_capabilities

        @staticmethod
        def check_effect_period(test_case, response, expected):
            """
            Check effect_period field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutEffectGeneralInfo to check
            :type response: ``InfoAboutEffectGeneralInfo``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effect_period),
                msg="The effect_period parameter differs "
                    f"(expected:{expected}, obtained:{response.effect_period})")
        # end def check_effect_period

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutEffectGeneralInfo to check
            :type response: ``InfoAboutEffectGeneralInfo``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetInfoAboutEffect0ResponseChecker

    class GetInfoAboutCustomOnboardStoredEffect0ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutCustomOnboardStoredEffect0`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutCustomOnboardStoredEffect0`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            cluster_index, custom_onboard_stored_effect_index = \
                RGBEffectsTestUtils.get_effect_index_by_id(test_case,
                                                           RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(custom_onboard_stored_effect_index, None)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, cluster_index),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, custom_onboard_stored_effect_index),
                "type_of_info": (cls.check_type_of_info, 1),
                "slot": (cls.check_slot, 0),
                "slot_info_type": (cls.check_slot_info_type, RGBEffectsTestUtils.SlotInfoType.SLOT_STATE),
                "data_validity": (cls.check_data_validity, int(config.F_SlotState[0], 16)),
                "length_frames": (cls.check_length_frames,
                                  (int(config.F_SlotState[1], 16) << 8) + int(config.F_SlotState[2], 16))
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect0 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect0``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect0 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect0``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect0 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect0``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_slot(test_case, response, expected):
            """
            Check slot field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect0 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect0``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot),
                msg="The slot parameter differs "
                    f"(expected:{expected}, obtained:{response.slot})")
        # end def check_slot

        @staticmethod
        def check_slot_info_type(test_case, response, expected):
            """
            Check slot_info_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect0 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect0``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot_info_type),
                msg="The slot_info_type parameter differs "
                    f"(expected:{expected}, obtained:{response.slot_info_type})")
        # end def check_slot_info_type

        @staticmethod
        def check_data_validity(test_case, response, expected):
            """
            Check data_validity field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect0 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect0``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_validity),
                msg="The data_validity parameter differs "
                    f"(expected:{expected}, obtained:{response.data_validity})")
        # end def check_data_validity

        @staticmethod
        def check_length_frames(test_case, response, expected):
            """
            Check length_frames field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect0 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect0``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.length_frames),
                msg="The length_frames parameter differs "
                    f"(expected:{expected}, obtained:{response.length_frames})")
        # end def check_length_frames
    # end class GetInfoAboutCustomOnboardStoredEffect0ResponseChecker

    class GetInfoAboutCustomOnboardStoredEffect1ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutCustomOnboardStoredEffect1`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutCustomOnboardStoredEffect1`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            cluster_index, custom_onboard_stored_effect_index = \
                RGBEffectsTestUtils.get_effect_index_by_id(test_case,
                                                           RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(custom_onboard_stored_effect_index, None)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, cluster_index),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, custom_onboard_stored_effect_index),
                "type_of_info": (cls.check_type_of_info, 1),
                "slot": (cls.check_slot, 0),
                "slot_info_type": (cls.check_slot_info_type, RGBEffectsTestUtils.SlotInfoType.DEFAULTS),
                "init_frame": (cls.check_init_frame,
                               (int(config.F_SlotState[0], 16) << 8) + int(config.F_SlotState[1], 16)),
                "length_frames_to_play": (cls.check_length_frames_to_play,
                                          (int(config.F_SlotState[2], 16) << 8) + int(config.F_SlotState[3], 16)),
                "frame_period": (cls.check_frame_period,
                                 (int(config.F_SlotState[4], 16) << 8) + int(config.F_SlotState[5], 16)),
                "intensity": (cls.check_intensity, int(config.F_SlotState[6], 16))
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_slot(test_case, response, expected):
            """
            Check slot field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot),
                msg="The slot parameter differs "
                    f"(expected:{expected}, obtained:{response.slot})")
        # end def check_slot

        @staticmethod
        def check_slot_info_type(test_case, response, expected):
            """
            Check slot_info_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot_info_type),
                msg="The slot_info_type parameter differs "
                    f"(expected:{expected}, obtained:{response.slot_info_type})")
        # end def check_slot_info_type

        @staticmethod
        def check_init_frame(test_case, response, expected):
            """
            Check init_frame field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.init_frame),
                msg="The init_frame parameter differs "
                    f"(expected:{expected}, obtained:{response.init_frame})")
        # end def check_init_frame

        @staticmethod
        def check_length_frames_to_play(test_case, response, expected):
            """
            Check length_frames_to_play field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.length_frames_to_play),
                msg="The length_frames_to_play parameter differs "
                    f"(expected:{expected}, obtained:{response.length_frames_to_play})")
        # end def check_length_frames_to_play

        @staticmethod
        def check_frame_period(test_case, response, expected):
            """
            Check frame_period field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.frame_period),
                msg="The frame_period parameter differs "
                    f"(expected:{expected}, obtained:{response.frame_period})")
        # end def check_frame_period

        @staticmethod
        def check_intensity(test_case, response, expected):
            """
            Check intensity field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect1 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.intensity),
                msg="The intensity parameter differs "
                    f"(expected:{expected}, obtained:{response.intensity})")
        # end def check_intensity
    # end class GetInfoAboutCustomOnboardStoredEffect0ResponseChecker

    class GetInfoAboutCustomOnboardStoredEffect2ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutCustomOnboardStoredEffect2`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutCustomOnboardStoredEffect2`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            cluster_index, custom_onboard_stored_effect_index = \
                RGBEffectsTestUtils.get_effect_index_by_id(test_case,
                                                           RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(custom_onboard_stored_effect_index, None)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, cluster_index),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, custom_onboard_stored_effect_index),
                "type_of_info": (cls.check_type_of_info, 1),
                "slot": (cls.check_slot, 0),
                "slot_info_type": (cls.check_slot_info_type, RGBEffectsTestUtils.SlotInfoType.UUID_0_10),
                "uuid_0_10": (cls.check_uuid_0_10, config.F_UUID_0_10[0])
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect2 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect2``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect2 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect2``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect2 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect2``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_slot(test_case, response, expected):
            """
            Check slot field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect2 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect2``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot),
                msg="The slot parameter differs "
                    f"(expected:{expected}, obtained:{response.slot})")
        # end def check_slot

        @staticmethod
        def check_slot_info_type(test_case, response, expected):
            """
            Check slot_info_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect2 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect2``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot_info_type),
                msg="The slot_info_type parameter differs "
                    f"(expected:{expected}, obtained:{response.slot_info_type})")
        # end def check_slot_info_type

        @staticmethod
        def check_uuid_0_10(test_case, response, expected):
            """
            Check uuid_0_10 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect2 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect2``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.uuid_0_10),
                msg="The uuid_0_10 parameter differs "
                    f"(expected:{expected}, obtained:{response.uuid_0_10})")
        # end def check_uuid_0_10
    # end class GetInfoAboutCustomOnboardStoredEffect2ResponseChecker

    class GetInfoAboutCustomOnboardStoredEffect3ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutCustomOnboardStoredEffect3`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutCustomOnboardStoredEffect3`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            cluster_index, custom_onboard_stored_effect_index = \
                RGBEffectsTestUtils.get_effect_index_by_id(test_case,
                                                           RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(custom_onboard_stored_effect_index, None)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, cluster_index),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, custom_onboard_stored_effect_index),
                "type_of_info": (cls.check_type_of_info, 1),
                "slot": (cls.check_slot, 0),
                "slot_info_type": (cls.check_slot_info_type, RGBEffectsTestUtils.SlotInfoType.UUID_11_16),
                "uuid_11_16": (cls.check_uuid_11_16, config.F_UUID_11_16[0]),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect3 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect3 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect3 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_slot(test_case, response, expected):
            """
            Check slot field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect3 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot),
                msg="The slot parameter differs "
                    f"(expected:{expected}, obtained:{response.slot})")
        # end def check_slot

        @staticmethod
        def check_slot_info_type(test_case, response, expected):
            """
            Check slot_info_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect3 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot_info_type),
                msg="The slot_info_type parameter differs "
                    f"(expected:{expected}, obtained:{response.slot_info_type})")
        # end def check_slot_info_type

        @staticmethod
        def check_uuid_11_16(test_case, response, expected):
            """
            Check uuid_11_16 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect3 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.uuid_11_16),
                msg="The uuid_11_16 parameter differs "
                    f"(expected:{expected}, obtained:{response.uuid_11_16})")
        # end def check_uuid_11_16

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect3 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetInfoAboutCustomOnboardStoredEffect3ResponseChecker

    class GetInfoAboutCustomOnboardStoredEffect4ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutCustomOnboardStoredEffect4`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutCustomOnboardStoredEffect4`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            cluster_index, custom_onboard_stored_effect_index = \
                RGBEffectsTestUtils.get_effect_index_by_id(test_case,
                                                           RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(custom_onboard_stored_effect_index, None)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, cluster_index),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, custom_onboard_stored_effect_index),
                "type_of_info": (cls.check_type_of_info, 1),
                "slot": (cls.check_slot, 0),
                "slot_info_type": (cls.check_slot_info_type, RGBEffectsTestUtils.SlotInfoType.EFFECT_NAME_0_10),
                "effect_name_0_10": (cls.check_effect_name_0_10, config.F_effect_name_0_10[0])
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect4 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect4 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect4 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_slot(test_case, response, expected):
            """
            Check slot field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect4 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot),
                msg="The slot parameter differs "
                    f"(expected:{expected}, obtained:{response.slot})")
        # end def check_slot

        @staticmethod
        def check_slot_info_type(test_case, response, expected):
            """
            Check slot_info_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect4 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot_info_type),
                msg="The slot_info_type parameter differs "
                    f"(expected:{expected}, obtained:{response.slot_info_type})")
        # end def check_slot_info_type

        @staticmethod
        def check_effect_name_0_10(test_case, response, expected):
            """
            Check effect_name_0_10 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect4 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effect_name_0_10),
                msg="The effect_name_0_10 parameter differs "
                    f"(expected:{expected}, obtained:{response.effect_name_0_10})")
        # end def check_effect_name_0_10
    # end class GetInfoAboutCustomOnboardStoredEffect4ResponseChecker

    class GetInfoAboutCustomOnboardStoredEffect5ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutCustomOnboardStoredEffect5`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutCustomOnboardStoredEffect5`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            cluster_index, custom_onboard_stored_effect_index = \
                RGBEffectsTestUtils.get_effect_index_by_id(test_case,
                                                           RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(custom_onboard_stored_effect_index, None)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, cluster_index),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, custom_onboard_stored_effect_index),
                "type_of_info": (cls.check_type_of_info, 1),
                "slot": (cls.check_slot, 0),
                "slot_info_type": (cls.check_slot_info_type, RGBEffectsTestUtils.SlotInfoType.EFFECT_NAME_11_21),
                "effect_name_11_21": (cls.check_effect_name_11_21, config.F_effect_name_11_21[0])
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect5 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect5 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect5 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_slot(test_case, response, expected):
            """
            Check slot field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect5 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot),
                msg="The slot parameter differs "
                    f"(expected:{expected}, obtained:{response.slot})")
        # end def check_slot

        @staticmethod
        def check_slot_info_type(test_case, response, expected):
            """
            Check slot_info_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect5 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot_info_type),
                msg="The slot_info_type parameter differs "
                    f"(expected:{expected}, obtained:{response.slot_info_type})")
        # end def check_slot_info_type

        @staticmethod
        def check_effect_name_11_21(test_case, response, expected):
            """
            Check effect_name_11_21 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect5 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effect_name_11_21),
                msg="The effect_name_11_21 parameter differs "
                    f"(expected:{expected}, obtained:{response.effect_name_11_21})")
        # end def check_effect_name_11_21
    # end class GetInfoAboutCustomOnboardStoredEffect5ResponseChecker

    class GetInfoAboutCustomOnboardStoredEffect6ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``InfoAboutCustomOnboardStoredEffect6`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``InfoAboutCustomOnboardStoredEffect6`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            cluster_index, custom_onboard_stored_effect_index = \
                RGBEffectsTestUtils.get_effect_index_by_id(test_case,
                                                           RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(custom_onboard_stored_effect_index, None)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE
            return {
                "rgb_cluster_index": (cls.check_rgb_cluster_index, cluster_index),
                "rgb_cluster_effect_index": (cls.check_rgb_cluster_effect_index, custom_onboard_stored_effect_index),
                "type_of_info": (cls.check_type_of_info, 1),
                "slot": (cls.check_slot, 0),
                "slot_info_type": (cls.check_slot_info_type, RGBEffectsTestUtils.SlotInfoType.EFFECT_NAME_22_31),
                "effect_name_22_31": (cls.check_effect_name_22_31, config.F_EffectName_22_31[0]),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect6 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_rgb_cluster_effect_index(test_case, response, expected):
            """
            Check rgb_cluster_effect_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect6 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_effect_index),
                msg="The rgb_cluster_effect_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_effect_index})")
        # end def check_rgb_cluster_effect_index

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect6 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_slot(test_case, response, expected):
            """
            Check slot field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect6 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot),
                msg="The slot parameter differs "
                    f"(expected:{expected}, obtained:{response.slot})")
        # end def check_slot

        @staticmethod
        def check_slot_info_type(test_case, response, expected):
            """
            Check slot_info_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect6 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.slot_info_type),
                msg="The slot_info_type parameter differs "
                    f"(expected:{expected}, obtained:{response.slot_info_type})")
        # end def check_slot_info_type

        @staticmethod
        def check_effect_name_22_31(test_case, response, expected):
            """
            Check effect_name_22_31 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect6 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.effect_name_22_31),
                msg="The effect_name_22_31 parameter differs "
                    f"(expected:{expected}, obtained:{response.effect_name_22_31})")
        # end def check_effect_name_22_31

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: InfoAboutCustomOnboardStoredEffect6 to check
            :type response: ``InfoAboutCustomOnboardStoredEffect6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetInfoAboutCustomOnboardStoredEffect6ResponseChecker

    class ManageNvConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``ManageNvConfig`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ManageNvConfigResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            feature_8071_index, feature_8071, device_index, _ = \
                RGBEffectsTestUtils.HIDppHelper.get_parameters(test_case)

            config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.NV_CAPABILITY_INFO_TABLE
            fields_to_check = {
                "get_or_set": (cls.check_get_or_set, 0),
                "nv_capabilities": (cls.check_nv_capabilities, int(config.F_NvCapabilities[0], 16)),
                "capability_state": (cls.check_capability_state, int(config.F_CapabilityState[0], 16)),
                "param_1": (cls.check_param_1, int(config.F_Param1[0], 16)),
                "param_2": (cls.check_param_2, int(config.F_Param2[0], 16)),
                "reserved": (cls.check_reserved, 0)
            }

            if feature_8071.VERSION == 3:
                fields_to_check = {
                    **fields_to_check,
                    "param_3": (cls.check_param_3, int(config.F_Param3[0], 16)),
                    "param_4": (cls.check_param_4, int(config.F_Param4[0], 16)),
                    "param_5": (cls.check_param_5, int(config.F_Param5[0], 16)),
                    "param_6": (cls.check_param_6, int(config.F_Param6[0], 16)),
                }
            # end if

            return fields_to_check
        # end def get_default_check_map

        @staticmethod
        def check_get_or_set(test_case, response, expected):
            """
            Check get_or_set field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV0ToV2`` or ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.get_or_set),
                msg="The get_or_set parameter differs "
                    f"(expected:{expected}, obtained:{response.get_or_set})")
        # end def check_get_or_set

        @staticmethod
        def check_nv_capabilities(test_case, response, expected):
            """
            Check nv_capabilities field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV0ToV2`` or ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nv_capabilities),
                msg="The nv_capabilities parameter differs "
                    f"(expected:{expected}, obtained:{response.nv_capabilities})")
        # end def check_nv_capabilities

        @staticmethod
        def check_capability_state(test_case, response, expected):
            """
            Check capability_state field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV0ToV2`` or ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.capability_state),
                msg="The capability_state parameter differs "
                    f"(expected:{expected}, obtained:{response.capability_state})")
        # end def check_capability_state

        @staticmethod
        def check_param_1(test_case, response, expected):
            """
            Check param_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV0ToV2`` or ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_1),
                msg="The param_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_1})")
        # end def check_param_1

        @staticmethod
        def check_param_2(test_case, response, expected):
            """
            Check param_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV0ToV2`` or ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_2),
                msg="The param_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_2})")
        # end def check_param_2

        @staticmethod
        def check_param_3(test_case, response, expected):
            """
            Check param_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_3),
                msg="The param_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_3})")
        # end def check_param_3

        @staticmethod
        def check_param_4(test_case, response, expected):
            """
            Check param_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_4),
                msg="The param_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_4})")
        # end def check_param_4

        @staticmethod
        def check_param_5(test_case, response, expected):
            """
            Check param_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_5),
                msg="The param_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_5})")
        # end def check_param_5

        @staticmethod
        def check_param_6(test_case, response, expected):
            """
            Check param_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_6),
                msg="The param_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_6})")
        # end def check_param_6

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageNvConfigResponse to check
            :type response: ``ManageNvConfigResponseV0ToV2`` or ``ManageNvConfigResponseV3ToV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class ManageNvConfigResponseChecker

    class ManageRgbLedBinInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``ManageRgbLedBinInfo`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ManageRgbLedBinInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "get_or_set": (cls.check_get_or_set, 0),
                "rgb_cluster_index": (cls.check_rgb_cluster_index, 0),
                "led_bin_index": (cls.check_led_bin_index, 0),
                "param_1": (cls.check_param_1, 0),
                "param_2": (cls.check_param_2, 0),
                "param_3": (cls.check_param_3, 0),
                "param_4": (cls.check_param_4, 0),
                "param_5": (cls.check_param_5, 0),
                "param_6": (cls.check_param_6, 0),
                "param_7": (cls.check_param_7, 0),
                "param_8": (cls.check_param_8, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_get_or_set(test_case, response, expected):
            """
            Check get_or_set field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.get_or_set),
                msg="The get_or_set parameter differs "
                    f"(expected:{expected}, obtained:{response.get_or_set})")
        # end def check_get_or_set

        @staticmethod
        def check_rgb_cluster_index(test_case, response, expected):
            """
            Check rgb_cluster_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_cluster_index),
                msg="The rgb_cluster_index parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_cluster_index})")
        # end def check_rgb_cluster_index

        @staticmethod
        def check_led_bin_index(test_case, response, expected):
            """
            Check led_bin_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.led_bin_index),
                msg="The led_bin_index parameter differs "
                    f"(expected:{expected}, obtained:{response.led_bin_index})")
        # end def check_led_bin_index

        @staticmethod
        def check_param_1(test_case, response, expected):
            """
            Check param_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_1),
                msg="The param_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_1})")
        # end def check_param_1

        @staticmethod
        def check_param_2(test_case, response, expected):
            """
            Check param_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_2),
                msg="The param_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_2})")
        # end def check_param_2

        @staticmethod
        def check_param_3(test_case, response, expected):
            """
            Check param_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_3),
                msg="The param_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_3})")
        # end def check_param_3

        @staticmethod
        def check_param_4(test_case, response, expected):
            """
            Check param_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_4),
                msg="The param_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_4})")
        # end def check_param_4

        @staticmethod
        def check_param_5(test_case, response, expected):
            """
            Check param_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_5),
                msg="The param_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_5})")
        # end def check_param_5

        @staticmethod
        def check_param_6(test_case, response, expected):
            """
            Check param_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_6),
                msg="The param_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_6})")
        # end def check_param_6

        @staticmethod
        def check_param_7(test_case, response, expected):
            """
            Check param_7 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_7),
                msg="The param_7 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_7})")
        # end def check_param_7

        @staticmethod
        def check_param_8(test_case, response, expected):
            """
            Check param_8 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param_8),
                msg="The param_8 parameter differs "
                    f"(expected:{expected}, obtained:{response.param_8})")
        # end def check_param_8

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbLedBinInfoResponse to check
            :type response: ``ManageRgbLedBinInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class ManageRgbLedBinInfoResponseChecker

    class ManageSWControlResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``ManageSWControl`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ManageSWControlResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "get_or_set": (cls.check_get_or_set, 0),
                "sw_control_flags": (cls.check_sw_control_flags, 0),
                "events_notification_flags": (cls.check_events_notification_flags, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_get_or_set(test_case, response, expected):
            """
            Check get_or_set field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageSWControlResponse to check
            :type response: ``ManageSWControlResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.get_or_set),
                msg="The get_or_set parameter differs "
                    f"(expected:{expected}, obtained:{response.get_or_set})")
        # end def check_get_or_set

        @staticmethod
        def check_sw_control_flags(test_case, response, expected):
            """
            Check sw_control_flags field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageSWControlResponse to check
            :type response: ``ManageSWControlResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sw_control_flags),
                msg="The sw_control_flags parameter differs "
                    f"(expected:{expected}, obtained:{response.sw_control_flags})")
        # end def check_sw_control_flags

        @staticmethod
        def check_events_notification_flags(test_case, response, expected):
            """
            Check events_notification_flags field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageSWControlResponse to check
            :type response: ``ManageSWControlResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.events_notification_flags),
                msg="The events_notification_flags parameter differs "
                    f"(expected:{expected}, obtained:{response.events_notification_flags})")
        # end def check_events_notification_flags

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageSWControlResponse to check
            :type response: ``ManageSWControlResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class ManageSWControlResponseChecker

    class ManageRgbPowerModeConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``ManageRgbPowerModeConfig`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ManageRgbPowerModeConfigResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "get_or_set": (cls.check_get_or_set, 0),
                "rgb_power_mode_flags": (cls.check_rgb_power_mode_flags, 0),
                "rgb_no_act_timeout_to_save": (cls.check_rgb_no_act_timeout_to_save, 0),
                "rgb_no_act_timeout_to_off": (cls.check_rgb_no_act_timeout_to_off, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_get_or_set(test_case, response, expected):
            """
            Check get_or_set field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeConfigResponse to check
            :type response: ``ManageRgbPowerModeConfigResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.get_or_set),
                msg="The get_or_set parameter differs "
                    f"(expected:{expected}, obtained:{response.get_or_set})")
        # end def check_get_or_set

        @staticmethod
        def check_rgb_power_mode_flags(test_case, response, expected):
            """
            Check rgb_power_mode_flags field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeConfigResponse to check
            :type response: ``ManageRgbPowerModeConfigResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """

            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_power_mode_flags),
                msg="The rgb_power_mode_flags parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_power_mode_flags})")
        # end def check_rgb_power_mode_flags

        @staticmethod
        def check_rgb_no_act_timeout_to_save(test_case, response, expected):
            """
            Check rgb_no_act_timeout_to_save field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeConfigResponse to check
            :type response: ``ManageRgbPowerModeConfigResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_no_act_timeout_to_save),
                msg="The rgb_no_act_timeout_to_save parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_no_act_timeout_to_save})")
        # end def check_rgb_no_act_timeout_to_save

        @staticmethod
        def check_rgb_no_act_timeout_to_off(test_case, response, expected):
            """
            Check rgb_no_act_timeout_to_off field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeConfigResponse to check
            :type response: ``ManageRgbPowerModeConfigResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_no_act_timeout_to_off),
                msg="The rgb_no_act_timeout_to_off parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_no_act_timeout_to_off})")
        # end def check_rgb_no_act_timeout_to_off

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeConfigResponse to check
            :type response: ``ManageRgbPowerModeConfigResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class ManageRgbPowerModeConfigResponseChecker

    class ManageRgbPowerModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``ManageRgbPowerMode`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ManageRgbPowerModeResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "get_or_set": (cls.check_get_or_set, 0),
                "rgb_power_mode": (cls.check_rgb_power_mode, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_get_or_set(test_case, response, expected):
            """
            Check get_or_set field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeResponse to check
            :type response: ``ManageRgbPowerModeResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.get_or_set),
                msg="The get_or_set parameter differs "
                    f"(expected:{expected}, obtained:{response.get_or_set})")
        # end def check_get_or_set

        @staticmethod
        def check_rgb_power_mode(test_case, response, expected):
            """
            Check rgb_power_mode field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeResponse to check
            :type response: ``ManageRgbPowerModeResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_power_mode),
                msg="The rgb_power_mode parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_power_mode})")
        # end def check_rgb_power_mode

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ManageRgbPowerModeResponse to check
            :type response: ``ManageRgbPowerModeResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class ManageRgbPowerModeResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=RGBEffects.FEATURE_ID, factory=RGBEffectsFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_info_about_device(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetInfoAboutDevice``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: InfoAboutDeviceResponse
            :rtype: ``InfoAboutDeviceV0ToV1`` or ``InfoAboutDeviceV2ToV4``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            if feature_8071.VERSION == 0:
                report = feature_8071.get_info_cls(
                    device_index, feature_8071_index,
                    rgb_cluster_index=0xFF, rgb_cluster_effect_index=0xFF)
            else:
                report = feature_8071.get_info_cls(
                    device_index, feature_8071_index,
                    rgb_cluster_index=0xFF, rgb_cluster_effect_index=0xFF, type_of_info=0)
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.get_info_response_cls)

            return InfoAboutDeviceV0ToV1.fromHexList(HexList(response)) if feature_8071.VERSION <= 1 else \
                InfoAboutDeviceV2ToV4.fromHexList(HexList(response))
        # end def get_info_about_device

        @classmethod
        def get_info_about_rgb_cluster(cls, test_case, rgb_cluster_index, device_index=None, port_index=None):
            """
            Process ``GetInfoAboutRGBCluster``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_cluster_index: RGB cluster index
            :type rgb_cluster_index: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: InfoAboutRGBCluster
            :rtype: ``InfoAboutRGBClusterV0`` or ``InfoAboutRGBClusterV1ToV4``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            if feature_8071.VERSION == 0:
                report = feature_8071.get_info_cls(
                    device_index, feature_8071_index,
                    rgb_cluster_index=rgb_cluster_index, rgb_cluster_effect_index=0xFF)
            else:
                report = feature_8071.get_info_cls(
                    device_index, feature_8071_index,
                    rgb_cluster_index=rgb_cluster_index, rgb_cluster_effect_index=0xFF, type_of_info=0)
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.get_info_response_cls)

            return InfoAboutRGBClusterV0.fromHexList(HexList(response)) if feature_8071.VERSION == 0 else \
                InfoAboutRGBClusterV1ToV4.fromHexList(HexList(response))
        # end def get_info_about_rgb_cluster

        @classmethod
        def get_info_about_effect_general_info(cls, test_case, rgb_cluster_index, rgb_cluster_effect_index,
                                               device_index=None, port_index=None):
            """
            Process ``GetInfoAboutEffectGeneralInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_cluster_index: RGB cluster index
            :type rgb_cluster_index: ``int``
            :param rgb_cluster_effect_index: RGB cluster effect index
            :type rgb_cluster_effect_index: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetInfoAboutEffectGeneralInfoResponse
            :rtype: ``InfoAboutEffectGeneralInfo``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.get_info_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=HexList(rgb_cluster_index),
                rgb_cluster_effect_index=HexList(rgb_cluster_effect_index),
                type_of_info=0)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.get_info_response_cls)

            return InfoAboutEffectGeneralInfo.fromHexList(HexList(response))
        # end def get_info_about_effect_general_info

        @classmethod
        def get_info_about_custom_onboard_stored_effect(cls, test_case, slot, slot_info_type,
                                                        device_index=None, port_index=None):
            """
            Process ``GetInfo`` for Custom Onboard Stored Effect

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param slot: Slot
            :type slot: ``int``
            :param slot_info_type: Slot info type
            :type slot_info_type: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetInfoAboutCustomOnboardStoredEffectResponse
            :rtype: ``InfoAboutCustomOnboardStoredEffect0`` or ``InfoAboutCustomOnboardStoredEffect1`` or
                    ``InfoAboutCustomOnboardStoredEffect2`` or ``InfoAboutCustomOnboardStoredEffect3`` or
                    ``InfoAboutCustomOnboardStoredEffect4`` or ``InfoAboutCustomOnboardStoredEffect5`` or
                    ``InfoAboutCustomOnboardStoredEffect6``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            test_case.assertGreater(feature_8071.VERSION, 0)

            cluster_index, effect_index = RGBEffectsTestUtils.get_effect_index_by_id(
                test_case, RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(effect_index, None)

            report = feature_8071.get_info_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=0xFF,
                rgb_cluster_effect_index=effect_index,
                type_of_info=1, param_1=slot, param_2=slot_info_type)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.get_info_response_cls)

            if slot_info_type == RGBEffectsTestUtils.SlotInfoType.SLOT_STATE:
                response = InfoAboutCustomOnboardStoredEffect0.fromHexList(HexList(response))
            elif slot_info_type == RGBEffectsTestUtils.SlotInfoType.DEFAULTS:
                response = InfoAboutCustomOnboardStoredEffect1.fromHexList(HexList(response))
            elif slot_info_type == RGBEffectsTestUtils.SlotInfoType.UUID_0_10:
                response = InfoAboutCustomOnboardStoredEffect2.fromHexList(HexList(response))
            elif slot_info_type == RGBEffectsTestUtils.SlotInfoType.UUID_11_16:
                response = InfoAboutCustomOnboardStoredEffect3.fromHexList(HexList(response))
            elif slot_info_type == RGBEffectsTestUtils.SlotInfoType.EFFECT_NAME_0_10:
                response = InfoAboutCustomOnboardStoredEffect4.fromHexList(HexList(response))
            elif slot_info_type == RGBEffectsTestUtils.SlotInfoType.EFFECT_NAME_11_21:
                response = InfoAboutCustomOnboardStoredEffect5.fromHexList(HexList(response))
            elif slot_info_type == RGBEffectsTestUtils.SlotInfoType.EFFECT_NAME_22_31:
                response = InfoAboutCustomOnboardStoredEffect6.fromHexList(HexList(response))
            # end if

            return response
        # end def get_info_about_custom_onboard_stored_effect

        @classmethod
        def set_disabled_effect(cls, test_case, cluster_index, persistence=0, power_mode=0, device_index=None,
                                port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.\
                get_effect_index_by_effect_id_and_cluster_id(test_case=test_case, cluster_index=cluster_index,
                                                             effect_id=RGBEffects.RGBEffectID.DISABLED)
            test_case.assertNotNone(effect_index, msg="No effect_index found for Disabled RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_disabled_effect

        @classmethod
        def set_fixed_effect(cls, test_case, cluster_index, red, green, blue, mode=0, persistence=0, power_mode=0,
                             device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param red: Red color value
            :type red: ``int`` or ``HexList``
            :param green: Green color value
            :type green: ``int`` or ``HexList``
            :param blue: Blue color value
            :type blue: ``int`` or ``HexList``
            :param mode: The possible values are default=0, ramp up.down=1, no effect=2 - OPTIONAL
            :type mode: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.\
                get_effect_index_by_effect_id_and_cluster_id(test_case=test_case, cluster_index=cluster_index,
                                                             effect_id=RGBEffects.RGBEffectID.FIXED)
            test_case.assertNotNone(effect_index, msg="No effect_index found for Fixed RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_1=red,
                param_2=green,
                param_3=blue,
                param_4=mode,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_fixed_effect

        @classmethod
        def set_pulsing_breathing_effect(cls, test_case, cluster_index, red, green, blue, period, persistence=0,
                                         power_mode=0, device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param red: Red color value
            :type red: ``int`` or ``HexList``
            :param green: Green color value
            :type green: ``int`` or ``HexList``
            :param blue: Blue color value
            :type blue: ``int`` or ``HexList``
            :param period: The effect period in ms
            :type period: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.get_effect_index_by_effect_id_and_cluster_id(
                test_case=test_case, cluster_index=cluster_index,
                effect_id=RGBEffects.RGBEffectID.PULSING_BREATHING)

            test_case.assertNotNone(effect_index, msg="No effect_index found for Pulsing/breathing RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_1=red,
                param_2=green,
                param_3=blue,
                param_4=period,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_pulsing_breathing_effect

        @classmethod
        def set_cycling_effect(cls, test_case, cluster_index, period_msb, period_lsb, intensity, persistence=0,
                               power_mode=0, device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param period_msb: The effect period in ms
            :type period_msb: ``int`` or ``HexList``
            :param period_lsb: The effect period in ms
            :type period_lsb: ``int`` or ``HexList``
            :param intensity: Intensity in range 1..100, default = 100, 0 or > 100 = default
            :type intensity: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.\
                get_effect_index_by_effect_id_and_cluster_id(test_case=test_case, cluster_index=cluster_index,
                                                             effect_id=RGBEffects.RGBEffectID.CYCLING)

            test_case.assertNotNone(effect_index, msg="No effect_index found for Cycling RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_6=period_msb,
                param_7=period_lsb,
                param_8=intensity,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_cycling_effect

        @classmethod
        def set_pulsing_breathing_waveform_effect(cls, test_case, cluster_index, red, green, blue, period_msb,
                                                  period_lsb, waveform, intensity, persistence=0, power_mode=0,
                                                  device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param red: Red color value
            :type red: ``int`` or ``HexList``
            :param green: Green color value
            :type green: ``int`` or ``HexList``
            :param blue: Blue color value
            :type blue: ``int`` or ``HexList``
            :param period_msb: The effect period in ms
            :type period_msb: ``int`` or ``HexList``
            :param period_lsb: The effect period in ms
            :type period_lsb: ``int`` or ``HexList``
            :param waveform: The waveform of the pulsing effect (default, sine, square, triangle, ...)
            :type waveform: ``int`` or ``HexList``
            :param intensity: Intensity in range 1..100, default = 100, 0 or > 100 = default
            :type intensity: ``int`` or ``HexList``
            :param cluster_index: Cluster index
            :type cluster_index: ``int``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.get_effect_index_by_effect_id_and_cluster_id(
                test_case=test_case, cluster_index=cluster_index,
                effect_id=RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)

            test_case.assertNotNone(effect_index, msg="No effect_index found for Pulsing/Breathing RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_1=red,
                param_2=green,
                param_3=blue,
                param_4=period_msb,
                param_5=period_lsb,
                param_6=waveform,
                param_7=intensity,
                power_mode=power_mode,
                persistence=persistence)

            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_pulsing_breathing_waveform_effect

        @classmethod
        def set_color_cycling_configurable_s_effect(cls, test_case, cluster_index, saturation, period_msb, period_lsb,
                                                    intensity, persistence=0, power_mode=0, device_index=None,
                                                    port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param saturation: saturation HSV value
            :type saturation: ``int`` or ``HexList``
            :param period_msb: The effect period in ms
            :type period_msb: ``int`` or ``HexList``
            :param period_lsb: The effect period in ms
            :type period_lsb: ``int`` or ``HexList``
            :param intensity: Intensity in range 1..100, default = 100, 0 or > 100 = default
            :type intensity: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.get_effect_index_by_effect_id_and_cluster_id(
                test_case=test_case, cluster_index=cluster_index,
                effect_id=RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)

            test_case.assertNotNone(effect_index, msg="No effect_index found for Color cycling configurable saturation "
                                                      "RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_2=saturation,
                param_7=period_msb,
                param_8=period_lsb,
                param_9=intensity,
                power_mode=power_mode,
                persistence=persistence)

            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_color_cycling_configurable_s_effect

        @classmethod
        def set_color_wave_configurable_s_effect(cls, test_case, cluster_index, saturation, period_msb, period_lsb,
                                                 intensity, pattern, persistence=0, power_mode=0, device_index=None,
                                                 port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param saturation: saturation HSV value
            :type saturation: ``int`` or ``HexList``
            :param period_msb: The effect period in ms
            :type period_msb: ``int`` or ``HexList``
            :param period_lsb: The effect period in ms
            :type period_lsb: ``int`` or ``HexList``
            :param intensity: Intensity in range 1..100, default = 100, 0 or > 100 = default
            :type intensity: ``int`` or ``HexList``
            :param pattern: Direction of the Wave
            :type pattern: ``int``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.get_effect_index_by_effect_id_and_cluster_id(
                test_case=test_case, cluster_index=cluster_index,
                effect_id=RGBEffects.RGBEffectID.COLOR_WAVE_CONFIGURABLE_S)

            test_case.assertNotNone(effect_index, msg="No effect_index found for Color wave configurable saturation "
                                                      "RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_2=saturation,
                param_7=period_msb,
                param_8=period_lsb,
                param_9=intensity,
                param_10=pattern,
                power_mode=power_mode,
                persistence=persistence)

            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_color_wave_configurable_s_effect

        @classmethod
        def set_color_wave_effect(cls, test_case, cluster_index, red_start, green_start, blue_start, red_stop,
                                  green_stop, blue_stop, period=0, display_mode=0, intensity=0, persistence=0,
                                  power_mode=0, device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param red_start: The red value in starting
            :type red_start: ``int`` or ``HexList``
            :param green_start: The green value in starting
            :type green_start: ``int`` or ``HexList``
            :param blue_start: The blue value in starting
            :type blue_start: ``int`` or ``HexList``
            :param red_stop: The red value in stopping
            :type red_stop: ``int`` or ``HexList``
            :param green_stop: The green value in stopping
            :type green_stop: ``int`` or ``HexList``
            :param blue_stop: The blue value in stopping
            :type blue_stop: ``int`` or ``HexList``
            :param period: The effect period in ms - OPTIONAL
            :type period: ``int`` or ``HexList``
            :param display_mode: The display mode - OPTIONAL
            :type display_mode: ``int`` or ``HexList``
            :param intensity: Intensity in range 1..100, default = 100, 0 or > 100 = default - OPTIONAL
            :type intensity: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.\
                get_effect_index_by_effect_id_and_cluster_id(test_case=test_case, cluster_index=cluster_index,
                                                             effect_id=RGBEffects.RGBEffectID.COLOR_WAVE)

            test_case.assertNotNone(effect_index, msg="No effect_index found for Color wave RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_1=red_start,
                param_2=green_start,
                param_3=blue_start,
                param_4=red_stop,
                param_5=green_stop,
                param_6=blue_stop,
                param_7=period & 0xFF,
                param_8=display_mode,
                param_9=intensity,
                param_10=(period & 0xFF00) >> 8,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_color_wave_effect

        @classmethod
        def set_smooth_star_breathing_effect(cls, test_case, cluster_index, red_first_choice=0, green_first_choice=0,
                                             blue_first_choice=0, red_second_choice=0, green_second_choice=0,
                                             blue_second_choice=0, period_msb=0, period_lsb=0, intensity=0,
                                             persistence=0, power_mode=0, device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param red_first_choice: Red color value - OPTIONAL
            :type red_first_choice: ``int`` or ``HexList``
            :param green_first_choice: Green color value - OPTIONAL
            :type green_first_choice: ``int`` or ``HexList``
            :param blue_first_choice: Blue color value - OPTIONAL
            :type blue_first_choice: ``int`` or ``HexList``
            :param red_second_choice: Red color value - OPTIONAL
            :type red_second_choice: ``int`` or ``HexList``
            :param green_second_choice: Green color value - OPTIONAL
            :type green_second_choice: ``int`` or ``HexList``
            :param blue_second_choice: Blue color value - OPTIONAL
            :type blue_second_choice: ``int`` or ``HexList``
            :param period_msb: MSB of the effect period in ms - OPTIONAL
            :type period_msb: ``int``
            :param period_lsb: LSB of the effect period in ms - OPTIONAL
            :type period_lsb: ``int``
            :param intensity: Intensity in range 1..100, default = 100, 0 or > 100 = default - OPTIONAL
            :type intensity: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils.get_effect_index_by_effect_id_and_cluster_id(
                test_case=test_case,
                cluster_index=cluster_index,
                effect_id=RGBEffects.RGBEffectID.SMOOTH_STAR_BREATHING)
            test_case.assertNotNone(effect_index, msg="No effect_index found for smooth star breathing RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_1=red_first_choice,
                param_2=green_first_choice,
                param_3=blue_first_choice,
                param_4=red_second_choice,
                param_5=green_second_choice,
                param_6=blue_second_choice,
                param_7=period_msb,
                param_8=period_lsb,
                param_9=intensity,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_smooth_star_breathing_effect

        @classmethod
        def set_smooth_wave_effect(cls, test_case, cluster_index, red_first_choice=0, green_first_choice=0,
                                   blue_first_choice=0, red_second_choice=0, green_second_choice=0,
                                   blue_second_choice=0, period_msb=0, period_lsb=0, intensity=0,
                                   persistence=0, power_mode=0, device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param red_first_choice: Red color value - OPTIONAL
            :type red_first_choice: ``int`` or ``HexList``
            :param green_first_choice: Green color value - OPTIONAL
            :type green_first_choice: ``int`` or ``HexList``
            :param blue_first_choice: Blue color value - OPTIONAL
            :type blue_first_choice: ``int`` or ``HexList``
            :param red_second_choice: Red color value - OPTIONAL
            :type red_second_choice: ``int`` or ``HexList``
            :param green_second_choice: Green color value - OPTIONAL
            :type green_second_choice: ``int`` or ``HexList``
            :param blue_second_choice: Blue color value - OPTIONAL
            :type blue_second_choice: ``int`` or ``HexList``
            :param period_msb: MSB of the effect period in ms - OPTIONAL
            :type period_msb: ``int``
            :param period_lsb: LSB of the effect period in ms - OPTIONAL
            :type period_lsb: ``int``
            :param intensity: Intensity in range 1..100, default = 100, 0 or > 100 = default - OPTIONAL
            :type intensity: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils. \
                get_effect_index_by_effect_id_and_cluster_id(test_case=test_case, cluster_index=cluster_index,
                                                             effect_id=RGBEffects.RGBEffectID.SMOOTH_WAVE)
            test_case.assertNotNone(effect_index, msg="No effect_index found for smooth wave RGB effect")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_1=red_first_choice,
                param_2=green_first_choice,
                param_3=blue_first_choice,
                param_4=red_second_choice,
                param_5=green_second_choice,
                param_6=blue_second_choice,
                param_7=period_msb,
                param_8=period_lsb,
                param_9=intensity,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_smooth_wave_effect

        @classmethod
        def set_custom_onboard_effect(cls, test_case, slot, init_frame_msb, init_frame_lsb, length_msb, length_lsb,
                                      frame_period_msb, frame_period_lsb, intensity, persistence=0, power_mode=0,
                                      device_index=None, port_index=None):
            """
            Process ``SetRgbClusterEffectV0`` or ``SetRgbClusterEffectV1ToV4``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param slot: Effect slot
            :type slot: ``int`` or ``HexList``
            :param init_frame_msb: Init frame MSB
            :type init_frame_msb: ``int`` or ``HexList``
            :param init_frame_lsb: Init frame LSB
            :type init_frame_lsb: ``int`` or ``HexList``
            :param length_msb: The length MSB
            :type length_msb: ``int`` or ``HexList``
            :param length_lsb: The length LSB
            :type length_lsb: ``int`` or ``HexList``
            :param frame_period_msb: The frame period MSB
            :type frame_period_msb: ``int`` or ``HexList``
            :param frame_period_lsb: The frame period LSB
            :type frame_period_lsb: ``int`` or ``HexList``
            :param intensity: The intensity
            :type intensity: ``int`` or ``HexList``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            cluster_index, effect_index = RGBEffectsTestUtils.get_effect_index_by_id(
                test_case, RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED)
            test_case.assertNotEqual(cluster_index, None)
            test_case.assertNotEqual(effect_index, None)

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                param_1=slot,
                param_2=init_frame_msb,
                param_3=init_frame_lsb,
                param_4=length_msb,
                param_5=length_lsb,
                param_6=frame_period_msb,
                param_7=frame_period_lsb,
                param_8=intensity,
                power_mode=power_mode,
                persistence=persistence)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_custom_effect

        @classmethod
        def set_rgb_cluster_effect_with_default_values(cls, test_case, effect_id, cluster_index, persistence=0,
                                                       power_mode=0, device_index=None, port_index=None):
            """
            Set RGB effect according to effect_id and cluster_index parameters with default values for others parameters

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param effect_id: Effect ID
            :type effect_id: `` int``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
            :type persistence: ``int`` or ``HexList``
            :param power_mode: Power mode - OPTIONAL
            :type power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRgbClusterEffectResponse
            :rtype: ``SetRgbClusterEffectResponse``
            """
            effect_index = RGBEffectsTestUtils. \
                get_effect_index_by_effect_id_and_cluster_id(test_case=test_case, cluster_index=cluster_index,
                                                             effect_id=effect_id)
            test_case.assertNotNone(effect_index, msg="No effect_index found")

            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_rgb_cluster_effect_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=cluster_index,
                rgb_cluster_effect_index=effect_index,
                power_mode=power_mode,
                persistence=persistence
            )

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_rgb_cluster_effect_response_cls)
            return response
        # end def set_rgb_cluster_effect_with_default_values

        @classmethod
        def set_multi_led_rgb_cluster_pattern(
                cls, test_case, rgb_cluster_index, pattern, device_index=None, port_index=None):
            """
            Process ``SetMultiLedRgbClusterPattern``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_cluster_index: The index of the RGB cluster.
            :type rgb_cluster_index: ``int`` or ``HexList``
            :param pattern: The code that has been arbitrarily assigned to a combination of ON and OFF LEDs,
                            which is known by both FW and SW. 0xFF means all LEDs ON and 0x00 means all LEDs OFF.
                            Example: for 3 LEDs in a single RGB Cluster, code 0x01 could mean first LED ON,
                            code 0x02 could mean first and second LEDs ON, 0x03 all LEDs ON and 0x04 third and
                            second LEDs ON.
            :type pattern: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetMultiLedRgbClusterPatternResponse
            :rtype: ``SetMultiLedRgbClusterPatternResponse``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_multi_led_rgb_cluster_pattern_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=HexList(rgb_cluster_index),
                pattern=HexList(pattern))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_multi_led_rgb_cluster_pattern_response_cls)
            return response
        # end def set_multi_led_rgb_cluster_pattern

        @classmethod
        def manage_nv_config(cls, test_case, get_or_set, nv_capabilities, capability_state=0, param_1=0, param_2=0,
                             param_3=0, param_4=0, param_5=0, param_6=0, device_index=None, port_index=None):
            """
            Process ``ManageNvConfig``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_or_set: Determines the access type: read or modify
            :type get_or_set: ``int`` or ``HexList``
            :param nv_capabilities: One of the non-volatile capabilities. Only one must be provided.
            :type nv_capabilities: ``int`` or ``HexList``
            :param capability_state: Value only needed in case getOrSet parameter = 0x01 (Set) - OPTIONAL
            :type capability_state: ``int`` or ``HexList``
            :param param_1: Optional parameter 1 - OPTIONAL
            :type param_1: ``int`` or ``HexList``
            :param param_2: Optional parameter 2 - OPTIONAL
            :type param_2: ``int`` or ``HexList``
            :param param_3: Optional parameter 3 - OPTIONAL
            :type param_3: ``int`` or ``HexList``
            :param param_4: Optional parameter 4 - OPTIONAL
            :type param_4: ``int`` or ``HexList``
            :param param_5: Optional parameter 5 - OPTIONAL
            :type param_5: ``int`` or ``HexList``
            :param param_6: Optional parameter 6 - OPTIONAL
            :type param_6: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ManageNvConfigResponse
            :rtype: ``ManageNvConfigResponseV0ToV2`` or ``ManageNvConfigResponseV3ToV4``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            if feature_8071.VERSION < 3:
                report = feature_8071.manage_nv_config_cls(
                    device_index, feature_8071_index,
                    get_or_set=HexList(get_or_set),
                    nv_capabilities=nv_capabilities,
                    capability_state=HexList(capability_state),
                    param_1=HexList(param_1),
                    param_2=HexList(param_2))
            else:
                report = feature_8071.manage_nv_config_cls(
                    device_index, feature_8071_index,
                    get_or_set=HexList(get_or_set),
                    nv_capabilities=nv_capabilities,
                    capability_state=HexList(capability_state),
                    param_1=HexList(param_1),
                    param_2=HexList(param_2),
                    param_3=HexList(param_3),
                    param_4=HexList(param_4),
                    param_5=HexList(param_5),
                    param_6=HexList(param_6))
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.manage_nv_config_response_cls)
            return response
        # end def manage_nv_config

        @classmethod
        def manage_rgb_led_bin_info(cls, test_case, get_or_set, rgb_cluster_index, led_bin_index,
                                    param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8,
                                    device_index=None, port_index=None):
            """
            Process ``ManageRgbLedBinInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_or_set: Determines the access type: read or modify
            :type get_or_set: ``int`` or ``HexList``
            :param rgb_cluster_index: The index of the RGB cluster.
            :type rgb_cluster_index: ``int`` or ``HexList``
            :param led_bin_index: The index of the bin factor.
            :type led_bin_index: ``int`` or ``HexList``
            :param param_1: Those parameters help to define led bin information.
            :type param_1: ``int`` or ``HexList``
            :param param_2: Those parameters help to define led bin information.
            :type param_2: ``int`` or ``HexList``
            :param param_3: Those parameters help to define led bin information.
            :type param_3: ``int`` or ``HexList``
            :param param_4: Those parameters help to define led bin information.
            :type param_4: ``int`` or ``HexList``
            :param param_5: Those parameters help to define led bin information.
            :type param_5: ``int`` or ``HexList``
            :param param_6: Those parameters help to define led bin information.
            :type param_6: ``int`` or ``HexList``
            :param param_7: Those parameters help to define led bin information.
            :type param_7: ``int`` or ``HexList``
            :param param_8: Those parameters help to define led bin information.
            :type param_8: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ManageRgbLedBinInfoResponse
            :rtype: ``ManageRgbLedBinInfoResponse``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.manage_rgb_led_bin_info_cls(
                device_index, feature_8071_index,
                get_or_set=HexList(get_or_set),
                rgb_cluster_index=HexList(rgb_cluster_index),
                led_bin_index=HexList(led_bin_index),
                param_1=HexList(param_1),
                param_2=HexList(param_2),
                param_3=HexList(param_3),
                param_4=HexList(param_4),
                param_5=HexList(param_5),
                param_6=HexList(param_6),
                param_7=HexList(param_7),
                param_8=HexList(param_8))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.manage_rgb_led_bin_info_response_cls)
            return response
        # end def manage_rgb_led_bin_info

        @classmethod
        def manage_sw_control(cls, test_case, get_or_set, sw_control_flags=0, events_notification_flags=0,
                              device_index=None, port_index=None):
            """
            Process ``ManageSWControl``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_or_set: Determines the access type: read or modify
            :type get_or_set: ``int`` or ``HexList``
            :param sw_control_flags: Software control flags - OPTIONAL
            :type sw_control_flags: ``int`` or ``HexList``
            :param events_notification_flags: Allow synchronization of the effect between devices. - OPTIONAL
            :type events_notification_flags: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ManageSWControlResponse
            :rtype: ``ManageSWControlResponse``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.manage_sw_control_cls(
                device_index, feature_8071_index,
                get_or_set=HexList(get_or_set),
                sw_control_flags=HexList(sw_control_flags),
                events_notification_flags=HexList(events_notification_flags))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.manage_sw_control_response_cls)
            return response
        # end def manage_sw_control

        @classmethod
        def set_effect_sync_correction(cls, test_case, rgb_cluster_index, drift_value,
                                       device_index=None, port_index=None):
            """
            Process ``SetEffectSyncCorrection``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_cluster_index: The index of the RGB cluster.
                                      0xFF can be used for all RGB clusters.
            :type rgb_cluster_index: ``int`` or ``HexList``
            :param drift_value: Phase correction value (in ms) to be applied to achieve synchronisation with SW. Device
                                will speed-up or slow down the current effect play to minimise the driftValue reported
                                by SW.
            :type drift_value: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetEffectSyncCorrectionResponse
            :rtype: ``SetEffectSyncCorrectionResponse``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.set_effect_sync_correction_cls(
                device_index, feature_8071_index,
                rgb_cluster_index=HexList(rgb_cluster_index),
                drift_value=HexList(drift_value))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.set_effect_sync_correction_response_cls)
            return response
        # end def set_effect_sync_correction

        @classmethod
        def manage_rgb_power_mode_config(cls, test_case, get_or_set, rgb_power_mode_flags=0,
                                         rgb_no_act_timeout_to_psave=0, rgb_no_act_timeout_to_off=0,
                                         device_index=None, port_index=None):
            """
            Process ``ManageRgbPowerModeConfig``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_or_set: Determines the access type: read or modify
            :type get_or_set: ``int`` or ``HexList``
            :param rgb_power_mode_flags: The power mode flags - OPTIONAL
            :type rgb_power_mode_flags: ``int`` or ``HexList``
            :param rgb_no_act_timeout_to_psave: Timeout (in seconds) since last user activity until Power Save mode
                                                is set - OPTIONAL
            :type rgb_no_act_timeout_to_psave: ``int`` or ``HexList``
            :param rgb_no_act_timeout_to_off: Timeout (in seconds) without any user activity since entering Power Save
                                              mode until Power Off mode is set - OPTIONAL
            :type rgb_no_act_timeout_to_off: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ManageRgbPowerModeConfigResponse
            :rtype: ``ManageRgbPowerModeConfigResponse``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            # TODO: handle inout data type is HexList
            report = feature_8071.manage_rgb_power_mode_config_cls(
                device_index, feature_8071_index,
                get_or_set=HexList(get_or_set),
                rgb_power_mode_flags=HexList(rgb_power_mode_flags.to_bytes(2, 'big')),
                rgb_no_act_timeout_to_psave=HexList(rgb_no_act_timeout_to_psave.to_bytes(2, 'big')),
                rgb_no_act_timeout_to_off=HexList(rgb_no_act_timeout_to_off.to_bytes(2, 'big')))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.manage_rgb_power_mode_config_response_cls)
            return response
        # end def manage_rgb_power_mode_config

        @classmethod
        def manage_rgb_power_mode(cls, test_case, get_or_set, rgb_power_mode=0, device_index=None, port_index=None):
            """
            Process ``ManageRgbPowerMode``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_or_set: Determines the access type: read or modify
            :type get_or_set: ``int`` or ``HexList``
            :param rgb_power_mode: The power mode - OPTIONAL
            :type rgb_power_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ManageRgbPowerModeResponse
            :rtype: ``ManageRgbPowerModeResponse``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.manage_rgb_power_mode_cls(
                device_index, feature_8071_index,
                get_or_set=HexList(get_or_set),
                rgb_power_mode=HexList(rgb_power_mode))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.manage_rgb_power_mode_response_cls)
            return response
        # end def manage_rgb_power_mode

        @classmethod
        def shutdown(cls, test_case, device_index=None, port_index=None):
            """
            Process ``Shutdown``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ShutdownResponse
            :rtype: ``ShutdownResponse``
            """
            feature_8071_index, feature_8071, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8071.shutdown_cls(device_index, feature_8071_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8071.shutdown_response_cls)
            return response
        # end def shutdown

        @classmethod
        def effect_sync_event(cls, test_case, device_index=None, port_index=None):
            """
            Process ``EffectSyncEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: EffectSyncEvent
            :rtype: ``EffectSyncEvent``
            """
            _, feature_8071, _, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8071.effect_sync_event_cls)
        # end def effect_sync_event

        @classmethod
        def user_activity_event(cls, test_case, device_index=None, port_index=None):
            """
            Process ``UserActivityEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: UserActivityEvent
            :rtype: ``UserActivityEvent``
            """
            _, feature_8071, _, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8071.user_activity_event_cls)
        # end def user_activity_event

        @classmethod
        def rgb_cluster_changed_event(cls, test_case, device_index=None, port_index=None):
            """
            Process ``RgbClusterChangedEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: RgbClusterChangedEvent
            :rtype: ``RgbClusterChangedEvent``
            """
            _, feature_8071, _, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8071.rgb_cluster_changed_event_cls)
        # end def rgb_cluster_changed_event

        @classmethod
        def get_rgb_calibration_values(cls, test_case):
            """
            Get the rbg calibration values on ZONE 0, ZONE 1 and ZONE 2 using 0x1806 or 0x1807 feature

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: reb, blue and green calibration data for zone0, zone1 and zone2
            :rtype: ``list[list[int]]``
            """
            calibration_data = []

            feature_1807_index, _, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
                test_case=test_case, feature_id=ConfigurableProperties.FEATURE_ID,
                factory=ConfigurablePropertiesFactory, skip_not_found=True)
            if feature_1807_index != Root.FEATURE_NOT_FOUND:
                for property_id in (ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0,
                                    ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1,
                                    ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2,):
                    get_property_info_response = ConfigurablePropertiesTestUtils.HIDppHelper.get_property_info(
                        test_case=test_case, property_id=property_id)

                    if get_property_info_response.flags.supported:
                        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(test_case=test_case,
                                                                                    property_id=property_id)
                        read_data = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(test_case=test_case)
                        calibration_data.append([read_data.data[1], read_data.data[3], read_data.data[5]])
                    # end if
                # end for
            else:
                feature_1806_index, _, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
                    test_case=test_case, feature_id=ConfigurableDeviceProperties.FEATURE_ID,
                    factory=ConfigurableDevicePropertiesFactory, skip_not_found=True)
                if feature_1806_index != Root.FEATURE_NOT_FOUND:
                    for property_id in (ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE0,
                                        ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE1,
                                        ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE2,):
                        if str(property_id) in test_case.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_PROPERTIES.F_SupportedPropertyIds:
                            response = ConfigurableDevicePropertiesTestUtils.GetDevicePropertiesHelper.HIDppHelper.read(
                                test_case=test_case,
                                property_id=property_id,
                                flag=1,
                                sub_data_index=0x02)
                            calibration_data.append([response.property_data[1], response.property_data[3],
                                                     response.property_data[5]])
                        # end if
                    # end for
                # end if
            # end if
            return calibration_data
        # end def get_rgb_calibration_values
    # end class HIDppHelper

    @classmethod
    def get_effect_index_by_effect_id_and_cluster_id(cls, test_case, cluster_index, effect_id):
        """
        Get the effect index by effect ID and cluster index

        Note: return None if cannot found.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param cluster_index: RGB cluster index
        :type cluster_index: `` int``
        :param effect_id: Effect ID
        :type effect_id: `` int``

        :return: Effect index
        :rtype: ``int`` or ``None``
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.EFFECT_INFO_TABLE
        effect_index = None
        for i, (e_id, c_id) in enumerate(zip(config.F_EffectId, config.F_ClusterIndex)):
            if effect_id == int(e_id, 16) and cluster_index == int(c_id, 16):
                effect_index = int(config.F_EffectIndex[i], 16)
                break
            # end if
        # end for
        return effect_index
    # end def get_effect_index_by_effect_id_and_cluster_id

    @classmethod
    def get_effect_index_by_id(cls, test_case, effect_id):
        """
        Get the effect index by effect ID

        Note: return None if cannot found.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param effect_id: Effect ID
        :type effect_id: `` RGBEffectsTestUtils.RGBEffectID``

        :return: Cluster and effect index
        :rtype: ``int, int`` or ``None, None``
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.EFFECT_INFO_TABLE
        cluster_index = None
        effect_index = None
        for idx, e_id in enumerate(config.F_EffectId):
            if effect_id == int(e_id, 16):
                cluster_index = int(config.F_ClusterIndex[idx], 16)
                effect_index = int(config.F_EffectIndex[idx], 16)
                break
            # end if
        # end for
        return cluster_index, effect_index
    # end def get_effect_index_by_id

    @classmethod
    def get_effect_info(cls, test_case, effect_id):
        """
        Get the effect info by effect ID

        Note: return None if cannot found.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param effect_id: Effect ID
        :type effect_id: `` RGBEffectsTestUtils.RGBEffectID``

        :return: Cluster and effect index
        :rtype: ``int, list[int, int, int, int]`` or ``None, None``
        """
        cluster_index = None
        effect_info = None
        effect_info_table = test_case.config_manager.get_feature(ConfigurationManager.ID.EFFECTS_INFO_TABLE)
        for key in effect_info_table:
            for effect_settings in effect_info_table[key]:
                if effect_id == effect_settings[1]:
                    cluster_index = key
                    effect_info = effect_settings
                    break
                # end if
            # end for
        # end for
        return cluster_index, effect_info
    # end def get_effect_info

    @classmethod
    def get_supported_effect_ids_by_cluster(cls, test_case, cluster_index):
        """
        Get the list of effect IDs supported by a given cluster index

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param cluster_index: Index of the cluster
        :type cluster_index: ``int``

        :return: The effect IDs supported by the cluster
        :rtype: ``list[int]``
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.EFFECT_INFO_TABLE
        effects = []
        for index, cluster_idx in enumerate(config.F_ClusterIndex):
            if int(cluster_idx, 16) == cluster_index:
                effects.append(int(config.F_EffectId[index], 16))
            # end if
        # end for

        return effects
    # end def get_supported_effect_ids_by_cluster

    class RgbSpyHelper:
        """
        RGB effects Spy module Helper class
        """

        @classmethod
        def start_monitoring(cls, test_case, reset=True):
            """
            Start the LED spy over I2C monitoring or LED RGB spy.
            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param reset: flag indicating if we reset the module before starting the monitoring - OPTIONAL
            :type reset: ``bool``
            """
            if test_case.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
                test_case.led_rgb_parser = None
                fw_id = test_case.f.PRODUCT.F_ProductReference
                has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver
                if test_case.led_spy_over_i2c is not None:
                    # enable I2C monitoring
                    test_case.led_spy_over_i2c.start(reset=reset)
                elif test_case.led_spy is not None and \
                        LED_ID.RGB_PRIMARY_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:

                    led_ids = [LED_ID.RGB_RED_LED, LED_ID.RGB_GREEN_LED, LED_ID.RGB_BLUE_LED]

                    if has_edge_led_driver and \
                            LED_ID.RGB_EDGE_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                            LED_ID.RGB_EDGE_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                            LED_ID.RGB_EDGE_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:

                        led_ids.extend([LED_ID.RGB_EDGE_RED_LED, LED_ID.RGB_EDGE_GREEN_LED, LED_ID.RGB_EDGE_BLUE_LED])
                    # end if
                    # enable LED monitoring on the RGB LEDs
                    test_case.led_spy.start(led_ids)
                # end if
            else:
                warn("The LED Spy module is not discovered..., LED monitoring is not available.")
            # end if
        # end def start_monitoring

        @classmethod
        def stop_monitoring(cls, test_case):
            """
            Stop the LED spy over I2C monitoring or LED RGB spy.
            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            if test_case.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
                fw_id = test_case.f.PRODUCT.F_ProductReference
                has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver
                if test_case.led_spy_over_i2c is not None:
                    # stop I2C monitoring
                    test_case.led_spy_over_i2c.stop()
                elif test_case.led_spy is not None and \
                        LED_ID.RGB_PRIMARY_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:

                    led_ids = [LED_ID.RGB_RED_LED, LED_ID.RGB_GREEN_LED, LED_ID.RGB_BLUE_LED]

                    if has_edge_led_driver and \
                            LED_ID.RGB_EDGE_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                            LED_ID.RGB_EDGE_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                            LED_ID.RGB_EDGE_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:

                        led_ids.extend([LED_ID.RGB_EDGE_RED_LED, LED_ID.RGB_EDGE_GREEN_LED, LED_ID.RGB_EDGE_BLUE_LED])
                    # end if
                    # stop LED monitoring on the RGB LEDs
                    test_case.led_spy.stop(led_ids)
                # end if
            else:
                warn("The LED Spy module is not discovered..., LED monitoring is not available.")
            # end if
        # end def stop_monitoring

        @classmethod
        def check_disabled_effect(cls, test_case, calibration_data, cluster_index, excluded_indicators=None):
            """
            Verify the rgb effect is disabled

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
            :type calibration_data: ``list[list[int, int, int]]``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
             check - OPTIONAL
            :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``

            :raise ``NotImplementedError``: If RGB parser wants to use kosmos led spy module
            """
            has_rgb_led_spy = False
            led_values = []
            timestamps = []
            capture_duration = 0
            fw_id = test_case.f.PRODUCT.F_ProductReference
            has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver

            if test_case.led_spy is not None:
                if cluster_index == (RGBEffectsTestUtils.RGBClusterId.PRIMARY or
                                     RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER) and \
                        LED_ID.RGB_PRIMARY_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                elif cluster_index == RGBEffectsTestUtils.RGBClusterId.EDGE and \
                        LED_ID.RGB_EDGE_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                # end if
            # end if

            if test_case.led_spy_over_i2c is not None:
                # parse I2C or pwm data to led_values and timestamps lists
                timestamps, led_values, capture_duration = test_case.led_spy_over_i2c.parse_rgb_i2c(
                    enable_i2c1=has_edge_led_driver)
            elif test_case.led_spy is not None and has_rgb_led_spy:
                raise NotImplementedError('RGB LED parser not implemented yet')
            # end if

            # Check disabled effect
            test_case.led_rgb_parser = LedDataRgbParser(
                timestamps=timestamps,
                led_values=led_values,
                capture_duration=capture_duration,
                fw_id=fw_id)

            test_case.assertTrue(
                expr=test_case.led_rgb_parser.is_disabled_effect(
                    led_spy_values=led_values, cluster_index=cluster_index,
                    led_spy_timestamp=timestamps, excluded_indicators=excluded_indicators),
                msg='The Disabled effect is not correct'
            )
        # end def check_disabled_effect

        @classmethod
        def check_fixed_effect(cls, test_case, red_value, green_value, blue_value, calibration_data, cluster_index,
                               brightness=None, excluded_indicators=None, check_last_packet_only=False,
                               layout=KeyboardInternationalLayouts.LAYOUT.US):
            """
            Verify the fixed rgb effect is correct (rgb values and LED Id)

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param red_value: Red value of RGB color model
            :type red_value: ``int``
            :param green_value: Green value of RGB color model
            :type green_value: ``int``
            :param blue_value: Blue value of RGB color model
            :type blue_value: ``int``
            :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
            :type calibration_data: ``list[list[int, int, int]]``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param brightness: Brightness of LED - OPTIONAL
            :type brightness: ``int | None``
            :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
             check - OPTIONAL
            :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``
            :param check_last_packet_only: Flag indicating that the checker function will check the last I2C packet of
             MCU to LED driver IC - OPTIONAL
            :type check_last_packet_only: ``bool``
            :param layout: keyboard international layout type - OPTIONAL
            :type layout: ``KeyboardInternationalLayouts.LAYOUT``

            :raise ``NotImplementedError``: If RGB parser wants to use kosmos led spy module
            """
            has_rgb_led_spy = False
            led_values = []
            timestamps = []
            capture_duration = 0
            fw_id = test_case.f.PRODUCT.F_ProductReference
            has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver
            if test_case.led_spy is not None:
                if cluster_index == (RGBEffectsTestUtils.RGBClusterId.PRIMARY or
                                     RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER) and \
                        LED_ID.RGB_PRIMARY_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                elif cluster_index == RGBEffectsTestUtils.RGBClusterId.EDGE and \
                        LED_ID.RGB_EDGE_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                # end if
            # end if
            if test_case.led_spy_over_i2c is not None:
                # parse I2C or pwm data to led_values and timestamps lists
                timestamps, led_values, capture_duration = test_case.led_spy_over_i2c.parse_rgb_i2c(
                    enable_i2c1=has_edge_led_driver)
            elif test_case.led_spy is not None and has_rgb_led_spy:
                raise NotImplementedError('RGB LED parser not implemented yet')
            # end if

            # Creation of plot directory
            plot_dir = join(test_case.getContext().getOutputDir(), test_case.getContext().getCurrentTarget(),
                            'plot')
            if not access(plot_dir, F_OK):
                makedirs(plot_dir)
            # end if
            file_name = f"{test_case.id()}.png"
            plot_path = join(plot_dir, file_name)

            # Check fixed effect
            if test_case.led_rgb_parser is None:
                test_case.led_rgb_parser = LedDataRgbParser(
                    timestamps=timestamps,
                    led_values=led_values,
                    capture_duration=capture_duration,
                    fw_id=fw_id,
                    layout=layout,
                    plot_path=plot_path)
            # end if
            if brightness == 0 and len(led_values) == 0:
                # If the brightness is 0, and the previous status of RGB effect is OFF, then there might be no packet
                # sent from MCU to LED driver.
                pass
            else:
                test_case.assertTrue(
                    expr=test_case.led_rgb_parser.is_fixed_effect(
                        test_case=test_case,
                        fw_id=fw_id, led_spy_values=led_values, led_spy_timestamp=timestamps,
                        cluster_index=cluster_index, red_value=red_value, green_value=green_value,
                        blue_value=blue_value, calibration_data=calibration_data,
                        check_last_packet_only=check_last_packet_only,
                        brightness=brightness,
                        excluded_indicators=excluded_indicators, layout=layout),
                    msg='The Fixed effect is not correct'
                )
            # end if
        # end def check_fixed_effect

        @classmethod
        def check_pulsing_breathing_effect(cls, test_case, red_value, green_value, blue_value, period_msb, period_lsb,
                                           brightness, calibration_data, cluster_index, excluded_indicators=None,
                                           layout=KeyboardInternationalLayouts.LAYOUT.US):
            """
            Verify the pulsing/breathing rgb effect is correct (rgb values, period, brightness and LED Id)

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param red_value: Red value of RGB color model
            :type red_value: ``int``
            :param green_value: Green value of RGB color model
            :type green_value: ``int``
            :param blue_value: Blue value of RGB color model
            :type blue_value: ``int``
            :param period_msb: MSB of the effect period
            :type period_msb: ``int``
            :param period_lsb: LSB of the effect period
            :type period_lsb: ``int``
            :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100,
             >100 = default
            :type brightness: ``int``
            :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
            :type calibration_data: ``list[list[int, int, int]]``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
             check - OPTIONAL
            :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``
            :param layout: keyboard international layout type - OPTIONAL
            :type layout: ``KeyboardInternationalLayouts.LAYOUT``

            :raise ``NotImplementedError``: If RGB parser wants to use kosmos led spy module
            """
            has_rgb_led_spy = False
            led_values = []
            timestamps = []
            capture_duration = 0
            fw_id = test_case.f.PRODUCT.F_ProductReference
            has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver
            if test_case.led_spy is not None:
                if cluster_index == (RGBEffectsTestUtils.RGBClusterId.PRIMARY or
                                     RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER) and \
                        LED_ID.RGB_PRIMARY_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                elif cluster_index == RGBEffectsTestUtils.RGBClusterId.EDGE and \
                        LED_ID.RGB_EDGE_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                # end if
            # end if
            if test_case.led_spy_over_i2c is not None:
                # parse I2C or pwm data to led_values and timestamps lists
                timestamps, led_values, capture_duration = test_case.led_spy_over_i2c.parse_rgb_i2c(
                    enable_i2c1=has_edge_led_driver)
            elif test_case.led_spy is not None and has_rgb_led_spy:
                raise NotImplementedError('RGB LED parser not implemented yet')
            # end if

            # Creation of plot directory
            plot_dir = join(test_case.getContext().getOutputDir(), test_case.getContext().getCurrentTarget(), 'plot')
            if not access(plot_dir, F_OK):
                makedirs(plot_dir)
            # end if
            file_name = f"{test_case.id()}.png"
            plot_path = join(plot_dir, file_name)

            # Check pulsing/breathing effect
            if test_case.led_rgb_parser is None:
                test_case.led_rgb_parser = LedDataRgbParser(
                    timestamps=timestamps,
                    led_values=led_values,
                    capture_duration=capture_duration,
                    fw_id=fw_id,
                    layout=layout,
                    plot_path=plot_path)
            # end if

            test_case.assertTrue(
                expr=test_case.led_rgb_parser.is_pulsing_breathing_effect(
                    fw_id=fw_id, led_spy_values=led_values, led_spy_timestamp=timestamps,
                    cluster_index=cluster_index, red_value=red_value,
                    green_value=green_value, blue_value=blue_value, period_msb=period_msb,
                    period_lsb=period_lsb, brightness=brightness,
                    calibration_data=calibration_data,
                    excluded_indicators=excluded_indicators, layout=layout),
                msg='The pulsing/breathing effect is not correct'
            )
        # end def check_pulsing_breathing_effect

        @classmethod
        def check_color_cycling_configurable_s_effect(cls, test_case, saturation, period_msb, period_lsb,
                                                      brightness, calibration_data, cluster_index,
                                                      excluded_indicators=None,
                                                      layout=KeyboardInternationalLayouts.LAYOUT.US):
            """
            Verify the color cycling configurable saturation rgb effect is correct (saturation value, period, brightness
             and LED Id)

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param saturation: Saturation modulator of HSV color representation
            :type saturation: ``int``
            :param period_msb: MSB of the effect period
            :type period_msb: ``int``
            :param period_lsb: LSB of the effect period
            :type period_lsb: ``int``
            :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100,
             >100 = default
            :type brightness: ``int``
            :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
            :type calibration_data: ``list[list[int, int, int]]``
            :param cluster_index: RGB cluster index
            :type cluster_index: ``int``
            :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
             check - OPTIONAL
            :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``
            :param layout: keyboard international layout type - OPTIONAL
            :type layout: ``KeyboardInternationalLayouts.LAYOUT``

            :raise ``NotImplementedError``: If RGB parser wants to use kosmos led spy module
            """
            has_rgb_led_spy = False
            led_values = []
            timestamps = []
            capture_duration = 0
            fw_id = test_case.f.PRODUCT.F_ProductReference
            has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver
            if test_case.led_spy is not None:
                if cluster_index == (RGBEffectsTestUtils.RGBClusterId.PRIMARY or
                                     RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER) and \
                        LED_ID.RGB_PRIMARY_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_PRIMARY_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                elif cluster_index == RGBEffectsTestUtils.RGBClusterId.EDGE and \
                        LED_ID.RGB_EDGE_RED_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_GREEN_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS and \
                        LED_ID.RGB_EDGE_BLUE_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                    has_rgb_led_spy = True
                # end if
            # end if
            if test_case.led_spy_over_i2c is not None:
                # parse I2C or pwm data to led_values and timestamps lists
                timestamps, led_values, capture_duration = test_case.led_spy_over_i2c.parse_rgb_i2c(
                    enable_i2c1=has_edge_led_driver)
            elif test_case.led_spy is not None and has_rgb_led_spy:
                raise NotImplementedError('RGB LED parser not implemented yet')
            # end if

            # Creation of plot directory
            plot_dir = join(test_case.getContext().getOutputDir(), test_case.getContext().getCurrentTarget(),
                            'plot')
            if not access(plot_dir, F_OK):
                makedirs(plot_dir)
            # end if
            file_name = f"{test_case.id()}.png"
            plot_path = join(plot_dir, file_name)

            if test_case.led_rgb_parser is None:
                test_case.led_rgb_parser = LedDataRgbParser(
                    timestamps=timestamps,
                    led_values=led_values,
                    capture_duration=capture_duration,
                    fw_id=fw_id,
                    layout=layout,
                    plot_path=plot_path)
            # end if
            # Check color cycling configurable saturation effect
            test_case.assertTrue(
                expr=test_case.led_rgb_parser.is_color_cycling_configurable_s_effect(
                    fw_id=fw_id, led_spy_values=led_values,
                    led_spy_timestamp=timestamps, cluster_index=cluster_index,
                    saturation=saturation, period_msb=period_msb,
                    period_lsb=period_lsb, brightness=brightness,
                    calibration_data=calibration_data,
                    excluded_indicators=excluded_indicators, layout=layout),
                msg='The color cycling configurable saturation effect is not correct'
            )
        # end def check_color_cycling_configurable_s_effect

        @classmethod
        def check_immersive_lighting_with_oob_effect(cls, test_case, immersive_lighting_state, exact_duration=None,
                                                     minimum_duration=None, last_effect=False,
                                                     layout=KeyboardInternationalLayouts.LAYOUT.US,
                                                     previous_immersive_lighting_state=None):
            """
            Verify immersive lighting is correct (state and duration)

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param immersive_lighting_state: effect to check
            :type immersive_lighting_state: ``ImmersiveLightingState``
            :param exact_duration: fast blink state exact duration in ms to enforce (default is 3 minutes) - OPTIONAL
            :type exact_duration: ``int`` or ``None``
            :param minimum_duration: fast blink state minimum duration in ms to verify (exclusive with exact_duration)
            :type minimum_duration: ``int`` or ``None``
            :param last_effect: Flag indicating if we expect that it is the last effect - OPTIONAL
            :type last_effect: ``bool``
            :param layout: keyboard international layout type - OPTIONAL
            :type layout: ``KeyboardInternationalLayouts.LAYOUT``
            :param previous_immersive_lighting_state: Previous effect before recording - OPTIONAL
            :type previous_immersive_lighting_state: ``ImmersiveLightingState`` or ``None``

            Note: Only works with oob effect
            """
            has_rgb_led_spy = False
            led_values = []
            timestamps = []
            capture_duration = 0
            fw_id = test_case.f.PRODUCT.F_ProductReference
            has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver

            if test_case.led_spy_over_i2c is not None:
                # parse I2C or pwm data to led_values and timestamps lists
                timestamps, led_values, capture_duration = test_case.led_spy_over_i2c.\
                    parse_rgb_i2c(enable_i2c1=has_edge_led_driver)
            elif test_case.led_spy is not None and has_rgb_led_spy:
                raise NotImplementedError('RGB LED parser not implemented yet')
            # end if

            # Creation of plot directory
            plot_dir = join(test_case.getContext().getOutputDir(), test_case.getContext().getCurrentTarget(),
                            'plot')
            if not access(plot_dir, F_OK):
                makedirs(plot_dir)
            # end if
            file_name = f"{test_case.id()}.png"
            plot_path = join(plot_dir, file_name)

            if test_case.led_rgb_parser is None:
                test_case.led_rgb_parser = LedDataRgbParser(
                    timestamps=timestamps,
                    led_values=led_values,
                    capture_duration=capture_duration,
                    fw_id=fw_id,
                    layout=layout,
                    previous_immersive_lighting_state=previous_immersive_lighting_state,
                    plot_path=plot_path)
            # end if

            # Check immersive lighting with oob effect
            test_case.assertTrue(
                expr=test_case.led_rgb_parser.is_immersive_lighting_correct(
                    immersive_lighting_state=immersive_lighting_state,
                    exact_duration=exact_duration,
                    minimum_duration=minimum_duration,
                    last_effect=last_effect),
                msg=f'The immersive lighting is not correct in rgb timeline: {str(test_case.led_rgb_parser.timeline)}'
            )
        # end def check_immersive_lighting_with_oob_effect

        @classmethod
        def save_record(cls, test_case, file_name, start_index=0, save_timestamp=False):
            """
            Save a RGB spy record in pickle format

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param file_name: Name of the file
            :type file_name: ``string``
            :param start_index: Index where the record begins
            :type start_index: ``int``  - OPTIONAL
            :param save_timestamp: Flag indicationg if the timestamp is saved
            :type save_timestamp: ``bool`` - OPTIONAL
            """
            has_rgb_led_spy = False
            led_values = []
            timestamps = []
            has_edge_led_driver = test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver

            if test_case.led_spy_over_i2c is not None:
                # parse I2C or pwm data to led_values and timestamps lists
                timestamps, led_values, _ = test_case.led_spy_over_i2c.parse_rgb_i2c(enable_i2c1=has_edge_led_driver)
            elif test_case.led_spy is not None and has_rgb_led_spy:
                raise NotImplementedError('RGB LED parser not implemented yet')
            # end if

            file_path = join(LIBS_PATH, 'PYRASPI', 'pyraspi', 'services', 'kosmos', 'config', 'rgbconfigurations',
                             'recordings', file_name)
            # Save records
            with open(file_path + '.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                dump(led_values[start_index::], f, HIGHEST_PROTOCOL)
            # end with
            if save_timestamp:
                with open(file_path + '_timestamp.pickle', 'wb') as f:
                    # Pickle the 'data' dictionary using the highest protocol available.
                    dump(timestamps, f, HIGHEST_PROTOCOL)
                # end with
            # end if
        # end def save_record
    # end class RgbSpyHelper

    @classmethod
    def delete_led_brightness_chunk(cls, test_case):
        """
        Delete RGB led brightness chunk

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        test_case.memory_manager.read_nvs()
        invalidated_chunk_count = test_case.memory_manager.invalidate_chunks(chunk_names=["NVS_LED_BRIGHTNESS_ID"])
        if invalidated_chunk_count > 0:
            test_case.memory_manager.load_nvs()
        # end if
    # end def delete_led_brightness_chunk
# end class RGBEffectsTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
