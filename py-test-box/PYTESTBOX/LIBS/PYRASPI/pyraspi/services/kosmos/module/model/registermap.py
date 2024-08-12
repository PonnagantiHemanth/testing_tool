#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.model.registermap
:brief: Kosmos Module Register Map Model Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/05/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from ctypes import c_uint8
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from enum import IntEnum
from enum import IntFlag
from enum import auto
from enum import unique
from operator import itemgetter
from typing import ClassVar
from typing import Dict
from typing import Tuple
from typing import Type
from typing import Union

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.utils import AutoNameEnum
from pyraspi.services.kosmos.utils import get_attributes
from pyraspi.services.kosmos.utils import sort_attributes_by_value
from pyraspi.services.kosmos.utils import sort_dict

# ------------------------------------------------------------------------------
# Types
# ------------------------------------------------------------------------------

# Register address and value types
reg_addr_type = Union[IntEnum, int]
reg_val_type = Union[IntFlag, int]

# Command index and value types
cmd_idx_type = Union[IntEnum, int]
cmd_val_type = Union[IntFlag, int]


@unique
class BIT(IntFlag):
    """
    Mapping of bit index name to bit mask
    """
    BIT_0 = (1 << 0)
    BIT_1 = (1 << 1)
    BIT_2 = (1 << 2)
    BIT_3 = (1 << 3)
    BIT_4 = (1 << 4)
    BIT_5 = (1 << 5)
    BIT_6 = (1 << 6)
    BIT_7 = (1 << 7)
# end class BIT


# Shorthand notations
BIT_0 = BIT.BIT_0
BIT_1 = BIT.BIT_1
BIT_2 = BIT.BIT_2
BIT_3 = BIT.BIT_3
BIT_4 = BIT.BIT_4
BIT_5 = BIT.BIT_5
BIT_6 = BIT.BIT_6
BIT_7 = BIT.BIT_7

BIT_COUNT = 8  # current implementation assumes all registers are 8-bit wide


@unique
class MASK_TYPE(str, Enum):
    """
    Register Value Mask types.
    Refer to ``MaskedRegVal`` class.
    """
    DEFAULT = 'x'
    FORCE_SET = '1'
    FORCE_CLR = '0'
# end class MASK_TYPE


# Default Register Value Mask: 'xxxxxxxx' for 8-bit registers
default_mask = MASK_TYPE.DEFAULT.value * BIT_COUNT


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


def bits(byte):
    """
    Return the binary string representation of a byte, most significant bits first.

    Examples:
      - ``bits(0x12)`` returns ``'00010010'``
      - ``bits(0xF0)`` returns ``'11110000'``

    :param byte: Value to be converted
    :type byte: ``int``

    :return: binary string representation of the byte
    :rtype: ``str``
    """
    return f'{byte:08b}'
# end def bits


@dataclass
class RegValBase(metaclass=ABCMeta):
    """
    Register Value dataclass base.
    """
    value: reg_val_type = 0
    type: Type[reg_val_type] = field(repr=False, default=int, compare=False)

    @abstractmethod
    def set(self, value, mask=0xFF):
        """
        Set Register bits.

        :param value: value to be set to the Register Value
        :type value: ``int``
        :param mask: mask selecting Register Value bits to clear/set depending on value, defaults to 0xFF - OPTIONAL
        :type mask: ``int``

        :raise ``AssertionError``: out-of-bounds parameter
        """
        raise NotImplementedAbstractMethodError()
    # end def set

    @abstractmethod
    def reset(self, mask=0xFF):
        """
        Reset Register bits.

        :param mask: mask selecting Register Value bits to clear, defaults to 0xFF - OPTIONAL
        :type mask: ``int``

        :raise ``AssertionError``: out-of-bounds parameter
        """
        raise NotImplementedAbstractMethodError()
    # end def reset

    @property
    def value_unsigned(self):
        """
        Return the unsigned integer representation of the Register signed value.

        :return: unsigned integer representation of the Register signed value
        :rtype: ``int``
        """
        return c_uint8(self.value).value
    # end def property getter value_unsigned
# end class RegValBase


