#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.pes_timer_test
:brief: Kosmos PES TIMER Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from random import randint

from pyraspi.services.kosmos.fpgatransport import UnderrunPayloadError
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.error import KosmosFatalError
from pyraspi.services.kosmos.module.module import ModuleStatusSanityChecksError
from pyraspi.services.kosmos.module.pes import PES_MARKER
from pyraspi.services.kosmos.module.pestimer import ALL_TIMERS
from pyraspi.services.kosmos.module.pestimer import RESETABLE_TIMERS
from pyraspi.services.kosmos.module.pestimer import STOPWATCH_OFFSET
from pyraspi.services.kosmos.module.pestimer import STOPWATCH_TIMERS
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.module.pestimer import TIMER_OFFSET_MAP
from pyraspi.services.kosmos.module.pestimer import TIMER_RESET_MARKER_ACTION_MAP
from pyraspi.services.kosmos.module.pestimer import TIMER_RESTART_MARKER_ACTION_MAP
from pyraspi.services.kosmos.module.pestimer import TIMER_SAVE_MARKER_ACTION_MAP
from pyraspi.services.kosmos.module.pestimer import TIMER_START_MARKER_ACTION_MAP
from pyraspi.services.kosmos.module.pestimer import TIMER_STOP_MARKER_ACTION_MAP
from pyraspi.services.kosmos.module.pestimer import TIMESTAMP_OFFSET
from pyraspi.services.kosmos.module.pestimer import TIMESTAMP_TIMERS
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import PES_TIMER_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RUNNING
from pyraspi.services.kosmos.test.common_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@require_kosmos_device(DeviceName.TIMERS)
class PesTimersModuleTestCase(KosmosCommonTestCase):
    """
    Kosmos PES TIMERS Module Test Class.
    """
    def setUp(self):
        """
        Setup PES TIMERS module.
        """
        super().setUp()
        self.kosmos.dt.timers.reset_module()
    # end def setUp

    def tearDown(self):
        """
        Teardown PES TIMERS module.
        """
        try:
            super().tearDown()
        finally:
            self.kosmos.dt.pes.clear()
            self.kosmos.dt.timers.reset_module()
        # end try
    # end def tearDown

    def test_simple(self):
        """
        Simple test case: Save timestamp, and validate its value.
        """
        for t in TIMER:
            # Create and play test sequence
            self.kosmos.dt.timers[t].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()
            self.kosmos.dt.sequencer.play_sequence()

            # Validate status
            status = self.kosmos.dt.timers[t].status()
            self.assertEqual(1, status.buffer_count, msg=f'{t.name}, status={status}')

            # Validate timestamp
            buffer = self.kosmos.dt.timers[t].download(count=1)
            self.assertEqual(self.kosmos.dt.timers[t].get_offset(), buffer[0], msg=f'{t.name}, buffer={buffer}')
        # end for
    # end def test_simple

    def test_status(self):
        """
        Validate `timers.status()` and `timers[t].status()` methods.
        """
        for t in TIMER:
            # Create and play test sequence
            self.kosmos.dt.timers[t].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()
            self.kosmos.dt.sequencer.play_sequence()

            # Validate status
            status_1 = self.kosmos.dt.timers[t].status()         # OK, best practice
            status_2 = self.kosmos.dt.timers.status()[t]         # OK, but harder to understand
            status_3 = self.kosmos.dt.timers._timer[t].status()  # Discouraged: access to private member
            self.assertEqual(bytes(status_1), bytes(status_2), msg=f'{t.name}, {status_1}, {status_2}')
            self.assertEqual(bytes(status_1), bytes(status_3), msg=f'{t.name}, {status_1}, {status_3}')
            self.kosmos.dt.timers.reset_module()
        # end for

        # Create and play test sequence
        for t in TIMER:
            for _ in range(t + 1):
                self.kosmos.dt.timers[t].save()
                self.kosmos.dt.timers.pes_delay_for_timer_interrupt()
            # end for
        # end for
        self.kosmos.dt.sequencer.play_sequence()

        # Validate status
        status_all = self.kosmos.dt.timers.status()
        self.assertEqual(1, status_all[TIMER.GLOBAL].buffer_count)
        self.assertEqual(2, status_all[TIMER.LOCAL].buffer_count)
        self.assertEqual(3, status_all[TIMER.STOPWATCH_1].buffer_count)
        self.assertEqual(4, status_all[TIMER.STOPWATCH_2].buffer_count)
        for t in TIMER:
            status_timer = self.kosmos.dt.timers[t].status()
            self.assertEqual(status_timer.buffer_count, status_all[t].buffer_count, msg=f'timer={t.name}')
        # end for
        self.kosmos.dt.timers.reset_module()
    # end def test_status

    def test_buffer_overrun(self):
        """
        Validate remote buffer overrun behavior.
        """
        count_range = range(1, PES_TIMER_BUFFER_SIZE + 3)
        for t in TIMER:
            # Create and play test sequence
            for i in count_range:
                self.kosmos.dt.pes.wait_go_signal()
                self.kosmos.dt.timers[t].save()
            # end for
            self.kosmos.dt.sequencer.play_sequence(block=False)

            # Validate status
            for i in count_range:
                self.kosmos.fpga.pulse_global_go_line()

                if i < PES_TIMER_BUFFER_SIZE:
                    # No buffer overrun
                    status = self.kosmos.dt.timers[t].status()
                    self.assertFalse(status.buffer_overrun, msg=f'{t.name}, i={i}, {status}')
                    self.assertEqual(i, status.buffer_count, msg=f'{t.name}, i={i}, {status}')
                else:
                    # Get Timer module status, without raising an exception for buffer_overrun
                    status = self.kosmos.dt.timers[t].status(sanity_checks=False)
                    self.assertTrue(status.buffer_overrun, msg=f'{t.name}, i={i}, {status}')
                    self.assertEqual(i % PES_TIMER_BUFFER_SIZE, status.buffer_count, msg=f'{t.name}, i={i}, {status}')
                    with self.assertRaisesRegex(ModuleStatusSanityChecksError, 'overrun'):
                        self.kosmos.dt.timers[t].status(sanity_checks=True)
                    # end with
                # end if
            # end for

            # Validate test sequence is finished
            # Get Sequencer module status, without raising an exception for buffer_overrun
            status = self.kosmos.dt.sequencer.status(sanity_checks=False)
            self.assertTrue(self.kosmos.dt.sequencer.is_end_of_sequence(status), msg=status)

            self.kosmos.dt.timers.reset_module()
            KosmosFatalError.clear_exception()
        # end for
    # end def test_buffer_overrun

    def test_download(self):
        """
        Validate download() method.
        """
        # Validate download of all available data, of a given Timer
        for t in TIMER:
            for i in range(1, 5):
                for _ in range(i):
                    self.kosmos.dt.timers[t].save()
                    self.kosmos.dt.timers.pes_delay_for_timer_interrupt()
                # end for
                self.kosmos.dt.sequencer.play_sequence()
                status = self.kosmos.dt.timers[t].status()
                self.assertFalse(status.buffer_overrun, msg=f'{t.name}, i={i}, status={status}')
                self.assertEqual(i, status.buffer_count, msg=f'{t.name}, i={i}, status={status}')
                buffer = self.kosmos.dt.timers[t].download()
                self.assertEqual(i, len(buffer), msg=f'{t.name}, i={i}, status={status}')
            # end for
        # end for

        # Validate download of all available data, of all Timers
        count = 5
        for _ in range(count):
            for t in TIMER:
                self.kosmos.dt.timers[t].save()
                self.kosmos.dt.timers.pes_delay_for_timer_interrupt()
            # end for
        # end for
        self.kosmos.dt.sequencer.play_sequence()
        status = self.kosmos.dt.timers.status()
        for t in TIMER:
            self.assertFalse(status[t].buffer_overrun, msg=f'{t.name}, status={status[t]}')
            self.assertEqual(count, status[t].buffer_count, msg=f'{t.name} status={status[t]}')
        # end for
        buffer = self.kosmos.dt.timers.download()
        for t in TIMER:
            self.assertEqual(count, len(buffer[t]), msg=f'{t.name}, buffer={buffer}')
        # end for

        # Validate Download specified data, of all Timers
        count = 5
        for _ in range(count):
            for t in TIMER:
                self.kosmos.dt.timers[t].save()
                self.kosmos.dt.timers.pes_delay_for_timer_interrupt()
            # end for
        # end for
        self.kosmos.dt.sequencer.play_sequence()
        status = self.kosmos.dt.timers.status()
        for t in TIMER:
            self.assertFalse(status[t].buffer_overrun, msg=f'{t.name}, status={status[t]}')
            self.assertEqual(count, status[t].buffer_count, msg=f'{t.name} status={status[t]}')
        # end for
        buffer = self.kosmos.dt.timers.download(count=count)
        for t in TIMER:
            self.assertEqual(count, len(buffer[t]), msg=f'{t.name}, buffer={buffer}')
        # end for
        status = self.kosmos.dt.timers.status()
        for t in TIMER:
            self.assertFalse(status[t].buffer_overrun, msg=f'{t.name}, status={status[t]}')
            self.assertEqual(0, status[t].buffer_count, msg=f'{t.name} status={status[t]}')
        # end for

        # Validate downloading more items than available raises an exception
        with self.assertRaisesRegex(UnderrunPayloadError, 'MSG_REPLY_RETURN_CODE_BUFFER_UNDERRUN'):
            self.kosmos.dt.timers.download(count=5)
        # end with
    # end def test_download

    def test_marker_action_exception(self):
        """
        Validate exception raised by reset(t), save(t), start(t), stop(t) and restart(t) methods.
        """
        # TIMER SAVE OPERATION
        for t in TIMER:
            self.kosmos.dt.timers.save(t)
        # end for

        # TIMER RESET OPERATION
        t = TIMER.GLOBAL
        with self.assertRaisesRegex(KeyError, f'{t.name} does not support RESET operation'):
            self.kosmos.dt.timers.reset(t)
        # end with
        for t in RESETABLE_TIMERS:
            self.kosmos.dt.timers.save(t)
        # end for

        # TIMER START OPERATION
        for t in STOPWATCH_TIMERS:
            self.kosmos.dt.timers.start(t)
        # end for
        for t in TIMESTAMP_TIMERS:
            with self.assertRaisesRegex(KeyError, f'{t.name} does not support START operation'):
                self.kosmos.dt.timers.start(t)
            # end with
        # end for

        # TIMER STOP OPERATION
        for t in STOPWATCH_TIMERS:
            self.kosmos.dt.timers.stop(t)
        # end for
        for t in TIMESTAMP_TIMERS:
            with self.assertRaisesRegex(KeyError, f'{t.name} does not support STOP operation'):
                self.kosmos.dt.timers.stop(t)
            # end with
        # end for

        # TIMER RESTART OPERATION
        for t in RESETABLE_TIMERS:
            self.kosmos.dt.timers.restart(t)
        # end for
        for t in [TIMER.GLOBAL]:
            with self.assertRaisesRegex(KeyError, f'{t.name} does not support RESTART operation'):
                self.kosmos.dt.timers.restart(t)
            # end with
        # end for
        self.kosmos.dt.pes.clear()
    # end def test_marker_action_exception

    def test_marker_action_combination(self):
        """
        Validate values of timers descriptors, by affinity or type.
        """
        self.kosmos.dt.timers.save(ALL_TIMERS)
        self.assertEqual(sum(TIMER_SAVE_MARKER_ACTION_MAP.values()), self.kosmos.dt.pes._buffer[-1].operand.raw)

        self.kosmos.dt.timers.reset(RESETABLE_TIMERS)
        self.assertEqual(sum(TIMER_RESET_MARKER_ACTION_MAP.values()), self.kosmos.dt.pes._buffer[-1].operand.raw)

        self.kosmos.dt.timers.stop(STOPWATCH_TIMERS)
        self.assertEqual(sum(TIMER_STOP_MARKER_ACTION_MAP.values()), self.kosmos.dt.pes._buffer[-1].operand.raw)

        self.kosmos.dt.timers.start(STOPWATCH_TIMERS)
        self.assertEqual(sum(TIMER_START_MARKER_ACTION_MAP.values()), self.kosmos.dt.pes._buffer[-1].operand.raw)

        self.kosmos.dt.timers.restart(RESETABLE_TIMERS)
        self.assertEqual(sum(TIMER_RESTART_MARKER_ACTION_MAP.values()), self.kosmos.dt.pes._buffer[-1].operand.raw)

        self.kosmos.dt.pes.clear()
    # end def test_marker_action_combination

    def test_marker_save_all(self):
        """
        Validate saving all timers simultaneously.
        """
        ticks = 10
        self.kosmos.dt.timers.restart(timers=STOPWATCH_TIMERS)
        self.kosmos.dt.pes.delay(delay_ticks=ticks)
        self.kosmos.dt.timers.save(timers=ALL_TIMERS)
        self.kosmos.dt.timers.pes_delay_for_timer_interrupt()
        self.kosmos.dt.timers.stop(timers=STOPWATCH_TIMERS)
        self.kosmos.dt.timers.reset(timers=RESETABLE_TIMERS)

        self.kosmos.dt.sequencer.play_sequence()
        status = self.kosmos.dt.timers.status()
        timestamps = self.kosmos.dt.timers.download()

        for t in ALL_TIMERS:
            self.assertEqual(1, status[t].buffer_count, msg=f'{t.name}, status={status[t]}')
            self.assertEqual(1, len(timestamps[t]), msg=f'{t.name}, buffer={timestamps[t]}')
        # end for
        for t in TIMESTAMP_TIMERS:
            # expect +1 tick to account for the PES:MARKER:START instruction
            self.assertEqual(TIMER_OFFSET_MAP[t] + ticks + 1, timestamps[t][0], msg=f'{t.name}, buffer={timestamps[t]}')
        # end for
        for t in STOPWATCH_TIMERS:
            self.assertEqual(TIMER_OFFSET_MAP[t] + ticks, timestamps[t][0], msg=f'{t.name}, buffer={timestamps[t]}')
        # end for
    # end def test_marker_save_all

    def test_stopwatch_start_stop(self):
        """
        Validate the START/STOP features of PES STOPWATCHes
        """
        for t in STOPWATCH_TIMERS:
            for delay_ticks in [10**6, 10**5, 10**4]:
                with self.subTest(timer=t, delay_ticks=delay_ticks):
                    # Reset and start timer
                    self.kosmos.dt.timers.restart(timers=t)
                    # Add a DELAY instruction matching the first half of the required delay
                    self.kosmos.dt.pes.delay(delay_ticks=delay_ticks // 2)
                    # Pause timer
                    self.kosmos.dt.timers.stop(timers=t)
                    # Add a DELAY instruction with a random delay between 1ms and 0.1s
                    self.kosmos.dt.pes.delay(delay_s=randint(1, 100) / 1000)
                    # Resume  timer
                    self.kosmos.dt.timers.start(timers=t)
                    # Add a DELAY instruction matching the second half of the required delay
                    self.kosmos.dt.pes.delay(delay_ticks=delay_ticks // 2)
                    # Save time mark timer
                    self.kosmos.dt.timers.save(timers=t)

                    # Upload and execute test sequence
                    self.kosmos.dt.sequencer.play_sequence()
                    # Download time marks
                    timemarks = self.kosmos.dt.timers.download()

                    # Validate time marks
                    self.assertEqual(sum(len(tm) for tm in timemarks.values()), 1)
                    self.assertEqual(len(timemarks[t]), 1)
                    self.assertEqual(timemarks[t][0], delay_ticks + 1)  # "+1" for the second delay instruction
                # end with
            # end for
        # end for
    # end def test_stopwatch_start_stop

    def test_timer_fixed_offset(self):
        """
        Validate constants ``TIMESTAMP_OFFSET`` and ``STOPWATCH_OFFSET``.
        This validates that the measured timers' count offset values match the expected offsets induced by the
        PES pipelined architecture.
        """
        delay_ticks = 10000

        # Validate GLOBAL/LOCAL timestamp timer offset (test initial timer capture + subsequent captures)
        for t in TIMESTAMP_TIMERS:
            with self.subTest(timers=t):
                # Subtest 1: Save timer value immediately after PES soft-reset
                self.kosmos.dt.timers[t].save()

                # Subtest 2: Save timer value, without prior reset
                self.kosmos.dt.pes.delay(delay_ticks=delay_ticks)
                self.kosmos.dt.timers[t].save()

                # Subtest 3: Save timer value, without prior reset
                self.kosmos.dt.pes.delay(delay_ticks=delay_ticks)
                self.kosmos.dt.timers[t].save()
                self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

                # Upload and execute test sequence
                self.kosmos.dt.sequencer.play_sequence()
                # Download time mark
                timemarks = self.kosmos.dt.timers.download()

                # Validate time marks
                self.assertEqual(len(timemarks[t]), 3)
                t0 = TIMESTAMP_OFFSET
                t1 = t0 + (delay_ticks + 1)  # +1 for the delay instruction
                t2 = t1 + (delay_ticks + 1)  # +1 for the two delay instructions (count as one instruction)
                self.assertEqual(timemarks[t][0], t0, msg='First timer capture with initial offset')
                self.assertEqual(timemarks[t][1], t1, msg='Second timer capture without additional offset')
                self.assertEqual(timemarks[t][2], t2, msg='Third timer capture without additional offset')
            # end with
        # end for

        # Test GLOBAL & LOCAL timestamp timers, consecutively
        with self.subTest(timers=TIMESTAMP_TIMERS):
            # Save timers value immediately after PES soft-reset
            self.kosmos.dt.timers[TIMER.GLOBAL].save()
            self.kosmos.dt.timers[TIMER.LOCAL].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            # Upload and execute test sequence
            self.kosmos.dt.sequencer.play_sequence()
            # Download time mark
            timemarks = self.kosmos.dt.timers.download()

            # Validate time marks
            self.assertEqual(len(timemarks[TIMER.GLOBAL]), 1)
            self.assertEqual(len(timemarks[TIMER.LOCAL]), 1)
            self.assertEqual(timemarks[TIMER.GLOBAL][0], TIMESTAMP_OFFSET)      # Global (1st instruction)
            self.assertEqual(timemarks[TIMER.LOCAL][0], TIMESTAMP_OFFSET + 1)  # Local  (2nd instruction)
        # end with

        # Test LOCAL timers
        t = TIMER.LOCAL
        with self.subTest(timers=t):
            # Subtest 1: Save timer value
            self.kosmos.dt.timers[t].save()

            # A delay is required between two timer saves, because of the time required for the interrupt to
            # copy the saved timer value into the dedicated software buffer.
            self.kosmos.dt.pes.delay(delay_ticks=delay_ticks)

            # Subtest 2: Reset, start, then save timer value
            self.kosmos.dt.timers[t].restart()
            self.kosmos.dt.timers[t].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            # Subtest 3: Reset, start, then save timer value
            self.kosmos.dt.timers[t].restart()
            self.kosmos.dt.timers[t].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            # Upload and execute test sequence
            self.kosmos.dt.sequencer.play_sequence()
            # Download time mark
            timemarks = self.kosmos.dt.timers.download()

            # Validate time marks
            self.assertEqual(len(timemarks[t]), 3)
            self.assertEqual(timemarks[t][0], TIMESTAMP_OFFSET)
            self.assertEqual(timemarks[t][1], 0, msg='No offset measured after timer reset instruction was executed')
            self.assertEqual(timemarks[t][2], 0, msg='No offset measured after timer reset instruction was executed')
        # end with

        # Test STOPWATCH timers, individually
        for t in STOPWATCH_TIMERS:
            with self.subTest(timers=t):
                # Subtest 1: Start, then save timer value
                self.kosmos.dt.timers[t].restart()
                self.kosmos.dt.timers[t].save()
                self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

                # Subtest 2: Restart (reset & start) then save timer value
                self.kosmos.dt.timers[t].restart()
                self.kosmos.dt.timers[t].save()
                self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

                # Subtest 3: Restart (reset & start) then save timer value
                self.kosmos.dt.timers[t].restart()
                self.kosmos.dt.timers[t].save()
                self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

                # Upload and execute test sequence
                self.kosmos.dt.sequencer.play_sequence()

                # Download time mark
                timemarks = self.kosmos.dt.timers.download()

                # Validate time marks
                self.assertEqual(sum(len(tm) for tm in timemarks.values()), 3)
                self.assertEqual(len(timemarks[t]), 3)
                self.assertEqual(timemarks[t][0], STOPWATCH_OFFSET)
                self.assertEqual(timemarks[t][1], STOPWATCH_OFFSET)
                self.assertEqual(timemarks[t][2], STOPWATCH_OFFSET)
            # end with
        # end for

        # Test stopwatch timers, consecutively
        with self.subTest(t=STOPWATCH_TIMERS):
            # Subtest 1: Restart (reset & start) then save timer value
            self.kosmos.dt.timers[TIMER.STOPWATCH_1].restart()
            self.kosmos.dt.timers[TIMER.STOPWATCH_1].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            # Subtest 2: Restart (reset & start) then save timer value
            self.kosmos.dt.timers[TIMER.STOPWATCH_2].restart()
            self.kosmos.dt.timers[TIMER.STOPWATCH_2].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            # Subtest 3: Reset, Start then Save timer value
            self.kosmos.dt.timers[TIMER.STOPWATCH_1].stop()
            self.kosmos.dt.timers[TIMER.STOPWATCH_1].reset()
            self.kosmos.dt.timers[TIMER.STOPWATCH_1].start()
            self.kosmos.dt.timers[TIMER.STOPWATCH_1].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            # Subtest 4: Reset, Start then Save timer value
            self.kosmos.dt.timers[TIMER.STOPWATCH_2].stop()
            self.kosmos.dt.timers[TIMER.STOPWATCH_2].reset()
            self.kosmos.dt.timers[TIMER.STOPWATCH_2].start()
            self.kosmos.dt.timers[TIMER.STOPWATCH_2].save()
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            self.kosmos.dt.timers.reset(timers=STOPWATCH_TIMERS)

            # Upload and execute test sequence
            self.kosmos.dt.sequencer.play_sequence()

            # Download time marks
            timemarks = self.kosmos.dt.timers.download()

            # Validate time marks
            self.assertEqual(2, len(timemarks[TIMER.STOPWATCH_1]))
            self.assertEqual(2, len(timemarks[TIMER.STOPWATCH_2]))
            self.assertEqual(timemarks[TIMER.STOPWATCH_1][0], STOPWATCH_OFFSET)
            self.assertEqual(timemarks[TIMER.STOPWATCH_1][1], STOPWATCH_OFFSET)
            self.assertEqual(timemarks[TIMER.STOPWATCH_2][0], STOPWATCH_OFFSET)
            self.assertEqual(timemarks[TIMER.STOPWATCH_2][1], STOPWATCH_OFFSET)
        # end with

        timers = ALL_TIMERS
        with self.subTest(t=timers):
            self.kosmos.dt.timers.restart(STOPWATCH_TIMERS)
            self.kosmos.dt.timers.save(timers)
            self.kosmos.dt.timers.pes_delay_for_timer_interrupt()

            # Upload and execute test sequence
            self.kosmos.dt.sequencer.play_sequence()
            # Download time marks
            timemarks = self.kosmos.dt.timers.download()

            # Validate time marks
            for t in TIMESTAMP_TIMERS:
                self.assertEqual(1, len(timemarks[t]))
                self.assertEqual(timemarks[t][0], self.kosmos.dt.timers[t].get_offset() + 1, msg=t)
            # end for
            for t in STOPWATCH_TIMERS:
                self.assertEqual(1, len(timemarks[t]))
                self.assertEqual(timemarks[t][0], self.kosmos.dt.timers[t].get_offset(), msg=t)
            # end for
        # end with
    # end def test_timer_fixed_offset

    def test_download_timemarks_while_running_test_sequence(self):
        """
        Validate the download of timemarks during the execution of the test sequence
        """
        delays = [1.e-4, 0.005, 0.02]
        count = 10
        for t in TIMER:
            for delay in delays:
                for i in range(count):
                    self.kosmos.dt.timers[t].save()
                    self.kosmos.dt.pes.delay(delay_s=delay)
                # end for
                self.kosmos.dt.sequencer.play_sequence(block=False)

                buffer = []
                while True:
                    status = self.kosmos.dt.sequencer.status()
                    timestamps = self.kosmos.dt.timers[t].download(count=status.pes_timer[t].buffer_count)
                    buffer.extend(timestamps)
                    if status.state != SEQUENCER_STATE_RUNNING:
                        break
                    # end if
                # end while
                status = self.kosmos.dt.sequencer.status()
                self.assertTrue(self.kosmos.dt.sequencer.is_end_of_sequence(status))
                self.assertEqual(0, status.pes_timer[t].buffer_count, msg=status.pes_timer[t])
                self.assertEqual(count, len(buffer))
            # end for
        # end for
    # end def test_download_timemarks_while_running_test_sequence
# end class PesTimersModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
