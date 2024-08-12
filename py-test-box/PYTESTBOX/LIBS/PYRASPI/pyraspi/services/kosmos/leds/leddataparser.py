#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.leds.leddataparser.py
:brief: Kosmos LED data parser Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/08/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique
from typing import Dict

from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
TICKS_PER_SEC = FPGA_CURRENT_CLOCK_FREQ
TICKS_PER_MILLI_SEC = TICKS_PER_SEC // 1000
TICKS_PER_MICRO_SEC = TICKS_PER_SEC // 10**6
BACKLIGHT_LED_UPDATE_MILLI_SEC_DURATION = 32  # in ms
BACKLIGHT_LED_UPDATE_TICK_DURATION = BACKLIGHT_LED_UPDATE_MILLI_SEC_DURATION * TICKS_PER_MILLI_SEC

# 5% Tolerance
_95_PERCENT = 95 / 100
_105_PERCENT = 105 / 100


class State:
    """
    LED Data Parser State
    """
    ACTIVE = 0
    INACTIVE = 1
# end class State


@unique
class SchemeType(IntEnum):
    """
    LED Data Parser Scheme Type
    """
    UNDETERMINED = auto()
    OFF = auto()
    STEADY = auto()
    SLOW_BLINKING = auto()
    FAST_BLINKING = auto()
    PULSING = auto()
    CAPS_LOCK_BLINK = auto()
# end class SchemeType


BLINKING_TYPES = [SchemeType.SLOW_BLINKING, SchemeType.FAST_BLINKING, SchemeType.PULSING, SchemeType.CAPS_LOCK_BLINK]


class PulseDuration:
    """
    LED blinking frequency (1 unit is 10ns)
    """
    SLOW_BLINKING_FREQUENCY = 500 * TICKS_PER_MILLI_SEC
    SLOW_BLINKING_LOWER_LIMIT = SLOW_BLINKING_FREQUENCY * _95_PERCENT
    SLOW_BLINKING_UPPER_LIMIT = SLOW_BLINKING_FREQUENCY * _105_PERCENT
    FAST_BLINKING_FREQUENCY = 128 * TICKS_PER_MILLI_SEC
    FAST_BLINKING_LOWER_LIMIT = FAST_BLINKING_FREQUENCY * _95_PERCENT
    FAST_BLINKING_UPPER_LIMIT = FAST_BLINKING_FREQUENCY * _105_PERCENT
    PULSING_FREQUENCY = 1000 * TICKS_PER_MILLI_SEC
    PULSING_LOWER_LIMIT = PULSING_FREQUENCY * _95_PERCENT
    PULSING_UPPER_LIMIT = PULSING_FREQUENCY * _105_PERCENT
    CAPS_LOCK_BLINK_FREQUENCY = 1500 * TICKS_PER_MILLI_SEC
    CAPS_LOCK_BLINK_LOWER_LIMIT = CAPS_LOCK_BLINK_FREQUENCY * _95_PERCENT
    CAPS_LOCK_BLINK_UPPER_LIMIT = CAPS_LOCK_BLINK_FREQUENCY * _105_PERCENT
# end class PulseDuration


