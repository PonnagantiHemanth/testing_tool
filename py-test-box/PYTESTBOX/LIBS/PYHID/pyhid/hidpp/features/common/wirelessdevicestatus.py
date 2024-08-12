#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.common.wirelessdevicestatus

@brief  HID++ 2.0 Wireless Device Status command interface definition

@author Stanislas Cottard

@date   2019/07/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class WirelessDeviceStatus(HidppMessage):
    """
    Wireless Device Status implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x1D4B
    MAX_FUNCTION_INDEX = 0

    # Wireless Device Status status values
    class Status:
        NO_STATUS = 0
        RECONNECTION = 1
    # end class Status

    # Wireless Device Status request values
    class Request:
        NO_REQUEST = 0
        SOFTWARE_RECONFIGURATION_NEEDED = 1
    # end class Request

    # Wireless Device Status reason values
    class Reason:
        UNKNOWN = 0
        POWER_SWITCH_ACTIVATED = 1
    # end class Reason

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index           [in] (int)  feature Index
        """
        super(WirelessDeviceStatus, self).__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class WirelessDeviceStatus


class WirelessDeviceStatusBroadcastEvent(WirelessDeviceStatus):
    """
    WirelessDeviceStatus WirelessDeviceStatusBroadcastEvent implementation class

    Sent by the device after a power-on reset.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Status                 || 8            ||
    || Request                || 8            ||
    || Reason                 || 8            ||
    || Padding                || 104          ||
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(WirelessDeviceStatus.FID):
        """
        Field Identifiers
        """
        STATUS = 0xFA
        REQUEST = 0xF9
        REASON = 0xF8
        PADDING = 0xF7

    # end class FID

    class LEN(WirelessDeviceStatus.LEN):
        """
        Field Lengths
        """
        STATUS = 0x08
        REQUEST = 0x08
        REASON = 0x08
        PADDING = 0x68

    # end class LEN

    FIELDS = WirelessDeviceStatus.FIELDS + (
        BitField(FID.STATUS,
                 LEN.STATUS,
                 0x00,
                 0x00,
                 title='Status',
                 name='status',
                 checks=(CheckHexList(LEN.STATUS // 8),
                         CheckByte(),),),
        BitField(FID.REQUEST,
                 LEN.REQUEST,
                 0x00,
                 0x00,
                 title='Request',
                 name='request',
                 checks=(CheckHexList(LEN.REQUEST // 8),
                         CheckByte(),),),
        BitField(FID.REASON,
                 LEN.REASON,
                 0x00,
                 0x00,
                 title='Reason',
                 name='reason',
                 checks=(CheckHexList(LEN.REASON // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=WirelessDeviceStatus.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_id, status, request, reason):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_id              [in] (int)  desired feature Id
        @param  status                  [in] (int)  Status of the wireless connection
        @param  request                 [in] (int)  Request
        @param  reason                  [in] (int)  Reason of the power-on reset
        """
        super(WirelessDeviceStatusBroadcastEvent, self).__init__(device_index, feature_id)

        self.functionIndex = self.FUNCTION_INDEX
        self.status = status
        self.request = request
        self.reason = reason
    # end def __init__
# end class WirelessDeviceStatusBroadcastEvent

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
