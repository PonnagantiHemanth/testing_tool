#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.cinderellatkl
:brief: Cinderella TKL keyboard key layout definition
:author: YY Liu <yliu5@logitech.com>
:date: 2024/02/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CinderellaKeyMatrix(CommonKeyMatrix):
    """
    Configure the Cinderella TKL key matrix layout

    Key matrix map:
    https://docs.google.com/spreadsheets/d/1zg9WYya5aGZAJ3SHtPWoWLzhypp6CvarFqWRXBSA_t8/edit#gid=196209428
    """
    HAS_KEYPAD = False

    KEYS = {
        # ROW_0
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

        # ROW_1
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
        KEY_ID.KEYBOARD_INSERT: (KbdMatrix.COL_15, KbdMatrix.ROW_1),

        # ROW_2
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
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_15, KbdMatrix.ROW_2),

        # ROW_3
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

        # ROW_4
        # COL_0, ROW_4: N/A,
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        # COL_7, ROW_4: N/A,
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_9, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_10, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_11, KbdMatrix.ROW_4),
        KEY_ID.CONTEXTUAL_MENU: (KbdMatrix.COL_12, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_13, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_14, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_PAGE_DOWN: (KbdMatrix.COL_15, KbdMatrix.ROW_4),

        # ROW_5
        # COL_0, ROW_5: N/A,
        # COL_1, ROW_5: N/A,
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        # COL_9, ROW_5: N/A,
        # COL_10, ROW_5: N/A,
        KEY_ID.FN_KEY: (KbdMatrix.COL_11, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_12, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_13, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_14, KbdMatrix.ROW_5),
        # COL_15, ROW_5: N/A,

        # ROW_6
        # COL_0, ROW_6: N/A,
        # COL_1, ROW_6: N/A,
        KEY_ID.BLE_CONNECTION: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        # COL_3, ROW_6: N/A,
        # COL_4, ROW_6: N/A,
        # COL_5, ROW_6: N/A,
        # COL_6, ROW_6: N/A,
        # COL_7, ROW_6: N/A,
        # COL_8, ROW_6: N/A,
        # COL_9, ROW_6: N/A,
        # COL_10, ROW_6: N/A,
        # COL_11, ROW_6: N/A,
        # COL_12, ROW_6: N/A,
        # COL_13, ROW_6: N/A,
        # COL_14, ROW_6: N/A,
        # COL_15, ROW_6: N/A,

        # ROW_7
        # COL_0, ROW_7: N/A,
        KEY_ID.LS2_CONNECTION: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.GAME_MODE_KEY: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        # COL_3, ROW_7: N/A,
        # COL_4, ROW_7: N/A,
        # COL_5, ROW_7: N/A,
        # COL_6, ROW_7: N/A,
        # COL_7, ROW_7: N/A,
        # COL_8, ROW_7: N/A,
        # COL_9, ROW_7: N/A,
        # COL_10, ROW_7: N/A,
        # COL_11, ROW_7: N/A,
        # COL_12, ROW_7: N/A,
        # COL_13, ROW_7: N/A,
        # COL_14, ROW_7: N/A,
        # COL_15, ROW_7: N/A,
    }

    FN_KEYS = {
        KEY_ID.FKC_TOGGLE: KEY_ID.KEYBOARD_F1,
        KEY_ID.DIMMING_KEY: KEY_ID.KEYBOARD_F8,
        KEY_ID.PLAY_PAUSE: KEY_ID.KEYBOARD_F9,
        KEY_ID.KEYBOARD_STOP: KEY_ID.KEYBOARD_F10,
        KEY_ID.PREV_TRACK: KEY_ID.KEYBOARD_F11,
        KEY_ID.NEXT_TRACK: KEY_ID.KEYBOARD_F12,
        KEY_ID.KEYBOARD_MUTE: KEY_ID.KEYBOARD_PRINT_SCREEN,
        KEY_ID.KEYBOARD_VOLUME_DOWN: KEY_ID.KEYBOARD_SCROLL_LOCK,
        KEY_ID.KEYBOARD_VOLUME_UP: KEY_ID.KEYBOARD_PAUSE,
    }
# end class CinderellaKeyMatrix


class CinderellaUkLayoutKeyMatrix(CommonKeyMatrix):
    """
    Configure the Cinderella TKL key matrix UK layout

    Key matrix map:
    https://docs.google.com/spreadsheets/d/1zg9WYya5aGZAJ3SHtPWoWLzhypp6CvarFqWRXBSA_t8/edit#gid=196209428
    """
    LAYOUT = 'UK'

    KEYS = CinderellaKeyMatrix.KEYS.copy()
    FN_KEYS = CinderellaKeyMatrix.FN_KEYS.copy()

    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_14, KbdMatrix.ROW_2)
    KEYS[KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE] = (KbdMatrix.COL_1, KbdMatrix.ROW_5)
