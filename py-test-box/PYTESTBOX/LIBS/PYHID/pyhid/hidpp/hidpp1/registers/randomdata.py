#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.randomdata
    :brief: HID++ 1.0 Receiver Random Data register definition
    :author: Christophe Roquebert
    :date: 2020/11/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel, GetLongRegisterRequest, GetLongRegister
from pyhid.hidpp.hidppmessage import HidppMessage


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class RandomDataModel(BaseRegisterModel):
    """
    Register Receiver Random Data model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                "request": GetRandomDataRequest,
                "response": GetRandomDataResponse,
            }
        }
    # end def _get_data_model
# end class RandomDataModel

class GetRandomDataRequest(GetLongRegisterRequest):
    """
    Random Data request

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
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.RANDOM_DATA)
    # end def __init__
# end class GetRandomDataRequest


class GetRandomDataResponse(GetLongRegister):
    """
    Random Data response

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    RandomData                    128
    ============================  ==========
    """
    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        RANDOM_DATA = GetLongRegister.FID.ADDRESS - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        RANDOM_DATA = 0x80
    # end class LEN

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.RANDOM_DATA,
                 LEN.RANDOM_DATA,
                 title='RandomData',
                 name='random_data',
                 checks=(CheckHexList(LEN.RANDOM_DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RANDOM_DATA) - 1),)),
    )

    def __init__(self, random_data):
        """
        Constructor

        :param random_data: 16 bytes of data (r0..r15) returned by the receiver
        :type random_data: ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.RANDOM_DATA)
        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.random_data = random_data
    # end def __init__
# end class GetRandomDataResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