SCHEME_STR_MAP = {
    SchemeType.UNDETERMINED: 'undetermined',
    SchemeType.OFF: 'off',
    SchemeType.STEADY: 'steady',
    SchemeType.SLOW_BLINKING: 'slow blinking',
    SchemeType.FAST_BLINKING: 'fast blinking',
    SchemeType.PULSING: 'pulsing',
    SchemeType.CAPS_LOCK_BLINK: 'caps lock blink',
}


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TimeLine:
    """
    This class lists important events and successive scheme transitions within the LEDs monitoring period

    It will keep the list of channels for which the monitoring was enabled
    """
    def __init__(self):
        self.channel_count = 0
        self._channels = {}
        self.transitions = []
        self.transition_iterator = None
        # None if no overrun detected on this timeline
        # Else the index of the channel which triggers the warning
        self.overrun_detected = None
    # end def __init__

    def add_channel(self, channel_id):
        """
        Add a ``Channel`` entry to the list of monitored channels

        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``

        :raise ``AssertionError``: if the given identifier is not part of the known channels
        """
        assert channel_id not in self._channels
        self._channels[channel_id] = Channel(channel_id)
        self.channel_count += 1
    # end def add_channel

    def get_channel(self, channel_id):
        """
        Retrieve a specific channel based on the given identifier

        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``

        :return: The monitored channel
        :rtype: ``Channel``

        :raise ``AssertionError``: if the given identifier is not part of the known channels
        """
        assert channel_id in self._channels
        return self._channels[channel_id]
    # end def get_channel

    def get_channels(self):
        """
        Get all existing channels

        :return: Dictionnary of channel id and Channel object
        :rtype: ``dict[int, Channel]``
        """
        return self._channels
    # end def get_channels

    def add_scheme(self, channel_id, scheme):
        """
        Add a ``LedScheme`` entry to the channel timeline

        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``
        :param scheme: The new LED scheme to include
        :type scheme: ``LedScheme``

        :raise ``AssertionError``: if the given identifier is not part of the known channels
        """
        assert channel_id in self._channels
        self._channels[channel_id].add_scheme(scheme)
    # end def add_scheme

    def add_transition(self, channel_id, source, destination):
        """
        Add a ``Transition`` entry to the timeline

        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``
        :param source: The type of scheme registered before the transition
        :type source: ``SchemeType``
        :param destination: The type of scheme registered after the transition
        :type destination: ``SchemeType``

        :raise ``AssertionError``: if the given identifier is not part of the known channels
        """
        assert channel_id in self._channels
        new_transition = Transition(channel_id, self._channels[channel_id].end_time, source, destination)
        if len(self.transitions) == 0:
            self.transitions.append(new_transition)
        else:
            for index in reversed(range(len(self.transitions))):
                if self.transitions[index] > new_transition:
                    if index == 0:
                        self.transitions = [new_transition] + self.transitions
                    else:
                        continue
                    # end if
                else:
                    self.transitions = self.transitions[:index + 1] + [new_transition] + self.transitions[index + 1:]
                    break
                # end if
            # end for
        # end if
    # end def add_transition

    def get_next_transition(self, channel_id=None, from_last=False, clear_from_last_iterator=True):
        """
        Retrieve the next ``Transition`` registered in the timeline

        NB: the iterator is created during the first method call

        :param channel_id: The unique identifier of the channel for which a transition is required - OPTIONAL
                           None to extend the filtering to all existing channels.
        :type channel_id: ``int`` or ``None``
        :param from_last: Flag indicating that the iterator starts from the end - OPTIONAL
        :type from_last: ``bool``
        :param clear_from_last_iterator: Clear the reversed transition iterator - OPTIONAL
        :type clear_from_last_iterator: ``bool``

        :return: The next transition matching the given channel id
        :rtype: ``Transition``
        """
        next_transition = None
        matching = False
        if self.transition_iterator is None:
            if from_last:
                self.transition_iterator = reversed(self.transitions)
            else:
                self.transition_iterator = iter(self.transitions)
            # end if
        # end if
        while not matching:
            try:
                next_transition = next(self.transition_iterator)
                if channel_id is None or channel_id == next_transition.channel_id:
                    matching = True
                # end if
            except StopIteration:
                self.transition_iterator = None
                return None
            # end try
        # end while

        if from_last and clear_from_last_iterator:
            self.transition_iterator = None
        # end if

        return next_transition
    # end def get_next_transition

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        message = f'TimeLine with {self.channel_count} channel{"s" if self.channel_count > 1 else ""}\n'
        if self.overrun_detected is not None:
            message += f'Overrun detected on channel {self.overrun_detected}'
        # end if
        for channel_id in sorted(self._channels):
            message += f' - {self._channels[channel_id]}'
        # end for
        message += f'TimeLine with {len(self.transitions)} transition{"s" if len(self.transitions) > 1 else ""}\n'
        for transition in self.transitions:
            message += f' - {transition}'
        # end for
        return message
    # end def __str__

    def reset(self):
        """
        Reset transition and channel iterator variables
        """
        self.transition_iterator = None
        for channel_id in self.get_channels():
            channel = self.get_channel(channel_id)
            channel.scheme_iterator = None
        # end for
    # end def reset
# end class TimeLine


