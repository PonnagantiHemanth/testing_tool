#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.model.optemu.test.em_test
:brief: Tests for KOSMOS EM (Electro-Marin) Family Optical Sensors Emulator Model Package
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/04/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta

from pyraspi.services.kosmos.module.model.optemu.em import Em12BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.em import Em16BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.em import EmRegisterMapBase
from pyraspi.services.kosmos.module.model.optemu.test.base_test import RegisterMapBaseTest


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class EmRegisterMapBaseTest(RegisterMapBaseTest, metaclass=ABCMeta):
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """

    class EmRegisterMapTestCaseMixin(RegisterMapBaseTest.OptEmuRegisterMapTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Register Map Mixin Test class, for Electro-Marin (EM) Optical Sensors family.
        """
        regmap: EmRegisterMapBase
        bits: int
        mask: int

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class

            :raise ``AssertionError``: Invalid register map type
            """
            super().setUpClass()
            assert isinstance(cls.regmap, EmRegisterMapBase), cls.regmap
        # end def setUpClass
    # end class EmRegisterMapTestCaseMixin
# end class EmRegisterMapBaseTest


class OptEmuEm12BitsRegisterMapTestCase(EmRegisterMapBaseTest.EmRegisterMapTestCaseMixin):
    """
    Kosmos Optical Sensor Emulator Register Map Test class, for Electro-Marin (EM) 12-bit Optical Sensors family.
    """
    regmap = Em12BitsRegisterMap()
    bits = 12
    mask = 0xFFF
# end class OptEmuEm12BitsRegisterMapTestCase


class OptEmuEm16BitsRegisterMapTestCase(EmRegisterMapBaseTest.EmRegisterMapTestCaseMixin):
    """
    Kosmos Optical Sensor Emulator Register Map Test class, for Electro-Marin (EM) 16-bit Optical Sensors family.
    """
    regmap = Em16BitsRegisterMap()
    bits = 16
    mask = 0xFFFF
# end class OptEmuEm16BitsRegisterMapTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
