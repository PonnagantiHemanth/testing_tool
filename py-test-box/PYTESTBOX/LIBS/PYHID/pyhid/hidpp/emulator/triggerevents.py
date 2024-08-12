#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package    pyhid.hidpp.emulator.triggerevents

@brief  HID++ 2.0 Trigger Events command interface definition

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

class TriggerEvents(HidppMessage):
    """
    Trigger Events Features implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0xA000
    MAX_FUNCTION_INDEX = 4

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  Feature Index
        """
        super(TriggerEvents, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
    # end def __init__
# end class TriggerEvents


class GenericAcknowledgeResponse(TriggerEvents):
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

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=TriggerEvents.DEFAULT.PADDING),
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


class GetTriggerCount(TriggerEvents):
    """
    TriggerEvents GetTriggerCount implementation class

    Request the maximum number of possible trigger in the emulator.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=TriggerEvents.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        """
        super(GetTriggerCount, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetTriggerCountResponse.FUNCTION_INDEX
    # end def __init__
# end class GetTriggerCount


class GetTriggerCountResponse(TriggerEvents):
    """
    TriggerEvents GetTriggerCount response implementation class

    Returns the maximum number of possible trigger in the emulator.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TriggerCount           || 8            ||
    || Padding                || 120          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetTriggerCount,)
    FUNCTION_INDEX = 0
    VERSION = (0,)

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        TRIGGER_COUNT = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        TRIGGER_COUNT = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.TRIGGER_COUNT,
                 LEN.TRIGGER_COUNT,
                 0x00,
                 0x00,
                 title='TriggerCount',
                 name='trigger_count',
                 checks=(CheckHexList(LEN.TRIGGER_COUNT // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=TriggerEvents.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, trigger_count):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  Desired feature Id
        @param  trigger_count          [in] (int)  The maximum number of possible trigger in the emulator.
        """
        super(GetTriggerCountResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.trigger_count = trigger_count
    # end def __init__
# end class GetTriggerCountResponse


class ClearTrigger(TriggerEvents):
    """
    TriggerEvents ClearTrigger implementation class

    Clear an entry.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TriggerIndex           || 8            ||
    || Padding                || 16           ||
    """

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        TRIGGER_INDEX = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        TRIGGER_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.TRIGGER_INDEX,
                 LEN.TRIGGER_INDEX,
                 0x00,
                 0x00,
                 title='TriggerIndex',
                 name='trigger_index',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=TriggerEvents.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, trigger_index):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  trigger_index          [in] (int)  Index of the trigger to clear
        """
        super(ClearTrigger, self).__init__(deviceIndex, featureId)

        self.functionIndex = ClearTriggerResponse.FUNCTION_INDEX
        self.trigger_index = trigger_index
    # end def __init__
# end class ClearTrigger


class ClearTriggerResponse(GenericAcknowledgeResponse):
    """
    TriggerEvents ClearTrigger response implementation class

    Acknowledges the trigger entry is cleared.

    Format: see GenericAcknowledgeResponse
    """
    REQUEST_LIST = (ClearTrigger,)
    FUNCTION_INDEX = 1
    VERSION = (0,)

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(ClearTriggerResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class ClearTriggerResponse


class TriggerSequence(TriggerEvents):
    """
    TriggerEvents TriggerSequence implementation class

    Trigger a sequence of stimuli starting from the one defined in the firstTriggerIndex input parameter to the one
    defined in the lastTriggerIndex input parameter.
    The sequence is played all at once (i.e. without any delay between them) if the delay is set to 0x0000 else a
    delay is applied between each of them.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || FirstTriggerIndex      || 8            ||
    || LastTriggerIndex       || 8            ||
    || Delay                  || 32           ||
    || Padding                || 80           ||
    """

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        FIRST_TRIGGER_INDEX = 0xFA
        LAST_TRIGGER_INDEX = 0xF9
        DELAY = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        FIRST_TRIGGER_INDEX = 0x08
        LAST_TRIGGER_INDEX = 0x08
        DELAY = 0x20
        PADDING = 0x50
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.FIRST_TRIGGER_INDEX,
                 LEN.FIRST_TRIGGER_INDEX,
                 0x00,
                 0x00,
                 title='FirstTriggerIndex',
                 name='first_trigger_index',
                 checks=(CheckHexList(LEN.FIRST_TRIGGER_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.LAST_TRIGGER_INDEX,
                 LEN.LAST_TRIGGER_INDEX,
                 0x00,
                 0x00,
                 title='LastTriggerIndex',
                 name='last_trigger_index',
                 checks=(CheckHexList(LEN.LAST_TRIGGER_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.DELAY,
                 LEN.DELAY,
                 0x00,
                 0x00,
                 title='Delay',
                 name='delay',
                 checks=(CheckHexList(LEN.DELAY // 8),
                         CheckInt(max_value=0xFFFFFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=TriggerEvents.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, first_trigger_index, last_trigger_index, delay):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  first_trigger_index    [in] (int)  First index of the triggers to start
        @param  last_trigger_index     [in] (int)  Last index of the triggers to start
        @param  delay                  [in] (int)  Time delay in us to apply between two stimuli
        """
        super(TriggerSequence, self).__init__(deviceIndex, featureId)

        self.functionIndex = TriggerSequenceResponse.FUNCTION_INDEX
        self.first_trigger_index = first_trigger_index
        self.last_trigger_index = last_trigger_index
        self.delay = delay
    # end def __init__
# end class TriggerSequence


class TriggerSequenceResponse(GenericAcknowledgeResponse):
    """
    TriggerEvents TriggerSequence response implementation class

    Acknowledges the trigger sequence is started.

    Format: see GenericAcknowledgeResponse
    """
    REQUEST_LIST = (TriggerSequence,)
    FUNCTION_INDEX = 2
    VERSION = (0,)

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(TriggerSequenceResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class TriggerSequenceResponse


class TriggerSingle(TriggerEvents):
    """
    TriggerEvents TriggerSingle implementation class

    Trigger a single stimuli referenced by its index.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || TriggerIndex           || 8            ||
    || Padding                || 16           ||
    """

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        TRIGGER_INDEX = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        TRIGGER_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.TRIGGER_INDEX,
                 LEN.TRIGGER_INDEX,
                 0x00,
                 0x00,
                 title='TriggerIndex',
                 name='trigger_index',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=TriggerEvents.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, trigger_index):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  trigger_index          [in] (int)  Index of the trigger to start
        """
        super(TriggerSingle, self).__init__(deviceIndex, featureId)

        self.functionIndex = TriggerSingleResponse.FUNCTION_INDEX
        self.trigger_index = trigger_index
    # end def __init__
# end class TriggerSingle


class TriggerSingleResponse(GenericAcknowledgeResponse):
    """
    TriggerEvents TriggerSingle response implementation class

    Acknowledges the trigger is started.

    Format: see GenericAcknowledgeResponse
    """
    REQUEST_LIST = (TriggerSingle,)
    FUNCTION_INDEX = 3
    VERSION = (0,)

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(TriggerSingleResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class TriggerSingleResponse


class TriggerList(TriggerEvents):
    """
    TriggerEvents TriggerList implementation class

    Trigger a list of stimuli referenced by their indexes.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || StimuliCount           || 8            ||
    || Delay                  || 32           ||
    || TriggerIndex0          || 8            ||
    || TriggerIndex1          || 8            ||
    || TriggerIndex2          || 8            ||
    || TriggerIndex3          || 8            ||
    || TriggerIndex4          || 8            ||
    || TriggerIndex5          || 8            ||
    || TriggerIndex6          || 8            ||
    || TriggerIndex7          || 8            ||
    || Padding                || 24           ||
    """

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        STIMULI_COUNT = 0xFA
        DELAY = 0xF9
        TRIGGER_INDEX_0 = 0xF8
        TRIGGER_INDEX_1 = 0xF7
        TRIGGER_INDEX_2 = 0xF6
        TRIGGER_INDEX_3 = 0xF5
        TRIGGER_INDEX_4 = 0xF4
        TRIGGER_INDEX_5 = 0xF3
        TRIGGER_INDEX_6 = 0xF2
        TRIGGER_INDEX_7 = 0xF1
        PADDING = 0xF0
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        STIMULI_COUNT = 0x08
        DELAY = 0x20
        TRIGGER_INDEX_0 = 0x08
        TRIGGER_INDEX_1 = 0x08
        TRIGGER_INDEX_2 = 0x08
        TRIGGER_INDEX_3 = 0x08
        TRIGGER_INDEX_4 = 0x08
        TRIGGER_INDEX_5 = 0x08
        TRIGGER_INDEX_6 = 0x08
        TRIGGER_INDEX_7 = 0x08
        PADDING = 0x18
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.STIMULI_COUNT,
                 LEN.STIMULI_COUNT,
                 0x00,
                 0x00,
                 title='StimuliCount',
                 name='stimuli_count',
                 checks=(CheckHexList(LEN.STIMULI_COUNT // 8),
                         CheckByte(),),),
        BitField(FID.DELAY,
                 LEN.DELAY,
                 0x00,
                 0x00,
                 title='Delay',
                 name='delay',
                 checks=(CheckHexList(LEN.DELAY // 8),
                         CheckInt(max_value=0xFFFFFFFF),), ),
        BitField(FID.TRIGGER_INDEX_0,
                 LEN.TRIGGER_INDEX_0,
                 0x00,
                 0x00,
                 title='TriggerIndex0',
                 name='trigger_index_0',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_0 // 8),
                         CheckByte(),),),
        BitField(FID.TRIGGER_INDEX_1,
                 LEN.TRIGGER_INDEX_1,
                 0x00,
                 0x00,
                 title='TriggerIndex1',
                 name='trigger_index_1',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_1 // 8),
                         CheckByte(),),),
        BitField(FID.TRIGGER_INDEX_2,
                 LEN.TRIGGER_INDEX_2,
                 0x00,
                 0x00,
                 title='TriggerIndex2',
                 name='trigger_index_2',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_2 // 8),
                         CheckByte(),),),
        BitField(FID.TRIGGER_INDEX_3,
                 LEN.TRIGGER_INDEX_3,
                 0x00,
                 0x00,
                 title='TriggerIndex3',
                 name='trigger_index_3',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_3 // 8),
                         CheckByte(),),),
        BitField(FID.TRIGGER_INDEX_4,
                 LEN.TRIGGER_INDEX_4,
                 0x00,
                 0x00,
                 title='TriggerIndex4',
                 name='trigger_index_4',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_4 // 8),
                         CheckByte(),),),
        BitField(FID.TRIGGER_INDEX_5,
                 LEN.TRIGGER_INDEX_5,
                 0x00,
                 0x00,
                 title='TriggerIndex5',
                 name='trigger_index_5',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_5 // 8),
                         CheckByte(),),),
        BitField(FID.TRIGGER_INDEX_6,
                 LEN.TRIGGER_INDEX_6,
                 0x00,
                 0x00,
                 title='TriggerIndex6',
                 name='trigger_index_6',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_6 // 8),
                         CheckByte(),),),
        BitField(FID.TRIGGER_INDEX_7,
                 LEN.TRIGGER_INDEX_7,
                 0x00,
                 0x00,
                 title='TriggerIndex7',
                 name='trigger_index_7',
                 checks=(CheckHexList(LEN.TRIGGER_INDEX_7 // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=TriggerEvents.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, stimuli_count, delay, trigger_index_0=0, trigger_index_1=0,
                 trigger_index_2=0, trigger_index_3=0, trigger_index_4=0, trigger_index_5=0, trigger_index_6=0,
                 trigger_index_7=0):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  stimuli_count          [in] (int)  Total number of stimuli to chain
        @param  delay                  [in] (int)  Time delay in us to apply between two stimuli
        @param  trigger_index_0        [in] (int)  First stimuli to release
        @param  trigger_index_1        [in] (int)  Second stimuli to release
        @param  trigger_index_2        [in] (int)  Third stimuli to release
        @param  trigger_index_3        [in] (int)  Forth stimuli to release
        @param  trigger_index_4        [in] (int)  Fifth stimuli to release
        @param  trigger_index_5        [in] (int)  Sixth stimuli to release
        @param  trigger_index_6        [in] (int)  Seventh stimuli to release
        @param  trigger_index_7        [in] (int)  Eighth stimuli to release
        """
        super(TriggerList, self).__init__(deviceIndex, featureId)

        self.functionIndex = TriggerListResponse.FUNCTION_INDEX
        self.stimuli_count = stimuli_count
        self.delay = delay
        self.trigger_index_0 = trigger_index_0
        self.trigger_index_1 = trigger_index_1
        self.trigger_index_2 = trigger_index_2
        self.trigger_index_3 = trigger_index_3
        self.trigger_index_4 = trigger_index_4
        self.trigger_index_5 = trigger_index_5
        self.trigger_index_6 = trigger_index_6
        self.trigger_index_7 = trigger_index_7
    # end def __init__
# end class TriggerList


class TriggerListResponse(GenericAcknowledgeResponse):
    """
    TriggerEvents TriggerList response implementation class

    Acknowledges the trigger list is started.

    Format: see GenericAcknowledgeResponse
    """
    REQUEST_LIST = (TriggerList,)
    FUNCTION_INDEX = 4
    VERSION = (0,)

    def __init__(self, deviceIndex, featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(TriggerListResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class TriggerListResponse


class EndOfSequenceEvent(TriggerEvents):
    """
    TriggerEvents EndOfSequenceEvent implementation class

    This event reports the end of stimuli sequence execution.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Status                 || 8            ||
    || Padding                || 16           ||
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0
    VERSION = (0,)

    class FID(TriggerEvents.FID):
        """
        Field Identifiers
        """
        STATUS = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(TriggerEvents.LEN):
        """
        Field Lengths
        """
        STATUS = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = TriggerEvents.FIELDS + (
        BitField(FID.STATUS,
                 LEN.STATUS,
                 0x00,
                 0x00,
                 title='Status',
                 name='status',
                 checks=(CheckHexList(LEN.STATUS // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=TriggerEvents.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, status):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  status                 [in] (int)  Sequence execution status:
                                                        - 0:success
                                                        - 1:any error

        """
        super(EndOfSequenceEvent, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.status = status
    # end def __init__
# end class EndOfSequenceEvent

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
