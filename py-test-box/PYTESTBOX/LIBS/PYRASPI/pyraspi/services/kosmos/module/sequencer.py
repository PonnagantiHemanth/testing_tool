#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.sequencer
:brief: Kosmos SEQUENCER Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep
from time import time

from pylibrary.emulator.emulatorinterfaces import SEQUENCER_TIMEOUT_S
from pylibrary.emulator.emulatorinterfaces import SequencerInterface
from pyraspi.services.kosmos.module.error import KosmosFatalErrorException
from pyraspi.services.globalreset import GlobalReset
from pyraspi.services.kosmos.module.fpga import _gpio_interrupt_event
from pyraspi.services.kosmos.module.module import BufferModuleBaseClass
from pyraspi.services.kosmos.module.module import StatusResetModuleBaseClass
from pyraspi.services.kosmos.module.module import StatusResetModuleSettings
from pyraspi.services.kosmos.module.module import UploadModuleBaseClass
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER_CMD_INIT
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER_CMD_START
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_ERROR
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_IDLE
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_INIT_DONE
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RESET_DONE
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RUNNING
from pyraspi.services.kosmos.protocol.generated.messages import sequencer_state_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import sequencer_status_t


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SequencerError(KosmosFatalErrorException):
    """
     Exception base class for Sequencer errors.
    """
    pass
# end class SequencerError


class SequencerTimeoutError(SequencerError, TimeoutError):
    """
    Exception emitted when no message reply was received after a given timeout.
    """
    pass
# end class SequencerTimeoutError


class SequencerPayloadContentError(SequencerError):
    """
    Exception emitted when an error occurs in `check_instruction_lists` method.
    """
    pass
# end class SequencerPayloadContentError