class Channel:
    """
    This class stores LED scheme events occuring on a channel
    """
    def __init__(self, channel_id):
        """
        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``
        """
        self.channel_id = channel_id
        self.scheme_count = 0
        self._schemes: Dict[int, LedScheme] = {}
        self.start_time = 0
        self.end_time = 0
        self.scheme_iterator = None
    # end def __init__

    def add_scheme(self, scheme):
        """
        Add a ``LedScheme`` entry into the channel timeline.

        :param scheme: The new LED scheme to include
        :type scheme: ``LedScheme``
        """
        # Compute scheme start and end timings
        scheme.start_time = self.end_time
        scheme.end_time = scheme.start_time
        self._schemes[self.scheme_count] = scheme
        self.scheme_count += 1
    # end def add_scheme

    def get_scheme(self, index=None):
        """
        Retrieve a specific LED scheme from the channel database based on the given index

        :param index: The position of the scheme to retrieve. Default is None to get the last entry - OPTIONAL
        :type index: ``int`` or ``None``

        :return: LedScheme at index
        :rtype: ``LedScheme``
        """
        if len(self._schemes) == 0:
            return None
        elif index is not None:
            # return the required index
            return self._schemes[index]
        else:
            # return the last element
            return self._schemes[self.scheme_count - 1]
        # end if
    # end def get_scheme

    def replace_scheme(self, scheme, index=None):
        """
        Replace a LED scheme by another from the channel database based on the given index

        :param scheme: The new LED scheme to include
        :type scheme: ``LedScheme``
        :param index: The position of the scheme to retrieve. Default is None to get the last entry. - OPTIONAL
        :type index: ``int`` or ``None``

        :raise ``AssertionError``: Invalid scheme index, or no schemes available
        """
        assert len(self._schemes) > 0
        assert (index < len(self._schemes) if index is not None else True)

        if index is not None:
            # update the required index
            self._schemes[index] = scheme
        else:
            # update the last element
            self._schemes[self.scheme_count - 1] = scheme
        # end if
    # end def replace_scheme

    def extend_scheme(self, duration, state=None, disable_statistic=False, is_last=False):
        """
        Update the duration of the last LED scheme in the channel
        It also automatically compute the new end time of the channel.

        :param duration: The time spent on the current scheme
        :type duration: ``float``
        :param state: The high / low state measure on the IO - OPTIONAL
        :type state: ``int``
        :param disable_statistic: Flag to disable statistics computation on partial record - OPTIONAL
        :type disable_statistic: ``bool``
        :param is_last: Flag indicating that the scheme is fanilized - OPTIONAL
        :type is_last: ``bool``

        :raise ``AssertionError``: No schemes available
        """
        assert len(self._schemes) != 0
        # Get the last element
        last_scheme = self._schemes[self.scheme_count - 1]
        last_scheme.extend(duration, state, disable_statistic, is_last)
        # Update channel end timings
        self.end_time += duration
    # end def extend_scheme

    def get_next_scheme(self):
        """
        Retrieve the next ``LedScheme`` registered in the channel

        NB: the iterator is created during the first method call
        """
        if self.scheme_iterator is None:
            self.scheme_iterator = iter(self._schemes.values())
        # end if
        try:
            next_scheme = next(self.scheme_iterator)
        except StopIteration:
            return None
        # end try
        return next_scheme
    # end def get_next_scheme

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        message = f'Channel n°{self.channel_id} starts at {self.start_time / TICKS_PER_MILLI_SEC:.2f} and ends at ' \
                  f'{self.end_time / TICKS_PER_MILLI_SEC:6.2f} ms\n'
        for index in range(self.scheme_count):
            for line in [x for x in str(self.get_scheme(index)).split('\n') if x]:
                message += f'   + {line}\n'
            # end for
        # end for
        return message
    # end def __str__
# end class Channel


class LedScheme:
    """
    This class implements the characteristics of a LED behavior
    """
    DEBUG = False

    def __init__(self, scheme_type=SchemeType.OFF):
        """
        :param scheme_type: The type of LED behavior, defaults to `SchemeType.OFF` - OPTIONAL
        :type scheme_type: ``SchemeType``
        """
        self.type = scheme_type
        self.effect_duration = 0
        self.start_time = 0
        self.end_time = 0
        self.last_state = None
        self.compliance = Compliance()
        self.finalized = False
        if LedScheme.DEBUG:
            self.timing_list = []
        # end if
    # end def __init__

    def extend(self, duration, state=None, disable_statistic=False, is_last=False):
        """
        Update the duration of the LED scheme
        It also automatically compute the new end time of the scheme.

        :param duration: The time spent on the current scheme (1 tick means 10ns)
        :type duration: ``float``
        :param state: The high / low state measure on the IO - OPTIONAL
        :type state: ``int``
        :param disable_statistic: Flag to disable statistics computation on partial record - OPTIONAL
        :type disable_statistic: ``bool``
        :param is_last: Flag indicating that the scheme is fanilized - OPTIONAL
        :type is_last: ``bool``
        """
        self.effect_duration += duration
        self.end_time += duration
        self.last_state = state
        self.finalized = is_last
        if LedScheme.DEBUG:
            self.timing_list.append(duration)
        # end if
    # end def extend

    def is_completed(self):
        """
        Placeholder to match ``BlinkingScheme`` API

        :return: Flag indicating if the last period is completed
        :rtype: ``bool``
        """
        return True
    # end def is_completed

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        message = f'Scheme {SCHEME_STR_MAP[self.type]} lasted {self.effect_duration / TICKS_PER_MILLI_SEC:6.2f} ms\n'
        if self.compliance.is_corrupted():
            message += f' *** {self.compliance}\n'
        # end if
        if LedScheme.DEBUG:
            result = 0
            for value in self.timing_list:
                message += f'{hex(value)} ({value / TICKS_PER_MILLI_SEC:6.2f} ms) + '
                result += value
            # end for
            message += f'= {hex(result)} ({result / TICKS_PER_MILLI_SEC:6.2f} ms)\n'
        # end if
        return message
    # end def __str__
