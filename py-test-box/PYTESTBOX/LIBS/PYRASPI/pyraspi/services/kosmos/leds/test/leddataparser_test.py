#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.leds.test.leddataparser_test
:brief: Kosmos LEDs data parser test package
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/08/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from re import match
from unittest import skipIf

from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.raspi import UNSUPPORTED_SETUP_ERR_MSG
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator
from pyraspi.services.kosmos.leds.leddataparser import LedDataParser
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_MILLI_SEC
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_SEC
from pyraspi.services.kosmos.leds.leddataparser import _105_PERCENT
from pyraspi.services.kosmos.leds.leddataparser import _95_PERCENT
from pyraspi.services.kosmos.test.keymatrixemulator_test import KBD_FW_ID
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
TWO_MILLI_SEC = 0.002

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


@skipIf(not Daemon.is_host_kosmos(), UNSUPPORTED_SETUP_ERR_MSG)
class LedDataParserTestCase(KosmosCommonTestCase):
    """
    Unitary Test for LED data parser class
    """
    def _play_scenario(self):
        """
        Define the test sequence and  execute it on the DUT.

        :return: The list of downloaded LED entries
        :rtype: ``list[int]``

        :raise ``AssertionError``: LED Status message sanity check failed
        """
        # Keyboard emulator is used to toggle the state of the Keyboard's LEDs
        keymatrix_emulator = KosmosKeyMatrixEmulator(kosmos=self.kosmos, fw_id=KBD_FW_ID)

        # Prepare Test Sequence
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.execute(action=self.kosmos.led_spy.action_event.START)
        # Switch to Host 2 -> LED HOST2 is fast blinking for 4 seconds
        self.host2_fast_blinking_duration = 4
        keymatrix_emulator.keystroke(key_id=KEY_ID.HOST_2,
                                     duration=ButtonStimuliInterface.LONG_PRESS_THRESHOLD + TWO_MILLI_SEC,
                                     delay=None)
        self.kosmos.pes.delay(delay_s=self.host2_fast_blinking_duration)
        # Reconnect to Host 1 -> LED HOST2 is steady for 5 seconds
        keymatrix_emulator.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=10)
        self.kosmos.pes.delay(delay_s=2, action=self.kosmos.led_spy.action_event.RESET)
        self.kosmos.sequencer.offline_mode = False

        # Configure LED module
        # enable channel 1
        self.channels = [0, 1, 2]
        self.clock_gating = 0
        channel_enable = 0
        for channel in self.channels:
            channel_enable += (1 << channel)
        # end for
        self.kosmos.led_spy.set_channel_enable(channel_enable=channel_enable)
        self.kosmos.led_spy.set_gate_latch(gate_latch=self.clock_gating)

        # Upload and execute test sequence
        self.kosmos.sequencer.play_sequence()

        # Get the number of LED entries to download
        led_status = self.kosmos.led_spy.status()

        # Sanity check
        self.assertEqual(led_status.fifo_count, 0, msg="The LED FIFO should be empty at this moment.")
        self.assertGreater(led_status.buffer_count, 0, msg="The LED buffer should not be empty at this moment.")

        # Request download of LED entries
        leds = self.kosmos.led_spy.download(count=led_status.buffer_count)

        # Validate reply
        self.assertEqual(len(leds), led_status.buffer_count, msg=(leds, led_status))

        return leds
    # end def _play_scenario

    def test_timeline_str(self):
        """
        Validate the parsing of the raw LED data entries and its string representation.

        :raise ``AssertionError``: TimeLine does not contain channel
        """
        leds = self._play_scenario()

        leddataparser = LedDataParser(self.channels, self.clock_gating)
        timeline = leddataparser.parse_entries(leds)
        value = str(timeline)

        assert match(r'TimeLine with \d channels', value)
    # end def test_timeline_str

    def test_get_next_scheme(self):
        """
        Validate the get_next_scheme method of an ``TimeLine`` instance.

        :raise ``AssertionError``: Scheme error
        """
        leds = self._play_scenario()

        leddataparser = LedDataParser(self.channels, self.clock_gating)
        timeline = leddataparser.parse_entries(leds)

        # Check HOST.CH2 (i.e. channel_1)  first scheme is Off
        channel_1 = timeline.get_channel(HOST.CH2 - 1)
        ch1_scheme_0 = channel_1.get_next_scheme()
        assert ch1_scheme_0.type == SchemeType.OFF
        assert ch1_scheme_0.start_time == 0, f'Wrong scheme start timing: {ch1_scheme_0.start_time} != 0'
        assert ch1_scheme_0.effect_duration > ButtonStimuliInterface.LONG_PRESS_THRESHOLD * 1000, \
            f'Scheme duration does not comply with requirement: {ch1_scheme_0.effect_duration} < ' \
            f'{ButtonStimuliInterface.LONG_PRESS_THRESHOLD * 1000}'

        # Check HOST.CH2 next scheme is Fast blinking
        ch1_scheme_1 = channel_1.get_next_scheme()
        assert ch1_scheme_1.type == SchemeType.FAST_BLINKING
        assert ch1_scheme_1.start_time == ch1_scheme_0.end_time, \
            f'Wrong scheme start timing: {ch1_scheme_1.start_time} != {ch1_scheme_0.end_time}'
        assert (self.host2_fast_blinking_duration * _95_PERCENT) * TICKS_PER_SEC < ch1_scheme_1.effect_duration < (
                self.host2_fast_blinking_duration * _105_PERCENT) * TICKS_PER_SEC, \
            f'Scheme duration does not comply with requirement: ' \
            f'{(self.host2_fast_blinking_duration * _95_PERCENT) * TICKS_PER_SEC} < {ch1_scheme_1.effect_duration} < ' \
            f'{(self.host2_fast_blinking_duration * _105_PERCENT) * TICKS_PER_SEC}'

        # Check HOST.CH1 (i.e. channel_0) first scheme is Off
        channel_0 = timeline.get_channel(HOST.CH1 - 1)
        ch0_scheme_0 = channel_0.get_next_scheme()
        assert ch0_scheme_0.type == SchemeType.OFF
        assert ch0_scheme_0.start_time == 0, f'Wrong scheme start timing: {ch0_scheme_0.start_time} != 0'
        assert ch0_scheme_0.effect_duration > (ButtonStimuliInterface.LONG_PRESS_THRESHOLD +
                                               self.host2_fast_blinking_duration) * TICKS_PER_SEC, \
            f'Scheme duration does not comply with requirement: {ch0_scheme_0.effect_duration} < ' \
            f'{(ButtonStimuliInterface.LONG_PRESS_THRESHOLD + self.host2_fast_blinking_duration) * TICKS_PER_SEC}'

        # Check HOST.CH1 (i.e. channel_0) next scheme is Steady
        ch0_scheme_1 = channel_0.get_next_scheme()
        assert ch0_scheme_1.type == SchemeType.STEADY
        assert ch0_scheme_1.start_time == ch0_scheme_0.end_time, \
            f'Wrong scheme start timing: {ch0_scheme_1.start_time} != {ch0_scheme_0.end_time}'
        assert ch0_scheme_1.effect_duration <= 125 * TICKS_PER_MILLI_SEC, \
            f'Scheme duration does not comply with requirement: {ch0_scheme_1.effect_duration} > 125 ms'

        # Check HOST.CH1 (i.e. channel_0) next scheme is Off
        ch0_scheme_2 = channel_0.get_next_scheme()
        assert ch0_scheme_2.type == SchemeType.OFF
        assert ch0_scheme_2.start_time == ch0_scheme_1.end_time, \
            f'Wrong scheme start timing: {ch0_scheme_2.start_time} != {ch0_scheme_1.end_time}'
        assert ch0_scheme_2.effect_duration <= 30 * 10 ** 2, \
            f'Scheme duration does not comply with requirement: {ch0_scheme_2.effect_duration} > 30 us'

        # Check HOST.CH1 (i.e. channel_0) next scheme is Steady
        host1_steady_duration = 5
        ch0_scheme_3 = channel_0.get_next_scheme()
        assert ch0_scheme_3.type == SchemeType.STEADY
        assert ch0_scheme_3.start_time == ch0_scheme_2.end_time, \
            f'Wrong scheme start timing: {ch0_scheme_3.start_time} != {ch0_scheme_2.end_time}'
        assert (host1_steady_duration * _95_PERCENT) * TICKS_PER_SEC < ch0_scheme_3.effect_duration < (
                host1_steady_duration * _105_PERCENT) * TICKS_PER_SEC, \
            f'Scheme duration does not comply with requirement: ' \
            f'{(host1_steady_duration * _95_PERCENT) * TICKS_PER_SEC} < {ch0_scheme_3.effect_duration} < ' \
            f'{(host1_steady_duration * _105_PERCENT) * TICKS_PER_SEC}'

        # Check HOST.CH1 (i.e. channel_0) next scheme is Off
        host1_off_duration_in_sec = 2
        ch0_scheme_4 = channel_0.get_next_scheme()
        assert ch0_scheme_4.type == SchemeType.OFF
        assert ch0_scheme_4.start_time == ch0_scheme_3.end_time, \
            f'Wrong scheme start timing: {ch0_scheme_4.start_time} != {ch0_scheme_3.end_time}'
        assert ch0_scheme_4.effect_duration > host1_off_duration_in_sec * TICKS_PER_SEC, \
            f'Scheme duration does not comply with requirement: {ch0_scheme_4.effect_duration} > ' \
            f'{host1_off_duration_in_sec * TICKS_PER_SEC}s'
    # end def test_get_next_scheme

    def test_get_next_transition(self):
        """
        Validate the get_next_transition method of an ``TimeLine`` instance.

        :raise ``AssertionError``: Transition error
        """
        leds = self._play_scenario()

        leddataparser = LedDataParser(self.channels, self.clock_gating)
        timeline = leddataparser.parse_entries(leds)

        # Check first transition is on HOST.CH2 from Off to Fast Blinking
        transition_0 = timeline.get_next_transition()
        assert transition_0.channel_id == HOST.CH2 - 1
        assert transition_0.source == SchemeType.OFF, f'Wrong transition scheme source: {transition_0.source} != ' \
                                                      f'{SchemeType.OFF}'
        assert transition_0.destination == SchemeType.FAST_BLINKING, \
            f'Wrong transition scheme destination: {transition_0.destination} != {SchemeType.FAST_BLINKING}'
        assert transition_0.timing > ButtonStimuliInterface.LONG_PRESS_THRESHOLD * TICKS_PER_SEC, \
            f'Transition does not occur at the expected moment: {transition_0.timing} < ' \
            f'{ButtonStimuliInterface.LONG_PRESS_THRESHOLD * TICKS_PER_SEC}'
        assert transition_0.timing < ButtonStimuliInterface.LONG_PRESS_DURATION * TICKS_PER_SEC, \
            f'Transition does not occur at the expected moment: {transition_0.timing} > ' \
            f'{ButtonStimuliInterface.LONG_PRESS_DURATION * TICKS_PER_SEC}'

        # Check second transition is on HOST.CH2 from Fast Blinking to Off
        transition_1 = timeline.get_next_transition()
        assert transition_1.channel_id == HOST.CH2 - 1
        assert transition_1.source == SchemeType.FAST_BLINKING, \
            f'Wrong transition scheme source: {transition_1.source} != {SchemeType.FAST_BLINKING}'
        assert transition_1.destination == SchemeType.OFF, \
            f'Wrong transition scheme destination: {transition_1.destination} != {SchemeType.OFF}'
        assert transition_1.timing > 5 * TICKS_PER_SEC, \
            f'Transition does not occur at the expected moment: {transition_1.timing} < 5000 ms'

        # Check third transition is on HOST.CH1 from Off to Slow blinking but detected as Steady as it does not last
        # long enough (~120ms)
        transition_2 = timeline.get_next_transition()
        assert transition_2.channel_id == HOST.CH1 - 1
        assert transition_2.source == SchemeType.OFF, \
            f'Wrong transition scheme source: {transition_2.source} != {SchemeType.OFF}'
        assert transition_2.destination == SchemeType.STEADY, \
            f'Wrong transition scheme destination: {transition_2.destination} != {SchemeType.STEADY}'
        assert transition_2.timing <= transition_1.timing + 60 * TICKS_PER_MILLI_SEC, \
            f'Transition does not occur at the expected moment: {transition_2.timing} > {transition_1.timing} + 60 ms'

        # Check forth transition is on HOST.CH1 from Steady to Off
        transition_3 = timeline.get_next_transition()
        assert transition_3.channel_id == HOST.CH1 - 1
        assert transition_3.source == SchemeType.STEADY, \
            f'Wrong transition scheme source: {transition_3.source} != {SchemeType.STEADY}'
        assert transition_3.destination == SchemeType.OFF, \
            f'Wrong transition scheme destination: {transition_3.destination} != {SchemeType.OFF}'
        assert transition_3.timing <= (transition_2.timing + 125 * TICKS_PER_MILLI_SEC), \
            f'Transition does not occur at the expected moment: {transition_3.timing} > {transition_2.timing} + 125 ms'

        # Check fifth transition is on HOST.CH1 from Off to Steady
        transition_4 = timeline.get_next_transition()
        assert transition_4.channel_id == HOST.CH1 - 1
        assert transition_4.source == SchemeType.OFF, \
            f'Wrong transition scheme source: {transition_3.source} != {SchemeType.OFF}'
        assert transition_4.destination == SchemeType.STEADY, \
            f'Wrong transition scheme destination: {transition_3.destination} != {SchemeType.STEADY}'
        assert transition_4.timing <= transition_3.timing + 50 * TICKS_PER_MILLI_SEC, \
            f'Transition does not occur at the expected moment: {transition_3.timing} > 50 ms'

        # Check sixth transition is on HOST.CH1 from Steady to Off
        host1_steady_duration = 5
        transition_5 = timeline.get_next_transition()
        assert transition_5.channel_id == HOST.CH1 - 1
        assert transition_5.source == SchemeType.STEADY, \
            f'Wrong transition scheme source: {transition_3.source} != {SchemeType.STEADY}'
        assert transition_5.destination == SchemeType.OFF, \
            f'Wrong transition scheme destination: {transition_3.destination} != {SchemeType.OFF}'
        assert (transition_4.timing + (host1_steady_duration * _95_PERCENT) * TICKS_PER_SEC) < transition_5.timing < (
                transition_4.timing + (host1_steady_duration * _105_PERCENT) * TICKS_PER_SEC), \
            f'Transition does not occur at the expected moment: ' \
            f'{transition_4.timing + (host1_steady_duration * _95_PERCENT) * TICKS_PER_SEC} < {transition_5.timing} ' \
            f'< {transition_4.timing + (host1_steady_duration * _105_PERCENT) * TICKS_PER_SEC}'
    # end def test_get_next_transition
# end class LedDataParserTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
