#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.i2cspy_test
:brief: Tests for Kosmos I2C SPY class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/12/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from collections import Counter
from time import sleep
from time import time

from pyraspi.services.kosmos.i2cspyparser import I2cSpyFrameParser
from pyraspi.services.kosmos.i2cspyparser import I2cSpyRawParser
from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.i2cspy import I2cSpyExtendedModule
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_MODE_FRAME
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_MODE_RAW
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_STATE_RESET_OR_STOP
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_STATE_STARTED
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_mode_e__enumvalues


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@require_kosmos_device(DeviceName.I2C_SPY)
class KosmosI2cSpyTestCase(AbstractTestClass.DownloadModuleInterfaceTestCase):
    """
    Unitary Test for Kosmos I2C SPY class
    """
    VERBOSE = False
    TIMEOUT = 5  # seconds
    _slider_emulator: KosmosPowerSliderEmulator

    module: I2cSpyExtendedModule

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos
        """
        super().setUpClass()
        cls._slider_emulator = KosmosPowerSliderEmulator(kosmos=cls.kosmos, fw_id='RBK68')
    # end def setUpClass

    @classmethod
    def tearDownClass(cls):
        """
        Open Kosmos
        """
        cls._slider_emulator.power_off()
        super().tearDownClass()
    # end def tearDownClass

    def setUp(self):
        """
        Setup Test Case
        """
        super().setUp()
        self._slider_emulator.power_off()
        self.module.reset_module()
    # end def setUp

    def tearDown(self):
        """
        Validate I2C module is reset and clean by the end of the Test Case being teared down.
        """
        super().tearDown()
        status = self.module.status()
        self.module.reset_module()
        self.assertEqual(I2C_SPY_STATE_RESET_OR_STOP, status.state,
                         msg=f'I2C State should have been reset by the end of the test case '
                             f'<{self.test_name}>.\n{status}')
        self.assertEqual(0, status.buffer_count,
                         msg=f'I2C Buffer should have been emptied by the end of the test case '
                             f'<{self.test_name}>.\n{status}')
        self.assertEqual(0, status.fifo_count,
                         msg=f'I2C FIFO should have been emptied by the end of the test case '
                             f'<{self.test_name}>.\n{status}')
    # end def tearDown

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``I2cSpyExtendedModule``

        :raise ``AssertionError``: Module is not defined in the Device Tree
        """
        assert cls.kosmos.dt.i2c_spy[0], 'I2C SPY Module is not present in the Device Tree'
        return cls.kosmos.dt.i2c_spy[0]
    # end def _get_module_under_test

    def test_reset_module(self):
        """
        Validate I2C reset() method.
        Note: Assertion test are executed in the method itself.
        """
        self.module.reset_module()
    # end def test_reset_module

    def test_start(self):
        """
        Validate I2C start_capture() method.
        Note: Assertion test are executed in the method itself.
        """
        self.module.start_capture()

        # Reset I2C module, to clear buffer
        self.module.reset_module()
    # end def test_start

    def test_stop(self):
        """
        Validate I2C stop_capture() method.
        Note: Assertion test are executed in the method itself.
        """
        self.module.stop_capture()
    # end def test_stop

    def test_status(self):
        """
        Validate I2C status() method.
        Note: Assertion test are executed in the method itself.
        """
        self.module.status()
    # end def test_status

    def test_download_flush(self):
        """
        Validate I2C download(), status(), stop(), reset() methods.
        Validate PES i2c_spy.flush_fifo_to_buffer() methods.
        """
        duration = 10

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_RAW

        # Power on the DUT
        self._slider_emulator.power_on()

        # Start I2C module (enable FIFO interrupts and I2C state machine)
        self.debug_print(f'Start I2C capture.')
        self.module.start_capture()

        # Wait during capture
        sleep(duration)

        # Power off the DUT
        self._slider_emulator.power_off()

        # Stop I2C module (reset and hold I2C state machine)
        status_after_stop = self.module.stop_capture()
        self.assertLess(0, status_after_stop.buffer_count + status_after_stop.fifo_count,
                        msg=f'FIFO and buffer should NOT be reset by I2C STOP PES Action: {status_after_stop}')
        self.debug_print(f'Stop I2C capture ({status_after_stop.buffer_count} entries in buffer).')

        # Flush I2C SPY FIFO
        self.debug_print(f'Flush FIFO ({status_after_stop.fifo_count} entries in FIFO).')
        self.module.flush_fifo_to_buffer()
        self.kosmos.sequencer.play_sequence()
        status_after_flush = self.module.status()
        self.assertEqual(status_after_stop.buffer_count + status_after_stop.fifo_count, status_after_flush.buffer_count,
                         msg=f'Unexpected I2C FIFO Flush behavior:\n'
                             f'Before FIFO Flush: {status_after_stop}\n'
                             f'After FIFO Flush : {status_after_flush}\n')
        self.assertEqual(0, status_after_flush.fifo_count, msg=f'FIFO should be empty after flush: {status_after_flush}')

        # Download buffer
        self.debug_print(f'Downloading I2C capture data ({status_after_flush.buffer_count} entries in buffer)...')
        i2c_buffer = self.module.download(count=status_after_flush.buffer_count)
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Reset I2C module via CPU, to reset hardware and software
        self.module.reset_module()

        # Parse I2C SPY buffer into frames
        parser = self.module.get_parser()
        self.assertIsInstance(parser, I2cSpyRawParser)
        parser.parse(i2c_buffer)

        # Print I2C SPY frames
        self.debug_print(repr(parser))
    # end def test_download_flush

    def test_download_while_capture_is_in_progress(self):
        """
        Validate I2C SPY actions (via PES event): RESET, START, STOP.
        Validate i2c_spy.flush_fifo_to_buffer() methods.
        Validate download of I2C data while record is in progress.
        """
        duration = 10  # seconds

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_RAW

        # Prepare PES sequence
        self.kosmos.sequencer.offline_mode = True
        # Reset I2C module via PES
        self.kosmos.pes.execute(action=self.module.action_event.RESET)
        # Turn keyboard slider ON via PES
        self._slider_emulator.power_on()
        # Start I2C module via PES
        self.kosmos.pes.execute(action=self.module.action_event.START)
        # Run capture until Go signal is raised
        self.kosmos.pes.wait_go_signal()
        # Turn keyboard slider OFF via PES
        self._slider_emulator.power_off()
        # Stop I2C module via PES
        self.kosmos.pes.delay(delay_s=0.5)
        self.kosmos.pes.execute(action=self.module.action_event.STOP)
        self.module.flush_fifo_to_buffer()

        # Execute PES sequence
        self.debug_print(f'Start I2C capture.')
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # Record I2C data
        time_start = time()
        i2c_buffer = []
        count_prev = 0
        count_download = 0
        while time() < time_start + duration:
            status = self.module.status()
            count_new = status.buffer_count + status.fifo_count
            if count_new > count_prev - count_download:
                # new data was captured since last iteration
                count_prev = count_new
                count_download = min(status.buffer_count, 100)  # split download by small chunks
                i2c_buffer.extend(self.module.download(count=count_download))
            else:
                sleep(0.1)
            # end if
        # end while

        # Trigger I2C SPY module Stop event then FIFO Flush action
        self.debug_print(f'Stop I2C capture and Flush FIFO.')
        self.kosmos.fpga.pulse_global_go_line()
        sleep(1)

        # Validate test sequence is finished
        self.assertTrue(self.kosmos.sequencer.is_end_of_sequence())

        # Download the last entries that were flushed from FIFO to buffer
        status = self.module.status()
        if status.buffer_count > 0:
            self.debug_print(f'Download the last {status.buffer_count} entries that were flushed from FIFO to buffer.')
            i2c_buffer.extend(self.module.download(count=status.buffer_count))
        # end if

        # Sanity checks
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Reset I2C module via CPU, to reset hardware and software
        self.module.reset_module()

        # Parse I2C SPY buffer into frames
        parser = self.module.get_parser()
        self.assertIsInstance(parser, I2cSpyRawParser)
        parser.parse(i2c_buffer)

        # Print I2C SPY frames
        self.debug_print(repr(parser))
    # end def test_download_while_capture_is_in_progress

    def test_pes_action_event_start_reset(self):
        """
        Validate I2C status() and reset() methods.
        Validate `PES_ACTION_EVENT_I2C_SPY_0_START` and `PES_ACTION_EVENT_I2C_SPY_0_RESET` PES Actions.
        """
        duration = 2  # seconds

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_RAW

        # Turn keyboard slider ON
        self._slider_emulator.power_on()

        # Start I2C module via PES
        self.debug_print(f'Start I2C capture.')
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(I2C_SPY_STATE_STARTED, status.state, msg=status)

        # Wait for I2C data to be streamed on the I2C bus
        sleep(duration)

        self.debug_print(f'Reset I2C module.')

        # Reset I2C module via PES, after 1 second delay
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.RESET)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(I2C_SPY_STATE_RESET_OR_STOP, status.state, msg=status)
        self.assertFalse(status.fifo_overrun, msg='FIFO overrun status should be cleared by I2C RESET PES Action.')
        self.assertEqual(0, status.fifo_count, msg='FIFO should be reset by I2C RESET PES Action.')
        self.assertLess(0, status.buffer_count, msg='Buffer should NOT be reset by I2C RESET PES Action.')

        # Turn keyboard slider OFF
        self._slider_emulator.power_off()

        # Reset I2C module via CPU, to clear buffer
        self.module.reset_module()
    # end def test_pes_action_event_start_reset

    def test_pes_action_event_start_stop(self):
        """
        Validate I2C status(), reset(), download() methods.
        Validate `PES_ACTION_EVENT_I2C_SPY_0_START` and `PES_ACTION_EVENT_I2C_SPY_0_STOP` PES Actions.
        Validate i2c_spy.flush_fifo_to_buffer() methods.
        """
        duration = 2  # seconds

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_RAW

        # Turn keyboard slider ON
        self._slider_emulator.power_on()

        # Start I2C module via PES
        self.debug_print(f'Start I2C capture.')
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(I2C_SPY_STATE_STARTED, status.state, msg=status)

        # Wait for I2C data to be streamed on the I2C bus
        sleep(duration)

        # Stop capture via PES, after 1 second delay
        self.debug_print(f'Stop I2C capture.')
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.STOP)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(I2C_SPY_STATE_RESET_OR_STOP, status.state, msg=status)
        break1 = status.buffer_count + status.fifo_count

        # Resume capture via PES, after 1 second delay
        self.debug_print(f'Resume I2C capture.')
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.START)
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(I2C_SPY_STATE_STARTED, status.state, msg=status)

        # Stop capture via PES, after 1 second delay
        self.debug_print(f'Stop I2C capture and flush FIFO.')
        self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.STOP)
        self.module.flush_fifo_to_buffer()
        self.kosmos.sequencer.play_sequence()
        status = self.module.status()
        self.assertEqual(I2C_SPY_STATE_RESET_OR_STOP, status.state, msg=status)
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after flush: {status}')

        # Turn keyboard slider OFF
        self._slider_emulator.power_off()

        # Download buffer
        self.debug_print(f'Downloading I2C capture data ({status.buffer_count} entries in buffer)...')
        i2c_buffer = self.module.download(count=status.buffer_count)
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Parse I2C SPY buffer into frames
        parser = self.module.get_parser()
        self.assertIsInstance(parser, I2cSpyRawParser)
        parser.parse(i2c_buffer)

        # Print I2C SPY frames
        self.debug_print(repr(parser))
    # end def test_pes_action_event_start_stop

    def test_timestamp(self):
        """
        Validate I2C timestamps.
        """
        duration = 0.5  # seconds

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_RAW

        # Prepare test sequence
        self.kosmos.sequencer.offline_mode = True
        # Reset I2C module via PES
        self.kosmos.pes.execute(action=self.module.action_event.RESET)
        # Turn keyboard slider ON via PES
        self._slider_emulator.power_on()
        # Start I2C module via PES
        self.kosmos.pes.execute(action=self.module.action_event.START)
        self.kosmos.pes.delay(delay_s=duration)
        # Turn keyboard slider OFF via PES
        self._slider_emulator.power_off()
        # Stop I2C module via PES
        self.kosmos.pes.delay(delay_s=1)
        self.kosmos.pes.execute(action=self.module.action_event.STOP)
        self.module.flush_fifo_to_buffer()

        # Play test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(timeout=duration+5)
        status = self.module.status()

        # Download buffer
        self.debug_print(f'Downloading I2C capture data ({status.buffer_count} entries in buffer, '
              f'{100 * status.buffer_count // self.module.size()}% full)...')
        i2c_buffer = self.module.download(count=status.buffer_count)
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Reset I2C module via CPU, to reset hardware and software
        self.module.reset_module()

        # Parse I2C SPY buffer into frames
        parser = self.module.get_parser()
        self.assertIsInstance(parser, I2cSpyRawParser)
        parser.parse(i2c_buffer)

        # Print I2C SPY frames
        self.debug_print(repr(parser))
    # end def test_timestamp

    def test_i2c_frame(self):
        """
        Validate I2C stream parsing into I2C frames.
        """
        duration = 10  # seconds

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_FRAME

        # Prepare test sequence
        self.kosmos.sequencer.offline_mode = True
        # Reset I2C module via PES
        self.kosmos.pes.execute(action=self.module.action_event.RESET)
        # Turn keyboard slider ON via PES
        self._slider_emulator.power_on()
        # Start I2C module via PES
        self.kosmos.pes.execute(action=self.module.action_event.START)
        # Wait during capture
        self.kosmos.pes.delay(delay_s=duration)
        # Turn keyboard slider OFF via PES
        self._slider_emulator.power_off()
        # Stop I2C module via PES
        self.kosmos.pes.delay(delay_s=1)
        self.kosmos.pes.execute(action=self.module.action_event.STOP)
        self.module.flush_fifo_to_buffer()

        # Play test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(timeout=duration+5)

        # Download I2C SPY buffer
        i2c_frame_buffer = self.module.download()

        # Check I2C SPY Buffer and FIFO
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Reset I2C module via CPU, to reset hardware and software
        self.module.reset_module()

        # Parse I2C SPY buffer into frames
        parser = self.module.get_parser()
        self.assertIsInstance(parser, I2cSpyFrameParser)
        parser.parse(i2c_frame_buffer)

        # Print I2C SPY frames
        self.debug_print(repr(parser))
    # end def test_i2c_frame

    def test_i2c_frame_streaming(self):
        """
        Validate I2C stream parsing into I2C frames.
        """
        repetition = 10

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_FRAME

        # Prepare test sequence
        self.kosmos.sequencer.offline_mode = True
        self._slider_emulator.power_off()
        self.kosmos.pes.delay(delay_s=0.3)
        self.kosmos.pes.execute(action=self.module.action_event.RESET)

        for _ in range(repetition):
            self._slider_emulator.power_on()
            self.kosmos.pes.execute(action=self.module.action_event.START)
            self.kosmos.pes.delay(delay_s=1)
            self._slider_emulator.power_off()
            self.kosmos.pes.delay(delay_s=0.3)
            self.kosmos.pes.execute(action=self.module.action_event.STOP)
            self.kosmos.pes.delay(delay_s=0.7)
        # end for

        self.module.flush_fifo_to_buffer()

        # Play test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        parser = I2cSpyFrameParser(fpga_clock_freq_hz=FPGA_CURRENT_CLOCK_FREQ)

        run_index = 0
        frame_index = 0

        # Download and parse data while test sequencer is running
        while True:
            done = self.kosmos.sequencer.is_end_of_sequence()  # Get this information first
            status = self.module.status()
            if status.buffer_count == 0:
                if done:
                    # Exit loop at the end of test sequence, after all data was downloaded
                    break
                else:
                    # Test sequence is not done yet and there is nothing to download for the moment
                    continue
                # end if
            # end if

            # Download I2C SPY buffer
            dl = self.module.download(count=min(status.buffer_count, 28*5000))
            # Parse I2C SPY buffer into frames
            parser.parse(dl)

            # Print parsed frame, starting where last loop iteration stopped
            while True:
                for frame_idx in range(frame_index, len(parser.frame_runs[run_index])):
                    frame = parser.frame_runs[run_index][frame_idx]
                    frame_str = str(frame)
                    # assert not frame.nack, f'NACK in {frame_str}'  # depends on I2C implementation of DUT
                    if len(frame_str) > 40:
                        frame_str = frame_str[:40] + "..."
                    # end if
                    self.debug_print(f'[{run_index:03d}][{frame_idx:04d}]{frame_str}')
                    frame_index = frame_idx
                # end for
                if run_index + 1 < len(parser.frame_runs):
                    run_index += 1
                    frame_index = 0
                else:
                    break
                # end if
            # end while
        # end while

        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Reset I2C module via CPU, to reset hardware and software
        self.module.reset_module()
    # end def test_i2c_frame_streaming

    def test_i2c_frame_parser(self):
        """
        Validate I2C stream parsing into I2C frames.
        """
        repetition = 3

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_FRAME

        # Prepare test sequence
        self.kosmos.sequencer.offline_mode = True
        self._slider_emulator.power_off()
        self.kosmos.pes.delay(delay_s=0.3)
        self.kosmos.pes.execute(action=self.module.action_event.RESET)
        self.kosmos.pes.delay(delay_s=1)

        for _ in range(repetition):
            self._slider_emulator.power_on()
            self.kosmos.pes.execute(action=self.module.action_event.START)
            self.kosmos.pes.delay(delay_s=1)
            self._slider_emulator.power_off()
            self.kosmos.pes.delay(delay_s=0.3)
            self.kosmos.pes.execute(action=self.module.action_event.STOP)
            self.kosmos.pes.delay(delay_s=0.7)
        # end for

        self.module.flush_fifo_to_buffer()

        # Play test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(timeout=(repetition * 2 + 5))

        # Download I2C SPY buffer
        i2c_frame_buffer = self.module.download()

        # Check I2C SPY Buffer and FIFO
        status = self.module.status()
        self.assertEqual(0, status.buffer_count, msg=f'Buffer should be empty after download: {status}')
        self.assertEqual(0, status.fifo_count, msg=f'FIFO should be empty after download: {status}')

        # Reset I2C module via CPU, to reset hardware and software
        self.module.reset_module()

        # Parse I2C SPY buffer into frames
        parser = self.module.get_parser()
        self.assertIsInstance(parser, I2cSpyFrameParser)
        parser.parse(i2c_frame_buffer)

        # Print most common frame lengths
        len_list = [len(frame) for frames in parser.frame_runs for frame in frames]
        self.debug_print('\n'.join([f'{v:4} items of length {k:4}' for k, v in Counter(len_list).most_common(6)]))

        # Print I2C SPY frames
        self.debug_print(repr(parser))
    # end def test_i2c_frame_parser

    def test_i2c_frame_timestamp(self):
        """
        Validate I2C stream parsing into I2C frames.
        """
        repetition = 3
        timer = TIMER.LOCAL

        delay_0 = 0.3  # second
        delay_1 = 1    # second
        delay_2 = 1    # second
        delay_3 = 0.3  # second
        delay_4 = 0.7  # second

        # Configure I2C SPY module
        self.module.mode = I2C_SPY_MODE_FRAME

        # Prepare test sequence
        self.kosmos.sequencer.offline_mode = True
        self._slider_emulator.power_off()
        self.kosmos.pes.delay(delay_s=delay_0)
        self.kosmos.pes.execute(action=self.module.action_event.RESET)
        self.kosmos.timers[timer].reset()
        self.kosmos.pes.delay(delay_s=delay_1)

        for _ in range(repetition):
            self._slider_emulator.power_on()
            self.kosmos.pes.execute(action=self.module.action_event.START)
            self.kosmos.timers[timer].save()
            self.kosmos.pes.delay(delay_s=delay_2)
            self._slider_emulator.power_off()
            self.kosmos.pes.delay(delay_s=delay_3)
            self.kosmos.pes.execute(action=self.module.action_event.STOP)
            self.kosmos.timers[timer].save()
            self.kosmos.pes.delay(delay_s=delay_4)
        # end for

        self.module.flush_fifo_to_buffer()

        # Play test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(
            timeout=(delay_0 + delay_1 + (delay_2 + delay_3 + delay_4) * repetition) + 1)

        # Download I2C SPY buffer
        i2c_frame_buffer = self.module.download()

        # Reset I2C module via CPU, to reset hardware and software
        self.module.reset_module()

        # Parse I2C SPY buffer into frames
        parser = self.module.get_parser()
        self.assertIsInstance(parser, I2cSpyFrameParser)
        parser.parse(i2c_frame_buffer)

        # Download timer timestamps and convert them to seconds
        timer_buffer = self.kosmos.timers[timer].download()
        time_s = [t / FPGA_CURRENT_CLOCK_FREQ for t in timer_buffer]
        self.debug_print('\n'.join([f't{i} = {t:9d} ticks ({time_s[i]:.9f} s)' for i, t in enumerate(timer_buffer)]))

        # Print I2C SPY parser header and frame run headers
        self.debug_print(str(parser))
        self.debug_print('\n'.join(map(str, parser.frame_runs)))

        # Check timer timestamps match I2C timings
        delta = 1e-6  # second
        self.assertAlmostEqual(time_s[0], delay_1, delta=delta)
        self.assertAlmostEqual(time_s[1], time_s[0] + delay_2 + delay_3, delta=delta)
        self.assertAlmostEqual(time_s[2], time_s[1] + delay_4, delta=delta)
        self.assertAlmostEqual(time_s[3], time_s[2] + delay_2 + delay_3, delta=delta)
        self.assertAlmostEqual(time_s[4], time_s[3] + delay_4, delta=delta)
        self.assertAlmostEqual(time_s[5], time_s[4] + delay_2 + delay_3, delta=delta)
    # end def test_i2c_frame_timestamp

    def test_i2c_raw_and_frame_parsing(self):
        """
        Validate I2C frame parsing matches RAW I2C data parsing.
        """
        modes = [I2C_SPY_MODE_RAW, I2C_SPY_MODE_FRAME]
        i2c_buffers = {I2C_SPY_MODE_RAW: None, I2C_SPY_MODE_FRAME: None}
        parsers = {I2C_SPY_MODE_RAW: None, I2C_SPY_MODE_FRAME: None}

        for mode in modes:
            # Configure I2C SPY module
            self.module.mode = mode
            self.debug_print(f'\nConfiguring I2C SPY module in {i2c_spy_mode_e__enumvalues[mode]} mode.')

            # Prepare test sequence
            self.kosmos.sequencer.offline_mode = True
            self.kosmos.pes.execute(action=self.module.action_event.RESET)
            self._slider_emulator.power_on()
            self.kosmos.pes.execute(action=self.module.action_event.START)
            self.kosmos.pes.delay(delay_s=1)
            self._slider_emulator.power_off()
            self.kosmos.pes.delay(delay_s=0.3)
            self.kosmos.pes.execute(action=self.module.action_event.STOP)
            self.kosmos.pes.delay(delay_s=0.7)
            self.module.flush_fifo_to_buffer()

            # Play test sequence
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()

            # Download I2C SPY buffer
            i2c_buffers[mode] = self.module.download()

            # Parse I2C SPY buffer
            parsers[mode] = self.module.get_parser()
            self.assertIsInstance(parsers[mode], I2cSpyRawParser if mode == I2C_SPY_MODE_RAW else I2cSpyFrameParser)
            parsers[mode].parse(i2c_buffers[mode])

            # Print I2C SPY frames
            self.debug_print(repr(parsers[mode]))
        # end for
    # end def test_i2c_raw_and_frame_parsing

    @require_kosmos_device(DeviceName.I2C_SPY, 2)
    def test_concurrent_2nd_i2c_timestamp(self):
        """
        Validate the two I2C modules working at the same time
        """
        duration = 0.5  # seconds

        # Configure I2C SPY module
        self.kosmos.i2c_spy[0].mode = I2C_SPY_MODE_RAW
        self.kosmos.i2c_spy[1].mode = I2C_SPY_MODE_RAW

        # Prepare test sequence
        self.kosmos.sequencer.offline_mode = True
        # Reset I2C module via PES
        self.kosmos.pes.execute(action=self.kosmos.i2c_spy[0].action_event.RESET)
        self.kosmos.pes.execute(action=self.kosmos.i2c_spy[1].action_event.RESET)
        # Turn keyboard slider ON via PES
        self._slider_emulator.power_on()
        # Start I2C module via PES
        self.kosmos.pes.execute(action=self.kosmos.i2c_spy[0].action_event.START)
        self.kosmos.pes.execute(action=self.kosmos.i2c_spy[1].action_event.START)
        self.kosmos.pes.delay(delay_s=duration)
        # Turn keyboard slider OFF via PES
        self._slider_emulator.power_off()
        # Stop I2C module via PES
        self.kosmos.pes.delay(delay_s=1)
        self.kosmos.pes.execute(action=self.kosmos.i2c_spy[0].action_event.STOP)
        self.kosmos.pes.execute(action=self.kosmos.i2c_spy[1].action_event.STOP)
        self.kosmos.i2c_spy[0].flush_fifo_to_buffer()
        self.kosmos.i2c_spy[1].flush_fifo_to_buffer()

        # Play test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(timeout=duration+5)
        status_0 = self.kosmos.i2c_spy[0].status()
        status_1 = self.kosmos.i2c_spy[1].status()

        # Download buffer
        self.debug_print(f'Downloading I2C capture data ({status_0.buffer_count} entries in buffer, '
                         f'{100 * status_0.buffer_count // self.kosmos.i2c_spy[0].size()}% full)...')
        self.debug_print(f'Downloading I2C capture data ({status_1.buffer_count} entries in buffer, '
                         f'{100 * status_1.buffer_count // self.kosmos.i2c_spy[1].size()}% full)...')
        i2c_0_buffer = self.kosmos.i2c_spy[0].download(count=status_0.buffer_count)
        i2c_1_buffer = self.kosmos.i2c_spy[1].download(count=status_1.buffer_count)
        status_0 = self.kosmos.i2c_spy[0].status()
        status_1 = self.kosmos.i2c_spy[1].status()
        self.assertEqual(0, status_0.buffer_count, msg=f'Buffer should be empty after download: {status_0}')
        self.assertEqual(0, status_0.fifo_count, msg=f'FIFO should be empty after download: {status_0}')
        self.assertEqual(0, status_1.buffer_count, msg=f'Buffer should be empty after download: {status_1}')
        self.assertEqual(0, status_1.fifo_count, msg=f'FIFO should be empty after download: {status_1}')

        # Reset I2C module via CPU, to reset hardware and software
        self.kosmos.i2c_spy[0].reset_module()
        self.kosmos.i2c_spy[1].reset_module()

        # Parse I2C SPY buffer into frames
        parser_0 = self.kosmos.i2c_spy[0].get_parser()
        self.assertIsInstance(parser_0, I2cSpyRawParser)
        parser_0.parse(i2c_0_buffer)

        parser_1 = self.kosmos.i2c_spy[1].get_parser()
        self.assertIsInstance(parser_1, I2cSpyRawParser)
        parser_1.parse(i2c_1_buffer)

        # Print I2C SPY frames
        self.debug_print(repr(parser_0))
        self.debug_print(repr(parser_1))
    # end def test_concurrent_2nd_i2c_timestamp

    def debug_print(self, *args, **kwargs):
        """
        Print text to console if `VERBOSE` mode is enabled.

        :param args: arguments to be passed to `print()` function
        :type args: ``tuple[Any]``
        :param kwargs: arguments to be passed to `print()` function
        :type kwargs: ``dict[str, Any]``
        """
        if self.VERBOSE:
            print(*args, **kwargs)
        # end if
    # end def debug_print
# end class KosmosI2cSpyTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
