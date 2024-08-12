#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.common.equaddjdebuginfo

@brief  HID++ 2.0 EquadDJ Debug Info command interface definition

@author Stanislas Cottard

@date   2019/07/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class EquadDJDebugInfo(HidppMessage):
    """
    EquadDJ Debug Info implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x1DF3
    MAX_FUNCTION_INDEX = 1

    REG_DEBUG_OFF = 0
    REG_DEBUG_ON = 1

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index           [in] (int)  feature Index
        """
        super(EquadDJDebugInfo, self).__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class EquadDJDebugInfo


class ReadEquadDJDebugInfo(EquadDJDebugInfo):
    """
    Read EquadDJDebugInfo implementation class

    Requests the EquadDJDebugInfo register.
    This register enables/disables debug mode. It enables an eQuad device to send debug information in additional to
    the normal payload. When enabled, the receiver will post 0x49 notifications
    (see §3.23[HID++ Specification DWS-763341-0000 - Link]) containing the extra debug information.
    Upon device power-up, debug is disabled by default.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || Padding                 || 24           ||
    """

    class FID(EquadDJDebugInfo.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(EquadDJDebugInfo.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = EquadDJDebugInfo.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=EquadDJDebugInfo.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_id):
        """
        Constructor

        @param  device_index                    [in] (int)  Device Index
        @param  feature_id                      [in] (int)  Desired feature Id
        """
        super(ReadEquadDJDebugInfo, self).__init__(device_index, feature_id)

        self.functionIndex = ReadEquadDJDebugInfoResponse.FUNCTION_INDEX
    # end def __init__
# end class ReadEquadDJDebugInfo


class ReadEquadDJDebugInfoResponse(EquadDJDebugInfo):
    """
    Read EquadDJDebugInfo response implementation class

    This response contain the EquadDJDebugInfo register.
    This register enables/disables debug mode. It enables an eQuad device to send debug information in additional to
    the normal payload. When enabled, the receiver will post 0x49 notifications
    (see §3.23[HID++ Specification DWS-763341-0000 - Link]) containing the extra debug information.
    Upon device power-up, debug is disabled by default.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || EquadDJDebugInfoReg    || 8            ||
    || Padding                || 120          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadEquadDJDebugInfo,)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(EquadDJDebugInfo.FID):
        """
        Field Identifiers
        """
        EQUAD_DJ_DEBUG_INFO_REG = 0xFA
        PADDING = 0xF9

    # end class FID

    class LEN(EquadDJDebugInfo.LEN):
        """
        Field Lengths
        """
        EQUAD_DJ_DEBUG_INFO_REG = 0x08
        PADDING = 0x78

    # end class LEN

    FIELDS = EquadDJDebugInfo.FIELDS + (
        BitField(FID.EQUAD_DJ_DEBUG_INFO_REG,
                 LEN.EQUAD_DJ_DEBUG_INFO_REG,
                 0x00,
                 0x00,
                 title='EquadDJDebugInfoReg',
                 name='equad_dj_debug_info_reg',
                 checks=(CheckHexList(LEN.EQUAD_DJ_DEBUG_INFO_REG // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=EquadDJDebugInfo.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_id, equad_dj_debug_info_reg):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_id              [in] (int)  desired feature Id
        @param  equad_dj_debug_info_reg [in] (int)  The EquadDJDebugInfo register value
        """
        super(ReadEquadDJDebugInfoResponse, self).__init__(device_index, feature_id)

        self.functionIndex = self.FUNCTION_INDEX
        self.equad_dj_debug_info_reg = equad_dj_debug_info_reg
    # end def __init__
# end class ReadEquadDJDebugInfoResponse


class WriteEquadDJDebugInfo(EquadDJDebugInfo):
    """
    Write EquadDJDebugInfo implementation class

    Requests the change of EquadDJDebugInfo register.
    This register enables/disables debug mode. It enables an eQuad device to send debug information in additional to
    the normal payload. When enabled, the receiver will post 0x49 notifications
    (see §3.23[HID++ Specification DWS-763341-0000 - Link]) containing the extra debug information.
    Upon device power-up, debug is disabled by default.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || EquadDJDebugInfoReg     || 8            ||
    || Padding                 || 16           ||
    """

    class FID(EquadDJDebugInfo.FID):
        """
        Field Identifiers
        """
        EQUAD_DJ_DEBUG_INFO_REG = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(EquadDJDebugInfo.LEN):
        """
        Field Lengths
        """
        EQUAD_DJ_DEBUG_INFO_REG = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = EquadDJDebugInfo.FIELDS + (
        BitField(FID.EQUAD_DJ_DEBUG_INFO_REG,
                 LEN.EQUAD_DJ_DEBUG_INFO_REG,
                 0x00,
                 0x00,
                 title='EquadDJDebugInfoReg',
                 name='equad_dj_debug_info_reg',
                 checks=(CheckHexList(LEN.EQUAD_DJ_DEBUG_INFO_REG // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=EquadDJDebugInfo.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_id, equad_dj_debug_info_reg):
        """
        Constructor

        @param  device_index                    [in] (int)  Device Index
        @param  feature_id                      [in] (int)  Desired feature Id
        @param  equad_dj_debug_info_reg         [in] (int)  The EquadDJDebugInfo register value
        """
        super(WriteEquadDJDebugInfo, self).__init__(device_index, feature_id)

        self.functionIndex = WriteEquadDJDebugInfoResponse.FUNCTION_INDEX
        self.equad_dj_debug_info_reg = equad_dj_debug_info_reg
    # end def __init__
# end class WriteEquadDJDebugInfo


class WriteEquadDJDebugInfoResponse(EquadDJDebugInfo):
    """
    Write EquadDJDebugInfo response implementation class

    This response contain the EquadDJDebugInfo register.
    This register enables/disables debug mode. It enables an eQuad device to send debug information in additional to
    the normal payload. When enabled, the receiver will post 0x49 notifications
    (see §3.23[HID++ Specification DWS-763341-0000 - Link]) containing the extra debug information.
    Upon device power-up, debug is disabled by default.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || EquadDJDebugInfoReg    || 8            ||
    || Padding                || 120          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteEquadDJDebugInfo,)
    FUNCTION_INDEX = 1
    VERSION = (0, )

    class FID(EquadDJDebugInfo.FID):
        """
        Field Identifiers
        """
        EQUAD_DJ_DEBUG_INFO_REG = 0xFA
        PADDING = 0xF9

    # end class FID

    class LEN(EquadDJDebugInfo.LEN):
        """
        Field Lengths
        """
        EQUAD_DJ_DEBUG_INFO_REG = 0x08
        PADDING = 0x78

    # end class LEN

    FIELDS = EquadDJDebugInfo.FIELDS + (
        BitField(FID.EQUAD_DJ_DEBUG_INFO_REG,
                 LEN.EQUAD_DJ_DEBUG_INFO_REG,
                 0x00,
                 0x00,
                 title='EquadDJDebugInfoReg',
                 name='equad_dj_debug_info_reg',
                 checks=(CheckHexList(LEN.EQUAD_DJ_DEBUG_INFO_REG // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=EquadDJDebugInfo.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_id, equad_dj_debug_info_reg):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_id              [in] (int)  desired feature Id
        @param  equad_dj_debug_info_reg [in] (int)  The EquadDJDebugInfo register value
        """
        super(WriteEquadDJDebugInfoResponse, self).__init__(device_index, feature_id)

        self.functionIndex = self.FUNCTION_INDEX
        self.equad_dj_debug_info_reg = equad_dj_debug_info_reg
    # end def __init__
# end class WriteEquadDJDebugInfoResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
