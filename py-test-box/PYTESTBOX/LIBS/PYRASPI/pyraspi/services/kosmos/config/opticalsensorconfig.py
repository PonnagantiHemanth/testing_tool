#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.opticalsensorconfig
:brief: Kosmos optical sensor configuration per product
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/03/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from enum import IntEnum
from enum import IntFlag
from enum import auto
from enum import unique
from typing import Dict


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@unique
class DIRECTION(IntEnum):
    """
    Motion direction, expressed in the Mouse XY reference frame
    """
    X = auto()
    Y = auto()
# end class DIRECTION


@unique
class ORIENTATION(IntFlag):
    """
    Sensor orientation, expressed in the Sensor XY reference frame
    """
    X = auto()
    Y = auto()
    INVERSE = auto()
# end class ORIENTATION


class MouseLayoutInterface(metaclass=ABCMeta):
    """
    Device optical sensor orientation configuration Interface Class.

    DIRECTION: Mouse XY reference frame
    ORIENTATION: Sensor XY reference frame
    """
    MOTION: Dict[DIRECTION, ORIENTATION]

    DUT_VCC_SENSOR_VOLTAGE: float
# end class MouseLayoutInterface


class NormalMouseLayout(MouseLayoutInterface):
    """
    Configure the sensor orientation and the Vcc sensor of the device.

    DIRECTION: Mouse XY reference frame
    ORIENTATION: Sensor XY reference frame
    """
    MOTION = {
        DIRECTION.X: ORIENTATION.X,
        DIRECTION.Y: ORIENTATION.Y,
    }
    DUT_VCC_SENSOR_VOLTAGE = 2.0
# end class NormalMouseLayout


class HeroLayout(MouseLayoutInterface):
    """
    Configure the sensor orientation of Hero sensor.

    DIRECTION: Mouse XY reference frame
    ORIENTATION: Sensor XY reference frame
    """
    MOTION = {
        DIRECTION.X: ORIENTATION.Y,
        DIRECTION.Y: ORIENTATION.X | ORIENTATION.INVERSE,
    }
    DUT_VCC_SENSOR_VOLTAGE = 2.0
# end class HeroLayout


class Hero2Layout(HeroLayout):
    """
    Configure the sensor orientation of Hero2 sensor.
    """
# end class Hero2Layout


class Footloose2Layout(HeroLayout):
    """
    Configure the sensor orientation of the Footloose2 mouse.
    """
# end class Footloose2Layout


class CanovaSquareLayout(MouseLayoutInterface):
    """
    Configure the sensor orientation on the NPI PCB.

    NB: it's not compatible with the Canova Square board which has the following config:
        DIRECTION.X: ORIENTATION.X | ORIENTATION.INVERSE,
        DIRECTION.Y: ORIENTATION.Y | ORIENTATION.INVERSE,

    DIRECTION: Mouse XY reference frame
    ORIENTATION: Sensor XY reference frame
    """
    MOTION = {
        DIRECTION.X: ORIENTATION.X,
        DIRECTION.Y: ORIENTATION.Y,
    }
    DUT_VCC_SENSOR_VOLTAGE = 2.4
# end class CanovaSquareLayout


SENSOR_ORIENTATION_BY_ID = {
    'AVA02': NormalMouseLayout,
    'HAD01': HeroLayout,
    'HAD02': HeroLayout,
    'MPM25': HeroLayout,
    'MPM31': Footloose2Layout,
    'MPM32': Hero2Layout,
    'RBM22': NormalMouseLayout,
    'RBM23': NormalMouseLayout,
    'RBM27': CanovaSquareLayout,
    'TIG01': Hero2Layout,
}

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
