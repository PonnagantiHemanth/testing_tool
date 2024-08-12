#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.usbhubutils
:brief: Test Case Utils: wrapper around LibusbDriver to control the USB HUB ports ON/OFF states
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/04/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from time import sleep
from unittest import TestCase

from pytransport.usb.usbhub.smartusbhub import SmartUsbHub
from pytransport.usb.usbhub.usbhubconstants import UsbHubAction
from pyusb.libusbdriver import LibusbDriver


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class UsbHubTestCaseUtils(TestCase):
    """
    Test Case Utils: wrapper around LibusbDriver to control the USB HUB ports ON/OFF states
    """
    _smart_hub: SmartUsbHub

    @classmethod
    def setUpClass(cls):
        """
        Initialize the USB HUB library and select the Phidget USB hub.
        """
        super().setUpClass()
        cls._smart_hub = LibusbDriver.discover_usb_hub()[0]
    # end def setUpClass

    @classmethod
    def set_usb_port(cls, port_index, status, delay=None):
        """
        Set the power state of the given USB HUB port.

        :param port_index: Port index on the hub, from 1 (rightmost) to 7 (leftmost)
        :type port_index: ``int``
        :param status: ON/OFF status of the port
        :type status: ``UsbHubAction``
        :param delay: Delay after status change, defaults to None - OPTIONAL
        :type delay: ``None or int or float``
        """
        cls._smart_hub.set_usb_ports_status(port_index=port_index, status=status)
        if delay:
            sleep(delay)
        # end if
    # end def set_usb_port
# end class UsbHubTestCaseUtils


class UsbHubTestCaseUtilsTestCase(UsbHubTestCaseUtils):
    """
    USB HUB Utils Unitary Test Class.

    The test class provides an easy way to set the power state of any USB HUB port, directly from PyCharm IDE.
    """
    DELAY_S = 1  # 1-second delay after power on step and between power cycle steps

    # -------------------------------- PORT 1 --------------------------------

    def test_power_on_port_1(self):
        """
        Power ON the USB port 1
        """
        self.set_usb_port(port_index=1, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_on_port_1

    def test_power_off_port_1(self):
        """
        Power OFF the USB port 1
        """
        self.set_usb_port(port_index=1, status=UsbHubAction.OFF)
    # end def test_power_off_port_1

    def test_power_cycle_port_1(self):
        """
        Power CYCLE the USB port 1
        """
        self.set_usb_port(port_index=1, status=UsbHubAction.OFF, delay=self.DELAY_S)
        self.set_usb_port(port_index=1, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_cycle_port_1

    # -------------------------------- PORT 2 --------------------------------

    def test_power_on_port_2(self):
        """
        Power ON the USB port 2
        """
        self.set_usb_port(port_index=2, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_on_port_2

    def test_power_off_port_2(self):
        """
        Power OFF the USB port 2
        """
        self.set_usb_port(port_index=2, status=UsbHubAction.OFF)
    # end def test_power_off_port_2

    def test_power_cycle_port_2(self):
        """
        Power CYCLE the USB port 2
        """
        self.set_usb_port(port_index=2, status=UsbHubAction.OFF, delay=self.DELAY_S)
        self.set_usb_port(port_index=2, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_cycle_port_2

    # -------------------------------- PORT 3 --------------------------------

    def test_power_on_port_3(self):
        """
        Power ON the USB port 3
        """
        self.set_usb_port(port_index=3, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_on_port_3

    def test_power_off_port_3(self):
        """
        Power OFF the USB port 3
        """
        self.set_usb_port(port_index=3, status=UsbHubAction.OFF)
    # end def test_power_off_port_3

    def test_power_cycle_port_3(self):
        """
        Power CYCLE the USB port 3
        """
        self.set_usb_port(port_index=3, status=UsbHubAction.OFF, delay=self.DELAY_S)
        self.set_usb_port(port_index=3, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_cycle_port_3

    # -------------------------------- PORT 4 --------------------------------

    def test_power_on_port_4(self):
        """
        Power ON the USB port 4
        """
        self.set_usb_port(port_index=4, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_on_port_4

    def test_power_off_port_4(self):
        """
        Power OFF the USB port 4
        """
        self.set_usb_port(port_index=4, status=UsbHubAction.OFF)
    # end def test_power_off_port_4

    def test_power_cycle_port_4(self):
        """
        Power CYCLE the USB port 4
        """
        self.set_usb_port(port_index=4, status=UsbHubAction.OFF, delay=self.DELAY_S)
        self.set_usb_port(port_index=4, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_cycle_port_4

    # -------------------------------- PORT 5 --------------------------------

    def test_power_on_port_5(self):
        """
        Power ON the USB port 5
        """
        self.set_usb_port(port_index=5, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_on_port_5

    def test_power_off_port_5(self):
        """
        Power OFF the USB port 5
        """
        self.set_usb_port(port_index=5, status=UsbHubAction.OFF)
    # end def test_power_off_port_5

    def test_power_cycle_port_5(self):
        """
        Power CYCLE the USB port 5
        """
        self.set_usb_port(port_index=5, status=UsbHubAction.OFF, delay=self.DELAY_S)
        self.set_usb_port(port_index=5, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_cycle_port_5

    # -------------------------------- PORT 6 --------------------------------

    def test_power_on_port_6(self):
        """
        Power ON the USB port 6
        """
        self.set_usb_port(port_index=6, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_on_port_6

    def test_power_off_port_6(self):
        """
        Power OFF the USB port 6
        """
        self.set_usb_port(port_index=6, status=UsbHubAction.OFF)
    # end def test_power_off_port_6

    def test_power_cycle_port_6(self):
        """
        Power CYCLE the USB port 6
        """
        self.set_usb_port(port_index=6, status=UsbHubAction.OFF, delay=self.DELAY_S)
        self.set_usb_port(port_index=6, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_cycle_port_6

    # -------------------------------- PORT 7 --------------------------------

    def test_power_on_port_7(self):
        """
        Power ON the USB port 7
        """
        self.set_usb_port(port_index=7, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_on_port_7

    def test_power_off_port_7(self):
        """
        Power OFF the USB port 7
        """
        self.set_usb_port(port_index=7, status=UsbHubAction.OFF)
    # end def test_power_off_port_7

    def test_power_cycle_port_7(self):
        """
        Power CYCLE the USB port 7
        """
        self.set_usb_port(port_index=7, status=UsbHubAction.OFF, delay=self.DELAY_S)
        self.set_usb_port(port_index=7, status=UsbHubAction.ON, delay=self.DELAY_S)
    # end def test_power_cycle_port_7
# end class UsbHubTestCaseUtilsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
