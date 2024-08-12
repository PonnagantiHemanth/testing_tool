#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.i2cbacklightconfiguration.commonbacklightconfiguration
:brief: Common backlight configuration definition
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/01/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BacklightConfigurationMixin:
    """
    Common implementation class for mechanical and non mechanical keyboard backlight configuration.
    """
    # WOW and Static maximum value
    MAX_PWM_VALUE = 0xFF
    # WOW effect and fade in/out durations
    WOW_EFFECT_DURATION = 5  # in s
    FADE_IN_DURATION = 1  # in s
    FADE_OUT_DURATION = 1  # in s

    # For Inga BLE Pro On Contrast Backlight effect, the LED pwm value reach the expected level value for group keys 0
    # only at the beginning of the fadeout (https://jira.logitech.io/browse/ICFM-37). So the backlight parser is not
    # able to compute correctly the fade in/out durations without a workaround.
    # This workaround should not be enabled by default on Platform code or new NPI validation
    ENABLE_WORKAROUND_ON_CONTRAST_EFFECT = False
# end class BacklightConfigurationMixin


class MechanicalBacklightConfiguration(BacklightConfigurationMixin):
    """
    Configure the Backlight effect for Mechanical keyboard

    See https://docs.google.com/document/d/1vbOeYiJB8sEm_o2ys3NdBYvQ4SCou4HJ_-HpemeCJ0g/view
    """
    # Effect durations
    OOB_BACKLIGHT_DURATION_HANDS_OUT = 5  # in s
    OOB_BACKLIGHT_DURATION_HANDS_IN = 30  # in s
    OOB_BACKLIGHT_DURATION_POWERED = 5 * 60  # in s

    # Contrast effect
    CONTRAST_FADE_IN_GROUP_KEYS1_DURATION = 0.3  # in s
    CONTRAST_DELTA_GROUP_KEYS1_VS_2_DURATION = 0.2  # in s
    CONTRAST_FADE_IN_GROUP_KEYS2_DURATION = 0.5  # in s
    CONTRAST_FADE_OUT_DURATION = 0.5  # in s
    CONTRAST_INTENSITY_RATIO_G1_G2 = 3

    # Breathing effect
    BREATHING_EFFECT_PERIOD = 3  # in s
    BREATHING_FRAME_RATE = 0.032  # in s
    BREATHING_ZONE_NUMBER = 1  # Number of zone for breathing effect

    # Waves effect
    WAVES_EFFECT_PERIOD = 3  # in s

    # Reaction effect
    REACTION_UPDATE_LED_TIME = 0.032  # in s
    REACTION_RAMP_UP_KEY_PRESS_DURATION = 0.05  # in s
    REACTION_WAIT_KEY_RELEASE_DURATION = 0.1  # in s
    REACTION_RAMP_DOWN_KEY_RELEASE_DURATION = 0.5  # in s

    # Random effect
    RANDOM_EFFECT_LED_ON_NUMBER = 15
    RANDOM_RAMP_UP_DURATION = 0.3  # in s
    RANDOM_RAMP_DOWN_DURATION = 0.3  # in s

    # True if Backlight uses the led driver IC to drive LEDs independently. False if all leds are driven simultaneously
    COMPLEX_EFFECT = True
# end class MechanicalBacklightConfiguration


class NonMechanicalBacklightConfiguration(BacklightConfigurationMixin):
    """
    Configure the Backlight effect for Membrane keyboard

    See https://docs.google.com/document/d/1vbOeYiJB8sEm_o2ys3NdBYvQ4SCou4HJ_-HpemeCJ0g/view
    """
    # Effect durations
    OOB_BACKLIGHT_DURATION_HANDS_OUT = 15  # in s
    OOB_BACKLIGHT_DURATION_HANDS_IN = 30  # in s
    OOB_BACKLIGHT_DURATION_POWERED = 5 * 60  # in s

    # Breathing effect
    BREATHING_EFFECT_PERIOD = 3  # in s
    BREATHING_FRAME_RATE = 0.032  # in s
    BREATHING_ZONE_NUMBER = 1  # Number of zone for breathing effect

    # Level Backlight pwm value
    LEVEL_PWM_VALUE = [0x00, 0x1C, 0x27, 0x3C, 0x4E, 0x58, 0x6F, 0x97]
    LOW_LEVEL_VALUE = 0x00
    MAX_RAMP_UP_DOWN_TIME = 1  # in second

    # True if Backlight uses the led driver IC to drive LEDs independently. False if all leds are driven simultaneously
    COMPLEX_EFFECT = False
    # Only one led is driven during backlight effect
    LED_ID_AVAILABLE = [0]
# end class NonMechanicalBacklightConfiguration

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
