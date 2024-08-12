#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.hospoa
:brief: Hospoa keyboard key layout definition
:author: Alexandre Lafaye
:date: 2023/03/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import HybridKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pylibrary.emulator.keyid import KEY_ID


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class HospoaKeyMatrix(HybridKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1yaaFYhZSc8SQ85mfsXinFZ7N9rpb_iRQ5NX5iV4alQQ
    """

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_F1: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        # Col_4, Row_0: N/A
        # Col_5, Row_0: N/A
        KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.LS2_CONNECTION: (KbdMatrix.COL_7, KbdMatrix.ROW_0),

        # ROW 1
        KEY_ID.KEYBOARD_F2: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_F3: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        # Col_5, Row_1: UK K-45 (KEY_ID.KEYBOARD_NO_US_45) Disabled by 0x1876 available key scanning
        KEY_ID.KEYPAD_ASTERISK: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.DIMMING_KEY: (KbdMatrix.COL_7, KbdMatrix.ROW_1),

        # ROW 2
        KEY_ID.KEYBOARD_F4: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_F5: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_7_AND_HOME: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.BLE_CONNECTION: (KbdMatrix.COL_7, KbdMatrix.ROW_2),

        # ROW 3
        KEY_ID.KEYBOARD_F6: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_F7: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYPAD_5: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.GAME_MODE_KEY: (KbdMatrix.COL_7, KbdMatrix.ROW_3),

        # ROW 4
        KEY_ID.KEYBOARD_F8: (KbdMatrix.COL_0, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_F9: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_PLUS: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_7, KbdMatrix.ROW_4),

        # ROW 5
        KEY_ID.KEYBOARD_F10: (KbdMatrix.COL_0, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_F11: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYPAD_2_AND_DOWN_ARROW: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_7, KbdMatrix.ROW_5),

        # ROW 6
        KEY_ID.KEYBOARD_F12: (KbdMatrix.COL_0, KbdMatrix.ROW_6),
        KEY_ID.PRINT: (KbdMatrix.COL_1, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYPAD_0_AND_INSERT: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_7, KbdMatrix.ROW_6),

        # ROW 7
        KEY_ID.KEYBOARD_SCROLL_LOCK: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_PAUSE: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        # Col_4, Row_7: K-56 (KEY_ID.RO) Disabled by 0x1876 available key scanning
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYPAD_ENTER: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_7, KbdMatrix.ROW_7),

        # ROW 8
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYPAD_FORWARD_SLASH: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.SIGNAL_N_POWER_GOOD: (KbdMatrix.COL_7, KbdMatrix.ROW_8),

        # ROW 9
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        # Col_5, Row_9: K-131 (KEY_ID.MUHENKAN) Disabled by 0x1876 available key scanning
        KEY_ID.KEYPAD_MINUS: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.SIGNAL_N_CHARGE: (KbdMatrix.COL_7, KbdMatrix.ROW_9),

        # ROW 10
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_0, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_1, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_2, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_3, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_4, KbdMatrix.ROW_10),
        # Col_5, Row_10: # K-132 (KEY_ID.HENKAN) Disabled by 0x1876 available key scanning
        KEY_ID.KEYPAD_9_AND_PAGE_UP: (KbdMatrix.COL_6, KbdMatrix.ROW_10),
        KEY_ID.SIGNAL_N_OFF: (KbdMatrix.COL_7, KbdMatrix.ROW_10),

        # ROW 11
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_0, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_1, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_2, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_3, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_4, KbdMatrix.ROW_11),
        KEY_ID.FN_KEY: (KbdMatrix.COL_5, KbdMatrix.ROW_11),
        KEY_ID.KEYPAD_4_AND_LEFT_ARROW: (KbdMatrix.COL_6, KbdMatrix.ROW_11),
        # Col_7, Row_11: N/A

        # ROW 12
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_0, KbdMatrix.ROW_12),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_1, KbdMatrix.ROW_12),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_2, KbdMatrix.ROW_12),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_3, KbdMatrix.ROW_12),
        KEY_ID.CONTEXTUAL_MENU: (KbdMatrix.COL_4, KbdMatrix.ROW_12),
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_5, KbdMatrix.ROW_12),
        KEY_ID.KEYPAD_6_AND_RIGHT_ARROW: (KbdMatrix.COL_6, KbdMatrix.ROW_12),
        # Col_7, Row_12: N/A

        # ROW 13
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_0, KbdMatrix.ROW_13),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_1, KbdMatrix.ROW_13),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_2, KbdMatrix.ROW_13),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_3, KbdMatrix.ROW_13),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_13),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_13),
        KEY_ID.KEYPAD_1_AND_END: (KbdMatrix.COL_6, KbdMatrix.ROW_13),
        # Col_7, Row_13: N/A

        # ROW 14
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_0, KbdMatrix.ROW_14),
        # Col_1, Row_14: JP K-14 (KEY_ID.YEN) Disabled by 0x1876 available key scanning
        # Col_2, Row_14: UK K-42 (KEY_ID.KEYBOARD_NO_US_42) Disabled by 0x1876 available key scanning
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_3, KbdMatrix.ROW_14),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_14),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_14),
        KEY_ID.KEYPAD_3_AND_PAGE_DN: (KbdMatrix.COL_6, KbdMatrix.ROW_14),
        # Col_7, Row_14: N/A

        # ROW 15
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_0, KbdMatrix.ROW_15),
        KEY_ID.KEYBOARD_INSERT: (KbdMatrix.COL_1, KbdMatrix.ROW_15),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_2, KbdMatrix.ROW_15),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_3, KbdMatrix.ROW_15),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_4, KbdMatrix.ROW_15),
        KEY_ID.KEYPAD_8_AND_UP_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_15),
        KEY_ID.KEYPAD_PERIOD_AND_DELETE: (KbdMatrix.COL_6, KbdMatrix.ROW_15),
        # Col_7, Row_15: N/A
    }

    # Special case for optical matrices, for elements that are not on the optical matrix
    # E.g. Control signals (on/off) or galvanic switches
    NON_OPTICAL_KEYS = [
        KEY_ID.LS2_CONNECTION,  # Col_7, Row_0
        KEY_ID.DIMMING_KEY,  # Col_7, Row_1
        KEY_ID.BLE_CONNECTION,  # Col_7, Row_2
        KEY_ID.GAME_MODE_KEY,  # Col_7, Row_3
        KEY_ID.PREV_TRACK,  # Col_7, Row_4
        KEY_ID.PLAY_PAUSE,  # Col_7, Row_5
        KEY_ID.NEXT_TRACK,  # Col_7, Row_6
        KEY_ID.KEYBOARD_MUTE,  # Col_7, Row_7
        KEY_ID.SIGNAL_N_POWER_GOOD,  # Col_7, Row_8
        KEY_ID.SIGNAL_N_CHARGE,  # Col_7, Row_9
        KEY_ID.SIGNAL_N_OFF,  # Col_7, Row_10
    ]

    # Special case for optical switches, the MAKE and BREAK instructions are reversed
    REVERSE_MAKE_LOGIC_KEYS = list(KEYS.keys() - set(NON_OPTICAL_KEYS))
# end class HospoaKeyMatrix


class HospoaMT8816SetupKeyMatrix(HospoaKeyMatrix):
    """
    Hospoa Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15

    Key matrix map
    https://docs.google.com/spreadsheets/d/1yaaFYhZSc8SQ85mfsXinFZ7N9rpb_iRQ5NX5iV4alQQ/edit#gid=1923596818
    """
    KEYS = HospoaKeyMatrix.KEYS.copy()
    NON_OPTICAL_KEYS = HospoaKeyMatrix.NON_OPTICAL_KEYS.copy()

    KEYS[KEY_ID.LS2_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_0)       # Col_15, Row_0
    KEYS[KEY_ID.DIMMING_KEY] = (KbdMatrix.COL_15, KbdMatrix.ROW_1)          # Col_15, Row_1
    KEYS[KEY_ID.BLE_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_2)       # Col_15, Row_2
    KEYS[KEY_ID.GAME_MODE_KEY] = (KbdMatrix.COL_15, KbdMatrix.ROW_3)        # Col_15, Row_3
    KEYS[KEY_ID.PREV_TRACK] = (KbdMatrix.COL_15, KbdMatrix.ROW_4)           # Col_15, Row_4
    KEYS[KEY_ID.PLAY_PAUSE] = (KbdMatrix.COL_15, KbdMatrix.ROW_5)           # Col_15, Row_5
    KEYS[KEY_ID.NEXT_TRACK] = (KbdMatrix.COL_15, KbdMatrix.ROW_6)           # Col_15, Row_6
    KEYS[KEY_ID.KEYBOARD_MUTE] = (KbdMatrix.COL_15, KbdMatrix.ROW_7)        # Col_15, Row_7
    del KEYS[KEY_ID.SIGNAL_N_POWER_GOOD]                                    # Col_15, Row_8
    del KEYS[KEY_ID.SIGNAL_N_CHARGE]                                        # Col_15, Row_9
    del KEYS[KEY_ID.SIGNAL_N_OFF]                                           # Col_15, Row_10

    # Special case for optical switches, the MAKE and BREAK instructions are reversed
    REVERSE_MAKE_LOGIC_KEYS = list(KEYS.keys() - set(NON_OPTICAL_KEYS))
# end class HospoaMT8816SetupKeyMatrix


class HospoaUkLayoutMT8816SetupKeyMatrix(HospoaKeyMatrix):
    """
    Hospoa Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15
    Configure the UK key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1yaaFYhZSc8SQ85mfsXinFZ7N9rpb_iRQ5NX5iV4alQQ/edit#gid=111600182
    """
    LAYOUT = 'UK'
    HAS_KEYPAD = True

    KEYS = HospoaMT8816SetupKeyMatrix.KEYS.copy()
    NON_OPTICAL_KEYS = HospoaMT8816SetupKeyMatrix.NON_OPTICAL_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]
    KEYS[KEY_ID.KEYBOARD_NO_US_45] = (KbdMatrix.COL_1, KbdMatrix.ROW_5)
    KEYS[KEY_ID.KEYBOARD_NO_US_42] = (KbdMatrix.COL_2, KbdMatrix.ROW_14)

    # Special case for optical switches, the MAKE and BREAK instructions are reversed
    REVERSE_MAKE_LOGIC_KEYS = list(KEYS.keys() - set(NON_OPTICAL_KEYS))
# end class HospoaUkLayoutMT8816SetupKeyMatrix


class HospoaRusLayoutMT8816SetupKeyMatrix(HospoaKeyMatrix):
    """
    Hospoa Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15
    Configure the Russia key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1yaaFYhZSc8SQ85mfsXinFZ7N9rpb_iRQ5NX5iV4alQQ/edit#gid=1753235459
    """
    LAYOUT = 'RUS'
    HAS_KEYPAD = True

    KEYS = HospoaMT8816SetupKeyMatrix.KEYS.copy()
    NON_OPTICAL_KEYS = HospoaMT8816SetupKeyMatrix.NON_OPTICAL_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]
    KEYS[KEY_ID.KEYBOARD_NO_US_42] = (KbdMatrix.COL_2, KbdMatrix.ROW_14)

    # Special case for optical switches, the MAKE and BREAK instructions are reversed
    REVERSE_MAKE_LOGIC_KEYS = list(KEYS.keys() - set(NON_OPTICAL_KEYS))
# end class HospoaRusLayoutMT8816SetupKeyMatrix


class HospoaJpnLayoutMT8816SetupKeyMatrix(HospoaKeyMatrix):
    """
    Hospoa Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15
    Configure the JPN key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1yaaFYhZSc8SQ85mfsXinFZ7N9rpb_iRQ5NX5iV4alQQ/edit#gid=1540174579
    """
    LAYOUT = 'JPN'
    HAS_KEYPAD = True

    KEYS = HospoaMT8816SetupKeyMatrix.KEYS.copy()
    NON_OPTICAL_KEYS = HospoaMT8816SetupKeyMatrix.NON_OPTICAL_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]
    del KEYS[KEY_ID.KEYBOARD_RIGHT_ALT]
    KEYS[KEY_ID.MUHENKAN] = (KbdMatrix.COL_5, KbdMatrix.ROW_9)
    KEYS[KEY_ID.HENKAN] = (KbdMatrix.COL_5, KbdMatrix.ROW_10)
    KEYS[KEY_ID.KATAHIRA] = (KbdMatrix.COL_4, KbdMatrix.ROW_11)
    KEYS[KEY_ID.RO] = (KbdMatrix.COL_4, KbdMatrix.ROW_7)
    KEYS[KEY_ID.KEYBOARD_NO_US_42] = (KbdMatrix.COL_2, KbdMatrix.ROW_14)

    # Special case for optical switches, the MAKE and BREAK instructions are reversed
    REVERSE_MAKE_LOGIC_KEYS = list(KEYS.keys() - set(NON_OPTICAL_KEYS))
# end class HospoaJpnLayoutMT8816SetupKeyMatrix
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
