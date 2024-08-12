#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.linkqualityinfo
    :brief: HID++ 1.0 Link Quality Info event interface definition
    :author: Stanislas Cottard
    :date: 2019/08/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.field import CheckInt
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class LinkQualityInfoShort(Hidpp1Message):
    """
    This class defines the format of Link Quality Info short event.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SubID                  || 8            ||
    || EventType              || 8            ||
    || Channel                || 6            ||
    || Counter                || 2            ||
    || LastLinkLossDuration   || 8            ||
    || AgilityHops            || 4            ||
    || Repetitions            || 4            ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.LINK_QUALITY_INFO_SHORT

    class FID(object):
        """
        Field Identifiers
        """
        EVENT_TYPE = 0xFC
        CHANNEL = 0xFB
        COUNTER = 0xFA
        LAST_LINK_LOSS_DURATION = 0xF9
        AGILITY_HOPS = 0xF8
        REPETITIONS = 0xF7
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        EVENT_TYPE = 0x08
        CHANNEL = 0x06
        COUNTER = 0x02
        LAST_LINK_LOSS_DURATION = 0x08
        AGILITY_HOPS = 0x04
        REPETITIONS = 0x04
    # end class LEN

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.EVENT_TYPE,
                 LEN.EVENT_TYPE,
                 0x00,
                 0x00,
                 title='EventType',
                 name='event_type',
                 checks=(CheckHexList(LEN.EVENT_TYPE // 8), CheckByte(),)),
        BitField(FID.CHANNEL,
                 LEN.CHANNEL,
                 0x00,
                 0x00,
                 title='Channel',
                 name='channel',
                 checks=(CheckInt(0, pow(2, LEN.CHANNEL) - 1),)),
        BitField(FID.COUNTER,
                 LEN.COUNTER,
                 0x00,
                 0x00,
                 title='Counter',
                 name='counter',
                 checks=(CheckInt(0, pow(2, LEN.COUNTER) - 1),)),
        BitField(FID.LAST_LINK_LOSS_DURATION,
                 LEN.LAST_LINK_LOSS_DURATION,
                 0x00,
                 0x00,
                 title='LastLinkLossDuration',
                 name='last_link_loss_duration',
                 checks=(CheckHexList(LEN.LAST_LINK_LOSS_DURATION // 8), CheckByte(),)),
        BitField(FID.AGILITY_HOPS,
                 LEN.AGILITY_HOPS,
                 0x00,
                 0x00,
                 title='AgilityHops',
                 name='agility_hops',
                 checks=(CheckInt(0, pow(2, LEN.AGILITY_HOPS) - 1),)),
        BitField(FID.REPETITIONS,
                 LEN.REPETITIONS,
                 0x00,
                 0x00,
                 title='Repetitions',
                 name='repetitions',
                 checks=(CheckInt(0, pow(2, LEN.REPETITIONS) - 1),)),
    )

    def __init__(self, device_index, event_type, channel, counter, last_link_loss_duration, agility_hops,
                 repetitions):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  event_type              [in] (int)  The type of link quality information event
        @param  channel                 [in] (int)  Link channel
        @param  last_link_loss_duration [in] (int)  Last link loss duration, in ms. 0xFF means > 254ms
        @param  agility_hops            [in] (int)  Agility hops
        @param  repetitions             [in] (int)  Repetitions
        """
        super(LinkQualityInfoShort, self).__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.event_type = event_type
        self.channel = channel
        self.counter = counter
        self.last_link_loss_duration = last_link_loss_duration
        self.agility_hops = agility_hops
        self.repetitions = repetitions
    # end def __init__
# end class LinkQualityInfoShort


