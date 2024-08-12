#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.common.uniqueidentifier32bytes

@brief  HID++ 2.0 32 Bytes Unique Identifier command interface definition

@author Stanislas Cottard

@date   2019/10/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class UniqueIdentifier32Bytes(HidppMessage):
    """
    32 Bytes Unique Identifier implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x0021
    MAX_FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index: Device Index
        @type device_index: int or HexList
        @param  feature_index: feature Index
        @type feature_index: int or HexList
        """
        super(UniqueIdentifier32Bytes, self).__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class UniqueIdentifier32Bytes


class GetByte0To15(UniqueIdentifier32Bytes):
    """
    UniqueIdentifier32Bytes GetByte0To15 implementation class

    Request the bytes 0 to 15 of the unique identifier.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(UniqueIdentifier32Bytes.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(UniqueIdentifier32Bytes.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = UniqueIdentifier32Bytes.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UniqueIdentifier32Bytes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index: Device Index
        @type device_index: int or HexList
        @param  feature_index: feature Index
        @type feature_index: int or HexList
        """
        super(GetByte0To15, self).__init__(device_index, feature_index)

        self.functionIndex = GetByte0To15Response.FUNCTION_INDEX
    # end def __init__
# end class GetByte0To15


class GetByte0To15Response(UniqueIdentifier32Bytes):
    """
    UniqueIdentifier32Bytes GetByte0To15 response implementation class

    Returns the bytes 0 to 15 of the unique identifier.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || Bytes0To15              || 128          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetByte0To15,)
    FUNCTION_INDEX = 0
    VERSION = (1,)

    class FID(UniqueIdentifier32Bytes.FID):
        """
        Field Identifiers
        """
        BYTES_0_TO_15 = 0xFA
    # end class FID

    class LEN(UniqueIdentifier32Bytes.LEN):
        """
        Field Lengths
        """
        BYTES_0_TO_15 = 0x80
    # end class LEN

    FIELDS = UniqueIdentifier32Bytes.FIELDS + (
        BitField(FID.BYTES_0_TO_15,
                 LEN.BYTES_0_TO_15,
                 0x00,
                 0x00,
                 title='Bytes0To15',
                 name='bytes_0_to_15',
                 checks=(CheckHexList(LEN.BYTES_0_TO_15 // 8), CheckByte())),
    )

    def __init__(self, device_index, feature_index, bytes_0_to_15):
        """
        Constructor

        @param  device_index: Device Index
        @type device_index: int or HexList
        @param  feature_index: feature Index
        @type feature_index: int or HexList
        @param  bytes_0_to_15: The bytes 0 to 15 of the unique identifier
        @type bytes_0_to_15: int or HexList
        """
        super(GetByte0To15Response, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.bytes_0_to_15 = bytes_0_to_15
    # end def __init__
# end class GetByte0To15Response


class GetByte16To31(UniqueIdentifier32Bytes):
    """
    UniqueIdentifier32Bytes GetByte16To31 implementation class

    Request the bytes 16 to 31 of the unique identifier.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(UniqueIdentifier32Bytes.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(UniqueIdentifier32Bytes.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = UniqueIdentifier32Bytes.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UniqueIdentifier32Bytes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index: Device Index
        @type device_index: int or HexList
        @param  feature_index: feature Index
        @type feature_index: int or HexList
        """
        super(GetByte16To31, self).__init__(device_index, feature_index)

        self.functionIndex = GetByte16To31Response.FUNCTION_INDEX
    # end def __init__
# end class GetByte16To31


class GetByte16To31Response(UniqueIdentifier32Bytes):
    """
    UniqueIdentifier32Bytes GetByte16To31 response implementation class

    Returns the bytes 16 to 31 of the unique identifier.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || Bytes16To31             || 128          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetByte16To31,)
    FUNCTION_INDEX = 1
    VERSION = (1,)

    class FID(UniqueIdentifier32Bytes.FID):
        """
        Field Identifiers
        """
        BYTES_16_TO_31 = 0xFA
    # end class FID

    class LEN(UniqueIdentifier32Bytes.LEN):
        """
        Field Lengths
        """
        BYTES_16_TO_31 = 0x80
    # end class LEN

    FIELDS = UniqueIdentifier32Bytes.FIELDS + (
        BitField(FID.BYTES_16_TO_31,
                 LEN.BYTES_16_TO_31,
                 0x00,
                 0x00,
                 title='Bytes16To31',
                 name='bytes_16_to_31',
                 checks=(CheckHexList(LEN.BYTES_16_TO_31 // 8), CheckByte())),
    )

    def __init__(self, device_index, feature_index, bytes_16_to_31):
        """
        Constructor

        @param  device_index: Device Index
        @type device_index: int or HexList
        @param  feature_index: feature Index
        @type feature_index: int or HexList
        @param  bytes_16_to_31: The bytes 16 to 31 of the unique identifier
        @type bytes_16_to_31: int or HexList
        """
        super(GetByte16To31Response, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.bytes_16_to_31 = bytes_16_to_31
    # end def __init__
# end class GetByte16To31Response


class RegenId(UniqueIdentifier32Bytes):
    """
    UniqueIdentifier32Bytes RegenId implementation class

    This function re-generates a new unique identifier.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(UniqueIdentifier32Bytes.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(UniqueIdentifier32Bytes.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = UniqueIdentifier32Bytes.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UniqueIdentifier32Bytes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index: Device Index
        @type device_index: int or HexList
        @param  feature_index: feature Index
        @type feature_index: int or HexList
        """
        super(RegenId, self).__init__(device_index, feature_index)

        self.functionIndex = RegenIdResponse.FUNCTION_INDEX
    # end def __init__
# end class RegenId


class RegenIdResponse(UniqueIdentifier32Bytes):
    """
    UniqueIdentifier32Bytes RegenId response implementation class

    This function re-generates a new unique identifier.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || Padding                 || 128          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RegenId,)
    FUNCTION_INDEX = 2
    VERSION = (1,)

    class FID(UniqueIdentifier32Bytes.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(UniqueIdentifier32Bytes.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = UniqueIdentifier32Bytes.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UniqueIdentifier32Bytes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index: Device Index
        @type device_index: int or HexList
        @param  feature_index: feature Index
        @type feature_index: int or HexList
        """
        super(RegenIdResponse, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class RegenIdResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
