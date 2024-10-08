#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.power

@brief  HID parser usage pages power class
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


class Power(UsagePage):

    @classmethod
    def _get_usage_page_index(cls):
        return 0x84

    I_NAME = Usage(0x01, UsageType.DATA_STATIC_VALUE)
    PRESENT_STATUS = Usage(0x02, UsageType.COLLECTION_LOGICAL)
    CHANGED_STATUS = Usage(0x03, UsageType.COLLECTION_LOGICAL)
    UPS = Usage(0x04, UsageType.COLLECTION_APPLICATION)
    POWER_SUPPLY = Usage(0x05, UsageType.COLLECTION_APPLICATION)

    BATTERY_SYSTEM = Usage(0x10, UsageType.COLLECTION_PHYSICAL)
    BATTERY_SYSTEM_ID = Usage(0x11, UsageType.DATA_STATIC_VALUE)

    BATTERY = Usage(0x12, UsageType.COLLECTION_PHYSICAL)
    BATTERY_ID = Usage(0x13, UsageType.DATA_STATIC_VALUE)

    CHARGER = Usage(0x14, UsageType.COLLECTION_PHYSICAL)
    CHARGER_ID = Usage(0x15, UsageType.DATA_STATIC_VALUE)

    POWER_CONVERTER = Usage(0x16, UsageType.COLLECTION_PHYSICAL)
    POWER_CONVERTER_ID = Usage(0x17, UsageType.DATA_STATIC_VALUE)

    OUTLET_SYSTEM = Usage(0x18, UsageType.COLLECTION_PHYSICAL)
    OUTLET_SYSTEM_ID = Usage(0x19, UsageType.DATA_STATIC_VALUE)

    INPUT = Usage(0x1A, UsageType.COLLECTION_PHYSICAL)
    INPUT_ID = Usage(0x1B, UsageType.DATA_STATIC_VALUE)

    OUTPUT = Usage(0x1C, UsageType.COLLECTION_PHYSICAL)
    OUTPUT_ID = Usage(0x1D, UsageType.DATA_STATIC_VALUE)

    FLOW = Usage(0x1E, UsageType.COLLECTION_PHYSICAL)
    FLOW_ID = Usage(0x1F, UsageType.DATA_STATIC_VALUE)

    OUTLET = Usage(0x20, UsageType.COLLECTION_PHYSICAL)
    OUTLET_ID = Usage(0x21, UsageType.DATA_STATIC_VALUE)

    GANG = Usage(0x22, [UsageType.COLLECTION_PHYSICAL, UsageType.COLLECTION_LOGICAL])
    GANG_ID = Usage(0x23, UsageType.DATA_STATIC_VALUE)

    POWER_SUMMARY = Usage(0x24, [UsageType.COLLECTION_PHYSICAL, UsageType.COLLECTION_LOGICAL])
    POWER_SUMMARY_ID = Usage(0x25, UsageType.DATA_STATIC_VALUE)

    VOLTAGE = Usage(0x30, UsageType.DATA_DYNAMIC_VALUE)
    CURRENT = Usage(0x31, UsageType.DATA_DYNAMIC_VALUE)
    FREQUENCY = Usage(0x32, UsageType.DATA_DYNAMIC_VALUE)
    APPARENT_POWER = Usage(0x33, UsageType.DATA_DYNAMIC_VALUE)
    ACTIVE_POWER = Usage(0x34, UsageType.DATA_DYNAMIC_VALUE)
    PERCENT_LOAD = Usage(0x35, UsageType.DATA_DYNAMIC_VALUE)
    TEMPERATURE = Usage(0x36, UsageType.DATA_DYNAMIC_VALUE)
    HUMIDITY = Usage(0x37, UsageType.DATA_DYNAMIC_VALUE)
    BAD_COUNT = Usage(0x38, UsageType.DATA_DYNAMIC_VALUE)

    CONFIG_VOLTAGE = Usage(0x40, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])
    CONFIG_CURRENT = Usage(0x41, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])
    CONFIG_FREQUENCY = Usage(0x42, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])
    CONFIG_APPARENT_POWER = Usage(0x43, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])
    CONFIG_ACTIVE_POWER = Usage(0x44, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])
    CONFIG_PERCENT_LOAD = Usage(0x45, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])
    CONFIG_TEMPERATURE = Usage(0x46, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])
    CONFIG_HUMIDITY = Usage(0x47, [UsageType.DATA_DYNAMIC_VALUE, UsageType.DATA_STATIC_VALUE])

    SWITCH_ON_CONTROL = Usage(0x50, UsageType.DATA_DYNAMIC_VALUE)
    SWITCH_OFF_CONTROL = Usage(0x51, UsageType.DATA_DYNAMIC_VALUE)
    TOGGLE_CONTROL = Usage(0x52, UsageType.DATA_DYNAMIC_VALUE)
    LOW_VOLTAGE_TRANSFER = Usage(0x53, UsageType.DATA_DYNAMIC_VALUE)
    HIGH_VOLTAGE_TRANSFER = Usage(0x54, UsageType.DATA_DYNAMIC_VALUE)
    DELAY_BEFORE_REBOOT = Usage(0x55, UsageType.DATA_DYNAMIC_VALUE)
    DELAY_BEFORE_STARTUP = Usage(0x56, UsageType.DATA_DYNAMIC_VALUE)
    DELAY_BEFORE_SHUTDOWN = Usage(0x57, UsageType.DATA_DYNAMIC_VALUE)
    TEST = Usage(0x58, UsageType.DATA_DYNAMIC_VALUE)
    MODULE_RESET = Usage(0x59, UsageType.DATA_DYNAMIC_VALUE)
    AUDIBLE_ALARM_CONTROL = Usage(0x5A, UsageType.DATA_DYNAMIC_VALUE)

    PRESENT = Usage(0x60, UsageType.DATA_DYNAMIC_FLAG)
    GOOD = Usage(0x61, UsageType.DATA_DYNAMIC_FLAG)
    INTERNAL_FAILURE = Usage(0x62, UsageType.DATA_DYNAMIC_FLAG)
    VOLTAGE_OUT_OF_RANGE = Usage(0x63, UsageType.DATA_DYNAMIC_FLAG)
    FREQUENCY_OUT_OF_RANGE = Usage(0x64, UsageType.DATA_DYNAMIC_FLAG)
    OVERLOAD = Usage(0x65, UsageType.DATA_DYNAMIC_FLAG)
    OVER_CHARGED = Usage(0x66, UsageType.DATA_DYNAMIC_FLAG)
    OVER_TEMPERATURE = Usage(0x67, UsageType.DATA_DYNAMIC_FLAG)
    SHUTDOWN_REQUESTED = Usage(0x68, UsageType.DATA_DYNAMIC_FLAG)
    SHUTDOWN_IMMINENT = Usage(0x69, UsageType.DATA_DYNAMIC_FLAG)
    
    SWITCH_ON_OFF = Usage(0x6B, UsageType.DATA_DYNAMIC_FLAG)
    SWITCHABLE = Usage(0x6C, UsageType.DATA_DYNAMIC_FLAG)
    USED = Usage(0x6D, UsageType.DATA_DYNAMIC_FLAG)
    BOOST = Usage(0x6E, UsageType.DATA_DYNAMIC_FLAG)
    BUCK = Usage(0x6F, UsageType.DATA_DYNAMIC_FLAG)

    INITIALIZED = Usage(0x70, UsageType.DATA_DYNAMIC_FLAG)
    TESTED = Usage(0x71, UsageType.DATA_DYNAMIC_FLAG)
    AWAITING_POWER = Usage(0x72, UsageType.DATA_DYNAMIC_FLAG)
    COMMUNICATION_LOST = Usage(0x73, UsageType.DATA_DYNAMIC_FLAG)

    I_MANUFACTURER = Usage(0xFD, UsageType.DATA_STATIC_VALUE)
    I_PRODUCT = Usage(0xFE, UsageType.DATA_DYNAMIC_FLAG)
    I_SERIAL_NUMBER = Usage(0xFF, UsageType.DATA_DYNAMIC_FLAG)

# end class Power
