#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.kbdgtech
:brief: Kosmos Keyboard Gtech Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from enum import IntEnum

from pyraspi.services.kosmos.module.devicetree import DeviceTreeGenericModuleBaseClass
from pyraspi.services.kosmos.module.kbdmatrix import KbdActionEvent
from pyraspi.services.kosmos.module.kbdmatrix import KbdModuleSettings
from pyraspi.services.kosmos.module.kbdmatrix import KbdResumeEvent
from pyraspi.services.kosmos.module.module import ConsumerModuleBaseClass
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEvent
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventMapInterface
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.protocol.generated.messages import KBD_BANK_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COL_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_GTECH_ADDR_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_GTECH_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import KBD_GTECH_EMU_MODE_EMULATED
from pyraspi.services.kosmos.protocol.generated.messages import KBD_GTECH_EMU_MODE_REAL
from pyraspi.services.kosmos.protocol.generated.messages import KBD_GTECH_FIFO_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import KBD_GTECH_FUNC_MODE_ANALOG
from pyraspi.services.kosmos.protocol.generated.messages import KBD_GTECH_FUNC_MODE_LEGACY
from pyraspi.services.kosmos.protocol.generated.messages import KBD_LANE_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_ROW_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_EMU_MODE_EMULATED
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_EMU_MODE_REAL
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_FUNC_MODE_ANALOG
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_FUNC_MODE_LEGACY
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_WRITE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KBD_GTECH_CMD_WRITE_MAX
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_KBD_GTECH_EMU_MODE_EMULATED
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_KBD_GTECH_EMU_MODE_REAL
from pyraspi.services.kosmos.protocol.generated.messages import kbd_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import kbd_gtech_status_t


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class KbdCpuEvent(PesCpuEventMapInterface):
    """
    PES-CPU Events for GTECH KDB Emulator module
    """
    EMU_MODE_REAL: PesCpuEvent = PES_CPU_ACTION_KBD_GTECH_EMU_MODE_REAL
    EMU_MODE_EMULATED: PesCpuEvent = PES_CPU_ACTION_KBD_GTECH_EMU_MODE_EMULATED
# end class KbdCpuEvent


class KBD_GTECH_EMU_MODE(IntEnum):
    """
    Gtech KBD Emulator modes
    """
    REAL = KBD_GTECH_EMU_MODE_REAL
    EMULATED = KBD_GTECH_EMU_MODE_EMULATED
# end class KBD_GTECH_EMU_MODE


KBD_GTECH_EMU_MODE_2_MSG_CMD = {
    KBD_GTECH_EMU_MODE.REAL: MSG_ID_KBD_GTECH_CMD_EMU_MODE_REAL,
    KBD_GTECH_EMU_MODE.EMULATED: MSG_ID_KBD_GTECH_CMD_EMU_MODE_EMULATED,
}
MSG_CMD_2_KBD_GTECH_EMU_MODE = {
    MSG_ID_KBD_GTECH_CMD_EMU_MODE_REAL: KBD_GTECH_EMU_MODE.REAL,
    MSG_ID_KBD_GTECH_CMD_EMU_MODE_EMULATED: KBD_GTECH_EMU_MODE.EMULATED,
}


class KBD_GTECH_FUNC_MODE(IntEnum):
    """
    Gtech KBD Emulator functional modes
    """
    LEGACY = KBD_GTECH_FUNC_MODE_LEGACY
    ANALOG = KBD_GTECH_FUNC_MODE_ANALOG
# end class KBD_GTECH_FUNC_MODE