# end class LedScheme


class BlinkingLedScheme(LedScheme):
    """
    This class implements the characteristics of a LED behavior
    """
    def __init__(self, scheme_type=SchemeType.OFF):
        # See ``LedScheme.__init__``
        super().__init__(scheme_type=scheme_type)
        self.period_count = 0
        self.pulse_width = PulseWidth()
        self.period = Period()
        self.duty_cycle = DutyCycle()
    # end def __init__

    def extend(self, duration, state=None, disable_statistic=False, is_last=False):
        # See ``LedScheme.extend``
        super().extend(duration=duration, state=state, disable_statistic=disable_statistic, is_last=is_last)
        if not disable_statistic:
            self._compute_duty_cycle(duration, state)
        # end if
    # end def extend

    def _compute_duty_cycle(self, duration, state):
        """
        Compute the duty cycle as the ratio of the pulse width to the period

        :param duration: The time spent on the current scheme (1 means 10ns)
        :type duration: ``float``
        :param state: The high / low state measure on the IO
        :type state: ``int``
        """
        if state == State.ACTIVE:
            self.pulse_width.update(value=duration)
        else:
            period = self.pulse_width.last + duration
            self.period.update(value=period)
            duty_cycle = self.pulse_width.last / period
            self.duty_cycle.update(value=duty_cycle)
            self.period_count += 1
        # end if
    # end def _compute_duty_cycle

    def is_completed(self):
        """
        Check if both the active and inactive phases has been received

        :return: Flag indicating if the last period is completed
        :rtype: ``bool``
        """
        return self.pulse_width.counter == self.period.counter if not self.finalized else True
    # end def is_completed

    @classmethod
    def from_led_scheme(cls, scheme, scheme_type):
        """
        Create a ``BlinkingLedScheme`` from ``LedScheme``

        :param scheme:  LED scheme
        :type scheme: ``LedScheme``
        :param scheme_type: The scheme category
        :type scheme_type: ``SchemeType``

        :return: Create a ``BlinkingLedScheme`` matching the characteristics of the given scheme
        :rtype: ``BlinkingLedScheme``

        :raise ``AssertionError``: Invalid scheme type
        """
        assert isinstance(scheme, LedScheme)

        blinking_scheme = cls(scheme_type)
        # Compute scheme start and end timings
        blinking_scheme.start_time = scheme.start_time
        blinking_scheme.extend(duration=scheme.effect_duration, state=scheme.last_state,
                               disable_statistic=(False if scheme.last_state == State.ACTIVE else True))
        # Transfer scheme last state and compliance indicator
        blinking_scheme.last_state = scheme.last_state
        blinking_scheme.compliance = scheme.compliance
        return blinking_scheme
    # end def from_led_scheme

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        message = super().__str__()
        half_period = f'{".5" if self.pulse_width.counter > self.period.counter else ""}'
        message += f'  * Statistics computed over {self.period_count}{half_period} ' \
                   f'period{"s" if self.period_count > 1 else ""}\n'
        message += f'  * {self.pulse_width}'
        message += f'  * {self.period}'
        message += f'  * {self.duty_cycle}'

        return message
    # end def __str__
# end class BlinkingLedScheme


class Stat:
    """
    This class stores the variables used in statistics
    """
    def __init__(self):
        self.counter = 0
        self.last = None
        self.mean = None
        self.maxi = None
        self.mini = None
    # end def __init__

    def update(self, value):
        """
        Update statistics with a new measure

        :param value: measured value
        :type value: ``float``

        :raise ``AssertionError``: Invalid counter value
        """
        self.last = value
        if self.mean is None:
            self.mean = value
        else:
            assert self.counter != 0
            self.mean = ((self.mean * self.counter) + value) / (self.counter + 1)
        # end if
        if self.mini is None or value < self.mini:
            self.mini = value
        # end if
        if self.maxi is None or self.maxi < value:
            self.maxi = value
        # end if
        self.counter += 1
    # end def update
# end class Stat


class DutyCycle(Stat):
    """
    This class stores the duty cycle variables
    """
    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        if self.mean is not None:
            return f'Duty cycle average = {self.mean * 100:.2f}%, minimum = {self.mini * 100:.2f}% and ' \
                   f'maximum = {self.maxi * 100:.2f}%\n'
        # end if
        return ''
    # end def __str__
