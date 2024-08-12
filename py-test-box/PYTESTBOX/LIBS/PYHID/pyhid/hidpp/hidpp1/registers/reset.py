#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.reset
    :brief: HID++ 1.0 Reset registers definition
    :author: Martin Cryonnet
    :date: 2020/04/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum

from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import SetRegister


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class Reset:
    """
    Command Specific Constant
    """
    class FwInfoItem(IntEnum):
        WATCHDOG_TIMEOUT_RESET = 0x01
    # end class FwInfoItem
# end class Reset


class ResetModel(BaseRegisterModel):
    """
    Register Enter Upgrade Mode model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get register model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetResetRequest,
            }
        }
    # end def _get_data_model
# end class EnterUpgradeModeModel


class SetResetRequest(SetRegister):
    """
    Sending this command will reset the device
    """
    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        FW_INFO_ITEM = SetRegister.FID.ADDRESS - 1
        PADDING = FW_INFO_ITEM - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Fields Lengths in bits
        """
        FW_INFO_ITEM = 0x08
        PADDING = 0x10
    # end class LEN

    class DEFAULT(SetRegister.DEFAULT):
        """
        Fields default values
        """
        FW_INFO_ITEM = Reset.FwInfoItem.WATCHDOG_TIMEOUT_RESET

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.FW_INFO_ITEM,
                 LEN.FW_INFO_ITEM,
                 title='FwInfoItem',
                 name='fw_info_item',
                 default_value=DEFAULT.FW_INFO_ITEM,
                 checks=(CheckHexList(LEN.FW_INFO_ITEM // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FW_INFO_ITEM) - 1),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, device_index, fw_info_item=Reset.FwInfoItem.WATCHDOG_TIMEOUT_RESET):
        """
        Constructor
        """
        super().__init__(device_index=device_index, address=Hidpp1Data.Hidpp1RegisterAddress.RESET)
        self.fw_info_item = fw_info_item
    # end def __init__
# end class SetEnterUpgradeModeRequest

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
