#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.ledlayout
:brief: Kosmos LEDs configuration per product
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from typing import Dict

from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.kosmos.kosmosio import KosmosIO


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LedLayoutInterface(metaclass=ABCMeta):
    """
    Device LEDs layout Interface Class.
    """
    LEDS: Dict[LED_ID, KosmosIO.LEDS]       # LED mapping
    LED_ACTIVE_HIGH: bool                   # Indicates LED polarity
# end class LedLayoutInterface


class QuarkPlatformLedLayout(LedLayoutInterface):
    """
    Configure the LEDs layout on Quark development platform (BLE Keyboard & Mouse).
    """
    LEDS = {
        # Supported LEDs
        LED_ID.CONNECTIVITY_STATUS_LED_1: KosmosIO.LEDS.LED_0,
        LED_ID.CONNECTIVITY_STATUS_LED_2: KosmosIO.LEDS.LED_1,
        LED_ID.CONNECTIVITY_STATUS_LED_3: KosmosIO.LEDS.LED_2,
    }
    LED_ACTIVE_HIGH = False  # Indicates that a LED is active low
# end class QuarkPlatformLedLayout


class HerzogBleProLedLayout(QuarkPlatformLedLayout):
    """
    Configure the LEDs layout on Herzog BLE PRO.
    """
# end class HerzogBleProLedLayout


class FosterBleProLedLayout(QuarkPlatformLedLayout):
    """
    Configure the LEDs layout on Foster BLE PRO.
    """
# end class FosterBleProLedLayout


class FosterMiniBleProLedLayout(QuarkPlatformLedLayout):
    """
    Configure the LEDs layout on a Foster Mini BLE PRO keyboard.
    """
# end class FosterMiniBleProLedLayout

class IngaCsMacLedLayout(LedLayoutInterface):
    """
    Configure the LEDs layout on a Inga CS MAC keyboard.
    """
    LEDS = {
        LED_ID.PROXIMITY_SENSOR_ENABLED: KosmosIO.LEDS.LED_0,
        LED_ID.ALS_SENSOR_ENABLED: KosmosIO.LEDS.LED_1,
    }
    LED_ACTIVE_HIGH = True # True Indicates that a LED is active low.
# end class IngaCsMacLedLayout

class LetiLedLayout(LedLayoutInterface):
    """
    Configure the LEDs layout on LETI.
    """
    LEDS = {
        # Supported LEDs
        LED_ID.CONNECTIVITY_STATUS_LED_1: KosmosIO.LEDS.LED_0,
        # FIXME - Remove workaround: Channels 2 and 3 wires have been reversed on my LETI device
        LED_ID.CONNECTIVITY_STATUS_LED_2: KosmosIO.LEDS.LED_2,
        LED_ID.CONNECTIVITY_STATUS_LED_3: KosmosIO.LEDS.LED_1,
    }
    LED_ACTIVE_HIGH = True  # Indicates that a LED is active high.
# end class LetiLedLayout


class NormanLedLayout(LedLayoutInterface):
    """
    Configure the LEDs layout on Norman.
    """
    LEDS = {
        # Supported LEDs
        LED_ID.CONNECTIVITY_STATUS_LED_1: KosmosIO.LEDS.LED_0,
        LED_ID.CONNECTIVITY_STATUS_LED_2: KosmosIO.LEDS.LED_1,
        LED_ID.CONNECTIVITY_STATUS_LED_3: KosmosIO.LEDS.LED_2,
        LED_ID.CAPS_LOCK: KosmosIO.LEDS.LED_3,
        LED_ID.DEVICE_STATUS_RED_LED: KosmosIO.LEDS.LED_4,
        LED_ID.DEVICE_STATUS_GREEN_LED: KosmosIO.LEDS.LED_5,
        LED_ID.BACKLIGHT_LED: KosmosIO.LEDS.LED_6,
    }
    LED_ACTIVE_HIGH = False  # Indicates that a LED is active low.
# end class NormanLedLayout


class SlimplusLedLayout(LedLayoutInterface):
    """
    Configure the LEDs layout on Slimplus.
    """
    LEDS = {
        # Supported LEDs
        LED_ID.CONNECTIVITY_STATUS_LED_1: KosmosIO.LEDS.LED_0,
        LED_ID.CONNECTIVITY_STATUS_LED_2: KosmosIO.LEDS.LED_1,
        LED_ID.CONNECTIVITY_STATUS_LED_3: KosmosIO.LEDS.LED_2,
        LED_ID.CAPS_LOCK: KosmosIO.LEDS.LED_3,
        LED_ID.DEVICE_STATUS_RED_LED: KosmosIO.LEDS.LED_4,
        LED_ID.DEVICE_STATUS_GREEN_LED: KosmosIO.LEDS.LED_5,
    }
    LED_ACTIVE_HIGH = False  # Indicates that a LED is active low.
# end class SlimplusLedLayout


GET_LED_LAYOUT_BY_ID = {
    'RBK68': FosterBleProLedLayout,
    'RBK73': FosterMiniBleProLedLayout,
    'RBK75': IngaCsMacLedLayout,
    'RBK81': NormanLedLayout,
    'RBK90': SlimplusLedLayout,
    'RBM14': HerzogBleProLedLayout,
    'RBM21': LetiLedLayout,
}

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
