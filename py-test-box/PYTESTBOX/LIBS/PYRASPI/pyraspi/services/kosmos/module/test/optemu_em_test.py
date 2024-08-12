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
from abc import abstractmethod

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.model.optemu.em import Em12BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.em import Em16BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.em import EmRegisterMapBase
from pyraspi.services.kosmos.module.optemu import Action
from pyraspi.services.kosmos.module.optemu_em import Em12BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em12BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em12BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_em import Em16BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em16BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em16BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_em import EmOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import EmOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import EmOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_sensors import E7788Module
from pyraspi.services.kosmos.module.optemu_sensors import E7790Module
from pyraspi.services.kosmos.module.optemu_sensors import E7792Module
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
class EmOptEmuAbstractTestClass:
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """

    class EmOptEmuTestCaseMixin(OptEmuAbstractTestClass.OptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # update type hits
        module: EmOptEmuModuleMixin

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class

            :raise ``AssertionError``: Invalid module attribute types
            """
            super().setUpClass()
            assert isinstance(cls.module, EmOptEmuModuleMixin), cls.module
            assert isinstance(cls.module.ll_ctrl, EmOptEmuLowLevelControlMixin), cls.module.ll_ctrl
            assert isinstance(cls.module.hl_ctrl, EmOptEmuHighLevelControlMixin), cls.module.hl_ctrl
            assert isinstance(cls.module.ll_ctrl.reg_map, EmRegisterMapBase), cls.reg_map
        # end def setUpClass

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
                  o_raw=[raw(cmd_idx=c.STATUS_SET, cmd_val=t.STATUS.MOTION, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.STATUS_MOTION, False)],
                  o_raw=[raw(cmd_idx=c.STATUS_SET, cmd_val=t.STATUS(0)),
                         raw(cmd_idx=c.STATUS_CLR, cmd_val=t.STATUS.MOTION, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.STATUS_MOTION, True)],
                  o_raw=[raw(cmd_idx=c.STATUS_SET, cmd_val=t.STATUS.MOTION),
                         raw(cmd_idx=c.STATUS_CLR, cmd_val=t.STATUS(0), send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.STATUS_MOTION, None)],
                  o_raw=[raw(cmd_idx=c.STATUS_SET, cmd_val=t.STATUS(0), send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.LIFT, True)],
                  o_raw=[raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT.SF_LIFT, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.LIFT, False)],
                  o_raw=[raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT(0), send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.STATUS_MOTION, True), IN(Action.LIFT, True), IN(Action.LIFT, False)],
                  o_raw=[raw(cmd_idx=c.STATUS_SET, cmd_val=t.STATUS.MOTION, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.LIFT, True), IN(Action.LIFT, False)],
                  o_raw=[nop(send=True)],
                  o_cmp=IDEM),
            ]

            self.run_control_tests(tests=tests, compression={False, True})
        # end def test_hl_ctrl
    # end class EmOptEmuTestCaseMixin

    class Em12BitsOptEmuTestCaseMixin(OptEmuAbstractTestClass.OptEmu12BitsTestCaseMixin,
                                      EmOptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """

        # update type hits
        module: Em12BitsOptEmuModuleMixin

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class
            """
            super().setUpClass()
            assert isinstance(cls.module, Em12BitsOptEmuModuleMixin), cls.module
            assert isinstance(cls.module.ll_ctrl, Em12BitsOptEmuLowLevelControlMixin), cls.module.ll_ctrl
            assert isinstance(cls.module.hl_ctrl, Em12BitsOptEmuHighLevelControlMixin), cls.module.hl_ctrl
            assert isinstance(cls.module.ll_ctrl.reg_map, Em12BitsRegisterMap), cls.reg_map
        # end def setUpClass

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
                T(i_reg=[IN(addr=r.CONTROL, val=t.CONTROL.FORCE_SLEEP, mask=t.CONTROL.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL_SET, cmd_val=t.CONTROL.FORCE_SLEEP),
                         raw(cmd_idx=c.CONTROL_CLR, cmd_val=t.CONTROL.FORCE_REST2, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL, val=t.CONTROL.FORCE_REST2, mask=t.CONTROL.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL_SET, cmd_val=t.CONTROL.FORCE_REST2),
                         raw(cmd_idx=c.CONTROL_CLR, cmd_val=t.CONTROL.FORCE_SLEEP, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL, val=None, mask=t.CONTROL.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL_SET, cmd_val=t.CONTROL(0)),
                         raw(cmd_idx=c.CONTROL_CLR, cmd_val=t.CONTROL(0), send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL, val=t.CONTROL.FORCE_REST_BITS, mask=t.CONTROL.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL_SET, cmd_val=t.CONTROL.FORCE_REST_BITS, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL, val=t.CONTROL(0), mask=t.CONTROL.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL_SET, cmd_val=t.CONTROL(0)),
                         raw(cmd_idx=c.CONTROL_CLR, cmd_val=t.CONTROL.FORCE_REST_BITS, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL, val=None, mask=t.CONTROL.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL_CLR, cmd_val=t.CONTROL(0), send=True)],
                  o_cmp=IDEM),
            ]

            self.run_control_tests(tests=tests, compression={False, True})
        # end def test_ll_ctrl_power_modes

        def test_high_level_control_delta_xy_lift(self):
            """
            Validate the Delta X/Y displacement and Lift actions
            """
            # Shorthand notations
            raw = self.module.get_raw_instruction
            cmp = self.module.get_compressed_instruction
            t = self.module.ll_ctrl.reg_map.Types
            c = self.module.ll_ctrl.reg_map.Commands
            T = HighLevelTest
            IN = HighLevelInput

            tests = [
                T(i_actions=[IN(Action.LIFT, True)],
                  o_raw=[raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT.SF_LIFT, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.LIFT, False)],
                  o_raw=[raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT(0), send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 1), IN(Action.LIFT, True)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=1),
                         raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT.SF_LIFT, send=True)],
                  o_cmp=[cmp(dx=1, lift=True)]),
                T(i_actions=[IN(Action.DX, 2)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=2, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.LIFT, False)],
                  o_raw=[raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT(0), send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 3), IN(Action.DY, 1)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=3),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=1, send=True)],
                  o_cmp=[cmp(dx=3, dy=1, lift=False)]),
                T(i_actions=[IN(Action.DX, 1), IN(Action.DY, 3), IN(Action.LIFT, True)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=1),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=3),
                         raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT.SF_LIFT, send=True)],
                  o_cmp=[cmp(dx=1, dy=3, lift=True)]),
                T(i_actions=[IN(Action.DX, -1), IN(Action.DY, 3)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=-1),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0xF0, send=True)],
                  o_cmp=[cmp(dx=-1, dy=3, lift=True)]),
                T(i_actions=[IN(Action.DX, -10), IN(Action.DY, 3)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=0xF6, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, -0x100), IN(Action.DY, 2)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=0),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=2, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, -0x100), IN(Action.DY, 4)],
                  o_raw=[raw(cmd_idx=c.DELTA_Y_L, cmd_val=4, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, -1), IN(Action.DY, -1)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=0xFF),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=0xFF),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0xFF, send=True)],
                  o_cmp=[cmp(dx=-1, dy=-1, lift=True)]),
                T(i_actions=[IN(Action.DX, 1), IN(Action.DY, 2)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=1),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=2),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0x00, send=True)],
                  o_cmp=[cmp(dx=1, dy=2, lift=True)]),
                T(i_actions=[IN(Action.DX, 0x123), IN(Action.DY, 0x456)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=0x23),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=0x56),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0x14, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 1), IN(Action.DY, 0x456)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=1),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0x04, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 0x123), IN(Action.DY, 0x456)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=0x23),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0x14, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 0x100), IN(Action.DY, 0x456)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=0x00, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 1), IN(Action.DY, 2)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=1),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=2),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0, send=True)],
                  o_cmp=[cmp(dx=1, dy=2, lift=True)]),
                T(i_actions=[IN(Action.DX, 1), IN(Action.DY, 0x42)],
                  o_raw=[raw(cmd_idx=c.DELTA_Y_L, cmd_val=0x42, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 2), IN(Action.DY, 0x42)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=2, send=True)],
                  o_cmp=IDEM),
                T(i_actions=[IN(Action.DX, 2), IN(Action.DY, -1)],
                  o_raw=[raw(cmd_idx=c.DELTA_Y_L, cmd_val=0xFF),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0x0F, send=True)],
                  o_cmp=[cmp(dx=2, dy=-1, lift=True)]),
                T(i_actions=[IN(Action.DX, -1), IN(Action.DY, 1), IN(Action.LIFT, False)],
                  o_raw=[raw(cmd_idx=c.DELTA_X_L, cmd_val=0xFF),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=1),
                         raw(cmd_idx=c.DELTA_XY_H, cmd_val=0xF0),
                         raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT(0), send=True)],
                  o_cmp=[cmp(dx=-1, dy=1, lift=False)]),
                T(i_actions=[IN(Action.DX, -2), IN(Action.DY, 2),
                             IN(Action.LIFT, True), IN(Action.STATUS_MOTION, True)],
                  o_raw=[raw(cmd_idx=c.STATUS_SET, cmd_val=t.STATUS.MOTION),
                         raw(cmd_idx=c.DELTA_X_L, cmd_val=0xFE),
                         raw(cmd_idx=c.DELTA_Y_L, cmd_val=2),
                         raw(cmd_idx=c.LIFTSTAT, cmd_val=t.LIFTSTAT.SF_LIFT, send=True)],
                  o_cmp=[raw(cmd_idx=c.STATUS_SET, cmd_val=t.STATUS.MOTION),
                         cmp(dx=-2, dy=2, lift=True)]),
            ]

            self.run_control_tests(tests=tests, compression={False, True})
        # end def test_high_level_control_delta_xy_lift
    # end class Em12BitsOptEmuTestCaseMixin

    class Em16BitsOptEmuTestCaseMixin(OptEmuAbstractTestClass.OptEmu16BitsTestCaseMixin,
                                      EmOptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # update type hits
        module: Em16BitsOptEmuModuleMixin

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class

            :raise ``AssertionError``: Invalid module attribute types
            """
            super().setUpClass()
            assert isinstance(cls.module, Em16BitsOptEmuModuleMixin), cls.module
            assert isinstance(cls.module.ll_ctrl, Em16BitsOptEmuLowLevelControlMixin), cls.module.ll_ctrl
            assert isinstance(cls.module.hl_ctrl, Em16BitsOptEmuHighLevelControlMixin), cls.module.hl_ctrl
            assert isinstance(cls.module.ll_ctrl.reg_map, Em16BitsRegisterMap), cls.reg_map
        # end def setUpClass

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
                T(i_reg=[IN(addr=r.CONTROL2, val=t.CONTROL2.FORCE_SLEEP, mask=t.CONTROL2.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL2_SET, cmd_val=t.CONTROL2.FORCE_SLEEP),
                         raw(cmd_idx=c.CONTROL2_CLR, cmd_val=t.CONTROL2.FORCE_REST2, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL2, val=t.CONTROL2.FORCE_REST2, mask=t.CONTROL2.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL2_SET, cmd_val=t.CONTROL2.FORCE_REST2),
                         raw(cmd_idx=c.CONTROL2_CLR, cmd_val=t.CONTROL2.FORCE_SLEEP, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL2, val=None, mask=t.CONTROL2.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL2_SET, cmd_val=t.CONTROL2(0)),
                         raw(cmd_idx=c.CONTROL2_CLR, cmd_val=t.CONTROL2(0), send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL2, val=t.CONTROL2.FORCE_REST_BITS, mask=t.CONTROL2.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL2_SET, cmd_val=t.CONTROL2.FORCE_REST_BITS, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL2, val=t.CONTROL2(0), mask=t.CONTROL2.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL2_SET, cmd_val=t.CONTROL2(0)),
                         raw(cmd_idx=c.CONTROL2_CLR, cmd_val=t.CONTROL2.FORCE_REST_BITS, send=True)],
                  o_cmp=IDEM),
                T(i_reg=[IN(addr=r.CONTROL2, val=None, mask=t.CONTROL2.FORCE_REST_BITS)],
                  o_raw=[raw(cmd_idx=c.CONTROL2_CLR, cmd_val=t.CONTROL2(0), send=True)],
                  o_cmp=IDEM),
            ]

            self.run_control_tests(tests=tests, compression={False, True})
        # end def test_ll_ctrl_power_modes
    # end class Em16BitsOptEmuTestCaseMixin
# end class EmOptEmuAbstractTestClass


# ------------------------------------------------------------------------------
# Test case implementation
# ------------------------------------------------------------------------------

@require_kosmos_device(DeviceName.SPI_E7788)
class E7788ModuleTestCase(EmOptEmuAbstractTestClass.Em16BitsOptEmuTestCaseMixin):
    """
    Kosmos E7788 HERO Sensor Emulator Module Test Class.
    """
    # Update type hints
    module: E7788Module

    # Constants
    dut_vcc_sensor: float = 2.0  # Volts, from datasheet
    dut_sensor_polling_frequency_hz: float = 1000              # Hertz, depends on DUT firmware
    sensor_power_up_to_reset_done_time_s: float = 10.0 / 1000  # Seconds, estimated
    sensor_power_up_to_setup_done_time_s: float = 81.9 / 1000  # Seconds, as measured with a Logic Analyzer

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``E7788Module``

        :raise ``AssertionError``: Module is not defined in the Device Tree
        """
        assert cls.kosmos.dt.spi_e7788[0], 'SPI E7788 Module is not present in the Device Tree'
        return cls.kosmos.dt.spi_e7788[0]
    # end def _get_module_under_test
# end class E7788ModuleTestCase


@require_kosmos_device(DeviceName.SPI_E7790)
class E7790ModuleTestCase(EmOptEmuAbstractTestClass.Em16BitsOptEmuTestCaseMixin):
    """
    Kosmos E7790 HERO2 Sensor Emulator Module Test Class.
    """
    # Update type hints
    module: E7790Module

    # Constants
    dut_vcc_sensor: float = 2.0  # Volts, from datasheet
    dut_sensor_polling_frequency_hz: float = 1000              # Hertz, depends on DUT firmware
    sensor_power_up_to_reset_done_time_s: float = 10.0 / 1000  # Seconds, estimated
    sensor_power_up_to_setup_done_time_s: float = 128. / 1000  # Seconds, as measured with a Logic Analyzer

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``E7790Module``

        :raise ``AssertionError``: Module is not defined in the Device Tree
        """
        assert cls.kosmos.dt.spi_e7790[0], 'SPI E7790 Module is not present in the Device Tree'
        return cls.kosmos.dt.spi_e7790[0]
    # end def _get_module_under_test
# end class E7790ModuleTestCase


@require_kosmos_device(DeviceName.SPI_E7792)
class E7792ModuleTestCase(EmOptEmuAbstractTestClass.Em12BitsOptEmuTestCaseMixin):
    """
    Kosmos E7792 Pluto One Sensor Emulator Module Test Class.
    """
    # Update type hints
    module: E7792Module

    # Constants
    dut_vcc_sensor: float = 2.0  # Volts, from datasheet
    dut_sensor_polling_frequency_hz: float = 246.829  # 255    # Hertz, depends on DUT firmware
    sensor_power_up_to_reset_done_time_s: float = 10.0 / 1000  # Seconds, estimated
    sensor_power_up_to_setup_done_time_s: float = 34.8 / 1000  # Seconds, as measured with a Logic Analyzer

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``E7792Module``

        :raise ``AssertionError``: Module is not defined in the Device Tree
        """
        assert cls.kosmos.dt.spi_e7792[0], 'SPI E7792 Module is not present in the Device Tree'
        return cls.kosmos.dt.spi_e7792[0]
    # end def _get_module_under_test
# end class E7792ModuleTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
