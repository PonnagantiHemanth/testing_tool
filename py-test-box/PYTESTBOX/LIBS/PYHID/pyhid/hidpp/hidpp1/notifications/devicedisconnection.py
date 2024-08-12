#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.devicedisconnection
    :brief: HID++ 1.0 Device Disconnection event interface definition
    :author: Stanislas Cottard
    :date: 2019/10/31
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceDisconnection(Hidpp1Message):
    """
    This class defines the format of Device Disconnection event.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || DisconnectionType      || 8            ||
    || Padding                || 24           ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.DEVICE_DISCONNECTION

    PERMANENT_DISCONNECTION = 0x02

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        DISCONNECTION_TYPE = 0xFC
        PADDING = 0xFB
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        DISCONNECTION_TYPE = 0x08
        PADDING = 0x18
    # end class LEN

    FIELDS = (
        BitField(FID.REPORT_ID,
                 LEN.REPORT_ID,
                 title='ReportID',
                 name='report_id',
                 default_value=Hidpp1Message.DEFAULT.REPORT_ID,
                 checks=(CheckHexList(LEN.REPORT_ID // 8), CheckByte(),)),
        BitField(FID.DEVICE_INDEX,
                 LEN.DEVICE_INDEX,
                 title='DeviceIndex',
                 name='device_index',
                 aliases=('pairing_slot',),
                 checks=(CheckHexList(LEN.DEVICE_INDEX // 8), CheckByte(),)),
        BitField(FID.SUB_ID,
                 LEN.SUB_ID,
                 title='SubID',
                 name='sub_id',
                 checks=(CheckHexList(LEN.SUB_ID // 8), CheckByte(),)),
        BitField(FID.DISCONNECTION_TYPE,
                 LEN.DISCONNECTION_TYPE,
                 0x00,
                 0x00,
                 title='DisconnectionType',
                 name='disconnection_type',
                 checks=(CheckHexList(LEN.DISCONNECTION_TYPE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, disconnection_type):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param disconnection_type: The disconnection type
        :type disconnection_type: ``int or HexList``
        """
        super(DeviceDisconnection, self).__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.disconnection_type = disconnection_type
    # end def __init__
# end class DeviceDisconnection

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
