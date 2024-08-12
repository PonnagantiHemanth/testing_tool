#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.norman
:brief: Norman keyboard key layout definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/03/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.kosmos.config.keymatrix.foster import FosterBLEPROKeyMatrix


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class NormanKeyMatrix(FosterBLEPROKeyMatrix):
    """
    Configure the Norman key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1EHwfuSTbvi1RyA2lSDkYA5DJbZRhmtK_qA6bavzyWew/view
    """
    KEYS = FosterBLEPROKeyMatrix.KEYS.copy()
    del (KEYS[KEY_ID.KEYBOARD_LOCKING_NUM_LOCK])                                                   # Col_14, Row_4
    KEYS[KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR] = (KbdMatrix.COL_14, KbdMatrix.ROW_4)

    FN_KEYS = FosterBLEPROKeyMatrix.FN_KEYS.copy()
    del (FN_KEYS[KEY_ID.FN_KEYBOARD_RIGHT_CONTROL])                                                # Col_3, Row_5
    FN_KEYS[KEY_ID.FN_KEYBOARD_RIGHT_CONTROL_OR_OPTION] = KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION  # Col_3, Row_5

# end class NormanKeyMatrix


class NormanForMacKeyMatrix(CommonKeyMatrix):
    """
    Configure the Norman For Mac key matrix layout

    https://docs.google.com/spreadsheets/d/1EHwfuSTbvi1RyA2lSDkYA5DJbZRhmtK_qA6bavzyWew/view#gid=975315651
    """
    KEYS = NormanKeyMatrix.KEYS.copy()

    KEYS[KEY_ID.HOST_1] = (KbdMatrix.COL_2, KbdMatrix.ROW_0)                            # Col_2, Row_0
    KEYS[KEY_ID.HOST_2] = (KbdMatrix.COL_3, KbdMatrix.ROW_0)                            # Col_3, Row_0
    KEYS[KEY_ID.HOST_3] = (KbdMatrix.COL_4, KbdMatrix.ROW_0)                            # Col_4, Row_0
    KEYS[KEY_ID.KEYBOARD_Q] = (KbdMatrix.COL_10, KbdMatrix.ROW_0)                       # Col_10, Row_0
    KEYS[KEY_ID.KEYBOARD_B] = (KbdMatrix.COL_11, KbdMatrix.ROW_0)                       # Col_11, Row_0
    del(KEYS[KEY_ID.CONTEXTUAL_MENU])                                                   # Col_14, Row_0
    KEYS[KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT] = (KbdMatrix.COL_14, KbdMatrix.ROW_0)     # Col_14, Row_0
    KEYS[KEY_ID.KEYBOARD_LEFT_ALT] = (KbdMatrix.COL_1, KbdMatrix.ROW_2)                 # Col_1, Row_2
    KEYS[KEY_ID.KEYBOARD_RIGHT_ALT] = (KbdMatrix.COL_1, KbdMatrix.ROW_3)                # Col_1, Row_3
    KEYS[KEY_ID.YEN] = (KbdMatrix.COL_5, KbdMatrix.ROW_4)                               # Col_5, Row_4
    KEYS[KEY_ID.KEYBOARD_RIGHT_CONTROL] = (KbdMatrix.COL_2, KbdMatrix.ROW_5)            # Col_2, Row_5
    del(KEYS[KEY_ID.KEYBOARD_INSERT])                                                   # Col_8, Row_5
    KEYS[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION] = (KbdMatrix.COL_3, KbdMatrix.ROW_6)       # Col_3, Row_6
    KEYS[KEY_ID.HANGUEL] = (KbdMatrix.COL_4, KbdMatrix.ROW_6)                           # Col_4, Row_6
    KEYS[KEY_ID.SCREEN_CAPTURE] = (KbdMatrix.COL_5, KbdMatrix.ROW_6)                    # Col_5, Row_6
    KEYS[KEY_ID.CALCULATOR] = (KbdMatrix.COL_0, KbdMatrix.ROW_7)                        # Col_0, Row_7
    del (KEYS[KEY_ID.SCREEN_LOCK])                                                      # Col_1, Row_7
    KEYS[KEY_ID.DO_NOT_DISTURB] = (KbdMatrix.COL_1, KbdMatrix.ROW_7)                    # Col_1, Row_7
    KEYS[KEY_ID.KEYPAD_EQUAL] = (KbdMatrix.COL_2, KbdMatrix.ROW_7)                      # Col_2, Row_7
    KEYS[KEY_ID.KEYBOARD_VOLUME_UP] = (KbdMatrix.COL_3, KbdMatrix.ROW_7)                # Col_3, Row_7
    KEYS[KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION] = (KbdMatrix.COL_4, KbdMatrix.ROW_7)  # Col_4, Row_7

    # Jira Ticket: https://jira.logitech.io/browse/NMM-1
    # TODO: After the NMM-1 resolved, these swapped keys should be removed and apply the final key layout definition
    #       to above KEYS table
    # Swap KEYBOARD_LEFT_ALT and KEYBOARD_LEFT_WIN_OR_OPTION
    KEYS[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION] = (KbdMatrix.COL_1, KbdMatrix.ROW_2)       # Col_1, Row_2
    KEYS[KEY_ID.KEYBOARD_LEFT_ALT] = (KbdMatrix.COL_3, KbdMatrix.ROW_6)                 # Col_3, Row_6
    # Swap KEYBOARD_RIGHT_ALT and KEYBOARD_RIGHT_WIN_OR_OPTION
    KEYS[KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION] = (KbdMatrix.COL_1, KbdMatrix.ROW_3)  # Col_1, Row_3
    KEYS[KEY_ID.KEYBOARD_RIGHT_ALT] = (KbdMatrix.COL_4, KbdMatrix.ROW_7)                # Col_4, Row_7

    FN_KEYS = NormanKeyMatrix.FN_KEYS.copy()
    # No secondary function printed on the keypad
    del (FN_KEYS[KEY_ID.KEYBOARD_SCROLL_LOCK])                          # Col_14, Row_0
    del (FN_KEYS[KEY_ID.FN_KEYBOARD_RIGHT_ALT])                         # Col_1, Row_3
    del (FN_KEYS[KEY_ID.FN_KEYBOARD_RIGHT_CONTROL_OR_OPTION])           # Col_3, Row_5
    del (FN_KEYS[KEY_ID.FN_KEYPAD_PERIOD])                              # Col_13, Row_2
    del (FN_KEYS[KEY_ID.FN_KEYPAD_ENTER])                               # Col_13, Row_7
    del (FN_KEYS[KEY_ID.FN_KEYPAD_0])                                   # Col_13, Row_6
    del (FN_KEYS[KEY_ID.FN_KEYPAD_1])                                   # Col_12, Row_6
    del (FN_KEYS[KEY_ID.FN_KEYPAD_2])                                   # Col_15, Row_5
    del (FN_KEYS[KEY_ID.FN_KEYPAD_3])                                   # Col_15, Row_6
    del (FN_KEYS[KEY_ID.FN_KEYPAD_4])                                   # Col_14, Row_3
    del (FN_KEYS[KEY_ID.FN_KEYPAD_6])                                   # Col_15, Row_7
    del (FN_KEYS[KEY_ID.FN_KEYPAD_7])                                   # Col_13, Row_3
    del (FN_KEYS[KEY_ID.FN_KEYPAD_8])                                   # Col_15, Row_2
    del (FN_KEYS[KEY_ID.FN_KEYPAD_9])                                   # Col_15, Row_8
    FN_KEYS[KEY_ID.SCREEN_LOCK] = KEY_ID.KEYBOARD_VOLUME_UP             # Col_3, Row_4
    FN_KEYS[KEY_ID.KEYBOARD_F13] = KEY_ID.HOST_1                        # Col_2, Row_0
    FN_KEYS[KEY_ID.KEYBOARD_F14] = KEY_ID.HOST_2                        # Col_3, Row_0
    FN_KEYS[KEY_ID.KEYBOARD_F15] = KEY_ID.HOST_3                        # Col_4, Row_0
    FN_KEYS[KEY_ID.KEYBOARD_F16] = KEY_ID.CALCULATOR                    # Col_0, Row_7
    FN_KEYS[KEY_ID.KEYBOARD_F17] = KEY_ID.SCREEN_CAPTURE                # Col_5, Row_6
    FN_KEYS[KEY_ID.KEYBOARD_F18] = KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT  # Col_14, Row_0
    FN_KEYS[KEY_ID.KEYBOARD_F19] = KEY_ID.DO_NOT_DISTURB                # Col_1, Row_7
# end class NormanForMacKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
