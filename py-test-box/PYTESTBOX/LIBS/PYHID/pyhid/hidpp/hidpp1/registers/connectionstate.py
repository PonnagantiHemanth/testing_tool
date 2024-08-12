#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.connectionstate
    :brief: HID++ 1.0 Connection state registers definition
    :author: Christophe Roquebert
    :date: 2020/02/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse
from pyhid.hidpp.hidpp1.setgetregister import GetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegisterRequest
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConnectionStateModel(BaseRegisterModel):
    """
    TODO
    """
    @classmethod
    def _get_data_model(cls):
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetConnectionStateRequest,
                "response": SetConnectionStateResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": GetConnectionStateRequest,
                "response": GetConnectionStateResponse
            }
        }
    # end def _get_data_model
# end def ConnectionStateModel


class SetConnectionStateRequest(SetRegister):
    """
    Writing this register allowsthe SW to take an action on the connection scheme
    """

    class FID(SetRegister.FID):
        """
        Field Identifiers
        """
        WRITE_ACTION_ON_CONNECTION_STATE_RESERVED = SetRegister.FID.ADDRESS - 1
        WRITE_ACTION_ON_CONNECTION_FAKE_CTRL_ALT_F12 = WRITE_ACTION_ON_CONNECTION_STATE_RESERVED - 1
        WRITE_ACTION_ON_CONNECTION_FAKE_DEVICE_ARRIVAL = WRITE_ACTION_ON_CONNECTION_FAKE_CTRL_ALT_F12 - 1
        WRITE_ACTION_ON_CONNECTION_FAKE_CONNECT_BUTTON = WRITE_ACTION_ON_CONNECTION_FAKE_DEVICE_ARRIVAL - 1
        PADDING = WRITE_ACTION_ON_CONNECTION_FAKE_CONNECT_BUTTON - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Field Lengths in bits
        """
        WRITE_ACTION_ON_CONNECTION_STATE_RESERVED = 0x05
        WRITE_ACTION_ON_CONNECTION_FAKE_CTRL_ALT_F12 = 0x01
        WRITE_ACTION_ON_CONNECTION_FAKE_DEVICE_ARRIVAL = 0x01
        WRITE_ACTION_ON_CONNECTION_FAKE_CONNECT_BUTTON = 0x01
        PADDING = 0x10
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.WRITE_ACTION_ON_CONNECTION_STATE_RESERVED,
                 LEN.WRITE_ACTION_ON_CONNECTION_STATE_RESERVED,
                 title='WriteActionOnConnectionStateReserved',
                 name='write_action_on_connection_state_reserved',
                 checks=(CheckHexList(LEN.WRITE_ACTION_ON_CONNECTION_STATE_RESERVED // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.WRITE_ACTION_ON_CONNECTION_STATE_RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.WRITE_ACTION_ON_CONNECTION_FAKE_CTRL_ALT_F12,
                 LEN.WRITE_ACTION_ON_CONNECTION_FAKE_CTRL_ALT_F12,
                 title='WriteActionOnConnectionStateFakeCtrlAltF12',
                 name='write_action_on_connection_fake_ctrl_alt_f12',
                 checks=(CheckHexList(LEN.WRITE_ACTION_ON_CONNECTION_FAKE_CTRL_ALT_F12 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.WRITE_ACTION_ON_CONNECTION_FAKE_CTRL_ALT_F12) - 1),)),
        BitField(FID.WRITE_ACTION_ON_CONNECTION_FAKE_DEVICE_ARRIVAL,
                 LEN.WRITE_ACTION_ON_CONNECTION_FAKE_DEVICE_ARRIVAL,
                 title='WriteActionOnConnectionStateFakeDeviceArrival',
                 name='write_action_on_connection_fake_device_arrival',
                 checks=(CheckHexList(LEN.WRITE_ACTION_ON_CONNECTION_FAKE_DEVICE_ARRIVAL // 8),
                         CheckInt(min_value=0, max_value=pow(2,
                                                             LEN.WRITE_ACTION_ON_CONNECTION_FAKE_DEVICE_ARRIVAL) - 1),)),
        BitField(FID.WRITE_ACTION_ON_CONNECTION_FAKE_CONNECT_BUTTON,
                 LEN.WRITE_ACTION_ON_CONNECTION_FAKE_CONNECT_BUTTON,
                 title='WriteActionOnConnectionStateFakeConnectButton',
                 name='write_action_on_connection_fake_connect_button',
                 checks=(CheckHexList(LEN.WRITE_ACTION_ON_CONNECTION_FAKE_CONNECT_BUTTON // 8),
                         CheckInt(min_value=0, max_value=pow(2,
                                                             LEN.WRITE_ACTION_ON_CONNECTION_FAKE_CONNECT_BUTTON) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self,
                 write_action_on_connection_fake_ctrl_alt_f12=0,
                 write_action_on_connection_fake_device_arrival=0, write_action_on_connection_fake_connect_button=0):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.CONNECTION_STATE)

        self.write_action_on_connection_fake_ctrl_alt_f12 = write_action_on_connection_fake_ctrl_alt_f12
        self.write_action_on_connection_fake_device_arrival = write_action_on_connection_fake_device_arrival
        self.write_action_on_connection_fake_connect_button = write_action_on_connection_fake_connect_button
    # end def __init__
# end class SetConnectionStateRequest


class SetConnectionStateResponse(SetRegisterResponse):
    """
    Writing this register allowsthe SW to take an action on the connection scheme
    """
    ADDRESS = Hidpp1Data.Hidpp1RegisterAddress.CONNECTION_STATE

    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.CONNECTION_STATE)
    # end def __init__
# end class SetConnectionStateResponse


class GetConnectionStateRequest(GetRegisterRequest):
    """
    Reading this register allows to get information about the connection state
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.CONNECTION_STATE)
    # end def __init__
