#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.fostermini
:brief: Foster Mini keyboard key layout definition
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
class FosterMiniKeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://drive.google.com/file/d/1bk-Yj__JwQ-De4xth1HJIp1GM6EjQ48L/view
    """
    HAS_KEYPAD = False

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        # Col_1, Row_0: N/A
        # Col_2, Row_0: N/A
        # Col_3, Row_0: N/A
        # Col_4, Row_0: N/A
        # Col_5, Row_0: N/A
        KEY_ID.MUHENKAN: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_9, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_10, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_11, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_12, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_13, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_NO_US_1: (KbdMatrix.COL_14, KbdMatrix.ROW_0),
        # Col_15, Row_0: N/A

        # ROW 1
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        # Col_1, Row_1: N/A
        # Col_2, Row_1: N/A
        # Col_3, Row_1: N/A
        # Col_4, Row_1: N/A
        # Col_5, Row_1: N/A
        KEY_ID.HENKAN: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_9, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_10, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_11, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_12, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_13, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_14, KbdMatrix.ROW_1),
        KEY_ID.BACKLIGHT_UP: (KbdMatrix.COL_15, KbdMatrix.ROW_1),

        # ROW 2
        # Col_0, Row_2: N/A
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        # Col_2, Row_2: N/A
        # Col_3, Row_2: N/A
        # Col_4, Row_2: N/A
        # Col_5, Row_2: N/A
        KEY_ID.KATAHIRA: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_8, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_9, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_10, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_11, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_12, KbdMatrix.ROW_2),
        # Col_13, Row_2: N/A
        # Col_14, Row_2: N/A
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_15, KbdMatrix.ROW_2),

        # ROW 3
        # Col_0, Row_3: N/A
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        # Col_2, Row_3: N/A
        # Col_3, Row_3: N/A
        # Col_4, Row_3: N/A
        # Col_5, Row_3: N/A
        KEY_ID.HANJA: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_NO_US_42: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_8, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_9, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_10, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_11, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_12, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_13, KbdMatrix.ROW_3),
        KEY_ID.DICTATION: (KbdMatrix.COL_14, KbdMatrix.ROW_3),
        # Col_15, Row_3: N/A

        # ROW 4
        # Col_0, Row_4: N/A
        # Col_1, Row_4: N/A
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        # Col_3, Row_4: N/A
        # Col_4, Row_4: N/A
        # Col_5, Row_4: N/A
        KEY_ID.HANGUEL: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_9, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_10, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_11, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_12, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_13, KbdMatrix.ROW_4),
        KEY_ID.YEN: (KbdMatrix.COL_14, KbdMatrix.ROW_4),
        # Col_15, Row_4: N/A

        # ROW 5
        # Col_0, Row_5: N/A
        # Col_1, Row_5: N/A
        # Col_2, Row_5: N/A
        KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        # Col_4, Row_5: N/A
        # Col_5, Row_5: N/A
        # Col_6, Row_5: N/A
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_9, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_10, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_11, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_12, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_13, KbdMatrix.ROW_5),
        # Col_14, Row_5: N/A, None US Key
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_15, KbdMatrix.ROW_5),

        # ROW 6
        # Col_0, Row_6: N/A
        # Col_1, Row_6: N/A
        # Col_2, Row_6: N/A
        # Col_3, Row_6: N/A
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        # Col_5, Row_6: N/A
        # Col_6, Row_6: N/A
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_8, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_9, KbdMatrix.ROW_6),
        KEY_ID.HOST_2: (KbdMatrix.COL_10, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_11, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_12, KbdMatrix.ROW_6),
        KEY_ID.RO: (KbdMatrix.COL_13, KbdMatrix.ROW_6),
        # Col_14, Row_6: N/A
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_15, KbdMatrix.ROW_6),

        # ROW 7
        # Col_0, Row_7: N/A
        # Col_1, Row_7: N/A
        # Col_2, Row_7: N/A
        # Col_3, Row_7: N/A
        # Col_4, Row_7: N/A
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.FN_KEY: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_8, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_9, KbdMatrix.ROW_7),
        KEY_ID.HOST_1: (KbdMatrix.COL_10, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_11, KbdMatrix.ROW_7),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_12, KbdMatrix.ROW_7),
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_13, KbdMatrix.ROW_7),
        KEY_ID.BACKLIGHT_DOWN: (KbdMatrix.COL_14, KbdMatrix.ROW_7),
        # Col_15, Row_7: N/A

        # ROW 8
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.HOST_3: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        # Col_5, Row_8: N/A
        # Col_6, Row_8: N/A
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_8, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_9, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_10, KbdMatrix.ROW_8),
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_11, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_12, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_13, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_14, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_15, KbdMatrix.ROW_8),
    }

    FN_KEYS = {
        # Function Keys W/ Fn
        # https://docs.google.com/spreadsheets/d/1o7SMziy4lCSGyPjUVWWoP1NNPxPyWU_2VcnX-T8tVBQ/view#gid=127882645
        KEY_ID.KEYBOARD_F1: KEY_ID.HOST_1,
        KEY_ID.KEYBOARD_F2: KEY_ID.HOST_2,
        KEY_ID.KEYBOARD_F3: KEY_ID.HOST_3,
        KEY_ID.KEYBOARD_F4: KEY_ID.BACKLIGHT_DOWN,
        KEY_ID.KEYBOARD_F5: KEY_ID.BACKLIGHT_UP,
        KEY_ID.KEYBOARD_F6: KEY_ID.DICTATION,
        KEY_ID.KEYBOARD_F7: KEY_ID.EMOJI_PANEL,
        KEY_ID.KEYBOARD_F8: KEY_ID.SCREEN_CAPTURE,
        KEY_ID.KEYBOARD_F9: KEY_ID.MUTE_MICROPHONE,
        KEY_ID.KEYBOARD_F10: KEY_ID.PLAY_PAUSE,
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_MUTE,
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_DOWN,
        KEY_ID.KEYBOARD_INSERT: KEY_ID.KEYBOARD_VOLUME_UP,
        KEY_ID.SCREEN_LOCK: KEY_ID.KEYBOARD_DELETE_FORWARD,
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,
        # Hidden function: Fn + Arrow Up, down ,left and right
        KEY_ID.KEYBOARD_PAGE_UP: KEY_ID.KEYBOARD_UP_ARROW,
        KEY_ID.KEYBOARD_PAGE_DOWN: KEY_ID.KEYBOARD_DOWN_ARROW,
        KEY_ID.FN_KEYBOARD_LEFT_ARROW: KEY_ID.KEYBOARD_LEFT_ARROW,
        KEY_ID.FN_KEYBOARD_RIGHT_ARROW: KEY_ID.KEYBOARD_RIGHT_ARROW,
        KEY_ID.FN_KEYBOARD_B: KEY_ID.KEYBOARD_B,
        KEY_ID.FN_KEYBOARD_BACKSPACE: KEY_ID.KEYBOARD_BACKSPACE,
        KEY_ID.FN_KEYBOARD_ENTER: KEY_ID.KEYBOARD_RETURN_ENTER,
        KEY_ID.FN_KEYBOARD_RIGHT_ALT: KEY_ID.KEYBOARD_RIGHT_ALT,
        KEY_ID.FN_KEYBOARD_RIGHT_CONTROL: KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,
        KEY_ID.FN_KEYBOARD_SPACE_BAR: KEY_ID.KEYBOARD_SPACE_BAR,
    }
# end class FosterMiniKeyMatrix


class FosterMiniForMacKeyMatrix(CommonKeyMatrix):
    """
    Configure the Foster Mini For Mac key matrix layout

    Key matrix map: https://drive.google.com/file/d/1bk-Yj__JwQ-De4xth1HJIp1GM6EjQ48L/view
    The keymatrix difference between Foster mini and Foster mini Mac:
    https://docs.google.com/document/d/1eN9u3-TYEqydG9cvgxcixx2yR75KwC6MOpQPOIE6jfg/view
    """
    HAS_KEYPAD = False

    KEYS = FosterMiniKeyMatrix.KEYS.copy()
    # Swap Left-Fn and Left-Ctrl
    KEYS[KEY_ID.FN_KEY] = (KbdMatrix.COL_2, KbdMatrix.ROW_4)
    KEYS[KEY_ID.KEYBOARD_LEFT_CONTROL] = (KbdMatrix.COL_6, KbdMatrix.ROW_7)
    # One F-Row function key is different
    del(KEYS[KEY_ID.KEYBOARD_DELETE_FORWARD])
    KEYS[KEY_ID.DO_NOT_DISTURB] = (KbdMatrix.COL_11, KbdMatrix.ROW_2)
# end class FosterMiniForMacKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
