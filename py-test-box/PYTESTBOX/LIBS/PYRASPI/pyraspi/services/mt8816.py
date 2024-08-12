#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package:   pyraspi.services.mt8816
:brief:     MT8816 control library
:author:    Fred Chen
:date:      2021/02/01
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum, unique, auto
from sys import platform
from threading import Lock
from time import sleep

from pylibrary.tools.threadutils import synchronized
from pyraspi.raspi import is_kosmos_setup
from pyraspi.raspi import Raspi

if platform == 'linux':
    import RPi.GPIO as GPIO
# end if


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
MT8816_LOCK = Lock()

if not is_kosmos_setup():
    class CHIP:
        """
        Chip Select
        """
        CS0 = Raspi.PIN.MT8816_CS_0
        CS1 = Raspi.PIN.MT8816_CS_1
        CS2 = Raspi.PIN.MT8816_CS_2
    # end class CHIP
else:
    @unique
    class CHIP(IntEnum):
        """
        Chip Select
        """
        CS0 = auto()
        CS1 = auto()
        CS2 = auto()
    # end class CHIP
# end if


class MT8816:
    """
    MT8816 Analog Switch Array Control Library
    """

    class INTERSECTION:
        """
        The DATA to set the intersection state of X and Y
        """
        OFF = 0
        ON = 1
    # end class INTERSECTION

    class ADDRESS:
        """
        Refer to MT8816 datasheet Table 1. Address Decode Truth Table
        """
        X0 = [0, 0, 0, 0]
        X1 = [1, 0, 0, 0]
        X2 = [0, 1, 0, 0]
        X3 = [1, 1, 0, 0]
        X4 = [0, 0, 1, 0]
        X5 = [1, 0, 1, 0]
        X6 = [0, 0, 0, 1]
        X7 = [1, 0, 0, 1]
        X8 = [0, 1, 0, 1]
        X9 = [1, 1, 0, 1]
        X10 = [0, 0, 1, 1]
        X11 = [1, 0, 1, 1]
        X12 = [0, 1, 1, 0]
        X13 = [1, 1, 1, 0]
        X14 = [0, 1, 1, 1]
        X15 = [1, 1, 1, 1]

        Y0 = [CHIP.CS0, [0, 0, 0]]
        Y1 = [CHIP.CS0, [1, 0, 0]]
        Y2 = [CHIP.CS0, [0, 1, 0]]
        Y3 = [CHIP.CS0, [1, 1, 0]]
        Y4 = [CHIP.CS0, [0, 0, 1]]
        Y5 = [CHIP.CS0, [1, 0, 1]]
        Y6 = [CHIP.CS0, [0, 1, 1]]
        Y7 = [CHIP.CS0, [1, 1, 1]]
        Y8 = [CHIP.CS1, [0, 0, 0]]
        Y9 = [CHIP.CS1, [1, 0, 0]]
        Y10 = [CHIP.CS1, [0, 1, 0]]
        Y11 = [CHIP.CS1, [1, 1, 0]]
        Y12 = [CHIP.CS1, [0, 0, 1]]
        Y13 = [CHIP.CS1, [1, 0, 1]]
        Y14 = [CHIP.CS1, [0, 1, 1]]
        Y15 = [CHIP.CS1, [1, 1, 1]]
        Y16 = [CHIP.CS2, [0, 0, 0]]
        Y17 = [CHIP.CS2, [1, 0, 0]]
        Y18 = [CHIP.CS2, [0, 1, 0]]
        Y19 = [CHIP.CS2, [1, 1, 0]]
        Y20 = [CHIP.CS2, [0, 0, 1]]
        Y21 = [CHIP.CS2, [1, 0, 1]]
        Y22 = [CHIP.CS2, [0, 1, 1]]
        Y23 = [CHIP.CS2, [1, 1, 1]]
    # end class ADDRESS

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(Raspi.PIN.MT8816_CS_0, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_CS_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_CS_2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_STROBE, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_DATA_0, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_DATA_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_DATA_2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_RESET, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_AX_0, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_AX_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_AX_2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_AX_3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_AY_0, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_AY_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.MT8816_AY_2, GPIO.OUT, initial=GPIO.LOW)
        self.reset()
    # end def __init__

    @synchronized(MT8816_LOCK)
    def reset(self):
        """
        Reset all memory locations to logical 0
        """
        GPIO.output(Raspi.PIN.MT8816_CS_0, GPIO.LOW)
        GPIO.output(Raspi.PIN.MT8816_CS_1, GPIO.LOW)
        GPIO.output(Raspi.PIN.MT8816_CS_2, GPIO.LOW)
        GPIO.output(Raspi.PIN.MT8816_STROBE, GPIO.LOW)
        GPIO.output(Raspi.PIN.MT8816_DATA_0, GPIO.LOW)
        GPIO.output(Raspi.PIN.MT8816_DATA_1, GPIO.LOW)
        GPIO.output(Raspi.PIN.MT8816_DATA_2, GPIO.LOW)
        GPIO.output(Raspi.PIN.MT8816_RESET, GPIO.HIGH)
        sleep(.0001)
        GPIO.output(Raspi.PIN.MT8816_RESET, GPIO.LOW)
        sleep(.001)
    # end def reset

    @synchronized(MT8816_LOCK)
    def set_address(self, cs_pin, data_pin, x, y, state):
        """
        Set a specific address to INTERSECTION ON or OFF

        :param cs_pin: The rpi GPIO pin be connected to matrix control board chip selection pin
        :type cs_pin: ``Raspi.PIN``
        :param data_pin: The rpi GPIO pin be connected to matrix control board DATA pin
        :type data_pin: ``Raspi.PIN``
        :param x: The address of X
        :type x: ``MT8816.Address``
        :param y: The address of Y
        :type y: ``MT8816.Address``
        :param state: The intersection state of x and y
        :type state: ``MT8816.INTERSECTION``
        """
        GPIO.output(Raspi.PIN.MT8816_AX_0, x[0])
        GPIO.output(Raspi.PIN.MT8816_AX_1, x[1])
        GPIO.output(Raspi.PIN.MT8816_AX_2, x[2])
        GPIO.output(Raspi.PIN.MT8816_AX_3, x[3])
        GPIO.output(Raspi.PIN.MT8816_AY_0, y[0])
        GPIO.output(Raspi.PIN.MT8816_AY_1, y[1])
        GPIO.output(Raspi.PIN.MT8816_AY_2, y[2])
        sleep(.0001)
        GPIO.output(cs_pin, GPIO.HIGH)
        sleep(.00001)
        GPIO.output(Raspi.PIN.MT8816_STROBE, GPIO.HIGH)
        sleep(.0001)
        GPIO.output(data_pin, state)
        sleep(.0001)
        GPIO.output(Raspi.PIN.MT8816_STROBE, GPIO.LOW)
        GPIO.output(cs_pin, GPIO.LOW)
    # end def set_address

    def get_data_pin(self, cs_pin):
        """
        Return the data pin that maps to the specific cs pin.

        :param cs_pin: The rpi GPIO pin be connected to matrix control board chip selection pin
        :type cs_pin: ``Raspi.PIN``

        :return: The rpi GPIO pin that be connected to matrix control board DATA pin
        :rtype: ``Raspi.PIN``
        """
        if cs_pin == Raspi.PIN.MT8816_CS_0:
            return Raspi.PIN.MT8816_DATA_0
        elif cs_pin == Raspi.PIN.MT8816_CS_1:
            return Raspi.PIN.MT8816_DATA_1
        elif cs_pin == Raspi.PIN.MT8816_CS_2:
            return Raspi.PIN.MT8816_DATA_2
        else:
            raise ValueError
        # end if
    # end def get_data_pin

# end class MT8816

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
