#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.nerv
:brief: Nerv keyboard key layout definition
:author: Robin Liu <rliu10@logitech.com>
:date: 2023/04/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pylibrary.emulator.keyid import KEY_ID


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class NervKeyMatrix(CommonKeyMatrix):
    """
    Configure the US key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1jJvgkHkJwCg33v7OsQ0Emwa0gfk_evjvLeDkKPbozRU

    0x1876
    https://docs.google.com/spreadsheets/d/1sPLZOXhl_yqF4G33epUZR-d0QREif-fTKaxVD4Qn-PA
    """
    HAS_KEYPAD = False

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_0, KbdMatrix.ROW_0),  # G-logo
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_3, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.BLE_CONNECTION: (KbdMatrix.COL_6, KbdMatrix.ROW_0),

        # ROW 1
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_3, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.LS2_CONNECTION: (KbdMatrix.COL_6, KbdMatrix.ROW_1),

        # ROW 2
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_3, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        # Col_6, Row_2: N/A

        # ROW 3
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        # Col_6, Row_3: N/A

        # ROW 4
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_0, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_1, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_3, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        # Col_6, Row_4: N/A

        # ROW 5
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_0, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_1, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_3, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        # Col_6, Row_5: N/A

        # ROW 6
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_0, KbdMatrix.ROW_6),
        # Disabled by 0x1876 available key scanning
        # KEY_ID.KEYBOARD_INTERNATIONAL3: (KbdMatrix.COL_1, KbdMatrix.ROW_6),  # K-14
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_2, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        # Disabled by 0x1876 available key scanning
        # KEY_ID.KEYBOARD_NON_US_AND_TILDE: (KbdMatrix.COL_4, KbdMatrix.ROW_6),  # K-42 (NONE US NUMBER)
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        # Col_6, Row_6: N/A

        # ROW 7
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        # Col_1, Row_7: N/A
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        # Col_6, Row_7: N/A

        # ROW 8
        # Col_0, Row_8: N/A
        # Col_1, Row_8: N/A
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        # Disabled by 0x1876 available key scanning
        # KEY_ID.KEYBOARD_INTERNATIONAL5: (KbdMatrix.COL_5, KbdMatrix.ROW_8),  # K-131

        # ROW 9
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        # Disabled by 0x1876 available key scanning
        # KEY_ID.KEYBOARD_NO_US_45: (KbdMatrix.COL_1, KbdMatrix.ROW_9),  # K-45 (UK_LEFT_SHIFT)
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        # Disabled by 0x1876 available key scanning
        # KEY_ID.KEYBOARD_INTERNATIONAL4: (KbdMatrix.COL_5, KbdMatrix.ROW_9),  # K-132

        # ROW 10
        # Col_0, Row_10: N/A
        # Col_1, Row_10: N/A
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_2, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_3, KbdMatrix.ROW_10),
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_4, KbdMatrix.ROW_10),  # JP: K-133
        KEY_ID.FN_KEY: (KbdMatrix.COL_5, KbdMatrix.ROW_10),
        # Col_6, Row_10: N/A

        # ROW 11
        # Disabled by 0x1876 available key scanning
        # KEY_ID.KEYBOARD_INTERNATIONAL1: (KbdMatrix.COL_0, KbdMatrix.ROW_11),  # K-56
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_1, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_2, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_3, KbdMatrix.ROW_11),
        KEY_ID.CONTEXTUAL_MENU: (KbdMatrix.COL_4, KbdMatrix.ROW_11),
        KEY_ID.KEYBOARD_RIGHT_CONTROL: (KbdMatrix.COL_5, KbdMatrix.ROW_11),
        # Col_6, Row_11: N/A
    }

    FN_KEYS = {
        # OOB Fn Layer Function Keys
        KEY_ID.ONBOARD_PROFILE_1: KEY_ID.KEYBOARD_S,                                # Col_4, Row_1
        KEY_ID.ONBOARD_PROFILE_2: KEY_ID.KEYBOARD_D,                                # Col_5, Row_1
        KEY_ID.ONBOARD_PROFILE_3: KEY_ID.KEYBOARD_F,                                # Col_4, Row_2
        KEY_ID.PREV_TRACK: KEY_ID.KEYBOARD_O,                                       # Col_3, Row_4
        KEY_ID.PLAY_PAUSE: KEY_ID.KEYBOARD_P,                                       # Col_2, Row_5
        KEY_ID.NEXT_TRACK: KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE,                  # Col_3, Row_5
        KEY_ID.KEYBOARD_MUTE: KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE,              # Col_2, Row_6
        KEY_ID.KEYBOARD_UP_ARROW: KEY_ID.KEYBOARD_K,                                # Col_4, Row_4
        KEY_ID.KEYBOARD_LEFT_ARROW: KEY_ID.KEYBOARD_M,                              # Col_2, Row_10
        KEY_ID.KEYBOARD_DOWN_ARROW: KEY_ID.KEYBOARD_COMMA_AND_LESS,                 # Col_3, Row_10
        KEY_ID.KEYBOARD_RIGHT_ARROW: KEY_ID.KEYBOARD_PERIOD_AND_MORE,               # Col_2, Row_11
        KEY_ID.KEYBOARD_F1: KEY_ID.KEYBOARD_1,                                      # Col_1, Row_0
        KEY_ID.KEYBOARD_F2: KEY_ID.KEYBOARD_2,                                      # Col_0, Row_1
        KEY_ID.KEYBOARD_F3: KEY_ID.KEYBOARD_3,                                      # Col_1, Row_1
        KEY_ID.KEYBOARD_F4: KEY_ID.KEYBOARD_4,                                      # Col_0, Row_2
        KEY_ID.KEYBOARD_F5: KEY_ID.KEYBOARD_5,                                      # Col_1, Row_2
        KEY_ID.KEYBOARD_F6: KEY_ID.KEYBOARD_6,                                      # Col_0, Row_3
        KEY_ID.KEYBOARD_F7: KEY_ID.KEYBOARD_7,                                      # Col_1, Row_3
        KEY_ID.KEYBOARD_F8: KEY_ID.KEYBOARD_8,                                      # Col_0, Row_4
        KEY_ID.KEYBOARD_F9: KEY_ID.KEYBOARD_9,                                      # Col_1, Row_4
        KEY_ID.KEYBOARD_F10: KEY_ID.KEYBOARD_0,                                     # Col_0, Row_5
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE,                   # Col_1, Row_5
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_EQUAL_AND_PLUS,                        # Col_0, Row_6
        KEY_ID.KEYBOARD_DELETE_FORWARD: KEY_ID.KEYBOARD_BACKSPACE,                  # Col_0, Row_7
        KEY_ID.KEYBOARD_SCROLL_LOCK: KEY_ID.KEYBOARD_U,                             # Col_3, Row_3
        KEY_ID.KEYBOARD_INSERT: KEY_ID.KEYBOARD_I,                                  # Col_2, Row_4
        KEY_ID.KEYBOARD_PRINT_SCREEN: KEY_ID.KEYBOARD_J,                            # Col_5, Row_3
        KEY_ID.KEYBOARD_PAGE_UP: KEY_ID.KEYBOARD_L,                                 # Col_5, Row_4
        KEY_ID.KEYBOARD_PAGE_DOWN: KEY_ID.KEYBOARD_SEMICOLON_AND_COLON,             # Col_4, Row_5
        KEY_ID.KEYBOARD_HOME: KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK,        # Col_5, Row_5
        KEY_ID.KEYBOARD_PAUSE: KEY_ID.KEYBOARD_N,                                   # Col_3, Row_9
        KEY_ID.KEYBOARD_END: KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK,       # Col_3, Row_11
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: KEY_ID.KEYBOARD_ESCAPE,             # Col_0, Row_0
        KEY_ID.FKC_TOGGLE: KEY_ID.KEYBOARD_A,                                       # Col_5, Row_0
        KEY_ID.BACKLIGHT_DOWN: KEY_ID.KEYBOARD_Z,                                   # Col_2, Row_7
        KEY_ID.BACKLIGHT_UP: KEY_ID.KEYBOARD_X,                                     # Col_3, Row_7
        KEY_ID.CYCLE_THROUGH_ANIMATION_EFFECTS: KEY_ID.KEYBOARD_C,                  # Col_2, Row_8
        KEY_ID.CYCLE_THROUGH_COLOR_EFFECT_SUB_SETTINGS: KEY_ID.KEYBOARD_V,          # Col_3, Row_8
    }
