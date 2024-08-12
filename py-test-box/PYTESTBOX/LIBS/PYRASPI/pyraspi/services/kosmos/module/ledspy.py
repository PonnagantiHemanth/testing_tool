#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.ledspy
:brief: Kosmos LED SPY Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/12/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass

from pyraspi.services.kosmos.module.devicetree import DeviceTreeGenericModuleBaseClass
from pyraspi.services.kosmos.module.module import ProducerModuleBaseClass
from pyraspi.services.kosmos.module.module import ProducerModuleSettings
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEvent
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventMapInterface
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesActionEvent
from pyraspi.services.kosmos.module.pesevents import PesEventMapInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_FIFO_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_STATE_RESET_OR_STOP
from pyraspi.services.kosmos.protocol.generated.messages import LED_SPY_STATE_STARTED
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_CHANNEL_ENABLE_READ
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_CHANNEL_ENABLE_WRITE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_GATE_LATCH_READ
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_GATE_LATCH_WRITE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_READ_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_READ_MAX
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_START
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_LED_SPY_CMD_STOP
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_LED_SPY_FIFO_FLUSH
from pyraspi.services.kosmos.protocol.generated.messages import led_spy_channel_enable_t
from pyraspi.services.kosmos.protocol.generated.messages import led_spy_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import led_spy_gate_latch_t
from pyraspi.services.kosmos.protocol.generated.messages import led_spy_state_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import led_spy_status_t
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

@dataclass(frozen=True)
class LedSpyActionEvent(PesEventMapInterface):
    """
    PES Action Events for LED SPY module
    """
    RESET: PesActionEvent = None
    START: PesActionEvent = None
    STOP: PesActionEvent = None
# end class LedSpyActionEvent


@dataclass(frozen=True)
class LedSpyResumeEvent(PesEventMapInterface):
    """
    PES Resume Events for LED SPY module
    """
    pass
# end class LedSpyResumeEvent


@dataclass(frozen=True)
class LedSpyCpuEvent(PesCpuEventMapInterface):
    """
    PES-CPU Events for LED SPY module
    """
    FLUSH_FIFO: PesCpuEvent = PES_CPU_ACTION_LED_SPY_FIFO_FLUSH
# end class LedSpyCpuEvent


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class LedSpyModule(PesEventModuleInterface,
                   PesCpuEventModuleInterface,
                   ProducerModuleBaseClass,
                   DeviceTreeGenericModuleBaseClass):
    """
    Kosmos LED SPY Module class.
    """

    # PES Event maps related to the current module
    action_event = LedSpyActionEvent
    resume_event = LedSpyResumeEvent

    # PES CPU Event map related to the current module
    cpu_event = LedSpyCpuEvent

    def __init__(self, msg_id):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        """
        module_settings = ProducerModuleSettings(
            name=r'LED SPY',
            instance_id=None,  # Module is a singleton
            optional=True,
            msg_id=msg_id,
            buffer_size=(LED_SPY_BUFFER_SIZE - 1),
            fifo_size=(LED_SPY_FIFO_SIZE - 1),
            status_type=led_spy_status_t,
            status_state_reset_or_stop=LED_SPY_STATE_RESET_OR_STOP,
            status_state_started=LED_SPY_STATE_STARTED,
            status_state_enumvalues=led_spy_state_e__enumvalues,
            msg_cmd_status=MSG_ID_LED_SPY_CMD_STATUS,
            msg_cmd_reset=MSG_ID_LED_SPY_CMD_RESET,
            msg_cmd_start=MSG_ID_LED_SPY_CMD_START,
            msg_cmd_stop=MSG_ID_LED_SPY_CMD_STOP,
            msg_cmd_read_one=MSG_ID_LED_SPY_CMD_READ_1,
            msg_cmd_read_max=MSG_ID_LED_SPY_CMD_READ_MAX,
            data_type=led_spy_entry_t,
        )
        super().__init__(module_settings=module_settings)
    # end def __init__

    def flush_fifo_to_buffer(self):
        """
        Add a PES CPU Action: flush all remote FIFO entries into the remote buffer.
        """
        self.dt.pes_cpu.action(self.cpu_event.FLUSH_FIFO)
    # end def flush_fifo_to_buffer

    def set_channel_enable(self, channel_enable):
        """
        Set the LED module's "LED channel" parameter.
        This is a 32-bit parameter. Each bit encode the capture state of a particular LED.

        :param channel_enable: "LED channel" parameter
        :type channel_enable: ``led_spy_channel_enable_t or int``

        :raise ``AssertionError``: unexpected argument type or invalid argument value
        """
        assert isinstance(channel_enable, (led_spy_channel_enable_t, int)), channel_enable
        assert 0 <= channel_enable <= (1 << 32) - 1, f'32-bit positive integer only, got {channel_enable}'

        # Create request
        tx_frame = MessageFrame()
        tx_frame.frame.id = self.settings.msg_id
        tx_frame.frame.cmd = MSG_ID_LED_SPY_CMD_CHANNEL_ENABLE_WRITE
        tx_frame.frame.payload.led_spy_channel_enable = channel_enable

        # Send request
        txrx_msg = self.dt.fpga_transport.send_control_message_list([tx_frame])

        # Sanity checks
        self.dt.fpga_transport.check_status_message_replies(txrx_msg)
    # end def set_channel_enable

    def get_channel_enable(self):
        """
        Get the LED module's "LED channel" parameter.
        This is a 32-bit parameter. Each bit encode the capture state of a particular LED.

        :return: "LED channel" parameter
        :rtype: ``led_spy_channel_enable_t``
        """
        # Send request and get reply
        return self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                           msg_cmd=MSG_ID_LED_SPY_CMD_CHANNEL_ENABLE_READ)
    # end def get_channel_enable

    def set_gate_latch(self, gate_latch):
        """
        Set the LED module's "Clock gating" parameter.

        :param gate_latch: "Clock gating" parameter
        :type gate_latch: ``led_spy_gate_latch_t or int``

        :raise ``AssertionError``: unexpected argument type or invalid argument value
        """
        assert isinstance(gate_latch, (led_spy_gate_latch_t, int)), gate_latch
        assert 0 <= gate_latch <= (1 << 32) - 1, f'32-bit positive integer only, got {gate_latch}'

        # Create request
        tx_frame = MessageFrame()
        tx_frame.frame.id = self.settings.msg_id
        tx_frame.frame.cmd = MSG_ID_LED_SPY_CMD_GATE_LATCH_WRITE
        tx_frame.frame.payload.led_spy_gate_latch = gate_latch

        # Send request
        txrx_msg = self.dt.fpga_transport.send_control_message_list([tx_frame])

        # Sanity checks
        self.dt.fpga_transport.check_status_message_replies(txrx_msg)
    # end def set_gate_latch

    def get_gate_latch(self):
        """
        Get the LED module's "Clock gating" parameter.

        :return: "Clock gating" parameter
        :rtype: ``led_spy_gate_latch_t``
        """
        # Send request and get reply
        return self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                           msg_cmd=MSG_ID_LED_SPY_CMD_GATE_LATCH_READ)
    # end def get_gate_latch
# end class LedSpyModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
