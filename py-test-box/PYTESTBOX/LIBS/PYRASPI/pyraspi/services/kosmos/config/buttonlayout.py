#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.buttonlayout
:brief: Kosmos Button configuration per product
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from typing import Dict
from typing import Tuple
from typing import Union

from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.kosmos.kosmosio import KosmosIO


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MouseLayoutInterface(metaclass=ABCMeta):
    """
    Device button layout Interface Class
    """
    KEYS: Dict[KEY_ID, Union[KosmosIO.BUTTONS, Tuple[KosmosIO.BUTTONS, KosmosIO.SLIDERS]]]
    HAS_HYBRID_SWITCH = False
    OPTICAL_KEYS: Dict[KEY_ID, Union[KosmosIO.BUTTONS, KosmosIO.SLIDERS]]
# end class MouseLayoutInterface


class CoreMouseLayout(MouseLayoutInterface):
    """
    Configure the button layout of the device
    """
    KEYS = {
        KEY_ID.LEFT_BUTTON: KosmosIO.BUTTONS.BUTTON_0,
        KEY_ID.RIGHT_BUTTON: KosmosIO.BUTTONS.BUTTON_1,
        KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,
        KEY_ID.CONNECT_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
        KEY_ID.SMART_SHIFT: KosmosIO.BUTTONS.BUTTON_4,
        KEY_ID.FORWARD_BUTTON: KosmosIO.BUTTONS.BUTTON_5,
        KEY_ID.BACK_BUTTON: KosmosIO.BUTTONS.BUTTON_6,
    }
# end class CoreMouseLayout


class BazookaLayout(MouseLayoutInterface):
    """
    Configure the button layout of the Bazooka mouse
    """
    KEYS = {
        KEY_ID.LEFT_BUTTON: KosmosIO.BUTTONS.BUTTON_0,
        KEY_ID.RIGHT_BUTTON: KosmosIO.BUTTONS.BUTTON_1,
        # KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,  # TODO DUT 'SW3' nRF GPIO is damaged. Uncomment for new DUT.
        KEY_ID.BACK_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
        KEY_ID.FORWARD_BUTTON: KosmosIO.BUTTONS.BUTTON_4,
    }
# end class BazookaLayout


class Bazooka2Layout(MouseLayoutInterface):
    """
    Configure the button layout of the Bazooka2 mouse.

    Notes: Hybrid hardware,
           Buttons 0 to 4 are galvanic switches,
           Buttons 5 & 6 are optical switches.
    """
    HAS_HYBRID_SWITCH = True
    KEYS = {
        KEY_ID.LEFT_BUTTON:  (KosmosIO.BUTTONS.BUTTON_0, KosmosIO.BUTTONS.BUTTON_5),  # (galvanic, optical) switches
        KEY_ID.RIGHT_BUTTON: (KosmosIO.BUTTONS.BUTTON_1, KosmosIO.BUTTONS.BUTTON_6),  # (galvanic, optical) switches
        KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,
        KEY_ID.BACK_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
        KEY_ID.FORWARD_BUTTON: KosmosIO.BUTTONS.BUTTON_4,
    }

    #
    OPTICAL_KEYS = {
        KEY_ID.LEFT_BUTTON: KosmosIO.BUTTONS.BUTTON_5,
        KEY_ID.RIGHT_BUTTON: KosmosIO.BUTTONS.BUTTON_6,
    }
# end class Bazooka2Layout


class Footloose2Layout(MouseLayoutInterface):
    """
    Configure the button layout of the Footloose2 mouse.

    Notes: Hybrid hardware,
           Left Button,
           Right Buttons,
    """
    KEYS = {
        KEY_ID.LEFT_BUTTON:  KosmosIO.BUTTONS.BUTTON_0,
        KEY_ID.RIGHT_BUTTON: KosmosIO.BUTTONS.BUTTON_1,
        KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,
        KEY_ID.FORWARD_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
        KEY_ID.BACK_BUTTON: KosmosIO.BUTTONS.BUTTON_4,
        # KEY_ID.FORWARD_BUTTON: KosmosIO.BUTTONS.BUTTON_5,
        # KEY_ID.BACK_BUTTON: KosmosIO.BUTTONS.BUTTON_6,
        # (The default function of side buttons left and right on Footloose2 both are FORWARD and BACKWARD)
        KEY_ID.DPI_CYCLING_BUTTON: KosmosIO.BUTTONS.BUTTON_7,
    }
# end class Footloose2Layout


