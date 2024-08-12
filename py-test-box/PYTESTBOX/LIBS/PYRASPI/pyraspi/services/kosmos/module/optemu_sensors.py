#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.optemu_sensors
:brief: Kosmos Optical Sensor Emulator Modules Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/05/17
"""
from pyraspi.services.kosmos.module.model.optemu.base import OptEmu12BitsRegisterMapBase
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.services.kosmos.module.model.optemu.em import Em12BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.em import Em16BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import Paw3266RegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArt12BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import PixArt16BitsRegisterMap
from pyraspi.services.kosmos.module.model.optemu.pixart import Pmw3816RegisterMap
from pyraspi.services.kosmos.module.optemu import OptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_12bits import OptEmu12BitsHighLevelControl
from pyraspi.services.kosmos.module.optemu_12bits import OptEmu12BitsLowLevelControl
from pyraspi.services.kosmos.module.optemu_16bits import OptEmu16BitsHighLevelControl
from pyraspi.services.kosmos.module.optemu_16bits import OptEmu16BitsLowLevelControl
from pyraspi.services.kosmos.module.optemu_em import Em12BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em12BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em12BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_em import Em16BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em16BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_em import Em16BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_pixart import Paw3266OptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import Paw3266OptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt12BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt12BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt12BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt16BitsOptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt16BitsOptEmuLowLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import PixArt16BitsOptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_pixart import Pmw3816OptEmuHighLevelControlMixin
from pyraspi.services.kosmos.module.optemu_pixart import Pmw3816OptEmuLowLevelControlMixin


# ------------------------------------------------------------------------------
# 12-bit Sensors implementation
# ------------------------------------------------------------------------------

class E7792Module(Em12BitsOptEmuModuleMixin):
    """
    Kosmos E7792 Pluto One Optical Sensor Emulator Module class.
    """

    def __init__(self, msg_id, instance_id=None, name=r'E7792'):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        super().__init__(msg_id=msg_id, instance_id=instance_id, name=name,
                         reg_map=Em12BitsRegisterMap,
                         ll_ctrl=Em12BitsOptEmuLowLevelControlMixin,
                         hl_ctrl=Em12BitsOptEmuHighLevelControlMixin)
    # end def __init__
# end class E7792Module


class Paw3266Module(PixArt12BitsOptEmuModuleMixin):
    """
    Kosmos PixArt PAW3266 TCOB Optical Sensor Emulator Module class.
    """
    # update type hits
    ll_ctrl: Paw3266OptEmuLowLevelControlMixin
    hl_ctrl: Paw3266OptEmuHighLevelControlMixin

    def __init__(self, msg_id, instance_id=None, name=r'PAW3266'):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        super().__init__(msg_id=msg_id, instance_id=instance_id, name=name,
                         reg_map=Paw3266RegisterMap,
                         ll_ctrl=Paw3266OptEmuLowLevelControlMixin,
                         hl_ctrl=Paw3266OptEmuHighLevelControlMixin)
    # end def __init__
# end class Paw3266Module


# ------------------------------------------------------------------------------
# 16-bit Sensors implementation
# ------------------------------------------------------------------------------

class E7788Module(Em16BitsOptEmuModuleMixin):
    """
    Kosmos E7788 HERO Optical Sensor Emulator Module class.
    """

    def __init__(self, msg_id, instance_id=None, name=r'E7788'):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        super().__init__(msg_id=msg_id, instance_id=instance_id, name=name,
                         reg_map=Em16BitsRegisterMap,
                         ll_ctrl=Em16BitsOptEmuLowLevelControlMixin,
                         hl_ctrl=Em16BitsOptEmuHighLevelControlMixin)
    # end def __init__
# end class E7788Module


class E7790Module(Em16BitsOptEmuModuleMixin):
    """
    Kosmos E7790 HERO2 Optical Sensor Emulator Module class.
    """

    def __init__(self, msg_id, instance_id=None, name=r'E7790'):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        super().__init__(msg_id=msg_id, instance_id=instance_id, name=name,
                         reg_map=Em16BitsRegisterMap,
                         ll_ctrl=Em16BitsOptEmuLowLevelControlMixin,
                         hl_ctrl=Em16BitsOptEmuHighLevelControlMixin)
    # end def __init__
# end class E7790Module


class Pmw3816Module(PixArt16BitsOptEmuModuleMixin):
    """
    Kosmos PMW3816 Tog6 Optical Sensor Emulator Module class.
    """
    # update type hits
    ll_ctrl: Pmw3816OptEmuLowLevelControlMixin
    hl_ctrl: Pmw3816OptEmuHighLevelControlMixin

    def __init__(self, msg_id, instance_id=None, name=r'PMW3816'):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        super().__init__(msg_id=msg_id, instance_id=instance_id, name=name,
                         reg_map=Pmw3816RegisterMap,
                         ll_ctrl=Pmw3816OptEmuLowLevelControlMixin,
                         hl_ctrl=Pmw3816OptEmuHighLevelControlMixin)
    # end def __init__
# end class Pmw3816Module


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
