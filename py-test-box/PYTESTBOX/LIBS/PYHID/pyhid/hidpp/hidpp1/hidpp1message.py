#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.Hidpp1Message

@brief  HID++ 1.0 command Receiver Notification Event interface definition

@author Stanislas Cottard

@date   2019/08/14
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Hidpp1Message(TimestampedBitFieldContainerMixin):
    """
    This class defines the common format of all HID++1 messages.

    Since it is a HID++ message, find here the generic format of a HID++ message.
    Message format:           ReportID.SubID.payload

    The HID++ system extends the HID system by borrowing its transport layer
    to route vendor messages to some specified HID vendor collections.
    In short, HID++ collections are Logitech HID vendor collections that
    satisfy some criteria.
    The principal one concerns the size of the HID++ messages:
    they can be short, long, or very long.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SubID                  || 8            ||
    || FeatureIndex           || 8            ||
    || Params                 || 32           || short msg
                           or || 136          || long msg
                           or || 488          || very long msg
    """
    SUB_ID = None

    # Message sizes
    SHORT_MSG_SIZE = 7
    LONG_MSG_SIZE = 20
    VERY_LONG_MSG_SIZE = 64

    # Header field : ReportID, DeviceIndex, FeatureIndex -> 3 bytes
    HEADER_SIZE = 3
    
    class FID(object):
        """
        Field Identifiers
        """
        REPORT_ID = 0xFF
        DEVICE_INDEX = 0xFE
        SUB_ID = 0xFD
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        REPORT_ID = 0x08
        DEVICE_INDEX = 0x08
        SUB_ID = 0x08
    # end class LEN

    class OFFSET(object):
        """
        Field offset in bytes
        """
        REPORT_ID = 0x00
        DEVICE_INDEX = 0x01
        SUB_ID = 0x02
    # end class OFFSET

    class DEFAULT(object):
        """
        Fields Default values
        """
        REPORT_ID_SHORT = 0x10  # Short message
        REPORT_ID_LONG = 0x11  # Long message
        REPORT_ID_VERY_LONG = 0x12  # Very long message
        REPORT_ID = REPORT_ID_SHORT
        DEVICE_INDEX = 0xFF
        PADDING = 0x00
        RESERVED = PADDING
    # end class DEFAULT

    FIELDS = (BitField(FID.REPORT_ID,
                       LEN.REPORT_ID,
                       title='ReportID',
                       name='report_id',
                       aliases=('reportId',),
                       default_value=DEFAULT.REPORT_ID,
                       checks=(CheckHexList(LEN.REPORT_ID // 8), CheckByte(),)),
              BitField(FID.DEVICE_INDEX,
                       LEN.DEVICE_INDEX,
                       title='DeviceIndex',
                       name='device_index',
                       aliases=('deviceIndex',),
                       checks=(CheckHexList(LEN.DEVICE_INDEX // 8), CheckByte(),)),
              BitField(FID.SUB_ID,
                       LEN.SUB_ID,
                       title='SubID',
                       name='sub_id',
                       checks=(CheckHexList(LEN.SUB_ID // 8), CheckByte(),)),
              )

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        @param args: Positional arguments
        @type args: tuple
        @param kwargs: Keyword arguments
        @type kwargs: dict
        """
        assert (self.SUB_ID is not None), \
            ValueError('%s must define Hidpp1Message.SUB_ID at class level'
                       % self.__class__.__name__)
        assert (len(args) == 0), \
            ValueError('%s must not call its parent constructor with a SUB_ID any'
                       ' more.' % self.__class__.__name__)

        if 'mode' in kwargs:
            self.MODE = kwargs['mode']
            del kwargs['mode']
        # end if

        super(Hidpp1Message, self).__init__(*args, **kwargs)
        
        self.messageLength = None
    # end def __init__

    def __eq__(self, other):
        """
        Tests the equality of Hidpp1Message with other.

        @param other: Other Hidpp1Message instance
        @type other: Hidpp1Message

        @return: Comparison result
        @rtype: bool
        """
        if not isinstance(other, Hidpp1Message):
            raise TypeError("Other should be of type Hidpp1Message")
        # end if

        result = (self.SUB_ID == other.SUB_ID)

        if result:
            result = super(Hidpp1Message, self).__eq__(other)
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        """
        Tests the difference between Hidpp1Message and other.

        @param other: Other Hidpp1Message instance
        @type other: Hidpp1Message

        @return: Comparison result
        @rtype: bool
        """
        return not (self == other)
    # end def __ne__
# end class Hidpp1Message

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