@dataclass
class RegVal(RegValBase):
    """
    Register Value dataclass.
    For registers that can be written to directly.
    """
    def set(self, value, mask=0xFF):
        # See ``RegValBase.set``
        assert -0x80 <= value <= 0xFF, value
        assert 0 <= mask <= 0xFF, mask
        tmp = self.value & ~mask
        tmp |= value & mask
        self.value = self.type(tmp)
    # end def set

    def reset(self, mask=0xFF):
        # See ``RegValBase.reset``
        assert 0 <= mask <= 0xFF, mask
        tmp = self.value & ~mask
        self.value = self.type(tmp)
    # end def reset
# end class RegVal


@dataclass
class MaskedRegVal(RegVal):
    """
    Masked Register Value dataclass.
    For registers that NOT can be written to directly, but use `set` and `clear` mask registers instead.
    """
    mask: str = default_mask

    def set(self, value, mask=0xFF):
        # See ``RegValBase.set``
        super().set(value=value, mask=mask)
        self.mask = ''.join(MASK_TYPE.DEFAULT.value if bitmask == '0' else bitval
                            for bitval, bitmask in zip(bits(self.value_unsigned), bits(mask)))
    # end def set

    def reset(self, mask=0xFF):
        # See ``RegValBase.reset``
        super().reset(mask=mask)
        self.mask = ''.join(old_mask if new_mask == '0' else MASK_TYPE.DEFAULT.value
                            for old_mask, new_mask in zip(self.mask, bits(mask)))
    # end def reset

    @property
    def set_mask(self):
        """
        Return the 'set' mask value.

        :return: 'set' mask value
        :rtype: ``reg_val_type``
        """
        return self.type(sum((bitmask == MASK_TYPE.FORCE_SET.value) << (BIT_COUNT - 1 - bitpos)
                             for bitpos, (bitval, bitmask) in enumerate(zip(bits(self.value_unsigned), self.mask))))
    # end def property getter set_mask

    @property
    def clr_mask(self):
        """
        Return the 'clear' mask value.

        :return: 'clear' mask value
        :rtype: ``reg_val_type``
        """
        return self.type(sum((bitmask == MASK_TYPE.FORCE_CLR.value) << (BIT_COUNT - 1 - bitpos)
                             for bitpos, (bitval, bitmask) in enumerate(zip(bits(self.value_unsigned), self.mask))))
    # end def property getter clr_mask
# end class MaskedRegVal


@dataclass
class RegisterBase(metaclass=ABCMeta):
    """
    Register dataclass base
    """
    addr: reg_addr_type
    name: str
    type: Type[reg_val_type] = field(repr=False, default=int)
    resetval: reg_val_type = 0
    desc: str = field(compare=False, default='')
    regval_cls: ClassVar[Type[RegValBase]] = RegValBase

    def __post_init__(self):
        self.resetval = self.type(self.resetval)
        assert issubclass(self.regval_cls, RegValBase), self.regval_cls
    # end def __post_init__

    def update(self, value=None, mask=0xFF, regv=None):
        """
        Update Register value

        :param value: value to be set to the Register Value, defaults to None (value not updated) - OPTIONAL
        :type value: ``int``
        :param mask: mask selecting Register Value bits to clear/set depending on value, defaults to 0xFF - OPTIONAL
        :type mask: ``int``
        :param regv: instance of Register Value class to be updated, defaults to None (create new instance) - OPTIONAL
        :type regv: ``RegVal or MaskedRegVal``

        :return: Register value
        :rtype: ``RegVal or MaskedRegVal``
        """
        regv = self.regval_cls(value=self.resetval, type=self.type) if regv is None else regv
        if value is None:
            regv.reset(mask)
        else:
            regv.set(value, mask)
        # end if
        return regv
    # end def update
# end class RegisterBase


@dataclass
class Register(RegisterBase):
    """
    Register dataclass.
    For registers that can be written directly.
    """
    regval_cls: ClassVar[Type[RegVal]] = RegVal
# end class Register


@dataclass
class MaskedRegister(RegisterBase):
    """
    Masked Register dataclass.
    For registers that NOT can be written directly, but use `set` and `clear` mask registers instead.
    """
    regval_cls: ClassVar[Type[MaskedRegVal]] = MaskedRegVal
# end class MaskedRegister


@dataclass
class Command:
    """
    Commands dataclass.
    """
    idx: cmd_idx_type
    name: str
    type: Type[cmd_val_type] = field(repr=False, default=int)
    value: cmd_val_type = field(default=0)
    desc: str = field(compare=False, default='')

    def __post_init__(self):
        """
        Enforce value type after dataclass init.
        """
        self.set(self.value)
    # end def __post_init__

    def set(self, value):
        """
        Set command value, enforcing the value type.

        :param value: Command value to be set, typically of type `int` or `Enum`.
        :type value: ``self.type``
        """
        self.value = self.type(value)
    # end def set
