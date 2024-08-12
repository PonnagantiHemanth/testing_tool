#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.optemu_interfaces
:brief: Kosmos Optical Sensors Emulators module interface classes
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/04/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from enum import IntEnum
from enum import auto
from enum import unique
from typing import Dict
from typing import List

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.module.devicetree import DeviceTreeGenericModuleBaseClass
from pyraspi.services.kosmos.module.model.optemu.base import OptEmuRegisterMapBase
from pyraspi.services.kosmos.module.model.registermap import RegVal
from pyraspi.services.kosmos.module.model.registermap import cmd_idx_type
from pyraspi.services.kosmos.module.model.registermap import cmd_val_type
from pyraspi.services.kosmos.module.model.registermap import reg_addr_type
from pyraspi.services.kosmos.module.module import ConsumerModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleSettings
from pyraspi.services.kosmos.module.pesevents import PesActionEvent
from pyraspi.services.kosmos.module.pesevents import PesEventMapInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesResumeEvent
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_MODE
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_MODE
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_UPDATE
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_RAW_UPDATE_SEND
from pyraspi.services.kosmos.protocol.generated.messages import msg_cmd_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import opt_emu_data_t
from pyraspi.services.kosmos.protocol.generated.messages import opt_emu_status_t


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

@unique
class Action(Enum):
    """
    Kosmos Optical Sensor Emulator High-Level Actions
    """
    REPETITION = auto()
    SKIP = auto()
    DX = auto()
    DY = auto()
    LIFT = auto()
    STATUS_MOTION = auto()
    POWER_MODE_REST2 = auto()
    POWER_MODE_SLEEP = auto()
# end class Action


@unique
class MODE(IntEnum):
    """
    Optical Sensor Emulator Instruction data format mode: Raw or Compressed
    """
    RAW = OPT_EMU_RAW_MODE
    COMPRESSED = OPT_EMU_CMP_MODE
# end class MODE


@unique
class RAW_SEND(IntEnum):
    """
    Optical Sensor Emulator Raw Instruction Memory buffer update option: Update only or Update & Send.

    RATIONALE:
     * Setting a Raw instruction with `UPDATE`` will only update the Emulator's Model Data memory buffer,
       using the data contained in the Raw instruction.

     * Selecting ``UPDATE_SEND`` will first update the Emulator's Model Data memory buffer, then signal to the Emulator
       that the Model Data memory buffer can be copied/committed to the Emulated register array.
    """
    UPDATE = OPT_EMU_RAW_UPDATE
    UPDATE_SEND = OPT_EMU_RAW_UPDATE_SEND
# end class RAW_SEND


@dataclass(frozen=True)
class OpticalSensorActionEvent(PesEventMapInterface):
    """
    PES Action Events for Optical Sensor Emulator
    """
    RESET: PesActionEvent = None
    START: PesActionEvent = None
    STOP: PesActionEvent = None
    UPDATE: PesActionEvent = None
# end class OpticalSensorActionEvent


@dataclass(frozen=True)
class OpticalSensorResumeEvent(PesEventMapInterface):
    """
    PES Resume Events for Optical Sensor Emulator
    """
    SETUP_DONE: PesResumeEvent = None
    UPDATE_DONE: PesResumeEvent = None
    FIFO_EMPTY: PesResumeEvent = None
    FIFO_UNDERRUN: PesResumeEvent = None
# end class OpticalSensorResumeEvent