# end class DutyCycle


class Period(Stat):
    """
    This class stores the period variables
    """
    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        if self.mean is not None:
            return f'{self.__class__.__name__} average = {self.mean / TICKS_PER_MILLI_SEC:.2f} ms, ' \
                   f'minimum = {self.mini / TICKS_PER_MILLI_SEC:.2f} ms and ' \
                   f'maximum = {self.maxi / TICKS_PER_MILLI_SEC:.2f} ms\n'
        # end if
        return ''
    # end def __str__
# end class Period


class PulseWidth(Period):
    """
    This class stores the pulse width variables
    """
# end class PulseWidth


class Compliance:
    """
    This class stores the compliance indicator
    """
    def __init__(self):
        self.shorter_pulse_counter = 0
        self.longer_pulse_counter = 0
        self.inactive_state_start = 0
    # end def __init__

    def is_corrupted(self):
        """
        Flag indicating that anomalies have been detected

        :return: Flag indicating if a defect occurs
        :rtype: ``bool``
        """
        if self.shorter_pulse_counter > 0 or self.longer_pulse_counter > 0 or self.inactive_state_start > 0:
            return True
        else:
            return False
        # end if
    # end def is_corrupted

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        message = f"Compliance indicator: {'NOK' if self.is_corrupted() else 'OK'}"
        if self.is_corrupted():
            message += ' ('
            if self.shorter_pulse_counter > 0:
                message += f'{self.shorter_pulse_counter} pulse{"s" if self.shorter_pulse_counter > 1 else ""} shorter,'
            # end if
            if self.longer_pulse_counter > 0:
                message += f'{self.longer_pulse_counter} pulse{"s" if self.longer_pulse_counter > 1 else ""} longer, '
            # end if
            if self.inactive_state_start > 0:
                message += f'The first period starts with an inactive state'
            # end if
            message += ')'
        # end if
        return message
    # end def __str__
# end class Compliance


class Transition:
    """
    This class implements an event occuring when the LED behavior is changing
    """
    def __init__(self, channel_id, timing, source, destination):
        """
        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``
        :param timing: The timestamp of the event
        :type timing: ``flot``
        :param source: The type of scheme registered before the transition
        :type source: ``SchemeType``
        :param destination: The type of scheme registered after the transition
        :type destination: ``SchemeType``
        """
        self.channel_id = channel_id
        self.timing = timing
        self.source = source
        self.destination = destination
    # end def __init__

    def __lt__(self, other):
        """
        Compares the current object with the supplied one.

        :param other: The ``Transition`` instance to compare to
        :type other: ``Transition``

        :return: The result of the comparison with others.
        :rtype: ``bool``

        :raise ``AssertionError``: Invalid Transition type
        """
        assert isinstance(other, Transition)

        return self.timing < other.timing
    # end def __lt__

    def __gt__(self, other):
        """
        Compares the current object with the supplied one.

        :param other: The ``Transition`` instance to compare to
        :type other: ``Transition``

        :return: The result of the comparison with others.
        :rtype: ``bool``

        :raise ``AssertionError``: Invalid Transition type
        """
        assert isinstance(other, Transition)

        return self.timing > other.timing
    # end def __gt__

    def __str__(self):
        """
        Convert the current object to a string

        :return: A readable name for the object
        :rtype: ``str``
        """
        return f'Transition on channel n°{self.channel_id} from ' \
               f'{SCHEME_STR_MAP[self.source] if self.source is not None else "off"} ' \
               f'to {SCHEME_STR_MAP[self.destination]} at {self.timing / TICKS_PER_MILLI_SEC:6.2f} ms\n'
    # end def __str__
# end class Transition


