#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pytransport.tools.test.agilenttest
    :brief: Agilent Power Supply Control Class
    :author: Fred Chen <fchen7@logitech.com>
    :date: 2019/6/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep
from unittest import skipIf
from unittest import TestCase

from pytransport.tools.agilent import Agilent


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@skipIf(Agilent.discover_agilent() is False, 'Agilent power supply unit not found')
class AgilentTestCase(TestCase):
    """
    Test Agilent Power Supply Class
    """

    def test_can_open_serial_device(self):
        """
        Test can open serial device or not
        """
        serial_device = Agilent.get_instance()
        self.assertNotEqual(serial_device, None)
    # end def test_can_open_serial_device

    def test_can_get_controller(self):
        """
        Test can get controller or not
        """
        agilent = Agilent.get_instance()
        self.assertNotEqual(agilent, None)
        self.assertNotEqual(agilent.read_id(), None, 'Cannot contact to Agilent Power Supply!')
    # end def test_can_get_controller

    def test_can_set_voltage(self):
        """
        Test can set voltage or not
        """
        agilent = Agilent.get_instance()
        self.assertNotEqual(agilent, None)
        v = agilent.read_voltage()
        self.assertNotEqual(v, None)
        self.assertEqual(agilent.set_voltage(1.724), 1.724)
        sleep(2)
        self.assertEqual(agilent.set_voltage(v), v)
    # end def test_can_set_voltage

    def test_can_read_current(self):
        """
        Test can read current or not
        """
        agilent = Agilent.get_instance()
        self.assertNotEqual(agilent, None)
        agilent.output_voltage('on')
        self.assertNotEqual(agilent.read_current(), None)
    # end def test_can_read_current

    def test_can_set_current(self):
        """
        Test can set current or not
        """
        agilent = Agilent.get_instance()
        self.assertNotEqual(agilent, None)
        agilent.output_voltage('on')
        max_curr = agilent.get_max_current()
        self.assertNotEqual(agilent.set_current(max_curr), None)
    # end def test_can_set_current
# end class AgilentTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
