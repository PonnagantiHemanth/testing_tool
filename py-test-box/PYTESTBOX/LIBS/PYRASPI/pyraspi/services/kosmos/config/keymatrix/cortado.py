#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.cortado
:brief: Cortado keyboard key layout definition
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/11/21
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
class CortadoKeyMatrix(CommonKeyMatrix):
    """
    Configure the Cortado key matrix layout

    Key matrix map: https://docs.google.com/spreadsheets/d/1_KnzulAOE8ecM3fPiZ-ISwaRBFBDFdCJ/edit#gid=57755210
    """
    HAS_KEYPAD = True

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_LEFT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        # Col_1, Row_0: N/A
        # Col_2, Row_0: N/A
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_4, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_5, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_6, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_7, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_9, KbdMatrix.ROW_0),

        # ROW 1
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        # Col_1, Row_1: N/A
        # Col_2, Row_1: N/A
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_5, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_6, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_9, KbdMatrix.ROW_1),

        # ROW 2
        # Col_0, Row_2: N/A
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        # Col_2, Row_2: N/A
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_4, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_5, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_6, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_7, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_9, KbdMatrix.ROW_2),

        # ROW 3
        # Col_0, Row_3: N/A
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        # Col_2, Row_3: N/A
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_5, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_6, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_8, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_9, KbdMatrix.ROW_3),

        # ROW 4
        # Col_0, Row_4: N/A
        # Col_1, Row_4: N/A
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_4, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_5, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_6, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_7, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_9, KbdMatrix.ROW_4),

        # ROW 5
        # Col_0, Row_5: N/A
        # Col_1, Row_5: N/A
        KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        # Col_3, Row_5: N/A
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_4, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_5, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_6, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_7, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_9, KbdMatrix.ROW_5),

        # ROW 6
        # Col_0, Row_6: N/A
        # Col_1, Row_6: N/A
        # Col_2, Row_6: N/A
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_5, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_6, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_7, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_8, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_9, KbdMatrix.ROW_6),

        # ROW 7
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_0, KbdMatrix.ROW_7),
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_1, KbdMatrix.ROW_7),
        KEY_ID.BRIGHTNESS_DOWN: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.HOST_1: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_5, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_6, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_7, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_8, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_9, KbdMatrix.ROW_7),

        # ROW 8
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_0, KbdMatrix.ROW_8),
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_1, KbdMatrix.ROW_8),
        KEY_ID.BRIGHTNESS_UP: (KbdMatrix.COL_2, KbdMatrix.ROW_8),
        KEY_ID.HOST_2: (KbdMatrix.COL_3, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_5, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_6, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_7, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_8, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_9, KbdMatrix.ROW_8),

        # ROW 9
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_0, KbdMatrix.ROW_9),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_1, KbdMatrix.ROW_9),
        KEY_ID.MISSION_CTRL_TASK_VIEW: (KbdMatrix.COL_2, KbdMatrix.ROW_9),
        KEY_ID.HOST_3: (KbdMatrix.COL_3, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_4, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_6, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_8, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_9, KbdMatrix.ROW_9),

        # ROW 10
        # Col_0, Row_10: N/A
        # Col_1, Row_10: N/A
        # Col_2, Row_10: N/A
        KEY_ID.FN_KEY: (KbdMatrix.COL_3, KbdMatrix.ROW_10),
        # Col_7, Row_10: N/A
        # Col_8, Row_10: N/A
        # Col_9, Row_10: N/A
    }

    FN_KEYS = {
        KEY_ID.KEYBOARD_F1: KEY_ID.HOST_1,
        KEY_ID.KEYBOARD_F2: KEY_ID.HOST_2,
        KEY_ID.KEYBOARD_F3: KEY_ID.HOST_3,
        KEY_ID.KEYBOARD_F4: KEY_ID.BRIGHTNESS_DOWN,
        KEY_ID.KEYBOARD_F5: KEY_ID.BRIGHTNESS_UP,
        KEY_ID.KEYBOARD_F6: KEY_ID.MISSION_CTRL_TASK_VIEW,
        KEY_ID.KEYBOARD_F7: KEY_ID.EMOJI_PANEL,
        KEY_ID.KEYBOARD_F8: KEY_ID.SCREEN_CAPTURE,
        KEY_ID.KEYBOARD_F9: KEY_ID.PLAY_PAUSE,
        KEY_ID.KEYBOARD_F10: KEY_ID.KEYBOARD_MUTE,
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_VOLUME_DOWN,
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_UP,
        KEY_ID.FN_LOCK: KEY_ID.KEYBOARD_ESCAPE,
        KEY_ID.SCREEN_LOCK: KEY_ID.KEYBOARD_DELETE_FORWARD,
        # Hidden function: Fn + Arrow Up, down ,left and right
        KEY_ID.FN_KEYBOARD_UP_ARROW: KEY_ID.KEYBOARD_UP_ARROW,
        KEY_ID.FN_KEYBOARD_DOWN_ARROW: KEY_ID.KEYBOARD_DOWN_ARROW,
        KEY_ID.FN_KEYBOARD_LEFT_ARROW: KEY_ID.KEYBOARD_LEFT_ARROW,
        KEY_ID.FN_KEYBOARD_RIGHT_ARROW: KEY_ID.KEYBOARD_RIGHT_ARROW,
        KEY_ID.FN_KEYBOARD_B: KEY_ID.KEYBOARD_B,
        KEY_ID.FN_KEYBOARD_BACKSPACE: KEY_ID.KEYBOARD_BACKSPACE,
        KEY_ID.FN_KEYBOARD_ENTER: KEY_ID.KEYBOARD_RETURN_ENTER,
        KEY_ID.FN_KEYBOARD_RIGHT_ALT: KEY_ID.KEYBOARD_RIGHT_ALT,
        KEY_ID.FN_KEYBOARD_RIGHT_CONTROL_OR_OPTION: KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,
        KEY_ID.FN_KEYBOARD_SPACE_BAR: KEY_ID.KEYBOARD_SPACE_BAR,
    }
