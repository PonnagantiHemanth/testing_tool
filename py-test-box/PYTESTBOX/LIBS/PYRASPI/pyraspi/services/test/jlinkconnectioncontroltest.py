#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.test.ioswitchtest
:brief: Tests for Raspi jlinkconnectioncontrol Class
:author: Fred Chen <fchen7@logitech.com>
:date: 2020/1/9
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase
from unittest import skipIf
from time import sleep
import sys
if sys.platform == 'linux':
    from pyraspi.services.daemon import Daemon
    from pyraspi.raspi import Raspi
    from pyraspi.services.jlinkconnectioncontrol import PowerSupplyBoardJlinkConnectionControl
    import RPi.GPIO as GPIO
# end if


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@skipIf(sys.platform != 'linux', 'Support test on Raspi only!')
@skipIf(Daemon.is_host_kosmos(),
        'Support test on Raspberry Pi NOT configured for KOSMOS project (legacy test environment)!')
class LegacyJlinkConnectionControlTestCase(TestCase):
    """
    Test PowerSupplyBoardJlinkConnectionControl Class
    """

    def test_LegacyJlinkConnectionControl(self):
        """
        Validate the GPIO on/off control
        """
        io_switch = PowerSupplyBoardJlinkConnectionControl(control_pin=Raspi.PIN.JLINK_IO_SWITCH)
        io_switch.disconnect()
        self.assertEqual(GPIO.input(io_switch.control_pin), False)
        sleep(1)
        io_switch.connect()
        self.assertEqual(GPIO.input(io_switch.control_pin), True)
    # end def test_LegacyJlinkConnectionControl
# end class LegacyJlinkConnectionControlTestCase


# TODO add tests for KosmosJlinkConnectionControl


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
