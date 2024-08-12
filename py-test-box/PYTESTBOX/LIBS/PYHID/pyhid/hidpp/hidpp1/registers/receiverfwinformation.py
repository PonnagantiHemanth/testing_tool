#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.receiverfwinformation
    :brief: HID++ 1.0 Receiver FW Information registers definition
    :author: Martin Cryonnet
    :date: 2020/04/23
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
class ReceiverFwInfo:
    """
    Command specific constants
    """
    class EntityType(IntEnum):
        """
        Available entity types
        """
        MAIN_APP = 0
        BOOTLOADER = 1
        HARDWARE = 2
        SOFTDEVICE = 5
        RF_COMPANION = 6
        FACTORY_APP = 7
    # end class EntityType
# end class ReceiverFwInfo


class ReceiverFwInfoModel(BaseRegisterModel):
    """
    Register Receiver FW Information model
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
                "request": GetReceiverFwInfoRequest,
                "response": GetReceiverFwInfoResponse
            }
        }
    # end def _get_data_model
# end class ReceiverFwInfoModel


class GetReceiverFwInfoRequest(GetLongRegisterRequest):
    """
    Read Receiver FW Information request
    """
    def __init__(self, entity_idx):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.RECEIVER_FW_INFO)
        self.get_field_from_name("r0").add_alias("entity_idx")
        self.entity_idx = entity_idx
    # end def __init__
# end class GetReceiverFwInfoRequest


class GetReceiverFwInfoResponse(GetLongRegister):
    """
    Read Receiver FW Information response
    """
    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        ENTITY_TYPE = GetLongRegister.FID.ADDRESS - 1
        FW_NUMBER = ENTITY_TYPE - 1
        FW_REVISION = FW_NUMBER - 1
        FW_BUILD = FW_REVISION - 1
        EXTRA_VER = FW_BUILD - 1
        PADDING = EXTRA_VER - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        ENTITY_TYPE = 0x08
        FW_NUMBER = 0x08
        FW_REVISION = 0x08
        FW_BUILD = 0x10
        EXTRA_VER = 0x28
        PADDING = 0x30
    # end class LEN

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.ENTITY_TYPE,
                 LEN.ENTITY_TYPE,
                 title='EntityType',
                 name='entity_type',
                 checks=(CheckHexList(LEN.ENTITY_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ENTITY_TYPE) - 1),)),
        BitField(FID.FW_NUMBER,
                 LEN.FW_NUMBER,
                 title='FwNumber',
                 name='fw_number',
                 checks=(CheckHexList(LEN.FW_NUMBER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FW_NUMBER) - 1),)),
        BitField(FID.FW_REVISION,
                 LEN.FW_REVISION,
                 title='FwRevision',
                 name='fw_revision',
                 checks=(CheckHexList(LEN.FW_REVISION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FW_REVISION) - 1),)),
        BitField(FID.FW_BUILD,
                 LEN.FW_BUILD,
                 title='FwBuild',
                 name='fw_build',
                 checks=(CheckHexList(LEN.FW_BUILD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FW_BUILD) - 1),)),
        BitField(FID.EXTRA_VER,
                 LEN.EXTRA_VER,
                 title='ExtraVer',
                 name='extra_ver',
                 checks=(CheckHexList(LEN.EXTRA_VER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EXTRA_VER) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=GetLongRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, entity_type, fw_number, fw_revision, fw_build, extra_ver):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.RECEIVER_FW_INFO)
        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.entity_type = entity_type
        self.fw_number = fw_number
        self.fw_revision = fw_revision
        self.fw_build = fw_build
        self.extra_ver = extra_ver
    # end def __init__
# end class GetReceiverFwInfoResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
