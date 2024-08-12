#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.optemu_em
:brief: Kosmos EM (Electronic Marin) Optical Sensors Emulator Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/12/09
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta

from pyraspi.services.kosmos.module.model.optemu.em import Em12BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.em import Em16BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.em import EmRegisterMapBase
from pyraspi.services.kosmos.module.optemu import OptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu import OptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu import OptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_12bits import OptEmu12BitsHighLevelControl
from pyraspi.services.kosmos.module.optemu_12bits import OptEmu12BitsLowLevelControl
from pyraspi.services.kosmos.module.optemu_12bits import OptEmu12BitsModuleMixin
from pyraspi.services.kosmos.module.optemu_16bits import OptEmu16BitsHighLevelControl
from pyraspi.services.kosmos.module.optemu_16bits import OptEmu16BitsLowLevelControl
from pyraspi.services.kosmos.module.optemu_16bits import OptEmu16BitsModuleMixin
from pyraspi.services.kosmos.module.optemu_interfaces import Action


# ------------------------------------------------------------------------------
# EM (Electronic Marin) Optical Sensor Emulator Low-Level Module Mixin Classes
# ------------------------------------------------------------------------------

class EmOptEmuLowLevelControlMixin(OptEmuLowLevelControlMixin, metaclass=ABCMeta):
    """
    EM (Electronic Marin) Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    module: 'EmOptEmuModuleMixin'
    reg_map: EmRegisterMapBase

    def _get_lift(self, state):
        # See ``OptEmuLowLevelControlMixin._get_lift``
        # Shorthand notations
        c = self.reg_map.Commands
        r = self.reg_map.Registers
        t = self.reg_map.Types
        lift = state.regvs[r.LIFTSTAT].value
        return self.LiftLowLevelStatus(reg=lift,
                                       status=(lift == t.LIFTSTAT.SF_LIFT),
                                       masked=(lift & ~t.LIFTSTAT.SF_LIFT),
                                       cmd_idx=c.LIFTSTAT)
    # end def _get_lift
# end class EmOptEmuLowLevelControlMixin


class Em12BitsOptEmuLowLevelControlMixin(EmOptEmuLowLevelControlMixin, OptEmu12BitsLowLevelControl):
    """
    EM (Electronic Marin) 12-bits Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    reg_map: Em12BitsRegisterMap
# end class Em12BitsOptEmuLowLevelControlMixin


class Em16BitsOptEmuLowLevelControlMixin(EmOptEmuLowLevelControlMixin, OptEmu16BitsLowLevelControl):
    """
    EM (Electronic Marin) 16-bits Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    reg_map: Em16BitsRegisterMap
# end class Em16BitsOptEmuLowLevelControlMixin


# ------------------------------------------------------------------------------
# EM (Electronic Marin) Optical Sensor Emulator High-Level Module Mixin Classes
# ------------------------------------------------------------------------------

class EmOptEmuHighLevelControlMixin(OptEmuHighLevelControlMixin, metaclass=ABCMeta):
    """
    EM (Electronic Marin) Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    module: 'EmOptEmuModuleMixin'
    ll_ctrl: EmOptEmuLowLevelControlMixin

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        t = self.ll_ctrl.reg_map.Types

        if action == Action.LIFT:
            self.ll_ctrl.update_reg(reg_addr=r.LIFTSTAT,
                                    value=t.LIFTSTAT.SF_LIFT if value else t.LIFTSTAT(0),
                                    mask=t.LIFTSTAT.SF_LIFT)
        elif action == Action.STATUS_MOTION:
            val = None if value is None else t.STATUS.MOTION if value else t.STATUS(0)
            self.ll_ctrl.update_reg(reg_addr=r.STATUS,
                                    value=val,
                                    mask=t.STATUS.MOTION)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class EmOptEmuHighLevelControlMixin


class Em12BitsOptEmuHighLevelControlMixin(EmOptEmuHighLevelControlMixin, OptEmu12BitsHighLevelControl):
    """
    EM (Electronic Marin) 12-bits Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    ll_ctrl: Em12BitsOptEmuLowLevelControlMixin

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        t = self.ll_ctrl.reg_map.Types

        if action == Action.POWER_MODE_REST2:
            val = None if value is None else t.CONTROL.FORCE_REST2 if value else t.CONTROL(0)
            self.ll_ctrl.update_reg(reg_addr=r.CONTROL,
                                    value=val,
                                    mask=t.CONTROL.FORCE_REST_BITS)
        elif action == Action.POWER_MODE_SLEEP:
            val = None if value is None else t.CONTROL.FORCE_SLEEP if value else t.CONTROL(0)
            self.ll_ctrl.update_reg(reg_addr=r.CONTROL,
                                    value=val,
                                    mask=t.CONTROL.FORCE_REST_BITS)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class Em12BitsOptEmuHighLevelControlMixin


class Em16BitsOptEmuHighLevelControlMixin(EmOptEmuHighLevelControlMixin, OptEmu16BitsHighLevelControl):
    """
    EM (Electronic Marin) 16-bits Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    ll_ctrl: Em16BitsOptEmuLowLevelControlMixin

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        t = self.ll_ctrl.reg_map.Types

        if action == Action.POWER_MODE_REST2:
            val = None if value is None else t.CONTROL2.FORCE_REST2 if value else t.CONTROL2(0)
            self.ll_ctrl.update_reg(reg_addr=r.CONTROL2,
                                    value=val,
                                    mask=t.CONTROL2.FORCE_REST_BITS)
        elif action == Action.POWER_MODE_SLEEP:
            val = None if value is None else t.CONTROL2.FORCE_SLEEP if value else t.CONTROL2(0)
            self.ll_ctrl.update_reg(reg_addr=r.CONTROL2,
                                    value=val,
                                    mask=t.CONTROL2.FORCE_REST_BITS)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class Em16BitsOptEmuHighLevelControlMixin


# ------------------------------------------------------------------------------
# EM (Electronic Marin) Optical Sensor Emulator Module Mixin Classes
# ------------------------------------------------------------------------------

class EmOptEmuModuleMixin(OptEmuModuleMixin, metaclass=ABCMeta):
    """
    EM (Electronic Marin) Optical Sensor Emulator Module Mixin Class.
    """
    # update type hits
    ll_ctrl: EmOptEmuLowLevelControlMixin
    hl_ctrl: EmOptEmuHighLevelControlMixin
# end class EmOptEmuModuleMixin


class Em12BitsOptEmuModuleMixin(EmOptEmuModuleMixin, OptEmu12BitsModuleMixin, metaclass=ABCMeta):
    """
    EM (Electronic Marin) 12-bits Optical Sensor Emulator Module Mixin Class.
    """
    # update type hits
    ll_ctrl: Em12BitsOptEmuLowLevelControlMixin
    hl_ctrl: Em12BitsOptEmuHighLevelControlMixin
# end class Em12BitsOptEmuModuleMixin


class Em16BitsOptEmuModuleMixin(EmOptEmuModuleMixin, OptEmu16BitsModuleMixin, metaclass=ABCMeta):
    """
    EM (Electronic Marin) 16-bits Optical Sensor Emulator Module Mixin Class.
    """
    # update type hits
    ll_ctrl: Em16BitsOptEmuLowLevelControlMixin
    hl_ctrl: Em16BitsOptEmuHighLevelControlMixin
# end class Em16BitsOptEmuModuleMixin


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
