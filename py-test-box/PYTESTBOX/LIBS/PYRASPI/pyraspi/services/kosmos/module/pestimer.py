#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.pestimer
:brief: Kosmos PES Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from enum import IntEnum
from enum import unique
from typing import Dict
from typing import Iterable

from pylibrary.emulator.emulatorinterfaces import TimersInterface
from pyraspi.services.kosmos.module.module import DownloadModuleBaseClass
from pyraspi.services.kosmos.module.module import DownloadModuleSettings
from pyraspi.services.kosmos.module.module import StatusResetModuleBaseClass
from pyraspi.services.kosmos.module.module import StatusResetModuleSettings
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_STOPWATCH1_READ_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_STOPWATCH1_READ_MAX
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_STOPWATCH2_READ_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_STOPWATCH2_READ_MAX
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_TIMESTAMP1_READ_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_TIMESTAMP1_READ_MAX
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_TIMESTAMP2_READ_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_TIMER_CMD_TIMESTAMP2_READ_MAX
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
from pyraspi.services.kosmos.protocol.generated.messages import PES_TIMER_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import PES_TIMER_ID_STOPWATCH_1
from pyraspi.services.kosmos.protocol.generated.messages import PES_TIMER_ID_STOPWATCH_2
from pyraspi.services.kosmos.protocol.generated.messages import PES_TIMER_ID_TIMESTAMP_1
from pyraspi.services.kosmos.protocol.generated.messages import PES_TIMER_ID_TIMESTAMP_2
from pyraspi.services.kosmos.protocol.generated.messages import pes_timer_status_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_timer_t


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@unique
class TIMER(IntEnum):
    """
    Enumeration class to identify the different PES Timers.

    PES contains 4 different time reference units:
      - Two "timestamp" timers:
        - One "global" time mark counter.
        - One "local" time mark counter, resettable via a dedicated PES MARKER instruction.
      - Two "stopwatch" timers:
        - Each stopwatch timers can be reset, started, paused and resumed via dedicated PES MARKER instructions.
      - Time base: 1 timer tick = 10 ns.
      - All timers are 64-bit wide.
      - All timers are reset when PES soft-reset signal is asserted.
    """
    # Timestamp timers
    GLOBAL = PES_TIMER_ID_TIMESTAMP_1
    LOCAL = PES_TIMER_ID_TIMESTAMP_2

    # Stopwatch timers
    STOPWATCH_1 = PES_TIMER_ID_STOPWATCH_1
    STOPWATCH_2 = PES_TIMER_ID_STOPWATCH_2
# end class TIMER

# List of timer IDs, per affinity
ALL_TIMERS = list(TIMER)
TIMESTAMP_TIMERS = [TIMER.GLOBAL, TIMER.LOCAL]
STOPWATCH_TIMERS = [TIMER.STOPWATCH_1, TIMER.STOPWATCH_2]
RESETABLE_TIMERS = [TIMER.LOCAL, TIMER.STOPWATCH_1, TIMER.STOPWATCH_2]

# Map Timer IDs to PES:MARKER:SAVE actions
TIMER_SAVE_MARKER_ACTION_MAP = {
    TIMER.GLOBAL:      PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK,
    TIMER.LOCAL:       PES_ISA_MARKER_OP_SAVE_LOCAL_TIME_MARK,
    TIMER.STOPWATCH_1: PES_ISA_MARKER_OP_SAVE_STOPWATCH_1_TIME_MARK,
    TIMER.STOPWATCH_2: PES_ISA_MARKER_OP_SAVE_STOPWATCH_2_TIME_MARK}

# Map Timer IDs to PES:MARKER:RESET actions
TIMER_RESET_MARKER_ACTION_MAP = {
    TIMER.LOCAL:       PES_ISA_MARKER_OP_RESET_LOCAL_TIME_MARK,
    TIMER.STOPWATCH_1: PES_ISA_MARKER_OP_RESET_STOPWATCH_1_TIME_MARK,
    TIMER.STOPWATCH_2: PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK}

