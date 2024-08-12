#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.powerslideremulator
:brief: Kosmos Power Slider Emulator Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import PowerSliderEmulationInterface
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.kosmos.config.sliderlayout import SLIDER_LAYOUT_BY_ID
from pyraspi.services.kosmos.slideremulator import KosmosSliderEmulator


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosPowerSliderEmulator(PowerSliderEmulationInterface, KosmosSliderEmulator):
    """
    Power Slider emulator leveraging Kosmos
    """
    def __init__(self, kosmos, fw_id):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``

        :raise ``AssertionError``: Invalid fw_id
        """
        super().__init__(kosmos=kosmos)

        assert fw_id in SLIDER_LAYOUT_BY_ID, f'Don\'t support the fw_id : {fw_id}'
        self._slider_layout = SLIDER_LAYOUT_BY_ID[fw_id]
    # end def __init__

    def power_off(self):
        # See ``PowerSliderEmulationInterface.power_off``
        slider_id = self._slider_layout.KEYS[KEY_ID.POWER]
        self.open_slider(slider_id=slider_id)
    # end def power_off

    def power_on(self):
        # See ``PowerSliderEmulationInterface.power_on``
        slider_id = self._slider_layout.KEYS[KEY_ID.POWER]
        self.close_slider(slider_id=slider_id)
    # end def power_on

    def reset(self, duration=.5):
        # See ``PowerSliderEmulationInterface.reset``
        assert duration > 0
        self.power_off()
        self._kosmos.pes.delay(delay_s=duration)
        self.power_on()
    # end def reset
# end class KosmosPowerSliderEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