class LetiLayout(MouseLayoutInterface):
    """
    Configure the button layout of my LETI device with DPI switch replacing the SmartShift button
    """
    KEYS = CoreMouseLayout.KEYS.copy()
    del (KEYS[KEY_ID.SMART_SHIFT])
    KEYS[KEY_ID.DPI_SWITCH] = KosmosIO.BUTTONS.BUTTON_4
# end class LetiLayout


class HadronDevBoardLayout(MouseLayoutInterface):
    """
    Configure the button layout of the Hadron DEV board
    """
    KEYS = {
        KEY_ID.LEFT_BUTTON: KosmosIO.BUTTONS.BUTTON_0,
        KEY_ID.RIGHT_BUTTON: KosmosIO.BUTTONS.BUTTON_1,
        KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,
        KEY_ID.CONNECT_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
    }
# end class HadronDevBoardLayout


class BardiMouseLayout(HadronDevBoardLayout):
    """
    Configure the button layout of the Bardi Mouse
    """
# end class BardiMouseLayout


class TurbotMouseLayout(HadronDevBoardLayout):
    """
    Configure the button layout of the Turbot BLE Pro mouse
    """
# end class TurbotMouseLayout


class LizaMouseLayout(HadronDevBoardLayout):
    """
    Configure the button layout of the Liza mouse
    """
# end class LizaMouseLayout


class CardeaRefreshButtonLayout(CoreMouseLayout):
    """
    Configure the button layout of the Cardea Refresh mouse
    """
    KEYS = {
        KEY_ID.LEFT_BUTTON: KosmosIO.BUTTONS.BUTTON_0,
        KEY_ID.RIGHT_BUTTON: KosmosIO.BUTTONS.BUTTON_1,
        KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,
        KEY_ID.CONNECT_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
        KEY_ID.DPI_SWITCH: KosmosIO.BUTTONS.BUTTON_4,
    }
# end class CardeaRefreshButtonLayout


class TigerMiniDevBoardLayout(CoreMouseLayout):
    """
    Configure the button layout of the Tiger Mini Dev Board
    """
    HAS_HYBRID_SWITCH = True
    KEYS = {
        KEY_ID.LEFT_BUTTON: (KosmosIO.BUTTONS.BUTTON_0, KosmosIO.SLIDERS.SLIDER_1),  # (galvanic, optical) switches
        KEY_ID.RIGHT_BUTTON: (KosmosIO.BUTTONS.BUTTON_1, KosmosIO.SLIDERS.SLIDER_2),  # (galvanic, optical) switches
        KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,
        KEY_ID.BACK_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
        KEY_ID.FORWARD_BUTTON: KosmosIO.BUTTONS.BUTTON_4,
    }

    #
    OPTICAL_KEYS = {
        KEY_ID.LEFT_BUTTON: KosmosIO.SLIDERS.SLIDER_1,
        KEY_ID.RIGHT_BUTTON: KosmosIO.SLIDERS.SLIDER_2,
    }
# end class TigerMiniDevBoardLayout


class CanovaLayout(MouseLayoutInterface):
    """
    Configure the button layout of the Canova square board
    """
    KEYS = {
        KEY_ID.LEFT_BUTTON: KosmosIO.BUTTONS.BUTTON_0,
        KEY_ID.RIGHT_BUTTON: KosmosIO.BUTTONS.BUTTON_1,
        KEY_ID.MIDDLE_BUTTON: KosmosIO.BUTTONS.BUTTON_2,
        KEY_ID.CONNECT_BUTTON: KosmosIO.BUTTONS.BUTTON_3,
        KEY_ID.SMART_SHIFT: KosmosIO.BUTTONS.BUTTON_4,
        KEY_ID.FORWARD_BUTTON: KosmosIO.BUTTONS.BUTTON_5,
        KEY_ID.BACK_BUTTON: KosmosIO.BUTTONS.BUTTON_6,
        KEY_ID.VIRTUAL_GESTURE_BUTTON: KosmosIO.BUTTONS.BUTTON_7,
    }
# end class CanovaLayout


BUTTON_LAYOUT_BY_ID = {
    'AVA02': TurbotMouseLayout,
    'HAD01': HadronDevBoardLayout,
    'MPM25': BazookaLayout,
    'MPM28': CoreMouseLayout,
    'MPM31': Footloose2Layout,
    'MPM32': Bazooka2Layout,
    'RBM21': LetiLayout,
    'RBM22': LizaMouseLayout,
    'RBM23': TurbotMouseLayout,
    'RBM24': BardiMouseLayout,
    'RBM26': CardeaRefreshButtonLayout,
    'RBM27': CanovaLayout,
    'TIG01': TigerMiniDevBoardLayout,
}

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
