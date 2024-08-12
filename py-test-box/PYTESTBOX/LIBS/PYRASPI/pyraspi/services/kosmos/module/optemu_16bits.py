#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.optemu_em16bits
:brief: Kosmos EM (Electronic Marin) 16-bit Optical Sensors Emulator Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/12/09
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from ctypes import c_int16
from typing import Tuple

from pyraspi.services.kosmos.module.model.optemu.base import OptEmu16BitsRegisterMapBase
from pyraspi.services.kosmos.module.optemu import Action
from pyraspi.services.kosmos.module.optemu import OptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu import OptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu import OptEmuModuleMixin


# ------------------------------------------------------------------------------
# Interface implementation
# ------------------------------------------------------------------------------
class OptEmu16BitsLowLevelControl(OptEmuLowLevelControlMixin, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Low-Level Control Mixin Class for Electro-Marin (EM) 16-bit Optical Sensors family.
    """

    reg_map: OptEmu16BitsRegisterMapBase

    @staticmethod
    def _compute_deltas(dx_h, dx_l, dy_h, dy_l):
        """
        Compute the numerical value of DeltaX and DeltaY displacements, as unsigned integers.

        :param dx_h: DeltaX higher-byte register value as unsigned 8-bit integer
        :type dx_h: ``int``
        :param dx_l: DeltaX lower-byte register value as unsigned 8-bit integer
        :type dx_l: ``int``
        :param dy_h: DeltaY higher-byte register value as unsigned 8-bit integer
        :type dy_h: ``int``
        :param dy_l: DeltaY lower-byte register value as unsigned 8-bit integer
        :type dy_l: ``int``

        :return: DeltaX & DeltaY complete values, as unsigned 16-bit integers
        :rtype:  ``Tuple[int, int]``
        """
        dx_out = (dx_h << 8) | dx_l
        dy_out = (dy_h << 8) | dy_l
        return dx_out, dy_out
    # end def _compute_deltas

    @classmethod
    def _compute_deltas_signed(cls, dx_h, dx_l, dy_h, dy_l):
        """
        Compute the numerical value of DeltaX and DeltaY displacements, as signed integers.

        :param dx_h: DeltaX higher-byte register value as unsigned 8-bit integer
        :type dx_h: ``int``
        :param dx_l: DeltaX lower-byte register value as unsigned 8-bit integer
        :type dx_l: ``int``
        :param dy_h: DeltaY higher-byte register value as unsigned 8-bit integer
        :type dy_h: ``int``
        :param dy_l: DeltaY lower-byte register value as unsigned 8-bit integer
        :type dy_l: ``int``

        :return: DeltaX & DeltaY complete 16-bit values, as signed Python integers
        :rtype:  ``Tuple[int, int]``
        """
        dx_u, dy_u = cls._compute_deltas(dx_h=dx_h, dx_l=dx_l, dy_h=dy_h, dy_l=dy_l)
        dx_s = c_int16(dx_u).value
        dy_s = c_int16(dy_u).value
        return dx_s, dy_s
    # end def _compute_deltas_signed

    def _get_signed_deltas(self, state):
        # See ``OptEmuLowLevelControlMixin._get_signed_deltas``
        # Shorthand notations
        r = self.reg_map.Registers

        return self._compute_deltas_signed(dx_h=state.regvs[r.DELTA_X_H].value,
                                           dx_l=state.regvs[r.DELTA_X_L].value,
                                           dy_h=state.regvs[r.DELTA_Y_H].value,
                                           dy_l=state.regvs[r.DELTA_Y_L].value)
    # end def _get_signed_deltas
# end class OptEmu16BitsLowLevelControl


class OptEmu16BitsHighLevelControl(OptEmuHighLevelControlMixin, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator High-Level Control Mixin Class for Electro-Marin (EM) 16-bit Optical Sensors family.
    """

    module: OptEmuModuleMixin
    ll_ctrl: OptEmu16BitsLowLevelControl

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        l = self.ll_ctrl.reg_map.Limits

        if action == Action.DX:
            assert l.DELTA_SIGNED_MIN <= value <= l.DELTA_SIGNED_MAX, \
              f'DeltaX value {value} is out-of-bounds [{l.DELTA_SIGNED_MIN}, {l.DELTA_SIGNED_MAX}]'
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_X_H, value=(value >> 8) & 0xFF)
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_X_L, value=value & 0xFF)
        elif action == Action.DY:
            assert l.DELTA_SIGNED_MIN <= value <= l.DELTA_SIGNED_MAX, \
              f'DeltaY value {value} is out-of-bounds [{l.DELTA_SIGNED_MIN}, {l.DELTA_SIGNED_MAX}]'
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_Y_H, value=(value >> 8) & 0xFF)
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_Y_L, value=value & 0xFF)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class OptEmu16BitsHighLevelControl


class OptEmu16BitsModuleMixin(OptEmuModuleMixin, metaclass=ABCMeta):
    """
    Kosmos Optical Sensors Emulators module base class.
    """

    # update type hits
    ll_ctrl: OptEmu16BitsLowLevelControl
    hl_ctrl: OptEmu16BitsHighLevelControl

# end class OptEmu16BitsModuleMixin

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
