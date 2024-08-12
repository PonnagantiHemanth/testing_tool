#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.base.productdata
    :brief:  Product data shared with registration methods
    :author: Christophe Roquebert
    :date: 2020/11/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import KEYSTROKE
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
# Action type strings
PRE_RESET_ACTIONS = 'pre-reset_actions'
POST_RESET_ACTIONS = 'post-reset_actions'

# List of Keys to be pressed to enable entering the bootloader recovery mode
RECOVERY_KEYS_LIST_MAP = {
    None: {
        PRE_RESET_ACTIONS: [],
        POST_RESET_ACTIONS: [],
    },
    # Unifying Mouse variant
    "right-and-left-buttons-make_reset_right-and-left-buttons-break": {
        PRE_RESET_ACTIONS: [(KEY_ID.LEFT_BUTTON, MAKE), (KEY_ID.RIGHT_BUTTON, MAKE)],
        POST_RESET_ACTIONS: [(KEY_ID.LEFT_BUTTON, BREAK), (KEY_ID.RIGHT_BUTTON, BREAK)],
    },
    # Unifying Keyboard variant
    "kdb-recovery-keys-make_reset_kdb-recovery-keys-break": {
        PRE_RESET_ACTIONS: [(KEY_ID.KEYBOARD_LEFT_ARROW, MAKE), (KEY_ID.KEYBOARD_RIGHT_ARROW, MAKE)],
        POST_RESET_ACTIONS: [(KEY_ID.KEYBOARD_LEFT_ARROW, BREAK), (KEY_ID.KEYBOARD_RIGHT_ARROW, BREAK)],
    },
    # BLE Pro Mouse variant
    "right-button-make_reset_5-times-left-keystroke_right-button-break": {
        PRE_RESET_ACTIONS: [(KEY_ID.RIGHT_BUTTON, MAKE)],
        POST_RESET_ACTIONS: [(KEY_ID.LEFT_BUTTON, KEYSTROKE), (KEY_ID.LEFT_BUTTON, KEYSTROKE),
                             (KEY_ID.LEFT_BUTTON, KEYSTROKE), (KEY_ID.LEFT_BUTTON, KEYSTROKE),
                             (KEY_ID.LEFT_BUTTON, KEYSTROKE), (KEY_ID.RIGHT_BUTTON, BREAK)],
    },
    # BLE Pro Keyboard variant
    "right-arrow-make_reset_5-times-left-arrow_right-arrow-break": {
        PRE_RESET_ACTIONS: [(KEY_ID.KEYBOARD_RIGHT_ARROW, MAKE)],
        POST_RESET_ACTIONS: [(KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE), (KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE),
                             (KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE), (KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE),
                             (KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE), (KEY_ID.KEYBOARD_RIGHT_ARROW, BREAK)],
    },
}

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
