#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidppmessage
    :brief: HID++ 2.0 command interface definition
    :author: Christophe Roquebert
    :date: 2018/12/12
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TYPE(object):
    """
    HID++ message type
    """
    REQUEST = 0
    RESPONSE = 1
    EVENT = 2
# end class TYPE


class HidppMessage(TimestampedBitFieldContainerMixin):
    """
    This class defines the common format of all HID commands.
    
    The HID++ system extends the HID system by borrowing its transport layer 
    to route vendor messages to some specified HID vendor collections. 
    In short, HID++ collections are Logitech HID vendor collections that 
    satisfy some criteria. 
    The principal one concerns the size of the HID++ messages: 
    they can be short, long, or very long. 
    
    Find here the generic format of a HID++ message.
    Message format:           ReportID.DeviceIndex.payload

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           || short msg
                           or || 128          || long msg
                           or || 480          || very long msg
    """
    FEATURE_ID = None
    MSG_TYPE = TYPE.REQUEST
    VERSION = None

    # Message sizes
    SHORT_MSG_SIZE = 7
    LONG_MSG_SIZE = 20
    VERY_LONG_MSG_SIZE = 64

    # Header field : ReportID, DeviceIndex, FeatureIndex, FunctionID, softwareID -> 4 bytes
    HEADER_SIZE = 4
    
    class FID(object):
        """
        Field Identifiers
        """
        REPORT_ID = 0xFF
        DEVICE_INDEX = 0xFE
        FEATURE_INDEX = 0xFD
        FUNCTION_ID = 0xFC
        SOFTWARE_ID = 0xFB
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        REPORT_ID = 0x08
        DEVICE_INDEX = 0x08
        FEATURE_INDEX = 0x08
        FUNCTION_ID = 0x04
        SOFTWARE_ID = 0x04
    # end class LEN

    class OFFSET(object):
        """
        Field offset in bytes
        """
        REPORT_ID = 0x00
        DEVICE_INDEX = 0x01
        FEATURE_INDEX = 0x02
        FUNCTION_ID = 0x03
        SOFTWARE_ID = 0x03
    # end class OFFSET

    class DEFAULT(object):
        """
        Fields Default values
        """
        REPORT_ID_SHORT = 0x10  # Short message
        REPORT_ID_LONG = 0x11  # Long message
        REPORT_ID_VERY_LONG = 0x12  # Very long message
        REPORT_ID = REPORT_ID_SHORT
        SOFTWARE_ID = 0xF  # Test value
        PADDING = 0x00
        RESERVED = 0x00
    # end class DEFAULT

    HIDPP_REPORT_ID_LIST = [DEFAULT.REPORT_ID_SHORT, DEFAULT.REPORT_ID_LONG, DEFAULT.REPORT_ID_VERY_LONG]
    HIDPP_REPORT_LEN_LIST = [SHORT_MSG_SIZE, LONG_MSG_SIZE, VERY_LONG_MSG_SIZE]
    
    FIELDS = (BitField(FID.REPORT_ID,
                       LEN.REPORT_ID,
                       0x00,
                       0x00,
                       title='Report ID',
                       name='report_id',
                       aliases=('reportId',),
                       default_value=DEFAULT.REPORT_ID,
                       checks=(CheckHexList(LEN.REPORT_ID // 8), CheckByte(),)),
              BitField(FID.DEVICE_INDEX,
                       LEN.DEVICE_INDEX,
                       0x00,
                       0x00,
                       title='Device Index',
                       name='device_index',
                       aliases=('deviceIndex',),
                       checks=(CheckHexList(LEN.DEVICE_INDEX // 8), CheckByte(),)),
              BitField(FID.FEATURE_INDEX,
                       LEN.FEATURE_INDEX,
                       0x00,
                       0x00,
                       title='Feature Index',
                       name='feature_index',
                       aliases=('featureIndex',),
                       checks=(CheckHexList(LEN.FEATURE_INDEX // 8), CheckByte(),)),
              BitField(FID.FUNCTION_ID,
                       LEN.FUNCTION_ID,
                       0x00,
                       0x00,
                       title='Function Index',
                       name='function_index',
                       aliases=('functionIndex',),
                       checks=(CheckInt(0, pow(2, LEN.FUNCTION_ID) - 1),)),
              BitField(FID.SOFTWARE_ID,
                       LEN.SOFTWARE_ID,
                       0x00,
                       0x00,
                       title='Software Id',
                       name='software_id',
                       aliases=('softwareId',),
                       default_value=DEFAULT.SOFTWARE_ID,
                       checks=(CheckInt(0, pow(2, LEN.SOFTWARE_ID) - 1),)),
              )

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional Parameters
        :type args: ``object``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``object``
        """
        assert (self.FEATURE_ID is not None), \
            ValueError('%s must define HidppMessage.FEATURE_ID at class level' 
                       % self.__class__.__name__)
        assert (len(args) == 0), \
            ValueError('%s must not call its parent constructor with a FEATURE_ID any'
                       ' more.' % self.__class__.__name__)

        if 'mode' in kwargs:
            self.MODE = kwargs['mode']                                          # pylint:disable=C0103
            del kwargs['mode']
        # end if

        super(HidppMessage, self).__init__(*args, **kwargs)
        
        self.messageLength = None
    # end def __init__

    def __eq__(self, other):
        """
        Tests the equality of HidppMessage with the other.

        @param  other  [in] (HidppMessage) Other HidppMessage instance

        @return (bool) Comparison result
        """
        if not isinstance(other, HidppMessage):
            raise TypeError("Other should be of type HidppMessage")
        # end if

        result = (self.FEATURE_ID == other.FEATURE_ID)

        if result:
            result = super(HidppMessage, self).__eq__(other)
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        """
        Tests the difference between HidppMessage and other.

        @param  other  [in] (HidppMessage) Other HidppMessage instance

        @return (bool) Comparison result
        """
        return self != other
    # end def __ne__
# end class HidppMessage


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
