#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.enterupgrademode
    :brief: HID++ 1.0 Enter OTA Firmware upgrade mode registers definition
    :author: Christophe Roquebert
    :date: 2020/03/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegisterRequest


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
ENTER_USB_UPGRADE_KEY = HexList('494350')  # ICP
APP_STATE_KEY = HexList('000000')


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class EnterUpgradeModeModel(BaseRegisterModel):
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
                "request": SetEnterUpgradeModeRequest,
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": GetEnterUpgradeModeRequest,
                "response": GetEnterUpgradeModeResponse
            }
        }
    # end def _get_data_model
# end class EnterUpgradeModeModel


class SetEnterUpgradeModeRequest(SetRegister):
    """
    Sending this command will put the device into OTA firmware upgrade mode
    """

    class FID(SetRegister.FID):
        """
        Field Identifiers
        """
        KEY = SetRegister.FID.ADDRESS - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Field Lengths in bits
        """
        KEY = 0x18
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.KEY,
                 LEN.KEY,
                 title='Key',
                 name='key',
                 checks=(CheckHexList(LEN.KEY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.KEY) - 1),),
                 default_value=0),
    )

    def __init__(self,
                 key=0):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.ENTER_FIRMWARE_UPGRADE_MODE)

        self.key = key
    # end def __init__
# end class SetEnterUpgradeModeRequest


class GetEnterUpgradeModeRequest(GetRegisterRequest):
    """
    Reading this register allows to get information about the connection state
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.ENTER_FIRMWARE_UPGRADE_MODE)
    # end def __init__
# end class GetEnterUpgradeModeRequest


class GetEnterUpgradeModeResponse(GetRegister):
    """
    Reading this register allows to get information about the connection state
    """
    class FID(SetRegister.FID):
        """
        Field Identifiers
        """
        KEY = SetRegister.FID.ADDRESS - 1

    # end class FID

    class LEN(SetRegister.LEN):
        """
        Field Lengths in bits
        """
        KEY = 0x18

    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.KEY,
                 LEN.KEY,
                 title='Key',
                 name='key',
                 checks=(CheckHexList(LEN.KEY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.KEY) - 1),),
                 default_value=0),
    )

    def __init__(self, key=0):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.ENTER_FIRMWARE_UPGRADE_MODE)

        self.key = key
    # end def __init__
# end class GetEnterUpgradeModeResponse

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
