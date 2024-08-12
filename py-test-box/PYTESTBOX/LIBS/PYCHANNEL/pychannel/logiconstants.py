#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pychannel.logiconstants
:brief: Set of constants that are specific to Logitech
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/11/22
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import Enum
from enum import IntEnum
from enum import auto

from pylibrary.tools.hexlist import HexList
from pytransport.ble.bleconstants import BleAdvertisementFlags
from pytransport.ble.bleconstants import BleAdvertisingDataType
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.bleconstants import BleGapAddressType
from pytransport.ble.bleconstants import BleUuidStandardService


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
class LogitechVendorUuid:
    """
    BLE++ services and applications UUID
    """
    BLE_PRO_CHAR_BASE = [0xFD, 0x72, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x01, 0x1F, 0x20, 0x00, 0x04, 0x6D]
    BLE_PRO_SERVICE = BLE_PRO_CHAR_BASE
    BLE_PRO_SERVICE_INFORMATION_CHARACTERISTIC = BLE_PRO_CHAR_BASE[:2] + [0x00, 0x01] + BLE_PRO_CHAR_BASE[4:]
    BLE_PRO_AUTHENTICATION_CAPABILITIES_CHARACTERISTIC = BLE_PRO_CHAR_BASE[:2] + [0x00, 0x02] + BLE_PRO_CHAR_BASE[4:]
    BLE_PRO_AUTHENTICATION_CONTROL_CHARACTERISTIC = BLE_PRO_CHAR_BASE[:2] + [0x00, 0x03] + BLE_PRO_CHAR_BASE[4:]
    BLE_PRO_DEVICE_INFORMATION_CHARACTERISTIC = BLE_PRO_CHAR_BASE[:2] + [0x00, 0x04] + BLE_PRO_CHAR_BASE[4:]
    BLE_PRO_ATTRIBUTE_CAPABILITY_CHARACTERISTIC = BLE_PRO_CHAR_BASE[:2] + [0x00, 0x05] + BLE_PRO_CHAR_BASE[4:]
    BLE_PRO_ATTRIBUTE_CONTROL_CHARACTERISTIC = BLE_PRO_CHAR_BASE[:2] + [0x00, 0x06] + BLE_PRO_CHAR_BASE[4:]

    BLEPP_APP_BASE = [0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x01, 0x1F, 0x20, 0x00, 0x04, 0x6D]
    APPLICATION_SERVICE = BLEPP_APP_BASE
    APPLICATION_CHARACTERISTIC = BLEPP_APP_BASE[:2] + [0x00, 0x01] + BLEPP_APP_BASE[4:]

    BLEPP_BOOT_BASE = [0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x01, 0x1F, 0x20, 0x00, 0x04, 0x6D]
    BOOTLOADER_SERVICE = BLEPP_BOOT_BASE
    BOOTLOADER_CHARACTERISTIC = BLEPP_BOOT_BASE[:2] + [0x00, 0x01] + BLEPP_BOOT_BASE[4:]
# end class LogitechVendorUuid


