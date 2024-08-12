#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.model.optemu.em
:brief: Kosmos Module EM (Electro-Marin) Family Optical Sensors Emulator Models Package
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/04/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from abc import ABCMeta
from enum import IntFlag
from enum import unique

from pyraspi.services.kosmos.module.model.optemu.base import OptEmu12BitsRegisterMapBase
from pyraspi.services.kosmos.module.model.optemu.base import OptEmu16BitsRegisterMapBase
from pyraspi.services.kosmos.module.model.optemu.base import OptEmuRegisterMapBase
from pyraspi.services.kosmos.module.model.registermap import BIT_0
from pyraspi.services.kosmos.module.model.registermap import BIT_1
from pyraspi.services.kosmos.module.model.registermap import BIT_2
from pyraspi.services.kosmos.module.model.registermap import BIT_3
from pyraspi.services.kosmos.module.model.registermap import BIT_4
from pyraspi.services.kosmos.module.model.registermap import BIT_5
from pyraspi.services.kosmos.module.model.registermap import BIT_6
from pyraspi.services.kosmos.module.model.registermap import BIT_7
from pyraspi.services.kosmos.module.model.registermap import Command
from pyraspi.services.kosmos.module.model.registermap import MaskedRegister
from pyraspi.services.kosmos.module.model.registermap import Register