# end class CortadoKeyMatrix


class CortadoUkLayoutKeyMatrix(CortadoKeyMatrix):
    """
    Configure the Cortado key matrix UK layout

    Key matrix map: https://docs.google.com/spreadsheets/d/1_KnzulAOE8ecM3fPiZ-ISwaRBFBDFdCJ/edit#gid=57755210
    """
    LAYOUT = 'UK'

    KEYS = CortadoKeyMatrix.KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]  # COl_9, Row_0

    KEYS[KEY_ID.KEYBOARD_NO_US_1] = (KbdMatrix.COL_8, KbdMatrix.ROW_2)
    KEYS[KEY_ID.KEYBOARD_NO_US_42] = (KbdMatrix.COL_7, KbdMatrix.ROW_1)
    KEYS[KEY_ID.KEYBOARD_NO_US_45] = (KbdMatrix.COL_4, KbdMatrix.ROW_10)
# end class CortadoUkLayoutKeyMatrix


class CortadoJpnLayoutKeyMatrix(CortadoKeyMatrix):
    """
    Configure the Cortado key matrix Japan layout

    Key matrix map: https://docs.google.com/spreadsheets/d/1_KnzulAOE8ecM3fPiZ-ISwaRBFBDFdCJ/edit#gid=57755210
    """
    LAYOUT = 'JPN'

    KEYS = CortadoKeyMatrix.KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]  # COl_9, Row_0

    KEYS[KEY_ID.MUHENKAN] = (KbdMatrix.COL_3, KbdMatrix.ROW_0)
    KEYS[KEY_ID.HENKAN] = (KbdMatrix.COL_3, KbdMatrix.ROW_1)
    KEYS[KEY_ID.KATAHIRA] = (KbdMatrix.COL_3, KbdMatrix.ROW_2)
    KEYS[KEY_ID.HANJA] = (KbdMatrix.COL_3, KbdMatrix.ROW_3)
    KEYS[KEY_ID.HANGUEL] = (KbdMatrix.COL_3, KbdMatrix.ROW_4)
    KEYS[KEY_ID.YEN] = (KbdMatrix.COL_6, KbdMatrix.ROW_10)
    KEYS[KEY_ID.RO] = (KbdMatrix.COL_5, KbdMatrix.ROW_10)
