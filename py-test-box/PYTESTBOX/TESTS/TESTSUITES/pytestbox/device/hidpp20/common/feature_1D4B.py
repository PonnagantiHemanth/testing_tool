#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.hid.common.feature_1D4B
:brief: Validate HID++ 2.0 ``WirelessDeviceStatus`` feature
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/07/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.bootloadertest import DeviceBootloaderTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.powermodeutils import PowerModesTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class WirelessDeviceStatusTestCase(BaseTestCase):
    """
    Validate Wireless Device Status TestCases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x1D4B)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)

        ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=WirelessDeviceStatusBroadcastEvent)
    # end def setUp

    def common_WirelessDeviceStatusBroadcastEventPowerUpPowerSupply(self):
        """
        Test the reception of an event when the DUT is powered up. This is the common method for Application and
        Bootloader.
        """
        # Gaming device need to switch channel form wireless to USB cable connection in order to enter bootloader mode.
        # The test script shall be skipped for this case.
        if self.config_manager.current_protocol == LogitechProtocol.USB:
            self.skipTest("There is no wireless status update while connecting by USB cable.")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power off / on DUT using Power Supply")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_connection_reset=False,
                   verify_wireless_device_status_broadcast_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Should receive WirelessDeviceStatusBroadcastEvent and the value should be "
                                  "(Status=1, Request=1, Reason=1)")
        # --------------------------------------------------------------------------------------------------------------
        wireless_device_status_broadcast_event = ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.status)),
                         msg="The Status parameter differs from the one expected")
        self.assertEqual(expected=WirelessDeviceStatus.Request.SOFTWARE_RECONFIGURATION_NEEDED,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.request)),
                         msg="The Request parameter differs from the one expected")
        self.assertEqual(expected=WirelessDeviceStatus.Reason.POWER_SWITCH_ACTIVATED,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.reason)),
                         msg="The Reason parameter differs from the one expected")
    # end def common_WirelessDeviceStatusBroadcastEventPowerUpPowerSupply

    def common_WirelessDeviceStatusBroadcastEventPowerUpPowerSwitch(self):
        """
        Check an event is received when the DUT is switched off then on. This is the common method for Application and
        Bootloader.
        """
        # Gaming device need to switch channel form wireless to USB cable connection in order to enter bootloader mode.
        # The test script shall be skipped for this case.
        if self.config_manager.current_protocol == LogitechProtocol.USB:
            self.skipTest("There is no wireless status update while connecting by USB cable.")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power off/on DUT using Power Switch")
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Should receive WirelessDeviceStatusBroadcastEvent and the value should be "
                                  "(Status=1, Request=1, Reason=1)")
        # --------------------------------------------------------------------------------------------------------------
        wireless_device_status_broadcast_event = ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.status)),
                         msg="The Status parameter differs from the one expected")
        self.assertEqual(expected=WirelessDeviceStatus.Request.SOFTWARE_RECONFIGURATION_NEEDED,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.request)),
                         msg="The Request parameter differs from the one expected")
        self.assertEqual(expected=WirelessDeviceStatus.Reason.POWER_SWITCH_ACTIVATED,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.reason)),
                         msg="The Reason parameter differs from the one expected")
    # end def common_WirelessDeviceStatusBroadcastEventPowerUpPowerSwitch

    def common_WirelessDeviceStatusBroadcastEventDeepSleepWaited(self):
        """
        Check an event is received when the DUT is coming back from deep sleep. This is the common method for
        Application and Bootloader.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for deep sleep")
        # --------------------------------------------------------------------------------------------------------------
        f = self.getFeatures()
        sleep(f.PRODUCT.DEVICE.F_MaxWaitDeepSleep)

        self._wake_up_and_check_event()
    # end def common_WirelessDeviceStatusBroadcastEventDeepSleepWaited

    def common_WirelessDeviceStatusBroadcastEventSleep(self):
        """
        Check no event is received when the DUT is coming back from sleep mode. This is the common method for
        Application and Bootloader.
        """
        f = self.getFeatures()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop for 3 times")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(3):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait until DUT enter sleep mode")
            # ----------------------------------------------------------------------------------------------------------
            sleep(f.PRODUCT.DEVICE.F_MaxWaitSleep)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wake up DUT by button clicking")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
            sleep(0.3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Shouldn\"t receive WirelessDeviceStatusBroadcastEvent")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, timeout=1,
                                           class_type=WirelessDeviceStatusBroadcastEvent)

            # Empty all queues to avoid unwanted messages (HID for example)
            ChannelUtils.empty_queues(test_case=self)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def common_WirelessDeviceStatusBroadcastEventSleep

    def _wake_up_and_check_event(self):
        """
        Wake up the device and check the 0x1D4B event received
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up DUT by button clicking")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(0.3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Should receive WirelessDeviceStatusBroadcastEvent and the value should be "
                                  f"(Status=1, Request=1, Reason=1)")
        # --------------------------------------------------------------------------------------------------------------
        wireless_device_status_broadcast_event = ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.status)),
                         msg="The Status parameter differs from the one expected")
        self.assertEqual(expected=WirelessDeviceStatus.Request.SOFTWARE_RECONFIGURATION_NEEDED,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.request)),
                         msg="The Request parameter differs from the one expected")
        self.assertEqual(expected=WirelessDeviceStatus.Reason.POWER_SWITCH_ACTIVATED,
                         obtained=int(Numeral(wireless_device_status_broadcast_event.reason)),
                         msg="The Reason parameter differs from the one expected")

        # Empty all queues to avoid unwanted messages (HID for example)
        ChannelUtils.empty_queues(test_case=self)
    # end def _wake_up_and_check_event
# end class WirelessDeviceStatusTestCase


class ApplicationWirelessDeviceStatusTestCase(WirelessDeviceStatusTestCase, DeviceBaseTestCase):
    """
    Validate Wireless Device Status TestCases in Application mode
    """

    @features("Feature1D4B")
    @level('Business', 'SmokeTests')
    @services("HardwareReset")
    def test_WirelessDeviceStatusBroadcastEventPowerUp(self):
        """
        Test the reception of an event when the DUT is powered up.

        Status, Request, Reason = [0]WirelessDeviceStatusBroadcastEvent()
        """
        self.common_WirelessDeviceStatusBroadcastEventPowerUpPowerSupply()

        self.testCaseChecked("BUS_APP_1D4B_0001")
    # end def test_WirelessDeviceStatusBroadcastEventPowerUp

    @features("Feature1D4B")
    @features("Feature1830powerMode", 3)
    @level("Business")
    @services("ButtonPressed")
    def test_WirelessDeviceStatusBroadcastEventDeepSleepForced(self):
        """
        Check an event is received when the DUT is coming back from deep sleep.

        Status, Request, Reason = [0]WirelessDeviceStatusBroadcastEvent()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetPowerMode with powerModeNumber = 3")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        self._wake_up_and_check_event()

        self.testCaseChecked("BUS_APP_1D4B_0003")
    # end def test_WirelessDeviceStatusBroadcastEventDeepSleepForced

    @features("Feature1D4B")
    @level("DeepSleepWaitingTime")
    @services("ButtonPressed")
    def test_WirelessDeviceStatusBroadcastEventDeepSleepWaited(self):
        """
        Check an event is received when the DUT is coming back from deep sleep.

        Status, Request, Reason = [0]WirelessDeviceStatusBroadcastEvent()
        """
        self.common_WirelessDeviceStatusBroadcastEventDeepSleepWaited()

        self.testCaseChecked("FUN_APP_1D4B_0001")
    # end def test_WirelessDeviceStatusBroadcastEventDeepSleepWaited

    @features("Feature1D4B")
    @level("Robustness")
    @services("ButtonPressed")
    def test_WirelessDeviceStatusBroadcastEventSleep(self):
        """
        Check no event is received when the DUT is coming back from sleep mode.
        """
        self.common_WirelessDeviceStatusBroadcastEventSleep()

        self.testCaseChecked("ROB_APP_1D4B_0001")
    # end def test_WirelessDeviceStatusBroadcastEventSleep
