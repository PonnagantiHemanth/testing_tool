#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.ambientlightsensoremulator_test
:brief: Tests for Kosmos Ambient Light Sensor
:author: Sylvain Krieg <skrieg@logitech.com>
:date: 2024/01/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyraspi.services.kosmos.ambientlightsensoremulator import AmbientLightSensorEmulator
from pyraspi.services.kosmos.config.alsconfiguration import GET_ALS_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AmbientLightSensorEmulatorTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Ambient light sensor emulator class.
    """
    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos and instantiate the Ambient Light Sensor emulator class
        """
        super().setUpClass()

        cls.ambient_light_sensor_emulator = AmbientLightSensorEmulator(kosmos=cls.kosmos, fw_id='RBK71')
    # end def setUpClass

    def test_set_ambient_light_intensity(self):
        """
        Validate set_ambient_light_intensity() method
        """
        # Check optional argument, minimum value (0V)
        self.ambient_light_sensor_emulator.set_ambient_light_intensity(
            min(GET_ALS_CONFIGURATION_BY_ID['RBK71'].LUMINANCE_ADC_VALUE_LOOKUP_TABLE[0]))
        # Check optional argument, medium value (1.95V)
        self.ambient_light_sensor_emulator.set_ambient_light_intensity(
            max(GET_ALS_CONFIGURATION_BY_ID['RBK71'].LUMINANCE_ADC_VALUE_LOOKUP_TABLE[0]) / 2)
        # Check optional argument, maximum value (2.56V)
        self.ambient_light_sensor_emulator.set_ambient_light_intensity(
            max(GET_ALS_CONFIGURATION_BY_ID['RBK71'].LUMINANCE_ADC_VALUE_LOOKUP_TABLE[0]))
        # Check without optional argument, default value (0V)
        self.ambient_light_sensor_emulator.set_ambient_light_intensity()
    # end def test_set_ambient_light_intensity

    def test_get_luminance_threshold_backlight_off(self):
        """
        Validate get_luminance_threshold_backlight_off() method
        """
        self.assertEqual(GET_ALS_CONFIGURATION_BY_ID['RBK71'].LUMINANCE_THRESHOLD_BACKLIGHT_OFF,
                         self.ambient_light_sensor_emulator.get_luminance_threshold_backlight_off())
    # end def test_get_luminance_threshold_backlight_off
# end class AmbientLightSensorEmulatorTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
