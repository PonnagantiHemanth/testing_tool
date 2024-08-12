#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.requestdisplaypasskey
    :brief: HID++ 1.0 Request to display passkey notification definition
    :author: Christophe Roquebert
    :date: 2020/03/09
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


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class RequestDisplayPassKey(Hidpp1Message):
    """
    This class defines the format of Device Connection event.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SUB ID                 || 8            ||
    || PassKey Length (6)     || 8            ||
    || PassKey Digit          || 48           ||
    || Bluetooth Address      || 48           ||
    || Pading                 || 24           ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.REQUEST_DISPLAY_PASSKEY
    BINARY_PASSKEY_IN_BITS = 20
    PASSKEY_IN_DIGITS = 6

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        PASSKEY_LENGTH = Hidpp1Message.FID.SUB_ID - 1
        PASSKEY_DIGITS = PASSKEY_LENGTH - 1
        BLUETOOTH_ADDRESS = PASSKEY_DIGITS - 1
        PADDING = BLUETOOTH_ADDRESS - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        PASSKEY_LENGTH = 0x08
        PASSKEY_DIGITS = 0x30
        BLUETOOTH_ADDRESS = 0x30
        PADDING = 0x20
    # end class LEN

    class DEFAULT(Hidpp1Message.DEFAULT):
        """
        Fields Default values
        """
        PASSKEY_LENGTH = 0x06
    # end class DEFAULT

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.PASSKEY_LENGTH,
                 LEN.PASSKEY_LENGTH,
                 title='PasskeyLength',
                 name='passkey_length',
                 checks=(CheckHexList(LEN.PASSKEY_LENGTH // 8), CheckByte(),),
                 default_value=DEFAULT.PASSKEY_LENGTH),
        BitField(FID.PASSKEY_DIGITS,
                 LEN.PASSKEY_DIGITS,
                 title='PasskeyDigits',
                 name='passkey_digits',
                 checks=(CheckHexList(LEN.PASSKEY_DIGITS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PASSKEY_DIGITS) - 1),), ),
        BitField(FID.BLUETOOTH_ADDRESS,
                 LEN.BLUETOOTH_ADDRESS,
                 title='BluetoothAddress',
                 name='bluetooth_address',
                 checks=(CheckHexList(LEN.BLUETOOTH_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BLUETOOTH_ADDRESS) - 1),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=DEFAULT.PADDING),
    )

    def __init__(self, device_index, passkey_length, passkey_digits, bluetooth_address):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param passkey_length: The protocol type of the connection
        :type passkey_length: ``int or HexList``
        :param passkey_digits: The information linked to the protocol type
        :type passkey_digits: ``int or list or HexList``
        :param bluetooth_address: The bluetooth address
        :type bluetooth_address: ``int or list or HexList``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.passkey_length = passkey_length
        self.passkey_digits = passkey_digits
        self.bluetooth_address = bluetooth_address
    # end def __init__
# end class RequestDisplayPassKey

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