# Map Timer IDs to PES:MARKER:START actions
TIMER_START_MARKER_ACTION_MAP = {
    TIMER.STOPWATCH_1: PES_ISA_MARKER_OP_STOPWATCH_1_GO,
    TIMER.STOPWATCH_2: PES_ISA_MARKER_OP_STOPWATCH_2_GO}

# Map Timer IDs to PES:MARKER:STOP actions
TIMER_STOP_MARKER_ACTION_MAP = {
    TIMER.STOPWATCH_1: PES_ISA_MARKER_OP_STOPWATCH_1_STOP,
    TIMER.STOPWATCH_2: PES_ISA_MARKER_OP_STOPWATCH_2_STOP}

# Map Timer IDs to combination of PES:MARKER:RESET & PES:MARKER:START actions
TIMER_RESTART_MARKER_ACTION_MAP = {
    TIMER.LOCAL:       PES_ISA_MARKER_OP_RESET_LOCAL_TIME_MARK,
    TIMER.STOPWATCH_1: PES_ISA_MARKER_OP_RESET_STOPWATCH_1_TIME_MARK | PES_ISA_MARKER_OP_STOPWATCH_1_GO,
    TIMER.STOPWATCH_2: PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK | PES_ISA_MARKER_OP_STOPWATCH_2_GO}

# Timer measurement offsets.
#   It means that the Timestamp timers always reports 2 extra ticks counts than the duration of the event to be timed.
#   This has been verified by observation and by inspection of the FPGA design.
#   TODO: This is the result of a FPGA design flaw, that is compensated in software for the moment.
TIMESTAMP_OFFSET = 2  # 2 ticks offset
STOPWATCH_OFFSET = 0  # 0 tick, no offset

# Map Timer IDs to Timer offset
TIMER_OFFSET_MAP = {
    TIMER.GLOBAL: TIMESTAMP_OFFSET,
    TIMER.LOCAL: TIMESTAMP_OFFSET,
    TIMER.STOPWATCH_1: STOPWATCH_OFFSET,
    TIMER.STOPWATCH_2: STOPWATCH_OFFSET}


@dataclass(frozen=True)
class PesTimerSettings(DownloadModuleSettings):
    """
    Dataclass constructor arguments:
    ``timer_id``: Internal Timer identifier
    """
    timer_id: TIMER

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        assert self.timer_id in TIMER, self.timer_id
    # end def __post_init__
# end class PesTimerSettings


