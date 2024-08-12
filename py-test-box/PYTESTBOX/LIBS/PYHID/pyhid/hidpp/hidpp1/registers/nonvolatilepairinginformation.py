#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation
:brief: HID++ 1.0 Non-volatile and pairing information registers definition
:author: Christophe Roquebert
:date: 2020/02/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import Register
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterResponse
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class NonVolatilePairingInformation:
    class R0(IntEnum):
        """
        Non-Volatile and Pairing Information R0 available values
        """
        USB_SERIAL_NUMBER = 0x01
        FW_VERSION = 0x02
        TRANSCEIVER_EQUAD_INFORMATION = 0x03
        EQUAD_STEP4_DEVICE_PAIRING_INFO_MIN = 0x20
        EQUAD_STEP4_DEVICE_PAIRING_INFO_MAX = 0x25
        EQUAD_STEP4_DEVICE_EXT_PAIRING_INFO_MIN = 0x30
        EQUAD_STEP4_DEVICE_EXT_PAIRING_INFO_MAX = 0x35
        EQUAD_STEP4_DEVICE_NAME_MIN = 0x40
        EQUAD_STEP4_DEVICE_NAME_MAX = 0x45
        BLE_PRO_DEVICE_PAIRING_INFO_MIN = 0x51
        BLE_PRO_DEVICE_PAIRING_INFO_MAX = 0x5F
        BLE_PRO_DEVICE_DEVICE_NAME_MIN = 0x61
        BLE_PRO_DEVICE_DEVICE_NAME_MAX = 0x6F
        EQUAD_STEP4_AES_ENCRYPTION_KEY_MIN = 0xF0
        EQUAD_STEP4_AES_ENCRYPTION_KEY_MAX = 0xF5
    # end class R0

    class LinkStatus(IntEnum):
        """
        BLE Pro device pairing information - Device info - Link status values
        """
        LINK_ESTABLISHED = 0x00
        LINK_NOT_ESTABLISHED = 0x01
    # end class LinkStatus

    class BleProDeviceNamePart(IntEnum):
        """
        BLE Pro device - Device Name : Device name part values
        """
        PART_1 = 0x01
        PART_2 = 0x02
        PART_3 = 0x03
    # end class BleProDeviceNamePart

    class DeviceState(IntEnum):
        """
        BLE Pro device pairing information - Device State values
        """
        BOOTLOADER_RECOVERY = 0x00
        APPLICATION_BOOTLOADER_RECONNECTION = 0x01
    # end class DeviceState
# end class NonVolatilePairingInformation


class NonVolatilePairingInformationModel(BaseRegisterModel):
    """
    Register Non Volatile Pairing Information model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            "r0": {
                NonVolatilePairingInformation.R0.USB_SERIAL_NUMBER: {
                    Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                        "request": GetUsbSerialNumberRequest,
                        "response": GetUsbSerialNumberResponse
                    }
                },
                NonVolatilePairingInformation.R0.FW_VERSION: {
                    Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                        "request": GetFwVersionRequest,
                        "response": GetFwVersionResponse
                    }
                },
                NonVolatilePairingInformation.R0.TRANSCEIVER_EQUAD_INFORMATION: {
                    Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                        "request": GetTransceiverEQuadInformation,
                        "response": GetTransceiverEQuadInformationResponse
                    },
                    Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                        "request": SetTransceiverEQuadInformationRequest,
                        "response": SetTransceiverEQuadInformationResponse
                    }
                },
                **{
                    r0: {
                        Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                            "request": GetEQuadDevicePairingInfoRequest,
                            "response": GetEQuadDevicePairingInfoResponse
                        },
                        Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                            "request": SetEQuadDevicePairingInformationRequest,
                            "response": SetEQuadDevicePairingInformationResponse
                        }
                    } for r0 in range(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_PAIRING_INFO_MIN,
                                      NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_PAIRING_INFO_MAX + 1)
                },
                **{
                    r0: {
                        Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                            "request": GetEQuadDeviceExtendedPairingInfoRequest,
                            "response": GetEQuadDeviceExtendedPairingInfoResponse
                        },
                        Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                            "request": SetEQuadDeviceExtendedPairingInfoRequest,
                            "response": SetEQuadDeviceExtendedPairingInfoResponse
                        }
                    } for r0 in range(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_EXT_PAIRING_INFO_MIN,
                                      NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_EXT_PAIRING_INFO_MAX + 1)
                },
                **{
                    r0: {
                        Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                            "request": GetEQuadDeviceNameRequest,
                            "response": GetEQuadDeviceNameResponse
                        },
                        Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                            "request": SetEQuadDeviceNameRequest,
                            "response": SetEQuadDeviceNameResponse
                        }
                    } for r0 in range(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN,
                                      NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MAX + 1)
                },
                **{
                    r0: {
                        Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                            "request": GetBLEProDevicePairingInfoRequest,
                            "response": GetBLEProDevicePairingInfoResponse
                        }
                    } for r0 in range(NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN,
                                      NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MAX + 1)
                },
                **{
                    r0: {
                        Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                            "request": GetBLEProDeviceDeviceNameRequest,
                            "response": GetBLEProDeviceDeviceNameResponse
                        }
                    } for r0 in range(NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN,
                                      NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MAX + 1)
                },
                **{
                    r0: {
                        Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                            "request": SetAesEncryptionKeyRequest,
                            "response": SetAesEncryptionKeyResponse
                        }
                    } for r0 in range(NonVolatilePairingInformation.R0.EQUAD_STEP4_AES_ENCRYPTION_KEY_MIN,
                                      NonVolatilePairingInformation.R0.EQUAD_STEP4_AES_ENCRYPTION_KEY_MAX + 1)
                },
            }
        }
    # end def _get_data_model
# end class NonVolatilePairingInformationModel


class GetUsbSerialNumberRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get the USB serial Number
    """
    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=NonVolatilePairingInformation.R0.USB_SERIAL_NUMBER)
    # end def __init__
# end class GetUsbSerialNumberRequest


class GetUsbSerialNumberResponse(GetLongRegister):
    """
    Reading this register allows to get the USB serial Number
    """
    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        R0 = GetLongRegister.FID.ADDRESS - 1
        SERIAL_NUMBER = R0 - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        R0 = 0x08
        SERIAL_NUMBER = 0x78
    # end class LEN

    class OFFSET(GetLongRegister.OFFSET):
        """
        Fields offset in bytes
        """
        R0 = GetLongRegister.OFFSET.ADDRESS + 0x01
    # end class OFFSET

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.SERIAL_NUMBER,
                 LEN.SERIAL_NUMBER,
                 title='SerialNumber',
                 name='serial_number',
                 checks=(CheckHexList(LEN.SERIAL_NUMBER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SERIAL_NUMBER) - 1),)),
    )

    def __init__(self, serial_number=0):
        """
        :param serial_number: Serial number parameter value
        :type serial_number: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)
        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = NonVolatilePairingInformation.R0.USB_SERIAL_NUMBER
        self.serial_number = serial_number
    # end def __init__
# end class GetUsbSerialNumberResponse


class GetFwVersionRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get FW version
    """
    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=NonVolatilePairingInformation.R0.FW_VERSION)
    # end def __init__