# end class NervKeyMatrix


class NervMT8816SetupKeyMatrix(NervKeyMatrix):
    """
    Nerv Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15
    """
    KEYS = NervKeyMatrix.KEYS.copy()
    FN_KEYS = NervKeyMatrix.FN_KEYS.copy()

    KEYS[KEY_ID.BLE_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_0)       # Col_15, Row_0
    KEYS[KEY_ID.LS2_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_1)       # Col_15, Row_1
# end class NervMT8816SetupKeyMatrix


class NervJpnLayoutKeyMatrix(NervKeyMatrix):
    """
    Nerv Japanese Key Matrix layout definition

    Key matrix map
    https://docs.google.com/spreadsheets/d/1jJvgkHkJwCg33v7OsQ0Emwa0gfk_evjvLeDkKPbozRU
    """
    LAYOUT = 'JPN'

    KEYS = NervKeyMatrix.KEYS.copy()
    FN_KEYS = NervKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]
    del KEYS[KEY_ID.KEYBOARD_RIGHT_ALT]

    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL3] = (KbdMatrix.COL_1, KbdMatrix.ROW_6)       # Col_1, Row_6: K-14
    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_4, KbdMatrix.ROW_6)     # Col_4, Row_6: K-42(NONE US NUMBER)
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL5] = (KbdMatrix.COL_5, KbdMatrix.ROW_8)       # Col_5, Row_6: K-131
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL4] = (KbdMatrix.COL_5, KbdMatrix.ROW_9)       # Col_5, Row_9: K-132
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL2] = (KbdMatrix.COL_4, KbdMatrix.ROW_10)      # Col_4, Row_10: K-133
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL1] = (KbdMatrix.COL_0, KbdMatrix.ROW_11)      # Col_0, Row_11: K-56
# end class NervJpnLayoutKeyMatrix