class LogitechBleConnectionParameters:
    """
    Logitech nominal values for connection parameters as a host.
    """
    # Values for BLE Pro receiver as a central role
    # Source:
    # https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/mpr01_gravity/+/refs/heads/master/config/lble_cfg_ref_receiver.h#104
    BLE_PRO_RECEIVER_CONNECTION_INTERVAL_MS = 7.5
    BLE_PRO_RECEIVER_SUPERVISION_TIMEOUT_MS = 1980
    BLE_PRO_RECEIVER_SLAVE_LATENCY = 66  # In number of connection events

    # Values recommended by a logitech device of the pointer type (Mouse, Presenter, Gamepad, Touchpad) for any OS
    # but iOS/iPadOS
    # Source:
    # https://spaces.logitech.com/x/8g7oCQ
    DEFAULT_OS_POINTER_CONNECTION_INTERVAL_MIN_MS = 7.5
    DEFAULT_OS_POINTER_CONNECTION_INTERVAL_MAX_MS = 11.25
    DEFAULT_OS_POINTER_SUPERVISION_TIMEOUT_MS = 2160
    DEFAULT_OS_POINTER_SLAVE_LATENCY = 44  # In number of connection events

    # Values recommended by a logitech device of the keyboard type for any OS but iOS/iPadOS
    # Source:
    # https://spaces.logitech.com/x/8g7oCQ
    DEFAULT_OS_KEYBOARD_CONNECTION_INTERVAL_MIN_MS = 20
    DEFAULT_OS_KEYBOARD_CONNECTION_INTERVAL_MAX_MS = 25
    DEFAULT_OS_KEYBOARD_SUPERVISION_TIMEOUT_MS = 2100
    DEFAULT_OS_KEYBOARD_SLAVE_LATENCY = 20  # In number of connection events

    # Values recommended by a logitech device of any type for iOS/iPadOS
    # Source:
    # https://spaces.logitech.com/x/8g7oCQ
    IOS_IPADOS_CONNECTION_INTERVAL_MIN_MS = 15
    IOS_IPADOS_CONNECTION_INTERVAL_MAX_MS = 15
    IOS_IPADOS_SUPERVISION_TIMEOUT_MS = 2000
    IOS_IPADOS_SLAVE_LATENCY = 30  # In number of connection events

    # Values recommended by a logitech device of any type in bootloader
    # Source:
    # https://spaces.logitech.com/x/8g7oCQ
    BOOTLOADER_CONNECTION_INTERVAL_MIN_MS = 7.5
    BOOTLOADER_CONNECTION_INTERVAL_MAX_MS = 7.5
    BOOTLOADER_SUPERVISION_TIMEOUT_MS = 1000
    BOOTLOADER_SLAVE_LATENCY = 33  # In number of connection events

    # Values of the Preferred Peripheral Connection Parameters Characteristic in Application
    # Note : Interval_Min and Interval_Max have a 1.25ms unit. Timeout has a 10ms unit.
    # Source:
    # https://spaces.logitech.com/x/6R9HCQ
    # Gamepad
    GPD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MIN = 6
    GPD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MAX = 6
    GPD_APPLICATION_CHARACTERISTIC_VALUE_LATENCY = 66
    GPD_APPLICATION_CHARACTERISTIC_VALUE_TIMEOUT = 214
    # Mouse & Touchpad
    MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MIN = 6
    MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MAX = 9
    MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_LATENCY = 44
    MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_TIMEOUT = 216
    # Keyboard
    KBD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MIN = 16
    KBD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MAX = 20
    KBD_APPLICATION_CHARACTERISTIC_VALUE_LATENCY = 20
    KBD_APPLICATION_CHARACTERISTIC_VALUE_TIMEOUT = 210

    # Values of the Preferred Peripheral Connection Parameters Characteristic in Bootloader
    # Note : Interval_Min and Interval_Max have a 1.25ms unit. Timeout has a 10ms unit.
    # Source:
    # https://spaces.logitech.com/x/6R9HCQ
    BOOTLOADER_CHARACTERISTIC_VALUE_INTERVAL_MIN = 6
    BOOTLOADER_CHARACTERISTIC_VALUE_INTERVAL_MAX = 6
    BOOTLOADER_CHARACTERISTIC_VALUE_LATENCY = 33
    BOOTLOADER_CHARACTERISTIC_VALUE_TIMEOUT = 100
# end class LogitechBleConnectionParameters


class BleProAuthenticationValues(IntEnum):
    """
    Values for Authentication characteristics of BLE Pro service
    """
    # Source:
    # https://docs.google.com/spreadsheets/d/1PW_wT5PmNeHsGw6s_URL0nYtBOh4q-kclZO6a_w8we4/edit?usp=sharing

    NO_AUTHENTICATION = 0x00
    KEYBOARD_PASSKEY = 0x01
    TWO_BUTTONS_PASSKEY = 0x02
