#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.optemu_em_test
:brief: Kosmos Optical Sensor Emulator Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/03/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta

from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArt12BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArt16BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArtRegisterMapBase
from pyraspi.services.kosmos.module.optemu import Action
from pyraspi.services.kosmos.module.optemu_pixart import PixArt12BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt12BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt12BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt16BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt16BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt16BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArtOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArtOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArtOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_sensors import Paw3266Module
from pyraspi.services.kosmos.module.optemu_sensors import Pmw3816Module
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.module.test.optemu_test import HighLevelInput
from pyraspi.services.kosmos.module.test.optemu_test import HighLevelTest
from pyraspi.services.kosmos.module.test.optemu_test import IDEM
from pyraspi.services.kosmos.module.test.optemu_test import LowLevelInput
from pyraspi.services.kosmos.module.test.optemu_test import LowLevelTest
from pyraspi.services.kosmos.module.test.optemu_test import OptEmuAbstractTestClass


# ------------------------------------------------------------------------------
# Abstract Test Class definition
# ------------------------------------------------------------------------------
class PixArtOptEmuAbstractTestClass:
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """

    class PixArtOptEmuTestCaseMixin(OptEmuAbstractTestClass.OptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # update type hits
        module: PixArtOptEmuModuleMixin

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class
            """
            super().setUpClass()
            assert isinstance(cls.module, PixArtOptEmuModuleMixin), cls.module
            assert isinstance(cls.module.ll_ctrl, PixArtOptEmuLowLevelControlMixin), cls.module.ll_ctrl
            assert isinstance(cls.module.hl_ctrl, PixArtOptEmuHighLevelControlMixin), cls.module.hl_ctrl
            assert isinstance(cls.module.ll_ctrl.reg_map, PixArtRegisterMapBase), cls.reg_map
        # end def setUpClass
    # end class PixArtOptEmuTestCaseMixin

    class PixArt12BitsOptEmuTestCaseMixin(OptEmuAbstractTestClass.OptEmu12BitsTestCaseMixin,
                                          PixArtOptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # update type hits
        module: PixArt12BitsOptEmuModuleMixin

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class
            """
            super().setUpClass()
            assert isinstance(cls.module, PixArt12BitsOptEmuModuleMixin), cls.module
            assert isinstance(cls.module.ll_ctrl, PixArt12BitsOptEmuLowLevelControlMixin), cls.module.ll_ctrl
            assert isinstance(cls.module.hl_ctrl, PixArt12BitsOptEmuHighLevelControlMixin), cls.module.hl_ctrl
            assert isinstance(cls.module.ll_ctrl.reg_map, PixArt12BitsRegisterMap), cls.reg_map
        # end def setUpClass
    # end class PixArt12BitsOptEmuTestCaseMixin

    class PixArt16BitsOptEmuTestCaseMixin(OptEmuAbstractTestClass.OptEmu16BitsTestCaseMixin,
                                          PixArtOptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # update type hits
        module: PixArt16BitsOptEmuModuleMixin

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class
            """
            super().setUpClass()
            assert isinstance(cls.module, PixArt16BitsOptEmuModuleMixin), cls.module
            assert isinstance(cls.module.ll_ctrl, PixArt16BitsOptEmuLowLevelControlMixin), cls.module.ll_ctrl
            assert isinstance(cls.module.hl_ctrl, PixArt16BitsOptEmuHighLevelControlMixin), cls.module.hl_ctrl
            assert isinstance(cls.module.ll_ctrl.reg_map, PixArt16BitsRegisterMap), cls.reg_map
        # end def setUpClass
    # end class PixArt16BitsOptEmuTestCaseMixin
# end class PixArtOptEmuAbstractTestClass


# ------------------------------------------------------------------------------
# Test case implementation
# ------------------------------------------------------------------------------

@require_kosmos_device(DeviceName.SPI_PAW3266)
class Paw3266ModuleTestCase(PixArtOptEmuAbstractTestClass.PixArt12BitsOptEmuTestCaseMixin):
    """
    Kosmos PixArt PAW3266 TCOB Sensor Emulator Module Test Class.
    """
    # Update type hints
    module: Paw3266Module

    # Constants
    dut_vcc_sensor: float = 2.0  # Volts, from datasheet
    dut_sensor_polling_frequency_hz: float = 124.226  # Hertz, as measured with a Logic Analyzer
    sensor_power_up_to_reset_done_time_s: float = 57.23 / 1000  # Seconds, as measured with a Logic Analyzer
    sensor_power_up_to_setup_done_time_s: float = 93.47 / 1000  # Seconds, as measured with a Logic Analyzer

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``Paw3266Module``

        :raise ``AssertionError``: Module is not defined in the Device Tree
        """
        assert cls.kosmos.dt.spi_paw3266[0], 'SPI PAW3266 Module is not present in the Device Tree'
        return cls.kosmos.dt.spi_paw3266[0]
    # end def _get_module_under_test

    def test_ll_ctrl_power_modes(self):
        """
        Validate Low-level Control State Updates
        """
        # Shorthand notations
        raw = self.module.get_raw_instruction
        cmp = self.module.get_compressed_instruction
        r = self.module.ll_ctrl.reg_map.Registers
        t = self.module.ll_ctrl.reg_map.Types
        c = self.module.ll_ctrl.reg_map.Commands
        T = LowLevelTest
        IN = LowLevelInput

        tests = [
            T(i_reg=[IN(addr=r.OBSERVATION, val=t.OBSERVATION.MODE_REST1, mask=t.OBSERVATION.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.OBSERVATION_SET, cmd_val=t.OBSERVATION.MODE_REST1),
                     raw(cmd_idx=c.OBSERVATION_CLR, cmd_val=t.OBSERVATION.MODE_REST2, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.OBSERVATION, val=t.OBSERVATION.MODE_REST2, mask=t.OBSERVATION.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.OBSERVATION_SET, cmd_val=t.OBSERVATION.MODE_REST2),
                     raw(cmd_idx=c.OBSERVATION_CLR, cmd_val=t.OBSERVATION.MODE_REST1, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.OBSERVATION, val=t.OBSERVATION(0), mask=t.OBSERVATION.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.OBSERVATION_SET, cmd_val=t.OBSERVATION(0)),
                     raw(cmd_idx=c.OBSERVATION_CLR, cmd_val=t.OBSERVATION.MODE_REST3, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.OBSERVATION, val=t.OBSERVATION.MODE_REST3, mask=t.OBSERVATION.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.OBSERVATION_SET, cmd_val=t.OBSERVATION.MODE_REST3),
                     raw(cmd_idx=c.OBSERVATION_CLR, cmd_val=t.OBSERVATION(0), send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.OBSERVATION, val=t.OBSERVATION(0), mask=t.OBSERVATION.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.OBSERVATION_SET, cmd_val=t.OBSERVATION(0)),
                     raw(cmd_idx=c.OBSERVATION_CLR, cmd_val=t.OBSERVATION.MODE_REST3, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.OBSERVATION, val=None, mask=t.OBSERVATION.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.OBSERVATION_CLR, cmd_val=t.OBSERVATION(0), send=True)],
              o_cmp=IDEM),
        ]

        self.run_control_tests(tests=tests, compression={False, True})
    # end def test_ll_ctrl_power_modes

    def test_hl_ctrl(self):
        # See ``OptEmuTestCaseMixin.test_hl_ctrl``
        # Shorthand notations
        raw = self.module.get_raw_instruction
        cmp = self.module.get_compressed_instruction
        nop = self.module.get_nop_instruction
        t = self.module.ll_ctrl.reg_map.Types
        c = self.module.ll_ctrl.reg_map.Commands
        T = HighLevelTest
        IN = HighLevelInput

        tests = [
            T(i_actions=[IN(Action.STATUS_MOTION, True)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION.MOT, send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, False)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION(0)),
                     raw(cmd_idx=c.MOTION_CLR, cmd_val=t.MOTION.MOT, send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, True)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION.MOT),
                     raw(cmd_idx=c.MOTION_CLR, cmd_val=t.MOTION(0), send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, None)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION(0), send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, True)],
              o_raw=[raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT.LIFT, send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, False)],
              o_raw=[raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT(0), send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, True), IN(Action.LIFT, True), IN(Action.LIFT, False)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION.MOT, send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, True), IN(Action.LIFT, False)],
              o_raw=[nop(send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, True), IN(Action.LIFT, False)],
              o_raw=[nop(send=True)],
              o_cmp=IDEM),
        ]

        self.run_control_tests(tests=tests, compression=[False, True])
    # end def test_hl_ctrl
# end class Paw3266ModuleTestCase


@require_kosmos_device(DeviceName.SPI_PMW3816)
class Pmw3816ModuleTestCase(PixArtOptEmuAbstractTestClass.PixArt16BitsOptEmuTestCaseMixin):
    """
    Kosmos PixArt PMW3816 TCOG6 Sensor Emulator Module Test Class.
    """
    # Update type hints
    module: Pmw3816Module

    # Constants
    dut_vcc_sensor: float = 2.0  # Volts, from datasheet
    dut_sensor_polling_frequency_hz: float = 250  # Hertz, as measured with a Logic Analyzer
    sensor_power_up_to_reset_done_time_s: float = 68.41 / 1000  # Seconds, as measured with a Logic Analyzer
    sensor_power_up_to_setup_done_time_s: float = 77.60 / 1000  # Seconds, as measured with a Logic Analyzer

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``Pmw3816Module``

        :raise ``AssertionError``: Module is not defined in the Device Tree
        """
        assert cls.kosmos.dt.spi_pmw3816[0], 'SPI PMW3816 Module is not present in the Device Tree'
        return cls.kosmos.dt.spi_pmw3816[0]
    # end def _get_module_under_test

    def test_ll_ctrl_power_modes(self):
        """
        Validate Low-level Control State Updates
        """
        # Shorthand notations
        raw = self.module.get_raw_instruction
        cmp = self.module.get_compressed_instruction
        r = self.module.ll_ctrl.reg_map.Registers
        t = self.module.ll_ctrl.reg_map.Types
        c = self.module.ll_ctrl.reg_map.Commands
        T = LowLevelTest
        IN = LowLevelInput

        tests = [
            T(i_reg=[IN(addr=r.PERFORMANCE, val=t.PERFORMANCE.MODE_REST1, mask=t.PERFORMANCE.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.PERFORMANCE_SET, cmd_val=t.PERFORMANCE.MODE_REST1),
                     raw(cmd_idx=c.PERFORMANCE_CLR, cmd_val=t.PERFORMANCE.MODE_REST2, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.PERFORMANCE, val=t.PERFORMANCE.MODE_REST2, mask=t.PERFORMANCE.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.PERFORMANCE_SET, cmd_val=t.PERFORMANCE.MODE_REST2),
                     raw(cmd_idx=c.PERFORMANCE_CLR, cmd_val=t.PERFORMANCE.MODE_REST1, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.PERFORMANCE, val=t.PERFORMANCE(0), mask=t.PERFORMANCE.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.PERFORMANCE_SET, cmd_val=t.PERFORMANCE(0)),
                     raw(cmd_idx=c.PERFORMANCE_CLR, cmd_val=t.PERFORMANCE.MODE_REST3, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.PERFORMANCE, val=t.PERFORMANCE.MODE_REST3, mask=t.PERFORMANCE.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.PERFORMANCE_SET, cmd_val=t.PERFORMANCE.MODE_REST3),
                     raw(cmd_idx=c.PERFORMANCE_CLR, cmd_val=t.PERFORMANCE(0), send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.PERFORMANCE, val=t.PERFORMANCE(0), mask=t.PERFORMANCE.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.PERFORMANCE_SET, cmd_val=t.PERFORMANCE(0)),
                     raw(cmd_idx=c.PERFORMANCE_CLR, cmd_val=t.PERFORMANCE.MODE_REST3, send=True)],
              o_cmp=IDEM),
            T(i_reg=[IN(addr=r.PERFORMANCE, val=None, mask=t.PERFORMANCE.MODE_REST3)],
              o_raw=[raw(cmd_idx=c.PERFORMANCE_CLR, cmd_val=t.PERFORMANCE(0), send=True)],
              o_cmp=IDEM),
        ]

        self.run_control_tests(tests=tests, compression={False, True})
    # end def test_ll_ctrl_power_modes

    def test_hl_ctrl(self):
        # See ``OptEmuTestCaseMixin.test_hl_ctrl``
        # Shorthand notations
        raw = self.module.get_raw_instruction
        cmp = self.module.get_compressed_instruction
        nop = self.module.get_nop_instruction
        t = self.module.ll_ctrl.reg_map.Types
        c = self.module.ll_ctrl.reg_map.Commands
        l = self.module.ll_ctrl.reg_map.Limits
        T = HighLevelTest
        IN = HighLevelInput

        tests = [
            T(i_actions=[IN(Action.STATUS_MOTION, True)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION.MOT, send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, False)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION(0)),
                     raw(cmd_idx=c.MOTION_CLR, cmd_val=t.MOTION.MOT, send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, True)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION.MOT),
                     raw(cmd_idx=c.MOTION_CLR, cmd_val=t.MOTION(0), send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, None)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION(0), send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, True)],
              o_raw=[raw(cmd_idx=c.SQUAL, cmd_val=l.LIFT_THRESHOLD - 1, send=True)],  # Lift ON: SQUAL < LIFT_THRESHOLD
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, False)],
              o_raw=[raw(cmd_idx=c.SQUAL, cmd_val=l.LIFT_THRESHOLD, send=True)],     # Lift OFF: SQUAL >= LIFT_THRESHOLD
              o_cmp=IDEM),
            T(i_actions=[IN(Action.STATUS_MOTION, True), IN(Action.LIFT, True), IN(Action.LIFT, False)],
              o_raw=[raw(cmd_idx=c.MOTION_SET, cmd_val=t.MOTION.MOT, send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, True), IN(Action.LIFT, False)],
              o_raw=[nop(send=True)],
              o_cmp=IDEM),
            T(i_actions=[IN(Action.LIFT, True), IN(Action.LIFT, False)],
              o_raw=[nop(send=True)],
              o_cmp=IDEM),
        ]

        self.run_control_tests(tests=tests, compression=[False, True])
    # end def test_hl_ctrl
# end class Pmw3816ModuleTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
