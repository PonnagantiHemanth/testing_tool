#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.rgbconfigurations.commonrgbconfiguration
:brief: Common RGB effect configuration
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/02/14
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
@unique
class RgbLedIndicator(IntEnum):
    """
    LED indicators that overwrite RGB effects
    """
    BATTERY = auto()
    LIGHT_SPEED = auto()
    BLE = auto()
    CONNECTIVITY = auto()
    DIMMING = auto()
    GAMING_MODE = auto()
    FKC_TOGGLE = auto()
    FN_KEY = auto()
    CAPSLOCK = auto()
    MEDIA_PREVIOUS = auto()
    MEDIA_NEXT = auto()
    MEDIA_PLAY = auto()
    MEDIA_MUTE = auto()
    M1 = auto()
    M2 = auto()
    M3 = auto()
    MR = auto()
# end class RgbLedIndicator


@unique
class PwmDriverBitMode(IntEnum):
    """
    Number of bits to set pwm on LED driver
    """
    PWM_8_BITS_MODE = auto()
    PWM_12_BITS_MODE = auto()
    PWM_16_BITS_MODE = auto()
# end class PwmDriverBitMode


PWM_DRIVER_BIT_MODE_STR_MAP = {
    PwmDriverBitMode.PWM_8_BITS_MODE: 'u8 bits',
    PwmDriverBitMode.PWM_12_BITS_MODE: 'u12 bits',
    PwmDriverBitMode.PWM_16_BITS_MODE: 'u16 bits',
}


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class RgbConfigurationMixin:
    """
    Common implementation class for RGB effect configuration.
    """
    # Not mounted LEDs
    NOT_MOUNTED_LEDS_MAIN_ALL_LAYOUT = []
    NOT_MOUNTED_LEDS_EDGE_ALL_LAYOUT = []
    NOT_MOUNTED_LEDS_MAIN_US_LAYOUT = []
    NOT_MOUNTED_LEDS_MAIN_UK_LAYOUT = []
    NOT_MOUNTED_LEDS_MAIN_JP_LAYOUT = []
    NOT_MOUNTED_LEDS_MAIN_BR_LAYOUT = []
    NOT_MOUNTED_LEDS_MAIN_RU_LAYOUT = []

    # Range Zone_ID main
    MAIN_KEYS_LED_ID_RANGE = range(0, 0)
    EDGE_LIGHTING_LED_ID_RANGE = range(0, 0)

    # LED indicators present on the product and associated LED ID
    INDICATOR_TO_LED_ID = {}

    # LED indicators where the calibration coefficient is stored in calibration zone
    INDICATOR_ON_MEDIA_ZONE_CALIBRATION = []

    # LED indicators that are not affected by rgb effect
    INDICATOR_NOT_AFFECTED_BY_RGB_EFFECT = []

    # Breathing
    RGB_BREATHING_FRAME_RATE = 16.0  # in ms

    # Color cycling
    RGB_COLOR_CYCLING_FRAME_RATE = 16.0  # in ms

    # Number of bits to set pwm on LED driver
    PWM_DRIVER_BIT_MODE = PwmDriverBitMode.PWM_16_BITS_MODE

    # Immersive lighting state machine duration
    STARTUP_DURATION = 6  # in s
    SHUTDOWN_DURATION = 6  # in s
    OOB_NO_ACTIVITY_TO_POWER_SAVE_DURATION = 60  # in s
    OOB_NO_ACTIVITY_TO_OFF_DURATION = 60 * 6  # in s
# end class RgbConfigurationMixin

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
