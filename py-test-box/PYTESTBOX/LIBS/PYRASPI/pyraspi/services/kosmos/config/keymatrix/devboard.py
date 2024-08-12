#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.devboard
:brief: NRF52 DEV board keyboard key layout definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/03/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pyraspi.services.daemon import Daemon


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DevBoardKeyMatrix(CommonKeyMatrix):
    """
    Configure the NRF52 DEV board key matrix default layout

    Key matrix map: cf kbdm_Matrix in kdb_map_cfg.c file
    """
    HAS_KEYPAD = False

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_7: (KbdMatrix.COL_0, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_4: (KbdMatrix.COL_1, KbdMatrix.ROW_0),
        KEY_ID.KEYBOARD_1: (KbdMatrix.COL_2, KbdMatrix.ROW_0),
        # Col_3, Row_0: N/A

        # ROW 1
        KEY_ID.KEYBOARD_8: (KbdMatrix.COL_0, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_5: (KbdMatrix.COL_1, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_2: (KbdMatrix.COL_2, KbdMatrix.ROW_1),
        KEY_ID.KEYBOARD_0: (KbdMatrix.COL_3, KbdMatrix.ROW_1),

        # ROW 2
        KEY_ID.KEYBOARD_9: (KbdMatrix.COL_0, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_6: (KbdMatrix.COL_1, KbdMatrix.ROW_2),
        KEY_ID.KEYBOARD_3: (KbdMatrix.COL_2, KbdMatrix.ROW_2),
        KEY_ID.FN_KEY: (KbdMatrix.COL_3, KbdMatrix.ROW_2),

        # ROW 3
        KEY_ID.KEYPAD_PLUS: (KbdMatrix.COL_0, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_BACKSPACE: (KbdMatrix.COL_1, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_RETURN_ENTER: (KbdMatrix.COL_2, KbdMatrix.ROW_3),
        KEY_ID.KEYBOARD_POWER: (KbdMatrix.COL_3, KbdMatrix.ROW_3),
    }

    FN_KEYS = {
        # Function Keys W/ Fn
        KEY_ID.DESKTOP_SYSTEM_SLEEP: KEY_ID.KEYBOARD_0,
        KEY_ID.HOST_1: KEY_ID.KEYBOARD_1,
        KEY_ID.HOST_2: KEY_ID.KEYBOARD_2,
        KEY_ID.HOST_3: KEY_ID.KEYBOARD_3,
        KEY_ID.COMPOUND_ALT_TAB: KEY_ID.KEYBOARD_4,
        KEY_ID.KEYBOARD_MUTE: KEY_ID.KEYBOARD_5,
        KEY_ID.COMPOUND_HOME: KEY_ID.KEYBOARD_6,
        KEY_ID.LEFT_BUTTON: KEY_ID.KEYBOARD_7,
        KEY_ID.COMPOUND_PASTE: KEY_ID.KEYBOARD_8,
        KEY_ID.COMPOUND_CTRL_ALT_DEL: KEY_ID.KEYBOARD_9,
        KEY_ID.CONNECT_BUTTON: KEY_ID.KEYBOARD_BACKSPACE,
        KEY_ID.KEYPAD_MINUS: KEY_ID.KEYPAD_PLUS,
    }
# end class DevBoardKeyMatrix


class DevBoardIso104LayoutKeyMatrix(DevBoardKeyMatrix):
    """
    Configure the NRF52 DEV board key matrix ISO 104 layout

    NB: HOME_ISO104_IDX (Fn+'6' (ISO-104) -> d-o-m) replace HOME_DFT_IDX
    """
    LAYOUT = 'RUS'

    KEYS = DevBoardKeyMatrix.KEYS.copy()
    FN_KEYS = DevBoardKeyMatrix.FN_KEYS.copy()

    del FN_KEYS[KEY_ID.COMPOUND_HOME]                           # Col_1, Row_2
    FN_KEYS[KEY_ID.COMPOUND_HOME_ISO_104] = KEY_ID.KEYBOARD_6   # Col_1, Row_2
# end class DevBoardIso104LayoutKeyMatrix


class DevBoardIso105LayoutKeyMatrix(DevBoardKeyMatrix):
    """
    Configure the NRF52 DEV board key matrix ISO 105 layout

    NB: HOME_ISO105_IDX (Fn+'6' (ISO-105) -> m-a-i-s-o-n) replace HOME_DFT_IDX
    """
    LAYOUT = 'UK'

    KEYS = DevBoardKeyMatrix.KEYS.copy()
    FN_KEYS = DevBoardKeyMatrix.FN_KEYS.copy()

    del FN_KEYS[KEY_ID.COMPOUND_HOME]                           # Col_1, Row_2
    FN_KEYS[KEY_ID.COMPOUND_HOME_ISO_105] = KEY_ID.KEYBOARD_6   # Col_1, Row_2
# end class DevBoardIso105LayoutKeyMatrix


class DevBoardIso107LayoutKeyMatrix(DevBoardKeyMatrix):
    """
    Configure the NRF52 DEV board key matrix ISO 107 layout

    NB: HOME_ISO107_IDX (Fn+'6' (ISO-107) -> l-a-r) replace HOME_DFT_IDX
    """
    LAYOUT = 'BRA'

    KEYS = DevBoardKeyMatrix.KEYS.copy()
    FN_KEYS = DevBoardKeyMatrix.FN_KEYS.copy()

    del FN_KEYS[KEY_ID.COMPOUND_HOME]                           # Col_1, Row_2
    FN_KEYS[KEY_ID.COMPOUND_HOME_ISO_107] = KEY_ID.KEYBOARD_6   # Col_1, Row_2
# end class DevBoardIso107LayoutKeyMatrix


class DevBoardJis109LayoutKeyMatrix(DevBoardKeyMatrix):
    """
    Configure the NRF52 DEV board key matrix JIS 109 layout

    NB: HOME_JIS109_IDX (Fn+'6' (JIS-109) -> j-i-t-a-k-u) replace HOME_DFT_IDX
    """
    LAYOUT = 'JPA'

    KEYS = DevBoardKeyMatrix.KEYS.copy()
    FN_KEYS = DevBoardKeyMatrix.FN_KEYS.copy()

    del FN_KEYS[KEY_ID.COMPOUND_HOME]                           # Col_1, Row_2
    FN_KEYS[KEY_ID.COMPOUND_HOME_JIS_109] = KEY_ID.KEYBOARD_6   # Col_1, Row_2
# end class DevBoardJis109LayoutKeyMatrix


class DevBoardRawColConfigurableKeyMatrix(DevBoardKeyMatrix):
    """
    Configure the NRF52 DEV board key matrix to leverage all the IOs of the row and column connectors to verify that
    there is no short circuits on the high density connectors.
    """
    # Can be configured from ROW_00 to ROW_20 to cover the row connector up to 23
    BASE_ROW = KbdMatrix.ROW_20 if Daemon.is_host_kosmos() else 0
    # Can be configured from COL_00 to COL_16 to cover the column connector up to 19
    BASE_COL = KbdMatrix.COL_16 if Daemon.is_host_kosmos() else 0

    KEYS = {
        # ROW 0
        KEY_ID.KEYBOARD_7: (BASE_COL, BASE_ROW),
        KEY_ID.KEYBOARD_4: (BASE_COL + 1, BASE_ROW),
        KEY_ID.KEYBOARD_1: (BASE_COL + 2, BASE_ROW),
        # Col_3, Row_0: N/A

        # ROW 1
        KEY_ID.KEYBOARD_8: (BASE_COL, BASE_ROW + 1),
        KEY_ID.KEYBOARD_5: (BASE_COL + 1, BASE_ROW + 1),
        KEY_ID.KEYBOARD_2: (BASE_COL + 2, BASE_ROW + 1),
        KEY_ID.KEYBOARD_0: (BASE_COL + 3, BASE_ROW + 1),

        # ROW 2
        KEY_ID.KEYBOARD_9: (BASE_COL, BASE_ROW + 2),
        KEY_ID.KEYBOARD_6: (BASE_COL + 1, BASE_ROW + 2),
        KEY_ID.KEYBOARD_3: (BASE_COL + 2, BASE_ROW + 2),
        KEY_ID.FN_KEY: (BASE_COL + 3, BASE_ROW + 2),

        # ROW 3
        KEY_ID.KEYPAD_PLUS: (BASE_COL, BASE_ROW + 3),
        KEY_ID.KEYBOARD_BACKSPACE: (BASE_COL + 1, BASE_ROW + 3),
        KEY_ID.KEYBOARD_RETURN_ENTER: (BASE_COL + 2, BASE_ROW + 3),
        KEY_ID.KEYBOARD_POWER: (BASE_COL + 3, BASE_ROW + 3),
    }

    FN_KEYS = DevBoardKeyMatrix.FN_KEYS.copy()
# end class DevBoardRawColConfigurableKeyMatrix


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
