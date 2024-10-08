#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.battery

@brief  HID parser usage pages battery class
        Built from https://www.usb.org/sites/default/files/pdcv10.pdf

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


class Battery(UsagePage):

    @classmethod
    def _get_usage_page_index(cls):
        return 0x85

    SMB_BATTERY_MODE = Usage(0x01, UsageType.COLLECTION_LOGICAL)
    SMB_BATTERY_STATUS = Usage(0x02, UsageType.COLLECTION_LOGICAL)
    SMB_ALARM_WARNING = Usage(0x03, UsageType.COLLECTION_LOGICAL)
    SMB_CHARGER_MODE = Usage(0x04, UsageType.COLLECTION_APPLICATION)
    SMB_CHARGER_STATUS = Usage(0x05, UsageType.COLLECTION_APPLICATION)
    SMB_CHARGER_SPEC_INFO = Usage(0x06, UsageType.COLLECTION_APPLICATION)
    SMB_SELECTOR_STATE = Usage(0x07, UsageType.COLLECTION_APPLICATION)
    SMB_SELECTOR_PRESETS = Usage(0x07, UsageType.COLLECTION_APPLICATION)
    SMB_SELECTOR_INFO = Usage(0x07, UsageType.COLLECTION_APPLICATION)

    OPTIONAL_MFG_FUNCTION_1 = Usage(0x10, UsageType.DATA_DYNAMIC_VALUE)
    OPTIONAL_MFG_FUNCTION_2 = Usage(0x11, UsageType.DATA_DYNAMIC_VALUE)
    OPTIONAL_MFG_FUNCTION_3 = Usage(0x12, UsageType.DATA_DYNAMIC_VALUE)
    OPTIONAL_MFG_FUNCTION_4 = Usage(0x13, UsageType.DATA_DYNAMIC_VALUE)
    OPTIONAL_MFG_FUNCTION_5 = Usage(0x14, UsageType.DATA_DYNAMIC_VALUE)

    CONNECTION_TO_SMBUS = Usage(0x15, UsageType.DATA_DYNAMIC_FLAG)
    OUTPUT_CONNECTION = Usage(0x16, UsageType.DATA_DYNAMIC_FLAG)
    CHARGER_CONNECTION = Usage(0x17, UsageType.DATA_DYNAMIC_FLAG)
    BATTERY_INSERTION = Usage(0x18, UsageType.DATA_DYNAMIC_FLAG)
    USE_NEXT = Usage(0x19, UsageType.DATA_DYNAMIC_FLAG)
    OK_TO_USE = Usage(0x1A, UsageType.DATA_DYNAMIC_FLAG)
    BATTERY_SUPPORTED = Usage(0x1B, UsageType.DATA_DYNAMIC_FLAG)
    SELECTOR_REVISION = Usage(0x1C, UsageType.DATA_DYNAMIC_FLAG)
    CHARGING_INDICATOR = Usage(0x1D, UsageType.DATA_DYNAMIC_FLAG)

    MANUFACTURER_ACCESS = Usage(0x28, UsageType.DATA_DYNAMIC_VALUE)
    REMAINING_CAPACITY_LIMIT = Usage(0x29, UsageType.DATA_DYNAMIC_VALUE)
    REMAINING_TIME_LIMIT = Usage(0x2A, UsageType.DATA_DYNAMIC_VALUE)
    AT_RATE = Usage(0x2B, UsageType.DATA_DYNAMIC_VALUE)
    CAPACITY_MODE = Usage(0x2C, UsageType.DATA_DYNAMIC_VALUE)
    BROADCAST_TO_CHARGER = Usage(0x2D, UsageType.DATA_DYNAMIC_VALUE)
    PRIMARY_BATTERY = Usage(0x2E, UsageType.DATA_DYNAMIC_VALUE)
    CHARGE_CONTROLLER = Usage(0x2F, UsageType.DATA_DYNAMIC_VALUE)

    TERMINATE_CHARGE = Usage(0x40, UsageType.DATA_DYNAMIC_FLAG)
    TERMINATE_DISCHARGE = Usage(0x41, UsageType.DATA_DYNAMIC_FLAG)
    BELOW_REMAINING_CAPACITY_LIMIT = Usage(0x42, UsageType.DATA_DYNAMIC_FLAG)
    REMAINING_TIME_LIMIT_EXPIRED = Usage(0x43, UsageType.DATA_DYNAMIC_FLAG)
    CHARGING = Usage(0x44, UsageType.DATA_DYNAMIC_FLAG)
    DISCHARGING = Usage(0x45, UsageType.DATA_DYNAMIC_VALUE)
    FULLY_CHARGED = Usage(0x46, UsageType.DATA_DYNAMIC_FLAG)
    FULLY_DISCHARGED = Usage(0x47, UsageType.DATA_DYNAMIC_VALUE)
    CONDITIONING_FLAG = Usage(0x48, UsageType.DATA_DYNAMIC_VALUE)
    AT_RATE_OK = Usage(0x49, UsageType.DATA_DYNAMIC_VALUE)
    SMB_ERROR_CODE = Usage(0x4A, UsageType.DATA_DYNAMIC_FLAG)
    NEED_REPLACEMENT = Usage(0x4B, UsageType.DATA_DYNAMIC_FLAG)

    AT_RATE_TIME_TO_FULL = Usage(0x60, UsageType.DATA_DYNAMIC_VALUE)
    AT_RATE_TIME_TO_EMPTY = Usage(0x61, UsageType.DATA_DYNAMIC_VALUE)
    AVERAGE_CURRENT = Usage(0x62, UsageType.DATA_DYNAMIC_VALUE)
    MAX_ERROR = Usage(0x63, UsageType.DATA_DYNAMIC_VALUE)
    RELATIVE_STATE_OF_CHARGE = Usage(0x64, UsageType.DATA_DYNAMIC_VALUE)
    ABSOLUTE_STATE_OF_CHARGE = Usage(0x65, UsageType.DATA_DYNAMIC_VALUE)
    REMAINING_CAPACITY = Usage(0x66, UsageType.DATA_DYNAMIC_VALUE)
    FULL_CHARGE_CAPACITY = Usage(0x67, UsageType.DATA_DYNAMIC_VALUE)
    RUN_TIME_TO_EMPTY = Usage(0x68, UsageType.DATA_DYNAMIC_VALUE)
    AVERAGE_TIME_TO_EMPTY = Usage(0x69, UsageType.DATA_DYNAMIC_VALUE)
    AVERAGE_TIME_TO_FULL = Usage(0x6A, UsageType.DATA_DYNAMIC_VALUE)
    CYCLE_COUNT = Usage(0x6B, UsageType.DATA_DYNAMIC_VALUE)

    BATT_PACK_MODEL_LEVEL = Usage(0x80, UsageType.DATA_STATIC_VALUE)
    INTERNAL_CHARGE_CONTROLLER = Usage(0x81, UsageType.DATA_STATIC_FLAG)
    PRIMARY_BATTERY_SUPPORT = Usage(0x82, UsageType.DATA_STATIC_FLAG)
    DESIGN_CAPACITY = Usage(0x83, UsageType.DATA_STATIC_VALUE)
    SPECIFICATION_INFO = Usage(0x84, UsageType.DATA_STATIC_VALUE)
    MANUFACTURER_DATE = Usage(0x85, UsageType.DATA_STATIC_VALUE)
    SERIAL_NUMBER = Usage(0x86, UsageType.DATA_STATIC_VALUE)
    I_MANUFACTURER_NAME = Usage(0x87, UsageType.DATA_STATIC_VALUE)
    I_DEVICE_NAME = Usage(0x88, UsageType.DATA_STATIC_VALUE)
    I_DEVICE_CHEMISTERY = Usage(0x89, UsageType.DATA_STATIC_VALUE)
    MANUFACTURER_DATA = Usage(0x8A, UsageType.DATA_STATIC_VALUE)
    RECHARGABLE = Usage(0x8B, UsageType.DATA_STATIC_VALUE)
    WARNING_CAPACITY_LIMIT = Usage(0x8C, UsageType.DATA_STATIC_VALUE)
    CAPACITY_GRANULARITY_1 = Usage(0x8D, UsageType.DATA_STATIC_VALUE)
    CAPACITY_GRANULARITY_2 = Usage(0x8E, UsageType.DATA_STATIC_VALUE)
    I_OEM_INFORMATION = Usage(0x8F, UsageType.DATA_STATIC_VALUE)

    INHIBIT_CHARGE = Usage(0xC0, UsageType.DATA_DYNAMIC_FLAG)
    ENABLE_POLLING = Usage(0xC1, UsageType.DATA_DYNAMIC_FLAG)
    RESET_TO_ZERO = Usage(0xC2, UsageType.DATA_DYNAMIC_FLAG)

    AC_PRESENT = Usage(0xD0, UsageType.DATA_DYNAMIC_FLAG)
    BATTERY_PRESENT = Usage(0xD1, UsageType.DATA_DYNAMIC_FLAG)
    POWER_FAIL = Usage(0xD2, UsageType.DATA_DYNAMIC_FLAG)
    ALARM_INHIBITED = Usage(0xD3, UsageType.DATA_DYNAMIC_FLAG)
    THERMISTOR_UNDER_RANGE = Usage(0xD4, UsageType.DATA_DYNAMIC_FLAG)
    THERMISTOR_HOT = Usage(0xD5, UsageType.DATA_DYNAMIC_FLAG)
    THERMISTOR_COLD = Usage(0xD6, UsageType.DATA_DYNAMIC_FLAG)
    THERMISTOR_OVER_RANGE = Usage(0xD7, UsageType.DATA_DYNAMIC_FLAG)
    VOLTAGE_OUT_OF_RANGE = Usage(0xD8, UsageType.DATA_DYNAMIC_FLAG)
    CURRENT_OUT_OF_RANGE = Usage(0xD9, UsageType.DATA_DYNAMIC_FLAG)
    CURRENT_NOT_REGULATED = Usage(0xDA, UsageType.DATA_DYNAMIC_FLAG)
    VOLTAGE_NOT_REGULATED = Usage(0xDB, UsageType.DATA_DYNAMIC_FLAG)
    MASTER_MODE = Usage(0xDC, UsageType.DATA_DYNAMIC_FLAG)

    CHARGER_SELECTOR_SUPPORT = Usage(0xF0, UsageType.DATA_STATIC_FLAG)
    CHARGER_SPEC = Usage(0xF1, UsageType.DATA_STATIC_VALUE)
    LEVEL_2 = Usage(0xF2, UsageType.DATA_STATIC_FLAG)
    LEVEL_3 = Usage(0xF3, UsageType.DATA_STATIC_FLAG)