class PesTimerModule(DownloadModuleBaseClass):
    """
    Kosmos PES Timer class. This class represent one PES Timer.

    PES contains 4 different time reference units:
      - Two "timestamp" timers:
        - One "global" time mark counter.
        - One "local" time mark counter, resettable via a dedicated PES MARKER instruction.
      - Two "stopwatch" timers:
        - Each stopwatch timers can be reset, started, paused and resumed via dedicated PES MARKER instructions.
      - Time base: 1 timer tick = 10 ns.
      - All timers are 64-bit wide.
      - All timers are reset when PES soft-reset signal is asserted.

    Available base features, per timer:

        | timer       | save | reset | start | stop |
        |-------------|:----:|:-----:|:-----:|:----:|
        | Global      |  yes |   NO  |   NO  |  NO  |
        | Local       |  yes |  yes  |   NO  |  NO  |
        | Stopwatch 1 |  yes |  yes  |  yes  |  yes |
        | Stopwatch 2 |  yes |  yes  |  yes  |  yes |

    Available extended features, per timer:

        | timer       | restart |     restart = reset + start
        |-------------|:-------:|
        | Global      |    NO   |
        | Local       |   yes   |
        | Stopwatch 1 |   yes   |
        | Stopwatch 2 |   yes   |
    """

    def __init__(self, module_settings):
        """
        :param module_settings: Kosmos PES TIMER Module settings dataclass object
        :type module_settings: ``PesTimerSettings``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(module_settings, PesTimerSettings), module_settings
        super().__init__(module_settings=module_settings)
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``PesTimerSettings``
        """
        return self._settings
    # end def property getter settings

    def save(self):
        """
        Add a PES:MARKER:SAVE instruction to the local PES instruction buffer, for the current Timer.
        This instruction is available for all timers.
        """
        self.dt.pes.marker(action=self.get_save_marker_action())
    # end def save

    def reset(self):
        """
        Add a PES:MARKER:RESET instruction to the local PES instruction buffer, for the current Timer.
        This instruction is only available for LOCAL & STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.
        """
        self.dt.pes.marker(action=self.get_reset_marker_action())
    # end def reset

    def start(self):
        """
        Add a PES:MARKER:START instruction to the local PES instruction buffer, for the current Timer.
        This instruction is only available for STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.
        """
        self.dt.pes.marker(action=self.get_start_marker_action())
    # end def start

    def stop(self):
        """
        Add a PES:MARKER:STOP instruction to the local PES instruction buffer, for the current Timer.
        This instruction is only available for STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.
        """
        self.dt.pes.marker(action=self.get_stop_marker_action())
    # end def stop

    def restart(self):
        """
        Add a PES:MARKER:(RESET|START) instruction to the local PES instruction buffer, for the current Timer.
        This instruction is only available for LOCAL & STOPWATCH timers.

        Note: As LOCAL timer doesn't support START action, the present method returns a PES:MARKER:RESET instruction.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.
        """
        self.dt.pes.marker(action=self.get_restart_marker_action())
    # end def restart

    def get_save_marker_action(self):
        """
        Return a PES:MARKER:SAVE instruction, with opcode and operand fields set for the current timer.
        This instruction is available for all timers.

        :return: PES:MARKER:SAVE marker instruction. Refer to ``pes_isa_marker_operation_e__enumvalues``.
        :rtype: ``pes_isa_marker_operation_e or int``
        """
        return TIMER_SAVE_MARKER_ACTION_MAP[self.settings.timer_id]
    # end def get_save_marker_action

    def get_reset_marker_action(self):
        """
        Return a PES:MARKER:RESET instruction, with opcode and operand fields set for the current timer.
        This instruction is only available for LOCAL & STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.

        :return: PES:MARKER:RESET marker instruction. Refer to ``pes_isa_marker_operation_e__enumvalues``.
        :rtype: ``pes_isa_marker_operation_e or int``
        """
        try:
            return TIMER_RESET_MARKER_ACTION_MAP[self.settings.timer_id]
        except KeyError as e:
            e.args = (f'Invalid instruction: timer {e.args[0].name} does not support RESET operation.',) + e.args
            raise
        # end try
    # end def get_reset_marker_action

    def get_start_marker_action(self):
        """
        Return a PES:MARKER:START instruction, with opcode and operand fields set for the current timer.
        This instruction is only available for STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.

        :return: PES:MARKER:START marker instruction. Refer to ``pes_isa_marker_operation_e__enumvalues``.
        :rtype: ``pes_isa_marker_operation_e or int``
        """
        try:
            return TIMER_START_MARKER_ACTION_MAP[self.settings.timer_id]
        except KeyError as e:
            e.args = (f'Invalid instruction: timer {e.args[0].name} does not support START operation.',) + e.args
            raise
        # end try
    # end def get_start_marker_action

    def get_stop_marker_action(self):
        """
        Return a PES:MARKER:STOP instruction, with opcode and operand fields set for the current timer.
        This instruction is only available for STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.

        :return: PES:MARKER:STOP marker instruction. Refer to ``pes_isa_marker_operation_e__enumvalues``.
        :rtype: ``pes_isa_marker_operation_e or int``
        """
        try:
            return TIMER_STOP_MARKER_ACTION_MAP[self.settings.timer_id]
        except KeyError as e:
            e.args = (f'Invalid instruction: timer {e.args[0].name} does not support STOP operation.',) + e.args
            raise
        # end try
    # end def get_stop_marker_action

    def get_restart_marker_action(self):
        """
        Return a PES:MARKER:(RESET|START) instruction, with opcode and operand fields set for the current timer.
        This instruction is only available for LOCAL and STOPWATCH timers.

        Note: As LOCAL timer doesn't support START action, the present method returns a PES:MARKER:RESET instruction.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.

        :return: PES:MARKER:(RESET|START) marker instruction. Refer to ``pes_isa_marker_operation_e__enumvalues``.
        :rtype: ``pes_isa_marker_operation_e or int``
        """
        try:
            return TIMER_RESTART_MARKER_ACTION_MAP[self.settings.timer_id]
        except KeyError as e:
            e.args = (f'Invalid instruction: timer {e.args[0].name} does not support RESTART operation.',) + e.args
            raise
        # end try
    # end def get_restart_marker_action

    def get_offset(self):
        """
        Return the Timer's counter value offset.
        The TIMESTAMP timers always reports 2 extra ticks counts than the duration of the event to be timed.
        The STOPWATCH timers are producing an exact duration measurement. No offset to be compensated for.

        This is the result of a FPGA design flaw, that is compensated in software for the moment.
        This has been verified by observation and by inspection of the FPGA design.

        Refer to the ``TIMER_OFFSET_MAP``.

        :return: Timer's save value offset
        :rtype: ``int``
        """
        return TIMER_OFFSET_MAP[self.settings.timer_id]
    # end def get_offset

    def _status(self):
        """
        Return the current Timer Module's status.

        :return: module's status.
        :rtype: ``pes_timer_status_t``
        """
        # Send request and get reply
        status = super()._status()
        return status[self.settings.timer_id]
        # end if
    # end def _status

    def _reset_module(self):
        """
        Reset the module:
          - Mask all interrupt sources
          - Clear FIFO and buffer content
          - Clear FIFO and buffer overrun status
          - Reset module's FPGA state machine

        WARNING: The Timer reset message is shared between all the Timers. This resets each Timers.
                 That mean is it not possible to reset only one timer's module, for example.

        :return: module status after reset of the module.
        :rtype: ``pes_timer_status_t``
        """
        # Send request and get reply
        status = super()._reset_module()
        return status[self.settings.timer_id]
    # end def _reset_module
