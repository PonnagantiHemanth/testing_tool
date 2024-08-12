#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.uniqueidentifier
    :brief: HID++ 1.0 Receiver Unique Identifier register definition
    :author: Christophe Roquebert
    :date: 2020/12/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegister
from pyhid.hidpp.hidppmessage import HidppMessage


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class UniqueIdentifierModel(BaseRegisterModel):
    """
    Register Receiver Unique Identifier model
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
                "request": GetUniqueIdentifierRequest,
                "response": GetUniqueIdentifierResponse,
            }
        }
    # end def _get_data_model
# end class UniqueIdentifierModel


class GetUniqueIdentifierRequest(GetLongRegisterRequest):
    """
    Unique Identifier request

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
                         address=Hidpp1Data.Hidpp1RegisterAddress.UNIQUE_IDENTIFIER)
    # end def __init__
# end class GetUniqueIdentifierRequest


class GetUniqueIdentifierResponse(GetLongRegister):
    """
    Unique Identifier response

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    UniqueIdentifier              128
    ============================  ==========
    """
    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        UNIQUE_IDENTIFIER = GetLongRegister.FID.ADDRESS - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        UNIQUE_IDENTIFIER = 0x80
    # end class LEN

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.UNIQUE_IDENTIFIER,
                 LEN.UNIQUE_IDENTIFIER,
                 title='UniqueIdentifier',
                 name='unique_identifier',
                 checks=(CheckHexList(LEN.UNIQUE_IDENTIFIER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.UNIQUE_IDENTIFIER) - 1),)),
    )

    def __init__(self, unique_identifier):
        """
        Constructor

        :param unique_identifier: 16 bytes long unique identifier r0..r15 (Terminated by 0x00 if shorter than 16 bytes)
        :type unique_identifier: ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.UNIQUE_IDENTIFIER)
        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.unique_identifier = unique_identifier
    # end def __init__
# end class GetUniqueIdentifierResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
