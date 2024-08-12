#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.hidconsumer
:brief: HID consumer page response interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/03/17
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class HidConsumer(TimestampedBitFieldContainerMixin):  # pylint:disable=W0223
    """
    Define the USB HID Consumer Page report.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    Key 1        16
    Key 2        16
    ===========  =========
    """
    MSG_TYPE = 1  # RESPONSE
    BITFIELD_LENGTH = 4  # Byte

    class FID:
        """
        Field Identifiers
        """
        KEY_1 = 0xFF
        KEY_2 = 0xFE
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        KEY_1 = 0x10
        KEY_2 = 0x10
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        RELEASED = HexList("0000")
    # end class DEFAULT

    FIELDS = (BitField(fid=FID.KEY_1,
                       length=LEN.KEY_1,
                       title='Key 1',
                       name='key_1',
                       checks=(CheckHexList(LEN.KEY_1 // 8),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.KEY_2,
                       length=LEN.KEY_2,
                       title='Key 2',
                       name='key_2',
                       checks=(CheckHexList(LEN.KEY_2 // 8),),
                       default_value=DEFAULT.RELEASED),
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
        Test the equality of this ``HidConsumer`` instance with other.

        :param other: Other ``HidConsumer`` instance
        :type other: ``HidConsumer``

        :return: Comparison result
        :rtype: ``bool``

        :raise ``TypeError``: If other has not the right type
        """
        if not isinstance(other, HidConsumer):
            raise TypeError("Other should be of type HidConsumer")
        # end if

        result = (self.SUB_ID == other.SUB_ID)

        if result:
            result = super().__eq__(other)
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        """
        Test the difference between this ``HidConsumer`` instance and other.

        :param  other: Other ``HidConsumer`` instance
        :type other: ``HidConsumer``

        :return: Comparison result
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

    def is_key_empty(self, slot=1):
        """
        Test if a key slot is free

        :param slot: key slot in range [1..2] - OPTIONAL
        :type slot: ``int``

        :return: True if the 2 bytes value is equal to 0x0000, False otherwise
        :rtype: ``bool``
        """
        assert slot in [1, 2], f'Wrong provided key slot {slot}'

        if slot == 1:
            return self.key_1 == self.DEFAULT.RELEASED
        else:
            return self.key_2 == self.DEFAULT.RELEASED
        # end if
    # end def is_key_empty
# end class HidConsumer

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