# end class Command


# Character translation table: delete hyphen, underscore and space characters
# See ``test_names()`` method below
_translation_table = str.maketrans({c: '' for c in '-_ '})


def test_names(name_a, name_b):
    """
    Test if two name strings are identical.
    The comparison is case-insensitive and excludes hyphen, underscore and space characters.

    :param name_a: First name string to compare
    :type name_a: ``str``
    :param name_b: Second name string to compare
    :type name_b: ``str``

    :return: Comparison result
    :rtype: ``bool``
    """
    a = name_a.translate(_translation_table).lower()
    b = name_b.translate(_translation_table).lower()
    return a == b
# end def test_names


class RegisterMapBase(metaclass=ABCMeta):
    """
    Kosmos Emulator Register Map base class.
    """

    class Types:
        """
        Register Types: bitfield Enums.
        """
        # /!\ Types class attributes shall be initialized in derived class
        pass
    # end class Types

    class Registers:
        """
        Register Address Map.
        """
        # /!\ Registers class attributes shall be initialized in derived class
        pass
    # end class Registers

    class Commands:
        """
        Emulator-specific Command Index Map.
        """
        # /!\ Commands class attributes shall be initialized in derived class
        pass
    # end class Commands

    class Limits:
        """
        Register Limits.
        """
        # /!\ Limits class attributes shall be initialized in derived class
        pass
    # end class Limits

    # Register Mapping: Register name to Register address
    registers: Dict[str, int]  # will be automatically initialised from Registers class

    # Command Mapping: Command name to Command index
    commands: Dict[str, int]   # will be automatically initialised from Commands class

    # Register Mapping: Register address to Register dataclass
    regs: Dict[int, Register]  # /!\ shall be initialized in derived class

    # Command Mapping: Command index to Command dataclass
    cmds: Dict[int, Command]   # /!\ shall be initialized in derived class

    # Register to Command Mapping: Register address to Command index(es)
    reg2cmd: Dict[int, Union[int, Tuple[int, int]]]   # to be manually initialized in derived class

    def __init__(self):
        """
        :raise ``AssertionError``: Sanity checks failure
        :raise ``TypeError``: Invalid register type in `self.regs`
        """
        self.registers = sort_attributes_by_value(self.Registers)
        self.commands = sort_attributes_by_value(self.Commands)
        self.regs = sort_dict(self.regs)
        self.cmds = sort_dict(self.cmds)
        self.reg2cmd = sort_dict(self.reg2cmd)

        # Sanity checks between <self.Registers>, <self.registers> and <self.regs>
        for name, addr in self.registers.items():
            reg = self.regs[addr]
            assert test_names(name, reg.name), f'Reg name {addr:#04x}:{name} does not match {reg}'
            assert addr == reg.addr, f'Reg address {addr:#04x}:{name} does not match {reg}'
        # end for

        # Sanity checks between <self.Commands>, <self.commands> and <self.cmds>
        for name, idx in self.commands.items():
            cmd = self.cmds[idx]
            assert test_names(name, cmd.name), f'Cmd index {idx:#04x}:{name} does not match {cmd}'
            assert idx == cmd.idx, f'Cmd index {idx:#04x}:{name} does not match {cmd}'
        # end for

        # Sanity checks between <self.reg2cmd>, <self.commands> and <self.registers>
        assert self.reg2cmd.keys() == self.regs.keys(), set(self.reg2cmd.keys()).symmetric_difference(self.regs.keys())
        for reg_addr, cmd_idx in self.reg2cmd.items():
            reg = self.regs[reg_addr]
            if isinstance(reg, Register):
                assert cmd_idx in self.cmds, (reg, cmd_idx)
            elif isinstance(reg, MaskedRegister):
                assert isinstance(cmd_idx, tuple) and len(cmd_idx) == 2, (reg, cmd_idx)
                assert cmd_idx[0] in self.cmds, (reg, cmd_idx)
                assert cmd_idx[1] in self.cmds, (reg, cmd_idx)
            else:
                raise TypeError((reg, reg_addr, cmd_idx))
            # end if
        # end for
    # end def __init__
# end class RegisterMapBase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
