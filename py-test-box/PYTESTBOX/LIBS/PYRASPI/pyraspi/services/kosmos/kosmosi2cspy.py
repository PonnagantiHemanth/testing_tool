#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.kosmosi2cspy
:brief: Kosmos I2C Spy Control Class
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/01/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from enum import IntEnum
from enum import auto
from enum import unique
from sys import stdout
from typing import List

from numpy import array
from numpy import isnan
from numpy import mean
from numpy import zeros

from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import LedSpyOverI2cInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.numeral import Numeral
from pyraspi.services.daemon import Daemon
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.config.backlightconfiguration import GET_BACKLIGHT_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.commonbacklightconfiguration import \
    MechanicalBacklightConfiguration
from pyraspi.services.kosmos.fpgatransport import ExtractPayloadError
from pyraspi.services.kosmos.i2c.leddrivericframesparser import GET_I2C_LED_DRIVER_BY_ID
from pyraspi.services.kosmos.i2cspyparser import I2cSpyFrameParser
from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.leds.leddataparser import LedDataParser
from pyraspi.services.kosmos.leds.leddataparser import State
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_SEC
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.i2cspy import I2C_SPY_MODE_FRAME
from pyraspi.services.kosmos.module.i2cspy import I2C_SPY_MODE_RAW
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_0
from pyraspi.services.kosmos.protocol.generated.messages import led_spy_entry_t


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
@unique
class ReactionState(IntEnum):
    """
    Reaction backlight state
    """
    ON = auto()
    OFF = auto()
    RAMP_DOWN = auto()
    UNKNOWN = auto()
# end class ReactionState