class NervJpnLayoutMT8816SetupKeyMatrix(NervJpnLayoutKeyMatrix):
    """
    Nerv Japanese Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15

    Key matrix map
    https://docs.google.com/spreadsheets/d/1jJvgkHkJwCg33v7OsQ0Emwa0gfk_evjvLeDkKPbozRU
    """
    KEYS = NervJpnLayoutKeyMatrix.KEYS.copy()
    FN_KEYS = NervJpnLayoutKeyMatrix.FN_KEYS.copy()

    KEYS[KEY_ID.BLE_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_0)       # Col_15, Row_0
    KEYS[KEY_ID.LS2_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_1)       # Col_15, Row_1
# end class NervJpnLayoutMT8816SetupKeyMatrix


class NervUkLayoutKeyMatrix(NervKeyMatrix):
    """
    Nerv UK Key Matrix layout definition

    Key matrix map
    https://docs.google.com/spreadsheets/d/1jJvgkHkJwCg33v7OsQ0Emwa0gfk_evjvLeDkKPbozRU
    """
    LAYOUT = 'UK'

    KEYS = NervKeyMatrix.KEYS.copy()
    FN_KEYS = NervKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]

    KEYS[KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE] = (KbdMatrix.COL_1, KbdMatrix.ROW_9)  # Col_1, Row_9: K-45
    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_4, KbdMatrix.ROW_6)  # Col_4, Row_6: K-42(NONE US NUMBER)
# end class NervUkLayoutKeyMatrix


class NervUkLayoutMT8816SetupKeyMatrix(NervUkLayoutKeyMatrix):
    """
    Nerv UK Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15

    Key matrix map
    https://docs.google.com/spreadsheets/d/1jJvgkHkJwCg33v7OsQ0Emwa0gfk_evjvLeDkKPbozRU
    """
    KEYS = NervUkLayoutKeyMatrix.KEYS.copy()
    FN_KEYS = NervUkLayoutKeyMatrix.FN_KEYS.copy()

    KEYS[KEY_ID.BLE_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_0)       # Col_15, Row_0
    KEYS[KEY_ID.LS2_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_1)       # Col_15, Row_1
# end class NervUkLayoutMT8816SetupKeyMatrix


class NervRusLayoutKeyMatrix(NervKeyMatrix):
    """
    Nerv Russia Key Matrix layout definition

    Key matrix map
    https://docs.google.com/spreadsheets/d/1jJvgkHkJwCg33v7OsQ0Emwa0gfk_evjvLeDkKPbozRU
    """
    LAYOUT = 'RUS'

    KEYS = NervKeyMatrix.KEYS.copy()
    FN_KEYS = NervKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]

    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = (KbdMatrix.COL_4, KbdMatrix.ROW_6)     # Col_4, Row_6: K-42(NONE US NUMBER)
# end class NervRusLayoutKeyMatrix


class NervRusLayoutMT8816SetupKeyMatrix(NervRusLayoutKeyMatrix):
    """
    Nerv Russia Key Matrix layout definition with MT8816 Special Setup that supports Galvanic switch control on Col_15

    Key matrix map
    https://docs.google.com/spreadsheets/d/1jJvgkHkJwCg33v7OsQ0Emwa0gfk_evjvLeDkKPbozRU
    """
    KEYS = NervRusLayoutKeyMatrix.KEYS.copy()
    FN_KEYS = NervRusLayoutKeyMatrix.FN_KEYS.copy()

    KEYS[KEY_ID.BLE_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_0)       # Col_15, Row_0
    KEYS[KEY_ID.LS2_CONNECTION] = (KbdMatrix.COL_15, KbdMatrix.ROW_1)       # Col_15, Row_1
# end class NervRusLayoutMT8816SetupKeyMatrix
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
