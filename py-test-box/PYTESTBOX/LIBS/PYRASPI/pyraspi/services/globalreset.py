#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.globalreset
:brief: Fpga Global Reset Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/05/08
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from typing import Callable
from time import sleep

from RPi import GPIO

from pyraspi.raspi import Raspi


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
# noinspection PyUnusedLocal
def _dummy_callback(gpio):
    """
    Method called by the ``GPIO.add_event_detect()`` function when the Global Error signal is triggered by the PI.
    Note that it's a temporary workaround on raspberry PI 5 as an event occurred
    when re-enabling the detection after the reset.

    :param gpio: GPIO pin
    :type gpio: ``int``
    """
    pass
# end def _dummy_callback


class GlobalReset:
    """
    Define some methods to control the FPGA Global Reset pin.
    """

    @classmethod
    def raise_global_error_flag(cls, callback):
        """
        Send a low pulse on the Global Error signal going from the RaspberryPi to the FPGA.

        The low-pulse duration has been measured to last between 2 and 4 us.
        Beware that the RaspberryPi Linux OS is not real-time, so the actual pulse duration may be longer.

        :param callback: Method called by the ``GPIO.add_event_detect()`` function, triggered by the Global Error signal
        :type callback: ``Callable``
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        cls.gpio_setup_global_error_signal(callback=callback, as_input=False)
        GPIO.output(Raspi.PIN.GLOBAL_ERROR, GPIO.LOW)
        GPIO.output(Raspi.PIN.GLOBAL_ERROR, GPIO.HIGH)
        if Raspi.is_raspberry_pi_5():
            # Note that it's a temporary workaround on raspberry PI 5 as an event occurred
            # when re-enabling the detection after the reset.
            cls.gpio_setup_global_error_signal(callback=_dummy_callback)
            counter = 0
            while not GPIO.event_detected(Raspi.PIN.GLOBAL_ERROR) and counter < 10:
                sleep(.001)
                counter += 1
            # end while
        # end if
        cls.cleanup_global_error_line()
    # end def raise_global_error_flag

    @staticmethod
    def gpio_setup_global_error_signal(callback, as_input=True):
        """
        Set up the Global Error GPIO pin.

        The Global Error line is bidirectional. By default, both RPi and FPGA as configured as input with pull-ups.
        Whenever the RPi or the FPGA wants to signal an Error, its input is temporarily reconfigured as push-pull output

        :param callback: Method called by the ``GPIO.add_event_detect()`` function, triggered by the Global Error signal
        :type callback: ``Callable``
        :param as_input: Set `True` to configure the Global Error GPIO as Input (default: FPGA signals RPi).
                         Set `False` to configure the GPIO as Output (RPi signals FPGA) - OPTIONAL
        :type as_input: ``bool``
        """
        GPIO.remove_event_detect(Raspi.PIN.GLOBAL_ERROR)
        if as_input:
            GPIO.setup(Raspi.PIN.GLOBAL_ERROR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(Raspi.PIN.GLOBAL_ERROR, GPIO.FALLING, callback=callback, bouncetime=2)
        else:
            GPIO.setup(Raspi.PIN.GLOBAL_ERROR, GPIO.OUT, initial=GPIO.HIGH)
        # end if
    # end def gpio_setup_global_error_signal

    @staticmethod
    def cleanup_global_error_line():
        """
        Free the global error flag GPIO
        """
        GPIO.cleanup(Raspi.PIN.GLOBAL_ERROR)
    # end def cleanup_global_error_line

# end class GlobalReset

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
