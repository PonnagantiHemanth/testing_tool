#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.kosmosledspy_test
:brief: Tests for Kosmos Led Spy class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/07/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep
from unittest import SkipTest

from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator
from pyraspi.services.kosmos.leds.leddataparser import LedDataParser
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_MILLI_SEC
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_SEC
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.ledspy import LedSpyModule
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_STATE_RESET_OR_STOP
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_STATE_STARTED
from pyraspi.services.kosmos.test.keymatrixemulator_test import KBD_FW_ID
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
TWO_MILLI_SEC = 0.002
# The device stays in discoverable mode for 3 minutes
DEVICE_DISCOVERY_TIMEOUT = 180
# Tolerance around this timeout is fixed to 200ms
DEVICE_DISCOVERY_TOLERANCE = 200 * TICKS_PER_MILLI_SEC


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@require_kosmos_device(DeviceName.LED_SPY)
@require_kosmos_device(DeviceName.KBD_MATRIX)
class KosmosLedSpyTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos Led Spy class
    """
    # Reference to the module under test
    module: LedSpyModule

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos

        :raise ``SkipTest``: if LED SPY module is not present in the Device Tree
        """
        super().setUpClass()

        if not cls.kosmos.led_spy:
            raise SkipTest('Module is not present in the Device Tree')
        # end if

        # Keyboard emulator is used to toggle the state of the Keyboard's LEDs
        cls.kosmos_kbd = KosmosKeyMatrixEmulator(kosmos=cls.kosmos, fw_id=KBD_FW_ID)
    # end def setUpClass

    def setUp(self):
        """
        Reset Kosmos LED module buffers before each tests
        """
        super().setUp()

        # Reset LED module
        self.kosmos.led_spy.reset_module()
    # end def setUp

    def tearDown(self):
        """
        Reset Kosmos LED module buffers after each tests
        """
        super().tearDown()


        #TODO: Detect test failure and perform DUT reset
        #      LED SPY Test cases may fail in cascade.
        #      For example, a LED blinking sequence started in a test that failed and returned before the blinking
        #      sequence what finished, may interfere with the next test case.


        led_status = self.kosmos.led_spy.status()
        self.assertEqual(led_status.fifo_count, 0,
                         f'LED module FIFO should be empty at the end of the test case.\n'
                         f'fifo_count = {led_status.fifo_count}')
        self.assertEqual(led_status.buffer_count, 0,
                         f'LED module buffer should be empty at the end of the test case.\n'
                         f'buffer_count = {led_status.fifo_count}')
    # end def tearDown

    def test_change_host_pattern(self):
        """
        Validate "Change HOST" blinking pattern.

        #TODO: make use of KosmosLedSpy Class, instead of calling methods directly from Kosmos
        """
        # Prepare Test Sequence
        long_delay = 15  # seconds
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.pes.delay(delay_s=1)
        for host in HOST.ALL:
            self.kosmos_kbd.enter_pairing_mode(host_index=host, delay=None)
        # end for
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=long_delay, action=self.module.action_event.STOP)
        self.kosmos.led_spy.flush_fifo_to_buffer()
        self.kosmos.sequencer.offline_mode = False

        # Configure LED module
        # Enable the monitoring of the 3 connectivity LEDs connected on channels 0, 1 & 2
        channels = [0, 1, 2]
        channel_enable = sum([(1 << ch) for ch in channels])
        self.kosmos.led_spy.set_channel_enable(channel_enable=channel_enable)
        self.kosmos.led_spy.set_gate_latch(gate_latch=0)

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

        leddataparser = LedDataParser(channels)
        timeline = leddataparser.parse_entries(leds)

        # Validate LED behavior when calling 'enter_pairing_mode' method
        for channel_id in channels:
            channel = timeline.get_channel(channel_id)

            scheme = channel.get_next_scheme()
            self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
            self.assertEqual(scheme.type, SchemeType.OFF, msg=channel_id)

            scheme = channel.get_next_scheme()
            self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
            self.assertEqual(scheme.type, SchemeType.FAST_BLINKING, msg=channel_id)

            scheme = channel.get_next_scheme()
            self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
            self.assertEqual(scheme.type, SchemeType.OFF, msg=channel_id)
        # end for

        # Validate LED behavior when calling 'change_host' method and the channel is paired
        channel = timeline.get_channel(0)

        # Check the connectivity LED on HOST 1 is switching to Steady
        scheme = channel.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.STEADY)

        # FIXME - start
        # The firmware of the Foster keyboard presents a 15us glitch at this moment.
        # This workaround makes the test passes with success.
        # This must be removed once the bug is fixed in firmware.
        scheme = channel.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.OFF)
        scheme = channel.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.STEADY)
        # FIXME - end

        # Check the connectivity LED on HOST 1 is switching back to Off
        scheme = channel.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.OFF)

        # Check this is the end of measurements
        for channel_id in channels:
            channel = timeline.get_channel(channel_id)
            scheme = channel.get_next_scheme()
            self.assertIsNone(scheme, msg=channel_id)
        # end for
    # end def test_change_host_pattern

    def test_fast_blinking_channel_2(self):
        """
        Validate the fast blinking LED effect on channel 2.

        #TODO: make use of KosmosLedSpy Class, instead of calling methods directly from Kosmos
        """
        # Prepare Test Sequence
        host2_keystroke_duration = ButtonStimuliInterface.LONG_PRESS_THRESHOLD + TWO_MILLI_SEC
        host2_fast_blinking_test_duration = DEVICE_DISCOVERY_TIMEOUT + 5
        host1_change_duration = 6  # 5 seconds for paired HOST key LED + 1 s margin
        timeout = host2_keystroke_duration + host2_fast_blinking_test_duration + host1_change_duration + 1  # +1 s margin
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.execute(action=self.kosmos.led_spy.action_event.START)
        self.kosmos_kbd.keystroke(key_id=KEY_ID.HOST_2, duration=host2_keystroke_duration, delay=None)
        self.kosmos.pes.delay(delay_s=host2_fast_blinking_test_duration)
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration, action=self.kosmos.led_spy.action_event.STOP)
        self.kosmos.led_spy.flush_fifo_to_buffer()
        self.kosmos.sequencer.offline_mode = False

        # Configure LED module
        # enable channel 1
        channels = [1]
        channel_enable = sum([(1 << ch) for ch in channels])
        self.kosmos.led_spy.set_channel_enable(channel_enable=channel_enable)
        self.kosmos.led_spy.set_gate_latch(gate_latch=0)

        # Upload and execute test sequence
        self.kosmos.sequencer.play_sequence(timeout=timeout)

        # Validate remote buffer count
        led_status = self.kosmos.led_spy.status()
        self.assertGreater(led_status.buffer_count, 0)
        self.assertEqual(led_status.fifo_count, 0)

        # Request download of LED entries
        leds = self.kosmos.led_spy.download(count=led_status.buffer_count)

        leddataparser = LedDataParser(channels)
        timeline = leddataparser.parse_entries(leds)

        channel = timeline.get_channel(1)
        scheme_0 = channel.get_next_scheme()
        self.assertIsNotNone(scheme_0)
        self.assertEqual(SchemeType.OFF, scheme_0.type)
        self.assertEqual(0, scheme_0.start_time)
        self.assertGreater(scheme_0.effect_duration, ButtonStimuliInterface.LONG_PRESS_THRESHOLD * 1000)

        scheme_1 = channel.get_next_scheme()
        self.assertIsNotNone(scheme_1)
        self.assertEqual(SchemeType.FAST_BLINKING, scheme_1.type)
        self.assertEqual(scheme_0.end_time, scheme_1.start_time)
        self.assertGreater(scheme_1.effect_duration, ButtonStimuliInterface.LONG_PRESS_THRESHOLD * 1000)
        self.assertLess(DEVICE_DISCOVERY_TIMEOUT * TICKS_PER_SEC - DEVICE_DISCOVERY_TOLERANCE, scheme_1.effect_duration)
        self.assertGreater(DEVICE_DISCOVERY_TIMEOUT * TICKS_PER_SEC + DEVICE_DISCOVERY_TOLERANCE, scheme_1.effect_duration)
    # end def test_fast_blinking_channel_2

    def test_remote_fifo_and_buffer_persistence_across_test_scenarios(self):
        """
        Test the persistence of the LED FIFO (in FPGA) and LED buffer (in the Microblaze RAM),
        across consecutive Test Scenarios.
        """
        # Configure LED module
        channels = [0]   # enable channel 0 for HOST 1 key
        channel_enable = sum([(1 << ch) for ch in channels])
        self.kosmos.led_spy.set_channel_enable(channel_enable=channel_enable)
        self.kosmos.led_spy.set_gate_latch(gate_latch=0)

        # PART 1/3 : Prepare Test Sequence
        host1_change_duration = 7  # 5 seconds for paired HOST key LED + 2 s margin
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.execute(action=self.kosmos.led_spy.action_event.START)
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration)
        self.kosmos.sequencer.offline_mode = False

        # Upload and execute test sequence
        self.kosmos.sequencer.play_sequence()

        # Validate remote buffer count
        led_status_1 = self.kosmos.led_spy.status()
        led_count_1 = led_status_1.buffer_count + led_status_1.fifo_count
        self.assertGreater(led_count_1, 0, msg=led_status_1)
        self.assertEqual(led_status_1.state, LED_SPY_STATE_STARTED, msg=led_status_1)

        # PART 2/3 : Prepare & Execute simple Test Sequence
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)

        # Wait for the HOST key LED to turn off
        sleep(host1_change_duration)

        # Get the number of LED entries to download
        led_status_2 = self.kosmos.led_spy.status()
        led_count_2 = led_status_2.buffer_count + led_status_2.fifo_count
        self.assertGreater(led_count_2, led_count_1, msg=led_status_2)

        # PART 3/3 : Prepare Test Sequence
        self.kosmos.sequencer.offline_mode = True
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration, action=self.kosmos.led_spy.action_event.STOP)
        self.kosmos.led_spy.flush_fifo_to_buffer()
        self.kosmos.sequencer.offline_mode = False

        # Upload and execute test sequence
        self.kosmos.sequencer.play_sequence()

        # Get the number of LED entries to download
        led_status_3 = self.kosmos.led_spy.status()
        self.assertEqual(led_status_3.fifo_count, 0, msg=led_status_3)
        self.assertGreater(led_status_3.buffer_count, led_count_2, msg=led_status_3)
        self.assertEqual(led_status_3.state, LED_SPY_STATE_RESET_OR_STOP, msg=led_status_3)

        # Request download of LED entries
        leds = self.kosmos.led_spy.download(count=led_status_3.buffer_count)

        # Parse LED measurements
        leddataparser = LedDataParser(channels)
        timeline = leddataparser.parse_entries(leds)

        # Validate that the LED of HOST 1 key was lit three times for 5 seconds
        channel_0 = timeline.get_channel(channels[0])
        for host_led_cycle_id in range(3):
            # Validate state from OFF to STEADY
            scheme = channel_0.get_next_scheme()
            self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
            self.assertEqual(scheme.type, SchemeType.OFF)

            # Validate state from STEADY to OFF
            scheme = channel_0.get_next_scheme()
            self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
            self.assertEqual(scheme.type, SchemeType.STEADY)
            self.assertAlmostEqual(scheme.effect_duration, 5 * TICKS_PER_SEC, delta=50 * TICKS_PER_MILLI_SEC)
        # end for

        # Validate final state from OFF to STEADY
        scheme = channel_0.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.OFF)

        # Validate this is the end of measurements
        self.assertIsNone(channel_0.get_next_scheme())
    # end def test_remote_fifo_and_buffer_persistence_across_test_scenarios

    def test_led_events_start_stop(self):
        """
        Validate the FPGA LED module integration with PES event.

        Test case: Validate that only two LED HOST1 blinking cycles are recorded instead of three,
        using a combination of PES START/STOP events to pause the LED recording of during the second HOST1 LED cycle.
        """
        # Configure LED module
        channels = [0]   # enable channel 0 for HOST 1 key
        channel_enable = sum([(1 << ch) for ch in channels])
        self.kosmos.led_spy.set_channel_enable(channel_enable=channel_enable)
        self.kosmos.led_spy.set_gate_latch(gate_latch=0)

        # Prepare Test Sequence
        host1_change_duration = 7  # 5 seconds for paired HOST key LED + 2 s margin
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.execute(action=self.kosmos.led_spy.action_event.START)
        self.kosmos.pes.delay(delay_s=1)
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration, action=self.kosmos.led_spy.action_event.STOP)
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration, action=self.kosmos.led_spy.action_event.START)
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration, action=self.kosmos.led_spy.action_event.STOP)
        self.kosmos.led_spy.flush_fifo_to_buffer()
        self.kosmos.sequencer.offline_mode = False

        # Upload and execute test sequence
        self.kosmos.sequencer.play_sequence()

        # Validate remote buffer count
        led_status = self.kosmos.led_spy.status()
        self.assertGreater(led_status.buffer_count, 0)
        self.assertEqual(led_status.fifo_count, 0)

        # Request download of LED entries
        leds = self.kosmos.led_spy.download(count=led_status.buffer_count)

        # Parse LED measurements
        leddataparser = LedDataParser(channels)
        timeline = leddataparser.parse_entries(leds)

        # Validate that only two pairing cycles were recorded instead of three
        channel_0 = timeline.get_channel(channels[0])
        for host_led_cycle_id in range(2):
            # Validate state from OFF to STEADY
            scheme = channel_0.get_next_scheme()
            self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
            self.assertEqual(scheme.type, SchemeType.OFF)

            # Validate state from STEADY to OFF
            scheme = channel_0.get_next_scheme()
            self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
            self.assertEqual(scheme.type, SchemeType.STEADY)
            self.assertAlmostEqual(scheme.effect_duration, 5 * TICKS_PER_SEC, delta=50 * TICKS_PER_MILLI_SEC)
        # end for

        # Validate final state from OFF to STEADY
        scheme = channel_0.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.OFF)

        # Validate this is the end of measurements
        self.assertIsNone(channel_0.get_next_scheme())
    # end def test_led_events_start_stop

    def test_led_events_reset(self):
        """
        Validate the FPGA LED module integration with PES event.

        Test case: Validate that only one LED HOST1 blinking cycle is recorded instead of two,
        using a PES RESET event to reset the LED controller to a halt, before the second HOST1 LED cycle.
        """
        # Configure LED module
        channels = range(32)  # enable all channels to generate more data
        channel_enable = sum([(1 << ch) for ch in channels])
        self.kosmos.led_spy.set_channel_enable(channel_enable=channel_enable)
        self.kosmos.led_spy.set_gate_latch(gate_latch=0)

        # Prepare Test Sequence
        host1_change_duration = 7  # 5 seconds for paired HOST key LED + 2 s margin
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.execute(action=self.kosmos.led_spy.action_event.START)
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration, action=self.kosmos.led_spy.action_event.RESET)
        self.kosmos_kbd.change_host(host_index=HOST.CH1, delay=None)
        self.kosmos.pes.delay(delay_s=host1_change_duration, action=self.kosmos.led_spy.action_event.STOP)
        self.kosmos.sequencer.offline_mode = False

        # Upload and execute test sequence
        self.kosmos.sequencer.play_sequence()

        # Validate remote buffer count
        led_status = self.kosmos.led_spy.status()
        self.assertGreater(led_status.buffer_count, 0)
        self.assertEqual(led_status.fifo_count, 0)

        # Request download of LED entries
        leds = self.kosmos.led_spy.download(count=led_status.buffer_count)

        # Parse LED measurements
        leddataparser = LedDataParser(list(channels))
        timeline = leddataparser.parse_entries(leds)

        # Validate final state from OFF to STEADY
        channel_0 = timeline.get_channel(channels[0])
        scheme = channel_0.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.OFF)

        # Validate state from STEADY to OFF
        scheme = channel_0.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.STEADY)
        self.assertAlmostEqual(scheme.effect_duration, 5 * TICKS_PER_SEC, delta=50 * TICKS_PER_MILLI_SEC)
        # end for

        # Validate final state from OFF to STEADY
        scheme = channel_0.get_next_scheme()
        self.assertIsNotNone(scheme, msg='Cannot fetch next LED Scheme.')
        self.assertEqual(scheme.type, SchemeType.OFF)

        # Validate this is the end of measurements
        self.assertIsNone(channel_0.get_next_scheme())
    # end def test_led_events_reset
# end class KosmosLedSpyTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
