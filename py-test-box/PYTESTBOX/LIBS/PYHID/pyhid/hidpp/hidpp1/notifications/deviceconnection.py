#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.deviceconnection
    :brief: HID++ 1.0 Device Connection event interface definition
    :author: Stanislas Cottard
    :date: 2019/10/31
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidppmessage import HidppMessage


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceConnection(Hidpp1Message):
    """
    This class defines the format of Device Connection event.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    ProtocolType                  8
    Information                   24 or 128
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.DEVICE_CONNECTION

    class ProtocolTypes:
        UNKNOWN = 0x00
        BLUETOOTH = 0x01
        MHZ27 = 0x02
        QUAD_OR_EQUAD = 0x03
        EQUAD_STEP_4_DJ = 0x04
        DFU_LITE = 0x05
        EQUAD_STEP_4_LITE = 0x06
        EQUAD_STEP_4_GAMING = 0x07
        EQUAD_STEP_4_GAMEPADS = 0x08
        DVC_DEF_PROTOCOL_GOTHARD = 0x09
        DVC_DEF_PROTOCOL_DVC_DEF_ROMD = 0x0A
        DVC_DEF_PROTOCOL_UNIFYING_V2 = 0x0B  # Never used
        DVC_DEF_PROTOCOL_GAMING = 0x0C
        DVC_DEF_PROTOCOL_GAMING_V2 = 0x0D
        DVC_DEF_PROTOCOL_GAMING_LS2_LLPM = 0x0E
        DVC_DEF_PROTOCOL_GAMING_LS2_CA = 0x0F
        DVC_DEF_PROTOCOL_GAMING_LS2_CA_2 = 0x11
        BLE_PRO = 0x10
    # end class ProtocolTypes

    class LinkStatus:
        LINK_ESTABLISHED = 0x00
        LINK_NOT_ESTABLISHED = 0x01
    # end class LinkStatus

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        PROTOCOL_TYPE = 0xFC
        INFORMATION = 0xFB
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        PROTOCOL_TYPE = 0x08
        INFORMATION_SHORT = 0x18
        INFORMATION_LONG = 0x80
    # end class LEN

    FIELDS = (
        BitField(FID.REPORT_ID,
                 LEN.REPORT_ID,
                 title='ReportID',
                 name='report_id',
                 default_value=Hidpp1Message.DEFAULT.REPORT_ID,
                 checks=(CheckHexList(LEN.REPORT_ID // 8), CheckByte(),)),
        BitField(FID.DEVICE_INDEX,
                 LEN.DEVICE_INDEX,
                 title='DeviceIndex',
                 name='device_index',
                 aliases=('pairing_slot',),
                 checks=(CheckHexList(LEN.DEVICE_INDEX // 8), CheckByte(),)),
        BitField(FID.SUB_ID,
                 LEN.SUB_ID,
                 title='SubID',
                 name='sub_id',
                 checks=(CheckHexList(LEN.SUB_ID // 8), CheckByte(),)),
        BitField(FID.PROTOCOL_TYPE,
                 LEN.PROTOCOL_TYPE,
                 title='ProtocolType',
                 name='protocol_type',
                 checks=(CheckHexList(LEN.PROTOCOL_TYPE // 8), CheckByte(),)),
        BitField(FID.INFORMATION,
                 LEN.INFORMATION_LONG,
                 title='Information',
                 name='information',
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, protocol_type, information):
        """
        Constructor

        @param device_index: Device Index
        @type device_index: int or HexList
        @param protocol_type: The protocol type of the connection
        @type protocol_type: int or HexList
        @param information: The information linked to the protocol type
        @type information: int or list or HexList
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.protocol_type = protocol_type
        self.information = information
    # end def __init__
# end class DeviceConnection


