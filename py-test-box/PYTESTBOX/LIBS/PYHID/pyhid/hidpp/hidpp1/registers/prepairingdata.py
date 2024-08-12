#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.setprepairingdata
    :brief: HID++ 1.0 Set Prepairing Data registers definition
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
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel, GetLongRegisterRequest, GetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterResponse
from pyhid.hidpp.hidppmessage import HidppMessage


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PrepairingData:
    """
    Command specific constants
    """
    class DataType(IntEnum):
        """
        Data Type values
        """
        LOCAL_ADDRESS = 0
        REMOTE_ADDRESS = 1
    # end class DataType
# end class PrepairingData


class PrepairingDataModel(BaseRegisterModel):
    """
    Register Prepairing Data model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": SetPrepairingDataRequest,
                "response": SetPrepairingDataResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                "request": GetPrepairingDataRequest,
                "response": GetPrepairingDataResponse
            },
        }
    # end def _get_data_model
# end class PrepairingDataModel


class SetPrepairingDataRequest(SetLongRegister):
    """
    Write Prepairing Data request
    """
    class FID(SetLongRegister.FID):
        """
        Fields Identifiers
        """
        DATA_TYPE = SetLongRegister.FID.ADDRESS - 1
        BLE_ADDRESS = DATA_TYPE - 1
        PADDING = BLE_ADDRESS - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        """
        Fields Lengths in bits
        """
        DATA_TYPE = 0x08
        BLE_ADDRESS = 0x30
        PADDING = 0x48
    # end class LEN

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.DATA_TYPE,
                 LEN.DATA_TYPE,
                 title='DataType',
                 name='data_type',
                 checks=(CheckHexList(LEN.DATA_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA_TYPE) - 1),)),
        BitField(FID.BLE_ADDRESS,
                 LEN.BLE_ADDRESS,
                 title='BleAddress',
                 name='ble_address',
                 aliases=('local_address', 'remote_address',),
                 checks=(CheckHexList(LEN.BLE_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BLE_ADDRESS) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SetLongRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, data_type, ble_address):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA)
        self.data_type = data_type
        self.ble_address = ble_address
        # end if
    # end def __init__
# end class SetPrepairingDataRequest


class SetPrepairingDataResponse(SetLongRegisterResponse):
    """
    Write Prepairing Data response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA)
    # end def __init__
# end class SetPrepairingDataResponse


class GetPrepairingDataRequest(GetLongRegisterRequest):
    """
    Read Prepairing Data request
    """
    def __init__(self, data_type):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA)
        self.get_field_from_name("r0").add_alias("data_type")
        self.data_type = data_type
    # end def __init__
# end class GetPrepairingDataRequest


class GetPrepairingDataResponse(GetLongRegister):
    """
    Read Prepairing Data response
    """
    class FID(SetLongRegister.FID):
        """
        Fields Identifiers
        """
        DATA_TYPE = GetLongRegister.FID.ADDRESS - 1
        BLE_ADDRESS = DATA_TYPE - 1
        PADDING = BLE_ADDRESS - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        """
        Fields Lengths in bits
        """
        DATA_TYPE = 0x08
        BLE_ADDRESS = 0x30
        PADDING = 0x48
    # end class LEN

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.DATA_TYPE,
                 LEN.DATA_TYPE,
                 title='DataType',
                 name='data_type',
                 checks=(CheckHexList(LEN.DATA_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA_TYPE) - 1),)),
        BitField(FID.BLE_ADDRESS,
                 LEN.BLE_ADDRESS,
                 title='BleAddress',
                 name='ble_address',
                 aliases=('local_address', 'remote_address',),
                 checks=(CheckHexList(LEN.BLE_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BLE_ADDRESS) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SetLongRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, data_type, ble_address):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA)
        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.data_type = data_type
        self.ble_address = ble_address
        # end if
    # end def __init__
# end class GetPrepairingDataResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