# ------------------------------------------------------------------------------
# implementation
# -----------------------------------------------------------------------------
class EmRegisterMapBase(OptEmuRegisterMapBase, metaclass=ABCMeta):
    """
    Kosmos Optical Sensor Emulator Register Map, for Electro-Marin (EM) Optical Sensors family.

    Electro-Marin Optical Sensors Specifications:
     - E7792: https://drive.google.com/drive/folders/1C4XvZRduBTefP3EAXPhMwSf6deQRbLR6
     - E7788: https://drive.google.com/file/d/1dZ5uIkPv8uzB9cZ5PobKMzChTsj6yDhx
    """

    class Types(OptEmuRegisterMapBase.Types):
        """
        Register Types: bitfield Enums.
        """
        @unique
        class CONTROL(IntFlag):
            """
            Sensor Mode Control Register.
            """
            pass  # Control register definition is device-specific. Refer to derived classes.
        # end class CONTROL

        @unique
        class STATUS(IntFlag):
            """
            Sensor Status Register.
              * E7792 datasheet: Register List, page 11
            """
            UPDATE_ACK = BIT_0
            REST1 = BIT_1
            REST2 = BIT_2
            REST3 = REST1 | REST2
            STATUS3 = BIT_3
            STOPPED = BIT_4
            LIFT_DETECTED = BIT_5
            LOSS_OF_MATCHING = BIT_6
            MOTION = BIT_7
        # end class STATUS

        @unique
        class SERVREQ(IntFlag):
            """
            Service Request Register.
              * E7792 datasheet:
                - Register List, page 12
                - Usage, section 8.2.5
            """
            TUNE_OSC = BIT_0
            FLASH_RATE_UP = BIT_1
            FLASH_RATE_DOWN = BIT_2
            STOPPED = BIT_3
            LIFT_DETECTED = BIT_4
            LOSS_OF_MATCHING = BIT_5
            MOTION = BIT_6
            FLASH_DONE = BIT_7
        # end class SERVREQ

        @unique
        class LIFTSTAT(IntFlag):
            """
            Lift Detection Status Register.
              * E7792 datasheet: Register List, page 14
            """
            OPT_LIFT_RIGHT = BIT_0
            OPT_LIFT_CENTER = BIT_1
            NO_EDGE_LIFT = BIT_2
            STRONG_SLOPE_X = BIT_3
            WEAK_SLOPE_X = BIT_4
            SURF_CLASS = BIT_5
            TIMEOUT_LIFT = BIT_6
            SF_LIFT = BIT_7
        # end class LIFTSTAT
    # end class Types

    class Registers(OptEmuRegisterMapBase.Registers):
        """
        Register Address Map.
          * E7792 datasheet: Register List, section 7.1
        """
        CONTROL = 0x02
        STATUS = 0x04
        SERVREQ = 0x0B
        LIFTSTAT = 0x16
        LIFTMASK = 0x27
        REST_1_2_TIME = 0x22
        REST_S_TIME = 0x23
    # end class Registers

    class Commands(OptEmuRegisterMapBase.Commands):
        """
        Emulator-specific Command Index Map.
        This matches the FPGA implementation of the Optical Sensor Emulators.
        """
        CONTROL_SET = 0x02
        CONTROL_CLR = 0x12
        STATUS_SET = 0x04
        STATUS_CLR = 0x14
        SERVREQ_SET = 0x0B
        SERVREQ_CLR = 0x1B
        LIFTSTAT = 0x16
        LIFTMASK = 0x27
        REST_1_2_TIME = 0x22
        REST_S_TIME = 0x23
    # end class Commands

    def __init__(self):
        # Shorthand notations
        c = self.Commands
        r = self.Registers
        t = self.Types

        # Register Mapping: Register address to Register dataclass
        self.regs.update({
            r.CONTROL: MaskedRegister(addr=r.CONTROL, name='Control', type=t.CONTROL,
                                      desc='Sensor Operating Mode Control'),
            r.STATUS: MaskedRegister(addr=r.STATUS, name='Status', type=t.STATUS,
                                     desc='Sensor Status', resetval=t.STATUS.STOPPED),
            r.SERVREQ: MaskedRegister(addr=r.SERVREQ, name='ServReq', type=t.SERVREQ,
                                      desc='Service Request Selection'),
            r.LIFTSTAT: Register(addr=r.LIFTSTAT, name='LiftStat', type=t.LIFTSTAT,
                                 desc='Lift Detection Status'),
            r.LIFTMASK: Register(addr=r.LIFTMASK, name='LiftMask', type=t.LIFTSTAT,
                                 desc='Lift Detector Mask'),
            r.REST_1_2_TIME: Register(addr=r.REST_1_2_TIME, name='Rest1-2Time',
                                      desc='Rest1 to Rest2 transition time, by 480 ms increment'),
            r.REST_S_TIME: Register(addr=r.REST_S_TIME, name='Rest-STime',
                                    desc='Rest to Sleep transition time, by 4 sec increment'),
        })

        # Command Mapping: Command index to Command dataclass
        self.cmds.update({
            **OptEmuRegisterMapBase.cmds,
            c.CONTROL_SET: Command(idx=c.CONTROL_SET, name='Control_set', type=t.CONTROL,
                                   desc='Sensor Operating Mode Control: Force-Set Mask'),
            c.CONTROL_CLR: Command(idx=c.CONTROL_CLR, name='Control_clr', type=t.CONTROL,
                                   desc='Sensor Operating Mode Control: Force-Clear Mask'),
            c.STATUS_SET: Command(idx=c.STATUS_SET, name='Status_set', type=t.STATUS,
                                  desc='Sensor Status: Force-Set Mask'),
            c.STATUS_CLR: Command(idx=c.STATUS_CLR, name='Status_clr', type=t.STATUS,
                                  desc='Sensor Status: Force-Clear Mask'),
            c.SERVREQ_SET: Command(idx=c.SERVREQ_SET, name='ServReq_set', type=t.SERVREQ,
                                   desc='Service Request Selection: Force-Set Mask'),
            c.SERVREQ_CLR: Command(idx=c.SERVREQ_CLR, name='ServReq_clr', type=t.SERVREQ,
                                   desc='Service Request Selection: Force-Clear Mask'),
            c.LIFTSTAT: Command(idx=c.LIFTSTAT, name='LiftStat', type=t.LIFTSTAT,
                                desc='Lift Detection Status'),
            c.LIFTMASK: Command(idx=c.LIFTMASK, name='LiftMask', type=t.LIFTSTAT,
                                desc='Lift Detector Mask'),
            c.REST_1_2_TIME: Command(idx=c.REST_1_2_TIME, name='Rest1-2Time',
                                     desc='Rest1 to Rest2 transition time, by 480 ms increment'),
            c.REST_S_TIME: Command(idx=c.REST_S_TIME, name='Rest-STime',
                                   desc='Rest to Sleep transition time, by 4 sec increment'),
        })

        # Register to Command Mapping: Register address to Command index(es)
        self.reg2cmd.update({
            r.CONTROL: (c.CONTROL_SET, c.CONTROL_CLR),
            r.STATUS: (c.STATUS_SET, c.STATUS_CLR),
            r.SERVREQ: (c.SERVREQ_SET, c.SERVREQ_CLR),
            r.LIFTSTAT: c.LIFTSTAT,
            r.LIFTMASK: c.LIFTMASK,
            r.REST_1_2_TIME: c.REST_1_2_TIME,
            r.REST_S_TIME: c.REST_S_TIME,
        })

        # Command indexes that are affected by Compressed instruction data format
        self.cmp_cmd_idx.add(c.LIFTSTAT)

        super().__init__()
    # end def __init__
# end class EmRegisterMapBase


