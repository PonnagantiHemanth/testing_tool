#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1814.functionality
:brief: HID++ 2.0 ``ChangeHost`` functionality test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import sys
from time import sleep
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.hidpp20.common.feature_1814.changehost import ChangeHostMultiReceiverTestCase
from pytestbox.device.hidpp20.common.feature_1814.changehost import ChangeHostTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
from pyusb.libusbdriver import ChannelIdentifier

_AUTHOR = "Kevin Dayet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostFunctionalityTestCase(ChangeHostTestCase):
    """
    Validate ``ChangeHost`` functionality test cases
    """

    @features('Feature1814TypeC')
    @level('Functionality')
    def test_validate_connect_by_type_c(self):
        """
        Validate connect host by type-c usb cable (Feature 0x1814)

        Change Host
         nbHost, currHost, flags [0]GetHostInfov1
         [1]SetCurrentHost
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable the type-c USB port")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCurrentHost with host_index=1")
        # --------------------------------------------------------------------------------------------------------------
        response = ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=1)
        if response is not None:
            LogHelper.log_info(self, f"SetCurrentHost Response: {str(response)}\n")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostInfo")
        # --------------------------------------------------------------------------------------------------------------
        response = ChangeHostTestUtils.HIDppHelper.get_host_info(
            self, device_index=ChannelUtils.get_device_index(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate GetHostInfo current Host value")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=int(Numeral(response.curr_host)),
                         msg='The currHost parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Disable the host 2 USB port")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1814_0001", _AUTHOR)
    # end def test_validate_connect_by_type_c
# end class ChangeHostFunctionalityTestCase


class ChangeHostMultiReceiverFunctionalityTestCase(ChangeHostMultiReceiverTestCase):
    """
    Validate ``ChangeHost`` with Multi Receivers functionality test cases
    """

    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    def test_set_to_connected_host(self):
        """
        Validate SetCurrentHost to a connected host (Feature 0x1814)
        Change Host
         nbHost, currHost, flags [0]GetHostInfov1
         [1]SetCurrentHost
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable the host 2 USB port")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCurrentHost with hostIndex=1")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=1)

        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(1), device_index=1),
            close_associated_channel=False)

        # Empty queue
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostInfo")
        # --------------------------------------------------------------------------------------------------------------
        response = ChangeHostTestUtils.HIDppHelper.get_host_info(
            self, device_index=ChannelUtils.get_device_index(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate GetHostInfo curr_host value")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=int(Numeral(response.curr_host)),
                         msg='The currHost parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Send SetCurrentHost with hostIndex=0")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=0)

        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(0), device_index=1),
            close_associated_channel=False,
            open_associated_channel=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Disable the host 2 USB port")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1814_0002", _AUTHOR)
        # end def test_set_to_connected_host

    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    def test_set_to_unconnected_host(self):
        """
        Validate SetCurrentHost to a unconnected host (Feature 0x1814)
        Change Host
         nbHost, currHost, flags [0]GetHostInfov1
         [1]SetCurrentHost
        """
        max_host_index = self.f.PRODUCT.DEVICE.F_NbHosts - 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Disable the host index {max_host_index} USB port")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_channel_enable = True
        self.device.disable_usb_port(self.host_number_to_port_index(max_host_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetCurrentHost with hostIndex = {max_host_index} (unconnected host)")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=max_host_index)
        sleep(5)

        # Switch communication channel to receiver on initial port
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel=self.current_channel,
            close_associated_channel=False,
            open_associated_channel=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostInfo")
        # --------------------------------------------------------------------------------------------------------------
        response = ChangeHostTestUtils.HIDppHelper.get_host_info(
            self, device_index=ChannelUtils.get_device_index(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate GetHostInfo current host value")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=self.port_index_to_host_number(port_index=ChannelUtils.get_port_index(test_case=self)),
            obtained=int(Numeral(response.curr_host)),
            msg='The currHost parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, f"Enable the host {max_host_index} USB port")
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(self.host_number_to_port_index(max_host_index))
        self.post_requisite_channel_enable = False

        self.testCaseChecked("FUN_1814_0003", _AUTHOR)
    # end def test_set_to_unconnected_host

    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    def test_enhanced_host_switch(self):
        """
        Validate SetCurrentHost to a unconnected host when connected with the host 1
                FW tries to connect the specified host then after no success:
                - switch to host 0 if enhanced host switch flag is enable
                - reconnect to original host 1 if enhanced host switch flag is disable
        Change Host
         nbHost, currHost, flags [0]GetHostInfov1
         [1]SetCurrentHost
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable the host 2 USB port")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_channel_enable = True
        self.device.disable_usb_port(self.host_number_to_port_index(2))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostInfo")
        # --------------------------------------------------------------------------------------------------------------
        response = ChangeHostTestUtils.HIDppHelper.get_host_info(
            self, device_index=ChannelUtils.get_device_index(test_case=self))
        self.logTrace('enhanced host switch  on/off flag = %d' % response.flags)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCookie with hostIndex=0 and cookie=0x11")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_cookie(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=0, cookie=0x11)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Test Step 2: Send SetCurrentHost with hostIndex=1")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=1)

        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(1), device_index=1),
            close_associated_channel=False)

        # Empty queue
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostInfo")
        # --------------------------------------------------------------------------------------------------------------
        response = ChangeHostTestUtils.HIDppHelper.get_host_info(
            self, device_index=ChannelUtils.get_device_index(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate GetHostInfo.currentHost value")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=int(Numeral(response.curr_host)),
                         msg='The currHost parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCurrentHost with hostIndex=2 (unconnected host)")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=2)
        sleep(3)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)

        if response.flags == 0:
            # Let the device some time to reconnect to the initial host 1
            sleep(1)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test Step 5: Send GetHostInfo")
            # ----------------------------------------------------------------------------------------------------------
            response = ChangeHostTestUtils.HIDppHelper.get_host_info(
                self, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate GetHostInfo currentHost value")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1,
                             obtained=int(Numeral(response.curr_host)),
                             msg='The currHost parameter differs from the one expected')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Send SetCurrentHost with hostIndex=0")
            # ----------------------------------------------------------------------------------------------------------
            ChangeHostTestUtils.HIDppHelper.set_current_host(
                self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=0)

            # Switch communication channel to receiver on port 0
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(0), device_index=1),
                open_associated_channel=False)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check channel switch to port 0 succeeded")
            # ----------------------------------------------------------------------------------------------------------
            # Switch communication channel to receiver on port 0
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(0), device_index=1),
                close_associated_channel=False,
                open_associated_channel=False)

            # Empty queue
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ChangeHost.GetHostInfo")
            # ----------------------------------------------------------------------------------------------------------
            response = ChangeHostTestUtils.HIDppHelper.get_host_info(
                self, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate GetHostInfo currentHost value")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=int(Numeral(response.curr_host)),
                             msg='The currHost parameter differs from the one expected')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Enable the host 2 USB port")
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(self.host_number_to_port_index(2))
        self.post_requisite_channel_enable = False

        self.testCaseChecked("FUN_1814_0004", _AUTHOR)
    # end def test_enhanced_host_switch
# end class ChangeHostMultiReceiverFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
