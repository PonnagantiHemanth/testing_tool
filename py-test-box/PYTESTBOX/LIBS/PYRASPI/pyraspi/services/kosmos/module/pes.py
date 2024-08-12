#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.pes
:brief: Kosmos PES Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from enum import IntFlag
from typing import Iterable
from typing import Union
from warnings import warn

from math import ceil
from math import floor
from math import log2

from pylibrary.emulator.emulatorinterfaces import EventInterface
from pyraspi.services.kosmos.module.module import ConsumerModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleSettings
from pyraspi.services.kosmos.module.pesevents import PES_ACTION_EVENT_NOP
from pyraspi.services.kosmos.module.pesevents import PES_RESUME_EVENT_NOP
from pyraspi.services.kosmos.module.pesevents import PesActionEvent
from pyraspi.services.kosmos.module.pesevents import PesActionEventBase
from pyraspi.services.kosmos.module.pesevents import PesEventMapInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesEvents
from pyraspi.services.kosmos.module.pesevents import PesResumeEvent
from pyraspi.services.kosmos.module.pesevents import PesResumeEventBase
from pyraspi.services.kosmos.module.pesevents import get_pes_action_events_combined_bitmask
from pyraspi.services.kosmos.module.pesevents import get_pes_resume_events_combined_bitmask
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CMD_WRITE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CMD_WRITE_MAX
from pyraspi.services.kosmos.protocol.generated.messages import PES_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import PES_FIFO_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_ENUM_MAX_VALUE
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_NOP
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_RESERVED_BITS
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_RESET_LOCAL_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_RESET_STOPWATCH_1_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_SAVE_LOCAL_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_SAVE_STOPWATCH_1_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_SAVE_STOPWATCH_2_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_STOPWATCH_1_GO
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_STOPWATCH_1_STOP
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_STOPWATCH_2_GO
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_STOPWATCH_2_STOP
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_EXECUTE
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_MARKER
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_SUBDELAY_NIBBLE_05_TICKS
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_SUBDELAY_NIBBLE_10_TICKS
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_SUBDELAY_NIBBLE_90_TICKS
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_WAIT
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_delay_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_execute_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_field_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_marker_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_subdelay_opcode_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_subdelay_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_wait_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_isa_opcode_delay_nibble_ns_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import pes_status_t

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
pes_instruction_types = (pes_instruction_t,
                         pes_instruction_field_t,
                         pes_instruction_delay_t,
                         pes_instruction_execute_t,
                         pes_instruction_marker_t,
                         pes_instruction_subdelay_t,
                         pes_instruction_wait_t)


class PES_MARKER(IntFlag):
    """
    PES Markers OP CODE

    Enumeration class matching auto-generated PES markers:
        `pyraspi.services.kosmos.protocol.generated.messages.pes_isa_marker_operation_e__enumvalues`

    Specification: Refer to section '3.4.MARKER Instruction' of PES specs document
        https://docs.google.com/document/d/1FzrnFcy_0Fy4edVqQQXLtfVlnJQbWFOtY-f4cpIdCNM/edit#heading=h.bbgbfv8m8gig
    """
    NOP                         = PES_ISA_MARKER_OP_NOP
    SAVE_GLOBAL_TIME_MARK       = PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK
    SAVE_LOCAL_TIME_MARK        = PES_ISA_MARKER_OP_SAVE_LOCAL_TIME_MARK
    SAVE_STOPWATCH_1_TIME_MARK  = PES_ISA_MARKER_OP_SAVE_STOPWATCH_1_TIME_MARK
    SAVE_STOPWATCH_2_TIME_MARK  = PES_ISA_MARKER_OP_SAVE_STOPWATCH_2_TIME_MARK
    RESET_LOCAL_TIME_MARK       = PES_ISA_MARKER_OP_RESET_LOCAL_TIME_MARK
    RESET_STOPWATCH_1_TIME_MARK = PES_ISA_MARKER_OP_RESET_STOPWATCH_1_TIME_MARK
    RESET_STOPWATCH_2_TIME_MARK = PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK
    STOPWATCH_1_GO              = PES_ISA_MARKER_OP_STOPWATCH_1_GO
    STOPWATCH_2_GO              = PES_ISA_MARKER_OP_STOPWATCH_2_GO
    STOPWATCH_1_STOP            = PES_ISA_MARKER_OP_STOPWATCH_1_STOP
    STOPWATCH_2_STOP            = PES_ISA_MARKER_OP_STOPWATCH_2_STOP
    # RESERVED_BITS             = PES_ISA_MARKER_OP_RESERVED_BITS