# end class ApplicationDeviceTypeAndNameTestCase


@features.class_decorator("BootloaderAvailable")
class BootloaderWirelessDeviceStatusTestCase(WirelessDeviceStatusTestCase, DeviceBootloaderTestCase):
    """
    Validate Wireless Device Status TestCases in Bootloader mode
    """

    @features("Feature1D4B")
    @features("Feature00D0")
    @level("Business")
    @services("HardwareReset")
    def test_WirelessDeviceStatusBroadcastEventPowerUp(self):
        """
        Test the reception of an event when the DUT is powered up.

        Status, Request, Reason = [0]WirelessDeviceStatusBroadcastEvent()
        """
        self.common_WirelessDeviceStatusBroadcastEventPowerUpPowerSupply()

        self.testCaseChecked("BUS_BOOT_1D4B_0001")
    # end def test_WirelessDeviceStatusBroadcastEventPowerUp

    @features("Feature1D4B")
    @features("Feature00D0")
    @level("DeepSleepWaitingTime")
    @services("ButtonPressed")
    def test_WirelessDeviceStatusBroadcastEventDeepSleepWaited(self):
        """
        Check an event is received when the DUT is coming back from deep sleep.

        Status, Request, Reason = [0]WirelessDeviceStatusBroadcastEvent()
        """
        self.common_WirelessDeviceStatusBroadcastEventDeepSleepWaited()

        self.testCaseChecked("FUN_BOOT_1D4B_0001")
    # end def test_WirelessDeviceStatusBroadcastEventDeepSleepWaited

    @features("Feature1D4B")
    @features("Feature00D0")
    @level("Robustness")
    @services("ButtonPressed")
    def test_WirelessDeviceStatusBroadcastEventSleep(self):
        """
        Check no event is received when the DUT is coming back from sleep mode.
        """
        self.common_WirelessDeviceStatusBroadcastEventSleep()

        self.testCaseChecked("ROB_BOOT_1D4B_0001")
    # end def test_WirelessDeviceStatusBroadcastEventSleep
# end class BootloaderWirelessDeviceStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
