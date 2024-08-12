#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.bleservicechanged
    :brief: HID++ 1.0 BLE Service Changed interface definition
    :author: Martin Cryonnet
    :date: 2020/06/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from pyhid.bitfield import BitField
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleServiceChanged(Hidpp1Message):
    """
    This class defines the format of BLE Service Changed notification

    This notification is used to indicate the status of the pairing process.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    PairingSlot                   8
    ServiceChangedStatus          8
    Padding                       16
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.BLE_SERVICE_CHANGED

    class ServiceChangedStatus(IntEnum):
        """
        Service Changed Status values
        """
        START = 0x00
        END = 0x01
    # end class STATUS

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        PAIRING_SLOT = Hidpp1Message.FID.SUB_ID - 1
        SERVICE_CHANGED_STATUS = PAIRING_SLOT - 1
        PADDING = SERVICE_CHANGED_STATUS - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        PAIRING_SLOT = 0x08
        SERVICE_CHANGED_STATUS = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.PAIRING_SLOT,
                 LEN.PAIRING_SLOT,
                 title='PairingSlot',
                 name='pairing_slot',
                 checks=(CheckHexList(LEN.PAIRING_SLOT // 8), CheckByte(),),),
        BitField(FID.SERVICE_CHANGED_STATUS,
                 LEN.SERVICE_CHANGED_STATUS,
                 title='ServiceChangedStatus',
                 name='service_changed_status',
                 checks=(CheckHexList(LEN.SERVICE_CHANGED_STATUS // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, pairing_slot, service_changed_status):
        """
        Constructor

        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param pairing_slot: Pairing Slot
        :type pairing_slot: ``int`` or ``HexList``
        :param service_changed_status: Service Changed Status
        :type service_changed_status: ``int`` or ``HexList``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.pairing_slot = pairing_slot
        self.service_changed_status = service_changed_status
    # end def __init__
# end class BleServiceChanged


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
