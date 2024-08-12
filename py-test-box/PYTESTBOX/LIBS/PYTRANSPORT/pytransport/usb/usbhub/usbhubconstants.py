#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.usb.usbhub.usbhubconstants
:brief: USB hub constants
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import Enum
from enum import IntEnum

from pyraspi.raspi import Raspi
from pytransport.usb.usbconstants import VendorId


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class UsbHubVid(IntEnum):
    """
    USB hub VID known by the library.
    """
    PHIDGETS_VID = VendorId.TERMINUS_TECHNOLOGY_INC.value
# end class UsbHubVid


class UsbHubPid(IntEnum):
    """
    USB hub PID known by the library.
    """
    # Phidgets USB 2.0 Hub (7 ports) Identifier
    PHIDGETS_HUB0003_0_7_PORTS_PID = 0x0201
# end class UsbHubPid


class UsbHubAction(Enum):
    """
    USB hub actions known by the library.
    """
    ON = 'on'
    OFF = 'off'
# end class UsbHubAction


class UsbHubUtils(IntEnum):
    """
    USB hub useful constants.
    """
    PHIDGETS_HUB0003_NUMBER_PORTS = 7
    if Raspi.is_raspberry_pi_5():
        DEVICE_ON_HUB_PORT_PATH_DEPTH = 2
    else:
        DEVICE_ON_HUB_PORT_PATH_DEPTH = 3
    # end if
# end class UsbHubUtils

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