class LedDriverIcI2cFramesParser:
    """
    Parse the data retrieved from the i2c_spy_parser to extract a usable leds pwm values timeline
    """
    MAX_COUNTER_VALUE = 0xFFFFFF
    # Maximum timestamp difference between spy0 and spy1 to consider that they belong to the same frame
    # Todo : Need to do investigation on this value and implement the condition where the delta timestamp is greater
    #  than this value
    MAXIMUM_TIMESTAMP_DIFFERENCE_BETWEEN_SPY0_AND_SPY1 = 0.1  # in seconds

    def __init__(self, fw_id):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``

        :raise ``AssertionError``: If the firmware identifier is not in its valid range
        """
        assert fw_id in GET_I2C_LED_DRIVER_BY_ID, f"fw_id {fw_id} not supported"
        self._fw_id = fw_id

        # Result from LedDriverIcI2cFramesParser for i2c_spy0
        self.i2c_spy0_buffer_values = []
        self.i2c_spy0_buffer_timestamp = []
        self.is_i2c_spy0_buffer_parsed = False
        # Result from LedDriverIcI2cFramesParser for i2c_spy1
        self.i2c_spy1_buffer_values = []
        self.i2c_spy1_buffer_timestamp = []
        self.is_i2c_spy1_buffer_parsed = False
        # Monitoring period
        self._capture_duration = None
    # end def __init__

    @property
    def capture_duration(self):
        """
        Get the duration of the LED monitoring.

        :return: Time during which the monitoring has been active
        :rtype: ``float``
        """
        return self._capture_duration
    # end def property getter capture_duration

    @capture_duration.setter
    def capture_duration(self, value):
        """
        Set the duration of the LED monitoring.

        :param value: Time during which the monitoring has been active
        :type value: ``float``
        """
        self._capture_duration = value
    # end def property setter capture_duration

    def parse_entries(self, i2c_spy_parser, i2c_id=0):
        """
        Parse the i2c spy parser to extract a usable leds pwm values timeline

        :param i2c_spy_parser: I2c spy parser
        :type i2c_spy_parser: ``I2cSpyFrameParser`` or ``I2cSpyRawParser``

        :param i2c_id: I2C SPY module instance identifier - OPTIONAL
        :type i2c_id: ``int``
        """
        driver_ic_parser = GET_I2C_LED_DRIVER_BY_ID[self._fw_id]
        driver_ic_parser.reset()
        for frame_run in i2c_spy_parser.frame_runs:
            for frame in frame_run:
                if (frame.time - driver_ic_parser.led_ic_buffer_spy_timestamp) > \
                        driver_ic_parser.MAXIMUM_TIMESTAMP_DIFFERENCE_BETWEEN_DATA_ON_A_SAME_FRAME and \
                        driver_ic_parser.led_ic_buffer_state == driver_ic_parser.BufferStatus.BUFFER_IN_PROGRESS:
                    # Buffer is not empty but the difference between the new data and the last data are too important,
                    # so it is considered that this is a new frame.
                    # add the next values and timestamp
                    if i2c_id == 1:
                        self.i2c_spy1_buffer_values.append(driver_ic_parser.get_led_spy_buffer())
                        self.i2c_spy1_buffer_timestamp.append(driver_ic_parser.led_ic_buffer_spy_timestamp)
                    else:
                        self.i2c_spy0_buffer_values.append(driver_ic_parser.get_led_spy_buffer())
                        self.i2c_spy0_buffer_timestamp.append(driver_ic_parser.led_ic_buffer_spy_timestamp)
                    # end if
                # end if
                driver_ic_parser.update(frame, i2c_id)
                if driver_ic_parser.led_ic_buffer_state == driver_ic_parser.BufferStatus.BUFFER_FULL:
                    # add the next values and timestamp
                    if i2c_id == 1:
                        self.i2c_spy1_buffer_values.append(driver_ic_parser.get_led_spy_buffer())
                        self.i2c_spy1_buffer_timestamp.append(driver_ic_parser.led_ic_buffer_spy_timestamp)
                    else:
                        self.i2c_spy0_buffer_values.append(driver_ic_parser.get_led_spy_buffer())
                        self.i2c_spy0_buffer_timestamp.append(driver_ic_parser.led_ic_buffer_spy_timestamp)
                    # end if
                # end if
            # end for
        # end for
        if i2c_id == 1:
            self.is_i2c_spy1_buffer_parsed = True
        else:
            self.is_i2c_spy0_buffer_parsed = True
        # end if

        if self.is_i2c_spy1_buffer_parsed and self.is_i2c_spy0_buffer_parsed:
            # Data concatenation of the 2 I2C parser
            if len(self.i2c_spy1_buffer_timestamp) == len(self.i2c_spy1_buffer_timestamp):
                for i, (t0, t1, v0, v1) in enumerate(zip(self.i2c_spy0_buffer_timestamp,
                                                         self.i2c_spy1_buffer_timestamp,
                                                         self.i2c_spy0_buffer_values,
                                                         self.i2c_spy1_buffer_values)):
                    # Check the timestamp difference between spy0 and spy1 to consider that they belong to the same
                    # frame
                    if abs(t0 - t1) < self.MAXIMUM_TIMESTAMP_DIFFERENCE_BETWEEN_SPY0_AND_SPY1:
                        self.i2c_spy0_buffer_values[i] = []
                        for led_data0, led_data1 in zip(v0, v1):
                            is_led_data0_nan = isnan(led_data0.r) or isnan(led_data0.g) or isnan(led_data0.b)
                            if is_led_data0_nan:
                                self.i2c_spy0_buffer_values[i].append(led_data1)
                            else:
                                self.i2c_spy0_buffer_values[i].append(led_data0)
                            # end if
                        # end for
                    else:
                        warnings.warn("Timestamp difference between I2C and I2C1 are too important, no method is "
                                      "implemented to handle this case")
                    # end if
                # end for
            else:
                warnings.warn("Concatenation of data packets with different length is not implemented")
            # end if
        # end if
    # end def parse_entries

    def convert_i2c_to_pwm(self, pwm_led_ids):
        """
        Convert the parsed data to a ``led_spy_entry_t`` that can be used by ``LedDataParser``.

        :param pwm_led_ids: List of LED identifiers
        :type pwm_led_ids:``list[LED_ID]``

        :return: The converted entries for the given list of LED identifiers
        :rtype: ``list[led_spy_entry_t]``
        """
        led_spy_entries = []
        if len(self.i2c_spy0_buffer_timestamp) == 0 or len(self.i2c_spy0_buffer_values) == 0:
            return led_spy_entries
        # end if
        led_id_map = GET_BACKLIGHT_CONFIGURATION_BY_ID[self._fw_id][KeyboardMixin.LAYOUT.DEFAULT].PWM_LED_ID_TO_LED_ID
        led_indexes = [led_id_map[x] for x in pwm_led_ids if x in led_id_map]
        led_i2c_zip = zip(self.i2c_spy0_buffer_timestamp, self.i2c_spy0_buffer_values)
        previous_timestamp, previous_value = led_i2c_zip.__next__()
        # Handle the first frame values
        if previous_timestamp > MechanicalBacklightConfiguration.REACTION_UPDATE_LED_TIME:
            duration = int(previous_timestamp * TICKS_PER_SEC)
            entry_count = (duration >> Numeral(self.MAX_COUNTER_VALUE).bitCount())
            for _ in range(entry_count):
                for led_index in led_indexes:
                    entry = led_spy_entry_t()
                    entry.bit.channel = list(led_id_map.values()).index(led_index)
                    entry.bit.counter = self.MAX_COUNTER_VALUE
                    entry.bit.state = State.INACTIVE
                    led_spy_entries.append(entry)
                # end for
            # end for
            # Force an inactive state on all LEDs while no regular I2C frames are sent by the DUT
            for led_index in led_indexes:
                entry = led_spy_entry_t()
                entry.bit.channel = list(led_id_map.values()).index(led_index)
                entry.bit.counter = duration & self.MAX_COUNTER_VALUE
                entry.bit.state = State.INACTIVE
                led_spy_entries.append(entry)
            # end for
        # end if
        # Handle the next frames values
        for timestamp, value in led_i2c_zip:
            duration = int((timestamp - previous_timestamp) * TICKS_PER_SEC)
            entry_count = duration >> 24
            for _ in range(entry_count):
                for led_index in led_indexes:
                    entry = led_spy_entry_t()
                    entry.bit.channel = list(led_id_map.values()).index(led_index)
                    entry.bit.counter = self.MAX_COUNTER_VALUE
                    entry.bit.state = State.ACTIVE if previous_value[led_index] == 0xFF else State.INACTIVE
                    led_spy_entries.append(entry)
                # end for
            # end for
            for led_index in led_indexes:
                entry = led_spy_entry_t()
                entry.bit.channel = list(led_id_map.values()).index(led_index)
                entry.bit.counter = duration & self.MAX_COUNTER_VALUE
                entry.bit.state = State.ACTIVE if previous_value[led_index] == 0xFF else State.INACTIVE
                led_spy_entries.append(entry)
            # end for
            previous_timestamp = timestamp
            previous_value = value
        # end for

        # Handle end of sequence
        # TODO: update actual duration value when monitoring time is available
        if self.capture_duration is not None:
            final_duration = int((self.capture_duration - previous_timestamp) * TICKS_PER_SEC)
            entry_count = final_duration >> 24
            for _ in range(entry_count):
                for led_index in led_indexes:
                    entry = led_spy_entry_t()
                    entry.bit.channel = list(led_id_map.values()).index(led_index)
                    entry.bit.counter = self.MAX_COUNTER_VALUE
                    entry.bit.state = State.ACTIVE if previous_value[led_index] == 0xFF else State.INACTIVE
                    led_spy_entries.append(entry)
                # end for
            # end for
            # Force an inactive state on all LEDs while no regular I2C frames are sent by the DUT
            for led_index in led_indexes:
                entry = led_spy_entry_t()
                entry.bit.channel = list(led_id_map.values()).index(led_index)
                entry.bit.counter = final_duration & self.MAX_COUNTER_VALUE
                entry.bit.state = State.ACTIVE if previous_value[led_index] == 0xFF else State.INACTIVE
                led_spy_entries.append(entry)
            # end for
        # end if

        # Reset local variables
        self.i2c_spy0_buffer_values = []
        self.i2c_spy0_buffer_timestamp = []

        return led_spy_entries
    # end def convert_i2c_to_pwm
# end class LedDriverIcI2cFramesParser


class KosmosLedSpyOverI2c(LedSpyOverI2cInterface):
    """
    Interface for KOSMOS I2C led monitoring module.
    """
    VERBOSE = False

    @unique
    class STATE(IntEnum):
        """
        I2C data parsing state
        """
        NOT_STARTED = auto()
        IN_PROGRESS = auto()
        COMPLETED = auto()
    # end class STATE

    _i2c_spy_frame_parsers: List[I2cSpyFrameParser]
    _led_frame_parser: LedDriverIcI2cFramesParser
    _led_frame_parsing_state: STATE

    def __init__(self, kosmos, fw_id):
        """
        :param kosmos: an instance of a ``Kosmos`` class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``

        :raise ``AssertionError``: multiple source of error:
         - If not Kosmos hardware
         - If the firmware identifier is not in its valid range
        """
        assert Daemon.is_host_kosmos(), 'This class supports only Kosmos hardware'
        assert fw_id in GET_I2C_LED_DRIVER_BY_ID, f"fw_id {fw_id} not supported"
        assert len(kosmos.dt.i2c_spy), 'No I2C SPY module found in Kosmos firmware'

        self._fw_id = fw_id
        self._kosmos = kosmos

        self._i2c_spy_module_available_ids = GET_I2C_LED_DRIVER_BY_ID[fw_id].i2c_spy_module_available_ids
        self._i2c_spy_frame_parsers = [
            I2cSpyFrameParser(fpga_clock_freq_hz=FPGA_CURRENT_CLOCK_FREQ) for _ in self._kosmos.dt.i2c_spy]
        self._led_frame_parser = LedDriverIcI2cFramesParser(fw_id=self._fw_id)
        self._led_frame_parsing_state = self.STATE.NOT_STARTED
        self._led_backlight_parsing_state = self.STATE.NOT_STARTED
        self._led_identifiers = None
        self._led_monitoring_duration = None

        if fw_id in GET_BACKLIGHT_CONFIGURATION_BY_ID:
            self._configuration = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id]
        # end if

        self._check_pods_configuration()
    # end def __init__

    def get_channel_id(self, led_id):
        """
        Retrieve the channel id from the led identifier

        :param led_id: unique LED identifier to monitor
        :type led_id: ``LED_ID``

        :return: The unique identifier of the monitored channel, starting at 0.
        :rtype: ``int``
        """
        return list(self._configuration[KeyboardMixin.LAYOUT.DEFAULT].PWM_LED_ID_TO_LED_ID).index(led_id)
    # end def get_channel_id

    def start(self, reset=True, led_identifiers=None):
        # See ``LedSpyOverI2cInterface.start``
        self._led_identifiers = led_identifiers

        if reset:
            # Reset I2C module via CPU, to reset hardware and software
            for i2c_spy in self._kosmos.dt.i2c_spy:
                i2c_spy.reset_module()
            # end for

            # Configure I2C SPY module in frame mode
            for i2c_spy in self._kosmos.dt.i2c_spy:
                i2c_spy.mode = I2C_SPY_MODE_FRAME
            # end for

            # Reinitialize frames parser after module reset
            for index, i2c_spy in enumerate(self._kosmos.dt.i2c_spy):
                self._i2c_spy_frame_parsers[index] = i2c_spy.get_parser()
            # end for

            # Reinitialize led driver i2c frames parser
            self._led_frame_parser = LedDriverIcI2cFramesParser(fw_id=self._fw_id)
        # end if

        # Prepare test sequence
        is_offline_enabled = self._kosmos.sequencer.offline_mode
        if not is_offline_enabled:
            self._kosmos.sequencer.offline_mode = True
        # end if

        # Start I2C module via PES
        for i2c_spy in self._kosmos.dt.i2c_spy:
            self._kosmos.pes.execute(action=i2c_spy.action_event.START)
            self.debug_print(f'[{i2c_spy.name}] Capturing I2C traffic...')
        # end for

        # Start timer
        self._kosmos.timers.restart(timers=[TIMER.STOPWATCH_1])

        if not is_offline_enabled:
            self._kosmos.sequencer.offline_mode = False
            self._kosmos.sequencer.play_sequence()
        # end if
        self._kosmos._enable_i2c_monitoring = True
    # end def start

    def stop(self, parse_i2c_frame=True):
        # See ``LedSpyOverI2cInterface.stop``
        if self._kosmos._enable_i2c_monitoring:
            # Stop I2C module (reset and hold I2C state machine)
            for i2c_spy in self._kosmos.dt.i2c_spy:
                self.debug_print(f'[{i2c_spy.name}] Capture STOP.')
                self._kosmos.pes.execute(action=i2c_spy.action_event.STOP)
            # end for

            # Save Stop watch Timer 1
            self._kosmos.timers.save(timers=[TIMER.STOPWATCH_1])
            try:
                for index, i2c_spy in enumerate(self._kosmos.dt.i2c_spy):
                    status_after_stop = i2c_spy.stop_capture()
                    self.debug_print(f'[{i2c_spy.name}] Flush FIFO :({status_after_stop.fifo_count} entries in FIFO).')
                # end for
            except AssertionError as e:
                if str(e) in [f'[{i2c_spy.name}] Buffer is overrun.' for i2c_spy in self._kosmos.dt.i2c_spy]:
                    # Reset I2C module via CPU, to reset hardware and software
                    for i2c_spy in self._kosmos.dt.i2c_spy:
                        i2c_spy.reset_module()
                        i2c_spy.mode = I2C_SPY_MODE_RAW
                    # end for
                    self._kosmos._enable_i2c_monitoring = False

                    # Clear local PES buffer
                    self._kosmos.dt.pes.clear()
                    # Reset the PES TIMERS module
                    self._kosmos.dt.timers.reset_module()
                    raise e
                # end if
            # end try

            # Flush I2C SPY FIFO
            for i2c_spy in self._kosmos.dt.i2c_spy:
                i2c_spy.flush_fifo_to_buffer()
            # end for

            # Play sequence
            self._kosmos.sequencer.play_sequence()

            # Download I2C frames
            self.download()

            # Download time marks
            timemarks = self._kosmos.timers.download()
            self._led_frame_parser.capture_duration = timemarks[TIMER.STOPWATCH_1][0] / FPGA_CURRENT_CLOCK_FREQ

            if parse_i2c_frame:
                # Parse I2C frames to led driver frame
                for index, i2c_spy_frame_parser in enumerate(self._i2c_spy_frame_parsers):
                    self._led_frame_parser.parse_entries(i2c_spy_frame_parser, i2c_id=index)
                # end for
                self._led_frame_parsing_state = self.STATE.COMPLETED
            else:
                # Reset the parsing status
                self._led_frame_parsing_state = self.STATE.NOT_STARTED
            # end if
            self._kosmos._enable_i2c_monitoring = False
        # end if

        for i2c_spy in self._kosmos.dt.i2c_spy:
            i2c_spy.mode = I2C_SPY_MODE_RAW
        # end for
    # end def stop

    def download(self):
        # See ``LedSpyOverI2cInterface.download``
        raw_i2c_buffers = []
        # Download buffer
        for index, i2c_spy in enumerate(self._kosmos.dt.i2c_spy):
            status = i2c_spy.status()
            self.debug_print(f'[{i2c_spy.name}] Downloading capture data ({status.buffer_count} entries in buffer)...')
            try:
                raw_i2c_buffers.append(i2c_spy.download(count=status.buffer_count))
            except ExtractPayloadError as e:
                if str(e) in (
                        "Unexpected Status Message, with return code 0x07:MSG_REPLY_RETURN_CODE_BUFFER_UNDERRUN",):
                    # Reset I2C module via CPU, to reset hardware and software
                    i2c_spy.reset_module()
                    # Reset the PES TIMERS module
                    self._kosmos.dt.timers.reset_module()
                    raise e
                # end if
            # end try
        # end for

        # Parse I2C SPY buffer into frames
        for index, buffer in enumerate(raw_i2c_buffers):
            self._i2c_spy_frame_parsers[index].parse(buffer)
        # end for

        # Print I2C SPY frames
        for frame_parser in self._i2c_spy_frame_parsers:
            self.debug_print(repr(frame_parser))
        # end for

        # Reset the parsing status
        self._led_frame_parsing_state = self.STATE.NOT_STARTED
    # end def download

    def get_timeline(self):
        # See ``LedSpyOverI2cInterface.get_timeline``
        if self._led_frame_parsing_state == self.STATE.NOT_STARTED:
            # Parse I2C frames to led driver frame
            self._led_frame_parser.parse_entries(self._i2c_spy_frame_parsers[0])
            self._led_frame_parsing_state = self.STATE.COMPLETED
        # end if

        # Parse I2C frames to led driver frame
        leds = self._led_frame_parser.convert_i2c_to_pwm(self._led_identifiers)
        led_id_map = self._configuration[KeyboardMixin.LAYOUT.DEFAULT].PWM_LED_ID_TO_LED_ID
        channels = [list(led_id_map).index(x) for x in self._led_identifiers if x in led_id_map]
        led_data_parser = LedDataParser(channels=channels)
        led_timeline = led_data_parser.parse_entries(leds)
        return led_timeline
    # end def get_timeline

    def parse_backlight_i2c(self):
        """
        Post process the data received through the Stream Channel of the backlight I2C

        :return: led_timestamps and led_values of the backlight I2C
        :rtype: ``tuple[list[float], list[list[int]]]``
        """
        if self._led_frame_parsing_state == self.STATE.NOT_STARTED:
            # Parse I2C frames to led driver frame
            self._led_frame_parser.parse_entries(self._i2c_spy_frame_parsers[0])
            self._led_frame_parsing_state = self.STATE.COMPLETED
        # end if
        return self._led_frame_parser.i2c_spy0_buffer_timestamp, self._led_frame_parser.i2c_spy0_buffer_values
    # end def parse_backlight_i2c

    def parse_rgb_i2c(self, enable_i2c0=True, enable_i2c1=False):
        """
        Post process the data received through the Stream Channel of the RGB I2C

        :param enable_i2c0: Flag to enable the rgb parsing on i2c_0 spy module (default is True) - OPTIONAL
        :type enable_i2c0: ``bool``
        :param enable_i2c1: Flag to enable the rgb parsing on i2c_1 spy module (default is False) - OPTIONAL
        :type enable_i2c1: ``bool``

        :return: led_timestamps and led_values of the backlight I2C and the duration of the capture
        :rtype: ``tuple[list[float], list[list[int]], float]``
        """
        if self._led_frame_parsing_state == self.STATE.NOT_STARTED:
            # Parse I2C frames to led driver frame
            if enable_i2c0:
                self._led_frame_parser.parse_entries(self._i2c_spy_frame_parsers[0])
            # end if
            if enable_i2c1:
                self._led_frame_parser.parse_entries(self._i2c_spy_frame_parsers[1], i2c_id=1)
            # end if
            self._led_frame_parsing_state = self.STATE.COMPLETED
        # end if
        return self._led_frame_parser.i2c_spy0_buffer_timestamp, self._led_frame_parser.i2c_spy0_buffer_values, \
               self._led_frame_parser.capture_duration
    # end def parse_rgb_i2c

    def is_backlight_reaction_sequence_correct(self, sequence, layout_type=KeyboardMixin.LAYOUT.DEFAULT):
        """
        Check backlight reaction sequence.

        :param sequence: List of unique ``KEY_ID`` and its list of action name (make or break) with timestamp
        :type sequence: ``list[KEY_ID, list[tuple(str, float)]]``
        :param layout_type: keyboard international layout type - OPTIONAL
        :type layout_type: ``KeyboardMixin.LAYOUT``

        :return: Flag indicating if the backlight reaction sequence is correct
        :rtype: ``bool``

        :raise ``AssertionError``: multiple source of error:
         - If the KEY_IDs of the sequence are not unique
         - If the list of action name is not sort by timestamp
        """
        status = True
        configuration = GET_BACKLIGHT_CONFIGURATION_BY_ID[self._fw_id][layout_type]
        key_ids = [sequence[i][0] for i in range(len(sequence))]
        assert len(set(key_ids)) == len(key_ids), "sequence must contain unique KEY_IDs"

        if self._led_frame_parsing_state == self.STATE.NOT_STARTED:
            # Parse I2C frames to led driver frame
            self._led_frame_parser.parse_entries(self._i2c_spy_frame_parsers[0])
            self._led_frame_parsing_state = self.STATE.COMPLETED
        # end if

        led_ic_buffer_spy_values = array(self._led_frame_parser.i2c_spy0_buffer_values)
        i2c_spy0_buffer_timestamp = array(self._led_frame_parser.i2c_spy0_buffer_timestamp)

        # Select only the key ids used in the sequence
        reaction_led_buffer_to_check = zeros([len(key_ids), len(i2c_spy0_buffer_timestamp)])
        for index, key_id in enumerate(key_ids):
            led_id = configuration.KEY_ID_TO_LED_ID[key_id]
            reaction_led_buffer_to_check[index, :] = led_ic_buffer_spy_values[:, led_id]
        # end for

        # Create the reference reaction sequence with timing
        reference_sequence = self.reference_reaction_sequence_timing(sequence)

        # Compute the reaction sequence timing from i2c spy record
        record_sequence = self.compute_reaction_sequence_timing_from_record(key_ids, reaction_led_buffer_to_check,
                                                                            i2c_spy0_buffer_timestamp)

        # Compute the timing error between the reference sequence and the record sequence
        timing_error_stats = self.compute_timing_error_between_sequences(reference_sequence, record_sequence)

        if timing_error_stats is None:
            # The 2 sequences have not the same list of action
            status = False
        # end if

        if timing_error_stats["mean_state_on"] > 3 * 32 / 1000:
            status = False
        # end if

        if timing_error_stats["mean_state_off"] > 3 * 32 / 1000:
            status = False
        # end if

        if timing_error_stats["mean_state_ramp_down"] > 200 / 1000:
            status = False
        # end if
        return status
    # end def is_backlight_reaction_sequence_correct

    def reference_reaction_sequence_timing(self, sequence, layout_type=KeyboardMixin.LAYOUT.DEFAULT):
        """
        Create the reference reaction backlight timing sequence from a sequence compose of ``MAKE`` and ``BREAK``

        :param sequence: List of unique ``KEY_ID`` and its list of action name (make or break) with timestamp
        :type sequence: ``list[KEY_ID, list[tuple(str, float)]]``
        :param layout_type: keyboard international layout type - OPTIONAL
        :type layout_type: ``KeyboardMixin.LAYOUT``

        :return: List of unique ``KEY_ID`` and its list of ``ReactionState`` with timestamp
        :rtype: ``list[KEY_ID, list[tuple(ReactionState, float)]]``

        :raise ``AssertionError``: If the KEY_IDs of the sequence are not unique
        """
        configuration = GET_BACKLIGHT_CONFIGURATION_BY_ID[self._fw_id][layout_type]
        key_ids = [sequence[i][0] for i in range(len(sequence))]
        assert len(set(key_ids)) == len(key_ids), "sequence must contain unique KEY_IDs"

        reference_sequence = []
        duration_ramp_down = configuration.REACTION_RAMP_DOWN_KEY_RELEASE_DURATION
        for key_id_sequence in sequence:
            key_id_reference_sequence = [key_id_sequence[0], []]
            action = None
            for action in key_id_sequence[1]:
                if action[0] == BREAK:
                    if len(key_id_reference_sequence[1]) != 0:
                        previous_state = key_id_reference_sequence[1][-1][0]
                        if previous_state == ReactionState.ON:
                            key_id_reference_sequence[1].append((ReactionState.RAMP_DOWN, action[1]))
                        # end if
                    # end if
                elif action[0] == MAKE:
                    if len(key_id_reference_sequence[1]) != 0:
                        previous_timestamp = key_id_reference_sequence[1][-1][1]
                        previous_state = key_id_reference_sequence[1][-1][0]
                        if (action[1] > previous_timestamp + duration_ramp_down) and \
                                (previous_state == ReactionState.RAMP_DOWN):
                            key_id_reference_sequence[1].append((ReactionState.OFF,
                                                                 previous_timestamp + duration_ramp_down))
                            key_id_reference_sequence[1].append((ReactionState.ON, action[1]))
                        elif previous_state != ReactionState.ON:
                            key_id_reference_sequence[1].append((ReactionState.ON, action[1]))
                        # end if
                    else:
                        key_id_reference_sequence[1].append((ReactionState.ON, action[1]))
                    # end if
                # end if
            # end for
            # Add last off state after a break
            if action[0] == BREAK:
                if len(key_id_reference_sequence[1]) != 0:
                    previous_timestamp = key_id_reference_sequence[1][-1][1]
                    key_id_reference_sequence[1].append((ReactionState.OFF, previous_timestamp + duration_ramp_down))
                # end if
            # end if
            reference_sequence.append(key_id_reference_sequence)
        # end for
        return reference_sequence
    # end def reference_reaction_sequence_timing

    def compute_reaction_sequence_timing_from_record(self, key_ids, reaction_led_buffer, reaction_led_timestamp,
                                                     layout_type=KeyboardMixin.LAYOUT.DEFAULT):
        """
        Compute the reaction backlight timing sequence from a record

        :param key_ids: List of unique ``KEY_ID`` and its list of action name (make or break) with timestamp
        :type key_ids: ``list[KEY_ID, list[tuple(str, float)]]``
        :param reaction_led_buffer: List of unique ``KEY_ID`` and its list of action name (make or break) with timestamp
        :type reaction_led_buffer: ``list[KEY_ID, list[tuple(str, float)]]``
        :param reaction_led_timestamp: List of unique ``KEY_ID`` and its list of action name (make or break) with
                                       timestamp
        :type reaction_led_timestamp: ``list[KEY_ID, list[tuple(str, float)]]``
        :param layout_type: keyboard international layout type - OPTIONAL
        :type layout_type: ``KeyboardMixin.LAYOUT``

        :return: List of unique ``KEY_ID`` and its list of ``ReactionState`` with timestamp
        :rtype: ``list[KEY_ID, list[tuple(ReactionState, float)]]``
        """
        record_sequence = [[key_id, []] for key_id in key_ids]
        value_reaction_state_on = reaction_led_buffer.max()
        key_ids_state = [ReactionState.OFF for _ in range(len(key_ids))]
        configuration = GET_BACKLIGHT_CONFIGURATION_BY_ID[self._fw_id][layout_type]

        for index, timestamp in enumerate(reaction_led_timestamp):
            for key_id_index, key_id in enumerate(key_ids):
                if reaction_led_buffer[key_id_index, index] == value_reaction_state_on:
                    state = ReactionState.ON
                elif reaction_led_buffer[key_id_index, index] == configuration.LOW_LEVEL_VALUE or \
                        reaction_led_buffer[key_id_index, index] == 0:
                    state = ReactionState.OFF
                else:
                    # As there is no ramp up on reaction effect, we suppose backlight is on ramp down state, so we don't
                    #  check that the LED intensity decreases
                    state = ReactionState.RAMP_DOWN
                # end if
                if state != key_ids_state[key_id_index]:
                    key_ids_state[key_id_index] = state
                    record_sequence[key_id_index][1].append((state, timestamp))
                # end if
            # end for
        # end for
        return record_sequence
    # end def compute_reaction_sequence_timing_from_record

    def compute_timing_error_between_sequences(self, reference_sequence, record_sequence):
        """
        Compute timing error between the reference sequence and the recorded sequence

        :param reference_sequence: Reference list of unique ``KEY_ID`` and its list of ``ReactionState`` with timestamp
        :type reference_sequence: ``list[KEY_ID, list[tuple(ReactionState, float)]]``
        :param record_sequence: Recorded list of unique ``KEY_ID`` and its list of ``ReactionState`` with timestamp
        :type record_sequence: ``list[KEY_ID, list[tuple(ReactionState, float)]]``

        :return: Dictionary of timing errors with : max_state_on, max_state_off, max_state_ramp_down,
         mean_state_on, mean_state_off, mean_state_ramp_down
        :rtype: ``dict``

        :raise ``AssertionError``: sequence mismatch
        """
        timing_error_stats = {"max_state_on": None, "max_state_off": None, "max_state_ramp_down": None,
                              "mean_state_on": None, "mean_state_off": None, "mean_state_ramp_down": None}
        timing_error_state_on = []
        timing_error_state_off = []
        timing_error_state_ramp_down = []
        # First compare the reaction state sequence of all the keys
        for key_id_ref_sequence, key_id_record_sequence in zip(reference_sequence, record_sequence):
            self.debug_print(key_id_ref_sequence)
            self.debug_print(key_id_record_sequence)
            assert key_id_ref_sequence[0] == key_id_record_sequence[0]
            assert len(key_id_ref_sequence[1]) == len(key_id_record_sequence[1])

            for ref_action, record_action in zip(key_id_ref_sequence[1], key_id_record_sequence[1]):
                assert ref_action[0] == record_action[0]
                timing_error = record_action[1] - ref_action[1]
                if ref_action[0] == ReactionState.ON:
                    timing_error_state_on.append(timing_error)
                elif ref_action[0] == ReactionState.OFF:
                    timing_error_state_off.append(timing_error)
                elif ref_action[0] == ReactionState.RAMP_DOWN:
                    timing_error_state_ramp_down.append(timing_error)
                # end if
            # end for
        # end for
        timing_error_stats["mean_state_on"] = mean(timing_error_state_on)
        timing_error_stats["mean_state_off"] = mean(timing_error_state_off)
        timing_error_stats["mean_state_ramp_down"] = mean(timing_error_state_ramp_down)
        timing_error_stats["max_state_on"] = max(timing_error_state_on, key=abs)
        timing_error_stats["max_state_off"] = max(timing_error_state_off, key=abs)
        timing_error_stats["max_state_ramp_down"] = max(timing_error_state_ramp_down, key=abs)
        return timing_error_stats
    # end def compute_timing_error_between_sequences

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

    def _check_pods_configuration(self):
        """
        Check that the PODS configuration on DAC0 matches the number of I2C spy module.

        :raise ``AssertionError``: If the PODS configuration on DAC0 does not match the number of I2C spy module.
        """
        # Extract DAC0 channels associated to the I2C spy
        i2c_spy_channels_ids = []
        for channel_id, channel in self._kosmos.pods_configuration.dacs[ADDA_SEL_DAC_0].channels.items():
            if channel.associated_device == DeviceName.I2C_SPY:
                i2c_spy_channels_ids.append(channel_id)
            # end if
        # end for
        assert len(i2c_spy_channels_ids) == len(self._kosmos.dt.i2c_spy), (
            f"The number of I2C SPY modules found in Kosmos firmware (i.e. {len(self._kosmos.dt.i2c_spy)}) does not "
            f"match the number of DAC0 channels associated to an I2C spy (i.e. {len(self._kosmos.dt)}) ")
    # end def _check_pods_configuration
# end class KosmosLedSpyOverI2c

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
