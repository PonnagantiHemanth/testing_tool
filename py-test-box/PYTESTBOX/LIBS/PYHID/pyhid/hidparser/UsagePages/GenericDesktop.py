#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.genericdesktop

@brief  HID parser usage pages generic desktop class
        Built from https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import UsagePage, UsageType, Usage

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class GenericDesktop(UsagePage):
    POINTER = Usage(0x01, UsageType.COLLECTION_PHYSICAL)
    MOUSE = Usage(0x02, UsageType.COLLECTION_APPLICATION)
    JOYSTICK = Usage(0x04, UsageType.COLLECTION_APPLICATION)
    GAME_PAD = Usage(0x05, UsageType.COLLECTION_APPLICATION)
    KEYBOARD = Usage(0x06, UsageType.COLLECTION_APPLICATION)
    KEYPAD = Usage(0x07, UsageType.COLLECTION_APPLICATION)
    MULTI_AXIS_CONTROLLER = Usage(0x08, UsageType.COLLECTION_APPLICATION)
    TABLET_PC_SYSTEM_CONTROLS = Usage(0x09, UsageType.COLLECTION_APPLICATION)
    CALL_STATE_MANAGEMENT_CONTROL = Usage(0x13, UsageType.COLLECTION_APPLICATION)

    X = Usage(0x30, UsageType.DATA_DYNAMIC_VALUE)
    Y = Usage(0x31, UsageType.DATA_DYNAMIC_VALUE)
    Z = Usage(0x32, UsageType.DATA_DYNAMIC_VALUE)
    R_X = Usage(0x33, UsageType.DATA_DYNAMIC_VALUE)
    R_Y = Usage(0x34, UsageType.DATA_DYNAMIC_VALUE)
    R_Z = Usage(0x35, UsageType.DATA_DYNAMIC_VALUE)
    SLIDER = Usage(0x36, UsageType.DATA_DYNAMIC_VALUE)
    DIAL = Usage(0x37, UsageType.DATA_DYNAMIC_VALUE)
    WHEEL = Usage(0x38, UsageType.DATA_DYNAMIC_VALUE)
    HAT_SWITCH = Usage(0x39, UsageType.DATA_DYNAMIC_VALUE)
    COUNTED_BUFFER = Usage(0x3A, UsageType.COLLECTION_LOGICAL)
    BYTE_COUNT = Usage(0x3B, UsageType.DATA_DYNAMIC_VALUE)
    MOTION_WAKEUP = Usage(0x3C, UsageType.CONTROL_ONE_SHOT)
    START = Usage(0x3D, UsageType.CONTROL_ON_OFF)
    SELECT = Usage(0x3E, UsageType.CONTROL_ON_OFF)

    V_X = Usage(0x40, UsageType.DATA_DYNAMIC_VALUE)
    V_Y = Usage(0x41, UsageType.DATA_DYNAMIC_VALUE)
    V_Z = Usage(0x42, UsageType.DATA_DYNAMIC_VALUE)
    V_BRX = Usage(0x43, UsageType.DATA_DYNAMIC_VALUE)
    V_BRY = Usage(0x44, UsageType.DATA_DYNAMIC_VALUE)
    V_BRZ = Usage(0x45, UsageType.DATA_DYNAMIC_VALUE)
    V_NO = Usage(0x46, UsageType.DATA_DYNAMIC_VALUE)
    FEATURE_NOTIFICATION = Usage(0x47, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_DYNAMIC_FLAG])
    RESOLUTION_MULTIPLIER = Usage(0x48, UsageType.DATA_DYNAMIC_VALUE)

    SYSTEM_CONTROL = Usage(0x80, UsageType.COLLECTION_APPLICATION)
    SYSTEM_POWER_DOWN = Usage(0x81, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_SLEEP = Usage(0x82, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_WAKE_UP = Usage(0x83, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_CONTEXT_MENU = Usage(0x84, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_MAIN_MENU = Usage(0x85, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_APP_MENU = Usage(0x86, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_MENU_HELP = Usage(0x87, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_MENU_EXIT = Usage(0x88, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_MENU_SELECT = Usage(0x89, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_MENU_RIGHT = Usage(0x8A, UsageType.CONTROL_RE_TRIGGER)
    SYSTEM_MENU_LEFT = Usage(0x8B, UsageType.CONTROL_RE_TRIGGER)
    SYSTEM_MENU_UP = Usage(0x8C, UsageType.CONTROL_RE_TRIGGER)
    SYSTEM_MENU_DOWN = Usage(0x8D, UsageType.CONTROL_RE_TRIGGER)
    SYSTEM_COLD_RESTART = Usage(0x8E, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_WARM_RESTART = Usage(0x8F, UsageType.CONTROL_ONE_SHOT)
    D_PAD_UP = Usage(0x90, UsageType.CONTROL_ON_OFF)
    D_PAY_DOWN = Usage(0x91, UsageType.CONTROL_ON_OFF)
    D_PAD_RIGHT = Usage(0x92, UsageType.CONTROL_ON_OFF)
    D_PAD_LEFT = Usage(0x93, UsageType.CONTROL_ON_OFF)

    SYSTEM_DO_NOT_DISTURB = Usage(0x9B, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DOCK = Usage(0xA0, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_UNDOCK = Usage(0xA1, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_SETUP = Usage(0xA2, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_BREAK = Usage(0xA3, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DEBUGGER_BREAK = Usage(0xA4, UsageType.CONTROL_ONE_SHOT)
    APPLICATION_BREAK = Usage(0xA5, UsageType.CONTROL_ONE_SHOT)
    APPLICATION_DEBUGGER_BREAK = Usage(0xA6, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_SPEAKER_MUTE = Usage(0xA7, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_HIBERNATE = Usage(0xA8, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_MICROPHONE_MUTE = Usage(0xA9, UsageType.CONTROL_ONE_SHOT)

    SYSTEM_DISPLAY_INVERT = Usage(0xB0, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DISPLAY_INTERNAL = Usage(0xB1, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DISPLAY_EXTERNAL = Usage(0xB2, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DISPLAY_BOTH = Usage(0xB3, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DISPLAY_DUAL = Usage(0xB4, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DISPLAY_TOGGLE_INT_EXT = Usage(0xB5, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DISPLAY_SWAP_PRIMARY_SECONDARY = Usage(0xB6, UsageType.CONTROL_ONE_SHOT)
    SYSTEM_DISPLAY_LCD_AUTOSCALE = Usage(0xB7, UsageType.CONTROL_ONE_SHOT)

    # cf https://www.usb.org/sites/default/files/hutrr106-callstatemanagementcontrol_0.pdf
    CALL_ACTIVE_LED = Usage(0xE0, UsageType.CONTROL_ON_OFF)
    CALL_MUTE_TOGGLE = Usage(0xE1, UsageType.CONTROL_ONE_SHOT)
    CALL_MUTE_LED = Usage(0xE2, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_E3 = Usage(0xE3, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_E4 = Usage(0xE4, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_E5 = Usage(0xE5, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_E6 = Usage(0xE6, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_E7 = Usage(0xE7, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_E8 = Usage(0xE8, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_E9 = Usage(0xE9, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_EA = Usage(0xEA, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_EB = Usage(0xEB, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_EC = Usage(0xEC, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_ED = Usage(0xED, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_EE = Usage(0xEE, UsageType.CONTROL_ON_OFF)
    CALL_STATE_RESERVED_EF = Usage(0xEF, UsageType.CONTROL_ON_OFF)

    @classmethod
    def _get_usage_page_index(cls):
        return 0x01
