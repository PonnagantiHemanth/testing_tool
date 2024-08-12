#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.dac_test
:brief: Kosmos DAC Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase

from math import ceil

from pyraspi.services.kosmos.module.dac import Dac


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DacTestCase(TestCase):
    """
    Kosmos Dac Module Test Class
    """

    VOLTAGES_RANGE = [i / 10 for i in range(ceil(Dac.MAX_VOLTAGE * 10))] + [Dac.MAX_VOLTAGE]

    def test_constants(self):
        """
        Validate constants have the expected values.
        """
        self.assertEqual(16, Dac.DAC_RESOLUTION, f'LTC2654-H is a 16-bit DAC')
        self.assertEqual(0xFFFF, Dac.DAC_MAX_VALUE, f'LTC2654-H is a 16-bit DAC')
        self.assertEqual(4.096, Dac.DAC_OUTPUT_FULL_SCALE,
                         f'The LTC2654-H DAC has a 2.048V reference that provides a full-scale output of 4.096V')
        self.assertEqual(2, Dac.OUTPUT_OPAMP_GAIN, f'The external op-amp LT1970 has a 2x gain')
        self.assertEqual(8.191875, Dac.MAX_VOLTAGE, f'DAC_VOLT = Gain * Vref * DAC_VALUE / 2^n')

    # end def test_constants

    def test_volt_to_dac_value(self):
        """
        Validate ``volt_to_dac_value()`` method.
        """
        self.assertEqual(0x0000, Dac.volt_to_dac_value(0))
        self.assertEqual(0x1F40, Dac.volt_to_dac_value(1))
        self.assertEqual(0xFFFF, Dac.volt_to_dac_value(8.191875))

        self.assertRaises(ValueError, Dac.volt_to_dac_value, -0.1)  # Out of range
        self.assertRaises(ValueError, Dac.volt_to_dac_value, 8.2)  # Out of range

    # end def test_volt_to_dac_value

    def test_dac_value_to_volt(self):
        """
        Validate ``dac_value_to_volt()`` method.
        """
        self.assertEqual(0, Dac.dac_value_to_volt(0x0000))
        self.assertEqual(1, Dac.dac_value_to_volt(0x1F40))
        self.assertEqual(8.191875, Dac.dac_value_to_volt(0xFFFF))

        self.assertRaises(ValueError, Dac.dac_value_to_volt, -1)  # Out of range
        self.assertRaises(ValueError, Dac.dac_value_to_volt, 0x10000)  # Out of range
        self.assertRaises(TypeError, Dac.dac_value_to_volt, -1.5)  # Not an integer value
        self.assertRaises(TypeError, Dac.dac_value_to_volt, 1.5)  # Not an integer value
        self.assertRaises(TypeError, Dac.dac_value_to_volt, '1')  # wrong type
        self.assertEqual(8.191875, Dac.dac_value_to_volt(65535.0))  # OK: float type with integer value

    # end def test_dac_value_to_volt

    def test_dac_conversions(self):
        """
        Validate both ``volt_to_dac_value()`` and ``dac_value_to_volt()`` methods.

        Validate DAC conversion operations are commutative.
        """
        self.assertEqual(0, Dac.volt_to_dac_value(Dac.dac_value_to_volt(0)))
        self.assertEqual(1, Dac.volt_to_dac_value(Dac.dac_value_to_volt(1)))
        self.assertEqual(0xFFFF, Dac.volt_to_dac_value(Dac.dac_value_to_volt(0xFFFF)))

        self.assertEqual(0, Dac.dac_value_to_volt(Dac.volt_to_dac_value(0)))
        self.assertEqual(1, Dac.dac_value_to_volt(Dac.volt_to_dac_value(1)))
        self.assertEqual(8.191875, Dac.dac_value_to_volt(Dac.volt_to_dac_value(8.191875)))

        for dac_value in range(0x10000):
            self.assertEqual(dac_value, Dac.volt_to_dac_value(Dac.dac_value_to_volt(dac_value)),
                             msg=dac_value)
        # end for

        for dac_volt in self.VOLTAGES_RANGE:
            self.assertAlmostEqual(dac_volt, Dac.dac_value_to_volt(Dac.volt_to_dac_value(dac_volt)),
                                   msg=dac_volt, delta=1 / (1 << 16))  # delta set to ~15 micro volt
        # end for
    # end def test_dac_conversions
# end class DacTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
