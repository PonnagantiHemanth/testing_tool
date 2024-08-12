#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.usb.usbconstants
:brief: USB constants
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum

from logiusb_py.logiusb_constants import LogiusbEndpointDirection
from logiusb_py.logiusb_constants import LogiusbHidClassSpecificRequest
from logiusb_py.logiusb_constants import LogiusbRequestType
from logiusb_py.logiusb_constants import LogiusbStandardDeviceRequest
from logiusb_py.logiusb_constants import LogiusbStandardEndpointRequest
from logiusb_py.logiusb_constants import LogiusbStandardInterfaceRequest

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
# To avoid having the classes doubled, it is just wrapping the wanted class
RequestType = LogiusbRequestType
StandardDeviceRequest = LogiusbStandardDeviceRequest
StandardInterfaceRequest = LogiusbStandardInterfaceRequest
StandardEndpointRequest = LogiusbStandardEndpointRequest
HidClassSpecificRequest = LogiusbHidClassSpecificRequest
EndpointDirection = LogiusbEndpointDirection


class VendorId(IntEnum):
    """
    USB VID known by the library.

    Source: https://www.usb.org/sites/default/files/vendor_ids033021.pdf
    """
    LOGITECH_INC = 0x046D
    NORDIC_SEMICONDUCTOR_ASA = 0x1915
    SEGGER_MICROCONTROLLER_SYSTEM_GMBH = 0x1366
    # Total Phase, Inc.
    TOTAL_PHASE = 0x1679
    TERMINUS_TECHNOLOGY_INC = 0x1A40  # For Phidgets
    MAAXTER = 0x248A  # For Telink probes
    # ST Microelectronics
    ST_MICROELECTRONICS = 0x0483
# end class VendorId


class ProductId(IntEnum):
    """
    USB PID known by the library.
    """
    NRF52_DK_V1 = 0x0105
    NRF52_DK_V2 = 0x1015
    NRF52_DK_V3 = 0x1051

    # Logitech Gotthard receiver
    LOGITECH_GOTTHARD_RECEIVER = 0xF013
    # USB Tools PID (0x5500-0x55FF)
    LOGITECH_GRAVITON_EMULATOR = 0x555A
    # Logitech Crush-pad receiver
    LOGITECH_CRUSH_RECEIVER = 0xC53A

    # J-link Identifier
    SEGGER_J_LINK = 0x0101
    SEGGER_J_LINK_PLUS = 0x1020
    # Beagle USB 480 Protocol Analyzer TP1126-695756Identifier
    BEAGLE_USB_480 = 0x2001
    # TELINK Probe (Maxxter) Identifier
    TELINK_MAXXTER = 0x8266
    # ST Link V2
    ST_LINK_V2_PROBE = 0x3748
# end class ProductId


class LogitechReceiverProductId(IntEnum):
    """
    Logitech USB PID for user receivers (gotthard is NOT a user receiver and therefore is not in this enumeration).

    This list is taken from ccp_fw/lfa/logitech_id/usb_vid_pid.h in the section ``Receivers PID (0xC500-0xC5FF)``
    """
    NANO_FS = 0xC526
    LORELEI = 0xC527
    KIWI = 0xC529
    DELL_NAUSICAA = 0xC52A
    UNIFYING = 0xC52B
    BERING = 0xC52D
    GURAMI = 0xC52E
    BICKY_DAGGY = 0xC52F
    DELL_VIOLET = 0xC530
    KENNY = 0xC531
    ANKH = 0xC532
    TOSHIBA_BEIJING = 0xC533
    DAGGAMI = 0xC534
    DELL_AQUA = 0xC535
    DELL_COBALT = 0xC536
    ALLSPARK = 0xC537
    BERING_CR = 0xC538
    GOLEM = 0xC539
    CRUSH = 0xC53A
    MORTAL = 0xC53B
    IMMORTAL = 0xC53C
    BEASTBOY = 0xC53D
    BONNIE = 0xC53E
    GOBBLET = 0xC53F
    HELLULAND = 0xC540
    GRAVITY = 0xC541
    NALINK = 0xC542
    GOLDUCK = 0xC543
    AVALONLINK = 0xC544
    GRAVITY_LS2_CA = 0xC545
    GRAVITY_BLE_PRO = 0xC546
    MEZZY_LS2_CA = 0xC547
    MEZZY_BLE_PRO = 0xC548
    GOBID = 0xC549
    QBERT_BLE_PRO = 0xC54B
    COILY_BLE_PRO = 0xC54C
    SAVITUCK = 0xC54D

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
    # end def has_value

    @classmethod
    def ble_pro_pids(cls):
        """
        Get all available BLE Pro PIDs

        :return: BLE Pro PIDs
        :rtype: ``tuple[LogitechReceiverProductId]``
        """
        return (
            cls.GRAVITY_BLE_PRO,
            cls.MEZZY_BLE_PRO,
            cls.QBERT_BLE_PRO,
            cls.COILY_BLE_PRO,
        )
    # end def ble_pro_pids

    @classmethod
    def unifying_pids(cls):
        """
        Get all available Unifying PIDs

        :return: Unifying PIDS
        :rtype: ``tuple[LogitechReceiverProductId]``
        """
        return (
            cls.UNIFYING,
            cls.GOLEM,
            cls.CRUSH,
            cls.GRAVITY,
            cls.GOLDUCK,
            cls.GRAVITY_LS2_CA,
            cls.MEZZY_LS2_CA,
            cls.SAVITUCK,
        )
    # end def unifying_pids

    @classmethod
    def uhs_pids(cls):
        """
        Get the list of PID of the receivers supporting the UHS protocol

        :return: PIDS of receiver supporting the Ultra High Speed protocol
        :rtype: ``tuple[LogitechReceiverProductId]``
        """
        return (
            cls.SAVITUCK,
        )
    # end def uhs_pids
# end class LogitechReceiverProductId

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
