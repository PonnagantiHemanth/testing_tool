#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.pescpu
:brief: Kosmos PES CPU Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass

from pyraspi.services.kosmos.module.module import ConsumerModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleSettings
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEvent
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventBase
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventMapInterface
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventModuleInterface
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEvents
from pyraspi.services.kosmos.module.pesevents import PesActionEvent
from pyraspi.services.kosmos.module.pesevents import PesEventMapInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesResumeEvent
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CPU
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CPU_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CPU_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CPU_CMD_WRITE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CPU_CMD_WRITE_MAX
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_PES_NOP
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_PARAM_BIT
from pyraspi.services.kosmos.protocol.generated.messages import pes_cpu_action_e
from pyraspi.services.kosmos.protocol.generated.messages import pes_cpu_action_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_cpu_status_t


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

@dataclass(frozen=True)
class PesCpuActionEvent(PesEventMapInterface):
    """
    PES Action Events for PES-CPU module
    """
    CPU_REQ: PesActionEvent = None
# end class PesCpuActionEvent


@dataclass(frozen=True)
class PesCpuResumeEvent(PesEventMapInterface):
    """
    PES Resume Events for PES-CPU module
    """
    CPU_RET: PesResumeEvent = None
# end class PesCpuResumeEvent


@dataclass(frozen=True)
class PesCpuCoreEvent(PesCpuEventMapInterface):
    """
    PES-CPU Events for PES core module
    """
    NOP_EVENT: PesCpuEvent = PES_CPU_ACTION_PES_NOP
# end class PesCpuCoreEvent


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PesCpuModule(ConsumerModuleBaseClass, PesEventModuleInterface, PesCpuEventModuleInterface):
    """
    Kosmos PES CPU Module class. This is an auxiliary module, attached to PES module.
    Its goal is to handle the Microblaze CPU interrupt request from and to PES module.
    """

    # PES Event maps related to the current module
    action_event = PesCpuActionEvent
    resume_event = PesCpuResumeEvent

    # PES CPU Event map related to the current module
    cpu_event = PesCpuCoreEvent

    # PES CPU Events manager
    cpu_events: PesCpuEvents = None

    def __init__(self):
        module_settings = ConsumerModuleSettings(
            name=r'PES CPU',
            instance_id=None,  # Module is a singleton
            optional=False,
            msg_id=MSG_ID_PES_CPU,
            buffer_size=(PES_CPU_ACTION_BUFFER_SIZE - 1),
            fifo_size=None,
            status_type=pes_cpu_status_t,
            msg_cmd_status=MSG_ID_PES_CPU_CMD_STATUS,
            msg_cmd_reset=MSG_ID_PES_CPU_CMD_RESET,
            data_type=pes_cpu_action_t,
            msg_cmd_write_one=MSG_ID_PES_CPU_CMD_WRITE_1,
            msg_cmd_write_max=MSG_ID_PES_CPU_CMD_WRITE_MAX,
            msg_payload_name=r'pes_cpu_actions'
        )
        super().__init__(module_settings=module_settings)
    # end def __init__

    def post_init_device_tree(self):
        """
        Action to be done after Device Tree has been initialized.
        """
        self.cpu_events = PesCpuEvents(dt=self._dt)
    # end def post_init_device_tree

    def action(self, cpu_event):
        """
        Add a PES CPU Action to the PES instruction buffer.

        Execution flow:
         1) Trigger an interrupt on the Microblaze
         2) Halt PES Sequence execution
         3) Execute the action `cpu_action` using CPU
         4) Resume PES Sequence execution

        This creates two PES instructions and add them to the PES instruction buffer:
         - PES EXEC:CPU instruction: The PES module triggers a PES CPU interrupt
         - PES WAIT:CPU instruction: The PES module waits for the PES CPU interrupt to finish

        This also add the `cpu_action` to the PES CPU Action buffer.
        This buffer will be consumed by the PES CPU interrupt (pop one entry per interrupt call).

        :param cpu_event: Specify which CPU action to be executed
        :type cpu_event: ``PesCpuEventBase``

        :raise ``AssertionError``: invalid arguments
        """
        assert isinstance(cpu_event, PesCpuEventBase), cpu_event

        # Add PES CPU Action instruction
        self.append(pes_cpu_action_t(module=cpu_event.module_id,
                                     action=pes_cpu_action_e(raw=cpu_event.event),
                                     param=cpu_event.param))

        # Add PES:EXEC:CPU instruction to trigger the CPU interrupt
        self._pes_exec_cpu()
        # Add PES:WAIT:CPU instruction to wait for the CPU interrupt to finnish
        self._pes_wait_cpu()
    # end def action

    def _pes_exec_cpu(self):
        """
        Add a PES:EXEC:CPU instruction to the local PES instruction buffer.
        """
        self.dt.pes.execute(action=self.action_event.CPU_REQ)
    # end def _pes_exec_cpu

    def _pes_wait_cpu(self):
        """
        Add a PES:WAIT:CPU instruction to the local PES instruction buffer.
        """
        self.dt.pes.wait(action=self.resume_event.CPU_RET)
    # end def _pes_wait_cpu
# end class PesCpuModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
