#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.pairingstatus
    :brief: HID++ 1.0 Pairing Status event interface definition
    :author: Christophe Roquebert
    :date: 2020/04/08
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
from pylibrary.tools.hexlist import HexList, RandHexList
from pylibrary.tools.numeral import Numeral
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingStatus(Hidpp1Message):
    """
    This class defines the format of Pairing Status event.

    This notification is used to indicate the status of the pairing process.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SUB ID                 || 8            ||
    || Device Pairing Status  || 8            ||
    || Error Type             || 8            ||
    || Bluetooth Address      || 48           ||
    || Pairing Slot           || 8            ||
    || Padding                || 64           ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.PAIRING_STATUS


    class STATUS():
        """
        Device Pairing notification status
        """
        PAIRING_START = 0x00
        PAIRING_CANCEL =  0x01
        PAIRING_STOP =  0x02
    # end class STATUS


    class ERROR_TYPE():
        """
        Device Pairing notification error types
        """
        NO_ERROR = 0x00
        TIMEOUT = 0x01
        FAILED = 0x02
        RESERVED = [0x03, 0xFF]  # Other values
    # end class ERROR_TYPE


    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        DEVICE_PAIRING_STATUS = Hidpp1Message.FID.SUB_ID - 1
        ERROR_TYPE = DEVICE_PAIRING_STATUS - 1
        BLUETOOTH_ADDRESS = ERROR_TYPE - 1
        PAIRING_SLOT = BLUETOOTH_ADDRESS - 1
        PADDING = PAIRING_SLOT - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        DEVICE_PAIRING_STATUS = 0x08
        ERROR_TYPE = 0x08
        BLUETOOTH_ADDRESS = 0x30
        PAIRING_SLOT = 0x08
        PADDING = 0x40
    # end class LEN

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.DEVICE_PAIRING_STATUS,
                 LEN.DEVICE_PAIRING_STATUS,
                 title='DevicePairingStatus',
                 name='device_pairing_status',
                 checks=(CheckHexList(LEN.DEVICE_PAIRING_STATUS // 8), CheckByte(),),),
        BitField(FID.ERROR_TYPE,
                 LEN.ERROR_TYPE,
                 title='ErrorType',
                 name='error_type',
                 checks=(CheckHexList(LEN.ERROR_TYPE // 8), CheckByte(),),),
        BitField(FID.BLUETOOTH_ADDRESS,
                 LEN.BLUETOOTH_ADDRESS,
                 title    = 'BluetoothAddress',
                 name     = 'bluetooth_address',
                 checks   = (CheckHexList(LEN.BLUETOOTH_ADDRESS // 8),)),
        BitField(FID.PAIRING_SLOT,
                 LEN.PAIRING_SLOT,
                 title='PairingSlot',
                 name='pairing_slot',
                 checks   = (CheckHexList(LEN.PAIRING_SLOT // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index,
                 device_pairing_status=STATUS.PAIRING_START,
                 error_type=ERROR_TYPE.NO_ERROR,
                 bluetooth_address=RandHexList(LEN.BLUETOOTH_ADDRESS//8),
                 pairing_slot=0):
        """
        Constructor

        :param device_index: Device index
        :type device_index: ``int or HexList``
        :param device_pairing_status: Device Pairing Status
        :type device_pairing_status: ``int or HexList``
        :param error_type: Error Type
        :type error_type: ``int``
        :param bluetooth_address: Bluetooth Address  (LSB first)
        :type bluetooth_address: ``HexList``
        :param pairing_slot: Pairing Slot
        :type pairing_slot: ``int or HexList``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.device_pairing_status = device_pairing_status
        self.error_type = error_type
        self.bluetooth_address = bluetooth_address
        self.pairing_slot = pairing_slot
    # end def __init__
# end class PairingStatus

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