class SequencerModule(StatusResetModuleBaseClass, SequencerInterface):
    """
    Kosmos SEQUENCER Module class.

    This module is the orchestra leader of the other modules. It does not hold any data by itself.
    Its goal is to supervise the test sequence preparation and execution.
    """
    _offline_mode: bool

    def __init__(self):
        module_settings = StatusResetModuleSettings(
            name=r'SEQUENCER',
            instance_id=None,  # Module is a singleton
            optional=False,
            msg_id=MSG_ID_SEQUENCER,
            status_type=sequencer_status_t,
            msg_cmd_status=MSG_ID_SEQUENCER_CMD_STATUS,
            msg_cmd_reset=MSG_ID_SEQUENCER_CMD_RESET
        )
        super().__init__(module_settings=module_settings)

        # Flag to define the mode used to handle the instructions
        # - True: instructions are sent immediately to the FPGA via the SEQUENCER Module.
        # - False: store the whole list of instructions locally before sending
        self._offline_mode = False
    # end def __init__

    def play_sequence(self, repetition=0, timeout=SEQUENCER_TIMEOUT_S, block=True):
        """
        Configure the FPGA and Microblaze core to receive and play the test sequence
        directed by each module's instructions lists.

        Execution flow:
         1) Check Global Error flag is not raised
         2) Check current SEQUENCER state
         3) Reset SEQUENCER module (propagate reset to other modules too)
         4) Send instructions lists to Microblaze software buffers
         5) Initialise FPGA (fill hardware FIFO from software buffers)
         6) Start SEQUENCER test execution
         7) Wait for end of SEQUENCER execution (optional)

        NB: If the offline mode is enabled, the function returns immediately and keep the instruction buffer untouched.

        For raised exceptions, refer to ``SequencerInterface.wait_end_of_sequence``.

        :param repetition: How many times the scenario is played again - OPTIONAL
        :type repetition: ``int``
        :param timeout: maximum allowed time without any status change, in seconds,
                        defaults to ``SEQUENCER_TIMEOUT_S`` - OPTIONAL
        :type timeout: ``int or float``
        :param block: Wait until the SEQUENCER state changes from RUNNING to IDLE or ERROR. - OPTIONAL
                      Note: `block` parameter must be True if `repetition` parameter is used.
        :type block: ``bool``

        :raise ``AssertionError``: if one of the following conditions is met:
                                    - `block` and `repetition` parameters values are incompatible
                                    - Global Error flag was raised by the Microblaze core
                                    - SEQUENCER state is not clean (refer to `assert_sequencer_state_clean()``)
        :raise ``ValueError``: Invalid repetition argument value
        """
        # Enable the monitoring of the Global Error flag during the execution of this test sequence
        # NB: We could not keep this Pin continuously configured in Input mode as it could prevent us
        # from reconfiguring it in Output mode to trigger a Microblaze reset
        # With the previous implementation (i.e. initialization in FpgaModule.__init__) the 'GPIO Busy' exception
        # could be received when calling GPIO.setup
        GlobalReset.gpio_setup_global_error_signal(callback=_gpio_interrupt_event)

        # Check input parameters
        if repetition < 0:
            raise ValueError(f'repetition parameter must be a positive or null integer: got {repetition}')
        # end if

        # In offline mode, return immediately and keep the instruction buffer untouched
        if self._offline_mode:
            return
        # end if

        # Check method parameter compatibility
        if repetition:
            assert block, '`block` parameter must be True if `repetition` parameter is used'
        # end if

        # Workaround: Ensure sequence start when KBD module is ready (after end of KBD module reset)
        self.dt.pes.insert_pes_wait_kbd_workaround()

        for _ in range(repetition + 1):
            # Check Global Error flag
            assert not self.dt.fpga.is_global_error_flag_raised(), \
                'Global Error flag was raised by the Microblaze core.'

            # Check current Sequencer state
            self.assert_sequencer_state_clean(self.status())

            # Reset Sequencer
            self.reset_sequence()

            # Send instructions lists to Microblaze buffers
            self.send()

            # Initialise Sequencer
            self.init_sequence()

            # Send a GO message to trigger the start of sequence execution by the CPU
            self.start_sequence()

            if block:
                # Wait for end of sequence execution
                self.wait_end_of_sequence(timeout=timeout)
            # end if
        # end for

        # Disable the monitoring of the Global Error flag to avoid 'GPIO Busy' exception at the next pin configuration
        GlobalReset.cleanup_global_error_line()

        self.clear_buffer()
    # end def play_sequence

    def send(self):
        """
        Transfer all local buffers to remote buffers.
        """
        for module in self.dt.flatmap.values():
            if isinstance(module, UploadModuleBaseClass):
                module.send()
            # end if
        # end for
    # end def send

    def clear_buffer(self):
        """
        Clear all local buffers. Remote buffers are not impacted.
        """
        for module in self.dt.flatmap.values():
            if isinstance(module, BufferModuleBaseClass):
                module.clear()
            # end if
        # end for
    # end def clear_buffer

    @property
    def offline_mode(self):
        """
        Get offline mode parameter.

        :return: Flag to enable/disable the automatic sending of instructions to the FPGA
        :rtype: ``bool``
        """
        return self._offline_mode
    # end def property getter offline_mode

    @offline_mode.setter
    def offline_mode(self, offline_mode):
        """
        Set offline mode parameter.

        :param offline_mode: Flag to enable/disable the automatic sending of instructions to the FPGA
        :type offline_mode: ``bool``

        :raise ``AssertionError``: argument type should be bool
        """
        assert isinstance(offline_mode, bool)
        self._offline_mode = offline_mode
    # end def property setter offline_mode

    def assert_sequencer_state_clean(self, status):
        """
        Assert Sequencer state is clean.

        :param status: SequencerModule status
        :type status: ``sequencer_status_t``

        :raise ``AssertionError``: if Sequencer state is not clean
        """
        error_list = self.is_sequencer_state_clean(status)
        assert not error_list, '\n'.join(error_list)
    # end def assert_sequencer_state_clean

    def is_sequencer_state_clean(self, status):
        """
        Check if Sequencer state is clean (FIFOs are empty, Sequencer state is IDLE or RESET)

        :param status: SequencerModule status
        :type status: ``sequencer_status_t``

        :return: clean flag (True if clean) and message string list (details what is not clean)
        :rtype: ``list[str]``
        """
        error_list = []

        # FIXME: this method needs to be reworked
        if status.state not in [SEQUENCER_STATE_IDLE, SEQUENCER_STATE_RESET_DONE]:
            error_list.append(
                f'[{self.name}] Unexpected SEQUENCER status {status.state:#04x}:'
                f'{sequencer_state_e__enumvalues.get(status.state, "?")}.')
        # end if
        if status.pes.fifo_count > 0:
            error_list.append(
                f'[{self.name}] PES FIFO is not empty (contains {status.pes.fifo_count} entries).')
        # end if
        if status.pes.buffer_count > 0:
            error_list.append(
                f'[{self.name}] PES buffer is not empty (contains {status.pes.buffer_count} entries).')
        # end if
        if status.pes_cpu.buffer_count > 0:
            error_list.append(
                f'[{self.name}] CPU Action buffer is not empty (contains {status.pes_cpu.buffer_count} entries).')
        # end if
        if status.kbd_matrix.fifo_count > 0:
            error_list.append(
                f'[{self.name}] KBD_MATRIX FIFO is not empty (contains {status.kbd_matrix.fifo_count} entries)')
        # end if
        if status.kbd_matrix.buffer_count > 0:
            error_list.append(
                f'[{self.name}] KBD_MATRIX buffer is not empty (contains {status.kbd_matrix.buffer_count} entries).')
        # end if
        if status.bas.fifo_count > 0:
            error_list.append(
                f'[{self.name}] BAS FIFO is not empty (contains {status.bas.fifo_count} entries).')
        # end if
        if status.bas.buffer_count > 0:
            error_list.append(
                f'[{self.name}] BAS buffer is not empty (contains {status.bas.buffer_count} entries).')
        # end if
        if status.pes_timer[TIMER.GLOBAL].buffer_count > 0:
            error_list.append(
                f'[{self.name}] TIMESTAMP1 buffer is not empty '
                f'(contains {status.pes_timer[TIMER.GLOBAL].buffer_count} entries).')
        # end if
        if status.pes_timer[TIMER.LOCAL].buffer_count > 0:
            error_list.append(
                f'[{self.name}] TIMESTAMP2 buffer is not empty '
                f'(contains {status.pes_timer[TIMER.LOCAL].buffer_count} entries).')
        # end if
        if status.pes_timer[TIMER.STOPWATCH_1].buffer_count > 0:
            error_list.append(
                f'[{self.name}] STOPWATCH1 buffer is not empty '
                f'(contains {status.pes_timer[TIMER.STOPWATCH_1].buffer_count} entries).')
        # end if
        if status.pes_timer[TIMER.STOPWATCH_2].buffer_count > 0:
            error_list.append(
                f'[{self.name}] STOPWATCH2 buffer is not empty '
                f'(contains {status.pes_timer[TIMER.STOPWATCH_2].buffer_count} entries).')
        # end if

        return error_list
    # end def is_sequencer_state_clean

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``sequencer_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - Unknown Sequencer state value (refer to ``sequencer_state_e__enumvalues``).
                  - any of the other module's status is invalid
        :rtype: ``list[str]``
        """
        # Check Sequencer module's status
        error_list = super().is_status_reply_valid(status)
        if status.state not in sequencer_state_e__enumvalues:
            error_list.append(f'{status.name} Unknown state value: {status.state}.')
        # end if

        # Check each other module's status
        error_list.extend(self.dt.pes.is_status_reply_valid(status.pes))
        error_list.extend(self.dt.pes_cpu.is_status_reply_valid(status.pes_cpu))
        error_list.extend(self.dt.timers.is_status_reply_valid(status.pes_timer))
        if self.dt.kbd_matrix:
            error_list.extend(self.dt.kbd_matrix.is_status_reply_valid(status.kbd_matrix))
        # end if
        if self.dt.bas:
            error_list.extend(self.dt.bas.is_status_reply_valid(status.bas))
        # end if
        for led_spy in self.dt.led_spy:
            error_list.extend(led_spy.is_status_reply_valid(status.led_spy))
        # end for
        for i2c_spy in self.dt.i2c_spy:
            error_list.extend(i2c_spy.is_status_reply_valid(status.i2c_spy))
        # end for

        return error_list
    # end def is_status_reply_valid

    def is_reset_reply_valid(self, status):
        """
        Validate Reset command's Status reply structure: check FIFO & buffer item counts and overrun state.

        :param status: Status structure
        :type status: ``sequencer_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - Unexpected Sequencer state value after reset operation
                  - any of the submodule's status is invalid after reset operation
        :rtype: ``list[str]``
        """
        # Check Sequencer module's status
        error_list = super().is_reset_reply_valid(status)
        if status.state != SEQUENCER_STATE_RESET_DONE:
            error_list.append(f'[{self.name}] State should be RESET_DONE: got {status.state}:'
                              f'{sequencer_state_e__enumvalues.get(status.state, "?")}.')
        # end if

        # Check each sub module's status
        for module in self.dt.flatmap.values():
            if isinstance(module, StatusResetModuleBaseClass) and module is not self.dt.sequencer:
                status = module.status(sanity_checks=False)
                error_list.extend(module.is_reset_reply_valid(status=status))
            # end if
        # end for

        return error_list
    # end def is_reset_reply_valid

    def reset_sequence(self):
        """
        Reset Sequencer modules & other modules controlled by Sequencer.

        Note: To force-reset PES Sequence, independently of the current state, refer to ``reset_module()``.

        :raise ``AssertionError``: if Sequencer state is not ``SEQUENCER_STATE_IDLE`` or ``SEQUENCER_STATE_RESET_DONE``
                                   before resetting PES Sequence.
        """
        # Check initial Sequencer status, before sending the message
        status = self.status()
        assert status.state in [SEQUENCER_STATE_IDLE, SEQUENCER_STATE_RESET_DONE], \
            f'[{self.name}] Sequencer Reset was prevented because Sequencer state is ' \
            f'{status.state}:{sequencer_state_e__enumvalues.get(status.state, "?")}.'

        # Send Sequencer Reset message
        self.reset_module()
    # end def reset_sequence

    def init_sequence(self):
        """
        Trigger the processing of the instructions stored in the modules buffers.

        :raise ``AssertionError``: if at least one of the condition is met:
                                   - Sequencer state is not as expected before and after Sequencer Init.
                                   - PES is not is in soft-reset state.
                                   - any of the other module's status is invalid
        """
        # Check initial Sequencer status, before sending the message
        status = self.status()
        assert status.state == SEQUENCER_STATE_RESET_DONE, \
            f'[{self.name}] Sequencer Init was prevented because Sequencer state is ' \
            f'{status.state}:{sequencer_state_e__enumvalues.get(status.state, "?")}.'

        # Send Sequencer Init message
        status = self.dt.fpga_transport.send_control_message(msg_id=MSG_ID_SEQUENCER, msg_cmd=MSG_ID_SEQUENCER_CMD_INIT)

        # Check current Sequencer status, after sending the message
        error_list = self.is_status_reply_valid(status)

        if not status.state == SEQUENCER_STATE_INIT_DONE:
            error_list.append(
                f'[{self.name}] Sequencer state should be INIT_DONE: got '
                f'{status.state}:{sequencer_state_e__enumvalues.get(status.state, "?")}.')
        # end if
        if not status.pes.soft_reset:
            error_list.append(f'[{self.name}] PES should be in soft-reset state after Sequencer Init.')
        # end if

        assert not error_list, '\n'.join(error_list)
    # end def init_sequence

    def start_sequence(self):
        """
        Trigger the processing of the instructions stored in the modules buffers.

        :raise ``AssertionError``: if one of the following conditions is met:
                                   - Sequencer status message is invalid.
                                   - Sequencer state is not as expected before and after Sequencer start.
        """
        # Check initial Sequencer status, before sending the message
        status = self.status()
        assert status.state == SEQUENCER_STATE_INIT_DONE, \
            f'[{self.name}] Sequencer Start was prevented because Sequencer state is ' \
            f'{status.state}:{sequencer_state_e__enumvalues.get(status.state, "?")}.'

        # Send Sequencer Start message
        status = self.dt.fpga_transport.send_control_message(msg_id=MSG_ID_SEQUENCER,
                                                             msg_cmd=MSG_ID_SEQUENCER_CMD_START)

        # Check current Sequencer status, after sending the message
        error_list = self.is_status_reply_valid(status)

        if status.state not in [SEQUENCER_STATE_RUNNING, SEQUENCER_STATE_ERROR, SEQUENCER_STATE_IDLE]:
            error_list.append(
                f'[{self.name}] Sequencer state should be either RUNNING, ERROR or IDLE. Got '
                f'{status.state}:{sequencer_state_e__enumvalues.get(status.state, "?")}.')
        # end if

        assert not error_list, '\n'.join(error_list)
    # end def start_sequence

    def wait_end_of_sequence(self, timeout=SEQUENCER_TIMEOUT_S):
        # See ``SequencerInterface.wait_end_of_sequence``
        assert timeout > 0, timeout
        time_start = time()
        status_prev = None
        while True:
            time_mark = time()

            # Get Sequencer status
            status = self.status()

            # Check Sequencer status, if new or different from last status query
            if status_prev is None or bytes(status_prev) != bytes(status):
                status_prev = status

                if self.is_end_of_sequence(status):
                    break
                # end if
            # end if

            # Timeout
            if time_mark > time_start + timeout:
                raise SequencerTimeoutError(
                    f'[{self.name}] Timeout while waiting for Sequencer execution ({timeout:.3f} s).\n'
                    f'Sequencer: {status}')
            # end if

            # Wait before next Sequencer status retrieval
            sleep(0.01)  # 10 ms
        # end while

        # Check other module's status: FIFO and buffer should be empty, without underrun or overrun
        error_list = []
        # Skip PES state check
        error_list.extend(super(self.dt.pes.__class__, self.dt.pes).is_reset_reply_valid(status.pes))
        error_list.extend(self.dt.pes_cpu.is_reset_reply_valid(status.pes_cpu))
        if self.dt.kbd_matrix:
            error_list.extend(self.dt.kbd_matrix.is_reset_reply_valid(status.kbd_matrix))
        # end if
        if self.dt.kbd_gtech:
            gtech_status = self.dt.kbd_gtech.status()
            error_list.extend(self.dt.kbd_gtech.is_reset_reply_valid(gtech_status))
        # end if
        if self.dt.bas:
            error_list.extend(self.dt.bas.is_reset_reply_valid(status.bas))
        # end if
    # end def wait_end_of_sequence

    def is_end_of_sequence(self, status=None):
        """
        Check Sequencer status and return when test sequence is done or presents errors.

        :param status: Status structure, defaults to None (fetch new Sequencer Status message) - OPTIONAL
        :type status: ``sequencer_status_t``

        :return: True if Test Sequence has ended, False otherwise
        :rtype: ``bool``

        :raise ``SequencerError``: if Sequencer state value is ``SEQUENCER_STATE_ERROR`` or is unexpected
        """
        if status is None:
            status = self.status()
        # end if

        if status.state == SEQUENCER_STATE_RUNNING:
            return False
        elif status.state == SEQUENCER_STATE_IDLE:
            return True
        elif status.state == SEQUENCER_STATE_ERROR:
            raise SequencerError(f'[{self.name}] state ERROR.\n'
                                 f'Status: {status}')
        else:
            raise SequencerError(f'[{self.name}] state is unexpected: '
                                 f'{status.state}:{sequencer_state_e__enumvalues.get(status.state, "?")}.\n'
                                 f'Status: {status}')
        # end if
    # end def is_end_of_sequence
# end class SequencerModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
