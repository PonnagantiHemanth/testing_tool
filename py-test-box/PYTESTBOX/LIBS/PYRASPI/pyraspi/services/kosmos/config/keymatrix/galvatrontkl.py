#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keymatrix.galvatrontkl
:brief: Galvatron TKL keyboard key layout definition
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/03/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import AnalogKeyMatrix
from pylibrary.emulator.keybaordlayout import COL_ROW_UNDEFINED
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pylibrary.emulator.keyid import KEY_ID


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GalvatronTklKeyMatrix(AnalogKeyMatrix):
    """
    Configure the Galvatron TKL key matrix layout

    Mechanical Key matrix map:
        https://docs.google.com/spreadsheets/d/1ooO1k3y5ymplfaR9VgFDexHGZN-mivJXcF21vP2f5X4/view#gid=1932519598
    Schematic:
        https://drive.google.com/file/d/1fRhLxC3gSsCKc2U9HKUfYQmtZv0dGfw2
    Analog Key map:
        https://docs.google.com/spreadsheets/d/1U3Ee_pG--NqNQnPZv2F81-B8Tf07ubyUvebCBd-INdU
    """
    HAS_KEYPAD = False

    # The mapping {key_id} to {chain_id} is specified in the following spreadsheet
    # https://docs.google.com/spreadsheets/d/1U3Ee_pG--NqNQnPZv2F81-B8Tf07ubyUvebCBd-INdU/edit#gid=1826149686
    KEYID_2_CHAINID = {
        ### US LAYOUT ###
        # Chain 0
        KEY_ID.KEYBOARD_ESCAPE: 0,
        KEY_ID.KEYBOARD_F1: 1,
        KEY_ID.KEYBOARD_F2: 2,
        KEY_ID.KEYBOARD_F3: 3,
        KEY_ID.KEYBOARD_F4: 4,
        KEY_ID.KEYBOARD_F5: 5,
        KEY_ID.KEYBOARD_F6: 6,
        KEY_ID.KEYBOARD_F7: 7,
        KEY_ID.KEYBOARD_F8: 8,
        KEY_ID.KEYBOARD_F9: 9,
        KEY_ID.KEYBOARD_F10: 10,
        KEY_ID.KEYBOARD_F11: 11,
        KEY_ID.KEYBOARD_F12: 12,
        # Chain 1
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: 13,
        KEY_ID.KEYBOARD_1: 14,
        KEY_ID.KEYBOARD_2: 15,
        KEY_ID.KEYBOARD_3: 16,
        KEY_ID.KEYBOARD_4: 17,
        KEY_ID.KEYBOARD_5: 18,
        KEY_ID.KEYBOARD_6: 19,
        KEY_ID.KEYBOARD_7: 20,
        KEY_ID.KEYBOARD_8: 21,
        KEY_ID.KEYBOARD_9: 22,
        KEY_ID.KEYBOARD_0: 23,
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: 24,
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: 25,
        KEY_ID.KEYBOARD_BACKSPACE: 26,
        # Chain 2
        KEY_ID.KEYBOARD_TAB: 27,
        KEY_ID.KEYBOARD_Q: 28,
        KEY_ID.KEYBOARD_W: 29,
        KEY_ID.KEYBOARD_E: 30,
        KEY_ID.KEYBOARD_R: 31,
        KEY_ID.KEYBOARD_F: 32,
        KEY_ID.KEYBOARD_D: 33,
        KEY_ID.KEYBOARD_S: 34,
        KEY_ID.KEYBOARD_A: 35,
        KEY_ID.KEYBOARD_CAPS_LOCK: 36,
        KEY_ID.KEYBOARD_LEFT_SHIFT: 37,
        KEY_ID.KEYBOARD_Z: 38,
        KEY_ID.KEYBOARD_X: 39,
        KEY_ID.KEYBOARD_C: 40,
        # Chain 3
        KEY_ID.KEYBOARD_T: 41,
        KEY_ID.KEYBOARD_Y: 42,
        KEY_ID.KEYBOARD_U: 43,
        KEY_ID.KEYBOARD_I: 44,
        KEY_ID.KEYBOARD_O: 45,
        KEY_ID.KEYBOARD_L: 46,
        KEY_ID.KEYBOARD_K: 47,
        KEY_ID.KEYBOARD_J: 48,
        KEY_ID.KEYBOARD_H: 49,
        KEY_ID.KEYBOARD_G: 50,
        KEY_ID.KEYBOARD_V: 51,
        KEY_ID.KEYBOARD_B: 52,
        KEY_ID.KEYBOARD_N: 53,
        KEY_ID.KEYBOARD_M: 54,
        KEY_ID.KEYBOARD_COMMA_AND_LESS: 55,
        # Chain 4
        KEY_ID.KEYBOARD_P: 56,
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: 57,
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: 58,
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: 59,
        KEY_ID.KEYBOARD_RETURN_ENTER: 60,
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: 61,
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: 62,
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: 63,
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: 64,
        KEY_ID.KEYBOARD_RIGHT_SHIFT: 65,
        # Chain 5
        KEY_ID.KEYBOARD_LEFT_CONTROL: 66,
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: 67,
        KEY_ID.KEYBOARD_LEFT_ALT: 68,
        KEY_ID.KEYBOARD_SPACE_BAR: 69,
        KEY_ID.KEYBOARD_RIGHT_ALT: 70,
        KEY_ID.FN_KEY: 71,
        KEY_ID.CONTEXTUAL_MENU: 72,  # APP
        KEY_ID.KEYBOARD_RIGHT_CONTROL: 73,
        # Chain 6
        KEY_ID.KEYBOARD_PRINT_SCREEN: 74,
        KEY_ID.KEYBOARD_SCROLL_LOCK: 75,
        KEY_ID.KEYBOARD_PAUSE: 76,
        KEY_ID.KEYBOARD_PAGE_UP: 77,
        KEY_ID.KEYBOARD_HOME: 78,
        KEY_ID.KEYBOARD_INSERT: 79,
        KEY_ID.KEYBOARD_DELETE_FORWARD: 80,
        KEY_ID.KEYBOARD_END: 81,
        KEY_ID.KEYBOARD_PAGE_DOWN: 82,
        KEY_ID.KEYBOARD_UP_ARROW: 83,
        KEY_ID.KEYBOARD_RIGHT_ARROW: 84,
        KEY_ID.KEYBOARD_DOWN_ARROW: 85,
        KEY_ID.KEYBOARD_LEFT_ARROW: 86
    }

    KEYS = {
        # ==============================================================================================================
        # Rows 0 to 5 keys are analog keys, controlled via Gtech chip. They do not have logical ROW, COL coordinates.
        # They are instead defined above in the `KEYID_2_CHAINID` mapping.
        # ==============================================================================================================

        # ROW_0
        KEY_ID.KEYBOARD_ESCAPE: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F2: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F4: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F6: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F8: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F10: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F12: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_SCROLL_LOCK: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_2: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_4: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_6: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_8: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_0: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_EQUAL_AND_PLUS: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_BACKSPACE: COL_ROW_UNDEFINED,

        # ROW_1
        KEY_ID.KEYBOARD_F1: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F3: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F5: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F7: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F9: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F11: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_PRINT_SCREEN: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_PAUSE: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_1: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_3: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_5: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_7: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_9: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_INSERT: COL_ROW_UNDEFINED,

        # ROW_2
        KEY_ID.KEYBOARD_TAB: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_W: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_R: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_Y: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_I: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_P: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_HOME: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_CAPS_LOCK: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_S: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_F: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_H: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_K: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_DELETE_FORWARD: COL_ROW_UNDEFINED,

        # ROW_3
        KEY_ID.KEYBOARD_Q: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_E: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_T: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_U: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_O: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_PAGE_UP: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_A: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_D: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_G: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_J: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_L: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_RETURN_ENTER: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_END: COL_ROW_UNDEFINED,

        # ROW_4
        # COL_0, ROW_4: N/A,
        KEY_ID.KEYBOARD_LEFT_SHIFT: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_Z: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_C: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_B: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_M: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_PERIOD_AND_MORE: COL_ROW_UNDEFINED,
        # COL_7, ROW_4: N/A,
        KEY_ID.KEYBOARD_LEFT_CONTROL: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_LEFT_ALT: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_SPACE_BAR: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_RIGHT_ALT: COL_ROW_UNDEFINED,
        KEY_ID.CONTEXTUAL_MENU: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_LEFT_ARROW: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_DOWN_ARROW: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_PAGE_DOWN: COL_ROW_UNDEFINED,

        # ROW_5
        # COL_0, ROW_5: N/A,
        # COL_1, ROW_5: N/A,
        KEY_ID.KEYBOARD_X: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_V: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_N: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_COMMA_AND_LESS: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_RIGHT_SHIFT: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: COL_ROW_UNDEFINED,
        # COL_9, ROW_5: N/A,
        # COL_10, ROW_5: N/A,
        KEY_ID.FN_KEY: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_RIGHT_CONTROL: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_UP_ARROW: COL_ROW_UNDEFINED,
        KEY_ID.KEYBOARD_RIGHT_ARROW: COL_ROW_UNDEFINED,
        # COL_15, ROW_5: N/A,

        # ==============================================================================================================
        # Rows 6 to 7 keys are true mechanical (galvanic) keys, and they have a ROW, COL coordinates.
        # They are not part of the Gtech key set.
        # ==============================================================================================================

        # ROW_6
        # COL_0, ROW_6: N/A,
        # COL_1, ROW_6: N/A,
        # KEY_ID.BLE_CONNECTION: (KbdMatrix.COL_2, KbdMatrix.ROW_6),  # "CONNECTIVITY" on sch, not populated on pcb
        KEY_ID.DIMMING_KEY: (KbdMatrix.COL_3, KbdMatrix.ROW_6),
        KEY_ID.PLAY_PAUSE: (KbdMatrix.COL_4, KbdMatrix.ROW_6),
        KEY_ID.KEYBOARD_MUTE: (KbdMatrix.COL_5, KbdMatrix.ROW_6),

        # ROW_7
        # COL_0, ROW_7: N/A,
        # KEY_ID.LS2_CONNECTION: (KbdMatrix.COL_1, KbdMatrix.ROW_7),  # "LightSpeed" on sch, not populated on pcb
        KEY_ID.GAME_MODE_KEY: (KbdMatrix.COL_2, KbdMatrix.ROW_7),
        KEY_ID.PREV_TRACK: (KbdMatrix.COL_3, KbdMatrix.ROW_7),
        KEY_ID.NEXT_TRACK: (KbdMatrix.COL_4, KbdMatrix.ROW_7),
        # COL_5, ROW_7: N/A,
    }

    FN_KEYS = {
        # Function Keys W/ Fn
        KEY_ID.FKC_TOGGLE: KEY_ID.KEYBOARD_F1,
        KEY_ID.ONBOARD_PROFILE_1: KEY_ID.KEYBOARD_F2,
        KEY_ID.ONBOARD_PROFILE_2: KEY_ID.KEYBOARD_F3,
        KEY_ID.ONBOARD_PROFILE_3: KEY_ID.KEYBOARD_F4,
        KEY_ID.ONBOARD_BASE_PROFILE: KEY_ID.KEYBOARD_F5,
        KEY_ID.ONBOARD_ACTUATION_MODE: KEY_ID.KEYBOARD_F6,
        KEY_ID.ONBOARD_RAPID_TRIGGER_MODE: KEY_ID.KEYBOARD_F7,
    }
