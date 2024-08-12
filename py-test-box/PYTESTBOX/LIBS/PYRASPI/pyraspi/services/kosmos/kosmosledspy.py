#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.kosmosledspy
:brief: Kosmos LED Spy Control Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/02/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique

from pylibrary.emulator.emulatorinterfaces import LedSpyInterface
from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.config.ledlayout import GET_LED_LAYOUT_BY_ID
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.kosmosio import KOSMOS_LEDS_TO_CHANNELS_DAC2_MAP
from pyraspi.services.kosmos.leds.leddataparser import LedDataParser
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_SEC
from pyraspi.services.kosmos.protocol.generated.messages import adda_dac_channels_e__enumvalues


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosLedSpy(LedSpyInterface):
    """
    Interface for KOSMOS LEDs monitoring module.
    """
    # We accept 7% tolerance around the expected value
    TOLERANCE = 0.07
    LOWER_BOUNDARY = 1 - TOLERANCE
    UPPER_BOUNDARY = 1 + TOLERANCE

    @unique
    class STATE(IntEnum):
        """
        LED data parsing state
        """
        NOT_STARTED = auto()
        IN_PROGRESS = auto()
        COMPLETED = auto()
    # end class STATE

    def __init__(self, kosmos, fw_id):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``

        :raise ``AssertionError``: If the firmware identifier is not in its valid range
        """
        assert Daemon.is_host_kosmos(), 'This class supports only Kosmos hardware'

        self._kosmos = kosmos
        assert fw_id in GET_LED_LAYOUT_BY_ID, f"Kosmos LED Spy doesn't support the fw_id : {fw_id}"
        self._led_layout = GET_LED_LAYOUT_BY_ID[fw_id]
        self._led_identifiers = None
        self._data_parsing_state = self.STATE.NOT_STARTED
        self._next_transition_time = None
        self._timeline = None
        self._leddataparser = None
        self._leds = None
        self.clock_gating = 0

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
        return self._led_layout.LEDS[led_id]
    # end def get_channel_id

    def start(self, led_identifiers):
        # See ``LedSpyInterface.start``
        assert set(led_identifiers).issubset(self._led_layout.LEDS), \
            f"Led Spy module doesn't support one of the led ids : {led_identifiers}"

        self._led_identifiers = led_identifiers
        # Configure LED module: enable required channels
        channel_enable = 0
        for index in self._led_identifiers:
            channel_enable += (1 << self._led_layout.LEDS[index])
        # end for
        self._kosmos.dt.led_spy[0].set_channel_enable(channel_enable=channel_enable)
        self._kosmos.dt.led_spy[0].set_gate_latch(gate_latch=self.clock_gating)

        self._kosmos._enable_led_monitoring = True
        self._kosmos.pes.execute(action=self._kosmos.dt.led_spy[0].action_event.RESET)
        self._kosmos.pes.execute(action=self._kosmos.dt.led_spy[0].action_event.START)
        # Upload and execute test sequence
        self._kosmos.sequencer.play_sequence()

        # reset the local variable
        self._leds = []

        channels = [self._led_layout.LEDS[x] for x in self._led_identifiers]
        self._leddataparser = LedDataParser(channels, clock_gating=self.clock_gating,
                                            is_active_high=self._led_layout.LED_ACTIVE_HIGH)
    # end def start

    def stop(self, led_identifiers):
        # See ``LedSpyInterface.stop``
        assert set(led_identifiers).issubset(self._led_layout.LEDS), \
            f"Led Spy module doesn't support one of the led ids : {led_identifiers}"

        if hasattr(self._kosmos, '_enable_led_monitoring') and self._kosmos._enable_led_monitoring:
            # Compute maximum timing in seconds needed to generate a set of data on all channels
            delay = 0xFFFFFF / TICKS_PER_SEC * (1 + self.clock_gating)
            delay += max(len(self._led_identifiers), 5) / TICKS_PER_SEC
            self._kosmos.sequencer.offline_mode = True
            self._kosmos.pes.delay(delay_s=delay, action=self._kosmos.dt.led_spy[0].action_event.STOP)
            # Flush LED fifo into SW buffer
            self._kosmos.dt.led_spy[0].flush_fifo_to_buffer()
            self._kosmos.sequencer.offline_mode = False
            # Upload and execute test sequence
            self._kosmos.sequencer.play_sequence()
            # Reset the parsing status
            self._data_parsing_state = self.STATE.NOT_STARTED
        # end if

        self._kosmos._enable_led_monitoring = False
    # end def stop

    def get_timeline(self):
        # See ``LedSpyInterface.get_timeline``
        if self._led_identifiers is None:
            return
        # end if
        self._data_parsing_state = self.STATE.IN_PROGRESS

        # Request download of LED entries
        leds = self._kosmos.dt.led_spy[0].download()

        # Aggregate all the raw data
        self._leds += leds
        # Reset LED parser variables
        self._leddataparser.reset()
        # Parse the received LED entry list
        self._timeline = self._leddataparser.parse_entries(self._leds)
        # Update processing status
        self._data_parsing_state = self.STATE.COMPLETED

        return self._timeline
    # end def get_timeline

    def flush_led_data(self):
        # See ``LedSpyInterface.flush_led_data``
        # Flush LED fifo into SW buffer
        self._kosmos.sequencer.offline_mode = True
        self._kosmos.dt.led_spy[0].flush_fifo_to_buffer()
        self._kosmos.sequencer.offline_mode = False
        # Upload and execute test sequence
        self._kosmos.sequencer.play_sequence()
    # end def flush_led_data

    def get_led_identifiers(self):
        # See ``LedSpyInterface.get_led_identifiers``
        return self._led_identifiers
    # end def get_led_identifiers

    def parse_backlight_pwm(self):
        """
        Post process the data received through the Stream Channel of the backlight led

        :return: led_timestamps and led_values of the backlight pwm
        :rtype: ``tuple[list[float], list[list[int]]]`` or ``None``
        """
        if self._led_identifiers is None:
            return
        # end if
        self._data_parsing_state = self.STATE.IN_PROGRESS

        # Request download of LED entries
        leds = self._kosmos.dt.led_spy[0].download()

        # Aggregate all the raw data
        self._leds += leds
        # Reset LED parser variables
        self._leddataparser.reset()
        # Parse the received LED entry list
        timestamp, led_values = self._leddataparser.parse_backlight_led_pwm(self._leds,
                                                                            self._led_layout.LEDS[LED_ID.BACKLIGHT_LED])
        # Update processing status
        self._data_parsing_state = self.STATE.COMPLETED
        return timestamp, led_values
    # end def parse_backlight_pwm

    def _check_pods_configuration(self):
        """
        Check that the PODS configuration (thresholds voltage set by DAC2) matches the LED layout.

        :raise ``AssertionError``: If one of the DAC2 voltages associated with a LED is equal to 0 (i.e. not configured)
        """
        for kosmos_led_id in self._led_layout.LEDS.values():
            dac_channel = KOSMOS_LEDS_TO_CHANNELS_DAC2_MAP[kosmos_led_id]
            voltage = self._kosmos.pods_configuration.dac_2.channels[dac_channel].voltage
            assert voltage != 0.0, (f"Kosmos LED ID n°{kosmos_led_id} is used but DAC2 channel "
                                    f"{adda_dac_channels_e__enumvalues[dac_channel]} voltage is not configured "
                                    "in pods configuration")
        # end for
    # end def _check_pods_configuration
# end class KosmosLedSpy

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
