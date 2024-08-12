#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.model.optemu.pixart
:brief: Kosmos Module PixArt Family Optical Sensors Emulator Models Package
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/05/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from abc import ABCMeta
from enum import IntFlag
from enum import unique
from typing import Dict
from typing import Set
from typing import Tuple
from typing import Union

from pyraspi.services.kosmos.module.model.optemu.base import OptEmu12BitsRegisterMapBase
from pyraspi.services.kosmos.module.model.optemu.base import OptEmu16BitsRegisterMapBase
from pyraspi.services.kosmos.module.model.optemu.base import OptEmuRegisterMapBase
from pyraspi.services.kosmos.module.model.registermap import BIT_0
from pyraspi.services.kosmos.module.model.registermap import BIT_1
from pyraspi.services.kosmos.module.model.registermap import BIT_2
from pyraspi.services.kosmos.module.model.registermap import BIT_3
from pyraspi.services.kosmos.module.model.registermap import BIT_4
from pyraspi.services.kosmos.module.model.registermap import BIT_5
from pyraspi.services.kosmos.module.model.registermap import BIT_6
from pyraspi.services.kosmos.module.model.registermap import BIT_7
from pyraspi.services.kosmos.module.model.registermap import Command
from pyraspi.services.kosmos.module.model.registermap import MaskedRegister
from pyraspi.services.kosmos.module.model.registermap import Register
from pyraspi.services.kosmos.module.model.registermap import RegisterBase
from pyraspi.services.kosmos.module.model.registermap import cmd_idx_type
from pyraspi.services.kosmos.module.model.registermap import reg_addr_type


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PixArtRegisterMapBase(OptEmuRegisterMapBase, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Register Map, for PixArt Optical Sensors family.

    PixArt Optical Sensors Specifications:
     - PAW3266DB : https://drive.google.com/file/d/1b1QdpFQ5JkBHtZrK9Yfhh7MnAP2mfwug
     - PMW3816DM : https://drive.google.com/file/d/1Gw4C6Hek6xse0yNRDOvfLCH19zkFIPyb
    """

    class Types(OptEmuRegisterMapBase.Types):
        # See ``OptEmuRegisterMapBase.Types``
        @unique
        class MOTION(IntFlag):
            """
            Sensor Motion Status Register.
            """
            pass  # Register bits will be defined in derived classes
        # end class MOTION

        @unique
        class PERFORMANCE(IntFlag):
            """
            Sensor Performance Register.
            """
            pass  # Register bits will be defined in derived classes
        # end class PERFORMANCE

        @unique
        class OBSERVATION(IntFlag):
            """
            Sensor Observation Status Register.
            """
            pass  # Register bits will be defined in derived classes
        # end class OBSERVATION

        @unique
        class XY_DIRECTION(IntFlag):
            """
            Sensor XY Direction Register.
            """
            pass  # Register bits will be defined in derived classes
        # end class XY_DIRECTION
    # end class Types

    class Registers(OptEmuRegisterMapBase.Registers):
        """
        Register Address Map.
          * PAW3266 datasheet: Register List, section 8.1, page 27
        """
        MOTION: int
        SQUAL: int
        PERFORMANCE: int
        OBSERVATION: int
        POWER_UP_RESET = 0x3A
        SHUTDOWN = 0x3B
    # end class Registers

    class Commands(OptEmuRegisterMapBase.Commands):
        # See ``OptEmuRegisterMapBase.Commands``
        MOTION_SET = 0x02
        MOTION_CLR = 0x12
        OBSERVATION_SET: int
        OBSERVATION_CLR: int
        POWER_UP_RESET = 0x3A
        SHUTDOWN = 0x3B
    # end class Commands

    # Register Mapping: Register address to Register dataclass
    regs: Dict[reg_addr_type, RegisterBase] = {
        Registers.POWER_UP_RESET: Register(addr=Registers.POWER_UP_RESET, name='Power Up Reset', type=int,
                                           desc='Write 0x5a to this register to reset the chip, all settings will '
                                                'revert to default values.'),
        Registers.SHUTDOWN: Register(addr=Registers.SHUTDOWN, name='Shutdown', type=int,
                                     desc='Write 0xe7 to set the chip to shutdown mode.'),
    }

    # Command Mapping: Command index to Command dataclass
    cmds: Dict[cmd_idx_type, Command] = {
        **OptEmuRegisterMapBase.cmds,
        Commands.MOTION_SET: Command(idx=Commands.MOTION_SET, name='Motion_set',
                                     desc='Motion Status Register: Force-Set Mask'),
        Commands.MOTION_CLR: Command(idx=Commands.MOTION_CLR, name='Motion_clr',
                                     desc='Motion Status Register: Force-Clr Mask'),
        Commands.POWER_UP_RESET: Command(idx=Commands.POWER_UP_RESET, name='Power-up Reset',
                                         desc='Write 0x5a to this register to reset the chip, all settings will '
                                              'revert to default values.'),
        Commands.SHUTDOWN: Command(idx=Commands.SHUTDOWN, name='Shutdown',
                                   desc='Write 0xe7 to set the chip to shutdown mode.'),
    }

    # Register to Command Mapping: Register address to Command index(es)
    reg2cmd: Dict[cmd_idx_type, Union[int, Tuple[int, int]]] = {
        Registers.POWER_UP_RESET: Commands.POWER_UP_RESET,
        Registers.SHUTDOWN: Commands.SHUTDOWN,
    }
# end class PixArtRegisterMapBase


class PixArt12BitsRegisterMap(OptEmu12BitsRegisterMapBase, PixArtRegisterMapBase, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Register Map, for PixArt 12-bit Optical Sensors family.

    PixArt Optical Sensors Specifications:
     - PAW3266DB : https://drive.google.com/file/d/1b1QdpFQ5JkBHtZrK9Yfhh7MnAP2mfwug
    """

    class Types(PixArtRegisterMapBase.Types, OptEmu12BitsRegisterMapBase.Types):
        # See ``PixArtRegisterMapBase.Types`` and to ``OptEmu12BitsRegisterMapBase.Types``
        pass
    # end class Types

    class Registers(PixArtRegisterMapBase.Registers, OptEmu12BitsRegisterMapBase.Registers):
        # See ``PixArtRegisterMapBase.Registers`` and to ``OptEmu12BitsRegisterMapBase.Registers``
        DELTA_X_L = 0x03
        DELTA_Y_L = 0x04
        DELTA_XY_H = 0x05
    # end class Registers

    class Commands(PixArtRegisterMapBase.Commands, OptEmu12BitsRegisterMapBase.Commands):
        # See ``PixArtRegisterMapBase.Commands`` and to ``OptEmu12BitsRegisterMapBase.Commands``
        DELTA_X_L = 0x03
        DELTA_Y_L = 0x04
        DELTA_XY_H = 0x05
    # end class Commands

    class Limits(OptEmu12BitsRegisterMapBase.Limits):
        # See ``OptEmu12BitsRegisterMapBase.Limits``
        pass
    # end class Limits

    # Register Mapping: Register address to Register dataclass
    regs = {
        **PixArtRegisterMapBase.regs,
    }

    # Command Mapping: Command index to Command dataclass
    cmds = {
        **PixArtRegisterMapBase.cmds,
    }

    # Register to Command Mapping: Register address to Command index(es)
    reg2cmd = {
        **PixArtRegisterMapBase.reg2cmd,
    }
# end class PixArt12BitsRegisterMap


class PixArt16BitsRegisterMap(OptEmu16BitsRegisterMapBase, PixArtRegisterMapBase, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Register Map, for PixArt 16-bit Optical Sensors family.

    PixArt Optical Sensors Specifications:
     - PMW3816DM : https://drive.google.com/file/d/1Gw4C6Hek6xse0yNRDOvfLCH19zkFIPyb
    """

    class Types(PixArtRegisterMapBase.Types, OptEmu16BitsRegisterMapBase.Types):
        # See ``PixArtRegisterMapBase.Types`` and to ``OptEmu16BitsRegisterMapBase.Types``
        pass
    # end class Types

    class Registers(PixArtRegisterMapBase.Registers, OptEmu16BitsRegisterMapBase.Registers):
        # See ``PixArtRegisterMapBase.Registers`` and to ``OptEmu16BitsRegisterMapBase.Registers``
        DELTA_X_L = 0x03
        DELTA_X_H = 0x04
        DELTA_Y_L = 0x05
        DELTA_Y_H = 0x06
        pass
    # end class Registers

    class Commands(PixArtRegisterMapBase.Commands, OptEmu16BitsRegisterMapBase.Commands):
        # See ``PixArtRegisterMapBase.Commands`` and to ``OptEmu16BitsRegisterMapBase.Commands``
        DELTA_X_L = 0x03
        DELTA_X_H = 0x04
        DELTA_Y_L = 0x05
        DELTA_Y_H = 0x06
        pass
    # end class Commands

    class Limits(OptEmu16BitsRegisterMapBase.Limits):
        # See ``OptEmu16BitsRegisterMapBase.Limits``
        pass
    # end class Limits

    # Register Mapping: Register address to Register dataclass
    regs = {
        **PixArtRegisterMapBase.regs,
    }

    # Command Mapping: Command index to Command dataclass
    cmds = {
        **PixArtRegisterMapBase.cmds,
    }

    # Register to Command Mapping: Register address to Command index(es)
    reg2cmd = {
        **PixArtRegisterMapBase.reg2cmd,
    }
# end class PixArt16BitsRegisterMap


class Paw3266RegisterMap(PixArt12BitsRegisterMap):
    """
    Kosmos Optical Sensor Emulator Register Map, for PixArt 12-bit PAW3266 Optical Sensor.

    PixArt Optical Sensors Specifications:
     - PAW3266DB : https://drive.google.com/file/d/1b1QdpFQ5JkBHtZrK9Yfhh7MnAP2mfwug
    """

    class Types(PixArt12BitsRegisterMap.Types):
        # See ``PixArt12BitsRegisterMap.Types``
        @unique
        class MOTION(PixArt12BitsRegisterMap.Types.MOTION):
            """
            Sensor Motion Status Register.
              * PAW3266 datasheet: section 8.2.2 Motion Data status, page 28
            """
            OVF = BIT_4  # Motion overflow, DeltaY and/or DeltaX buffer has overflowed since last report.
            MOT = BIT_7  # Motion occurred since last report. Also indicate data ready for Delta registers.
        # end class MOTION

        @unique
        class PERFORMANCE(PixArt12BitsRegisterMap.Types.PERFORMANCE):
            """
            Sensor Performance Register.
              * PAW3266 datasheet: section 8.2.3 Device Settings, page 32
            """
            AWAKE = BIT_7  # set bit to force awake enable (engineering & debug only)
        # end class PERFORMANCE

        @unique
        class OBSERVATION(PixArt12BitsRegisterMap.Types.OBSERVATION):
            """
            Sensor Observation Register.
              * PAW3266 datasheet: section 8.2.3 Device Settings, page 34
            """
            # Power modes (read state)              00: Run mode
            MODE_REST1 = BIT_5                    # 01: Rest 1
            MODE_REST2 = BIT_6                    # 10: Rest 2
            MODE_REST3 = MODE_REST2 | MODE_REST1  # 11: Rest 3

            RESET_FLAG = BIT_7
        # end class OBSERVATION

        @unique
        class XY_DIRECTION(PixArt12BitsRegisterMap.Types.XY_DIRECTION):
            """
            Sensor XY Direction Register.
              * PAW3266 datasheet: section 8.2.3 Device Settings, page 35
            """
            INV_Y = BIT_4    # Set bit to inverse Y-direction
            INV_X = BIT_5    # Set bit to inverse X-direction
            SWAPXY = BIT_6   # Set bit to swap X & Y
            RES_SEL = BIT_7  # Resolution select, refer to datasheet
        # end class XY_DIRECTION

        @unique
        class LIFT_CUTOFF(IntFlag):
            """
            Sensor Lift Cutoff Register.
              * PAW3266 datasheet: section 8.2.3 Device Settings, page 37
            """
            EN = BIT_2  # Set bit to enable lift cutoff
        # end class LIFT_CUTOFF

        @unique
        class LIFTSTAT(IntFlag):
            """
            Sensor Lift Status Register.
              * undocumented, refer to email "PAW3266+One lens FW Guideline / Rev0.3 / 2022-9-29 / CY Wang", page 3
                https://docs.google.com/document/d/1iMEnCUKopFCDcJGsCgPQpLbHh5RerMQknx03bAOC11E
            """
            LIFT = BIT_7  # Set when lift is detected
        # end class LIFTSTAT
    # end class Types

    class Registers(PixArt12BitsRegisterMap.Registers):
        # See ``PixArt12BitsRegisterMap.Registers``
        MOTION = 0x02
        SQUAL = 0x06
        OBSERVATION = 0x1D
        LIFT_CUTOFF = 0x40
        LIFTSTAT = 0x6C
    # end class Registers

    class Commands(PixArt12BitsRegisterMap.Commands):
        # See ``PixArt12BitsRegisterMap.Commands``
        SQUAL = 0x06
        OBSERVATION_SET = 0x07
        OBSERVATION_CLR = 0x08
        LIFT_CUTOFF = 0x0B
        LIFTSTAT = 0x0C
    # end class Commands

    class Limits(PixArt12BitsRegisterMap.Limits):
        # See ``PixArt12BitsRegisterMap.Limits``
        pass
    # end class Limits

    # Register Mapping: Register address to Register dataclass
    regs = {
        **PixArt12BitsRegisterMap.regs,
        Registers.MOTION: MaskedRegister(addr=Registers.MOTION, name='Motion', type=Types.MOTION,
                                         desc='Motion Status Register'),
        Registers.SQUAL: Register(addr=Registers.SQUAL, name='SQual', type=int,
                                  desc='SQUAL (Surface Quality) is a measure of the number of valid features '
                                       'visible by the chip in the current frame'),
        Registers.OBSERVATION: MaskedRegister(addr=Registers.OBSERVATION, name='Observation',
                                              type=Types.OBSERVATION,
                                              desc='This register provides bits that are set every frame to verify '
                                                   'chip operating state.'),
        Registers.LIFT_CUTOFF: Register(addr=Registers.LIFT_CUTOFF, name='Lift Cutoff', type=Types.LIFT_CUTOFF,
                                        desc='Lift Cutoff control.'),
        Registers.LIFTSTAT: Register(addr=Registers.LIFTSTAT, name='LiftStat', type=Types.LIFTSTAT,
                                     desc='Lift Detection Status Register'),
    }

    # Command Mapping: Command index to Command dataclass
    cmds = {
        **PixArt12BitsRegisterMap.cmds,
        Commands.SQUAL: Command(idx=Commands.SQUAL, name='SQual',
                                desc='SQUAL (Surface Quality) is a measure of the number of valid features '
                                     'visible by the chip in the current frame'),
        Commands.OBSERVATION_SET: Command(idx=Commands.OBSERVATION_SET, name='Observation_set',
                                          desc='Observation Status Register: Force-Set Mask'),
        Commands.OBSERVATION_CLR: Command(idx=Commands.OBSERVATION_CLR, name='Observation_clr',
                                          desc='Observation Status Register: Force-Clr Mask'),
        Commands.LIFT_CUTOFF: Command(idx=Commands.LIFT_CUTOFF, name='Lift Cutoff',
                                      desc='Lift Cutoff control.'),
        Commands.LIFTSTAT: Command(idx=Commands.LIFTSTAT, name='LiftStat',
                                   desc='Lift Detection Status Register'),
    }

    # Register to Command Mapping: Register address to Command index(es)
    reg2cmd = {
        **PixArt12BitsRegisterMap.reg2cmd,
        Registers.MOTION: (Commands.MOTION_SET, Commands.MOTION_CLR),
        Registers.SQUAL: Commands.SQUAL,
        Registers.OBSERVATION: (Commands.OBSERVATION_SET, Commands.OBSERVATION_CLR),
        Registers.LIFT_CUTOFF: Commands.LIFT_CUTOFF,
        Registers.LIFTSTAT: Commands.LIFTSTAT,
    }

    # Command indexes that are affected by Compressed instruction data format
    cmp_cmd_idx: Set[cmd_idx_type] = {
        *PixArt12BitsRegisterMap.cmp_cmd_idx,
        Commands.LIFTSTAT,
    }
# end class Paw3266RegisterMap


class Pmw3816RegisterMap(PixArt16BitsRegisterMap):
    """
    Kosmos Optical Sensor Emulator Register Map, for PixArt 16-bit PMW3816 Optical Sensor.

    PixArt Optical Sensors Specifications:
     - PMW3816DM : https://drive.google.com/file/d/1Gw4C6Hek6xse0yNRDOvfLCH19zkFIPyb
    """

    class Types(PixArt16BitsRegisterMap.Types):
        # See ``PixArt16BitsRegisterMap.Types``
        @unique
        class MOTION(PixArt16BitsRegisterMap.Types.MOTION):
            """
            Sensor Motion Status Register.
              * PMW3816 datasheet: section 10.0, page 31
            """
            # Power modes (read state)              00: Run mode
            MODE_REST1 = BIT_0                    # 01: Rest 1
            MODE_REST2 = BIT_1                    # 10: Rest 2
            MODE_REST3 = MODE_REST2 | MODE_REST1  # 11: Rest 3

            MOT = BIT_7  # Motion occurred since last report. Also indicate data ready for Delta registers.
        # end class MOTION

        @unique
        class PERFORMANCE(PixArt12BitsRegisterMap.Types.PERFORMANCE):
            """
            Sensor Performance Register.
              * PMW3816 datasheet: section 10.0, page 32
            """
            # Power modes (force state)             00: Run mode
            MODE_REST1 = BIT_5                    # 01: Force Rest 1
            MODE_REST2 = BIT_6                    # 10: Force Rest 2
            MODE_REST3 = MODE_REST2 | MODE_REST1  # 11: Force Rest 3

            FORCE_RUN_MODE = BIT_7  # 0 = Rest mode enabled / 1 = Force run mode
        # end class PERFORMANCE

        @unique
        class OBSERVATION(PixArt16BitsRegisterMap.Types.OBSERVATION):
            """
            Chip Observation Register.
              * PAW3216 datasheet: section 10.0 Registers Description, page 37
            """
            # Recovery scheme (linked EFT/B or ESD event.)
            CO_0 = BIT_0
            CO_1 = BIT_1
            CO_2 = BIT_2
            CO_3 = BIT_3
            CO_4 = BIT_4
            CO_5 = BIT_5
        # end class OBSERVATION

        @unique
        class XY_DIRECTION(PixArt16BitsRegisterMap.Types.XY_DIRECTION):
            """
            Sensor XY Direction Register.
              * PMW3816 datasheet: section 10.0, page 40
            """
            INV_X = BIT_5   # Set bit to inverse X-direction
            INV_Y = BIT_6   # Set bit to inverse Y-direction
            SWAPXY = BIT_7  # Set bit to swap X & Y
        # end class XY_DIRECTION
    # end class Types

    class Registers(PixArt16BitsRegisterMap.Registers):
        # See ``PixArt16BitsRegisterMap.Registers``
        MOTION = 0x02
        SQUAL = 0x07
        OBSERVATION = 0x15
        PERFORMANCE = 0x40
    # end class Registers

    class Commands(PixArt16BitsRegisterMap.Commands):
        # See ``PixArt16BitsRegisterMap.Commands``
        SQUAL = 0x07
        OBSERVATION_SET = 0x08
        OBSERVATION_CLR = 0x18
        PERFORMANCE_SET = 0x09
        PERFORMANCE_CLR = 0x19
    # end class Commands

    class Limits(PixArt16BitsRegisterMap.Limits):
        # See ``PixArt16BitsRegisterMap.Limits``

        # SQUAL register value below LIFT_THRESHOLD means mouse is lifted
        # Refer to ccp_fw/rbm24_bardi_ble_pro/application/pmw3816.c > #define LIFT_THRESHOLD
        LIFT_THRESHOLD = 0x06
    # end class Limits

    # Register Mapping: Register address to Register dataclass
    regs = {
        **PixArt16BitsRegisterMap.regs,
        Registers.MOTION: MaskedRegister(addr=Registers.MOTION, name='Motion', type=Types.MOTION,
                                         desc='Motion Status Register'),
        Registers.SQUAL: Register(addr=Registers.SQUAL, name='SQual', type=int,
                                  desc='SQUAL (Surface Quality) is a measure of the number of valid features '
                                       'visible by the chip in the current frame. '
                                       'Note: Lift Status is computed from SQUAL value.',
                                  resetval=Limits.LIFT_THRESHOLD),
        Registers.OBSERVATION: MaskedRegister(addr=Registers.OBSERVATION, name='Observation',
                                              type=Types.OBSERVATION,
                                              desc='This register provides bits that are set every frame to verify '
                                                   'chip operating state.'),
        Registers.PERFORMANCE: MaskedRegister(addr=Registers.PERFORMANCE, name='Performance',
                                              type=Types.PERFORMANCE,
                                              desc='This register is used to set the sensor into different operating '
                                                   'modes.'),
    }

    # Command Mapping: Command index to Command dataclass
    cmds = {
        **PixArt16BitsRegisterMap.cmds,
        Commands.SQUAL: Command(idx=Commands.SQUAL, name='SQual',
                                desc='SQUAL (Surface Quality) is a measure of the number of valid features '
                                     'visible by the chip in the current frame'),
        Commands.OBSERVATION_SET: Command(idx=Commands.OBSERVATION_SET, name='Observation_set',
                                          desc='Observation Status Register: Force-Set Mask'),
        Commands.OBSERVATION_CLR: Command(idx=Commands.OBSERVATION_CLR, name='Observation_clr',
                                          desc='Observation Status Register: Force-Clr Mask'),
        Commands.PERFORMANCE_SET: Command(idx=Commands.PERFORMANCE_SET, name='Performance_set',
                                          desc='Performance Control Register: Force-Set Mask'),
        Commands.PERFORMANCE_CLR: Command(idx=Commands.PERFORMANCE_CLR, name='Performance_clr',
                                          desc='Performance Control Register: Force-Clr Mask'),
    }

    # Register to Command Mapping: Register address to Command index(es)
    reg2cmd = {
        **PixArt16BitsRegisterMap.reg2cmd,
        Registers.MOTION: (Commands.MOTION_SET, Commands.MOTION_CLR),
        Registers.SQUAL: Commands.SQUAL,
        Registers.OBSERVATION: (Commands.OBSERVATION_SET, Commands.OBSERVATION_CLR),
        Registers.PERFORMANCE: (Commands.PERFORMANCE_SET, Commands.PERFORMANCE_CLR),
    }

    # Command indexes that are affected by Compressed instruction data format
    cmp_cmd_idx: Set[cmd_idx_type] = {
        *PixArt16BitsRegisterMap.cmp_cmd_idx,
        Commands.SQUAL,
    }
# end class Pmw3816RegisterMap


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