# end class BleProAuthenticationValues


class BleAdvertisementModelSpecificFields(Enum):
    """
    List of fields in the advertising/scan response data that have model specific value IE names, tx power, appearances
    Note: the first few values are names with a set length stored in the enum data
    """
    NAME_9_CHAR = 9
    NAME_11_CHAR = 11
    NAME_14_CHAR = 14
    NAME_17_CHAR = 17
    NAME_FULL = auto()
    TX_POWER = auto()
    APPLICATION_APPEARANCE = auto()
    BOOTLOADER_APPEARANCE = auto()
    FAST_PAIR_DATA_FIELD = auto()
    BLE_PRO_DATA_FIELD = auto()
# end class BleAdvertisementModelSpecificFields


class BleAdvertisingDataConstants(Enum):
    """
    Generic constants for advertising data

    Source:
    https://spaces.logitech.com/x/gwAnDQ
    """
    SWIFT_PAIR_ADVERTISING_BEACON = HexList("0600030080")
# end class BleAdvertisingDataConstants


class BleAdvertisingInterval(IntEnum):
    """
    Possible interval values for ble advertising in milisecond
    source : https://spaces.logitech.com/x/gwAnDQ
    """
    HIGH_DUTY_CYCLE = -1 # set to -1 as not a raw value, need to be dealt with differently
    EXTRA_SHORT = 20
    SHORT = 30
    LONG = 100
# end class BleAdvertisingInterval


class BleAdvertisingSeriesStartTimeCategory(IntEnum):
    """
    Possible start times for ble advertising series in seconds
    source : https://spaces.logitech.com/x/gwAnDQ
    """
    START = 0  # when entering in discovery mode or reconnection or bootloader
    SECOND = 30  # starts when the first series end
    SECOND_INTERLACED = 32  # starts when the first series, when there is interlaced series
    INTERLACED = 2  # for interlaced series
    FAST_SECOND_BOOTLOADER = 5  # start after the bootloader, quickly
    SLOW_SECOND_BOOTLOADER = 20  # start after the bootloader, slowly
    THIRD_BOOTLOADER = 180  # start 3min after the bootloader, for long term advertising
# end class BleAdvertisingSeriesStartTimeCategory


class BleAdvertisingSeriesEndTimeCategory(IntEnum):
    """
    Possible stop times for ble advertising series in seconds
    source : https://spaces.logitech.com/x/gwAnDQ
    """
    EARLY = 30  # Ends quickly, usually for fast intervals series
    STANDARD = 180  # End of usual discovery  period (3min)
    RECONNECTION = 5  # End of reconnection period
    END_FAST_BOOTLOADER = 5  # End of fast bootloader reconnection period
    END_SLOW_BOOTLOADER = 7200  # End of slow bootloader reconnection period
# end class BleAdvertisingSeriesEndTimeCategory

class BleAdvertisingSeriesWindows(Enum):
    """
    Possible advertising windows for ble advertising series tuple of active period and repetition length, in seconds
    source : https://spaces.logitech.com/x/gwAnDQ
    """
    INTERLACED_ALTERNATING = (2, 4)
    PREPARING = (1.28, 6.28)
    RECONNECTION_HIGH_DUTY_CYCLE = (1.28, 1.28)
    BOOTLOADER_ALTERNATING_LONG = (15, 16)
    BOOTLOADER_ALTERNATING_SHORT = (1, 16)
    WHOLE_PERIOD = None
# end class BleAdvertisingSeriesWindows