# end class GetFwVersionRequest


class GetFwVersionResponse(GetLongRegister):
    """
    Reading this register allows to get FW version
    """
    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        R0 = GetLongRegister.FID.ADDRESS - 1
        FW_NAME = R0 - 1
        FW_VERSION = FW_NAME - 1
        FW_BUILD_NUMBER = FW_VERSION - 1
        PROTOCOL_ID = FW_BUILD_NUMBER - 1
        R7 = PROTOCOL_ID - 1
        R8 = R7 - 1
        PADDING = R8 - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        R0 = 0x08
        FW_NAME = 0x08
        FW_VERSION = 0x08
        FW_BUILD_NUMBER = 0x10
        PROTOCOL_ID = 0x10
        R7 = 0x08
        R8 = 0x08
        PADDING = 0x38
    # end class LEN

    class OFFSET(GetLongRegister.OFFSET):
        """
        Fields offset in bytes
        """
        R0 = GetLongRegister.OFFSET.ADDRESS + 0x01
        FW_NAME = R0 + 0x01
        FW_VERSION = FW_NAME + 0x01
        FW_BUILD_NUMBER = FW_VERSION + 0x01
        PROTOCOL_ID = FW_BUILD_NUMBER + 0x02
        R7 = PROTOCOL_ID + 0x02
        R8 = R7 + 0x01
        PADDING = R8 + 0x01
    # end class OFFSET

    class DEFAULT(GetLongRegister.DEFAULT):
        """
        Fields default values
        """
    # end class DEFAULT

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.FW_NAME,
                 LEN.FW_NAME,
                 title='FwName',
                 name='fw_name',
                 aliases=('fw_number',),
                 checks=(CheckHexList(LEN.FW_NAME // 8), CheckByte(),)),
        BitField(FID.FW_VERSION,
                 LEN.FW_VERSION,
                 title='FwVersion',
                 name='fw_version',
                 checks=(CheckHexList(LEN.FW_VERSION // 8), CheckByte(),)),
        BitField(FID.FW_BUILD_NUMBER,
                 LEN.FW_BUILD_NUMBER,
                 title='FwBuildNumber',
                 name='fw_build_number',
                 checks=(CheckHexList(LEN.FW_BUILD_NUMBER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FW_BUILD_NUMBER) - 1),)),
        BitField(FID.PROTOCOL_ID,
                 LEN.PROTOCOL_ID,
                 title='ProtocolId',
                 name='protocol_id',
                 aliases=('equad_id', 'bluetooth_pid',),
                 checks=(CheckHexList(LEN.PROTOCOL_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PROTOCOL_ID) - 1),)),
        BitField(FID.R7,
                 LEN.R7,
                 title='R7',
                 name='r7',
                 aliases=('equad_version_msb', 'ble_protocol_version',),
                 checks=(CheckHexList(LEN.R7 // 8), CheckByte(),)),
        BitField(FID.R8,
                 LEN.R8,
                 title='R8',
                 name='r8',
                 aliases=('equad_version_lsb', 'number_of_pairing_slots',),
                 checks=(CheckHexList(LEN.R8 // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8), CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, fw_name=0, fw_version=0, fw_build_number=0, protocol_id=0, r7=0, r8=0):
        """
        :param fw_name: FW name parameter value
        :type fw_name: ``int`` or ``HexList``
        :param fw_version: FW version parameter value
        :type fw_version: ``int`` or ``HexList``
        :param fw_build_number: FW build number parameter value
        :type fw_build_number: ``int`` or ``HexList``
        :param protocol_id: Protocol ID parameter value
        :type protocol_id: ``int`` or ``HexList``
        :param r7: R7 parameter value
        :type r7: ``int`` or ``HexList``
        :param r8: R8 parameter value
        :type r8: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = NonVolatilePairingInformation.R0.FW_VERSION
        self.fw_name = fw_name
        self.fw_version = fw_version
        self.fw_build_number = fw_build_number
        self.protocol_id = protocol_id
        self.r7 = r7
        self.r8 = r8
    # end def __init__
# end class GetFwVersionResponse


class GetTransceiverEQuadInformation(GetLongRegisterRequest):
    """
    Reading this register allows to get Transceiver eQuad Information
    """

    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=NonVolatilePairingInformation.R0.TRANSCEIVER_EQUAD_INFORMATION)
    # end def __init__
# end class GetTransceiverEQuadInformation


class GetTransceiverEQuadInformationResponse(GetLongRegister):
    """
    Reading this register allows to get Transceiver eQuad Information
    """

    class FID(GetLongRegister.FID):
        # See ``GetLongRegister.FID``
        R0 = GetLongRegister.FID.ADDRESS - 1
        BASE_ADDRESS = R0 - 1
        RF_CHANNEL_INDEX = BASE_ADDRESS - 1
        NUMBER_OF_PAIRING_SLOTS = RF_CHANNEL_INDEX - 1
        LAST_DEST_ID = NUMBER_OF_PAIRING_SLOTS - 1
        NUMBER_OF_REMAINING_CONNECTIONS = LAST_DEST_ID - 1
        PADDING = NUMBER_OF_REMAINING_CONNECTIONS - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        # See ``GetLongRegister.LEN``
        R0 = 0x08
        BASE_ADDRESS = 0x20
        RF_CHANNEL_INDEX = 0x08
        NUMBER_OF_PAIRING_SLOTS = 0x08
        LAST_DEST_ID = 0x08
        NUMBER_OF_REMAINING_CONNECTIONS = 0x08
        PADDING = 0x38
    # end class LEN

    class OFFSET(GetLongRegister.OFFSET):
        # See ``GetLongRegister.OFFSET``
        R0 = GetLongRegister.OFFSET.ADDRESS + 0x01
        BASE_ADDRESS = R0 + 0x01
        RF_CHANNEL_INDEX = BASE_ADDRESS + 0x04
        NUMBER_OF_PAIRING_SLOTS = RF_CHANNEL_INDEX + 0x01
        LAST_DEST_ID = NUMBER_OF_PAIRING_SLOTS + 0x01
        NUMBER_OF_REMAINING_CONNECTIONS = LAST_DEST_ID + 0x01
        PADDING = NUMBER_OF_REMAINING_CONNECTIONS + 0x01
    # end class OFFSET

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.BASE_ADDRESS,
                 LEN.BASE_ADDRESS,
                 title='BaseAddress',
                 name='base_address',
                 checks=(CheckHexList(LEN.BASE_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BASE_ADDRESS) - 1),)),
        BitField(FID.RF_CHANNEL_INDEX,
                 LEN.RF_CHANNEL_INDEX,
                 title='RFChannelIndex',
                 name='rf_channel_index',
                 checks=(CheckHexList(LEN.RF_CHANNEL_INDEX // 8),
                         CheckByte(),)),
        BitField(FID.NUMBER_OF_PAIRING_SLOTS,
                 LEN.NUMBER_OF_PAIRING_SLOTS,
                 title='NumberOfPairingSlots',
                 name='number_of_pairing_slots',
                 checks=(CheckHexList(LEN.NUMBER_OF_PAIRING_SLOTS // 8),
                         CheckByte(),)),
        BitField(FID.LAST_DEST_ID,
                 LEN.LAST_DEST_ID,
                 title='LastDestID',
                 name='last_dest_id',
                 checks=(CheckHexList(LEN.LAST_DEST_ID // 8),
                         CheckByte(),)),
        BitField(FID.NUMBER_OF_REMAINING_CONNECTIONS,
                 LEN.NUMBER_OF_REMAINING_CONNECTIONS,
                 title='NumberOfRemainingConnections',
                 name='number_of_remaining_connections',
                 checks=(CheckHexList(LEN.NUMBER_OF_REMAINING_CONNECTIONS // 8),
                         CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=GetLongRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, base_address=0, rf_channel_index=0, number_of_pairing_slots=0, last_dest_id=0,
                 number_of_remaining_connections=0):
        """
        :param base_address: eQuad base address
        :type base_address: ``HexList``
        :param rf_channel_index: RF channel index, 0=reserved, 1-24=valid channel index, 24-255=reserved
        :type rf_channel_index: ``HexList``
        :param number_of_pairing_slots: number of pairing slots
        :type number_of_pairing_slots: ``HexList``
        :param last_dest_id: last dest id assigned
        :type last_dest_id: ``HexList``
        :param number_of_remaining_connections: number of remaining receiver connections available for factory pairing
        :type number_of_remaining_connections: ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = NonVolatilePairingInformation.R0.TRANSCEIVER_EQUAD_INFORMATION
        self.base_address = base_address
        self.rf_channel_index = rf_channel_index
        self.number_of_pairing_slots = number_of_pairing_slots
        self.last_dest_id = last_dest_id
        self.number_of_remaining_connections = number_of_remaining_connections
    # end def __init__
# end class GetTransceiverEQuadInformationResponse


class SetTransceiverEQuadInformationRequest(SetLongRegister):
    """
    Set Transceiver eQuad Information request
    """
    class FID(SetLongRegister.FID):
        # See ``SetLongRegister.FID``
        R0 = SetLongRegister.FID.ADDRESS - 1
        BASE_ADDRESS = R0 - 1
        RF_CHANNEL_INDEX = BASE_ADDRESS - 1
        NUMBER_OF_PAIRING_SLOTS = RF_CHANNEL_INDEX - 1
        LAST_DEST_ID = NUMBER_OF_PAIRING_SLOTS - 1
        PADDING = LAST_DEST_ID - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        # See ``SetLongRegister.LEN``
        R0 = 0x08
        BASE_ADDRESS = 0x20
        RF_CHANNEL_INDEX = 0x08
        NUMBER_OF_PAIRING_SLOTS = 0x08
        LAST_DEST_ID = 0x08
        NUMBER_OF_REMAINING_CONNECTIONS = 0x08
        PADDING = 0x40
    # end class LEN

    class OFFSET(SetLongRegister.OFFSET):
        # See ``SetLongRegister.OFFSET``
        R0 = SetLongRegister.OFFSET.ADDRESS + 0x01
        BASE_ADDRESS = R0 + 0x01
        RF_CHANNEL_INDEX = BASE_ADDRESS + 0x04
        NUMBER_OF_PAIRING_SLOTS = RF_CHANNEL_INDEX + 0x01
        LAST_DEST_ID = NUMBER_OF_PAIRING_SLOTS + 0x01
        NUMBER_OF_REMAINING_CONNECTIONS = LAST_DEST_ID + 0x01
        PADDING = NUMBER_OF_REMAINING_CONNECTIONS + 0x01
    # end class OFFSET

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.BASE_ADDRESS,
                 LEN.BASE_ADDRESS,
                 title='BaseAddress',
                 name='base_address',
                 checks=(CheckHexList(LEN.BASE_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BASE_ADDRESS) - 1),)),
        BitField(FID.RF_CHANNEL_INDEX,
                 LEN.RF_CHANNEL_INDEX,
                 title='RFChannelIndex',
                 name='rf_channel_index',
                 checks=(CheckHexList(LEN.RF_CHANNEL_INDEX // 8),
                         CheckByte(),)),
        BitField(FID.NUMBER_OF_PAIRING_SLOTS,
                 LEN.NUMBER_OF_PAIRING_SLOTS,
                 title='NumberOfPairingSlots',
                 name='number_of_pairing_slots',
                 checks=(CheckHexList(LEN.NUMBER_OF_PAIRING_SLOTS // 8),
                         CheckByte(),)),
        BitField(FID.LAST_DEST_ID,
                 LEN.LAST_DEST_ID,
                 title='LastDestID',
                 name='last_dest_id',
                 checks=(CheckHexList(LEN.LAST_DEST_ID // 8),
                         CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SetLongRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, base_address=0, rf_channel_index=0, number_of_pairing_slots=0, last_dest_id=0,):
        """
        :param base_address: eQuad base address
        :type base_address: ``HexList``
        :param rf_channel_index: RF channel index, 0=reserved, 1-24=valid channel index, 24-255=reserved
        :type rf_channel_index: ``HexList``
        :param number_of_pairing_slots: number of pairing slots
        :type number_of_pairing_slots: ``HexList``
        :param last_dest_id: last dest id assigned
        :type last_dest_id: ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = NonVolatilePairingInformation.R0.TRANSCEIVER_EQUAD_INFORMATION
        self.base_address = base_address
        self.rf_channel_index = rf_channel_index
        self.number_of_pairing_slots = number_of_pairing_slots
        self.last_dest_id = last_dest_id
    # end def __init__
# end class SetTransceiverEQuadInformationRequest


class SetTransceiverEQuadInformationResponse(SetLongRegisterResponse):
    """
    Set Transceiver eQuad Information response
    """
    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)
    # end def __init__
# end class SetTransceiverEQuadInformationResponse


class GetEQuadDevicePairingInfoRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get eQuad "step 4" device pairing information
    """
    def __init__(self, r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_PAIRING_INFO_MIN):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=r0)
    # end def __init__
# end class GetEQuadDevicePairingInfoRequest


class DevicePairingInfoPacketDataFormat(Register):
    """
    Allow this class is to be used as a base class for messages in this feature
        - GetEQuadDevicePairingInfoResponse
        - SetEQuadDevicePairingInfoRequest
    """
    class FID(Register.FID):
        # See ``Register.FID``
        R0 = Register.FID.ADDRESS - 1
        DESTINATION_ID = R0 - 1
        DEFAULT_REPORT_INTERVAL = DESTINATION_ID - 1
        DEVICE_QUID = DEFAULT_REPORT_INTERVAL - 1
        EQUAD_MAJOR_VERSION = DEVICE_QUID - 1
        EQUAD_MINOR_VERSION = EQUAD_MAJOR_VERSION - 1
        EQUAD_DEVICE_SUBCLASS = EQUAD_MINOR_VERSION - 1
        EQUAD_ATTRIBUTES = EQUAD_DEVICE_SUBCLASS - 1
        PADDING = EQUAD_ATTRIBUTES - 1
    # end class FID

    class LEN(Register.LEN):
        # See ``Register.LEN``
        R0 = 0x08
        DESTINATION_ID = 0x08
        DEFAULT_REPORT_INTERVAL = 0x08
        DEVICE_QUID = 0x10
        EQUAD_MAJOR_VERSION = 0x08
        EQUAD_MINOR_VERSION = 0x08
        EQUAD_DEVICE_SUBCLASS = 0x08
        EQUAD_ATTRIBUTES = 0x30
        PADDING = 0x10
    # end class LEN

    class OFFSET(Register.OFFSET):
        # See ``Register.OFFSET``
        R0 = GetLongRegister.OFFSET.ADDRESS + 0x01
        DESTINATION_ID = R0 + 0x01
        DEFAULT_REPORT_INTERVAL = DESTINATION_ID + 0x01
        DEVICE_QUID = DEFAULT_REPORT_INTERVAL + 0x01
        EQUAD_MAJOR_VERSION = DEVICE_QUID + 0x02
        EQUAD_MINOR_VERSION = EQUAD_MAJOR_VERSION + 0x01
        EQUAD_DEVICE_SUBCLASS = EQUAD_MINOR_VERSION + 0x01
        EQUAD_ATTRIBUTES = EQUAD_DEVICE_SUBCLASS + 0x01
        PADDING = EQUAD_ATTRIBUTES + 0x06
    # end class OFFSET

    class DEFAULT(Register.DEFAULT):
        """
        Fields default values
        """
    # end class DEFAULT

    FIELDS = Register.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 aliases=('index', 'pairing_slot',),
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.DESTINATION_ID,
                 LEN.DESTINATION_ID,
                 title='DestinationID',
                 name='destination_id',
                 checks=(CheckHexList(LEN.DESTINATION_ID // 8), CheckByte())),
        BitField(FID.DEFAULT_REPORT_INTERVAL,
                 LEN.DEFAULT_REPORT_INTERVAL,
                 title='DefaultReportInterval',
                 name='default_report_interval',
                 checks=(CheckHexList(LEN.DEFAULT_REPORT_INTERVAL // 8), CheckByte())),
        BitField(FID.DEVICE_QUID,
                 LEN.DEVICE_QUID,
                 title='DeviceQUID',
                 name='device_quid',
                 checks=(CheckHexList(LEN.DEVICE_QUID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_QUID) - 1),)),
        BitField(FID.EQUAD_MAJOR_VERSION,
                 LEN.EQUAD_MAJOR_VERSION,
                 title='eQuadMajorVersion',
                 name='equad_major_version',
                 checks=(CheckHexList(LEN.EQUAD_MAJOR_VERSION // 8), CheckByte())),
        BitField(FID.EQUAD_MINOR_VERSION,
                 LEN.EQUAD_MINOR_VERSION,
                 title='eQuadMinorVersion',
                 name='equad_minor_version',
                 checks=(CheckHexList(LEN.EQUAD_MINOR_VERSION // 8), CheckByte())),
        BitField(FID.EQUAD_DEVICE_SUBCLASS,
                 LEN.EQUAD_DEVICE_SUBCLASS,
                 title='eQuadDeviceSubclass',
                 name='equad_device_subclass',
                 checks=(CheckHexList(LEN.EQUAD_DEVICE_SUBCLASS // 8), CheckByte())),
        BitField(FID.EQUAD_ATTRIBUTES,
                 LEN.EQUAD_ATTRIBUTES,
                 title='eQuadAttributes',
                 name='equad_attributes',
                 checks=(CheckHexList(LEN.EQUAD_ATTRIBUTES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EQUAD_ATTRIBUTES) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )
# end class DevicePairingInfoPacketDataFormat


class GetEQuadDevicePairingInfoResponse(DevicePairingInfoPacketDataFormat, GetLongRegister):
    """
    Response to device - pairing information read long register command
    """

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_PAIRING_INFO_MIN,
                 destination_id=0,
                 default_report_interval=0,
                 device_quid=0,
                 equad_major_version=0,
                 equad_minor_version=0,
                 equad_device_subclass=0,
                 equad_attributes=0):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param destination_id: Destination ID parameter value
        :type destination_id: ``int`` or ``HexList``
        :param default_report_interval: Default report interval parameter value
        :type default_report_interval: ``int`` or ``HexList``
        :param device_quid: Device QUID parameter value
        :type device_quid: ``int`` or ``HexList``
        :param equad_major_version: eQuad major version parameter value
        :type equad_major_version: ``int`` or ``HexList``
        :param equad_minor_version: eQuad minor version parameter value
        :type equad_minor_version: ``int`` or ``HexList``
        :param equad_device_subclass: eQuad device subclass parameter value
        :type equad_device_subclass: ``int`` or ``HexList``
        :param equad_attributes: eQuad attributes parameter value
        :type equad_attributes: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.destination_id = destination_id
        self.default_report_interval = default_report_interval
        self.device_quid = device_quid
        self.equad_major_version = equad_major_version
        self.equad_minor_version = equad_minor_version
        self.equad_device_subclass = equad_device_subclass
        self.equad_attributes = equad_attributes
    # end def __init__
# end class GetEQuadDevicePairingInfoResponse


class SetEQuadDevicePairingInformationRequest(DevicePairingInfoPacketDataFormat, SetLongRegister):
    """
    Set Device pairing information request
    """

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_PAIRING_INFO_MIN,
                 destination_id=0,
                 default_report_interval=0,
                 device_quid=0,
                 equad_major_version=0,
                 equad_minor_version=0,
                 equad_device_subclass=0,
                 equad_attributes=0):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param destination_id: Destination ID parameter value
        :type destination_id: ``int`` or ``HexList``
        :param default_report_interval: Default report interval parameter value
        :type default_report_interval: ``int`` or ``HexList``
        :param device_quid: Device QUID parameter value
        :type device_quid: ``int`` or ``HexList``
        :param equad_major_version: eQuad major version parameter value
        :type equad_major_version: ``int`` or ``HexList``
        :param equad_minor_version: eQuad minor version parameter value
        :type equad_minor_version: ``int`` or ``HexList``
        :param equad_device_subclass: eQuad device subclass parameter value
        :type equad_device_subclass: ``int`` or ``HexList``
        :param equad_attributes: eQuad attributes parameter value
        :type equad_attributes: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.destination_id = destination_id
        self.default_report_interval = default_report_interval
        self.device_quid = device_quid
        self.equad_major_version = equad_major_version
        self.equad_minor_version = equad_minor_version
        self.equad_device_subclass = equad_device_subclass
        self.equad_attributes = equad_attributes
    # end def __init__
# end class SetEQuadDevicePairingInformationRequest


class SetEQuadDevicePairingInformationResponse(SetLongRegisterResponse):
    """
    Set Device pairing information response
    """
    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)
    # end def __init__
# end class SetEQuadDevicePairingInformationResponse


class GetEQuadDeviceExtendedPairingInfoRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get eQuad "step 4" device extended pairing information
    """
    def __init__(self, r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_EXT_PAIRING_INFO_MIN):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=r0)
    # end def __init__
# end class GetEQuadDeviceExtendedPairingInfoRequest


class DeviceExtendedPairingInfoPacketDataFormat(Register):
    """
    Allow this class is to be used as a base class for messages in this feature
        - GetEQuadDeviceExtendedPairingInfoRequest
        - SetEQuadDeviceExtendedPairingInfoRequest
    """
    class FID(Register.FID):
        # See ``Register.FID``
        R0 = Register.FID.ADDRESS - 1
        SERIAL_NUMBER = R0 - 1
        REPORT_TYPES = SERIAL_NUMBER - 1
        USABILITY_INFO = REPORT_TYPES - 1
        PADDING = USABILITY_INFO - 1
    # end class FID

    class LEN(Register.LEN):
        # See ``Register.LEN``
        R0 = 0x08
        SERIAL_NUMBER = 0x20
        REPORT_TYPES = 0x20
        USABILITY_INFO = 0x08
        PADDING = 0x30
    # end class LEN

    class OFFSET(Register.OFFSET):
        # See ``Register.OFFSET``
        R0 = Register.OFFSET.ADDRESS + 0x01
        SERIAL_NUMBER = R0 + 0x01
        REPORT_TYPES = SERIAL_NUMBER + 0x04
        USABILITY_INFO = REPORT_TYPES + 0x04
        PADDING = USABILITY_INFO + 0x01
    # end class OFFSET

    class DEFAULT(Register.DEFAULT):
        """
        Fields default values
        """
    # end class DEFAULT

    FIELDS = Register.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 aliases=('index', 'pairing_slot',),
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.SERIAL_NUMBER,
                 LEN.SERIAL_NUMBER,
                 title='SerialNumber',
                 name='serial_number',
                 checks=(CheckHexList(LEN.SERIAL_NUMBER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SERIAL_NUMBER) - 1),)),
        BitField(FID.REPORT_TYPES,
                 LEN.REPORT_TYPES,
                 title='ReportTypes',
                 name='report_types',
                 checks=(CheckHexList(LEN.REPORT_TYPES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REPORT_TYPES) - 1),)),
        BitField(FID.USABILITY_INFO,
                 LEN.USABILITY_INFO,
                 title='UsabilityInfo',
                 name='usability_info',
                 checks=(CheckHexList(LEN.USABILITY_INFO // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.USABILITY_INFO) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )
# end class DeviceExtendedPairingInfoPacketDataFormat


class GetEQuadDeviceExtendedPairingInfoResponse(DeviceExtendedPairingInfoPacketDataFormat, GetLongRegister):
    """
    Get device extended pairing information response
    """

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_EXT_PAIRING_INFO_MIN,
                 serial_number=0,
                 report_types=0,
                 usability_info=0):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param serial_number: Serial number parameter value
        :type serial_number: ``int`` or ``HexList``
        :param report_types: Report types parameter value
        :type report_types: ``int`` or ``HexList``
        :param usability_info: Device usability info parameter value
        :type usability_info: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.serial_number = serial_number
        self.report_types = report_types
        self.usability_info = usability_info
    # end def __init__
# end class GetEQuadDeviceExtendedPairingInfoResponse


class SetEQuadDeviceExtendedPairingInfoRequest(DeviceExtendedPairingInfoPacketDataFormat, SetLongRegister):
    """
    Set device extended pairing information request
    """

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_EXT_PAIRING_INFO_MIN,
                 serial_number=0,
                 report_types=0,
                 usability_info=0):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param serial_number: Serial number parameter value
        :type serial_number: ``int`` or ``HexList``
        :param report_types: Report types parameter value
        :type report_types: ``int`` or ``HexList``
        :param usability_info: Device usability info parameter value
        :type usability_info: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.serial_number = serial_number
        self.report_types = report_types
        self.usability_info = usability_info
    # end def __init__
# end class SetEQuadDeviceExtendedPairingInfoRequest


class SetEQuadDeviceExtendedPairingInfoResponse(SetLongRegisterResponse):
    """
    Set device extended pairing information response
    """
    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)
    # end def __init__
# end class SetEQuadDeviceExtendedPairingInfoResponse


class SetAesEncryptionKeyRequest(SetLongRegister):
    """
    Writing AES encryption key request
    """
    class FID(SetLongRegister.FID):
        # See ``SetLongRegister.FID``
        P0 = SetLongRegister.FID.ADDRESS - 1
        AES_ENCRYPTION_KEY_BYTE_1_TO_6 = P0 - 1
        AES_ENCRYPTION_KEY_BYTE_9_TO_16 = AES_ENCRYPTION_KEY_BYTE_1_TO_6 - 1
        PADDING = AES_ENCRYPTION_KEY_BYTE_9_TO_16 - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        # See ``SetLongRegister.LEN``
        P0 = 0x08
        AES_ENCRYPTION_KEY_BYTE_1_TO_6 = 0x30
        AES_ENCRYPTION_KEY_BYTE_9_TO_16 = 0x40
        PADDING = 0x08
    # end class LEN

    class DEFAULT(SetLongRegister.DEFAULT):
        """
        Fields default values
        """
    # end class DEFAULT

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.P0,
                 LEN.P0,
                 title='P0',
                 name='p0',
                 checks=(CheckHexList(LEN.P0 // 8), CheckByte())),
        BitField(FID.AES_ENCRYPTION_KEY_BYTE_1_TO_6,
                 LEN.AES_ENCRYPTION_KEY_BYTE_1_TO_6,
                 title='AesEncryptionKeyByte1To6',
                 name='aes_encryption_key_byte_1_to_6',
                 checks=(CheckHexList(LEN.AES_ENCRYPTION_KEY_BYTE_1_TO_6 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.AES_ENCRYPTION_KEY_BYTE_1_TO_6) - 1),)),
        BitField(FID.AES_ENCRYPTION_KEY_BYTE_9_TO_16,
                 LEN.AES_ENCRYPTION_KEY_BYTE_9_TO_16,
                 title='AesEncryptionKeyByte9To16',
                 name='aes_encryption_key_byte_9_to_16',
                 checks=(CheckHexList(LEN.AES_ENCRYPTION_KEY_BYTE_9_TO_16 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.AES_ENCRYPTION_KEY_BYTE_9_TO_16) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.AES_ENCRYPTION_KEY_BYTE_9_TO_16 // 8), CheckByte()),
                 default_value=DEFAULT.PADDING),
    )

    def __init__(self,
                 p0=NonVolatilePairingInformation.R0.EQUAD_STEP4_AES_ENCRYPTION_KEY_MIN,
                 aes_encryption_key_byte_1_to_6=0,
                 aes_encryption_key_byte_9_to_16=0):
        """
        :param p0: P0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type p0: ``int`` or ``HexList``
        :param aes_encryption_key_byte_1_to_6: AES encryption key bytes 1 to 6 parameter value
        :type aes_encryption_key_byte_1_to_6: ``HexList``
        :param aes_encryption_key_byte_9_to_16: AES encryption key bytes 9 to 16 parameter value
        :type aes_encryption_key_byte_9_to_16: ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.p0 = p0
        self.aes_encryption_key_byte_1_to_6 = aes_encryption_key_byte_1_to_6
        self.aes_encryption_key_byte_9_to_16 = aes_encryption_key_byte_9_to_16
    # end def __init__
# end class SetAesEncryptionKeyRequest


class SetAesEncryptionKeyResponse(SetLongRegisterResponse):
    """
    Writing AES encryption key response
    """
    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)
    # end def __init__
# end class SetAesEncryptionKeyResponse


class GetEQuadDeviceNameRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get eQuad Device name
    """
    def __init__(self, r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=r0)
    # end def __init__
# end class GetEQuadDeviceNameRequest


class EQuadDeviceNamePacketDataFormat(Register):
    """
    Allow this class is to be used as a base class for messages in this feature
        - GetEQuadDeviceNameResponse
        - SetEQuadDeviceNameRequest
    """
    class FID(Register.FID):
        # See ``Register.FID``
        R0 = Register.FID.ADDRESS - 1
        SEGMENT_LENGTH = R0 - 1
        NAME_STRING = SEGMENT_LENGTH - 1
    # end class FID

    class LEN(Register.LEN):
        # See ``Register.LEN``
        R0 = 0x08
        SEGMENT_LENGTH = 0x08
        NAME_STRING = 14 * 0x08
    # end class LEN

    class OFFSET(Register.OFFSET):
        # See ``Register.OFFSET``
        R0 = Register.OFFSET.ADDRESS + 0x01
    # end class OFFSET

    FIELDS = Register.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.SEGMENT_LENGTH,
                 LEN.SEGMENT_LENGTH,
                 title='SegmentLength',
                 name='segment_length',
                 checks=(CheckHexList(LEN.SEGMENT_LENGTH // 8), CheckByte())),
        BitField(FID.NAME_STRING,
                 LEN.NAME_STRING,
                 title='NameString',
                 name='name_string',
                 checks=(CheckHexList(LEN.NAME_STRING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NAME_STRING) - 1),)),
    )
# end class EQuadDeviceNamePacketDataFormat


class GetEQuadDeviceNameResponse(EQuadDeviceNamePacketDataFormat, GetLongRegister):
    """
    Read eQuad Device name response
    """

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN,
                 segment_length=0,
                 name_string=0):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param segment_length: Segment length parameter value
        :type segment_length: ``int`` or ``HexList``
        :param name_string: Name string parameter value
        :type name_string: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.segment_length = segment_length
        self.name_string = name_string
    # end def __init__
# end class GetEQuadDeviceNameResponse


class SetEQuadDeviceNameRequest(EQuadDeviceNamePacketDataFormat, SetLongRegister):
    """
    Set eQuad Device name request
    """

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN,
                 segment_length=0,
                 name_string=0):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param segment_length: Segment length parameter value
        :type segment_length: ``int`` or ``HexList``
        :param name_string: Name string parameter value
        :type name_string: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.segment_length = segment_length
        self.name_string = name_string
    # end def __init__
# end class SetEQuadDeviceNameRequest


class SetEQuadDeviceNameResponse(SetLongRegisterResponse):
    """
    Set eQuad Device name response
    """
    def __init__(self):
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)
    # end def __init__
# end class SetEQuadDeviceNameResponse


class GetBLEProDevicePairingInfoRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get BLE Pro device pairing information
    """
    def __init__(self, r0=NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=r0)
    # end def __init__
# end class GetBLEProDevicePairingInfoRequest


class GetBLEProDevicePairingInfoResponse(GetLongRegister):
    """
    Response to BLE Pro device - pairing information read long register command
    """
    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        R0 = GetLongRegister.FID.ADDRESS - 1
        DEVICE_INFO_RESERVED_7 = R0 - 1
        LINK_STATUS = DEVICE_INFO_RESERVED_7 - 1
        DEVICE_INFO_RESERVED_4_5 = LINK_STATUS - 1
        DEVICE_TYPE = DEVICE_INFO_RESERVED_4_5 - 1
        BLUETOOTH_PID = DEVICE_TYPE - 1
        DEVICE_UNIT_ID = BLUETOOTH_PID - 1
        BLE_PRO_SERVICE_VERSION = DEVICE_UNIT_ID - 1
        PRODUCT_SPECIFIC_DATA = BLE_PRO_SERVICE_VERSION - 1
        PREPAIRING_AUTH_METHOD = PRODUCT_SPECIFIC_DATA - 1
        RESERVED_AUTH_METHOD = PREPAIRING_AUTH_METHOD - 1
        EMU_2BUTTONS_AUTH_METHOD = RESERVED_AUTH_METHOD - 1
        PASSKEY_AUTH_METHOD = EMU_2BUTTONS_AUTH_METHOD - 1
        AUTH_ENTROPY = PASSKEY_AUTH_METHOD - 1
        DEVICE_STATE = AUTH_ENTROPY - 1
        PADDING = DEVICE_STATE - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        R0 = 0x08
        DEVICE_INFO_RESERVED_7 = 0x01
        LINK_STATUS = 0x01
        DEVICE_INFO_RESERVED_4_5 = 0x02
        DEVICE_TYPE = 0x04
        BLUETOOTH_PID = 0x10
        DEVICE_UNIT_ID = 0x20
        BLE_PRO_SERVICE_VERSION = 0x08
        PRODUCT_SPECIFIC_DATA = 0x08
        PREPAIRING_AUTH_METHOD = 0x01
        RESERVED_AUTH_METHOD = 0x05
        EMU_2BUTTONS_AUTH_METHOD = 0x01
        PASSKEY_AUTH_METHOD = 0x01
        AUTH_ENTROPY = 0x08
        DEVICE_STATE = 0x08
        PADDING = 0x18
    # end class LEN

    class OFFSET(GetLongRegister.OFFSET):
        """
        Fields offset in bytes
        """
        R0 = GetLongRegister.OFFSET.ADDRESS + 0x01
        DEVICE_INFO = R0 + 0x01
        BLUETOOTH_PID = DEVICE_INFO + 0x01
        DEVICE_UNIT_ID = BLUETOOTH_PID + 0x02
        BLE_PROTOCOL_VERSION = DEVICE_UNIT_ID + 0x04
        PRODUCT_SPECIFIC_DATA = BLE_PROTOCOL_VERSION + 0x01
        DEVICE_STATE = PRODUCT_SPECIFIC_DATA + 0x01
        PADDING = DEVICE_STATE + 0x01
    # end class OFFSET

    class DEFAULT(GetLongRegister.DEFAULT):
        """
        Fields default values
        """
    # end class DEFAULT

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 aliases=('index', 'pairing_slot',),
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.DEVICE_INFO_RESERVED_7,
                 LEN.DEVICE_INFO_RESERVED_7,
                 title='DeviceInfoReserved7',
                 name='device_info_reserved_7',
                 checks=(CheckHexList(LEN.DEVICE_INFO_RESERVED_7 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_RESERVED_7) - 1),)),
        BitField(FID.LINK_STATUS,
                 LEN.LINK_STATUS,
                 title='LinkStatus',
                 name='link_status',
                 checks=(CheckHexList(LEN.LINK_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LINK_STATUS) - 1),)),
        BitField(FID.DEVICE_INFO_RESERVED_4_5,
                 LEN.DEVICE_INFO_RESERVED_4_5,
                 title='DeviceInfoReserved45',
                 name='device_info_reserved_4_5',
                 checks=(CheckHexList(LEN.DEVICE_INFO_RESERVED_4_5 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_RESERVED_4_5) - 1),)),
        BitField(FID.DEVICE_TYPE,
                 LEN.DEVICE_TYPE,
                 title='DeviceType',
                 name='device_type',
                 checks=(CheckHexList(LEN.DEVICE_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_TYPE) - 1),)),
        BitField(FID.BLUETOOTH_PID,
                 LEN.BLUETOOTH_PID,
                 title='BluetoothPid',
                 name='bluetooth_pid',
                 checks=(CheckHexList(LEN.BLUETOOTH_PID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BLUETOOTH_PID) - 1),)),
        BitField(FID.DEVICE_UNIT_ID,
                 LEN.DEVICE_UNIT_ID,
                 title='DeviceUnitId',
                 name='device_unit_id',
                 checks=(CheckHexList(LEN.DEVICE_UNIT_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_UNIT_ID) - 1),)),
        BitField(FID.BLE_PRO_SERVICE_VERSION,
                 LEN.BLE_PRO_SERVICE_VERSION,
                 title='BleProServiceVersion',
                 name='ble_pro_service_version',
                 checks=(CheckHexList(LEN.BLE_PRO_SERVICE_VERSION // 8), CheckByte())),
        BitField(FID.PRODUCT_SPECIFIC_DATA,
                 LEN.PRODUCT_SPECIFIC_DATA,
                 title='ProductSpecificData',
                 name='product_specific_data',
                 aliases=('extended_model_id',),
                 checks=(CheckHexList(LEN.PRODUCT_SPECIFIC_DATA // 8), CheckByte())),
        BitField(FID.PREPAIRING_AUTH_METHOD,
                 LEN.PREPAIRING_AUTH_METHOD,
                 title='PrepairingAuthMethod',
                 name='prepairing_auth_method',
                 checks=(CheckHexList(LEN.PREPAIRING_AUTH_METHOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PREPAIRING_AUTH_METHOD) - 1),),
                 default_value=0),
        BitField(FID.RESERVED_AUTH_METHOD,
                 LEN.RESERVED_AUTH_METHOD,
                 title='ReservedAuthMethod',
                 name='reserved_auth_method',
                 checks=(CheckHexList(LEN.RESERVED_AUTH_METHOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED_AUTH_METHOD) - 1),)),
        BitField(FID.EMU_2BUTTONS_AUTH_METHOD,
                 LEN.EMU_2BUTTONS_AUTH_METHOD,
                 title='Emu2ButtonsAuthMethod',
                 name='emu_2_buttons_auth_method',
                 checks=(CheckHexList(LEN.EMU_2BUTTONS_AUTH_METHOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EMU_2BUTTONS_AUTH_METHOD) - 1),)),
        BitField(FID.PASSKEY_AUTH_METHOD,
                 LEN.PASSKEY_AUTH_METHOD,
                 title='PasskeyAuthMethod',
                 name='passkey_auth_method',
                 checks=(CheckHexList(LEN.PASSKEY_AUTH_METHOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PASSKEY_AUTH_METHOD) - 1),)),
        BitField(FID.AUTH_ENTROPY,
                 LEN.AUTH_ENTROPY,
                 title='AuthEntropy',
                 name='auth_entropy',
                 checks=(CheckHexList(LEN.AUTH_ENTROPY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.AUTH_ENTROPY) - 1),)),
        BitField(FID.DEVICE_STATE,
                 LEN.DEVICE_STATE,
                 title='DeviceState',
                 name='device_state',
                 checks=(CheckHexList(LEN.DEVICE_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_STATE) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN,
                 device_type=0,
                 link_status=0,
                 bluetooth_pid=0,
                 device_unit_id=0,
                 ble_pro_service_version=0,
                 product_specific_data=0,
                 prepairing_auth_method=0,
                 emu_2buttons_auth_method=0,
                 passkey_auth_method=0,
                 auth_entropy=0,
                 device_state=0):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param device_type: Device type parameter value
        :type device_type: ``int`` or ``HexList``
        :param link_status: Link status parameter value
        :type link_status: ``int`` or ``HexList``
        :param bluetooth_pid: Bluetooth PID parameter value
        :type bluetooth_pid: ``int`` or ``HexList``
        :param device_unit_id: Device Unit ID parameter value
        :type device_unit_id: ``int`` or ``HexList``
        :param ble_pro_service_version: BLE Pro service version parameter value
        :type ble_pro_service_version: ``int`` or ``HexList``
        :param product_specific_data: Product specific data parameter value
        :type product_specific_data: ``int`` or ``HexList``
        :param prepairing_auth_method: Prepairing authentication method parameter value
        :type prepairing_auth_method: ``int`` or ``HexList``
        :param emu_2buttons_auth_method: Emulate 2 buttons authentication method parameter value
        :type emu_2buttons_auth_method: ``int`` or ``HexList``
        :param passkey_auth_method: Passkey authentication method parameter value
        :type passkey_auth_method: ``int`` or ``HexList``
        :param auth_entropy: Authentication entropy parameter value
        :type auth_entropy: ``int`` or ``HexList``
        :param device_state: Device state parameter value
        :type device_state: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.device_type = device_type
        self.link_status = link_status
        self.bluetooth_pid = bluetooth_pid
        self.device_unit_id = device_unit_id
        self.ble_pro_service_version = ble_pro_service_version
        self.product_specific_data = product_specific_data
        self.prepairing_auth_method = prepairing_auth_method
        self.emu_2buttons_auth_method = emu_2buttons_auth_method
        self.passkey_auth_method = passkey_auth_method
        self.auth_entropy = auth_entropy
        self.device_state = device_state
    # end def __init__
# end class GetBLEProDevicePairingInfoResponse


class GetBLEProDeviceDeviceNameRequest(GetLongRegisterRequest):
    """
    Reading this register allows to get BLE Pro device device name
    """
    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN,
                 device_name_part=NonVolatilePairingInformation.BleProDeviceNamePart.PART_1):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param device_name_part: Device name part parameter value
        :type device_name_part: ``int`` or ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION,
                         r0=r0)
        self.get_field_from_name("r1").add_alias("device_name_part")
        self.device_name_part = device_name_part
    # end def __init__
# end class GetBLEProDeviceDeviceNameRequest


class GetBLEProDeviceDeviceNameResponse(GetLongRegister):
    """
    Response to BLE Pro device - device name read long register command
    """
    class FID(GetLongRegister.FID):
        """
        Field Identifiers
        """
        R0 = GetLongRegister.FID.ADDRESS - 1
        DEVICE_NAME_PART = R0 - 1
        DATA = DEVICE_NAME_PART - 1
    # end class FID

    class LEN(GetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        R0 = 0x08
        DEVICE_NAME_PART = 0x08
        DATA = 0x70
    # end class LEN

    class OFFSET(GetLongRegister.OFFSET):
        """
        Fields offset in bytes
        """
        R0 = GetLongRegister.OFFSET.ADDRESS + 0x01
        DEVICE_NAME_PART = R0 + 0x01
        DATA = DEVICE_NAME_PART + 0x01
    # end class OFFSET

    class DeviceNamePart1(BitFieldContainerMixin):
        """
        This class defines the format of BLE Pro Device - Device Name Part 1 response

        Format:
        || @b Name                || @b Bit count ||
        || Device Name length     || 8            ||
        || Device Name start      || 104          ||
        """
        class FID:
            """
            Field identifiers
            """
            DEVICE_NAME_LENGTH = 0xFF
            DEVICE_NAME_START = DEVICE_NAME_LENGTH - 1
        # end class FID

        class LEN:
            """
            Field identifiers
            """
            DEVICE_NAME_LENGTH = 0x08
            DEVICE_NAME_START = 0x68
        # end class FID

        FIELDS = (
            BitField(FID.DEVICE_NAME_LENGTH,
                     LEN.DEVICE_NAME_LENGTH,
                     title='DeviceNameLength',
                     name='device_name_length',
                     checks=(CheckHexList(LEN.DEVICE_NAME_LENGTH // 8),
                             CheckByte(),), ),
            BitField(FID.DEVICE_NAME_START,
                     LEN.DEVICE_NAME_START,
                     title='DeviceNameStart',
                     name='device_name_start',
                     checks=(CheckHexList(LEN.DEVICE_NAME_START // 8),),
                     )
        )
    # end class DeviceNamePart1

    class DeviceNamePart2or3(BitFieldContainerMixin):
        """
        This class defines the format of Device Discovery Part 2 event.

        Format:
        || @b Name                || @b Bit count ||
        || Device Name Chunk      || 112          ||
        """
        class FID:
            """
            Field Identifiers
            """
            DEVICE_NAME_CHUNK = 0xFF
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            DEVICE_NAME_CHUNK = 0x70
        # end class LEN

        FIELDS = (
            BitField(FID.DEVICE_NAME_CHUNK,
                     LEN.DEVICE_NAME_CHUNK,
                     title='DeviceNameChunk',
                     name='device_name_chunk',
                     checks=(CheckHexList(LEN.DEVICE_NAME_CHUNK // 8),),
                     ),
        )
    # end class DeviceNamePart2or3

    FIELDS = GetLongRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 aliases=('index', 'pairing_slot',),
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.DEVICE_NAME_PART,
                 LEN.DEVICE_NAME_PART,
                 title='DeviceNamePart',
                 name='device_name_part',
                 checks=(CheckHexList(LEN.DEVICE_NAME_PART // 8), CheckByte())),
        BitField(FID.DATA,
                 LEN.DATA,
                 title='Data',
                 name='data',
                 checks=(CheckHexList(LEN.DATA // 8),)),
    )

    def __init__(self,
                 r0=NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN,
                 device_name_part=0,
                 data=None):
        """
        :param r0: R0 parameter value, values can be found ``NonVolatilePairingInformation.R0``
        :type r0: ``int`` or ``HexList``
        :param device_name_part: Device name part parameter value
        :type device_name_part: ``int`` or ``HexList``
        :param data: Device name data parameter value
        :type data: ``HexList``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION)

        if data is None:
            data = HexList(Numeral(byteCount=self.LEN.DATA // 8))
        # end if

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.r0 = r0
        self.device_name_part = device_name_part
        if int(Numeral(self.device_name_part)) == NonVolatilePairingInformation.BleProDeviceNamePart.PART_1:
            self.data = GetBLEProDeviceDeviceNameResponse.DeviceNamePart1.fromHexList(data)
        elif int(Numeral(self.device_name_part)) == NonVolatilePairingInformation.BleProDeviceNamePart.PART_2:
            self.data = GetBLEProDeviceDeviceNameResponse.DeviceNamePart2or3.fromHexList(data)
        elif int(Numeral(self.device_name_part)) == NonVolatilePairingInformation.BleProDeviceNamePart.PART_3:
            self.data = GetBLEProDeviceDeviceNameResponse.DeviceNamePart2or3.fromHexList(data)
        else:
            self.data = data
        # end if
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        parts = NonVolatilePairingInformation.BleProDeviceNamePart

        if int(Numeral(inner_field_container_mixin.device_name_part)) == parts.PART_1:
            inner_field_container_mixin.data = GetBLEProDeviceDeviceNameResponse.DeviceNamePart1.fromHexList(
                inner_field_container_mixin.data)
        elif int(Numeral(inner_field_container_mixin.device_name_part)) in [parts.PART_2, parts.PART_3]:
            inner_field_container_mixin.data = GetBLEProDeviceDeviceNameResponse.DeviceNamePart2or3.fromHexList(
                inner_field_container_mixin.data)
        # end if
        return inner_field_container_mixin
    # end def fromHexList
# end class GetBLEProDevicePairingInfoResponse


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
