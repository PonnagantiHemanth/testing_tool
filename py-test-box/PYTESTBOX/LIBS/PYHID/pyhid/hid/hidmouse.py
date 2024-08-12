#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.hidmouse
:brief: HID mouse response interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/01/31
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class HidMouse(TimestampedBitFieldContainerMixin):
    """
    Define the common format of an HID mouse report.

    Format:

    ================  =========
    Name              Bit count
    ================  =========
    Button x          16
    X Delta           16
    Y Delta           16
    Wheel             8
    AC Pan            8
    ================  =========
    """
    MSG_TYPE = 1  # RESPONSE
    BITFIELD_LENGTH = 8  # Bytes

    class FID:
        """
        Field Identifiers
        """
        BUTTON1 = 0xFF
        BUTTON2 = 0xFE
        BUTTON3 = 0xFD
        BUTTON4 = 0xFC
        BUTTON5 = 0xFB
        BUTTON6 = 0xFA
        BUTTON7 = 0xF9
        BUTTON8 = 0xF8
        BUTTON9 = 0xF7
        BUTTON10 = 0xF6
        BUTTON11 = 0xF5
        BUTTON12 = 0xF4
        BUTTON13 = 0xF3
        BUTTON14 = 0xF2
        BUTTON15 = 0xF1
        BUTTON16 = 0xF0
        X_POS = 0xEF
        Y_POS = 0xEE
        WHEEL = 0xED
        AC_PAN = 0xEC
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        BUTTON1 = 0x01
        BUTTON2 = 0x01
        BUTTON3 = 0x01
        BUTTON4 = 0x01
        BUTTON5 = 0x01
        BUTTON6 = 0x01
        BUTTON7 = 0x01
        BUTTON8 = 0x01
        BUTTON9 = 0x01
        BUTTON10 = 0x01
        BUTTON11 = 0x01
        BUTTON12 = 0x01
        BUTTON13 = 0x01
        BUTTON14 = 0x01
        BUTTON15 = 0x01
        BUTTON16 = 0x01
        X_POS = 0x10
        Y_POS = 0x10
        WHEEL = 0x08
        AC_PAN = 0x08
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        RELEASED = 0
        NULL_POS = HexList('0000')
        NULL_BYTE = HexList('00')
    # end class DEFAULT

    FIELDS = (BitField(FID.BUTTON1,
                       LEN.BUTTON1,
                       title='Button1',
                       name='button1',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON1) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON2,
                       LEN.BUTTON2,
                       title='Button2',
                       name='button2',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON2) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON3,
                       LEN.BUTTON3,
                       title='Button3',
                       name='button3',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON3) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON4,
                       LEN.BUTTON4,
                       title='Button4',
                       name='button4',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON4) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON5,
                       LEN.BUTTON5,
                       title='Button5',
                       name='button5',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON5) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON6,
                       LEN.BUTTON6,
                       title='Button6',
                       name='button6',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON6) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON7,
                       LEN.BUTTON7,
                       title='Button7',
                       name='button7',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON7) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON8,
                       LEN.BUTTON8,
                       title='Button8',
                       name='button8',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON8) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON9,
                       LEN.BUTTON9,
                       title='Button9',
                       name='button9',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON9) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON10,
                       LEN.BUTTON10,
                       title='Button10',
                       name='button10',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON10) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON11,
                       LEN.BUTTON11,
                       title='Button11',
                       name='button11',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON11) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON12,
                       LEN.BUTTON12,
                       title='Button12',
                       name='button12',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON12) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON13,
                       LEN.BUTTON13,
                       title='Button13',
                       name='button13',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON13) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON14,
                       LEN.BUTTON14,
                       title='Button14',
                       name='button14',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON14) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON15,
                       LEN.BUTTON15,
                       title='Button15',
                       name='button15',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON15) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.BUTTON16,
                       LEN.BUTTON16,
                       title='Button16',
                       name='button16',
                       checks=(CheckInt(0, pow(2, LEN.BUTTON16) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.X_POS,
                       LEN.X_POS,
                       title='X position',
                       name='x',
                       checks=(CheckHexList(LEN.X_POS // 8),
                               CheckInt(max_value=0xFFFF),),
                       default_value=DEFAULT.NULL_POS),
              BitField(FID.Y_POS,
                       LEN.Y_POS,
                       title='Y position',
                       name='y',
                       checks=(CheckHexList(LEN.Y_POS // 8),
                               CheckInt(max_value=0xFFFF),),
                       default_value=DEFAULT.NULL_POS),
              BitField(FID.WHEEL,
                       LEN.WHEEL,
                       title='Wheel',
                       name='wheel',
                       checks=(CheckHexList(LEN.WHEEL // 8),
                               CheckByte(),),
                       default_value=DEFAULT.NULL_BYTE),
              BitField(FID.AC_PAN,
                       LEN.AC_PAN,
                       title='AC Pan',
                       name='ac_pan',
                       checks=(CheckHexList(LEN.AC_PAN // 8),
                               CheckByte(),),
                       default_value=DEFAULT.NULL_BYTE),
              )

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional arguments.
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(*args, **kwargs)
        self.timestamp = None
    # end def __init__

    def __eq__(self, other):
        """
        Test the equality of this ``HidMouse`` instance with other.

        :param other: Other ``HidMouse`` instance
        :type other: ``HidMouse``

        :return: Comparison result
        :rtype: ``bool``
        """
        if not isinstance(other, HidMouse):
            raise TypeError("Other should be of type HidMouse")
        # end if

        result = (self.SUB_ID == other.SUB_ID)

        if result:
            result = super(HidMouse, self).__eq__(other)
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        """
        Test the difference between this ``HidMouse`` instance and other.

        :param other: Other ``HidMouse`` instance
        :type other: ``HidMouse``

        :return: Comparison result
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

    def get_absolute_value(self, fid, use_default_value=True):
        """
        Get the field value for a given FID.

        :param fid: Field Identifier
        :type fid: ``int``
        :param use_default_value: The default value to use if no value is supplied - OPTIONAL
        :type use_default_value: ``bool``

        :return: The value or default value of the field.
        :rtype: ``int``
        """
        result = int(Numeral(super(HidMouse, self).getValue(fid, use_default_value)))

        if (fid == HidMouse.FID.X_POS or
           fid == HidMouse.FID.Y_POS):
            offset = 16
            if fid == HidMouse.FID.Y_POS:
                offset = 17
            # end if
            field_length = self.FIELDS[offset].length
            if result >= pow(2, (field_length - 1)):
                result = result - pow(2, field_length)
            # end if
        # end if

        return result
    # end def get_absolute_value
# end class HidMouse


class HidMouseNvidiaExtension(HidMouse):
    """
    Define the common format of an HID mouse report with the Nvidia extension.

    Format:

    ================  =========
    Name              Bit count
    ================  =========
    Button x          16
    X Delta           16
    Y Delta           16
    Wheel             8
    AC Pan            8
    Nvidia Extension  40
    ================  =========
    """
    BITFIELD_LENGTH = 13  # Bytes

    class FID(HidMouse.FID):
        # See ``HidMouse.FID``
        EXTENSION_ID = HidMouse.FID.AC_PAN - 1
        DELTA_TIME = EXTENSION_ID - 1
        RESERVED = DELTA_TIME - 1
    # end class FID

    class LEN(HidMouse.LEN):
        # See ``HidMouse.LEN``
        EXTENSION_ID = 0x8
        DELTA_TIME = 0x10
        RESERVED = 0x10
    # end class LEN

    class DEFAULT(HidMouse.DEFAULT):
        # See ``HidMouse.DEFAULT``
        PADDING = 0x0
        EXT_ID_LATENCY = 0x3
        INVALID_WIRED_LATENCY = 0xFF7F
    # end class DEFAULT

    FIELDS = HidMouse.FIELDS + (
        BitField(FID.EXTENSION_ID,
                 LEN.EXTENSION_ID,
                 title='ExtensionId',
                 name='extension_id',
                 checks=(CheckHexList(LEN.EXTENSION_ID // 8), CheckByte(),),
                 default_value=DEFAULT.EXT_ID_LATENCY),
        BitField(FID.DELTA_TIME,
                 LEN.DELTA_TIME,
                 title='DeltaTime',
                 name='delta_time',
                 checks=(CheckHexList(LEN.DELTA_TIME // 8), CheckInt(min_value=0, max_value=pow(2, LEN.DELTA_TIME) - 1),),
                 default_value=DEFAULT.PADDING),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=DEFAULT.PADDING),
    )

    def __eq__(self, other):
        # Ignore the fields linked to the NVIDIA extension
        # and compare only the generic HID Mouse fields
        for field in HidMouse.FIELDS:
            field_value = self.getValue(field.getFid())
            other_value = other.getValue(field.getFid())
            if field_value != other_value:
                return False
            # end if
        # end for

        return True
    # end def __eq__
# end class HidMouseNvidiaExtension

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
