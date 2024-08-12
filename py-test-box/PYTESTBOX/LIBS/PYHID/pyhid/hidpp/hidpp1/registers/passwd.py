#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.hidpp1.registers.passwd
:brief: HID++ 1.0 Receiver ``Password`` register definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/11/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PasswordModel(BaseRegisterModel):
    """
    Register ``Password`` model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get data model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": PasswordRequest,
                "response": PasswordResponse
            },
        }
    # end def _get_data_model
# end class PasswordModel


class PasswordRequest(SetLongRegister):
    """
    Write ``Password`` request

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Password                      128
    ============================  ==========
    """

    class FID(SetLongRegister.FID):
        # See ``SetLongRegister.FID``
        PASSWORD = SetLongRegister.FID.ADDRESS - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        # See ``SetLongRegister.LEN``
        PASSWORD = 0x80
    # end class LEN

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.PASSWORD,
                 LEN.PASSWORD,
                 title='Password',
                 name='password',
                 checks=(CheckHexList(max_length=LEN.PASSWORD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PASSWORD) - 1),)),
    )

    def __init__(self, password):
        """
        :param password: Password value (LSB first)
        :type password: ``str | HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PASSWORD)
        self.password = password
    # end def __init__
# end class PasswordRequest


class PasswordResponse(SetRegister):
    """
    Write ``Password`` response

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Status                        8
    Padding                       16
    ============================  ==========
    """
    SUB_ID = SetLongRegister.SUB_ID

    class FID(SetRegister.FID):
        # See ``SetRegister.FID``
        STATUS = SetRegister.FID.ADDRESS - 1
        PADDING = STATUS - 1
    # end class FID

    class LEN(SetRegister.LEN):
        # See ``SetRegister.LEN``
        STATUS = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.STATUS,
                 LEN.STATUS,
                 title='Status',
                 name='status',
                 checks=(CheckHexList(LEN.STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.STATUS) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, status):
        """
        :param status: password processing status
        :type status: ``int``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PASSWORD)
        self.status = status
    # end def __init__
# end class PasswordResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
