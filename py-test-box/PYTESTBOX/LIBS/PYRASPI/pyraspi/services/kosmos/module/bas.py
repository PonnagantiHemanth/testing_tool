#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.bas
:brief: Kosmos BAS Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Union

from pyraspi.services.kosmos.module.devicetree import DeviceTreeGenericModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleSettings
from pyraspi.services.kosmos.module.pesevents import PesActionEvent
from pyraspi.services.kosmos.module.pesevents import PesEventMapInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesResumeEvent
from pyraspi.services.kosmos.protocol.generated.messages import BAS_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import BAS_FIFO_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_BAS_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_BAS_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_BAS_CMD_WRITE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_BAS_CMD_WRITE_MAX
from pyraspi.services.kosmos.protocol.generated.messages import bas_buttons_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import bas_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import bas_sliders_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import bas_status_t

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
bas_instruction_types = (bas_entry_t, bas_buttons_entry_t, bas_sliders_entry_t)


@dataclass(frozen=True)
class BasActionEvent(PesEventMapInterface):
    """
    PES Action Events for BAS module
    """
    SEND: PesActionEvent = None
# end class BasActionEvent


@dataclass(frozen=True)
class BasResumeEvent(PesEventMapInterface):
    """
    PES Resume Events for BAS module
    """
    READY: PesResumeEvent = None
# end class BasResumeEvent


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class BasModule(PesEventModuleInterface,
                ConsumerModuleBaseClass,
                DeviceTreeGenericModuleBaseClass):
    """
    Kosmos BAS Module class. BAS stands for "Buttons and Sliders".
    """

    # PES Event maps related to the current module
    action_event = BasActionEvent
    resume_event = BasResumeEvent

    def __init__(self, msg_id):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        """
        module_settings = ConsumerModuleSettings(
            name=r'BAS',
            instance_id=None,  # Module is a singleton
            optional=True,
            msg_id=msg_id,
            buffer_size=(BAS_BUFFER_SIZE - 1),
            fifo_size=(BAS_FIFO_SIZE - 1),
            status_type=bas_status_t,
            msg_cmd_status=MSG_ID_BAS_CMD_STATUS,
            msg_cmd_reset=MSG_ID_BAS_CMD_RESET,
            data_type=bas_instruction_types,
            msg_cmd_write_one=MSG_ID_BAS_CMD_WRITE_1,
            msg_cmd_write_max=MSG_ID_BAS_CMD_WRITE_MAX,
            msg_payload_name=r'bas'
        )
        super().__init__(module_settings=module_settings)
    # end def __init__

    @staticmethod
    def _set_message_payload(payload, payload_index, data):
        """
        Override base class method to set the MessageFrame payload, depending on data type.

        :param payload: Ctypes Array
        :type payload: ``ctypes.Array``
        :param payload_index: index of payload array
        :type payload_index: ``int``
        :param data: instruction data to be set in the payload
        :type data: ``Union[bas_instruction_types]``

        :raise ``AssertionError``: Invalid payload type
        :raise ``TypeError``: Invalid instruction data type
        """
        assert isinstance(payload[payload_index], bas_entry_t), f'Payload has type {type(payload[payload_index])}'
        if isinstance(data, bas_entry_t):
            payload[payload_index] = data
        elif isinstance(data, bas_buttons_entry_t):
            payload[payload_index].bloc.buttons = data
            # payload[payload_index].bloc.sliders was zero-initialized during MessageFrame instantiation
        elif isinstance(data, bas_sliders_entry_t):
            payload[payload_index].bloc.sliders = data
            # payload[payload_index].bloc.buttons was zero-initialized during MessageFrame instantiation
        else:
            raise TypeError(f'Instruction {data} type should be in {bas_instruction_types}.')
        # end if
    # end def _set_message_payload

    def pes_wait_bas(self):
        """
        Add a PES:WAIT:BAS instruction (wait while BAS module is busy)
        """
        self.dt.pes.wait(action=self.resume_event.READY)
    # end def pes_wait_bas
# end class BasModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
