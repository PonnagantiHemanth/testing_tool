#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.yoko
:brief: Yoko keyboard key layout definition
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
class YokoBLEPROKeyMatrix(CommonKeyMatrix):
    """
    Configure the Yoko BLE PRO key matrix layout

    Key matrix map: https://drive.google.com/file/d/1Ve0DNKQPFTnR7z8mwOUwtVarR-Nl2Vb1/view
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
        # Col_6, Row_0: N/A
        # Col_7, Row_0: N/A
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_8, KbdMatrix.ROW_0),
        # Col_9, Row_0: N/A
        # Col_10, Row_0: N/A
        KEY_ID.KEYBOARD_DELETE_FORWARD: (KbdMatrix.COL_11, KbdMatrix.ROW_0),
        # Col_12, Row_0: N/A
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_13, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_H: (KbdMatrix.COL_14, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_15, KbdMatrix.ROW_0),
        KEY_ID.EMOJI_PANEL: (KbdMatrix.COL_16, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_N: (KbdMatrix.COL_17, KbdMatrix.ROW_0),


        # ROW 1
        KEY_ID.KEYBOARD_RIGHT_SHIFT: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        # Col_1, Row_1: N/A
        # Col_2, Row_1: N/A
        # Col_3, Row_1: N/A
        # Col_4, Row_1: N/A
        # Col_5, Row_1: N/A
        # Col_6, Row_1: N/A
        KEY_ID.KEYBOARD_W: (KbdMatrix.COL_7, KbdMatrix.ROW_1),
        KEY_ID.YEN: (KbdMatrix.COL_8, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: (KbdMatrix.COL_9, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: (KbdMatrix.COL_10, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_E: (KbdMatrix.COL_11, KbdMatrix.ROW_1),
        # Col_12, Row_1: N/A
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: (KbdMatrix.COL_13, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: (KbdMatrix.COL_14, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_VOLUME_UP: (KbdMatrix.COL_15, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_M: (KbdMatrix.COL_16, KbdMatrix.ROW_1),
        KEY_ID.MUTE_MICROPHONE: (KbdMatrix.COL_17, KbdMatrix.ROW_1),

        # ROW 2
        # Col_0, Row_2: N/A
        KEY_ID.KEYBOARD_LEFT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        # Col_2, Row_2: N/A
        # Col_3, Row_2: N/A
        # Col_4, Row_2: N/A
        # Col_5, Row_2: N/A
        # Col_6, Row_2: N/A
        # Col_7, Row_2: N/A
        # Col_8, Row_2: N/A
        # Col_9, Row_2: N/A
        # Col_10, Row_2: N/A
        # Col_11, Row_2: N/A
        # Col_12, Row_2: N/A
        KEY_ID.KEYBOARD_SPACE_BAR: (KbdMatrix.COL_13, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_14, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_G: (KbdMatrix.COL_15, KbdMatrix.ROW_2),
        KEY_ID.HOST_1: (KbdMatrix.COL_16, KbdMatrix.ROW_2),
        # Col_17, Row_2: N/A

        # ROW 3
        # Col_0, Row_3: N/A
        KEY_ID.KEYBOARD_RIGHT_ALT: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        # Col_2, Row_3: N/A
        # Col_3, Row_3: N/A
        # Col_4, Row_3: N/A
        # Col_5, Row_3: N/A
        # Col_6, Row_3: N/A KEY_ID.HANJA:  isn't configured in FW for any Layout
        KEY_ID.KEYBOARD_J: (KbdMatrix.COL_7, KbdMatrix.ROW_3),
        # Col_8, Row_3: N/A
        KEY_ID.KEYBOARD_O: (KbdMatrix.COL_9, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_D: (KbdMatrix.COL_10, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_K: (KbdMatrix.COL_11, KbdMatrix.ROW_3),
        KEY_ID.RO: (KbdMatrix.COL_12, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_13, KbdMatrix.ROW_3),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_14, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_15, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_DOWN_ARROW: (KbdMatrix.COL_16, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_RIGHT_ARROW: (KbdMatrix.COL_17, KbdMatrix.ROW_3),

        # ROW 4
        # Col_0, Row_4: N/A
        # Col_1, Row_4: N/A
        KEY_ID.KEYBOARD_LEFT_CONTROL: (KbdMatrix.COL_2, KbdMatrix.ROW_4),
        # Col_3, Row_4: N/A
        # Col_4, Row_4: N/A
        # Col_5, Row_4: N/A
        # Col_6, Row_4: N/A
        # Col_7, Row_4: N/A
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: (KbdMatrix.COL_8, KbdMatrix.ROW_4),
        # Col_9, Row_4: N/A
        # Col_10, Row_4: N/A
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: (KbdMatrix.COL_11, KbdMatrix.ROW_4),
        # Col_12, Row_4: N/A
        KEY_ID.KEYBOARD_TAB: (KbdMatrix.COL_13, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Q: (KbdMatrix.COL_14, KbdMatrix.ROW_4),
        KEY_ID.KEYBOARD_Y: (KbdMatrix.COL_15, KbdMatrix.ROW_4),
        KEY_ID.HOST_3: (KbdMatrix.COL_16, KbdMatrix.ROW_4),
        KEY_ID.SCREEN_CAPTURE: (KbdMatrix.COL_17, KbdMatrix.ROW_4),

        # ROW 5
        # Col_0, Row_5: N/A
        # Col_1, Row_5: N/A
        KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION: (KbdMatrix.COL_2, KbdMatrix.ROW_5),
        # Col_3, Row_5: N/A
        # Col_4, Row_5: N/A
        # Col_5, Row_5: N/A
        # Col_6, Row_5: N/A
        # Col_7, Row_5: N/A
        KEY_ID.KEYBOARD_A: (KbdMatrix.COL_8, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: (KbdMatrix.COL_9, KbdMatrix.ROW_5),
        KEY_ID.KEYBOARD_COMMA_AND_LESS: (KbdMatrix.COL_10, KbdMatrix.ROW_5),
        # Col_11, Row_5: N/A
        KEY_ID.KEYBOARD_F: (KbdMatrix.COL_12, KbdMatrix.ROW_5),
        # Col_13, Row_5: N/A
        # Col_14, Row_5: N/A
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_15, KbdMatrix.ROW_5),
        # Col_16, Row_5: N/A
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_17, KbdMatrix.ROW_5),

        # ROW 6
        # Col_0, Row_6: N/A
        # Col_1, Row_6: N/A
        # Col_2, Row_6: N/A
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        # Col_4, Row_6: N/A
        # Col_5, Row_6: N/A
        # Col_6, Row_6: N/A
        # Col_7, Row_6: N/A
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_8, KbdMatrix.ROW_6),
        # Col_9, Row_6: N/A
        # Col_10, Row_6: N/A
        # Col_11, Row_6: N/A
        # Col_12, Row_6: N/A
        KEY_ID.KEYBOARD_T: (KbdMatrix.COL_13, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_14, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_X: (KbdMatrix.COL_15, KbdMatrix.ROW_6),
        KEY_ID.DICTATION: (KbdMatrix.COL_16, KbdMatrix.ROW_6),
        KEY_ID.HOST_2: (KbdMatrix.COL_17, KbdMatrix.ROW_6),

        # ROW 7
        # Col_0, Row_7: N/A
        # Col_1, Row_7: N/A
        # Col_2, Row_7: N/A
        # Col_3, Row_7: N/A
        # Col_4, Row_7: N/A
        # Col_5, Row_7: N/A
        # Col_6, Row_7: N/A
        # Col_7, Row_7: N/A
        KEY_ID.KEYBOARD_L: (KbdMatrix.COL_8, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_S: (KbdMatrix.COL_9, KbdMatrix.ROW_7),
        # Col_10, Row_7: N/A
        # Col_11, Row_7: N/A
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: (KbdMatrix.COL_12, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_13, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: (KbdMatrix.COL_14, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_VOLUME_DOWN: (KbdMatrix.COL_15, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_UP_ARROW: (KbdMatrix.COL_16, KbdMatrix.ROW_7),
        KEY_ID.KEYBOARD_LEFT_ARROW: (KbdMatrix.COL_17, KbdMatrix.ROW_7),

        # ROW 8
        # Col_0, Row_8: N/A
        # Col_1, Row_8: N/A
        # Col_2, Row_8: N/A
        # Col_3, Row_8: N/A
        KEY_ID.KEYBOARD_ESCAPE: (KbdMatrix.COL_4, KbdMatrix.ROW_8),
        # Col_5, Row_8: N/A
        # Col_6, Row_8: N/A
        # Col_7, Row_8: N/A
        # Col_8, Row_8: N/A
        # Col_9, Row_8: N/A
        # Col_10, Row_8: N/A
        KEY_ID.KEYBOARD_U: (KbdMatrix.COL_11, KbdMatrix.ROW_8),
        # Col_12, Row_8: N/A
        KEY_ID.KEYBOARD_Z: (KbdMatrix.COL_13, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_14, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_15, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_B: (KbdMatrix.COL_16, KbdMatrix.ROW_8),
        KEY_ID.KEYBOARD_R: (KbdMatrix.COL_17, KbdMatrix.ROW_8),

        # ROW 9
        # Col_0, Row_9: N/A
        # Col_1, Row_9: N/A
        # Col_2, Row_9: N/A
        # Col_3, Row_9: N/A
        # Col_4, Row_9: N/A
        KEY_ID.KEYBOARD_CAPS_LOCK: (KbdMatrix.COL_5, KbdMatrix.ROW_9),
        # Col_6, Row_9: N/A
        KEY_ID.KEYBOARD_I: (KbdMatrix.COL_7, KbdMatrix.ROW_9),
        # Col_8, Row_9: N/A
        # Col_9, Row_9: N/A
        # Col_10, Row_9: N/A
        KEY_ID.KEYBOARD_P: (KbdMatrix.COL_11, KbdMatrix.ROW_9),
        # Col_12, Row_9: N/A
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: (KbdMatrix.COL_13, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_14, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_15, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_C: (KbdMatrix.COL_16, KbdMatrix.ROW_9),
        KEY_ID.KEYBOARD_V: (KbdMatrix.COL_17, KbdMatrix.ROW_9),

        # ROW 10
        # Col_0, Row_10: N/A
        # Col_1, Row_10: N/A
        # Col_2, Row_10: N/A
        # Col_3, Row_10: N/A
        # Col_4, Row_10: N/A
        # Col_5, Row_10: N/A
        KEY_ID.FN_KEY: (KbdMatrix.COL_6, KbdMatrix.ROW_10),
        # Col_7, Row_10: N/A
        # Col_8, Row_10: N/A
        # Col_9, Row_10: N/A
        # Col_10, Row_10: N/A
        # Col_11, Row_10: N/A
        # Col_12, Row_10: N/A
        # Col_13, Row_10: N/A
        # Col_14, Row_10: N/A
        # Col_15, Row_10: N/A
        # Col_16, Row_10: N/A
        # Col_17, Row_10: N/A
    }

    FN_KEYS = {
        # Function Keys W/ Fn
        # https://docs.google.com/spreadsheets/d/1o7SMziy4lCSGyPjUVWWoP1NNPxPyWU_2VcnX-T8tVBQ/view#gid=127882645
        KEY_ID.KEYBOARD_F1: KEY_ID.HOST_1,
        KEY_ID.KEYBOARD_F2: KEY_ID.HOST_2,
        KEY_ID.KEYBOARD_F3: KEY_ID.HOST_3,
        KEY_ID.KEYBOARD_F4: KEY_ID.EMOJI_PANEL,
        KEY_ID.KEYBOARD_F5: KEY_ID.DICTATION,
        KEY_ID.KEYBOARD_F6: KEY_ID.SCREEN_CAPTURE,
        KEY_ID.KEYBOARD_F7: KEY_ID.PREV_TRACK,
        KEY_ID.KEYBOARD_F8: KEY_ID.PLAY_PAUSE,
        KEY_ID.KEYBOARD_F9: KEY_ID.NEXT_TRACK,
        KEY_ID.KEYBOARD_F10: KEY_ID.KEYBOARD_MUTE,
        KEY_ID.KEYBOARD_F11: KEY_ID.KEYBOARD_VOLUME_DOWN,
        KEY_ID.KEYBOARD_F12: KEY_ID.KEYBOARD_VOLUME_UP,
        KEY_ID.KEYBOARD_INSERT: KEY_ID.MUTE_MICROPHONE,
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
# end class YokoBLEPROKeyMatrix


class YokoBLEPROUkLayoutKeyMatrix(YokoBLEPROKeyMatrix):
    """
    Configure the Yoko BLE PRO key matrix UK layout

    Key matrix map: https://drive.google.com/file/d/1Ve0DNKQPFTnR7z8mwOUwtVarR-Nl2Vb1/view
    """
    LAYOUT = 'UK'

    KEYS = YokoBLEPROKeyMatrix.KEYS.copy()
    FN_KEYS = YokoBLEPROKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]
    del KEYS[KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE]

    KEYS[KEY_ID.KEYBOARD_NO_US_42]: (KbdMatrix.COL_8, KbdMatrix.ROW_2)  # Col_8, Row_2
    KEYS[KEY_ID.KEYBOARD_NO_US_45]: (KbdMatrix.COL_17, KbdMatrix.ROW_2)  # Col_17, Row_2
    KEYS[KEY_ID.KEYBOARD_NO_US_1]: (KbdMatrix.COL_12, KbdMatrix.ROW_9)  # Col_12, Row_9
# end class YokoBLEPROUkLayoutKeyMatrix


class YokoBLEPROJpnLayoutKeyMatrix(YokoBLEPROKeyMatrix):
    """
        Configure the Yoko BLE PRO key matrix Japan layout

        Key matrix map: https://drive.google.com/file/d/1Ve0DNKQPFTnR7z8mwOUwtVarR-Nl2Vb1/view
        """
    LAYOUT = 'JPN'

    KEYS = YokoBLEPROKeyMatrix.KEYS.copy()
    FN_KEYS = YokoBLEPROKeyMatrix.FN_KEYS.copy()

    del KEYS[KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE]
    del KEYS[KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION]
    del FN_KEYS[KEY_ID.FN_KEYBOARD_RIGHT_CONTROL]

    KEYS[KEY_ID.MUHENKAN]: (KbdMatrix.COL_6, KbdMatrix.ROW_0)  # Col_6, Row_0
    KEYS[KEY_ID.HENKAN]: (KbdMatrix.COL_6, KbdMatrix.ROW_1)  # Col_6, Row_1
    KEYS[KEY_ID.KATAHIRA]: (KbdMatrix.COL_6, KbdMatrix.ROW_2)  # Col_6, Row_2
    KEYS[KEY_ID.HANJA]: (KbdMatrix.COL_6, KbdMatrix.ROW_3)  # Col_6, Row_3
    KEYS[KEY_ID.HANGUEL]: (KbdMatrix.COL_6, KbdMatrix.ROW_4)  # Col_6, Row_4
# end class YokoBLEPROJpnLayoutKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