class LinkQualityInfoLong(Hidpp1Message):
    """
    This class defines the format of Link Quality Info long event.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SubID                  || 8            ||
    || NumberOfRecords        || 8            ||
    || RecordDeviceIndex1     || 8            ||
    || EventType1             || 8            ||
    || Channel1               || 6            ||
    || Counter1               || 2            ||
    || LastLinkLossDuration1  || 8            ||
    || AgilityHops1           || 4            ||
    || Repetitions1           || 4            ||
    || RecordDeviceIndex2     || 8            ||
    || EventType2             || 8            ||
    || Channel2               || 6            ||
    || Counter2               || 2            ||
    || LastLinkLossDuration2  || 8            ||
    || AgilityHops2           || 4            ||
    || Repetitions2           || 4            ||
    || RecordDeviceIndex3     || 8            ||
    || EventType3             || 8            ||
    || Channel3               || 6            ||
    || Counter3               || 2            ||
    || LastLinkLossDuration3  || 8            ||
    || AgilityHops3           || 4            ||
    || Repetitions3           || 4            ||
    || Padding                || 8            ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.LINK_QUALITY_INFO_LONG

    class FID(object):
        """
        Field Identifiers
        """
        NUMBER_OF_RECORDS = 0xFC
        RECORD_DEVICE_INDEX_1 = 0xFB
        EVENT_TYPE_1 = 0xFA
        CHANNEL_1 = 0xF9
        COUNTER_1 = 0xF8
        LAST_LINK_LOSS_DURATION_1 = 0xF7
        AGILITY_HOPS_1 = 0xF6
        REPETITIONS_1 = 0xF5
        RECORD_DEVICE_INDEX_2 = 0xF4
        EVENT_TYPE_2 = 0xF3
        CHANNEL_2 = 0xF2
        COUNTER_2 = 0xF1
        LAST_LINK_LOSS_DURATION_2 = 0xF0
        AGILITY_HOPS_2 = 0xEF
        REPETITIONS_2 = 0xEE
        RECORD_DEVICE_INDEX_3 = 0xED
        EVENT_TYPE_3 = 0xEC
        CHANNEL_3 = 0xEB
        COUNTER_3 = 0xEA
        LAST_LINK_LOSS_DURATION_3 = 0xE9
        AGILITY_HOPS_3 = 0xE8
        REPETITIONS_3 = 0xE7
        PADDING = 0xE6
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        NUMBER_OF_RECORDS = 0x08
        RECORD_DEVICE_INDEX = 0x08
        EVENT_TYPE = 0x08
        CHANNEL = 0x06
        COUNTER = 0x02
        LAST_LINK_LOSS_DURATION = 0x08
        AGILITY_HOPS = 0x04
        REPETITIONS = 0x04
        PADDING = 0x08
    # end class LEN

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.NUMBER_OF_RECORDS,
                 LEN.NUMBER_OF_RECORDS,
                 0x00,
                 0x00,
                 title='NumberOfRecords',
                 name='number_of_records',
                 checks=(CheckHexList(LEN.NUMBER_OF_RECORDS // 8), CheckByte(),)),
        BitField(FID.RECORD_DEVICE_INDEX_1,
                 LEN.RECORD_DEVICE_INDEX,
                 0x00,
                 0x00,
                 title='RecordDeviceIndex1',
                 name='record_device_index_1',
                 checks=(CheckHexList(LEN.RECORD_DEVICE_INDEX // 8), CheckByte(),)),
        BitField(FID.EVENT_TYPE_1,
                 LEN.EVENT_TYPE,
                 0x00,
                 0x00,
                 title='EventType1',
                 name='event_type_1',
                 checks=(CheckHexList(LEN.EVENT_TYPE // 8), CheckByte(),)),
        BitField(FID.CHANNEL_1,
                 LEN.CHANNEL,
                 0x00,
                 0x00,
                 title='Channel1',
                 name='channel_1',
                 checks=(CheckInt(0, pow(2, LEN.CHANNEL) - 1),)),
        BitField(FID.COUNTER_1,
                 LEN.COUNTER,
                 0x00,
                 0x00,
                 title='Counter1',
                 name='counter_1',
                 checks=(CheckInt(0, pow(2, LEN.COUNTER) - 1),)),
        BitField(FID.LAST_LINK_LOSS_DURATION_1,
                 LEN.LAST_LINK_LOSS_DURATION,
                 0x00,
                 0x00,
                 title='LastLinkLossDuration1',
                 name='last_link_loss_duration_1',
                 checks=(CheckHexList(LEN.LAST_LINK_LOSS_DURATION // 8), CheckByte(),)),
        BitField(FID.AGILITY_HOPS_1,
                 LEN.AGILITY_HOPS,
                 0x00,
                 0x00,
                 title='AgilityHops1',
                 name='agility_hops_1',
                 checks=(CheckInt(0, pow(2, LEN.AGILITY_HOPS) - 1),)),
        BitField(FID.REPETITIONS_1,
                 LEN.REPETITIONS,
                 0x00,
                 0x00,
                 title='Repetitions1',
                 name='repetitions_1',
                 checks=(CheckInt(0, pow(2, LEN.REPETITIONS) - 1),)),
        BitField(FID.RECORD_DEVICE_INDEX_2,
                 LEN.RECORD_DEVICE_INDEX,
                 0x00,
                 0x00,
                 title='RecordDeviceIndex2',
                 name='record_device_index_2',
                 checks=(CheckHexList(LEN.RECORD_DEVICE_INDEX // 8), CheckByte(),)),
        BitField(FID.EVENT_TYPE_2,
                 LEN.EVENT_TYPE,
                 0x00,
                 0x00,
                 title='EventType2',
                 name='event_type_2',
                 checks=(CheckHexList(LEN.EVENT_TYPE // 8), CheckByte(),)),
        BitField(FID.CHANNEL_2,
                 LEN.CHANNEL,
                 0x00,
                 0x00,
                 title='Channel2',
                 name='channel_2',
                 checks=(CheckInt(0, pow(2, LEN.CHANNEL) - 1),)),
        BitField(FID.COUNTER_2,
                 LEN.COUNTER,
                 0x00,
                 0x00,
                 title='Counter2',
                 name='counter_2',
                 checks=(CheckInt(0, pow(2, LEN.COUNTER) - 1),)),
        BitField(FID.LAST_LINK_LOSS_DURATION_2,
                 LEN.LAST_LINK_LOSS_DURATION,
                 0x00,
                 0x00,
                 title='LastLinkLossDuration2',
                 name='last_link_loss_duration_2',
                 checks=(CheckHexList(LEN.LAST_LINK_LOSS_DURATION // 8), CheckByte(),)),
        BitField(FID.AGILITY_HOPS_2,
                 LEN.AGILITY_HOPS,
                 0x00,
                 0x00,
                 title='AgilityHops2',
                 name='agility_hops_2',
                 checks=(CheckInt(0, pow(2, LEN.AGILITY_HOPS) - 1),)),
        BitField(FID.REPETITIONS_2,
                 LEN.REPETITIONS,
                 0x00,
                 0x00,
                 title='Repetitions2',
                 name='repetitions_2',
                 checks=(CheckInt(0, pow(2, LEN.REPETITIONS) - 1),)),
        BitField(FID.RECORD_DEVICE_INDEX_3,
                 LEN.RECORD_DEVICE_INDEX,
                 0x00,
                 0x00,
                 title='RecordDeviceIndex3',
                 name='record_device_index_3',
                 checks=(CheckHexList(LEN.RECORD_DEVICE_INDEX // 8), CheckByte(),)),
        BitField(FID.EVENT_TYPE_3,
                 LEN.EVENT_TYPE,
                 0x00,
                 0x00,
                 title='EventType3',
                 name='event_type_3',
                 checks=(CheckHexList(LEN.EVENT_TYPE // 8), CheckByte(),)),
        BitField(FID.CHANNEL_3,
                 LEN.CHANNEL,
                 0x00,
                 0x00,
                 title='Channel3',
                 name='channel_3',
                 checks=(CheckInt(0, pow(2, LEN.CHANNEL) - 1),)),
        BitField(FID.COUNTER_3,
                 LEN.COUNTER,
                 0x00,
                 0x00,
                 title='Counter3',
                 name='counter_3',
                 checks=(CheckInt(0, pow(2, LEN.COUNTER) - 1),)),
        BitField(FID.LAST_LINK_LOSS_DURATION_3,
                 LEN.LAST_LINK_LOSS_DURATION,
                 0x00,
                 0x00,
                 title='LastLinkLossDuration3',
                 name='last_link_loss_duration_3',
                 checks=(CheckHexList(LEN.LAST_LINK_LOSS_DURATION // 8), CheckByte(),)),
        BitField(FID.AGILITY_HOPS_3,
                 LEN.AGILITY_HOPS,
                 0x00,
                 0x00,
                 title='AgilityHops3',
                 name='agility_hops_3',
                 checks=(CheckInt(0, pow(2, LEN.AGILITY_HOPS) - 1),)),
        BitField(FID.REPETITIONS_3,
                 LEN.REPETITIONS,
                 0x00,
                 0x00,
                 title='Repetitions3',
                 name='repetitions_3',
                 checks=(CheckInt(0, pow(2, LEN.REPETITIONS) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckInt(0, pow(2, LEN.PADDING) - 1),),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, number_of_records, record_device_index_1, event_type_1, channel_1, counter_1,
                 last_link_loss_duration_1, agility_hops_1, repetitions_1, record_device_index_2, event_type_2,
                 channel_2, counter_2, last_link_loss_duration_2, agility_hops_2, repetitions_2, record_device_index_3,
                 event_type_3, channel_3, counter_3, last_link_loss_duration_3, agility_hops_3, repetitions_3):
        """
        Constructor

        @param  device_index              [in] (int)  Device Index (it is supposed to be 0xFF, but for tests the
                                                      possibility of another value is accepted)
        @param  number_of_records         [in] (int)  Number of record in the notification
        @param  record_device_index_1     [in] (int)  Device index of the first record
        @param  event_type_1              [in] (int)  First type of link quality information event
        @param  channel_1                 [in] (int)  First information link channel
        @param  counter_1                 [in] (int)  First information link counter
        @param  last_link_loss_duration_1 [in] (int)  First information last link loss duration, in ms.
                                                        0xFF means > 254ms
        @param  agility_hops_1            [in] (int)  First information agility hops
        @param  repetitions_1             [in] (int)  First information repetitions
        @param  record_device_index_2     [in] (int)  Device index of the second record
        @param  event_type_2              [in] (int)  Second type of link quality information event
        @param  channel_2                 [in] (int)  Second information link channel
        @param  counter_2                 [in] (int)  Second information link counter
        @param  last_link_loss_duration_2 [in] (int)  Second information last link loss duration, in ms.
                                                        0xFF means > 254ms
        @param  agility_hops_2            [in] (int)  Second information agility hops
        @param  repetitions_2             [in] (int)  Second information repetitions
        @param  record_device_index_3     [in] (int)  Device index of the third record
        @param  event_type_3              [in] (int)  Third type of link quality information event
        @param  channel_3                 [in] (int)  Third information link channel
        @param  counter_3                 [in] (int)  Third information link counter
        @param  last_link_loss_duration_3 [in] (int)  Third information last link loss duration, in ms.
                                                        0xFF means > 254ms
        @param  agility_hops_3            [in] (int)  Third information agility hops
        @param  repetitions_3             [in] (int)  Third information repetitions
        """
        super(LinkQualityInfoLong, self).__init__()

        self.report_id = Hidpp1Message.DEFAULT.REPORT_ID_LONG
        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.number_of_records = number_of_records
        self.record_device_index_1 = record_device_index_1
        self.event_type_1 = event_type_1
        self.channel_1 = channel_1
        self.counter_1 = counter_1
        self.last_link_loss_duration_1 = last_link_loss_duration_1
        self.agility_hops_1 = agility_hops_1
        self.repetitions_1 = repetitions_1
        self.record_device_index_2 = record_device_index_2
        self.event_type_2 = event_type_2
        self.channel_2 = channel_2
        self.counter_2 = counter_2
        self.last_link_loss_duration_2 = last_link_loss_duration_2
        self.agility_hops_2 = agility_hops_2
        self.repetitions_2 = repetitions_2
        self.record_device_index_3 = record_device_index_3
        self.event_type_3 = event_type_3
        self.channel_3 = channel_3
        self.counter_3 = counter_3
        self.last_link_loss_duration_3 = last_link_loss_duration_3
        self.agility_hops_3 = agility_hops_3
        self.repetitions_3 = repetitions_3
    # end def __init__
# end class LinkQualityInfoLong

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
