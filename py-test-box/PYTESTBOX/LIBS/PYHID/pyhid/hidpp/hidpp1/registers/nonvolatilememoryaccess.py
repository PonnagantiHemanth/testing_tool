#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess
:brief: HID++ 1.0 Non Volatile Memory Acces registers definition
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/05/11
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
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class NonVolatileMemoryAccessModel(BaseRegisterModel):
    """
    Register Non-Volatile Memory Access model
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
                "request": GetNonVolatileMemoryAccessRequest,
                "response": GetNonVolatileMemoryAccessResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetNonVolatileMemoryAccessRequest,
                "response": SetNonVolatileMemoryAccessResponse
            },
        }
    # end def _get_data_model
# end class NonVolatileMemoryAccessModel


class GetNonVolatileMemoryAccessRequest(GetRegister):
    """
    Read Non-Volatile Memory Access request
    """
    class FID(SetRegister.FID):
        """
        Field Identifiers
        """
        NVM_ADDRESS_LSB = GetRegister.FID.ADDRESS - 1
        NVM_ADDRESS_MSB = NVM_ADDRESS_LSB - 1
        PADDING = NVM_ADDRESS_MSB - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        NVM_ADDRESS_LSB = 0x08
        NVM_ADDRESS_MSB = 0x08
        PADDING = 0x08
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.NVM_ADDRESS_LSB,
                 LEN.NVM_ADDRESS_LSB,
                 title='NvmAddressLSB',
                 name='nvm_address_lsb',
                 checks=(CheckHexList(LEN.NVM_ADDRESS_LSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NVM_ADDRESS_LSB) - 1),)),
        BitField(FID.NVM_ADDRESS_MSB,
                 LEN.NVM_ADDRESS_MSB,
                 title='NvmAddressMSB',
                 name='nvm_address_msb',
                 checks=(CheckHexList(LEN.NVM_ADDRESS_MSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NVM_ADDRESS_MSB) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=GetRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER, nvm_address_lsb=0x00, nvm_address_msb=0x00):
        """
        Constructor
        """
        super().__init__(device_index=device_index, address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS)
        self.nvm_address_lsb = nvm_address_lsb
        self.nvm_address_msb = nvm_address_msb
    # end def __init__
# end class GetNonVolatileMemoryAccessRequest


class GetNonVolatileMemoryAccessResponse(GetRegister):
    """
    Read Non-Volatile Memory Access response
    """
    class FID(GetRegister.FID):
        """
        Field Identifiers
        """
        NVM_ADDRESS_LSB = GetRegister.FID.ADDRESS - 1
        NVM_ADDRESS_MSB = NVM_ADDRESS_LSB - 1
        DATA = NVM_ADDRESS_MSB - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        NVM_ADDRESS_LSB = 0x08
        NVM_ADDRESS_MSB = 0x08
        DATA = 0x08
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.NVM_ADDRESS_LSB,
                 LEN.NVM_ADDRESS_LSB,
                 title='NvmAddressLSB',
                 name='nvm_address_lsb',
                 checks=(CheckHexList(LEN.NVM_ADDRESS_LSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NVM_ADDRESS_LSB) - 1),)),
        BitField(FID.NVM_ADDRESS_MSB,
                 LEN.NVM_ADDRESS_MSB,
                 title='NvmAddressMSB',
                 name='nvm_address_msb',
                 checks=(CheckHexList(LEN.NVM_ADDRESS_MSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NVM_ADDRESS_MSB) - 1),)),
        BitField(FID.DATA,
                 LEN.DATA,
                 title='Data',
                 name='data',
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )

    def __init__(self, device_index, nvm_address_lsb, nvm_address_msb, data):
        """
        Constructor
        """
        super().__init__(device_index=device_index, address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS)
        self.nvm_address_lsb = nvm_address_lsb
        self.nvm_address_msb = nvm_address_msb
        self.data = data
    # end def __init__
# end class GetNonVolatileMemoryAccessResponse


class SetNonVolatileMemoryAccessRequest(SetRegister):
    """
    Write Non-Volatile Memory Access response
    """
    class FID(SetRegister.FID):
        """
        Field Identifiers
        """
        NVM_ADDRESS_LSB = GetRegister.FID.ADDRESS - 1
        NVM_ADDRESS_MSB = NVM_ADDRESS_LSB - 1
        DATA = NVM_ADDRESS_MSB - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Field Lengths in bits
        """
        NVM_ADDRESS_LSB = 0x08
        NVM_ADDRESS_MSB = 0x08
        DATA = 0x08
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.NVM_ADDRESS_LSB,
                 LEN.NVM_ADDRESS_LSB,
                 title='NvmAddressLSB',
                 name='nvm_address_lsb',
                 checks=(CheckHexList(LEN.NVM_ADDRESS_LSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NVM_ADDRESS_LSB) - 1),)),
        BitField(FID.NVM_ADDRESS_MSB,
                 LEN.NVM_ADDRESS_MSB,
                 title='NvmAddressMSB',
                 name='nvm_address_msb',
                 checks=(CheckHexList(LEN.NVM_ADDRESS_MSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NVM_ADDRESS_MSB) - 1),)),
        BitField(FID.DATA,
                 LEN.DATA,
                 title='Data',
                 name='data',
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )

    def __init__(self, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER, nvm_address_lsb=0x00, nvm_address_msb=0x00,
                 data=0x00):
        """
        Constructor
        """
        super().__init__(device_index=device_index, address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS)
        self.nvm_address_lsb = nvm_address_lsb
        self.nvm_address_msb = nvm_address_msb
        self.data = data
    # end def __init__
# end class SetNonVolatileMemoryAccessRequest


class SetNonVolatileMemoryAccessResponse(SetRegisterResponse):
    """
    Write Non Volatile Memory Access response
    """
    def __init__(self, device_index):
        """
        Constructor
        """
        super().__init__(device_index=device_index, address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS)
    # end def __init__
# end class SetNonVolatileMemoryAccessResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