# end class PES_MARKER

@dataclass(frozen=True)
class PesCoreActionEvent(PesEventMapInterface):
    """
    PES Action Events for PES core module
    """
    NOP_EVENT: PesActionEvent = None
# end class PesCoreActionEvent


@dataclass(frozen=True)
class PesCoreResumeEvent(PesEventMapInterface):
    """
    PES Resume Events for PES core module
    """
    NOP_EVENT: PesResumeEvent = None
    GO_RPI: PesResumeEvent = None
# end class PesCoreResumeEvent


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class PesModule(ConsumerModuleBaseClass, EventInterface, PesEventModuleInterface):
    """
    Kosmos PES module class. PES stands for "Programmable Event Sequencer".

    Specifications: 'Programmable Event Sequencer. System Level Specification. By Maxim Vlassov.'
        https://docs.google.com/document/d/1FzrnFcy_0Fy4edVqQQXLtfVlnJQbWFOtY-f4cpIdCNM
    """

    # PES Event maps related to the current module
    action_event = PesCoreActionEvent
    resume_event = PesCoreResumeEvent

    # PES Events manager
    events: PesEvents = None

    def __init__(self, fpga_clock_period_ns):
        """
        :param fpga_clock_period_ns: FPGA clock period expressed in nanoseconds
        :type fpga_clock_period_ns: ``float``
        """
        module_settings = ConsumerModuleSettings(
            name=r'PES',
            instance_id=None,  # Module is a singleton
            optional=False,
            msg_id=MSG_ID_PES,
            buffer_size=(PES_BUFFER_SIZE - 1),
            fifo_size=(PES_FIFO_SIZE - 1),
            status_type=pes_status_t,
            msg_cmd_status=MSG_ID_PES_CMD_STATUS,
            msg_cmd_reset=MSG_ID_PES_CMD_RESET,
            data_type=pes_instruction_types,
            msg_cmd_write_one=MSG_ID_PES_CMD_WRITE_1,
            msg_cmd_write_max=MSG_ID_PES_CMD_WRITE_MAX,
            msg_payload_name=r'pes'
        )
        super().__init__(module_settings=module_settings)

        self._fpga_clock_period_ns = fpga_clock_period_ns
    # end def __init__

    def post_init_device_tree(self):
        """
        Action to be done after Device Tree has been initialized.
        """
        self.events = PesEvents(dt=self._dt)
    # end def post_init_device_tree

    @staticmethod
    def _set_message_payload(payload, payload_index, data):
        """
        Override base class method to set the MessageFrame payload, depending on data type.

        :param payload: Ctypes Array
        :type payload: ``ctypes.Array``
        :param payload_index: index of payload array
        :type payload_index: ``int``
        :param data: instruction data to be set in the payload
        :type data: ``Union[pes_instruction_types]``

        :raise ``AssertionError``: Invalid payload type
        :raise ``TypeError``: Invalid instruction data type
        """
        assert isinstance(payload[payload_index], pes_instruction_t), payload[payload_index]
        if isinstance(data, pes_instruction_t):
            payload[payload_index] = data
        elif isinstance(data, pes_instruction_field_t):
            payload[payload_index].field = data
        elif isinstance(data, pes_instruction_delay_t):
            payload[payload_index].delay = data
        elif isinstance(data, pes_instruction_execute_t):
            payload[payload_index].execute = data
        elif isinstance(data, pes_instruction_marker_t):
            payload[payload_index].marker = data
        elif isinstance(data, pes_instruction_subdelay_t):
            payload[payload_index].subdelay = data
        elif isinstance(data, pes_instruction_wait_t):
            payload[payload_index].wait = data
        else:
            raise TypeError(f'Instruction {data} type should be in {pes_instruction_types}.')
        # end if
    # end def _set_message_payload

    def execute(self, action):
        """
        Add a PES:EXEC instruction to the local PES instruction buffer.

        :param action: Action(s) to be executed.
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase]``
        """
        self.append(self.get_execute_instruction(action=action))
    # end def execute

    def wait(self, action):
        """
        Add a PES:WAIT instruction to the local PES instruction buffer.

        :param action: Trigger(s) to be awaited for.
        :type action: ``PesResumeEventBase or Iterable[PesResumeEventBase]``
        """
        self.append(self.get_wait_instruction(action=action))
    # end def wait

    def delay(self, delay_s=None, delay_ns=None, delay_ticks=None, action=PES_ACTION_EVENT_NOP):
        """
        Add a list of PES:DELAY, PES:SUBDELAY and/or PES:EXEC instructions to the local PES instruction buffer.

        Note that the delay duration can be expressed in seconds, nanoseconds or clock tick units.
        Only one delay argument can be used at a time.

        :param delay_s: Delay duration expressed in seconds - OPTIONAL
        :type delay_s: ``float or int or None``
        :param delay_ns: Delay duration expressed in nanoseconds - OPTIONAL
        :type delay_ns: ``float or int or None``
        :param delay_ticks: Delay duration expressed in FPGA clock ticks - OPTIONAL
        :type delay_ticks: ``int or None``
        :param action: Action(s) to be executed at the end of the delay - OPTIONAL
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase] or None``
        """
        self.extend(self.get_delay_instructions(delay_s=delay_s, delay_ns=delay_ns,
                                                delay_ticks=delay_ticks, action=action))
    # end def delay

    def marker(self, action):
        """
        Add a PES:MARKER instruction to the local PES instruction buffer.

        :param action: Marker(s) to be triggered. Refer to ``pes_isa_marker_operation_e__enumvalues``.
        :type action: ``pes_isa_marker_operation_e or int``
        """
        self.append(self.get_marker_instruction(action=action))
    # end def marker

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``pes_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - PES BAD OPCODE state is set: an invalid PES instruction was executed by PES engine.
        :rtype: ``list[str]``
        """
        error_list = super().is_status_reply_valid(status)

        if status.bad_opcode:
            error_list.append(f'[{self.name}] BAD OPCODE state is set.')
        # end if

        return error_list
    # end def is_status_reply_valid

    def is_reset_reply_valid(self, status):
        """
        Validate Reset command's Status reply structure.

        :param status: Status structure
        :type status: ``pes_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - PES module is not in soft-reset state
        :rtype: ``list[str]``
        """
        error_list = super().is_reset_reply_valid(status)

        if not status.soft_reset:
            error_list.append(f'[{self.name}] module should be in soft-reset state.')
        # end if

        return error_list
    # end def is_reset_reply_valid

    @staticmethod
    def get_execute_instruction(action=PES_ACTION_EVENT_NOP):
        """
        Return a PES:EXEC instruction, with opcode and operand fields set.

        :param action: Action(s) to be executed - OPTIONAL
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase]``

        :return: PES:EXEC instruction, with opcode and operand fields set.
        :rtype: ``pes_instruction_execute_t``
        """
        bitmask = get_pes_action_events_combined_bitmask(action)
        return pes_instruction_execute_t(opcode=PES_OPCODE_EXECUTE, action_event=bitmask)
    # end def get_execute_instruction

    @staticmethod
    def get_wait_instruction(action=PES_RESUME_EVENT_NOP):
        """
        Return a PES:WAIT instruction, with opcode and operand fields set.

        :param action: Trigger(s) to be awaited for - OPTIONAL
        :type action: ``PesResumeEventBase or Iterable[PesResumeEventBase]``

        :return: PES:WAIT instruction, with opcode and operand fields set.
        :rtype: ``pes_instruction_wait_t``
        """
        bitmask = get_pes_resume_events_combined_bitmask(action)
        return pes_instruction_wait_t(opcode=PES_OPCODE_WAIT, resume_event=bitmask)
    # end def get_wait_instruction

    def get_delay_instructions(self, delay_s=None, delay_ns=None, delay_ticks=None, action=PES_ACTION_EVENT_NOP):
        """
        Return a list of PES:DELAY, PES:SUBDELAY and/or PES:EXEC instructions, with opcode and operand fields set.

        Note 1: The delay duration can be expressed in seconds, nanoseconds or clock tick units.
                Only one delay argument can be used at a time.

        Note 2: If the delay duration is not an exact multiple of the FPGA clock period, a warning will be raised.
                Refer to ``PesSequence.roundup_delay_ns_to_clock_period()``
                and ``PesSequence.roundup_delay_s_to_clock_period()`` methods to round up the delay duration before
                calling this method.


        :param delay_s: Delay duration expressed in seconds - OPTIONAL
        :type delay_s: ``float or int or None``
        :param delay_ns: Delay duration expressed in nanoseconds - OPTIONAL
        :type delay_ns: ``float or int or None``
        :param delay_ticks: Delay duration expressed in FPGA clock ticks - OPTIONAL
        :type delay_ticks: ``int or None``
        :param action: Action(s) to be executed at the end of the delay. - OPTIONAL
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase]``

        :return: list of PES:DELAY, PES:SUBDELAY and/or PES:EXEC instructions, with opcode and operand fields set.
        :rtype: ``list[pes_instruction_delay_t or pes_instruction_subdelay_t or pes_instruction_execute_t]``

        :raise ``AssertionError``: if less or more than one delay argument is used at a time.
        """
        assert sum([delay_s is None, delay_ns is None, delay_ticks is None]) == 2, \
            f'Only one delay argument can be used at a time.'

        if delay_ticks is None:
            if delay_s is not None:
                # Convert seconds to nanoseconds
                delay_ns = round(delay_s * 10 ** 9)
            # end if
            instructions, remaining_ns = self._get_delay_instructions_from_duration_ns(delay_ns=delay_ns, action=action)

            # Check if the commanded delay duration could not be entirely encoded into delay instructions.
            if remaining_ns > 0:
                warn(f'PES DELAY: Effective delay is shorter by {remaining_ns} ns.\n'
                     f'Target duration was {delay_ns} ns.\n'
                     f'The smallest implementable duration increment is {self._fpga_clock_period_ns} ns.')
            # end if
        else:
            instructions = self._get_delay_instructions_from_ticks(ticks=delay_ticks, action=action)
        # end if

        return instructions
    # end def get_delay_instructions

    @staticmethod
    def get_marker_instruction(action=PES_ISA_MARKER_OP_NOP):
        """
        Return a PES:MARKER instruction, with opcode and operand fields set.

        :param action: Marker(s) to be triggered. Refer to ``pes_isa_marker_operation_e__enumvalues``,
                       defaults to `PES_ISA_MARKER_OP_NOP` - OPTIONAL
        :type action: ``pes_isa_marker_operation_e or int``

        :return: PES:MARKER instruction, with opcode and operand fields set.
        :rtype: ``pes_instruction_marker_t``

        :raise ``AssertionError``: invalid action value
        """
        assert PES_ISA_MARKER_OP_NOP <= action <= PES_ISA_MARKER_OP_ENUM_MAX_VALUE, \
            f'Invalid PES:MARKER action value {action:#x}.'
        assert not action & PES_ISA_MARKER_OP_RESERVED_BITS, \
            f'Invalid PES:MARKER action value {action:#x}: uses reserved bits ' \
            f'{action & PES_ISA_MARKER_OP_RESERVED_BITS:#x}.'

        pes_marker = pes_instruction_marker_t(opcode=PES_OPCODE_MARKER)
        pes_marker.operand.raw = action
        return pes_marker
    # end def get_marker_instruction

    def get_execution_duration_ns(self, instructions):
        """
        Return PES instructions execution duration, in nanoseconds.

        :param instructions: list of PES instructions
        :type instructions: ``list[pes_instruction_delay_t or pes_instruction_subdelay_t or
                                  pes_instruction_execute_t or pes_instruction_marker_t]``

        :return: PES instructions execution duration, in nanoseconds
        :rtype: ``int``
        """
        return self.get_execution_duration_ticks(instructions) * self._fpga_clock_period_ns
    # end def get_execution_duration_ns

    @staticmethod
    def get_execution_duration_ticks(instructions):
        """
        Return the PES instructions execution duration, in tick count.

        :param instructions: list of PES instructions
        :type instructions: ``list[pes_instruction_delay_t or pes_instruction_subdelay_t or
                                  pes_instruction_execute_t or pes_instruction_marker_t]``

        :return: PES instructions execution duration, in tick count
        :rtype: ``int``

        :raise ``TypeError``: Unexpected ``instruction`` type
        """
        ticks = 0
        for instruction in instructions:
            if isinstance(instruction, pes_instruction_delay_t):
                ticks += PesModule._get_execution_duration_ticks_from_pes_delay_instruction(instruction)
            elif isinstance(instruction, pes_instruction_subdelay_t):
                ticks += PesModule._get_execution_duration_ticks_from_pes_subdelay_instruction(instruction)
            elif isinstance(instruction, (pes_instruction_execute_t, pes_instruction_marker_t)):
                ticks += 1
            else:
                raise TypeError(instruction)
            # end if
        # end for
        return ticks
    # end def get_execution_duration_ticks

    def _get_delay_instructions_from_duration_ns(self, delay_ns, action=PES_ACTION_EVENT_NOP):
        """
        Convert a delay duration into a list of PES instructions.

        Relevant PES instructions:
        | PES INSTRUCTION  | execution duration in ticks |
        |------------------|-----------------------------|
        | PES NOP          |  1                          |
        | PES SUBDELAY_05  |  5                          |
        | PES SUBDELAY_10  | 10                          |
        | PES SUBDELAY_20  | 20                          |
        | PES SUBDELAY_30  | 30                          |
        | PES SUBDELAY_40  | 40                          |
        | PES SUBDELAY_50  | 50                          |
        | PES SUBDELAY_60  | 60                          |
        | PES SUBDELAY_70  | 70                          |
        | PES SUBDELAY_80  | 80                          |
        | PES SUBDELAY_90  | 90                          |
        | PES DELAY        | 100 to 0xFFE*100 = 409400   |

        :param delay_ns: Number of nanoseconds to convert
        :type delay_ns: ``float or int``
        :param action: Action(s) to be executed at the end of the delay. - OPTIONAL
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase]``

        :return: List of PES instructions, and remaining tick count
        :rtype: ``tuple[list[pes_instruction_delay_t or pes_instruction_subdelay_t or pes_instruction_execute_t],
                        int]``

       :raise ``AssertionError``: If delay duration is shorter than one FPGA clock tick.
        """
        assert delay_ns >= self._fpga_clock_period_ns, \
            f'Delay duration ({delay_ns} ns) must be at least one clock period long ' \
            f'({self._fpga_clock_period_ns})'

        ticks = floor(delay_ns / self._fpga_clock_period_ns)
        remaining_delay_ns = delay_ns % self._fpga_clock_period_ns
        instructions = self._get_delay_instructions_from_ticks(ticks=ticks, action=action)
        return instructions, remaining_delay_ns
    # end def _get_delay_instructions_from_duration_ns

    @staticmethod
    def _get_delay_instructions_from_ticks(ticks, action=PES_ACTION_EVENT_NOP):
        """
        Convert a clock tick duration into a list of PES instructions.

        Relevant PES instructions:
        | PES INSTRUCTION  | execution duration in ticks |
        |------------------|-----------------------------|
        | PES NOP          |  1                          |
        | PES SUBDELAY_05  |  5                          |
        | PES SUBDELAY_10  | 10                          |
        | PES SUBDELAY_20  | 20                          |
        | PES SUBDELAY_30  | 30                          |
        | PES SUBDELAY_40  | 40                          |
        | PES SUBDELAY_50  | 50                          |
        | PES SUBDELAY_60  | 60                          |
        | PES SUBDELAY_70  | 70                          |
        | PES SUBDELAY_80  | 80                          |
        | PES SUBDELAY_90  | 90                          |
        | PES DELAY        | 100 to 0xFFE*100 = 409400   |

        :param ticks: Number of delay ticks to convert into PES instructions
        :type ticks: ``int``
        :param action: Action to be executed at the end of the delay. - OPTIONAL
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase]``

        :return: List of PES instructions
        :rtype: ``list[pes_instruction_delay_t or pes_instruction_subdelay_t or pes_instruction_execute_t]``

        :raise ``AssertionError``: invalid `tick` argument value
        """
        assert ticks >= 1 and isinstance(ticks, int), \
            f'Tick count must be a strictly positive integer, got ticks={ticks}.'

        remaining_ticks = ticks
        instructions = []

        # Each PES DELAY instruction lasts between 100 and 409400 clock cycles, depending on operand value
        if remaining_ticks >= 100:
            pes_delay_instructions, remaining_ticks = \
                PesModule._get_pes_delay_instructions_from_ticks(ticks=remaining_ticks)
            instructions.extend(pes_delay_instructions)
        # end if

        # Each PES SUBDELAY instruction lasts between 5 and 90 clock cycles, depending on operand value
        if remaining_ticks >= 5:
            pes_subdelay_instructions, remaining_ticks = \
                PesModule._get_pes_subdelay_instructions_from_ticks(ticks=remaining_ticks)
            instructions.extend(pes_subdelay_instructions)
        # end if

        # Each PES EXEC:NOP instruction lasts exactly 1 clock cycle
        if remaining_ticks >= 1:
            pes_exec_nop_instructions, remaining_ticks = \
                PesModule._get_pes_exec_nop_instructions_from_ticks(ticks=remaining_ticks)
            instructions.extend(pes_exec_nop_instructions)
        # end if

        # Sanity checks
        assert remaining_ticks == 0, remaining_ticks

        # Set last instruction action event field
        bitmask = get_pes_action_events_combined_bitmask(action)
        instructions[-1].action_event = bitmask

        return instructions
    # end def _get_delay_instructions_from_ticks

    @staticmethod
    def _get_pes_delay_instructions_from_ticks(ticks):
        """
        Convert a clock tick duration into a list of PES:DELAY instructions.

        PES:DELAY instruction specifications:
          - The tick count value is encoded as a 16-bit floating point number (WARNING: POSSIBLE LOSS OF PRECISION)
            having a strictly positive mantissa and a positive or null exponential part.
          - Mantissa occupies 12 bits, whereas the exponent is coded in 4 bits.
          - Mantissa value can only range from 0x001 to 0xFFE.
          - Exponent value can only range from 0x0 to 0xF.
          - tick count is `Mantissa * 2^Exponent`.
          - Exponent is `log2(delay_us / Mantissa)`
          - Mantissa is `tick_count / 2^Exponent`
          - Counter clock frequency = FPGA clock frequency / 100

        :param ticks: Number of delay ticks to convert into PES:DELAY instructions
        :type ticks: ``int``

        :return: List of PES:DELAY instructions, and remaining tick count
        :rtype: ``(list[pes_instruction_delay_t], int)``

        :raise ``AssertionError``: invalid argument value
        """
        assert isinstance(ticks, int) and ticks >= 0, ticks

        exponent_max = 0xF
        mantissa_max = 0xFFE
        prescaler_ticks = 100  # 1 delay counter tick every 100 FPGA clock ticks
        remaining_ticks = ticks
        instructions = []

        while remaining_ticks >= prescaler_ticks:
            timer_tick = remaining_ticks // prescaler_ticks
            if timer_tick > mantissa_max:
                exponent = min(floor(log2(timer_tick / mantissa_max)), exponent_max)
            else:
                exponent = 0
            # end if
            mantissa = min((timer_tick >> exponent), mantissa_max)
            assert 1 <= mantissa <= mantissa_max, mantissa
            pes_delay = pes_instruction_delay_t()
            pes_delay.opcode.exponent = exponent
            pes_delay.opcode.mantissa = mantissa
            instructions.append(pes_delay)
            remaining_ticks -= PesModule._get_execution_duration_ticks_from_pes_delay_instruction(pes_delay)
        # end while

        return instructions, remaining_ticks
    # end def _get_pes_delay_instructions_from_ticks

    @staticmethod
    def _get_pes_subdelay_instructions_from_ticks(ticks):
        """
        Convert a tick duration into a list of PES:SUBDELAY instructions.

        PES:SUBDELAY instructions:
          - set of 10 dedicated fixed-delay instructions: 5, 10, 20, 30, 40, 50, 60, 70, 80, 90 ticks

        :param ticks: Number of delay ticks to convert into PES:SUBDELAY instructions
        :type ticks: ``int``

        :return: List of PES:SUBDELAY instructions, and remaining tick count
        :rtype: ``(list[pes_instruction_subdelay_t], int)``

        :raise ``AssertionError``: invalid argument value
        """
        assert isinstance(ticks, int) and ticks >= 0, ticks

        instructions = []
        remaining_ticks = ticks

        # SUBDELAY: 10 to 90 ticks
        while remaining_ticks >= 10:
            opcode_index = min(remaining_ticks // 10, 9)
            nibble = PES_OPCODE_SUBDELAY_NIBBLE_05_TICKS + opcode_index
            assert PES_OPCODE_SUBDELAY_NIBBLE_10_TICKS <= nibble <= PES_OPCODE_SUBDELAY_NIBBLE_90_TICKS, nibble
            opcode = pes_instruction_subdelay_opcode_t(nibble=nibble)
            instructions.append(pes_instruction_subdelay_t(opcode=opcode))
            remaining_ticks -= opcode_index * 10
        # end while

        # SUBDELAY: 5 ticks
        if remaining_ticks >= 5:
            opcode = pes_instruction_subdelay_opcode_t(nibble=PES_OPCODE_SUBDELAY_NIBBLE_05_TICKS)
            instructions.append(pes_instruction_subdelay_t(opcode=opcode))
            remaining_ticks -= 5
        # end if
        return instructions, remaining_ticks
    # end def _get_pes_subdelay_instructions_from_ticks

    @staticmethod
    def _get_pes_exec_nop_instructions_from_ticks(ticks):
        """
        Convert a tick duration into a list of PES:EXEC:NOP instructions.

        PES:EXEC:NOP instruction: does nothing during 1 clock cycle

        :param ticks: Number of delay ticks to convert into PES:EXEC:NOP instructions
        :type ticks: ``int``

        :return: List of PES:EXEC:NOP instructions, and remaining tick count
        :rtype: ``(list[pes_instruction_execute_t], int)``

        :raise ``AssertionError``: invalid argument value
        """
        assert isinstance(ticks, int) and ticks >= 0, ticks

        instructions = []
        remaining_ticks = ticks

        # Each PES:EXEC:NOP instruction lasts exactly 1 clock cycle
        while remaining_ticks >= 1:
            pes_execute_instruction = pes_instruction_execute_t(opcode=PES_OPCODE_EXECUTE,
                                                                action_event=PES_ACTION_EVENT_NOP.value)
            instructions.append(pes_execute_instruction)
            remaining_ticks -= 1
        # end while

        return instructions, remaining_ticks
    # end def _get_pes_exec_nop_instructions_from_ticks

    @staticmethod
    def _get_execution_duration_ticks_from_pes_delay_instruction(instruction):
        """
        Return the instruction execution duration, in tick count, of a PES:DELAY instruction.

        :param instruction: PES:DELAY Instruction
        :type instruction: ``pes_instruction_delay_t``

        :return: Delay duration in tick count
        :rtype: ``int``

        :raise ``AssertionError``: invalid argument value
        """
        assert isinstance(instruction, pes_instruction_delay_t), instruction
        assert 1 <= instruction.opcode.mantissa <= 0xFFE
        return (instruction.opcode.mantissa * (1 << instruction.opcode.exponent)) * 100
    # end def _get_execution_duration_ticks_from_pes_delay_instruction

    @staticmethod
    def _get_execution_duration_ticks_from_pes_subdelay_instruction(instruction):
        """
        Return the instruction execution duration, in tick count, of a PES:SUBDELAY instruction.

        :param instruction: PES:SUBDELAY Instruction
        :type instruction: ``pes_instruction_subdelay_t``

        :return: Delay duration in tick count
        :rtype: ``int``

        :raise ``AssertionError``: Invalid Delay instruction opcode (i.e. using reserved value)
        """
        assert isinstance(instruction, pes_instruction_subdelay_t), instruction
        assert instruction.opcode.zero == 0, \
            f'Invalid Delay instruction opcode: field zero must be null. Opcode: {instruction.opcode}'
        assert instruction.opcode.nibble in pes_isa_opcode_delay_nibble_ns_e__enumvalues, \
            f'Invalid Delay instruction opcode: reserved value. Opcode: {instruction.opcode}'

        if instruction.opcode.nibble == PES_OPCODE_SUBDELAY_NIBBLE_05_TICKS:
            ticks = 5
        else:
            ticks = (instruction.opcode.nibble - PES_OPCODE_SUBDELAY_NIBBLE_10_TICKS + 1) * 10
        # end if
        return ticks
    # end def _get_execution_duration_ticks_from_pes_subdelay_instruction

    def wait_go_signal(self):
        """
        Add a PES:WAIT:GO instruction with resume event set to 'Go from RPi' signal.
        """
        self.wait(action=self.resume_event.GO_RPI)
    # end def wait_go_signal

    def insert_pes_wait_kbd_workaround(self):
        """
        Workaround: Ensure Test Sequence starts when KBD Emulators module are ready.
        This adds a PES:WAIT instruction to start the Test Sequence once the reset of the KBD Emulator modules are done.
        """
        # If KBD buffers are empty, skip workaround
        if not sum((kbd_dev.length() for kbd_dev in (self.dt.kbd_matrix, self.dt.kbd_gtech) if kbd_dev)):
            return
        # end if

        # Gather resume events for all available keymatrix emulators
        resume_events = (kbd_dev.resume_event.READY for kbd_dev in (self.dt.kbd_matrix, self.dt.kbd_gtech) if kbd_dev)

        # Insert PES:WAIT instruction as first position of the PES buffer
        pes_wait_kbd = self.get_wait_instruction(action=resume_events)
        if bytes(self._buffer[0]) != bytes(pes_wait_kbd):
            self._buffer.insert(0, pes_wait_kbd)
        # end if
    # end def insert_pes_wait_kbd_workaround

    def roundup_delay_ns_to_clock_period(self, delay_ns):
        """
        Round delay duration (in nanoseconds) up to the next FPGA clock period.

        Use this method to prevent the warning raised in ``PesSequence.get_delay_instructions()`` if the given delay
        is not an exact multiple of the FPGA clock period.

        :param delay_ns: delay duration to be rounded up, in nanoseconds
        :type delay_ns: ``int or float``

        :return: delay duration rounded up to the next FPGA clock period
        :rtype: ``int or float``
        """
        return ceil(delay_ns / self._fpga_clock_period_ns) * self._fpga_clock_period_ns
    # end def roundup_delay_ns_to_clock_period

    def roundup_delay_s_to_clock_period(self, delay_s):
        """
        Round delay duration (in seconds) up to the next FPGA clock period.

        Use this method to prevent the warning raised in ``PesSequence.get_delay_instructions()`` if the given delay
        is not an exact multiple of the FPGA clock period.

        :param delay_s: delay duration to be rounded up, in seconds
        :type delay_s: ``int or float``

        :return: delay duration rounded up to the next FPGA clock period
        :rtype: ``int or float``
        """
        return self.roundup_delay_ns_to_clock_period(delay_ns=(delay_s * 10 ** 9)) / 10**9
    # end def roundup_delay_s_to_clock_period
# end class PesModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
