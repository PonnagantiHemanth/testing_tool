#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.rfregisteraccess
    :brief: HID++ 1.0 Receiver RF Register Access registers definition
    :author: Martin Cryonnet
    :date: 2020/05/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel, SetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegister, GetRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterRequest, SetRegisterResponse


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class RFRegisterAccess:
    """
    Command specific constants
    """
    class RFPageRegister(IntEnum):
        """
        RF Page Register values
        """
        PAGE_0 = 0x00
        QUAD_AND_EQUAD_RF_PAGE_0 = PAGE_0
        SIMPLIFIED_QUAD_RF_PAGE_1 = 0x01
        GENERIC_RF_REGISTER_ACCESS = 0x02
    # end class RFPageRegister

    class Page0AddrReg(IntEnum):
        """
        Page 0, Parameter 1 / Address Register values
        """
        TEST_MODE_ENABLE_DISABLE = 0x00
        RF_CHANNEL = 0x01
        RF_TX_POWER = 0x02
        RF_CHANNEL_INDEX = 0x03
        RF_FREQUENCY_TUNING = 0x04
        RF_FREQUENCY_MODULATION = 0x05
    # end class Page0AddrReg

    class TestModeEnableDisable(IntEnum):
        """
        Test Mode Enable/Disable values
        """
        RF_OFF = 0x00
        CONTINUOUS_WAVE_MODE_ENABLED = 0x01
        CONTINUOUS_RX_MODE_ENABLED = 0x02
        RETURN_TO_NORMAL_RECEIVER_MODE = 0x03
    # end class TestModeEnableDisable

    class RFChannel(IntEnum):
        """
        RF Channel values
        """
        F_2400_MHZ = 0x00
        F_2401_MHZ = 0x01
        F_2402_MHZ = 0x02
        # etc.
        # transceiver hops every 1s from 2481 to 2401 MHz in 5MHz steps, looping forever
        HOP_5MHZ_EVERY_1S = 0xFF
    # end class RFChannel

    class RFTXPower:
        """
        RF TX Power values
        """
        class NRF24xxxFamily(IntEnum):
            """
            For nRF24xxx family
            """
            NRF2401A_MINUS_20_DBM = 0x00
            NRF24L01_MINUS_18_DBM = 0x00
            NRF2401A_MINUS_10_DBM = 0x01
            NRF24L01_MINUS_12_DBM = 0x01
            NRF2401A_MINUS_5_DBM = 0x02
            NRF24L01_MINUS_6_DBM = 0x02
            NRF2401A_0_DBM = 0x03
            NRF24L01_0_DBM = 0x03
        # end class NRF24xxxFamily

        class TICC254xFamily(IntEnum):
            """
            For TI:CC254x family
            """
            PLUS_4_DBM = 0x0F
            PLUS_3_DBM = 0x0E
            # ...
            MINUS_11_DBM = 0x00
        # end class TICC254xFamily

        class NRF52xxxFamily(IntEnum):
            """
            For nRF52xxx family
            """
            PLUS_8_DBM = 0x08
            PLUS_7_DBM = 0x07
            PLUS_6_DBM = 0x06
            PLUS_5_DBM = 0x05
            PLUS_4_DBM = 0x04
            PLUS_3_DBM = 0x03
            PLUS_2_DBM = 0x02
            PLUS_0_DBM = 0x00
            MINUS_4_DBM = 0xFC
            MINUS_8_DBM = 0xF8
            MINUS_12_DBM = 0xF4
            MINUS_16_DBM = 0xF0
            MINUS_20_DBM = 0xEC
            MINUS_40_DBM = 0xD8
        # end class NRF52xxxFamily
    # end class RFTXPower

    class RFChannelIndex(IntEnum):
        """
        RF Channel Index values
        """
        MIN = 1
        MAX = 24
    # end class RFChannelIndex

    class RFFrequencyModulation(IntEnum):
        """
        RF Frequency modulation values
        """
        F_320_KHZ = 0x00
        F_500_KHZ = 0x01
        F_250_KHZ = 0x02
        F_160_KHZ = 0x03
    # end class RFFrequencyModulation
# end class RFRegisterAccess


class RFRegisterAccessModel(BaseRegisterModel):
    """
    Register RF Register Access model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetRFRegisterAccessRequest,
                "response": SetRFRegisterAccessResponse
            },
        }
    # end def _get_data_model
# end class RFRegisterAccessModel


class SetRFRegisterAccessRequest(SetRegister):
    """
    Write RF Register Access request
    """
    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        RF_PAGE_REGISTER = SetRegister.FID.ADDRESS - 1
        ADDRESS_REGISTER = RF_PAGE_REGISTER - 1
        DATA = ADDRESS_REGISTER - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Fields Lengths in bits
        """
        RF_PAGE_REGISTER = 0x08
        ADDRESS_REGISTER = 0x08
        DATA = 0x08
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.RF_PAGE_REGISTER,
                 LEN.RF_PAGE_REGISTER,
                 title='RFPageRegister',
                 name='rf_page_register',
                 checks=(CheckHexList(LEN.RF_PAGE_REGISTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RF_PAGE_REGISTER) - 1),)),
        BitField(FID.ADDRESS_REGISTER,
                 LEN.ADDRESS_REGISTER,
                 title='AddressRegister',
                 name='address_register',
                 checks=(CheckHexList(LEN.ADDRESS_REGISTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ADDRESS_REGISTER) - 1),)),
        BitField(FID.DATA,
                 LEN.DATA,
                 title='Data',
                 name='data',
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )

    def __init__(self, rf_page_register, address_register, data):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS)
        self.rf_page_register = rf_page_register
        self.address_register = address_register
        self.data = data
    # end def __init__
# end class SetRFRegisterAccessRequest


class SetRFRegisterAccessResponse(SetRegisterResponse):
    """
    Write RF Register Access response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS)
    # end def __init__
# end class SetRFRegisterAccessResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
