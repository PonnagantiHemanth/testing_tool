#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package    pyhid.hidpp.emulator.configurebuttons

@brief  HID++ 2.0 Configure Buttons command interface definition

@author Stanislas Cottard

@date   2019/05/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class ConfigureButtons(HidppMessage):
    """
    Configure Buttons Features implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0xA002
    MAX_FUNCTION_INDEX = 3

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  Feature Index
        """
        super(ConfigureButtons, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
    # end def __init__
# end class LoadOpticalSensorData


class GenericAcknowledgeResponse(ConfigureButtons):
    """
    Generic acknowledge response implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 128          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    VERSION = (0,)

    class FID(ConfigureButtons.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(ConfigureButtons.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = ConfigureButtons.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=ConfigureButtons.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GenericAcknowledgeResponse, self).__init__(deviceIndex, featureId)
    # end def __init__
# end class GenericAcknowledgeResponse


class GetButtonTableInfo(ConfigureButtons):
    """
    ConfigureButtons GetButtonTableInfo implementation class

    Request the maximum number of tables and points per table managed by the emulator.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(ConfigureButtons.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(ConfigureButtons.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ConfigureButtons.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=ConfigureButtons.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        """
        super(GetButtonTableInfo, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetButtonTableInfoResponse.FUNCTION_INDEX
    # end def __init__
# end class GetButtonTableInfo


class GetButtonTableInfoResponse(ConfigureButtons):
    """
    ConfigureButtons GetButtonTableInfo response implementation class

    Returns the maximum number of tables and points per table managed by the emulator.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TableIdCount           || 8            ||
    || PointsPerTable         || 8            ||
    || Padding                || 112          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetButtonTableInfo,)
    FUNCTION_INDEX = 0
    VERSION = (0,)

    class FID(ConfigureButtons.FID):
        """
        Field Identifiers
        """
        TABLE_ID_COUNT = 0xFA
        POINTS_PER_TABLE = 0xF9
        PADDING = 0xF8
    # end class FID

    class LEN(ConfigureButtons.LEN):
        """
        Field Lengths
        """
        TABLE_ID_COUNT = 0x08
        POINTS_PER_TABLE = 0x08
        PADDING = 0x70
    # end class LEN

    FIELDS = ConfigureButtons.FIELDS + (
        BitField(FID.TABLE_ID_COUNT,
                 LEN.TABLE_ID_COUNT,
                 0x00,
                 0x00,
                 title='TableIdCount',
                 name='table_id_count',
                 checks=(CheckHexList(LEN.TABLE_ID_COUNT // 8),
                         CheckByte(),),),
        BitField(FID.POINTS_PER_TABLE,
                 LEN.POINTS_PER_TABLE,
                 0x00,
                 0x00,
                 title='PointsPerTable',
                 name='points_per_table',
                 checks=(CheckHexList(LEN.POINTS_PER_TABLE // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=ConfigureButtons.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, table_id_count, points_per_table):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        @param  table_id_count         [in] (int)  Number of tables available
        @param  points_per_table       [in] (int)  Maximum number of points (same for each table)
        """
        super(GetButtonTableInfoResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.table_id_count = table_id_count
        self.points_per_table = points_per_table
    # end def __init__
# end class GetButtonTableInfoResponse


class CreateSimpleEvent(ConfigureButtons):
    """
    ConfigureButtons CreateSimpleEvent implementation class

    Create a simple key pressed event (i.e. single make or break on a simple gpio) at a specific position
    (i.e. trigger index) in the stimuli sequence.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TriggerIndex           || 8            ||
    || Gpio                   || 8            ||
    || polarity               || 8            ||
    || Padding                || 104          ||
    """

    class FID(ConfigureButtons.FID):
        """
        Field Identifiers
        """
        TRIGGER_INDEX = 0xFA
        GPIO = 0xF9
        POLARITY = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(ConfigureButtons.LEN):
        """
        Field Lengths
        """
        TRIGGER_INDEX = 0x08
        GPIO = 0x08
        POLARITY = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = ConfigureButtons.FIELDS + (
        BitField(FID.TRIGGER_INDEX,
                 LEN.TRIGGER_INDEX,
                 0x00,
                 0x00,
                 title='TriggerIndex',
                 name='trigger_index',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.GPIO,
                 LEN.GPIO,
                 0x00,
                 0x00,
                 title='Gpio',
                 name='gpio',
                 checks=(CheckHexList(LEN.GPIO // 8),
                         CheckByte(),),),
        BitField(FID.POLARITY,
                 LEN.POLARITY,
                 0x00,
                 0x00,
                 title='Polarity',
                 name='polarity',
                 checks=(CheckHexList(LEN.POLARITY // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=ConfigureButtons.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, trigger_index, gpio, polarity):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        @param  trigger_index          [in] (int)  Stimuli position in the test sequence
        @param  gpio                   [in] (int)  Gpio position (TBD)
        @param  polarity               [in] (int)  0 / 1 (break/make device dependent)
        """
        super(CreateSimpleEvent, self).__init__(deviceIndex, featureId)

        self.functionIndex = CreateSimpleEventResponse.FUNCTION_INDEX
        self.trigger_index = trigger_index
        self.gpio = gpio
        self.polarity = polarity
    # end def __init__
# end class CreateSimpleEvent


class CreateSimpleEventResponse(GenericAcknowledgeResponse):
    """
    ConfigureButtons CreateSimpleEventResponse response implementation class

    Acknowledges the button simple event creation.

    Format: see GenericAcknowledgeResponse
    """
    REQUEST_LIST = (CreateSimpleEvent,)
    FUNCTION_INDEX = 1
    VERSION = (0,)

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        """
        super(CreateSimpleEventResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class CreateSimpleEventResponse


class CreateWaveformEvent(ConfigureButtons):
    """
    ConfigureButtons CreateWaveformEvent implementation class

    Create a simple key pressed event (i.e. single make or break on a simple gpio) at a specific position
    (i.e. trigger index) in the stimuli sequence.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TriggerIndex           || 8            ||
    || TableId                || 8            ||
    || Gpio                   || 8            ||
    || Padding                || 104          ||
    """

    class FID(ConfigureButtons.FID):
        """
        Field Identifiers
        """
        TRIGGER_INDEX = 0xFA
        TABLE_ID = 0xF9
        GPIO = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(ConfigureButtons.LEN):
        """
        Field Lengths
        """
        TRIGGER_INDEX = 0x08
        TABLE_ID = 0x08
        GPIO = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = ConfigureButtons.FIELDS + (
        BitField(FID.TRIGGER_INDEX,
                 LEN.TRIGGER_INDEX,
                 0x00,
                 0x00,
                 title='TriggerIndex',
                 name='trigger_index',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.TABLE_ID,
                 LEN.TABLE_ID,
                 0x00,
                 0x00,
                 title='TableId',
                 name='table_id',
                 checks=(CheckHexList(LEN.TABLE_ID // 8),
                         CheckByte(),),),
        BitField(FID.GPIO,
                 LEN.GPIO,
                 0x00,
                 0x00,
                 title='Gpio',
                 name='gpio',
                 checks=(CheckHexList(LEN.GPIO // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=ConfigureButtons.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, trigger_index, table_id, gpio):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        @param  trigger_index          [in] (int)  Stimuli position in the test sequence
        @param  table_id               [in] (int)  Reference to the table storing the waveform points for this event.
        @param  gpio                   [in] (int)  Gpio position (TBD)
        """
        super(CreateWaveformEvent, self).__init__(deviceIndex, featureId)

        self.functionIndex = CreateWaveformEventResponse.FUNCTION_INDEX
        self.trigger_index = trigger_index
        self.table_id = table_id
        self.gpio = gpio
    # end def __init__
# end class CreateWaveformEvent


class CreateWaveformEventResponse(GenericAcknowledgeResponse):
    """
    ConfigureButtons CreateSimpleEvent response implementation class

    Acknowledges the button waveform event creation.

    Format: see GenericAcknowledgeResponse
    """
    REQUEST_LIST = (CreateWaveformEvent,)
    FUNCTION_INDEX = 2
    VERSION = (0,)

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        """
        super(CreateWaveformEventResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class CreateWaveformEventResponse


class ConfigureWaveformPoints(ConfigureButtons):
    """
    ConfigureButtons ConfigureWaveformPoints implementation class

    Create a simple key pressed event (i.e. single make or break on a simple gpio) at a specific position
    (i.e. trigger index) in the stimuli sequence.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TableId                || 8            ||
    || RowIndex               || 8            ||
    || Point0                 || 16           ||
    || Point1                 || 16           ||
    || Point2                 || 16           ||
    || Point3                 || 16           ||
    || Point4                 || 16           ||
    || Point5                 || 16           ||
    || Point6                 || 16           ||
    """

    class FID(ConfigureButtons.FID):
        """
        Field Identifiers
        """
        TABLE_ID = 0xFA
        ROW_INDEX = 0xF8
        POINT_0 = 0xF7
        POINT_1 = 0xF6
        POINT_2 = 0xF5
        POINT_3 = 0xF4
        POINT_4 = 0xF3
        POINT_5 = 0xF2
        POINT_6 = 0xF1
    # end class FID

    class LEN(ConfigureButtons.LEN):
        """
        Field Lengths
        """
        TABLE_ID = 0x08
        ROW_INDEX = 0x08
        POINT_0 = 0x10
        POINT_1 = 0x10
        POINT_2 = 0x10
        POINT_3 = 0x10
        POINT_4 = 0x10
        POINT_5 = 0x10
        POINT_6 = 0x10
    # end class LEN

    FIELDS = ConfigureButtons.FIELDS + (
        BitField(FID.TABLE_ID,
                 LEN.TABLE_ID,
                 0x00,
                 0x00,
                 title='TableId',
                 name='table_id',
                 checks=(CheckHexList(LEN.TABLE_ID // 8),
                         CheckByte(),),),
        BitField(FID.ROW_INDEX,
                 LEN.ROW_INDEX,
                 0x00,
                 0x00,
                 title='RowIndex',
                 name='row_index',
                 checks=(CheckHexList(LEN.ROW_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.POINT_0,
                 LEN.POINT_0,
                 0x00,
                 0x00,
                 title='Point0',
                 name='point_0',
                 checks=(CheckHexList(LEN.POINT_0 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.POINT_1,
                 LEN.POINT_1,
                 0x00,
                 0x00,
                 title='Point1',
                 name='point_1',
                 checks=(CheckHexList(LEN.POINT_1 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.POINT_2,
                 LEN.POINT_2,
                 0x00,
                 0x00,
                 title='Point2',
                 name='point_2',
                 checks=(CheckHexList(LEN.POINT_2 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.POINT_3,
                 LEN.POINT_3,
                 0x00,
                 0x00,
                 title='Point3',
                 name='point_3',
                 checks=(CheckHexList(LEN.POINT_3 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.POINT_4,
                 LEN.POINT_4,
                 0x00,
                 0x00,
                 title='Point4',
                 name='point_4',
                 checks=(CheckHexList(LEN.POINT_4 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.POINT_5,
                 LEN.POINT_5,
                 0x00,
                 0x00,
                 title='Point5',
                 name='point_5',
                 checks=(CheckHexList(LEN.POINT_5 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.POINT_6,
                 LEN.POINT_6,
                 0x00,
                 0x00,
                 title='Point6',
                 name='point_6',
                 checks=(CheckHexList(LEN.POINT_6 // 8),
                         CheckInt(max_value=0xFFFF),), ),
    )

    def __init__(self, deviceIndex, featureId, table_id, row_index, point_0=0, point_1=0, point_2=0, point_3=0,
                 point_4=0, point_5=0, point_6=0):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        @param  table_id               [in] (int)  Reference to the table storing the waveform points for this event.
        @param  row_index              [in] (int)  Index of the row to add / update.
        @param  point_0                [in] (int)  Point.
                                                    - 1 Msb: polarity bit (0 / 1) released or pressed depending on
                                                      device
                                                    - 15 Lsb: time in us during which the button is kept at a level
                                                      (up to 32 ms).

        @param  point_1                [in] (int)  Point.
        @param  point_2                [in] (int)  Point.
        @param  point_3                [in] (int)  Point.
        @param  point_4                [in] (int)  Point.
        @param  point_5                [in] (int)  Point.
        @param  point_6                [in] (int)  Point.

        NB:	function with rowIndex = 0 shall be called first
            pointX = 0x0000 End of Table
        """
        super(ConfigureWaveformPoints, self).__init__(deviceIndex, featureId)

        self.functionIndex = ConfigureWaveformPointsResponse.FUNCTION_INDEX
        self.table_id = table_id
        self.row_index = row_index
        self.point_0 = point_0
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3
        self.point_4 = point_4
        self.point_5 = point_5
        self.point_6 = point_6
    # end def __init__
# end class ConfigureWaveformPoints


class ConfigureWaveformPointsResponse(GenericAcknowledgeResponse):
    """
    ConfigureButtons ConfigureWaveformPoints response implementation class

    Acknowledges the button waveform points added.

    Format: see GenericAcknowledgeResponse
    """
    REQUEST_LIST = (ConfigureWaveformPoints,)
    FUNCTION_INDEX = 3
    VERSION = (0,)

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        """
        super(ConfigureWaveformPointsResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class ConfigureWaveformPointsResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