KBD_GTECH_FUNC_MODE_2_MSG_CMD = {
    KBD_GTECH_FUNC_MODE.LEGACY: MSG_ID_KBD_GTECH_CMD_FUNC_MODE_LEGACY,
    KBD_GTECH_FUNC_MODE.ANALOG: MSG_ID_KBD_GTECH_CMD_FUNC_MODE_ANALOG,
}
MSG_CMD_2_KBD_GTECH_FUNC_MODE = {
    MSG_ID_KBD_GTECH_CMD_FUNC_MODE_LEGACY: KBD_GTECH_FUNC_MODE.LEGACY,
    MSG_ID_KBD_GTECH_CMD_FUNC_MODE_ANALOG: KBD_GTECH_FUNC_MODE.ANALOG,
}


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KbdGtechModule(PesEventModuleInterface,
                     PesCpuEventModuleInterface,
                     ConsumerModuleBaseClass,
                     DeviceTreeGenericModuleBaseClass):
    """
    Kosmos Gtech KBD Module class. KBD stands for "Keyboard".
    Gtech is the name of the company that produce the Gtech chip onboard the keyboard that handle all the hall-effect
    analog keys.

    Refer to the System Level Specification document
      Galvatron Analog Keyboard Kosmos Emulator Project
      https://docs.google.com/document/d/1rLcB5X7VNgh3wG0p3ZGXUQwhK9sys4-xTgk_O_TdZFc
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
            name=r'KBD GTECH',
            instance_id=None,  # Module is a singleton
            optional=True,
            msg_id=msg_id,
            buffer_size=(KBD_GTECH_BUFFER_SIZE - 1),
            fifo_size=(KBD_GTECH_FIFO_SIZE - 1),
            status_type=kbd_gtech_status_t,
            msg_cmd_status=MSG_ID_KBD_GTECH_CMD_STATUS,
            msg_cmd_reset=MSG_ID_KBD_GTECH_CMD_RESET,
            data_type=kbd_entry_t,
            msg_cmd_write_one=MSG_ID_KBD_GTECH_CMD_WRITE_1,
            msg_cmd_write_max=MSG_ID_KBD_GTECH_CMD_WRITE_MAX,
            msg_payload_name=r'kbd_gtech',
            kbd_row_count=KBD_ROW_COUNT,
            kbd_col_count=KBD_COL_COUNT,
            kbd_addr_count=KBD_GTECH_ADDR_COUNT,
            kbd_lane_count=KBD_LANE_COUNT,
            kbd_bank_count=KBD_BANK_COUNT
        )
        super().__init__(module_settings=module_settings)

        self._func_mode: KBD_GTECH_FUNC_MODE
        self._emu_mode: KBD_GTECH_EMU_MODE
        self.__reset_mode()
        self.register_reset_callback(self.__reset_mode)
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
        Add a PES:WAIT:KBD instruction (wait while KBD module is busy)
        """
        self.dt.pes.wait(action=self.resume_event.READY)
    # end def pes_wait_kbd

    @property
    def emu_mode_val(self):
        """
        Return the current KBD Emulator Mode value. Read from hardware.

        :return: the current KBD Emulator Mode value, read from hardware
        :rtype: ``KBD_GTECH_EMU_MODE``
        """
        return KBD_GTECH_EMU_MODE(self.status().emu_mode_val)
    # end def property getter emu_mode_val

    @property
    def emu_mode(self):
        """
        Return the current KBD Emulator Mode command. Read from hardware.

        :return: the current KBD Emulator Mode command, read from hardware
        :rtype: ``KBD_GTECH_EMU_MODE``
        """
        return KBD_GTECH_EMU_MODE(self.status().emu_mode_cmd)
    # end def property getter emu_mode

    @emu_mode.setter
    def emu_mode(self, mode):
        """
        Add a PES CPU Action to set the Emulator Mode.

        :param mode: Mode to be set via PES CPU Action
        :type mode: ``KBD_GTECH_EMU_MODE``

        :raise ``ValueError``: Invalid mode, not in `KBD_GTECH_EMU_MODE`
        """
        if mode == KBD_GTECH_EMU_MODE.REAL:
            self.dt.pes_cpu.action(self.cpu_event.EMU_MODE_REAL)
        elif mode == KBD_GTECH_EMU_MODE.EMULATED:
            self.dt.pes_cpu.action(self.cpu_event.EMU_MODE_EMULATED)
        else:
            raise ValueError(mode)
        # end if
    # end def property setter emu_mode

    def emu_mode_real(self):
        """
        Add a PES CPU Action to set the Emulator Mode to REAL.
        """
        self.emu_mode = KBD_GTECH_EMU_MODE.REAL
    # end def emu_mode_real

    def emu_mode_emulated(self):
        """
        Add a PES CPU Action to set the Emulator Mode to EMULATED.
        """
        self.emu_mode = KBD_GTECH_EMU_MODE.EMULATED
    # end def emu_mode_emulated

    def emu_mode_msg(self, mode):
        """
        Send a message to set the Emulator Mode now, via direct SPI message.

        :param mode: Mode to be set via direct SPI message
        :type mode: ``KBD_GTECH_EMU_MODE``

        :return: KBD status message reply
        :rtype: ``kbd_gtech_status_t``

        :raise ``AssertionError``: KBD Emulator mode mismatch
        """
        status = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                             msg_cmd=KBD_GTECH_EMU_MODE_2_MSG_CMD[mode])
        assert status.emu_mode_cmd == mode, status
        return status
    # end def emu_mode_msg

    def check_func_mode(self):
        """
        Check values of KBD Functional Mode are the same in local Python cache and remote hardware FPGA.

        :raise ``AssertionError``: KBD functional mode mismatch
        """
        func_mode_hw = KBD_GTECH_FUNC_MODE(self.status().func_mode)
        assert self.func_mode == func_mode_hw, \
            f'Local func_mode={self.func_mode.name} does not match ' \
            f'hardware func_mode={func_mode_hw.name}'
    # end def check_func_mode

    @property
    def func_mode(self):
        """
        Return the current KBD Functional Mode. Read from hardware.

        :return: current KBD Functional Mode, as read from hardware
        :rtype: ``KBD_GTECH_FUNC_MODE``
        """
        return self._func_mode
    # end def property getter func_mode

    @func_mode.setter
    def func_mode(self, mode):
        """
        Add a PES CPU Action to set the Functional Mode, via direct SPI message.

        :param mode: Functional Mode to be set via direct SPI message
        :type mode: ``KBD_GTECH_FUNC_MODE``

        :raise ``AssertionError``: Functional mode was not set correctly
        """
        mode = KBD_GTECH_FUNC_MODE(mode)
        status = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                             msg_cmd=KBD_GTECH_FUNC_MODE_2_MSG_CMD[mode])
        assert status.func_mode == mode, (f'Cannot set func_mode={mode.name}, got status={status!s} '
                                          f'(func_mode={KBD_GTECH_FUNC_MODE(status.func_mode).name})')
        self._func_mode = mode
    # end def property setter func_mode

    def func_mode_legacy(self):
        """
        Set Gtech Emulator functional mode to LEGACY, via direct SPI message.
        """
        self.func_mode = KBD_GTECH_FUNC_MODE.LEGACY
    # end def func_mode_legacy

    def func_mode_analog(self):
        """
        Set Gtech Emulator functional mode to ANALOG, via direct SPI message.
        """
        self.func_mode = KBD_GTECH_FUNC_MODE.ANALOG
    # end def func_mode_analog

    # Private method declaration
    def __reset_mode(self):
        """
        Reset modes to default.
        Note: NEVER call this method from anywhere else than this module's init method and reset callback.
        """
        self._emu_mode = KBD_GTECH_EMU_MODE.REAL      # FIXME local variable _emu_mode is not used
        self._func_mode = KBD_GTECH_FUNC_MODE.LEGACY  # FIXME local variable _func_mode is not used
    # end def __reset_mode

# end class KbdGtechModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