@dataclass(frozen=True)
class OpticalSensorEmulatorModuleSettings(ConsumerModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``msg_cmd_start``: Start Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``msg_cmd_stop``: Stop Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``reg_map``: Optical Sensors Emulator Registers Map
    """
    msg_cmd_start: int
    msg_cmd_stop: int
    msg_cmd_update: int
    reg_map: OptEmuRegisterMapBase

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        assert self.msg_cmd_start in msg_cmd_e__enumvalues, self.msg_cmd_start
        assert self.msg_cmd_stop in msg_cmd_e__enumvalues, self.msg_cmd_stop
        assert self.msg_cmd_update in msg_cmd_e__enumvalues, self.msg_cmd_update
        assert isinstance(self.reg_map, OptEmuRegisterMapBase), self.reg_map
    # end def __post_init__
# end class OpticalSensorEmulatorModuleSettings


@dataclass
class OpticalSensorEmulatorState:
    """
    Optical Sensor Emulator OpticalSensorEmulatorState, representing the Registers, Commands and instructions for
    Sensor Data Model update.
    """
    regvs: Dict[reg_addr_type, RegVal]
    cmds: Dict[cmd_idx_type, cmd_val_type] = field(default_factory=dict)
    instructions: List[opt_emu_data_t] = field(default_factory=list)
# end class OpticalSensorEmulatorState


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class OptEmuModuleInterface(ConsumerModuleBaseClass,
                            PesEventModuleInterface,
                            DeviceTreeGenericModuleBaseClass,
                            metaclass=ABCMeta):
    """
    Kosmos Optical Sensors Emulators module Interface class.
    """

    # PES Event maps related to the current module
    action_event = OpticalSensorActionEvent
    resume_event = OpticalSensorResumeEvent

    ll_ctrl: 'OptEmuLowLevelControlInterface'
    hl_ctrl: 'OptEmuHighLevelControlInterface'

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``OpticalSensorEmulatorModuleSettings``
        """
        return self._settings
    # end def property getter settings

    @abstractmethod
    def start_emulator(self):
        """
        Start the sensor emulator module immediately, independently of Sequencer module.

        Actions:
          - Enable FIFO Underrun interrupt
          - Enable FIFO threshold interrupts
          - Enable FIFO read operations from FPGA

        :return: Module's status after start of the module.
        :rtype: ``opt_emu_status_t``

        :raise ``AssertionError``: Invalid or unexpected status values, after start of the module
        """
        raise NotImplementedAbstractMethodError()
    # end def start_emulator

    @abstractmethod
    def stop_emulator(self):
        """
        Stop the sensor emulator module immediately, independently of Sequencer module.

        Actions:
          - Disable FIFO read operations from FPGA
          - Preserve module buffer and FIFO content
          - Preserve module interrupt source state

        :return: Module's status after stop of the module.
        :rtype: ``opt_emu_status_t``

        :raise ``AssertionError``: Invalid or unexpected status values, after stop of the module
        """
        raise NotImplementedAbstractMethodError()
    # end def stop_emulator

    @abstractmethod
    def force_update(self):
        """
        Trigger a single Sensor Model Data update immediately, independently of Sequencer module.
        Force an update of the emulated Sensor Model data (Delta X/Y registers and others).
        To be used when the DUT is not polling the Sensor via SPI (because it is in sleep mode for example).

        Action:
          - Send an "update_force" event to the Sensor FPGA module

        :return: Module's status after update of the module.
        :rtype: ``opt_emu_status_t``

        :raise ``AssertionError``: Invalid or unexpected status values, after update of the module
        """
        raise NotImplementedAbstractMethodError()
    # end def force_update

    @staticmethod
    @abstractmethod
    def get_raw_instruction(cmd_idx, cmd_val, send=False):
        """
        Return an OpticalSensor instruction, in Raw data format.

        :param cmd_idx: Command index: 64 addresses, mapped to internal registers or to custom functions
        :type cmd_idx: ``int``
        :param cmd_val: Command value
        :type cmd_val: ``int``
        :param send:  Send Hardware Memory buffer after processing this instruction, default is ``False`` - OPTIONAL
        :type send: ``bool``

        :return: OpticalSensor instruction, in Raw data format
        :rtype: ``opt_emu_data_t``

        :raise ``AssertionError``: Out-of-bounds argument value
        """
        raise NotImplementedAbstractMethodError()
    # end def get_raw_instruction

    @abstractmethod
    def get_nop_instruction(self, send=False):
        """
        Return an OpticalSensor NOP instruction, in Raw data format.

        :param send:  Send Hardware Memory buffer after processing this instruction, default is ``False`` - OPTIONAL
        :type send: ``bool``

        :return: OpticalSensor NOP instruction, in Raw data format
        :rtype: ``opt_emu_data_t``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_nop_instruction

    @staticmethod
    @abstractmethod
    def get_compressed_instruction(dx=0, dy=0, lift=0, skip=0, repeat=0):
        """
        Return an OpticalSensor instruction, in Compressed data format.

        Note 1: Hardware Memory buffer is always sent after processing each compressed instructions.
                This is similar to using ``RAW_SEND.UPDATE_SEND`` for Raw instructions.

        Note 2: Argument values are constrained (min & max bounds).
                Refer to ``OptEmuModuleMixin.test_compressed_bitfields_bounds`` for lower and upper
                limits.

        Arguments explanation:

        ``dx``, ``dy``:
            Set values of `Delta X` and `Delta Y` displacements.
            Values are intended to be passed as a signed integers.

        ``lift``:
            Set the Optical Sensor Lift state.
            ``True``: Mouse is lifted, in the air, the optical sensor lost focus.
            ``False``: Mouse is put on a surface, the optical sensor is focused.
            Lift state is not affected by Skip and Repeat features.

        ``Skip``:
            This is an emulator-specific feature.
            Set the number of Sensor Model updates that shall occur with Delta X/Y registers cleared to zero,
            after the present Sensor Model update is being process by the emulator.
            This allows to delay the application of the next Sensor Model update.

        ``Repeat`:
            This is an emulator-specific feature.
            Set the number of time the present Sensor Model update shall be repeated.
            This allows to use one instruction for a continuous displacement.

        ``Skip`` and ``Repeat` arguments can be used together to repeat the same displacement, at a slower pace.

        :param dx: DeltaX, as signed int, defaults to zero - OPTIONAL
        :type dx: ``int``
        :param dy: DeltaY, as signed int, defaults to zero - OPTIONAL
        :type dy: ``int``
        :param lift: Lift, as unsigned int or bool, defaults to zero - OPTIONAL
        :type lift: ``int or bool``
        :param skip: Sensor model update Skip count, as signed int, defaults to zero - OPTIONAL
        :type skip: ``int``
        :param repeat: Sensor model update Repeat count, as signed int, defaults to zero - OPTIONAL
        :type repeat: ``int``

        :return: OpticalSensor instruction, in compressed data format.
        :rtype: ``opt_emu_data_t``

        :raise ``AssertionError``: Out-of-bounds argument value
        """
        raise NotImplementedAbstractMethodError()
    # end def get_compressed_instruction

    @staticmethod
    @abstractmethod
    def test_compressed_bitfields_bounds(dx=0, dy=0, lift=0, skip=0, repeat=0):
        """
        Test if the all the Compressed instruction bitfield values are within bounds.

        Refer to ``OptEmuModuleInterface.get_compressed_instruction()`` method for argument details.

        :param dx: DeltaX, as signed int, defaults to zero - OPTIONAL
        :type dx: ``int``
        :param dy: DeltaY, as signed int, defaults to zero - OPTIONAL
        :type dy: ``int``
        :param lift: Lift, as unsigned int or bool, defaults to zero - OPTIONAL
        :type lift: ``int or bool``
        :param skip: Sensor model update Skip count, as signed int, defaults to zero - OPTIONAL
        :type skip: ``int``
        :param repeat: Sensor model update Repeat count, as signed int, defaults to zero - OPTIONAL
        :type repeat: ``int``

        :return: ``True`` if the arguments values fit within in a Compressed instruction, else ``False``
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def test_compressed_bitfields_bounds

    @staticmethod
    @abstractmethod
    def test_raw_bitfields_bounds(cmd_idx=0, cmd_val=0, send=False):
        """
        Test if the all the Raw instruction bitfield values are within bounds.

        :param cmd_idx: Command Index, as unsigned int, defaults to zero - OPTIONAL
        :type cmd_idx: ``int``
        :param cmd_val: Command Value, as either signed or unsigned int, defaults to zero - OPTIONAL
        :type cmd_val: ``int``
        :param send: Command Send flag, as unsigned int or bool, defaults to ``False`` - OPTIONAL
        :type send: ``int or bool``

        :return: ``True`` if the arguments values fit within a Raw instruction, else ``False``
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def test_raw_bitfields_bounds

    @staticmethod
    @abstractmethod
    def test_instruction_is_raw(opt_emu_entry):
        """
        Test if the instruction is using Raw or Compressed data format.

        :param opt_emu_entry: an Optical Sensor Emulator instruction
        :type opt_emu_entry: ``opt_emu_data_t``

        :return: ``True`` if the instruction is RAW else ``False``
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def test_instruction_is_raw

    @abstractmethod
    def test_instruction_is_nop(self, opt_emu_entry):
        """
        Test if the instruction is a NOP instruction.

        :param opt_emu_entry: an Optical Sensor Emulator instruction
        :type opt_emu_entry: ``opt_emu_data_t``

        :return: ``True`` if the instruction is NOP else ``False``
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def test_instruction_is_nop

    @classmethod
    @abstractmethod
    def instruction_to_str(cls, opt_emu_entry):
        """
        Return an Optical Sensor Emulator instruction as a human-readable string.
        Refer to ``instructions_to_str()`` for examples.

        :param opt_emu_entry: an Optical Sensor Emulator instruction
        :type opt_emu_entry: ``opt_emu_data_t``

        :return: OpticalSensor instruction as a human-readable string
        :rtype: ``str``
        """
        raise NotImplementedAbstractMethodError()
    # end def instruction_to_str

    @classmethod
    @abstractmethod
    def instructions_to_str(cls, instructions=None):
        """
        Return an OpticalSensor instructions list as a human-readable text.
        Use the module's local instructions buffer if no argument is passed.

        Example list:
            CMP: dX=0x1=  1, dY=0x6= -2, lift=0, skip=0, repeat=0
            CMP: dX=0x0=  0, dY=0x4= -4, lift=0, skip=0, repeat=0
            RAW: UPDATE,  CMD=0x05:  dX, VAL=0x09:   9
            RAW: UPDATE,  CMD=0x06:  dY, VAL=0xf8:  -8
            RAW: UP_SEND, CMD=0x07: dXY, VAL=0x0f:  15

        :param instructions: list of OpticalSensor instructions,
                             defaults to None (use the module's local instruction buffer instead) - OPTIONAL
        :type instructions: ``list[opt_emu_data_t] or None``

        :return: OpticalSensor instruction list as a human-readable text
        :rtype: ``str``
        """
        raise NotImplementedAbstractMethodError()
    # end def instructions_to_str
# end class OptEmuModuleInterface


class OptEmuLowLevelControlInterface(metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Low-Level Control Mixin Class.
    """
    module: OptEmuModuleInterface
    reg_map: OptEmuRegisterMapBase

    # Optical Sensor Model State history
    states: List[OpticalSensorEmulatorState]

    # Enable / Disable conversion from Raw to Compressed instructions, whenever this is possible
    compress: bool

    @abstractmethod
    def __init__(self, module):
        """
        :param module: Instance of OptEmuModuleInterface
        :type module: ``OptEmuModuleInterface``
        """
        raise NotImplementedAbstractMethodError()
    # end def __init__

    @abstractmethod
    def reset(self):
        """
        Reset the Optical Sensor Model OpticalSensorEmulatorState History and initialize initial current and previous states.
        """
        raise NotImplementedAbstractMethodError()
    # end def reset

    @property
    def current_state(self):
        """
        Return the Optical Sensor Model's current State

        :return: Optical Sensor Model's current State
        :rtype: ``OpticalSensorEmulatorState``
        """
        return self.states[-1]  # current state is last item in list
    # end def property getter current_state

    @property
    def previous_state(self):
        """
        Return the Optical Sensor Model's previous State

        :return: Optical Sensor Model's previous State
        :rtype: ``OpticalSensorEmulatorState``
        """
        return self.states[-2]  # previous state is before last item in list
    # end def property getter previous_state

    @abstractmethod
    def update_reg(self, reg_addr, value=None, mask=0xFF):
        """
        Update an Optical Sensor Model Current OpticalSensorEmulatorState Register value.
        :param reg_addr: Optical Sensor Model's register address
        :type reg_addr: ``int``
        :param value: value to be set to the Register Value, defaults to None - OPTIONAL
        :type value: ``int or None``
        :param mask: mask selecting Register Value bits to clear/set depending on value, defaults to 0xFF - OPTIONAL
        :type mask: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def update_reg

    @abstractmethod
    def finalize_state(self):
        """
        Finalize current OpticalSensorEmulatorState of Optical Sensor:
         1) Generate Commands list from Register differences from previous OpticalSensorEmulatorState.
         2) Generate Raw Instructions list from the Commands.
         3) Compress the Raw Instructions list using a Compressed Instruction, if enabled and applicable.
         4) Save current OpticalSensorEmulatorState and initialize the new next OpticalSensorEmulatorState.
        """
        raise NotImplementedAbstractMethodError()
    # end def finalize_state

    @abstractmethod
    def commit_state(self):
        """
        Copy the current OpticalSensorEmulatorState Instructions list at the end of the Optical Sensor Emulator module local buffer.
        """
        raise NotImplementedAbstractMethodError()
    # end def commit_state

    @abstractmethod
    def init_next_state(self):
        """
        Create a new Optical Sensor Model OpticalSensorEmulatorState and append it to the OpticalSensorEmulatorState history.
        Current OpticalSensorEmulatorState is becoming Previous OpticalSensorEmulatorState, and newly created OpticalSensorEmulatorState is now Current OpticalSensorEmulatorState.
        """
        raise NotImplementedAbstractMethodError()
    # end def init_next_state
# end class OptEmuLowLevelControlInterface


class OptEmuHighLevelControlInterface(metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator High-Level Control Mixin Class.
    """

    module: OptEmuModuleInterface
    ll_ctrl: OptEmuLowLevelControlInterface

    @abstractmethod
    def __init__(self, module):
        """
        :param module: Optical Sensors Emulator module
        :type module: ``OptEmuModuleInterface``
        """
        raise NotImplementedAbstractMethodError()
    # end def __init__

    @abstractmethod
    def update(self, action, value):
        """
        Update the Optical Sensor Emulator current state, with the given action and value.

        Notes:
         - Call ``update(action, value)`` method as many times as required.
         - Duplicate actions or value rollbacks have no impact. Only the OpticalSensorEmulatorState difference matters.
         - Call ``commit()`` once done with updates.

        :param action: High-level action for updating the Optical Sensor Emulator OpticalSensorEmulatorState
        :type action: ``Action``
        :param value: High-level action value
        :type value: ``int or bool or None``
        """
        raise NotImplementedAbstractMethodError()
    # end def update

    @abstractmethod
    def commit(self):
        """
        Commit the Optical Sensor Emulator current OpticalSensorEmulatorState:
         1) Generate Emulator instructions
         2) Add Emulator instructions to the module's local buffer
         3) Initialize next Emulator OpticalSensorEmulatorState
        """
        raise NotImplementedAbstractMethodError()
    # end def commit
# end class OptEmuHighLevelControlInterface

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
