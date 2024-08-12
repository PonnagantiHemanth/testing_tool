#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.optemu_pixart
:brief: Kosmos PixArt Optical Sensors Emulator Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/12/09
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
# PixArt Optical Sensor Emulator Low-Level Module Mixin Classes
# ------------------------------------------------------------------------------

class PixArtOptEmuLowLevelControlMixin(OptEmuLowLevelControlMixin, metaclass=ABCMeta):
    """
    PixArt Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    module: 'PixArtOptEmuModuleMixin'
    reg_map: PixArtRegisterMapBase
# end class PixArtOptEmuLowLevelControlMixin


class PixArt12BitsOptEmuLowLevelControlMixin(PixArtOptEmuLowLevelControlMixin, OptEmu12BitsLowLevelControl,
                                             metaclass=ABCMeta):
    """
    PixArt 12-bits Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    reg_map: PixArt12BitsRegisterMap
# end class PixArt12BitsOptEmuLowLevelControlMixin


class PixArt16BitsOptEmuLowLevelControlMixin(PixArtOptEmuLowLevelControlMixin, OptEmu16BitsLowLevelControl,
                                             metaclass=ABCMeta):
    """
    PixArt 16-bits Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    reg_map: PixArt16BitsRegisterMap
# end class PixArt16BitsOptEmuLowLevelControlMixin


class Paw3266OptEmuLowLevelControlMixin(PixArt12BitsOptEmuLowLevelControlMixin):
    """
    PixArt PAW3266 12-bits Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    reg_map: Paw3266RegisterMap

    def _get_lift(self, state):
        # See ``OptEmuLowLevelControlMixin._get_lift``
        # Shorthand notations
        c = self.reg_map.Commands
        r = self.reg_map.Registers
        t = self.reg_map.Types
        lift = state.regvs[r.LIFTSTAT].value
        return self.LiftLowLevelStatus(reg=lift,
                                       status=(lift == t.LIFTSTAT.LIFT),
                                       masked=(lift & ~t.LIFTSTAT.LIFT),
                                       cmd_idx=c.LIFTSTAT)
    # end def _get_lift
# end class Paw3266OptEmuLowLevelControlMixin


class Pmw3816OptEmuLowLevelControlMixin(PixArt16BitsOptEmuLowLevelControlMixin):
    """
    PixArt PMW3816 16-bits Optical Sensor Emulator Low-Level Module Mixin Class.
    """
    # update type hits
    reg_map: Pmw3816RegisterMap

    def _get_lift(self, state):
        # See ``OptEmuLowLevelControlMixin._get_lift``
        c = self.reg_map.Commands
        r = self.reg_map.Registers
        l = self.reg_map.Limits
        squal = state.regvs[r.SQUAL].value  # Note: Lift Status is computed from Surface Quality register
        status = squal < l.LIFT_THRESHOLD
        return self.LiftLowLevelStatus(reg=squal,
                                       status=status,
                                       masked=0x00 if status else squal,
                                       cmd_idx=c.SQUAL)
    # end def _get_lift
# end class Pmw3816OptEmuLowLevelControlMixin


# ------------------------------------------------------------------------------
# PixArt Optical Sensor Emulator High-Level Module Mixin Classes
# ------------------------------------------------------------------------------

class PixArtOptEmuHighLevelControlMixin(OptEmuHighLevelControlMixin, metaclass=ABCMeta):
    """
    PixArt Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    module: 'PixArtOptEmuModuleMixin'
    ll_ctrl: PixArtOptEmuLowLevelControlMixin

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        t = self.ll_ctrl.reg_map.Types

        if action == Action.STATUS_MOTION:
            val = None if value is None else t.MOTION.MOT if value else t.MOTION(0)
            self.ll_ctrl.update_reg(reg_addr=r.MOTION,
                                    value=val,
                                    mask=t.MOTION.MOT)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class PixArtOptEmuHighLevelControlMixin


class PixArt12BitsOptEmuHighLevelControlMixin(PixArtOptEmuHighLevelControlMixin, OptEmu12BitsHighLevelControl):
    """
    PixArt 12-bits Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    ll_ctrl: PixArt12BitsOptEmuLowLevelControlMixin
# end class PixArt12BitsOptEmuHighLevelControlMixin


