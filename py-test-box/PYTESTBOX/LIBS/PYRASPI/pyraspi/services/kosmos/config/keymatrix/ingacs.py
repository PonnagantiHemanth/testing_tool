#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.ingacs
:brief: Inga CS universal & For MAC keyboards key layout definition
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
class IngaCSKeyMatrix(CommonKeyMatrix):
    """
    Configure the key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1aoQbFQDzgBQc31D6oADPxbttsl-H9oNNmVtIJnZMMi8/view#gid=0
    """
    HAS_KEYPAD = False

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        # Col_8, Row_0: N/A
        # Col_9, Row_0: N/A
        # Col_10, Row_0: N/A
        # Col_11, Row_0: N/A
        # Col_12, Row_0: N/A
        # Col_13, Row_0: N/A
        # Col_14, Row_0: N/A
        # Col_15, Row_0: N/A

        # ROW 1
        KEY_ID.HOST_1: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        # Col_8, Row_1: N/A
        # Col_9, Row_1: N/A
        # Col_10, Row_1: N/A
        # Col_11, Row_1: N/A
        # Col_12, Row_1: N/A
        # Col_13, Row_1: N/A
        # Col_14, Row_1: N/A
        # Col_15, Row_1: N/A

        # ROW 2
        KEY_ID.HOST_2: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        # Col_8, Row_2: N/A
        # Col_9, Row_2: N/A
        # Col_10, Row_2: N/A
        # Col_11, Row_2: N/A
        # Col_12, Row_2: N/A
        # Col_13, Row_2: N/A
        # Col_14, Row_2: N/A
        # Col_15, Row_2: N/A

        # ROW 3
        KEY_ID.HOST_3: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        # Col_8, Row_3: N/A
        # Col_9, Row_3: N/A
        # Col_10, Row_3: N/A
        # Col_11, Row_3: N/A
        # Col_12, Row_3: N/A
        # Col_13, Row_3: N/A
        # Col_14, Row_3: N/A
        # Col_15, Row_3: N/A

        # ROW 4
        KEY_ID.BACKLIGHT_DOWN: (KbdMatrix.COL_0, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        # Col_8, Row_4: N/A
        # Col_9, Row_4: N/A
        # Col_10, Row_4: N/A
        # Col_11, Row_4: N/A
        # Col_12, Row_4: N/A
        # Col_13, Row_4: N/A
        # Col_14, Row_4: N/A
        # Col_15, Row_4: N/A

        # ROW 5
        KEY_ID.BACKLIGHT_UP: (KbdMatrix.COL_0, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.FN_KEY: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_PAGE_UP: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        # Col_8, Row_5: N/A
        # Col_9, Row_5: N/A
        # Col_10, Row_5: N/A
        # Col_11, Row_5: N/A
        # Col_12, Row_5: N/A
        # Col_13, Row_5: N/A
        # Col_14, Row_5: N/A
        # Col_15, Row_5: N/A

        # ROW 6
        KEY_ID.DICTATION: (KbdMatrix.COL_0, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_1, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_HOME: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        # Col_8, Row_6: N/A
        # Col_9, Row_6: N/A
        # Col_10, Row_6: N/A
        # Col_11, Row_6: N/A
        # Col_12, Row_6: N/A
        # Col_13, Row_6: N/A
        # Col_14, Row_6: N/A
        # Col_15, Row_6: N/A

        # ROW 7
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_END: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        # Col_8, Row_7: N/A
        # Col_9, Row_7: N/A
        # Col_10, Row_7: N/A
        # Col_11, Row_7: N/A
        # Col_12, Row_7: N/A
        # Col_13, Row_7: N/A
        # Col_14, Row_7: N/A
        # Col_15, Row_7: N/A

        # ROW 8
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        # Col_8, Row_8: N/A
        # Col_9, Row_8: N/A
        # Col_10, Row_8: N/A
        # Col_11, Row_8: N/A
        # Col_12, Row_8: N/A
        # Col_13, Row_8: N/A
        # Col_14, Row_8: N/A
        # Col_15, Row_8: N/A

        # ROW 9
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_STOP: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        # Col_8, Row_9: N/A
        # Col_9, Row_9: N/A
        # Col_10, Row_9: N/A
        # Col_11, Row_9: N/A
        # Col_12, Row_9: N/A
        # Col_13, Row_9: N/A
        # Col_14, Row_9: N/A
        # Col_15, Row_9: N/A

        # ROW 10
        KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: (KbdMatrix.COL_0, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_1, KbdMatrix.ROW_10),
        # Col_2, Row_10: N/A
        KEY_ID.KEYBOARD_INTERNATIONAL5: (KbdMatrix.COL_3, KbdMatrix.ROW_10),
        # Col_4, Row_10: N/A
        # Col_5, Row_10: N/A
        # Col_6, Row_10: N/A
        # Col_7, Row_10: N/A
        # Col_8, Row_10: N/A
        # Col_9, Row_10: N/A
        # Col_10, Row_10: N/A
        # Col_11, Row_10: N/A
        # Col_12, Row_10: N/A
        # Col_13, Row_10: N/A
        # Col_14, Row_10: N/A
        # Col_15, Row_10: N/A

        # ROW 11
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_0, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_1, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_INTERNATIONAL1: (KbdMatrix.COL_2, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_INTERNATIONAL4: (KbdMatrix.COL_3, KbdMatrix.ROW_11),
        # Col_4, Row_11: N/A
        # Col_5, Row_11: N/A
        # Col_6, Row_11: N/A
        # Col_7, Row_11: N/A
        # Col_8, Row_11: N/A
        # Col_9, Row_11: N/A
        # Col_10, Row_11: N/A
        # Col_11, Row_11: N/A
        # Col_12, Row_11: N/A
        # Col_13, Row_11: N/A
        # Col_14, Row_11: N/A
        # Col_15, Row_11: N/A
    }

    FN_KEYS = {
        # Function Keys
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,                         # Col_0, Row_0
        KEY_ID.KEYBOARD_F1: KEY_ID.HOST_1,                              # Col_0, Row_1
        KEY_ID.KEYBOARD_F2: KEY_ID.HOST_2,                              # Col_0, Row_2
        KEY_ID.KEYBOARD_F3: KEY_ID.HOST_3,                              # Col_0, Row_3
        KEY_ID.KEYBOARD_F4: KEY_ID.BACKLIGHT_DOWN,                      # Col_0, Row_4
        KEY_ID.KEYBOARD_F5: KEY_ID.BACKLIGHT_UP,                        # Col_0, Row_5
        KEY_ID.KEYBOARD_F6: KEY_ID.DICTATION,                           # Col_0, Row_6
        KEY_ID.KEYBOARD_F7: KEY_ID.EMOJI_PANEL,                         # Col_0, Row_7
        KEY_ID.KEYBOARD_F8: KEY_ID.SCREEN_CAPTURE,                      # Col_0, Row_8
        KEY_ID.KEYBOARD_F9: KEY_ID.MUTE_MICROPHONE,                     # Col_0, Row_9
        KEY_ID.KEYBOARD_F10: KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT,       # Col_0, Row_10
        KEY_ID.KEYBOARD_F11: KEY_ID.PLAY_PAUSE,                         # Col_0, Row_11
        KEY_ID.FN_KEYBOARD_B: KEY_ID.KEYBOARD_B,                       # Col_4, Row_4
        KEY_ID.FN_KEYBOARD_SPACE_BAR: KEY_ID.KEYBOARD_SPACE_BAR,        # Col_5, Row_3
        KEY_ID.FN_KEYBOARD_RIGHT_ALT: KEY_ID.KEYBOARD_RIGHT_ALT,        # Col_5, Row_4
        KEY_ID.FN_KEYBOARD_DOWN_ARROW: KEY_ID.KEYBOARD_DOWN_ARROW,      # Col_5, Row_8
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_MUTE,                      # Col_6, Row_0
        KEY_ID.LIGHTNING_PATTERNS: KEY_ID.KEYBOARD_VOLUME_DOWN,         # Col_6, Row_1
        KEY_ID.SCREEN_LOCK: KEY_ID.KEYBOARD_DELETE_FORWARD,             # Col_6, Row_3
        KEY_ID.FN_KEYBOARD_BACKSPACE: KEY_ID.KEYBOARD_BACKSPACE,    # Col_6, Row_5
        KEY_ID.KEYBOARD_SCROLL_LOCK: KEY_ID.KEYBOARD_HOME,              # Col_6, Row_6
        KEY_ID.KEYBOARD_MENU: KEY_ID.KEYBOARD_END,                      # Col_6, Row_7
        KEY_ID.FN_KEYBOARD_ENTER: KEY_ID.KEYBOARD_RETURN_ENTER,         # Col_7, Row_4
        KEY_ID.KEYBOARD_INSERT: KEY_ID.KEYBOARD_PAGE_UP,                # Col_7, Row_5
        KEY_ID.FN_KEYBOARD_LEFT_ARROW: KEY_ID.KEYBOARD_LEFT_ARROW,      # Col_5, Row_7
        KEY_ID.FN_KEYBOARD_UP_ARROW: KEY_ID.KEYBOARD_UP_ARROW,          # Col_7, Row_8
        KEY_ID.FN_KEYBOARD_RIGHT_ARROW: KEY_ID.KEYBOARD_RIGHT_ARROW,    # Col_5, Row_9
    }
# end class IngaCSKeyMatrix


class IngaCSMacKeyMatrix(CommonKeyMatrix):
    """
    Configure the INGA Compact Size For MAC US layout key matrix

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ZSSQRrsWq_q86rT4A-5I1WdANSpDxpKVeOB2S8Dzml0/view#gid=0
    """
    HAS_KEYPAD = False

    KEYS = IngaCSKeyMatrix.KEYS.copy()
    FN_KEYS = IngaCSKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_DELETE_FORWARD]                                # Col_6, Row_3
    KEYS[KEY_ID.DO_NOT_DISTURB] = (KbdMatrix.COL_6, KbdMatrix.ROW_3)        # Col_6, Row_3
    del KEYS[KEY_ID.KEYBOARD_RIGHT_CONTROL]                                 # Col_5, Row_6
    KEYS[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION] = (KbdMatrix.COL_5, KbdMatrix.ROW_6)   # Col_5, Row_6
    KEYS[KEY_ID.KEYBOARD_PERIOD_AND_MORE] = KEYS[KEY_ID.KEYBOARD_STOP]      # Col_4, Row_9

    FN_KEYS[KEY_ID.SCREEN_LOCK] = KEY_ID.DO_NOT_DISTURB                     # Col_6, Row_3
    del FN_KEYS[KEY_ID.KEYBOARD_INSERT]                                     # Col_7, Row_5
    del FN_KEYS[KEY_ID.KEYBOARD_SCROLL_LOCK]                                # Col_6, Row_6
    del FN_KEYS[KEY_ID.KEYBOARD_MENU]                                       # Col_6, Row_7
# end class IngaCSMacKeyMatrix


class IngaCSMacUkLayoutKeyMatrix(CommonKeyMatrix):
    """
    Configure the INGA Compact Size For MAC Uk layout key matrix

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ZSSQRrsWq_q86rT4A-5I1WdANSpDxpKVeOB2S8Dzml0/view#gid=0
    """
    LAYOUT = 'UK'
    HAS_KEYPAD = False

    KEYS = IngaCSMacKeyMatrix.KEYS.copy()
    FN_KEYS = IngaCSMacKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]                            # Col_1, Row_0
    KEYS[KEY_ID.KEYBOARD_NO_US_1] = (KbdMatrix.COL_1, KbdMatrix.ROW_0)          # Col_1, Row_0
    KEYS[KEY_ID.KEYBOARD_NO_US_42] = (KbdMatrix.COL_7, KbdMatrix.ROW_4)         # Col_7, Row_4
    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]                                # Col_6, Row_9
    KEYS[KEY_ID.KEYBOARD_RETURN_ENTER] = (KbdMatrix.COL_6, KbdMatrix.ROW_9)     # Col_6, Row_9
    KEYS[KEY_ID.KEYBOARD_NO_US_45] = (KbdMatrix.COL_2, KbdMatrix.ROW_10)    # Col_2, Row_10
