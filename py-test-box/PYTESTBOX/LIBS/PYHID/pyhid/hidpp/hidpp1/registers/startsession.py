#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.hidpp1.registers.startsession
:brief: HID++ 1.0 Receiver ``StartSession`` register definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/11/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.bitfield import BitField
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
class StartSessionModel(BaseRegisterModel):
    """
    Register ``StartSession`` model
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
                "request": StartSessionRequest,
                "response": StartSessionResponse,
            }
        }
    # end def _get_data_model
# end class StartSessionModel


class StartSessionRequest(SetLongRegister):
    """
    Write ``StartSession`` request

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Account Name                  128
    ============================  ==========
    """

    class FID(SetLongRegister.FID):
        # See ``SetLongRegister.FID``
        ACCOUNT_NAME = SetLongRegister.FID.ADDRESS - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        # See ``SetLongRegister.LEN``
        ACCOUNT_NAME = 0x80
    # end class LEN

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.ACCOUNT_NAME,
                 LEN.ACCOUNT_NAME,
                 title='AccountName',
                 name='account_name',
                 checks=(CheckHexList(max_length=LEN.ACCOUNT_NAME // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACCOUNT_NAME) - 1),)),
    )

    def __init__(self, account_name):
        """
        :param account_name: Account Name expressed as UTF-8 string (except 0).
        :type account_name: ``str | HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.START_SESSION)
        account_name = HexList.fromString(account_name) if isinstance(account_name, str) else account_name
        account_name_copy = HexList(account_name.copy())
        account_name_copy.addPadding(self.LEN.ACCOUNT_NAME // 8, fromLeft=False)
        self.account_name = account_name_copy
    # end def __init__
# end class StartSessionRequest


class StartSessionResponse(SetRegister):
    """
    Write ``StartSession`` response

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      5
    Long Password                 1
    Full Authentication           1
    Constant Credentials          1
    Padding                       16
    ============================  ==========
    """
    SUB_ID = SetLongRegister.SUB_ID

    class FID(SetRegister.FID):
        # See ``SetRegister.FID``
        RESERVED = SetRegister.FID.ADDRESS - 1
        LONG_PASSWORD = RESERVED - 1
        FULL_AUTHENTICATION = LONG_PASSWORD - 1
        CONSTANT_CREDENTIALS = FULL_AUTHENTICATION - 1
        PADDING = CONSTANT_CREDENTIALS - 1
    # end class FID

    class LEN(SetRegister.LEN):
        # See ``SetRegister.LEN``
        RESERVED = 0x05
        LONG_PASSWORD = 0x01
        FULL_AUTHENTICATION = 0x01
        CONSTANT_CREDENTIALS = 0x01
        PADDING = 0x10
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 default_value=SetRegister.DEFAULT.RESERVED,
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
        BitField(FID.LONG_PASSWORD,
                 LEN.LONG_PASSWORD,
                 title='LongPassword',
                 name='long_password',
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.LONG_PASSWORD) - 1),)),
        BitField(FID.FULL_AUTHENTICATION,
                 LEN.FULL_AUTHENTICATION,
                 title='FullAuthentication',
                 name='full_authentication',
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FULL_AUTHENTICATION) - 1),)),
        BitField(FID.CONSTANT_CREDENTIALS,
                 LEN.CONSTANT_CREDENTIALS,
                 title='ConstantCredentials',
                 name='constant_credentials',
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.CONSTANT_CREDENTIALS) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=Hidpp1Message.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, constant_credentials=False, full_authentication=False, long_password=False):
        """
        :param constant_credentials: Flag enabling to change the credentials.
                                     False = The credentials may be modified - OPTIONAL
        :type constant_credentials: ``bool``
        :param full_authentication: Flag to switch from semi to full authentication.
                                    False = semi-authentication only - OPTIONAL
        :type full_authentication: ``bool``
        :param long_password: Flag to switch from 16 to 32 bytes long passwords.
                              False = Password are limited to 16 bytes - OPTIONAL
        :type long_password: ``bool``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.START_SESSION)
        self.constant_credentials = constant_credentials
        self.full_authentication = full_authentication
        self.long_password = long_password
    # end def __init__
# end class StartSessionResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
