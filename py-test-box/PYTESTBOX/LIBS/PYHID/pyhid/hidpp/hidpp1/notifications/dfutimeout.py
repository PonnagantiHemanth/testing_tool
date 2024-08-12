#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.dfutimeout
    :brief: HID++ 1.0 DFU Timeout interface definition
    :author: Stanislas Cottard
    :date: 2020/09/28
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
class DfuTimeout(Hidpp1Message):
    """
    This class defines the format of DFU Timeout notification

    This notification is used to indicate that the timeout to enter DFU mode has been reached.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Padding                       32
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.DFU_TIMEOUT

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        PADDING = Hidpp1Message.FID.SUB_ID - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        PADDING = 0x20
    # end class LEN

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index):
        """
        Constructor

        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
    # end def __init__
# end class DfuTimeout

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
