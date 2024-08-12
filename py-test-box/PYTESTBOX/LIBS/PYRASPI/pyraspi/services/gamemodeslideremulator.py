#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.gamemodeslideremulator
:brief: Game Mode Slider Emulator Class
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pylibrary.emulator.emulatorinterfaces import GameModeEmulationInterface
from pyraspi.raspi import Raspi
from pyraspi.services.daemon import Daemon

if Raspi.is_host_raspberry_pi():
    import RPi.GPIO as GPIO
# end if


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GameModeSliderEmulator(GameModeEmulationInterface):
    """
    Game Mode Slider emulator, directly controlled by the Raspberry Pi GPIOs.

    Upon class instantiation, turn on Game Mode Slider switch.
    """
    def __init__(self):
        """
        :raise ``AssertionError``: If Raspberry Pi host is incompatible with this class
        """
        # GPIO can be setup only if host is a RaspberryPi, but not configured for Kosmos project
        assert Raspi.is_host_raspberry_pi() and not Daemon.is_host_kosmos(),\
            f'GPIO can be setup only if host is a RaspberryPi, but not configured for Kosmos project.'

        self.state = None

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(Raspi.PIN.GAME_MODE_SLIDER, GPIO.OUT, initial=GPIO.HIGH)
        self.set_mode()
    # end def __init__

    def __del__(self):
        """
        Cleanup GPIO
        """
        if Raspi.is_host_raspberry_pi() and not Daemon.is_host_kosmos():
            GPIO.cleanup(Raspi.PIN.GAME_MODE_SLIDER)
        # end if
    # end def __del__

    def get_state(self):
        # See ``GameModeEmulationInterface.get_state``
        return self.state
    # end def get_state

    def set_mode(self, activate_game_mode=False):
        # See ``GameModeEmulationInterface.set_mode``
        if not activate_game_mode:
            gpio_level = GPIO.HIGH
            self.state = GameModeEmulationInterface.MODE.DISABLED
        else:
            gpio_level = GPIO.LOW
            self.state = GameModeEmulationInterface.MODE.ENABLED
        # end if

        GPIO.output(Raspi.PIN.GAME_MODE_SLIDER, gpio_level)
        count = 0
        while GPIO.input(Raspi.PIN.GAME_MODE_SLIDER) != gpio_level and count < 10:
            count += 1
            sleep(1e-4)
        # end while
        sleep(.05)
    # end def set_mode
# end class GameModeSliderEmulator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
