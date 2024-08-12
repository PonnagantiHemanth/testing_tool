#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.batteryunifiedlevelstatus

@brief  HID++ 2.0 BatteryStatus command interface definition

@author Andy Su

@date   2019/2/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

from pyhid.bitfield                  import BitField
from pyhid.hidpp.hidppmessage        import HidppMessage, TYPE
from pyhid.field                     import CheckByte
from pyhid.field                     import CheckHexList
from pyhid.field                     import CheckInt
from pylibrary.tools.hexlist         import HexList
from pylibrary.tools.numeral         import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class BatteryStatus:
    """
    Battery status definition class
    """
    DISCHARGING                         = 0
    RECHARGING                          = 1
    CHARGE_IN_FINAL_STAGE               = 2
    CHARGE_COMPLETE                     = 3
    RECHARGE_BELOW_OPTIMAL_SPEED        = 4
    INVALID_BATTERY_TYPE                = 5
    THERMAL_ERROR                       = 6
    OTHER_CHARGING_ERROR                = 7
    START_CHARGING_AND_DISCONNECT_RF    = 8
    INVALID                             = 9
# end class BatteryStatus


class BatteryUnifiedLevelStatus(HidppMessage):
    """
    BatteryUnifiedLevelStatus implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x1000
    MAX_FUNCTION_INDEX_V0 = 1
    MAX_FUNCTION_INDEX_V1 = 2

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        """
        super(BatteryUnifiedLevelStatus, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
# end class BatteryUnifiedLevelStatus


class GetBatteryLevelStatus(BatteryUnifiedLevelStatus):
    """
    BatteryUnifiedLevelStatus GetBatteryLevelStatus implementation class

    Returns battery status to SW

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(BatteryUnifiedLevelStatus.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(BatteryUnifiedLevelStatus.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = BatteryUnifiedLevelStatus.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=BatteryUnifiedLevelStatus.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetBatteryLevelStatus, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetBatteryLevelStatusResponse.FUNCTION_INDEX
    # end def __init__
# end class GetBatteryLevelStatus


class GetBatteryLevelStatusResponse(BatteryUnifiedLevelStatus):
    """
    BatteryUnifiedLevelStatus GetBatteryLevelStatus response implementation class

    Returns battery status to SW

    Format:
    || @b Name                    || @b Bit count ||
    || ReportID                   || 8            ||
    || DeviceIndex                || 8            ||
    || FeatureIndex               || 8            ||
    || FunctionID                 || 4            ||
    || SoftwareID                 || 4            ||
    || BatteryDischargeLevel      || 8            ||
    || BatteryDischargeNextLevel  || 8            ||
    || BatteryStatus              || 8            ||
    || Padding                    || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBatteryLevelStatus)
    FUNCTION_INDEX = 0
    VERSION = (0, 1,)

    class FID(BatteryUnifiedLevelStatus.FID):
        """
        Field Identifiers
        """
        BATTERY_DISCHARGE_LEVEL      = 0xFA
        BATTERY_DISCHARGE_NEXT_LEVEL = 0xF9
        BATTERY_STATUS               = 0xF8
        PADDING                      = 0xF7

    # end class FID

    class LEN(BatteryUnifiedLevelStatus.LEN):
        """
        Field Lengths
        """
        BATTERY_DISCHARGE_LEVEL      = 0x08
        BATTERY_DISCHARGE_NEXT_LEVEL = 0x08
        BATTERY_STATUS               = 0x08
        PADDING                      = 0x68

    # end class LEN

    FIELDS = BatteryUnifiedLevelStatus.FIELDS + (
        BitField(FID.BATTERY_DISCHARGE_LEVEL,
                 LEN.BATTERY_DISCHARGE_LEVEL,
                 0x00,
                 0x00,
                 title='Battery Discharge Level',
                 name='batteryDischargeLevel',
                 checks=(CheckHexList(LEN.BATTERY_DISCHARGE_LEVEL // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.BATTERY_DISCHARGE_NEXT_LEVEL,
                 LEN.BATTERY_DISCHARGE_NEXT_LEVEL,
                 0x00,
                 0x00,
                 title='Battery Discharge Next Level',
                 name='batteryDischargeNextLevel',
                 checks=(CheckHexList(LEN.BATTERY_DISCHARGE_NEXT_LEVEL // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.BATTERY_STATUS,
                 LEN.BATTERY_STATUS,
                 0x00,
                 0x00,
                 title='Battery Status',
                 name='batteryStatus',
                 checks=(CheckHexList(LEN.BATTERY_STATUS // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=BatteryUnifiedLevelStatus.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        batteryDischargeLevel,
                        batteryDischargeNextLevel,
                        batteryStatus):
        """
        Constructor

        @param  deviceIndex               [in] (int)  Device Index
        @param  featureId                 [in] (int)  desired feature Id
        @param  batteryDischargeLevel     [in] (int)  returned battery discharge level
        @param  batteryDischargeNextLevel [in] (int)  returned battery discharge next level
        @param  batteryStatus             [in] (int)  returned battery status
        """
        super(GetBatteryLevelStatusResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.batteryDischargeLevel = batteryDischargeLevel
        self.batteryDischargeNextLevel = batteryDischargeNextLevel
        self.batteryStatus = batteryStatus
    # end def __init__
# end class GetBatteryLevelStatusResponse


class GetBatteryCapability(BatteryUnifiedLevelStatus):
    """
    BatteryUnifiedLevelStatus GetBatteryCapability implementation class

    Returns the static capability information about the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(BatteryUnifiedLevelStatus.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(BatteryUnifiedLevelStatus.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = BatteryUnifiedLevelStatus.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=BatteryUnifiedLevelStatus.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetBatteryCapability, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetBatteryCapabilityResponse.FUNCTION_INDEX
    # end def __init__
# end class GetBatteryCapability


class GetBatteryCapabilityResponse(BatteryUnifiedLevelStatus):
    """
    BatteryUnifiedLevelStatus GetBatteryCapability response implementation class

    Returns the static capability information about the device.

    Format:
    || @b Name               || @b Bit count ||
    || ReportID              || 8            ||
    || DeviceIndex           || 8            ||
    || FeatureIndex          || 8            ||
    || FunctionID            || 4            ||
    || SoftwareID            || 4            ||
    || NumberOfLevels        || 8            ||
    || Flags                 || 8            ||
    || NominalBatteryLife    || 16           ||
    || BatteryCriticalLevel  || 8            ||
    || Padding               || 88           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBatteryCapability)
    FUNCTION_INDEX = 1
    VERSION = (0, 1,)

    class FID(BatteryUnifiedLevelStatus.FID):
        """
        Field Identifiers
        """
        NUMBER_OF_LEVELS       = 0xFA
        FLAGS                  = 0xF9
        NOMINAL_BATTERY_LIFE   = 0xF8
        BATTERY_CRITICAL_LEVEL = 0xF7
        PADDING                = 0xF6

    # end class FID

    class LEN(BatteryUnifiedLevelStatus.LEN):
        """
        Field Lengths
        """
        NUMBER_OF_LEVELS       = 0x08
        FLAGS                  = 0x08
        NOMINAL_BATTERY_LIFE   = 0x10
        BATTERY_CRITICAL_LEVEL = 0x08
        PADDING                = 0x58

    # end class LEN

    FIELDS = BatteryUnifiedLevelStatus.FIELDS + (
        BitField(FID.NUMBER_OF_LEVELS,
                 LEN.NUMBER_OF_LEVELS,
                 0x00,
                 0x00,
                 title='Number Of Levels',
                 name='numberOfLevels',
                 checks=(CheckHexList(LEN.NUMBER_OF_LEVELS // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.FLAGS,
                 LEN.FLAGS,
                 0x00,
                 0x00,
                 title='Flags',
                 name='flags',
                 checks=(CheckHexList(LEN.FLAGS // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.NOMINAL_BATTERY_LIFE,
                 LEN.NOMINAL_BATTERY_LIFE,
                 0x00,
                 0x00,
                 title='Nominal Battery Life',
                 name='nominalBatteryLife',
                 checks=(CheckHexList(LEN.NOMINAL_BATTERY_LIFE // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.BATTERY_CRITICAL_LEVEL,
                 LEN.BATTERY_CRITICAL_LEVEL,
                 0x00,
                 0x00,
                 title='Battery Critical Level',
                 name='batteryCriticalLevel',
                 checks=(CheckHexList(LEN.BATTERY_CRITICAL_LEVEL // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=BatteryUnifiedLevelStatus.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        numberOfLevels,
                        flags,
                        nominalBatteryLife,
                        batteryCriticalLevel):
        """
        Constructor

        @param  deviceIndex               [in] (int)  Device Index
        @param  featureId                 [in] (int)  desired feature Id
        @param  numberOfLevels            [in] (int)  returned number of levels
        @param  flags                     [in] (int)  returned flags
        @param  nominalBatteryLife        [in] (int)  returned nominal battery life
        @param  batteryCriticalLevel      [in] (int)  returned battery critical level
        """
        super(GetBatteryCapabilityResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.numberOfLevels = numberOfLevels
        self.flags = flags
        self.nominalBatteryLife = nominalBatteryLife
        self.batteryCriticalLevel = batteryCriticalLevel
    # end def __init__
# end class GetBatteryCapabilityResponse


class ShowBatteryStatus(BatteryUnifiedLevelStatus):
    """
    BatteryUnifiedLevelStatus ShowBatteryStatus implementation class

    Returns the battery status by lightening LED

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(BatteryUnifiedLevelStatus.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(BatteryUnifiedLevelStatus.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = BatteryUnifiedLevelStatus.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=BatteryUnifiedLevelStatus.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                    featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(ShowBatteryStatus, self).__init__(deviceIndex, featureId)

        self.functionIndex = ShowBatteryStatusResponse.FUNCTION_INDEX
    # end def __init__
# end class ShowBatteryStatus


class ShowBatteryStatusResponse(BatteryUnifiedLevelStatus):
    """
    BatteryUnifiedLevelStatus ShowBatteryStatus response implementation class

    Returns the battery status by lightening LED

    Format:
    || @b Name               || @b Bit count ||
    || ReportID              || 8            ||
    || DeviceIndex           || 8            ||
    || FeatureIndex          || 8            ||
    || FunctionID            || 4            ||
    || SoftwareID            || 4            ||
    || Padding               || 128           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ShowBatteryStatus)
    FUNCTION_INDEX = 2
    VERSION = (1,)

    class FID(BatteryUnifiedLevelStatus.FID):
        """
        Field Identifiers
        """
        PADDING                = 0xFA

    # end class FID

    class LEN(BatteryUnifiedLevelStatus.LEN):
        """
        Field Lengths
        """
        PADDING                = 0x80

    # end class LEN

    FIELDS = BatteryUnifiedLevelStatus.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=BatteryUnifiedLevelStatus.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId):
        """
        Constructor

        @param  deviceIndex               [in] (int)  Device Index
        @param  featureId                 [in] (int)  desired feature Id
        """
        super(ShowBatteryStatusResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class ShowBatteryStatusResponse


class BatteryLevelStatusBroadcastEvent(BatteryUnifiedLevelStatus):
    """
    BatteryUnifiedLevelStatus BatteryLevelStatusBroadcastEvent implementation class

    Returns battery status to SW

    Format:
    || @b Name                    || @b Bit count ||
    || ReportID                   || 8            ||
    || DeviceIndex                || 8            ||
    || FeatureIndex               || 8            ||
    || FunctionID                 || 4            ||
    || SoftwareID                 || 4            ||
    || BatteryDischargeLevel      || 8            ||
    || BatteryDischargeNextLevel  || 8            ||
    || BatteryStatus              || 8            ||
    || Padding                    || 104          ||
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0
    VERSION = (0, 1,)

    class FID(BatteryUnifiedLevelStatus.FID):
        """
        Field Identifiers
        """
        BATTERY_DISCHARGE_LEVEL = 0xFA
        BATTERY_DISCHARGE_NEXT_LEVEL = 0xF9
        BATTERY_STATUS = 0xF8
        PADDING = 0xF7

    # end class FID

    class LEN(BatteryUnifiedLevelStatus.LEN):
        """
        Field Lengths
        """
        BATTERY_DISCHARGE_LEVEL = 0x08
        BATTERY_DISCHARGE_NEXT_LEVEL = 0x08
        BATTERY_STATUS = 0x08
        PADDING = 0x68

    # end class LEN

    FIELDS = BatteryUnifiedLevelStatus.FIELDS + (
        BitField(FID.BATTERY_DISCHARGE_LEVEL,
                 LEN.BATTERY_DISCHARGE_LEVEL,
                 0x00,
                 0x00,
                 title='Battery Discharge Level',
                 name='batteryDischargeLevel',
                 checks=(CheckHexList(LEN.BATTERY_DISCHARGE_LEVEL // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.BATTERY_DISCHARGE_NEXT_LEVEL,
                 LEN.BATTERY_DISCHARGE_NEXT_LEVEL,
                 0x00,
                 0x00,
                 title='Battery Discharge Next Level',
                 name='batteryDischargeNextLevel',
                 checks=(CheckHexList(LEN.BATTERY_DISCHARGE_NEXT_LEVEL // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.BATTERY_STATUS,
                 LEN.BATTERY_STATUS,
                 0x00,
                 0x00,
                 title='Battery Status',
                 name='batteryStatus',
                 checks=(CheckHexList(LEN.BATTERY_STATUS // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=BatteryUnifiedLevelStatus.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                 featureId,
                 batteryDischargeLevel,
                 batteryDischargeNextLevel,
                 batteryStatus):
        """
        Constructor

        @param  deviceIndex               [in] (int)  Device Index
        @param  featureId                 [in] (int)  desired feature Id
        @param  batteryDischargeLevel     [in] (int)  returned battery discharge level
        @param  batteryDischargeNextLevel [in] (int)  returned battery discharge next level
        @param  batteryStatus             [in] (int)  returned battery status
        """
        super(BatteryLevelStatusBroadcastEvent, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.batteryDischargeLevel = batteryDischargeLevel
        self.batteryDischargeNextLevel = batteryDischargeNextLevel
        self.batteryStatus = batteryStatus
    # end def __init__
# end class BatteryLevelStatusBroadcastEvent


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
