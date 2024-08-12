#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.i2c.i2cbacklightparser.py
:brief: Backlight I2C data parser Class
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/10/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from enum import Enum
from enum import IntEnum
from enum import auto
from enum import unique
from sys import stdout
from warnings import warn

from numpy import array
from numpy import sqrt
from numpy import uint16

from pyhid.hidpp.features.common.backlight import Backlight
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.config.backlightconfiguration import GET_BACKLIGHT_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.i2c.rgbalgorithms.rgbalgoc import RgbCAlgo
from pyraspi.services.kosmos.i2c.rgbalgorithms.rgbalgoc import RgbComponents

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
# 5% Tolerance
_5_PERCENT = 5 / 100
# 20% Tolerance for wave and breathing effects timing verification
_20_PERCENT = 20 / 100
_UPPER_STATIC_EFFECT_MARGIN = 1.5
_LOWER_STATIC_EFFECT_MARGIN = 1.5
_MIN_DURATION_STATIC_EFFECT = 0.5  # in second
_MIN_DURATION_UNDETERMINED = 0.1  # in second
_MIN_ACCEPTABLE_TIMING_ERROR = 0.3  # in second
_MIN_PERIOD_BREATHING_EFFECT = 0.5  # in second
_MAX_FADE_IN_DURATION = 2  # in second
# On random effect the number of LEDs ON is not always exactly the same because one LED goes off every 300 ms while
# another lights up, so during this transition there may be 1 more (or less) LED ON
_RANDOM_EFFECT_LED_ON_NUMBER_MARGIN = 1


@unique
class BacklightEffectType(IntEnum):
    """
    Backlight types
    """
    STATIC_EFFECT = Backlight.BacklightEffect.STATIC_EFFECT.value
    NONE_EFFECT = Backlight.BacklightEffect.NONE_EFFECT.value
    BREATHING_EFFECT = Backlight.BacklightEffect.BREATHING_LIGHT_EFFECT.value
    CONTRAST_EFFECT = Backlight.BacklightEffect.CONTRAST_EFFECT.value
    REACTION_EFFECT = Backlight.BacklightEffect.REACTION_EFFECT.value
    RANDOM_EFFECT = Backlight.BacklightEffect.RANDOM_EFFECT.value
    WAVES_EFFECT = Backlight.BacklightEffect.WAVES_EFFECT.value
    # Other situation
    WOW_EFFECT = auto()
    BREATHING_OR_RAMP_UP_DOWN = auto()
    UNDETERMINED = auto()
# end class BacklightEffectType


BACKLIGHT_EFFECT_STR_MAP = {
    BacklightEffectType.STATIC_EFFECT: 'static',
    BacklightEffectType.NONE_EFFECT: 'none',
    BacklightEffectType.BREATHING_EFFECT: 'breathing',
    BacklightEffectType.CONTRAST_EFFECT: 'contrast',
    BacklightEffectType.REACTION_EFFECT: 'reaction',
    BacklightEffectType.RANDOM_EFFECT: 'random',
    BacklightEffectType.WAVES_EFFECT: 'waves',
    BacklightEffectType.WOW_EFFECT: 'wow',
    BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN: 'breathing or fade in/out',
    BacklightEffectType.UNDETERMINED: 'undetermined',
}


class BacklightPhaseType(Enum):
    """
    Possible phase of a backlight effect
    """
    STATIONARY = "Stationary"
    FADE_IN = "Fade In"
    FADE_OUT = "Fade Out"
    OFF = "Off"
    UNDETERMINED = "Undetermined"
# end class BacklightPhaseType


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@dataclass
class BacklightEffect:
    """
    Implementation of the minimal characteristics of a Backlight effect
    """
    type: BacklightEffectType = BacklightEffectType.UNDETERMINED
    duration: float = 0.0
    start_time: float = 0.0
    start_index: int = 0
    end_time: float = 0.0
    end_index: int = 0
# end class BacklightEffect


class TimeLineMixin:
    """
    Common implementation to list the successive backlight or immersive (RGB) effect capture from the i2c or led
    pwm monitoring
    """
    def __init__(self):
        self.effects = []
        self.effect_iterator = None
    # end def __init__

    def add_end_info(self, end_time, end_index):
        """
        Add end info when the effect is finished

        :param end_time: The time when the effect ends
        :type end_time: ``float``
        :param end_index: The index list when the effect ends
        :type end_index: ``int``
        """
        self.effects[-1].end_time = end_time
        self.effects[-1].end_index = end_index
        if self.effects[-1].start_time is not None:
            self.effects[-1].duration = self.effects[-1].end_time - self.effects[-1].start_time
        # end if
    # end def add_end_info

    def get_effect(self, index=None):
        """
        Retrieve a specific Backlight or RGB effect from the timeline based on the given index

        :param index: The position of the effect to retrieve. Default is None to get the last entry - OPTIONAL
        :type index: ``int`` or ``None``

        :return: The immersive lighting effect from the timeline based on the given index
        :rtype: ``BacklightEffect`` or ``pyraspi.services.kosmos.i2c.rgbparser.ImmersiveLightingEffect`` or ``None``
        """
        if len(self.effects) == 0 or (index is not None and len(self.effects) <= index):
            return None
        elif index is not None:
            # return the required index
            return self.effects[index]
        else:
            # return the last element
            return self.effects[-1]
        # end if
    # end def get_effect

    def replace_effect_type(self, new_type, index=None):
        """
        Replace a Backlight or RGB effect by another from the timeline based on the given index

        :param new_type: The new Backlight to replace
        :type new_type: ``BacklightEffectType`` or ``pyraspi.services.kosmos.i2c.rgbparser.ImmersiveLightingState``
        :param index: The position of the effect to retrieve. Default is None to get the last entry - OPTIONAL
        :type index: ``int`` or ``None``

        :raise ``AssertionError``: if index is not in this valid range or if effect timeline list is empty
        """
        assert len(self.effects) > 0
        assert (index < len(self.effects) if index is not None else True)

        if index is not None:
            # update the effect type of the given index
            self.effects[index].type = new_type
        else:
            # update the effect type of the last element
            self.effects[-1].type = new_type
        # end if
    # end def replace_effect_type

    def concatenate_effect(self, index, with_previous):
        """
        Combine two adjacent backlight or RGB effects in one either with the previous one (i.e. index and index-1) or
        with the next one (index and index+1)

        :param index: The position of the main effect to retrieve.
        :type index: ``int``
        :param with_previous: Flag indicating to concatenate index and index-1 if True else index and index+1
        :type with_previous: ``bool``

        :raise ``AssertionError``: if index is not in this valid range or if effect timeline list is empty
        """
        assert len(self.effects) > 0
        index_max = index if with_previous else index + 1
        assert index_max < len(self.effects)

        if with_previous:
            assert index > 0
            main_effect = self.effects[index]
            previous_effect = self.effects[index - 1]
            main_effect.start_time = previous_effect.start_time
            main_effect.start_index = previous_effect.start_index
            main_effect.duration = main_effect.end_time - main_effect.start_time
            self.effects[index] = main_effect
            self.effects.pop(index - 1)
        else:
            assert index + 1 < len(self.effects)
            main_effect = self.effects[index]
            next_effect = self.effects[index + 1]
            main_effect.end_time = next_effect.end_time
            main_effect.end_index = next_effect.end_index
            main_effect.duration = main_effect.end_time - main_effect.start_time
            self.effects[index] = main_effect
            self.effects.pop(index + 1)
        # end if
    # end def concatenate_effect

    def get_next_effect(self):
        """
        Retrieve the next ``BacklightEffect`` or ``pyraspi.services.kosmos.i2c.rgbparser.ImmersiveLightingEffect``
        registered in the timeline

        NB: the iterator is created during the first method call

        :return: The next effect registered in the timeline
        :rtype: ``BacklightEffect or pyraspi.services.kosmos.i2c.rgbparser.ImmersiveLightingEffect or None``
        """
        if self.effect_iterator is None:
            self.effect_iterator = iter(self.effects)
        # end if
        try:
            next_effect = next(self.effect_iterator)
        except StopIteration:
            return None
        # end try
        return next_effect
    # end def get_next_effect
# end class TimeLineMixin


class TimeLine(TimeLineMixin):
    """
    List the successive backlight effect capture from the i2c or led pwm monitoring
    """
    def add_effect(self, effect_type, start_time, start_index):
        """
        Add a backlight effect into the timeline.

        :param effect_type: The new Backlight effect to include
        :type effect_type: ``BacklightEffectType``
        :param start_time: The time when the effect starts
        :type start_time: ``float``
        :param start_index: The index list when the effect starts
        :type start_index: ``int``
        """
        effect = BacklightEffect(type=effect_type, start_time=start_time, start_index=start_index,
                                 end_time=0.0, end_index=0)
        self.effects.append(effect)
    # end def add_effect

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        message = 'Backlight TimeLine:\n'
        if not self.effects:
            message += f'Timeline is empty'
        # end if
        for effect in self.effects:
            message += f'* {BACKLIGHT_EFFECT_STR_MAP[effect.type]}\n'
            message += f'   -start time : {effect.start_time}\n'
            message += f'   -end time : {effect.end_time}\n'
            message += f'   -duration time : {effect.duration}\n'
        # end for
        return message
    # end def __str__
