#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.slideremulator_test
:brief: Tests for Kosmos Button & Slider Controller
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/29
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.services.kosmos.kosmosio import KosmosIO
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@require_kosmos_device(DeviceName.BAS)
class KosmosSliderEmulatorTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos Power Slider Emulator class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos
        """
        super().setUpClass()

        cls._slider_emulator = KosmosPowerSliderEmulator(kosmos=cls.kosmos, fw_id='RBK71')
    # end def setUpClass

    def test_open_slider(self):
        """
        Validate open_slider() method.
        """
        for slider_id in KosmosIO.SLIDERS:
            self._slider_emulator.open_slider(slider_id)
        # end for
    # end def test_open_slider

    def test_close_slider(self):
        """
        Validate close_slider() method.
        """
        for slider_id in KosmosIO.SLIDERS:
            self._slider_emulator.close_slider(slider_id)
        # end for
    # end def test_close_slider

    def test_make_before_break(self):
        """
        Validate make_before_break() method.
        """
        for slider_id in KosmosIO.SLIDERS:
            self._slider_emulator.make_before_break(slider_id)
        # end for
    # end def test_make_before_break

    def _test_make_before_make(self):
        """
        Validate no_contact_2() method.
        """
        for slider_id in KosmosIO.SLIDERS:
            self._slider_emulator.no_contact_2(slider_id)
        # end for
    # end def _test_make_before_make

    def test_power_off(self):
        """
        Validate power_off() method.
        """
        self._slider_emulator.power_off()
    # end def test_power_off

    def test_power_on(self):
        """
        Validate power_on() method.
        """
        self._slider_emulator.power_on()
    # end def test_power_on

    def test_reset(self):
        """
        Validate reset() method.
        """
        # Test duration default value
        self._slider_emulator.reset()

        # Test duration input parameter
        self._slider_emulator.reset(duration=2)
    # end def test_reset
# end class KosmosSliderEmulatorTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