# end class IngaCSMacUkLayoutKeyMatrix


class IngaCSMacJpnLayoutKeyMatrix(CommonKeyMatrix):
    """
    Configure the INGA Compact Size For MAC japanese layout key matrix

    Key matrix map
    https://docs.google.com/spreadsheets/d/1ZSSQRrsWq_q86rT4A-5I1WdANSpDxpKVeOB2S8Dzml0/view#gid=0
    """
    LAYOUT = 'JPN'
    HAS_KEYPAD = False

    KEYS = IngaCSMacKeyMatrix.KEYS.copy()
    FN_KEYS = IngaCSMacKeyMatrix.FN_KEYS.copy()

    # Quote from Brian Lee: "The marketing decided to use the US layout for the Japanese keyboard.
    # That's why I changed the key code for Inga CS Mac.
    # The Inga CS Mac Japanese keyboard didn't use the JP layout."
    # del KEYS[KEY_ID.KEYBOARD_RIGHT_ALT]                                             # Col_5, Row_4
    # KEYS[KEY_ID.KATAHIRA] = (KbdMatrix.COL_5, KbdMatrix.ROW_4)                      # Col_5, Row_4
    # del FN_KEYS[KEY_ID.KEYBOARD_FN_RIGHT_ALT]                                       # Col_5, Row_4

    KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE] = (KbdMatrix.COL_7, KbdMatrix.ROW_4)   # Col_7, Row_4
    KEYS[KEY_ID.KEYBOARD_RETURN_ENTER] = (KbdMatrix.COL_6, KbdMatrix.ROW_9)         # Col_6, Row_9
    KEYS[KEY_ID.YEN] = (KbdMatrix.COL_2, KbdMatrix.ROW_10)                          # Col_2, Row_10
# end class IngaCSMacJpnLayoutKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
