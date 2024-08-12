#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.emulator.keyid
:brief: Internal Key identifiers
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/07/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
@unique
class KEY_ID(IntEnum):
    """
    Internal key identifiers allowing a unique interpretation of the key to be pressed.
    """
    # Mouse
    LEFT_BUTTON = auto()
    RIGHT_BUTTON = auto()
    MIDDLE_BUTTON = auto()
    BACK_BUTTON = auto()
    FORWARD_BUTTON = auto()
    LEFT_SCROLL = auto()
    RIGHT_SCROLL = auto()
    CONNECT_BUTTON = auto()
    DPI_CYCLING_BUTTON = auto()
    DPI_UP_BUTTON = auto()
    DPI_DOWN_BUTTON = auto()
    DPI_SHIFT_BUTTON = auto()
    APP_SWITCH_GESTURE = auto()
    SMART_SHIFT = auto()
    VIRTUAL_GESTURE_BUTTON = auto()
    DPI_CHANGE = auto()
    DPI_SWITCH = auto()
    LAUNCH_DIDOT = auto()

    BUTTON_1 = auto()
    BUTTON_2 = auto()
    BUTTON_3 = auto()
    BUTTON_4 = auto()
    BUTTON_5 = auto()
    BUTTON_6 = auto()
    BUTTON_7 = auto()
    BUTTON_8 = auto()
    BUTTON_9 = auto()
    BUTTON_10 = auto()
    BUTTON_11 = auto()
    BUTTON_12 = auto()
    BUTTON_13 = auto()
    BUTTON_14 = auto()
    BUTTON_15 = auto()
    BUTTON_16 = auto()

    # Keyboard
    KEYBOARD_A = auto()
    KEYBOARD_B = auto()
    KEYBOARD_C = auto()
    KEYBOARD_D = auto()
    KEYBOARD_E = auto()
    KEYBOARD_F = auto()
    KEYBOARD_G = auto()
    KEYBOARD_H = auto()
    KEYBOARD_I = auto()
    KEYBOARD_J = auto()
    KEYBOARD_K = auto()
    KEYBOARD_L = auto()
    KEYBOARD_M = auto()
    KEYBOARD_N = auto()
    KEYBOARD_O = auto()
    KEYBOARD_P = auto()
    KEYBOARD_Q = auto()
    KEYBOARD_R = auto()
    KEYBOARD_S = auto()
    KEYBOARD_T = auto()
    KEYBOARD_U = auto()
    KEYBOARD_V = auto()
    KEYBOARD_W = auto()
    KEYBOARD_X = auto()
    KEYBOARD_Y = auto()
    KEYBOARD_Z = auto()
    KEYBOARD_1 = auto()
    KEYBOARD_2 = auto()
    KEYBOARD_3 = auto()
    KEYBOARD_4 = auto()
    KEYBOARD_5 = auto()
    KEYBOARD_6 = auto()
    KEYBOARD_7 = auto()
    KEYBOARD_8 = auto()
    KEYBOARD_9 = auto()
    KEYBOARD_0 = auto()
    KEYBOARD_RETURN_ENTER = auto()
    KEYBOARD_ESCAPE = auto()
    KEYBOARD_BACKSPACE = auto()
    KEYBOARD_TAB = auto()
    KEYBOARD_SPACE_BAR = auto()
    KEYBOARD_DASH_AND_UNDERSCORE = auto()
    KEYBOARD_EQUAL_AND_PLUS = auto()
    KEYBOARD_LEFT_BRACKET_AND_BRACE = auto()
    KEYBOARD_RIGHT_BRACKET_AND_BRACE = auto()
    KEYBOARD_BACKSLASH_AND_PIPE = auto()
    KEYBOARD_NON_US_AND_TILDE = auto()
    KEYBOARD_SEMICOLON_AND_COLON = auto()
    KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK = auto()
    KEYBOARD_GRAVE_ACCENT_AND_TILDE = auto()
    KEYBOARD_COMMA_AND_LESS = auto()
    KEYBOARD_PERIOD_AND_MORE = auto()
    KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK = auto()
    KEYBOARD_CAPS_LOCK = auto()
    KEYBOARD_F1 = auto()
    KEYBOARD_F2 = auto()
    KEYBOARD_F3 = auto()
    KEYBOARD_F4 = auto()
    KEYBOARD_F5 = auto()
    KEYBOARD_F6 = auto()
    KEYBOARD_F7 = auto()
    KEYBOARD_F8 = auto()
    KEYBOARD_F9 = auto()
    KEYBOARD_F10 = auto()
    KEYBOARD_F11 = auto()
    KEYBOARD_F12 = auto()
    KEYBOARD_F13 = auto()
    KEYBOARD_F14 = auto()
    KEYBOARD_F15 = auto()
    KEYBOARD_F16 = auto()
    KEYBOARD_F17 = auto()
    KEYBOARD_F18 = auto()
    KEYBOARD_F19 = auto()
    KEYBOARD_F20 = auto()
    KEYBOARD_F21 = auto()
    KEYBOARD_F22 = auto()
    KEYBOARD_F23 = auto()
    KEYBOARD_F24 = auto()
    KEYBOARD_PRINT_SCREEN = auto()
    KEYBOARD_SCROLL_LOCK = auto()
    KEYBOARD_COMPOSE = auto()
    KEYBOARD_KANA = auto()
    KEYBOARD_PAUSE = auto()
    KEYBOARD_INSERT = auto()
    KEYBOARD_HOME = auto()
    KEYBOARD_PAGE_UP = auto()
    KEYBOARD_DELETE_FORWARD = auto()
    KEYBOARD_END = auto()
    KEYBOARD_PAGE_DOWN = auto()
    KEYBOARD_RIGHT_ARROW = auto()
    KEYBOARD_LEFT_ARROW = auto()
    KEYBOARD_DOWN_ARROW = auto()
    KEYBOARD_UP_ARROW = auto()
    KEYPAD_NUM_LOCK_AND_CLEAR = auto()
    KEYPAD_FORWARD_SLASH = auto()
    KEYPAD_ASTERISK = auto()
    KEYPAD_MINUS = auto()
    KEYPAD_PLUS = auto()
    KEYPAD_ENTER = auto()
    KEYPAD_1_AND_END = auto()
    KEYPAD_2_AND_DOWN_ARROW = auto()
    KEYPAD_3_AND_PAGE_DN = auto()
    KEYPAD_4_AND_LEFT_ARROW = auto()
    KEYPAD_5 = auto()
    KEYPAD_6_AND_RIGHT_ARROW = auto()
    KEYPAD_7_AND_HOME = auto()
    KEYPAD_8_AND_UP_ARROW = auto()
    KEYPAD_9_AND_PAGE_UP = auto()
    KEYPAD_0_AND_INSERT = auto()
    KEYPAD_PERIOD_AND_DELETE = auto()
    KEYBOARD_NON_US_BACKSLASH_AND_PIPE = auto()
    KEYBOARD_POWER = auto()
    KEYPAD_EQUAL = auto()
    KEYBOARD_EXECUTE = auto()
    KEYBOARD_HELP = auto()
    KEYBOARD_MENU = auto()
    KEYBOARD_SELECT = auto()
    KEYBOARD_STOP = auto()
    KEYBOARD_AGAIN = auto()
    KEYBOARD_UNDO = auto()
    KEYBOARD_CUT = auto()
    KEYBOARD_COPY = auto()
    KEYBOARD_PASTE = auto()
    KEYBOARD_FIND = auto()
    KEYBOARD_MUTE = auto()
    KEYBOARD_VOLUME_UP = auto()
    KEYBOARD_VOLUME_DOWN = auto()
    KEYBOARD_LOCKING_CAPS_LOCK = auto()
    KEYBOARD_LOCKING_NUM_LOCK = auto()
    KEYBOARD_LOCKING_SCROLL_LOCK = auto()
    KEYPAD_COMMA = auto()
    KEYPAD_EQUAL_SIGN = auto()
    KEYBOARD_INTERNATIONAL1 = auto()
    KEYBOARD_INTERNATIONAL2 = auto()
    KEYBOARD_INTERNATIONAL3 = auto()
    KEYBOARD_INTERNATIONAL4 = auto()
    KEYBOARD_INTERNATIONAL5 = auto()
    KEYBOARD_INTERNATIONAL6 = auto()
    KEYBOARD_INTERNATIONAL7 = auto()
    KEYBOARD_INTERNATIONAL8 = auto()
    KEYBOARD_INTERNATIONAL9 = auto()
    KEYBOARD_LANG1 = auto()
    KEYBOARD_LANG2 = auto()
    KEYBOARD_LANG3 = auto()
    KEYBOARD_LANG4 = auto()
    KEYBOARD_LANG5 = auto()
    KEYBOARD_LANG6 = auto()
    KEYBOARD_LANG7 = auto()
    KEYBOARD_LANG8 = auto()
    KEYBOARD_LANG9 = auto()
    KEYBOARD_ALTERNATE_ERASE = auto()
    KEYBOARD_SYS_REQ_ATTENTION = auto()
    KEYBOARD_CANCEL = auto()
    KEYBOARD_CLEAR = auto()
    KEYBOARD_PRIOR = auto()
    KEYBOARD_RETURN = auto()
    KEYBOARD_SEPARATOR = auto()
    KEYBOARD_OUT = auto()
    KEYBOARD_OPER = auto()
    KEYBOARD_CLEAR_AGAIN = auto()
    KEYBOARD_CRSEL_PROPS = auto()
    KEYBOARD_EXSEL = auto()
    KEYPAD_00 = auto()
    KEYPAD_000 = auto()
    THOUSANDS_SEPARATOR = auto()
    DECIMAL_SEPARATOR = auto()
    CURRENCY_UNIT = auto()
    CURRENCY_SUB_UNIT = auto()
    KEYPAD_RIGHT_PARENTHESES = auto()
    KEYPAD_LEFT_PARENTHESES = auto()
    KEYPAD_RIGHT_BRACE = auto()
    KEYPAD_LEFT_BRACE = auto()
    KEYPAD_TAB = auto()
    KEYPAD_BACKSPACE = auto()
    KEYPAD_A = auto()
    KEYPAD_B = auto()
    KEYPAD_C = auto()
    KEYPAD_D = auto()
    KEYPAD_E = auto()
    KEYPAD_F = auto()
    KEYPAD_XOR = auto()
    KEYPAD_CARET = auto()
    KEYPAD_PERCENT = auto()
    KEYPAD_LESS = auto()
    KEYPAD_MORE = auto()
    KEYPAD_AMPERSAND = auto()
    KEYPAD_LOGICAL_AND = auto()
    KEYPAD_VERTICAL_BAR = auto()
    KEYPAD_LOGICAL_OR = auto()
    KEYPAD_COLON = auto()
    KEYPAD_HASH = auto()
    KEYPAD_SPACE = auto()
    KEYPAD_AT_SIGN = auto()
    KEYPAD_EXCLAMATION_MARK = auto()
    KEYPAD_MEMORY_STORE = auto()
    KEYPAD_MEMORY_RECALL = auto()
    KEYPAD_MEMORY_CLEAR = auto()
    KEYPAD_MEMORY_ADD = auto()
    KEYPAD_MEMORY_SUBSTRACT = auto()
    KEYPAD_MEMORY_MULTIPLY = auto()
    KEYPAD_MEMORY_DIVIDE = auto()
    KEYPAD_PLUS_MINUS = auto()
    KEYPAD_CLEAR = auto()
    KEYPAD_CLEAR_ENTRY = auto()
    KEYPAD_BINARY = auto()
    KEYPAD_OCTAL = auto()
    KEYPAD_DECIMAL = auto()
    KEYPAD_HEXADECIMAL = auto()
    KEYBOARD_LEFT_CONTROL = auto()
    KEYBOARD_LEFT_SHIFT = auto()
    KEYBOARD_LEFT_ALT = auto()
    KEYBOARD_LEFT_WIN_OR_OPTION = auto()
    KEYBOARD_RIGHT_CONTROL = auto()
    KEYBOARD_RIGHT_CONTROL_OR_OPTION = auto()
    KEYBOARD_RIGHT_SHIFT = auto()
    KEYBOARD_RIGHT_ALT = auto()
    KEYBOARD_RIGHT_WIN_OR_OPTION = auto()
    KEYBOARD_EASY_SWITCH_H1 = auto()

    # Fn + Standard Key for legacy keyboard
    FN_KEYBOARD_B = auto()
    FN_KEYBOARD_C = auto()
    FN_KEYBOARD_G = auto()
    FN_KEYBOARD_I = auto()
    FN_KEYBOARD_O = auto()
    FN_KEYBOARD_P = auto()
    FN_KEYBOARD_U = auto()
    FN_KEYBOARD_ENTER = auto()
    FN_KEYBOARD_SPACE_BAR = auto()
    FN_KEYBOARD_RIGHT_ARROW = auto()
    FN_KEYBOARD_LEFT_ARROW = auto()
    FN_KEYBOARD_DOWN_ARROW = auto()
    FN_KEYBOARD_UP_ARROW = auto()
    FN_KEYBOARD_RIGHT_CONTROL = auto()
    FN_KEYBOARD_RIGHT_CONTROL_OR_OPTION = auto()
    FN_KEYBOARD_RIGHT_ALT = auto()
    # Fn + Backspace
    FN_KEYBOARD_BACKSPACE = auto()
    # Fn + KP keys
    FN_KEYPAD_0 = auto()
    FN_KEYPAD_1 = auto()
    FN_KEYPAD_2 = auto()
    FN_KEYPAD_3 = auto()
    FN_KEYPAD_4 = auto()
    FN_KEYPAD_6 = auto()
    FN_KEYPAD_7 = auto()
    FN_KEYPAD_8 = auto()
    FN_KEYPAD_9 = auto()
    FN_KEYPAD_PERIOD = auto()
    FN_KEYPAD_ENTER = auto()

    # Not US
    KEYBOARD_NO_US_1 = auto()
    KEYBOARD_NO_US_42 = auto()
    KEYBOARD_NO_US_45 = auto()
    KEYBOARD_NO_US_64 = auto()

    # Multi-hosts
    HOST_1 = auto()
    HOST_2 = auto()
    HOST_3 = auto()

    # Gaming G-Keys
    G_1 = auto()
    G_2 = auto()
    G_3 = auto()
    G_4 = auto()
    G_5 = auto()
    G_6 = auto()
    G_7 = auto()
    G_8 = auto()
    G_9 = auto()
    G_10 = auto()
    G_11 = auto()
    G_12 = auto()
    G_13 = auto()
    G_14 = auto()
    G_15 = auto()
    G_16 = auto()
    G_17 = auto()
    G_18 = auto()

    # Gaming M-Keys
    M_1 = auto()
    M_2 = auto()
    M_3 = auto()
    M_4 = auto()
    M_5 = auto()
    M_6 = auto()
    M_7 = auto()
    M_8 = auto()

    # Macro Record MR key
    MR = auto()

    # Compound Keys
    COMPOUND_ALT_TAB = auto()       # Shift-GUI-P
    COMPOUND_PASTE = auto()         # Ctrl-V
    COMPOUND_HOME = auto()          # h-o-m-e
    COMPOUND_HOME_ISO_104 = auto()  # d-o-m
    COMPOUND_HOME_ISO_105 = auto()  # m-a-i-s-o-n
    COMPOUND_HOME_ISO_107 = auto()  # l-a-r
    COMPOUND_HOME_JIS_109 = auto()  # j-i-t-a-k-u
    COMPOUND_CTRL_ALT_DEL = auto()  # Ctrl-Alt-Delete

    # Function Keys
    NO_ACTION = auto()
    TILT_LEFT = auto()
    TILT_RIGHT = auto()
    SELECT_NEXT_DPI = auto()
    SELECT_PREV_DPI = auto()
    CYCLE_THROUGH_DPI = auto()
    DEFAULT_DPI = auto()
    DPI_SHIFT = auto()
    SELECT_NEXT_ONBOARD_PROFILE = auto()
    SELECT_PREV_ONBOARD_PROFILE = auto()
    CYCLE_THROUGH_ONBOARD_PROFILE = auto()
    G_SHIFT = auto()
    BATTERY_LIFE_INDICATOR = auto()
    SWITCH_TO_SPECIFIC_ONBOARD_PROFILE = auto()
    ONBOARD_PROFILE_1 = auto()
    ONBOARD_PROFILE_2 = auto()
    ONBOARD_PROFILE_3 = auto()
    ONBOARD_BASE_PROFILE = auto()
    ONBOARD_ACTUATION_MODE = auto()
    ONBOARD_RAPID_TRIGGER_MODE = auto()
    FKC_TOGGLE = auto()
    CYCLE_THROUGH_ANIMATION_EFFECTS = auto()
    CYCLE_THROUGH_COLOR_EFFECT_SUB_SETTINGS = auto()
    BACKLIGHT_DOWN = auto()
    BACKLIGHT_UP = auto()
    BACKLIGHT_CYCLING = auto()  # PWS Keyboard Keys Guidelines v3.1
    DIMMING_KEY = auto()  # Cycling through backlight intensity
    MISSION_CTRL_TASK_VIEW = auto()
    LAUNCHPAD_ACTION_CENTER = auto()
    APP_SWITCH = auto()
    SHOW_DESKTOP = auto()
    # Called Search / SpotLight in Guidelines doc
    MULTI_PLATF_SEARCH_SPOTLIGHT = auto()
    # Called Back in Guidelines doc
    MULTI_PLATF_BACK = auto()
    BRIGHTNESS_DOWN = auto()
    BRIGHTNESS_UP = auto()
    PREV_TRACK = auto()
    PLAY_PAUSE = auto()
    NEXT_TRACK = auto()
    CALCULATOR = auto()
    EJECT = auto()
    WAKE_SUSPEND = auto()
    BATTERY_CHECK = auto()
    FN_LOCK = auto()
    FN_INVERSION_CHANGE = auto()
    FN_INVERSION = auto()
    FN_KEY = auto()
    R_FN_KEY = auto()
    GAME_MODE_KEY = auto()
    LS2_BLE_CONNECTION_TOGGLE = auto()
    BLE_CONNECTION = auto()
    LS2_CONNECTION = auto()

    APP_SWITCH_LAUNCHPAD = auto()
    SCREEN_CAPTURE = auto()
    CONTEXTUAL_MENU = auto()
    SCREEN_LOCK = auto()
    DESKTOP_SYSTEM_SLEEP = auto()
    HOME = auto()
    EMOJI_PANEL = auto()
    DICTATION = auto()
    DO_NOT_DISTURB = auto()
    MUTE_MICROPHONE = auto()
    # Called Language switch in Guidelines doc
    LANGUAGE_SWITCH = auto()
    LIGHTNING_PATTERNS = auto()

    SMILING_FACE_WITH_HEART_SHAPED_EYES = auto()
    LOUDLY_CRYING_FACE = auto()
    EMOJI_SMILEY = auto()
    EMOJI_SMILEY_WITH_TEARS = auto()

    # New keys added in Guidelines v2.1
    AC_BACK = auto()  # Web page back
    REFRESH = auto()  # Web page refresh
    OPEN_NEW_TAB = auto()
    CLOSE_TAB = auto()
    PRINT = auto()
    OS_SETTINGS = auto()

    # New keys added in Guidelines v2.8
    GLOBE_KEY = auto()  # Mac only

    # JP & KR Language keys
    MUHENKAN = auto()
    HENKAN = auto()
    YEN = auto()
    KATAHIRA = auto()
    RO = auto()
    KANA = auto()
    HANJA = auto()
    HANGUEL = auto()

    # New Keys added in Guidelines v3.1
    SMART_ACTION_1 = auto()
    SMART_ACTION_2 = auto()
    SMART_ACTION_3 = auto()
    SMART_ACTION_4 = auto()

    # New Keys added in Guidelines v3.2
    HOME_APPLE_SKU = auto()
    FW_DELETE_APPLE_SKU = auto()

    # New Keys added in Guidelines v3.3
    WINDOWS_COPILOT = auto()
    CUT = auto()
    COPY = auto()
    PASTE = auto()

    # SWISS
    EURO_1 = auto()

    # Sliders
    POWER = auto()

    # ROLLERS
    ROLLER0_SCROLL_UP = auto()
    ROLLER0_SCROLL_DOWN = auto()
    ROLLER1_SCROLL_UP = auto()
    ROLLER1_SCROLL_DOWN = auto()

    MAX = auto()

    # Signals present on the keymatrix
    SIGNAL_N_POWER_GOOD = auto()
    SIGNAL_N_CHARGE = auto()
    SIGNAL_N_OFF = auto()
# end class KEY_ID


class ModifierKeys:
    """
    Shift
    Ctrl (Control)
    Alt (Alternate) – also labelled Option on Apple Macintosh keyboards
    AltGr (Alternate Graphic)
    Meta – Meta key, found on MIT, Symbolics, and Sun Microsystems keyboards
    Win (Windows logo) – found on Windows keyboards
    Cmd – Command key, found on Apple Macintosh keyboards. On older keyboards marked with the Apple logo.
    Fn (Function) – present on small-layout keyboard, usually on notebooks.
    """
    SHIFT = [KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_SHIFT]
    CTRL = [KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION]
    ALT = [KEY_ID.KEYBOARD_LEFT_ALT, KEY_ID.KEYBOARD_RIGHT_ALT]
    WIN = [KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION]
    CMD = ALT
    FN = [KEY_ID.FN_KEY, KEY_ID.R_FN_KEY]
    ALL = SHIFT + CTRL + ALT + WIN + FN
    FKC = SHIFT + CTRL + ALT + WIN
# end class ModifierKeys

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