class PixArt16BitsOptEmuHighLevelControlMixin(PixArtOptEmuHighLevelControlMixin, OptEmu16BitsHighLevelControl):
    """
    PixArt 16-bits Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    ll_ctrl: PixArt16BitsOptEmuLowLevelControlMixin
# end class PixArt16BitsOptEmuHighLevelControlMixin


class Paw3266OptEmuHighLevelControlMixin(PixArt12BitsOptEmuHighLevelControlMixin):
    """
    PixArt PAW3266 12-bits Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    ll_ctrl: Paw3266OptEmuLowLevelControlMixin

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        t = self.ll_ctrl.reg_map.Types

        if action == Action.LIFT:
            val = None if value is None else t.LIFTSTAT.LIFT if value else t.LIFTSTAT(0)
            self.ll_ctrl.update_reg(reg_addr=r.LIFTSTAT,
                                    value=val,
                                    mask=t.LIFTSTAT.LIFT)
        elif action == Action.POWER_MODE_REST2:
            val = None if value is None else t.OBSERVATION.MODE_REST2 if value else t.OBSERVATION(0)
            self.ll_ctrl.update_reg(reg_addr=r.OBSERVATION,
                                    value=val,
                                    mask=t.OBSERVATION.MODE_REST3)
        elif action == Action.POWER_MODE_SLEEP:
            val = None if value is None else t.OBSERVATION.MODE_REST3 if value else t.OBSERVATION(0)
            self.ll_ctrl.update_reg(reg_addr=r.OBSERVATION,
                                    value=val,
                                    mask=t.OBSERVATION.MODE_REST3)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class Paw3266OptEmuHighLevelControlMixin


class Pmw3816OptEmuHighLevelControlMixin(PixArt16BitsOptEmuHighLevelControlMixin):
    """
    PixArt PMW3816 16-bits Optical Sensor Emulator High-Level Module Mixin Class.
    """
    # update type hits
    ll_ctrl: Pmw3816OptEmuLowLevelControlMixin

    def _update(self, action, value):
        # See ``OptEmuHighLevelControlMixin._update``
        # Shorthand notations
        r = self.ll_ctrl.reg_map.Registers
        t = self.ll_ctrl.reg_map.Types
        l = self.ll_ctrl.reg_map.Limits

        if action == Action.LIFT:
            # Note: Lift Status is computed from Surface Quality register
            val = None if value is None else l.LIFT_THRESHOLD - 1 if value else l.LIFT_THRESHOLD
            self.ll_ctrl.update_reg(reg_addr=r.SQUAL,
                                    value=val,
                                    mask=0xFF)
        elif action == Action.POWER_MODE_REST2:
            val = None if value is None else t.PERFORMANCE.MODE_REST2 if value else t.PERFORMANCE(0)
            self.ll_ctrl.update_reg(reg_addr=r.PERFORMANCE,
                                    value=val,
                                    mask=t.PERFORMANCE.MODE_REST3)
        elif action == Action.POWER_MODE_SLEEP:
            val = None if value is None else t.PERFORMANCE.MODE_REST3 if value else t.PERFORMANCE(0)
            self.ll_ctrl.update_reg(reg_addr=r.PERFORMANCE,
                                    value=val,
                                    mask=t.PERFORMANCE.MODE_REST3)
        else:
            super()._update(action=action, value=value)
        # end if
    # end def _update
# end class Pmw3816OptEmuHighLevelControlMixin


# ------------------------------------------------------------------------------
# PixArt Optical Sensor Emulator Module Mixin Classes
# ------------------------------------------------------------------------------

class PixArtOptEmuModuleMixin(OptEmuModuleMixin, metaclass=ABCMeta):
    """
    PixArt Optical Sensor Emulator Module Mixin Class.
    """
    # update type hits
    ll_ctrl: PixArtOptEmuLowLevelControlMixin
    hl_ctrl: PixArtOptEmuHighLevelControlMixin
# end class PixArtOptEmuModuleMixin


class PixArt12BitsOptEmuModuleMixin(PixArtOptEmuModuleMixin, OptEmu12BitsModuleMixin, metaclass=ABCMeta):
    """
    PixArt 12-bits Optical Sensor Emulator Module Mixin Class.
    """
    # update type hits
    ll_ctrl: PixArt12BitsOptEmuLowLevelControlMixin
    hl_ctrl: PixArt12BitsOptEmuHighLevelControlMixin
# end class PixArt12BitsOptEmuModuleMixin


class PixArt16BitsOptEmuModuleMixin(PixArtOptEmuModuleMixin, OptEmu16BitsModuleMixin, metaclass=ABCMeta):
    """
    PixArt 16-bits Optical Sensor Emulator Module Mixin Class.
    """
    # update type hits
    ll_ctrl: PixArt16BitsOptEmuLowLevelControlMixin
    hl_ctrl: PixArt16BitsOptEmuHighLevelControlMixin
# end class PixArt16BitsOptEmuModuleMixin


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
