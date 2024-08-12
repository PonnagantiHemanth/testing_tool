#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.topaztkl
:brief: Topaz TKL keyboard key layout definition
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
class TopazTklCordedKeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1TDmtVgCcZwjHWAOVbC44zUF9c_fiJK5J/view#gid=1512151450
    """
    HAS_KEYPAD = False

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
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_9, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_10, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_11, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_12, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_13, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_14, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_15, KbdMatrix.ROW_0),

        # ROW 1
        KEY_ID.KEYBOARD_F1: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F3: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F5: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F7: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F9: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F11: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PRINT_SCREEN: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PAUSE: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_9, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_10, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_11, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_12, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_13, KbdMatrix.ROW_1),
        KEY_ID.YEN: (KbdMatrix.COL_14, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_INSERT: (KbdMatrix.COL_15, KbdMatrix.ROW_1),

        # ROW 2
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_8, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_9, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_10, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_11, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_12, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_13, KbdMatrix.ROW_2),
        KEY_ID.EURO_1: (KbdMatrix.COL_14, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_15, KbdMatrix.ROW_2),

        # ROW 3
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_8, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_9, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_10, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_11, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_12, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_13, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_14, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_15, KbdMatrix.ROW_3),

        # ROW 4
        # Col_0, Row_4: N/A
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_STOP: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.RO: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_9, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_10, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_11, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_MENU: (KbdMatrix.COL_12, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_13, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_14, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_15, KbdMatrix.ROW_4),

        # ROW 5
        # Col_0, Row_5: N/A
        KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.MUHENKAN: (KbdMatrix.COL_9, KbdMatrix.ROW_5),
        KEY_ID.HENKAN: (KbdMatrix.COL_10, KbdMatrix.ROW_5),
        KEY_ID.FN_KEY: (KbdMatrix.COL_11, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_12, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_13, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_14, KbdMatrix.ROW_5),
        # Col_15, Row_5: N/A

        # ROW 6
        # Col_0, Row_6: N/A
        # Col_1, Row_6: N/A
        # Col_2, Row_6: N/A
        KEY_ID.DIMMING_KEY: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        # Col_6, Row_6: N/A
        # Col_7, Row_6: N/A
        # Col_8, Row_6: N/A
        # Col_9, Row_6: N/A
        # Col_10, Row_6: N/A
        # Col_11, Row_6: N/A
        # Col_12, Row_6: N/A
        # Col_13, Row_6: N/A
        # Col_14, Row_6: N/A
        # Col_15, Row_6: N/A

        # ROW 7
        # Col_0, Row_7: N/A
        # Col_1, Row_7: N/A
        KEY_ID.GAME_MODE_KEY: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        # Col_5, Row_7: N/A
        # Col_6, Row_7: N/A
        # Col_7, Row_7: N/A
        # Col_8, Row_7: N/A
        # Col_9, Row_7: N/A
        # Col_10, Row_7: N/A
        # Col_11, Row_7: N/A
        # Col_12, Row_7: N/A
        # Col_13, Row_7: N/A
        # Col_14, Row_7: N/A
        # Col_15, Row_7: N/A
    }


# end class TopazTklCordedKeyMatrix


class TopazTklKeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1TDmtVgCcZwjHWAOVbC44zUF9c_fiJK5J/view#gid=1512151450
    """
    HAS_KEYPAD = False

    KEYS = TopazTklCordedKeyMatrix.KEYS.copy()
    # One additional key on topaz wireless
    KEYS[KEY_ID.LS2_BLE_CONNECTION_TOGGLE] = (KbdMatrix.COL_2, KbdMatrix.ROW_6)
# end class TopazTklKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
