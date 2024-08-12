#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.model.optemu.base
:brief: Kosmos Optical Sensor Emulator Register Map base Package
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/05/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from abc import ABCMeta
from typing import Dict
from typing import Set
from typing import Tuple
from typing import Union

from pyraspi.services.kosmos.module.model.registermap import Command
from pyraspi.services.kosmos.module.model.registermap import MaskedRegister
from pyraspi.services.kosmos.module.model.registermap import Register
from pyraspi.services.kosmos.module.model.registermap import RegisterMapBase
from pyraspi.services.kosmos.module.model.registermap import cmd_idx_type


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class OptEmuRegisterMapBase(RegisterMapBase, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Register Map base class.

    Refer to ``RegisterMapBase`` class for details.
    """

    class Types(RegisterMapBase.Types):
        # See ``PixArtRegisterMapBase.Types``
        # /!\ Types class attributes shall be initialized in derived class
        pass
    # end class Types

    class Registers(RegisterMapBase.Registers):
        # See ``PixArtRegisterMapBase.Registers``
        # /!\ Registers class attributes shall be initialized in derived class
        DELTA_X_L: int
        DELTA_Y_L: int
    # end class Registers

    class Commands(RegisterMapBase.Commands):
        # See ``PixArtRegisterMapBase.Commands``
        REPEAT = 0x00
        SKIP = 0x01
        DELTA_X_L: int
        DELTA_Y_L: int
        GRW_ADDR = 0x3E
        GRW_DATA = 0x3F
    # end class Commands

    class Limits(RegisterMapBase.Limits):
        # See ``PixArtRegisterMapBase.Limits``
        # /!\ Limits class attributes shall be initialized in derived class
        REPEAT_MAX: int = 0xFF
        SKIP_MAX: int = 0xFF
        DELTA_BIT_COUNT: int
        DELTA_UNSIGNED_MIN: int
        DELTA_UNSIGNED_MAX: int
        DELTA_SIGNED_MIN: int
        DELTA_SIGNED_MAX: int
    # end class Limits

    # Register Mapping: Register address to Register dataclass
    # /!\ regs shall be initialized in derived class
    regs: Dict[int, Union[Register, MaskedRegister]] = {}

    # Command Mapping: Command index to Command dataclass
    cmds: Dict[cmd_idx_type, Command] = {
        Commands.SKIP: Command(idx=Commands.SKIP, name='Skip',
                               desc='Model Data Update Skip counter value'),
        Commands.REPEAT: Command(idx=Commands.REPEAT, name='Repeat',
                                 desc='Model Data Update Repeat counter value'),
        Commands.GRW_ADDR: Command(idx=Commands.GRW_ADDR, name='GRW_addr',
                                   desc='Generic Register Write: address selection'),
        Commands.GRW_DATA: Command(idx=Commands.GRW_DATA, name='GRW_data',
                                   desc='Generic Register Write: data selection')
    }

    # Register to Command Mapping: Register address to Command index(es)
    # /!\ reg2cmd shall be initialized in derived class
    reg2cmd: Dict[int, Union[int, Tuple[int, int]]] = {}

    # Set of Delta X/Y related commands
    # /!\ delta_cmds shall be initialized in derived class
    delta_cmds: Set[cmd_idx_type]

    # Command indexes that are affected by Compressed instruction data format
    #  /!\ cmp_cmd_idx shall be completed in derived class
    cmp_cmd_idx: Set[cmd_idx_type] = {
        Commands.SKIP,
        Commands.REPEAT
    }

    def __init__(self):

        # Command indexes that are affected by Compressed instruction data format
        self.cmp_cmd_idx.update(self.delta_cmds)

        super().__init__()
    # end def __init__
# end class OptEmuRegisterMapBase


class OptEmu12BitsRegisterMapBase(OptEmuRegisterMapBase, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Register Map base class, 12-bit Optical Sensors.
    """

    class Registers(OptEmuRegisterMapBase.Registers):
        # See ``OptEmuRegisterMapBase.Registers``
        DELTA_X_L: int
        DELTA_Y_L: int
        DELTA_XY_H: int
    # end class Registers

    class Commands(OptEmuRegisterMapBase.Commands):
        # See ``OptEmuRegisterMapBase.Commands``
        DELTA_X_L: int
        DELTA_Y_L: int
        DELTA_XY_H: int
    # end class Commands

    class Limits(OptEmuRegisterMapBase.Limits):
        # See ``OptEmuRegisterMapBase.Limits``
        DELTA_BIT_COUNT = 12
        DELTA_UNSIGNED_MIN = 0x800
        DELTA_UNSIGNED_MAX = 0x7FF
        DELTA_SIGNED_MIN = -2048
        DELTA_SIGNED_MAX = +2047
    # end class Limits

    def __init__(self):
        # Shorthand notations
        c = self.Commands
        r = self.Registers

        # Register Mapping: Register address to Register dataclass
        self.regs.update({
            r.DELTA_X_L: Register(addr=r.DELTA_X_L, name='Delta X_l', type=int,
                                  desc='X Displacement (lower bits)'),
            r.DELTA_Y_L: Register(addr=r.DELTA_Y_L, name='Delta Y_l', type=int,
                                  desc='Y Displacement (lower bits)'),
            r.DELTA_XY_H: Register(addr=r.DELTA_XY_H, name='Delta XY_h', type=int,
                                   desc='X and Y Displacements (higher bits)')
        })

        # Command Mapping: Command index to Command dataclass
        self.cmds.update({
            c.DELTA_X_L: Command(idx=c.DELTA_X_L, name='Delta X_l',
                                 desc='X Displacement (lower bits)'),
            c.DELTA_Y_L: Command(idx=c.DELTA_Y_L, name='Delta Y_l',
                                 desc='Y Displacement (lower bits)'),
            c.DELTA_XY_H: Command(idx=c.DELTA_XY_H, name='Delta XY_h',
                                  desc='X and Y Displacements (higher bits)')
        })

        # Register to Command Mapping: Register address to Command index(es)
        self.reg2cmd.update({
            r.DELTA_X_L: c.DELTA_X_L,
            r.DELTA_Y_L: c.DELTA_Y_L,
            r.DELTA_XY_H: c.DELTA_XY_H
        })

        # Set of Delta X/Y related commands
        self.delta_cmds = {c.DELTA_X_L, c.DELTA_Y_L, c.DELTA_XY_H}

        super().__init__()
    # end def __init__
# end class OptEmu12BitsRegisterMapBase


class OptEmu16BitsRegisterMapBase(OptEmuRegisterMapBase, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Register Map base class, 16-bit Optical Sensors.
    """

    class Types(OptEmuRegisterMapBase.Types):
        # See ``OptEmuRegisterMapBase.Types``
        pass
    # end class Types

    class Registers(OptEmuRegisterMapBase.Registers):
        # See ``OptEmuRegisterMapBase.Registers``
        DELTA_X_H: int
        DELTA_X_L: int
        DELTA_Y_H: int
        DELTA_Y_L: int
    # end class Registers

    class Commands(OptEmuRegisterMapBase.Commands):
        # See ``OptEmuRegisterMapBase.Commands``
        DELTA_X_H: int
        DELTA_X_L: int
        DELTA_Y_H: int
        DELTA_Y_L: int
    # end class Commands

    class Limits(OptEmuRegisterMapBase.Limits):
        # See ``OptEmuRegisterMapBase.Limits``
        DELTA_BIT_COUNT = 16
        DELTA_UNSIGNED_MIN = 0x8000
        DELTA_UNSIGNED_MAX = 0x7FFF
        DELTA_SIGNED_MIN = -32768
        DELTA_SIGNED_MAX = +32767
    # end class Limits

    def __init__(self):
        # Shorthand notations
        c = self.Commands
        r = self.Registers

        # Register Mapping: Register address to Register dataclass
        self.regs.update({
            r.DELTA_X_H: Register(addr=r.DELTA_X_H, name='Delta X_h', type=int,
                                  desc='X Displacement (higher byte)'),
            r.DELTA_X_L: Register(addr=r.DELTA_X_L, name='Delta X_l', type=int,
                                  desc='X Displacement (lower byte)'),
            r.DELTA_Y_H: Register(addr=r.DELTA_Y_H, name='Delta Y_h', type=int,
                                  desc='Y Displacement (higher byte)'),
            r.DELTA_Y_L: Register(addr=r.DELTA_Y_L, name='Delta Y_l', type=int,
                                  desc='Y Displacement (lower byte)')
        })

        # Command Mapping: Command index to Command dataclass
        self.cmds.update({
            c.DELTA_X_H: Command(idx=c.DELTA_X_H, name='Delta X_h',
                                 desc='X Displacement (higher byte)'),
            c.DELTA_X_L: Command(idx=c.DELTA_X_L, name='Delta X_l',
                                 desc='X Displacement (lower byte)'),
            c.DELTA_Y_H: Command(idx=c.DELTA_Y_H, name='Delta Y_h',
                                 desc='Y Displacement (higher byte)'),
            c.DELTA_Y_L: Command(idx=c.DELTA_Y_L, name='Delta Y_l',
                                 desc='Y Displacement (lower byte)')
        })

        # Register to Command Mapping: Register address to Command index(es)
        self.reg2cmd.update({
            r.DELTA_X_H: c.DELTA_X_H,
            r.DELTA_X_L: c.DELTA_X_L,
            r.DELTA_Y_H: c.DELTA_Y_H,
            r.DELTA_Y_L: c.DELTA_Y_L
        })

        # Set of Delta X/Y related commands
        self.delta_cmds = {c.DELTA_X_H, c.DELTA_X_L,
                           c.DELTA_Y_H, c.DELTA_Y_L}

        super().__init__()
    # end def __init__
# end class OptEmu16BitsRegisterMapBase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