class LedDataParser:
    """
    Raw LED entries parser

    This class parses the data retrieved from the FPGA to extract a usable ``TimeLine`` of the recording
    """
    def __init__(self, channels, clock_gating=0, is_active_high=False):
        """
        :param channels: The channel identifiers for which the LED monitoring has been enabled
        :type channels: ``list[int]``
        :param clock_gating: Clock gating value in cycle counts - OPTIONAL
        :type clock_gating: ``int``
        :param is_active_high: Flag indicating if the LED is active high or low - OPTIONAL
        :type is_active_high: ``bool``
        """
        self.channels = channels
        self.clock_gating = clock_gating
        self.timeline = None
        self.states = None
        self.durations = None
        self.is_active_high = is_active_high

        self.reset()
    # end def __init__

    def reset(self):
        """
        Reset the timeline object
        """
        self.timeline = TimeLine()
        for channel in self.channels:
            self.timeline.add_channel(channel)
        # end for
        self.states = list([None for _ in range(max(self.channels)+1)])
        self.durations = list([0 for _ in range(max(self.channels)+1)])
    # end def reset

    def convert_state(self, raw_state):
        """
        Handle the case when the LED supports the reverse convention

        :param raw_state: The high / low state measure on the IO
        :type raw_state: ``State``

        :return: Active or inactive state
        :rtype: ``State``
        """
        if self.is_active_high and raw_state == State.ACTIVE:
            return State.INACTIVE
        elif self.is_active_high and raw_state == State.INACTIVE:
            return State.ACTIVE
        else:
            return raw_state
        # end if
    # end def convert_state

    def parse_entries(self, leds):
        """
        Parse the raw ``led_spy_entry_t`` structure to create a suitable ``Timeline``

        :param leds: LED entries received from the FPGA
        :type leds: ``list[led_spy_entry_t]``

        :return: A structure with all events that occurred during the LED monitoring period
        :rtype: ``Timeline``
        """
        for i, led in enumerate(leds):
            if led.bit.overrun:
                self.timeline.overrun_detected = led.bit.channel
                if led.bit.counter == 0:
                    continue
                # end if
            # end if
            if self.states[led.bit.channel] is None:
                self.states[led.bit.channel] = self.convert_state(led.bit.state)
            # end if
            if not self.convert_state(led.bit.state) == self.states[led.bit.channel]:
                # transition detected
                self.update_schemes(led.bit.channel, self.states[led.bit.channel], self.durations[led.bit.channel])
                # apply state transition
                self.states[led.bit.channel] = self.convert_state(led.bit.state)
                # restart state duration
                self.durations[led.bit.channel] = led.bit.counter * (1 + self.clock_gating)
            else:
                # increase state duration
                self.durations[led.bit.channel] += led.bit.counter * (1 + self.clock_gating)
            # end if
        # end for
        for channel in self.channels:
            self.update_schemes(channel, self.states[channel], self.durations[channel])
        # end for
        return self.timeline
    # end def parse_entries

    def parse_backlight_led_pwm(self, leds, backlight_led_channel):
        """
        Parse the raw ``led_spy_entry_t`` structure to return the pwm backlight vector

        :param leds: LED entries received from the FPGA
        :type leds: ``list[led_spy_entry_t]``
        :param backlight_led_channel: led ID of the backlight channel
        :type backlight_led_channel: ``int``

        :return: led_timestamps and led_values of the backlight pwm
        :rtype: ``tuple[list, list[list]]``
        """
        timestamp = 0
        clock_gating = 0
        state = None
        duration = 0
        duration_led_update = 0
        duration_state_on = 0
        number_state_on = 0
        duration_state_off = 0
        number_state_off = 0
        led_values = []
        led_timestamps = []

        for i, led in enumerate(leds):
            if led.bit.channel == backlight_led_channel:
                # Warning : No check is done on led.bit.overrun because overrun appends a lot on fade in/out backlight
                # led monitoring when PWM ON is less than 400ns
                if state is None:
                    state = self.convert_state(led.bit.state)
                # end if
                if not self.convert_state(led.bit.state) == state:
                    # update led values every 32 ms
                    if duration_led_update > BACKLIGHT_LED_UPDATE_TICK_DURATION:
                        if number_state_on == number_state_off:
                            led_values.append([round((255 * duration_state_on) / duration_led_update)])
                            led_timestamps.append((timestamp - duration_led_update) / TICKS_PER_SEC)
                            # restart states duration_led_update
                            duration_led_update = 0
                            duration_state_on = 0
                            duration_state_off = 0
                            number_state_on = 0
                            number_state_off = 0
                        # end if
                    # end if

                    # apply state transition
                    state = self.convert_state(led.bit.state)
                    duration_led_update += led.bit.counter * (1 + self.clock_gating)
                    if state == State.ACTIVE:
                        duration_state_on += led.bit.counter * (1 + self.clock_gating)
                        number_state_on += 1
                    else:
                        duration_state_off += led.bit.counter * (1 + self.clock_gating)
                        number_state_off += 1
                    # end if
                    # restart state duration
                    duration = led.bit.counter * (1 + self.clock_gating)
                else:
                    # increase state duration_led_update
                    duration += led.bit.counter * (1 + clock_gating)
                    duration_led_update += led.bit.counter * (1 + clock_gating)
                    # increase state_on or state_off duration_led_update
                    if state == State.ACTIVE:
                        duration_state_on += led.bit.counter * (1 + clock_gating)
                    else:
                        duration_state_off += led.bit.counter * (1 + clock_gating)
                    # end if
                # end if
                timestamp += led.bit.counter * (1 + clock_gating)
            # end if
        # end for
        if duration_led_update > BACKLIGHT_LED_UPDATE_TICK_DURATION:
            led_values.append([round((255 * duration_state_on) / duration_led_update)])
            led_timestamps.append((timestamp - duration_led_update) / TICKS_PER_SEC)
        # end if

        return led_timestamps, led_values
    # end def parse_backlight_led_pwm

    def update_schemes(self, channel_id, state, duration):
        """
        Update the ``Timeline`` internal variables with the provided characteristics

        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``
        :param state: The high / low state measure on the IO
        :type state: ``int``
        :param duration: The time spent on the previous scheme
        :type duration: ``float``
        """
        current_channel = self.timeline.get_channel(channel_id=channel_id)
        current_scheme = current_channel.get_scheme()
        if current_scheme is not None:
            current_type = current_scheme.type
        else:
            current_type = None
        # end if
        if current_type is not None and PulseDuration.CAPS_LOCK_BLINK_LOWER_LIMIT <= duration <= \
                PulseDuration.CAPS_LOCK_BLINK_UPPER_LIMIT:
            # Extend caps lock blinking scheme
            self.extend_blinking_scheme(channel_id, state, duration, SchemeType.CAPS_LOCK_BLINK)
        elif current_type is not None and PulseDuration.PULSING_LOWER_LIMIT <= duration <= \
                PulseDuration.PULSING_UPPER_LIMIT:
            # Extend fast blinking scheme
            self.extend_blinking_scheme(channel_id, state, duration, SchemeType.PULSING)
        elif current_type is not None and PulseDuration.FAST_BLINKING_LOWER_LIMIT <= duration <= \
                PulseDuration.FAST_BLINKING_UPPER_LIMIT:
            # Extend fast blinking scheme
            self.extend_blinking_scheme(channel_id, state, duration, SchemeType.FAST_BLINKING)
        elif current_type is not None and PulseDuration.SLOW_BLINKING_LOWER_LIMIT <= duration <= \
                PulseDuration.SLOW_BLINKING_UPPER_LIMIT:
            # Extend slow blinking scheme
            self.extend_blinking_scheme(channel_id, state, duration, SchemeType.SLOW_BLINKING)
        elif current_type == SchemeType.FAST_BLINKING and duration < 270 * TICKS_PER_MILLI_SEC:
            # TODO - remove workaround when detection discontinuity in Fast blinking scheme
            current_channel.extend_scheme(duration, state, is_last=True)
            if duration < PulseDuration.FAST_BLINKING_LOWER_LIMIT:
                current_scheme.compliance.shorter_pulse_counter += 1
            else:
                current_scheme.compliance.longer_pulse_counter += 1
            # end if
        elif current_type in BLINKING_TYPES and state == State.INACTIVE and not current_scheme.is_completed():
            # Handle end of blinking scheme
            if ((current_type == SchemeType.FAST_BLINKING and duration < PulseDuration.FAST_BLINKING_LOWER_LIMIT) or
                    (current_type == SchemeType.SLOW_BLINKING and duration < PulseDuration.SLOW_BLINKING_LOWER_LIMIT)
                    or (current_type == SchemeType.PULSING and duration < PulseDuration.PULSING_LOWER_LIMIT)
                    or (current_type == SchemeType.CAPS_LOCK_BLINK and
                        duration < PulseDuration.CAPS_LOCK_BLINK_LOWER_LIMIT)):
                # Final extension of the blinking scheme: add incomplete period but disable the statistics computation
                current_channel.extend_scheme(duration, state, disable_statistic=True, is_last=True)
            elif current_scheme.period.mean is not None:
                # End of blinking scheme merged with the following 'off' scheme
                estimated_blinking_duration = int(current_scheme.period.mean - current_scheme.pulse_width.last)
                current_channel.extend_scheme(estimated_blinking_duration, state, disable_statistic=True, is_last=True)
                self.timeline.add_transition(channel_id=channel_id, source=current_type, destination=SchemeType.OFF)
                self.timeline.add_scheme(channel_id=channel_id, scheme=LedScheme(SchemeType.OFF))
                current_channel.extend_scheme(duration - estimated_blinking_duration)
            else:
                print(f'previous pulse_width={current_scheme.pulse_width.last}')
                print(f'current duration={duration}')
            # end if
        elif current_type in [None, SchemeType.OFF] and duration <= PulseDuration.SLOW_BLINKING_LOWER_LIMIT:
            # When starting to parse the LED data, the first block is not enough to differentiate between all the scheme
            # That s why the scheme is set to undetermined
            if current_type == SchemeType.OFF:
                self.timeline.add_transition(channel_id=channel_id, source=current_type,
                                             destination=SchemeType.UNDETERMINED)
            # end if
            self.timeline.add_scheme(channel_id=channel_id, scheme=LedScheme(SchemeType.UNDETERMINED))
            current_channel.extend_scheme(duration, state=state)
            current_channel.get_scheme().compliance.shorter_pulse_counter += 1
        elif state == State.ACTIVE:
            # Steady
            if current_type == SchemeType.UNDETERMINED:
                self.convert_from_undetermined(channel_id=channel_id, new_scheme_type=SchemeType.OFF)
                current_type = SchemeType.OFF
            # end if
            if current_type is not None and current_type != SchemeType.STEADY:
                self.timeline.add_transition(channel_id=channel_id, source=current_type, destination=SchemeType.STEADY)
            # end if
            if current_type is None or current_type != SchemeType.STEADY:
                self.timeline.add_scheme(channel_id=channel_id, scheme=LedScheme(SchemeType.STEADY))
            # end if
            current_channel.extend_scheme(duration)
        else:
            # Off
            if current_type == SchemeType.UNDETERMINED:
                self.convert_from_undetermined(channel_id=channel_id, new_scheme_type=SchemeType.STEADY)
                current_type = SchemeType.STEADY
            # end if
            if current_type is not None and current_type != SchemeType.OFF:
                self.timeline.add_transition(channel_id=channel_id, source=current_type, destination=SchemeType.OFF)
            # end if
            if current_type is None or current_type != SchemeType.OFF:
                self.timeline.add_scheme(channel_id=channel_id, scheme=LedScheme(SchemeType.OFF))
            # end if
            current_channel.extend_scheme(duration)
        # end if
    # end def update_schemes

    def extend_blinking_scheme(self, channel_id, state, duration, scheme_type):
        """
        Extend the duration of the current blinking scheme if the given scheme type is matching
        else add a transition and create a new blinking scheme.

        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``
        :param state: The high / low state measure on the IO
        :type state: ``int``
        :param duration: The time spent on the previous scheme
        :type duration: ``float``
        :param scheme_type: The scheme category
        :type scheme_type: ``SchemeType``
        """
        current_channel = self.timeline.get_channel(channel_id=channel_id)
        current_scheme = current_channel.get_scheme()
        if current_scheme is not None:
            current_type = current_scheme.type
        else:
            current_type = None
        # end if
        # Extend the existing blinking scheme
        if current_type == scheme_type:
            current_channel.extend_scheme(duration, state)
        elif current_type == SchemeType.UNDETERMINED:
            # Convert the undetermined scheme into a blinking one
            self.convert_from_undetermined(channel_id=channel_id, new_scheme_type=scheme_type)
            current_channel.extend_scheme(duration, state)
        else:
            if current_type is not None:
                # End the preceding scheme
                self.timeline.add_transition(channel_id=channel_id, source=current_type, destination=scheme_type)
            # end if
            # Create a new blinking one
            self.timeline.add_scheme(channel_id=channel_id, scheme=BlinkingLedScheme(scheme_type))
            if state == State.ACTIVE:
                # Requirement: scheme shall start at 100% (i.e with an active state)
                current_channel.extend_scheme(duration, state)
            else:
                # This use case shall not occur - track the issue by setting the ``Compliance`` parameter
                current_channel.extend_scheme(duration, state, disable_statistic=True)
                if current_scheme is None:
                    current_scheme = current_channel.get_scheme()
                # end if
                current_scheme.compliance.inactive_state_start += 1
            # end if
        # end if
    # end def extend_blinking_scheme

    def convert_from_undetermined(self, channel_id, new_scheme_type):
        """
        Convert an undetermined Scheme into a known one

        :param channel_id: The unique identifier of the monitored channel, starting at 0.
        :type channel_id: ``int``
        :param new_scheme_type: The scheme category to convert to
        :type new_scheme_type: ``SchemeType``
        """
        current_channel = self.timeline.get_channel(channel_id=channel_id)
        current_scheme = current_channel.get_scheme()
        if new_scheme_type in BLINKING_TYPES:
            # Convert the undetermined scheme into a blinking one
            current_channel.replace_scheme(BlinkingLedScheme.from_led_scheme(current_scheme, new_scheme_type))
        else:
            current_scheme.type = new_scheme_type
        # end if
        if len(self.timeline.transitions) > 0:
            transition = self.timeline.get_next_transition(channel_id=channel_id, from_last=True)
            if transition is not None and transition.destination == SchemeType.UNDETERMINED:
                transition.destination = new_scheme_type
            # end if
        # end if
    # end def convert_from_undetermined
# end class LedDataParser

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
