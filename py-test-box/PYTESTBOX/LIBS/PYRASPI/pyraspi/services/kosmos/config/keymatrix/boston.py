#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.boston
:brief: BostonUNV and BostonMAC keyboard key layout definition
:author: Masan Xu <mxu11@logitech.com>
:date: 2024/06/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pylibrary.emulator.keyid import KEY_ID


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BostonKeyMatrix(CommonKeyMatrix):
    """
    Configure the BostonUNV key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/16GfvzTuA3SJy1kAm_urYI4OR7XLc-OmjvpNpj57ngHg/edit#gid=1430003069
    """
    HAS_KEYPAD = True
    KEYS = {
        #ROW_0
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.HOST_1: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.HOST_2: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.HOST_3: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        #COL_4, ROW_0: N/A
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        KEY_ID.KEYPAD_ASTERISK: (KbdMatrix.COL_9, KbdMatrix.ROW_0),
        KEY_ID.KEYPAD_PERIOD_AND_DELETE: (KbdMatrix.COL_10, KbdMatrix.ROW_0),
        KEY_ID.KEYPAD_MINUS: (KbdMatrix.COL_11, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_12, KbdMatrix.ROW_0),

        #ROW_1
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        #COL_1, ROW_1: N/A
        #COL_2, ROW_1: N/A
        # TODO: This key is SMART_ACTION_4, but OOB function is CALCULATOR which is defined in Boston PRD
        KEY_ID.CALCULATOR: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        #COL_4, ROW_1: N/A
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_ENTER: (KbdMatrix.COL_9, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_3_AND_PAGE_DN: (KbdMatrix.COL_10, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_9_AND_PAGE_UP: (KbdMatrix.COL_11, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_PLUS: (KbdMatrix.COL_12, KbdMatrix.ROW_1),

        #ROW_2
        #COL_0, ROW_2: N/A
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        #COL_2, ROW_2: N/A
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        #COL_4, ROW_2: N/A
        KEY_ID.RO: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.YEN: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_1_AND_END: (KbdMatrix.COL_8, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_9, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_10, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_11, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_12, KbdMatrix.ROW_2),

        #ROW_3
        #COL_0, ROW_3: N/A
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        #COL_2, ROW_3: N/A
        KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        #COL_4, ROW_3: N/A
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYPAD_7_AND_HOME: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYPAD_FORWARD_SLASH: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_8, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_9, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_10, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_11, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_12, KbdMatrix.ROW_3),

        #ROW_4
        #COL_0, ROW_4: N/A
        #COL_1, ROW_4: N/A
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.SCREEN_LOCK: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        #COL_4, ROW_4: N/A
        KEY_ID.KEYPAD_0_AND_INSERT: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_2_AND_DOWN_ARROW: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_9, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_10, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_11, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_12, KbdMatrix.ROW_4),

        #ROW_5
        #COL_0, ROW_5: N/A
        #COL_1, ROW_5: N/A
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_INSERT: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        #COL_4, ROW_5: N/A
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_9, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_10, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_11, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_12, KbdMatrix.ROW_5),

        #ROW_6
        #COL_0, ROW_6: N/A
        #COL_1, ROW_6: N/A
        #COL_2, ROW_6: N/A
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        #COL_4, ROW_6: N/A
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        #(COL_10, ROW_6) to be moved here due to test_all_key_quadruplets
        KEY_ID.KEYBOARD_NO_US_1: (KbdMatrix.COL_10, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_8, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_9, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_11, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_12, KbdMatrix.ROW_6),

        #ROW_7
        KEY_ID.MUHENKAN: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.HENKAN: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.KATAHIRA: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        #COL_3, ROW_7: N/A
        #COL_4, ROW_7: N/A
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_8, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_9, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_10, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_11, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_NO_US_45: (KbdMatrix.COL_12, KbdMatrix.ROW_7),

        #ROW_8
        #COL_0, ROW_8: N/A
        KEY_ID.HANGUEL: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.HANJA: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        #COL_3, ROW_8: N/A
        KEY_ID.FN_KEY: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        #COL_8, ROW_8: N/A
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_9, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_10, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_11, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_12, KbdMatrix.ROW_8),

        #ROW_9
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYPAD_4_AND_LEFT_ARROW: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYPAD_8_AND_UP_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_NO_US_42: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.BRIGHTNESS_UP: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_8, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_9, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_10, KbdMatrix.ROW_9),
        KEY_ID.BRIGHTNESS_DOWN: (KbdMatrix.COL_11, KbdMatrix.ROW_9),
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_12, KbdMatrix.ROW_9),

        #ROW_10
        #COL_5, ROW_10 be moved here due to test_all_key_triplets
        KEY_ID.MISSION_CTRL_TASK_VIEW: (KbdMatrix.COL_5, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_0, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_1, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_2, KbdMatrix.ROW_10),
        KEY_ID.KEYPAD_5: (KbdMatrix.COL_3, KbdMatrix.ROW_10),
        KEY_ID.KEYPAD_6_AND_RIGHT_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_10),
        KEY_ID.DICTATION: (KbdMatrix.COL_6, KbdMatrix.ROW_10),
        KEY_ID.APP_SWITCH_LAUNCHPAD: (KbdMatrix.COL_7, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_8, KbdMatrix.ROW_10),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_9, KbdMatrix.ROW_10),
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_10, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_11, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_12, KbdMatrix.ROW_10),
    }
    FN_KEYS = {
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,
        KEY_ID.KEYBOARD_F1: KEY_ID.BRIGHTNESS_DOWN,
        KEY_ID.KEYBOARD_F2: KEY_ID.BRIGHTNESS_UP,
        KEY_ID.KEYBOARD_F3: KEY_ID.MISSION_CTRL_TASK_VIEW,
        KEY_ID.KEYBOARD_F4: KEY_ID.APP_SWITCH_LAUNCHPAD,
        KEY_ID.KEYBOARD_F5: KEY_ID.DICTATION,
        KEY_ID.KEYBOARD_F6: KEY_ID.EMOJI_PANEL,
        KEY_ID.KEYBOARD_F7: KEY_ID.MUTE_MICROPHONE,
        KEY_ID.KEYBOARD_F8: KEY_ID.PREV_TRACK,
        KEY_ID.KEYBOARD_F9: KEY_ID.PLAY_PAUSE,
        KEY_ID.KEYBOARD_F10: KEY_ID.NEXT_TRACK,
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_MUTE,
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_DOWN,
        KEY_ID.CONTEXTUAL_MENU: KEY_ID.SCREEN_CAPTURE,  # TODO: Confirm with FW owner about key code issue
        KEY_ID.KEYBOARD_SCROLL_LOCK: KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT,
        KEY_ID.FN_KEYPAD_1: KEY_ID.KEYPAD_1_AND_END,
        KEY_ID.FN_KEYPAD_2: KEY_ID.KEYPAD_2_AND_DOWN_ARROW,
        KEY_ID.FN_KEYPAD_3: KEY_ID.KEYPAD_3_AND_PAGE_DN,
        KEY_ID.FN_KEYPAD_4: KEY_ID.KEYPAD_4_AND_LEFT_ARROW,
        KEY_ID.FN_KEYPAD_6: KEY_ID.KEYPAD_6_AND_RIGHT_ARROW,
        KEY_ID.FN_KEYPAD_7: KEY_ID.KEYPAD_7_AND_HOME,
        KEY_ID.FN_KEYPAD_8: KEY_ID.KEYPAD_8_AND_UP_ARROW,
        KEY_ID.FN_KEYPAD_9: KEY_ID.KEYPAD_9_AND_PAGE_UP,
        KEY_ID.FN_KEYPAD_0: KEY_ID.KEYPAD_0_AND_INSERT,
        KEY_ID.FN_KEYPAD_PERIOD: KEY_ID.KEYPAD_PERIOD_AND_DELETE,
        KEY_ID.FN_KEYPAD_ENTER: KEY_ID.KEYPAD_ENTER,

        # Hidden functions which are defined in KBD guideline
        KEY_ID.FN_KEYBOARD_BACKSPACE: KEY_ID.KEYBOARD_BACKSPACE,
        KEY_ID.FN_KEYBOARD_ENTER: KEY_ID.KEYBOARD_RETURN_ENTER,
        KEY_ID.FN_KEYBOARD_B: KEY_ID.KEYBOARD_B,
        KEY_ID.FN_KEYBOARD_LEFT_ARROW: KEY_ID.KEYBOARD_LEFT_ARROW,
        KEY_ID.FN_KEYBOARD_RIGHT_ARROW: KEY_ID.KEYBOARD_RIGHT_ARROW,
        KEY_ID.FN_KEYBOARD_UP_ARROW: KEY_ID.KEYBOARD_UP_ARROW,
        KEY_ID.FN_KEYBOARD_DOWN_ARROW: KEY_ID.KEYBOARD_DOWN_ARROW,
        KEY_ID.FN_KEYBOARD_RIGHT_ALT: KEY_ID.KEYBOARD_RIGHT_ALT,
        KEY_ID.FN_KEYBOARD_SPACE_BAR: KEY_ID.KEYBOARD_SPACE_BAR,
    }
