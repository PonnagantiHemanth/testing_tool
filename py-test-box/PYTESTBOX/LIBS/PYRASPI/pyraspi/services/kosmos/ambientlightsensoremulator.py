#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.ambientlightsensoremulator
:brief: Kosmos Ambient Light Sensor Emulator Class
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from warnings import warn

from numpy import interp

from pylibrary.emulator.emulatorinterfaces import AmbientLightSensorEmulationInterface
from pyraspi.services.kosmos.config.alsconfiguration import GET_ALS_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_1

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
MAXIMUM_VOLTAGE_OUTPUT = 3.3


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AmbientLightSensorEmulator(AmbientLightSensorEmulationInterface):
    """
    Ambient Light Sensor Emulator
    """
    def __init__(self, kosmos, fw_id):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``pyraspi.services.kosmos.kosmos.Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``

        :raise ``AssertionError``: multiple sources of errors:
          - Invalid fw_id
          - No DAC channel found in PODs configuration for ALS emulator
        """
        assert fw_id in GET_ALS_CONFIGURATION_BY_ID, f'Don\'t support the fw_id : {fw_id}'
        self._als_configuration = GET_ALS_CONFIGURATION_BY_ID[fw_id]
        self._kosmos = kosmos

        self._als_dac_sel = ADDA_SEL_DAC_1
        self._als_dac_channel = None
        # Find the DAC channel in port 1 (PIO output voltage levels) associated to the ALS emulator
        for channel_id, channel in self._kosmos.pods_configuration.dacs[ADDA_SEL_DAC_1].channels.items():
            if channel.associated_device == DeviceFamilyName.AMBIENT_LIGHT_SENSOR:
                self._als_dac_channel = channel_id
                break
            # end if
        # end for
        assert self._als_dac_channel is not None, 'No DAC channel found in PODs configuration for ALS emulator'
    # end def __init__

    def set_ambient_light_intensity(self, illuminance=None):
        # See ``AmbientLightSensorEmulationInterface.set_ambient_light_intensity``
        illuminance = self._als_configuration.LUMINANCE_DEFAULT_VALUE if illuminance is None else illuminance

        voltage = self.get_voltage_from_lux_and_config(illuminance=illuminance,
                                                       als_configuration=self._als_configuration)

        self._kosmos.adda.write_dac(volts=voltage,
                                    dac_sel=self._als_dac_sel,
                                    channels=self._als_dac_channel)
    # end def set_ambient_light_intensity

    def get_luminance_threshold_backlight_off(self):
        # See ``AmbientLightSensorEmulationInterface.get_luminance_threshold_backlight_off``
        return self._als_configuration.LUMINANCE_THRESHOLD_BACKLIGHT_OFF
    # end def get_luminance_threshold_backlight_off

    @staticmethod
    def get_voltage_from_lux_and_config(illuminance, als_configuration):
        """
        Compute the voltage to set on the DAC from the given illuminance value and ALS configuration

        :param illuminance: illuminance value in Lux
        :type illuminance: ``float``
        :param als_configuration: Ambient light sensor configuration of the device
        :type als_configuration: ``pyraspi.services.kosmos.config.alsconfiguration.AlsConfigurationMixin``

        :return: Voltage value corresponding to the given illuminance value
        :rtype: ``float``
        """
        adc_value = interp(illuminance, als_configuration.LUMINANCE_ADC_VALUE_LOOKUP_TABLE[0],
                           als_configuration.LUMINANCE_ADC_VALUE_LOOKUP_TABLE[1])

        voltage = adc_value / als_configuration.ADC_COEFFICIENT

        # Protection against over-voltage
        if voltage > min(als_configuration.MAXIMUM_VOLTAGE_OUTPUT, MAXIMUM_VOLTAGE_OUTPUT):
            warn(f'The interpolated voltage matching the given illuminance value was to high (i.e. = {voltage}), '
                 'the output voltage is then clamped to MAXIMUM_VOLTAGE_OUTPUT value')
            voltage = min(als_configuration.MAXIMUM_VOLTAGE_OUTPUT, MAXIMUM_VOLTAGE_OUTPUT)
        # end if

        return voltage
    # end def get_voltage_from_lux_and_config
# end class AmbientLightSensorEmulator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
