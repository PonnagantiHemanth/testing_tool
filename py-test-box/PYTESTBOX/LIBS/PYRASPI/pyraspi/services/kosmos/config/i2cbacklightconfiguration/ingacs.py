#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.i2cbacklightconfiguration.ingacs
:brief: Inga CS universal & For MAC keyboards key backlight configuration
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/01/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.commonbacklightconfiguration import \
    MechanicalBacklightConfiguration


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class IngaCsMacBacklightConfiguration(MechanicalBacklightConfiguration):
    """
    Configure the backlight effect and I2C layout of INGA Compact Size For MAC US layout

    For now, most of the information have been found directly in the NPI codeline:
    https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/rbk75_inga_cs_mac/+/refs/heads/master/application/led_backlight.c

    - KEY_ID_TO_LED_ID can be configured from "led_reaction_key_id" table and "getLedAddress" functions.
        Example : for Col 2, Row 0 (corresponding to KEY_ID.KEYBOARD_TAB on Key matrix map
        https://docs.google.com/spreadsheets/d/1aoQbFQDzgBQc31D6oADPxbttsl-H9oNNmVtIJnZMMi8/view#gid=0)
        led_reaction_key_id[0][2] = 32 and getLedAddress(led_reaction_key_id[0][2]) = 64
        so {KEY_ID.KEYBOARD_TAB: 64}
    - KEY_ID_CONTRAST_GROUP_KEYS1 can be configured from "LedContrast_G1" table
    - KEY_ID_CONTRAST_GROUP_KEYS2 can be configured from "LedContrast_G2" table
    - KEY_ID_WAVE_MAP_HORIZONTAL can be configured from  "LedWaveMap_H" table

    But for the last 3 elements (KEY_ID_CONTRAST_GROUP_KEYS1, KEY_ID_CONTRAST_GROUP_KEYS2, KEY_ID_WAVE_MAP_HORIZONTAL)
    it shall come from the "ESW Project Monitoring & Control" instantiated for your NPI and be defined for each
    supported physical layout
    """
    # For Inga BLE Pro On Contrast Backlight effect, the LED pwm value reach the expected level value for group keys 0
    # only at the beginning of the fadeout (https://jira.logitech.io/browse/ICFM-37). So the backlight parser is not
    # able to compute correctly the fade in/out durations without a workaround.
    # This workaround should not be enabled by default on Platform code or new NPI validation
    ENABLE_WORKAROUND_ON_CONTRAST_EFFECT = True

    # Backlight effect parameters
    # Number of backlight level
    NB_LEVEL = 8

    # Level Backlight pwm value
    LEVEL_PWM_VALUE = [0x00, 0x1C, 0x2E, 0x3C, 0x4E, 0x58, 0x6F, 0x97]
    LOW_LEVEL_VALUE = 0x01

    # Backlight Parameter
    WAVES_EFFECT_MIN_NUMBER_LED_ON = 5
    WAVES_EFFECT_MIN_NUMBER_LED_OFF = 10
    MAX_RAMP_UP_DOWN_TIME = 0.6  # in second

    # Keys that affect backlight effect
    BACKLIGHT_EFFECT_FORBIDDEN_KEYS = [KEY_ID.BACKLIGHT_DOWN,
                                       KEY_ID.BACKLIGHT_UP,
                                       KEY_ID.HOST_1,
                                       KEY_ID.HOST_2,
                                       KEY_ID.HOST_3,
                                       KEY_ID.KEYBOARD_CAPS_LOCK
                                       ]

    # I2C led driver layout
    KEY_ID_TO_LED_ID = {
        # ROW 0
        KEY_ID.KEYBOARD_ESCAPE: 1,
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: 33,
        KEY_ID.KEYBOARD_TAB: 64,
        KEY_ID.KEYBOARD_CAPS_LOCK: 95,
        KEY_ID.KEYBOARD_LEFT_SHIFT: 125,
        KEY_ID.KEYBOARD_LEFT_CONTROL: 155,
        KEY_ID.KEYBOARD_MUTE: 13,
        KEY_ID.KEYBOARD_P: 74,

        # ROW 1
        KEY_ID.HOST_1: 2,
        KEY_ID.KEYBOARD_1: 34,
        KEY_ID.KEYBOARD_Q: 65,
        KEY_ID.KEYBOARD_A: 96,
        KEY_ID.KEYBOARD_Z: 126,
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: 156,
        KEY_ID.KEYBOARD_VOLUME_DOWN: 14,
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: 91,

        # ROW 2
        KEY_ID.HOST_2: 3,
        KEY_ID.KEYBOARD_2: 35,
        KEY_ID.KEYBOARD_W: 66,
        KEY_ID.KEYBOARD_S: 97,
        KEY_ID.KEYBOARD_X: 127,
        KEY_ID.KEYBOARD_LEFT_ALT: 157,
        KEY_ID.KEYBOARD_VOLUME_UP: 31,
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: 121,

        # ROW 3
        KEY_ID.HOST_3: 4,
        KEY_ID.KEYBOARD_3: 36,
        KEY_ID.KEYBOARD_E: 67,
        KEY_ID.KEYBOARD_D: 98,
        KEY_ID.KEYBOARD_C: 128,
        KEY_ID.KEYBOARD_SPACE_BAR: 158,
        KEY_ID.DO_NOT_DISTURB: 32,
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: 122,

        # ROW 4
        KEY_ID.BACKLIGHT_DOWN: 5,
        KEY_ID.KEYBOARD_4: 37,
        KEY_ID.KEYBOARD_R: 68,
        KEY_ID.KEYBOARD_F: 99,
        KEY_ID.KEYBOARD_V: 129,
        KEY_ID.KEYBOARD_RIGHT_ALT: 159,
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: 61,
        KEY_ID.KEYBOARD_RETURN_ENTER: 123,

        # ROW 5
        KEY_ID.BACKLIGHT_UP: 6,
        KEY_ID.KEYBOARD_5: 38,
        KEY_ID.KEYBOARD_T: 69,
        KEY_ID.KEYBOARD_G: 100,
        KEY_ID.KEYBOARD_B: 130,
        KEY_ID.FN_KEY: 160,
        KEY_ID.KEYBOARD_BACKSPACE: 62,
        KEY_ID.KEYBOARD_PAGE_UP: 124,

        # ROW 6
        KEY_ID.DICTATION: 7,
        KEY_ID.KEYBOARD_6: 39,
        KEY_ID.KEYBOARD_Y: 70,
        KEY_ID.KEYBOARD_H: 101,
        KEY_ID.KEYBOARD_N: 131,
        KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION: 161,
        KEY_ID.KEYBOARD_HOME: 63,
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: 151,

        # ROW 7
        KEY_ID.EMOJI_PANEL: 8,
        KEY_ID.KEYBOARD_7: 40,
        KEY_ID.KEYBOARD_U: 71,
        KEY_ID.KEYBOARD_J: 102,
        KEY_ID.KEYBOARD_M: 132,
        KEY_ID.KEYBOARD_LEFT_ARROW: 162,
        KEY_ID.KEYBOARD_END: 94,
        KEY_ID.KEYBOARD_RIGHT_SHIFT: 152,

        # ROW 8
        KEY_ID.SCREEN_CAPTURE: 9,
        KEY_ID.KEYBOARD_8: 41,
        KEY_ID.KEYBOARD_I: 72,
        KEY_ID.KEYBOARD_K: 103,
        KEY_ID.KEYBOARD_COMMA_AND_LESS: 133,
        KEY_ID.KEYBOARD_DOWN_ARROW: 163,
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: 92,
        KEY_ID.KEYBOARD_UP_ARROW: 153,

        # ROW 9
        KEY_ID.MUTE_MICROPHONE: 10,
        KEY_ID.KEYBOARD_9: 42,
        KEY_ID.KEYBOARD_O: 73,
        KEY_ID.KEYBOARD_L: 104,
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: 134,
        KEY_ID.KEYBOARD_RIGHT_ARROW: 164,
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: 93,
        KEY_ID.KEYBOARD_PAGE_DOWN: 154,

        # ROW 10
        KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: 11,
        KEY_ID.KEYBOARD_0: 43,

        # ROW 11
        KEY_ID.PLAY_PAUSE: 12,
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: 44,
    }

    # To be used by the I2C parser to convert frames into PWM payload
    PWM_LED_ID_TO_LED_ID = {
        LED_ID.CONNECTIVITY_STATUS_LED_1: KEY_ID_TO_LED_ID[KEY_ID.HOST_1],
        LED_ID.CONNECTIVITY_STATUS_LED_2: KEY_ID_TO_LED_ID[KEY_ID.HOST_2],
        LED_ID.CONNECTIVITY_STATUS_LED_3: KEY_ID_TO_LED_ID[KEY_ID.HOST_3],
        LED_ID.CAPS_LOCK: KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_CAPS_LOCK],
    }

    LED_ID_AVAILABLE = list(KEY_ID_TO_LED_ID.values())

    KEY_ID_CONTRAST_GROUP_KEYS1 = [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE, KEY_ID.KEYBOARD_TAB,
                                   KEY_ID.KEYBOARD_CAPS_LOCK, KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_CONTROL,
                                   KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_LEFT_ALT,
                                   KEY_ID.KEYBOARD_SPACE_BAR, KEY_ID.KEYBOARD_RIGHT_ALT, KEY_ID.FN_KEY,
                                   KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION, KEY_ID.BACKLIGHT_UP, KEY_ID.DICTATION,
                                   KEY_ID.EMOJI_PANEL, KEY_ID.SCREEN_CAPTURE, KEY_ID.KEYBOARD_VOLUME_DOWN,
                                   KEY_ID.KEYBOARD_VOLUME_UP, KEY_ID.DO_NOT_DISTURB, KEY_ID.KEYBOARD_HOME,
                                   KEY_ID.KEYBOARD_END, KEY_ID.KEYBOARD_PAGE_UP, KEY_ID.KEYBOARD_PAGE_DOWN,
                                   KEY_ID.KEYBOARD_BACKSPACE, KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE,
                                   KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_RIGHT_SHIFT]

    KEY_ID_CONTRAST_GROUP_KEYS2 = [KEY_ID.HOST_1, KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_Q, KEY_ID.KEYBOARD_A,
                                   KEY_ID.KEYBOARD_Z, KEY_ID.HOST_2, KEY_ID.KEYBOARD_2, KEY_ID.KEYBOARD_W,
                                   KEY_ID.KEYBOARD_S, KEY_ID.KEYBOARD_X, KEY_ID.HOST_3, KEY_ID.KEYBOARD_3,
                                   KEY_ID.KEYBOARD_E, KEY_ID.KEYBOARD_D, KEY_ID.KEYBOARD_C, KEY_ID.BACKLIGHT_DOWN,
                                   KEY_ID.KEYBOARD_4, KEY_ID.KEYBOARD_R, KEY_ID.KEYBOARD_F, KEY_ID.KEYBOARD_V,
                                   KEY_ID.KEYBOARD_5, KEY_ID.KEYBOARD_T, KEY_ID.KEYBOARD_G, KEY_ID.KEYBOARD_B,
                                   KEY_ID.KEYBOARD_6, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_H, KEY_ID.KEYBOARD_N,
                                   KEY_ID.KEYBOARD_7, KEY_ID.KEYBOARD_U, KEY_ID.KEYBOARD_J, KEY_ID.KEYBOARD_M,
                                   KEY_ID.KEYBOARD_8, KEY_ID.KEYBOARD_I, KEY_ID.KEYBOARD_K,
                                   KEY_ID.KEYBOARD_COMMA_AND_LESS, KEY_ID.MUTE_MICROPHONE, KEY_ID.KEYBOARD_9,
                                   KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_L, KEY_ID.KEYBOARD_PERIOD_AND_MORE,
                                   KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT, KEY_ID.KEYBOARD_0, KEY_ID.KEYBOARD_P,
                                   KEY_ID.KEYBOARD_SEMICOLON_AND_COLON, KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK,
                                   KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE,
                                   KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE,
                                   KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK,
                                   KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_EQUAL_AND_PLUS,
                                   KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE, KEY_ID.KEYBOARD_LEFT_ARROW,
                                   KEY_ID.KEYBOARD_RIGHT_ARROW, KEY_ID.KEYBOARD_UP_ARROW, KEY_ID.KEYBOARD_DOWN_ARROW]

    KEY_ID_WAVE_MAP_HORIZONTAL = [
        # Group 0 (leftmost on a sample)
        [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE, KEY_ID.KEYBOARD_TAB, KEY_ID.KEYBOARD_CAPS_LOCK,
         KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_CONTROL],
        # Group 1
        [KEY_ID.HOST_1, KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_Q, KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z,
         KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
        # Group 2
        [KEY_ID.HOST_2, KEY_ID.KEYBOARD_2, KEY_ID.KEYBOARD_W, KEY_ID.KEYBOARD_S, KEY_ID.KEYBOARD_X,
         KEY_ID.KEYBOARD_LEFT_ALT],
        # Group 3
        [KEY_ID.HOST_3, KEY_ID.KEYBOARD_3, KEY_ID.KEYBOARD_E, KEY_ID.KEYBOARD_D, KEY_ID.KEYBOARD_C],
        # Group 4
        [KEY_ID.BACKLIGHT_DOWN, KEY_ID.KEYBOARD_4, KEY_ID.KEYBOARD_R, KEY_ID.KEYBOARD_F, KEY_ID.KEYBOARD_V],
        # Group 5
        [KEY_ID.BACKLIGHT_UP, KEY_ID.KEYBOARD_5, KEY_ID.KEYBOARD_T, KEY_ID.KEYBOARD_G, KEY_ID.KEYBOARD_B,
         KEY_ID.KEYBOARD_SPACE_BAR],
        # Group 6
        [KEY_ID.DICTATION, KEY_ID.KEYBOARD_6, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_H, KEY_ID.KEYBOARD_N],
        # Group 7
        [KEY_ID.EMOJI_PANEL, KEY_ID.KEYBOARD_7, KEY_ID.KEYBOARD_U, KEY_ID.KEYBOARD_J, KEY_ID.KEYBOARD_M],
        # Group 8
        [KEY_ID.SCREEN_CAPTURE, KEY_ID.KEYBOARD_8, KEY_ID.KEYBOARD_I, KEY_ID.KEYBOARD_K,
         KEY_ID.KEYBOARD_COMMA_AND_LESS],
        # Group 9
        [KEY_ID.MUTE_MICROPHONE, KEY_ID.KEYBOARD_9, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_L,
         KEY_ID.KEYBOARD_PERIOD_AND_MORE, KEY_ID.KEYBOARD_RIGHT_ALT],
        # Group 10
        [KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT, KEY_ID.KEYBOARD_0, KEY_ID.KEYBOARD_P,
         KEY_ID.KEYBOARD_SEMICOLON_AND_COLON, KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK, KEY_ID.FN_KEY],
        # Group 11
        [KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE, KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE,
         KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION],
        # Group 12
        [KEY_ID.KEYBOARD_VOLUME_DOWN, KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_EQUAL_AND_PLUS,
         KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE, KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_RIGHT_SHIFT,
         KEY_ID.KEYBOARD_LEFT_ARROW],
        # Group 13
        [KEY_ID.KEYBOARD_VOLUME_UP, KEY_ID.KEYBOARD_BACKSPACE, KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE,
         KEY_ID.KEYBOARD_UP_ARROW, KEY_ID.KEYBOARD_DOWN_ARROW],
        # Group 14 (rightmost on a sample)
        [KEY_ID.DO_NOT_DISTURB, KEY_ID.KEYBOARD_HOME, KEY_ID.KEYBOARD_END, KEY_ID.KEYBOARD_PAGE_UP,
         KEY_ID.KEYBOARD_PAGE_DOWN, KEY_ID.KEYBOARD_RIGHT_ARROW]]
# end class IngaCsMacBacklightConfiguration


class IngaCsMacUkBacklightConfiguration(IngaCsMacBacklightConfiguration):
    """
    Configure the backlight effect and I2C layout of INGA Compact Size For MAC Uk layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ZSSQRrsWq_q86rT4A-5I1WdANSpDxpKVeOB2S8Dzml0/view#gid=0
    """
    # I2C led driver layout
    KEY_ID_TO_LED_ID = IngaCsMacBacklightConfiguration.KEY_ID_TO_LED_ID.copy()
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]    # Col_1, Row_0
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_NO_US_1] = 33                  # Col_1, Row_0
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]        # Col_6, Row_9
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RETURN_ENTER] = 93             # Col_6, Row_9
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_NO_US_45] = 15

    LED_ID_AVAILABLE = list(KEY_ID_TO_LED_ID.values())

    KEY_ID_CONTRAST_GROUP_KEYS1 = IngaCsMacBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS1.copy()

    KEY_ID_CONTRAST_GROUP_KEYS2 = IngaCsMacBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS2.copy()
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.KEYBOARD_NO_US_45)

    KEY_ID_WAVE_MAP_HORIZONTAL = IngaCsMacBacklightConfiguration.KEY_ID_WAVE_MAP_HORIZONTAL.copy()
    # Group 0 :
    KEY_ID_WAVE_MAP_HORIZONTAL[0] = [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE,
                                     KEY_ID.KEYBOARD_TAB, KEY_ID.KEYBOARD_CAPS_LOCK, KEY_ID.KEYBOARD_LEFT_SHIFT,
                                     KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_NO_US_45]
