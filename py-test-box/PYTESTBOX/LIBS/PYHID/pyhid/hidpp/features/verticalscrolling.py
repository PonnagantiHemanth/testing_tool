#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.verticalscrolling

@brief  HID++ 2.0 Vertical Scrolling command interface definition

@author christophe.roquebert

@date   2019/03/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class VerticalScrolling(HidppMessage):
    """
    VerticalScrolling implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x2100
    MAX_FUNCTION_INDEX = 0

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        """
        super(VerticalScrolling, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
    # end def __init__
# end class VerticalScrolling


class GetRollerInfo(VerticalScrolling):
    """
    VerticalScrolling GetRollerInfo implementation class

    Request the type & description of supported roller.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(VerticalScrolling.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(VerticalScrolling.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = VerticalScrolling.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=VerticalScrolling.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                 featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetRollerInfo, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetRollerInfoResponse.FUNCTION_INDEX
    # end def __init__

# end class GetRollerInfo


class GetRollerInfoResponse(VerticalScrolling):
    """
    VerticalScrolling GetRollerInfo response implementation class

    Returns the type & description of supported roller (vertical scrolling)

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || RollerType             || 8            ||
    || NumOfRatchetByTurn     || 8            ||
    || ScrollLines            || 8            ||
    || Padding                || 8            ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRollerInfo)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(VerticalScrolling.FID):
        """
        Field Identifiers
        """
        ROLLER_TYPE = 0xFA
        NUM_OF_RATCHET_BY_TURN = 0xF9
        SCROLL_LINES = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(VerticalScrolling.LEN):
        """
        Field Lengths
        """
        ROLLER_TYPE = 0x08
        NUM_OF_RATCHET_BY_TURN = 0x08
        SCROLL_LINES = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = VerticalScrolling.FIELDS + (
        BitField(FID.ROLLER_TYPE,
                 LEN.ROLLER_TYPE,
                 0x00,
                 0x00,
                 title='RollerType',
                 name='rollerType',
                 checks=(CheckHexList(LEN.ROLLER_TYPE // 8),
                         CheckByte(),),),
        BitField(FID.NUM_OF_RATCHET_BY_TURN,
                 LEN.NUM_OF_RATCHET_BY_TURN,
                 0x00,
                 0x00,
                 title='NumOfRatchetByTurn',
                 name='numOfRatchetByTurn',
                 checks=(CheckHexList(LEN.NUM_OF_RATCHET_BY_TURN // 8),
                         CheckByte(),),),
        BitField(FID.SCROLL_LINES,
                 LEN.SCROLL_LINES,
                 0x00,
                 0x00,
                 title='ScrollLines',
                 name='scrollLines',
                 checks=(CheckHexList(LEN.SCROLL_LINES // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=VerticalScrolling.DEFAULT.PADDING),
    )

    def __init__(self,
                 deviceIndex,
                 featureId,
                 roller_type,
                 ratchet_by_turn,
                 scroll_lines):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  roller_type            [in] (int)  Type of roller (Standard, 3G, Micro, TouchPad ...)
        @param  ratchet_by_turn        [in] (int)  Number of ratchet by turn
        @param  scroll_lines           [in] (int)  Number of scrolled lines by scroll event
        """
        super(GetRollerInfoResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.rollerType = roller_type
        self.numOfRatchetByTurn = ratchet_by_turn
        self.scrollLines = scroll_lines
    # end def __init__
# end class GetAnalysisModeResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
