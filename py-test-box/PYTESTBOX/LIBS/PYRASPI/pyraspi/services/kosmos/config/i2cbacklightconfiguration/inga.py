#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.i2cbacklightconfiguration.inga
:brief: Inga universal keyboard backlight configuration
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
class IngaBacklightConfiguration(MechanicalBacklightConfiguration):
    """
    Configure the backlight effect and I2C layout of INGA Compact Size For MAC US layout

    For now, most of the information have been found directly in the NPI codeline:
    https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/rbk71_inga/+/refs/heads/master/application/led_backlight.c

    - KEY_ID_TO_LED_ID can be configured from "led_reaction_key_id" table and "getLedAddress" functions.
        Example : for Col 2, Row 0 (corresponding to KEY_ID.KEYBOARD_TAB on Key matrix map
        https://docs.google.com/spreadsheets/d/1NWV_o1Sxui_C6StNQwpNWtopWlpkkkrGLcsxONfGG8Y/view#gid=0)
        led_reaction_key_id[0][2] = 44 and getLedAddress(led_reaction_key_id[0][2]) = 66
        so {KEY_ID.KEYBOARD_TAB: 66}
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
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: 34,
        KEY_ID.KEYBOARD_TAB: 66,
        KEY_ID.KEYBOARD_CAPS_LOCK: 97,
        KEY_ID.KEYBOARD_LEFT_SHIFT: 125,
        KEY_ID.KEYBOARD_LEFT_CONTROL: 152,
        KEY_ID.KEYBOARD_VOLUME_UP: 15,
        KEY_ID.KEYBOARD_END: 92,

        # ROW 1
        KEY_ID.BRIGHTNESS_DOWN: 2,
        KEY_ID.KEYBOARD_1: 35,
        KEY_ID.KEYBOARD_Q: 67,
        KEY_ID.KEYBOARD_A: 98,
        KEY_ID.KEYBOARD_Z: 126,
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: 153,
        KEY_ID.HOST_1: 16,
        KEY_ID.KEYBOARD_PAGE_DOWN: 93,

        # ROW 2
        KEY_ID.BRIGHTNESS_UP: 3,
        KEY_ID.KEYBOARD_2: 36,
        KEY_ID.KEYBOARD_W: 68,
        KEY_ID.KEYBOARD_S: 99,
        KEY_ID.KEYBOARD_X: 127,
        KEY_ID.KEYBOARD_LEFT_ALT: 154,
        KEY_ID.HOST_2: 17,
        KEY_ID.KEYPAD_7_AND_HOME: 94,

        # ROW 3
        KEY_ID.BACKLIGHT_DOWN: 4,
        KEY_ID.KEYBOARD_3: 37,
        KEY_ID.KEYBOARD_E: 69,
        KEY_ID.KEYBOARD_D: 100,
        KEY_ID.KEYBOARD_C: 128,
        KEY_ID.KEYBOARD_SPACE_BAR: 155,
        KEY_ID.HOST_3: 18,
        KEY_ID.KEYPAD_8_AND_UP_ARROW: 95,

        # ROW 4
        KEY_ID.BACKLIGHT_UP: 5,
        KEY_ID.KEYBOARD_4: 38,
        KEY_ID.KEYBOARD_R: 70,
        KEY_ID.KEYBOARD_F: 101,
        KEY_ID.KEYBOARD_V: 129,
        KEY_ID.KEYBOARD_RIGHT_ALT: 156,
        KEY_ID.CALCULATOR: 19,
        KEY_ID.KEYPAD_9_AND_PAGE_UP: 96,

        # ROW 5
        KEY_ID.DICTATION: 6,
        KEY_ID.KEYBOARD_5: 39,
        KEY_ID.KEYBOARD_T: 71,
        KEY_ID.KEYBOARD_G: 102,
        KEY_ID.KEYBOARD_B: 130,
        KEY_ID.FN_KEY: 157,
        KEY_ID.SHOW_DESKTOP: 31,
        KEY_ID.KEYPAD_MINUS: 65,

        # ROW 6
        KEY_ID.EMOJI_PANEL: 7,
        KEY_ID.KEYBOARD_6: 40,
        KEY_ID.KEYBOARD_Y: 72,
        KEY_ID.KEYBOARD_H: 103,
        KEY_ID.KEYBOARD_N: 131,
        KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION: 158,
        KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: 32,
        KEY_ID.KEYPAD_4_AND_LEFT_ARROW: 121,

        # ROW 7
        KEY_ID.SCREEN_CAPTURE: 8,
        KEY_ID.KEYBOARD_7: 41,
        KEY_ID.KEYBOARD_U: 73,
        KEY_ID.KEYBOARD_J: 104,
        KEY_ID.KEYBOARD_M: 132,
        KEY_ID.KEYBOARD_RIGHT_CONTROL: 159,
        KEY_ID.SCREEN_LOCK: 33,
        KEY_ID.KEYPAD_5: 122,

        # ROW 8
        KEY_ID.MUTE_MICROPHONE: 9,
        KEY_ID.KEYBOARD_8: 42,
        KEY_ID.KEYBOARD_I: 74,
        KEY_ID.KEYBOARD_K: 105,
        KEY_ID.KEYBOARD_COMMA_AND_LESS: 133,
        KEY_ID.KEYBOARD_LEFT_ARROW: 160,
        KEY_ID.KEYBOARD_INSERT: 48,
        KEY_ID.KEYPAD_6_AND_RIGHT_ARROW: 123,

        # ROW 9
        KEY_ID.PREV_TRACK: 10,
        KEY_ID.KEYBOARD_9: 43,
        KEY_ID.KEYBOARD_O: 75,
        KEY_ID.KEYBOARD_L: 106,
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: 134,
        KEY_ID.KEYBOARD_DOWN_ARROW: 161,
        KEY_ID.KEYBOARD_HOME: 49,
        KEY_ID.KEYPAD_PLUS: 124,

        # ROW 10
        KEY_ID.PLAY_PAUSE: 11,
        KEY_ID.KEYBOARD_0: 44,
        KEY_ID.KEYBOARD_P: 76,
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: 107,
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: 135,
        KEY_ID.KEYBOARD_RIGHT_ARROW: 162,
        KEY_ID.KEYBOARD_PAGE_UP: 61,
        KEY_ID.KEYPAD_2_AND_DOWN_ARROW: 139,

        # ROW 11
        KEY_ID.NEXT_TRACK: 12,
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: 45,
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: 77,
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: 108,
        KEY_ID.KEYBOARD_RIGHT_SHIFT: 136,
        KEY_ID.KEYPAD_0_AND_INSERT: 163,
        KEY_ID.KEYBOARD_LOCKING_NUM_LOCK: 62,
        KEY_ID.KEYPAD_3_AND_PAGE_DN: 151,

        # ROW 12
        KEY_ID.KEYBOARD_MUTE: 13,
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: 46,
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: 78,
        KEY_ID.KEYBOARD_RETURN_ENTER: 109,
        KEY_ID.KEYBOARD_UP_ARROW: 137,
        KEY_ID.KEYPAD_PERIOD_AND_DELETE: 164,
        KEY_ID.KEYPAD_FORWARD_SLASH: 63,

        # ROW 13
        KEY_ID.KEYBOARD_VOLUME_DOWN: 14,
        KEY_ID.KEYBOARD_BACKSPACE: 47,
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: 79,
        KEY_ID.KEYBOARD_DELETE_FORWARD: 91,
        KEY_ID.KEYPAD_1_AND_END: 138,
        KEY_ID.KEYPAD_ENTER: 165,
        KEY_ID.KEYPAD_ASTERISK: 64,
    }

    # To be used by the I2C parser to convert frames into PWM payload
    PWM_LED_ID_TO_LED_ID = {
        LED_ID.CONNECTIVITY_STATUS_LED_1: KEY_ID_TO_LED_ID[KEY_ID.HOST_1],
        LED_ID.CONNECTIVITY_STATUS_LED_2: KEY_ID_TO_LED_ID[KEY_ID.HOST_2],
        LED_ID.CONNECTIVITY_STATUS_LED_3: KEY_ID_TO_LED_ID[KEY_ID.HOST_3],
        LED_ID.CAPS_LOCK: KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_CAPS_LOCK],
        LED_ID.NUM_LOCK: KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_LOCKING_NUM_LOCK],
    }

    LED_ID_AVAILABLE = list(KEY_ID_TO_LED_ID.values())

    KEY_ID_CONTRAST_GROUP_KEYS1 = [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE, KEY_ID.KEYBOARD_TAB,
                                   KEY_ID.KEYBOARD_CAPS_LOCK, KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_CONTROL,
                                   KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_LEFT_ALT,
                                   KEY_ID.KEYBOARD_SPACE_BAR, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,
                                   KEY_ID.KEYBOARD_RIGHT_ALT, KEY_ID.FN_KEY, KEY_ID.KEYBOARD_RIGHT_CONTROL,
                                   KEY_ID.DICTATION, KEY_ID.EMOJI_PANEL, KEY_ID.SCREEN_CAPTURE, KEY_ID.MUTE_MICROPHONE,
                                   KEY_ID.KEYBOARD_VOLUME_DOWN, KEY_ID.KEYBOARD_VOLUME_UP,
                                   KEY_ID.KEYBOARD_BACKSPACE, KEY_ID.KEYBOARD_RETURN_ENTER,
                                   KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE, KEY_ID.KEYBOARD_RIGHT_SHIFT, KEY_ID.HOST_1,
                                   KEY_ID.HOST_2, KEY_ID.HOST_3, KEY_ID.KEYBOARD_INSERT, KEY_ID.KEYBOARD_HOME,
                                   KEY_ID.KEYBOARD_DELETE_FORWARD, KEY_ID.KEYBOARD_END, KEY_ID.KEYBOARD_PAGE_UP,
                                   KEY_ID.KEYBOARD_PAGE_DOWN, KEY_ID.KEYBOARD_LEFT_ARROW,
                                   KEY_ID.KEYBOARD_RIGHT_ARROW, KEY_ID.KEYBOARD_UP_ARROW,
                                   KEY_ID.KEYBOARD_DOWN_ARROW, KEY_ID.KEYPAD_ENTER, KEY_ID.KEYPAD_ASTERISK,
                                   KEY_ID.KEYPAD_PLUS, KEY_ID.KEYPAD_MINUS, KEY_ID.KEYPAD_FORWARD_SLASH,
                                   KEY_ID.KEYBOARD_LOCKING_NUM_LOCK, KEY_ID.SCREEN_LOCK,
                                   KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT, KEY_ID.SHOW_DESKTOP, KEY_ID.CALCULATOR]

    KEY_ID_CONTRAST_GROUP_KEYS2 = [KEY_ID.BRIGHTNESS_DOWN, KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_Q, KEY_ID.KEYBOARD_A,
                                   KEY_ID.KEYBOARD_Z, KEY_ID.BRIGHTNESS_UP, KEY_ID.KEYBOARD_2, KEY_ID.KEYBOARD_W,
                                   KEY_ID.KEYBOARD_S, KEY_ID.KEYBOARD_X, KEY_ID.BACKLIGHT_DOWN, KEY_ID.KEYBOARD_3,
                                   KEY_ID.KEYBOARD_E, KEY_ID.KEYBOARD_D, KEY_ID.KEYBOARD_C, KEY_ID.BACKLIGHT_UP,
                                   KEY_ID.KEYBOARD_4, KEY_ID.KEYBOARD_R, KEY_ID.KEYBOARD_F, KEY_ID.KEYBOARD_V,
                                   KEY_ID.KEYBOARD_5, KEY_ID.KEYBOARD_T, KEY_ID.KEYBOARD_G, KEY_ID.KEYBOARD_B,
                                   KEY_ID.KEYBOARD_6, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_H, KEY_ID.KEYBOARD_N,
                                   KEY_ID.KEYBOARD_7, KEY_ID.KEYBOARD_U, KEY_ID.KEYBOARD_J, KEY_ID.KEYBOARD_M,
                                   KEY_ID.KEYBOARD_8, KEY_ID.KEYBOARD_I, KEY_ID.KEYBOARD_K,
                                   KEY_ID.KEYBOARD_COMMA_AND_LESS, KEY_ID.PREV_TRACK, KEY_ID.KEYBOARD_9,
                                   KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_L, KEY_ID.KEYBOARD_PERIOD_AND_MORE,
                                   KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_0, KEY_ID.KEYBOARD_P,
                                   KEY_ID.KEYBOARD_SEMICOLON_AND_COLON, KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK,
                                   KEY_ID.NEXT_TRACK, KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE,
                                   KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE,
                                   KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK,
                                   KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_EQUAL_AND_PLUS,
                                   KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE, KEY_ID.KEYPAD_7_AND_HOME,
                                   KEY_ID.KEYPAD_8_AND_UP_ARROW, KEY_ID.KEYPAD_9_AND_PAGE_UP,
                                   KEY_ID.KEYPAD_4_AND_LEFT_ARROW, KEY_ID.KEYPAD_5, KEY_ID.KEYPAD_6_AND_RIGHT_ARROW,
                                   KEY_ID.KEYPAD_1_AND_END, KEY_ID.KEYPAD_2_AND_DOWN_ARROW, KEY_ID.KEYPAD_3_AND_PAGE_DN,
                                   KEY_ID.KEYPAD_0_AND_INSERT, KEY_ID.KEYPAD_PERIOD_AND_DELETE]

    KEY_ID_WAVE_MAP_HORIZONTAL = [
        # Group 0 (leftmost on a sample)
        [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE, KEY_ID.KEYBOARD_TAB, KEY_ID.KEYBOARD_CAPS_LOCK,
         KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_CONTROL],
        # Group 1
        [KEY_ID.BRIGHTNESS_DOWN, KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_Q, KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z,
         KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
        # Group 2
        [KEY_ID.BRIGHTNESS_UP, KEY_ID.KEYBOARD_2, KEY_ID.KEYBOARD_W, KEY_ID.KEYBOARD_S, KEY_ID.KEYBOARD_X,
         KEY_ID.KEYBOARD_LEFT_ALT],
        # Group 3
        [KEY_ID.BACKLIGHT_DOWN, KEY_ID.KEYBOARD_3, KEY_ID.KEYBOARD_E, KEY_ID.KEYBOARD_D, KEY_ID.KEYBOARD_C],
        # Group 4
        [KEY_ID.BACKLIGHT_UP, KEY_ID.KEYBOARD_4, KEY_ID.KEYBOARD_R, KEY_ID.KEYBOARD_F, KEY_ID.KEYBOARD_V],
        # Group 5
        [KEY_ID.DICTATION, KEY_ID.KEYBOARD_5, KEY_ID.KEYBOARD_T, KEY_ID.KEYBOARD_G, KEY_ID.KEYBOARD_B,
         KEY_ID.KEYBOARD_SPACE_BAR],
        # Group 6
        [KEY_ID.EMOJI_PANEL, KEY_ID.KEYBOARD_6, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_H, KEY_ID.KEYBOARD_N],
        # Group 7
        [KEY_ID.SCREEN_CAPTURE, KEY_ID.KEYBOARD_7, KEY_ID.KEYBOARD_U, KEY_ID.KEYBOARD_J, KEY_ID.KEYBOARD_M],
        # Group 8
        [KEY_ID.MUTE_MICROPHONE, KEY_ID.KEYBOARD_8, KEY_ID.KEYBOARD_I, KEY_ID.KEYBOARD_K,
         KEY_ID.KEYBOARD_COMMA_AND_LESS],
        # Group 9
        [KEY_ID.PREV_TRACK, KEY_ID.KEYBOARD_9, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_L,
         KEY_ID.KEYBOARD_PERIOD_AND_MORE, KEY_ID.KEYBOARD_RIGHT_ALT],
        # Group 10
        [KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_0, KEY_ID.KEYBOARD_P,
         KEY_ID.KEYBOARD_SEMICOLON_AND_COLON, KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK, KEY_ID.FN_KEY],
        # Group 11
        [KEY_ID.NEXT_TRACK, KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE, KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE,
         KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION],
        # Group 12
        [KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_EQUAL_AND_PLUS, KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE,
         KEY_ID.KEYBOARD_RIGHT_SHIFT],
        # Group 13
        [KEY_ID.KEYBOARD_VOLUME_DOWN, KEY_ID.KEYBOARD_VOLUME_UP, KEY_ID.KEYBOARD_BACKSPACE,
         KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE],
        # Group 14
        [KEY_ID.HOST_1, KEY_ID.KEYBOARD_INSERT, KEY_ID.KEYBOARD_DELETE_FORWARD, KEY_ID.KEYBOARD_LEFT_ARROW],
        # Group 15
        [KEY_ID.HOST_2, KEY_ID.KEYBOARD_HOME, KEY_ID.KEYBOARD_END, KEY_ID.KEYBOARD_UP_ARROW,
         KEY_ID.KEYBOARD_DOWN_ARROW],
        # Group 16
        [KEY_ID.HOST_3, KEY_ID.KEYBOARD_PAGE_UP, KEY_ID.KEYBOARD_PAGE_DOWN, KEY_ID.KEYBOARD_RIGHT_ARROW],
        # Group 17
        [KEY_ID.CALCULATOR, KEY_ID.KEYBOARD_LOCKING_NUM_LOCK, KEY_ID.KEYPAD_7_AND_HOME, KEY_ID.KEYPAD_4_AND_LEFT_ARROW,
         KEY_ID.KEYPAD_1_AND_END],
        # Group 18
        [KEY_ID.SHOW_DESKTOP, KEY_ID.KEYPAD_FORWARD_SLASH, KEY_ID.KEYPAD_8_AND_UP_ARROW, KEY_ID.KEYPAD_5,
         KEY_ID.KEYPAD_2_AND_DOWN_ARROW, KEY_ID.KEYPAD_0_AND_INSERT],
        # Group 19
        [KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT, KEY_ID.KEYPAD_ASTERISK, KEY_ID.KEYPAD_9_AND_PAGE_UP,
         KEY_ID.KEYPAD_6_AND_RIGHT_ARROW, KEY_ID.KEYPAD_3_AND_PAGE_DN, KEY_ID.KEYPAD_PERIOD_AND_DELETE],
        # Group 20 (rightmost on a sample)
        [KEY_ID.KEYPAD_ENTER, KEY_ID.KEYPAD_PLUS, KEY_ID.KEYPAD_MINUS, KEY_ID.SCREEN_LOCK]]
# end class IngaBacklightConfiguration


class IngaUkBacklightConfiguration(IngaBacklightConfiguration):
    """
    Configure the backlight effect and I2C layout of INGA Uk layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1NWV_o1Sxui_C6StNQwpNWtopWlpkkkrGLcsxONfGG8Y/view#gid=1538394432
    """
    # I2C led driver layout
    KEY_ID_TO_LED_ID = IngaBacklightConfiguration.KEY_ID_TO_LED_ID.copy()
    # Modified keys
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]  # Col_1, Row_0
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]  # Col_2, Row_13
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RETURN_ENTER]  # Col_3, Row_13
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_NO_US_1] = 34  # Col_1, Row_0
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RETURN_ENTER] = 79  # Col_2, Row_13
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_NO_US_42] = 109  # Col_3, Row_12
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_NO_US_45] = 166  # Col_7, Row_12

    LED_ID_AVAILABLE = list(KEY_ID_TO_LED_ID.values())

    # Contrast group Keys 1
    KEY_ID_CONTRAST_GROUP_KEYS1 = IngaBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS1.copy()
    KEY_ID_CONTRAST_GROUP_KEYS1.remove(KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE)
    KEY_ID_CONTRAST_GROUP_KEYS1.remove(KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE)
    KEY_ID_CONTRAST_GROUP_KEYS1.append(KEY_ID.KEYBOARD_NO_US_1)
    # Contrast group Keys 2
    KEY_ID_CONTRAST_GROUP_KEYS2 = IngaBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS2.copy()
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.KEYBOARD_NO_US_45)
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.KEYBOARD_NO_US_42)

    # Wave configuration
    KEY_ID_WAVE_MAP_HORIZONTAL = IngaBacklightConfiguration.KEY_ID_WAVE_MAP_HORIZONTAL.copy()
    # Group 0 :
    KEY_ID_WAVE_MAP_HORIZONTAL[0] = [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_NO_US_1, KEY_ID.KEYBOARD_TAB,
                                     KEY_ID.KEYBOARD_CAPS_LOCK, KEY_ID.KEYBOARD_LEFT_SHIFT,
                                     KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_NO_US_45]
    # Group 13
    KEY_ID_WAVE_MAP_HORIZONTAL[13] = [KEY_ID.KEYBOARD_VOLUME_DOWN, KEY_ID.KEYBOARD_VOLUME_UP,
                                      KEY_ID.KEYBOARD_BACKSPACE, KEY_ID.KEYBOARD_RETURN_ENTER,
                                      KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_NO_US_42]
# end class IngaUkBacklightConfiguration


class IngaJpnBacklightConfiguration(IngaBacklightConfiguration):
    """
    Configure the backlight effect and I2C layout of INGA japanese layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1NWV_o1Sxui_C6StNQwpNWtopWlpkkkrGLcsxONfGG8Y/view#gid=565940325
    """
    # I2C led driver layout
    # Modified keys
    KEY_ID_TO_LED_ID = IngaBacklightConfiguration.KEY_ID_TO_LED_ID.copy()
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]  # Col_2, Row_13
    del KEY_ID_TO_LED_ID[KEY_ID.FN_KEY]  # Col_5, Row_5
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION]  # Col_5, Row_6
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RIGHT_CONTROL]  # Col_5, Row_7
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RETURN_ENTER]  # Col_3, Row_13
    del KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RIGHT_ALT]  # Col_5, Row_4
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RETURN_ENTER] = 79  # Col_2, Row_13
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RIGHT_ALT] = 157  # Col_5, Row_5
    KEY_ID_TO_LED_ID[KEY_ID.FN_KEY] = 158  # Col_5, Row_6
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION] = 159  # Col_5, Row_7
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_NO_US_42] = 109  # Col_3, Row_13
    KEY_ID_TO_LED_ID[KEY_ID.KATAHIRA] = 156  # Col_5, Row_4
    KEY_ID_TO_LED_ID[KEY_ID.YEN] = 166  # Col_7, Row_12
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_INTERNATIONAL1] = 167  # Col_7, Row_13
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_INTERNATIONAL5] = 168  # Col_4, Row_14
    KEY_ID_TO_LED_ID[KEY_ID.KEYBOARD_INTERNATIONAL4] = 169  # Col_5, Row_14

    LED_ID_AVAILABLE = list(KEY_ID_TO_LED_ID.values())

    # Contrast group Keys 1
    KEY_ID_CONTRAST_GROUP_KEYS1 = IngaBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS1.copy()
    KEY_ID_CONTRAST_GROUP_KEYS1.remove(KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE)
    KEY_ID_CONTRAST_GROUP_KEYS1.remove(KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION)
    KEY_ID_CONTRAST_GROUP_KEYS1.remove(KEY_ID.KEYBOARD_RIGHT_CONTROL)
    KEY_ID_CONTRAST_GROUP_KEYS1.append(KEY_ID.KEYBOARD_INTERNATIONAL5)
    KEY_ID_CONTRAST_GROUP_KEYS1.append(KEY_ID.KEYBOARD_INTERNATIONAL4)
    KEY_ID_CONTRAST_GROUP_KEYS1.append(KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION)
    KEY_ID_CONTRAST_GROUP_KEYS1.append(KEY_ID.KATAHIRA)
    # Contrast group Keys 2
    KEY_ID_CONTRAST_GROUP_KEYS2 = IngaBacklightConfiguration.KEY_ID_CONTRAST_GROUP_KEYS2.copy()
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.YEN)
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.KEYBOARD_INTERNATIONAL1)
    KEY_ID_CONTRAST_GROUP_KEYS2.append(KEY_ID.KEYBOARD_NO_US_42)

    # Wave configuration
    KEY_ID_WAVE_MAP_HORIZONTAL = IngaBacklightConfiguration.KEY_ID_WAVE_MAP_HORIZONTAL.copy()
    # Group 3 :
    KEY_ID_WAVE_MAP_HORIZONTAL[3] = [KEY_ID.BACKLIGHT_DOWN, KEY_ID.KEYBOARD_3, KEY_ID.KEYBOARD_E, KEY_ID.KEYBOARD_D,
                                     KEY_ID.KEYBOARD_C, KEY_ID.KEYBOARD_INTERNATIONAL5]
    # Group 8
    KEY_ID_WAVE_MAP_HORIZONTAL[8] = [KEY_ID.MUTE_MICROPHONE, KEY_ID.KEYBOARD_8, KEY_ID.KEYBOARD_I, KEY_ID.KEYBOARD_K,
                                     KEY_ID.KEYBOARD_COMMA_AND_LESS, KEY_ID.KEYBOARD_INTERNATIONAL4]
    # Group 9
    KEY_ID_WAVE_MAP_HORIZONTAL[9] = [KEY_ID.PREV_TRACK, KEY_ID.KEYBOARD_9, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_L,
                                     KEY_ID.KEYBOARD_PERIOD_AND_MORE, KEY_ID.KATAHIRA]
    # Group 10
    KEY_ID_WAVE_MAP_HORIZONTAL[10] = [KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_0, KEY_ID.KEYBOARD_P,
                                      KEY_ID.KEYBOARD_SEMICOLON_AND_COLON,
                                      KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK, KEY_ID.KEYBOARD_RIGHT_ALT,
                                      KEY_ID.KEYBOARD_INTERNATIONAL1]
    # Group 11
    KEY_ID_WAVE_MAP_HORIZONTAL[11] = [KEY_ID.NEXT_TRACK, KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE,
                                      KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE,
                                      KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK,
                                      KEY_ID.FN_KEY]
    # Group 13
    KEY_ID_WAVE_MAP_HORIZONTAL[13] = [KEY_ID.KEYBOARD_VOLUME_DOWN, KEY_ID.KEYBOARD_VOLUME_UP,
                                      KEY_ID.KEYBOARD_BACKSPACE, KEY_ID.KEYBOARD_RETURN_ENTER,
                                      KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION, KEY_ID.YEN, KEY_ID.KEYBOARD_NO_US_42]


    # Workaround : No Test Point on US layout for ROW14, so Inga keymatrix is not configured for all the keys in this
    # row. Need to add the 2 keys in BACKLIGHT_EFFECT_FORBIDDEN_KEYS to avoid key press on backlight reaction test.
    BACKLIGHT_EFFECT_FORBIDDEN_KEYS = IngaBacklightConfiguration.BACKLIGHT_EFFECT_FORBIDDEN_KEYS.copy()
    BACKLIGHT_EFFECT_FORBIDDEN_KEYS.append(KEY_ID.KEYBOARD_INTERNATIONAL4)
    BACKLIGHT_EFFECT_FORBIDDEN_KEYS.append(KEY_ID.KEYBOARD_INTERNATIONAL5)
# end class IngaJpnBacklightConfiguration

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
