#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.hidkeyboard
:brief: HID keyboard response interface definition
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


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class HidKeyboard(TimestampedBitFieldContainerMixin):
    """
    Define the common format of an HID Keyboard report.

    Format:

    ================  =========
    Name              Bit count
    ================  =========
    KeyBoard Control  8
    Leds              8
    Key Codes         48
    ================  =========
    """
    MSG_TYPE = 1  # RESPONSE  
    BITFIELD_LENGTH = 8  # Byte

    class FID:
        """
        Field Identifiers
        """
        KEYBOARD_RIGHT_GUI = 0xFF
        KEYBOARD_RIGHT_ALT = 0xFE
        KEYBOARD_RIGHT_SHIFT = 0xFD
        KEYBOARD_RIGHT_CONTROL = 0xFC
        KEYBOARD_LEFT_GUI = 0xFB
        KEYBOARD_LEFT_ALT = 0xFA
        KEYBOARD_LEFT_SHIFT = 0xF9
        KEYBOARD_LEFT_CONTROL = 0xF8
        LEDS = 0xF7
        KEY_CODE1 = 0xF6
        KEY_CODE2 = 0xF5
        KEY_CODE3 = 0xF4
        KEY_CODE4 = 0xF3
        KEY_CODE5 = 0xF2
        KEY_CODE6 = 0xF1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        KEYBOARD_RIGHT_GUI = 0x01
        KEYBOARD_RIGHT_ALT = 0x01
        KEYBOARD_RIGHT_SHIFT = 0x01
        KEYBOARD_RIGHT_CONTROL = 0x01
        KEYBOARD_LEFT_GUI = 0x01
        KEYBOARD_LEFT_ALT = 0x01
        KEYBOARD_LEFT_SHIFT = 0x01
        KEYBOARD_LEFT_CONTROL = 0x01
        LEDS = 0x08
        KEY_CODE1 = 0x08
        KEY_CODE2 = 0x08
        KEY_CODE3 = 0x08
        KEY_CODE4 = 0x08
        KEY_CODE5 = 0x08
        KEY_CODE6 = 0x08
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        RELEASED = 0
        EMPTY = HexList('00')
    # end class DEFAULT

    FIELDS = (BitField(fid=FID.KEYBOARD_LEFT_CONTROL,
                       length=LEN.KEYBOARD_LEFT_CONTROL,
                       title='KeyboardLeftControl',
                       name='keyboard_left_control',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_CONTROL) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_SHIFT,
                       length=LEN.KEYBOARD_LEFT_SHIFT,
                       title='KeyboardLeftShift',
                       name='keyboard_left_shift',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_SHIFT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_ALT,
                       length=LEN.KEYBOARD_LEFT_ALT,
                       title='KeyboardLeftALT',
                       name='keyboard_left_alt',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_ALT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_LEFT_GUI,
                       length=LEN.KEYBOARD_LEFT_GUI,
                       title='KeyboardLeftGUI',
                       name='keyboard_left_gui',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_LEFT_GUI) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_CONTROL,
                       length=LEN.KEYBOARD_RIGHT_CONTROL,
                       title='KeyboardRightControl',
                       name='keyboard_right_control',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_CONTROL) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_SHIFT,
                       length=LEN.KEYBOARD_RIGHT_SHIFT,
                       title='KeyboardRightShift',
                       name='keyboard_right_shift',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_SHIFT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_ALT,
                       length=LEN.KEYBOARD_RIGHT_ALT,
                       title='KeyboardRightALT',
                       name='keyboard_right_alt',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_ALT) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEYBOARD_RIGHT_GUI,
                       length=LEN.KEYBOARD_RIGHT_GUI,
                       title='KeyboardRightGUI',
                       name='keyboard_right_gui',
                       checks=(CheckInt(0, pow(2, LEN.KEYBOARD_RIGHT_GUI) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(FID.LEDS,
                       LEN.LEDS,
                       title='Leds',
                       name='leds',
                       checks=(CheckHexList(LEN.LEDS // 8), CheckByte(),),
                       default_value=DEFAULT.EMPTY),
              BitField(FID.KEY_CODE1,
                       LEN.KEY_CODE1,
                       title='Key Code 1',
                       name='key_code1',
                       checks=(CheckHexList(LEN.KEY_CODE1 // 8), CheckByte(),),
                       default_value=DEFAULT.EMPTY),
              BitField(FID.KEY_CODE2,
                       LEN.KEY_CODE2,
                       title='Key Code 2',
                       name='key_code2',
                       checks=(CheckHexList(LEN.KEY_CODE2 // 8), CheckByte(),),
                       default_value=DEFAULT.EMPTY),
              BitField(FID.KEY_CODE3,
                       LEN.KEY_CODE3,
                       title='Key Code 3',
                       name='key_code3',
                       checks=(CheckHexList(LEN.KEY_CODE3 // 8), CheckByte(),),
                       default_value=DEFAULT.EMPTY),
              BitField(FID.KEY_CODE4,
                       LEN.KEY_CODE4,
                       title='Key Code 4',
                       name='key_code4',
                       checks=(CheckHexList(LEN.KEY_CODE4 // 8), CheckByte(),),
                       default_value=DEFAULT.EMPTY),
              BitField(FID.KEY_CODE5,
                       LEN.KEY_CODE5,
                       title='Key Code 5',
                       name='key_code5',
                       checks=(CheckHexList(LEN.KEY_CODE5 // 8), CheckByte(),),
                       default_value=DEFAULT.EMPTY),
              BitField(FID.KEY_CODE6,
                       LEN.KEY_CODE6,
                       title='Key Code 6',
                       name='key_code6',
                       checks=(CheckHexList(LEN.KEY_CODE6 // 8), CheckByte(),),
                       default_value=DEFAULT.EMPTY),
              )

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional arguments.
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(*args, **kwargs)
    # end def __init__

    def __eq__(self, other):
        """
        Test the equality of HidppMessage with other.

        :param other: Other HidConsumer instance
        :type other: ``HidKeyboard``

        :return: Comparison result
        :rtype: ``bool``

        :raise ``TypeError``: If other has not the right type
        """
        if not isinstance(other, HidKeyboard):
            raise TypeError("Other should be of type HidKeyboard")
        # end if

        result = (self.SUB_ID == other.SUB_ID)

        if result:
            result = super(HidKeyboard, self).__eq__(other)
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        """
        Test the difference between HidppMessage and other.

        :param other: Other HidConsumer instance
        :type other: ``HidKeyboard``

        :return: Comparison result
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

# end class HidKeyboard

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
