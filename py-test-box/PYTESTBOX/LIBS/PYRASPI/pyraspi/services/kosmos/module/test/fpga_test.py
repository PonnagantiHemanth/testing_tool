#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.fpga_test
:brief: Kosmos FPGA Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyraspi.services.globalreset import GlobalReset
from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.fpga import _gpio_interrupt_event
from pyraspi.services.kosmos.module.pesevents import PES_ACTION_EVENT_NOP
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST_CMD_ERROR_SIGNAL
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_SUCCESS
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RESET_DONE
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RUNNING
from pyraspi.services.kosmos.protocol.generated.messages import msg_reply_return_code_e__enumvalues


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@require_kosmos_device(DeviceName.FPGA)
class FpgaModuleTestCase(AbstractTestClass.ModuleInterfaceTestCase):
    """
    Kosmos FPGA Module Test Class
    """

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``FpgaModule``
        """
        return cls.kosmos.dt.fpga
    # end def _get_module_under_test

    def test_status(self):
        """
        Validate ``FpgaModule.status()`` method.
        """
        self.kosmos.dt.fpga.status()
    # end def test_status

    def test_reset_module(self):
        """
        Validate ``FpgaModule.reset_module()`` method.
        """
        self.kosmos.dt.fpga.reset_module()
    # end def test_reset_module

    def test_soft_reset_microblaze(self):
        """
        Validate ``FpgaModule.soft_reset_microblaze()`` method.
        """
        self.kosmos.dt.fpga.soft_reset_microblaze()
    # end def test_soft_reset_microblaze

    def test_global_go_signal_simple(self):
        """
        Validates ``PesModule.wait_go_signal()`` and ``FpgaModule.pulse_global_go_line()`` methods.
        """
        # Define test sequence
        timer_id = TIMER.LOCAL
        self.kosmos.dt.pes.wait_go_signal()
        self.kosmos.dt.timers[timer_id].reset()

        self.kosmos.dt.pes.wait_go_signal()
        self.kosmos.dt.timers[timer_id].save()

        # Upload and start executing test sequence
        self.kosmos.dt.sequencer.play_sequence(block=False)

        # Generate expected Go signal stimuli
        # Toggle Go signal twice with a pause
        delay = 0.1  # second
        self.kosmos.dt.fpga.pulse_global_go_line()
        sleep(delay)
        self.kosmos.dt.fpga.pulse_global_go_line()

        # Wait for end of sequence execution
        self.kosmos.dt.sequencer.wait_end_of_sequence(timeout=1)

        # Check Timer status
        timer_status = self.kosmos.dt.timers[timer_id].status()
        self.assertEqual(1, timer_status.buffer_count, msg=timer_status)

        # Download time mark
        timemarks = self.kosmos.dt.timers[timer_id].download()

        # Validate time marks
        self.assertEqual(1, len(timemarks))
        self.assertAlmostEqual(timemarks[0] / FPGA_CURRENT_CLOCK_FREQ, delay, delta=0.01)
    # end def test_global_go_signal_simple

    def test_global_go_signal_loop(self):
        """
        Validates wait_go_signal() and gpio_send_go_signal() methods, in loops of increasing frequency.
        """
        timer_id = TIMER.LOCAL
        repetition = 3
        delays = [1.e-1, 1.e-2, 1.e-3, 1.e-4, 1.e-5]  # second

        # Define test sequence
        for delay in delays:
            with self.subTest(delay=delay):
                for _ in range(repetition):
                    self.kosmos.dt.pes.wait_go_signal()
                    self.kosmos.dt.timers[timer_id].reset()

                    self.kosmos.dt.pes.wait_go_signal()
                    self.kosmos.dt.timers[timer_id].save()
                # end for

                # Upload and start executing test sequence
                self.kosmos.dt.sequencer.play_sequence(block=False)
                status = self.kosmos.dt.sequencer.status()
                self.assertEqual(status.state, SEQUENCER_STATE_RUNNING,
                                 msg=f'Test sequence should be running. Sequencer status is {status}')

                # Generate expected Go signal stimuli
                for _ in range(repetition):
                    # Toggle Go signal twice within a given period
                    self.kosmos.dt.fpga.pulse_global_go_line()
                    sleep(delay)
                    self.kosmos.dt.fpga.pulse_global_go_line()
                    sleep(0.01)  # give time to timer interrupt to save timestamp
                # end for

                # Validate test sequence is finished
                status = self.kosmos.dt.sequencer.status()
                self.assertTrue(self.kosmos.dt.sequencer.is_end_of_sequence(status=status), msg=status)

                # Download time mark
                timemarks = self.kosmos.dt.timers.download()

                # Validate time marks
                self.assertEqual(sum(len(tm) for tm in timemarks.values()), repetition)
                self.assertEqual(len(timemarks[timer_id]), repetition)
                for i in range(repetition):
                    # The following acceptance criteria (delta) was set after the maximum measured delta across the
                    # whole test case.
                    # Consequently, this test will also serve as RPi OS regression test. If the CPU is overloaded,
                    # the GPIO toggling timings will not be respected and the test will fail.
                    self.assertAlmostEqual(timemarks[timer_id][i] / FPGA_CURRENT_CLOCK_FREQ, delay, delta=1.5e-3,
                                           msg=f'Issue with timer {timer_id.name}, capture number {i}.')
                # end for
            # end with
        # end for
    # end def test_global_go_signal_loop

    def test_global_error_signal_as_input(self):
        """
        Validates _gpio_interrupt_event() and is_global_error_flag_raised() methods.
        """
        # Enable the monitoring of the Global Error flag during the execution of this test sequence
        GlobalReset.gpio_setup_global_error_signal(callback=_gpio_interrupt_event)

        # Send special test message, dedicated to trigger the Error signal from FPGA to RPi.
        status = self.kosmos.dt.fpga_transport.send_control_message(msg_id=MSG_ID_TEST,
                                                                    msg_cmd=MSG_ID_TEST_CMD_ERROR_SIGNAL)
        self.assertEqual(status.return_code, MSG_REPLY_RETURN_CODE_SUCCESS,
                         msg=f'Received FPGA status {msg_reply_return_code_e__enumvalues[status.return_code]}.')

        # Add a 3ms empirical delay to let the error propagate to the PI
        sleep(.003)

        # Disable the monitoring of the Global Error flag to avoid 'GPIO Busy' exception at the next pin configuration
        GlobalReset.cleanup_global_error_line()
        # Validate the Error Flag has been raised
        self.assertTrue(self.kosmos.dt.fpga.is_global_error_flag_raised())

        # Validate a test sequence cannot be sent when the Error Flag is raised
        with self.assertRaises(AssertionError):
            self.kosmos.dt.sequencer.play_sequence()
        # end with

        # Reset Error Flag before exiting test
        self.kosmos.dt.fpga.reset_global_error_flag()

        # Validate a test sequence can be sent if the Error Flag was set then reset
        self.kosmos.dt.pes.execute(action=PES_ACTION_EVENT_NOP)
        self.kosmos.dt.sequencer.play_sequence(timeout=1)
    # end def test_global_error_signal_as_input

    def test_global_error_signal_as_output(self):
        """
        Validates soft_reset_microblaze() and raise_global_error_flag() methods.
        """
        # Setup initial condition: send a test sequence to fill the FPGA FIFOs
        self.kosmos.dt.pes.wait_go_signal()  # Wait indefinitely: Go signal will not be raised for this test
        self.kosmos.dt.sequencer.play_sequence(block=False)

        # Validate initial condition
        status = self.kosmos.dt.sequencer.status()
        self.assertEqual(status.state, SEQUENCER_STATE_RUNNING,
                         msg=f'Test sequence should be running. Sequencer status is {status}')

        # Raise Global Error signal and wait for Microblaze to reboot
        self.kosmos.dt.fpga.soft_reset_microblaze()

        # Validate that the Microblaze core was reset
        status = self.kosmos.dt.sequencer.status()
        self.assertEqual(status.state, SEQUENCER_STATE_RESET_DONE,
                         msg=f'PES should be reset. Sequencer status is {status}')
    # end def test_global_error_signal_as_output
# end class FpgaModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
