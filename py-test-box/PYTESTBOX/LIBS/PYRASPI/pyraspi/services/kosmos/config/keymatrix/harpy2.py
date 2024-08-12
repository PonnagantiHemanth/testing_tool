#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.harpy2
:brief: Harpy2 keyboard key layout definition
:author: Robin Liu <rliu10@logitech.com>
:date: 2023/10/30
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
class Harpy2KeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ooO1k3y5ymplfaR9VgFDexHGZN-mivJXcF21vP2f5X4/view#gid=475819092
    """
    HAS_KEYPAD = True

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_F2: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_F4: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_F6: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_F8: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_F10: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_F12: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_SCROLL_LOCK: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        KEY_ID.KEYPAD_ASTERISK: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        # Col_9, Row_0: N/A

        # ROW 1
        KEY_ID.KEYBOARD_F1: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F3: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F5: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F7: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F9: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F11: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PRINT_SCREEN: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PAUSE: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_MINUS: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        # Col_9, Row_1: N/A

        # ROW 2
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_8, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: (KbdMatrix.COL_9, KbdMatrix.ROW_2),

        # ROW 3
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.YEN: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_INSERT: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_8, KbdMatrix.ROW_3),
        KEY_ID.KEYPAD_FORWARD_SLASH: (KbdMatrix.COL_9, KbdMatrix.ROW_3),

        # ROW 4
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_0, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_8_AND_UP_ARROW: (KbdMatrix.COL_9, KbdMatrix.ROW_4),

        # ROW 5
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_0, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYPAD_7_AND_HOME: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.KEYPAD_9_AND_PAGE_UP: (KbdMatrix.COL_9, KbdMatrix.ROW_5),

        # ROW 6
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_0, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_1, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_NON_US_AND_TILDE: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYPAD_4_AND_LEFT_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        KEY_ID.KEYPAD_6_AND_RIGHT_ARROW: (KbdMatrix.COL_8, KbdMatrix.ROW_6),
        # Col_9, Row_6: N/A

        # ROW 7
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYPAD_5: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        KEY_ID.KEYPAD_PLUS: (KbdMatrix.COL_8, KbdMatrix.ROW_7),
        # Col_9, Row_7: N/A

        # ROW 8
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.RO: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        KEY_ID.KEYPAD_2_AND_DOWN_ARROW: (KbdMatrix.COL_8, KbdMatrix.ROW_8),
        # Col_9, Row_8: N/A

        # ROW 9
        KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.KEYPAD_1_AND_END: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        KEY_ID.KEYPAD_3_AND_PAGE_DN: (KbdMatrix.COL_8, KbdMatrix.ROW_9),
        # Col_9, Row_9: N/A

        # ROW 10
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_0, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_2, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_3, KbdMatrix.ROW_10),
        # KEY_ID.KEYBOARD_MENU: (KbdMatrix.COL_4, KbdMatrix.ROW_10),
        KEY_ID.CONTEXTUAL_MENU: (KbdMatrix.COL_4, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_6, KbdMatrix.ROW_10),
        KEY_ID.KEYPAD_PERIOD_AND_DELETE: (KbdMatrix.COL_7, KbdMatrix.ROW_10),
        # Col_8, Row_10: N/A
        # Col_9, Row_10: N/A

        # ROW 11
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_0, KbdMatrix.ROW_11),
        KEY_ID.MUHENKAN: (KbdMatrix.COL_1, KbdMatrix.ROW_11),
        KEY_ID.HENKAN: (KbdMatrix.COL_2, KbdMatrix.ROW_11),
        KEY_ID.FN_KEY: (KbdMatrix.COL_3, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_4, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_11),
        KEY_ID.KEYPAD_0_AND_INSERT: (KbdMatrix.COL_6, KbdMatrix.ROW_11),
        KEY_ID.KEYPAD_ENTER: (KbdMatrix.COL_7, KbdMatrix.ROW_11),
        # Col_8, Row_11: N/A
        # Col_9, Row_11: N/A

        # ROW 12
        KEY_ID.G_1: (KbdMatrix.COL_0, KbdMatrix.ROW_12),
        KEY_ID.G_3: (KbdMatrix.COL_1, KbdMatrix.ROW_12),
        KEY_ID.G_5: (KbdMatrix.COL_2, KbdMatrix.ROW_12),
        KEY_ID.G_7: (KbdMatrix.COL_3, KbdMatrix.ROW_12),
        KEY_ID.G_9: (KbdMatrix.COL_4, KbdMatrix.ROW_12),
        KEY_ID.BLE_CONNECTION: (KbdMatrix.COL_5, KbdMatrix.ROW_12),
        KEY_ID.DIMMING_KEY: (KbdMatrix.COL_6, KbdMatrix.ROW_12),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_7, KbdMatrix.ROW_12),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_8, KbdMatrix.ROW_12),
        # Col_9, Row_12: N/A

        # ROW 13
        KEY_ID.G_2: (KbdMatrix.COL_0, KbdMatrix.ROW_13),
        KEY_ID.G_4: (KbdMatrix.COL_1, KbdMatrix.ROW_13),
        KEY_ID.G_6: (KbdMatrix.COL_2, KbdMatrix.ROW_13),
        KEY_ID.G_8: (KbdMatrix.COL_3, KbdMatrix.ROW_13),
        KEY_ID.LS2_CONNECTION: (KbdMatrix.COL_4, KbdMatrix.ROW_13),
        KEY_ID.GAME_MODE_KEY: (KbdMatrix.COL_5, KbdMatrix.ROW_13),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_6, KbdMatrix.ROW_13),
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_7, KbdMatrix.ROW_13),
        # Col_8, Row_13: N/A
        # Col_9, Row_13: N/A
    }

    FN_KEYS = {
        KEY_ID.FKC_TOGGLE: KEY_ID.KEYBOARD_F1,
        KEY_ID.ONBOARD_PROFILE_1: KEY_ID.KEYBOARD_F2,
        KEY_ID.ONBOARD_PROFILE_2: KEY_ID.KEYBOARD_F3,
        KEY_ID.ONBOARD_PROFILE_3: KEY_ID.KEYBOARD_F4,
    }
# end class Harpy2KeyMatrix


class Harpy2JpnLayoutKeyMatrix:
    """
    Configure the JPN key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ooO1k3y5ymplfaR9VgFDexHGZN-mivJXcF21vP2f5X4/view#gid=840134108
    """
    LAYOUT = 'JPN'
    HAS_KEYPAD = True

    KEYS = Harpy2KeyMatrix.KEYS.copy()
    FN_KEYS = Harpy2KeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_RIGHT_ALT]
    del KEYS[KEY_ID.CONTEXTUAL_MENU]
    del KEYS[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION]
    KEYS[KEY_ID.KATAHIRA] = (KbdMatrix.COL_3, KbdMatrix.ROW_10)
# end class Harpy2JpnLayoutKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
