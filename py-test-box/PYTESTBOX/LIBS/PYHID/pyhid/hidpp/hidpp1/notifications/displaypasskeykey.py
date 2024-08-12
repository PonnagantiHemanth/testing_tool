#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.displaypasskeykey
    :brief: HID++ 1.0 Display passkey key notification definition
    :author: Christophe Roquebert
    :date: 2020/03/16
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
class DisplayPassKeyKey(Hidpp1Message):
    """
    This class defines the format of Device Connection event.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SUB ID                 || 8            ||
    || KeyCode                || 8            ||
    || Padding                || 128          ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.DISPLAY_PASSKEY_KEY

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        KEY_CODE = Hidpp1Message.FID.SUB_ID - 1
        BLUETOOTH_ADDRESS = KEY_CODE - 1
        PADDING = BLUETOOTH_ADDRESS - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        KEY_CODE = 0x08
        BLUETOOTH_ADDRESS = 0x30
        PADDING = 0x50
    # end class LEN

    class KEY_CODE():
        """
        Key Code meaning
        """
        PASSKEY_ENTRY_STARTED = 0x00
        PASSKEY_DIGIT_ENTERED = 0x01
        PASSKEY_DIGIT_ERASED = 0x02
        PASSKEY_CLEARED = 0x03
        PASSKEY_ENTRY_COMPLETED = 0x04
    # end class KEY_CODE

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.KEY_CODE,
                 LEN.KEY_CODE,
                 title='KeyCode',
                 name='key_code',
                 checks=(CheckHexList(LEN.KEY_CODE // 8), CheckByte(),),),
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
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, key_code, bluetooth_address):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param key_code: Passkey state
        :type key_code: ``int or HexList``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.key_code = key_code
        self.bluetooth_address = bluetooth_address
    # end def __init__

# end class DisplayPassKeyKey

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
