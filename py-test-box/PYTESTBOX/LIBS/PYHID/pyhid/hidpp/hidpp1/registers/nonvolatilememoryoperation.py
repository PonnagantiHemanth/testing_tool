#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.hidpp1.registers.nonvolatilememoryoperation
:brief: HID++ 1.0 Non Volatile Memory Operation registers definition
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum
from enum import unique

from pyhid.bitfield import BitField
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class NonVolatileMemoryOperationModel(BaseRegisterModel):
    """
    Register Non-Volatile Memory Operation model
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
                "request": SetNonVolatileMemoryOperationRequest,
                "response": SetNonVolatileMemoryOperationResponse
            },
        }
    # end def _get_data_model
# end class NonVolatileMemoryOperationModel


class SetNonVolatileMemoryOperationRequest(SetRegister):
    """
    Write Non-Volatile Memory operation request
    """
    @unique
    class NvmOperation(IntEnum):
        """
        Data definition for Non-volatile memory operations
        """
        NO_OPERATION = 0
        ERASE_ALL_MEM = 1
        REVERT_AND_STAY = 2
        REVERT_AND_RELOAD = 3
        RELOAD = 4
        REVERT_OOB = 5
        ERASE_PAIRING_DATA = 6
        SAVE_PAIRING_INFO = 7
    # end class NvmOperation

    @unique
    class TargetSelection(IntEnum):
        """
        Data definition for target selections
        """
        EEPROM = 0
        RFID = 1
    # end class TargetSelection

    class FID(SetRegister.FID):
        # See ``SetRegister.FID``
        RESERVED = SetRegister.FID.ADDRESS - 1
        TARGET_SELECTION = RESERVED - 1
        NVM_OPERATION = TARGET_SELECTION - 1
        PADDING = NVM_OPERATION - 1
    # end class FID

    class LEN(SetRegister.LEN):
        # See ``SetRegister.LEN``
        RESERVED = 0x02
        TARGET_SELECTION = 0x02
        NVM_OPERATION = 0x04
        PADDING = 0x10
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 default_value=SetRegister.DEFAULT.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
        BitField(FID.TARGET_SELECTION,
                 LEN.TARGET_SELECTION,
                 title='TargetSelection',
                 name='target_selection',
                 checks=(CheckHexList(LEN.TARGET_SELECTION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TARGET_SELECTION) - 1),)),
        BitField(FID.NVM_OPERATION,
                 LEN.NVM_OPERATION,
                 title='NvmOperation',
                 name='nvm_operation',
                 checks=(CheckHexList(LEN.NVM_OPERATION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NVM_OPERATION) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SetRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, device_index, nvm_operation, target_selection):
        """
        :param device_index: Device index
        :type device_index: ``int``
        :param nvm_operation: Non-Volatile memory operation parameter value
        :type nvm_operation: ``int`` or ``HexList``
        :param target_selection: Target selection parameter value
        :type target_selection: ``int`` or ``HexList``
        """
        super().__init__(device_index=device_index,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_OPERATION)
        self.nvm_operation = nvm_operation
        self.target_selection = target_selection
    # end def __init__
# end class SetNonVolatileMemoryOperationRequest


class SetNonVolatileMemoryOperationResponse(SetRegisterResponse):
    """
    Write Non-Volatile Memory operation response
    """
    def __init__(self, device_index):
        """
        :param device_index: Device index
        :type device_index: ``int``
        """
        super().__init__(device_index=device_index,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_OPERATION)
    # end def __init__
# end class SetNonVolatileMemoryOperationResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
