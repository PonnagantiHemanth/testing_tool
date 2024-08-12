#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.jilin
:brief: Jilin keyboard key layout definition
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
class JilinWirelessKeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/13AVGbSNk9hfCgCSo4EZkYZiegatiZuxlLnwSiflxEs0/view
    """
    HAS_KEYPAD = False

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.HOST_2: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        # Col_7, Row_0: N/A
        # Col_8, Row_0: N/A
        # Col_9, Row_0: N/A
        # Col_10, Row_0: N/A
        # Col_11, Row_0: N/A
        # Col_12, Row_0: N/A
        # Col_13, Row_0: N/A
        # Col_14, Row_0: N/A
        # Col_15, Row_0: N/A

        # ROW 1
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.HOST_1: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.HOST_3: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.DICTATION: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        # Col_7, Row_1: N/A
        # Col_8, Row_1: N/A
        # Col_9, Row_1: N/A
        # Col_10, Row_1: N/A
        # Col_11, Row_1: N/A
        # Col_12, Row_1: N/A
        # Col_13, Row_1: N/A
        # Col_14, Row_1: N/A
        # Col_15, Row_1: N/A

        # ROW 2
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        # Col_7, Row_2: N/A
        # Col_8, Row_2: N/A
        # Col_9, Row_2: N/A
        # Col_10, Row_2: N/A
        # Col_11, Row_2: N/A
        # Col_12, Row_2: N/A
        # Col_13, Row_2: N/A
        # Col_14, Row_2: N/A
        # Col_15, Row_2: N/A

        # ROW 3
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_INTERNATIONAL3: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        # Col_7, Row_3: N/A
        # Col_8, Row_3: N/A
        # Col_9, Row_3: N/A
        # Col_10, Row_3: N/A
        # Col_11, Row_3: N/A
        # Col_12, Row_3: N/A
        # Col_13, Row_3: N/A
        # Col_14, Row_3: N/A
        # Col_15, Row_3: N/A

        # ROW 4
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_0, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        # Col_8, Row_4: N/A
        # Col_9, Row_4: N/A
        # Col_10, Row_4: N/A
        # Col_11, Row_4: N/A
        # Col_12, Row_4: N/A
        # Col_13, Row_4: N/A
        # Col_14, Row_4: N/A
        # Col_15, Row_4: N/A

        # ROW 5
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_0, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_INSERT: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        # Col_8, Row_5: N/A
        # Col_9, Row_5: N/A
        # Col_10, Row_5: N/A
        # Col_11, Row_5: N/A
        # Col_12, Row_5: N/A
        # Col_13, Row_5: N/A
        # Col_14, Row_5: N/A
        # Col_15, Row_5: N/A

        # ROW 6
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_0, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_1, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        # Col_8, Row_6: N/A
        # Col_9, Row_6: N/A
        # Col_10, Row_6: N/A
        # Col_11, Row_6: N/A
        # Col_12, Row_6: N/A
        # Col_13, Row_6: N/A
        # Col_14, Row_6: N/A
        # Col_15, Row_6: N/A

        # ROW 7
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_NON_US_AND_TILDE: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        # Col_8, Row_7: N/A
        # Col_9, Row_7: N/A
        # Col_10, Row_7: N/A
        # Col_11, Row_7: N/A
        # Col_12, Row_7: N/A
        # Col_13, Row_7: N/A
        # Col_14, Row_7: N/A
        # Col_15, Row_7: N/A

        # ROW 8
        KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_8, KbdMatrix.ROW_8),
        # Col_9, Row_8: N/A
        # Col_10, Row_8: N/A
        # Col_11, Row_8: N/A
        # Col_12, Row_8: N/A
        # Col_13, Row_8: N/A
        # Col_14, Row_8: N/A
        # Col_15, Row_8: N/A

        # ROW 9
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_STOP: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_INTERNATIONAL1: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        # Col_7, Row_9: N/A
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_8, KbdMatrix.ROW_9),
        # Col_9, Row_9: N/A
        # Col_10, Row_9: N/A
        # Col_11, Row_9: N/A
        # Col_12, Row_9: N/A
        # Col_13, Row_9: N/A
        # Col_14, Row_9: N/A
        # Col_15, Row_9: N/A

        # ROW 10
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_0, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_INTERNATIONAL5: (KbdMatrix.COL_1, KbdMatrix.ROW_10),
        # Col_2, Row_10: N/A
        KEY_ID.KEYBOARD_INTERNATIONAL4: (KbdMatrix.COL_3, KbdMatrix.ROW_10),
        # Col_4, Row_10: N/A
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_5, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_MENU: (KbdMatrix.COL_6, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_8, KbdMatrix.ROW_10),
        # Col_9, Row_10: N/A
        # Col_10, Row_10: N/A
        # Col_11, Row_10: N/A
        # Col_12, Row_10: N/A
        # Col_13, Row_10: N/A
        # Col_14, Row_10: N/A
        # Col_15, Row_10: N/A

        # ROW 11
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_0, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_11),
        # Col_2, Row_11: N/A
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_3, KbdMatrix.ROW_11),
        # Col_4, Row_11: N/A
        # Col_5, Row_11: N/A
        # Col_6, Row_11: N/A
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_7, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_8, KbdMatrix.ROW_11),
        # Col_9, Row_11: N/A
        # Col_10, Row_11: N/A
        # Col_11, Row_11: N/A
        # Col_12, Row_11: N/A
        # Col_13, Row_11: N/A
        # Col_14, Row_11: N/A
        # Col_15, Row_11: N/A
    }

    # Function Keys w/ Fn
    FN_KEYS = {
        KEY_ID.KEYBOARD_F1: KEY_ID.HOST_1,
        KEY_ID.KEYBOARD_F2: KEY_ID.HOST_2,
        KEY_ID.KEYBOARD_F3: KEY_ID.HOST_3,
        KEY_ID.KEYBOARD_F4: KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT,
        KEY_ID.KEYBOARD_F5: KEY_ID.DICTATION,
        KEY_ID.KEYBOARD_F6: KEY_ID.EMOJI_PANEL,
        KEY_ID.KEYBOARD_F7: KEY_ID.SCREEN_CAPTURE,
        KEY_ID.KEYBOARD_F8: KEY_ID.MUTE_MICROPHONE,
        KEY_ID.KEYBOARD_F9: KEY_ID.PLAY_PAUSE,
        KEY_ID.KEYBOARD_F10: KEY_ID.MUTE_MICROPHONE,
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_VOLUME_DOWN,
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_UP,
        KEY_ID.KEYBOARD_MENU: KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT,
        KEY_ID.SCREEN_LOCK: KEY_ID.KEYBOARD_HOME,
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,
    }
# end class JilinWirelessKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
