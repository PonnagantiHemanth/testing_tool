#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :package: pyhid.hidpp.features.mouse.smartshift
    :brief: HID++ 2.0 SmartShift 3G/EPM wheel enhancement command interface definition
    :author: Fred Chen <fchen7@logitech.com>
    :date: 2019/08/20
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SmartShift(HidppMessage):
    """
    Smart Shift implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """

    class WheelMode:
        """
        Supported wheel modes
        """
        DoNotChange = 0
        FreeSpin = 1
        Ratchet = 2
    # end class WheelMode

    FEATURE_ID = 0x2110
    MAX_FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index           [in] (int)  feature Index
        """
        super(SmartShift, self).__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__

# end class SmartShift


class GetRatchetControlMode(SmartShift):
    """
    SmartShift GetRatchetControlMode implementation class

    Request the current smartshift configuration.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(SmartShift.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(SmartShift.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = SmartShift.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SmartShift.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index           [in] (int)  desired feature index
        """
        super(GetRatchetControlMode, self).__init__(device_index, feature_index)

        self.functionIndex = GetRatchetControlModeResponse.FUNCTION_INDEX
    # end def __init__

# end class GetRatchetControlMode


class GetRatchetControlModeResponse(SmartShift):
    """
    SmartShift GetRatchetControlMode response implementation class

    Returns the current smartshift configuration.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || WheelMode               || 8            ||
    || AutoDisengage           || 8            ||
    || AutoDisengageDefault    || 8            ||
    || Padding                 || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRatchetControlMode,)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(SmartShift.FID):
        """
        Field Identifiers
        """
        WHEEL_MODE = 0xFA
        AUTO_DISENGAGE = 0xF9
        AUTO_DISENGAGE_DEFAULT = 0xF8
        PADDING = 0xF7

    # end class FID

    class LEN(SmartShift.LEN):
        """
        Field Lengths
        """
        WHEEL_MODE = 0x08
        AUTO_DISENGAGE = 0x08
        AUTO_DISENGAGE_DEFAULT = 0x08
        PADDING = 0x68

    # end class LEN

    FIELDS = SmartShift.FIELDS + (
        BitField(FID.WHEEL_MODE,
                 LEN.WHEEL_MODE,
                 0x00,
                 0x00,
                 title='WheelMode',
                 name='wheel_mode',
                 checks=(CheckHexList(LEN.WHEEL_MODE // 8), CheckByte(),),),
        BitField(FID.AUTO_DISENGAGE,
                 LEN.AUTO_DISENGAGE,
                 0x00,
                 0x00,
                 title='AutoDisengage',
                 name='auto_disengage',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE // 8), CheckByte(),),),
        BitField(FID.AUTO_DISENGAGE_DEFAULT,
                 LEN.AUTO_DISENGAGE_DEFAULT,
                 0x00,
                 0x00,
                 title='AutoDisengageDefault',
                 name='auto_disengage_default',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE_DEFAULT // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SmartShift.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, wheel_mode, auto_disengage, auto_disengage_default):
        """
        Constructor

        @param  device_index                [in] (int)  Device Index
        @param  feature_index               [in] (int)  Desired feature index
        @param  wheel_mode                  [in] (int)  The current wheel mode
        @param  auto_disengage              [in] (int)  The speed at which the ratchet automatically disengages
        @param  auto_disengage_default      [in] (int)  The default value of the autoDisengage setting
        """
        super(GetRatchetControlModeResponse, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.wheel_mode = wheel_mode
        self.auto_disengage = auto_disengage
        self.auto_disengage_default = auto_disengage_default
    # end def __init__

# end class GetRatchetControlModeResponse


class SetRatchetControlMode(SmartShift):
    """
    SmartShift SetRatchetControlMode implementation class

    Set the wheel mode and the automatic disengage setting.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || WheelMode              || 8            ||
    || AutoDisengage          || 8            ||
    || AutoDisengageDefault   || 8            ||
    """

    class FID(SmartShift.FID):
        """
        Field Identifiers
        """
        WHEEL_MODE = 0xFA
        AUTO_DISENGAGE = 0xF9
        AUTO_DISENGAGE_DEFAULT = 0xF8

    # end class FID

    class LEN(SmartShift.LEN):
        """
        Field Lengths
        """
        WHEEL_MODE = 0x08
        AUTO_DISENGAGE = 0x08
        AUTO_DISENGAGE_DEFAULT = 0x08

    # end class LEN

    FIELDS = SmartShift.FIELDS + (
        BitField(FID.WHEEL_MODE,
                 LEN.WHEEL_MODE,
                 0x00,
                 0x00,
                 title='WheelMode',
                 name='wheel_mode',
                 checks=(CheckHexList(LEN.WHEEL_MODE // 8), CheckByte(),),
                 default_value=0,
                 optional=True),
        BitField(FID.AUTO_DISENGAGE,
                 LEN.AUTO_DISENGAGE,
                 0x00,
                 0x00,
                 title='AutoDisengage',
                 name='auto_disengage',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE // 8), CheckByte(),),
                 default_value=0,
                 optional=True),
        BitField(FID.AUTO_DISENGAGE_DEFAULT,
                 LEN.AUTO_DISENGAGE_DEFAULT,
                 0x00,
                 0x00,
                 title='AutoDisengageDefault',
                 name='auto_disengage_default',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE_DEFAULT // 8), CheckByte(),),
                 default_value=0,
                 optional=True),
    )

    def __init__(self, device_index, feature_index, wheel_mode=0, auto_disengage=0, auto_disengage_default=0):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index           [in] (int)  desired feature index
        @option wheel_mode              [in] (int)  The target wheel mode
        @option auto_disengage          [in] (int)  The speed at which the ratchet automatically disengages
        @option auto_disengage_default  [in] (int)  The default value of the autoDisengage setting
        """
        super(SetRatchetControlMode, self).__init__(device_index, feature_index)

        self.functionIndex = SetRatchetControlModeResponse.FUNCTION_INDEX
        self.wheel_mode = wheel_mode
        self.auto_disengage = auto_disengage
        self.auto_disengage_default = auto_disengage_default

    # end def __init__

# end class SetRatchetControlMode


class SetRatchetControlModeResponse(SmartShift):
    """
    SmartShift SetRatchetControlMode response implementation class

    Echo request settings.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || WheelMode               || 8            ||
    || AutoDisengage           || 8            ||
    || AutoDisengageDefault    || 8            ||
    || Padding                 || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRatchetControlMode,)
    FUNCTION_INDEX = 1
    VERSION = (0,)

    class FID(SmartShift.FID):
        """
        Field Identifiers
        """
        WHEEL_MODE = 0xFA
        AUTO_DISENGAGE = 0xF9
        AUTO_DISENGAGE_DEFAULT = 0xF8
        PADDING = 0xF7

    # end class FID

    class LEN(SmartShift.LEN):
        """
        Field Lengths
        """
        WHEEL_MODE = 0x08
        AUTO_DISENGAGE = 0x08
        AUTO_DISENGAGE_DEFAULT = 0x08
        PADDING = 0x68

    # end class LEN

    FIELDS = SmartShift.FIELDS + (
        BitField(FID.WHEEL_MODE,
                 LEN.WHEEL_MODE,
                 0x00,
                 0x00,
                 title='WheelMode',
                 name='wheel_mode',
                 checks=(CheckHexList(LEN.WHEEL_MODE // 8), CheckByte(),),),
        BitField(FID.AUTO_DISENGAGE,
                 LEN.AUTO_DISENGAGE,
                 0x00,
                 0x00,
                 title='AutoDisengage',
                 name='auto_disengage',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE // 8), CheckByte(),),),
        BitField(FID.AUTO_DISENGAGE_DEFAULT,
                 LEN.AUTO_DISENGAGE_DEFAULT,
                 0x00,
                 0x00,
                 title='AutoDisengageDefault',
                 name='auto_disengage_default',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE_DEFAULT // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SmartShift.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, wheel_mode, auto_disengage, auto_disengage_default):
        """
        Constructor

        @param  device_index                [in] (int)  Device Index
        @param  feature_index               [in] (int)  Desired feature Id
        @param  wheel_mode                  [in] (int)  The target wheel mode
        @param  auto_disengage              [in] (int)  The speed at which the ratchet automatically disengages
        @param  auto_disengage_default      [in] (int)  The default value of the autoDisengage setting
        """
        super(SetRatchetControlModeResponse, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.wheel_mode = wheel_mode
        self.auto_disengage = auto_disengage
        self.auto_disengage_default = auto_disengage_default
    # end def __init__

# end class SetRatchetControlModeResponse

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
