#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.led

@brief  HID parser usage pages led class
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


class Led(UsagePage):

    @classmethod
    def _get_usage_page_index(cls):
        return 0x8

    UNDEFINED = Usage(0x00, UsageType.CONTROL_ON_OFF)  # OOC
    NUM_LOCK = Usage(0x01, UsageType.CONTROL_ON_OFF)  # OOC
    CAPS_LOCK = Usage(0x02, UsageType.CONTROL_ON_OFF)  # OOC
    SCROLL_LOCK = Usage(0x03, UsageType.CONTROL_ON_OFF)  # OOC
    COMPOSE = Usage(0x04, UsageType.CONTROL_ON_OFF)  # OOC
    KANA = Usage(0x05, UsageType.CONTROL_ON_OFF)  # OOC
    POWER = Usage(0x06, UsageType.CONTROL_ON_OFF)  # OOC
    SHIFT = Usage(0x07, UsageType.CONTROL_ON_OFF)  # OOC
    DO_NOT_DISTURB = Usage(0x08, UsageType.CONTROL_ON_OFF)  # OOC
    MUTE = Usage(0x09, UsageType.CONTROL_ON_OFF)  # OOC
    TONE_ENABLE = Usage(0x0A, UsageType.CONTROL_ON_OFF)  # OOC
    HIGH_CUT_FILTER = Usage(0x0B, UsageType.CONTROL_ON_OFF)  # OOC
    LOW_CUT_FILTER = Usage(0x0C, UsageType.CONTROL_ON_OFF)  # OOC
    EQUALIZER_ENABLE = Usage(0x0D, UsageType.CONTROL_ON_OFF)  # OOC
    SOUND_FIELD_ON = Usage(0x0E, UsageType.CONTROL_ON_OFF)  # OOC
    SURROUND_FIELD_ON = Usage(0x0F, UsageType.CONTROL_ON_OFF)  # OOC
    REPEAT = Usage(0x10, UsageType.CONTROL_ON_OFF)  # OOC
    STEREO = Usage(0x11, UsageType.CONTROL_ON_OFF)  # OOC
    SAMPLING_RATE_DETECT = Usage(0x12, UsageType.CONTROL_ON_OFF)  # OOC
    SPINNING = Usage(0x13, UsageType.CONTROL_ON_OFF)  # OOC
    CAV = Usage(0x14, UsageType.CONTROL_ON_OFF)  # OOC
    CLV = Usage(0x15, UsageType.CONTROL_ON_OFF)  # OOC
    RECORDING_FORMAT_DETECT = Usage(0x16, UsageType.CONTROL_ON_OFF)  # OOC
    OFF_HOOK = Usage(0x17, UsageType.CONTROL_ON_OFF)  # OOC
    RING = Usage(0x18, UsageType.CONTROL_ON_OFF)  # OOC
    MESSAGE_WAITING = Usage(0x19, UsageType.CONTROL_ON_OFF)  # OOC
    DATA_MODE = Usage(0x1A, UsageType.CONTROL_ON_OFF)  # OOC
    BATTERY_OPERATION = Usage(0x1B, UsageType.CONTROL_ON_OFF)  # OOC
    BATTERY_OK = Usage(0x1C, UsageType.CONTROL_ON_OFF)  # OOC
    BATTERY_LOW = Usage(0x1D, UsageType.CONTROL_ON_OFF)  # OOC
    SPEAKER = Usage(0x1E, UsageType.CONTROL_ON_OFF)  # OOC
    HEAD_SET = Usage(0x1F, UsageType.CONTROL_ON_OFF)  # OOC
    HOLD	 = Usage(0x20, UsageType.CONTROL_ON_OFF)  # OOC
    MICROPHONE	 = Usage(0x21, UsageType.CONTROL_ON_OFF)  # OOC
    COVERAGE	 = Usage(0x22, UsageType.CONTROL_ON_OFF)  # OOC
    NIGHT_MODE	 = Usage(0x23, UsageType.CONTROL_ON_OFF)  # OOC
    SEND_CALLS	 = Usage(0x24, UsageType.CONTROL_ON_OFF)  # OOC
    CALL_PICKUP	 = Usage(0x25, UsageType.CONTROL_ON_OFF)  # OOC
    CONFERENCE	 = Usage(0x26, UsageType.CONTROL_ON_OFF)  # OOC
    STAND_BY	 = Usage(0x27, UsageType.CONTROL_ON_OFF)  # OOC
    CAMERA_ON	 = Usage(0x28, UsageType.CONTROL_ON_OFF)  # OOC
    CAMERA_OFF	 = Usage(0x29, UsageType.CONTROL_ON_OFF)  # OOC
    ON_LINE	 = Usage(0x2A, UsageType.CONTROL_ON_OFF)  # OOC
    OFF_LINE	 = Usage(0x2B, UsageType.CONTROL_ON_OFF)  # OOC
    BUSY	 = Usage(0x2C, UsageType.CONTROL_ON_OFF)  # OOC
    READY	 = Usage(0x2D, UsageType.CONTROL_ON_OFF)  # OOC
    PAPER_OUT	 = Usage(0x2E, UsageType.CONTROL_ON_OFF)  # OOC
    PAPER_JAM	 = Usage(0x2F, UsageType.CONTROL_ON_OFF)  # OOC
    REMOTE	 = Usage(0x30, UsageType.CONTROL_ON_OFF)  # OOC
    FORWARD	 = Usage(0x31, UsageType.CONTROL_ON_OFF)  # OOC
    REVERSE	 = Usage(0x32, UsageType.CONTROL_ON_OFF)  # OOC
    STOP	 = Usage(0x33, UsageType.CONTROL_ON_OFF)  # OOC
    REWIND	 = Usage(0x34, UsageType.CONTROL_ON_OFF)  # OOC
    FAST_FORWARD	 = Usage(0x35, UsageType.CONTROL_ON_OFF)  # OOC
    PLAY	 = Usage(0x36, UsageType.CONTROL_ON_OFF)  # OOC
    PAUSE	 = Usage(0x37, UsageType.CONTROL_ON_OFF)  # OOC
    RECORD	 = Usage(0x38, UsageType.CONTROL_ON_OFF)  # OOC
    ERROR	 = Usage(0x39, UsageType.CONTROL_ON_OFF)  # OOC
    USAGE_SELECTED_INDICATOR	 = Usage(0x3A, UsageType.CONTROL_ON_OFF)  # OOC
    USAGE_IN_USE_INDICATOR	 = Usage(0x3B, UsageType.CONTROL_ON_OFF)  # OOC
    USAGE_MULTI_MODE_INDICATOR	 = Usage(0x3C, UsageType.CONTROL_ON_OFF)  # OOC
    INDICATOR_ON	 = Usage(0x3D, UsageType.CONTROL_ON_OFF)  # OOC
    INDICATOR_FLASH	 = Usage(0x3E, UsageType.CONTROL_ON_OFF)  # OOC
    INDICATOR_SLOW_BLINK	 = Usage(0x3F, UsageType.CONTROL_ON_OFF)  # OOC
    INDICATOR_FAST_BLINK	 = Usage(0x40, UsageType.CONTROL_ON_OFF)  # OOC
    INDICATOR_OFF	 = Usage(0x41, UsageType.CONTROL_ON_OFF)  # OOC
    FLASH_ON_TIME	 = Usage(0x42, UsageType.CONTROL_ON_OFF)  # OOC
    SLOW_BLINK_ON_TIME	 = Usage(0x43, UsageType.CONTROL_ON_OFF)  # OOC
    SLOW_BLINK_OFF_TIME	 = Usage(0x44, UsageType.CONTROL_ON_OFF)  # OOC
    FAST_BLINK_ON_TIME	 = Usage(0x45, UsageType.CONTROL_ON_OFF)  # OOC
    FAST_BLINK_OFF_TIME	 = Usage(0x46, UsageType.CONTROL_ON_OFF)  # OOC
    USAGE_INDICATOR_COLOR	 = Usage(0x47, UsageType.CONTROL_ON_OFF)  # OOC
    RED	 = Usage(0x48, UsageType.CONTROL_ON_OFF)  # OOC
    GREEN	 = Usage(0x49, UsageType.CONTROL_ON_OFF)  # OOC
    AMBER	 = Usage(0x4A, UsageType.CONTROL_ON_OFF)  # OOC
    GENERIC_INDICATOR	 = Usage(0x4B, UsageType.CONTROL_ON_OFF)  # OOC
    SYSTEM_SUSPEND	 = Usage(0x4C, UsageType.CONTROL_ON_OFF)  # OOC
    EXTERNAL_POWER_CONNECTED	 = Usage(0x4D, UsageType.CONTROL_ON_OFF)  # OOC
    #  RESERVED	 = Usage(0x4C_FFFF, UsageType.CONTROL_ON_OFF)  # OOC
