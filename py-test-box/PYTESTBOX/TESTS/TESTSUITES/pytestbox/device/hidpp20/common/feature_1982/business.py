#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1982.business
:brief: HID++ 2.0 ``Backlight`` business test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import random
import warnings
from time import sleep
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.backlight import Backlight
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.config.backlightconfiguration import GET_BACKLIGHT_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.i2c.i2cbacklightparser import BacklightEffectType
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_1982.backlight import BacklightTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_GET_BACKLIGHT_INFO_REQUEST = "Send GetBacklightInfo request"
_SET_BACKLIGHT_CONFIG_REQUEST = "Send SetBacklightConfig request"
_REACTION_FADE_OUT_DURATION_MARGIN = 0.1  # in second


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightBusinessTestCase(BacklightTestCase):
    """
    Validate ``Backlight`` business test cases
    """

    @features("Feature1982")
    @level('Business', 'SmokeTests')
    def test_enable_disable_backlight(self):
        """
        Validate that we can enable or disable the backlightEffect
        """
        self.post_requisite_reload_nvs = True
        default_options = Utils.get_default_options(self)

        for config in Backlight.Configuration:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_backlight_config(test_case=self, configuration=config, options=default_options)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetBacklightConfig request")
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check configuration field in GetBacklightConfig response")
            # ----------------------------------------------------------------------------------------------------------
            Utils.GetBacklightConfigResponseChecker.check_configuration(self, get_backlight_config_resp, config)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check backlightStatus field in GetBacklightInfo response")
            # ----------------------------------------------------------------------------------------------------------
            backlight_status = Backlight.BacklightStatus.ALS_AUTOMATIC_MODE \
                if config == Backlight.Configuration.ENABLE else Backlight.BacklightStatus.DISABLED_BY_SW

            Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                         backlight_status)
        # end for

        self.testCaseChecked("BUS_1982_0001", _AUTHOR)
    # end def test_enable_disable_backlight

    @features("Feature1982v2+")
    @level("Business")
    def test_all_backlight_effects_by_set_backlight_config(self):
        """
        Validate all supported backlightEffects by ``setBacklightConfig``
        """
        self.post_requisite_reload_nvs = True
        default_options = Utils.get_default_options(self)
        supported_backlight_effects = Utils.get_supported_backlight_effects(self)

        for effect in supported_backlight_effects:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_backlight_config(self,
                                                   configuration=Backlight.Configuration.ENABLE,
                                                   options=default_options,
                                                   backlight_effect=effect)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check backlightStatus and all supported backlightEffects")
            # ----------------------------------------------------------------------------------------------------------
            Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                         Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
            Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, effect)
        # end for

        self.testCaseChecked("BUS_1982_0002", _AUTHOR)
    # end def test_all_backlight_effects_by_set_backlight_config

    @features("Feature1982v2+")
    @level("Business")
    def test_all_backlight_effects_by_set_backlight_effect(self):
        """
        Validate all supported backlightEffects by ``setBacklightEffect``
        """
        supported_backlight_effects = Utils.get_supported_backlight_effects(self)

        for effect in supported_backlight_effects:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetBacklightEffect request")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_backlight_effect(self, backlight_effect=HexList(effect))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check backlightStatus and all the supported backlightEffects")
            # ----------------------------------------------------------------------------------------------------------
            Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                         Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
            Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, effect)
        # end for

        self.testCaseChecked("BUS_1982_0003", _AUTHOR)
    # end def test_all_backlight_effects_by_set_backlight_effect

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.STATIC)
    @level('Business')
    @services('BacklightMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_static_backlight_effect_on_all_level_by_backlight_monitoring(self):
        """
        Validate the Static Backlight Effect behaviour (value and fade in/out) on all the brightness level from
        max to min by backlight monitoring
        """
        self.post_requisite_reload_nvs = True
        number_of_level = int(self.config.F_NumberOfLevel)
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_20_PERCENT_MARGIN

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with static effect')
        # --------------------------------------------------------------------------------------------------------------
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               backlight_effect=Backlight.BacklightEffect.STATIC_EFFECT,
                                               current_backlight_level=number_of_level - 1)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
        # --------------------------------------------------------------------------------------------------------------
        sleep(backlight_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Static requirements by backlight monitoring on level '
                                  f'{number_of_level - 1}')
        # ----------------------------------------------------------------------------------------------------------
        level_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LEVEL_PWM_VALUE[number_of_level - 1]
        max_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].MAX_PWM_VALUE
        duration_fade_in_by_level = backlight_duration_fade_in * level_pwm_value / max_pwm_value
        duration_fade_out_by_level = backlight_duration_fade_out * level_pwm_value / max_pwm_value

        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.STATIC_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              fade_in_phase_duration=duration_fade_in_by_level,
                                                              level=number_of_level - 1,
                                                              fade_out_phase_duration=duration_fade_out_by_level)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect from max to min level by led driver ic spy")
        # --------------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            current_level = number_of_level - 1 - press - 1
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press backlight - button to  decrease the backlight level")
            # --------------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # --------------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.start_monitoring(self)
            # Wait 1 second to be able to verify that no effect is played before interacting with the device
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.proximity_sensor_emulator.set_proximity_presence()
            self.button_stimuli_emulator.user_action()
            self.proximity_sensor_emulator.set_proximity_presence(enable=False)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # ----------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.stop_monitoring(self)

            if current_level != 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording starts with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the Static requirements by backlight monitoring on '
                                          f'level {current_level}')
                # ------------------------------------------------------------------------------------------------------
                level_pwm_value = (
                    GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LEVEL_PWM_VALUE[current_level])
                max_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].MAX_PWM_VALUE
                duration_fade_in_by_level = backlight_duration_fade_in * level_pwm_value / max_pwm_value
                duration_fade_out_by_level = backlight_duration_fade_out * level_pwm_value / max_pwm_value

                Utils.BacklightSpyHelper.check_backlight_requirements(
                    test_case=self,
                    effect_type=BacklightEffectType.STATIC_EFFECT,
                    led_id_to_check=led_id_to_check,
                    fade_in_phase_duration=duration_fade_in_by_level,
                    level=current_level,
                    fade_out_phase_duration=duration_fade_out_by_level)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording ends with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("BUS_1982_0004", _AUTHOR)
    # end test_static_backlight_effect_on_all_level_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.CONTRAST)
    @level('Business')
    @services('BacklightMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_contrast_backlight_effect_on_all_level_by_backlight_monitoring(self):
        """
        Validate the Contrast Backlight Effect behaviour (value and fade in/out) on all the brightness level from
        max to min by backlight monitoring
        """
        self.post_requisite_reload_nvs = True
        number_of_level = int(self.config.F_NumberOfLevel)
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_IN_GROUP_KEYS1_DURATION + \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_DELTA_GROUP_KEYS1_VS_2_DURATION + \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_IN_GROUP_KEYS2_DURATION

        backlight_duration_fade_out = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with contrast effect')
        # --------------------------------------------------------------------------------------------------------------
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               backlight_effect=Backlight.BacklightEffect.CONTRAST_EFFECT,
                                               current_backlight_level=number_of_level - 1)

        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
        # --------------------------------------------------------------------------------------------------------------
        sleep(backlight_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Contrast requirements by backlight monitoring on level '
                                  f'{number_of_level - 1}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(
            test_case=self,
            effect_type=BacklightEffectType.CONTRAST_EFFECT,
            led_id_to_check=led_id_to_check,
            fade_in_phase_duration=backlight_duration_fade_in,
            level=number_of_level - 1,
            fade_out_phase_duration=backlight_duration_fade_out)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect from max to min level by led driver ic spy")
        # --------------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            current_level = number_of_level - 1 - press - 1
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press backlight - button to  decrease the backlight level")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # ----------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.start_monitoring(self)
            # Wait 1 second to be able to verify that no effect is played before interacting with the device
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.proximity_sensor_emulator.set_proximity_presence()
            self.button_stimuli_emulator.user_action()
            self.proximity_sensor_emulator.set_proximity_presence(enable=False)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # ----------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.stop_monitoring(self)

            if current_level != 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording starts with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the Static requirements by backlight monitoring on '
                                          f'level {current_level}')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(
                    test_case=self,
                    effect_type=BacklightEffectType.CONTRAST_EFFECT,
                    led_id_to_check=led_id_to_check,
                    fade_in_phase_duration=backlight_duration_fade_in,
                    level=current_level,
                    fade_out_phase_duration=backlight_duration_fade_out)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording ends with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0005", _AUTHOR)
    # end test_contrast_backlight_effect_on_all_level_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.BREATHING_LIGHT)
    @level('Business')
    @services('BacklightMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    @bugtracker("Backlight_BreathingEffectLevelByMonitoring")
    def test_breathing_backlight_effect_on_all_level_by_backlight_monitoring(self):
        """
        Validate the Breathing Backlight Effect behaviour (level, period and waveform) on all the brightness level from
        max to min by backlight monitoring
        """
        self.post_requisite_reload_nvs = True
        number_of_level = int(self.config.F_NumberOfLevel)
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN
        period = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].BREATHING_EFFECT_PERIOD
        three_period_duration_with_margin = 3 * period * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with breathing effect')
        # --------------------------------------------------------------------------------------------------------------
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               backlight_effect=Backlight.BacklightEffect.BREATHING_LIGHT_EFFECT,
                                               current_backlight_level=number_of_level - 1)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(delay_s=(3 * period - backlight_duration_with_margin))
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {three_period_duration_with_margin}s to monitor 3 period of breathing effect")
        # --------------------------------------------------------------------------------------------------------------
        sleep(three_period_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Contrast requirements by backlight monitoring on level '
                                  f'{number_of_level - 1}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.BREATHING_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              level=number_of_level - 1,)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect from max to min level by led driver ic spy")
        # --------------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            current_level = number_of_level - 1 - press - 1
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press backlight - button to  decrease the backlight level")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # ----------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.start_monitoring(self)
            # Wait 1 second to be able to verify that no effect is played before interacting with the device
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.proximity_sensor_emulator.set_proximity_presence()
            self.button_stimuli_emulator.user_action()
            self.kosmos.pes.delay(delay_s=(3 * period - backlight_duration_with_margin))
            self.proximity_sensor_emulator.set_proximity_presence(enable=False)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {three_period_duration_with_margin}s to monitor 3 periods of effect")
            # ----------------------------------------------------------------------------------------------------------
            sleep(three_period_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.stop_monitoring(self)

            if current_level != 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording starts with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the Breathing requirements by backlight monitoring on '
                                          f'level {current_level}')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.BREATHING_EFFECT,
                                                                      led_id_to_check=led_id_to_check,
                                                                      level=current_level)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording ends with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0006", _AUTHOR)
    # end test_breathing_backlight_effect_on_all_level_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.RANDOM)
    @level('Business')
    @services('BacklightMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_random_backlight_effect_on_all_level_by_backlight_monitoring(self):
        """
        Validate the Random Backlight Effect behaviour (value, number of led, fade in) on all the brightness level from
        max to min by backlight monitoring
        """
        self.post_requisite_reload_nvs = True
        number_of_level = int(self.config.F_NumberOfLevel)
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN
        twenty_keys_on_duration_with_margin = \
            20 * (GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].RANDOM_RAMP_UP_DURATION +
                  GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].RANDOM_RAMP_DOWN_DURATION) \
            * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with breathing effect')
        # --------------------------------------------------------------------------------------------------------------
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               backlight_effect=Backlight.BacklightEffect.RANDOM_EFFECT,
                                               current_backlight_level=number_of_level - 1)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(delay_s=(twenty_keys_on_duration_with_margin - backlight_duration_with_margin))
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {twenty_keys_on_duration_with_margin}s to monitor random effect")
        # --------------------------------------------------------------------------------------------------------------
        sleep(twenty_keys_on_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Contrast requirements by backlight monitoring on level '
                                  f'{number_of_level - 1}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.RANDOM_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              level=number_of_level - 1, )

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect from max to min level by led driver ic spy")
        # --------------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            current_level = number_of_level - 1 - press - 1
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press backlight - button to  decrease the backlight level")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # ----------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.start_monitoring(self)
            # Wait 1 second to be able to verify that no effect is played before interacting with the device
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.proximity_sensor_emulator.set_proximity_presence()
            self.button_stimuli_emulator.user_action()
            self.kosmos.pes.delay(delay_s=(twenty_keys_on_duration_with_margin - backlight_duration_with_margin))
            self.proximity_sensor_emulator.set_proximity_presence(enable=False)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {twenty_keys_on_duration_with_margin}s to monitor random effect")
            # ----------------------------------------------------------------------------------------------------------
            sleep(twenty_keys_on_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.stop_monitoring(self)

            if current_level != 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording starts with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the Random requirements by backlight monitoring on '
                                          f'level {current_level}')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.RANDOM_EFFECT,
                                                                      led_id_to_check=led_id_to_check,
                                                                      level=current_level)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording ends with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0006", _AUTHOR)
    # end test_random_backlight_effect_on_all_level_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.WAVES)
    @level('Business')
    @services('BacklightMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_waves_backlight_effect_on_all_level_by_backlight_monitoring(self):
        """
        Validate the Waves Backlight Effect behaviour (value, period, waveform) on all the brightness level from
        max to min by backlight monitoring
        """
        self.post_requisite_reload_nvs = True
        number_of_level = int(self.config.F_NumberOfLevel)
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN
        period = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].WAVES_EFFECT_PERIOD
        three_period_duration_with_margin = 3 * period * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with waves effect')
        # --------------------------------------------------------------------------------------------------------------
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               backlight_effect=Backlight.BacklightEffect.WAVES_EFFECT,
                                               current_backlight_level=number_of_level - 1)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(delay_s=(3 * period - backlight_duration_with_margin))
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {three_period_duration_with_margin}s to monitor 3 period of waves effect")
        # --------------------------------------------------------------------------------------------------------------
        sleep(three_period_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Waves requirements by backlight monitoring on level '
                                  f'{number_of_level - 1}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.WAVES_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              level=number_of_level - 1, )

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect from max to min level by led driver ic spy")
        # --------------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            current_level = number_of_level - 1 - press - 1
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press backlight - button to  decrease the backlight level")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # ----------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.start_monitoring(self)
            # Wait 1 second to be able to verify that no effect is played before interacting with the device
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set proximity presence, user action and remove proximity presence")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.proximity_sensor_emulator.set_proximity_presence()
            self.button_stimuli_emulator.user_action()
            self.kosmos.pes.delay(delay_s=(3 * period - backlight_duration_with_margin))
            self.proximity_sensor_emulator.set_proximity_presence(enable=False)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {three_period_duration_with_margin}s to monitor 3 period of waves effect")
            # ----------------------------------------------------------------------------------------------------------
            sleep(three_period_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.stop_monitoring(self)

            if current_level != 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording starts with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the Random requirements by backlight monitoring on '
                                          f'level {current_level}')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.WAVES_EFFECT,
                                                                      led_id_to_check=led_id_to_check,
                                                                      level=current_level)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check recording ends with None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)

            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check None effect')
                # ------------------------------------------------------------------------------------------------------
                Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                      effect_type=BacklightEffectType.NONE_EFFECT,
                                                                      led_id_to_check=led_id_to_check)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0007", _AUTHOR)
    # end test_waves_backlight_effect_on_all_level_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.NONE)
    @level('Business')
    @services('BacklightMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_none_backlight_effect_on_all_level_by_backlight_monitoring(self):
        """
        Validate the None Backlight Effect behaviour (value and fade in/out) on all the brightness level from
        max to min and min to max by backlight monitoring
        """
        self.post_requisite_reload_nvs = True
        number_of_level = int(self.config.F_NumberOfLevel)
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with none effect')
        # --------------------------------------------------------------------------------------------------------------
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               backlight_effect=Backlight.BacklightEffect.NONE_EFFECT,
                                               current_backlight_level=number_of_level - 1)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect on all the level by led driver ic spy")
        # ----------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring')
            # ------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.start_monitoring(self)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press backlight + button ")
            # ------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait 2 seconds to see that no effect is played after a keystroke")
            # ------------------------------------------------------------------------------------------------------
            sleep(2)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring')
            # ------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.stop_monitoring(self)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check None effect')
            # ------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                                  effect_type=BacklightEffectType.NONE_EFFECT,
                                                                  led_id_to_check=led_id_to_check)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0009", _AUTHOR)
    # end test_none_backlight_effect_on_all_level_by_backlight_monitoring

    @features("Feature1982v2+")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.WOW_S)
    @level('Business')
    @services('BacklightMonitoring')
    def test_wow_effect_by_backlight_monitoring(self):
        """
        Validate wow effect by LED Driver IC Spy.
        """
        self.post_requisite_reload_nvs = True
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        if GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].COMPLEX_EFFECT:
            led_id_to_check.remove(
                GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].KEY_ID_TO_LED_ID[KEY_ID.HOST_1])
        # end if
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        wow_effect_duration = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].WOW_EFFECT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + wow_effect_duration +
                                          backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        # Workaround to be connected faster to the receiver and avoid breathing effect for non mechanical keybooard
        # (when device is in searching mode) before the WOW effect
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Plug USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unplug_usb_charging_cable = True
        self.device.turn_on_usb_charging_cable()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power reset device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the WOW effect is finished")
        # --------------------------------------------------------------------------------------------------------------
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # Workaround to be connected faster to the receiver and avoid breathing effect (when device is in searching
        # mode) before the WOW effect
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Plug off USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_off_usb_charging_cable()
        self.post_requisite_unplug_usb_charging_cable = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # -------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the WOW requirements by the LED Driver IC Spy')
        # -------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.WOW_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              stationary_phase_duration=wow_effect_duration,
                                                              fade_in_phase_duration=backlight_duration_fade_in,
                                                              fade_out_phase_duration=backlight_duration_fade_out)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)
        self.testCaseChecked("BUS_1982_0010", _AUTHOR)
    # end def test_wow_effect_by_backlight_monitoring

    @features("Feature1982")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.CROWN_S)
    @level("Business")
    @skip("Can be tested once the kosmos is available")
    def test_crown_effect_by_led_driver_ic_spy(self):
        """
        Validate crown effect by LED Driver IC Spy.
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, configuration=Backlight.Configuration.ENABLE, options=Backlight.Options.CROWN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Trigger crown effect")
        # --------------------------------------------------------------------------------------------------------------
        warnings.warn("TODO: Kosmos is required and not ready yet")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the crown effect by the LED Driver IC Spy")
        # --------------------------------------------------------------------------------------------------------------
        warnings.warn("TODO: Kosmos is required and not ready yet")

        self.testCaseChecked("BUS_1982_0012", _AUTHOR)
    # end def test_crown_effect_by_led_driver_ic_spy

    @features("Feature1982v3+")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.PERM_MANUAL_MODE_S)
    @level("Business")
    def test_change_backlight_level_in_permanent_manual_mode(self):
        """
        [Since v3] Validate currentBacklightLevel can be changed through setBacklightConfig with bcklMode =
        Permanent Manual Mode
        """
        self.post_requisite_reload_nvs = True
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set baclMode = Permanent manual mode by setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check baclMode = Permanent manual mode by getBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            self, get_backlight_config_resp,
            (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (enable_permanent_manual_mode << 8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop backlight_level in range [0..7]")
        # --------------------------------------------------------------------------------------------------------------
        for backlight_level in range(8):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set currentBacklightLevel = {backlight_level} by setBacklightConfig")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_backlight_config(self,
                                                   configuration=Backlight.Configuration.ENABLE,
                                                   options=enable_permanent_manual_mode,
                                                   current_backlight_level=backlight_level)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check currentLevel = {backlight_level} by getBacklightInfo")
            # ----------------------------------------------------------------------------------------------------------
            backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
            checker = Utils.GetBacklightInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "current_level": (checker.check_current_level, backlight_level),
                "backlight_status": (checker.check_backlight_status, Backlight.BacklightStatus.PERMANENT_MANUAL_MODE),
            })
            checker.check_fields(self, backlight_info_resp,
                                 self.feature_1982.get_backlight_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0007", _AUTHOR)
    # end def test_change_backlight_level_in_permanent_manual_mode

    @features("Feature1982")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_DOWN, ))
    def test_set_backlight_level_to_0_by_backlight_key(self):
        """
        Validate device supports to set backlight level to 0 by HW manner.
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Compute press count that be able to set backlight level to 0")
        # --------------------------------------------------------------------------------------------------------------
        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Short press Backlight down button {press_count} times")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.BACKLIGHT_DOWN, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check currentLevel = 0 by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)

        self.testCaseChecked("BUS_1982_0008#1", _AUTHOR)
    # end def test_set_backlight_level_to_0_by_backlight_key

    @features("Feature1982v3+")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.PERM_MANUAL_MODE_S)
    @level("Business")
    def test_set_backlight_level_to_0_by_sw(self):
        """
        [Since v3] Validate device shupports to set backlight level to 0 by SW manner.
        """
        self.post_requisite_reload_nvs = True
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set baclMode = Permanent manual mode, currentBacklightLevel = 0 by "
                                 "setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check currentLevel = 0 by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)

        self.testCaseChecked("BUS_1982_0008#2", _AUTHOR)
    # end def test_set_backlight_level_to_0_by_sw

    @features("Feature1982v3+")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_DOWN, KEY_ID.BACKLIGHT_UP,))
    def test_backlight_level_synchronized_by_button_and_sw(self):
        """
        [Since v3] Validate the currentLevel changed by backlight buttons and setBacklightConfig are synchronized
        by device in Permanent Manual Mode.
        """
        self.post_requisite_reload_nvs = True
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop backlight_level in range [0..7]")
        # --------------------------------------------------------------------------------------------------------------
        for backlight_level in range(8):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set baclMode = Permanent manual mode, currentBacklightLevel = {backlight_level} "
                                     f"by setBacklightConfig")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_backlight_config(self,
                                                   configuration=Backlight.Configuration.ENABLE,
                                                   options=enable_permanent_manual_mode,
                                                   current_backlight_level=backlight_level)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check baclMode = Permanent manual mode and currentLevel = {backlight_level} "
                                      f"by getBacklightConfig")
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
            Utils.GetBacklightConfigResponseChecker.check_supported_options(
                self, get_backlight_config_resp,
                (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (enable_permanent_manual_mode << 8))
            Utils.GetBacklightConfigResponseChecker.check_current_backlight_level(self, get_backlight_config_resp,
                                                                                  backlight_level)

            ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=self.feature_1982.backlight_info_event_cls)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Short press Backlight down button")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

            if backlight_level > 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Wait backlightInfoEvent then check currentLevel = {backlight_level - 1} "
                                          f"or 0 if backlight_level = 0")
                # ------------------------------------------------------------------------------------------------------
                backlight_info_event = Utils.HIDppHelper.backlight_info_event(self)
                Utils.GetBacklightInfoResponseChecker.check_current_level(self, backlight_info_event,
                                                                          backlight_level - 1)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Short press Backlight up button")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Wait backlightInfoEvent then check currentLevel = {backlight_level} "
                                      f"or 1 if backlight_level = 0")
            # ----------------------------------------------------------------------------------------------------------
            backlight_info_event = Utils.HIDppHelper.backlight_info_event(self)
            Utils.GetBacklightInfoResponseChecker.check_current_level(self, backlight_info_event,
                                                                      backlight_level if backlight_level > 0 else 1)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0009", _AUTHOR)
    # end def test_backlight_level_synchronized_by_button_and_sw

    @features("Feature1982v3+")
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.STATIC)
    @level("Business")
    @services("ProximitySensor")
    @services("BacklightMonitoring")
    def test_backlight_hands_out_minimum_duration(self):
        """
        [Since v3] Validate the duration of backlight effect affected by backlight duration HandsOut settings set to
        minimum duration.
        """
        self.post_requisite_reload_nvs = True
        hands_out_duration = 1  # equivalent to 5 seconds
        hands_out_duration_in_seconds = hands_out_duration * Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set currDurationHandsOUT = {hands_out_duration_in_seconds}s and "
                                 f"backlightEffect = static effect by setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self),
                                               backlight_effect=Backlight.BacklightEffect.STATIC_EFFECT,
                                               curr_duration_hands_out=hands_out_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check currDurationHandsOUT = {hands_out_duration_in_seconds}s and "
                                  f"backlightEffect = static effect")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                     Backlight.BacklightEffect.STATIC_EFFECT)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_out(self, get_backlight_config_resp,
                                                                              hands_out_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate proximity presence and User action")
        # --------------------------------------------------------------------------------------------------------------
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        # Wait 1 second for complete the fade in period of the backlight effect and be in stationary phase
        sleep(1)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start backlight effect monitoring and emulate no-proximity')
        # ----------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        Utils.BacklightSpyHelper.start_monitoring(self)
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring when backlight duration hands out is reached')
        # ----------------------------------------------------------------------------------------------------------
        sleep(hands_out_duration_in_seconds * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN)
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the duration for backlight effect equals to {hands_out_duration_in_seconds}s")
        # --------------------------------------------------------------------------------------------------------------
        max_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].MAX_PWM_VALUE
        level_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LEVEL_PWM_VALUE[
            int(Numeral(get_backlight_info_resp.current_level))]
        current_level_fade_out_duration = backlight_duration_fade_out * level_pwm_value / max_pwm_value
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.STATIC_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              stationary_phase_duration=hands_out_duration_in_seconds,
                                                              fade_out_phase_duration=current_level_fade_out_duration,
                                                              previous_effect=BacklightEffectType.STATIC_EFFECT)

        self.testCaseChecked("BUS_1982_0010", _AUTHOR)
    # end def test_backlight_hands_out_minimum_duration

    @features("Feature1982v3+")
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.STATIC)
    @level("Business")
    @services("ProximitySensor")
    @services("BacklightMonitoring")
    def test_backlight_hands_in_minimum_duration(self):
        """
        [Since v3] Validate the duration of backlight effect affected by backlight duration HandsIN settings set to
        minimum duration.
        """
        self.post_requisite_reload_nvs = True
        hands_in_duration = 1  # equivalent to 5 seconds
        hands_in_duration_in_seconds = hands_in_duration * Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set currDurationHandsIN = {hands_in_duration_in_seconds}s and "
                                 f"backlightEffect = static effect by setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self),
                                               backlight_effect=Backlight.BacklightEffect.STATIC_EFFECT,
                                               curr_duration_hands_in=hands_in_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check currDurationHandsIN = {hands_in_duration_in_seconds}s and "
                                  f"backlightEffect = static effect")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                     Backlight.BacklightEffect.STATIC_EFFECT)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_in(self, get_backlight_config_resp,
                                                                             hands_in_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start backlight effect monitoring and emulate proximity')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        Utils.BacklightSpyHelper.start_monitoring(self)
        self.proximity_sensor_emulator.set_proximity_presence()
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring when backlight duration hands out is reached')
        # ----------------------------------------------------------------------------------------------------------
        sleep(hands_in_duration_in_seconds * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN)
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the duration fo backlight effect equals to {hands_in_duration_in_seconds}s")
        # --------------------------------------------------------------------------------------------------------------
        max_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].MAX_PWM_VALUE
        level_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LEVEL_PWM_VALUE[
            int(Numeral(get_backlight_info_resp.current_level))]
        current_level_fade_in_duration = backlight_duration_fade_in * level_pwm_value / max_pwm_value
        current_level_fade_out_duration = backlight_duration_fade_out * level_pwm_value / max_pwm_value
        Utils.BacklightSpyHelper.check_backlight_requirements(
            test_case=self,
            effect_type=BacklightEffectType.STATIC_EFFECT,
            led_id_to_check=led_id_to_check,
            fade_in_phase_duration=current_level_fade_in_duration,
            stationary_phase_duration=hands_in_duration_in_seconds - current_level_fade_in_duration,
            fade_out_phase_duration=current_level_fade_out_duration)

        self.testCaseChecked("BUS_1982_0011", _AUTHOR)
    # end def test_backlight_hands_in_minimum_duration

    @features("Feature1982v3+")
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.STATIC)
    @level("Business")
    @services("ProximitySensor")
    @services("BacklightMonitoring")
    def test_backlight_powered_minimum_duration(self):
        """
        [Since v3] Validate the duration of backlight effect affected by backlight duration Powered settings set to
        minimum duration.
        """
        self.post_requisite_reload_nvs = True
        powered_duration = 1  # equivalent to 5 seconds
        powered_duration_in_seconds = powered_duration * Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set currDurationPowered = {powered_duration_in_seconds}s and "
                                 f"backlightEffect = static effect by setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self),
                                               backlight_effect=Backlight.BacklightEffect.STATIC_EFFECT,
                                               curr_duration_powered=powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check currDurationPowered = {powered_duration_in_seconds}s and "
                                  f"backlightEffect = static effect")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                     Backlight.BacklightEffect.STATIC_EFFECT)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_powered(self, get_backlight_config_resp,
                                                                            powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Plug USB charging cable and emulate user action")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unplug_usb_charging_cable = True
        self.device.turn_on_usb_charging_cable()
        self.button_stimuli_emulator.user_action()
        # Wait 1 second for complete the fade in period of the backlight effect and be in stationary phase
        sleep(1)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start backlight effect monitoring and emulate user action')
        # ----------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        Utils.BacklightSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.user_action()
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring when backlight duration hands out is reached')
        # ----------------------------------------------------------------------------------------------------------
        sleep(powered_duration_in_seconds * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN)
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Plug off USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_off_usb_charging_cable()
        self.post_requisite_unplug_usb_charging_cable = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the duration for backlight effect equals to {powered_duration_in_seconds}s")
        # --------------------------------------------------------------------------------------------------------------
        max_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].MAX_PWM_VALUE
        level_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LEVEL_PWM_VALUE[
            int(Numeral(get_backlight_info_resp.current_level))]
        current_level_fade_out_duration = backlight_duration_fade_out * level_pwm_value / max_pwm_value
        Utils.BacklightSpyHelper.check_backlight_requirements(test_case=self,
                                                              effect_type=BacklightEffectType.STATIC_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              stationary_phase_duration=powered_duration_in_seconds,
                                                              fade_out_phase_duration=current_level_fade_out_duration,
                                                              previous_effect=BacklightEffectType.STATIC_EFFECT)

        self.testCaseChecked("BUS_1982_0012", _AUTHOR)
    # end def test_backlight_powered_minimum_duration

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.REACTION)
    @level('Business')
    @services('LedSpyOverI2cMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_reaction_backlight_effect_on_all_level_by_led_driver_ic_spy(self):
        """
        Validate the Reaction Backlight Effect behaviour (timing, value and fade in/out) on all the brightness level
        and on all the keys (one after the other) by LED Driver IC Spy.
        """
        self.post_requisite_reload_nvs = True

        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        key_ids = list(GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].KEY_ID_TO_LED_ID.keys())
        key_ids_to_not_used = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].BACKLIGHT_EFFECT_FORBIDDEN_KEYS
        key_ids = [ele for ele in key_ids if ele not in key_ids_to_not_used]

        make_duration = ButtonStimuliInterface.DEFAULT_DURATION
        # Need to be greater than REACTION_RAMP_DOWN_KEY_RELEASE_DURATION to take into account the duration of fade out
        # after key release
        break_duration = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].REACTION_RAMP_DOWN_KEY_RELEASE_DURATION + \
            _REACTION_FADE_OUT_DURATION_MARGIN

        # Create key make and break sequence sorted by delay
        sequence = []
        timestamp = 0
        for key_id in key_ids:
            timestamp += break_duration
            key_id_sequence = [key_id, []]
            key_id_sequence[1].append((MAKE, timestamp))

            timestamp += make_duration
            key_id_sequence[1].append((BREAK, timestamp))

            sequence.append(key_id_sequence)
        # end for
        sequence_sorted_by_delay, max_timestamp = self._sort_sequence_by_delay(sequence)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with reaction effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.REACTION_EFFECT)

        duration = Utils.compute_duration_to_max_or_min_level(self, to_max_level=False)

        if duration > 0:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press backlight down button with duration {duration}s to the min level")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, duration=duration)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check current level is O')
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect on all the level by led driver ic spy")
        # --------------------------------------------------------------------------------------------------------------
        number_of_level = int(self.config.F_NumberOfLevel)
        # --------------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press backlight + button ")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, delay=break_duration)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring and play sequence')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            Utils.BacklightSpyHelper.start_monitoring(self)
            self.button_stimuli_emulator.perform_action_list_with_multiple_delays(sequence_sorted_by_delay)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(timeout=max_timestamp + 10, block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring when sequence is finished')
            # ----------------------------------------------------------------------------------------------------------
            # Wait reaction sequence is finished with 1 second margin
            sleep(max_timestamp + 1)
            Utils.BacklightSpyHelper.stop_monitoring(self)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check reaction effect on single key press')
            # ------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.check_reaction_effect(self, sequence)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0013", _AUTHOR)
    # end test_reaction_backlight_effect_on_all_level_by_led_driver_ic_spy

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.REACTION)
    @level('Business')
    @services('LedSpyOverI2cMonitoring')
    def test_reaction_multiple_mix_keys(self):
        """
        Validate the Reaction Backlight Effect behaviour (timing, value and fade in/out) on multiple (simultaneous or
        not) pressed keys by LED Driver IC Spy.
        """
        self.post_requisite_reload_nvs = True

        number_of_trial = 10
        number_possible_keys = [2, 3, 4]
        number_possible_keystrokes = [2, 3, 4]
        delay_break_possible_values = [0.1, 0.2, 0.5, 1, 2]
        delay_make_possible_values = [0.2, 0.3, 0.5, 1, 2]

        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        key_ids = list(GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].KEY_ID_TO_LED_ID.keys())
        key_ids_to_not_used = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].BACKLIGHT_EFFECT_FORBIDDEN_KEYS
        key_ids = [ele for ele in key_ids if ele not in key_ids_to_not_used]

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with reaction effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.REACTION_EFFECT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to test multiple keystrokes combinations")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(number_of_trial):
            # Create key make and break sequence
            sequence = []
            key_number = random.choice(number_possible_keys)
            key_ids_list = key_ids.copy()
            for i in range(key_number):
                key_id = random.choice(key_ids_list)
                key_ids_list.remove(key_id)
                key_id_sequence = [key_id, []]
                keystrokes_number = random.choice(number_possible_keystrokes)
                timestamp = 0
                for j in range(2 * keystrokes_number):
                    if (j % 2) == 0:
                        action = MAKE
                        delay = random.choice(delay_make_possible_values)
                    else:
                        action = BREAK
                        delay = random.choice(delay_break_possible_values)
                    # end if
                    timestamp += delay
                    key_id_sequence[1].append((action, timestamp))
                # end for
                sequence.append(key_id_sequence)
            # end for
            sequence_sorted_by_delay, max_timestamp = self._sort_sequence_by_delay(sequence)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring and play sequence')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            Utils.BacklightSpyHelper.start_monitoring(self)
            self.button_stimuli_emulator.perform_action_list_with_multiple_delays(sequence_sorted_by_delay)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring when sequence is finished')
            # ----------------------------------------------------------------------------------------------------------
            # Wait reaction sequence is finished with 1 second margin
            sleep(max_timestamp + 1)
            Utils.BacklightSpyHelper.stop_monitoring(self)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check reaction effect on multiple key press')
            # ------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.check_reaction_effect(self, sequence)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1982_0014", _AUTHOR)
    # end def test_reaction_multiple_mix_keys
# end class BacklightBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
