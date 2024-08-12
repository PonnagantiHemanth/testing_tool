#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.pio_test
:brief: Tests for Kosmos PIO Module Class
:author: Alexandre Lafaye <alafaye@logitech.com>
:date: 2022/10/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from sys import stdout

from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.pio import PIO_COUNT
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.test.keymatrixemulator_test import KBD_FW_ID
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@require_kosmos_device(DeviceName.PIO)
class KosmosPioTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos Pio class
    """
    _slider_emulator: KosmosPowerSliderEmulator

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos
        """
        super().setUpClass()
        cls._slider_emulator = KosmosPowerSliderEmulator(kosmos=cls.kosmos, fw_id=KBD_FW_ID)
        cls._slider_emulator.power_on()
    # end def setUpClass

    @classmethod
    def tearDownClass(cls):
        """
        Open Kosmos
        """
        cls._slider_emulator.power_off()
        super().tearDownClass()
    # end def tearDownClass

    def test_read_one(self):
        """
        Validate reading from the Kosmos PIO pins one by one
        """
        states = [(self.kosmos.pio.read_pio(x)) for x in range(PIO_COUNT)]
        self.assertEqual(first=PIO_COUNT, second=len(states), msg=states)
        stdout.write(f'Kosmos PIO module read PIO states = {states}')
    # end def test_read_one

    def test_read_all(self):
        """
        Validate reading all the Kosmos PIO pins
        """
        print(self.kosmos.pio.read_all())
    # end def test_read_all
# end class KosmosPioTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
