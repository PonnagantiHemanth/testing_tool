#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.i2c.rgbparser
:brief: RGB I2C data parser Class
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/10/02
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from enum import IntEnum
from enum import auto
from enum import unique

from matplotlib import pyplot as plt
from numpy import all
from numpy import array
from numpy import iinfo
from numpy import max
from numpy import mean
from numpy import nan
from numpy import ones
from numpy import sqrt
from numpy import uint16
from numpy import uint8

from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pylibrary.system.tracelogger import TraceLogger, TraceLevel
from pyraspi.services.kosmos.config.rgbconfiguration import GET_RGB_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.config.rgbconfigurations.commonrgbconfiguration import PWM_DRIVER_BIT_MODE_STR_MAP
from pyraspi.services.kosmos.config.rgbconfigurations.commonrgbconfiguration import PwmDriverBitMode
from pyraspi.services.kosmos.config.rgbconfigurations.commonrgbconfiguration import RgbLedIndicator
from pyraspi.services.kosmos.i2c.i2cbacklightparser import TimeLineMixin
from pyraspi.services.kosmos.i2c.rgbalgorithms.rgbalgoc import RgbCAlgo
from pyraspi.services.kosmos.i2c.rgbalgorithms.rgbalgoc import RgbComponents

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

# Configure RGB parser traces verbosity
#  - None: disable all traces
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for minimal information
#  - TraceLevel.DEBUG: Debug level will be for maximum log information
#  - TraceLevel.EXTRA_DEBUG: Extra Debug level will be for maximum log and plot information
FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_LEVEL = TraceLevel.ERROR
FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_FILE_NAME = None

# 10% Tolerance
_10_PERCENT = 10 / 100
# 20% Tolerance
_20_PERCENT = 20 / 100

_MIN_ACCEPTABLE_TIMING_ERROR = 1  # in second
_MIN_ACCEPTABLE_ABSOLUTE_ERROR = 2   # in second
_MIN_DURATION_OFF_EFFECT = 3   # in second

MAXIMUM_LED_ID = 255
# The RGB zone ID of Main  keys (the most part of LED)
RGB_ZONE_ID_MAIN = 0
# The RGB zone ID of Edge strip
RGB_ZONE_ID_EDGE = 1
# The RGB zone ID of Media keys
RGB_ZONE_ID_MEDIA = 2

RGB_RED_ID = 0
RGB_GREEN_ID = 1
RGB_BLUE_ID = 2


class RGBClusterId:
    """
    RGB cluster ID
    """
    PRIMARY = 0x00
    EDGE = 0x01
    MULTI_CLUSTER = 0xFF
# end class RGBClusterId


@unique
class ImmersiveLightingState(IntEnum):
    """
    Immersive lighting states
    """
    START_UP = auto()
    ACTIVE = auto()
    PASSIVE = auto()
    SHUTDOWN = auto()
    OFF = auto()
    UNDETERMINED = auto()
# end class ImmersiveLightingState


IMMERSIVE_LIGHTING_STATE_STR_MAP = {
    ImmersiveLightingState.START_UP: 'start up',
    ImmersiveLightingState.ACTIVE: 'active',
    ImmersiveLightingState.PASSIVE: 'passive',
    ImmersiveLightingState.SHUTDOWN: 'shutdown',
    ImmersiveLightingState.OFF: 'off',
    ImmersiveLightingState.UNDETERMINED: 'undetermined',
}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class ImmersiveLightingEffect:
    """
    Implementation of the minimal characteristics of an immersive lighting effect
    """
    type: ImmersiveLightingState = ImmersiveLightingState.UNDETERMINED
    duration: float = 0.0
    start_time: float = 0.0
    start_index: int = 0
    end_time: float = 0.0
    end_index: int = 0
# end class ImmersiveLightingEffect


class TimeLine(TimeLineMixin):
    """
    List the successive immersive lighting effect capture from the i2c or led pwm monitoring
    """
    def add_effect(self, effect_type, start_time, start_index):
        """
        Add an immersive lighting effect into the timeline.

        :param effect_type: The new immersive lighting effect to include
        :type effect_type: ``ImmersiveLightingState``
        :param start_time: The time when the effect starts
        :type start_time: ``float``
        :param start_index: The index list when the effect starts
        :type start_index: ``int``
        """
        effect = ImmersiveLightingEffect(type=effect_type, start_time=start_time, start_index=start_index,
                                         end_time=0.0, end_index=0)
        self.effects.append(effect)
    # end def add_effect

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        message = 'Immersive lighting TimeLine:\n'
        if not self.effects:
            message += f'Timeline is empty'
        # end if
        for effect in self.effects:
            message += f'* {IMMERSIVE_LIGHTING_STATE_STR_MAP[effect.type]}\n'
            message += f'   -start time : {effect.start_time}\n'
            message += f'   -end time : {effect.end_time}\n'
            message += f'   -duration time : {effect.duration}\n'
        # end for
        return message
    # end def __str__
# end class TimeLine