# end class IngaCsMacUkBacklightConfiguration


class IngaCsMacJpnBacklightConfiguration(IngaCsMacBacklightConfiguration):
    """
    Configure the backlight effect and I2C layout of INGA Compact Size For MAC japanese layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ZSSQRrsWq_q86rT4A-5I1WdANSpDxpKVeOB2S8Dzml0/view#gid=0
    """
    # I2C led driver layout
    KEY_ID_TO_LED_ID = IngaCsMacBacklightConfiguration.KEY_ID_TO_LED_ID.copy()
    KEY_ID_TO_LED_ID[KEY_ID.YEN] = 15
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_INTERNATIONAL5] = 75
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_INTERNATIONAL1] = 45
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_INTERNATIONAL4] = 105

    LED_ID_AVAILABLE = list(KEY_ID_TO_LED_ID.values())

    KEY_ID_CONTRAST_GROUP_KEYS1 = IngaCsMacBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS1.copy()
    KEY_ID_CONTRAST_GROUP_KEYS1.append(KEY_ID.KEYBOARD_INTERNATIONAL5)
    KEY_ID_CONTRAST_GROUP_KEYS1.append(KEY_ID.KEYBOARD_INTERNATIONAL4)

    KEY_ID_CONTRAST_GROUP_KEYS2 = IngaCsMacBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS2.copy()
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.YEN)
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.KEYBOARD_INTERNATIONAL1)

    KEY_ID_WAVE_MAP_HORIZONTAL = IngaCsMacBacklightConfiguration.KEY_ID_WAVE_MAP_HORIZONTAL.copy()
    # Group 3 :
    KEY_ID_WAVE_MAP_HORIZONTAL[3] = [KEY_ID.HOST_3, KEY_ID.KEYBOARD_3, KEY_ID.KEYBOARD_E, KEY_ID.KEYBOARD_D,
                                     KEY_ID.KEYBOARD_C, KEY_ID.KEYBOARD_INTERNATIONAL5]
    # Group 8
    KEY_ID_WAVE_MAP_HORIZONTAL[8] = [KEY_ID.SCREEN_CAPTURE, KEY_ID.KEYBOARD_8, KEY_ID.KEYBOARD_I, KEY_ID.KEYBOARD_K,
                                     KEY_ID.KEYBOARD_COMMA_AND_LESS, KEY_ID.KEYBOARD_INTERNATIONAL4]
    # Group 11
    KEY_ID_WAVE_MAP_HORIZONTAL[11] = [KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE,
                                      KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE,
                                      KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK,
                                      KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION, KEY_ID.KEYBOARD_INTERNATIONAL1]
    # Group 13
    KEY_ID_WAVE_MAP_HORIZONTAL[11] = [KEY_ID.KEYBOARD_VOLUME_UP, KEY_ID.KEYBOARD_BACKSPACE,
                                      KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE, KEY_ID.KEYBOARD_UP_ARROW,
                                      KEY_ID.KEYBOARD_DOWN_ARROW, KEY_ID.KEYBOARD_INTERNATIONAL5]
# end class IngaCsMacJpnBacklightConfiguration

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