# end class TimeLine


class LedDataBacklightParser:
    """
    Leds data parser to backlight effect

    This class parses the LEDs backlight data to extract a usable backlight effect timeline
    """
    VERBOSE = False

    @unique
    class STATE(IntEnum):
        """
        Led data backlight parsing state
        """
        NOT_STARTED = auto()
        COMPLETED = auto()
    # end class STATE

    def __init__(self, timestamps, led_values, fw_id, led_id_to_check, previous_effect=BacklightEffectType.NONE_EFFECT,
                 layout_type=KeyboardMixin.LAYOUT.DEFAULT):
        """
        :param timestamps: The timestamp list of the LED list.
        :type timestamps: ``list[float]``
        :param led_values: The LED pwm values list over time.
        :type led_values: ``list[list[int]]``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param led_id_to_check: The LED ID index of ``led_values``to used for the parser.
        :type led_id_to_check: ``list[int]``
        :param previous_effect: Backlight previous effect at the start of the recording - OPTIONAL
        :type previous_effect: ``BacklightEffectType``
        :param layout_type: keyboard international layout type - OPTIONAL
        :type layout_type: ``KeyboardMixin.LAYOUT``

        :raise ``AssertionError``: If the firmware identifier or layout type is not in its valid range
        """
        assert fw_id in GET_BACKLIGHT_CONFIGURATION_BY_ID, f"Backlight configuration is not done for fw_id {fw_id}"
        assert layout_type <= KeyboardMixin.LAYOUT.MAX
        self._fw_id = fw_id
        self._layout_type = layout_type
        self._configuration = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][layout_type]
        self._complex_effect = self._configuration.COMPLEX_EFFECT

        self.timeline = TimeLine()
        self.state = previous_effect
        self.timeline.add_effect(self.state, start_time=0.0, start_index=0)
        self.start_time = 0.0
        self.duration = 0.0

        self._led_backlight_parsing_state = self.STATE.NOT_STARTED

        self._backlight_timeline = None
        self._timestamps = timestamps
        self._led_values = led_values
        self._led_id_to_check = led_id_to_check
        if self._complex_effect:
            self._led_id_to_check_g1 = [self._configuration.KEY_ID_TO_LED_ID.get(key_id) for key_id in
                                        self._configuration.KEY_ID_CONTRAST_GROUP_KEYS1]
            self._led_id_to_check_g1 = [led_id for led_id in self._led_id_to_check_g1 if led_id in led_id_to_check]
            self._led_id_to_check_g2 = [self._configuration.KEY_ID_TO_LED_ID.get(key_id) for key_id in
                                        self._configuration.KEY_ID_CONTRAST_GROUP_KEYS2]
            self._led_id_to_check_g2 = [led_id for led_id in self._led_id_to_check_g2 if led_id in led_id_to_check]
        # end if
    # end def __init__

    def parse_entries(self, led_spy_values, led_spy_timestamp):
        """
        Parse the buffer to create a suitable Timeline

        :param led_spy_values: The LED pwm values list over time.
        :type led_spy_values: ``list[list[int]]``
        :param led_spy_timestamp: The timestamp list of the LED list
        :type led_spy_timestamp: ``list[float]``

        :return: The Backlight Timeline
        :rtype: ``TimeLine``
        """
        # First loop to create (with possible error) a backlight timeline
        index = 0
        for value, timestamp in zip(led_spy_values, led_spy_timestamp):
            previous_state = self.state

            # Update the current effect according to the LEDs pwm values and timestamp
            self.update(value, timestamp)

            if previous_state != self.state:
                # Add end info to timeline for the previous effect
                self.timeline.add_end_info(end_time=timestamp, end_index=index)
                # Add the new current effect to timeline
                self.timeline.add_effect(self.state, start_time=timestamp, start_index=index)
            # end if
            index += 1
        # end for
        # Add end info to timeline for the last effect
        if len(led_spy_timestamp) > 0:
            self.timeline.add_end_info(end_time=led_spy_timestamp[-1], end_index=index)
        # end if

        # Second Loop to check and modify timeline
        index = 0
        while index < len(self.timeline.effects):
            effect_type = self.timeline.effects[index].type
            if index > 0:
                previous_effect_type = self.timeline.effects[index - 1].type
            else:
                previous_effect_type = BacklightEffectType.UNDETERMINED
            # end if

            # Concatenate identical successive state
            while effect_type == previous_effect_type:
                self.timeline.concatenate_effect(index, with_previous=True)
                index -= 1
                if index > 0:
                    previous_effect_type = self.timeline.effects[index - 1].type
                else:
                    previous_effect_type = BacklightEffectType.UNDETERMINED
                    break
                # end if
            # end while

            # replace and concatenate "BREATHING_OR_RAMP_UP_DOWN" by "BREATHING_EFFECT" or "STATIC_EFFECT" or
            # "WOW_EFFECT"
            if effect_type == BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN:
                if previous_effect_type == BacklightEffectType.BREATHING_EFFECT:
                    self.timeline.replace_effect_type(new_type=previous_effect_type, index=index)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                elif previous_effect_type == BacklightEffectType.STATIC_EFFECT:
                    self.timeline.replace_effect_type(new_type=previous_effect_type, index=index)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                elif previous_effect_type == BacklightEffectType.WOW_EFFECT:
                    self.timeline.replace_effect_type(new_type=previous_effect_type, index=index)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                # end if

            elif effect_type == BacklightEffectType.STATIC_EFFECT:
                # Verification than the STATIC_EFFECT effect was really a STATIC_EFFECT effect
                if 0 < self.timeline.effects[index].duration < _MIN_DURATION_STATIC_EFFECT:
                    if previous_effect_type == BacklightEffectType.BREATHING_EFFECT:
                        self.timeline.replace_effect_type(new_type=previous_effect_type, index=index)
                        self.timeline.concatenate_effect(index, with_previous=True)
                        index -= 1
                        if index > 0:
                            previous_effect_type = self.timeline.effects[index - 1].type
                        else:
                            previous_effect_type = BacklightEffectType.UNDETERMINED
                        # end if
                    elif previous_effect_type == BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN:
                        self.timeline.replace_effect_type(new_type=previous_effect_type, index=index)
                        self.timeline.concatenate_effect(index, with_previous=True)
                        index -= 1
                        if index > 0:
                            previous_effect_type = self.timeline.effects[index - 1].type
                        else:
                            previous_effect_type = BacklightEffectType.UNDETERMINED
                        # end if
                    elif previous_effect_type == BacklightEffectType.WOW_EFFECT:
                        self.timeline.replace_effect_type(new_type=previous_effect_type, index=index)
                        self.timeline.concatenate_effect(index, with_previous=True)
                        index -= 1
                        if index > 0:
                            previous_effect_type = self.timeline.effects[index - 1].type
                        else:
                            previous_effect_type = BacklightEffectType.UNDETERMINED
                        # end if
                    # end if
                # end if

                # replace and concatenate "BREATHING_OR_RAMP_UP_DOWN" by "STATIC_EFFECT"
                if previous_effect_type == BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN:
                    self.timeline.replace_effect_type(new_type=BacklightEffectType.STATIC_EFFECT, index=index - 1)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                # end if
            elif effect_type == BacklightEffectType.BREATHING_EFFECT:
                # replace and concatenate "BREATHING_OR_RAMP_UP_DOWN" by "BREATHING_EFFECT"
                if previous_effect_type == BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN:
                    self.timeline.replace_effect_type(new_type=BacklightEffectType.BREATHING_EFFECT, index=index - 1)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                # Replace short "STATIC_EFFECT" by "BREATHING_EFFECT"and concatenate effect durations
                elif previous_effect_type == BacklightEffectType.STATIC_EFFECT:
                    self.timeline.replace_effect_type(new_type=BacklightEffectType.BREATHING_EFFECT, index=index - 1)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                # end if
            elif effect_type == BacklightEffectType.RANDOM_EFFECT:
                # Replace and concatenate very short "BREATHING_OR_RAMP_UP_DOWN" by "RANDOM_EFFECT"
                if previous_effect_type == BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN and \
                        self.timeline.effects[index - 1].duration < _MIN_DURATION_STATIC_EFFECT:
                    self.timeline.replace_effect_type(new_type=BacklightEffectType.RANDOM_EFFECT, index=index - 1)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                # end if
            elif effect_type == BacklightEffectType.WOW_EFFECT:
                # replace and concatenate "BREATHING_OR_RAMP_UP_DOWN" by "WOW_EFFECT"
                if previous_effect_type == BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN:
                    self.timeline.replace_effect_type(new_type=BacklightEffectType.WOW_EFFECT, index=index - 1)
                    self.timeline.concatenate_effect(index, with_previous=True)
                    index -= 1
                # end if
            elif effect_type == BacklightEffectType.UNDETERMINED and \
                    self.timeline.effects[index].duration < _MIN_DURATION_UNDETERMINED:
                # concatenate the short "UNDETERMINED" period with the previous effect
                self.timeline.replace_effect_type(new_type=previous_effect_type, index=index)
                self.timeline.concatenate_effect(index, with_previous=True)
                index -= 1
            # end if
            index += 1
        # end while

        return self.timeline
    # end def parse_entries

    def update(self, led_pwm_value, timestamp):
        """
        Update the effect state from current ``led_pwm_value`` and ``timestamp``

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``
        :param timestamp: timestamp of the led_pwm_value list
        :type timestamp: ``float``
        """
        if self.is_contrast_effect(led_pwm_value):
            self.state = BacklightEffectType.CONTRAST_EFFECT
        elif self.is_waves_effect(led_pwm_value):
            self.state = BacklightEffectType.WAVES_EFFECT
        elif self.is_random_effect(led_pwm_value):
            self.state = BacklightEffectType.RANDOM_EFFECT
        elif self.is_none_effect(led_pwm_value):
            self.state = BacklightEffectType.NONE_EFFECT
        elif self.is_static_effect(led_pwm_value):
            self.state = BacklightEffectType.STATIC_EFFECT
        elif self.is_wow_effect(led_pwm_value):
            self.state = BacklightEffectType.WOW_EFFECT
        elif self.is_breathing_effect(led_pwm_value, timestamp):
            self.state = BacklightEffectType.BREATHING_EFFECT
        elif self.is_breathing_or_ramp_up_down(led_pwm_value):
            self.state = BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN
        else:
            self.state = BacklightEffectType.UNDETERMINED
        # end if
    # end def update

    def is_random_effect(self, led_pwm_value):
        """
        Check if the led_pwm_value fit the random effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``

        :return: Flag indicating if the LED pwm list matches the random effect
        :rtype: ``bool``
        """
        status = False
        if self._complex_effect:
            data_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check]
            # Count the number of keys that are ON
            temp = [x > self._configuration.LOW_LEVEL_VALUE for x in data_to_check]
            nb_leds_on = temp.count(True)
            # Check the number of leds that are ON
            if (self._configuration.RANDOM_EFFECT_LED_ON_NUMBER - _RANDOM_EFFECT_LED_ON_NUMBER_MARGIN) <= \
                    nb_leds_on <= \
                    (self._configuration.RANDOM_EFFECT_LED_ON_NUMBER + _RANDOM_EFFECT_LED_ON_NUMBER_MARGIN):
                status = True
            # end if
        # end if
        return status
    # end def is_random_effect

    def is_contrast_effect(self, led_pwm_value):
        """
        Check if the led_pwm_value fit the contrast effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``

        :return: Flag indicating if the LED pwm list matches the contrast effect
        :rtype: ``bool``
        """
        status = False
        if self._complex_effect:
            data_g0_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check_g1]
            data_g1_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check_g2]

            # check if group 0 leds are all equal
            if all(x == data_g0_to_check[0] for x in data_g0_to_check):
                # check if group 1 leds are all equal
                if all(x == data_g1_to_check[0] for x in data_g1_to_check):
                    # check if g0 and g1 leds are different
                    if data_g0_to_check[0] != data_g1_to_check[0]:
                        status = True
                    # end if
                # end if
            # end if
        # end if
        return status
    # end def is_contrast_effect

    def is_none_effect(self, led_pwm_value):
        """
        Check if the led_pwm_value fit the none effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``

        :return: Flag indicating if the LED pwm list matches the none effect
        :rtype: ``bool``
        """
        status = False

        data_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check]
        if all(x == 0x00 for x in data_to_check):
            status = True
        # end if
        # For DUT with only one backlight LED spied by LED pwm spy module, fast transition to zero can be missed if
        # checking only zero value, so we tolerate than 1 is also a LED off
        if self._complex_effect is False and all(x == 0x01 for x in data_to_check):
            status = True
        # end if
        return status
    # end def is_none_effect

    def is_wow_effect(self, led_pwm_value):
        """
        Check if the led_pwm_value fit the wow effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``

        :return: Flag indicating if the LED pwm list matches the wow effect
        :rtype: ``bool``
        """
        status = False

        data_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check]
        # Check if led value are all equal and if equal to MAX_PWM_VALUE
        if all(x == data_to_check[0] for x in data_to_check):
            if data_to_check[0] == self._configuration.MAX_PWM_VALUE:
                status = True
            # end if
        # end if
        return status
    # end def is_wow_effect

    def is_static_effect(self, led_pwm_value):
        """
        Check if the led_pwm_value fit the STATIC effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``

        :return: Flag indicating if the LED pwm list matches the static effect
        :rtype: ``bool``
        """
        status = False

        data_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check]
        # Check if data_keys_to_check are all equal and if equal to specific level 1-7
        if all(x == data_to_check[0] for x in data_to_check):
            for expected_value in self._configuration.LEVEL_PWM_VALUE[1::]:
                if expected_value - _LOWER_STATIC_EFFECT_MARGIN < data_to_check[0] < expected_value + \
                        _UPPER_STATIC_EFFECT_MARGIN:
                    status = True
                    break
                # end if
            # end for
        # end if
        return status
    # end def is_static_effect

    def is_waves_effect(self, led_pwm_value):
        """
        Check if the led_pwm_value fit the waves effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``

        :return: Flag indicating if the LED pwm list matches the waves effect
        :rtype: ``bool``
        """
        status = False
        if self._complex_effect:
            data_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check]
            # Count the number of keys that are ON
            temp = [x > 0 for x in data_to_check]
            nb_leds_on = temp.count(True)
            # Count the number of keys that are OFF
            temp = [x == 0 for x in data_to_check]
            nb_leds_off = temp.count(True)
            # Check the number of leds ON
            if nb_leds_on >= self._configuration.WAVES_EFFECT_MIN_NUMBER_LED_ON:
                # Check the number of leds OFF
                if nb_leds_off >= self._configuration.WAVES_EFFECT_MIN_NUMBER_LED_OFF:
                    status = True
                    # Check all the leds in the column have the same value
                    for key_ids in self._configuration.KEY_ID_WAVE_MAP_HORIZONTAL:
                        led_ids = [self._configuration.KEY_ID_TO_LED_ID[key_id] for key_id in key_ids]
                        data_to_check = [led_pwm_value[led_id] for led_id in led_ids]
                        if not all(x == data_to_check[0] for x in data_to_check):
                            status = False
                            break
                        # end if
                    # end for
                # end if
            # end if
        # end if
        return status
    # end def is_waves_effect

    def is_breathing_effect(self, led_pwm_value, timestamp):
        """
        Check if the led_pwm_value fit the breathing effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``
        :param timestamp: timestamp of the led_pwm_value list
        :type timestamp: ``float``

        :return: Flag indicating if the LED pwm list matches the breathing effect
        :rtype: ``bool``
        """
        status = False
        data_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check]

        # Check if led_pwm_value are all equal
        if all(x == data_to_check[0] for x in data_to_check):
            if self.state == BacklightEffectType.BREATHING_EFFECT:
                status = True
            # Check if actual state is BREATHING_OR_RAMP_UP_DOWN for more than MAX_RAMP_UP_DOWN_TIME
            elif self.state == BacklightEffectType.BREATHING_OR_RAMP_UP_DOWN:
                start_time = self.timeline.get_effect().start_time
                if (timestamp - start_time) > self._configuration.MAX_RAMP_UP_DOWN_TIME:
                    if data_to_check[0] >= self._configuration.LOW_LEVEL_VALUE:
                        status = True
                    # end if
                # end if
            # end if
        # end if
        return status
    # end def is_breathing_effect

    def is_breathing_or_ramp_up_down(self, led_pwm_value):
        """
        Check if it is an undetermined state between breathing effect  and ramp up/ down on STATIC_EFFECT or wow effect

        :param led_pwm_value: LED pwm value at a given timestamp
        :type led_pwm_value: ``list[int]``

        :return: Flag indicating if the LED pwm list matches the breathing effect
        :rtype: ``bool``
        """
        status = False
        data_to_check = [led_pwm_value[led_id] for led_id in self._led_id_to_check]

        # Check if led_pwm_value are all equal
        if all(x == data_to_check[0] for x in data_to_check):
            status = True
        # end if
        return status
    # end def is_breathing_or_ramp_up_down

    def is_backlight_complying_with_requirement(self, effect_type, led_id_to_check, brightness_level,
                                                stationary_phase_duration, fade_in_phase_duration,
                                                fade_out_phase_duration, previous_effect):
        """
        Verify the backlight requirements for the given effect type, level and duration (on the expected keys where
        it is played)

        :param effect_type: effect to check
        :type effect_type: ``BacklightEffectType``
        :param led_id_to_check: List of expected keys where the backlight effect is played
        :type led_id_to_check: ``list[int]``
        :param brightness_level: level to check (default is None)
        :type brightness_level: ``int`` or ``None``
        :param stationary_phase_duration: duration of the stationary phase in second
        :type stationary_phase_duration: ``float`` or ``None``
        :param fade_in_phase_duration: duration of the fade in period in second
        :type fade_in_phase_duration: ``float`` or ``None``
        :param fade_out_phase_duration: duration of the fade out period in second
        :type fade_out_phase_duration: ``float`` or ``None``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``

        :return: Flag indicating if the backlight effect matches the requirements
        :rtype: ``bool``
        """
        status = True

        if self._led_backlight_parsing_state == self.STATE.NOT_STARTED:
            # Parse PWM led entries to backlight timeline
            self._backlight_timeline = self.parse_entries(led_spy_values=self._led_values,
                                                          led_spy_timestamp=self._timestamps)
            self._led_backlight_parsing_state = self.STATE.COMPLETED
        # end if

        next_effect = self._backlight_timeline.get_next_effect()

        # Check backlight type
        self.debug_print(f'The effect is :  {BACKLIGHT_EFFECT_STR_MAP[next_effect.type]}, '
                         f'the total duration is : {next_effect.duration} seconds')
        if next_effect.type != effect_type:
            warn(f'Wrong scheme type: {BACKLIGHT_EFFECT_STR_MAP[next_effect.type]} != '
                 f'{BACKLIGHT_EFFECT_STR_MAP[effect_type]}')
            status = False
        # end if

        if effect_type != BacklightEffectType.NONE_EFFECT:
            # Check backlight pattern
            backlight_pattern_parser = BacklightPatternParser(self._fw_id, led_id_to_check=led_id_to_check,
                                                              previous_effect=previous_effect,
                                                              layout_type=self._layout_type)
            backlight_pattern_parser.parse_backlight(effect=next_effect,
                                                     leds_pwm_values=self._led_values,
                                                     leds_pwm_timestamp=self._timestamps)

            if not backlight_pattern_parser.check_characteristic(brightness_level=brightness_level,
                                                                 stationary_phase_duration=stationary_phase_duration,
                                                                 fade_in_phase_duration=fade_in_phase_duration,
                                                                 fade_out_phase_duration=fade_out_phase_duration,
                                                                 verbose=self.VERBOSE):
                status = False
            # end if
        # end if
        return status
    # end def is_backlight_complying_with_requirement

    def get_last_backlight_state(self):
        """
        Retrieve the current backlight state for given keys.

        :return: The last Backlight effect type in the timeline
        :rtype: ``BacklightEffectType``
        """

        if self._led_backlight_parsing_state == self.STATE.NOT_STARTED:
            # Parse PWM led entries to backlight timeline
            self._backlight_timeline = self.parse_entries(led_spy_values=self._led_values,
                                                          led_spy_timestamp=self._timestamps)
            self._led_backlight_parsing_state = self.STATE.COMPLETED
        # end if

        last_effect = self._backlight_timeline.get_effect()

        return last_effect.type
    # end def get_last_backlight_state

    def debug_print(self, text):
        """
        Print text, but only when ``self.VERBOSE`` is `True`.

        :param text: Text to print in Verbose mode
        :type text: ``str``
        """
        if self.VERBOSE:
            stdout.write(f'{text}\n')
        # end if
    # end def debug_print
