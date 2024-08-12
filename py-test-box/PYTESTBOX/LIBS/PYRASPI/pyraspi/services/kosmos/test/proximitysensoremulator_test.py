#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.proximitysensoremulator_test.py
:brief: Tests for Kosmos Proximity Sensor
:author: Sylvain Krieg <skrieg@logitech.com>
:date: 2024/01/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyraspi.services.kosmos.proximitysensoremulator import ProximitySensorEmulator
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProximitySensorEmulatorTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos Proximity Sensor Emulator class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos and instantiate the Proximity Sensor Emulator class.
        """
        super().setUpClass()

        cls.proximity_sensor = ProximitySensorEmulator(kosmos=cls.kosmos, fw_id='RBK71')
    # end def setUpClass

    def test_set_proximity_presence(self):
        """
        Validate set_proximity_presence() method.
        """
        self.proximity_sensor.set_proximity_presence(False)
        self.proximity_sensor.set_proximity_presence(True)
        self.proximity_sensor.set_proximity_presence(False)
    # end def test_set_proximity_presence
# end class ProximitySensorEmulatorTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
