#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.gansu
:brief: Gansu keyboard key layout definition
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
class GansuBLEPROKeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1YbsjjT7-YI1LZR_S2inoHOBRLRXUyHxy1VLAg1LtBp8/view
    """
    HAS_KEYPAD = False

    KEYS = {
        # Row 0
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.HOST_1: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.HOST_3: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        KEY_ID.SMILING_FACE_WITH_HEART_SHAPED_EYES: (KbdMatrix.COL_8, KbdMatrix.ROW_0),

        # Row 1
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.HOST_2: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.SHOW_DESKTOP: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.DICTATION: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.LOUDLY_CRYING_FACE: (KbdMatrix.COL_8, KbdMatrix.ROW_1),

        # Row 2
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.EMOJI_SMILEY_WITH_TEARS: (KbdMatrix.COL_8, KbdMatrix.ROW_2),

        # Row 3
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.EMOJI_SMILEY: (KbdMatrix.COL_8, KbdMatrix.ROW_3),

        # Row 4
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_0, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_8, KbdMatrix.ROW_4),

        # Row 5
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_8, KbdMatrix.ROW_5),

        # Row 6
        KEY_ID.FN_KEY: (KbdMatrix.COL_0, KbdMatrix.ROW_6,),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_1, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION: (KbdMatrix.COL_8, KbdMatrix.ROW_6),

        # Row 7
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        # Col_8, Row_7: N/A

        # Row 8
        # Col_0, Row_8: N/A
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        # Col_8, Row_8: N/A

        # Row 9
        # Col_0, Row_9: N/A
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        # Col_8, Row_9: N/A
    }

    FN_KEYS = {
        # Function Keys
        KEY_ID.KEYBOARD_F1: KEY_ID.HOST_1,
        KEY_ID.KEYBOARD_F2: KEY_ID.HOST_2,
        KEY_ID.KEYBOARD_F3: KEY_ID.HOST_3,
        KEY_ID.KEYBOARD_F4: KEY_ID.SHOW_DESKTOP,
        KEY_ID.KEYBOARD_F5: KEY_ID.SCREEN_CAPTURE,
        KEY_ID.KEYBOARD_F6: KEY_ID.MUTE_MICROPHONE,
        KEY_ID.KEYBOARD_F7: KEY_ID.PREV_TRACK,
        KEY_ID.KEYBOARD_F8: KEY_ID.PLAY_PAUSE,
        KEY_ID.KEYBOARD_F9: KEY_ID.NEXT_TRACK,
        KEY_ID.KEYBOARD_F10: KEY_ID.KEYBOARD_MUTE,
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_VOLUME_DOWN,
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_UP,
        KEY_ID.FN_KEYBOARD_BACKSPACE: KEY_ID.KEYBOARD_BACKSPACE,
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,
        # Hidden function: Fn + Arrow Up, down ,left and right
        KEY_ID.KEYBOARD_HOME: KEY_ID.KEYBOARD_LEFT_ARROW,  # Left arrow + Fn
        KEY_ID.KEYBOARD_END: KEY_ID.KEYBOARD_RIGHT_ARROW,  # Right arrow + Fn
        KEY_ID.KEYBOARD_PAGE_UP: KEY_ID.KEYBOARD_UP_ARROW,  # Up arrow + Fn
        KEY_ID.KEYBOARD_PAGE_DOWN: KEY_ID.KEYBOARD_DOWN_ARROW,  # Down arrow + Fn
    }
# end class GansuBLEPROKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