# end class CortadoJpnLayoutKeyMatrix


class CortadoForAppleKeyMatrix(CortadoKeyMatrix):
    """
    Configure the Cortado for Apple key matrix layout

    Key matrix map: https://docs.google.com/spreadsheets/d/1e98-IFi5l-fNDPzibuJE65E-2l9nO_WT/edit#gid=499836346
    """
    KEYS = CortadoKeyMatrix.KEYS.copy()
    FN_KEYS = {}

    del KEYS[KEY_ID.KEYBOARD_LEFT_CONTROL]  # COl_2, Row_4
    del KEYS[KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION]  # COl_2, Row_5
    del KEYS[KEY_ID.KEYBOARD_DELETE_FORWARD]  # COl_6, Row_5
    del KEYS[KEY_ID.FN_KEY]  # COl_3, Row_10
    del KEYS[KEY_ID.KEYBOARD_ESCAPE]  # COl_8, Row_1

    KEYS[KEY_ID.HOME] = (KbdMatrix.COL_8, KbdMatrix.ROW_1)
    KEYS[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION] = (KbdMatrix.COL_1, KbdMatrix.ROW_2)
    KEYS[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION] = (KbdMatrix.COL_1, KbdMatrix.ROW_3)
    KEYS[KEY_ID.KEYBOARD_LEFT_ALT] = (KbdMatrix.COL_2, KbdMatrix.ROW_4)
    KEYS[KEY_ID.KEYBOARD_RIGHT_ALT] = (KbdMatrix.COL_2, KbdMatrix.ROW_5)
    KEYS[KEY_ID.DO_NOT_DISTURB] = (KbdMatrix.COL_6, KbdMatrix.ROW_5)
    KEYS[KEY_ID.KEYBOARD_LEFT_CONTROL] = (KbdMatrix.COL_3, KbdMatrix.ROW_6)
    KEYS[KEY_ID.GLOBE_KEY] = (KbdMatrix.COL_3, KbdMatrix.ROW_10)
# end class CortadoForAppleKeyMatrix


class CortadoForAppleUkLayoutKeyMatrix(CortadoForAppleKeyMatrix):
    """
    Configure the Cortado for Apple key matrix UK layout

    Key matrix map: https://docs.google.com/spreadsheets/d/1e98-IFi5l-fNDPzibuJE65E-2l9nO_WT/edit#gid=499836346
    """
    LAYOUT = 'UK'

    KEYS = CortadoKeyMatrix.KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]  # COl_9, Row_0

    KEYS[KEY_ID.KEYBOARD_NO_US_1] = (KbdMatrix.COL_8, KbdMatrix.ROW_2)
    KEYS[KEY_ID.KEYBOARD_NO_US_42] = (KbdMatrix.COL_7, KbdMatrix.ROW_1)
    KEYS[KEY_ID.KEYBOARD_NO_US_45] = (KbdMatrix.COL_4, KbdMatrix.ROW_10)
# end class CortadoForAppleUkLayoutKeyMatrix


class CortadoForAppleJpnLayoutKeyMatrix(CortadoForAppleKeyMatrix):
    """
    Configure the Cortado for Apple key matrix Japan layout

    Key matrix map: https://docs.google.com/spreadsheets/d/1e98-IFi5l-fNDPzibuJE65E-2l9nO_WT/edit#gid=499836346
    """
    LAYOUT = 'JPN'

    KEYS = CortadoKeyMatrix.KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]  # COl_9, Row_0

    KEYS[KEY_ID.KANA] = (KbdMatrix.COL_3, KbdMatrix.ROW_4)
    KEYS[KEY_ID.RO] = (KbdMatrix.COL_5, KbdMatrix.ROW_10)
    KEYS[KEY_ID.YEN] = (KbdMatrix.COL_6, KbdMatrix.ROW_10)
# end class CortadoForAppleJpnLayoutKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
