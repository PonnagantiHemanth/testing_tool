#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package    pyhid.hidpp.emulator.loadopticalsensordata

@brief  HID++ 2.0 Load Optical Sensor Data command interface definition

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

class LoadOpticalSensorData(HidppMessage):
    """
    Load Optical Sensor Data Features implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0xA001
    MAX_FUNCTION_INDEX = 0

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  Feature Index
        """
        super(LoadOpticalSensorData, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
    # end def __init__
# end class LoadOpticalSensorData


class CreateImmediateDisplacement(LoadOpticalSensorData):
    """
    LoadOpticalSensorData CreateImmediateDisplacement implementation class

    Create a single displacement event at a specific position (i.e. trigger index) in the stimuli sequence.
    The FPGA is programmed immediately with these values but the motion line is not yet asserted (This final action is
    done when the event is triggered).

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TriggerIndex           || 8            ||
    || XDisplacement          || 16           ||
    || YDisplacement          || 16           ||
    || Repetition             || 8            ||
    || Delay                  || 16           ||
    || Padding                || 64           ||
    """

    class FID(LoadOpticalSensorData.FID):
        """
        Field Identifiers
        """
        TRIGGER_INDEX = 0xFA
        X_DISPLACEMENT = 0xF9
        Y_DISPLACEMENT = 0xF8
        REPETITION = 0xF7
        DELAY = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(LoadOpticalSensorData.LEN):
        """
        Field Lengths
        """
        TRIGGER_INDEX = 0x08
        X_DISPLACEMENT = 0x10
        Y_DISPLACEMENT = 0x10
        REPETITION = 0x08
        DELAY = 0x10
        PADDING = 0x40
    # end class LEN

    FIELDS = LoadOpticalSensorData.FIELDS + (
        BitField(FID.TRIGGER_INDEX,
                 LEN.TRIGGER_INDEX,
                 0x00,
                 0x00,
                 title='TriggerIndex',
                 name='trigger_index',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.X_DISPLACEMENT,
                 LEN.X_DISPLACEMENT,
                 0x00,
                 0x00,
                 title='XDisplacement',
                 name='x_displacement',
                 checks=(CheckHexList(LEN.X_DISPLACEMENT // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.Y_DISPLACEMENT,
                 LEN.Y_DISPLACEMENT,
                 0x00,
                 0x00,
                 title='YDisplacement',
                 name='y_displacement',
                 checks=(CheckHexList(LEN.Y_DISPLACEMENT // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.REPETITION,
                 LEN.REPETITION,
                 0x00,
                 0x00,
                 title='Repetition',
                 name='repetition',
                 checks=(CheckHexList(LEN.REPETITION // 8),
                         CheckByte(),),),
        BitField(FID.DELAY,
                 LEN.DELAY,
                 0x00,
                 0x00,
                 title='Delay',
                 name='delay',
                 checks=(CheckHexList(LEN.DELAY // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=LoadOpticalSensorData.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, trigger_index, x_displacement, y_displacement, repetition, delay):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        @param  trigger_index          [in] (int)  Stimuli position in the test sequence
        @param  x_displacement         [in] (int)  Mouse X data to be injected
        @param  y_displacement         [in] (int)  Mouse Y data to be injected
        @param  repetition             [in] (int)  Number of repeated motion line assertions
        @param  delay                  [in] (int)  Timings in us to be added between two assertion
                                                   (ignored if repetition = 0)
        """
        super(CreateImmediateDisplacement, self).__init__(deviceIndex, featureId)

        self.functionIndex = CreateImmediateDisplacementResponse.FUNCTION_INDEX
        self.trigger_index = trigger_index
        self.x_displacement = x_displacement
        self.y_displacement = y_displacement
        self.repetition = repetition
        self.delay = delay
    # end def __init__
# end class CreateImmediateDisplacement


class CreateImmediateDisplacementResponse(LoadOpticalSensorData):
    """
    LoadOpticalSensorData CreateImmediateDisplacement response implementation class

    Acknowledges the immediate displacement trigger creation.

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
    REQUEST_LIST = (CreateImmediateDisplacement,)
    FUNCTION_INDEX = 0
    VERSION = (0,)

    class FID(LoadOpticalSensorData.FID):
        """
        Field Identifiers
        """
        PADDING = 0xF9
    # end class FID

    class LEN(LoadOpticalSensorData.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = LoadOpticalSensorData.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=LoadOpticalSensorData.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        """
        super(CreateImmediateDisplacementResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class CreateImmediateDisplacementResponse


class SensorPolledEvent(LoadOpticalSensorData):
    """
    LoadOpticalSensorData SensorPolledEvent implementation class

    This event reports sensor successful polling.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Status                 || 8            ||
    || MotionAssertedTS       || 16           ||
    || SensorPolledTS         || 16           ||
    || Padding                || 88           ||
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0
    VERSION = (0,)

    class FID(LoadOpticalSensorData.FID):
        """
        Field Identifiers
        """
        STATUS = 0xFA
        MOTION_ASSERTED_TS = 0xF9
        SENSOR_POLLED_TS = 0xF8
        DELTA_TIME = 0xF7
        PADDING = 0xF6
    # end class FID

    class LEN(LoadOpticalSensorData.LEN):
        """
        Field Lengths
        """
        STATUS = 0x08
        MOTION_ASSERTED_TS = 0x20
        SENSOR_POLLED_TS = 0x20
        DELTA_TIME = 0x20
        PADDING = 0x18
    # end class LEN

    FIELDS = LoadOpticalSensorData.FIELDS + (
        BitField(FID.STATUS,
                 LEN.STATUS,
                 0x00,
                 0x00,
                 title='Status',
                 name='status',
                 checks=(CheckHexList(LEN.STATUS // 8),
                         CheckByte(),),),
        BitField(FID.MOTION_ASSERTED_TS,
                 LEN.MOTION_ASSERTED_TS,
                 0x00,
                 0x00,
                 title='MotionAssertedTS',
                 name='motion_asserted_ts',
                 checks=(CheckHexList(LEN.MOTION_ASSERTED_TS // 8),
                         CheckInt(max_value=0xFFFFFFFF),), ),
        BitField(FID.SENSOR_POLLED_TS,
                 LEN.SENSOR_POLLED_TS,
                 0x00,
                 0x00,
                 title='SensorPolledTS',
                 name='sensor_polled_ts',
                 checks=(CheckHexList(LEN.SENSOR_POLLED_TS // 8),
                         CheckInt(max_value=0xFFFFFFFF),), ),
        BitField(FID.DELTA_TIME,
                 LEN.DELTA_TIME,
                 0x00,
                 0x00,
                 title='DeltaTime',
                 name='delta_time',
                 checks=(CheckHexList(LEN.DELTA_TIME // 8),
                         CheckInt(max_value=0xFFFFFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=LoadOpticalSensorData.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, status, motion_asserted_ts, sensor_polled_ts, delta_time):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  status                 [in] (int)  Sequence execution status:
                                                        - 0:success
                                                        - 1:timeout (2s timeout hardcoded in the FPGA)
        @param  motion_asserted_ts     [in] (int)  Timings in us where the motion line has been asserted.
        @param  sensor_polled_ts       [in] (int)  Timings in us where the device has polled the sensor.
        @param  delta_time       [in] (int)  delta from motion assertion timestamp to polling timestamp in us.
        """
        super(SensorPolledEvent, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.status = status
        self.motion_asserted_ts = motion_asserted_ts
        self.sensor_polled_ts = sensor_polled_ts
        self.delta_time = delta_time
    # end def __init__
# end class SensorPolledEvent

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