# end class LedDataBacklightParser


class BacklightPatternParser:
    """
    Backlight Pattern Parser

    This class parses the Backlight effect to check this pattern (level, duration, phase:fade in/out, stationary)
    """
    def __init__(self, fw_id, led_id_to_check, previous_effect, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param led_id_to_check: The LED ID index of ``led_values``to used for the parser
        :type led_id_to_check: ``list[int]``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``

        :raise ``AssertionError``: If the firmware identifier is not in its valid range
        """
        assert fw_id in GET_BACKLIGHT_CONFIGURATION_BY_ID, f'Don\'t support the fw_id : {fw_id}'

        self._configuration = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][layout_type]
        self._fw_id = fw_id
        self._layout_type = layout_type
        self._complex_effect = self._configuration.COMPLEX_EFFECT
        self._previous_effect = previous_effect
        self._led_id_to_check = led_id_to_check

        if self._complex_effect:
            self._led_id_to_check_g1 = [self._configuration.KEY_ID_TO_LED_ID.get(key_id) for key_id in
                                        self._configuration.KEY_ID_CONTRAST_GROUP_KEYS1]
            self._led_id_to_check_g1 = [led_id for led_id in self._led_id_to_check_g1 if led_id in led_id_to_check]
            self._led_id_to_check_g2 = [self._configuration.KEY_ID_TO_LED_ID.get(key_id) for key_id in
                                        self._configuration.KEY_ID_CONTRAST_GROUP_KEYS2]
            self._led_id_to_check_g2 = [led_id for led_id in self._led_id_to_check_g2 if led_id in led_id_to_check]
        # end if

        self.backlight_characteristics = None
    # end def __init__

    def parse_backlight(self, effect, leds_pwm_values, leds_pwm_timestamp):
        """
        Parse the backlight pattern (level, duration, phase:fade in/out, stationary) of an effect from the LED pwm
        values and timestamp.

        :param effect: Backlight effect registered in the timeline
        :type effect: ``BacklightEffect``
        :param leds_pwm_values: The LED pwm values list over time
        :type leds_pwm_values: ``list[list[int]]``
        :param leds_pwm_timestamp: The timestamp list of the LED list
        :type leds_pwm_timestamp: ``list[float]``
        """
        backlight_type = effect.type
        start_index = effect.start_index
        end_index = effect.end_index + 1
        max_pwm_value = max(max([[values[led_id] for led_id in self._led_id_to_check] for values in
                                 leds_pwm_values[start_index:end_index]]))

        if backlight_type == BacklightEffectType.WOW_EFFECT:
            self.backlight_characteristics = WowBacklightPattern(fw_id=self._fw_id,
                                                                 previous_effect=self._previous_effect,
                                                                 max_pwm_value=max_pwm_value,
                                                                 led_id=self._led_id_to_check[0],
                                                                 layout_type=self._layout_type)
        elif backlight_type == BacklightEffectType.STATIC_EFFECT:
            self.backlight_characteristics = StaticBacklightPattern(fw_id=self._fw_id,
                                                                    previous_effect=self._previous_effect,
                                                                    max_pwm_value=max_pwm_value,
                                                                    led_id=self._led_id_to_check[0],
                                                                    layout_type=self._layout_type)
        elif backlight_type == BacklightEffectType.BREATHING_EFFECT:
            self.backlight_characteristics = BreathingBacklightPattern(fw_id=self._fw_id,
                                                                       previous_effect=self._previous_effect,
                                                                       max_pwm_value=max_pwm_value,
                                                                       led_id=self._led_id_to_check[0],
                                                                       layout_type=self._layout_type)
        elif self._complex_effect:
            if backlight_type == BacklightEffectType.CONTRAST_EFFECT:
                self.backlight_characteristics = \
                    ContrastBacklightPattern(fw_id=self._fw_id,
                                             previous_effect=self._previous_effect,
                                             max_pwm_value=max_pwm_value,
                                             led_id_group_keys1=self._led_id_to_check_g1[0],
                                             led_id_group_keys2=self._led_id_to_check_g2[0],
                                             layout_type=self._layout_type)
            elif backlight_type == BacklightEffectType.RANDOM_EFFECT:
                self.backlight_characteristics = RandomBacklightPattern(fw_id=self._fw_id,
                                                                        previous_effect=self._previous_effect,
                                                                        max_pwm_value=max_pwm_value,
                                                                        led_ids=self._led_id_to_check,
                                                                        layout_type=self._layout_type)
            elif backlight_type == BacklightEffectType.WAVES_EFFECT:
                self.backlight_characteristics = WavesBacklightPattern(fw_id=self._fw_id,
                                                                       previous_effect=self._previous_effect,
                                                                       max_pwm_value=max_pwm_value,
                                                                       led_ids=self._led_id_to_check,
                                                                       layout_type=self._layout_type)
            else:
                return
            # end if
        else:
            return
        # end if

        for value, timestamp in zip(leds_pwm_values[start_index:end_index], leds_pwm_timestamp[start_index:end_index]):
            self.backlight_characteristics.update_characteristic(value, timestamp)
        # end for
    # end def parse_backlight

    def check_characteristic(self, brightness_level, stationary_phase_duration, fade_in_phase_duration,
                             fade_out_phase_duration, verbose):
        """
        Check the characteristic of the Backlight effect

        :param brightness_level: level to check (default is None)
        :type brightness_level: ``int`` or ``None``
        :param stationary_phase_duration: duration of the stationary phase in s
        :type stationary_phase_duration: ``float`` or ``None``
        :param fade_in_phase_duration: duration of the fade in period in second
        :type fade_in_phase_duration: ``float`` or ``None``
        :param fade_out_phase_duration: duration of the fade out period in second
        :type fade_out_phase_duration: ``float`` or ``None``
        :param verbose: To enable the debug message or not
        :type verbose: ``bool``

        :return: Check Characteristics status: `True` is success, `False` is failure
        :rtype: ``bool``
        """
        return self.backlight_characteristics.check_characteristic(brightness_level=brightness_level,
                                                                   stationary_phase_duration=stationary_phase_duration,
                                                                   fade_in_phase_duration=fade_in_phase_duration,
                                                                   fade_out_phase_duration=fade_out_phase_duration,
                                                                   verbose=verbose)
    # end def check_characteristic
# end class BacklightPatternParser


class BacklightPatternMixin:
    """
    Common implementation class for backlight effect pattern characterisation (Static, WOW, Contrast, Breathing, random
    and Waves).
    """
    def __init__(self, fw_id, previous_effect, max_pwm_value, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param max_pwm_value: Maximum value of the current static effect
        :type max_pwm_value: ``int``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``

        :raise ``AssertionError``: If the firmware identifier is not in its valid range
        """
        assert fw_id in GET_BACKLIGHT_CONFIGURATION_BY_ID, f"Backlight configuration is not done for fw_id {fw_id}"
        self._fw_id = fw_id
        self._layout_type = layout_type
        self._configuration = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][layout_type]

        # Possible check
        self.check_phase_effect = False
        self.check_stationary_duration = False
        self.check_fade_in_duration = False
        self.check_fade_out_duration = False
        self.check_fade_in_group_keys1_duration = False
        self.check_fade_in_group_keys2_duration = False
        self.check_fade_in_delta_group_keys1_vs_2_duration = False
        self.check_level = False
        self.expected_period = None
        self.check_waveform = False
        self.check_random_effect = False
        self.previous_effect = previous_effect

        # Variable used for check
        self.effect_type = BacklightEffectType.UNDETERMINED
        self.level_pwm_value = None
        self.state_list = []
        self.start_time_fade_in = None
        self.stop_time_fade_in = None
        self.start_time_fade_out = None
        self.stop_time_fade_out = None
        self.start_time_fade_in_group_keys1 = None
        self.start_time_fade_in_group_keys2 = None
        self.stop_time_fade_in_group_keys1 = None
        self.stop_time_fade_in_group_keys2 = None
        self.level_pwm_value_group_keys1 = None
        self.level_pwm_value_group_keys2 = None
        self.timestamp_max_value = None
        self.is_vertical_wave = True
        self.expected_delta_duration_between_column = None
        self.monitored_waveform = None
        self.expected_waveform = None
        self.led_ids_states = None
        self.states_transition_timing = None

        # To detect level and stationary phase
        self.set_level_pwm_value(max_pwm_value)

        self.verbose = False
    # end def __init__

    def check_characteristic(self, brightness_level=None,
                             stationary_phase_duration=None,
                             fade_in_phase_duration=None,
                             fade_out_phase_duration=None,
                             verbose=False):
        """
        Check the characteristic of the backlight effect

        :param brightness_level: the backlight level - OPTIONAL
        :type brightness_level: ``int``
        :param stationary_phase_duration: duration of the stationary phase in s - OPTIONAL
        :type stationary_phase_duration: ``float`` or ``None``
        :param fade_in_phase_duration: duration of the fade in period in second - OPTIONAL
        :type fade_in_phase_duration: ``float`` or ``None``
        :param fade_out_phase_duration: duration of the fade out period in second - OPTIONAL
        :type fade_out_phase_duration: ``float`` or ``None``
        :param verbose: To enable the debug message or not - OPTIONAL
        :type verbose: ``bool``

        :return: Check Characteristics status: `True` is success, `False` is failure
        :rtype: ``bool``
        """
        status = True
        self.verbose = verbose

        if self.check_phase_effect:
            expected_phase = []
            if fade_in_phase_duration is not None:
                expected_phase.append(BacklightPhaseType.FADE_IN)
            # end if
            if stationary_phase_duration is not None or fade_in_phase_duration is not None or \
                    fade_out_phase_duration is not None:
                expected_phase.append(BacklightPhaseType.STATIONARY)
            # end if
            if fade_out_phase_duration is not None:
                expected_phase.append(BacklightPhaseType.FADE_OUT)
            # end if
            # Check state_list
            self.debug_print(f'The phase of the effect are : {self.state_list}')
            if self.state_list != expected_phase:
                warn(f'Backlight phase is not correct, expected : {expected_phase}, obtained : {self.state_list}')
                status = False
            # end if
        # end if

        if self.check_level:
            # Check pwm_led_value during the "stationary" phase
            if brightness_level is not None:
                if self.level_pwm_value in self._configuration.LEVEL_PWM_VALUE:
                    self.debug_print(f'The level is {self._configuration.LEVEL_PWM_VALUE.index(self.level_pwm_value)}')
                else:
                    self.debug_print(f'The led PWM value is not in the list, value = {self.level_pwm_value}')
                # end if
                if self.level_pwm_value not in self._configuration.LEVEL_PWM_VALUE:
                    warn('The brightness level is not correct')
                    status = False
                elif self._configuration.LEVEL_PWM_VALUE.index(self.level_pwm_value) != brightness_level:
                    warn(f'The brightness level is not correct '
                         f'{self._configuration.LEVEL_PWM_VALUE.index(self.level_pwm_value)} != {brightness_level}')
                    status = False
                # end if
                # Check Contrast effect level for group keys1 and group keys2
                if self.effect_type == BacklightEffectType.CONTRAST_EFFECT:
                    expected_level_group_keys1 = self._configuration.LEVEL_PWM_VALUE[brightness_level]
                    expected_level_group_keys2 = int(expected_level_group_keys1 /
                                                     self._configuration.CONTRAST_INTENSITY_RATIO_G1_G2)
                    error_level_group_keys1 = \
                        (self.level_pwm_value_group_keys1 - expected_level_group_keys1) / expected_level_group_keys1
                    error_level_group_keys2 = \
                        (self.level_pwm_value_group_keys2 - expected_level_group_keys2) / expected_level_group_keys2

                    if abs(error_level_group_keys1) > _5_PERCENT:
                        warn('The brightness level for group keys1 is not correct, pwm value expected : '
                             f'{expected_level_group_keys1}, obtained : {self.level_pwm_value_group_keys1}, error : '
                             f'{error_level_group_keys1 * 100} %')
                        status = False
                    # end if
                    if abs(error_level_group_keys2) > _5_PERCENT:
                        warn('The brightness level for group keys2 is not correct, pwm value expected : '
                             f'{expected_level_group_keys2}, obtained : {self.level_pwm_value_group_keys2}, error : '
                             f'{error_level_group_keys2 * 100} %')
                        status = False
                    # end if
                # end if
            elif self.effect_type == BacklightEffectType.WOW_EFFECT:
                if self.level_pwm_value != self._configuration.MAX_PWM_VALUE:
                    warn(
                        f'The brightness level is not correct {self.level_pwm_value} != '
                        f'{self._configuration.MAX_PWM_VALUE}')
                    status = False
                # end if
            # end if
        # end if

        if self.check_stationary_duration and stationary_phase_duration is not None:
            # Check stationary duration
            duration = self.start_time_fade_out - self.stop_time_fade_in
            self.debug_print(f'The duration of the stationary phase  is : {duration} seconds')
            error = (duration - stationary_phase_duration) / stationary_phase_duration
            if abs(error) > _5_PERCENT:
                warn(f'Backlight stationary duration is not correct, expected : {stationary_phase_duration}, '
                     f'obtained : {duration}, error : {error * 100} %')
                status = False
            # end if
        # end if

        if self.check_fade_in_duration and fade_in_phase_duration is not None:
            # Check fade in duration
            duration = self.stop_time_fade_in - self.start_time_fade_in
            self.debug_print(f'The duration of the FADE IN is : {duration} seconds')
            error = (duration - fade_in_phase_duration) / fade_in_phase_duration
            is_fade_in_short = (fade_in_phase_duration * _5_PERCENT < _MIN_ACCEPTABLE_TIMING_ERROR)
            if (is_fade_in_short and abs(duration - fade_in_phase_duration) > _MIN_ACCEPTABLE_TIMING_ERROR) or \
                    (not is_fade_in_short and abs(error) > _5_PERCENT):

                warn(f'Backlight fade in duration is not correct, expected : {fade_in_phase_duration}, '
                     f'obtained : {duration}, error : {error * 100} %')
                status = False
            # end if

            if self.check_fade_in_group_keys1_duration:
                # Check fade in duration for group keys1 (contrast effect)
                duration = self.stop_time_fade_in_group_keys1 - self.start_time_fade_in_group_keys1
                expected_duration = self._configuration.CONTRAST_FADE_IN_GROUP_KEYS1_DURATION
                self.debug_print(f'The duration of the FADE IN for group keys1 is : {duration} seconds')
                error = (duration - expected_duration) / expected_duration
                is_fade_in_short = (expected_duration * _5_PERCENT < _MIN_ACCEPTABLE_TIMING_ERROR)
                if (is_fade_in_short and abs(duration - expected_duration) > _MIN_ACCEPTABLE_TIMING_ERROR) or \
                        (not is_fade_in_short and abs(error) > _5_PERCENT):
                    warn(f'Backlight fade in group keys1 duration is not correct, expected : {expected_duration}, '
                         f'obtained : {duration}, error : {error * 100} %')
                    status = False
                # end if
            # end if
            if self.check_fade_in_delta_group_keys1_vs_2_duration:
                # Check fade in delta duration between group keys1 and keys2 (contrast effect)
                duration = self.start_time_fade_in_group_keys2 - self.stop_time_fade_in_group_keys1
                expected_duration = self._configuration.CONTRAST_DELTA_GROUP_KEYS1_VS_2_DURATION
                self.debug_print(f'The delta duration between group keys1 and keys2 in FADE IN  is : {duration} '
                                 f'seconds')
                error = (duration - expected_duration) / expected_duration
                is_fade_in_short = (expected_duration * _5_PERCENT < _MIN_ACCEPTABLE_TIMING_ERROR)
                if (is_fade_in_short and abs(duration - expected_duration) > _MIN_ACCEPTABLE_TIMING_ERROR) or \
                        (not is_fade_in_short and abs(error) > _5_PERCENT):
                    warn(f'Backlight delta duration between group keys1 and keys2 in FADE IN is not correct, expected :'
                         f' {expected_duration}, obtained : {duration}, error : {error * 100} %')
                    status = False
                # end if
            # end if
            if self.check_fade_in_group_keys2_duration:
                # Check fade in duration for group keys2 (contrast effect)
                duration = self.stop_time_fade_in_group_keys2 - self.start_time_fade_in_group_keys2
                expected_duration = self._configuration.CONTRAST_FADE_IN_GROUP_KEYS2_DURATION
                self.debug_print(f'The duration of the FADE IN for group keys2 is : {duration} seconds')
                error = (duration - expected_duration) / expected_duration
                is_fade_in_short = (expected_duration * _5_PERCENT < _MIN_ACCEPTABLE_TIMING_ERROR)
                if (is_fade_in_short and abs(duration - expected_duration) > _MIN_ACCEPTABLE_TIMING_ERROR) or \
                        (not is_fade_in_short and abs(error) > _5_PERCENT):
                    warn(f'Backlight fade in group keys2 duration is not correct, expected : {expected_duration}, '
                         f'obtained : {duration}, error : {error * 100} %')
                    status = False
                # end if
            # end if
        # end if

        if self.check_fade_out_duration and fade_out_phase_duration is not None:
            # Check fade out duration
            duration = self.stop_time_fade_out - self.start_time_fade_out
            self.debug_print(f'The duration of the FADE OUT is : {duration} seconds')
            error = (duration - fade_out_phase_duration) / fade_out_phase_duration
            is_fade_out_short = (fade_out_phase_duration * _5_PERCENT < _MIN_ACCEPTABLE_TIMING_ERROR)
            if (is_fade_out_short and abs(duration - fade_out_phase_duration) > _MIN_ACCEPTABLE_TIMING_ERROR) or \
                    (not is_fade_out_short and abs(error) > _5_PERCENT):

                warn(f'Backlight fade out duration is not correct, expected : {fade_out_phase_duration}, '
                     f'obtained : {duration}, error : {error * 100} %')
                status = False
            # end if
        # end if

        if self.expected_period is not None:
            # Check the period of the effect
            if self.effect_type == BacklightEffectType.WAVES_EFFECT:
                periods = [y - x for y, x in zip(self.timestamp_max_value[0][1::], self.timestamp_max_value[0][0:-1])]
            else:
                periods = [y - x for y, x in zip(self.timestamp_max_value[1::], self.timestamp_max_value[0:-1])]
            # end if
            mean_period = sum(periods) / len(periods)
            self.debug_print(f'The mean period of the effect is : {mean_period} seconds')
            mean_error = (mean_period - self.expected_period) / self.expected_period
            if abs(mean_error) > _5_PERCENT:
                warn(f'Period of the effect is not correct, expected : {self.expected_period}, '
                     f'obtained : {mean_period}, error : {mean_error * 100} %')
                status = False
            # end if

            # Check wave goes left to right with good timing
            if self.effect_type == BacklightEffectType.WAVES_EFFECT:
                first_timestamp_max_value_column_0 = self.timestamp_max_value[0][0]
                next_timestamp_max_value_column = [first_timestamp_max_value_column_0]
                for timestamp_max_value_column in self.timestamp_max_value[1::]:
                    for timestamp_max in timestamp_max_value_column:
                        if timestamp_max >= next_timestamp_max_value_column[-1]:
                            next_timestamp_max_value_column.append(timestamp_max)
                            break
                        # end if
                    # end for
                # end for
                delta_timestamp = [y - x for y, x in zip(next_timestamp_max_value_column[1::],
                                                         next_timestamp_max_value_column[0:-1])]
                min_error = \
                    (min(delta_timestamp) - self.expected_delta_duration_between_column) / \
                    self.expected_delta_duration_between_column
                max_error = \
                    (max(delta_timestamp) - self.expected_delta_duration_between_column) / \
                    self.expected_delta_duration_between_column
                max_abs_error = max(abs(min_error), abs(max_error))

                if max_abs_error > _20_PERCENT:
                    warn(f'waves do not go from left to right with good timing, error = {max_abs_error} %')
                    status = False
                # end if
            # end if
        # end if

        if self.check_waveform:
            if not self.is_vertical_wave:
                warn('Led values on vertical axis are not identical')
                status = False
            # end if
            if self.effect_type == BacklightEffectType.BREATHING_EFFECT:
                # compute error on the first period of signal to avoid fadeout period ( nb : for now
                # fade out period is not check on breathing effect)
                # 2 errors are computed :
                # - error_1 : The relative RMS value of the error between signals (RRMSE) ( Very sensitive to the time
                #             lag of signals (delay), but very good indicator of similarity, that why we choose an
                #             error margin of 20%
                #             RRMSE documentation :
                #             https://www.maplesoft.com/support/help/maple/view.aspx?path=SignalProcessing%2FRootMeanSquareError
                #             https://www.analyticsvidhya.com/blog/2021/10/evaluation-metric-for-regression-models/#:~:text=Relative%20Root%20Mean%20Square%20Error,to%20compare%20different%20measurement%20techniques
                # - error_2 : Relative difference of RMS (insensitive to the time shift of signals but two signals of
                #             different shape can have the same value)
                x = array(self.monitored_waveform)
                y = array(self.expected_waveform)
                error_1 = sqrt(((x - y) ** 2).mean() / (y ** 2).mean())
                error_2 = (sqrt((x ** 2).mean()) - sqrt((y ** 2).mean())) / sqrt((y ** 2).mean())
                self.debug_print(f'The mse error of the waveform is  : {error_1 * 100} %, '
                                 f'and the relative difference of RMS is : {error_2 * 100} %')
                if abs(error_1) > _20_PERCENT:
                    warn(f'Waveform does not comply with the spec, RRMSE: {error_1 * 100}  %')
                    status = False
                # end if
                if abs(error_2) > _5_PERCENT:
                    warn(f'Waveform of the effect is not correct, relative difference of RMS : {error_2 * 100}  %')
                    status = False
                # end if
            # end if
        # end if

        if self.check_random_effect:
            warn('Check on the specificity of random effect is not implemented yet')
        # end if
        return status
    # end def check_characteristic

    def update_characteristic(self, leds_value, timestamp):
        """
        Check the characteristic of the backlight effect

        :param leds_value: LED pwm value at a given timestamp
        :type leds_value: ``list[int]``
        :param timestamp: timestamp of the led_pwm_value list
        :type timestamp: ``float``
        """
        raise NotImplementedError()
    # end def update_characteristic

    def set_level_pwm_value(self, max_pwm_value):
        """
        Set ``level_pwm_value`` corresponding to the max pwm value recorded

        :param max_pwm_value: Maximum value of the current effect
        :type max_pwm_value: ``int``
        """
        for expected_value in self._configuration.LEVEL_PWM_VALUE:
            if expected_value - _LOWER_STATIC_EFFECT_MARGIN < max_pwm_value < \
                    expected_value + _UPPER_STATIC_EFFECT_MARGIN:
                self.level_pwm_value = expected_value
                break
            else:
                self.level_pwm_value = max_pwm_value
            # end if
        # end for
    # end def set_level_pwm_value

    def debug_print(self, text):
        """
        Print text, but only when ``self.VERBOSE`` is `True`.

        :param text: Text to print in Verbose mode
        :type text: ``str``
        """
        if self.verbose:
            stdout.write(f'{text}\n')
        # end if
    # end def debug_print
