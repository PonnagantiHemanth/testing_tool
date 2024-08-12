#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.led.pwsfunctionalled.batterynotification
:brief: Validate battery notification evt test cases
:author: Gautham S B <gsb@logitech.com>
:date: 2023/12/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.ledspyhelper import LedSpyHelper
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BatteryNotificationTestCase(DeviceBaseTestCase):
    """
    Validate battery notification test cases
    """
    FIVE_SECONDS = 5
    FIVE_SECONDS_IN_MS = 5000
    HUNDRED_MILLISECONDS = 100
    THIRTY_SECONDS = 30
    THREE_MINUTES = 180
    THREE_MINUTES_IN_MS = 180000
    ANY = LedSpyHelper.POSITION.ANY
    FIRST = LedSpyHelper.POSITION.FIRST
    LED_IDENTIFIERS = [LED_ID.DEVICE_STATUS_GREEN_LED, LED_ID.DEVICE_STATUS_RED_LED, LED_ID.CONNECTIVITY_STATUS_LED_1]
    NEXT = LedSpyHelper.POSITION.NEXT
    RECONNECT_TO_HOST_MAX_TIME_MS_BLE_PRO = 100
    RECONNECT_TO_HOST_MAX_TIME_MS_DIRECT_BLE = 2000

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_reconnect_to_host = False
        self.post_requisite_set_nominal_voltage = False

        super().setUp()

        self.reconnect_to_host_time_duration = self.RECONNECT_TO_HOST_MAX_TIME_MS_BLE_PRO \
            if self.current_channel.protocol == LogitechProtocol.BLE_PRO \
            else self.RECONNECT_TO_HOST_MAX_TIME_MS_DIRECT_BLE

        # Sleep for 5 seconds to let all leds in dut turn off
        sleep(5)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_set_nominal_voltage:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Set DUT Nominal voltage")
                # ------------------------------------------------------------------------------------------------------
                # TODO: Set nominal voltage using power emulator board
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reconnect_to_host:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reconnect back to host")
                # ------------------------------------------------------------------------------------------------------
                LibusbDriver.enable_usb_port(ChannelUtils.get_port_index(self))
            # end if
        # end with

        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Clean WirelessDeviceStatusBroadcastEvent messages")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Clean Battery Status messages")
            # ----------------------------------------------------------------------------------------------------------
            self.cleanup_battery_event_from_queue()
        # end with
        super().tearDown()
    # end def tearDown

    def set_voltage_and_start_leds_monitoring(self, duration=FIVE_SECONDS, power_reset=False,
                                              disconnect_from_host=False, deepsleep=False, wakeup=False, voltage=None):
        """
        Set the required voltage to the DUT and start LED monitoring, can optionally do actions like do a power reset,
        put DUT in deep sleep or wake up the DUT from deepsleep

        :param duration: The duration of LED monitoring (Default is 5 seconds) - OPTIONAL
        :type duration: ``int``
        :param power_reset: The power reset flag - OPTIONAL
        :type power_reset: ``bool`` or ``None``
        :param disconnect_from_host: The disconnect from host flag - OPTIONAL
        :type disconnect_from_host: ``bool``
        :param deepsleep: The device deepsleep enable flag - OPTIONAL
        :type deepsleep: ``bool`` or ``None``
        :param wakeup: The device wakeup enable flag - OPTIONAL
        :type wakeup: ``bool`` or ``None``
        :param voltage: The voltage value to be set - OPTIONAL
        :type voltage: ``int`` or ``float`` or ``None``
        """
        self.disconnected = False
        led_monitoring_time_buffer = 0.3
        voltage = self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage if voltage is None else voltage
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set DUT voltage = {voltage} v")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Set voltage using power emulator

        if disconnect_from_host:
            self.disconnected = True
            self.post_requisite_reconnect_to_host = True
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Disconnect from host")
            # ----------------------------------------------------------------------------------------------------------
            LibusbDriver.disable_usb_port(ChannelUtils.get_port_index(self))
        # end if

        if power_reset:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Turn off the power slider")
            # ----------------------------------------------------------------------------------------------------------
            self.power_slider_emulator.power_off()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Start LEDs monitoring")
            # ----------------------------------------------------------------------------------------------------------
            LedSpyHelper.start_monitoring(self, self.LED_IDENTIFIERS)

            # Sleep for a second to add delay between power slider off and on action
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Turn on the power slider")
            # ----------------------------------------------------------------------------------------------------------
            self.power_slider_emulator.power_on()
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Start LEDs monitoring")
            # ----------------------------------------------------------------------------------------------------------
            LedSpyHelper.start_monitoring(self, self.LED_IDENTIFIERS)

            # Add a small delay after starting led monitoring
            sleep(1)
        # end if

        # If the device is disconnected from the host, it immediately goes into deep sleep
        if deepsleep and not self.disconnected:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Force the device into deep sleep mode through the 0x1830 "
                                     "SetPowerMode request")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Device immediately goes into deep sleep mode when disconnected from the host")
            # ----------------------------------------------------------------------------------------------------------
        # end if

        if wakeup:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Emulate user action to wake up the device")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Monitor LEDs for {duration} seconds")
        # --------------------------------------------------------------------------------------------------------------
        sleep(duration + led_monitoring_time_buffer)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.stop_monitoring(self, self.LED_IDENTIFIERS)
    # end def set_voltage_and_start_leds_monitoring

    def check_connectivity_led_after_power_reset_device_connected(self, led_id, reconnection_time_duration=None,
                                                                  steady_duration=FIVE_SECONDS_IN_MS):
        """
        Check the connectivity LED behaviour after a power reset when the device remains connected to the host

        :param led_id: The unique LED identifier to monitor
        :type led_id: ``LED_ID``
        :param reconnection_time_duration: The time duration for which connectivity LED remains in On state before the
                                           device is reconnected to the host in ms - OPTIONAL
        :type reconnection_time_duration: ``int``
        :param steady_duration: The time duration for which connectivity LED remains in Steady state after the
                                device gets connected to host in ms - OPTIONAL
        :type steady_duration: ``int``
		"""
        reconnection_time_duration = self.reconnect_to_host_time_duration if reconnection_time_duration is None \
            else reconnection_time_duration

        # Check Led behaviour as it reconnects back to host after device power on/device wakeup from deepsleep
        LedSpyHelper.check_effect_duration(
            self, led_id, effect=SchemeType.STEADY, maximum_duration=reconnection_time_duration, position=self.NEXT)

        # Check Led steady time after reconnection
        LedSpyHelper.check_effect_duration(self, led_id, effect=SchemeType.STEADY, exact_duration=steady_duration,
                                           position=self.ANY)
    # end def check_connectivity_led_after_power_reset_device_connected
# end class BatteryNotificationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
