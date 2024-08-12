#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8071.functionality
:brief: HID++ 2.0 ``RGBEffects`` functionality test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.config.rgbconfiguration import GET_RGB_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.i2c.rgbparser import ImmersiveLightingState
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.hidpp20.gaming.feature_8071.rgbeffects import RGBEffectsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"
_LED_INDICATOR_TIMEOUT = 5  # in seconds
_ONE_SECOND = 1  # in seconds
OOB_EFFECT_DETECTION_TIME = 3  # duration needed to be sure to detect oob effect (in seconds)
SHUTDOWN_DURATION_MARGIN = 1  # in seconds
RGB_MONITORING_DURATION_MARGIN = 5  # in seconds


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RGBEffectsFunctionalityTestCase(RGBEffectsTestCase):
    """
    Validate ``RGBEffects`` functionality test cases
    """
    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.FIXED)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_fixed_effect_param1_2_3_primary(self):
        """
        Validate the Fixed effect on primary cluster can be set with param1 (red), param2 (green), param3 (blue) to
        min and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected
        values
        """
        red_values = [255, 0, 0, RandHexList(1, minVal=100).toLong()]
        green_values = [0, 255, 0, RandHexList(1, minVal=100).toLong()]
        blue_values = [0, 0, 255, RandHexList(1, minVal=100).toLong()]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param1 (red), param2 (green), param3 (blue)")
        # --------------------------------------------------------------------------------------------------------------
        for red_value, green_value, blue_value in zip(red_values, green_values, blue_values):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper.\
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set a fixed effect on primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_fixed_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY, red=red_value,
                                 green=green_value, blue=blue_value,
                                 mode=RGBEffectsTestUtils.FixedRGBEffectMode.DEFAULT,
                                 persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 1 second')
            # ----------------------------------------------------------------------------------------------------------
            sleep(_ONE_SECOND)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match fixed effect reference for the primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_fixed_effect(self, red_value=red_value, green_value=green_value, blue_value=blue_value,
                                   calibration_data=calibration_data,
                                   cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            if self.config.F_HasEdgeLedDriver:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
                # ---------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper. \
                    check_disabled_effect(self, calibration_data=calibration_data,
                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0070", _AUTHOR)
    # end def test_fixed_effect_param1_2_3_primary

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.EDGE,
              RGBEffects.RGBEffectID.FIXED)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_fixed_effect_param1_2_3_edge(self):
        """
        Validate the Fixed effect on edge cluster can be set with param1 (red), param2 (green), param3 (blue) to
        min and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected
        values
        """
        red_values = [255, 0, 0, RandHexList(1, minVal=100).toLong()]
        green_values = [0, 255, 0, RandHexList(1, minVal=100).toLong()]
        blue_values = [0, 0, 255, RandHexList(1, minVal=100).toLong()]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param1 (red), param2 (green), param3 (blue)")
        # --------------------------------------------------------------------------------------------------------------
        for red_value, green_value, blue_value in zip(red_values, green_values, blue_values):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper.\
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set a fixed effect on the edge cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_fixed_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE, red=red_value,
                                 green=green_value, blue=blue_value,
                                 mode=RGBEffectsTestUtils.FixedRGBEffectMode.DEFAULT,
                                 persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 1 second')
            # ----------------------------------------------------------------------------------------------------------
            sleep(_ONE_SECOND)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match fixed effect reference for the edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_fixed_effect(self, red_value=red_value, green_value=green_value, blue_value=blue_value,
                                   calibration_data=calibration_data,
                                   cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no effect is played on the primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(self, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0071", _AUTHOR)
    # end def test_fixed_effect_param1_2_3_edge

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
              RGBEffects.RGBEffectID.FIXED)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_fixed_effect_param1_2_3_multi_cluster(self):
        """
        Validate the Fixed effect on multi cluster can be set with param1 (red), param2 (green), param3 (blue) to
        min and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected
        values
        """
        red_values = [255, 0, 0, RandHexList(1, minVal=100).toLong()]
        green_values = [0, 255, 0, RandHexList(1, minVal=100).toLong()]
        blue_values = [0, 0, 255, RandHexList(1, minVal=100).toLong()]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable SW Control of RGB Cluster")
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait indicator leds turned off after a reset")
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param1 (red), param2 (green), param3 (blue)")
        # --------------------------------------------------------------------------------------------------------------
        for red_value, green_value, blue_value in zip(red_values, green_values, blue_values):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper.\
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set a fixed effect on the multi-cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_fixed_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER, red=red_value,
                                 green=green_value, blue=blue_value,
                                 mode=RGBEffectsTestUtils.FixedRGBEffectMode.DEFAULT,
                                 persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 1 second')
            # ----------------------------------------------------------------------------------------------------------
            sleep(_ONE_SECOND)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match fixed effect reference for the multi-cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_fixed_effect(self, red_value=red_value, green_value=green_value, blue_value=blue_value,
                                   calibration_data=calibration_data,
                                   cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0072", _AUTHOR)
    # end def test_fixed_effect_param1_2_3_multi_cluster

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param1_2_3_primary(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Primary cluster can be set with param1 (red), param2 (green)
        , param3 (blue) to min and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values
        """
        red_values = [255, 0, 0, RandHexList(1, minVal=100).toLong()]
        green_values = [0, 255, 0, RandHexList(1, minVal=100).toLong()]
        blue_values = [0, 0, 255, RandHexList(1, minVal=100).toLong()]
        brightness = 100
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param1 (red), param2 (green), param3 (blue)")
        # --------------------------------------------------------------------------------------------------------------
        for red_value, green_value, blue_value in zip(red_values, green_values, blue_values):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.\
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            if self.config.F_HasEdgeLedDriver:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
                # ---------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper. \
                    check_disabled_effect(self, calibration_data=calibration_data,
                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
            # end if

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0073", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param1_2_3_primary

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.EDGE,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param1_2_3_edge(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Edge cluster can be set with param1 (red), param2 (green)
        , param3 (blue) to min and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values
        """
        red_values = [255, 0, 0, RandHexList(1, minVal=100).toLong()]
        green_values = [0, 255, 0, RandHexList(1, minVal=100).toLong()]
        blue_values = [0, 0, 255, RandHexList(1, minVal=100).toLong()]
        brightness = 100
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param1 (red), param2 (green), param3 (blue)")
        # --------------------------------------------------------------------------------------------------------------
        for red_value, green_value, blue_value in zip(red_values, green_values, blue_values):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on edge cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no effect is played on Primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(self, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0074", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param1_2_3_edge

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param1_2_3_multi_cluster(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Multi-cluster can be set with param1 (red), param2 (green)
        , param3 (blue) to min and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values
        """
        red_values = [255, 0, 0, RandHexList(1, minVal=100).toLong()]
        green_values = [0, 255, 0, RandHexList(1, minVal=100).toLong()]
        blue_values = [0, 0, 255, RandHexList(1, minVal=100).toLong()]
        brightness = 100
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param1 (red), param2 (green), param3 (blue)")
        # --------------------------------------------------------------------------------------------------------------
        for red_value, green_value, blue_value in zip(red_values, green_values, blue_values):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on Multi-cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self,
                    cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'multi-cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0075", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param1_2_3_multi_cluster

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param_4_5_primary(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Primary cluster can be set with param7 (Period MSB)
        and param8 (Period LSB) to min and max. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values
        """
        red_value = RandHexList(1, minVal=150).toLong()
        green_value = RandHexList(1, minVal=150).toLong()
        blue_value = RandHexList(1, minVal=150).toLong()
        brightness = 100
        period_msb_values = [0, 255, RandHexList(1).toLong()]
        period_lsb_values = [255, 0, RandHexList(1).toLong()]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (Period MSB) and param8 (Period LSB)")
        # --------------------------------------------------------------------------------------------------------------
        for period_msb, period_lsb in zip(period_msb_values, period_lsb_values):
            two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000  # seconds
            max_recording_duration = 6  # seconds

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Stop RGB effect monitoring after min of (2 periods of effects or '
                                     f'{max_recording_duration}')
            # ----------------------------------------------------------------------------------------------------------
            sleep(min(two_periods_duration, max_recording_duration))
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            if self.config.F_HasEdgeLedDriver:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
                # ---------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper. \
                    check_disabled_effect(self, calibration_data=calibration_data,
                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
            # end if

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0076", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param_4_5_primary

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.EDGE,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param_4_5_edge(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Edge cluster can be set with param7 (Period MSB)
        and param8 (Period LSB) to min and max. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values
        """
        red_value = RandHexList(1, minVal=150).toLong()
        green_value = RandHexList(1, minVal=150).toLong()
        blue_value = RandHexList(1, minVal=150).toLong()
        brightness = 100
        period_msb_values = [0, 255, RandHexList(1).toLong()]
        period_lsb_values = [255, 0, RandHexList(1).toLong()]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (Period MSB) and param8 (Period LSB)")
        # --------------------------------------------------------------------------------------------------------------
        for period_msb, period_lsb in zip(period_msb_values, period_lsb_values):
            two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000  # seconds
            max_recording_duration = 6  # seconds

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on edge cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Stop RGB effect monitoring after min of (2 periods of effects or '
                                     f'{max_recording_duration}')
            # ----------------------------------------------------------------------------------------------------------
            sleep(min(two_periods_duration, max_recording_duration))
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no effect is played on Primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(self, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0077", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param_4_5_edge

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param_4_5_multi_cluster(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Multi-cluster can be set with param7 (Period MSB)
        and param8 (Period LSB) to min and max. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values
        """
        red_value = RandHexList(1, minVal=150).toLong()
        green_value = RandHexList(1, minVal=150).toLong()
        blue_value = RandHexList(1, minVal=150).toLong()
        brightness = 100
        period_msb_values = [0, 255, RandHexList(1).toLong()]
        period_lsb_values = [255, 0, RandHexList(1).toLong()]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (Period MSB) and param8 (Period LSB)")
        # --------------------------------------------------------------------------------------------------------------
        for period_msb, period_lsb in zip(period_msb_values, period_lsb_values):
            two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000  # seconds
            max_recording_duration = 6  # seconds

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on Multi-cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self,
                    cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Stop RGB effect monitoring after min of (2 periods of effects or '
                                     f'{max_recording_duration}')
            # ----------------------------------------------------------------------------------------------------------
            sleep(min(two_periods_duration, max_recording_duration))
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'multi-cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0078", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param_4_5_multi_cluster

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param7_primary(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Primary cluster can be set with param7 (intensity).
        Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected values
        """
        red_value = RandHexList(1, minVal=100).toLong()
        green_value = RandHexList(1, minVal=100).toLong()
        blue_value = RandHexList(1, minVal=100).toLong()
        brightness_values = [0, RandHexList(1).toLong(), 100, 101, 255]
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (intensity)")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in brightness_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            if self.config.F_HasEdgeLedDriver:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
                # ---------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper. \
                    check_disabled_effect(self, calibration_data=calibration_data,
                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
            # end if

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0079", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param7_primary

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param7_edge(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Primary cluster can be set with with param7 (intensity).
         Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected values
        """
        red_value = RandHexList(1, minVal=100).toLong()
        green_value = RandHexList(1, minVal=100).toLong()
        blue_value = RandHexList(1, minVal=100).toLong()
        brightness_values = [0, RandHexList(1).toLong(), 100, 101, 255]
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (intensity)")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in brightness_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on edge cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no effect is played on Primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(self, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0080", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param7_edge

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
              RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pulsing_breathing_waveform_param7_multi_cluster(self):
        """
        Validate the Pulsing/Breathing (Waveform) effect on Multi-cluster can be set with with param7 (intensity).
         Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected values
        """
        red_value = RandHexList(1, minVal=100).toLong()
        green_value = RandHexList(1, minVal=100).toLong()
        blue_value = RandHexList(1, minVal=100).toLong()
        brightness_values = [0, RandHexList(1).toLong(), 100, 101, 255]
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (intensity)")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in brightness_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set pulsing/breathing (waveform) effect on Multi-cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_pulsing_breathing_waveform_effect(
                    self,
                    cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                    red=red_value, green=green_value, blue=blue_value,
                    period_msb=period_msb, period_lsb=period_lsb,
                    waveform=RGBEffectsTestUtils.PulsingBreathingWaveformEffect.DEFAULT,
                    intensity=brightness,
                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                      'multi-cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_pulsing_breathing_effect(self, red_value=red_value, green_value=green_value,
                                               blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                               brightness=brightness, calibration_data=calibration_data,
                                               cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0081", _AUTHOR)
    # end def test_pulsing_breathing_waveform_param7_multi_cluster

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param2_primary(self):
        """
        Validate the color cycling configurable S effect on Primary cluster can be set with param2 (saturation) to min
        and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected
        values.
        """
        saturation_values = [0, RandHexList(1).toLong(), 255]
        brightness = 100
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param2 (saturation)")
        # --------------------------------------------------------------------------------------------------------------
        for saturation in saturation_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on Primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            if self.config.F_HasEdgeLedDriver:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
                # ---------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper. \
                    check_disabled_effect(self, calibration_data=calibration_data,
                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
            # end if

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0082", _AUTHOR)
    # end def test_color_cycling_configurable_s_param2_primary

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.EDGE,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param2_edge(self):
        """
        Validate the color cycling configurable S effect on Edge cluster can be set with param2 (saturation) to min
        and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected
        values.
        """
        saturation_values = [0, RandHexList(1).toLong(), 255]
        brightness = 100
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param2 (saturation)")
        # --------------------------------------------------------------------------------------------------------------
        for saturation in saturation_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect for edge cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no effect is played on Primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(self, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0083", _AUTHOR)
    # end def test_color_cycling_configurable_s_param2_edge

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param2_multi_cluster(self):
        """
        Validate the color cycling configurable S effect on Multi-cluster can be set with param2 (saturation) to min
        and max value. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected
        values.
        """
        saturation_values = [0, RandHexList(1).toLong(), 255]
        brightness = 100
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param2 (saturation)")
        # --------------------------------------------------------------------------------------------------------------
        for saturation in saturation_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on Multi-cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self,
                                                        cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'multi-cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0084", _AUTHOR)
    # end def test_color_cycling_configurable_s_param2_multi_cluster

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param7_8_primary(self):
        """
        Validate the color cycling configurable S effect on Primary cluster can be set with param7 (Period MSB) and
        param8 (Period LSB) to min and max. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values.
        """
        saturation = RandHexList(1).toLong()
        brightness = 100
        period_msb_values = [0, 255, RandHexList(1).toLong()]
        period_lsb_values = [255, 0, RandHexList(1).toLong()]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (Period MSB) and param8 (Period LSB)")
        # --------------------------------------------------------------------------------------------------------------
        for period_msb, period_lsb in zip(period_msb_values, period_lsb_values):
            two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000  # seconds
            max_recording_duration = 6  # seconds

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on Primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(min(two_periods_duration, max_recording_duration))
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            if self.config.F_HasEdgeLedDriver:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
                # ---------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper. \
                    check_disabled_effect(self, calibration_data=calibration_data,
                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
            # end if

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0085", _AUTHOR)
    # end def test_color_cycling_configurable_s_param7_8_primary

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.EDGE,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param7_8_edge(self):
        """
        Validate the color cycling configurable S effect on Edge cluster can be set with param7 (Period MSB) and
        param8 (Period LSB) to min and max. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values.
        """
        saturation = RandHexList(1).toLong()
        brightness = 100
        period_msb_values = [0, 255, RandHexList(1).toLong()]
        period_lsb_values = [255, 0, RandHexList(1).toLong()]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (Period MSB) and param8 (Period LSB)")
        # --------------------------------------------------------------------------------------------------------------
        for period_msb, period_lsb in zip(period_msb_values, period_lsb_values):
            two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000  # seconds
            max_recording_duration = 6  # seconds

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on Edge cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(min(two_periods_duration, max_recording_duration))
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(self, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0086", _AUTHOR)
    # end def test_color_cycling_configurable_s_param7_8_edge

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param7_8_multi_cluster(self):
        """
        Validate the color cycling configurable S effect on Multi-cluster can be set with param7 (Period MSB) and
        param8 (Period LSB) to min and max. Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and
        compare to the expected values.
        """
        saturation = RandHexList(1).toLong()
        brightness = 100
        period_msb_values = [0, 255, RandHexList(1).toLong()]
        period_lsb_values = [255, 0, RandHexList(1).toLong()]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param7 (Period MSB) and param8 (Period LSB)")
        # --------------------------------------------------------------------------------------------------------------
        for period_msb, period_lsb in zip(period_msb_values, period_lsb_values):
            two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000  # seconds
            max_recording_duration = 6  # seconds

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on Multi-cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self,
                                                        cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(min(two_periods_duration, max_recording_duration))
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'multi-cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0087", _AUTHOR)
    # end def test_color_cycling_configurable_s_param7_8_multi_cluster

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.PRIMARY,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param9_primary(self):
        """
        Validate the color cycling configurable S effect on Primary cluster can be set with param9 (intensity).
        Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected values.
        """
        saturation = RandHexList(1).toLong()
        brightness_values = [0, RandHexList(1).toLong(), 100, 101, 255]
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param9 (intensity)")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in brightness_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on Primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            if self.config.F_HasEdgeLedDriver:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check no effect is played on Edge cluster')
                # ---------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper. \
                    check_disabled_effect(self, calibration_data=calibration_data,
                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
            # end if

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0088", _AUTHOR)
    # end def test_color_cycling_configurable_s_param9_primary

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.EDGE,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param9_edge(self):
        """
        Validate the color cycling configurable S effect on Edge cluster can be set with param9 (intensity).
        Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected values.
        """
        saturation = RandHexList(1).toLong()
        brightness_values = [0, RandHexList(1).toLong(), 100, 101, 255]
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param9 (intensity)")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in brightness_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on EDGE cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'edge cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no effect is played on Primary cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(self, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0089", _AUTHOR)
    # end def test_color_cycling_configurable_s_param9_edge

    @features("Feature8071")
    @features("Feature8071RequiredEffect", RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
              RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_color_cycling_configurable_s_param9_multi_cluster(self):
        """
        Validate the color cycling configurable S effect on Multi-cluster can be set with param9 (intensity).
        Use Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare to the expected values.
        """
        saturation = RandHexList(1).toLong()
        brightness_values = [0, RandHexList(1).toLong(), 100, 101, 255]
        # period effect of 1s
        period_msb = 0x03
        period_lsb = 0xE8
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.\
            manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                              sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the hidden features to get access to the calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait indicator leds turned off after a reset')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_LED_INDICATOR_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of param9 (intensity)")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in brightness_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Disable effect')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set color cycling configurable S effect on Multi-cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_color_cycling_configurable_s_effect(self, 
                                                        cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                                                        saturation=saturation, period_msb=period_msb,
                                                        period_lsb=period_lsb, intensity=brightness,
                                                        persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after 2 periods of effects')
            # ----------------------------------------------------------------------------------------------------------
            sleep(two_periods_duration)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check RGB data match color cycling configurable S effect reference for the '
                                      'multi cluster')
            # ---------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_color_cycling_configurable_s_effect(self, saturation=saturation, period_msb=period_msb,
                                                          period_lsb=period_lsb, brightness=brightness,
                                                          calibration_data=calibration_data,
                                                          cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER)

            # Test too long , need to wake up the device
            self._wake_up_device()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8071_0090", _AUTHOR)
    # end def test_color_cycling_configurable_s_param9_multi_cluster

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_disable_enable_start_up_animation(self):
        """
        Validate the startup animation can be disabled or enabled
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable startup animation')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.manage_nv_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.GET,
            nv_capabilities=RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT)
        RGBEffectsTestUtils.HIDppHelper.manage_nv_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
            nv_capabilities=RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT,
            capability_state=RGBEffectsTestUtils.NvCapabilityState.DISABLE,
            param_1=response.param_1, param_2=response.param_2, param_3=response.param_3,
            param_4=response.param_4, param_5=response.param_5, param_6=response.param_6)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and power on the dut')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.power_slider_emulator.power_on()
        self.post_requisite_power_on_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 3 seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable startup animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_nv_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
            nv_capabilities=RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT,
            capability_state=RGBEffectsTestUtils.NvCapabilityState.ENABLE,
            param_1=response.param_1, param_2=response.param_2, param_3=response.param_3,
            param_4=response.param_4, param_5=response.param_5, param_6=response.param_6)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and power on the dut')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.power_slider_emulator.power_on()
        self.post_requisite_power_on_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 3 seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with startup animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.START_UP)

        self.testCaseChecked("FUN_8071_0058", _AUTHOR)
    # end def test_disable_enable_start_up_animation

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_disable_enable_shutdown_animation(self):
        """
        Validate the shutdown animation can be disabled or enabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable shutdown animation')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.manage_nv_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.GET,
            nv_capabilities=RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
        RGBEffectsTestUtils.HIDppHelper.manage_nv_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
            nv_capabilities=RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT,
            capability_state=RGBEffectsTestUtils.NvCapabilityState.DISABLE,
            param_1=response.param_1, param_2=response.param_2, param_3=response.param_3,
            param_4=response.param_4, param_5=response.param_5, param_6=response.param_6)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 3 seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_on()
        self.post_requisite_power_on_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with no animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable shutdown animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_nv_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
            nv_capabilities=RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT,
            capability_state=RGBEffectsTestUtils.NvCapabilityState.ENABLE,
            param_1=response.param_1, param_2=response.param_2, param_3=response.param_3,
            param_4=response.param_4, param_5=response.param_5, param_6=response.param_6)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 3 seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_on()
        self.post_requisite_power_on_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with shutdown animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN)

        self.testCaseChecked("FUN_8071_0061", _AUTHOR)
    # end def test_disable_enable_shutdown_animation

    @features("Feature8071")
    @level("Functionality")
    @services("RGBMonitoring")
    def test_no_effect_when_device_is_off(self):
        """
        Validate no immersive lighting is played when the device is off
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start device charging and wait 3 seconds")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_turn_off_usb_charging_cable = True
        if self.power_supply_emulator is not None:
            self.power_supply_emulator.recharge(enable=True)
        # end if
        self.device.turn_on_usb_charging_cable()
        sleep(OOB_EFFECT_DETECTION_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop device charging and wait 3 seconds")
        # --------------------------------------------------------------------------------------------------------------
        if self.power_supply_emulator is not None:
            self.power_supply_emulator.recharge(enable=False)
        # end if
        self.device.turn_off_usb_charging_cable()
        self.post_requisite_turn_off_usb_charging_cable = False
        sleep(OOB_EFFECT_DETECTION_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_on()
        self.post_requisite_power_on_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get info about device')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.get_info_about_device(self)

        if (to_int(response.nv_capabilities) & RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT) == \
                RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check immersive lighting shutdown animation')
            # -------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
                self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting is off at the end of the record')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0062", _AUTHOR)
    # end def test_no_effect_when_device_is_off

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT)
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_startup_animation_and_power_off(self):
        """
        Validate the transition between startup animation and power off animation
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT, wait 3s (to be able to detect the effect), power off the DUT and '
                                 'wait the shutdown animation duration')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.power_slider_emulator.power_on()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.power_slider_emulator.power_off()
        self.kosmos.pes.delay(shutdown_duration + SHUTDOWN_DURATION_MARGIN + OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with startup animation and then shutdown animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.START_UP, exact_duration=OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=shutdown_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0090", _AUTHOR)
    # end def test_startup_animation_and_power_off

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_startup_animation_transition_to_active_animation_when_no_user_action(self):
        """
        Validate the transition between startup animation and active animation appends after the expected duration
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        startup_duration = rgb_configuration.STARTUP_DURATION
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT and wait the necessary duration to see transition between startup '
                                 'animation and active animation')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_on()
        self.post_requisite_power_on_device = False
        sleep(startup_duration + RGB_MONITORING_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with startup animation and then active animation is'
                                  ' played after the expected duration')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.START_UP, exact_duration=startup_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, last_effect=True)

        self.testCaseChecked("FUN_8071_0091", _AUTHOR)
    # end def test_startup_animation_transition_to_active_animation_when_no_user_action

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_startup_animation_transition_to_active_animation_when_user_action(self):
        """
        Validate the transition between startup animation and active animation appends before the expected startup
        duration when a user action is done before the end of the startup animation
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT, wait 3s (to be able to detect the effect), do user action and '
                                 'wait 3s (to be able to detect the effect)')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.power_slider_emulator.power_on()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        self.post_requisite_power_on_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with startup animation and then active animation is'
                                  ' played after the expected duration')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.START_UP, exact_duration=OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, last_effect=True)

        self.testCaseChecked("FUN_8071_0092", _AUTHOR)
    # end def test_startup_animation_transition_to_active_animation_when_user_action

    @features("Feature8071v4+")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.BOOT_UP_EFFECT)
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_startup_animation_and_pc_shutdown(self):
        """
        Validate the transition between active animation and shutdown animation when sending shutdown() hidpp command
        and shutdown effect is enabled
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_device = True
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT and wait 3s (to be able to detect the effect)')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.power_slider_emulator.power_on()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        self.post_requisite_power_on_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send pc shutdown')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.shutdown(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait the shutdown animation duration and stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN + OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with startup animation and then shutdown animation '
                                  'after pc shutdown message')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.START_UP, exact_duration=OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=shutdown_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0093", _AUTHOR)
    # end def test_startup_animation_and_pc_shutdown

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_active_animation_and_power_off(self):
        """
        Validate the transition between active animation and shutdown animation when power off the dut
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Start RGB effect monitoring, '
                                 f'Do user action, wait {OOB_EFFECT_DETECTION_TIME}s, power off the dut and wait the '
                                 'necessary duration to be sure no more effect is played')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.power_slider_emulator.power_off()
        self.kosmos.pes.delay(shutdown_duration + SHUTDOWN_DURATION_MARGIN + OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        self.post_requisite_power_on_device = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation and then shutdown animation '
                                  'after powered off the dut')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=OOB_EFFECT_DETECTION_TIME,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=shutdown_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0094", _AUTHOR)
    # end def test_active_animation_and_power_off

    @features("Feature8071v4+")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_active_animation_and_pc_shutdown_enable(self):
        """
        Validate the transition between active animation and shutdown animation when sending shutdown() hidpp command
        and shutdown effect is enabled
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Start RGB effect monitoring, '
                                 f'Do user action, wait {OOB_EFFECT_DETECTION_TIME}s, send shutdown hidpp command '
                                 f'and wait the necessary duration to be sure no more effect is played')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        RGBEffectsTestUtils.HIDppHelper.shutdown(self)
        sleep(shutdown_duration + OOB_EFFECT_DETECTION_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation and then shutdown animation '
                                  'after powered off the dut')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=OOB_EFFECT_DETECTION_TIME,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=shutdown_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0095", _AUTHOR)
    # end def test_active_animation_and_pc_shutdown_enable

    @features("Feature8071")
    @level("Functionality")
    @services("RGBMonitoring")
    def test_active_animation_transition_to_passive_animation_oob_duration(self):
        """
        Validate the transition between active animation and passive animation
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        active_duration = rgb_configuration.OOB_NO_ACTIVITY_TO_POWER_SAVE_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and perform user action')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after the expected time to capture passive animation')
        # --------------------------------------------------------------------------------------------------------------
        sleep(active_duration + RGB_MONITORING_DURATION_MARGIN)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation and then passive animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=active_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE)

        self.testCaseChecked("FUN_8071_0096", _AUTHOR)
    # end def test_active_animation_transition_to_passive_animation_oob_duration

    @features("Feature8071")
    @level("Functionality")
    @services("RGBMonitoring")
    def test_active_animation_transition_to_passive_animation_non_default_duration(self):
        """
        Validate the transition between active animation and passive animation with non default duration
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        active_durations = [5, rgb_configuration.OOB_NO_ACTIVITY_TO_POWER_SAVE_DURATION + 5]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get rgb power mode configuration response')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with different values of active duration")
        # --------------------------------------------------------------------------------------------------------------
        for active_duration in active_durations:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure rgbNoActTimeoutToPSave to {active_duration} seconds and")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
                self,
                get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                rgb_no_act_timeout_to_psave=active_duration,
                rgb_no_act_timeout_to_off=to_int(response.rgb_no_act_timeout_to_off))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure '
                                     'active animation is played')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start RGB effect monitoring and perform user action')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop RGB effect monitoring after the expected time to capture passive animation')
            # ----------------------------------------------------------------------------------------------------------
            sleep(active_duration + RGB_MONITORING_DURATION_MARGIN)
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check immersive lighting starts with active animation and then passive '
                                      'animation')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
                self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=active_duration,
                previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
            RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
                self, immersive_lighting_state=ImmersiveLightingState.PASSIVE)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8071_0097", _AUTHOR)
    # end def test_active_animation_transition_to_passive_animation_non_default_duration

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_passive_animation_and_power_off(self):
        """
        Validate the transition between passive animation and shutdown animation when power off the dut
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION
        rgb_no_act_timeout_to_psave = 5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get rgb power mode configuration response')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Configure rgbNoActTimeoutToPSave to {rgb_no_act_timeout_to_psave}s to have a faster '
                                 f'test')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET, rgb_no_act_timeout_to_psave=rgb_no_act_timeout_to_psave,
            rgb_no_act_timeout_to_off=to_int(response.rgb_no_act_timeout_to_off))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Start RGB effect monitoring, Do user action and wait the necessary duration to be '
                                 f'sure passive animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(rgb_no_act_timeout_to_psave)  # transition from active to passive
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)  # to be able to detect passive animation
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation and then passive animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=rgb_no_act_timeout_to_psave,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, last_effect=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and power off the dut')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.power_slider_emulator.power_off()
        self.kosmos.pes.delay(shutdown_duration + SHUTDOWN_DURATION_MARGIN + OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        self.post_requisite_power_on_device = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with passive animation and then power off animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, exact_duration=OOB_EFFECT_DETECTION_TIME,
            previous_immersive_lighting_state=ImmersiveLightingState.PASSIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=shutdown_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0098", _AUTHOR)
    # end def test_passive_animation_and_power_off

    @features("Feature8071v4+")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_passive_animation_and_pc_shutdown(self):
        """
        Validate the transition between passive animation and shutdown animation when sending shutdown() hidpp command
        and shutdown effect is enabled
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION
        rgb_no_act_timeout_to_psave = 5
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get rgb power mode configuration response')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Configure rgbNoActTimeoutToPSave to {rgb_no_act_timeout_to_psave}s to have a faster '
                                 f'test')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET, rgb_no_act_timeout_to_psave=rgb_no_act_timeout_to_psave,
            rgb_no_act_timeout_to_off=to_int(response.rgb_no_act_timeout_to_off))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action, wait the necessary duration to be sure passive animation is '
                                 'played and send shutdown hidpp command')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(rgb_no_act_timeout_to_psave)  # transition from active to passive
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)  # to be able to detect passive animation
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        RGBEffectsTestUtils.HIDppHelper.shutdown(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring when shutdown animation is over')
        # --------------------------------------------------------------------------------------------------------------
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation and then shutdown animation '
                                  'after powered off the dut')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=rgb_no_act_timeout_to_psave,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, exact_duration=OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=shutdown_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0099", _AUTHOR)
    # end def test_passive_animation_and_pc_shutdown

    @features("Feature8071")
    @level("Functionality")
    @services("RGBMonitoring")
    def test_passive_animation_transition_to_deep_sleep_oob_duration(self):
        """
        Validate the transition between passive animation and deep spleep with oob duration
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        active_to_passive_duration = 5
        passive_to_off_duration = rgb_configuration.OOB_NO_ACTIVITY_TO_OFF_DURATION - active_to_passive_duration

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get rgb power mode configuration response')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Configure rgbNoActTimeoutToPSave to {active_to_passive_duration}s to have a faster '
                                 f'test')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET, rgb_no_act_timeout_to_psave=active_to_passive_duration,
            rgb_no_act_timeout_to_off=to_int(response.rgb_no_act_timeout_to_off))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and perform user action')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after the expected duration to be in deep sleep')
        # --------------------------------------------------------------------------------------------------------------
        sleep(active_to_passive_duration + passive_to_off_duration + RGB_MONITORING_DURATION_MARGIN)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation, then passive animation and '
                                  'finally off animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=active_to_passive_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, exact_duration=passive_to_off_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0100", _AUTHOR)
    # end def test_passive_animation_transition_to_deep_sleep_oob_duration

    @features("Feature8071")
    @level("Functionality")
    @services("RGBMonitoring")
    def test_passive_animation_transition_to_deep_sleep_non_default_duration(self):
        """
        Validate the transition between passive animation and deep spleep with non default duration
        """
        active_to_passive_duration = 5
        passive_to_off_duration = 40

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Configure rgbNoActTimeoutToPSave to {active_to_passive_duration} seconds and '
                                 f'rgb_no_act_timeout_to_off to {active_to_passive_duration + passive_to_off_duration}'
                                 f'to have a faster test')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper. \
            manage_rgb_power_mode_config(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                                         rgb_no_act_timeout_to_psave=active_to_passive_duration,
                                         rgb_no_act_timeout_to_off=active_to_passive_duration + passive_to_off_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and perform user action')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after the expected duration to be in deep sleep')
        # --------------------------------------------------------------------------------------------------------------
        sleep(active_to_passive_duration + passive_to_off_duration + RGB_MONITORING_DURATION_MARGIN)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation, then passive animation and '
                                  'finally off animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=active_to_passive_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, exact_duration=passive_to_off_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0101", _AUTHOR)
    # end def test_passive_animation_transition_to_deep_sleep_non_default_duration

    @features("Feature8071")
    @level("Functionality")
    @services("RGBMonitoring")
    def test_passive_animation_transition_to_active_animation(self):
        """
        Validate the transition between passive animation and active animation
        """
        active_to_passive_duration = 5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get rgb power mode configuration response')
        # --------------------------------------------------------------------------------------------------------------
        response = RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Configure rgbNoActTimeoutToPSave to {active_to_passive_duration}s to have a faster '
                                 f'test')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET, rgb_no_act_timeout_to_psave=active_to_passive_duration,
            rgb_no_act_timeout_to_off=to_int(response.rgb_no_act_timeout_to_off))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action, wait the necessary duration to be sure passive animation '
                                 'is played and do user action')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(active_to_passive_duration)  # transition from active to passive
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)  # to be able to detect passive animation
        self.button_stimuli_emulator.user_action()
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 3s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation, then passive animation and '
                                  'finally active animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=active_to_passive_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, exact_duration=OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, last_effect=True)

        self.testCaseChecked("FUN_8071_0102", _AUTHOR)
    # end def test_passive_animation_transition_to_active_animation

    @features("Feature8071")
    @level("Functionality")
    @services("RGBMonitoring")
    def test_deep_sleep_transition_to_active_animation(self):
        """
        Validate the transition between deep spleep and active animation
        """
        active_to_passive_duration = 5
        passive_to_off_duration = 40
        off_duration = 5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Configure rgbNoActTimeoutToPSave to {active_to_passive_duration} seconds and '
                                 f'rgb_no_act_timeout_to_off to {active_to_passive_duration + passive_to_off_duration}'
                                 f'to have a faster test')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET, rgb_no_act_timeout_to_psave=active_to_passive_duration,
            rgb_no_act_timeout_to_off=active_to_passive_duration + passive_to_off_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and perform user action')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()

        wait_duration = active_to_passive_duration + passive_to_off_duration + OOB_EFFECT_DETECTION_TIME + \
            RGB_MONITORING_DURATION_MARGIN
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Stop RGB effect monitoring after {wait_duration}s to be sure no effect is played')
        # --------------------------------------------------------------------------------------------------------------
        sleep(wait_duration)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation, then passive animation and '
                                  'finally leds are off')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=active_to_passive_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, exact_duration=passive_to_off_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Start RGB effect monitoring and perform user action after {off_duration}s')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.delay(off_duration)
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with no animation, then active animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, exact_duration=off_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.OFF)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, last_effect=True)

        self.testCaseChecked("FUN_8071_0103", _AUTHOR)
    # end def test_deep_sleep_transition_to_active_animation

    @features("Feature8071")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_deep_sleep_transition_and_power_off(self):
        """
        Validate the transition between deep sleep and power off animation
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION
        active_to_passive_duration = 5
        passive_to_off_duration = 40
        off_duration = 5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Configure rgbNoActTimeoutToPSave to {active_to_passive_duration} seconds and '
                                 f'rgb_no_act_timeout_to_off to {active_to_passive_duration + passive_to_off_duration}'
                                 f'to have a faster test')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET, rgb_no_act_timeout_to_psave=active_to_passive_duration,
            rgb_no_act_timeout_to_off=active_to_passive_duration + passive_to_off_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform user action to be in active animation state and wait 1s to be sure active '
                                 'animation is played')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and perform user action')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()

        wait_duration = active_to_passive_duration + passive_to_off_duration + OOB_EFFECT_DETECTION_TIME + \
            RGB_MONITORING_DURATION_MARGIN
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Stop RGB effect monitoring after {wait_duration}s to be sure no effect is played')
        # --------------------------------------------------------------------------------------------------------------
        sleep(wait_duration)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with active animation, then passive animation and '
                                  'finally leds are off')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, exact_duration=active_to_passive_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.ACTIVE)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.PASSIVE, exact_duration=passive_to_off_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Start RGB effect monitoring and power off the DUT after {off_duration}s')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.delay(off_duration)
        self.power_slider_emulator.power_off()
        self.kosmos.pes.delay(shutdown_duration + OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        self.post_requisite_power_on_device = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with no animation, then power off animation and '
                                  'finally leds off')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, exact_duration=off_duration,
            previous_immersive_lighting_state=ImmersiveLightingState.OFF)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=shutdown_duration)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.OFF, last_effect=True)

        self.testCaseChecked("FUN_8071_0104", _AUTHOR)
    # end def test_deep_sleep_transition_and_power_off

    @features("Feature8071v4+")
    @features("Feature8071RequiredNvCapability", RGBEffectsTestUtils.NvCapabilities.SHUTDOWN_EFFECT)
    @level("Functionality")
    @services("RGBMonitoring")
    def test_pc_shutdown_and_device_activity(self):
        """
        Validate the transition between shutdown animation (from pc shutdown) and active animation
        """
        fw_id = self.f.PRODUCT.F_ProductReference

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring and send shutdown Hidpp command')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
        RGBEffectsTestUtils.HIDppHelper.shutdown(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 3s (to be able to detect the effect) and perform user action')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(OOB_EFFECT_DETECTION_TIME)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check immersive lighting starts with shutdown animation and then active animation')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.SHUTDOWN, exact_duration=OOB_EFFECT_DETECTION_TIME)
        RGBEffectsTestUtils.RgbSpyHelper.check_immersive_lighting_with_oob_effect(
            self, immersive_lighting_state=ImmersiveLightingState.ACTIVE, last_effect=True)

        self.testCaseChecked("FUN_8071_0105", _AUTHOR)
    # end def test_pc_shutdown_and_device_activity

    def _wake_up_device(self,
                        sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS):
        """
        Wake up the device with a user action if the button stimuli emulator is available on the test setup. Else wake
        up the device with a power reset and manage SW control of RGB cluster

        :param sw_control_flags: Software control flags - OPTIONAL
        :type sw_control_flags: ``int`` or ``HexList``
        """
        if self.button_stimuli_emulator is not None:
            self.wake_up_device_with_user_action()
        elif self.power_slider_emulator is not None:
            # Turn the power slider off/on
            self.power_slider_emulator.reset()
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait indicator leds turned off after a reset")
            # ----------------------------------------------------------------------------------------------------------
            sleep(_LED_INDICATOR_TIMEOUT)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Manage SW Control of RGB Cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper.manage_sw_control(self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                                                              sw_control_flags=sw_control_flags)
        # end if
    # end def _wake_up_device
# end class RGBEffectsFunctionalityTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