class Em12BitsRegisterMap(EmRegisterMapBase, OptEmu12BitsRegisterMapBase):
    """
    Kosmos Optical Sensor Emulator Register Map, for Electro-Marin (EM) 12-bit Optical Sensors family.

    Electro-Marin Optical Sensor Specifications:
     - E7792: https://drive.google.com/drive/folders/1C4XvZRduBTefP3EAXPhMwSf6deQRbLR6
    """

    class Types(EmRegisterMapBase.Types):
        # See ``EmRegisterMapBase.Types``
        @unique
        class CONTROL(IntFlag):
            """
            Sensor Mode Control Register.
              * E7792 datasheet:
                - Register List, page 10
                - Usage, section 8.2
            """
            FORCE_SLEEP = BIT_3
            FORCE_REST2 = BIT_4
            FORCE_REST_BITS = FORCE_SLEEP | FORCE_REST2
            FLASH_CONTINUOUSLY = BIT_7
        # end class CONTROL
    # end class Types

    class Registers(EmRegisterMapBase.Registers, OptEmu12BitsRegisterMapBase.Registers):
        # See ``EmRegisterMap.Registers`` and ``OptEmu12BitsRegisterMapBase.Registers``
        DELTA_X_L = 0x05
        DELTA_Y_L = 0x06
        DELTA_XY_H = 0x07
    # end class Registers

    class Commands(EmRegisterMapBase.Commands, OptEmu12BitsRegisterMapBase.Commands):
        # See ``EmRegisterMap.Commands`` and ``OptEmu12BitsRegisterMapBase.Commands``
        DELTA_X_L = 0x05
        DELTA_Y_L = 0x06
        DELTA_XY_H = 0x07
    # end class Commands
# end class Em12BitsRegisterMap


class Em16BitsRegisterMap(EmRegisterMapBase, OptEmu16BitsRegisterMapBase):
    """
    Kosmos Optical Sensor Emulator Register Map, for Electro-Marin (EM) 16-bit Optical Sensors family.

    Electro-Marin Optical Sensor Specifications:
     - E7788: https://drive.google.com/file/d/1dZ5uIkPv8uzB9cZ5PobKMzChTsj6yDhx
    """

    class Types(EmRegisterMapBase.Types):
        # See ``EmRegisterMapBase.Types``
        @unique
        class CONTROL(IntFlag):
            """
            Sensor Mode Control Register.
              * E7788 datasheet:
                - Register List, page 7
                - Usage, section 8.1
            """
            FLASH_CONTINUOUSLY = BIT_7
        # end class CONTROL

        @unique
        class CONTROL2(IntFlag):
            """
            Sensor Mode Control2 Register.
              * E7788 datasheet:
                - Register List, page 7
                - Usage, section 8.1
            """
            HIGH_RESOLUTION = BIT_2
            FORCE_SLEEP = BIT_3
            FORCE_REST2 = BIT_4
            FORCE_REST_BITS = FORCE_SLEEP | FORCE_REST2
            SPURIOUS_CANCELATION_REST1 = BIT_5
            POWER_SAVING = BIT_6
            CORDED_GAMING = BIT_7
        # end class CONTROL2
    # end class Types

    class Registers(EmRegisterMapBase.Registers, OptEmu16BitsRegisterMapBase.Registers):
        # See ``EmRegisterMapBase.Registers`` and ``OptEmu16BitsRegisterMapBase.Registers``
        CONTROL2 = 0x03
        DELTA_X_H = 0x05
        DELTA_X_L = 0x06
        DELTA_Y_H = 0x07
        DELTA_Y_L = 0x08
    # end class Registers

    class Commands(EmRegisterMapBase.Commands, OptEmu16BitsRegisterMapBase.Commands):
        # See ``EmRegisterMapBase.Commands`` and ``OptEmu16BitsRegisterMapBase.Commands``
        CONTROL2_SET = 0x03
        CONTROL2_CLR = 0x13
        DELTA_X_H = 0x05
        DELTA_X_L = 0x06
        DELTA_Y_H = 0x07
        DELTA_Y_L = 0x08
    # end class Commands

    def __init__(self):
        # Shorthand notations
        c = self.Commands
        r = self.Registers
        t = self.Types

        # Register Mapping: Register address to Register dataclass
        self.regs.update({
            r.CONTROL2: MaskedRegister(addr=r.CONTROL2, name='Control2',
                                       type=t.CONTROL2,
                                       desc='Sensor Operating Mode Control2')
        })

        # Command Mapping: Command index to Command dataclass
        self.cmds.update({
            c.CONTROL2_SET: Command(idx=c.CONTROL2_SET, name='Control2_set',
                                    type=t.CONTROL2,
                                    desc='Sensor Operating Mode Control2: Force-Set Mask'),
            c.CONTROL2_CLR: Command(idx=c.CONTROL2_CLR, name='Control2_clr',
                                    type=t.CONTROL2,
                                    desc='Sensor Operating Mode Control2: Force-Clear Mask')
        })

        # Register to Command Mapping: Register address to Command index(es)
        self.reg2cmd.update({
            self.Registers.CONTROL2: (c.CONTROL2_SET, c.CONTROL2_CLR)
        })

        super().__init__()
    # end def __init__
# end class Em16BitsRegisterMap


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
