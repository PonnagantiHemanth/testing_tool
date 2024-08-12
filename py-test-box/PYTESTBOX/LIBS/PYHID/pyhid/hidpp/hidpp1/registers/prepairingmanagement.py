#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.prepairingmanagement
    :brief: HID++ 1.0 Prepairing Data Management registers definition
    :author: Martin Cryonnet
    :date: 2020/05/12
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
from pyhid.hidpp.hidpp1.setgetregister import SetRegister, SetRegisterResponse


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PrepairingManagement:
    """
    Command specific constants
    """
    class PrepairingManagementControl(IntEnum):
        """
        Pairing Mode bit 0 values
        """
        START = 0
        STORE = 1
        DELETE = 2
    # end class PrepairingManagementControl
# end class PrepairingDataManagement


class PrepairingManagementModel(BaseRegisterModel):
    """
    Register Prepairing Management model
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
                "request": SetPrepairingManagementRequest,
                "response": SetPrepairingManagementResponse
            },
        }
    # end def _get_data_model
# end class PrepairingManagementModel


class SetPrepairingManagementRequest(SetRegister):
    """
    Write Prepairing Management request
    """

    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        PAIRING_SLOT = SetRegister.FID.ADDRESS - 1
        PREPAIRING_MANAGEMENT_CONTROL = PAIRING_SLOT - 1
        PADDING = PREPAIRING_MANAGEMENT_CONTROL - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Fields Lengths in bits
        """
        PAIRING_SLOT = 0x08
        PREPAIRING_MANAGEMENT_CONTROL = 0x08
        PADDING = 0x08
    # end class LEN

    class DEFAULT(SetRegister.DEFAULT):
        """
        Fields default values
        """
        PREPAIRING_MANAGEMENT_CONTROL = PrepairingManagement.PrepairingManagementControl.START
    # end class DEFAULT

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.PAIRING_SLOT,
                 LEN.PAIRING_SLOT,
                 title='PairingSlot',
                 name='pairing_slot',
                 aliases=('index',),
                 checks=(CheckHexList(LEN.PAIRING_SLOT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PAIRING_SLOT) - 1),)),
        BitField(FID.PREPAIRING_MANAGEMENT_CONTROL,
                 LEN.PREPAIRING_MANAGEMENT_CONTROL,
                 title='PrepairingManagementControl',
                 name='prepairing_management_control',
                 default_value=DEFAULT.PREPAIRING_MANAGEMENT_CONTROL,
                 checks=(CheckHexList(LEN.PREPAIRING_MANAGEMENT_CONTROL // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PREPAIRING_MANAGEMENT_CONTROL) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='Padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, pairing_slot, prepairing_management_control):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT)
        self.pairing_slot = pairing_slot
        self.prepairing_management_control = prepairing_management_control
    # end def __init__
# end class SetPrepairingManagementRequest


class SetPrepairingManagementResponse(SetRegisterResponse):
    """
    Write Prepairing Management response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT)
    # end def __init__
# end class SetPrepairingManagementResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
