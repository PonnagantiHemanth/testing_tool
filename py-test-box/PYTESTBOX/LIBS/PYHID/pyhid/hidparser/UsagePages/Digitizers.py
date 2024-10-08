#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.digitizers

@brief  HID parser usage pages digitizers class
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


class Digitizers(UsagePage):

    @classmethod
    def _get_usage_page_index(cls):
        return 0x0D

    DIGITIZER = Usage(0x01,UsageType.COLLECTION_APPLICATION)
    PEN = Usage(0x02,UsageType.COLLECTION_APPLICATION)
    LIGHT_PEN = Usage(0x03,UsageType.COLLECTION_APPLICATION)
    TOUCH_SCREEN = Usage(0x04,UsageType.COLLECTION_APPLICATION)
    TOUCH_PAD = Usage(0x05,UsageType.COLLECTION_APPLICATION)
    WHITE_BOARD = Usage(0x06,UsageType.COLLECTION_APPLICATION)
    COORDINATE_MEASURING_MACHINE = Usage(0x07,UsageType.COLLECTION_APPLICATION)
    DIGITIZER_3D = Usage(0x08,UsageType.COLLECTION_APPLICATION)
    STEREO_PLOTTER = Usage(0x09,UsageType.COLLECTION_APPLICATION)
    ARTICULATED_ARM = Usage(0x0A,UsageType.COLLECTION_APPLICATION)
    ARMATURE = Usage(0x0B,UsageType.COLLECTION_APPLICATION)
    MULTIPLE_POINT_DIGITIZER = Usage(0x0C,UsageType.COLLECTION_APPLICATION)
    FREE_SPACE_WAND = Usage(0x0D,UsageType.COLLECTION_APPLICATION)

    STYLUS = Usage(0x20,UsageType.COLLECTION_LOGICAL)
    PUCK = Usage(0x21,UsageType.COLLECTION_LOGICAL)
    FINGER = Usage(0x22,UsageType.COLLECTION_LOGICAL)

    TIP_PRESSURE = Usage(0x30,UsageType.DATA_DYNAMIC_VALUE)
    BARREL_PRESSURE = Usage(0x31,UsageType.DATA_DYNAMIC_VALUE)
    IN_RANGE = Usage(0x32,UsageType.CONTROL_MOMENTARY)
    TOUCH = Usage(0x33,UsageType.CONTROL_MOMENTARY)
    UNTOUCH = Usage(0x34,UsageType.CONTROL_ONE_SHOT)
    TAP = Usage(0x35,UsageType.CONTROL_ONE_SHOT)
    QUALITY = Usage(0x36,UsageType.DATA_DYNAMIC_VALUE)
    DATA_VALID = Usage(0x37,UsageType.CONTROL_MOMENTARY)
    TRANSDUCER_INDEX = Usage(0x38,UsageType.DATA_DYNAMIC_VALUE)
    TABLET_FUNCTION_KEYS = Usage(0x39,UsageType.COLLECTION_LOGICAL)
    PROGRAM_CHANGE_KEYS = Usage(0x3A,UsageType.COLLECTION_LOGICAL)
    BATTERY_STRENGTH = Usage(0x3B,UsageType.DATA_DYNAMIC_VALUE)
    INVERT = Usage(0x3C,UsageType.CONTROL_MOMENTARY)
    X_TILT = Usage(0x3D,UsageType.DATA_DYNAMIC_VALUE)
    Y_TILT = Usage(0x3E,UsageType.DATA_DYNAMIC_VALUE)
    AZIMUTH = Usage(0x3F,UsageType.DATA_DYNAMIC_VALUE)
    ALTITUDE = Usage(0x40,UsageType.DATA_DYNAMIC_VALUE)
    TWIST = Usage(0x41,UsageType.DATA_DYNAMIC_VALUE)
    TIP_SWITCH = Usage(0x42,UsageType.CONTROL_MOMENTARY)
    SECONDARY_TIP_SWITCH = Usage(0x43,UsageType.CONTROL_MOMENTARY)
    BARREL_SWITCH = Usage(0x44,UsageType.CONTROL_MOMENTARY)
    ERASER = Usage(0x45,UsageType.CONTROL_MOMENTARY)
    TABLET_PICK = Usage(0x46,UsageType.CONTROL_MOMENTARY)

    # HID Usage Table Request 30: Addition of usages related to touch digitizers
    TOUCH_VALID = Usage(0x47, UsageType.CONTROL_MOMENTARY)
    WIDTH = Usage(0x48, UsageType.DATA_DYNAMIC_VALUE)
    HEIGHT = Usage(0x49, UsageType.DATA_DYNAMIC_VALUE)

    # HID Usage Table Request 34: Addition of usages related to multi-touch digitizers
    DEVICE_CONFIGURATION = Usage(0x0E, UsageType.COLLECTION_APPLICATION)
    DEVICE_SETTINGS = Usage(0x23, UsageType.COLLECTION_LOGICAL)

    CONTACT_IDENTIFIER = Usage(0x51, UsageType.DATA_DYNAMIC_VALUE)
    DEVICE_MODE = Usage(0x52, UsageType.DATA_DYNAMIC_VALUE)
    DEVICE_IDENTIFIER = Usage(0x53, UsageType.DATA_DYNAMIC_VALUE)
    CONTACT_COUNT = Usage(0x54, UsageType.DATA_DYNAMIC_VALUE)
    CONTACT_COUNT_MAXIMUM = Usage(0x55, UsageType.DATA_STATIC_VALUE)
    # Used by Microsoft... but not documented. Thanks!
    SCAN_TIME = Usage(0x56, UsageType.DATA_DYNAMIC_VALUE)

    # HID Usage Table Request 46: Additional Stylus Usages
    SECONDARY_BARREL_SWITCH = Usage(0x5A, UsageType.CONTROL_MOMENTARY)
    TRANSDUCER_SERIAL_NUMBER = Usage(0x5B, UsageType.DATA_STATIC_VALUE)

    # HID Usage Table Request 60: Stylus Width and Type Usages, Diagnostics, and Errors
    PREFERRED_COLOR_IS_LOCKED = Usage(0x5D, UsageType.CONTROL_MOMENTARY)
    PREFERRED_LINE_WIDTH = Usage(0x5E, UsageType.DATA_DYNAMIC_VALUE)
    PREFERRED_LINE_WIDTH_IS_LOCKED = Usage(0x5F, UsageType.CONTROL_MOMENTARY)
    PREFERRED_LINE_STYLE = Usage(0x70, UsageType.COLLECTION_NAMED_ARRAY)
    PREFERRED_LINE_STYLE_IS_LOCKED = Usage(0x71, UsageType.CONTROL_MOMENTARY)
    INK = Usage(0x72, UsageType.DATA_SELECTOR)
    PENCIL = Usage(0x73, UsageType.DATA_SELECTOR)
    HIGHLIGHTER = Usage(0x74, UsageType.DATA_SELECTOR)
    CHISEL_MARKER = Usage(0x75, UsageType.DATA_SELECTOR)
    BRUSH = Usage(0x76, UsageType.DATA_SELECTOR)
    NO_PREFERENCE = Usage(0x77, UsageType.DATA_SELECTOR)

    DIGITIZER_DIAGNOSTIC = Usage(0x80, UsageType.COLLECTION_LOGICAL)
    DIGITIZER_ERROR = Usage(0x81, UsageType.COLLECTION_NAMED_ARRAY)
    ERR_NORMAL_STATUS = Usage(0x82, UsageType.DATA_SELECTOR)
    ERR_TRANSDUCERS_EXCEEDED = Usage(0x83, UsageType.DATA_SELECTOR)
    ERR_FULL_TRANS_FEATURES_UNAVAIL = Usage(0x84, UsageType.DATA_SELECTOR)
    ERR_CHARGE_LOW = Usage(0x85, UsageType.DATA_SELECTOR)
