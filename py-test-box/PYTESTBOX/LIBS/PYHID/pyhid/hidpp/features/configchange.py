#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.configchange

@brief  HID++ 2.0 Config Change command interface definition

@author christophe.roquebert

@date   2019/01/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

from pyhid.bitfield                  import BitField
from pyhid.hidpp.hidppmessage        import HidppMessage, TYPE
from pyhid.field                     import CheckByte
from pyhid.field                     import CheckInt
from pyhid.field                     import CheckHexList
from pylibrary.tools.hexlist         import HexList
from pylibrary.tools.numeral         import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigChange(HidppMessage):
    """
    ConfigChange implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x0020

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        """
        super(ConfigChange, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
# end class DeviceTypeAndName


class GetConfigurationCookie(ConfigChange):
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
    || Padding                || 24           ||
    """

    class FID(ConfigChange.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(ConfigChange.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ConfigChange.FIELDS + (
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       default_value=ConfigChange.DEFAULT.PADDING),
              )

    def __init__(self, deviceIndex,
                       featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetConfigurationCookie, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetConfigurationCookieResponse.FUNCTION_INDEX
    # end def __init__
# end class GetConfigurationCookie

    
class GetConfigurationCookieResponse(ConfigChange):
    """
    ConfigChange GetConfigurationCookie response implementation class
    
    Reads cookie from device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || ConfigurationCookie    || 16           ||
    || Padding                || 8            ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetConfigurationCookie)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(ConfigChange.FID):
        """
        Field Identifiers
        """
        CONFIGURATION_COOKIE = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(ConfigChange.LEN):
        """
        Field Lengths
        """
        CONFIGURATION_COOKIE = 0x10
        PADDING = 0x08
    # end class LEN

    FIELDS = ConfigChange.FIELDS + (
              BitField(FID.CONFIGURATION_COOKIE,
                       LEN.CONFIGURATION_COOKIE,
                       0x00,
                       0x00,
                       title='ConfigurationCookie',
                       name ='configurationCookie',
                       checks=(CheckHexList(LEN.CONFIGURATION_COOKIE // 8),
                                   CheckByte(),),
                       conversions  = {HexList : Numeral},),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8),
                               CheckByte(),),
                       default_value=ConfigChange.DEFAULT.PADDING),
              )

    def __init__(self, deviceIndex,
                       featureId,
                       configurationCookie):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  configurationCookie    [in] (int)  returned configurationCookie
        """
        super(GetConfigurationCookieResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex          = self.FUNCTION_INDEX
        self.configurationCookie    = configurationCookie
    # end def __init__
# end class GetConfigurationCookieResponse


class SetConfigurationComplete(ConfigChange):
    """
    ConfigChange SetConfigurationComplete implementation class
    
    Changes the configuration complete flag on the device or 
    resets the device flags.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || ConfigurationCookie    || 16           ||
    || Padding                || 8            ||
    """

    class FID(ConfigChange.FID):
        """
        Field Identifiers
        """
        CONFIGURATION_COOKIE        = 0xFA
        PADDING                     = 0xF9
    # end class FID

    class LEN(ConfigChange.LEN):
        """
        Field Lengths
        """
        CONFIGURATION_COOKIE        = 0x10
        PADDING                     = 0x08
    # end class LEN

    FIELDS = ConfigChange.FIELDS + (
              BitField(FID.CONFIGURATION_COOKIE,
                       LEN.CONFIGURATION_COOKIE,
                       0x00,
                       0x00,
                       title='ConfigurationCookie',
                       name='configurationCookie',
                       checks=(CheckHexList(LEN.CONFIGURATION_COOKIE // 8),
                                   CheckInt(0, 0xFFFF),)),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name ='padding',
                       default_value = ConfigChange.DEFAULT.PADDING),
              )

    def __init__(self, deviceIndex,
                       featureId,
                       configurationCookie):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  configurationCookie    [in] (int)  randomly generated cookie 
                                                   associated with current device configuration.
        """
        super(SetConfigurationComplete, self).__init__(deviceIndex, featureId)

        self.functionIndex = SetConfigurationCompleteResponse.FUNCTION_INDEX
        self.configurationCookie = configurationCookie
    # end def __init__
# end class SetConfigurationComplete


class SetConfigurationCompleteResponse(SetConfigurationComplete):
    """
    ConfigChange SetConfigurationComplete implementation class
    
    Sets and returns the configuration complete flag on the device 
    or resets the device flags.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || ConfigurationCookie    || 16           ||
    || Padding                || 8            ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetConfigurationComplete)
    FUNCTION_INDEX = 1
    VERSION = (0, )

# end class SetConfigurationCompleteResponse


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
