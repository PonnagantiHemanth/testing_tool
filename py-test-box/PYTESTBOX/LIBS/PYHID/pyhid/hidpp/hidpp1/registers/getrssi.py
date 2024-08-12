#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyhid.hidpp.hidpp1.registers.getrssi
:brief: HID++ 1.0 Get RSSI register definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/02/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import GetRegister


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class GetRssiModel(BaseRegisterModel):
    """
    Register Get RSSI model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": GetRssiRequest,
                "response": GetRssiResponse
            },
        }
    # end def _get_data_model
# end class GetRssiModel


class GetRssiRequest(GetRegister):
    """
    Read Get RSSI request
    """
    class FID(GetRegister.FID):
        """
        Field Identifiers
        """
        INDEX = GetRegister.FID.ADDRESS - 1
        PADDING = INDEX - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.INDEX,
                 LEN.INDEX,
                 title='Index',
                 name='index',
                 checks=(CheckHexList(LEN.INDEX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.INDEX) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=GetRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER, index=0x00):
        """
        Constructor
        """
        super().__init__(device_index=device_index, address=Hidpp1Data.Hidpp1RegisterAddress.GET_RSSI)
        self.index = index
    # end def __init__
# end class GetRssiRequest


class GetRssiResponse(GetRegister):
    """
    Read Get Rssi response
    """
    class FID(GetRegister.FID):
        """
        Field Identifiers
        """
        INDEX = GetRegister.FID.ADDRESS - 1
        DEVICE_TYPE = INDEX - 1
        SIGNAL_STRENGTH = DEVICE_TYPE - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        INDEX = 0x08
        DEVICE_TYPE = 0x08
        SIGNAL_STRENGTH = 0x08
    # end class LEN

    class STRENGTH:
        """
        Received signal strength indication in dBm
        """
        TI_CC2544_MIN = 0
        TI_CC2544_MAX = 64
        NRF52_MIN = -90
        NRF52_MAX = 8
    # end class STRENGTH

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.INDEX,
                 LEN.INDEX,
                 title='Index',
                 name='index',
                 checks=(CheckHexList(LEN.INDEX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.INDEX) - 1),)),
        BitField(FID.DEVICE_TYPE,
                 LEN.DEVICE_TYPE,
                 title='Device Type',
                 name='device_type',
                 checks=(CheckHexList(LEN.DEVICE_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_TYPE) - 1),)),
        BitField(FID.SIGNAL_STRENGTH,
                 LEN.SIGNAL_STRENGTH,
                 title='Received Signal Strength',
                 name='signal_strength',
                 checks=(CheckHexList(LEN.SIGNAL_STRENGTH // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SIGNAL_STRENGTH) - 1),)),
    )

    def __init__(self, index, device_type, signal_strength):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER, address=Hidpp1Data.Hidpp1RegisterAddress.GET_RSSI)
        self.index = index
        self.device_type = device_type
        self.signal_strength = signal_strength
    # end def __init__
# end class GetRssiResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
