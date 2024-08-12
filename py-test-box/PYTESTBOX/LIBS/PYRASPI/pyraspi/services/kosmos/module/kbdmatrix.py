#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.kbdmatrix
:brief: Kosmos KBD Matrix Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass

from pyraspi.services.kosmos.module.devicetree import DeviceTreeGenericModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleSettings
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEvent
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventMapInterface
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesActionEvent
from pyraspi.services.kosmos.module.pesevents import PesEventMapInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesResumeEvent
from pyraspi.services.kosmos.protocol.generated.messages import KBD_BANK_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COL_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_LANE_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_MATRIX_ADDR_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_MATRIX_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import KBD_MATRIX_FIFO_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import KBD_ROW_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_MATRIX_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_MATRIX_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_MATRIX_CMD_WRITE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_MATRIX_CMD_WRITE_MAX
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_KBD_MATRIX_SET_DEFAULT_FREEZE
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_KBD_MATRIX_SET_DEFAULT_WRITE
from pyraspi.services.kosmos.protocol.generated.messages import kbd_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import kbd_matrix_status_t


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class KbdActionEvent(PesEventMapInterface):
    """
    PES Action Events for MATRIX KBD module
    """
    SEND: PesActionEvent = None
# end class KbdActionEvent


@dataclass(frozen=True)
class KbdResumeEvent(PesEventMapInterface):
    """
    PES Resume Events for MATRIX KBD module
    """
    READY: PesResumeEvent = None
# end class KbdResumeEvent


@dataclass(frozen=True)
class KbdCpuEvent(PesCpuEventMapInterface):
    """
    PES-CPU Events for MATRIX KDB Emulator module
    """
    SET_DEFAULT_FREEZE: PesCpuEvent = PES_CPU_ACTION_KBD_MATRIX_SET_DEFAULT_FREEZE
    SET_DEFAULT_WRITE: PesCpuEvent = PES_CPU_ACTION_KBD_MATRIX_SET_DEFAULT_WRITE
# end class KbdCpuEvent


@dataclass(frozen=True)
class KbdModuleSettings(ConsumerModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``kbd_row_count``: Physical matrix ROW dimension
    ``kbd_col_count``: Physical matrix COL dimension
    ``kbd_addr_count``: FPGA block RAM size (address count)
    ``kbd_lane_count``: FPGA block RAM width (bit count)
    ``kbd_bank_count``: FPGA block RAM instance (bank count)
    """
    kbd_row_count: int
    kbd_col_count: int
    kbd_addr_count: int
    kbd_lane_count: int
    kbd_bank_count: int

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        assert isinstance(self.kbd_row_count, int) and self.kbd_row_count > 0, self.kbd_row_count
        assert isinstance(self.kbd_col_count, int) and self.kbd_col_count > 0, self.kbd_col_count
        assert isinstance(self.kbd_addr_count, int) and self.kbd_addr_count > 0, self.kbd_addr_count
        assert isinstance(self.kbd_lane_count, int) and self.kbd_lane_count > 0, self.kbd_lane_count
        assert isinstance(self.kbd_bank_count, int) and self.kbd_bank_count > 0, self.kbd_bank_count
    # end def __post_init__
# end class KbdModuleSettings


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KbdMatrixModule(PesEventModuleInterface,
                      PesCpuEventModuleInterface,
                      ConsumerModuleBaseClass,
                      DeviceTreeGenericModuleBaseClass):
    """
    Kosmos KBD Matrix Module class.
      KBD stands for "Keyboard".
      Matrix refer to the keys' electrical layout & probing methods.
    """

    # PES Event maps related to the current module
    action_event = KbdActionEvent
    resume_event = KbdResumeEvent

    # PES CPU Event map related to the current module
    cpu_event = KbdCpuEvent

    def __init__(self, msg_id):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        """
        module_settings = KbdModuleSettings(
            name=r'KBD MATRIX',
            instance_id=None,  # Module is a singleton
            optional=True,
            msg_id=msg_id,
            buffer_size=(KBD_MATRIX_BUFFER_SIZE - 1),
            fifo_size=(KBD_MATRIX_FIFO_SIZE - 1),
            status_type=kbd_matrix_status_t,
            msg_cmd_status=MSG_ID_KBD_MATRIX_CMD_STATUS,
            msg_cmd_reset=MSG_ID_KBD_MATRIX_CMD_RESET,
            data_type=kbd_entry_t,
            msg_cmd_write_one=MSG_ID_KBD_MATRIX_CMD_WRITE_1,
            msg_cmd_write_max=MSG_ID_KBD_MATRIX_CMD_WRITE_MAX,
            msg_payload_name=r'kbd_matrix',
            kbd_row_count=KBD_ROW_COUNT,
            kbd_col_count=KBD_COL_COUNT,
            kbd_addr_count=KBD_MATRIX_ADDR_COUNT,
            kbd_lane_count=KBD_LANE_COUNT,
            kbd_bank_count=KBD_BANK_COUNT
        )
        super().__init__(module_settings=module_settings)
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``KbdModuleSettings``
        """
        return self._settings
    # end def property getter settings

    def pes_wait_kbd(self):
        """
        Add a PES:WAIT:KBD_MATRIX instruction (wait while KBD_MATRIX module is busy)
        """
        self.dt.pes.wait(action=self.resume_event.READY)
    # end def pes_wait_kbd

    def enable_set_default(self):
        """
        Add a PES CPU Action to enable the set_default mode.
        """
        self.dt.pes_cpu.action(self.cpu_event.SET_DEFAULT_WRITE)
    # end def enable_set_default

    def disable_set_default(self):
        """
        Add a PES CPU Action to disable the set_default mode.
        """
        self.dt.pes_cpu.action(self.cpu_event.SET_DEFAULT_FREEZE)
    # end def disable_set_default
# end class KbdMatrixModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
