#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.emulator.ledid
:brief: Internal LED identifiers
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/01/21
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
class LED_ID(IntEnum):
    """
    Internal LED identifers allowing a unique interpretation of the LED to be monitored.
    """
    # C&P Device Status LEDs (Battery status or DFU)
    # https://docs.google.com/document/d/19LPqGV_zZRhDB2yzJvt-AtR7yHzaOv7B13bIaXetYNs/edit#
    DEVICE_STATUS_GREEN_LED = auto()
    DEVICE_STATUS_RED_LED = auto()

    # Gaming Device Status LEDs (Battery notification or DFU)
    # https://docs.google.com/document/d/1KfcgEZN6jzfyF0QPDS3caeZ1k4tY-SbtKDjFR4Apwao/edit
    # LED 1 means left-most or lowermost
    DEVICE_STATUS_LED_1 = auto()
    DEVICE_STATUS_LED_2 = auto()
    # LED 3 means rightmost or topmost
    DEVICE_STATUS_LED_3 = auto()

    # Gaming Device Fn key LED
    FN_KEY_LED = auto()

    # Gaming Device Macro key LEDs
    M1_LED = auto()
    M2_LED = auto()
    M3_LED = auto()
    MR_LED = auto()

    # Connectivity Status LEDs
    # LED 1 means left-most or lowermost
    CONNECTIVITY_STATUS_LED_1 = auto()
    CONNECTIVITY_STATUS_LED_2 = auto()
    # LED 3 means rightmost or topmost
    CONNECTIVITY_STATUS_LED_3 = auto()

    # C&P backlight effects
    # https://docs.google.com/document/d/1vbOeYiJB8sEm_o2ys3NdBYvQ4SCou4HJ_-HpemeCJ0g/edit?ts=5f7dec6c#
    BACKLIGHT_LED = auto()
    CAPS_LOCK = auto()
    NUM_LOCK = auto()
    SCROLL_LOCK = auto()
    COMPOSE = auto()
    KANA = auto()

    # RGB effects
    RGB_PRIMARY_RED_LED = auto()
    RGB_PRIMARY_GREEN_LED = auto()
    RGB_PRIMARY_BLUE_LED = auto()
    RGB_EDGE_RED_LED = auto()
    RGB_EDGE_GREEN_LED = auto()
    RGB_EDGE_BLUE_LED = auto()

    # Digital inputs used by kosmos ledspy module
    PROXIMITY_SENSOR_ENABLED = auto()
    ALS_SENSOR_ENABLED = auto()
# end class LED_ID


CONNECTIVITY_STATUS_LEDS = [LED_ID.CONNECTIVITY_STATUS_LED_1,
                            LED_ID.CONNECTIVITY_STATUS_LED_2,
                            LED_ID.CONNECTIVITY_STATUS_LED_3]
LOCK_KEYS_LEDS = [LED_ID.CAPS_LOCK,
                  LED_ID.NUM_LOCK,
                  LED_ID.SCROLL_LOCK,
                  LED_ID.COMPOSE,
                  LED_ID.KANA]
MACRO_KEYS_LEDS = [LED_ID.M1_LED,
                   LED_ID.M2_LED,
                   LED_ID.M3_LED,
                   LED_ID.MR_LED]

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
