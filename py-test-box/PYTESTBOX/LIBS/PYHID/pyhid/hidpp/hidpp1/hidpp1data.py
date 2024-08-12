#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.hidpp1data
    :brief: HID++ 1.0 Set Register Data
    :author: Martin Cryonnet
    :date: 2020/03/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class Hidpp1Data:
    """
    HID++ 1.0 Generic Data
    """
    class DeviceIndex(IntEnum):
        """
        Device Index in HID++
        """
        TRANSCEIVER = 0xFF
    # end class DeviceIndex

    class Offset(IntEnum):
        """
        Offsets of generic fields in HID++ 1.0
        """
        SUB_ID = 0x02
        REGISTER_ADDRESS = 0x03
        REGISTER_R0 = 0x04
        REGISTER_R1 = 0x05
        REGISTER_R2 = 0x06
    # end class Offset

    class Hidpp1RegisterSubId(IntEnum):
        """
        Register Sub Ids
        """
        SET_REGISTER = 0x80
        GET_REGISTER = 0x81
        SET_LONG_REGISTER = 0x82
        GET_LONG_REGISTER = 0x83
        SET_VERY_LONG_REGISTER = 0x84
        GET_VERY_LONG_REGISTER = 0x85
        ERROR_MSG = 0x8F
    # end class Hidpp1SubId

    class Hidpp1NotificationSubId(IntEnum):
        """
        Notifications Sub Ids
        """
        POWER_KEYS = 0x04
        ROLLER = 0x05
        DEVICE_DISCONNECTION = 0x40
        DEVICE_CONNECTION = 0x41
        LINK_QUALITY_INFO_LONG = 0x48
        LINK_QUALITY_INFO_SHORT = 0x49
        REQUEST_DISPLAY_PASSKEY = 0x4D
        DISPLAY_PASSKEY_KEY = 0x4E
        DEVICE_DISCOVERY = 0x4F
        DEVICE_RECOVERY = 0x52
        DISCOVERY_STATUS = 0x53
        PAIRING_STATUS = 0x54
        BLE_SERVICE_CHANGED = 0x55
        DFU_TIMEOUT = 0x56
    # end class Hidpp1Notification

    class Hidpp1RegisterAddress(IntEnum):
        """
        Register addresses
        """
        ENABLE_HIDPP_REPORTING = 0x00
        CONNECTION_STATE = 0x02
        QUAD_DEVICE_CONNECTION = 0xB2
        GET_RSSI = 0xB4
        NON_VOLATILE_PAIRING_INFORMATION = 0xB5
        PERFORM_DEVICE_DISCOVERY = 0xC0
        PERFORM_DEVICE_CONNECTION_DISCONNECTION = 0xC1
        TEST_MODE_CONTROL = 0xD0
        RF_REGISTER_ACCESS = 0xD1
        NON_VOLATILE_MEMORY_ACCESS = 0xD4
        NON_VOLATILE_MEMORY_OPERATION = 0xD7
        PREPAIRING_MANAGEMENT = 0xE7
        SET_LTK_KEY = 0xE8
        SET_IRK_KEY_CENTRAL = 0xE9
        SET_IRK_KEY_PERIPHERAL = 0xEA
        SET_CSRK_KEY_CENTRAL = 0xEB
        SET_CSRK_KEY_PERIPHERAL = 0xEC
        PREPAIRING_DATA = 0xED
        ENTER_FIRMWARE_UPGRADE_MODE = 0xF0
        RESET = 0xF2
        RECEIVER_FW_INFO = 0xF4
        DFU_CONTROL = 0xF5
        RANDOM_DATA = 0xF6
        START_SESSION = 0xF7
        PASSWORD = 0xF8
        MANAGE_DEACTIVATABLE_FEATURES_GET_INFO_AND_DISABLE_FEATURES = 0xF9
        MANAGE_DEACTIVATABLE_FEATURES_ENABLE_FEATURES = 0xFA
        UNIQUE_IDENTIFIER = 0xFB
    # end class Hidpp1RegisterAddress

    class DeviceType(IntEnum):
        """
        BLE Pro device pairing information - Device info - Device type values
        """
        UNKNOWN = 0x00
        KEYBOARD = 0x01
        MOUSE = 0x02
        NUM_PAD = 0x03
        PRESENTER = 0x04
        REMOTE_CONTROL = 0x07
        TRACK_BALL = 0x08
        TOUCH_PAD = 0x09
        TABLET = 0x0A
        GAME_PAD = 0x0B
        JOYSTICK = 0x0C
        DIAL = 0x0D
    # end class DeviceType
# end class Hidpp1Data

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
