#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.alsconfiguration
:brief: Ambient Light Sensor configuration per product
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/10/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AlsConfigurationMixin:
    """
    Common implementation class for ambient light sensor emulators.
    """
    MAXIMUM_VOLTAGE_OUTPUT = 2.6
    ADC_COEFFICIENT = None
    LUMINANCE_ADC_VALUE_LOOKUP_TABLE = None
# end class AlsConfigurationMixin


class IngaAlsConfiguration(AlsConfigurationMixin):
    """
    Configure the ambient light sensor emulator for Inga keyboard

    Lookup table for guide light and als calibration can be found on :
    https://docs.google.com/spreadsheets/d/1KWN-RlXKuv26If7wl2SyE7si5LoobE6Qb_0rX-xO3n8/view
    """
    MAXIMUM_VOLTAGE_OUTPUT = 2.6

    ADC_COEFFICIENT = 341.33  # ADC sample / Volt
    # ADV values measured with R=33 k - 0.08 % - Unit 3T8
    LUMINANCE_ADC_VALUE_LOOKUP_TABLE = [[0, 27, 89, 144, 208, 275, 362, 395, 440, 462, 600],  # Luminance (Lux)
                                        [0, 66, 221, 345, 490, 623, 798, 839, 862, 868, 879]  # ADC value
                                        ]
    # https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/rbk71_inga/+/refs/heads/master/application/als.c
    ALS_MEASURE_PERIOD = 60  # Unit: s

    # TODO ALS luminance thresholds are put here until the test feature 0x1A20 ALS Calibration is implemented,
    #  then these thresholds could be put on each settings.ini file
    #  https://jira.logitech.io/browse/PTB-442
    LUMINANCE_THRESHOLD_BACKLIGHT_OFF = 200
    LUMINANCE_THRESHOLD_BACKLIGHT_LEVEL_2_4 = 100

    LUMINANCE_DEFAULT_VALUE = 0
# end class IngaAlsConfiguration


class NormanAlsConfiguration(IngaAlsConfiguration):
    """
    Configure the ambient light sensor emulator for Norman keyboard
    TODO For now LUMINANCE_ADC_VALUE_LOOKUP_TABLE and ADC_COEFFICIENT is a copy of Inga value
    """
# end class NormanAlsConfiguration


GET_ALS_CONFIGURATION_BY_ID = {
    'RBK71': IngaAlsConfiguration,
    'RBK75': IngaAlsConfiguration,
    'RBK81': NormanAlsConfiguration,
}

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