class BleAdvertisingSeriesDefinition:
    """
    Definition of a single advertising series
    """
    def __init__(self, packet, scan_response, interval, adv_type, start, stop, window):
        """
        :param packet: Dictionary describing the advertising packet format, keys are ``BleAdvertisingDataType``
        :type packet: ``dict``
        :param scan_response: Dictionary describing the scan response packet format, keys are ``BleAdvertisingDataType``
        :type scan_response: ``dict``
        :param interval: Interval of advertising
        :type interval: ``BleAdvertisingInterval``
        :param adv_type: Type of advertisement
        :type adv_type: ``BleAdvertisingPduType``
        :param start: Time the series starts
        :type start: ``BleAdvertisingSeriesStartTimeCategory``
        :param stop: Time the series stops
        :type stop: ``BleAdvertisingSeriesEndTimeCategory``
        :param window: Definition of the advertising windows during the series
        :type window: ``BleAdvertisingSeriesWindows``
        """
        self.packet = packet
        self.scan_response = scan_response
        self.interval = interval
        self.adv_type = adv_type
        self.start = start
        self.stop = stop
        self.window = window
    # end def __init__
# end class BleAdvertisingSeriesDefinition


class BleAdvertisingSeries(Enum):
    """
    Definitions of all ble advertising series, each label correspond to a ``BleAdvertisingSeriesDefinition``
    Source:
    https://spaces.logitech.com/x/gwAnDQ 1.1 Series & 2.2 Series
    """
    A = BleAdvertisingSeriesDefinition(packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
            BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA: BleAdvertisingDataConstants.SWIFT_PAIR_ADVERTISING_BEACON,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_11_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_17_CHAR,
        },
        interval=BleAdvertisingInterval.SHORT,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.EARLY,
        window=BleAdvertisingSeriesWindows.INTERLACED_ALTERNATING
    )

    B = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
            BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA: BleAdvertisingDataConstants.SWIFT_PAIR_ADVERTISING_BEACON,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_11_CHAR,
        },
        scan_response={
           BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_17_CHAR,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.SECOND_INTERLACED,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.INTERLACED_ALTERNATING
        )

    C = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.LOGITECH_BLE_PRO,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.FAST_PAIR_DATA_FIELD,
        },
        scan_response={
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_17_CHAR,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.INTERLACED,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.INTERLACED_ALTERNATING
    )
    D = BleAdvertisingSeriesDefinition(
        packet={},
        scan_response={},
        interval=BleAdvertisingInterval.HIGH_DUTY_CYCLE,
        adv_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.PREPARING
    )
    E = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: (BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
                                                                 BleUuidStandardService.LOGITECH_BLE_PRO),
            BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA: BleAdvertisingDataConstants.SWIFT_PAIR_ADVERTISING_BEACON,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_9_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_14_CHAR,
        },
        interval=BleAdvertisingInterval.SHORT,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.EARLY,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    F = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: (BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
                                                                 BleUuidStandardService.LOGITECH_BLE_PRO),
            BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA: BleAdvertisingDataConstants.SWIFT_PAIR_ADVERTISING_BEACON,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_9_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_14_CHAR,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.SECOND,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    G = BleAdvertisingSeriesDefinition(
        packet={},
        scan_response={},
        interval=BleAdvertisingInterval.HIGH_DUTY_CYCLE,
        adv_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.RECONNECTION,
        window=BleAdvertisingSeriesWindows.RECONNECTION_HIGH_DUTY_CYCLE
    )
    H = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.NON_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: (BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
                                                                 BleUuidStandardService.LOGITECH_BLE_PRO),
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_9_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_14_CHAR,
        },
        interval=BleAdvertisingInterval.EXTRA_SHORT,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.RECONNECTION,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    I = BleAdvertisingSeriesDefinition(
        packet={},
        scan_response={},
        interval=BleAdvertisingInterval.HIGH_DUTY_CYCLE,
        adv_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.END_FAST_BOOTLOADER,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    J = BleAdvertisingSeriesDefinition(
        packet={},
        scan_response={},
        interval=BleAdvertisingInterval.EXTRA_SHORT,
        adv_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.FAST_SECOND_BOOTLOADER,
        stop=BleAdvertisingSeriesEndTimeCategory.END_SLOW_BOOTLOADER,
        window=BleAdvertisingSeriesWindows.BOOTLOADER_ALTERNATING_LONG
    )
    K = BleAdvertisingSeriesDefinition(
        packet={},
        scan_response={},
        interval=BleAdvertisingInterval.HIGH_DUTY_CYCLE,
        adv_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.SLOW_SECOND_BOOTLOADER,
        stop=BleAdvertisingSeriesEndTimeCategory.END_SLOW_BOOTLOADER,
        window=BleAdvertisingSeriesWindows.BOOTLOADER_ALTERNATING_SHORT
    )
    L = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.BOOTLOADER_APPEARANCE,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_FULL,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.LOGITECH_BLE_PRO
        },
        scan_response={
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    M = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.BOOTLOADER_APPEARANCE,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_FULL,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.LOGITECH_BLE_PRO
        },
        scan_response={
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.THIRD_BOOTLOADER,
        stop=BleAdvertisingSeriesEndTimeCategory.END_SLOW_BOOTLOADER,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    N = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.BOOTLOADER_APPEARANCE,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_FULL,
        },
        scan_response={
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    O = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.FAST_PAIR_DATA_FIELD,
        },
        scan_response={
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.THIRD_BOOTLOADER,
        stop=BleAdvertisingSeriesEndTimeCategory.END_SLOW_BOOTLOADER,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    P = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.BOOTLOADER_APPEARANCE,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_FULL,
        },
        scan_response={
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_17_CHAR
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.INTERLACED,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.INTERLACED_ALTERNATING
    )
    Q = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
            BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA: BleAdvertisingDataConstants.SWIFT_PAIR_ADVERTISING_BEACON,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_9_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_14_CHAR,
        },
        interval=BleAdvertisingInterval.SHORT,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.EARLY,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    R = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
            BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA: BleAdvertisingDataConstants.SWIFT_PAIR_ADVERTISING_BEACON,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_9_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_14_CHAR,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.SECOND,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    S = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_11_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_17_CHAR
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.INTERLACED_ALTERNATING
    )
    T = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: (BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
                                                                 BleUuidStandardService.LOGITECH_BLE_PRO),
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_9_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.SERVICE_DATA: BleAdvertisementModelSpecificFields.BLE_PRO_DATA_FIELD,
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_14_CHAR
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
    U = BleAdvertisingSeriesDefinition(
        packet={
            BleAdvertisingDataType.FLAGS: BleAdvertisementFlags.LIMITED_DISCOVERABLE,
            BleAdvertisingDataType.APPEARANCE: BleAdvertisementModelSpecificFields.APPLICATION_APPEARANCE,
            BleAdvertisingDataType.SERVICE_16BIT_UUID_COMPLETE: BleUuidStandardService.HUMAN_INTERFACE_DEVICE,
            BleAdvertisingDataType.SHORT_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_9_CHAR,
        },
        scan_response={
            BleAdvertisingDataType.TX_POWER_LEVEL: BleAdvertisementModelSpecificFields.TX_POWER,
            BleAdvertisingDataType.COMPLETE_LOCAL_NAME: BleAdvertisementModelSpecificFields.NAME_14_CHAR,
        },
        interval=BleAdvertisingInterval.LONG,
        adv_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        start=BleAdvertisingSeriesStartTimeCategory.START,
        stop=BleAdvertisingSeriesEndTimeCategory.STANDARD,
        window=BleAdvertisingSeriesWindows.WHOLE_PERIOD
    )
# end class BleAdvertisingSeries


class LogitechBleConstants:
    """
    General constant that are just related to the BLE protocol for Logitech devices
    """
    # See Logitech advertising specification in the introduction:
    # https://spaces.logitech.com/x/7gPTBw
    ADDRESS_TYPE = BleGapAddressType.RANDOM_STATIC

    HIDPP_MESSAGE_SIZE = 19
    BLEPP_MESSAGE_SIZE = 18
# end class LogitechBleConstants


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
