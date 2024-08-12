#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.rangoon
:brief: Rangoon keyboard key layout definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/03/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class RangoonBLEProKeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1T1_kEYmUCsjLA9jGiN-4cCLU6KN6YSP-/view#gid=1242817251
    """
    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.HOST_1: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.SCREEN_LOCK: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.OS_SETTINGS: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_5, KbdMatrix.ROW_0),  # TODO: remove it in EU layout
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.OPEN_NEW_TAB: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_9, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_10, KbdMatrix.ROW_0),
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_11, KbdMatrix.ROW_0),
        # Col_12, Row_0: N/A in US layout, TODO: EU layout

        # ROW 1
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.MUHENKAN: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_2_AND_DOWN_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_9, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_10, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_11, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_12, KbdMatrix.ROW_1),

        # ROW 2
        # Col_0, Row_2: N/A
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.HENKAN: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_3_AND_PAGE_DN: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_8, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_9, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_10, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_ASTERISK: (KbdMatrix.COL_11, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_PERIOD_AND_DELETE: (KbdMatrix.COL_12, KbdMatrix.ROW_2),

        # ROW 3
        # Col_0, Row_3: N/A
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KATAHIRA: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYPAD_6_AND_RIGHT_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_NO_US_42: (KbdMatrix.COL_8, KbdMatrix.ROW_3),  # TODO: Multi-os key
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_9, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_10, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_11, KbdMatrix.ROW_3),
        KEY_ID.DICTATION: (KbdMatrix.COL_12, KbdMatrix.ROW_3),

        # ROW 4
        # Col_0, Row_4: N/A
        # Col_1, Row_4: N/A
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.HANJA: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_9_AND_PAGE_UP: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_9, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_10, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_FORWARD_SLASH: (KbdMatrix.COL_11, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_PLUS: (KbdMatrix.COL_12, KbdMatrix.ROW_4),

        # ROW 5
        # Col_0, Row_5: N/A
        # Col_1, Row_5: N/A
        KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.HANGUEL: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.RO: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.CLOSE_TAB: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_LOCKING_NUM_LOCK: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_9, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_10, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_11, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_12, KbdMatrix.ROW_5),

        # ROW 6
        KEY_ID.CALCULATOR: (KbdMatrix.COL_0, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_1, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.YEN: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        KEY_ID.BRIGHTNESS_UP: (KbdMatrix.COL_8, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_9, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_10, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_NO_US_64: (KbdMatrix.COL_11, KbdMatrix.ROW_6),  # TODO: EU layout
        KEY_ID.MISSION_CTRL_TASK_VIEW: (KbdMatrix.COL_12, KbdMatrix.ROW_6),

        # ROW 7
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.PRINT: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        # Col_2, Row_7: N/A
        KEY_ID.SHOW_DESKTOP: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.FN_KEY: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        KEY_ID.BRIGHTNESS_DOWN: (KbdMatrix.COL_8, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_9, KbdMatrix.ROW_7),
        KEY_ID.REFRESH: (KbdMatrix.COL_10, KbdMatrix.ROW_7),
        KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: (KbdMatrix.COL_11, KbdMatrix.ROW_7),
        KEY_ID.KEYPAD_ENTER: (KbdMatrix.COL_12, KbdMatrix.ROW_7),

        # ROW 8
        KEY_ID.KEYPAD_4_AND_LEFT_ARROW: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.KEYPAD_8_AND_UP_ARROW: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.KEYPAD_0_AND_INSERT: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYPAD_5: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_8, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_9, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_10, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_11, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_12, KbdMatrix.ROW_8),

        # ROW 9
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.KEYPAD_7_AND_HOME: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYPAD_1_AND_END: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYPAD_MINUS: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.LANGUAGE_SWITCH: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.AC_BACK: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.APP_SWITCH_LAUNCHPAD: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_8, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_9, KbdMatrix.ROW_9),
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_10, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_11, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_12, KbdMatrix.ROW_9),
    }

    FN_KEYS = {
        # Function Keys w/ Fn
        KEY_ID.KEYBOARD_F1: KEY_ID.BRIGHTNESS_DOWN,
        KEY_ID.KEYBOARD_F2: KEY_ID.BRIGHTNESS_UP,
        KEY_ID.KEYBOARD_F3: KEY_ID.MISSION_CTRL_TASK_VIEW,
        KEY_ID.KEYBOARD_F4: KEY_ID.APP_SWITCH_LAUNCHPAD,
        KEY_ID.KEYBOARD_F5: KEY_ID.DICTATION,
        KEY_ID.KEYBOARD_F6: KEY_ID.EMOJI_PANEL,
        KEY_ID.KEYBOARD_F7: KEY_ID.SCREEN_CAPTURE,
        KEY_ID.KEYBOARD_F8: KEY_ID.MUTE_MICROPHONE,
        KEY_ID.KEYBOARD_F9: KEY_ID.AC_BACK,
        KEY_ID.KEYBOARD_F10: KEY_ID.REFRESH,
        KEY_ID.KEYBOARD_F11: KEY_ID.OPEN_NEW_TAB,
        KEY_ID.KEYBOARD_F12: KEY_ID.CLOSE_TAB,
        KEY_ID.CONTEXTUAL_MENU: KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT,
        KEY_ID.KEYBOARD_INSERT: KEY_ID.LANGUAGE_SWITCH,
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,
        KEY_ID.FN_KEYBOARD_B: KEY_ID.KEYBOARD_B,
        KEY_ID.KEYBOARD_PAGE_DOWN: KEY_ID.KEYBOARD_DOWN_ARROW,
        KEY_ID.KEYBOARD_PAGE_UP: KEY_ID.KEYBOARD_UP_ARROW,
        KEY_ID.KEYBOARD_HOME: KEY_ID.KEYBOARD_LEFT_ARROW,
        KEY_ID.KEYBOARD_END: KEY_ID.KEYBOARD_RIGHT_ARROW,
        KEY_ID.KEYBOARD_DOWN_ARROW: KEY_ID.KEYPAD_2_AND_DOWN_ARROW,
        KEY_ID.KEYBOARD_UP_ARROW: KEY_ID.KEYPAD_8_AND_UP_ARROW,
        KEY_ID.KEYBOARD_LEFT_ARROW: KEY_ID.KEYPAD_4_AND_LEFT_ARROW,
        KEY_ID.KEYBOARD_RIGHT_ARROW: KEY_ID.KEYPAD_6_AND_RIGHT_ARROW
    }
# end class RangoonBLEProKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
