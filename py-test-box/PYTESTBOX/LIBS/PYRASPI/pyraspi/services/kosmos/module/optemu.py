#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.optemu
:brief: Kosmos Optical Sensors Emulators module base class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/04/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from ctypes import c_int8
from dataclasses import dataclass
from dataclasses import replace
from typing import Dict
from typing import List
from typing import Tuple

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.module.model.registermap import MaskedRegVal
from pyraspi.services.kosmos.module.model.registermap import RegVal
from pyraspi.services.kosmos.module.model.registermap import reg_val_type
from pyraspi.services.kosmos.module.optemu_interfaces import Action
from pyraspi.services.kosmos.module.optemu_interfaces import MODE
from pyraspi.services.kosmos.module.optemu_interfaces import OptEmuHighLevelControlInterface
from pyraspi.services.kosmos.module.optemu_interfaces import OptEmuLowLevelControlInterface
from pyraspi.services.kosmos.module.optemu_interfaces import OptEmuModuleInterface
from pyraspi.services.kosmos.module.optemu_interfaces import OpticalSensorEmulatorModuleSettings
from pyraspi.services.kosmos.module.optemu_interfaces import OpticalSensorEmulatorState
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_OPT_EMU_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_OPT_EMU_CMD_START
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_OPT_EMU_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_OPT_EMU_CMD_STOP
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_OPT_EMU_CMD_UPDATE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_OPT_EMU_CMD_WRITE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_OPT_EMU_CMD_WRITE_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_DX_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_DX_MIN
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_DY_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_DY_MIN
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_LIFT_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_LIFT_MIN
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_REPEAT_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_REPEAT_MIN
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_SKIP_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_SKIP_MIN
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_FIFO_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_IDX_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_IDX_MIN
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_SEND_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_SEND_MIN
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_VAL_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_VAL_MIN
from pyraspi.services.kosmos.protocol.generated.messages import opt_emu_data_t
from pyraspi.services.kosmos.protocol.generated.messages import opt_emu_status_t
from pyraspi.services.kosmos.utils import sign_ext_3bits


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class OptEmuLowLevelControlMixin(OptEmuLowLevelControlInterface, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Low-Level Control Mixin Class.
    """
    @dataclass(frozen=True)
    class LiftLowLevelStatus:
        """
        Internal dataclass representing Lift feature status.
        """
        reg: reg_val_type       # Lift Register value
        status: bool            # Lift status (as read by firmware), True means lifted
        masked: reg_val_type    # Lift Register value, with lift status bits masked out
        cmd_idx: int            # Lift Command index
    # end class LiftLowLevelStatus

    def __init__(self, module):
        # See ``OptEmuLowLevelControlInterface.__init__``
        assert isinstance(module, OptEmuModuleInterface), module
        self.module = module
        self.reg_map = self.module.settings.reg_map

        # Initialize Low-level Control module
        self.reset()
    # end def __init__

    def reset(self):
        # See ``OptEmuLowLevelControlInterface.reset``
        # Init initial (previous) state and current state
        initial_state = OpticalSensorEmulatorState(regvs={reg.addr: reg.update(mask=0)
                                                          for reg in self.reg_map.regs.values()})
        current_state = OpticalSensorEmulatorState(regvs=initial_state.regvs.copy())
        self.states = [initial_state, current_state]

        # Enable conversion from Raw to Compressed instructions, whenever this is possible
        self.compress = True
    # end def reset

    @staticmethod
    def reg_state_diff(p_state, c_state):
        """
        Compute the Register differences between two Optical Sensor States.

        :param p_state: Previous state
        :type p_state: ``OpticalSensorEmulatorState``
        :param c_state: Current state
        :type c_state: ``OpticalSensorEmulatorState``

        :return: Register differences between two Optical Sensor States
        :rtype: ``Dict[reg_addr_type, Tuple[RegVal, RegVal]]``

        :raise ``AssertionError``: Register address mismatch
        """
        diff = {}
        for prev, curr in zip(p_state.regvs.items(), c_state.regvs.items()):
            assert prev[0] == curr[0], (prev, curr)  # ensure register addresses matches
            if prev[1] != curr[1]:
                diff[prev[0]] = (prev[1], curr[1])   # save register values
            # end if
        # end for
        return diff
    # end def reg_state_diff

    def update_reg(self, reg_addr, value=None, mask=0xFF):
        # See ``OptEmuLowLevelControlInterface.update_reg``
        # Shorthand notations
        c_state, p_state = self.current_state, self.previous_state

        reg = self.reg_map.regs[reg_addr]
        new_regv = replace(c_state.regvs[reg_addr])  # make copy of current register value
        new_regv = reg.update(value=value, mask=mask, regv=new_regv)  # update new register value
        if new_regv != c_state.regvs[reg_addr]:  # save new register value only if it differs from current
            c_state.regvs[reg_addr] = new_regv
        # end if
    # end def update_reg

    def finalize_state(self):
        # See ``OptEmuLowLevelControlInterface.finalize_state``
        # Shorthand notations
        p_state, c_state = self.previous_state, self.current_state

        # Generate commands list from registers diff
        reg_diff = self.reg_state_diff(p_state, c_state)
        for reg_addr, (p_regv, c_regv) in reg_diff.items():
            cmds = self._generate_commands(reg_addr=reg_addr, p_regv=p_regv, c_regv=c_regv)
            c_state.cmds.update(cmds)
        # end for

        # Generate instructions list from commands
        instructions = [self.module.get_raw_instruction(cmd_idx=cmd_idx, cmd_val=cmd_val)
                        for cmd_idx, cmd_val in c_state.cmds.items()]

        # Optimize instructions: convert RAW to COMPRESSED data format whenever possible
        if self.compress:
            instructions = self.compress_instructions(instructions)
        # end if

        # Handle empty update: add NOP instruction
        if not instructions:
            instructions.append(self.module.get_nop_instruction())
        # end if

        # Mark last instruction as UPDATE & SEND (only for RAW instruction)
        if self.module.test_instruction_is_raw(instructions[-1]):
            instructions[-1].raw.send = True
        # end if

        # Save instructions to current state
        c_state.instructions = instructions
    # end def finalize_state

    def commit_state(self):
        # See ``OptEmuLowLevelControlInterface.commit_state``
        self.module.extend(self.current_state.instructions)
    # end def commit_state

    def init_next_state(self):
        # See ``OptEmuLowLevelControlInterface.init_next_state``
        # new state starts with previous register values
        new_state = OpticalSensorEmulatorState(regvs=self.current_state.regvs.copy())
        self.states.append(new_state)
        return new_state
    # end def init_next_state

    def _generate_commands(self, reg_addr, p_regv, c_regv):
        """
        Generate Command index:value mapping, computed after a change of Register value.
        Command value is taken from Register value / set mask / clear mask, depending on register type and change.

        :param reg_addr: Register address
        :type reg_addr: ``reg_addr_type``
        :param p_regv: Previous state Register Value
        :type p_regv: ``RegVal or MaskedRegVal``
        :param c_regv: Current state Register Value
        :type c_regv: ``RegVal or MaskedRegVal``

        :return: Mapping of Command index to Command value
        :rtype: ``Dict[cmd_idx_type, Tuple[reg_val_type, reg_val_type]]``

        :raise ``TypeError``: Invalid type for Current state Register Value
        """
        cmd_idx = self.reg_map.reg2cmd[reg_addr]
        commands = {}
        if isinstance(c_regv, MaskedRegVal):
            if p_regv.set_mask != c_regv.set_mask:
                commands[cmd_idx[0]] = c_regv.set_mask
            # end if
            if p_regv.clr_mask != c_regv.clr_mask:
                commands[cmd_idx[1]] = c_regv.clr_mask
            # end if
        elif isinstance(c_regv, RegVal):
            if p_regv.value != c_regv.value:
                commands[cmd_idx] = c_regv.value
            # end if
        else:
            raise TypeError((reg_addr, p_regv, c_regv, cmd_idx))
        # end if
        return commands
    # end def _generate_commands

    def compress_instructions(self, instructions):
        """
        Process instructions list and replace some Raw instructions by a Compressed one if possible.

        RATIONALE:
        A compressed instruction can be generated if all the following conditions are met:
         - data change: current state of (dx, dy, lift, skip, repeat) differs from previous state
         - value bounds: (dx, dy, lift, skip, repeat) values are within limits of compressed data format
         - instruction count: a compressed instruction is generated only if it can replace more than one raw instruction

        RESULT:
         - if a compressed instruction is generated, return a new list of instructions composed of:
           - the raw instructions, excluding the (dx, dy, lift, skip, repeat) related instructions
           - the compressed instruction as the last item in the instructions list
         - if no compressed instruction could be generated:
           - return the unmodified input raw instructions list.

        :param instructions: Raw instructions list corresponding to one Sensor Model OpticalSensorEmulatorState update
        :type instructions: ``List[opt_emu_data_t]``

        :return: The optimized instructions list (RAWs + CMP) or the unmodified input Raw instructions list
        :rtype: ``List[opt_emu_data_t]``
        """
        # Shorthand notations
        c = self.reg_map.Commands
        r = self.reg_map.Registers
        t = self.reg_map.Types
        c_state = self.current_state

        # ==========================================
        # Check if state is eligible for compression

        # If there is zero or one optimizable command, it is not worth optimizing
        if len(self.reg_map.cmp_cmd_idx.intersection(c_state.cmds)) < 2:
            return instructions
        # end if

        # Check if current state registers are eligible to make a compressed instruction (test values bounds)
        dx, dy = self._get_signed_deltas(c_state)
        liftStat = self._get_lift(c_state)
        lift = False if liftStat is None else liftStat.status
        skip = c_state.cmds.get(c.SKIP, 0)
        repeat = c_state.cmds.get(c.REPEAT, 0)
        if not self.module.test_compressed_bitfields_bounds(dx=dx, dy=dy, lift=lift, skip=skip, repeat=repeat):
            return instructions
        # end if

        # =====================================
        # Perform instructions list compression

        # Construct the new instructions list by excluding some instructions from the input instructions list
        new_instructions = []
        for instr in instructions:
            if instr.raw.cmd_idx not in self.reg_map.cmp_cmd_idx:
                if liftStat is not None and not liftStat.masked and liftStat.cmd_idx == instr.raw.cmd_idx:
                    # Exclude LIFT instruction only if it can be entirely replaced by the compressed instruction
                    continue
                # end if
                new_instructions.append(instr)
            # end if
        # end for

        # Add new compressed instruction as last item in list
        cmp = self.module.get_compressed_instruction(dx=dx, dy=dy, lift=lift, skip=skip, repeat=repeat)
        new_instructions.append(cmp)

        return new_instructions
    # end def compress_instructions

    @abstractmethod
    def _get_signed_deltas(self, state):
        """
        Return the numerical value of DeltaX and DeltaY displacements, for the given state, as signed integers.
        This is taking into account the sensor model-specific Delta X/Y registers layout.

        :param state: OpticalSensorEmulatorState to compute DeltaX and DeltaY displacements from
        :type state: ``OpticalSensorEmulatorState``

        :return: DeltaX & DeltaY complete values, as signed integer
        :rtype:  ``Tuple[int, int]``
        """
        raise NotImplementedAbstractMethodError()
    # end def _get_signed_deltas

    @abstractmethod
    def _get_lift(self, state):
        """
        Return the Lift feature status.
        This is an abstraction layer as Lift status implementation varies a lot between sensors.

        :param state: OpticalSensorEmulatorState to compute Lift from
        :type state: ``OpticalSensorEmulatorState``

        :return: Lift status dataclass or ``None`` if Lift feature is not supported.
        :rtype:  ``OptEmuLowLevelControlMixin.LiftLowLevelStatus or None``
        """
        raise NotImplementedAbstractMethodError()
    # end def _get_lift
# end class OptEmuLowLevelControlMixin


class OptEmuHighLevelControlMixin(OptEmuHighLevelControlInterface, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator High-Level Control Mixin Class.
    """

    def __init__(self, module):
        # See ``OptEmuHighLevelControlInterface.__init__``
        assert isinstance(module, OptEmuModuleInterface), module
        self.module = module
        self.ll_ctrl = self.module.ll_ctrl
    # end def __init__

    def update(self, action, value):
        # See ``OptEmuHighLevelControlInterface.update``
        assert action in Action, action

        return self._update(action=action, value=value)
    # end def update

    @abstractmethod
    def _update(self, action, value):
        """
        Update the Optical Sensor Emulator current state, with the given action and value.
        This method shall be implemented in derived classes, to bring specialized update actions depending on emulator
        hardware.

        :param action: High-level action for updating the Optical Sensor Emulator OpticalSensorEmulatorState
        :type action: ``Action``
        :param value: High-level action value
        :type value: ``int or bool or None``
        """
        # Shorthand notations
        c = self.ll_ctrl.reg_map.Commands
        l = self.ll_ctrl.reg_map.Limits

        if action == Action.REPETITION:
            assert isinstance(value, int) and 0 <= value <= l.REPEAT_MAX, \
              f'REPETITION value {value} is out-of-bounds [0, {l.REPEAT_MAX}]'
            self.ll_ctrl.current_state.cmds[c.REPEAT] = value
        elif action == Action.SKIP:
            assert isinstance(value, int) and 0 <= value <= l.SKIP_MAX, \
              f'DELAY value {value} is out-of-bounds [0, {l.SKIP_MAX}]'
            self.ll_ctrl.current_state.cmds[c.SKIP] = value
        else:
            raise NotImplementedError(action)
        # end if
    # end def _update

    def commit(self):
        # See ``OptEmuHighLevelControlInterface.commit``
        self.ll_ctrl.finalize_state()
        self.ll_ctrl.commit_state()
        self.ll_ctrl.init_next_state()
    # end def commit
# end class OptEmuHighLevelControlMixin


class OptEmuModuleMixin(OptEmuModuleInterface, metaclass=ABCMeta):
    """
    Kosmos Optical Sensors Emulators module base class.
    """

    # update type hits
    ll_ctrl: OptEmuLowLevelControlMixin
    hl_ctrl: OptEmuHighLevelControlMixin

    def __init__(self, msg_id, instance_id, name, reg_map, ll_ctrl, hl_ctrl):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton
        :type instance_id: ``int``
        :param name: Optical Sensors Emulator Module given name
        :type name: ``str``
        :param reg_map: Optical Sensors Emulator Registers Class
        :type reg_map: ``Type[EmRegisterMapBase]``
        :param ll_ctrl: Optical Sensors Emulator Low-Level Control Class
        :type ll_ctrl: ``Type[OptEmuLowLevelControlMixin]``
        :param hl_ctrl: Optical Sensors Emulator High-Level Control Class
        :type hl_ctrl: ``Type[OptEmuHighLevelControlMixin]``

        :raise ``AssertionError``: invalid Control class types
        """
        module_settings = OpticalSensorEmulatorModuleSettings(
            name=name,
            instance_id=instance_id,
            optional=True,
            msg_id=msg_id,
            buffer_size=(OPT_EMU_BUFFER_SIZE - 1),
            fifo_size=(OPT_EMU_FIFO_SIZE - 1),
            status_type=opt_emu_status_t,
            msg_cmd_status=MSG_ID_OPT_EMU_CMD_STATUS,
            msg_cmd_reset=MSG_ID_OPT_EMU_CMD_RESET,
            data_type=opt_emu_data_t,
            msg_cmd_write_one=MSG_ID_OPT_EMU_CMD_WRITE_1,
            msg_cmd_write_max=MSG_ID_OPT_EMU_CMD_WRITE_MAX,
            msg_payload_name=r'opt_emu_fifo',
            msg_cmd_start=MSG_ID_OPT_EMU_CMD_START,
            msg_cmd_stop=MSG_ID_OPT_EMU_CMD_STOP,
            msg_cmd_update=MSG_ID_OPT_EMU_CMD_UPDATE,
            reg_map=reg_map()
        )
        super().__init__(module_settings=module_settings)

        assert issubclass(ll_ctrl, OptEmuLowLevelControlMixin), ll_ctrl
        assert issubclass(hl_ctrl, OptEmuHighLevelControlMixin), hl_ctrl
        self.ll_ctrl = ll_ctrl(module=self)
        self.hl_ctrl = hl_ctrl(module=self)

        self.register_reset_callback(self.ll_ctrl.reset)
    # end def __init__

    def start_emulator(self):
        # See ``OptEmuModuleInterface.start_emulator``
        # Send request
        status: opt_emu_status_t = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                                               msg_cmd=self.settings.msg_cmd_start)

        # Sanity checks
        error_list = self.is_status_reply_valid(status)
        if not (status.fifo_en or status.fifo_count == 0):
            # Checking FIFO count is required because very short test sequences may disable FIFO within a few CPU cycles
            error_list.append(f'[{self.name}] Unexpected module fifo_en state.\n{status}')
        # end if
        assert not error_list, '\n'.join(error_list)

        return status
    # end def start_emulator

    def stop_emulator(self):
        # See ``OptEmuModuleInterface.stop_emulator``
        # Send request
        status: opt_emu_status_t = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                                               msg_cmd=self.settings.msg_cmd_stop)

        # Sanity checks
        error_list = self.is_status_reply_valid(status)
        if status.fifo_en:
            error_list.append(f'[{self.name}] Unexpected module fifo_en state.\n{status}')
        # end if
        assert not error_list, '\n'.join(error_list)

        return status
    # end def stop_emulator

    def force_update(self):
        # See ``OptEmuModuleInterface.force_update``
        # Send request
        status: opt_emu_status_t = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                                               msg_cmd=self.settings.msg_cmd_update)

        # Sanity checks
        error_list = self.is_status_reply_valid(status)
        assert not error_list, '\n'.join(error_list)

        return status
    # end def force_update

    @classmethod
    def get_raw_instruction(cls, cmd_idx, cmd_val, send=False):
        # See ``OptEmuModuleInterface.get_raw_instruction``
        assert cls.test_raw_bitfields_bounds(cmd_idx, cmd_val, send), (cmd_idx, cmd_val, send)

        data = opt_emu_data_t()
        data.raw.send = send
        data.raw.cmd_idx = cmd_idx
        data.raw.cmd_val = cmd_val
        data.raw.mode = MODE.RAW
        return data
    # end def get_raw_instruction

    @classmethod
    def get_compressed_instruction(cls, dx=0, dy=0, lift=0, skip=0, repeat=0):
        # See ``OptEmuModuleInterface.get_compressed_instruction``
        assert cls.test_compressed_bitfields_bounds(dx, dy, lift, skip, repeat), (dx, dy, lift, skip, repeat)

        data = opt_emu_data_t()
        data.cmp.dx = dx
        data.cmp.dy = dy
        data.cmp.lift = lift
        data.cmp.skip = skip
        data.cmp.repeat = repeat
        data.cmp.mode = MODE.COMPRESSED
        return data
    # end def get_compressed_instruction

    def get_nop_instruction(self, send=False):
        # See ``OptEmuModuleInterface.get_nop_instruction``
        c = self.settings.reg_map.Commands
        return self.get_raw_instruction(cmd_idx=c.REPEAT, cmd_val=0, send=send)
    # end def get_nop_instruction

    @staticmethod
    def test_compressed_bitfields_bounds(dx=0, dy=0, lift=0, skip=0, repeat=0):
        # See ``OptEmuModuleInterface.test_compressed_bitfields_bounds``
        # CAUTION: Some arguments are evaluated as signed integers !
        return ((OPT_EMU_CMP_DX_MIN <= dx <= OPT_EMU_CMP_DX_MAX) and
                (OPT_EMU_CMP_DY_MIN <= dy <= OPT_EMU_CMP_DY_MAX) and
                (lift in [OPT_EMU_CMP_LIFT_MIN, OPT_EMU_CMP_LIFT_MAX]) and
                (OPT_EMU_CMP_SKIP_MIN <= skip <= OPT_EMU_CMP_SKIP_MAX) and
                (OPT_EMU_CMP_REPEAT_MIN <= repeat <= OPT_EMU_CMP_REPEAT_MAX))
    # end def test_compressed_bitfields_bounds

    @staticmethod
    def test_raw_bitfields_bounds(cmd_idx=0, cmd_val=0, send=0):
        # See ``OptEmuModuleInterface.test_raw_bitfields_bounds``
        # CAUTION: Some arguments are evaluated as signed integers !
        return ((OPT_EMU_RAW_IDX_MIN <= cmd_idx <= OPT_EMU_RAW_IDX_MAX) and
                (OPT_EMU_RAW_VAL_MIN <= cmd_val <= OPT_EMU_RAW_VAL_MAX) and
                (send in [OPT_EMU_RAW_SEND_MIN, OPT_EMU_RAW_SEND_MAX]))
    # end def test_raw_bitfields_bounds

    @staticmethod
    def test_instruction_is_raw(opt_emu_entry):
        # See ``OptEmuModuleInterface.test_instruction_is_raw``
        return opt_emu_entry.raw.mode == MODE.RAW
    # end def test_instruction_is_raw

    def test_instruction_is_nop(self, opt_emu_entry):
        # See ``OptEmuModuleInterface.test_instruction_is_nop``
        c = self.settings.reg_map.Commands
        return (self.test_instruction_is_raw(opt_emu_entry)
                and opt_emu_entry.raw.cmd_idx == c.REPEAT
                and opt_emu_entry.raw.cmd_val == 0)
    # end def test_instruction_is_nop

    def instruction_to_str(self, instruction):
        # See ``OptEmuModuleInterface.instruction_to_str``
        if self.test_instruction_is_raw(instruction):
            raw = instruction.raw
            return f'RAW: {"UP_SEND," if raw.send else "UPDATE, "} ' \
                   f'CMD={raw.cmd_idx:#04x}:{self.settings.reg_map.cmds[raw.cmd_idx].name[:12]:>12}, ' \
                   f'VAL={raw.cmd_val:#04x}:{c_int8(raw.cmd_val).value:4}'
        else:
            cmp = instruction.cmp
            return f'CMP: dX={cmp.dx:#03x}={sign_ext_3bits(cmp.dx):3}, ' \
                   f'dY={cmp.dy:#03x}={sign_ext_3bits(cmp.dy):3}, ' \
                   f'lift={cmp.lift}, skip={cmp.skip}, repeat={cmp.repeat}'
        # end if
    # end def instruction_to_str

    def instructions_to_str(self, instructions=None):
        # See ``OptEmuModuleInterface.instructions_to_str``
        return '\n'.join(map(self.instruction_to_str, self._buffer if instructions is None else instructions))
    # end def instructions_to_str
# end class OptEmuModuleMixin


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