class BluetoothOrQuadReceiverInformation(BitFieldContainerMixin):
    """
    Bitfield structure of Bluetooth or QUAD Receiver Device Connection register.

    This structure is for Protocol type:
    0x01 = Bluetooth
    0x03 = QUAD

    Format:
    || @b Name                                          || @b Bit count ||
    || DeviceInfoManufacturer                           || 1            ||
    || DeviceInfoLinkStatus                             || 1            ||
    || DeviceInfoEncryptionStatus                       || 1            ||
    || DeviceInfoReserved                               || 1            ||
    || DeviceInfoDeviceType                             || 4            ||
    || DeviceCommIDLSB                                  || 8            ||
    || DeviceCommIDMSB                                  || 8            ||
    """
    class FID(object):
        """
        Field Identifiers
        """
        DEVICE_INFO_MANUFACTURER = 0xFF
        DEVICE_INFO_LINK_STATUS = 0xFE
        DEVICE_INFO_ENCRYPTION_STATUS = 0xFD
        DEVICE_INFO_RESERVED = 0xFC
        DEVICE_INFO_DEVICE_TYPE = 0xFB
        DEVICE_COMM_ID_LSB = 0xFA
        DEVICE_COMM_ID_MSB = 0xF9
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        DEVICE_INFO_MANUFACTURER = 0x01
        DEVICE_INFO_LINK_STATUS = 0x01
        DEVICE_INFO_ENCRYPTION_STATUS = 0x01
        DEVICE_INFO_RESERVED = 0x01
        DEVICE_INFO_DEVICE_TYPE = 0x04
        DEVICE_COMM_ID_LSB = 0x08
        DEVICE_COMM_ID_MSB = 0x08
    # end class LEN

    FIELDS = (
        # Write action: SetConfiguration
        BitField(FID.DEVICE_INFO_MANUFACTURER,
                 LEN.DEVICE_INFO_MANUFACTURER,
                 0x00,
                 0x00,
                 title='DeviceInfoManufacturer',
                 name='device_info_manufacturer',
                 checks=(CheckHexList(LEN.DEVICE_INFO_MANUFACTURER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_MANUFACTURER) - 1),)),
        BitField(FID.DEVICE_INFO_LINK_STATUS,
                 LEN.DEVICE_INFO_LINK_STATUS,
                 0x00,
                 0x00,
                 title='DeviceInfoLinkStatus',
                 name='device_info_link_status',
                 checks=(CheckHexList(LEN.DEVICE_INFO_LINK_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_LINK_STATUS) - 1),)),
        BitField(FID.DEVICE_INFO_ENCRYPTION_STATUS,
                 LEN.DEVICE_INFO_ENCRYPTION_STATUS,
                 0x00,
                 0x00,
                 title='DeviceInfoEncryptionStatus',
                 name='device_info_encryption_status',
                 checks=(CheckHexList(LEN.DEVICE_INFO_ENCRYPTION_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_ENCRYPTION_STATUS) - 1),)),
        BitField(FID.DEVICE_INFO_RESERVED,
                 LEN.DEVICE_INFO_RESERVED,
                 0x00,
                 0x00,
                 title='DeviceInfoReserved',
                 name='device_info_reserved',
                 checks=(CheckHexList(LEN.DEVICE_INFO_RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.DEVICE_INFO_DEVICE_TYPE,
                 LEN.DEVICE_INFO_DEVICE_TYPE,
                 0x00,
                 0x00,
                 title='DeviceInfoDeviceType',
                 name='device_info_device_type',
                 checks=(CheckHexList(LEN.DEVICE_INFO_DEVICE_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_DEVICE_TYPE) - 1),)),
        BitField(FID.DEVICE_COMM_ID_LSB,
                 LEN.DEVICE_COMM_ID_LSB,
                 0x00,
                 0x00,
                 title='DeviceCommIDLSB',
                 name='device_comm_id_lsb',
                 checks=(CheckHexList(LEN.DEVICE_COMM_ID_LSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_COMM_ID_LSB) - 1),)),
        BitField(FID.DEVICE_COMM_ID_MSB,
                 LEN.DEVICE_COMM_ID_MSB,
                 0x00,
                 0x00,
                 title='DeviceCommIDMSB',
                 name='device_comm_id_msb',
                 checks=(CheckHexList(LEN.DEVICE_COMM_ID_MSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_COMM_ID_MSB) - 1),)),
    )
# end class BluetoothOrQuadReceiverInformation


