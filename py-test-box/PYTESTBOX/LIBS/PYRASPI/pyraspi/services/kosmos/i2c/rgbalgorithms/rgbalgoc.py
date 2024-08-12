#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.i2c.rgbalgorithms.rgbalgoc
:brief: Python RGB algorithms Class from lfa C function thanks to pythonCTestFunctions.so library
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/08/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from enum import IntEnum
from enum import unique
from platform import machine
from platform import system

from numpy import int16
from numpy import uint16

if system() == 'Linux':
    if machine() == 'armv7l':
        from pyraspi.services.kosmos.i2c.rgbalgorithms.arm.pythonCTestFunctions import *
    elif machine() == 'aarch64':
        from pyraspi.services.kosmos.i2c.rgbalgorithms.arm64.pythonCTestFunctions import *
    else:
        raise RuntimeError(f"Linux platform machine {machine()} not supported")
    # end if
else:
    raise RuntimeError(f"Platform system {system()} not supported")
# end if


# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
@unique
class RgbBrState(IntEnum):
    """
    States of RGB Breathing Effects
    """
    BOTTOM_SEG = 0
    RAMP_UP = 1
    TOP_SEG = 2
    RAMP_DOWN = 3
    STARTUP = 4
    PASSTHROUGH = 5
# end class RgbBrState


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class HsvComponents:
    """
    Representation of the HSV(hue, saturation, value) color model
    """
    h: int = 0
    s: int = 0
    v: int = 0
# end class HsvComponents


@dataclass
class RgbComponents:
    """
    Representation of the RGB(red, green, blue) color model
    """
    r: uint16 = 0
    g: uint16 = 0
    b: uint16 = 0
# end class RgbComponents


@dataclass
class LedZoneParam:
    """
    Representation of the parameters used to compute the color cycling and breathing effect at each time
    """
    cc_index: uint16
    br_index: uint16
    br_segment_index: uint16
    rgb_comp_out: RgbComponents
    hsv_comp: HsvComponents
    hsv_comp_out: HsvComponents
    br_state: RgbBrState
    cc_drift_counts: int16
    br_drift_counts: int16
# end class LedZoneParam


@dataclass
class LedZoneEffectParam:
    """
    Representation of the initial parameters used for color cycling and breathing effect
    """
    cc_period: uint16
    cc_slope: int
    cc_enable: bool
    br_period: uint16
    br_ramp_period: uint16
    br_bottom_period: uint16
    br_top_period: uint16
    br_slope: int
    br_enabled: bool
# end class LedZoneEffectParam