# end class BostonKeyMatrix

class BostonMacKeyMatrix(CommonKeyMatrix):
    """
    Configure the BostonMac key matrix layout

    https://docs.google.com/spreadsheets/d/16GfvzTuA3SJy1kAm_urYI4OR7XLc-OmjvpNpj57ngHg/edit#gid=1944729330
    """
    KEYS = BostonKeyMatrix.KEYS.copy()
    del (KEYS[KEY_ID.CALCULATOR])
    del (KEYS[KEY_ID.SCREEN_LOCK])
    del (KEYS[KEY_ID.KEYBOARD_INSERT])
    KEYS[KEY_ID.SMART_ACTION_4] = (KbdMatrix.COL_3, KbdMatrix.ROW_1)
    KEYS[KEY_ID.DO_NOT_DISTURB] = (KbdMatrix.COL_3, KbdMatrix.ROW_4)
    KEYS[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION] = (KbdMatrix.COL_3, KbdMatrix.ROW_7)

    FN_KEYS = {
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,
        KEY_ID.KEYBOARD_F1: KEY_ID.BRIGHTNESS_DOWN,
        KEY_ID.KEYBOARD_F2: KEY_ID.BRIGHTNESS_UP,
        KEY_ID.KEYBOARD_F3: KEY_ID.MISSION_CTRL_TASK_VIEW,
        KEY_ID.KEYBOARD_F4: KEY_ID.APP_SWITCH_LAUNCHPAD,
        KEY_ID.KEYBOARD_F5: KEY_ID.DICTATION,
        KEY_ID.KEYBOARD_F6: KEY_ID.EMOJI_PANEL,
        KEY_ID.KEYBOARD_F7: KEY_ID.MUTE_MICROPHONE,
        KEY_ID.KEYBOARD_F8: KEY_ID.PREV_TRACK,
        KEY_ID.KEYBOARD_F9: KEY_ID.PLAY_PAUSE,
        KEY_ID.KEYBOARD_F10: KEY_ID.NEXT_TRACK,
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_MUTE,
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_DOWN,
        KEY_ID.SCREEN_LOCK: KEY_ID.KEYBOARD_VOLUME_UP,
        KEY_ID.KEYBOARD_F13: KEY_ID.HOST_1,
        KEY_ID.KEYBOARD_F14: KEY_ID.HOST_2,
        KEY_ID.KEYBOARD_F15: KEY_ID.HOST_3,
        KEY_ID.KEYBOARD_F16: KEY_ID.SMART_ACTION_4,
        KEY_ID.KEYBOARD_F17: KEY_ID.SCREEN_CAPTURE,
        KEY_ID.KEYBOARD_F18: KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT,
        KEY_ID.KEYBOARD_F19: KEY_ID.DO_NOT_DISTURB,

        # Hidden functions which are defined in KBD guideline
        KEY_ID.FN_KEYBOARD_BACKSPACE: KEY_ID.KEYBOARD_BACKSPACE,
        KEY_ID.FN_KEYBOARD_ENTER: KEY_ID.KEYBOARD_RETURN_ENTER,
        KEY_ID.FN_KEYBOARD_B: KEY_ID.KEYBOARD_B,
        KEY_ID.FN_KEYBOARD_LEFT_ARROW: KEY_ID.KEYBOARD_LEFT_ARROW,
        KEY_ID.FN_KEYBOARD_RIGHT_ARROW: KEY_ID.KEYBOARD_RIGHT_ARROW,
        KEY_ID.FN_KEYBOARD_UP_ARROW: KEY_ID.KEYBOARD_UP_ARROW,
        KEY_ID.FN_KEYBOARD_DOWN_ARROW: KEY_ID.KEYBOARD_DOWN_ARROW,
        KEY_ID.FN_KEYBOARD_RIGHT_ALT: KEY_ID.KEYBOARD_RIGHT_ALT,
        KEY_ID.FN_KEYBOARD_SPACE_BAR: KEY_ID.KEYBOARD_SPACE_BAR,
    }
# end class BostonMacKeyMatrix