# end class CinderellaUkLayoutKeyMatrix


class CinderellaJpnLayoutKeyMatrix(CommonKeyMatrix):
    """
    Configure the Cinderella TKL key matrix JPN layout

    Key matrix map:
    https://docs.google.com/spreadsheets/d/1ooO1k3y5ymplfaR9VgFDexHGZN-mivJXcF21vP2f5X4/edit#gid=424992944
    """
    LAYOUT = 'JPN'

    KEYS = CinderellaKeyMatrix.KEYS.copy()
    FN_KEYS = CinderellaKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_RIGHT_ALT]
    KEYS[KEY_ID.YEN] = (KbdMatrix.COL_14, KbdMatrix.ROW_1)
    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_14, KbdMatrix.ROW_2)
    KEYS[KEY_ID.RO] = (KbdMatrix.COL_7, KbdMatrix.ROW_4)
    KEYS[KEY_ID.KATAHIRA] = (KbdMatrix.COL_11, KbdMatrix.ROW_4)
    KEYS[KEY_ID.MUHENKAN] = (KbdMatrix.COL_9, KbdMatrix.ROW_5)
    KEYS[KEY_ID.HENKAN] = (KbdMatrix.COL_10, KbdMatrix.ROW_5)
# end class CinderellaJpnLayoutKeyMatrix


class CinderellaCordedKeyMatrix(CommonKeyMatrix):
    """
    Configure the Cinderella TKL Corded key matrix layout

    Key matrix map:
    https://docs.google.com/spreadsheets/d/1zg9WYya5aGZAJ3SHtPWoWLzhypp6CvarFqWRXBSA_t8/edit#gid=196209428
    """
    HAS_KEYPAD = False

    KEYS = CinderellaKeyMatrix.KEYS.copy()
    FN_KEYS = CinderellaKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.BLE_CONNECTION]
    del KEYS[KEY_ID.LS2_CONNECTION]
    del KEYS[KEY_ID.GAME_MODE_KEY]
    KEYS[KEY_ID.GAME_MODE_KEY] = (KbdMatrix.COL_1, KbdMatrix.ROW_7)
# end class CinderellaCordedKeyMatrix


class CinderellaCordedUkLayoutKeyMatrix(CommonKeyMatrix):
    """
    Configure the Cinderella TKL Corded key matrix UK layout

    Key matrix map:
    https://docs.google.com/spreadsheets/d/1zg9WYya5aGZAJ3SHtPWoWLzhypp6CvarFqWRXBSA_t8/edit#gid=196209428
    """
    LAYOUT = 'UK'

    KEYS = CinderellaCordedKeyMatrix.KEYS.copy()
    FN_KEYS = CinderellaCordedKeyMatrix.FN_KEYS.copy()

    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_14, KbdMatrix.ROW_2)
    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_1, KbdMatrix.ROW_5)
# end class CinderellaCordedUkLayoutKeyMatrix


class CinderellaCordedJpnLayoutKeyMatrix(CommonKeyMatrix):
    """
    Configure the Cinderella TKL Corded key matrix JPN layout

    Key matrix map:
    https://docs.google.com/spreadsheets/d/1zg9WYya5aGZAJ3SHtPWoWLzhypp6CvarFqWRXBSA_t8/edit#gid=196209428
    """
    LAYOUT = 'JPN'

    KEYS = CinderellaCordedKeyMatrix.KEYS.copy()
    FN_KEYS = CinderellaCordedKeyMatrix.FN_KEYS.copy()

    KEYS[KEY_ID.YEN] = (KbdMatrix.COL_14, KbdMatrix.ROW_1)
    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_14, KbdMatrix.ROW_2)
    KEYS[KEY_ID.RO] = (KbdMatrix.COL_7, KbdMatrix.ROW_4)
    KEYS[KEY_ID.KATAHIRA] = (KbdMatrix.COL_11, KbdMatrix.ROW_4)
    KEYS[KEY_ID.MUHENKAN] = (KbdMatrix.COL_9, KbdMatrix.ROW_5)
    KEYS[KEY_ID.HENKAN] = (KbdMatrix.COL_10, KbdMatrix.ROW_5)
# end class CinderellaCordedJpnLayoutKeyMatrix

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
