#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.keyboard

@brief  HID parser usage pages keyboard class
        Built from https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage, UsageType, UsagePage

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class Keyboard(UsagePage):
    @classmethod
    def _get_usage_page_index(cls):
        return 0x07
    # end def _get_usage_page_index

    # keyboard category usages
    RESERVED_NO_EVENT_INDICATED = Usage(0x00, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_ERROR_ROLLOVER = Usage(0x01, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_POST_FAIL = Usage(0x02, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_ERROR_UNDEFINED = Usage(0x03, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_A_AND_A = Usage(0x04, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_B_AND_B = Usage(0x05, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_C_AND_C = Usage(0x06, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_D_AND_D = Usage(0x07, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_E_AND_E = Usage(0x08, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_F_AND_F = Usage(0x09, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_G_AND_G = Usage(0x0A, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_H_AND_H = Usage(0x0B, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_I_AND_I = Usage(0x0C, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_J_AND_J = Usage(0x0D, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_K_AND_K = Usage(0x0E, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_L_AND_L = Usage(0x0F, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_M_AND_M = Usage(0x10, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_N_AND_N = Usage(0x11, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_O_AND_O = Usage(0x12, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_P_AND_P = Usage(0x13, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_Q_AND_Q = Usage(0x14, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_R_AND_R = Usage(0x15, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_S_AND_S = Usage(0x16, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_T_AND_T = Usage(0x17, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_U_AND_U = Usage(0x18, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_V_AND_V = Usage(0x19, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_W_AND_W = Usage(0x1A, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_X_AND_X = Usage(0x1B, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_Y_AND_Y = Usage(0x1C, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_Z_AND_Z = Usage(0x1D, UsageType.DATA_SELECTOR)   # Sel
    KEYBOARD_1_AND_ = Usage(0x1E, UsageType.DATA_SELECTOR)  # KEYBOARD_1_AND_!
    KEYBOARD_2_AND_ = Usage(0x1F, UsageType.DATA_SELECTOR)  # KEYBOARD_2_AND_@
    KEYBOARD_3_AND_ = Usage(0x20, UsageType.DATA_SELECTOR)  # KEYBOARD_3_AND_#
    KEYBOARD_4_AND_ = Usage(0x21, UsageType.DATA_SELECTOR)  # KEYBOARD_4_AND_$
    KEYBOARD_5_AND_ = Usage(0x22, UsageType.DATA_SELECTOR)  # KEYBOARD_5_AND_%
    KEYBOARD_6_AND_ = Usage(0x23, UsageType.DATA_SELECTOR)  # KEYBOARD_6_AND_^
    KEYBOARD_7_AND_ = Usage(0x24, UsageType.DATA_SELECTOR)  # KEYBOARD_7_AND_&
    KEYBOARD_8_AND_ = Usage(0x25, UsageType.DATA_SELECTOR)  # KEYBOARD_8_AND_*
    KEYBOARD_9_AND_ = Usage(0x26, UsageType.DATA_SELECTOR)  # KEYBOARD_9_AND_(
    KEYBOARD_0_AND_ = Usage(0x27, UsageType.DATA_SELECTOR)  # KEYBOARD_0_AND_)
    KEYBOARD_RETURN_ENTER = Usage(0x28, UsageType.DATA_SELECTOR)  # KEYBOARD_RETURN_(ENTER)
    KEYBOARD_ESCAPE = Usage(0x29, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_DELETE_BACKSPACE = Usage(0x2A, UsageType.DATA_SELECTOR)  # KEYBOARD_DELETE_(BACKSPACE)
    KEYBOARD_TAB = Usage(0x2B, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_SPACE_BAR = Usage(0x2C, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_DASH_AND_UNDERSCORE = Usage(0x2D, UsageType.DATA_SELECTOR)  # KEYBOARD_-_AND_(UNDERSCORE)
    KEYBOARD_EQUAL_AND_PLUS = Usage(0x2E, UsageType.DATA_SELECTOR)  # KEYBOARD_=_AND_+
    KEYBOARD_LEFT_BRACKET_AND_BRACE = Usage(0x2F, UsageType.DATA_SELECTOR)  # KEYBOARD_[_AND_{
    KEYBOARD_RIGHT_BRACKET_AND_BRACE = Usage(0x30, UsageType.DATA_SELECTOR)  # KEYBOARD_]_AND_}
    KEYBOARD_BACKSLASH_AND_PIPE = Usage(0x31, UsageType.DATA_SELECTOR)  # KEYBOARD_\_AND_|
    KEYBOARD_NON_US_AND_TILDE = Usage(0x32, UsageType.DATA_SELECTOR)  # KEYBOARD_NON-US_#_AND_~
    KEYBOARD_SEMICOLON_AND_COLON = Usage(0x33, UsageType.DATA_SELECTOR)  # KEYBOARD_;_AND_:
    KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK = Usage(0x34, UsageType.DATA_SELECTOR)  # KEYBOARD_'_AND_"
    KEYBOARD_GRAVE_ACCENT_AND_TILDE = Usage(0x35, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_COMMA_AND_LESS = Usage(0x36, UsageType.DATA_SELECTOR)  # KEYBOARD,_AND_<
    KEYBOARD_PERIOD_AND_MORE = Usage(0x37, UsageType.DATA_SELECTOR)  # KEYBOARD_._AND_>
    KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK = Usage(0x38, UsageType.DATA_SELECTOR)  # KEYBOARD_/_AND_?
    KEYBOARD_CAPS_LOCK = Usage(0x39, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F1 = Usage(0x3A, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F2 = Usage(0x3B, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F3 = Usage(0x3C, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F4 = Usage(0x3D, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F5 = Usage(0x3E, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F6 = Usage(0x3F, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F7 = Usage(0x40, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F8 = Usage(0x41, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F9 = Usage(0x42, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F10 = Usage(0x43, UsageType.DATA_SELECTOR)  # Sel   
    KEYBOARD_F11 = Usage(0x44, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F12 = Usage(0x45, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_PRINT_SCREEN = Usage(0x46, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_SCROLL_LOCK = Usage(0x47, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_PAUSE = Usage(0x48, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INSERT = Usage(0x49, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_HOME = Usage(0x4A, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_PAGE_UP = Usage(0x4B, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_DELETE_FORWARD = Usage(0x4C, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_END = Usage(0x4D, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_PAGE_DOWN = Usage(0x4E, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_RIGHT_ARROW = Usage(0x4F, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_LEFT_ARROW = Usage(0x50, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_DOWN_ARROW = Usage(0x51, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_UP_ARROW = Usage(0x52, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_NUM_LOCK_AND_CLEAR = Usage(0x53, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_FORWARD_SLASH = Usage(0x54, UsageType.DATA_SELECTOR)  # KEYPAD_/
    KEYPAD_ASTERISK = Usage(0x55, UsageType.DATA_SELECTOR)  # KEYPAD_*
    KEYPAD_DASH = Usage(0x56, UsageType.DATA_SELECTOR)  # KEYPAD_-
    KEYPAD_PLUS = Usage(0x57, UsageType.DATA_SELECTOR)  # KEYPAD_+
    KEYPAD_ENTER = Usage(0x58, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_1_AND_END = Usage(0x59, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_2_AND_DOWN_ARROW = Usage(0x5A, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_3_AND_PAGE_DN = Usage(0x5B, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_4_AND_LEFT_ARROW = Usage(0x5C, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_5 = Usage(0x5D, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_6_AND_RIGHT_ARROW = Usage(0x5E, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_7_AND_HOME = Usage(0x5F, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_8_AND_UP_ARROW = Usage(0x60, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_9_AND_PAGE_UP = Usage(0x61, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_0_AND_INSERT = Usage(0x62, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_COMMA_AND_DELETE = Usage(0x63, UsageType.DATA_SELECTOR)  # KEYPAD_._AND_DELETE
    KEYBOARD_NON_US_BACKSLASH_AND_PIPE = Usage(0x64, UsageType.DATA_SELECTOR)  # KEYBOARD_NON-US_\_AND_|
    KEYBOARD_APPLICATION = Usage(0x65, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_POWER = Usage(0x66, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_EQUAL = Usage(0x67, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F13 = Usage(0x68, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F14 = Usage(0x69, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F15 = Usage(0x6A, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F16 = Usage(0x6B, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F17 = Usage(0x6C, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F18 = Usage(0x6D, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F19 = Usage(0x6E, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F20 = Usage(0x6F, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F21 = Usage(0x70, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F22 = Usage(0x71, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F23 = Usage(0x72, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_F24 = Usage(0x73, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_EXECUTE = Usage(0x74, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_HELP = Usage(0x75, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_MENU = Usage(0x76, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_SELECT = Usage(0x77, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_STOP = Usage(0x78, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_AGAIN = Usage(0x79, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_UNDO = Usage(0x7A, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_CUT = Usage(0x7B, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_COPY = Usage(0x7C, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_PASTE = Usage(0x7D, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_FIND = Usage(0x7E, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_MUTE = Usage(0x7F, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_VOLUME_UP = Usage(0x80, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_VOLUME_DOWN = Usage(0x81, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_LOCKING_CAPS_LOCK = Usage(0x82, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_LOCKING_NUM_LOCK = Usage(0x83, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_LOCKING_SCROLL_LOCK = Usage(0x84, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_COMMA = Usage(0x85, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_EQUAL_SIGN = Usage(0x86, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL1 = Usage(0x87, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL2 = Usage(0x88, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL3 = Usage(0x89, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL4 = Usage(0x8A, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL5 = Usage(0x8B, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL6 = Usage(0x8C, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL7 = Usage(0x8D, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL8 = Usage(0x8E, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_INTERNATIONAL9 = Usage(0x8F, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_LANG1 = Usage(0x90, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG2 = Usage(0x91, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG3 = Usage(0x92, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG4 = Usage(0x93, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG5 = Usage(0x94, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG6 = Usage(0x95, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG7 = Usage(0x96, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG8 = Usage(0x97, UsageType.DATA_SELECTOR)
    KEYBOARD_LANG9 = Usage(0x98, UsageType.DATA_SELECTOR)
    KEYBOARD_ALTERNATE_ERASE = Usage(0x99, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_SYS_REQ_ATTENTION = Usage(0x9A, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_CANCEL = Usage(0x9B, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_CLEAR = Usage(0x9C, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_PRIOR = Usage(0x9D, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_RETURN = Usage(0x9E, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_SEPARATOR = Usage(0x9F, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_OUT = Usage(0xA0, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_OPER = Usage(0xA1, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_CLEAR_AGAIN = Usage(0xA2, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_CRSEL_PROPS = Usage(0xA3, UsageType.DATA_SELECTOR)  # Sel
    KEYBOARD_EXSEL = Usage(0xA4, UsageType.DATA_SELECTOR)  # Sel
    RESERVED_A5 = Usage(0xA5, UsageType.DATA_SELECTOR)
    RESERVED_A6 = Usage(0xA6, UsageType.DATA_SELECTOR)
    RESERVED_A7 = Usage(0xA7, UsageType.DATA_SELECTOR)
    RESERVED_A8 = Usage(0xA8, UsageType.DATA_SELECTOR)
    RESERVED_A9 = Usage(0xA9, UsageType.DATA_SELECTOR)
    RESERVED_AA = Usage(0xAA, UsageType.DATA_SELECTOR)
    RESERVED_AB = Usage(0xAB, UsageType.DATA_SELECTOR)
    RESERVED_AC = Usage(0xAC, UsageType.DATA_SELECTOR)
    RESERVED_AD = Usage(0xAD, UsageType.DATA_SELECTOR)
    RESERVED_AE = Usage(0xAE, UsageType.DATA_SELECTOR)
    RESERVED_AF = Usage(0xAF, UsageType.DATA_SELECTOR)
    KEYPAD_00 = Usage(0xB0, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_000 = Usage(0xB1, UsageType.DATA_SELECTOR)  # Sel
    THOUSANDS_SEPARATOR = Usage(0xB2, UsageType.DATA_SELECTOR)  # Sel
    DECIMAL_SEPARATOR = Usage(0xB3, UsageType.DATA_SELECTOR)  # Sel
    CURRENCY_UNIT = Usage(0xB4, UsageType.DATA_SELECTOR)  # Sel
    CURRENCY_SUB_UNIT = Usage(0xB5, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_RIGHT_PARENTHESES = Usage(0xB6, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_LEFT_PARENTHESES = Usage(0xB7, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_RIGHT_BRACE = Usage(0xB8, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_LEFT_BRACE = Usage(0xB9, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_TAB = Usage(0xBA, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_BACKSPACE = Usage(0xBB, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_A = Usage(0xBC, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_B = Usage(0xBD, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_C = Usage(0xBE, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_D = Usage(0xBF, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_E = Usage(0xC0, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_F = Usage(0xC1, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_XOR = Usage(0xC2, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_CARET = Usage(0xC3, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_PERCENT = Usage(0xC4, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_LESS = Usage(0xC5, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MORE = Usage(0xC6, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_AMPERSAND = Usage(0xC7, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_LOGICAL_AND = Usage(0xC8, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_VERTICAL_BAR = Usage(0xC9, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_LOGICAL_OR = Usage(0xCA, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_COLON = Usage(0xCB, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_HASH = Usage(0xCC, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_SPACE = Usage(0xCD, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_AT_SIGN = Usage(0xCE, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_EXCLAMATION_MARK = Usage(0xCF, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MEMORY_STORE = Usage(0xD0, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MEMORY_RECALL = Usage(0xD1, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MEMORY_CLEAR = Usage(0xD2, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MEMORY_ADD = Usage(0xD3, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MEMORY_SUBSTRACT = Usage(0xD4, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MEMORY_MULTIPLY = Usage(0xD5, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_MEMORY_DIVIDE = Usage(0xD6, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_PLUS_MINUS = Usage(0xD7, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_CLEAR = Usage(0xD8, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_CLEAR_ENTRY = Usage(0xD9, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_BINARY = Usage(0xDA, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_OCTAL = Usage(0xDB, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_DECIMAL = Usage(0xDC, UsageType.DATA_SELECTOR)  # Sel
    KEYPAD_HEXADECIMAL = Usage(0xDD, UsageType.DATA_SELECTOR)  # Sel
    RESERVED_DE = Usage(0xDE, UsageType.DATA_SELECTOR)
    RESERVED_DF = Usage(0xDF, UsageType.DATA_SELECTOR)
    KEYBOARD_LEFT_CONTROL = Usage(0xE0, UsageType.DATA_DYNAMIC_VALUE)  # DV
    KEYBOARD_LEFTSHIFT = Usage(0xE1, UsageType.DATA_DYNAMIC_VALUE)  # DV
    KEYBOARD_LEFT_ALT = Usage(0xE2, UsageType.DATA_DYNAMIC_VALUE)  # DV
    KEYBOARD_LEFT_GUI = Usage(0xE3, UsageType.DATA_DYNAMIC_VALUE)  # DV
    KEYBOARD_RIGHT_CONTROL = Usage(0xE4, UsageType.DATA_DYNAMIC_VALUE)  # DV
    KEYBOARD_RIGHTSHIFT = Usage(0xE5, UsageType.DATA_DYNAMIC_VALUE)  # DV
    KEYBOARD_RIGHT_ALT = Usage(0xE6, UsageType.DATA_DYNAMIC_VALUE)  # DV
    KEYBOARD_RIGHT_GUI = Usage(0xE7, UsageType.DATA_DYNAMIC_VALUE)  # DV
    RESERVED_E8 = Usage(0xE8, UsageType.DATA_SELECTOR)
    RESERVED_E9 = Usage(0xE9, UsageType.DATA_SELECTOR)
    RESERVED_EA = Usage(0xEA, UsageType.DATA_SELECTOR)
    RESERVED_EB = Usage(0xEB, UsageType.DATA_SELECTOR)
    RESERVED_EC = Usage(0xEC, UsageType.DATA_SELECTOR)
    RESERVED_ED = Usage(0xED, UsageType.DATA_SELECTOR)
    RESERVED_EE = Usage(0xEE, UsageType.DATA_SELECTOR)
    RESERVED_EF = Usage(0xEF, UsageType.DATA_SELECTOR)
    RESERVED_F0 = Usage(0xF0, UsageType.DATA_SELECTOR)
    RESERVED_F1 = Usage(0xF1, UsageType.DATA_SELECTOR)
    RESERVED_F2 = Usage(0xF2, UsageType.DATA_SELECTOR)
    RESERVED_F3 = Usage(0xF3, UsageType.DATA_SELECTOR)
    RESERVED_F4 = Usage(0xF4, UsageType.DATA_SELECTOR)
    RESERVED_F5 = Usage(0xF5, UsageType.DATA_SELECTOR)
    RESERVED_F6 = Usage(0xF6, UsageType.DATA_SELECTOR)
    RESERVED_F7 = Usage(0xF7, UsageType.DATA_SELECTOR)
    RESERVED_F8 = Usage(0xF8, UsageType.DATA_SELECTOR)
    RESERVED_F9 = Usage(0xF9, UsageType.DATA_SELECTOR)
    RESERVED_FA = Usage(0xFA, UsageType.DATA_SELECTOR)
    RESERVED_FB = Usage(0xFB, UsageType.DATA_SELECTOR)
    RESERVED_FC = Usage(0xFC, UsageType.DATA_SELECTOR)
    RESERVED_FD = Usage(0xFD, UsageType.DATA_SELECTOR)
    RESERVED_FE = Usage(0xFE, UsageType.DATA_SELECTOR)
    RESERVED_FF = Usage(0xFF, UsageType.DATA_SELECTOR)

# end class Keyboard
