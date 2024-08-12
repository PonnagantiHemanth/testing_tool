#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.featureinfo

@brief  HID++ 2.0 FeatureInfo command interface definition

@author christophe.roquebert

@date   2018/12/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

from pyhid.bitfield                  import BitField
from pyhid.hidpp.hidppmessage        import HidppMessage, TYPE
from pyhid.field                     import CheckByte
from pyhid.field                     import CheckHexList
from pylibrary.tools.hexlist         import HexList
from pylibrary.tools.numeral         import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class FeatureInfo(HidppMessage):
    '''
    FeatureInfo implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    '''
    FEATURE_ID     = 0x0002

    def __init__(self, deviceIndex, featureIndex):
        '''
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        '''
        super(FeatureInfo, self).__init__()

        self.deviceIndex        = deviceIndex
        self.featureIndex       = featureIndex
# end class FeatureInfo
    
class GetExtendee(FeatureInfo):
    '''
    FeatureInfo GetExtendee implementation class
    
    Returns the number of features contained in the set, 
    not including the root feature.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || ExtenderID             || 16           ||
    || Padding                || 8            ||
    '''
    GET_COUNT_FUNCTION_INDEX = 0

    class FID(FeatureInfo.FID):
        '''
        Field Identifiers
        '''
        EXTENDER_ID                 = 0xFA
        PADDING                     = 0xF9
    # end class FID

    class LEN(FeatureInfo.LEN):
        '''
        Field Lengths
        '''
        EXTENDER_ID                 = 0x10
        PADDING                     = 0x08
    # end class LEN

    FIELDS = FeatureInfo.FIELDS + (
              BitField(FID.EXTENDER_ID,
                       LEN.EXTENDER_ID,
                       0x00,
                       0x00,
                       title    = 'ExtenderID',
                       name     = 'extenderID',
                       checks   = (CheckHexList(LEN.EXTENDER_ID // 8),),
                       conversions  = {HexList : Numeral},),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title    = 'Padding',
                       name     = 'padding',
                       default_value = FeatureInfo.DEFAULT.PADDING),
              )

    def __init__(self, deviceIndex,
                       featureId,
                       extenderID):
        '''
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  extenderID             [in] (int)  The ID of the hypothetic extender feature
        '''
        super(GetExtendee, self).__init__(deviceIndex, featureId)

        self.functionIndex          = self.GET_COUNT_FUNCTION_INDEX
        self.extenderID             = extenderID
    # end def __init__
# end class GetExtendee

    
class GetExtendeeResponse(FeatureInfo):
    '''
    FeatureInfo GetExtendee response implementation class
    
    Returns the index of the feature which is extended 
    by the given hypothetical extender

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || ExtendeeID             || 16           ||
    || Padding                || 8            ||
    '''
    MSG_TYPE        = TYPE.RESPONSE
    REQUEST_LIST    = (GetExtendee)

    class FID(FeatureInfo.FID):
        '''
        Field Identifiers
        '''
        EXTENDEE_ID                 = 0xFA
        PADDING                     = 0xF9
    # end class FID

    class LEN(FeatureInfo.LEN):
        '''
        Field Lengths
        '''
        EXTENDEE_ID                 = 0x10
        PADDING                     = 0x08
    # end class LEN

    FIELDS = FeatureInfo.FIELDS + (
              BitField(FID.EXTENDEE_ID,
                       LEN.EXTENDEE_ID,
                       0x00,
                       0x00,
                       title    = 'ExtendeeId',
                       name     = 'extendeeId',
                       checks   = (CheckHexList(LEN.EXTENDEE_ID // 8),
                                   CheckByte(),),
                       conversions  = {HexList : Numeral},),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title    = 'Padding',
                       name     = 'padding',
                       checks   = (CheckHexList(LEN.PADDING // 8),
                                   CheckByte(),),
                       default_value = FeatureInfo.DEFAULT.PADDING),
              )

    def __init__(self, deviceIndex,
                       featureId,
                       extendeeId):
        '''
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  extendeeId             [in] (int)  returned extendeeId
        '''
        super(GetExtendeeResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex          = GetExtendee.GET_COUNT_FUNCTION_INDEX
        self.extendeeId             = extendeeId
    # end def __init__
# end class GetExtendeeResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
