#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.perkeylighting

@brief  HID++ 2.0 Per key lighting command interface definition

@author christophe.roquebert

@date   2019/02/19
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

class PerKeyLighting(HidppMessage):
    """
    PerKeyLighting implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 128          ||
    """
    FEATURE_ID = 0x8081
    ZONES_COUNT = 114  # keyboard with 114 RGB zones

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        """
        super(PerKeyLighting, self).__init__()

        self.deviceIndex        = deviceIndex
        self.featureIndex       = featureIndex
# end class PerKeyLighting


class SetIndividualRgbZones(PerKeyLighting):
    """
    ConfigChange GetConfigurationCookie implementation class
    
    Requests cookie from device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || rgbZoneID_0            || 8            ||
    || R_0                    || 8            ||
    || G_0                    || 8            ||
    || B_0                    || 8            ||
    || rgbZoneID_1            || 8            ||
    || R_1                    || 8            ||
    || G_1                    || 8            ||
    || B_1                    || 8            ||
    || rgbZoneID_2            || 8            ||
    || R_2                    || 8            ||
    || G_2                    || 8            ||
    || B_2                    || 8            ||
    || rgbZoneID_3            || 8            ||
    || R_3                    || 8            ||
    || G_3                    || 8            ||
    || B_3                    || 8            ||
    """

    class FID(PerKeyLighting.FID):
        """
        Field Identifiers
        """
        RGB_ZONE_ID_0 = 0xFA
        R_0 = 0xF9
        G_0 = 0xF8
        B_0 = 0xF7
        RGB_ZONE_ID_1 = 0xF6
        R_1 = 0xF5
        G_1 = 0xF4
        B_1 = 0xF3
        RGB_ZONE_ID_2 = 0xF2
        R_2 = 0xF1
        G_2 = 0xF0
        B_2 = 0xEF
        RGB_ZONE_ID_3 = 0xEE
        R_3 = 0xED
        G_3 = 0xEC
        B_3 = 0xEB
    # end class FID

    class LEN(PerKeyLighting.LEN):
        """
        Field Lengths
        """
        RGB_ZONE_ID_0 = 0x08
        R_0 = 0x08
        G_0 = 0x08
        B_0 = 0x08
        RGB_ZONE_ID_1 = 0x08
        R_1 = 0x08
        G_1 = 0x08
        B_1 = 0x08
        RGB_ZONE_ID_2 = 0x08
        R_2 = 0x08
        G_2 = 0x08
        B_2 = 0x08
        RGB_ZONE_ID_3 = 0x08
        R_3 = 0x08
        G_3 = 0x08
        B_3 = 0x08
    # end class LEN

    class DEFAULT(object):
        '''
        Fields Default values
        '''
        PADDING = 0xFF
    # end class DEFAULT

    FIELDS = PerKeyLighting.FIELDS + (
              BitField(FID.RGB_ZONE_ID_0,
                       LEN.RGB_ZONE_ID_0,
                       0x00,
                       0x00,
                       title='RgbZoneID_0',
                       name='rgb_zone_id_0',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                               CheckByte(),),),
              BitField(FID.R_0,
                       LEN.R_0,
                       0x00,
                       0x00,
                       title='R_0',
                       name='r_0',
                       checks=(CheckHexList(LEN.R_0 // 8),
                               CheckByte(),),),
              BitField(FID.G_0,
                       LEN.G_0,
                       0x00,
                       0x00,
                       title='G_0',
                       name='g_0',
                       checks=(CheckHexList(LEN.G_0 // 8),
                               CheckByte(),),),
              BitField(FID.B_0,
                       LEN.B_0,
                       0x00,
                       0x00,
                       title='B_0',
                       name='b_0',
                       checks=(CheckHexList(LEN.B_0 // 8),
                               CheckByte(),),),
              BitField(FID.RGB_ZONE_ID_1,
                       LEN.RGB_ZONE_ID_1,
                       0x00,
                       0x00,
                       title='RgbZoneID_1',
                       name='rgb_zone_id_1',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_1 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.R_1,
                       LEN.R_1,
                       0x00,
                       0x00,
                       title='R_1',
                       name='r_1',
                       checks=(CheckHexList(LEN.R_1 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.G_1,
                       LEN.G_1,
                       0x00,
                       0x00,
                       title='G_1',
                       name='g_1',
                       checks=(CheckHexList(LEN.G_1 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.B_1,
                       LEN.B_1,
                       0x00,
                       0x00,
                       title='B_1',
                       name='b_1',
                       checks=(CheckHexList(LEN.B_1 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.RGB_ZONE_ID_2,
                       LEN.RGB_ZONE_ID_2,
                       0x00,
                       0x00,
                       title='RgbZoneID_2',
                       name='rgb_zone_id_2',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_2 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.R_2,
                       LEN.R_2,
                       0x00,
                       0x00,
                       title='R_2',
                       name='r_2',
                       checks=(CheckHexList(LEN.R_2 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.G_2,
                       LEN.G_2,
                       0x00,
                       0x00,
                       title='G_2',
                       name='g_2',
                       checks=(CheckHexList(LEN.G_2 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.B_2,
                       LEN.B_2,
                       0x00,
                       0x00,
                       title='B_2',
                       name='b_2',
                       checks=(CheckHexList(LEN.B_2 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.RGB_ZONE_ID_3,
                       LEN.RGB_ZONE_ID_3,
                       0x00,
                       0x00,
                       title='RgbZoneID_3',
                       name='rgb_zone_id_3',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_3 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.R_3,
                       LEN.R_3,
                       0x00,
                       0x00,
                       title='R_3',
                       name='r_3',
                       checks=(CheckHexList(LEN.R_3 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.G_3,
                       LEN.G_3,
                       0x00,
                       0x00,
                       title='G_3',
                       name='g_3',
                       checks=(CheckHexList(LEN.G_3 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              BitField(FID.B_3,
                       LEN.B_3,
                       0x00,
                       0x00,
                       title='B_3',
                       name='b_3',
                       checks=(CheckHexList(LEN.B_3 // 8),
                               CheckByte(),),
                       default_value=DEFAULT.PADDING),
              )

    def __init__(self,
                 deviceIndex,
                 featureId,
                 rgb_zone_id_0,
                 r_0,
                 g_0,
                 b_0,
                 rgb_zone_id_1=None,
                 r_1=None,
                 g_1=None,
                 b_1=None,
                 rgb_zone_id_2=None,
                 r_2=None,
                 g_2=None,
                 b_2=None,
                 rgb_zone_id_3=None,
                 r_3=None,
                 g_3=None,
                 b_3=None,
                 ):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(SetIndividualRgbZones, self).__init__(deviceIndex, featureId)

        self.functionIndex = SetIndividualRgbZonesResponse.FUNCTION_INDEX

        # rgb zone 0 parameters
        self.rgb_zone_id_0 = rgb_zone_id_0
        self.r_0 = r_0
        self.g_0 = g_0
        self.b_0 = b_0

        # rgb zone 1 parameters
        if rgb_zone_id_1 is not None:
            self.rgb_zone_id_1 = rgb_zone_id_1
            self.r_1 = r_1
            self.g_1 = g_1
            self.b_1 = b_1
        # end if

        # rgb zone 2 parameters
        if rgb_zone_id_2 is not None:
            self.rgb_zone_id_2 = rgb_zone_id_2
            self.r_2 = r_2
            self.g_2 = g_2
            self.b_2 = b_2
        # end if

        # rgb zone 3 parameters
        if rgb_zone_id_3 is not None:
            self.rgb_zone_id_3 = rgb_zone_id_3
            self.r_3 = r_3
            self.g_3 = g_3
            self.b_3 = b_3
        # end if
    # end def __init__
# end class SetIndividualRgbZones

    
class SetIndividualRgbZonesResponse(PerKeyLighting):
    """
    PerKeyLighting SetIndividualRgbZones response implementation class
    
    Reads cookie from device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || rgbZoneID_0            || 8            ||
    || rgbZoneID_1            || 8            ||
    || rgbZoneID_2            || 8            ||
    || rgbZoneID_3            || 8            ||
    || Padding                || 96           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetIndividualRgbZones)
    FUNCTION_INDEX = 1
    VERSION = (2, )

    class FID(PerKeyLighting.FID):
        """
        Field Identifiers
        """
        RGB_ZONE_ID_0 = 0xFA
        RGB_ZONE_ID_1 = 0xF9
        RGB_ZONE_ID_2 = 0xF8
        RGB_ZONE_ID_3 = 0xF7
        PADDING = 0xF6
    # end class FID

    class LEN(PerKeyLighting.LEN):
        """
        Field Lengths
        """
        RGB_ZONE_ID_0 = 0x08
        RGB_ZONE_ID_1 = 0x08
        RGB_ZONE_ID_2 = 0x08
        RGB_ZONE_ID_3 = 0x08
        PADDING = 0x60
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
              BitField(FID.RGB_ZONE_ID_0,
                       LEN.RGB_ZONE_ID_0,
                       0x00,
                       0x00,
                       title='Rgb_zone_id_0',
                       name='rgb_zone_id_0',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                               CheckByte(),),
                       conversions={HexList: Numeral},),
              BitField(FID.RGB_ZONE_ID_1,
                       LEN.RGB_ZONE_ID_1,
                       0x00,
                       0x00,
                       title='Rgb_zone_id_1',
                       name='rgb_zone_id_1',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_1 // 8),
                               CheckByte(),),
                       conversions={HexList: Numeral},),
              BitField(FID.RGB_ZONE_ID_2,
                       LEN.RGB_ZONE_ID_2,
                       0x00,
                       0x00,
                       title='Rgb_zone_id_2',
                       name='rgb_zone_id_2',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_2 // 8),
                               CheckByte(),),
                       conversions={HexList: Numeral},),
              BitField(FID.RGB_ZONE_ID_3,
                       LEN.RGB_ZONE_ID_3,
                       0x00,
                       0x00,
                       title='Rgb_zone_id_3',
                       name='rgb_zone_id_3',
                       checks=(CheckHexList(LEN.RGB_ZONE_ID_3 // 8),
                               CheckByte(),),
                       conversions={HexList: Numeral},),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8),
                               CheckByte(),),
                       default_value=PerKeyLighting.DEFAULT.PADDING),
              )

    def __init__(self, deviceIndex,
                       featureId,
                       rgb_zone_id_0,
                       rgb_zone_id_1=None,
                       rgb_zone_id_2=None,
                       rgb_zone_id_3=None):
        """
        Constructor

        @param  deviceIndex      [in] (int)  Device Index
        @param  featureId        [in] (int)  desired feature Id
        @param  rgb_zone_id_0    [in] (int)  returned rgb_zone_id index 0
        @option rgb_zone_id_1    [in] (int)  returned rgb_zone_id index 1
        @option rgb_zone_id_2    [in] (int)  returned rgb_zone_id index 2
        @option rgb_zone_id_3    [in] (int)  returned rgb_zone_id index 3
        """
        super(SetIndividualRgbZonesResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.rgb_zone_id_0 = rgb_zone_id_0

        if rgb_zone_id_1 is not None:
            self.rgb_zone_id_1 = rgb_zone_id_1
        # end if
        if rgb_zone_id_2 is not None:
            self.rgb_zone_id_2 = rgb_zone_id_2
        # end if
        if rgb_zone_id_3 is not None:
            self.rgb_zone_id_3 = rgb_zone_id_3
        # end if
    # end def __init__
# end class SetIndividualRgbZonesResponse


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
