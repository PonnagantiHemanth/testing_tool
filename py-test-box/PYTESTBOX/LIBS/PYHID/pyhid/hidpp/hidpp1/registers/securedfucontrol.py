#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.dfucontrol
    :brief: HID++ 1.0 DFU Control registers definition
    :author: Stanislas Cottard
    :date: 2020/09/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterResponse
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegisterRequest
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckBool
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SecureDfuControlModel(BaseRegisterModel):
    """
    Register DFU Control model
    """
    @classmethod
    def _get_data_model(cls):
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": SetDfuControlRequest,
                "response": SetDfuControlResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                "request": GetDfuControlRequest,
                "response": GetDfuControlResponse
            }
        }
    # end def _get_data_model
# end def SecureDfuControlModel


class SetDfuControlRequest(SetLongRegister):
    """
    Writing this register allows the SW to take an action on the DFU controls

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    ReservedDfuControl            7
    EnableDfu                     1
    Reserved                      24  # p1 (DFU Control param) + p2..p3 (Reserved)
    DfuMagicKey                   24
    Padding                       72
    ============================  ==========
    """

    class FID(SetLongRegister.FID):
        """
        Field Identifiers
        """
        RESERVED_DFU_CONTROL = SetLongRegister.FID.ADDRESS - 1
        ENABLE_DFU = RESERVED_DFU_CONTROL - 1
        RESERVED = ENABLE_DFU - 1
        DFU_MAGIC_KEY = RESERVED - 1
        PADDING = DFU_MAGIC_KEY - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        RESERVED_DFU_CONTROL = 0x07
        ENABLE_DFU = 0x01
        RESERVED = 0x18
        DFU_MAGIC_KEY = 0x18
        PADDING = 0x48
    # end class LEN

    class DEFAULT(SetLongRegister.DEFAULT):
        DFU_MAGIC_KEY = 0x505245  # ASCII code for 'PRE'
    # end class DEFAULT

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.RESERVED_DFU_CONTROL,
                 LEN.RESERVED_DFU_CONTROL,
                 title='ReservedDfuControl',
                 name='reserved_dfu_control',
                 aliases=('reserved_enable_dfu',),
                 checks=(CheckInt(min_value=0, max_value=0x7F),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.ENABLE_DFU,
                 LEN.ENABLE_DFU,
                 title='EnableDfu',
                 name='enable_dfu',
                 checks=(CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.DFU_MAGIC_KEY,
                 LEN.DFU_MAGIC_KEY,
                 title='DfuMagicKey',
                 name='dfu_magic_key',
                 checks=(CheckHexList(LEN.DFU_MAGIC_KEY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DFU_MAGIC_KEY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, enable_dfu=0, dfu_magic_key=DEFAULT.DFU_MAGIC_KEY):
        """
        Constructor

        :param enable_dfu: If not 0, the device will enter DFU mode on next restart
        :type enable_dfu: ``bool`` or ``int``
        :param dfu_magic_key: DFU Magic Key
        :type dfu_magic_key: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.DFU_CONTROL)

        self.enable_dfu = enable_dfu
        self.dfu_magic_key = dfu_magic_key
    # end def __init__
# end class SetDfuControlRequest


class SetDfuControlResponse(SetLongRegisterResponse):
    """
    Response to writing on the register DFU Control

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    Padding                       24
    ============================  ==========
    """
    ADDRESS = Hidpp1Data.Hidpp1RegisterAddress.DFU_CONTROL

    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.DFU_CONTROL)
    # end def __init__
# end class SetDfuControlResponse


class GetDfuControlRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get information about the DFU controls

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    Padding                       24
    ============================  ==========
    """

    class FID(GetLongRegisterRequest.FID):
        """
        Field Identifiers
        """
        PADDING = SetLongRegister.FID.ADDRESS - 1
    # end class FID

    class LEN(GetLongRegisterRequest.LEN):
        """
        Field Lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = GetLongRegisterRequest.FIELDS[:-3] + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.DFU_CONTROL)
    # end def __init__
# end class GetDfuControlRequest


class GetDfuControlResponse(GetLongRegister):
    """
    Response to reading the register DFU Control

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    ReservedDfuControl            7
    EnableDfu                     1
    Reserved                      8  # r0 (also named DFU Control Param)
    DfuControlTimeout             8
    DfuControlActionType          8
    Padding                       96  # r4..r6 (also named DFU Control Action Data) + 9 bytes long padding
    ============================  ==========
    """
    ADDRESS = Hidpp1Data.Hidpp1RegisterAddress.DFU_CONTROL

    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        RESERVED_DFU_CONTROL = GetLongRegister.FID.ADDRESS - 1
        ENABLE_DFU = RESERVED_DFU_CONTROL - 1
        RESERVED = ENABLE_DFU - 1
        DFU_CONTROL_TIMEOUT = RESERVED - 1
        DFU_CONTROL_ACTION_TYPE = DFU_CONTROL_TIMEOUT - 1
        PADDING = DFU_CONTROL_ACTION_TYPE - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        RESERVED_DFU_CONTROL = 0x07
        ENABLE_DFU = 0x01
        RESERVED = 0x08
        DFU_CONTROL_TIMEOUT = 0x08
        DFU_CONTROL_ACTION_TYPE = 0x08
        PADDING = 0x60
    # end class LEN

    class DEFAULT(GetLongRegister.DEFAULT):
        """
        Fields default values
        """
        DELAY_30_SECONDS = 0x1E
    # end class DEFAULT

    class STATE:
        """
        DFU state value in field EnableDfu
        """
        DFU_DISABLED = 0  # the device will not enter into DFU mode at next restart.
        DFU_ENABLED = 1  # the device will enter into DFU mode at next restart.
    # end

    class ACTION:
        """
        Control action to perform during the device reset in order to enter in bootloader at the next reset. Zero if
        unused.
        """
        NO_ACTION = 0  # No action required.
        OFF_ON = 1  # Receiver unplug/replug required.
        RESERVED = 4  # 4..255 - reserved
    # end class ACTION

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.RESERVED_DFU_CONTROL,
                 LEN.RESERVED_DFU_CONTROL,
                 title='ReservedDfuControl',
                 name='reserved_dfu_control',
                 aliases=('reserved_enable_dfu',),
                 checks=(CheckInt(min_value=0, max_value=0x7F),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.ENABLE_DFU,
                 LEN.ENABLE_DFU,
                 title='EnableDfu',
                 name='enable_dfu',
                 checks=(CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.DFU_CONTROL_TIMEOUT,
                 LEN.DFU_CONTROL_TIMEOUT,
                 title='DfuControlTimeout',
                 name='dfu_control_timeout',
                 checks=(CheckHexList(LEN.DFU_CONTROL_TIMEOUT // 8), CheckByte(),)),
        BitField(FID.DFU_CONTROL_ACTION_TYPE,
                 LEN.DFU_CONTROL_ACTION_TYPE,
                 title='DfuControlActionType',
                 name='dfu_control_action_type',
                 checks=(CheckHexList(LEN.DFU_CONTROL_ACTION_TYPE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, enable_dfu=0, dfu_control_timeout=DEFAULT.DELAY_30_SECONDS,
                 dfu_control_action_type=ACTION.OFF_ON):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.DFU_CONTROL)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.enable_dfu = enable_dfu
        self.dfu_control_timeout = dfu_control_timeout
        self.dfu_control_action_type = dfu_control_action_type
    # end def __init__
# end class GetDfuControlResponse

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