class RgbAlgorithms:
    """
    RGB effect algorithms
    """
    def __init__(self, fw_id, calibration_data, layout):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
        :type calibration_data: ``list[list[int, int, int]]``
        :param layout: keyboard international layout type
        :type layout: ``KeyboardInternationalLayouts.LAYOUT``
        """
        self.calibration_data = calibration_data
        self.rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        self.layout = layout

        # result of the algorithm
        self.led_algo_values_over_time = []
    # end def __init__

    def fixed_effect(self, timestamps, cluster_index, red_value, green_value, blue_value, brightness):
        """
        Fixed rgb Color effect algorithm

        :param timestamps: The timestamp list of the LED list
        :type timestamps: ``list[float]``
        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param red_value: Red color value
        :type red_value: ``int``
        :param green_value: Green color value
        :type green_value: ``int``
        :param blue_value: Blue color value
        :type blue_value: ``int``
        :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100, >100 is clamped to 100
        :type brightness: ``int``
        """
        rgb_led_input = RgbComponents()
        rgb_led_input.r = uint16(red_value) * uint16(iinfo(uint16).max / iinfo(uint8).max)
        rgb_led_input.g = uint16(green_value) * uint16(iinfo(uint16).max / iinfo(uint8).max)
        rgb_led_input.b = uint16(blue_value) * uint16(iinfo(uint16).max / iinfo(uint8).max)
        led_ids_to_check, _ = self._get_led_ids_and_zone_number(cluster_index)
        for _ in timestamps:
            temp_algo_res = [RgbComponents(nan, nan, nan) for _ in range(0, MAXIMUM_LED_ID)]
            for led_id in led_ids_to_check:
                calibration_zone_id = self.get_calibration_zone_id(led_id)
                temp_algo_res[led_id] = self.led_calibration(rgb_led_input, calibration_zone_id)
                temp_algo_res[led_id].r *= (brightness / 100)
                temp_algo_res[led_id].g *= (brightness / 100)
                temp_algo_res[led_id].b *= (brightness / 100)
            # end for
            # adjust with non-mounted led
            temp_algo_res = self.adjust_rgb_buffer_with_non_mounted_led(rgb_buffer=temp_algo_res, layout=self.layout)
            self.led_algo_values_over_time.append(temp_algo_res.copy())
        # end for
    # end def fixed_effect

    def pulsing_breathing_effect(self, timestamps, cluster_index, red_value, green_value, blue_value, period_msb,
                                 period_lsb, brightness):
        """
        Pulsing/breathing rgb Color effect algorithm

        :param timestamps: The timestamp list of the LED list
        :type timestamps: ``list[float]``
        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param red_value: Red value of RGB color model
        :type red_value: ``int``
        :param green_value: Green value of RGB color model
        :type green_value: ``int``
        :param blue_value: Blue value of RGB color model
        :type blue_value: ``int``
        :param period_msb: MSB of the effect period
        :type period_msb: ``int``
        :param period_lsb: LSB of the effect period
        :type period_lsb: ``int``
        :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100, >100 is clamped to 100
        :type brightness: ``int``
        """
        led_ids_to_check, zone_number = self._get_led_ids_and_zone_number(cluster_index)

        # initialisation of the effect
        rgb_effect = RgbCAlgo()
        input_rgb = RgbComponents()
        input_rgb.r = uint16(red_value) * uint16(iinfo(uint16).max / iinfo(uint8).max)
        input_rgb.g = uint16(green_value) * uint16(iinfo(uint16).max / iinfo(uint8).max)
        input_rgb.b = uint16(blue_value) * uint16(iinfo(uint16).max / iinfo(uint8).max)
        period = period_lsb | period_msb << 8
        led_zone_param = rgb_effect.get_led_param(zone_number)
        led_zone_param.hsv_comp = RgbCAlgo.rgb_to_hsv(input_rgb)
        rgb_effect.set_led_param(zone_number, led_zone_param)

        if (brightness > 100) or (brightness == 0):
            brightness = 100
        # end if
        # Limit the intensity from 20~100
        brightness = uint8(((brightness * 80) / 100) + 20)

        brightness_modulator = brightness / 100
        led_zone_param.hsv_comp.v = int(led_zone_param.hsv_comp.v * brightness_modulator)
        rgb_effect.set_led_param(zone_number, led_zone_param)

        frame_rate = self.rgb_configuration.RGB_BREATHING_FRAME_RATE
        period_samples = uint16(round(period / frame_rate))

        rgb_effect.br_reset_and_calculate_param(zone_number, period_samples)
        rgb_effect.execute_effects(zone_number)

        for _ in timestamps:
            rgb_effect.execute_effects(zone_number)
            led_zone_param = rgb_effect.get_led_param(zone_number)
            rgb_comp_out = RgbComponents(r=led_zone_param.rgb_comp_out.r,
                                         b=led_zone_param.rgb_comp_out.b,
                                         g=led_zone_param.rgb_comp_out.g)
            temp_algo_res = [RgbComponents(nan, nan, nan) for _ in range(0, MAXIMUM_LED_ID)]
            for led_id in led_ids_to_check:
                calibration_zone_id = self.get_calibration_zone_id(led_id)
                temp_algo_res[led_id] = self.led_calibration(rgb_comp_out, calibration_zone_id)
            # end for
            # adjust with non-mounted led
            temp_algo_res = self.adjust_rgb_buffer_with_non_mounted_led(rgb_buffer=temp_algo_res, layout=self.layout)
            self.led_algo_values_over_time.append(temp_algo_res.copy())
        # end for
    # end def pulsing_breathing_effect

    def color_cycling_configurable_s_effect(self, timestamps, cluster_index, saturation, period_msb, period_lsb,
                                            brightness):
        """
        Color cycling configurable S effect algorithm

        :param timestamps: The timestamp list of the LED list
        :type timestamps: ``list[float]``
        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param saturation: Saturation
        :type saturation: ``int``
        :param period_msb: MSB of the effect period
        :type period_msb: ``int``
        :param period_lsb: LSB of the effect period
        :type period_lsb: ``int``
        :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100, >100 is clamped to 100
        :type brightness: ``int``
        """
        led_ids_to_check, zone_number = self._get_led_ids_and_zone_number(cluster_index)

        # initialisation of the effect
        rgb_effect = RgbCAlgo()
        input_rgb = RgbComponents()
        input_rgb.r = iinfo(uint16).max
        input_rgb.g = 0
        input_rgb.b = 0
        period = period_lsb | period_msb << 8

        if (brightness > 100) or (brightness == 0):
            brightness = 100
        # end if
        # Limit the intensity from 20~100
        brightness = uint8(((brightness * 80) / 100) + 20)
        brightness_modulator = brightness / 100

        led_zone_param = rgb_effect.get_led_param(zone_number)
        led_zone_param.hsv_comp = RgbCAlgo.rgb_to_hsv(input_rgb)
        led_zone_param.hsv_comp.v = int(led_zone_param.hsv_comp.v * brightness_modulator)
        rgb_effect.set_led_param(zone_number, led_zone_param)

        frame_rate = self.rgb_configuration.RGB_COLOR_CYCLING_FRAME_RATE
        period_samples = uint16(round(period / frame_rate))

        rgb_effect.cc_reset_and_calculate_param(zone_number, period_samples)

        for _ in timestamps:
            led_zone_param = rgb_effect.get_led_param(zone_number)
            led_zone_param.hsv_comp_out = led_zone_param.hsv_comp
            rgb_effect.set_led_param(zone_number, led_zone_param)
            rgb_effect.execute_effects(zone_number)
            led_zone_param = rgb_effect.get_led_param(zone_number)

            # saturation
            saturation_modulator = saturation / 255
            led_zone_param.hsv_comp_out.s = int(led_zone_param.hsv_comp_out.s * saturation_modulator)
            rgb_effect.set_led_param(zone_number, led_zone_param)

            led_zone_param = rgb_effect.get_led_param(zone_number)
            rgb_comp_out = RgbCAlgo.hsv_to_rgb(led_zone_param.hsv_comp_out)
            temp_rgb = RgbComponents(r=rgb_comp_out.r,
                                     b=rgb_comp_out.b,
                                     g=rgb_comp_out.g)

            temp_algo_res = [RgbComponents(nan, nan, nan) for _ in range(0, MAXIMUM_LED_ID)]
            for led_id in led_ids_to_check:
                calibration_zone_id = self.get_calibration_zone_id(led_id)
                temp_algo_res[led_id] = self.led_calibration(temp_rgb, calibration_zone_id)
            # end for
            # adjust with non-mounted led
            temp_algo_res = self.adjust_rgb_buffer_with_non_mounted_led(rgb_buffer=temp_algo_res, layout=self.layout)
            self.led_algo_values_over_time.append(temp_algo_res.copy())
        # end for
    # end def color_cycling_configurable_s_effect

    def adjust_rgb_buffer_with_non_mounted_led(self, rgb_buffer, layout=KeyboardInternationalLayouts.LAYOUT.US):
        """
        Set RGB value to zero for non-mounted led

        :param rgb_buffer: list of RGB value for all the LEDs
        :type rgb_buffer: ``list[RgbComponents]``
        :param layout: keyboard international layout type - OPTIONAL
        :type layout: ``KeyboardInternationalLayouts.LAYOUT``

        :return: list of RGB value for all the LEDs with non-mounted LEDS set to zero
        :rtype: ``list[RgbComponents]``
        """
        # Non mounted Main Keys by layout
        if layout == KeyboardInternationalLayouts.LAYOUT.UK:
            nm_led = self.rgb_configuration.NOT_MOUNTED_LEDS_MAIN_UK_LAYOUT
        elif layout == KeyboardInternationalLayouts.LAYOUT.JAPANESE:
            nm_led = self.rgb_configuration.NOT_MOUNTED_LEDS_MAIN_JP_LAYOUT
        elif layout == KeyboardInternationalLayouts.LAYOUT.RUSSIAN:
            nm_led = self.rgb_configuration.NOT_MOUNTED_LEDS_MAIN_RU_LAYOUT
        elif layout == KeyboardInternationalLayouts.LAYOUT.PORTUGUESE_BRAZILIAN:
            nm_led = self.rgb_configuration.NOT_MOUNTED_LEDS_MAIN_BR_LAYOUT
        else:
            nm_led = self.rgb_configuration.NOT_MOUNTED_LEDS_MAIN_US_LAYOUT
        # end if

        for led_id in (self.rgb_configuration.NOT_MOUNTED_LEDS_MAIN_ALL_LAYOUT + nm_led +
                       self.rgb_configuration.NOT_MOUNTED_LEDS_EDGE_ALL_LAYOUT):
            rgb_buffer[led_id].r = 0
            rgb_buffer[led_id].g = 0
            rgb_buffer[led_id].b = 0
        # end for

        return rgb_buffer
    # end def adjust_rgb_buffer_with_non_mounted_led

    def get_calibration_zone_id(self, led_id):
        """
        Get the calibration zone ID corresponding to the led_id

        :param led_id: The LED ID
        :type led_id: ``int``

        :return: the calibration zone ID of the led_id
        :rtype: ``int``
        """
        zone_id = RGB_ZONE_ID_MAIN
        if led_id in self.rgb_configuration.EDGE_LIGHTING_LED_ID_RANGE:
            zone_id = RGB_ZONE_ID_EDGE
        elif led_id in self.rgb_configuration.INDICATOR_ON_MEDIA_ZONE_CALIBRATION:
            zone_id = RGB_ZONE_ID_MEDIA
        # end if
        return zone_id
    # end def get_calibration_zone_id

    def led_calibration(self, rgb_led, cal_id):
        """
        Apply LED calibration

        :param rgb_led: The RGB color representation.
        :type rgb_led: ``RgbComponents``
        :param cal_id: The calibration zone ID
        :type cal_id: ``int``

        :return: The RGB color representation after calibration.
        :rtype: ``RgbComponents``

        :raise ``AssertionError``: Wrong bit mode configuration
        """
        # do gamma correction first
        temp_rgb_out_r = RgbCAlgo.gamma_crt16_calc(rgb_led.r)
        temp_rgb_out_g = RgbCAlgo.gamma_crt16_calc(rgb_led.g)
        temp_rgb_out_b = RgbCAlgo.gamma_crt16_calc(rgb_led.b)

        # apply calibration and boost
        red_calibration = self.calibration_data[cal_id][RGB_RED_ID]
        green_calibration = self.calibration_data[cal_id][RGB_GREEN_ID]
        blue_calibration = self.calibration_data[cal_id][RGB_BLUE_ID]
        rgb_cal = RgbCAlgo.apply_calibration_and_boost(RgbComponents(temp_rgb_out_r, temp_rgb_out_g, temp_rgb_out_b),
                                                       [red_calibration, green_calibration, blue_calibration])

        if self.rgb_configuration.PWM_DRIVER_BIT_MODE == PwmDriverBitMode.PWM_8_BITS_MODE:
            rgb_cal.r = uint16(rgb_cal.r >> 8)
            rgb_cal.g = uint16(rgb_cal.g >> 8)
            rgb_cal.b = uint16(rgb_cal.b >> 8)
        elif self.rgb_configuration.PWM_DRIVER_BIT_MODE == PwmDriverBitMode.PWM_12_BITS_MODE:
            rgb_cal.r = uint16(rgb_cal.r >> 4)
            rgb_cal.g = uint16(rgb_cal.g >> 4)
            rgb_cal.b = uint16(rgb_cal.b >> 4)
        else:
            assert self.rgb_configuration.PWM_DRIVER_BIT_MODE == PwmDriverBitMode.PWM_16_BITS_MODE, \
                'Wrong bit mode configuration'
        # end if
        return rgb_cal
    # end def led_calibration

    def _get_led_ids_and_zone_number(self, cluster_index):
        """
        Get LED Ids and zone number from cluster index

        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``

        :return: LED Ids and zone number
        :rtype: ``tuple[list, int]``

        :raise ``AssertionError``: Invalid cluster_index
        """
        assert cluster_index in [RGBClusterId.PRIMARY, RGBClusterId.EDGE,
                                 RGBClusterId.MULTI_CLUSTER], 'Unknown cluster index'

        if cluster_index == RGBClusterId.PRIMARY:
            led_ids_to_check = list(self.rgb_configuration.MAIN_KEYS_LED_ID_RANGE)
            zone_number = 1
        elif cluster_index == RGBClusterId.EDGE:
            led_ids_to_check = list(self.rgb_configuration.EDGE_LIGHTING_LED_ID_RANGE)
            zone_number = 2
        elif cluster_index == RGBClusterId.MULTI_CLUSTER:
            led_ids_to_check = (list(self.rgb_configuration.MAIN_KEYS_LED_ID_RANGE) +
                                list(self.rgb_configuration.EDGE_LIGHTING_LED_ID_RANGE))
            zone_number = 1
        # end if
        return led_ids_to_check, zone_number
    # end def _get_led_ids_and_zone_number
# end class RgbAlgorithms


class LedDataRgbParser:
    """
    Leds data parser to validate oob rgb effect timeline or specific effect

    This class parses the LEDs rgb data to extract a usable immersive effect timeline. It can also check the validity of
    a specific effect
    """
    @unique
    class STATE(IntEnum):
        """
        RGB Led data parsing state
        """
        NOT_STARTED = auto()
        COMPLETED = auto()
    # end class STATE

    def __init__(self, timestamps, led_values, capture_duration, fw_id, layout=KeyboardInternationalLayouts.LAYOUT.US,
                 previous_immersive_lighting_state=None, trace_level=TraceLevel.NO_TRACE, trace_file_name=None,
                 plot_path=None):
        """
        :param timestamps: The timestamp list of the LED list.
        :type timestamps: ``list[float]``
        :param led_values: The LED pwm values list over time.
        :type led_values: ``list[list[RgbComponents]]``
        :param capture_duration: duration of the capture
        :type capture_duration: ``float``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param layout: keyboard international layout type - OPTIONAL
        :type layout: ``KeyboardInternationalLayouts.LAYOUT``
        :param previous_immersive_lighting_state: Previous effect before recording - OPTIONAL
        :type previous_immersive_lighting_state: ``ImmersiveLightingState`` or ``None``
        :param trace_level: Trace level of the hub - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``None``
        :param trace_file_name: Trace output of the hub - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        :param plot_path: The path where is saved the debug plot - OPTIONAL
        :type plot_path: ``str`` or ``None``

        :raise ``AssertionError``: If the firmware identifier or layout type is not in its valid range
        """
        # Trace logger subscription
        if FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_LEVEL
        # end if
        if FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_FILE_NAME
        # end if
        TRACE_LOGGER.subscribe(subscription_owner=self,
                               trace_level=trace_level,
                               trace_file_name=trace_file_name,
                               trace_name='RGB parser')

        assert fw_id in GET_RGB_CONFIGURATION_BY_ID, f"RGB configuration is not done for fw_id {fw_id}"
        self._fw_id = fw_id
        self._layout = layout
        self._configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        self._plot_path = plot_path

        self._led_ids_to_check = self._find_led_ids_to_check(cluster_index=RGBClusterId.PRIMARY,
                                                             rgb_configuration=self._configuration)
        #  Remove led_id for unmounted led
        nm_led = (self._configuration.NOT_MOUNTED_LEDS_MAIN_ALL_LAYOUT +
                  self._configuration.NOT_MOUNTED_LEDS_MAIN_US_LAYOUT)
        for led_id in nm_led:
            if led_id in self._led_ids_to_check:
                self._led_ids_to_check.remove(led_id)
            # end if
        # end for

        # Number of sample used for the comparison between reference effect and recording
        self._number_sample = self._configuration.SAMPLE_NUMBER_TO_CHECK_FOR_REFERENCE_EFFECT
        # Compute the mean value of the leds over the time
        leds_startup_reference = \
            self._configuration.OOB_RGB_START_UP_REFERENCE[self._configuration.OOB_RGB_START_UP_FIRST_INDEX:
                                                           self._configuration.OOB_RGB_START_UP_FIRST_INDEX +
                                                           self._number_sample]
        leds_active_reference = \
            self._configuration.OOB_RGB_ACTIVE_REFERENCE[self._configuration.OOB_RGB_ACTIVE_FIRST_INDEX:
                                                         self._configuration.OOB_RGB_ACTIVE_FIRST_INDEX +
                                                         self._number_sample]
        leds_passive_reference = \
            self._configuration.OOB_RGB_PASSIVE_REFERENCE[self._configuration.OOB_RGB_PASSIVE_FIRST_INDEX:
                                                          self._configuration.OOB_RGB_PASSIVE_FIRST_INDEX +
                                                          self._number_sample]
        leds_shutdown_reference = \
            self._configuration.OOB_RGB_SHUTDOWN_REFERENCE[self._configuration.OOB_RGB_SHUTDOWN_FIRST_INDEX:
                                                           self._configuration.OOB_RGB_SHUTDOWN_FIRST_INDEX +
                                                           self._number_sample]
        # Set mean value in a dictionary for all the reference OOB effect. It is these arrays that will be used as
        # reference to detect the immersive lighting effect. So it will not be a comparison led by led but a comparison
        # to the average of all mounted leds
        self.leds_mean_reference_dict = {ImmersiveLightingState.START_UP: self.compute_mean(leds_startup_reference),
                                         ImmersiveLightingState.ACTIVE: self.compute_mean(leds_active_reference),
                                         ImmersiveLightingState.PASSIVE: self.compute_mean(leds_passive_reference),
                                         ImmersiveLightingState.SHUTDOWN: self.compute_mean(leds_shutdown_reference)}

        # Compute RMS (root-mean-square) value of oob immersive lighting references
        rms_active_reference = self.compute_root_mean_square_of_mean_leds(leds_active_reference)
        rms_passive_reference = self.compute_root_mean_square_of_mean_leds(leds_passive_reference)
        rms_shutdown_reference = self.compute_root_mean_square_of_mean_leds(leds_shutdown_reference)
        rms_startup_reference = self.compute_root_mean_square_of_mean_leds(leds_startup_reference)
        self.rms_reference_dict = {ImmersiveLightingState.START_UP: rms_startup_reference,
                                   ImmersiveLightingState.ACTIVE: rms_active_reference,
                                   ImmersiveLightingState.PASSIVE: rms_passive_reference,
                                   ImmersiveLightingState.SHUTDOWN: rms_shutdown_reference,
                                   }

        # List the successive immersive lighting effect capture from the i2c or led pwm monitoring
        self.timeline = TimeLine()
        if previous_immersive_lighting_state is not None:
            self.timeline.add_effect(previous_immersive_lighting_state,
                                     start_time=0,
                                     start_index=0)
        # end if

        self._led_immersive_lighting_parsing_state = self.STATE.NOT_STARTED
        self._current_state = previous_immersive_lighting_state
        self._is_previous_state_off = False
        self._off_state_index = None
        self._timestamps = timestamps
        self._led_values = led_values
        self._capture_duration = capture_duration

        # Use for debug and plot (arrays with same length than self._timestamps) on OOB immersive lighting state machine
        self._led_mean_value_recorded = []
        self._rms_error_relative_startup = []
        self._rms_error_relative_active = []
        self._rms_error_relative_passive = []
        self._rms_error_relative_shutdown = []
    # end def __init__

    def parse_entries(self, led_spy_values, led_spy_timestamp):
        """
        Parse the buffer to create a suitable Timeline

        :param led_spy_values: The LED pwm values list over time.
        :type led_spy_values: ``list[list[RgbComponents]]``
        :param led_spy_timestamp: The timestamp list of the LED list
        :type led_spy_timestamp: ``list[float]``
        """
        previous_error = 100
        add_effect = False
        led_mean_value_recorded = []

        if led_spy_timestamp:
            # Compute the leds mean value for recorded leds
            led_mean_value_recorded = self.compute_mean(led_spy_values)
            self._led_mean_value_recorded = led_mean_value_recorded
        # end if

        for index, (mean_value, timestamp) in enumerate(zip(led_mean_value_recorded, led_spy_timestamp)):
            # Management of OFF effect
            update_off_state = False
            if all(mean_value == 0):
                if not self._is_previous_state_off:
                    self._off_state_index = index
                    self._is_previous_state_off = True
                elif (timestamp - led_spy_timestamp[self._off_state_index]) > _MIN_DURATION_OFF_EFFECT and \
                        self._current_state != ImmersiveLightingState.OFF:
                    update_off_state = True
                # end if
            elif self._is_previous_state_off:
                if (timestamp - led_spy_timestamp[self._off_state_index]) > _MIN_DURATION_OFF_EFFECT and \
                        self._current_state != ImmersiveLightingState.OFF:
                    update_off_state = True
                # end if
                self._is_previous_state_off = False
            # end if
            if update_off_state:
                if self._current_state is not None:
                    # Add end info to timeline for the previous effect
                    self.timeline.add_end_info(end_time=led_spy_timestamp[self._off_state_index],
                                               end_index=self._off_state_index)
                # end if
                # Add the new current effect to timeline
                self.timeline.add_effect(ImmersiveLightingState.OFF,
                                         start_time=led_spy_timestamp[self._off_state_index],
                                         start_index=self._off_state_index)
                # Change current state
                self._current_state = ImmersiveLightingState.OFF
            # end if

            if index < (len(led_spy_timestamp) - self._number_sample):
                # Compute rms error relative to oob references (startup, active, passive, suthdown)
                rms_error_relative_startup = self.compute_relative_root_mean_square_error_of_mean_leds(
                    led_mean_value_recorded[index:index + self._number_sample], ImmersiveLightingState.START_UP)
                rms_error_relative_active = self.compute_relative_root_mean_square_error_of_mean_leds(
                    led_mean_value_recorded[index:index + self._number_sample], ImmersiveLightingState.ACTIVE)
                rms_error_relative_passive = self.compute_relative_root_mean_square_error_of_mean_leds(
                    led_mean_value_recorded[index:index + self._number_sample], ImmersiveLightingState.PASSIVE)
                rms_error_relative_shutdown = self.compute_relative_root_mean_square_error_of_mean_leds(
                    led_mean_value_recorded[index:index + self._number_sample], ImmersiveLightingState.SHUTDOWN)
                relative_error_dict = {ImmersiveLightingState.START_UP: rms_error_relative_startup,
                                       ImmersiveLightingState.ACTIVE: rms_error_relative_active,
                                       ImmersiveLightingState.PASSIVE: rms_error_relative_passive,
                                       ImmersiveLightingState.SHUTDOWN: rms_error_relative_shutdown}
                # Find immersive lighting state where error is the smaller
                min_state = min(relative_error_dict, key=relative_error_dict.get)
                min_error = relative_error_dict[min_state]

                # For debug and plot
                self._rms_error_relative_startup.append(rms_error_relative_startup)
                self._rms_error_relative_active.append(rms_error_relative_active)
                self._rms_error_relative_passive.append(rms_error_relative_passive)
                self._rms_error_relative_shutdown.append(rms_error_relative_shutdown)

                if min_error <= _10_PERCENT:
                    if min_error > previous_error:
                        # A local minimum error during the previous step is detected
                        if self._current_state != min_state:
                            if self._current_state is not None:
                                # Add end info to timeline for the previous effect
                                self.timeline.add_end_info(end_time=led_spy_timestamp[index-1], end_index=index-1)
                            # end if
                            # Add the new current effect to timeline
                            self.timeline.add_effect(min_state,
                                                     start_time=led_spy_timestamp[index - 1],
                                                     start_index=index - 1)
                            # Change current state
                            self._current_state = min_state
                            add_effect = False
                        # end if
                    else:
                        add_effect = True
                    # end if
                    previous_error = min_error
                else:
                    if add_effect:
                        if self._current_state != min_state:
                            if self._current_state is not None:
                                # Add end info to timeline for the previous effect
                                self.timeline.add_end_info(end_time=led_spy_timestamp[index-1], end_index=index-1)
                            # end if
                            # Add the new current effect to timeline
                            self.timeline.add_effect(min_state,
                                                     start_time=led_spy_timestamp[index - 1],
                                                     start_index=index - 1)
                            # Change current state
                            self._current_state = min_state
                        # end if
                        add_effect = False
                    # end if
                    previous_error = 100
                # end if
            # end if
        # end for

        # Add end info to timeline for the last effect with management of OFF leds
        if self._is_previous_state_off:
            if (self._capture_duration - led_spy_timestamp[self._off_state_index]) > _MIN_DURATION_OFF_EFFECT and \
                    self._current_state != ImmersiveLightingState.OFF:
                if self._current_state is not None:
                    # Add end info to timeline for the previous effect
                    self.timeline.add_end_info(end_time=led_spy_timestamp[self._off_state_index],
                                               end_index=self._off_state_index)
                # end if
                # Add the new current effect to timeline
                self.timeline.add_effect(ImmersiveLightingState.OFF,
                                         start_time=led_spy_timestamp[self._off_state_index],
                                         start_index=self._off_state_index)
                # Change current state
                self._current_state = ImmersiveLightingState.OFF
            # end if
        # end if
        if self.timeline.effects:
            self.timeline.add_end_info(end_time=self._capture_duration, end_index=len(led_spy_timestamp))
        # end if
    # end def parse_entries

    def is_immersive_lighting_correct(self, immersive_lighting_state, exact_duration=None, minimum_duration=None,
                                      last_effect=False):
        """
        Verify immersive lighting is correct (state and duration)

        Note: Only works with OOB effect

        :param immersive_lighting_state: immersive lighting state to check
        :type immersive_lighting_state: ``ImmersiveLightingState``
        :param exact_duration: fast blink state exact duration in ms to enforce (default is 3 minutes) - OPTIONAL
        :type exact_duration: ``int`` or ``None``
        :param minimum_duration: fast blink state minimum duration in ms to verify
                                 (exclusive with exact_duration) - OPTIONAL
        :type minimum_duration: ``int`` or ``None``
        :param last_effect: Flag indicating if we expect that it is the last effect - OPTIONAL
        :type last_effect: ``bool``

        :return: Flag indicating if the immersive lighting matches is correct (ImmersiveLightingState and duration)
        :rtype: ``bool``
        """
        status = True

        if self._led_immersive_lighting_parsing_state == self.STATE.NOT_STARTED:
            # Parse PWM led entries to immersive lighting timeline
            self.parse_entries(led_spy_values=self._led_values, led_spy_timestamp=self._timestamps)

            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=str(self.timeline),
                                   trace_level=TraceLevel.DEBUG)
            self._led_immersive_lighting_parsing_state = self.STATE.COMPLETED
        # end if

        next_effect = self.timeline.get_next_effect()
        if next_effect is None:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message='No effect detected',
                                   trace_level=TraceLevel.ERROR)
            return False
        # end if

        # Check immersive lighting state
        TRACE_LOGGER.log_trace(subscription_owner=self,
                               message=f'The state is :  {IMMERSIVE_LIGHTING_STATE_STR_MAP[next_effect.type]}, '
                                       f'the duration is : {next_effect.duration} seconds',
                               trace_level=TraceLevel.DEBUG)
        if next_effect.type != immersive_lighting_state:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f'Wrong scheme type: {IMMERSIVE_LIGHTING_STATE_STR_MAP[next_effect.type]} '
                                           f'!= {IMMERSIVE_LIGHTING_STATE_STR_MAP[immersive_lighting_state]}',
                                   trace_level=TraceLevel.ERROR)
            status = False
        # end if

        # Check duration
        if exact_duration is not None:
            is_duration_error_short = (exact_duration * _10_PERCENT < _MIN_ACCEPTABLE_TIMING_ERROR)
            error = (next_effect.duration - exact_duration)/exact_duration
            if (is_duration_error_short and abs(next_effect.duration - exact_duration) > _MIN_ACCEPTABLE_TIMING_ERROR) \
                    or (not is_duration_error_short and abs(error) > _10_PERCENT):
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message='the exact duration of the effect is not correct, '
                                               f'expected={exact_duration}, obtained={next_effect.duration}',
                                       trace_level=TraceLevel.ERROR)
                status = False
            # end if
        elif minimum_duration is not None:
            # Check minimum duration
            if next_effect.duration < (minimum_duration * (1 + _10_PERCENT)):
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message='the minimum duration of the effect is not correct, '
                                               f'expected={minimum_duration}, obtained={next_effect.duration}',
                                       trace_level=TraceLevel.ERROR)
                status = False
            # end if
        # end if

        # Check last effect
        if last_effect:
            if self.timeline.get_next_effect() is not None:
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f'the effect {IMMERSIVE_LIGHTING_STATE_STR_MAP[next_effect.type]} is '
                                               'not the last effect detected',
                                       trace_level=TraceLevel.ERROR)
                status = False
            # end if
        # end if

        # save plot
        if not status or FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_LEVEL > TraceLevel.DEBUG:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f'A plot is saved at path : {self._plot_path}',
                                   trace_level=TraceLevel.INFO)

            self.save_plot_oob_immersive_lighting_timeline()
        # end if
        return status
    # end def is_immersive_lighting_correct

    def save_plot_oob_immersive_lighting_timeline(self):
        """
        Save on a plot all necessary information for debugging immersive lighting timeline
        """
        # convert timeline to state array
        state_array = []
        state_array_timestamp = []
        for effect in self.timeline.effects:
            state_array.append(effect.type)
            state_array_timestamp.append(effect.start_time)
            state_array.append(effect.type)
            state_array_timestamp.append(effect.end_time)
        # end for

        if len(self._timestamps) == 0:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message='No LED intensity data was recorded by LED spy module',
                                   trace_level=TraceLevel.ERROR)
        else:
            pwm_led_unit = PWM_DRIVER_BIT_MODE_STR_MAP[self._configuration.PWM_DRIVER_BIT_MODE]
            title = self._plot_path.split(sep='/')[-1].split(sep='.')[-2]
            f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex='all', figsize=(14, 14))
            plt.suptitle(f'{title}\n')
            # ax1
            ax1.plot(self._timestamps, self._led_mean_value_recorded, '+-')
            ax1.set_title('Mean of all the immersive LEDs (PWM values)')
            ax1.set_ylabel(f'Mean PWM LED intensity ({pwm_led_unit})')
            ax1.set_xlabel('time (s)')
            # ax2
            if len(self._timestamps) > self._number_sample:
                ax2.plot(self._timestamps, (_10_PERCENT * 100) * ones(len(self._timestamps)), color='r',
                         label='10% error threshold')
                ax2.plot(self._timestamps[0:-self._number_sample], 100 * array(self._rms_error_relative_active), '+-',
                         label='rrmse active')
                ax2.plot(self._timestamps[0:-self._number_sample], 100 * array(self._rms_error_relative_passive), '+-',
                         label='rrmse passive')
                ax2.plot(self._timestamps[0:-self._number_sample], 100 * array(self._rms_error_relative_startup), '+-',
                         label='rrmse startup')
                ax2.plot(self._timestamps[0:-self._number_sample], 100 * array(self._rms_error_relative_shutdown), '+-',
                         label='rrmse shutdown')
                ax2.legend()
            # end if
            ax2.set_ylim(0, _10_PERCENT * 100 * 2)
            ax2.set_title(f'Relative RMS error between (Mean PWM LED record) and (OBB reference) on a windows of '
                          f'{self._number_sample} samples  ')
            ax2.set_ylabel('relative RMS error (%)')
            ax2.set_xlabel('time (s)')
            # ax3
            ax3.plot(state_array_timestamp, state_array)
            ax3.set_title('Immersive lighting state detected by the parser')
            ax3.set_ylabel('State')
            ax3.set_xlabel('time (s)')
            ax3.set_yticks([ImmersiveLightingState.START_UP.value,
                            ImmersiveLightingState.ACTIVE.value,
                            ImmersiveLightingState.PASSIVE.value,
                            ImmersiveLightingState.SHUTDOWN.value,
                            ImmersiveLightingState.OFF.value,
                            ImmersiveLightingState.UNDETERMINED.value],
                           labels=['Startup', 'Active', 'Passive', 'shutdown', 'off', 'undetermined'])
            # ax4
            ax4.plot(self._timestamps[0:-1], array(self._timestamps[1::]) - array(self._timestamps[0:-1]), '+-')
            ax4.set_title('timestamp difference between sample n+1 and n')
            ax4.set_ylabel(f'delta timestamp (s)')
            ax4.set_xlabel('time (s)')
            ax4.set_ylim([0, max(array(self._timestamps[1::]) - array(self._timestamps[0:-1])) * 1.1])
            if self._plot_path is not None:
                plt.savefig(fname=self._plot_path)
            # end if
        # end if
    # end def save_plot_oob_immersive_lighting_timeline

    def compute_mean(self, reference_leds):
        """
        Compute the average value of all the leds in ``self._led_ids_to_check`` at each timestamp

        :param reference_leds: immersive lighting state to check
        :type reference_leds: ``list[list[RgbComponents]]``

        :return: Average value of all the leds at each timestamp
        :rtype: ``ndarray``
        """
        reference_leds_red = []
        reference_leds_green = []
        reference_leds_blue = []
        for leds in reference_leds:
            reference_leds_red.append([temp.r for temp in leds])
            reference_leds_green.append([temp.g for temp in leds])
            reference_leds_blue.append([temp.b for temp in leds])
        # end for
        leds_active_reference_red = array(reference_leds_red)
        leds_active_reference_red = leds_active_reference_red[:, self._led_ids_to_check]
        leds_active_reference_green = array(reference_leds_green)
        leds_active_reference_green = leds_active_reference_green[:, self._led_ids_to_check]
        leds_active_reference_blue = array(reference_leds_blue)
        leds_active_reference_blue = leds_active_reference_blue[:, self._led_ids_to_check]

        led_mean_active_reference = (mean(leds_active_reference_red, axis=1) +
                                     mean(leds_active_reference_green, axis=1) +
                                     mean(leds_active_reference_blue, axis=1)) / 3
        return led_mean_active_reference
    # end def compute_mean

    def compute_root_mean_square_of_mean_leds(self, reference_leds):
        """
        Compute the root-mean-square value of average value of all the leds in ``self._led_ids_to_check``

        :param reference_leds: immersive lighting state to check
        :type reference_leds: ``list[list[RgbComponents]]``

        :return: Root-mean-square value of average leds signal
        :rtype: ``float``
        """
        _led_mean_active_reference = self.compute_mean(reference_leds)

        return sqrt(mean(_led_mean_active_reference ** 2))
    # end def compute_root_mean_square_of_mean_leds

    def compute_relative_root_mean_square_error_of_mean_leds(self, led_mean_value_recorded,
                                                             immersive_lighting_reference):
        """
        Compute the relative RMS value of the error between signals (RRMSE) - Very sensitive to the time lag of signals
        (delay), but very good indicator of similarity:
        https://www.maplesoft.com/support/help/maple/view.aspx?path=SignalProcessing%2FRootMeanSquareError
        https://www.analyticsvidhya.com/blog/2021/10/evaluation-metric-for-regression-models/#:~:text=Relative%20Root%20Mean%20Square%20Error,to%20compare%20different%20measurement%20techniques


        :param led_mean_value_recorded: average value of the recording
        :type led_mean_value_recorded: ``ndarray``
        :param immersive_lighting_reference: immersive lighting state used as reference array
        :type immersive_lighting_reference: ``ImmersiveLightingState``

        :return: relative root-mean-square error between leds average recording and reference
        :rtype: ``float``

        """
        led_reference = self.leds_mean_reference_dict[immersive_lighting_reference]
        rms_reference = self.rms_reference_dict[immersive_lighting_reference]

        rms_error = sqrt(mean((led_mean_value_recorded - led_reference) ** 2))
        rms_error_relative = rms_error / rms_reference

        return rms_error_relative
    # end def compute_relative_root_mean_square_error_of_mean_leds

    def is_disabled_effect(self, led_spy_values, led_spy_timestamp, cluster_index, excluded_indicators=None):
        """
        Check if the rgb effect is disabled

        :param led_spy_values: The LED pwm values list over time.
        :type led_spy_values: ``list[list[RgbComponents]]``
        :param led_spy_timestamp: The timestamp list of the LED list
        :type led_spy_timestamp: ``list[float]``
        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
                 check - OPTIONAL
        :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``

        :return: Flag indicating if the rgb effect is disabled on the cluster
        :rtype: ``bool``
        """
        status = True
        self._led_ids_to_check = self._find_led_ids_to_check(
            cluster_index=cluster_index, rgb_configuration=self._configuration, excluded_indicators=excluded_indicators)

        expected_led_values_over_time = []
        for temp in led_spy_values:
            expected_led_values_over_time.append(
                [RgbComponents(r=uint8(0), g=uint8(0), b=uint8(0)) for _ in temp])
        # end for

        if expected_led_values_over_time:
            status = self.is_two_rgb_arrays_identical(
                recorded_led_values_over_time=array(led_spy_values),
                expected_led_values_over_time=array(expected_led_values_over_time),
                led_spy_timestamp=led_spy_timestamp)
        # end if
        return status
    # end def is_disabled_effect

    def is_fixed_effect(self, test_case, fw_id, led_spy_values, led_spy_timestamp, cluster_index,
                        red_value, green_value, blue_value, calibration_data, brightness=None, excluded_indicators=None,
                        check_last_packet_only=False, layout=KeyboardInternationalLayouts.LAYOUT.US):
        """
        Check if the fixed rgb effect is correct (rgb values and LED Id)

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param led_spy_values: The LED pwm values list over time.
        :type led_spy_values: ``list[list[RgbComponents]]``
        :param led_spy_timestamp: The timestamp list of the LED list
        :type led_spy_timestamp: ``list[float]``
        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param red_value: Red value of RGB color model
        :type red_value: ``int``
        :param green_value: Green value of RGB color model
        :type green_value: ``int``
        :param blue_value: Blue value of RGB color model
        :type blue_value: ``int``
        :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
        :type calibration_data: ``list[list[int, int, int]]``
        :param brightness: Brightness of LED - OPTIONAL
        :type brightness: ``int | None``
        :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
         check - OPTIONAL
        :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``
        :param check_last_packet_only: Flag indicating that the checker function will check the last I2C packet of
         MCU to LED driver IC - OPTIONAL
        :type check_last_packet_only: ``bool``
        :param layout: keyboard international layout type - OPTIONAL
        :type layout: ``KeyboardInternationalLayouts.LAYOUT``

        :return: Flag indicating if the rgb Fixed effect is correct on the cluster
        :rtype: ``bool``

        :raise ``AssertionError``: If the input brightness is not in the valid range(MinBrightness, MaxBrightness)
        """
        if brightness is not None:
            config = test_case.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL
            test_case.assertIn(member=brightness, container=range(config.F_MinBrightness, config.F_MaxBrightness + 1),
                               msg="The input brightness is not in the valid range: "
                                   f"range({config.F_MinBrightness}, {config.F_MaxBrightness})")
            brightness_percentage = ((brightness - config.F_MinBrightness) /
                                     (config.F_MaxBrightness - config.F_MinBrightness))
        else:
            brightness_percentage = 1
        # end if

        rgb_algo = RgbAlgorithms(fw_id=fw_id, calibration_data=calibration_data, layout=layout)
        rgb_algo.fixed_effect(timestamps=led_spy_timestamp, cluster_index=cluster_index, red_value=red_value,
                              green_value=green_value, blue_value=blue_value, brightness=brightness_percentage * 100)
        self._led_ids_to_check = self._find_led_ids_to_check(
            cluster_index=cluster_index, rgb_configuration=self._configuration, excluded_indicators=excluded_indicators)

        if not led_spy_values:
            status = False
        else:
            status = self.is_two_rgb_arrays_identical(
                recorded_led_values_over_time=array(led_spy_values),
                expected_led_values_over_time=array(rgb_algo.led_algo_values_over_time),
                check_last_packet_only=check_last_packet_only,
                led_spy_timestamp=led_spy_timestamp)
        # end if
        return status
    # end def is_fixed_effect

    def is_pulsing_breathing_effect(self, fw_id, led_spy_values, led_spy_timestamp, cluster_index, red_value,
                                    green_value, blue_value, period_msb, period_lsb, brightness, calibration_data,
                                    excluded_indicators=None, layout=KeyboardInternationalLayouts.LAYOUT.US):
        """
        Check if the pulsing/breathing rgb effect is correct (rgb values, period, brightness and LED Id)

        :param fw_id: The FW name
        :type fw_id: ``str``
        :param led_spy_values: The LED pwm values list over time.
        :type led_spy_values: ``list[list[RgbComponents]]``
        :param led_spy_timestamp: The timestamp list of the LED list
        :type led_spy_timestamp: ``list[float]``
        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param red_value: Red value of RGB color model
        :type red_value: ``int``
        :param green_value: Green value of RGB color model
        :type green_value: ``int``
        :param blue_value: Blue value of RGB color model
        :type blue_value: ``int``
        :param period_msb: MSB of the effect period
        :type period_msb: ``int``
        :param period_lsb: LSB of the effect period
        :type period_lsb: ``int``
        :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100, >100 is clamped to 100
        :type brightness: ``int``
        :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
        :type calibration_data: ``list[list[int, int, int]]``
        :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
         check - OPTIONAL
        :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``
        :param layout: keyboard international layout type - OPTIONAL
        :type layout: ``KeyboardInternationalLayouts.LAYOUT``

        :return: Flag indicating if the rgb pulsing/breathing effect is correct on the cluster
        :rtype: ``bool``
        """
        # Compute the expected LEDs values from reference algorithm
        rgb_algo = RgbAlgorithms(fw_id=fw_id, calibration_data=calibration_data, layout=layout)
        rgb_algo.pulsing_breathing_effect(timestamps=led_spy_timestamp, cluster_index=cluster_index,
                                          red_value=red_value,
                                          green_value=green_value, blue_value=blue_value, period_msb=period_msb,
                                          period_lsb=period_lsb, brightness=brightness)

        self._led_ids_to_check = self._find_led_ids_to_check(
            cluster_index=cluster_index, rgb_configuration=self._configuration, excluded_indicators=excluded_indicators)

        if not led_spy_values:
            status = False
        else:
            status = self.is_two_rgb_arrays_identical(
                recorded_led_values_over_time=array(led_spy_values),
                expected_led_values_over_time=array(rgb_algo.led_algo_values_over_time),
                led_spy_timestamp=led_spy_timestamp)
        # end if
        return status
    # end def is_pulsing_breathing_effect

    def is_color_cycling_configurable_s_effect(self, fw_id, led_spy_values, led_spy_timestamp, cluster_index,
                                               saturation, period_msb, period_lsb, brightness, calibration_data,
                                               excluded_indicators=None, layout=KeyboardInternationalLayouts.LAYOUT.US):
        """
        Check if the color cycling configurable saturation rgb effect is correct (saturation value, period, brightness
         and LED Id)

        :param fw_id: The FW name
        :type fw_id: ``str``
        :param led_spy_values: The LED pwm values list over time.
        :type led_spy_values: ``list[list[RgbComponents]]``
        :param led_spy_timestamp: The timestamp list of the LED list
        :type led_spy_timestamp: ``list[float]``
        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param saturation: Saturation modulator of HSV color representation
        :type saturation: ``int``
        :param period_msb: MSB of the effect period
        :type period_msb: ``int``
        :param period_lsb: LSB of the effect period
        :type period_lsb: ``int``
        :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100, >100 is clamped to 100
        :type brightness: ``int``
        :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2
        :type calibration_data: ``list[list[int, int, int]]``
        :param excluded_indicators:  list of LED indicators that are not taken into account for the rgb effect
         check - OPTIONAL
        :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``
        :param layout: keyboard international layout type - OPTIONAL
        :type layout: ``KeyboardInternationalLayouts.LAYOUT``

        :return: Flag indicating if the rgb color cycling effect is correct on the cluster
        :rtype: ``bool``
        """
        rgb_algo = RgbAlgorithms(fw_id=fw_id, calibration_data=calibration_data, layout=layout)
        rgb_algo.color_cycling_configurable_s_effect(timestamps=led_spy_timestamp, cluster_index=cluster_index,
                                                     saturation=saturation, period_msb=period_msb,
                                                     period_lsb=period_lsb,
                                                     brightness=brightness)

        self._led_ids_to_check = self._find_led_ids_to_check(
            cluster_index=cluster_index, rgb_configuration=self._configuration, excluded_indicators=excluded_indicators)

        if not led_spy_values:
            status = False
        else:
            status = self.is_two_rgb_arrays_identical(
                recorded_led_values_over_time=array(led_spy_values),
                expected_led_values_over_time=array(rgb_algo.led_algo_values_over_time),
                led_spy_timestamp=led_spy_timestamp)
        # end if
        return status
    # end def is_color_cycling_configurable_s_effect

    def is_two_rgb_arrays_identical(self, recorded_led_values_over_time, expected_led_values_over_time,
                                    led_spy_timestamp, check_last_packet_only=False):
        """
        Check if two arrays are almost identical with a tolerance of 20 % on the relative RMS value of the error between
        signals. The relative RMS value of the error between signals (RRMSE) - Very sensitive to the time lag of signals
        (delay), but very good indicator of similarity, that why we choose an error margin of 20%
        RRMSE documentation :
        https://www.maplesoft.com/support/help/maple/view.aspx?path=SignalProcessing%2FRootMeanSquareError
        https://www.analyticsvidhya.com/blog/2021/10/evaluation-metric-for-regression-models/#:~:text=Relative%20Root%20Mean%20Square%20Error,to%20compare%20different%20measurement%20techniques

        :param recorded_led_values_over_time: The recorded rgb value over the time
        :type recorded_led_values_over_time: ``numpy.ndarray``
        :param expected_led_values_over_time: The expected rgb value over the time
        :type expected_led_values_over_time: ``numpy.ndarray``
        :param led_spy_timestamp: The timestamp list of the LED list -
        :type led_spy_timestamp: ``list[float]``
        :param check_last_packet_only: Flag indicating that the checker function will check the last I2C packet of
         MCU to LED driver IC - OPTIONAL
        :type check_last_packet_only: ``bool``

        :return: Flag indicating if the two arrays are almost identical
        :rtype: ``bool``
        """
        status = True

        maximum_rmmse = -1
        maximum_rmmse_led_id = None
        maximum_rmmse_color_index = RGB_RED_ID

        for i in self._led_ids_to_check:
            expected_rgb = expected_led_values_over_time[:, i]
            expected_red = array([temp.r for temp in expected_rgb] if not check_last_packet_only
                                 else [expected_rgb[-1].r], dtype=float)
            expected_green = array([temp.g for temp in expected_rgb] if not check_last_packet_only
                                   else [expected_rgb[-1].g], dtype=float)
            expected_blue = array([temp.b for temp in expected_rgb] if not check_last_packet_only
                                  else [expected_rgb[-1].b], dtype=float)

            recorded_rgb = recorded_led_values_over_time[:, i]
            recorded_red = array([temp.r for temp in recorded_rgb] if not check_last_packet_only
                                 else [recorded_rgb[-1].r], dtype=float)
            recorded_green = array([temp.g for temp in recorded_rgb] if not check_last_packet_only
                                   else [recorded_rgb[-1].g], dtype=float)
            recorded_blue = array([temp.b for temp in recorded_rgb] if not check_last_packet_only
                                  else [recorded_rgb[-1].b], dtype=float)

            rms_expected_red = sqrt((expected_red ** 2).mean())
            rms_expected_green = sqrt((expected_green ** 2).mean())
            rms_expected_blue = sqrt((expected_blue ** 2).mean())

            rms_recorded_red = sqrt((recorded_red ** 2).mean())
            rms_recorded_green = sqrt((recorded_green ** 2).mean())
            rms_recorded_blue = sqrt((recorded_blue ** 2).mean())

            rms_error_red = sqrt(((recorded_red - expected_red) ** 2).mean())
            rms_error_green = sqrt(((recorded_green - expected_green) ** 2).mean())
            rms_error_blue = sqrt(((recorded_blue - expected_blue) ** 2).mean())

            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f'led_id {i} : \n'
                        f'  expected rms (RGB) = ({rms_expected_red:.1f},{rms_expected_green:.1f},'
                        f'{rms_expected_blue:.1f})\n'
                        f'  recorded rms (RGB) = ({rms_recorded_red:.1f},{rms_recorded_green:.1f},'
                        f'{rms_recorded_blue:.1f})\n'
                        f'  relative rms error (RGB)= ({rms_error_red:.1f},{rms_error_green:.1f},'
                        f'{rms_error_blue:.1f})\n'
                        f'  relative rms error (%) (RGB)= ({(rms_error_red/ rms_expected_red * 100):.1f},'
                        f'{(rms_error_green/ rms_expected_green * 100):.1f},'
                        f'{(rms_error_blue/ rms_expected_blue * 100):.1f})',
                trace_level=TraceLevel.DEBUG)

            # Check on red value
            if rms_expected_red == 0:
                if rms_error_red != 0:
                    TRACE_LOGGER.log_trace(subscription_owner=self,
                                           message=f'Error on red value for led_id {i}, expected : {rms_expected_red}, '
                                                   f'obtained {rms_error_red}',
                                           trace_level=TraceLevel.ERROR)
                    status = False
                # end if
            else:
                is_tolerance_error_short = (rms_expected_red * _20_PERCENT < _MIN_ACCEPTABLE_ABSOLUTE_ERROR)
                if (is_tolerance_error_short and rms_error_red > _MIN_ACCEPTABLE_ABSOLUTE_ERROR) or \
                        (not is_tolerance_error_short and (rms_error_red / rms_expected_red) > _20_PERCENT):
                    TRACE_LOGGER.log_trace(subscription_owner=self,
                                           message=f'Error on red value for led_id {i}, rms error = '
                                                   f'{rms_error_red / rms_expected_red * 100} % ',
                                           trace_level=TraceLevel.ERROR)
                    status = False
                # end if
            # end if
            if maximum_rmmse < rms_error_red:
                maximum_rmmse = rms_error_red
                maximum_rmmse_led_id = i
                maximum_rmmse_color_index = RGB_RED_ID
            # end if

            # Check on green value
            if rms_expected_green == 0:
                if rms_error_green != 0:
                    TRACE_LOGGER.log_trace(subscription_owner=self,
                                           message=f'Error on blue value for led_id {i}, expected : '
                                                   f'{rms_expected_green} obtained {rms_error_green}',
                                           trace_level=TraceLevel.ERROR)
                    status = False
                # end if
            else:
                is_tolerance_error_short = (rms_expected_green * _20_PERCENT < _MIN_ACCEPTABLE_ABSOLUTE_ERROR)
                if (is_tolerance_error_short and rms_error_green > _MIN_ACCEPTABLE_ABSOLUTE_ERROR) or \
                        (not is_tolerance_error_short and (rms_error_green / rms_expected_green) > _20_PERCENT):
                    TRACE_LOGGER.log_trace(subscription_owner=self,
                                           message=f'Error on green value for led_id {i}, rms error = '
                                                   f'{rms_error_green / rms_expected_green * 100} % ',
                                           trace_level=TraceLevel.ERROR)
                    status = False
                # end if
            # end if
            if maximum_rmmse < rms_error_green:
                maximum_rmmse = rms_error_green
                maximum_rmmse_led_id = i
                maximum_rmmse_color_index = RGB_GREEN_ID
            # end if

            # Check on blue value
            if rms_expected_blue == 0:
                if rms_error_blue != 0:
                    TRACE_LOGGER.log_trace(subscription_owner=self,
                                           message=f'Error on blue value for led_id {i}, expected : '
                                                   f'{rms_expected_blue}, obtained {rms_error_blue}',
                                           trace_level=TraceLevel.ERROR)
                    status = False
                # end if
            else:
                is_tolerance_error_short = (rms_expected_blue * _20_PERCENT < _MIN_ACCEPTABLE_ABSOLUTE_ERROR)
                if (is_tolerance_error_short and rms_error_blue > _MIN_ACCEPTABLE_ABSOLUTE_ERROR) or \
                        (not is_tolerance_error_short and (rms_error_blue / rms_expected_blue) > _20_PERCENT):
                    TRACE_LOGGER.log_trace(subscription_owner=self,
                                           message=f'Error on blue value for led_id {i}, rms error = '
                                                   f'{rms_error_blue / rms_expected_blue * 100} % ',
                                           trace_level=TraceLevel.ERROR)
                    status = False
                # end if
            # end if
            if maximum_rmmse < rms_error_blue:
                maximum_rmmse = rms_error_blue
                maximum_rmmse_led_id = i
                maximum_rmmse_color_index = RGB_BLUE_ID
            # end if
        # end for

        # save plot
        if self._plot_path and (not status or FORCE_AT_CREATION_ALL_RGB_PARSER_TRACE_LEVEL > TraceLevel.DEBUG):
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f'A plot of the waveform is ... ')

            expected_rgb = expected_led_values_over_time[:, maximum_rmmse_led_id]
            recorded_rgb = recorded_led_values_over_time[:, maximum_rmmse_led_id]
            if maximum_rmmse_color_index == RGB_RED_ID:
                expected_led_value = array([temp.r for temp in expected_rgb], dtype=float)
                recorded_led_value = array([temp.r for temp in recorded_rgb], dtype=float)
            elif maximum_rmmse_color_index == RGB_GREEN_ID:
                expected_led_value = array([temp.g for temp in expected_rgb], dtype=float)
                recorded_led_value = array([temp.g for temp in recorded_rgb], dtype=float)
            else:
                expected_led_value = array([temp.b for temp in expected_rgb], dtype=float)
                recorded_led_value = array([temp.b for temp in recorded_rgb], dtype=float)
            # end if
            self.save_plot_rgb_effect_comparison(
                led_spy_timestamp=led_spy_timestamp, expected_led_value=expected_led_value,
                recorded_led_value=recorded_led_value, led_id=maximum_rmmse_led_id)
        # end if
        return status
    # end def is_two_rgb_arrays_identical

    def save_plot_rgb_effect_comparison(self, led_spy_timestamp, expected_led_value, recorded_led_value, led_id):
        """
        Save on a plot all necessary information for debugging rgb effect between expected and recorded

        :param led_spy_timestamp: The timestamp list of the LED list
        :type led_spy_timestamp: ``list[float]``
        :param expected_led_value: The expected rgb value over the time
        :type expected_led_value: ``numpy.ndarray``
        :param recorded_led_value: The expected rgb value over the time
        :type recorded_led_value: ``numpy.ndarray``
        :param led_id: The LED index to be display on plot title
        :type led_id: ``int``
        """
        rms_expected = sqrt((expected_led_value ** 2).mean())
        rms_recorded = sqrt((recorded_led_value ** 2).mean())
        relative_rms_error = sqrt(((recorded_led_value - expected_led_value) ** 2).mean()) / rms_expected * 100

        pwm_led_unit = PWM_DRIVER_BIT_MODE_STR_MAP[self._configuration.PWM_DRIVER_BIT_MODE]
        f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='all', figsize=(10, 10))
        if self._plot_path is not None:
            title = self._plot_path.split(sep='/')[-1].split(sep='.')[-2]
            plt.suptitle(f'{title}\n'
                         f'LED intensity over time for led_id = {led_id}')
        # end if
        # ax1
        ax1.plot(led_spy_timestamp, expected_led_value, '+-', label=f'expected, RMS={rms_expected:.1f}')
        ax1.plot(led_spy_timestamp, recorded_led_value, '+-', label=f'recorded, RMS={rms_recorded:.1f}')
        ax1.legend()
        ax1.set_title('PWM LED intensity waveform')
        ax1.set_ylabel(f'PWM LED intensity ({pwm_led_unit})')
        ax1.set_xlabel('time (s)')
        # ax2
        ax2.plot(led_spy_timestamp, recorded_led_value - expected_led_value, '+-')
        ax2.set_title(f'PWM LED intensity difference between recorded and expected, '
                      f'relative RMS error ={relative_rms_error:.1f} %')
        ax2.set_ylabel('intensity difference')
        ax2.set_xlabel('time (s)')
        # ax3
        if len(led_spy_timestamp) > 1:
            ax3.plot(led_spy_timestamp[0:-1], array(led_spy_timestamp[1::]) - array(led_spy_timestamp[0:-1]), '+-')
            ax3.set_title('timestamp difference between sample n+1 and n')
            ax3.set_ylabel('delta timestamp (s)')
            ax3.set_xlabel('time (s)')
            ax3.set_ylim([0, max(array(led_spy_timestamp[1::]) - array(led_spy_timestamp[0:-1])) * 1.1])
        # end if
        if self._plot_path is not None:
            plt.savefig(fname=self._plot_path)
        # end if
    # end def save_plot_rgb_effect_comparison

    @staticmethod
    def _find_led_ids_to_check(cluster_index, rgb_configuration, excluded_indicators=None):
        """
        Find the LED Ids we want to check on a cluster, removing LED Indicators we don't want to check or that are not
        affect by rgb effect

        :param cluster_index: RGB cluster index
        :type cluster_index: ``int``
        :param rgb_configuration: RGB configuration
        :type rgb_configuration: ``pyraspi.services.kosmos.config.rgbconfigurations.RgbConfigurationMixin``
        :param excluded_indicators: list of LED indicators that are not taken into account for the rgb effect - OPTIONAL
        :type excluded_indicators: ``list[RgbLedIndicator]`` or ``None``

        :return: the LED Ids to check
        :rtype: ``list[int]``

        :raise ``AssertionError``: If cluster_index is unknown
        """
        assert cluster_index in [RGBClusterId.PRIMARY, RGBClusterId.EDGE,
                                 RGBClusterId.MULTI_CLUSTER], 'Unknown cluster index'

        # Find led ids to check
        if cluster_index == RGBClusterId.PRIMARY:
            led_ids_to_check = list(rgb_configuration.MAIN_KEYS_LED_ID_RANGE)
        elif cluster_index == RGBClusterId.EDGE:
            led_ids_to_check = list(rgb_configuration.EDGE_LIGHTING_LED_ID_RANGE)
        elif cluster_index == RGBClusterId.MULTI_CLUSTER:
            led_ids_to_check = (list(rgb_configuration.MAIN_KEYS_LED_ID_RANGE) +
                                list(rgb_configuration.EDGE_LIGHTING_LED_ID_RANGE))
        # end if

        # Remove LED Indicators we don't want to check or that are not affect by rgb effect
        if excluded_indicators is None:
            excluded_indicators = []
        # end if
        excluded_indicators = excluded_indicators + rgb_configuration.INDICATOR_NOT_AFFECTED_BY_RGB_EFFECT
        excluded_indicators = list(set(excluded_indicators))
        for indicator in excluded_indicators:
            if rgb_configuration.INDICATOR_TO_LED_ID[indicator] in led_ids_to_check:
                led_ids_to_check.remove(rgb_configuration.INDICATOR_TO_LED_ID[indicator])
            # end if
        # end for
        return led_ids_to_check
    # end def _find_led_ids_to_check
# end class LedDataRgbParser

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