class EQuadReceiverInformation(BitFieldContainerMixin):
    """
    Bitfield structure of eQuad Receiver Device Connection register.

    This structure is for Protocol type:
    0x03 = eQUAD
    0x04 = eQuad step 4 DJ
    0x06 = eQuad step 4 Lite
    0x07 = eQuad step 4 gaming (high report-rate gaming mice/keyboard)
    0x08 = eQuad step 4 for gamepads

    Format:
    || @b Name                                          || @b Bit count ||
    || DeviceInfoManufacturer                           || 1            ||
    || DeviceInfoLinkStatus                             || 1            ||
    || DeviceInfoEncryptionStatus                       || 1            ||
    || DeviceInfoSoftwarePresentFlag                    || 1            ||
    || DeviceInfoDeviceType                             || 4            ||
    || DeviceCommIDLSB                                  || 8            ||
    || DeviceCommIDMSB                                  || 8            ||
    """
    class FID(object):
        """
        Field Identifiers
        """
        DEVICE_INFO_MANUFACTURER = 0xFF
        DEVICE_INFO_LINK_STATUS = 0xFE
        DEVICE_INFO_ENCRYPTION_STATUS = 0xFD
        DEVICE_INFO_SOFTWARE_PRESENT_FLAG = 0xFC
        DEVICE_INFO_DEVICE_TYPE = 0xFB
        DEVICE_COMM_ID_LSB = 0xFA
        DEVICE_COMM_ID_MSB = 0xF9
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        DEVICE_INFO_MANUFACTURER = 0x01
        DEVICE_INFO_LINK_STATUS = 0x01
        DEVICE_INFO_ENCRYPTION_STATUS = 0x01
        DEVICE_INFO_SOFTWARE_PRESENT_FLAG = 0x01
        DEVICE_INFO_DEVICE_TYPE = 0x04
        DEVICE_COMM_ID_LSB = 0x08
        DEVICE_COMM_ID_MSB = 0x08
    # end class LEN

    FIELDS = (
        # Write action: SetConfiguration
        BitField(FID.DEVICE_INFO_MANUFACTURER,
                 LEN.DEVICE_INFO_MANUFACTURER,
                 0x00,
                 0x00,
                 title='DeviceInfoManufacturer',
                 name='device_info_manufacturer',
                 checks=(CheckHexList(LEN.DEVICE_INFO_MANUFACTURER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_MANUFACTURER) - 1),)),
        BitField(FID.DEVICE_INFO_LINK_STATUS,
                 LEN.DEVICE_INFO_LINK_STATUS,
                 0x00,
                 0x00,
                 title='DeviceInfoLinkStatus',
                 name='device_info_link_status',
                 checks=(CheckHexList(LEN.DEVICE_INFO_LINK_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_LINK_STATUS) - 1),)),
        BitField(FID.DEVICE_INFO_ENCRYPTION_STATUS,
                 LEN.DEVICE_INFO_ENCRYPTION_STATUS,
                 0x00,
                 0x00,
                 title='DeviceInfoEncryptionStatus',
                 name='device_info_encryption_status',
                 checks=(CheckHexList(LEN.DEVICE_INFO_ENCRYPTION_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_ENCRYPTION_STATUS) - 1),)),
        BitField(FID.DEVICE_INFO_SOFTWARE_PRESENT_FLAG,
                 LEN.DEVICE_INFO_SOFTWARE_PRESENT_FLAG,
                 0x00,
                 0x00,
                 title='DeviceInfoSoftwarePresentFlag',
                 name='device_info_software_present_flag',
                 checks=(CheckHexList(LEN.DEVICE_INFO_SOFTWARE_PRESENT_FLAG // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_SOFTWARE_PRESENT_FLAG) - 1),),
                 default_value=0),
        BitField(FID.DEVICE_INFO_DEVICE_TYPE,
                 LEN.DEVICE_INFO_DEVICE_TYPE,
                 0x00,
                 0x00,
                 title='DeviceInfoDeviceType',
                 name='device_info_device_type',
                 checks=(CheckHexList(LEN.DEVICE_INFO_DEVICE_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_DEVICE_TYPE) - 1),)),
        BitField(FID.DEVICE_COMM_ID_LSB,
                 LEN.DEVICE_COMM_ID_LSB,
                 0x00,
                 0x00,
                 title='DeviceCommIDLSB',
                 name='device_comm_id_lsb',
                 checks=(CheckHexList(LEN.DEVICE_COMM_ID_LSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_COMM_ID_LSB) - 1),)),
        BitField(FID.DEVICE_COMM_ID_MSB,
                 LEN.DEVICE_COMM_ID_MSB,
                 0x00,
                 0x00,
                 title='DeviceCommIDMSB',
                 name='device_comm_id_msb',
                 checks=(CheckHexList(LEN.DEVICE_COMM_ID_MSB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_COMM_ID_MSB) - 1),)),
    )
