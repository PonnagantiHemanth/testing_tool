#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.optemu_em12bits
:brief: Kosmos EM (Electronic Marin) 12-bit Optical Sensors Emulator Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/03/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from typing import Tuple

from pyraspi.services.kosmos.module.model.optemu.base import OptEmu12BitsRegisterMapBase
from pyraspi.services.kosmos.module.optemu import OptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu import OptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu import OptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_interfaces import Action
from pyraspi.services.kosmos.utils import sign_ext_12bits


# ------------------------------------------------------------------------------
# Interface implementation
# ------------------------------------------------------------------------------
class OptEmu12BitsLowLevelControl(OptEmuLowLevelControlMixin, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Low-Level Control Mixin Class for Electro-Marin (EM) 12-bit Optical Sensors family.
    """
    # update type hits
    reg_map: OptEmu12BitsRegisterMapBase

    @staticmethod
    def _compute_deltas(dx, dy, dh):
        """
        Process commands and compute the numerical value of DeltaX and DeltaY displacements, as unsigned integers.

        :param dx: DeltaX register value as unsigned 8-bit integer
        :type dx: ``int``
        :param dy: DeltaY register value as unsigned 8-bit integer
        :type dy: ``int``
        :param dh: DeltaH register value as unsigned 8-bit integer
        :type dh: ``int``

        :return: DeltaX & DeltaY complete values, as unsigned 12-bit integers
        :rtype:  ``Tuple[int, int]``
        """
        dx_out = ((dh & 0xF0) << 4) | dx  # dX := high_nibble(DeltaH) | DeltaX
        dy_out = ((dh & 0x0F) << 8) | dy  # dY :=  low_nibble(DeltaH) | DeltaY
        return dx_out, dy_out
    # end def _compute_deltas

    @classmethod
    def _compute_deltas_signed(cls, dx, dy, dh):
        """
        Process commands and compute the numerical value of DeltaX and DeltaY displacements, as signed integers.

        :param dx: DeltaX register value as unsigned 8-bit integer
        :type dx: ``int``
        :param dy: DeltaY register value as unsigned 8-bit integer
        :type dy: ``int``
        :param dh: DeltaH register value as unsigned 8-bit integer
        :type dh: ``int``

        :return: DeltaX & DeltaY complete 12-bit values, as signed Python integers
        :rtype:  ``Tuple[int, int]``
        """
        dx_u, dy_u = cls._compute_deltas(dx=dx, dy=dy, dh=dh)
        dx_s = sign_ext_12bits(dx_u)
        dy_s = sign_ext_12bits(dy_u)
        return dx_s, dy_s
    # end def _compute_deltas_signed

    def _get_signed_deltas(self, state):
        # See ``OptEmuLowLevelControlMixin._get_signed_deltas``
        # Shorthand notations
        r = self.reg_map.Registers

        return self._compute_deltas_signed(dx=state.regvs[r.DELTA_X_L].value,
                                           dy=state.regvs[r.DELTA_Y_L].value,
                                           dh=state.regvs[r.DELTA_XY_H].value)
    # end def _get_signed_deltas
# end class OptEmu12BitsLowLevelControl


class OptEmu12BitsHighLevelControl(OptEmuHighLevelControlMixin, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator High-Level Control Mixin Class for Electro-Marin (EM) 12-bit Optical Sensors family.
    """
    # update type hits
    module: OptEmuModuleMixin
    ll_ctrl: OptEmu12BitsLowLevelControl

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        l = self.ll_ctrl.reg_map.Limits

        if action == Action.DX:
            assert l.DELTA_SIGNED_MIN <= value <= l.DELTA_SIGNED_MAX, \
              f'DeltaX value {value} is out-of-bounds [{l.DELTA_SIGNED_MIN}, {l.DELTA_SIGNED_MAX}]'
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_X_L, value=value & 0xFF)
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_XY_H, value=(value >> 4) & 0xF0, mask=0xF0)
        elif action == Action.DY:
            assert l.DELTA_SIGNED_MIN <= value <= l.DELTA_SIGNED_MAX, \
              f'DeltaY value {value} is out-of-bounds [{l.DELTA_SIGNED_MIN}, {l.DELTA_SIGNED_MAX}]'
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_Y_L, value=value & 0xFF)
            self.ll_ctrl.update_reg(reg_addr=r.DELTA_XY_H, value=(value >> 8) & 0x0F, mask=0x0F)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class OptEmu12BitsHighLevelControl


class OptEmu12BitsModuleMixin(OptEmuModuleMixin, metaclass=ABCMeta):
    """
    Kosmos Optical Sensors Emulators module base class.
    """
    # update type hits
    ll_ctrl: OptEmu12BitsLowLevelControl
    hl_ctrl: OptEmu12BitsHighLevelControl
# end class OptEmu12BitsModuleMixin


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
