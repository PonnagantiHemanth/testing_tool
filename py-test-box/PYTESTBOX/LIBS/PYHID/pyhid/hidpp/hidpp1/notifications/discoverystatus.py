#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.discoverystatus
    :brief: HID++ 1.0 Discovery change notification definition
    :author: Martin Cryonnet
    :date: 2020/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DiscoveryStatus(Hidpp1Message):
    """
    This class defines the format of Discovery change notification

    Format:
    || @b Name                              || @b Bit count ||
    || ReportID                             || 8            ||
    || DeviceIndex                          || 8            ||
    || SUB ID                               || 8            ||
    || Device Discovery Status Reserved     || 7            ||
    || Device Discovery Status              || 1            ||
    || Error Type                           || 8            ||
    || Padding                              || 8            ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.DISCOVERY_STATUS

    class DeviceDiscoveryStatus(IntEnum):
        """
        Device Discovery Status values
        """
        START = 0x00
        CANCEL = 0x01
        STOP = 0x02
    # end class DeviceDiscoveryStatus

    class ErrorType(IntEnum):
        """
        Error Type values
        """
        NO_ERROR = 0x00
        TIMEOUT = 0x01
        FAILED = 0x02
    # end class ErrorType

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        DEVICE_DISCOVERY_STATUS = Hidpp1Message.FID.SUB_ID - 1
        ERROR_TYPE = DEVICE_DISCOVERY_STATUS - 1
        PADDING = ERROR_TYPE - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        DEVICE_DISCOVERY_STATUS = 0x08
        ERROR_TYPE = 0x08
        PADDING = 0x10
    # end class LEN

    class DEFAULT(Hidpp1Message.DEFAULT):
        """
        Field default value
        """
        DEVICE_DISCOVERY_STATUS = 0x00
        ERROR_TYPE = 0x00
    # end class DEFAULT

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.DEVICE_DISCOVERY_STATUS,
                 LEN.DEVICE_DISCOVERY_STATUS,
                 title='DeviceDiscoveryStatus',
                 name='device_discovery_status',
                 default_value=DEFAULT.DEVICE_DISCOVERY_STATUS,
                 checks=(CheckHexList(LEN.DEVICE_DISCOVERY_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_DISCOVERY_STATUS) - 1),)),
        BitField(FID.ERROR_TYPE,
                 LEN.ERROR_TYPE,
                 title='ErrorType',
                 name='error_type',
                 default_value=DEFAULT.ERROR_TYPE,
                 checks=(CheckHexList(LEN.ERROR_TYPE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ERROR_TYPE) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, device_index, device_discovery_status, error_type):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param device_discovery_status: Device Discovery Status
        :type device_discovery_status: ``int``
        :param error_type: Error Type
        :type error_type: ``int``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.device_discovery_status = device_discovery_status
        self.error_type = error_type
    # end def __init__
# end class DeviceRecovery

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
