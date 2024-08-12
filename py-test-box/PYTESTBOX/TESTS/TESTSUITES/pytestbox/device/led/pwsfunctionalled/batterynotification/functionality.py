#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.led.pwsfunctionalled.batterynotification.functionality
:brief: Battery Notification functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/12/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from numpy import arange

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.ledspyhelper import LedSpyHelper
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.led.pwsfunctionalled.batterynotification.battery_notification import BatteryNotificationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_SET_REQUIRED_VOLTAGE_AND_START_MONITORING = "Set required Voltage to DUT and start LEDs monitoring"
_VALIDATE_LED_BEHAVIOUR = "Validate LED behaviour is as expected"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BatteryNotificationFunctionalityTestCase(BatteryNotificationTestCase):
    """
    Validate Battery Notification LED behaviour functionality test cases
    """

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerSwitch")
    def test_good_battery_level_device_connected(self):
        """
        Check the LED behaviour at device power ON at good battery level when the device remains connected to the host

        Expected behaviour:
               * Green LED: Steady ON for 5 seconds
               * Red LED: OFF
               * Host White LED: Steady ON for 5 seconds
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        self.set_voltage_and_start_leds_monitoring(power_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Validate LEDs behaviour is Green LED: Steady ON for 5 seconds, "
                                 "Red LED: OFF, Host White LED: Steady ON for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        self.check_connectivity_led_after_power_reset_device_connected(LED_ID.CONNECTIVITY_STATUS_LED_1)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.STEADY,
                                           exact_duration=self.FIVE_SECONDS_IN_MS, reset=True)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.OFF,
                                           minimum_duration=self.FIVE_SECONDS_IN_MS, position=self.FIRST)

        self.testCaseChecked("FUN_BST_0001", _AUTHOR)
    # end def test_good_battery_level_device_connected

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerSwitch")
    def test_good_battery_level_device_disconnected(self):
        """
        Check the LED behaviour at device power ON at good battery level when the device is disconnected from the host

        Expected behaviour:
               * Green LED: Steady ON for 5 seconds
               * Red LED: OFF
               * Host White LED: Slow blinking for 5 seconds
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        self.set_voltage_and_start_leds_monitoring(power_reset=True, disconnect_from_host=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Validate LEDs behaviour is Green LED: Steady ON for 5 seconds, Red LED: OFF,"
                                 "Host White LED: Slow blinking for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(self, LED_ID.CONNECTIVITY_STATUS_LED_1, effect=SchemeType.SLOW_BLINKING,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.STEADY, reset=True,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.OFF,
                                           minimum_duration=self.FIVE_SECONDS_IN_MS, position=self.FIRST)

        self.testCaseChecked("FUN_BST_0002", _AUTHOR)
    # end def test_good_battery_level_device_disconnected

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerBoard")
    @services("PowerSwitch")
    def test_low_battery_level_device_connected(self):
        """
        Check the LED behaviour at device power ON at low battery level when the device remains connected to the host

        Expected behaviour:
               * Green LED: OFF
               * Red LED: Steady ON for 5 seconds + Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second)
               * Host White LED: Steady ON for 5 seconds
        """
        self.post_requisite_set_nominal_voltage = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set critical voltage to DUT and start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.set_voltage_and_start_leds_monitoring(duration=self.THREE_MINUTES + self.FIVE_SECONDS,
                                                   power_reset=True, voltage=critical_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Verify the LEDs behaviour is Green LED: OFF, Red LED: Steady ON for 5 seconds + "
                                 "Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second), "
                                 "Host White LED: Steady ON for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(self, LED_ID.CONNECTIVITY_STATUS_LED_1, effect=SchemeType.STEADY,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.OFF,
                                           minimum_duration=(self.THREE_MINUTES_IN_MS + self.FIVE_SECONDS_IN_MS),
                                           position=self.FIRST)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.STEADY, reset=True,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.PULSING,
                                           exact_duration=self.THREE_MINUTES_IN_MS)

        self.testCaseChecked("FUN_BST_0003", _AUTHOR)
    # end def test_low_battery_level_device_connected

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerBoard")
    @services("PowerSwitch")
    def test_low_battery_level_device_disconnected(self):
        """
        Check the LED behaviour at device power ON at low battery level when the device is disconnected from the host

        Expected behaviour:
               * Green LED: OFF
               * Red LED: Steady ON for 5 seconds + Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second)
               * Host White LED: Slow blinking for 5 seconds
        """
        self.post_requisite_set_nominal_voltage = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set critical voltage to DUT and start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.set_voltage_and_start_leds_monitoring(duration=self.THREE_MINUTES + self.FIVE_SECONDS,
                                                   power_reset=True, voltage=critical_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Verify the LEDs behaviour is Green LED: OFF, Red LED: Steady ON for 5 seconds + "
                                 "Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second)"
                                 "Host White LED: Slow blinking for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(self, LED_ID.CONNECTIVITY_STATUS_LED_1, effect=SchemeType.SLOW_BLINKING,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.OFF,
                                           minimum_duration=self.THREE_MINUTES_IN_MS, position=self.FIRST)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.STEADY, reset=True,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.PULSING,
                                           exact_duration=self.THREE_MINUTES_IN_MS)

        self.testCaseChecked("FUN_BST_0004", _AUTHOR)
    # end def test_low_battery_level_device_disconnected

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerSwitch")
    def test_good_battery_level_from_wakeup_device_connected(self):
        """
        Check the LEDs behaviour when the device wakes up from deep sleep at good battery level while the device
        remains connected to the host

        Expected behaviour:
               * Green LED: Steady ON for 5 seconds
               * Red LED: OFF
               * Host White LED: Steady ON for 5 seconds
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        self.set_voltage_and_start_leds_monitoring(deepsleep=True, wakeup=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Verify the LEDs behaviour is Green LED: Steady ON for 5 seconds, Red LED: OFF"
                                 "Host White LED: Steady ON for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        self.check_connectivity_led_after_power_reset_device_connected(LED_ID.CONNECTIVITY_STATUS_LED_1)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.STEADY, reset=True,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.OFF,
                                           minimum_duration=self.FIVE_SECONDS_IN_MS, position=self.FIRST)

        self.testCaseChecked("FUN_BST_0005", _AUTHOR)
    # end def test_good_battery_level_from_wakeup_device_connected

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerSwitch")
    def test_good_battery_level_from_wakeup_device_disconnected(self):
        """
        Checking the LED state when wake up from deep sleep + good battery and device disconnected

        Expected behaviour:
               * Green LED: Steady ON for 5 seconds
               * Red LED: OFF
               * Host White LED: Slow blinking for 5 seconds
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        self.set_voltage_and_start_leds_monitoring(disconnect_from_host=True, deepsleep=True, wakeup=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate LEDs behaviour is Green LED: Steady ON for 5 seconds, Red LED: OFF, "
                                 "Host White LED: Slow blinking for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(self, LED_ID.CONNECTIVITY_STATUS_LED_1, effect=SchemeType.SLOW_BLINKING,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.STEADY, reset=True,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.OFF,
                                           minimum_duration=self.FIVE_SECONDS_IN_MS, position=self.FIRST)

        self.testCaseChecked("FUN_BST_0006", _AUTHOR)
    # end def test_good_battery_level_from_wakeup_device_disconnected

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerBoard")
    @services("PowerSwitch")
    def test_low_battery_level_from_wakeup_device_connected(self):
        """
        Checking the LED state when wake up from deep sleep + low battery and device connected

        Expected behaviour:
               * Green LED: OFF
               * Red LED: Steady ON for 5 seconds + Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second)
               * Host White LED: Steady ON for 5 seconds
        """
        self.post_requisite_set_nominal_voltage = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.set_voltage_and_start_leds_monitoring(
            duration=self.THREE_MINUTES + self.FIVE_SECONDS, voltage=critical_voltage, deepsleep=True, wakeup=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate LEDs behaviour is Green LED: OFF, Red LED: Steady ON for 5 seconds + "
                                 "Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second) "
                                 "Host White LED: Steady ON for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(self, LED_ID.CONNECTIVITY_STATUS_LED_1, effect=SchemeType.STEADY,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.OFF,
                                           minimum_duration=(self.THREE_MINUTES_IN_MS + self.FIVE_SECONDS_IN_MS),
                                           position=self.FIRST)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.STEADY, reset=True,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.PULSING,
                                           exact_duration=self.THREE_MINUTES_IN_MS)

        self.testCaseChecked("FUN_BST_0007", _AUTHOR)
    # end def test_low_battery_level_from_wakeup_device_connected

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerBoard")
    @services("PowerSwitch")
    def test_low_battery_level_from_wakeup_device_disconnected(self):
        """
        Checking the LED state when wake up from deep sleep + low battery and device disconnected

        Expected behaviour:
               * Green LED: OFF
               * Red LED: Steady ON for 5 seconds + Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second)
               * Host White LED: Slow blinking for 5 seconds
        """
        self.post_requisite_set_nominal_voltage = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.set_voltage_and_start_leds_monitoring(
            duration=self.THREE_MINUTES + self.FIVE_SECONDS, voltage=critical_voltage, deepsleep=True, wakeup=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate LED behaviour is Green LED: OFF, Red LED: Steady ON for 5 seconds + "
                                 "Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second) "
                                 "Host White LED: Slow blinking for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(self, LED_ID.CONNECTIVITY_STATUS_LED_1, effect=SchemeType.SLOW_BLINKING,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_GREEN_LED, effect=SchemeType.OFF,
                                           minimum_duration=self.THREE_MINUTES_IN_MS, position=self.FIRST)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.STEADY, reset=True,
                                           exact_duration=self.FIVE_SECONDS_IN_MS)
        LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.PULSING,
                                           exact_duration=self.THREE_MINUTES_IN_MS)

        self.testCaseChecked("FUN_BST_0008", _AUTHOR)
    # end def test_low_battery_level_from_wakeup_device_disconnected

    @features("EvtBatteryNotification")
    @features("Feature1004")
    @level("Functionality")
    @level("Time-consuming")
    @services("LedIndicator")
    @services("PowerBoard")
    @services("PowerSwitch")
    def test_led_behaviour_device_critical_battery_level(self):
        """
        Test the LEDs behaviour when device voltage is gradually brought down from good battery level to
        critical battery level

        Expected behaviour:
               * Green LED: OFF
               * Red LED: Steady ON for 5 seconds + Pulsing for 3 minutes (ramp up 1 second, ramp down 1 second)
               * Host White LED: OFF
        """
        self.post_requisite_set_nominal_voltage = True

        self.critical_voltage_achieved = False
        nominal_voltage = self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage
        cutoff_voltage = self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage
        duration = self.THREE_MINUTES + self.FIVE_SECONDS
        step = 0.01

        for voltage in arange(nominal_voltage, cutoff_voltage, -step):
            if self.critical_voltage_achieved:
                break
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Start LEDs monitoring")
            # ----------------------------------------------------------------------------------------------------------
            LedSpyHelper.start_monitoring(self, self.LED_IDENTIFIERS)
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Set voltage = {voltage} v to DUT")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Set voltage using power emulator board

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request using feature 0x1004')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            if to_int(get_status_response.battery_level_critical):
                self.critical_voltage_achieved = True
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Continue monitoring for {duration} before stopping monitoring")
                # ------------------------------------------------------------------------------------------------------
                sleep(duration)
                LedSpyHelper.stop_monitoring(self, self.LED_IDENTIFIERS)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Achieved Critical voltage = {voltage} v, "
                                         f"Check LEDs behaviour on critical voltage")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate Battery Green and Host LEDs are in off state")
                # ------------------------------------------------------------------------------------------------------
                for led in [LED_ID.DEVICE_STATUS_LED_1, LED_ID.DEVICE_STATUS_GREEN_LED]:
                    LedSpyHelper.check_effect_duration(self, led, effect=SchemeType.OFF,
                                                       minimum_duration=self.THREE_MINUTES_IN_MS, position=self.FIRST,
                                                       reset=True)
                # end for

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate Red LED will be steady for 5 seconds and then be in pulsing state"
                                          "for three minutes")
                # ------------------------------------------------------------------------------------------------------
                LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.STEADY,
                                                   reset=True, exact_duration=self.FIVE_SECONDS_IN_MS)
                LedSpyHelper.check_effect_duration(self, LED_ID.DEVICE_STATUS_RED_LED, effect=SchemeType.PULSING,
                                                   exact_duration=self.THREE_MINUTES_IN_MS)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"If critical voltage level is not achieved with current voltage level = "
                                         f"{voltage} v, wait for thirty seconds and drop voltage level by {step} v")
                # ------------------------------------------------------------------------------------------------------
                sleep(self.THIRTY_SECONDS)
            # end if
        # end for

        assert self.critical_voltage_achieved is True, "Critical Voltage was not achieved during test execution"

        self.testCaseChecked("FUN_BST_0009", _AUTHOR)
    # end def test_led_behaviour_device_critical_battery_level

    @features("EvtBatteryNotification")
    @features("Feature1004")
    @level("Functionality")
    @level("Time-consuming")
    @services("LedIndicator")
    @services("PowerBoard")
    @services("PowerSwitch")
    def test_led_behaviour_device_cut_off_voltage(self):
        """
        Test the LEDs behaviour when device voltage is gradually brought down from good battery level to
        cut off voltage

        Expected behaviour:
               * Green LED: OFF
               * Red LED: OFF
               * Host White LED: OFF
        """
        self.post_requisite_set_nominal_voltage = True
        nominal_voltage = self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage
        cutoff_voltage = self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage
        step = 0.01

        for voltage in arange(nominal_voltage, cutoff_voltage + step, -step):
            if voltage == cutoff_voltage:
                LedSpyHelper.start_monitoring(self, self.LED_IDENTIFIERS)
                sleep(1)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Set voltage = {voltage} v to DUT")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Set voltage using power emulator board

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, _VALIDATE_LED_BEHAVIOUR)
            # ----------------------------------------------------------------------------------------------------------
            if voltage == cutoff_voltage:
                # Monitor LEDs for minimum 5 seconds before stopping
                sleep(5)
                LedSpyHelper.stop_monitoring(self, self.LED_IDENTIFIERS)
                for led in self.LED_IDENTIFIERS:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, "Validate all LEDs are in off state")
                    # --------------------------------------------------------------------------------------------------
                    LedSpyHelper.check_effect_duration(self, led, effect=SchemeType.OFF, position=self.FIRST,
                                                       minimum_duration=self.FIVE_SECONDS_IN_MS)
                # end for
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"If cutoff voltage level is not achieved with current voltage level = "
                                         f"{voltage} v, wait for thirty seconds and drop voltage level by {step} v")
                # ------------------------------------------------------------------------------------------------------
                sleep(30)
            # end if
        # end for

        self.testCaseChecked("FUN_BST_0011", _AUTHOR)
    # end def test_led_behaviour_device_cut_off_voltage

    @features("EvtBatteryNotification")
    @level("Functionality")
    @services("LedIndicator")
    @services("PowerSwitch")
    def test_led_behaviour_deep_sleep_mode(self):
        """
        Check the LEDs behaviour in device deep sleep mode

        Expected behaviour:
               * Green LED: OFF
               * Red LED: OFF
               * Host White LED: OFF
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        self.set_voltage_and_start_leds_monitoring(deepsleep=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate all LEDs are in OFF state")
        # --------------------------------------------------------------------------------------------------------------
        for led_id in self.LED_IDENTIFIERS:
            LedSpyHelper.check_effect_duration(self, led_id, effect=SchemeType.OFF, position=self.FIRST,
                                               minimum_duration=self.FIVE_SECONDS_IN_MS)
        # end for

        self.testCaseChecked("FUN_BST_0012", _AUTHOR)
    # end def test_led_behaviour_deep_sleep_mode
# end class BatteryNotificationFunctionalityTestCase


class BatteryNotificationBleFunctionalityTestCase(BatteryNotificationTestCase):
    """
    Contains test cases for LED behaviour in various scenarios in Ble mode.
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to BLE Mode")
        # --------------------------------------------------------------------------------------------------------------
        ProtocolManagerUtils.select_channel_by_protocol(self, LogitechProtocol.BLE)

        # sleep for 5 seconds to let all leds turn off
        sleep(5)
    # end def setUp

    def tearDown(self):
        """
        Manage test post-requisites
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Exit BLE channel")
            # ----------------------------------------------------------------------------------------------------------
            ProtocolManagerUtils.exit_ble_channel(self)
            # end if
        # end with

        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reload initial NVS")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.NvsHelper.restore_nvs(self)
        # end with
        super().tearDown()
    # end def tearDown

    @features("EvtBatteryNotification")
    @features('BLEProtocol')
    @level("Functionality")
    @services("PowerSwitch")
    @services("BleContext")
    def test_hid_off_mode(self):
        """
        Checking the LED state at hid-off mode in direct Ble protocol

        Expected behaviour:
               * Green LED: OFF
               * Red LED: OFF
               * Host White LED: OFF
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SET_REQUIRED_VOLTAGE_AND_START_MONITORING)
        # --------------------------------------------------------------------------------------------------------------
        self.set_voltage_and_start_leds_monitoring(deepsleep=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate all LEDs are in OFF state")
        # --------------------------------------------------------------------------------------------------------------
        for led_id in self.LED_IDENTIFIERS:
            LedSpyHelper.check_effect_duration(self, led_id, effect=SchemeType.OFF, position=self.FIRST,
                                               exact_duration=self.FIVE_SECONDS_IN_MS)
        # end for

        self.testCaseChecked("FUN_BST_0010", _AUTHOR)
    # end def test_hid_off_mode
# end class BatteryNotificationBleFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