# end class GetConnectionStateRequest


class GetConnectionStateResponse(GetRegister):
    """
    Reading this register allows to get information about the connection state
    """
    ADDRESS = Hidpp1Data.Hidpp1RegisterAddress.CONNECTION_STATE

    class FID(GetRegister.FID):
        """
        Field Identifiers
        """
        READ_NUMBER_CONNECTED_DEVICES = GetRegister.FID.ADDRESS - 1
        READ_NUMBER_REMAINING_PAIRING_SLOTS = READ_NUMBER_CONNECTED_DEVICES - 1
        PADDING = READ_NUMBER_REMAINING_PAIRING_SLOTS - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        READ_NUMBER_CONNECTED_DEVICES = 0x08
        READ_NUMBER_REMAINING_PAIRING_SLOTS = 0x08
        PADDING = 0x08
    # end class LEN

    class DEFAULT(GetRegister.DEFAULT):
        """
        Fields default values
        """
    # end class DEFAULT

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.READ_NUMBER_CONNECTED_DEVICES,
                 LEN.READ_NUMBER_CONNECTED_DEVICES,
                 title='ReadNumberConnectedDevices',
                 name='read_number_connected_devices',
                 checks=(CheckHexList(LEN.READ_NUMBER_CONNECTED_DEVICES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.READ_NUMBER_CONNECTED_DEVICES) - 1),)),
        BitField(FID.READ_NUMBER_REMAINING_PAIRING_SLOTS,
                 LEN.READ_NUMBER_REMAINING_PAIRING_SLOTS,
                 title='ReadNumberRemainingPairingSlots',
                 name='read_number_remaining_pairing_slots',
                 checks=(CheckHexList(LEN.READ_NUMBER_REMAINING_PAIRING_SLOTS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.READ_NUMBER_REMAINING_PAIRING_SLOTS) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, read_number_connected_devices=0,
                 read_number_remaining_pairing_slots=0):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.CONNECTION_STATE)

        self.read_number_connected_devices = read_number_connected_devices
        self.read_number_remaining_pairing_slots = read_number_remaining_pairing_slots
    # end def __init__
# end class SetConnectionStateResponse

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
