#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package    pyraspi.services.powersupply
:brief      Tests for power supply class
:author     fred.chen
:date       2020/01/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase, skipIf
from time import sleep
import sys
if sys.platform == 'linux':
    from pyraspi.services.daemon import Daemon
    from pyraspi.services.powersupply import MCP4725PowerSupplyEmulationInterface
# end if

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


@skipIf(sys.platform != 'linux', 'Support test on Raspi only!')
@skipIf(Daemon.is_host_kosmos(),
        'Support test on Raspberry Pi NOT configured for KOSMOS project (legacy test environment)!')
class MCP4725TestCase(TestCase):
    """
    Integration Test for Power Supply (MCP4725 and INA226)
    """

    R_SHUNT = 0.5

    def setUp(self):
        """
        Prerequisites setup
        """
        super(MCP4725TestCase, self).setUp()
        self.power_supply = MCP4725PowerSupplyEmulationInterface.get_instance(starting_voltage=3.8)
    # end def setUp

    def tearDown(self):
        """
        Post-requisite tear-down
        """
        if self.power_supply is not None:
            self.power_supply.__del__()
        # end if
        super(MCP4725TestCase, self).tearDown()
    # end def tearDown

    def test_MCP4725Set3_8V(self):
        """
        Set voltage to 3.8V
        Internal check without voltage output
        """
        assert self.power_supply is not None
        self.power_supply.set_raw_voltage(v=0)
        count = 0
        while (self.power_supply.read_voltage() * 1000) > 500:
            sleep(.1)
            count += 1
            self.assertLessEqual(a=count, b=100, msg='wait voltage dropping timeout (10s)')
        # end while
        self.power_supply.set_raw_voltage(v=3.8)
        sleep(.55)
        self.assertGreaterEqual(self.power_supply.read_voltage(digits=2), 3.75)
        self.assertLessEqual(self.power_supply.read_voltage(digits=2), 3.85)
    # end def test_MCP4725Set3_8V

    def test_MCP4725SetHighToLow(self):
        """
        Change voltage from 4.2V to 0.7V repeatedly
        Internal check without voltage output
        """
        assert self.power_supply is not None
        self.power_supply.set_raw_voltage(v=0)
        count = 0
        while (self.power_supply.read_voltage() * 1000) > 10:
            sleep(.1)
            count += 1
            self.assertLessEqual(a=count, b=100, msg='wait voltage dropping timeout (10s)')
        # end while
        for _ in range(30):
            self.power_supply.set_raw_voltage(v=0)
            # Need more time to drop voltage from high to low
            sleep(0.45)
            self.assertGreaterEqual(self.power_supply.read_voltage(digits=1), 0.0)
            self.assertLessEqual(self.power_supply.read_voltage(digits=1), 0.1)
            self.power_supply.set_raw_voltage(v=4.2)
            sleep(0.03)
            self.assertGreaterEqual(self.power_supply.read_voltage(digits=2), 4.15)
            self.assertLessEqual(self.power_supply.read_voltage(digits=2), 4.25)
        # end for
    # end def test_MCP4725SetHighToLow

# end class MCP4725TestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