# end class EQuadReceiverInformation


class BLEProReceiverInformation(BitFieldContainerMixin):
    """
    Bitfield structure of BLE Pro Receiver Device Connection register.

    This structure is for Protocol type:
    0x10 = BLE Pro

    Format:
    || @b Name                                          || @b Bit count ||
    || DeviceInfoReserved1                              || 1            ||
    || DeviceInfoLinkStatus                             || 1            ||
    || DeviceInfoReserved2                              || 2            ||
    || DeviceInfoDeviceType                             || 4            ||
    || Bluetooth PID LSB                                || 8            ||
    || Bluetooth PID MSB                                || 8            ||
    """
    class FID(object):
        """
        Field Identifiers
        """
        DEVICE_INFO_RESERVED1 = 0xFF
        DEVICE_INFO_LINK_STATUS = DEVICE_INFO_RESERVED1 - 1
        DEVICE_INFO_RESERVED2 = DEVICE_INFO_LINK_STATUS - 1
        DEVICE_INFO_DEVICE_TYPE = DEVICE_INFO_RESERVED2 - 1
        BLUETOOTH_PID_LSB = DEVICE_INFO_DEVICE_TYPE - 1
        BLUETOOTH_PID_MSB = BLUETOOTH_PID_LSB - 1
        PADDING = BLUETOOTH_PID_MSB - 1
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        DEVICE_INFO_RESERVED1 = 0x01
        DEVICE_INFO_LINK_STATUS = 0x01
        DEVICE_INFO_RESERVED2 = 0x02
        DEVICE_INFO_DEVICE_TYPE = 0x04
        BLUETOOTH_PID_LSB = 0x08
        BLUETOOTH_PID_MSB = 0x08
        PADDING = 0x65
    # end class LEN

    FIELDS = (
        BitField(FID.DEVICE_INFO_RESERVED1,
                 LEN.DEVICE_INFO_RESERVED1,
                 title='DeviceInfoReserved1',
                 name='device_info_reserved1',
                 checks=(CheckHexList(LEN.DEVICE_INFO_RESERVED1 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_RESERVED1) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.DEVICE_INFO_LINK_STATUS,
                 LEN.DEVICE_INFO_LINK_STATUS,
                 title='DeviceInfoLinkStatus',
                 name='device_info_link_status',
                 checks=(CheckHexList(LEN.DEVICE_INFO_LINK_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_LINK_STATUS) - 1),)),
        BitField(FID.DEVICE_INFO_RESERVED2,
                 LEN.DEVICE_INFO_RESERVED2,
                 title='DeviceInfoReserved2',
                 name='device_info_reserved2',
                 checks=(CheckHexList(LEN.DEVICE_INFO_RESERVED2 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_RESERVED2) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.DEVICE_INFO_DEVICE_TYPE,
                 LEN.DEVICE_INFO_DEVICE_TYPE,
                 title='DeviceInfoDeviceType',
                 name='device_info_device_type',
                 checks=(CheckHexList(LEN.DEVICE_INFO_DEVICE_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_DEVICE_TYPE) - 1),)),
        BitField(FID.BLUETOOTH_PID_LSB,
                 LEN.BLUETOOTH_PID_LSB,
                 title='BluetoothPidLsb',
                 name='bluetooth_pid_lsb',
                 checks=(CheckHexList(LEN.BLUETOOTH_PID_LSB // 8),),
                 aliases=('device_comm_id_lsb', )),
        BitField(FID.BLUETOOTH_PID_MSB,
                 LEN.BLUETOOTH_PID_MSB,
                 title='BluetoothPidMsb',
                 name='bluetooth_pid_msb',
                 checks=(CheckHexList(LEN.BLUETOOTH_PID_MSB // 8),),
                 aliases=('device_comm_id_msb', )),
    )
# end class BLEProReceiverInformation

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