# end class GalvatronTklKeyMatrix


class GalvatronTklUkLayoutKeyMatrix(AnalogKeyMatrix):
    """
    Configure the UK key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1vx_6j4wdvWs6qwntL_7K_t9DCiu9V1FfnueYCWcPcL4/view#gid=401535802
    """
    LAYOUT = 'UK'
    HAS_KEYPAD = True

    KEYID_2_CHAINID = GalvatronTklKeyMatrix.KEYID_2_CHAINID.copy()
    KEYS = GalvatronTklKeyMatrix.KEYS.copy()
    FN_KEYS = GalvatronTklKeyMatrix.FN_KEYS.copy()

    KEYID_2_CHAINID[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = 61
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE] = 38

    last_chain_id = -1
    for key_id in KEYID_2_CHAINID:
        if last_chain_id == KEYID_2_CHAINID[key_id]:
            KEYID_2_CHAINID[key_id] += 1
        # end if
        last_chain_id = KEYID_2_CHAINID[key_id]
    # end for

    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = COL_ROW_UNDEFINED              # K-42
    KEYS[KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE] = COL_ROW_UNDEFINED     # K-45
# end class GalvatronTklUkLayoutKeyMatrix


class GalvatronTklRusLayoutKeyMatrix(AnalogKeyMatrix):
    """
    Configure the RUS key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1vx_6j4wdvWs6qwntL_7K_t9DCiu9V1FfnueYCWcPcL4/view#gid=401535802
    """
    LAYOUT = 'RUS'
    HAS_KEYPAD = True

    KEYID_2_CHAINID = GalvatronTklKeyMatrix.KEYID_2_CHAINID.copy()
    KEYS = GalvatronTklKeyMatrix.KEYS.copy()
    FN_KEYS = GalvatronTklKeyMatrix.FN_KEYS.copy()

    KEYID_2_CHAINID[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = 60

    last_chain_id = -1
    for key_id in KEYID_2_CHAINID:
        if last_chain_id == KEYID_2_CHAINID[key_id]:
            KEYID_2_CHAINID[key_id] += 1
        # end if
        last_chain_id = KEYID_2_CHAINID[key_id]
    # end for

    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = COL_ROW_UNDEFINED              # K-42
# end class GalvatronTklRusLayoutKeyMatrix


class GalvatronTklJpnLayoutKeyMatrix(AnalogKeyMatrix):
    """
    Configure the Jpn key matrix layout

    Key matrix map
    https://drive.google.com/file/d/1HnyjQKE19jJZSu7pyX6q9GglPWNh9b8c/view
    """
    LAYOUT = 'JPN'
    HAS_KEYPAD = True

    KEYID_2_CHAINID = GalvatronTklKeyMatrix.KEYID_2_CHAINID.copy()
    KEYS = GalvatronTklKeyMatrix.KEYS.copy()
    FN_KEYS = GalvatronTklKeyMatrix.FN_KEYS.copy()

    del KEYID_2_CHAINID[KEY_ID.FN_KEY]
    del KEYS[KEY_ID.FN_KEY]

    KEYID_2_CHAINID[KEY_ID.KEYBOARD_SCROLL_LOCK] = 79
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = 61
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_INTERNATIONAL1] = 66
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_INTERNATIONAL2] = 74
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_INTERNATIONAL3] = 26
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_INTERNATIONAL4] = 73
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_INTERNATIONAL5] = 71

    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = COL_ROW_UNDEFINED  # K-42
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL1] = COL_ROW_UNDEFINED  # K-56
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL2] = COL_ROW_UNDEFINED  # K-133
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL3] = COL_ROW_UNDEFINED  # K-14
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL4] = COL_ROW_UNDEFINED  # K-132
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL5] = COL_ROW_UNDEFINED  # K-131
# end class GalvatronTklJpnLayoutKeyMatrix


