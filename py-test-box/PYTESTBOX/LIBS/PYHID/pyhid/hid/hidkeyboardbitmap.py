#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.hidkeyboardbitmap
:brief: HID keyboard bitmap response interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2020/09/15
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckInt
from pylibrary.tools.util import reverse_bits


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class HidKeyboardBitmap(TimestampedBitFieldContainerMixin):
    """
    Define the 128 keys bitmap format of an HID Keyboard report.
    cf. https://docs.google.com/spreadsheets/d/1UGi-p9rlDcR8eL5fWQifpmqrUDNkTvX3c4yoICO7W9k/edit?usp=sharing
    8 keyboard control keys + 112 keys + 8 KR and JP keys

    Format:

    ================  =========
    Name              Bit count
    ================  =========
    Key Bitmap        128
    ================  =========
    """
    MSG_TYPE = 1  # RESPONSE
    BITFIELD_LENGTH = 16  # Byte

    class FID:
        """
        Field Identifiers
        """
        KEYBOARD_RIGHT_GUI = 0xFF
        KEYBOARD_RIGHT_ALT = 0xFE
        KEYBOARD_RIGHT_SHIFT = 0xFD
        KEYBOARD_RIGHT_CONTROL = 0xFC
        KEYBOARD_LEFT_GUI = 0xFB
        KEYBOARD_LEFT_ALT = 0xFA
        KEYBOARD_LEFT_SHIFT = 0xF9
        KEYBOARD_LEFT_CONTROL = 0xF8
        KEYBOARD_H = 0xF7
        KEYBOARD_G = 0xF6
        KEYBOARD_F = 0xF5
        KEYBOARD_E = 0xF4
        KEYBOARD_D = 0xF3
        KEYBOARD_C = 0xF2
        KEYBOARD_B = 0xF1
        KEYBOARD_A = 0xF0
        KEYBOARD_P = 0xEF
        KEYBOARD_O = 0xEE
        KEYBOARD_N = 0xED
        KEYBOARD_M = 0xEC
        KEYBOARD_L = 0xEB
        KEYBOARD_K = 0xEA
        KEYBOARD_J = 0xE9
        KEYBOARD_I = 0xE8
        KEYBOARD_X = 0xE7
        KEYBOARD_W = 0xE6
        KEYBOARD_V = 0xE5
        KEYBOARD_U = 0xE4
        KEYBOARD_T = 0xE3
        KEYBOARD_S = 0xE2
        KEYBOARD_R = 0xE1
        KEYBOARD_Q = 0xE0
        KEYBOARD_6 = 0xDF
        KEYBOARD_5 = 0xDE
        KEYBOARD_4 = 0xDD
        KEYBOARD_3 = 0xDC
        KEYBOARD_2 = 0xDB
        KEYBOARD_1 = 0xDA
        KEYBOARD_Z = 0xD9
        KEYBOARD_Y = 0xD8
        KEYBOARD_TAB = 0xD7
        KEYBOARD_DELETE_BACKSPACE = 0xD6
        KEYBOARD_ESCAPE = 0xD5
        KEYBOARD_RETURN_ENTER = 0xD4
        KEYBOARD_0 = 0xD3
        KEYBOARD_9 = 0xD2
        KEYBOARD_8 = 0xD1
        KEYBOARD_7 = 0xD0
        KEYBOARD_SEMICOLON_AND_COLON = 0xCF
        KEYBOARD_NON_US_AND_TILDE = 0xCE
        KEYBOARD_BACKSLASH_AND_PIPE = 0xCD
        KEYBOARD_RIGHT_BRACKET_AND_BRACE = 0xCC
        KEYBOARD_LEFT_BRACKET_AND_BRACE = 0xCB
        KEYBOARD_EQUAL_AND_PLUS = 0xCA
        KEYBOARD_DASH_AND_UNDERSCORE = 0xC9
        KEYBOARD_SPACE_BAR = 0xC8
        KEYBOARD_F2 = 0xC7
        KEYBOARD_F1 = 0xC6
        KEYBOARD_CAPS_LOCK = 0xC5
        KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK = 0xC4
        KEYBOARD_PERIOD_AND_MORE = 0xC3
        KEYBOARD_COMMA_AND_LESS = 0xC2
        KEYBOARD_GRAVE_ACCENT_AND_TILDE = 0xC1
        KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK = 0xC0
        KEYBOARD_F10 = 0xBF
        KEYBOARD_F9 = 0xBE
        KEYBOARD_F8 = 0xBD
        KEYBOARD_F7 = 0xBC
        KEYBOARD_F6 = 0xBB
        KEYBOARD_F5 = 0xBA
        KEYBOARD_F4 = 0xB9
        KEYBOARD_F3 = 0xB8
        KEYBOARD_PAGE_UP = 0xB7
        KEYBOARD_HOME = 0xB6
        KEYBOARD_INSERT = 0xB5
        KEYBOARD_PAUSE = 0xB4
        KEYBOARD_SCROLL_LOCK = 0xB3
        KEYBOARD_PRINT_SCREEN = 0xB2
        KEYBOARD_F12 = 0xB1
        KEYBOARD_F11 = 0xB0
        KEYBOARD_LOCKING_NUM_LOCK = 0xAF
        KEYBOARD_UP_ARROW = 0xAE
        KEYBOARD_DOWN_ARROW = 0xAD
        KEYBOARD_LEFT_ARROW = 0xAC
        KEYBOARD_RIGHT_ARROW = 0xAB
        KEYBOARD_PAGE_DOWN = 0xAA
        KEYBOARD_END = 0xA9
        KEYBOARD_DELETE_FORWARD = 0xA8
        KEYPAD_3_AND_PAGE_DN = 0xA7
        KEYPAD_2_AND_DOWN_ARROW = 0xA6
        KEYPAD_1_AND_END = 0xA5
        KEYPAD_ENTER = 0xA4
        KEYPAD_PLUS = 0xA3
        KEYPAD_MINUS = 0xA2
        KEYPAD_ASTERISK = 0xA1
        KEYPAD_FORWARD_SLASH = 0xA0
        KEYPAD_COMMA_AND_DELETE = 0x9F
        KEYPAD_0_AND_INSERT = 0x9E
        KEYPAD_9_AND_PAGE_UP = 0x9D
        KEYPAD_8_AND_UP_ARROW = 0x9C
        KEYPAD_7_AND_HOME = 0x9B
        KEYPAD_6_AND_RIGHT_ARROW = 0x9A
        KEYPAD_5 = 0x99
        KEYPAD_4_AND_LEFT_ARROW = 0x98
        KEYBOARD_F16 = 0x97
        KEYBOARD_F15 = 0x96
        KEYBOARD_F14 = 0x95
        KEYBOARD_F13 = 0x94
        KEYPAD_EQUAL = 0x93
        KEYBOARD_POWER = 0x92
        KEYBOARD_MENU = 0x91
        KEYBOARD_NON_US_BACKSLASH_AND_PIPE = 0x90
        KEYBOARD_F24 = 0x8F
        KEYBOARD_F23 = 0x8E
        KEYBOARD_F22 = 0x8D
        KEYBOARD_F21 = 0x8C
        KEYBOARD_F20 = 0x8B
        KEYBOARD_F19 = 0x8A
        KEYBOARD_F18 = 0x89
        KEYBOARD_F17 = 0x88
        KEYBOARD_LANG3 = 0x87
        KEYBOARD_LANG2 = 0x86
        KEYBOARD_LANG1 = 0x85
        KEYBOARD_INTERNATIONAL5 = 0x84
        KEYBOARD_INTERNATIONAL4 = 0x83
        KEYBOARD_INTERNATIONAL3 = 0x82
        KEYBOARD_INTERNATIONAL2 = 0x81
        KEYBOARD_INTERNATIONAL1 = 0x80
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        KEYBOARD_RIGHT_GUI = 0x01
        KEYBOARD_RIGHT_ALT = 0x01
        KEYBOARD_RIGHT_SHIFT = 0x01
        KEYBOARD_RIGHT_CONTROL = 0x01
        KEYBOARD_LEFT_GUI = 0x01
        KEYBOARD_LEFT_ALT = 0x01
        KEYBOARD_LEFT_SHIFT = 0x01
        KEYBOARD_LEFT_CONTROL = 0x01
        KEYBOARD_H = 0x01
        KEYBOARD_G = 0x01
        KEYBOARD_F = 0x01
        KEYBOARD_E = 0x01
        KEYBOARD_D = 0x01
        KEYBOARD_C = 0x01
        KEYBOARD_B = 0x01
        KEYBOARD_A = 0x01
        KEYBOARD_P = 0x01
        KEYBOARD_O = 0x01
        KEYBOARD_N = 0x01
        KEYBOARD_M = 0x01
        KEYBOARD_L = 0x01
        KEYBOARD_K = 0x01
        KEYBOARD_J = 0x01
        KEYBOARD_I = 0x01
        KEYBOARD_X = 0x01
        KEYBOARD_W = 0x01
        KEYBOARD_V = 0x01
        KEYBOARD_U = 0x01
        KEYBOARD_T = 0x01
        KEYBOARD_S = 0x01
        KEYBOARD_R = 0x01
        KEYBOARD_Q = 0x01
        KEYBOARD_6 = 0x01
        KEYBOARD_5 = 0x01
        KEYBOARD_4 = 0x01
        KEYBOARD_3 = 0x01
        KEYBOARD_2 = 0x01
        KEYBOARD_1 = 0x01
        KEYBOARD_Z = 0x01
        KEYBOARD_Y = 0x01
        KEYBOARD_TAB = 0x01
        KEYBOARD_DELETE_BACKSPACE = 0x01
        KEYBOARD_ESCAPE = 0x01
        KEYBOARD_RETURN_ENTER = 0x01
        KEYBOARD_0 = 0x01
        KEYBOARD_9 = 0x01
        KEYBOARD_8 = 0x01
        KEYBOARD_7 = 0x01
        KEYBOARD_SEMICOLON_AND_COLON = 0x01
        KEYBOARD_NON_US_AND_TILDE = 0x01
        KEYBOARD_BACKSLASH_AND_PIPE = 0x01
        KEYBOARD_RIGHT_BRACKET_AND_BRACE = 0x01
        KEYBOARD_LEFT_BRACKET_AND_BRACE = 0x01
        KEYBOARD_EQUAL_AND_PLUS = 0x01
        KEYBOARD_DASH_AND_UNDERSCORE = 0x01
        KEYBOARD_SPACE_BAR = 0x01
        KEYBOARD_F2 = 0x01
        KEYBOARD_F1 = 0x01
        KEYBOARD_CAPS_LOCK = 0x01
        KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK = 0x01
        KEYBOARD_PERIOD_AND_MORE = 0x01
        KEYBOARD_COMMA_AND_LESS = 0x01
        KEYBOARD_GRAVE_ACCENT_AND_TILDE = 0x01
        KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK = 0x01
        KEYBOARD_F10 = 0x01
        KEYBOARD_F9 = 0x01
        KEYBOARD_F8 = 0x01
        KEYBOARD_F7 = 0x01
        KEYBOARD_F6 = 0x01
        KEYBOARD_F5 = 0x01
        KEYBOARD_F4 = 0x01
        KEYBOARD_F3 = 0x01
        KEYBOARD_PAGE_UP = 0x01
        KEYBOARD_HOME = 0x01
        KEYBOARD_INSERT = 0x01
        KEYBOARD_PAUSE = 0x01
        KEYBOARD_SCROLL_LOCK = 0x01
        KEYBOARD_PRINT_SCREEN = 0x01
        KEYBOARD_F12 = 0x01
        KEYBOARD_F11 = 0x01
        KEYBOARD_LOCKING_NUM_LOCK = 0x01
        KEYBOARD_UP_ARROW = 0x01
        KEYBOARD_DOWN_ARROW = 0x01
        KEYBOARD_LEFT_ARROW = 0x01
        KEYBOARD_RIGHT_ARROW = 0x01
        KEYBOARD_PAGE_DOWN = 0x01
        KEYBOARD_END = 0x01
        KEYBOARD_DELETE_FORWARD = 0x01
        KEYPAD_3_AND_PAGE_DN = 0x01
        KEYPAD_2_AND_DOWN_ARROW = 0x01
        KEYPAD_1_AND_END = 0x01
        KEYPAD_ENTER = 0x01
        KEYPAD_PLUS = 0x01
        KEYPAD_MINUS = 0x01
        KEYPAD_ASTERISK = 0x01
        KEYPAD_FORWARD_SLASH = 0x01
        KEYPAD_COMMA_AND_DELETE = 0x01
        KEYPAD_0_AND_INSERT = 0x01
        KEYPAD_9_AND_PAGE_UP = 0x01
        KEYPAD_8_AND_UP_ARROW = 0x01
        KEYPAD_7_AND_HOME = 0x01
        KEYPAD_6_AND_RIGHT_ARROW = 0x01
        KEYPAD_5 = 0x01
        KEYPAD_4_AND_LEFT_ARROW = 0x01
        KEYBOARD_F16 = 0x01
        KEYBOARD_F15 = 0x01
        KEYBOARD_F14 = 0x01
        KEYBOARD_F13 = 0x01
        KEYPAD_EQUAL = 0x01
        KEYBOARD_POWER = 0x01
        KEYBOARD_MENU = 0x01
        KEYBOARD_NON_US_BACKSLASH_AND_PIPE = 0x01
        KEYBOARD_F24 = 0x01
        KEYBOARD_F23 = 0x01
        KEYBOARD_F22 = 0x01
        KEYBOARD_F21 = 0x01
        KEYBOARD_F20 = 0x01
        KEYBOARD_F19 = 0x01
        KEYBOARD_F18 = 0x01
        KEYBOARD_F17 = 0x01
        KEYBOARD_LANG3 = 0x01
        KEYBOARD_LANG2 = 0x01
        KEYBOARD_LANG1 = 0x01
        KEYBOARD_INTERNATIONAL5 = 0x01
        KEYBOARD_INTERNATIONAL4 = 0x01
        KEYBOARD_INTERNATIONAL3 = 0x01
        KEYBOARD_INTERNATIONAL2 = 0x01
        KEYBOARD_INTERNATIONAL1 = 0x01
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        RELEASED = 0
    # end class DEFAULT

    FIELDS = (BitField(fid=FID.KEYBOARD_LEFT_CONTROL,
                       length=LEN.KEYBOARD_LEFT_CONTROL,
                       title='KeyboardLeftControl',
                       name='keyboard_left_control',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_CONTROL) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_SHIFT,
                       length=LEN.KEYBOARD_LEFT_SHIFT,
                       title='KeyboardLeftShift',
                       name='keyboard_left_shift',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_SHIFT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_ALT,
                       length=LEN.KEYBOARD_LEFT_ALT,
                       title='KeyboardLeftALT',
                       name='keyboard_left_alt',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_ALT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_GUI,
                       length=LEN.KEYBOARD_LEFT_GUI,
                       title='KeyboardLeftGUI',
                       name='keyboard_left_gui',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_GUI) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_CONTROL,
                       length=LEN.KEYBOARD_RIGHT_CONTROL,
                       title='KeyboardRightControl',
                       name='keyboard_right_control',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_CONTROL) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_SHIFT,
                       length=LEN.KEYBOARD_RIGHT_SHIFT,
                       title='KeyboardRightShift',
                       name='keyboard_right_shift',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_SHIFT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_ALT,
                       length=LEN.KEYBOARD_RIGHT_ALT,
                       title='KeyboardRightALT',
                       name='keyboard_right_alt',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_ALT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_GUI,
                       length=LEN.KEYBOARD_RIGHT_GUI,
                       title='KeyboardRightGUI',
                       name='keyboard_right_gui',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_GUI) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_A,
                       length=LEN.KEYBOARD_A,
                       title='KeyboardA',
                       name='keyboard_a',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_A) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_B,
                       length=LEN.KEYBOARD_B,
                       title='KeyboardB',
                       name='keyboard_b',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_B) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_C,
                       length=LEN.KEYBOARD_C,
                       title='KeyboardC',
                       name='keyboard_c',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_C) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_D,
                       length=LEN.KEYBOARD_D,
                       title='KeyboardD',
                       name='keyboard_d',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_D) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_E,
                       length=LEN.KEYBOARD_E,
                       title='KeyboardE',
                       name='keyboard_e',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_E) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F,
                       length=LEN.KEYBOARD_F,
                       title='KeyboardF',
                       name='keyboard_f',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_G,
                       length=LEN.KEYBOARD_G,
                       title='KeyboardG',
                       name='keyboard_g',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_G) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_H,
                       length=LEN.KEYBOARD_H,
                       title='KeyboardH',
                       name='keyboard_h',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_H) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_I,
                       length=LEN.KEYBOARD_I,
                       title='KeyboardI',
                       name='keyboard_i',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_I) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_J,
                       length=LEN.KEYBOARD_J,
                       title='KeyboardJ',
                       name='keyboard_j',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_J) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_K,
                       length=LEN.KEYBOARD_K,
                       title='KeyboardK',
                       name='keyboard_k',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_K) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_L,
                       length=LEN.KEYBOARD_L,
                       title='KeyboardL',
                       name='keyboard_l',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_L) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_M,
                       length=LEN.KEYBOARD_M,
                       title='KeyboardM',
                       name='keyboard_m',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_M) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_N,
                       length=LEN.KEYBOARD_N,
                       title='KeyboardN',
                       name='keyboard_n',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_N) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_O,
                       length=LEN.KEYBOARD_O,
                       title='KeyboardO',
                       name='keyboard_o',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_O) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_P,
                       length=LEN.KEYBOARD_P,
                       title='KeyboardP',
                       name='keyboard_p',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_P) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_Q,
                       length=LEN.KEYBOARD_Q,
                       title='KeyboardQ',
                       name='keyboard_q',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_Q) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_R,
                       length=LEN.KEYBOARD_R,
                       title='KeyboardR',
                       name='keyboard_r',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_R) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_S,
                       length=LEN.KEYBOARD_S,
                       title='KeyboardS',
                       name='keyboard_s',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_S) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_T,
                       length=LEN.KEYBOARD_T,
                       title='KeyboardT',
                       name='keyboard_t',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_T) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_U,
                       length=LEN.KEYBOARD_U,
                       title='KeyboardU',
                       name='keyboard_u',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_U) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_V,
                       length=LEN.KEYBOARD_V,
                       title='KeyboardV',
                       name='keyboard_v',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_V) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_W,
                       length=LEN.KEYBOARD_W,
                       title='KeyboardW',
                       name='keyboard_w',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_W) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_X,
                       length=LEN.KEYBOARD_X,
                       title='KeyboardX',
                       name='keyboard_x',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_X) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_Y,
                       length=LEN.KEYBOARD_Y,
                       title='KeyboardY',
                       name='keyboard_y',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_Y) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_Z,
                       length=LEN.KEYBOARD_Z,
                       title='KeyboardZ',
                       name='keyboard_z',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_Z) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_1,
                       length=LEN.KEYBOARD_1,
                       title='Keyboard1',
                       name='keyboard_1',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_1) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_2,
                       length=LEN.KEYBOARD_2,
                       title='Keyboard2',
                       name='keyboard_2',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_2) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_3,
                       length=LEN.KEYBOARD_3,
                       title='Keyboard3',
                       name='keyboard_3',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_3) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_4,
                       length=LEN.KEYBOARD_4,
                       title='Keyboard4',
                       name='keyboard_4',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_4) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_5,
                       length=LEN.KEYBOARD_5,
                       title='Keyboard5',
                       name='keyboard_5',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_5) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_6,
                       length=LEN.KEYBOARD_6,
                       title='Keyboard6',
                       name='keyboard_6',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_6) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_7,
                       length=LEN.KEYBOARD_7,
                       title='Keyboard7',
                       name='keyboard_7',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_7) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_8,
                       length=LEN.KEYBOARD_8,
                       title='Keyboard8',
                       name='keyboard_8',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_8) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_9,
                       length=LEN.KEYBOARD_9,
                       title='Keyboard9',
                       name='keyboard_9',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_9) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_0,
                       length=LEN.KEYBOARD_0,
                       title='Keyboard0',
                       name='keyboard_0',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_0) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RETURN_ENTER,
                       length=LEN.KEYBOARD_RETURN_ENTER,
                       title='KeyboardReturnEnter',
                       name='keyboard_return_enter',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RETURN_ENTER) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_ESCAPE,
                       length=LEN.KEYBOARD_ESCAPE,
                       title='KeyboardEscape',
                       name='keyboard_escape',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_ESCAPE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_DELETE_BACKSPACE,
                       length=LEN.KEYBOARD_DELETE_BACKSPACE,
                       title='KeyboardDeleteBackspace',
                       name='keyboard_delete_backspace',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_DELETE_BACKSPACE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_TAB,
                       length=LEN.KEYBOARD_TAB,
                       title='KeyboardTab',
                       name='keyboard_tab',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_TAB) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_SPACE_BAR,
                       length=LEN.KEYBOARD_SPACE_BAR,
                       title='KeyboardSpaceBar',
                       name='keyboard_space_bar',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_SPACE_BAR) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_DASH_AND_UNDERSCORE,
                       length=LEN.KEYBOARD_DASH_AND_UNDERSCORE,
                       title='KeyboardDashAndUnderscore',
                       name='keyboard_dash_and_underscore',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_DASH_AND_UNDERSCORE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_EQUAL_AND_PLUS,
                       length=LEN.KEYBOARD_EQUAL_AND_PLUS,
                       title='KeyboardEqualAndPlus',
                       name='keyboard_equal_and_plus',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_EQUAL_AND_PLUS) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_BRACKET_AND_BRACE,
                       length=LEN.KEYBOARD_LEFT_BRACKET_AND_BRACE,
                       title='KeyboardLeftBracketAndBrace',
                       name='keyboard_left_bracket_and_brace',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_BRACKET_AND_BRACE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_BRACKET_AND_BRACE,
                       length=LEN.KEYBOARD_RIGHT_BRACKET_AND_BRACE,
                       title='KeyboardRightBracketAndBrace',
                       name='keyboard_right_bracket_and_brace',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_BRACKET_AND_BRACE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_BACKSLASH_AND_PIPE,
                       length=LEN.KEYBOARD_BACKSLASH_AND_PIPE,
                       title='KeyboardBackslashAndPipe',
                       name='keyboard_backslash_and_pipe',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_BACKSLASH_AND_PIPE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_NON_US_AND_TILDE,
                       length=LEN.KEYBOARD_NON_US_AND_TILDE,
                       title='KeyboardNonUSAndTilde',
                       name='keyboard_non_us_and_tilde',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_NON_US_AND_TILDE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_SEMICOLON_AND_COLON,
                       length=LEN.KEYBOARD_SEMICOLON_AND_COLON,
                       title='KeyboardSemicolonAndColon',
                       name='keyboard_semicolon_and_colon',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_SEMICOLON_AND_COLON) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK,
                       length=LEN.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK,
                       title='KeyboardApostropheAndQuotationMark',
                       name='keyboard_apostrophe_and_quotation_mark',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_GRAVE_ACCENT_AND_TILDE,
                       length=LEN.KEYBOARD_GRAVE_ACCENT_AND_TILDE,
                       title='KeyboardGraveAccentAndTilde',
                       name='keyboard_grave_accent_and_tilde',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_GRAVE_ACCENT_AND_TILDE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_COMMA_AND_LESS,
                       length=LEN.KEYBOARD_COMMA_AND_LESS,
                       title='KeyboardCommaAndLess',
                       name='keyboard_comma_and_less',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_COMMA_AND_LESS) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_PERIOD_AND_MORE,
                       length=LEN.KEYBOARD_PERIOD_AND_MORE,
                       title='KeyboardPeriodAndMore',
                       name='keyboard_period_and_more',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_PERIOD_AND_MORE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK,
                       length=LEN.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK,
                       title='KeyboardForwardSlashAndQuestionMark',
                       name='keyboard_forward_slash_and_question_mark',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_CAPS_LOCK,
                       length=LEN.KEYBOARD_CAPS_LOCK,
                       title='KeyboardCapsLock',
                       name='keyboard_caps_lock',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_CAPS_LOCK) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F1,
                       length=LEN.KEYBOARD_F1,
                       title='KeyboardF1',
                       name='keyboard_f1',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F1) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F2,
                       length=LEN.KEYBOARD_F2,
                       title='KeyboardF2',
                       name='keyboard_f2',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F2) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F3,
                       length=LEN.KEYBOARD_F3,
                       title='KeyboardF3',
                       name='keyboard_f3',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F3) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F4,
                       length=LEN.KEYBOARD_F4,
                       title='KeyboardF4',
                       name='keyboard_f4',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F4) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F5,
                       length=LEN.KEYBOARD_F5,
                       title='KeyboardF5',
                       name='keyboard_f5',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F5) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F6,
                       length=LEN.KEYBOARD_F6,
                       title='KeyboardF6',
                       name='keyboard_f6',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F6) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F7,
                       length=LEN.KEYBOARD_F7,
                       title='KeyboardF7',
                       name='keyboard_f7',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F7) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F8,
                       length=LEN.KEYBOARD_F8,
                       title='KeyboardF8',
                       name='keyboard_f8',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F8) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F9,
                       length=LEN.KEYBOARD_F9,
                       title='KeyboardF9',
                       name='keyboard_f9',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F9) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F10,
                       length=LEN.KEYBOARD_F10,
                       title='KeyboardF10',
                       name='keyboard_f10',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F10) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F11,
                       length=LEN.KEYBOARD_F11,
                       title='KeyboardF11',
                       name='keyboard_f11',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F11) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F12,
                       length=LEN.KEYBOARD_F12,
                       title='KeyboardF12',
                       name='keyboard_f12',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F12) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_PRINT_SCREEN,
                       length=LEN.KEYBOARD_PRINT_SCREEN,
                       title='KeyboardPrintScreen',
                       name='keyboard_print_screen',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_PRINT_SCREEN) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_SCROLL_LOCK,
                       length=LEN.KEYBOARD_SCROLL_LOCK,
                       title='KeyboardScrollLock',
                       name='keyboard_scroll_lock',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_SCROLL_LOCK) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_PAUSE,
                       length=LEN.KEYBOARD_PAUSE,
                       title='KeyboardPause',
                       name='keyboard_pause',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_PAUSE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_INSERT,
                       length=LEN.KEYBOARD_INSERT,
                       title='KeyboardInsert',
                       name='keyboard_insert',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_INSERT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_HOME,
                       length=LEN.KEYBOARD_HOME,
                       title='KeyboardHome',
                       name='keyboard_home',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_HOME) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_PAGE_UP,
                       length=LEN.KEYBOARD_PAGE_UP,
                       title='KeyboardPageUp',
                       name='keyboard_page_up',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_PAGE_UP) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_DELETE_FORWARD,
                       length=LEN.KEYBOARD_DELETE_FORWARD,
                       title='KeyboardDeleteForward',
                       name='keyboard_delete_forward',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_DELETE_FORWARD) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_END,
                       length=LEN.KEYBOARD_END,
                       title='KeyboardEnd',
                       name='keyboard_end',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_END) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_PAGE_DOWN,
                       length=LEN.KEYBOARD_PAGE_DOWN,
                       title='KeyboardPageDown',
                       name='keyboard_page_down',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_PAGE_DOWN) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_ARROW,
                       length=LEN.KEYBOARD_RIGHT_ARROW,
                       title='KeyboardRightArrow',
                       name='keyboard_right_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_ARROW,
                       length=LEN.KEYBOARD_LEFT_ARROW,
                       title='KeyboardLeftArrow',
                       name='keyboard_left_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_DOWN_ARROW,
                       length=LEN.KEYBOARD_DOWN_ARROW,
                       title='KeyboardDownArrow',
                       name='keyboard_down_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_DOWN_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_UP_ARROW,
                       length=LEN.KEYBOARD_UP_ARROW,
                       title='KeyboardUpArrow',
                       name='keyboard_up_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_UP_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LOCKING_NUM_LOCK,
                       length=LEN.KEYBOARD_LOCKING_NUM_LOCK,
                       title='KeyboardLockingNumLock',
                       name='keypad_num_lock_and_clear',
                       aliases=('keyboard_locking_num_lock',),
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LOCKING_NUM_LOCK) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_FORWARD_SLASH,
                       length=LEN.KEYPAD_FORWARD_SLASH,
                       title='KeypadForwardSlash',
                       name='keypad_forward_slash',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_FORWARD_SLASH) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_ASTERISK,
                       length=LEN.KEYPAD_ASTERISK,
                       title='KeypadAsterisk',
                       name='keypad_asterisk',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_ASTERISK) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_MINUS,
                       length=LEN.KEYPAD_MINUS,
                       title='KeypadMinus',
                       name='keypad_minus',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_MINUS) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_PLUS,
                       length=LEN.KEYPAD_PLUS,
                       title='KeypadPlus',
                       name='keypad_plus',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_PLUS) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_ENTER,
                       length=LEN.KEYPAD_ENTER,
                       title='KeypadEnter',
                       name='keypad_enter',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_ENTER) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_1_AND_END,
                       length=LEN.KEYPAD_1_AND_END,
                       title='Keypad1AndEnd',
                       name='keypad_1_and_end',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_1_AND_END) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_2_AND_DOWN_ARROW,
                       length=LEN.KEYPAD_2_AND_DOWN_ARROW,
                       title='Keypad2AndDownArrow',
                       name='keypad_2_and_down_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_2_AND_DOWN_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_3_AND_PAGE_DN,
                       length=LEN.KEYPAD_3_AND_PAGE_DN,
                       title='Keypad3AndPageDn',
                       name='keypad_3_and_page_dn',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_3_AND_PAGE_DN) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_4_AND_LEFT_ARROW,
                       length=LEN.KEYPAD_4_AND_LEFT_ARROW,
                       title='Keypad4AndLeftArrow',
                       name='keypad_4_and_left_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_4_AND_LEFT_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_5,
                       length=LEN.KEYPAD_5,
                       title='Keypad5',
                       name='keypad_5',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_5) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_6_AND_RIGHT_ARROW,
                       length=LEN.KEYPAD_6_AND_RIGHT_ARROW,
                       title='Keypad6AndRightArrow',
                       name='keypad_6_and_right_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_6_AND_RIGHT_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_7_AND_HOME,
                       length=LEN.KEYPAD_7_AND_HOME,
                       title='Keypad7AndHome',
                       name='keypad_7_and_home',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_7_AND_HOME) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_8_AND_UP_ARROW,
                       length=LEN.KEYPAD_8_AND_UP_ARROW,
                       title='Keypad8AndUpArrow',
                       name='keypad_8_and_up_arrow',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_8_AND_UP_ARROW) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_9_AND_PAGE_UP,
                       length=LEN.KEYPAD_9_AND_PAGE_UP,
                       title='Keypad9AndPageUp',
                       name='keypad_9_and_page_up',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_9_AND_PAGE_UP) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_0_AND_INSERT,
                       length=LEN.KEYPAD_0_AND_INSERT,
                       title='Keypad0AndInsert',
                       name='keypad_0_and_insert',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_0_AND_INSERT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_COMMA_AND_DELETE,
                       length=LEN.KEYPAD_COMMA_AND_DELETE,
                       title='KeypadCommaAndDelete',
                       name='keypad_comma_and_delete',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_COMMA_AND_DELETE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE,
                       length=LEN.KEYBOARD_NON_US_BACKSLASH_AND_PIPE,
                       title='KeyboardNonUSBackslashAndPipe',
                       name='keyboard_non_us_backslash_and_pipe',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_NON_US_BACKSLASH_AND_PIPE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_MENU,
                       length=LEN.KEYBOARD_MENU,
                       title='KeyboardMenu',
                       name='keyboard_menu',
                       aliases=('keyboard_application',),
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_MENU) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_POWER,
                       length=LEN.KEYBOARD_POWER,
                       title='KeyboardPower',
                       name='keyboard_power',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_POWER) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYPAD_EQUAL,
                       length=LEN.KEYPAD_EQUAL,
                       title='KeypadEqual',
                       name='keypad_equal',
                       checks=(CheckInt(0, pow(2, LEN.KEYPAD_EQUAL) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F13,
                       length=LEN.KEYBOARD_F13,
                       title='KeyboardF13',
                       name='keyboard_f13',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F13) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F14,
                       length=LEN.KEYBOARD_F14,
                       title='KeyboardF14',
                       name='keyboard_f14',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F14) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F15,
                       length=LEN.KEYBOARD_F15,
                       title='KeyboardF15',
                       name='keyboard_f15',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F15) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F16,
                       length=LEN.KEYBOARD_F16,
                       title='KeyboardF16',
                       name='keyboard_f16',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F16) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F17,
                       length=LEN.KEYBOARD_F17,
                       title='KeyboardF17',
                       name='keyboard_f17',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F17) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F18,
                       length=LEN.KEYBOARD_F18,
                       title='KeyboardF18',
                       name='keyboard_f18',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F18) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F19,
                       length=LEN.KEYBOARD_F19,
                       title='KeyboardF19',
                       name='keyboard_f19',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F19) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F20,
                       length=LEN.KEYBOARD_F20,
                       title='KeyboardF20',
                       name='keyboard_f20',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F20) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F21,
                       length=LEN.KEYBOARD_F21,
                       title='KeyboardF21',
                       name='keyboard_f21',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F21) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F22,
                       length=LEN.KEYBOARD_F22,
                       title='KeyboardF22',
                       name='keyboard_f22',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F22) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F23,
                       length=LEN.KEYBOARD_F23,
                       title='KeyboardF23',
                       name='keyboard_f23',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F23) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_F24,
                       length=LEN.KEYBOARD_F24,
                       title='KeyboardF24',
                       name='keyboard_f24',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_F24) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_INTERNATIONAL1,
                       length=LEN.KEYBOARD_INTERNATIONAL1,
                       title='KeyboardInternational1',
                       name='keyboard_international1',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_INTERNATIONAL1) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_INTERNATIONAL2,
                       length=LEN.KEYBOARD_INTERNATIONAL2,
                       title='KeyboardInternational2',
                       name='keyboard_international2',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_INTERNATIONAL2) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_INTERNATIONAL3,
                       length=LEN.KEYBOARD_INTERNATIONAL3,
                       title='KeyboardInternational3',
                       name='keyboard_international3',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_INTERNATIONAL3) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_INTERNATIONAL4,
                       length=LEN.KEYBOARD_INTERNATIONAL4,
                       title='KeyboardInternational4',
                       name='keyboard_international4',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_INTERNATIONAL4) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_INTERNATIONAL5,
                       length=LEN.KEYBOARD_INTERNATIONAL5,
                       title='KeyboardInternational5',
                       name='keyboard_international5',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_INTERNATIONAL5) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LANG1,
                       length=LEN.KEYBOARD_LANG1,
                       title='KeyboardLang1',
                       name='keyboard_lang1',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LANG1) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LANG2,
                       length=LEN.KEYBOARD_LANG2,
                       title='KeyboardLang2',
                       name='keyboard_lang2',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LANG2) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LANG3,
                       length=LEN.KEYBOARD_LANG3,
                       title='KeyboardLang3',
                       name='keyboard_lang3',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LANG3) - 1),),
                       default_value=DEFAULT.RELEASED),
              )

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional arguments.
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(*args, **kwargs)
    # end def __init__

    def __eq__(self, other):
        """
        Test the equality of this ``HidKeyboardBitmap`` instance with other.

        :param other: Other ``HidKeyboardBitmap`` instance
        :type other: ``HidKeyboardBitmap``

        :return: Comparison result
        :rtype: ``bool``

        :raise ``TypeError``: If other has not the right type
        """
        if not isinstance(other, HidKeyboardBitmap):
            raise TypeError("Other should be of type HidKeyboardBitmap")
        # end if

        result = (self.SUB_ID == other.SUB_ID)

        if result:
            result = super().__eq__(other)
        # end if

        return result

    # end def __eq__

    def __ne__(self, other):
        """
        Test the difference between this ``HidKeyboardBitmap`` instance and other.

        :param other: Other ``HidKeyboardBitmap`` instance
        :type other: ``HidKeyboardBitmap``

        :return: Comparison result
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

    def __hexlist__(self):
        """
        Convert the current object to an HexList

        :return: The object as an HexList
        :rtype: ``HexList``
        """
        data = super().__hexlist__()
        for data_index in range(len(data)):
            data[data_index] = reverse_bits(data[data_index])
        # end for
        return data
    # end def __hexlist__
# end class HidKeyboardBitmap

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
