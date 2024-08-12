#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.ledspy_test
:brief: Tests for Kosmos LED SPY class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/07/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from random import getrandbits
from time import sleep
from unittest import SkipTest

from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator
from pyraspi.services.kosmos.leds.leddataparser import LedDataParser
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.ledspy import LedSpyModule
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_FIFO_DEFAULT_THRESHOLD
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_STATE_RESET_OR_STOP
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_STATE_STARTED
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RUNNING
from pyraspi.services.kosmos.test.keymatrixemulator_test import KBD_FW_ID


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@require_kosmos_device(DeviceName.LED_SPY)
class KosmosLedSpyTestCase(AbstractTestClass.DownloadModuleInterfaceTestCase):
    """
    Unitary Test for Kosmos LED SPY class
    """
    VERBOSE = False

    module: LedSpyModule

    @classmethod
    def setUpClass(cls):
        """
        Instantiate ``LedSpyModule``.
        """
        super().setUpClass()

        # Keyboard emulator is used to toggle the state of the Keyboard's LEDs
        cls._kbd = KosmosKeyMatrixEmulator(kosmos=cls.kosmos, fw_id=KBD_FW_ID)

        cls.module.reset_module()
    # end def setUpClass

    @classmethod
    def tearDownClass(cls):
        """
        Free ``LedSpyModule`` instance.
        """
        cls._kbd = None
        super().tearDownClass()
    # end def tearDownClass

    def tearDown(self):
        """
        Validate LED module is reset and clean by the end of the Test Case being torn down.
        """
        # Save LED module state before reset
        status = self.module.status()

        # Reset LED module and settings
        self.module.reset_module()
        self.module.set_channel_enable(channel_enable=0)
        self.module.set_gate_latch(gate_latch=0)

        # Warn user if state before reset was not clean
        try:
            self.assertEqual(LED_SPY_STATE_RESET_OR_STOP, status.state,
                             msg=f'LED State should have been reset by the end of the test case '
                                 f'<{self.test_name}>.\n{status}')
            self.assertEqual(0, status.buffer_count,
                             msg=f'LED Buffer should have been emptied by the end of the test case '
                                 f'<{self.test_name}>.\n{status}')
            self.assertEqual(0, status.fifo_count,
                             msg=f'LED FIFO should have been emptied by the end of the test case '
                                 f'<{self.test_name}>.\n{status}')
        finally:
            super().tearDown()
        # end try
    # end def tearDown

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``LedSpyModule``

        :raise ``SkipTest``: LED SPY Module is not present in the Device Tree
        """
        if not cls.kosmos.dt.led_spy:
            raise SkipTest('LED SPY Module is not present in the Device Tree')
        # end if
        return cls.kosmos.led_spy[0]
    # end def _get_module_under_test

    def test_reset_module(self):
        """
        Validate LED reset() and start() methods.
        Note: Assertion calls are executed in the tested method itself.
        """
        # Configure LED module
        channel_count = 32
        channels = range(channel_count)
        channel_enable = sum((1 << ch) for ch in channels)
        gate_latch = 0
        self.module.set_channel_enable(channel_enable=channel_enable)
        self.module.set_gate_latch(gate_latch=gate_latch)

        # Start capture
        self.module.start_capture()

        # Wait in order to gather LED entries
        sleep(2)

        # Read LED module status
        led_status = self.module.status()
        # Validate LED module state
        self.assertEqual(LED_SPY_STATE_STARTED, led_status.state, msg=led_status)
        # Validate remote buffer count
        self.assertGreater(led_status.buffer_count, LED_SPY_FIFO_DEFAULT_THRESHOLD, msg=led_status)

        # Reset LED module, to clear the FIFO and buffer
        self.module.reset_module()

        # Wait a bit more, to prove by measurements that the LED module has stopped capturing
        sleep(2)

        # Read LED module status
        led_status = self.module.status()
        # Validate reset action
        self.assertEqual(0, led_status.buffer_count, msg=led_status)
        self.assertEqual(0, led_status.fifo_count, msg=led_status)
        self.assertEqual(LED_SPY_STATE_RESET_OR_STOP, led_status.state, msg=led_status)

        # Validate LED module settings were preserved during the reset
        self.assertEqual(channel_enable, self.module.get_channel_enable())
        self.assertEqual(gate_latch, self.module.get_gate_latch())
    # end def test_reset_module

    def test_settings_persistence_across_reset(self):
        """
        Validate LED module settings are preserved when LED module gets reset
        """
        for _ in range(10):
            # Set arbitrary LED module settings
            channel_enable = getrandbits(32)
            gate_latch = getrandbits(32)
            self.module.set_channel_enable(channel_enable=channel_enable)
            self.module.set_gate_latch(gate_latch=gate_latch)

            # Reset LED module
            self.module.reset_module()

            # Validate LED module settings were preserved during the reset
            self.assertEqual(channel_enable, self.module.get_channel_enable())
            self.assertEqual(gate_latch, self.module.get_gate_latch())
        # end for
    # end def test_settings_persistence_across_reset

    def test_start(self):
        """
        Validate LED start() method.
        Note: Assertion calls are executed in the tested method itself.
        """
        self.module.start_capture()

        # Reset LED module, to clear buffer
        self.module.reset_module()
    # end def test_start

    def test_stop(self):
        """
        Validate LED stop() method.
        Note: Assertion calls are executed in the tested method itself.
        """
        self.module.stop_capture()
    # end def test_stop

    def test_status(self):
        """
        Validate LED status() method.
        Note: Assertion calls are executed in the tested method itself.
        """
        self.module.status()
    # end def test_status

    def test_download_flush(self):
        """
        Validate LED download(), status(), stop(), reset() methods.
        Validate PES led_spy.flush_fifo_to_buffer() methods.
        """
        # Configure LED module
        channel_count = 32
        channels = range(channel_count)
        channel_enable = sum((1 << ch) for ch in channels)
        self.module.set_channel_enable(channel_enable=channel_enable)
        self.module.set_gate_latch(gate_latch=0)

        # Start LED module (enable FIFO interrupts and LED state machine)
        self.module.start_capture()

        # Wait in order to gather LED entries
        sleep(2)

        # Stop LED module (reset and hold LED state machine)
        status_after_stop = self.module.stop_capture()
        self.assertGreater(status_after_stop.buffer_count, LED_SPY_FIFO_DEFAULT_THRESHOLD,
                           msg=f'Buffer should contain entries at this point: {status_after_stop}')
        self.assertGreater(status_after_stop.fifo_count, 0,
                           msg=f'FIFO should contain entries at this point: {status_after_stop}')

        # Flush LED SPY FIFO
        self.module.flush_fifo_to_buffer()
        self.kosmos.sequencer.play_sequence()
        status_after_flush = self.module.status()
        self.assertEqual(status_after_stop.buffer_count + status_after_stop.fifo_count, status_after_flush.buffer_count,
                         msg=f'Unexpected LED FIFO Flush behavior:\n'
                             f'Before FIFO Flush: {status_after_stop}\n'
                             f'After FIFO Flush : {status_after_flush}\n')
        self.assertEqual(0, status_after_flush.fifo_count, msg=f'FIFO should be empty after flush: {status_after_flush}')

        # Download buffer
        led_buffer = self.module.download(count=status_after_flush.buffer_count)
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Reset LED module via CPU, to reset hardware and software
        self.module.reset_module()

        # Print result
        if self.VERBOSE:
            print(self._buffer_to_str(led_buffer, channels))
        # end if
    # end def test_download_flush

    def test_download_while_capture_is_in_progress(self):
        """
        Validate LED download(), status(), stop(), reset() methods.
        Validate PES led_spy.flush_fifo_to_buffer() methods.
        """
        # Configure LED module
        channel_count = 32
        channels = range(channel_count)
        channel_enable = sum((1 << ch) for ch in channels)
        self.module.set_channel_enable(channel_enable=channel_enable)
        self.module.set_gate_latch(gate_latch=0)

        # --- Control Run ---

        # Prepare PES sequence
        capture_duration = 5
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.pes.delay(delay_s=capture_duration, action=self.module.action_event.STOP)
        self.module.flush_fifo_to_buffer()
        # Execute PES sequence
        self.kosmos.sequencer.play_sequence()
        # Save LED entry count for later
        led_status = self.module.status()
        led_count_control = led_status.buffer_count
        # Reset LED module, Buffer & FIFO
        self.module.reset_module()

        # --- Test Run ---

        # Prepare same PES sequence
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.pes.delay(delay_s=capture_duration, action=self.module.action_event.STOP)
        self.module.flush_fifo_to_buffer()
        # Execute PES sequence
        self.kosmos.sequencer.play_sequence(block=False)

        # Download LED entries continuously until end of PES sequence
        led_buffer = []
        while True:
            status = self.kosmos.sequencer.status()
            if status.led_spy.buffer_count > 0:
                led_buffer.extend(self.module.download(count=status.led_spy.buffer_count))
            # end if
            if status.state != SEQUENCER_STATE_RUNNING:
                break
            # end if
        # end while

        # Validate FIFO and Buffer got fully emptied from downloads
        led_status = self.module.status()
        self.assertEqual(0, led_status.buffer_count, msg=f'Buffer should be empty after download: {led_status}')
        self.assertEqual(0, led_status.fifo_count, msg=f'FIFO should be empty after download: {led_status}')

        # Validate that all LED entries got downloaded
        self.assertEqual(led_count_control, len(led_buffer))

        # Reset LED module
        self.module.reset_module()

        # Print result
        if self.VERBOSE:
            print(self._buffer_to_str(led_buffer, channels))
        # end if
    # end def test_download_while_capture_is_in_progress

    def test_pes_action_event_start_reset(self):
        """
        Validate LED status() and reset() methods.
        Validate `PES_ACTION_EVENT_LED_START` and `PES_ACTION_EVENT_LED_RESET` PES Actions.
        """
        # Configure LED module
        channel_count = 32
        channels = range(channel_count)
        channel_enable = sum((1 << ch) for ch in channels)
        self.module.set_channel_enable(channel_enable=channel_enable)
        self.module.set_gate_latch(gate_latch=0)

        # Start LED module via PES
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(LED_SPY_STATE_STARTED, status.state, msg=status)

        # Reset LED module via PES, after 1 second delay
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.RESET)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(LED_SPY_STATE_RESET_OR_STOP, status.state, msg=status)
        self.assertFalse(status.fifo_overrun, msg='FIFO overrun status should be cleared by LED RESET PES Action.')
        self.assertEqual(0, status.fifo_count, msg='FIFO should be reset by LED RESET PES Action.')
        self.assertGreater(status.buffer_count, 0, msg='Buffer should NOT be reset by LED RESET PES Action.')

        # Reset LED module via CPU, to clear buffer
        self.module.reset_module()
    # end def test_pes_action_event_start_reset

    def test_pes_action_event_start_stop(self):
        """
        Validate LED status(), reset(), download() methods.
        Validate `PES_ACTION_EVENT_LED_START` and `PES_ACTION_EVENT_LED_STOP` PES Actions.
        """
        # Configure LED module
        channel_count = 32
        channels = range(channel_count)
        channel_enable = sum((1 << ch) for ch in channels)
        self.module.set_channel_enable(channel_enable=channel_enable)
        self.module.set_gate_latch(gate_latch=0)

        # Start LED module via PES
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(LED_SPY_STATE_STARTED, status.state, msg=status)

        # Stop capture via PES, after 1 second delay
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.STOP)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(LED_SPY_STATE_RESET_OR_STOP, status.state, msg=status)

        # Resume capture via PES, after 1 second delay
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.START)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(LED_SPY_STATE_STARTED, status.state, msg=status)

        # Stop capture via PES, after 1 second delay
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.STOP)
        self.module.flush_fifo_to_buffer()
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(LED_SPY_STATE_RESET_OR_STOP, status.state, msg=status)
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after flush: {status}')

        # Download buffer
        led_buffer = self.module.download(count=status.buffer_count)
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Print result
        if self.VERBOSE:
            print(self._buffer_to_str(led_buffer, channels))
        # end if
    # end def test_pes_action_event_start_stop

    def test_channel_enable(self):
        """
        Validate set_channel_enable() and get_channel_enable() methods.
        """
        max_uint32 = (1 << 32) - 1
        channels = [0, max_uint32] + [getrandbits(32) for _ in range(10)]
        for channel_tx in channels:
            # Write value to remote device
            self.module.set_channel_enable(channel_enable=channel_tx)
            # Read value from remote device
            channel_rx = self.module.get_channel_enable()
            # Validate stored remote value
            self.assertEqual(channel_tx, channel_rx, "WRITE then READ operation failed.")
        # end for

        # Validate input bounds
        with self.assertRaises(AssertionError):
            self.module.set_channel_enable(channel_enable=(max_uint32 + 1))
        # end with
    # end def test_channel_enable

    def test_gate_latch(self):
        """
        Validate set_gate_latch() and get_gate_latch methods.
        """
        max_uint32 = (1 << 32) - 1
        gates = [0, (1 << 32) - 1] + [getrandbits(32) for _ in range(10)]
        for gates_tx in gates:
            # Write value to remote device
            self.module.set_gate_latch(gate_latch=gates_tx)
            # Read value from remote device
            gates_rx = self.module.get_gate_latch()
            # Validate stored remote value
            self.assertEqual(gates_tx, gates_rx, "WRITE then READ operation failed.")
        # end for

        # Validate input bounds
        with self.assertRaises(AssertionError):
            self.module.set_gate_latch(gate_latch=(max_uint32 + 1))
        # end with
    # end def test_gate_latch

    @staticmethod
    def _buffer_to_str(buffer, channels):
        """
        Simple string representation of LED traffic.

        :param buffer: LED capture buffer
        :type buffer: ``list[int]``
        :param channels: "LED channel" parameter
        :type channels: ``led_spy_channel_enable_t or int``

        :return: string representation of LED traffic
        :rtype: ``str``
        """
        leddataparser = LedDataParser(channels)
        timeline = leddataparser.parse_entries(buffer)
        return str(timeline)
    # end def _buffer_to_str

# end class KosmosLedSpyTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