class GalvatronTklBraLayoutKeyMatrix(AnalogKeyMatrix):
    """
    Configure the BRA key matrix layout

    Key matrix map
    https://docs.google.com/spreadsheets/d/1vx_6j4wdvWs6qwntL_7K_t9DCiu9V1FfnueYCWcPcL4/view#gid=401535802
    """
    LAYOUT = 'BRA'
    HAS_KEYPAD = True

    KEYID_2_CHAINID = GalvatronTklKeyMatrix.KEYID_2_CHAINID.copy()
    KEYS = GalvatronTklKeyMatrix.KEYS.copy()
    FN_KEYS = GalvatronTklKeyMatrix.FN_KEYS.copy()

    KEYID_2_CHAINID[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = 61
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE] = 38
    KEYID_2_CHAINID[KEY_ID.KEYBOARD_INTERNATIONAL1] = 66

    last_chain_id = -1
    for key_id in KEYID_2_CHAINID:
        if last_chain_id == KEYID_2_CHAINID[key_id]:
            KEYID_2_CHAINID[key_id] += 1
        # end if
        last_chain_id = KEYID_2_CHAINID[key_id]
    # end for

    KEYS[KEY_ID.KEYBOARD_NON_US_AND_TILDE] = COL_ROW_UNDEFINED              # K-42
    KEYS[KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE] = COL_ROW_UNDEFINED     # K-45
    KEYS[KEY_ID.KEYBOARD_INTERNATIONAL1] = COL_ROW_UNDEFINED                # K-56
# end class GalvatronTklBraLayoutKeyMatrix
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