# end class PesTimerModule


class PesTimersModule(StatusResetModuleBaseClass, TimersInterface):
    """
    PES Timers module, covering all four PES timers.
    """

    _timer: Dict[TIMER, PesTimerModule]

    def __init__(self):
        module_settings = StatusResetModuleSettings(
            name=r'PES TIMER',
            instance_id=None,  # Timers Module is a singleton
            optional=False,
            msg_id=MSG_ID_PES_TIMER,
            status_type=pes_timer_status_t,
            msg_cmd_status=MSG_ID_PES_TIMER_CMD_STATUS,
            msg_cmd_reset=MSG_ID_PES_TIMER_CMD_RESET
        )
        super().__init__(module_settings=module_settings)

        self._timer = dict()
        timestamp1_settings = PesTimerSettings(
            name='PES TIMESTAMP',
            instance_id=1,
            optional=False,
            timer_id=TIMER.GLOBAL,
            msg_id=MSG_ID_PES_TIMER,
            buffer_size=(PES_TIMER_BUFFER_SIZE - 1),
            fifo_size=None,
            status_type=pes_timer_status_t,
            msg_cmd_status=MSG_ID_PES_TIMER_CMD_STATUS,
            msg_cmd_reset=MSG_ID_PES_TIMER_CMD_RESET,
            data_type=pes_timer_t,
            msg_cmd_read_one=MSG_ID_PES_TIMER_CMD_TIMESTAMP1_READ_1,
            msg_cmd_read_max=MSG_ID_PES_TIMER_CMD_TIMESTAMP1_READ_MAX
        )
        self._timer[TIMER.GLOBAL] = PesTimerModule(module_settings=timestamp1_settings)
        timestamp2_settings = PesTimerSettings(
            name='PES TIMESTAMP',
            instance_id=2,
            optional=False,
            timer_id=TIMER.LOCAL,
            msg_id=MSG_ID_PES_TIMER,
            buffer_size=(PES_TIMER_BUFFER_SIZE - 1),
            fifo_size=None,
            status_type=pes_timer_status_t,
            msg_cmd_status=MSG_ID_PES_TIMER_CMD_STATUS,
            msg_cmd_reset=MSG_ID_PES_TIMER_CMD_RESET,
            data_type=pes_timer_t,
            msg_cmd_read_one=MSG_ID_PES_TIMER_CMD_TIMESTAMP2_READ_1,
            msg_cmd_read_max=MSG_ID_PES_TIMER_CMD_TIMESTAMP2_READ_MAX
        )
        self._timer[TIMER.LOCAL] = PesTimerModule(module_settings=timestamp2_settings)
        stopwatch1_settings = PesTimerSettings(
            name='PES STOPWATCH',
            instance_id=1,
            optional=False,
            timer_id=TIMER.STOPWATCH_1,
            msg_id=MSG_ID_PES_TIMER,
            buffer_size=(PES_TIMER_BUFFER_SIZE - 1),
            fifo_size=None,
            status_type=pes_timer_status_t,
            msg_cmd_status=MSG_ID_PES_TIMER_CMD_STATUS,
            msg_cmd_reset=MSG_ID_PES_TIMER_CMD_RESET,
            data_type=pes_timer_t,
            msg_cmd_read_one=MSG_ID_PES_TIMER_CMD_STOPWATCH1_READ_1,
            msg_cmd_read_max=MSG_ID_PES_TIMER_CMD_STOPWATCH1_READ_MAX
        )
        self._timer[TIMER.STOPWATCH_1] = PesTimerModule(module_settings=stopwatch1_settings)
        stopwatch2_settings = PesTimerSettings(
            name='PES STOPWATCH',
            instance_id=2,
            optional=False,
            timer_id=TIMER.STOPWATCH_2,
            msg_id=MSG_ID_PES_TIMER,
            buffer_size=(PES_TIMER_BUFFER_SIZE - 1),
            fifo_size=None,
            status_type=pes_timer_status_t,
            msg_cmd_status=MSG_ID_PES_TIMER_CMD_STATUS,
            msg_cmd_reset=MSG_ID_PES_TIMER_CMD_RESET,
            data_type=pes_timer_t,
            msg_cmd_read_one=MSG_ID_PES_TIMER_CMD_STOPWATCH2_READ_1,
            msg_cmd_read_max=MSG_ID_PES_TIMER_CMD_STOPWATCH2_READ_MAX
        )
        self._timer[TIMER.STOPWATCH_2] = PesTimerModule(module_settings=stopwatch2_settings)
    # end def __init__

    def __getitem__(self, timer):
        """
        Return instance of a timer using the array operator [].

        Note: ``IndexError`` will be raised for invalid timer value

        :param timer: Timer ID. Refer to enum `TIMER`.
        :type timer: ``TIMER``

        :return: PesTimerModule instance
        :rtype: ``PesTimerModule``
        """
        return self._timer[timer]
    # end def __getitem__

    def init_device_tree(self, dt):
        """
        Set Device Tree in this PesTimersModule instance and recursively in PesTimerModule instances.

        :param dt: Kosmos Module Device Tree
        :type dt: ``DeviceTree``
        """
        super().init_device_tree(dt=dt)
        for timer in self._timer.values():
            timer.init_device_tree(dt=dt)
        # end for
    # end def init_device_tree

    def status(self, sanity_checks=True):
        """
        Return the module's status.

        :param sanity_checks: If True, run sanity checks on the status reply and raise an error if something is wrong.
                              If False, skip sanity checks. Defaults to True - OPTIONAL
        :type sanity_checks: ``bool``

        :return: module's status.
        :rtype: ``Dict[TIMER, pes_timer_status_t]``
        """
        # Send request and get reply
        status = super().status(sanity_checks=sanity_checks)

        return dict(zip(TIMER, status))
    # end def status

    def reset(self, timers):
        """
        Add a PES:MARKER:RESET instruction to the local PES instruction buffer, for the given Timers.
        This instruction is only available for LOCAL & STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``
        """
        timers = timers if isinstance(timers, Iterable) else [timers]
        actions = sum(self[t].get_reset_marker_action() for t in timers)
        self.dt.pes.marker(action=actions)
    # end def reset

    def start(self, timers):
        """
        Add a PES:MARKER:START instruction to the local PES instruction buffer, for the given Timers.
        This instruction is only available for STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``
        """
        timers = timers if isinstance(timers, Iterable) else [timers]
        actions = sum(self[t].get_start_marker_action() for t in timers)
        self.dt.pes.marker(action=actions)
    # end def start

    def restart(self, timers):
        """
        Reset and start one or more timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested action.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``
        """
        timers = timers if isinstance(timers, Iterable) else [timers]
        actions = sum(self[t].get_restart_marker_action() for t in timers)
        self.dt.pes.marker(action=actions)
    # end def restart

    def stop(self, timers):
        """
        Add a PES:MARKER:STOP instruction to the local PES instruction buffer, for the given Timers.
        This instruction is only available for STOPWATCH timers.

        Note: ``KeyError`` will be raised if the present timer does not support the requested marker action.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``
        """
        timers = timers if isinstance(timers, Iterable) else [timers]
        actions = sum(self[t].get_stop_marker_action() for t in timers)
        self.dt.pes.marker(action=actions)
    # end def stop

    def save(self, timers):
        """
        Save one or more timer's counter value in their respective buffers.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``
        """
        timers = timers if isinstance(timers, Iterable) else [timers]
        actions = sum(self[t].get_save_marker_action() for t in timers)
        self.dt.pes.marker(action=actions)
    # end def save

    def download(self, count=None):
        """
        Download buffers of each timer.

        :param count: number of entries to be downloaded from remote buffer - OPTIONAL
                      If not provided, the whole buffers will be downloaded.
        :type count: ``int or None``

        :return: The list of downloaded entries
        :rtype: ``dict[TIMER, list[pes_timer_t]]``
        """
        status = self.status() if count is None else None
        buffers = dict()
        for t in TIMER:
            c = status[t].buffer_count if count is None else count
            buffers[t] = self[t].download(count=c)
        # end for
        return buffers
    # end def download

    @staticmethod
    def get_offset():
        """
        Return the Timers counter value offsets. Refer to ``TIMER_OFFSET_MAP``.

        :return: Timers counter value offsets
        :rtype: ``Dict[TIMER, int]``
        """
        return TIMER_OFFSET_MAP
    # end def get_offset

    def pes_delay_for_timer_interrupt(self):
        """
        Add a PES:DELAY instruction to give enough time to the Timer interrupt to copy the FIFO into the buffer.
        """
        self.dt.pes.delay(delay_ns=10**4)  # Arbitrary/Empirical value
    # end def pes_delay_for_timer_interrupt

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``pes_timer_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - any of the individual Timer module status reply is invalid
        :rtype: ``list[str]``
        """
        error_list = []
        for t in TIMER:
            error_list.extend(self[t].is_status_reply_valid(status[t]))
        # end for
        return error_list
    # end def is_status_reply_valid

    def is_reset_reply_valid(self, status):
        """
        Validate Reset command's Status reply structure.

        :param status: Status structure
        :type status: ``pes_timer_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - any of the individual Timer module status reply is invalid
        :rtype: ``list[str]``
        """
        error_list = []
        for t in TIMER:
            error_list.extend(self[t].is_reset_reply_valid(status[t]))
        # end for
        return error_list
    # end def is_reset_reply_valid
# end class PesTimersModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
