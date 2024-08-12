#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.model.optemu.test.base_test
:brief: Tests for KOSMOS Optical Sensors Emulator Model Package
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/05/17
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from ctypes import c_uint16
from unittest import TestCase

from pyraspi.services.kosmos.module.model.optemu.base import OptEmuRegisterMapBase
from pyraspi.services.kosmos.module.model.registermap import MaskedRegVal
from pyraspi.services.kosmos.module.model.registermap import MaskedRegister
from pyraspi.services.kosmos.module.model.registermap import RegVal
from pyraspi.services.kosmos.module.model.registermap import Register
from pyraspi.services.kosmos.utils import pretty_class
from pyraspi.services.kosmos.utils import pretty_dict
from pyraspi.services.kosmos.utils import pretty_list

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

VERBOSE: bool = False


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class RegisterMapBaseTest(metaclass=ABCMeta):
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """

    class OptEmuRegisterMapTestCaseMixin(TestCase, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Register Map Mixin Test class, for Electro-Marin (EM) Optical Sensors family.
        """
        regmap: OptEmuRegisterMapBase
        bits: int
        mask: int

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class

            :raise ``AssertionError``: Invalid initial values or types
            """
            assert cls.regmap, '`reg_map` must be initialized in derived class'
            assert isinstance(cls.regmap, OptEmuRegisterMapBase), cls.regmap
            assert cls.bits, '`bits` must be initialized in derived class'
            assert isinstance(cls.bits, int), cls.bits
        # end def setUpClass

        def test_registers(self):
            """
            Validate the ``EmRegisterMapBase.registers`` mapping
            """
            VERBOSE and print(pretty_dict(self.regmap.registers, hex))

            for name, addr in self.regmap.registers.items():
                reg = self.regmap.regs[addr]
                self.assertEqual(addr, reg.addr, msg=(name, addr, reg))
            # end for
        # end def test_registers

        def test_commands(self):
            """
            Validate the ``EmRegisterMapBase.commands`` mapping
            """
            VERBOSE and print(pretty_dict(self.regmap.commands, hex))

            for name, idx in self.regmap.commands.items():
                cmd = self.regmap.cmds[idx]
                self.assertEqual(idx, cmd.idx, msg=(name, idx, cmd))
            # end for
        # end def test_commands

        def test_regs(self):
            """
            Validate the ``EmRegisterMapBase.regs`` mapping
            """
            VERBOSE and print(pretty_dict(self.regmap.regs))

            for addr, reg in self.regmap.regs.items():
                self.assertEqual(addr, reg.addr)
            # end for
        # end def test_regs

        def test_cmds(self):
            """
            Validate the ``EmRegisterMapBase.cmds`` mapping
            """
            VERBOSE and print(pretty_dict(self.regmap.cmds))

            for idx, cmd in self.regmap.cmds.items():
                self.assertEqual(idx, cmd.idx)
            # end for
        # end def test_cmds

        def test_reg_val(self):
            """
            Validate the ``EmRegisterMapBase.regs`` Register Value Classes
            """
            VERBOSE and print(pretty_list(self.regmap.regs.values()))

            for reg in self.regmap.regs.values():
                regv = reg.update()
                self.assertIsInstance(obj=reg, cls=(Register, MaskedRegister))
                if isinstance(reg, Register):
                    self.assertIs(reg.regval_cls, RegVal)
                    self.assertIsInstance(regv, RegVal)
                else:
                    self.assertIs(reg.regval_cls, MaskedRegVal)
                    self.assertIsInstance(regv, MaskedRegVal)
                # end if
            # end for
        # end def test_reg_val

        def test_limits(self):
            """
            Validate the ``EmRegisterMapBase.Limits`` mapping
            """
            VERBOSE and print(pretty_class(self.regmap.Limits, hex))

            s_min = -(1 << self.bits - 1)
            u_min = c_uint16(s_min).value & self.mask
            s_max = (1 << self.bits - 1) - 1
            u_max = c_uint16(s_max).value & self.mask

            self.assertEqual(s_min, self.regmap.Limits.DELTA_SIGNED_MIN)
            self.assertEqual(u_min, self.regmap.Limits.DELTA_UNSIGNED_MIN)
            self.assertEqual(s_max, self.regmap.Limits.DELTA_SIGNED_MAX)
            self.assertEqual(u_max, self.regmap.Limits.DELTA_UNSIGNED_MAX)
        # end def test_limits
    # end class OptEmuRegisterMapTestCaseMixin
# end class RegisterMapBaseTest


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
