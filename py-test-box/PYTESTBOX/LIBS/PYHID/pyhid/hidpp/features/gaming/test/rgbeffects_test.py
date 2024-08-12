#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.test.rgbeffects_test
:brief: HID++ 2.0 ``RGBEffects`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.rgbeffects import EffectSyncEvent
from pyhid.hidpp.features.gaming.rgbeffects import GetInfoResponse
from pyhid.hidpp.features.gaming.rgbeffects import GetInfoV0
from pyhid.hidpp.features.gaming.rgbeffects import GetInfoV1ToV4
from pyhid.hidpp.features.gaming.rgbeffects import ManageNvConfigResponseV0ToV2
from pyhid.hidpp.features.gaming.rgbeffects import ManageNvConfigResponseV3ToV4
from pyhid.hidpp.features.gaming.rgbeffects import ManageNvConfigV0ToV2
from pyhid.hidpp.features.gaming.rgbeffects import ManageNvConfigV3ToV4
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbLedBinInfo
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbLedBinInfoResponse
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbPowerMode
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbPowerModeConfig
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbPowerModeConfigResponse
from pyhid.hidpp.features.gaming.rgbeffects import ManageRgbPowerModeResponse
from pyhid.hidpp.features.gaming.rgbeffects import ManageSWControl
from pyhid.hidpp.features.gaming.rgbeffects import ManageSWControlResponse
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsFactory
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsV0
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsV1
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsV2
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsV3
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsV4
from pyhid.hidpp.features.gaming.rgbeffects import RgbClusterChangedEvent
from pyhid.hidpp.features.gaming.rgbeffects import SetEffectSyncCorrection
from pyhid.hidpp.features.gaming.rgbeffects import SetEffectSyncCorrectionResponse
from pyhid.hidpp.features.gaming.rgbeffects import SetMultiLedRgbClusterPattern
from pyhid.hidpp.features.gaming.rgbeffects import SetMultiLedRgbClusterPatternResponse
from pyhid.hidpp.features.gaming.rgbeffects import SetRgbClusterEffectResponse
from pyhid.hidpp.features.gaming.rgbeffects import SetRgbClusterEffectV0
from pyhid.hidpp.features.gaming.rgbeffects import SetRgbClusterEffectV1ToV4
from pyhid.hidpp.features.gaming.rgbeffects import Shutdown
from pyhid.hidpp.features.gaming.rgbeffects import ShutdownResponse
from pyhid.hidpp.features.gaming.rgbeffects import UserActivityEvent
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RGBEffectsInstantiationTestCase(TestCase):
    """
    ``RGBEffects`` testing classes instantiations
    """
    @staticmethod
    def test_rgb_effects():
        """
        Tests ``RGBEffects`` class instantiation
        """
        my_class = RGBEffects(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = RGBEffects(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_rgb_effects

    @staticmethod
    def test_get_info_v0():
        """
        Tests ``GetInfoV0`` class instantiation
        """
        my_class = GetInfoV0(device_index=0, feature_index=0,
                             rgb_cluster_index=0,
                             rgb_cluster_effect_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetInfoV0(device_index=0xff, feature_index=0xff,
                             rgb_cluster_index=0xff,
                             rgb_cluster_effect_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info_v0

    @staticmethod
    def test_get_info_v1_to_v4():
        """
        Tests ``GetInfoV1ToV4`` class instantiation
        """
        my_class = GetInfoV1ToV4(device_index=0, feature_index=0,
                                 rgb_cluster_index=0,
                                 rgb_cluster_effect_index=0,
                                 type_of_info=0,
                                 param_1=0,
                                 param_2=0,
                                 param_3=0,
                                 param_4=0,
                                 param_5=0,
                                 param_6=0,
                                 param_7=0,
                                 param_8=0,
                                 param_9=0,
                                 param_10=0,
                                 param_11=0,
                                 param_12=0,
                                 param_13=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoV1ToV4(device_index=0xff, feature_index=0xff,
                                 rgb_cluster_index=0xff,
                                 rgb_cluster_effect_index=0xff,
                                 type_of_info=0xff,
                                 param_1=0xff,
                                 param_2=0xff,
                                 param_3=0xff,
                                 param_4=0xff,
                                 param_5=0xff,
                                 param_6=0xff,
                                 param_7=0xff,
                                 param_8=0xff,
                                 param_9=0xff,
                                 param_10=0xff,
                                 param_11=0xff,
                                 param_12=0xff,
                                 param_13=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_v1_to_v4

    @staticmethod
    def test_get_info_response():
        """
        Tests ``GetInfoResponse`` class instantiation
        """
        my_class = GetInfoResponse(device_index=0, feature_index=0,
                                   rgb_cluster_index=0,
                                   rgb_cluster_effect_index=0,
                                   param_1=0,
                                   param_2=0,
                                   param_3=0,
                                   param_4=0,
                                   param_5=0,
                                   param_6=0,
                                   param_7=0,
                                   param_8=0,
                                   param_9=0,
                                   param_10=0,
                                   param_11=0,
                                   param_12=0,
                                   param_13=0,
                                   param_14=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse(device_index=0xff, feature_index=0xff,
                                   rgb_cluster_index=0xff,
                                   rgb_cluster_effect_index=0xff,
                                   param_1=0xff,
                                   param_2=0xff,
                                   param_3=0xff,
                                   param_4=0xff,
                                   param_5=0xff,
                                   param_6=0xff,
                                   param_7=0xff,
                                   param_8=0xff,
                                   param_9=0xff,
                                   param_10=0xff,
                                   param_11=0xff,
                                   param_12=0xff,
                                   param_13=0xff,
                                   param_14=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response

    @staticmethod
    def test_set_rgb_cluster_effect_v0():
        """
        Tests ``SetRgbClusterEffectV0`` class instantiation
        """
        my_class = SetRgbClusterEffectV0(device_index=0, feature_index=0,
                                         rgb_cluster_index=0,
                                         rgb_cluster_effect_index=0,
                                         param_1=0,
                                         param_2=0,
                                         param_3=0,
                                         param_4=0,
                                         param_5=0,
                                         param_6=0,
                                         param_7=0,
                                         param_8=0,
                                         param_9=0,
                                         param_10=0,
                                         persistence=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRgbClusterEffectV0(device_index=0xff, feature_index=0xff,
                                         rgb_cluster_index=0xff,
                                         rgb_cluster_effect_index=0xff,
                                         param_1=0xff,
                                         param_2=0xff,
                                         param_3=0xff,
                                         param_4=0xff,
                                         param_5=0xff,
                                         param_6=0xff,
                                         param_7=0xff,
                                         param_8=0xff,
                                         param_9=0xff,
                                         param_10=0xff,
                                         persistence=0x3)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rgb_cluster_effect_v0

    @staticmethod
    def test_set_rgb_cluster_effect_v1_to_v4():
        """
        Tests ``SetRgbClusterEffectV1ToV4`` class instantiation
        """
        my_class = SetRgbClusterEffectV1ToV4(device_index=0, feature_index=0,
                                             rgb_cluster_index=0,
                                             rgb_cluster_effect_index=0,
                                             param_1=0,
                                             param_2=0,
                                             param_3=0,
                                             param_4=0,
                                             param_5=0,
                                             param_6=0,
                                             param_7=0,
                                             param_8=0,
                                             param_9=0,
                                             param_10=0,
                                             power_mode=0,
                                             persistence=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRgbClusterEffectV1ToV4(device_index=0xff, feature_index=0xff,
                                             rgb_cluster_index=0xff,
                                             rgb_cluster_effect_index=0xff,
                                             param_1=0xff,
                                             param_2=0xff,
                                             param_3=0xff,
                                             param_4=0xff,
                                             param_5=0xff,
                                             param_6=0xff,
                                             param_7=0xff,
                                             param_8=0xff,
                                             param_9=0xff,
                                             param_10=0xff,
                                             power_mode=0x3,
                                             persistence=0x3)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rgb_cluster_effect_v1_to_v4

    @staticmethod
    def test_set_rgb_cluster_effect_response():
        """
        Tests ``SetRgbClusterEffectResponse`` class instantiation
        """
        my_class = SetRgbClusterEffectResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRgbClusterEffectResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rgb_cluster_effect_response

    @staticmethod
    def test_set_multi_led_rgb_cluster_pattern():
        """
        Tests ``SetMultiLedRgbClusterPattern`` class instantiation
        """
        my_class = SetMultiLedRgbClusterPattern(device_index=0, feature_index=0,
                                                rgb_cluster_index=0,
                                                pattern=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetMultiLedRgbClusterPattern(device_index=0xff, feature_index=0xff,
                                                rgb_cluster_index=0xff,
                                                pattern=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_multi_led_rgb_cluster_pattern

    @staticmethod
    def test_set_multi_led_rgb_cluster_pattern_response():
        """
        Tests ``SetMultiLedRgbClusterPatternResponse`` class instantiation
        """
        my_class = SetMultiLedRgbClusterPatternResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetMultiLedRgbClusterPatternResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_multi_led_rgb_cluster_pattern_response

    @staticmethod
    def test_manage_nv_config_v0_to_v2():
        """
        Tests ``ManageNvConfigV0ToV2`` class instantiation
        """
        my_class = ManageNvConfigV0ToV2(device_index=0, feature_index=0,
                                        get_or_set=0,
                                        nv_capabilities=0,
                                        capability_state=0,
                                        param_1=0,
                                        param_2=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageNvConfigV0ToV2(device_index=0xff, feature_index=0xff,
                                        get_or_set=0xff,
                                        nv_capabilities=0xffff,
                                        capability_state=0xff,
                                        param_1=0xff,
                                        param_2=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_nv_config_v0_to_v2

    @staticmethod
    def test_manage_nv_config_v3_to_v4():
        """
        Tests ``ManageNvConfigV3ToV4`` class instantiation
        """
        my_class = ManageNvConfigV3ToV4(device_index=0, feature_index=0,
                                        get_or_set=0,
                                        nv_capabilities=0,
                                        capability_state=0,
                                        param_1=0,
                                        param_2=0,
                                        param_3=0,
                                        param_4=0,
                                        param_5=0,
                                        param_6=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageNvConfigV3ToV4(device_index=0xff, feature_index=0xff,
                                        get_or_set=0xff,
                                        nv_capabilities=0xffff,
                                        capability_state=0xff,
                                        param_1=0xff,
                                        param_2=0xff,
                                        param_3=0xff,
                                        param_4=0xff,
                                        param_5=0xff,
                                        param_6=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_nv_config_v3_to_v4

    @staticmethod
    def test_manage_nv_config_response_v0_to_v2():
        """
        Tests ``ManageNvConfigResponseV0ToV2`` class instantiation
        """
        my_class = ManageNvConfigResponseV0ToV2(device_index=0, feature_index=0,
                                                get_or_set=0,
                                                nv_capabilities=0,
                                                capability_state=0,
                                                param_1=0,
                                                param_2=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageNvConfigResponseV0ToV2(device_index=0xff, feature_index=0xff,
                                                get_or_set=0xff,
                                                nv_capabilities=0xffff,
                                                capability_state=0xff,
                                                param_1=0xff,
                                                param_2=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_nv_config_response_v0_to_v2

    @staticmethod
    def test_manage_nv_config_response_v3_to_v4():
        """
        Tests ``ManageNvConfigResponseV3ToV4`` class instantiation
        """
        my_class = ManageNvConfigResponseV3ToV4(device_index=0, feature_index=0,
                                                get_or_set=0,
                                                nv_capabilities=0,
                                                capability_state=0,
                                                param_1=0,
                                                param_2=0,
                                                param_3=0,
                                                param_4=0,
                                                param_5=0,
                                                param_6=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageNvConfigResponseV3ToV4(device_index=0xff, feature_index=0xff,
                                                get_or_set=0xff,
                                                nv_capabilities=0xffff,
                                                capability_state=0xff,
                                                param_1=0xff,
                                                param_2=0xff,
                                                param_3=0xff,
                                                param_4=0xff,
                                                param_5=0xff,
                                                param_6=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_nv_config_response_v3_to_v4

    @staticmethod
    def test_manage_rgb_led_bin_info():
        """
        Tests ``ManageRgbLedBinInfo`` class instantiation
        """
        my_class = ManageRgbLedBinInfo(device_index=0, feature_index=0,
                                       get_or_set=0,
                                       rgb_cluster_index=0,
                                       led_bin_index=0,
                                       param_1=0,
                                       param_2=0,
                                       param_3=0,
                                       param_4=0,
                                       param_5=0,
                                       param_6=0,
                                       param_7=0,
                                       param_8=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageRgbLedBinInfo(device_index=0xff, feature_index=0xff,
                                       get_or_set=0xff,
                                       rgb_cluster_index=0xff,
                                       led_bin_index=0xff,
                                       param_1=0xff,
                                       param_2=0xff,
                                       param_3=0xff,
                                       param_4=0xff,
                                       param_5=0xff,
                                       param_6=0xff,
                                       param_7=0xff,
                                       param_8=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_rgb_led_bin_info

    @staticmethod
    def test_manage_rgb_led_bin_info_response():
        """
        Tests ``ManageRgbLedBinInfoResponse`` class instantiation
        """
        my_class = ManageRgbLedBinInfoResponse(device_index=0, feature_index=0,
                                               get_or_set=0,
                                               rgb_cluster_index=0,
                                               led_bin_index=0,
                                               param_1=0,
                                               param_2=0,
                                               param_3=0,
                                               param_4=0,
                                               param_5=0,
                                               param_6=0,
                                               param_7=0,
                                               param_8=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageRgbLedBinInfoResponse(device_index=0xff, feature_index=0xff,
                                               get_or_set=0xff,
                                               rgb_cluster_index=0xff,
                                               led_bin_index=0xff,
                                               param_1=0xff,
                                               param_2=0xff,
                                               param_3=0xff,
                                               param_4=0xff,
                                               param_5=0xff,
                                               param_6=0xff,
                                               param_7=0xff,
                                               param_8=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_rgb_led_bin_info_response

    @staticmethod
    def test_manage_sw_control():
        """
        Tests ``ManageSWControl`` class instantiation
        """
        my_class = ManageSWControl(device_index=0, feature_index=0,
                                   get_or_set=0,
                                   sw_control_flags=0,
                                   events_notification_flags=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageSWControl(device_index=0xff, feature_index=0xff,
                                   get_or_set=0xff,
                                   sw_control_flags=0xff,
                                   events_notification_flags=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_sw_control

    @staticmethod
    def test_manage_sw_control_response():
        """
        Tests ``ManageSWControlResponse`` class instantiation
        """
        my_class = ManageSWControlResponse(device_index=0, feature_index=0,
                                           get_or_set=0,
                                           sw_control_flags=0,
                                           events_notification_flags=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageSWControlResponse(device_index=0xff, feature_index=0xff,
                                           get_or_set=0xff,
                                           sw_control_flags=0xff,
                                           events_notification_flags=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_sw_control_response

    @staticmethod
    def test_set_effect_sync_correction():
        """
        Tests ``SetEffectSyncCorrection`` class instantiation
        """
        my_class = SetEffectSyncCorrection(device_index=0, feature_index=0,
                                           rgb_cluster_index=0,
                                           drift_value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetEffectSyncCorrection(device_index=0xff, feature_index=0xff,
                                           rgb_cluster_index=0xff,
                                           drift_value=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_effect_sync_correction

    @staticmethod
    def test_set_effect_sync_correction_response():
        """
        Tests ``SetEffectSyncCorrectionResponse`` class instantiation
        """
        my_class = SetEffectSyncCorrectionResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetEffectSyncCorrectionResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_effect_sync_correction_response

    @staticmethod
    def test_manage_rgb_power_mode_config():
        """
        Tests ``ManageRgbPowerModeConfig`` class instantiation
        """
        my_class = ManageRgbPowerModeConfig(device_index=0, feature_index=0,
                                            get_or_set=0,
                                            rgb_power_mode_flags=0,
                                            rgb_no_act_timeout_to_psave=0,
                                            rgb_no_act_timeout_to_off=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageRgbPowerModeConfig(device_index=0xff, feature_index=0xff,
                                            get_or_set=0xff,
                                            rgb_power_mode_flags=0xffff,
                                            rgb_no_act_timeout_to_psave=0xffff,
                                            rgb_no_act_timeout_to_off=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_rgb_power_mode_config

    @staticmethod
    def test_manage_rgb_power_mode_config_response():
        """
        Tests ``ManageRgbPowerModeConfigResponse`` class instantiation
        """
        my_class = ManageRgbPowerModeConfigResponse(device_index=0, feature_index=0,
                                                    get_or_set=0,
                                                    rgb_power_mode_flags=0,
                                                    rgb_no_act_timeout_to_psave=0,
                                                    rgb_no_act_timeout_to_off=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageRgbPowerModeConfigResponse(device_index=0xff, feature_index=0xff,
                                                    get_or_set=0xff,
                                                    rgb_power_mode_flags=0xffff,
                                                    rgb_no_act_timeout_to_psave=0xffff,
                                                    rgb_no_act_timeout_to_off=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_rgb_power_mode_config_response

    @staticmethod
    def test_manage_rgb_power_mode():
        """
        Tests ``ManageRgbPowerMode`` class instantiation
        """
        my_class = ManageRgbPowerMode(device_index=0, feature_index=0,
                                      get_or_set=0,
                                      rgb_power_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageRgbPowerMode(device_index=0xff, feature_index=0xff,
                                      get_or_set=0xff,
                                      rgb_power_mode=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_rgb_power_mode

    @staticmethod
    def test_manage_rgb_power_mode_response():
        """
        Tests ``ManageRgbPowerModeResponse`` class instantiation
        """
        my_class = ManageRgbPowerModeResponse(device_index=0, feature_index=0,
                                              get_or_set=0,
                                              rgb_power_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageRgbPowerModeResponse(device_index=0xff, feature_index=0xff,
                                              get_or_set=0xff,
                                              rgb_power_mode=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_rgb_power_mode_response

    @staticmethod
    def test_shutdown():
        """
        Tests ``Shutdown`` class instantiation
        """
        my_class = Shutdown(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = Shutdown(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_shutdown

    @staticmethod
    def test_shutdown_response():
        """
        Tests ``ShutdownResponse`` class instantiation
        """
        my_class = ShutdownResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShutdownResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_shutdown_response

    @staticmethod
    def test_effect_sync_event():
        """
        Tests ``EffectSyncEvent`` class instantiation
        """
        my_class = EffectSyncEvent(device_index=0, feature_index=0,
                                   rgb_cluster_index=0,
                                   effect_counter=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EffectSyncEvent(device_index=0xff, feature_index=0xff,
                                   rgb_cluster_index=0xff,
                                   effect_counter=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_effect_sync_event

    @staticmethod
    def test_user_activity_event():
        """
        Tests ``UserActivityEvent`` class instantiation
        """
        my_class = UserActivityEvent(device_index=0, feature_index=0,
                                     activity_event_type=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = UserActivityEvent(device_index=0xff, feature_index=0xff,
                                     activity_event_type=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_user_activity_event

    @staticmethod
    def test_rgb_cluster_changed_event():
        """
        Tests ``RgbClusterChangedEvent`` class instantiation
        """
        my_class = RgbClusterChangedEvent(device_index=0, feature_index=0,
                                          rgb_cluster_index=0,
                                          rgb_cluster_effect_index=0,
                                          param_1=0,
                                          param_2=0,
                                          param_3=0,
                                          param_4=0,
                                          param_5=0,
                                          param_6=0,
                                          param_7=0,
                                          param_8=0,
                                          param_9=0,
                                          param_10=0,
                                          power_mode=0,
                                          persistence=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RgbClusterChangedEvent(device_index=0xff, feature_index=0xff,
                                          rgb_cluster_index=0xff,
                                          rgb_cluster_effect_index=0xff,
                                          param_1=0xff,
                                          param_2=0xff,
                                          param_3=0xff,
                                          param_4=0xff,
                                          param_5=0xff,
                                          param_6=0xff,
                                          param_7=0xff,
                                          param_8=0xff,
                                          param_9=0xff,
                                          param_10=0xff,
                                          power_mode=0x3,
                                          persistence=0x3)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rgb_cluster_changed_event
# end class RGBEffectsInstantiationTestCase


class RGBEffectsTestCase(TestCase):
    """
    ``RGBEffects`` factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            RGBEffectsV0.VERSION: {
                "cls": RGBEffectsV0,
                "interfaces": {
                    "get_info_cls": GetInfoV0,
                    "get_info_response_cls": GetInfoResponse,
                    "set_rgb_cluster_effect_cls": SetRgbClusterEffectV0,
                    "set_rgb_cluster_effect_response_cls": SetRgbClusterEffectResponse,
                    "set_multi_led_rgb_cluster_pattern_cls": SetMultiLedRgbClusterPattern,
                    "set_multi_led_rgb_cluster_pattern_response_cls": SetMultiLedRgbClusterPatternResponse,
                    "manage_nv_config_cls": ManageNvConfigV0ToV2,
                    "manage_nv_config_response_cls": ManageNvConfigResponseV0ToV2,
                    "manage_rgb_led_bin_info_cls": ManageRgbLedBinInfo,
                    "manage_rgb_led_bin_info_response_cls": ManageRgbLedBinInfoResponse,
                    "manage_sw_control_cls": ManageSWControl,
                    "manage_sw_control_response_cls": ManageSWControlResponse,
                    "set_effect_sync_correction_cls": SetEffectSyncCorrection,
                    "set_effect_sync_correction_response_cls": SetEffectSyncCorrectionResponse,
                    "manage_rgb_power_mode_config_cls": ManageRgbPowerModeConfig,
                    "manage_rgb_power_mode_config_response_cls": ManageRgbPowerModeConfigResponse,
                    "manage_rgb_power_mode_cls": ManageRgbPowerMode,
                    "manage_rgb_power_mode_response_cls": ManageRgbPowerModeResponse,
                    "effect_sync_event_cls": EffectSyncEvent,
                    "user_activity_event_cls": UserActivityEvent,
                },
                "max_function_index": 8
            },
            RGBEffectsV1.VERSION: {
                "cls": RGBEffectsV1,
                "interfaces": {
                    "get_info_cls": GetInfoV1ToV4,
                    "get_info_response_cls": GetInfoResponse,
                    "set_rgb_cluster_effect_cls": SetRgbClusterEffectV1ToV4,
                    "set_rgb_cluster_effect_response_cls": SetRgbClusterEffectResponse,
                    "set_multi_led_rgb_cluster_pattern_cls": SetMultiLedRgbClusterPattern,
                    "set_multi_led_rgb_cluster_pattern_response_cls": SetMultiLedRgbClusterPatternResponse,
                    "manage_nv_config_cls": ManageNvConfigV0ToV2,
                    "manage_nv_config_response_cls": ManageNvConfigResponseV0ToV2,
                    "manage_rgb_led_bin_info_cls": ManageRgbLedBinInfo,
                    "manage_rgb_led_bin_info_response_cls": ManageRgbLedBinInfoResponse,
                    "manage_sw_control_cls": ManageSWControl,
                    "manage_sw_control_response_cls": ManageSWControlResponse,
                    "set_effect_sync_correction_cls": SetEffectSyncCorrection,
                    "set_effect_sync_correction_response_cls": SetEffectSyncCorrectionResponse,
                    "manage_rgb_power_mode_config_cls": ManageRgbPowerModeConfig,
                    "manage_rgb_power_mode_config_response_cls": ManageRgbPowerModeConfigResponse,
                    "manage_rgb_power_mode_cls": ManageRgbPowerMode,
                    "manage_rgb_power_mode_response_cls": ManageRgbPowerModeResponse,
                    "effect_sync_event_cls": EffectSyncEvent,
                    "user_activity_event_cls": UserActivityEvent,
                },
                "max_function_index": 8
            },
            RGBEffectsV2.VERSION: {
                "cls": RGBEffectsV2,
                "interfaces": {
                    "get_info_cls": GetInfoV1ToV4,
                    "get_info_response_cls": GetInfoResponse,
                    "set_rgb_cluster_effect_cls": SetRgbClusterEffectV1ToV4,
                    "set_rgb_cluster_effect_response_cls": SetRgbClusterEffectResponse,
                    "set_multi_led_rgb_cluster_pattern_cls": SetMultiLedRgbClusterPattern,
                    "set_multi_led_rgb_cluster_pattern_response_cls": SetMultiLedRgbClusterPatternResponse,
                    "manage_nv_config_cls": ManageNvConfigV0ToV2,
                    "manage_nv_config_response_cls": ManageNvConfigResponseV0ToV2,
                    "manage_rgb_led_bin_info_cls": ManageRgbLedBinInfo,
                    "manage_rgb_led_bin_info_response_cls": ManageRgbLedBinInfoResponse,
                    "manage_sw_control_cls": ManageSWControl,
                    "manage_sw_control_response_cls": ManageSWControlResponse,
                    "set_effect_sync_correction_cls": SetEffectSyncCorrection,
                    "set_effect_sync_correction_response_cls": SetEffectSyncCorrectionResponse,
                    "manage_rgb_power_mode_config_cls": ManageRgbPowerModeConfig,
                    "manage_rgb_power_mode_config_response_cls": ManageRgbPowerModeConfigResponse,
                    "manage_rgb_power_mode_cls": ManageRgbPowerMode,
                    "manage_rgb_power_mode_response_cls": ManageRgbPowerModeResponse,
                    "effect_sync_event_cls": EffectSyncEvent,
                    "user_activity_event_cls": UserActivityEvent,
                },
                "max_function_index": 8
            },
            RGBEffectsV3.VERSION: {
                "cls": RGBEffectsV3,
                "interfaces": {
                    "get_info_cls": GetInfoV1ToV4,
                    "get_info_response_cls": GetInfoResponse,
                    "set_rgb_cluster_effect_cls": SetRgbClusterEffectV1ToV4,
                    "set_rgb_cluster_effect_response_cls": SetRgbClusterEffectResponse,
                    "set_multi_led_rgb_cluster_pattern_cls": SetMultiLedRgbClusterPattern,
                    "set_multi_led_rgb_cluster_pattern_response_cls": SetMultiLedRgbClusterPatternResponse,
                    "manage_nv_config_cls": ManageNvConfigV3ToV4,
                    "manage_nv_config_response_cls": ManageNvConfigResponseV3ToV4,
                    "manage_rgb_led_bin_info_cls": ManageRgbLedBinInfo,
                    "manage_rgb_led_bin_info_response_cls": ManageRgbLedBinInfoResponse,
                    "manage_sw_control_cls": ManageSWControl,
                    "manage_sw_control_response_cls": ManageSWControlResponse,
                    "set_effect_sync_correction_cls": SetEffectSyncCorrection,
                    "set_effect_sync_correction_response_cls": SetEffectSyncCorrectionResponse,
                    "manage_rgb_power_mode_config_cls": ManageRgbPowerModeConfig,
                    "manage_rgb_power_mode_config_response_cls": ManageRgbPowerModeConfigResponse,
                    "manage_rgb_power_mode_cls": ManageRgbPowerMode,
                    "manage_rgb_power_mode_response_cls": ManageRgbPowerModeResponse,
                    "effect_sync_event_cls": EffectSyncEvent,
                    "user_activity_event_cls": UserActivityEvent,
                },
                "max_function_index": 8
            },
            RGBEffectsV4.VERSION: {
                "cls": RGBEffectsV4,
                "interfaces": {
                    "get_info_cls": GetInfoV1ToV4,
                    "get_info_response_cls": GetInfoResponse,
                    "set_rgb_cluster_effect_cls": SetRgbClusterEffectV1ToV4,
                    "set_rgb_cluster_effect_response_cls": SetRgbClusterEffectResponse,
                    "set_multi_led_rgb_cluster_pattern_cls": SetMultiLedRgbClusterPattern,
                    "set_multi_led_rgb_cluster_pattern_response_cls": SetMultiLedRgbClusterPatternResponse,
                    "manage_nv_config_cls": ManageNvConfigV3ToV4,
                    "manage_nv_config_response_cls": ManageNvConfigResponseV3ToV4,
                    "manage_rgb_led_bin_info_cls": ManageRgbLedBinInfo,
                    "manage_rgb_led_bin_info_response_cls": ManageRgbLedBinInfoResponse,
                    "manage_sw_control_cls": ManageSWControl,
                    "manage_sw_control_response_cls": ManageSWControlResponse,
                    "set_effect_sync_correction_cls": SetEffectSyncCorrection,
                    "set_effect_sync_correction_response_cls": SetEffectSyncCorrectionResponse,
                    "manage_rgb_power_mode_config_cls": ManageRgbPowerModeConfig,
                    "manage_rgb_power_mode_config_response_cls": ManageRgbPowerModeConfigResponse,
                    "manage_rgb_power_mode_cls": ManageRgbPowerMode,
                    "manage_rgb_power_mode_response_cls": ManageRgbPowerModeResponse,
                    "shutdown_cls": Shutdown,
                    "shutdown_response_cls": ShutdownResponse,
                    "effect_sync_event_cls": EffectSyncEvent,
                    "user_activity_event_cls": UserActivityEvent,
                    "rgb_cluster_changed_event": RgbClusterChangedEvent,
                },
                "max_function_index": 9
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Tests ``RGBEffectsFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(RGBEffectsFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Tests ``RGBEffectsFactory`` with out of range versions
        """
        for version in [5, 6]:
            with self.assertRaises(KeyError):
                RGBEffectsFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``RGBEffectsFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = RGBEffectsFactory.create(version)
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
        """
        for version, expected in self.expected.items():
            obj = RGBEffectsFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class RGBEffectsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
