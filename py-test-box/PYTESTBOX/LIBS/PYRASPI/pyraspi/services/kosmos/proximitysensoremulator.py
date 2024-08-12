#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.proximitysensoremulator
:brief: Proximity sensor Emulator Class
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/10/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import ProximitySensorEmulationInterface
from pyraspi.services.kosmos.config.sliderlayout import PROXIMITY_SENSOR_LAYOUT_BY_ID
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.slideremulator import KosmosSliderEmulator


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProximitySensorEmulator(ProximitySensorEmulationInterface, KosmosSliderEmulator):
    """
    Proximity sensor emulator using a Kosmos slider
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

        assert fw_id in PROXIMITY_SENSOR_LAYOUT_BY_ID, f'Don\'t support the fw_id : {fw_id}'
        self._slider_layout = PROXIMITY_SENSOR_LAYOUT_BY_ID[fw_id]

        # set no proximity by default
        self.set_proximity_presence(enable=False)
    # end def __init__

    def set_proximity_presence(self, enable=True):
        # See ``ProximitySensorEmulationInterface.set_proximity_presence``
        if enable:
            self.close_slider(self._slider_layout.SLIDER_ID)
        else:
            self.open_slider(self._slider_layout.SLIDER_ID)
        # end if
    # end def set_proximity_presence
# end class ProximitySensorEmulator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
