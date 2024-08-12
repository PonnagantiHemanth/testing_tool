#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.model.optemu.test.pixart_test
:brief: Tests for KOSMOS PixArt Family Optical Sensors Emulator Model Package
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/04/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta

from pyraspi.services.kosmos.module.model.optemu.pixart import Paw3266RegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArt12BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArt16BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArtRegisterMapBase
from pyraspi.services.kosmos.module.model.optemu.pixart import Pmw3816RegisterMap
from pyraspi.services.kosmos.module.model.optemu.test.base_test import RegisterMapBaseTest


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class PixArtRegisterMapBaseTest(RegisterMapBaseTest, metaclass=ABCMeta):
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """

    class PixArtRegisterMapTestCaseMixin(RegisterMapBaseTest.OptEmuRegisterMapTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Register Map Mixin Test class, for PixArt Optical Sensors family.
        """
        regmap: PixArtRegisterMapBase
        bits: int
        mask: int

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class

            :raise ``AssertionError``: Invalid register map type
            """
            super().setUpClass()
            assert cls.regmap, '`reg_map` must be initialized in derived class'
            assert isinstance(cls.regmap, PixArtRegisterMapBase), cls.regmap
        # end def setUpClass
    # end class PixArtRegisterMapTestCaseMixin
# end class PixArtRegisterMapBaseTest


class PixArt12BitsRegisterMapTestCase(PixArtRegisterMapBaseTest.PixArtRegisterMapTestCaseMixin):
    """
    Kosmos Optical Sensor Emulator Register Map Test class, for PixArt 12-bit Optical Sensors family.
    """
    regmap = PixArt12BitsRegisterMap()
    bits = 12
    mask = 0xFFF
# end class PixArt12BitsRegisterMapTestCase


class PixArt16BitsRegisterMapTestCase(PixArtRegisterMapBaseTest.PixArtRegisterMapTestCaseMixin):
    """
    Kosmos Optical Sensor Emulator Register Map Test class, for PixArt 16-bit Optical Sensors family.
    """
    regmap = PixArt16BitsRegisterMap()
    bits = 16
    mask = 0xFFFF
# end class PixArt16BitsRegisterMapTestCase


class Paw3266RegisterMapTestCase(PixArt12BitsRegisterMapTestCase):
    """
    Kosmos Optical Sensor Emulator Register Map Test class, for PixArt PAW3266 12-bit Optical Sensor.
    """
    regmap = Paw3266RegisterMap()
# end class Paw3266RegisterMapTestCase


class Pmw3816RegisterMapTestCase(PixArt16BitsRegisterMapTestCase):
    """
    Kosmos Optical Sensor Emulator Register Map Test class, for PixArt PMW3816 16-bit Optical Sensor.
    """
    regmap = Pmw3816RegisterMap()
# end class Pmw3816RegisterMapTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
