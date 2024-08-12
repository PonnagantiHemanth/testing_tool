#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.fujian98
:brief: fujian98 keyboard key layout definition
:author: Masan Xu <mxu11@logitech.com>
:date: 2024/03/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pylibrary.emulator.keyid import KEY_ID


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class Fujian98KeyMatrix(CommonKeyMatrix):
    """
    Configure the US key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ooO1k3y5ymplfaR9VgFDexHGZN-mivJXcF21vP2f5X4/edit#gid=1548592914
    """
    HAS_KEYPAD = True
    KEYS = {
        # ROW_0
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.KEYPAD_ENTER: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.KEYPAD_3_AND_PAGE_DN: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        KEY_ID.KEYPAD_0_AND_INSERT: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        # COL_9, ROW_0: N/A

        # ROW_1
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_PLUS: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_6_AND_RIGHT_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.KEYPAD_PERIOD_AND_DELETE: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        # COL_9, ROW_1: N/A

        # ROW_2
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_MINUS: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_9_AND_PAGE_UP: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_2_AND_DOWN_ARROW: (KbdMatrix.COL_8, KbdMatrix.ROW_2),
        KEY_ID.KEYPAD_1_AND_END: (KbdMatrix.COL_9, KbdMatrix.ROW_2),

        # ROW_3
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.SMART_ACTION_3: (KbdMatrix.COL_6, KbdMatrix.ROW_3),  # KEYBOARD_PAGE_DOWN if SW is not installed
        KEY_ID.KEYPAD_ASTERISK: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.KEYPAD_5: (KbdMatrix.COL_8, KbdMatrix.ROW_3),
        KEY_ID.KEYPAD_4_AND_LEFT_ARROW: (KbdMatrix.COL_9, KbdMatrix.ROW_3),

        # ROW_4
        KEY_ID.DICTATION: (KbdMatrix.COL_0, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.FN_KEY: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.SMART_ACTION_2: (KbdMatrix.COL_6, KbdMatrix.ROW_4),  # KEYBOARD_PAGE_UP if SW is not installed
        KEY_ID.KEYPAD_FORWARD_SLASH: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.KEYPAD_8_AND_UP_ARROW: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_9, KbdMatrix.ROW_4),

        # ROW_5
        KEY_ID.BACKLIGHT_CYCLING: (KbdMatrix.COL_0, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.SMART_ACTION_1: (KbdMatrix.COL_6, KbdMatrix.ROW_5),  # KEYBOARD_END if SW is not installed
        KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYPAD_7_AND_HOME: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_9, KbdMatrix.ROW_5),

        # ROW_6
        KEY_ID.HOST_3: (KbdMatrix.COL_0, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_1, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_8, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_9, KbdMatrix.ROW_6),

        # ROW_7
        KEY_ID.HOST_2: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_8, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_9, KbdMatrix.ROW_7),

        # ROW_8
        KEY_ID.HOST_1: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_8, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_9, KbdMatrix.ROW_8),

        # ROW_9
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_8, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_9, KbdMatrix.ROW_9),
    }

    FN_KEYS = {
        # F-Row function Keys
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,                                     # Col_0, Row_9
        KEY_ID.KEYBOARD_F1: KEY_ID.HOST_1,                                          # Col_0, Row_8
        KEY_ID.KEYBOARD_F2: KEY_ID.HOST_2,                                          # Col_0, Row_7
        KEY_ID.KEYBOARD_F3: KEY_ID.HOST_3,                                          # Col_0, Row_6
        KEY_ID.KEYBOARD_F4: KEY_ID.BACKLIGHT_CYCLING,                               # Col_0, Row_5
        KEY_ID.KEYBOARD_F5: KEY_ID.DICTATION,                                       # Col_0, Row_4
        KEY_ID.KEYBOARD_F6: KEY_ID.EMOJI_PANEL,                                     # Col_0, Row_3
        KEY_ID.KEYBOARD_F7: KEY_ID.SCREEN_CAPTURE,                                  # Col_0, Row_2
        KEY_ID.KEYBOARD_F8: KEY_ID.MUTE_MICROPHONE,                                 # Col_0, Row_1
        KEY_ID.KEYBOARD_F9: KEY_ID.PLAY_PAUSE,                                      # Col_0, Row_0
        KEY_ID.KEYBOARD_F10: KEY_ID.KEYBOARD_MUTE,                                  # Col_6, Row_9
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_VOLUME_DOWN,                           # Col_6, Row_8
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_UP,                             # Col_6, Row_7

        # Keypad function keys
        KEY_ID.FN_KEYPAD_0: KEY_ID.KEYPAD_0_AND_INSERT,                             # Col_8, Row_0
        KEY_ID.FN_KEYPAD_1: KEY_ID.KEYPAD_1_AND_END,                                # Col_9, Row_2
        KEY_ID.FN_KEYPAD_2: KEY_ID.KEYPAD_2_AND_DOWN_ARROW,                         # Col_8, Row_2
        KEY_ID.FN_KEYPAD_3: KEY_ID.KEYPAD_3_AND_PAGE_DN,                            # Col_7, Row_0
        KEY_ID.FN_KEYPAD_4: KEY_ID.KEYPAD_4_AND_LEFT_ARROW,                         # Col_9, Row_3
        KEY_ID.FN_KEYPAD_6: KEY_ID.KEYPAD_6_AND_RIGHT_ARROW,                        # Col_7, Row_2
        KEY_ID.FN_KEYPAD_7: KEY_ID.KEYPAD_7_AND_HOME,                               # Col_8, Row_5
        KEY_ID.FN_KEYPAD_8: KEY_ID.KEYPAD_8_AND_UP_ARROW,                           # Col_8, Row_4
        KEY_ID.FN_KEYPAD_9: KEY_ID.KEYPAD_9_AND_PAGE_UP,                            # Col_7, Row_2
        KEY_ID.FN_KEYPAD_PERIOD: KEY_ID.KEYPAD_PERIOD_AND_DELETE,                   # Col_1, Row_8
        KEY_ID.FN_KEYPAD_ENTER: KEY_ID.KEYPAD_ENTER,                                # Col_6, Row_0

        # Hidden function keys
        KEY_ID.FN_KEYBOARD_LEFT_ARROW: KEY_ID.KEYBOARD_LEFT_ARROW,                  # Col_5, Row_2
        KEY_ID.FN_KEYBOARD_RIGHT_ARROW: KEY_ID.KEYBOARD_RIGHT_ARROW,                # Col_5, Row_0
        KEY_ID.FN_KEYBOARD_DOWN_ARROW: KEY_ID.KEYBOARD_DOWN_ARROW,                  # Col_5, Row_1
        KEY_ID.FN_KEYBOARD_UP_ARROW: KEY_ID.KEYBOARD_UP_ARROW,                      # Col_9, Row_4
        KEY_ID.KEYBOARD_HOME: KEY_ID.KEYBOARD_DELETE_FORWARD,                       # Col_6, Row_6
        KEY_ID.FN_KEYBOARD_ENTER: KEY_ID.KEYBOARD_RETURN_ENTER,                     # Col_9, Row_6
        KEY_ID.FN_KEYBOARD_BACKSPACE: KEY_ID.KEYBOARD_BACKSPACE,                    # Col_7, Row_6
        KEY_ID.FN_KEYBOARD_SPACE_BAR: KEY_ID.KEYBOARD_SPACE_BAR,                    # Col_5, Row_6
        KEY_ID.FN_KEYBOARD_RIGHT_CONTROL: KEY_ID.KEYBOARD_RIGHT_CONTROL,            # Col_5, Row_3
        KEY_ID.FN_KEYBOARD_RIGHT_ALT: KEY_ID.KEYBOARD_RIGHT_ALT,                    # Col_5, Row_5
        KEY_ID.FN_KEYBOARD_B: KEY_ID.KEYBOARD_B,                                    # Col_4, Row_4
    }
# end class Fujian98KeyMatrix



# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
