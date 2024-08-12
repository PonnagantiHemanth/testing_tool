#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.sliderlayout
:brief: Kosmos Slider configuration per product
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/29
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from typing import Dict

from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.kosmos.kosmosio import KosmosIO


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PowerSliderLayoutInterface(metaclass=ABCMeta):
    """
    Device power slider layout Interface Class
    """
    KEYS: Dict[KEY_ID, KosmosIO.SLIDERS]
# end class PowerSliderLayoutInterface


class PowerSliderLayout(PowerSliderLayoutInterface):
    """
    Configure the slider layout with only the power slider on position 0
    """
    KEYS = {
        KEY_ID.POWER: KosmosIO.SLIDERS.SLIDER_0
    }
# end class PowerSliderLayout


class BostonPowerSliderLayout(PowerSliderLayoutInterface):
    """
    Configure the slider layout with two power sliders on position 0 and 1
    """
    KEYS = {
        KEY_ID.POWER: (KosmosIO.SLIDERS.SLIDER_0, KosmosIO.SLIDERS.SLIDER_1)  # DPDT switch
    }
# end class BostonPowerSliderLayout


SLIDER_LAYOUT_BY_ID = {
    'AVA02': PowerSliderLayout,
    'HAD01': PowerSliderLayout,
    'HAD02': PowerSliderLayout,
    'MPK17': PowerSliderLayout,
    'MPK20': PowerSliderLayout,
    'MPK25': PowerSliderLayout,
    'MPM15': PowerSliderLayout,
    'MPM25': PowerSliderLayout,
    'MPM28': PowerSliderLayout,
    'MPM31': PowerSliderLayout,
    'MPM32': PowerSliderLayout,
    'RBK68': PowerSliderLayout,
    'RBK69': PowerSliderLayout,
    'RBK70': PowerSliderLayout,
    'RBK71': PowerSliderLayout,
    'RBK72': PowerSliderLayout,
    'RBK75': PowerSliderLayout,
    'RBK81': PowerSliderLayout,
    'RBK90': PowerSliderLayout,
    'RBK91': BostonPowerSliderLayout,
    'RBK92': PowerSliderLayout,
    'RBK93': PowerSliderLayout,
    'RBK94': PowerSliderLayout,
    'RBK95': PowerSliderLayout,
    'RBK96': BostonPowerSliderLayout,
    'RBM21': PowerSliderLayout,
    'RBM22': PowerSliderLayout,
    'RBM23': PowerSliderLayout,
    'RBM24': PowerSliderLayout,
    'RBM26': PowerSliderLayout,
    'RBM27': PowerSliderLayout,
    'RBO03': PowerSliderLayout,
    # 'U170': PowerSliderLayout,    # Slider is not needed as we can switch power via USB HUB
}


class ProximitySliderLayoutInterface(metaclass=ABCMeta):
    """
    Device proximity slider layout Interface Class
    """
    SLIDER_ID: KosmosIO.SLIDERS
# end class ProximitySliderLayoutInterface


class ProximitySliderLayout(ProximitySliderLayoutInterface):
    """
    Configure the proximity sensor as a slider. Using only the slider on position 1
    """
    SLIDER_ID = KosmosIO.SLIDERS.SLIDER_1
# end class ProximitySliderLayout


PROXIMITY_SENSOR_LAYOUT_BY_ID = {
    'RBK71': ProximitySliderLayout,
    'RBK75': ProximitySliderLayout,
    'RBK81': ProximitySliderLayout,
}
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