# end class BacklightPatternMixin


class StaticBacklightPattern(BacklightPatternMixin):
    """
    Class use for backlight Static effect pattern characterisation
    """

    def __init__(self, fw_id, previous_effect, max_pwm_value, led_id, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param max_pwm_value: Maximum value of the current static effect
        :type max_pwm_value: ``int``
        :param led_id: 1 Led id to check
        :type led_id: ``int``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``
        """
        BacklightPatternMixin.__init__(self, fw_id, previous_effect, max_pwm_value, layout_type)
        self.effect_type = BacklightEffectType.STATIC_EFFECT
        self._led_id = led_id

        # Possible check for Static effect
        self.check_phase_effect = True
        self.check_stationary_duration = True
        self.check_fade_in_duration = True
        self.check_fade_out_duration = True
        self.check_level = True

        self.state = BacklightPhaseType.UNDETERMINED
        self.previous_state = BacklightPhaseType.UNDETERMINED
        # When static effect is recorded with I2C and when starting to monitor on a stationary phase, no I2C data is
        # sent until fade out. Need to add stationary on state_list
        if self.previous_effect == BacklightEffectType.STATIC_EFFECT:
            self.state_list.append(BacklightPhaseType.STATIONARY)
            self.previous_value = max_pwm_value
            self.previous_state = BacklightPhaseType.STATIONARY
            self.stop_time_fade_in = 0
        else:
            self.previous_value = 0
        # end if
    # end def __init__

    def update_characteristic(self, leds_value, timestamp):
        # See ``BacklightPatternMixin.update_characteristic``
        value = leds_value[self._led_id]
        # Update fade in characteristic
        if self.previous_value < value <= self.level_pwm_value - _LOWER_STATIC_EFFECT_MARGIN :
            self.state = BacklightPhaseType.FADE_IN
            if self.state != self.previous_state:
                self.state_list.append(self.state)
            # end if
            if self.start_time_fade_in is None:
                self.start_time_fade_in = timestamp
            else:
                self.stop_time_fade_in = timestamp
            # end if
        # end if

        if self.level_pwm_value - _LOWER_STATIC_EFFECT_MARGIN < value < \
                self.level_pwm_value + _UPPER_STATIC_EFFECT_MARGIN:
            self.state = BacklightPhaseType.STATIONARY
            if self.state != self.previous_state:
                self.state_list.append(BacklightPhaseType.STATIONARY)
            # end if
        # end if

        # Update fade out characteristic
        if value < self.previous_value and value < self.level_pwm_value - _LOWER_STATIC_EFFECT_MARGIN:
            self.state = BacklightPhaseType.FADE_OUT
            if self.state != self.previous_state:
                if self.previous_state == BacklightPhaseType.FADE_IN:
                    if (timestamp - self.stop_time_fade_in) > _MIN_DURATION_STATIC_EFFECT:
                        self.state_list.append(BacklightPhaseType.STATIONARY)
                    # end if
                # end if
                self.state_list.append(self.state)
            # end if
            if self.start_time_fade_out is None:
                self.start_time_fade_out = timestamp
            else:
                self.stop_time_fade_out = timestamp
            # end if
        # end if

        self.previous_value = value
        self.previous_state = self.state
    # end def update_characteristic
# end class StaticBacklightPattern


class WowBacklightPattern(BacklightPatternMixin):
    """
    Class use for backlight WOW effect pattern characterisation
    """
    def __init__(self, fw_id, previous_effect, max_pwm_value, led_id, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param max_pwm_value: Maximum value of the current Wow effect
        :type max_pwm_value: ``int``
        :param led_id: 1 Led id to check
        :type led_id: ``int``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``
        """
        BacklightPatternMixin.__init__(self, fw_id, previous_effect, max_pwm_value, layout_type)
        self.effect_type = BacklightEffectType.WOW_EFFECT
        self._led_id = led_id

        # Possible check for Wow effect
        self.check_phase_effect = True
        self.check_stationary_duration = True
        self.check_fade_in_duration = True
        self.check_fade_out_duration = True
        self.check_level = True

        self.state = BacklightPhaseType.UNDETERMINED
        self.previous_state = BacklightPhaseType.UNDETERMINED

        self.previous_value = 0
    # end def __init__

    def update_characteristic(self, leds_value, timestamp):
        # See ``BacklightPatternMixin.update_characteristic``
        value = leds_value[self._led_id]
        # Update fade in characteristic
        if value > self.previous_value:
            self.state = BacklightPhaseType.FADE_IN
            self.level_pwm_value = value
            if self.state != self.previous_state:
                self.state_list.append(self.state)
            # end if
            if self.start_time_fade_in is None:
                self.start_time_fade_in = timestamp
            else:
                self.stop_time_fade_in = timestamp
            # end if
        # end if

        # Update fade out characteristic
        if value < self.previous_value:
            self.state = BacklightPhaseType.FADE_OUT
            if self.state != self.previous_state:
                if self.previous_state == BacklightPhaseType.FADE_IN:
                    if (timestamp - self.stop_time_fade_in) > _MIN_DURATION_STATIC_EFFECT:
                        self.state_list.append(BacklightPhaseType.STATIONARY)
                    # end if
                    self.state_list.append(self.state)
                # end if
            # end if
            if self.start_time_fade_out is None:
                self.start_time_fade_out = timestamp
            else:
                self.stop_time_fade_out = timestamp
            # end if
        # end if

        self.previous_value = value
        self.previous_state = self.state
    # end def update_characteristic
# end class WowBacklightPattern


class ContrastBacklightPattern(BacklightPatternMixin):
    """
    Class use for backlight Contrast effect pattern characterisation
    """
    def __init__(self, fw_id, previous_effect, max_pwm_value, led_id_group_keys1, led_id_group_keys2, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param max_pwm_value: Maximum value of the current contrast effect
        :type max_pwm_value: ``int``
        :param led_id_group_keys1: 1 Led id belong to group keys1
        :type led_id_group_keys1: ``int``
        :param led_id_group_keys2: 1 Led id belong to group keys2
        :type led_id_group_keys2: ``int``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``
        """
        BacklightPatternMixin.__init__(self, fw_id, previous_effect, max_pwm_value, layout_type)
        self.effect_type = BacklightEffectType.CONTRAST_EFFECT
        self._led_id_group_keys1 = led_id_group_keys1
        self._led_id_group_keys2 = led_id_group_keys2

        # Possible check for Contrast effect
        self.check_phase_effect = True
        self.check_stationary_duration = True
        self.check_fade_in_duration = True
        self.check_fade_in_group_keys1_duration = True
        self.check_fade_in_delta_group_keys1_vs_2_duration = True
        self.check_fade_in_group_keys2_duration = True
        self.check_fade_out_duration = True
        self.check_level = True

        self.start_time_fade_in_group_keys1 = None
        self.stop_time_fade_in_group_keys1 = None
        self.start_time_fade_in_group_keys2 = None
        self.stop_time_fade_in_group_keys2 = None
        self.start_time_fade_in = None
        self.stop_time_fade_in = None
        self.start_time_fade_out = None
        self.stop_time_fade_out = None
        self.level_pwm_value_group_keys1 = 0
        self.level_pwm_value_group_keys2 = 0
        self.state = BacklightPhaseType.UNDETERMINED
        self.previous_state = BacklightPhaseType.UNDETERMINED
        self.previous_timestamp = 0
        self.previous_value_group_keys1 = 0
        self.previous_value_group_keys2 = 0
    # end def __init__

    def update_characteristic(self, leds_value, timestamp):
        # See ``BacklightPatternMixin.update_characteristic``
        value_group_keys1 = leds_value[self._led_id_group_keys1]
        value_group_keys2 = leds_value[self._led_id_group_keys2]
        # Update group 1 fade in characteristic
        if value_group_keys1 > self.previous_value_group_keys1:
            if self.start_time_fade_in_group_keys1 is None:
                self.start_time_fade_in_group_keys1 = timestamp

            # Workaround : https://jira.logitech.io/browse/ICFM-37
            elif self._configuration.ENABLE_WORKAROUND_ON_CONTRAST_EFFECT:
                if (timestamp - self.start_time_fade_in_group_keys1) < _MAX_FADE_IN_DURATION:
                    self.stop_time_fade_in_group_keys1 = timestamp
                    self.level_pwm_value_group_keys1 = value_group_keys1
                # end if
            # end if
        # end if

        # Update group 2 fade in characteristic
        if value_group_keys2 > self.previous_value_group_keys2:
            if self.start_time_fade_in_group_keys2 is None:
                self.start_time_fade_in_group_keys2 = timestamp

            # Workaround : https://jira.logitech.io/browse/ICFM-37
            elif self._configuration.ENABLE_WORKAROUND_ON_CONTRAST_EFFECT:
                if (timestamp - self.start_time_fade_in_group_keys2) < _MAX_FADE_IN_DURATION:
                    self.stop_time_fade_in_group_keys2 = timestamp
                    self.level_pwm_value_group_keys2 = value_group_keys2
                # end if
            # end if
        # end if

        # Update global fade in (group0 + group1)
        if (value_group_keys1 > self.previous_value_group_keys1) or \
                (value_group_keys2 > self.previous_value_group_keys2):
            if self.start_time_fade_in is None:
                self.start_time_fade_in = timestamp
            # end if

            # Workaround : https://jira.logitech.io/browse/ICFM-37
            if self._configuration.ENABLE_WORKAROUND_ON_CONTRAST_EFFECT:
                if (timestamp - self.start_time_fade_in) < _MAX_FADE_IN_DURATION:
                    self.stop_time_fade_in = timestamp
                    self.state = BacklightPhaseType.FADE_IN
                    if self.state != self.previous_state:
                        self.state_list.append(self.state)
                    # end if
                # end if
            # end if
        # end if

        # Update fade out characteristic
        if (value_group_keys1 < self.previous_value_group_keys1) or \
                (value_group_keys2 < self.previous_value_group_keys2):
            self.state = BacklightPhaseType.FADE_OUT
            if self.state != self.previous_state:
                if self.previous_state == BacklightPhaseType.FADE_IN:
                    if (timestamp - self.stop_time_fade_in) > _MIN_DURATION_STATIC_EFFECT:
                        self.state_list.append(BacklightPhaseType.STATIONARY)
                    # end if
                    self.state_list.append(self.state)
                # end if
            # end if
            if self.start_time_fade_out is None:
                self.start_time_fade_out = timestamp
            # end if
            self.stop_time_fade_out = timestamp
        # end if

        self.previous_value_group_keys1 = value_group_keys1
        self.previous_value_group_keys2 = value_group_keys2
        self.previous_state = self.state
        self.previous_timestamp = timestamp
    # end def update_characteristic
# end class ContrastBacklightPattern


class BreathingBacklightPattern(BacklightPatternMixin):
    """
    Class use for backlight Breathing effect pattern characterisation
    """
    def __init__(self, fw_id, previous_effect, max_pwm_value, led_id, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param max_pwm_value: Maximum value of the current breathing effect
        :type max_pwm_value: ``int``
        :param led_id: 1 Led id to check
        :type led_id: ``int``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``
        """
        BacklightPatternMixin.__init__(self, fw_id, previous_effect, max_pwm_value, layout_type)
        self._led_id = led_id
        self.effect_type = BacklightEffectType.BREATHING_EFFECT
        self.max_pwm_value = max_pwm_value

        # Possible check for Breathing effect
        self.check_level = True
        self.check_period = True
        self.check_waveform = True

        self.timestamp_max_value = []  # list of timestamp corresponding to pwm max value (list[float])
        self.expected_waveform = []  # pwm values waveform from RgbCAlgo (list[int]) used as reference
        self.monitored_waveform = []  # pwm values waveform monitored on LED driver I2C bus (list[int])
        # We use RgbCAlgo to compute the expected waveform with only red value as led intensity
        self.expected_period = self._configuration.BREATHING_EFFECT_PERIOD
        self._frame_rate = self._configuration.BREATHING_FRAME_RATE
        self._period_samples = uint16(round(self.expected_period / self._frame_rate))
        self._rgb_effect = RgbCAlgo()
        self._rgb_effect.led_zone1_param.hsv_comp = RgbCAlgo.rgb_to_hsv(RgbComponents(r=uint16(self.max_pwm_value),
                                                                                      g=uint16(0),
                                                                                      b=uint16(0)))
        self._rgb_effect.br_reset_and_calculate_param(zone_number=self._configuration.BREATHING_ZONE_NUMBER,
                                                      period=self._period_samples)
    # end def __init__

    def update_characteristic(self, leds_value, timestamp):
        # See ``BacklightPatternMixin.update_characteristic``
        value = leds_value[self._led_id]
        # find maximum value to be able to compute the breathing period
        if value == self.max_pwm_value:
            if len(self.timestamp_max_value) == 0:
                self.timestamp_max_value.append(timestamp)
            elif (timestamp - self.timestamp_max_value[-1]) > _MIN_PERIOD_BREATHING_EFFECT:
                self.timestamp_max_value.append(timestamp)
            # end if
        # end if

        # Compute the next expected LED value for breathing effect
        self._rgb_effect.execute_effects(zone_number=self._configuration.BREATHING_ZONE_NUMBER)
        led_zone_param = self._rgb_effect.get_led_param(zone_number=self._configuration.BREATHING_ZONE_NUMBER)
        self.expected_waveform.append(int(self._rgb_effect.gamma_crt8_table(led_zone_param.rgb_comp_out.r)))
        self.monitored_waveform.append(value)
    # end def update_characteristic
# end class BreathingBacklightPattern


class RandomBacklightPattern(BacklightPatternMixin):
    """
    Class use for backlight Random effect pattern characterisation
    """
    def __init__(self, fw_id, previous_effect, max_pwm_value, led_ids, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param max_pwm_value: Maximum value of the current static effect
        :type max_pwm_value: ``int``
        :param led_ids: LED ids to check
        :type led_ids: ``list[int]``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``
        """
        BacklightPatternMixin.__init__(self, fw_id, previous_effect, max_pwm_value, layout_type)
        self.effect_type = BacklightEffectType.RANDOM_EFFECT
        self.max_pwm_value = max_pwm_value
        self._led_ids = led_ids

        self.level_pwm_value = max_pwm_value
        self.led_ids_states = [[BacklightPhaseType.OFF] for _ in led_ids]
        self.states_transition_timing = [[0.0] for _ in led_ids]
        self.previous_data_to_check = [self._configuration.LOW_LEVEL_VALUE for _ in led_ids]
        self.led_ids_on = []

        # Possible check for random effect
        self.check_level = True
        # Todo : Check on the specificity of random effect is not implemented yet
        self.check_random_effect = False
    # end def __init__

    def update_characteristic(self, leds_value, timestamp):
        # See ``BacklightPatternMixin.update_characteristic``
        data_to_check = [leds_value[led_id] for led_id in self._led_ids]
        for i, data in enumerate(data_to_check):
            # For each led search if transition append between BacklightPhaseType
            if data > self.previous_data_to_check[i] and data > self._configuration.LOW_LEVEL_VALUE and \
                    self.led_ids_states[i][-1] != BacklightPhaseType.FADE_IN:
                self.led_ids_states[i].append(BacklightPhaseType.FADE_IN)
                self.states_transition_timing[i].append(timestamp)
            elif self.previous_data_to_check[i] > data > self._configuration.LOW_LEVEL_VALUE \
                    and self.led_ids_states[i][-1] != BacklightPhaseType.FADE_OUT:
                self.led_ids_states[i].append(BacklightPhaseType.FADE_OUT)
                self.states_transition_timing[i].append(timestamp)
            elif data == self.max_pwm_value and self.led_ids_states[i][-1] != BacklightPhaseType.STATIONARY:
                self.led_ids_states[i].append(BacklightPhaseType.STATIONARY)
                self.states_transition_timing[i].append(timestamp)
            elif data <= self._configuration.LOW_LEVEL_VALUE and self.led_ids_states[i][-1] != BacklightPhaseType.OFF:
                self.led_ids_states[i].append(BacklightPhaseType.OFF)
                self.states_transition_timing[i].append(timestamp)
            # end if
        # end for
        self.previous_data_to_check = data_to_check
    # end def update_characteristic
# end class RandomBacklightPattern


class WavesBacklightPattern(BacklightPatternMixin):
    """
    Class use for backlight Waves effect pattern characterisation
    """
    def __init__(self, fw_id, previous_effect, max_pwm_value, led_ids, layout_type):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param previous_effect: Backlight previous effect at the start of the recording
        :type previous_effect: ``BacklightEffectType``
        :param max_pwm_value: Maximum value of the current static effect
        :type max_pwm_value: ``int``
        :param led_ids: LED ids to check
        :type led_ids: ``list[int]``
        :param layout_type: keyboard international layout type
        :type layout_type: ``KeyboardMixin.LAYOUT``
        """
        BacklightPatternMixin.__init__(self, fw_id, previous_effect, max_pwm_value, layout_type)
        self.effect_type = BacklightEffectType.WAVES_EFFECT
        self.max_pwm_value = max_pwm_value
        self._led_ids = led_ids

        # Possible check for Waves effect
        self.check_level = True
        self.expected_period = self._configuration.WAVES_EFFECT_PERIOD

        self.is_vertical_wave = True
        self._key_id_wave_map_horizontal = self._configuration.KEY_ID_WAVE_MAP_HORIZONTAL
        self.expected_delta_duration_between_column = self.expected_period / len(self._key_id_wave_map_horizontal)
        self.timestamp_max_value = [[] for _ in self._key_id_wave_map_horizontal]
    # end def __init__

    def update_characteristic(self, leds_value, timestamp):
        # See ``BacklightPatternMixin.update_characteristic``
        for col, key_ids in enumerate(self._key_id_wave_map_horizontal):
            led_ids = [self._configuration.KEY_ID_TO_LED_ID[key_id] for key_id in key_ids]
            data_to_check = [leds_value[led_id] for led_id in led_ids]

            # check all the keys in the column have the same value
            if not all(x == data_to_check[0] for x in data_to_check):
                self.is_vertical_wave = False
            # end if

            # find maximum value for each column to be able to compute the wave period
            value = data_to_check[0]
            if value == self.max_pwm_value:
                if len(self.timestamp_max_value[col]) == 0:
                    self.timestamp_max_value[col].append(timestamp)
                elif (timestamp - self.timestamp_max_value[col][-1]) > _MIN_PERIOD_BREATHING_EFFECT:
                    self.timestamp_max_value[col].append(timestamp)
                # end if
            # end if
        # end for
    # end def update_characteristic
# end class WavesBacklightPattern

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