class RgbCAlgo:
    """
    Define the RGB C algorithm from pythonCTestFunctions for rgb validation effect.
    """

    def __init__(self):
        rgb_Init()
        self.led_zone1_param = LedZoneParam(uint16(0), uint16(0), uint16(0),
                                            RgbComponents(uint16(0), uint16(0), uint16(0)), HsvComponents(0, 0, 0),
                                            HsvComponents(0, 0, 0), RgbBrState.BOTTOM_SEG, uint16(0), uint16(0))
        self.led_zone1_effect_param = LedZoneEffectParam(uint16(0), 0, False, uint16(0), uint16(0), uint16(0),
                                                         uint16(0), uint16(0), False)
        self.led_zone2_param = LedZoneParam(uint16(0), uint16(0), uint16(0),
                                            RgbComponents(uint16(0), uint16(0), uint16(0)), HsvComponents(0, 0, 0),
                                            HsvComponents(0, 0, 0), RgbBrState.BOTTOM_SEG, uint16(0), uint16(0))
        self.led_zone2_effect_param = LedZoneEffectParam(uint16(0), 0, False, uint16(0), uint16(0), uint16(0),
                                                         uint16(0), uint16(0), False)
    # end def __init__

    @staticmethod
    def gamma_crt16_calc(rgb_value):
        """
        Apply Gamma function to linearize the sRGB input component

        :param rgb_value: The R,G or B component value to linearize.
        :type rgb_value: ``uint16``

        :return: The R,G or B component value linearized.
        :rtype: ``uint16``
        """
        return uint16(rgb_gammaCrt16Calc(rgb_value))
    # end def gamma_crt16_calc

    @staticmethod
    def gamma_crt8_table(rgb_value):
        """
        Apply Gamma 8bit -> 8bit table to linearize the sRGB input component

        :param rgb_value: The R,G or B component value to linearize.
        :type rgb_value: ``uint16``

        :return: The R,G or B component value linearized.
        :rtype: ``uint16``
        """
        return uint16(rgb_gammaCrt8Table(rgb_value))
    # end def gamma_crt8_table

    @staticmethod
    def rgb_to_hsv(rgb_input):
        """
        Convert the RGB color input representation to HSV color representation.

        :param rgb_input: The RGB color representation.
        :type rgb_input: ``RgbComponents``

        :return: The HSV color representation
        :rtype: ``HsvComponents``
        """
        h, s, v = rgb_rgbToHsv(rgb_input.r, rgb_input.g, rgb_input.b)
        hsv_output = HsvComponents(h, s, v)
        return hsv_output
    # end def rgb_to_hsv

    @staticmethod
    def hsv_to_rgb(hsv_input):
        """
        Convert the HSV color input representation to RGB color representation.

        :param hsv_input: The HSV color representation.
        :type hsv_input: ``HsvComponents``

        :return: The RGB color representation
        :rtype: ``RgbComponents``
        """
        r, g, b = rgb_hsvToRgb(hsv_input.h, hsv_input.s, hsv_input.v)
        rgb_output = RgbComponents(r, g, b)
        return rgb_output
    # end def hsv_to_rgb

    @staticmethod
    def apply_calibration_and_boost(rgb_input, calibration_coef):
        """
        Apply the RGB calibration coefficients; and calculate and apply the boost factor.


        :param rgb_input: The RGB color representation.
        :type rgb_input: ``RgbComponents``
        :param calibration_coef: Calibration values of R, G and B components.
        :type calibration_coef: ``list``

        :return: The RGB color representation after calibration.
        :rtype: ``RgbComponents``
        """
        cal_boost_tuple = rgb_applyCalibrationAndBoost(rgb_input.r, rgb_input.g, rgb_input.b,
                                                       calibration_coef[0], calibration_coef[1], calibration_coef[2])

        return RgbComponents(cal_boost_tuple[1], cal_boost_tuple[2], cal_boost_tuple[3])
    # end def apply_calibration_and_boost

    def cc_reset_and_calculate_param(self, zone_number, period):
        """
        Reset and calculate the parameter of color cycle effect

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        :param period: Number of samples of 1 color cycle period.
        :type period: ``uint16``
        """
        if zone_number == 1:
            self.set_led_param(zone_number, self.led_zone1_param)
            self.set_led_effect_param(zone_number, self.led_zone1_effect_param)
            rgb_ccResetAndCalculateParam(zone_number, period)
            self.led_zone1_param = self.get_led_param(zone_number)
            self.led_zone1_effect_param = self.get_led_effect_param(zone_number)
        elif zone_number == 2:
            self.set_led_param(zone_number, self.led_zone2_param)
            self.set_led_effect_param(zone_number, self.led_zone2_effect_param)
            rgb_ccResetAndCalculateParam(zone_number, period)
            self.led_zone2_param = self.get_led_param(zone_number)
            self.led_zone2_effect_param = self.get_led_effect_param(zone_number)
        # end if
    # end def cc_reset_and_calculate_param

    def cc_calculate_param(self, zone_number, period):
        """
        Calculate the parameter of color cycle effect

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        :param period: Number of samples of 1 color cycle period.
        :type period: ``uint16``
        """
        if zone_number == 1:
            self.set_led_param(zone_number, self.led_zone1_param)
            self.set_led_effect_param(zone_number, self.led_zone1_effect_param)
            rgb_ccCalculateParam(zone_number, period)
            self.led_zone1_param = self.get_led_param(zone_number)
            self.led_zone1_effect_param = self.get_led_effect_param(zone_number)
        elif zone_number == 2:
            self.set_led_param(zone_number, self.led_zone2_param)
            self.set_led_effect_param(zone_number, self.led_zone2_effect_param)
            rgb_ccCalculateParam(zone_number, period)
            self.led_zone2_param = self.get_led_param(zone_number)
            self.led_zone2_effect_param = self.get_led_effect_param(zone_number)
        # end if
    # end def cc_calculate_param

    @staticmethod
    def calculate_cubic_function(input_color):
        """
        Calculate cubic function

        :param input_color: input of the cubic function
        :type input_color: ``int``

        :return: result
        :rtype: ``int``
        """
        return rgb_calculateCubicFunction(input_color)
    # end def calculate_cubic_function

    def br_reset_and_calculate_param(self, zone_number, period):
        """
        Reset and calculate the parameter of breathing effect

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        :param period: Number of samples of 1 color cycle period.
        :type period: ``uint16``
        """
        if zone_number == 1:
            self.set_led_param(zone_number, self.led_zone1_param)
            self.set_led_effect_param(zone_number, self.led_zone1_effect_param)
            rgb_brResetAndCalculateParam(zone_number, period)
            self.led_zone1_param = self.get_led_param(zone_number)
            self.led_zone1_effect_param = self.get_led_effect_param(zone_number)
        elif zone_number == 2:
            self.set_led_param(zone_number, self.led_zone2_param)
            self.set_led_effect_param(zone_number, self.led_zone2_effect_param)
            rgb_brResetAndCalculateParam(zone_number, period)
            self.led_zone2_param = self.get_led_param(zone_number)
            self.led_zone2_effect_param = self.get_led_effect_param(zone_number)
        # end if
    # end def br_reset_and_calculate_param

    def br_execute(self, zone_number):
        """
        Execute breathing effect

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        """
        if zone_number == 1:
            self.set_led_param(zone_number, self.led_zone1_param)
            self.set_led_effect_param(zone_number, self.led_zone1_effect_param)
            rgb_brExecute(zone_number)
            self.led_zone1_param = self.get_led_param(zone_number)
            self.led_zone1_effect_param = self.get_led_effect_param(zone_number)
        elif zone_number == 2:
            self.set_led_param(zone_number, self.led_zone2_param)
            self.set_led_effect_param(zone_number, self.led_zone2_effect_param)
            rgb_brExecute(zone_number)
            self.led_zone2_param = self.get_led_param(zone_number)
            self.led_zone2_effect_param = self.get_led_effect_param(zone_number)
        # end if
    # end def br_execute

    def cc_execute(self, zone_number):
        """
        Execute color cycling effect

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        """
        if zone_number == 1:
            self.set_led_param(zone_number, self.led_zone1_param)
            self.set_led_effect_param(zone_number, self.led_zone1_effect_param)
            rgb_ccExecute(zone_number)
            self.led_zone1_param = self.get_led_param(zone_number)
            self.led_zone1_effect_param = self.get_led_effect_param(zone_number)
        elif zone_number == 2:
            self.set_led_param(zone_number, self.led_zone2_param)
            self.set_led_effect_param(zone_number, self.led_zone2_effect_param)
            rgb_ccExecute(zone_number)
            self.led_zone2_param = self.get_led_param(zone_number)
            self.led_zone2_effect_param = self.get_led_effect_param(zone_number)
        # end if
    # end def cc_execute

    def execute_effects(self, zone_number):
        """
        Execute breathing and color cycling effects

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        """
        if zone_number == 1:
            self.set_led_param(zone_number, self.led_zone1_param)
            self.set_led_effect_param(zone_number, self.led_zone1_effect_param)
            rgb_executeEffects(zone_number)
            self.led_zone1_param = self.get_led_param(zone_number)
            self.led_zone1_effect_param = self.get_led_effect_param(zone_number)
        elif zone_number == 2:
            self.set_led_param(zone_number, self.led_zone2_param)
            self.set_led_effect_param(zone_number, self.led_zone2_effect_param)
            rgb_executeEffects(zone_number)
            self.led_zone2_param = self.get_led_param(zone_number)
            self.led_zone2_effect_param = self.get_led_effect_param(zone_number)
        # end if
    # end def execute_effects

    @staticmethod
    def get_led_effect_param(zone_number):
        """
        Get the ``LedZoneEffectParam`` from the zone number

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``

        :return: The led effect parameter corresponding to the desired zone.
        :rtype: ``LedZoneEffectParam``
        """
        led_effect_tuple = rgb_getLedEffectParam(zone_number)

        return LedZoneEffectParam(cc_period=led_effect_tuple[1],
                                  cc_slope=led_effect_tuple[2],
                                  cc_enable=led_effect_tuple[3],
                                  br_period=led_effect_tuple[4],
                                  br_ramp_period=led_effect_tuple[5],
                                  br_bottom_period=led_effect_tuple[6],
                                  br_top_period=led_effect_tuple[7],
                                  br_slope=led_effect_tuple[8],
                                  br_enabled=led_effect_tuple[9])
    # end def get_led_effect_param

    @staticmethod
    def get_led_param(zone_number):
        """
        Get the ``LedZoneParam`` from the zone number

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``

        :return: The led parameter corresponding to the desired zone.
        :rtype: ``LedZoneParam``
        """
        led_param_tuple = rgb_getLedParam(zone_number)

        return LedZoneParam(cc_index=led_param_tuple[1],
                            br_index=led_param_tuple[2],
                            br_segment_index=led_param_tuple[3],
                            rgb_comp_out=RgbComponents(led_param_tuple[4], led_param_tuple[5],
                                                       led_param_tuple[6]),
                            hsv_comp=HsvComponents(led_param_tuple[7], led_param_tuple[8], led_param_tuple[9]),
                            hsv_comp_out=HsvComponents(led_param_tuple[10], led_param_tuple[11],
                                                       led_param_tuple[12]),
                            br_state=led_param_tuple[13],
                            cc_drift_counts=led_param_tuple[14],
                            br_drift_counts=led_param_tuple[15])
    # end def get_led_param

    def set_led_effect_param(self, zone_number, led_zone_effect_param):
        """
        Set the ``LedZoneEffectParam`` from the zone number

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        :param led_zone_effect_param: The led effect parameter corresponding to the desired zone.
        :type led_zone_effect_param: ``LedZoneEffectParam``

        :raise ``AssertionError``: If zone_number is not in its valid range
        """
        assert zone_number in [1, 2], 'zone number is not in its valid range'
        if zone_number == 1:
            self.led_zone1_effect_param = led_zone_effect_param
        elif zone_number == 2:
            self.led_zone2_effect_param = led_zone_effect_param
        # end if
        rgb_setLedEffectParam(zone_number,
                              led_zone_effect_param.cc_period,
                              led_zone_effect_param.cc_slope,
                              led_zone_effect_param.cc_enable,
                              led_zone_effect_param.br_period,
                              led_zone_effect_param.br_ramp_period,
                              led_zone_effect_param.br_bottom_period,
                              led_zone_effect_param.br_top_period,
                              led_zone_effect_param.br_slope,
                              led_zone_effect_param.br_enabled)
    # end def set_led_effect_param

    def set_led_param(self, zone_number, led_zone_param):
        """
        Set the ``LedZoneParam`` from the zone number

        :param zone_number: The zone number of the effect.
        :type zone_number: ``int``
        :param led_zone_param: The led effect parameter corresponding to the desired zone.
        :type led_zone_param: ``LedZoneParam``

        :raise ``AssertionError``: If zone_number is not in its valid range
        """
        assert zone_number in [1, 2], 'zone number is not in its valid range'
        if zone_number == 1:
            self.led_zone1_param = led_zone_param
        elif zone_number == 2:
            self.led_zone2_param = led_zone_param
        # end if
        rgb_setLedParam(zone_number,
                        led_zone_param.cc_index,
                        led_zone_param.br_index,
                        led_zone_param.br_segment_index,
                        led_zone_param.rgb_comp_out.r,
                        led_zone_param.rgb_comp_out.g,
                        led_zone_param.rgb_comp_out.b,
                        led_zone_param.hsv_comp.h,
                        led_zone_param.hsv_comp.s,
                        led_zone_param.hsv_comp.v,
                        led_zone_param.hsv_comp_out.h,
                        led_zone_param.hsv_comp_out.s,
                        led_zone_param.hsv_comp_out.v,
                        led_zone_param.br_state,
                        led_zone_param.cc_drift_counts,
                        led_zone_param.br_drift_counts)
    # end def set_led_param
# end class RgbCAlgo

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
