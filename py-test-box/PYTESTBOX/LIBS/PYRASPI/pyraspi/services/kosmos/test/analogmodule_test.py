#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.analogmodule_test
:brief: Kosmos Analog Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/10/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from math import ceil
from time import sleep

from pyraspi.services.kosmos.analogmodule import AnalogModule
from pyraspi.services.kosmos.module.cmods6 import Cmods6
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AnalogModuleTestCase(KosmosCommonTestCase):
    """
    Kosmos Analog Module Test Class
    """
    @classmethod
    def setUpClass(cls):
        """
        Setup Kosmos and Analog module
        """
        super().setUpClass()
        cls._analog = AnalogModule(kosmos=cls.kosmos)
    # end def setUpClass

    def tearDown(self):
        """
        TearDown: Reset Analog Module state after each tests
        """
        self._analog.reset()
        self._analog.init()

        super().tearDown()
    # end def tearDown

    def test_output_voltage_ramp_up(self):
        """
        Implement a DAC voltage ramp up
        """
        voltage_ramp = [i / 10 for i in range(ceil(self._analog.VOLTAGE_LIMIT[Cmods6.CHANNEL.BATTERY] * 10))] \
            + [self._analog.VOLTAGE_LIMIT[Cmods6.CHANNEL.BATTERY]]

        # Actuate relay to connect output
        self._analog.turn_on()

        # Set USB DAC channel A (Output Voltage)
        for dac_volt in voltage_ramp:
            self._analog.set_voltage(dac_volt)
        # end for

        #######################################
        # Measure output voltage manually with a voltmeter, expect VOLTAGE_LIMIT[Cmods6.CHANNEL.BATTERY] volts
        sleep(10)
        #######################################
    # end def test_output_voltage_ramp_up
# end class AnalogModuleTestCase
