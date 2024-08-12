#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.rgbconfigurations.cinderellawirelessconfiguration.cinderellawireless
:brief: Cinderella RGB effect configuration
:author: YY Liu <yliu5@logitech.com>
:date: 2024/01/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import path
from pickle import load

from pyraspi.services.kosmos.config.rgbconfigurations.commonrgbconfiguration import PwmDriverBitMode
from pyraspi.services.kosmos.config.rgbconfigurations.commonrgbconfiguration import RgbConfigurationMixin
from pyraspi.services.kosmos.config.rgbconfigurations.commonrgbconfiguration import RgbLedIndicator


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CinderellaWirelessRgbConfiguration(RgbConfigurationMixin):
    """
    Configure the RGB effect and I2C layout of Cinderella Wireless


    For now, most of the information have been found on directly in the NPI codeline:
    https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/mpk25_cinderella_tkl/+/refs/heads/master/application/led_rgb.c
    https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/mpk25_cinderella_tkl/+/refs/heads/master/config/led_rgb_cfg.h
    or in https://drive.google.com/drive/folders/1fdjFujKVJk8hXsqXrtvMlSUY9V12Czv8
    - Non mounted led can be configured from "NM_3741_All", "NM_3746_All", "NM_3741_us", etc... but also can be found
    in the schematic
    - RGB_BREATHING_FRAME_RATE and RGB_COLOR_CYCLING_FRAME_RATE can be configured from "KEY_BREATHING_FRAMERATE"
    - INDICATOR_TO_LED_ID and INDICATOR_NOT_AFFECTED_BY_RGB_EFFECT  can be configured from
    "indicatorRGB_LedID" and "keep_on_leds"
    - INDICATOR_ON_MEDIA_ZONE_CALIBRATION has been configured according to the code line :
    "for(i=0;i<LEDRGB_CALI_INDICATIOR_ZONE_SIZE-1;i++) //Fn is not indicator calibration zone"
    But for the INDICATOR_TO_LED_ID, INDICATOR_NOT_AFFECTED_BY_RGB_EFFECT, INDICATOR_ON_MEDIA_ZONE_CALIBRATION it shall
    come from the "ESW Project Monitoring & Control" instantiated for your NPI.
    """
    # Not mounted LEDs
    NOT_MOUNTED_LEDS_MAIN_ALL_LAYOUT = [61, 62, 70, 71, 72, 81, 85, 90, 111, 112, 113, 114, 115, 116, 117]
    NOT_MOUNTED_LEDS_MAIN_US_LAYOUT = [42, 108, 54, 56, 105, 97]
    NOT_MOUNTED_LEDS_MAIN_UK_LAYOUT = [108, 54, 56, 97, 99]
    NOT_MOUNTED_LEDS_MAIN_JP_LAYOUT = [42, 99]
    NOT_MOUNTED_LEDS_MAIN_BR_LAYOUT = [54, 56, 97, 99]
    NOT_MOUNTED_LEDS_MAIN_RU_LAYOUT = [42, 108, 54, 56, 97]

    # Range Zone_ID main
    MAIN_KEYS_LED_ID_RANGE = range(1, 117)

    # LED indicators present on the product and associated LED ID
    INDICATOR_TO_LED_ID = {RgbLedIndicator.BATTERY: 65,
                           RgbLedIndicator.LIGHT_SPEED: 82,
                           RgbLedIndicator.BLE: 63,
                           RgbLedIndicator.GAMING_MODE: 73,
                           RgbLedIndicator.CAPSLOCK: 84,
                           RgbLedIndicator.FKC_TOGGLE: 2}

    # LED indicators where the calibration coefficient is stored in calibration zone
    # (RGB_LEDBIN_INFORMATION_BACKUP_ZONE2). Fn is not indicator calibration zone
    INDICATOR_ON_MEDIA_ZONE_CALIBRATION = [RgbLedIndicator.BATTERY, RgbLedIndicator.LIGHT_SPEED,
                                           RgbLedIndicator.BLE, RgbLedIndicator.GAMING_MODE]

    # LED indicators that are not affected by rgb effect
    INDICATOR_NOT_AFFECTED_BY_RGB_EFFECT = [RgbLedIndicator.BATTERY, RgbLedIndicator.LIGHT_SPEED, RgbLedIndicator.BLE,
                                            RgbLedIndicator.GAMING_MODE, RgbLedIndicator.CAPSLOCK,
                                            RgbLedIndicator.FKC_TOGGLE]

    # Breathing
    RGB_BREATHING_FRAME_RATE = 1 / 62 * 1000  # in ms

    # Number of bits to set pwm on LED driver
    PWM_DRIVER_BIT_MODE = PwmDriverBitMode.PWM_8_BITS_MODE

    # Load the OBB rgb effect reference arrays. These references are used in the rgbparser to detect and validate all
    # the transition of the immersive lighting state machine
    # Reference arrays are saved in pickle format and their type are
    # ``list[list[RgbComponents]]``, a list over the time of a list of RgbComponents for all leds on the product
    # The process of how to get these arrays can be found on :
    # https://docs.google.com/document/d/1_66ukzZN1SzdCglNKLZ0VwEXQfpD2HyacFENH1Vaqu8
    # Or records can directly be generated with
    # pytestbox.tools.rgbconfiguration.oobrgbeffectsrecordgeneration.RgbEffectsRecorder
    # using level=Tools and by filling the following 2 parameters(ACTIVE_EFFECT_ID, PASSIVE_EFFECT_ID) :
    # result can be found in PYTESTBOX/LIBS/PYRASPI/pyraspi/services/kosmos/config/rgbconfigurations/recordings
    ACTIVE_EFFECT_ID = 0x0018  # RGBEffectsTestUtils.RGBEffectID.SMOOTH_STAR_BREATHING
    PASSIVE_EFFECT_ID = 0x0019  # RGBEffectsTestUtils.RGBEffectID.SMOOTH_WAVE

    with open(path.join(path.dirname(path.abspath(__file__)), 'oob_rgb_start_up.pickle'), 'rb') as f:
        OOB_RGB_START_UP_REFERENCE = load(f)
    # end with
    with open(path.join(path.dirname(path.abspath(__file__)), 'oob_rgb_shutdown.pickle'), 'rb') as f:
        OOB_RGB_SHUTDOWN_REFERENCE = load(f)
    # end with
    with open(path.join(path.dirname(path.abspath(__file__)), 'oob_rgb_active.pickle'), 'rb') as f:
        OOB_RGB_ACTIVE_REFERENCE = load(f)
    # end with
    with open(path.join(path.dirname(path.abspath(__file__)), 'oob_rgb_passive.pickle'), 'rb') as f:
        OOB_RGB_PASSIVE_REFERENCE = load(f)
    # end with
    OOB_RGB_START_UP_FIRST_INDEX = 1
    OOB_RGB_SHUTDOWN_FIRST_INDEX = 1
    OOB_RGB_ACTIVE_FIRST_INDEX = 0
    OOB_RGB_PASSIVE_FIRST_INDEX = 1
    SAMPLE_NUMBER_TO_CHECK_FOR_REFERENCE_EFFECT = 82
# end class CinderellaWirelessRgbConfiguration

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
