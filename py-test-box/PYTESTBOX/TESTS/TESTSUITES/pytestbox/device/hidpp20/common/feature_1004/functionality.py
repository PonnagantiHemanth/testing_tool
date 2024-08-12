#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1004.functionality
:brief: HID++ 2.0 Unified Battery functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
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
from pyhid.hidpp.features.common.changehost import ChangeHost
from pyhid.hidpp.features.common.changehost import GetHostInfoV1
from pyhid.hidpp.features.common.changehost import GetHostInfoV1Response
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpi
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import DeviceState
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryGamingTest
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryGenericTest
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryMultiReceiverGenericTest
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UnifiedBatteryFunctionalityTestCase(UnifiedBatteryGenericTest):
    """
    Validates Unified Battery functionality TestCases
    """
    @features('Feature1004')
    @features('Unifying')
    @level('Functionality')
    @services('PowerSupply')
    @services('NoLedIndicator')
    def test_all_soc_ufy_no_led(self):
        self.generic_all_soc_ufy()

        self.testCaseChecked("FUN_1004_0006#1")
    # end def test_all_soc_ufy_no_led

    @features('Feature1004')
    @features('Unifying')
    @level('Functionality')
    @services('PowerSupply')
    @services('LedIndicator')
    def test_all_soc_ufy(self):
        self.generic_all_soc_ufy()

        self.testCaseChecked("FUN_1004_0006#1")
        self.testCaseChecked("FUN_1004_0006#2")
    # end def test_all_soc_ufy

    @features('Feature1004')
    @features('Bluetooth')
    @level('Functionality')
    @services('PowerSupply')
    @services('Debugger')
    @services('NoLedIndicator')
    def test_all_soc_ble_no_led(self):
        self.generic_all_soc_ble()

        self.testCaseChecked("FUN_1004_0007#1")
    # end def test_all_soc_ble_no_led

    @features('Feature1004')
    @features('Bluetooth')
    @level('Functionality')
    @services('PowerSupply')
    @services('Debugger')
    @services('LedIndicator')
    def test_all_soc_ble(self):
        self.generic_all_soc_ble()

        self.testCaseChecked("FUN_1004_0007#1")
        self.testCaseChecked("FUN_1004_0007#2")
    # end def test_all_soc_ble

    @features('Feature1004')
    @level('Functionality')
    def test_get_capabilities_after_reconnection_by_receiver_link_loss(self):
        """
        Validate get_capabilities responses after a reconnection triggered by a receiver link loss
        (receiver usb port off / on)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(
            test_case=self, channel=self.current_channel, enable=True, force_send_unknown_channel_type=True)
        self.button_stimuli_emulator.user_action()
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_capabilities request')
        # --------------------------------------------------------------------------------------------------------------
        get_capabilities_response = UnifiedBatteryTestUtils.HIDppHelper.get_capabilities(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_capabilities response and check product-specific constants')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(
            test_case=self, message=get_capabilities_response,
            expected_cls=self.feature_1004.get_capabilities_response_cls)

        self.testCaseChecked("FUN_1004_0008#1")
    # end def test_get_capabilities_after_reconnection_by_receiver_link_loss

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSwitch')
    def test_get_capabilities_after_reconnection_by_power_slider(self):
        """
        Validate get_capabilities responses after a reconnection triggered by a switch off / on by power slider
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch off / on the device using the power slider emulator')
        # --------------------------------------------------------------------------------------------------------------
        if self.power_slider_emulator is not None:
            DeviceBaseTestUtils.ResetHelper.power_switch_reset(self)
        # end if

        # ------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_capabilities request')
        # ------------------------------------------------------------------------------------------------------------
        get_capabilities_response = UnifiedBatteryTestUtils.HIDppHelper.get_capabilities(self)

        # ------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_capabilities response and check product-specific constants')
        # ------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(
            test_case=self, message=get_capabilities_response,
            expected_cls=self.feature_1004.get_capabilities_response_cls)

        self.testCaseChecked("FUN_1004_0008#3")
    # end def test_get_capabilities_after_reconnection_by_power_slider

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSupply')
    def test_get_capabilities_after_reconnection_by_power_supply(self):
        """
        Validate get_capabilities responses after a reconnection triggered by a switch off / on b by power supply.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch off / on the device using the battery emulator')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.power_supply_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_capabilities request')
        # --------------------------------------------------------------------------------------------------------------
        get_capabilities_response = UnifiedBatteryTestUtils.HIDppHelper.get_capabilities(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_capabilities response and check product-specific constants')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(
            test_case=self, message=get_capabilities_response,
            expected_cls=self.feature_1004.get_capabilities_response_cls)

        self.testCaseChecked("FUN_1004_0008#4")
    # end def test_get_capabilities_after_reconnection_by_power_supply

    @features('Feature1004')
    @level('Functionality')
    @services('MultiHost')
    @services('PowerSupply')
    @services('ButtonPressed')
    @services('NoLedIndicator')
    def test_battery_event_link_loss_no_led(self):
        self.generic_battery_event_link_loss()

        self.testCaseChecked("FUN_1004_0009#1")
    # end def test_battery_event_link_loss_no_led

    @features('Feature1004')
    @level('Functionality')
    @services('MultiHost')
    @services('PowerSupply')
    @services('ButtonPressed')
    @services('LedIndicator')
    def test_battery_event_link_loss(self):
        self.generic_battery_event_link_loss()

        self.testCaseChecked("FUN_1004_0009#1")
        self.testCaseChecked("FUN_1004_0009#2")
    # end def test_battery_event_link_loss

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSupply')
    @services('NoLedIndicator')
    def test_battery_event_restart_no_led(self):
        self.generic_battery_event_restart()

        self.testCaseChecked("FUN_1004_0011#1")
    # end def test_battery_event_restart_no_led

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSupply')
    @services('LedIndicator')
    def test_battery_event_restart(self):
        self.generic_battery_event_restart()

        self.testCaseChecked("FUN_1004_0011#1")
        self.testCaseChecked("FUN_1004_0011#2")
    # end def test_battery_event_restart

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSwitch')
    @services('PowerSupply')
    @services('NoLedIndicator')
    def test_battery_event_power_switch_no_led(self):
        self.generic_battery_event_power_switch()

        self.testCaseChecked("FUN_1004_0012#1")
    # end def test_battery_event_power_switch_no_led

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSwitch')
    @services('PowerSupply')
    @services('LedIndicator')
    def test_battery_event_power_switch(self):
        self.generic_battery_event_power_switch()

        self.testCaseChecked("FUN_1004_0012#1")
        self.testCaseChecked("FUN_1004_0012#2")
    # end def test_battery_event_power_switch

    @features('Feature1004')
    @level('DeepSleepWaitingTime')
    @services('PowerSupply')
    @services('ButtonPressed')
    @services('NoLedIndicator')
    def test_battery_event_deep_sleep_no_led(self):
        self.generic_battery_event_deep_sleep()

        self.testCaseChecked("FUN_1004_0013#1")
    # end def test_battery_event_deep_sleep_no_led

    @features('Feature1004')
    @level('DeepSleepWaitingTime')
    @services('PowerSupply')
    @services('ButtonPressed')
    @services('LedIndicator')
    def test_battery_event_deep_sleep(self):
        self.generic_battery_event_deep_sleep()

        self.testCaseChecked("FUN_1004_0013#1")
        self.testCaseChecked("FUN_1004_0013#2")
    # end def test_battery_event_deep_sleep

    @features('Feature1004')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_battery_diode_effect(self):
        self.generic_battery_diode_effect()

        self.testCaseChecked("FUN_1004_0014")
    # end def test_battery_diode_effect

    @features('Feature1004')
    @level('Timing')
    @services('PowerSupply')
    @services('Debugger')
    def test_measurement_timing(self):
        self.generic_measurement_timing()

        self.testCaseChecked("FUN_1004_0015")
    # end def test_measurement_timing

    @features('Feature1004')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Time-consuming')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('NoLedIndicator')
    def test_usb_charging_mechanism_no_led(self):
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRED)

        self.testCaseChecked("FUN_1004_0016#1")
    # end def test_usb_charging_mechanism_no_led

    @features('Feature1004')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Time-consuming')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('LedIndicator')
    def test_usb_charging_mechanism(self):
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRED)

        self.testCaseChecked("FUN_1004_0016#1")
        self.testCaseChecked("FUN_1004_0016#2")
    # end def test_usb_charging_mechanism

    @features('Feature1004')
    @features('Rechargeable')
    @features('NoGamingDevice')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('NoLedIndicator')
    def test_end_of_charge_mechanism_no_led(self):
        self.generic_end_of_charge_mechanism()

        self.testCaseChecked("FUN_1004_0017#1")
    # end def test_end_of_charge_mechanism_no_led

    @features('Feature1004')
    @features('Rechargeable')
    @features('NoGamingDevice')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('LedIndicator')
    def test_end_of_charge_mechanism(self):
        self.generic_end_of_charge_mechanism()

        self.testCaseChecked("FUN_1004_0017#1")
        self.testCaseChecked("FUN_1004_0017#2")
    # end def test_end_of_charge_mechanism

    @features('Feature1004')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSwitch')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('LedIndicator')
    def test_charging_mechanism_power_switch_off(self):
        """
        Validate device charging mechanism with the power slider switch OFF and battery level from lowest to highest.
        Check LED indicator.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the power switch')
        # --------------------------------------------------------------------------------------------------------------
        # TODO use PowerSwitch

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to CRITICAL level '
                                         'and a state_of_charge of 10%')
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.reset(hardware_reset=True, starting_voltage=battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode (i.e. connect USB cable)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        if self.f.PRODUCT.F_IsGaming:
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from '
                  f'{10 + self.config.F_StateOfChargeStep}% to 90% by step of '
                  f'{self.config.F_StateOfChargeStep}%')
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(10 + self.config.F_StateOfChargeStep, 91,
                                     self.config.F_StateOfChargeStep):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge,
                                                                                   discharge=False)
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait soc up-to-date')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.wait_soc_computation(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGING)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the power switch')
        # --------------------------------------------------------------------------------------------------------------
        # TODO use PowerSwitch

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for battery_status_event response')
        # --------------------------------------------------------------------------------------------------------------
        # TODO Depending on the time it take to the device to reconnect the timeout might have to be changed
        UnifiedBatteryTestUtils.wait_for_battery_status_event(
            self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check charging_status is '
                                  '\'charging\' and 90% battery level is returned')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, 90),
            "battery_level_full": (checker.check_full_battery_level, 1),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("FUN_1004_0018")
    # end def test_charging_mechanism_power_switch_off

    @features('Feature1004')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSwitch')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('LedIndicator')
    def test_end_of_charge_mechanism_power_switch_off(self):
        """
        Validate device end of charge detection with the power slider switch OFF.
        Check LED indicator.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the power switch')
        # --------------------------------------------------------------------------------------------------------------
        # TODO use PowerSwitch

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to GOOD level and '
                                         'a state_of_charge of 90%')
        # --------------------------------------------------------------------------------------------------------------
        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, 90, discharge=False)
        self.reset(hardware_reset=True, starting_voltage=battery_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode (i.e. connect USB cable)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        if self.f.PRODUCT.F_IsGaming:
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from '
                  f'{90 + self.config.F_StateOfChargeStep}% to 100% by step of '
                  f'{self.config.F_StateOfChargeStep}%')
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(90 + self.config.F_StateOfChargeStep, 101,
                                     self.config.F_StateOfChargeStep):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge,
                                                                                   discharge=False)
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait soc up-to-date')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.wait_soc_computation(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGING)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification (steady when end of charge reached than goes off after 5s)')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGE_COMPLETE,
                                 device_state=DeviceState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the power switch')
        # --------------------------------------------------------------------------------------------------------------
        # TODO use PowerSwitch

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for battery_status_event response')
        # --------------------------------------------------------------------------------------------------------------
        # TODO Depending on the time it take to the device to reconnect the timeout might have to be changed
        UnifiedBatteryTestUtils.wait_for_battery_status_event(
            self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check charging_status is '
                                  '\'charging\' and 90% battery level is returned')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, 100),
            "battery_level_full": (checker.check_full_battery_level, 1),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGE_COMPLETE),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("FUN_1004_0019")
    # end def test_end_of_charge_mechanism_power_switch_off

    @features('Feature1004')
    @features('Rechargeable')
    @features('Feature1805')
    @features('USBCharging')
    @level('Time-consuming')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('Debugger')
    @services('NoLedIndicator')
    def test_charging_mechanism_oob_no_led(self):
        self.generic_charging_mechanism_oob()

        self.testCaseChecked("FUN_1004_0020#1")
    # end def test_charging_mechanism_oob_no_led

    @features('Feature1004')
    @features('Rechargeable')
    @features('Feature1805')
    @features('USBCharging')
    @level('Time-consuming')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('Debugger')
    @services('LedIndicator')
    def test_charging_mechanism_oob(self):
        self.generic_charging_mechanism_oob()

        self.testCaseChecked("FUN_1004_0020#1")
        self.testCaseChecked("FUN_1004_0020#2")
    # end def test_charging_mechanism_oob

    @features('Feature1004')
    @features('Rechargeable')
    @features('Feature1805')
    @features('USBCharging')
    @level('DeepSleepWaitingTime')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('Debugger')
    @services('NoLedIndicator')
    def test_charging_mechanism_deep_sleep_oob_no_led(self):
        self.generic_charging_mechanism_deep_sleep_oob()

        self.testCaseChecked("FUN_1004_0021#1")
    # end def test_charging_mechanism_deep_sleep_oob_no_led

    @features('Feature1004')
    @features('Rechargeable')
    @features('Feature1805')
    @features('USBCharging')
    @level('DeepSleepWaitingTime')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('Debugger')
    @services('LedIndicator')
    def test_charging_mechanism_deep_sleep_oob(self):
        self.generic_charging_mechanism_deep_sleep_oob()

        self.testCaseChecked("FUN_1004_0021#1")
        self.testCaseChecked("FUN_1004_0021#2")
    # end def test_charging_mechanism_deep_sleep_oob

    @features('Feature1004')
    @level('DeepSleepWaitingTime')
    @services('PowerSupply')
    @services('LedIndicator')
    def test_led_behaviour_when_critical_level(self):
        """
        Validate LED indicators match the LED Guidelines when reaching critical level in the following use cases:
         - device in run/walk/sleep/deep sleep power mode
         - device restarting at this level
        """
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        low_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'low')
        battery_low = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, low_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set input voltage to CRITICAL level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait soc up-to-date')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                 'specification when critical level is reached in Run/walk mode')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=battery_critical, device_state=DeviceState.RUN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch off / on the device using the power supply emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                 'specification when restarting in critical level')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=battery_critical, device_state=DeviceState.RESTARTING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the device with input voltage to LOW level')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_low)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device to enter Sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set input voltage to CRITICAL level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait soc up-to-date')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                 'specification when critical level is reached in Sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=battery_critical, device_state=DeviceState.SLEEP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the device with input voltage to LOW level')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_low)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device to enter Deep Sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set input voltage to CRITICAL level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait soc up-to-date')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                 'specification when critical level is reached in Deep Sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=battery_critical, device_state=DeviceState.DEEP_SLEEP)

        self.testCaseChecked("FUN_1004_0022")
    # end def test_led_behaviour_when_critical_level

    @features('Feature1004')
    @features('WirelessCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('NoLedIndicator')
    def test_wireless_charging_mechanism_no_led(self):
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        self.testCaseChecked("FUN_1004_0023#1")
    # end def test_wireless_charging_mechanism_no_led

    @features('Feature1004')
    @features('WirelessCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('LedIndicator')
    def test_wireless_charging_mechanism(self):
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        self.testCaseChecked("FUN_1004_0023#1")
        self.testCaseChecked("FUN_1004_0023#2")
    # end def test_wireless_charging_mechanism

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSupply')
    @services('ChargingAtSlowRate')
    @services('NoLedIndicator')
    def test_charging_at_slow_rate_mechanism_no_led(self):
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING_AT_SLOW_RATE,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        self.testCaseChecked("FUN_1004_0024#1")
    # end def test_charging_at_slow_rate_mechanism_no_led

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSupply')
    @services('ChargingAtSlowRate')
    @services('LedIndicator')
    def test_charging_at_slow_rate_mechanism(self):
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING_AT_SLOW_RATE,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        self.testCaseChecked("FUN_1004_0024#1")
        self.testCaseChecked("FUN_1004_0024#2")
    # end def test_charging_at_slow_rate_mechanism

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSupply')
    @services('PowerSwitch')
    @services('NoLedIndicator')
    def test_battery_insertion_and_removal_no_led(self):
        self.generic_battery_insertion_and_removal()

        self.testCaseChecked("FUN_1004_0025#1")
    # end def test_battery_insertion_and_removal_no_led

    @features('Feature1004')
    @level('Functionality')
    @services('PowerSupply')
    @services('LedIndicator')
    def test_battery_insertion_and_removal(self):
        self.generic_battery_insertion_and_removal()

        self.testCaseChecked("FUN_1004_0025#1")
        self.testCaseChecked("FUN_1004_0025#2")
    # end def test_battery_insertion_and_removal

    @features('Feature1004')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSwitch')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('LedIndicator')
    def test_end_of_charge_power_switch_off_unplug_charging_while_led_still_on(self):
        """
        Validate LED indicator behavior if charging cable is unplugged while the LED indicator is ON
        (5s green steady) to signal end of charge with power slider off.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite('Turn off the power switch')
        # --------------------------------------------------------------------------------------------------------------
        # TODO use PowerSwitch

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite('Pre-requisite#3: Restart the device with input voltage to GOOD level and a '
                                   'state_of_charge of 90%')
        # --------------------------------------------------------------------------------------------------------------
        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, 90, discharge=False)
        self.reset(hardware_reset=True, starting_voltage=battery_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode (i.e. connect USB cable)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        if self.f.PRODUCT.F_IsGaming:
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery value to 100%')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification (steady when end of charge reached)')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGE_COMPLETE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Unplug the charging cable during the first 5s')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED turns off immediately')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=.1)

        self.testCaseChecked("FUN_1004_0026")
    # end def test_end_of_charge_power_switch_off_unplug_charging_while_led_still_on

    @features('Feature1004')
    @features('Mice')
    @level('Functionality')
    @services('PowerSupply')
    @services('OpticalSensor')
    @services('LedIndicator')
    def test_led_behaviour_when_critical_level_mice(self):
        """
        Validate LED indicators match the LED Guidelines when reaching critical level in the following use cases:
         - device is moving (mice only)
         - device is lifted (mice only)
        """
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        low_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'low')
        battery_low = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, low_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the device with input voltage to LOW level')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_low)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a continuous displacement using the "OpticalSensor" service')
        # --------------------------------------------------------------------------------------------------------------
        # TODO add method to start (and do not stop until further notice) an non blocking optical sensor emulation

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set input voltage to CRITICAL level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait soc up-to-date')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                 'specification when critical level is reached while the mouse is moving')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=battery_critical, device_state=DeviceState.MOVING)
        # TODO add method to stop the previous non blocking optical sensor emulation

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the device with input voltage to CRITICAL level')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a lifted mice using the \'OpticalSensor\' service')
        # --------------------------------------------------------------------------------------------------------------
        # TODO add method to start (and do not stop until further notice) an non blocking optical sensor emulation

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Check Battery LED indicators with the LED Guidelines specification when critical level is reached '
                  'while the mouse is lifted')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=battery_critical, device_state=DeviceState.LIFTED)
        # TODO add method to stop the previous non blocking optical sensor emulation

        self.testCaseChecked("FUN_1004_0027")
    # end def test_led_behaviour_when_critical_level_mice

    @features('Feature1004')
    @features('Feature2201')
    @level('Functionality')
    @services('PowerSupply')
    @services('LedIndicator')
    def test_led_behaviour_when_critical_level_updating_dpi(self):
        """
        Validate LED indicators match the LED Guidelines when reaching critical level in the following use cases:
         - user is changing the DPI settings (mice with adjustable DPI only)
        """
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        low_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'low')
        battery_low = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, low_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite('Send Root.GetFeature(0x2201)')
        # --------------------------------------------------------------------------------------------------------------
        feature_2201_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=AdjustableDpi.FEATURE_ID)
        feature_2201 = AdjustableDpiFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetSensorDpi with sensorIdx = 0 to retrieve current Dpi value')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi = feature_2201.get_sensor_dpi_cls(deviceIndex=self.deviceIndex,
                                                         featureId=feature_2201_index,
                                                         sensorIdx=0)
        get_sensor_dpi_response = ChannelUtils.send(
                                    test_case=self,
                                    report=get_sensor_dpi,
                                    response_queue_name=HIDDispatcher.QueueName.MOUSE,
                                    response_class_type=feature_2201.get_sensor_dpi_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the device with input voltage to LOW level')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_low)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetSensorDpi with sensorIdx = 0, dpi not equal to the current Dpi value')
        # --------------------------------------------------------------------------------------------------------------
        dpi_value = AdjustableDpi.MIN_DPI_VALUE + \
            (int(get_sensor_dpi_response.dpi) + 1 - AdjustableDpi.MIN_DPI_VALUE) % \
            (AdjustableDpi.MAX_DPI_VALUE - AdjustableDpi.MIN_DPI_VALUE + 1)
        dpi_value = HexList(F"{dpi_value:0{feature_2201.set_sensor_dpi_cls.LEN.DPI // 4}X}")
        set_sensor_dpi = feature_2201.set_sensor_dpi_cls(deviceIndex=self.deviceIndex,
                                                         featureId=feature_2201_index,
                                                         sensorIdx=0,
                                                         dpi=dpi_value)
        ChannelUtils.send(
            test_case=self,
            report=set_sensor_dpi,
            response_queue_name=HIDDispatcher.QueueName.MOUSE,
            response_class_type=feature_2201.set_sensor_dpi_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set input voltage to CRITICAL level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait soc up-to-date')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Check Battery LED indicators comply with the LED Guidelines specification when '
                                 'critical level is reached while DPI settings are updated')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=battery_critical, device_state=DeviceState.DPI_UPDATED)

        self.testCaseChecked("FUN_1004_0028")
    # end def test_led_behaviour_when_critical_level_updating_dpi

    @features('Feature1004')
    @features('Mice')
    @level('Functionality')
    @services('PowerSupply')
    @services('OpticalSensor')
    @services('LedIndicator')
    def test_battery_insertion_and_removal_while_moving_mouse(self):
        """
        Validate Battery insertion and removal mice specific use cases:
         - the mouse is moving
        Check LED indicator.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the device using the power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [GOOD, CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(len(self.config.F_SupportedLevels)):
            if (int(self.config.F_SupportedLevels[i]) == -1) or \
                    (UnifiedBatteryTestUtils.get_level_from_index(self, index=i) != 'good' and
                     UnifiedBatteryTestUtils.get_level_from_index(self, index=i) != 'critical'):
                continue
            # end if
            state_of_charge = int(self.config.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, 'Emulate a continuous displacement using the "OpticalSensor" service')
            # ----------------------------------------------------------------------------------------------------------
            # TODO add method to start (and do not stop until further notice) an non blocking optical sensor emulation

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Turn on the device using the power supply service with voltage to {battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Check Battery LED indicators comply with the LED Guidelines specification when '
                                     'critical level is reached while the mouse is moving')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(battery_value=battery_value, device_state=DeviceState.MOVING)
            # TODO add method to stop the previous non blocking optical sensor emulation
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1004_0029")
    # end def test_battery_insertion_and_removal_while_moving_mouse

    @features('Feature1004')
    @level('DeepSleepWaitingTime')
    @services('PowerSupply')
    @services('MultiHost')
    @services('ButtonPressed')
    @services('LedIndicator')
    def test_led_behaviour_power_on_and_deep_sleep_disconnected_state(self):
        """
        Validate battery LED behavior at power on and wake up from deep sleep while the device is in a disconnected
        state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Turn off all the receivers usb ports to force the device in a "disconnected" state')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_enable_all_port = True
        for port_index in range(LibusbDriver.MAX_USB_PORT_COUNT):
            self.channel_disable(port_index)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the device using the power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [FULL.. CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(len(self.config.F_SupportedLevels)):
            if int(self.config.F_SupportedLevels[i]) == -1:
                continue
            # end if
            state_of_charge = int(self.config.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Turn on the device using the power supply service with voltage to {battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for battery_status_event response')
            # ----------------------------------------------------------------------------------------------------------
            # TODO Depending on the time it take to the device to reconnect the timeout might have to be changed
            battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                                                    self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are synchronized on both responses')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self,
                                                   first_event_response=battery_status_event,
                                                   second_event_response=get_status_response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                      'specification when device disconnected')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(battery_value=battery_value, device_state=DeviceState.DISCONNECTED)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter deep sleep')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wake up DUT by button clicking')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for battery_status_event response')
            # ----------------------------------------------------------------------------------------------------------
            # TODO Depending on the time it take to the device to reconnect the timeout might have to be changed
            battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                                                    self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are synchronized on both responses')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self,
                                                   first_event_response=battery_status_event,
                                                   second_event_response=get_status_response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                      'specification when device disconnected')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(battery_value=battery_value, device_state=DeviceState.DISCONNECTED)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn off the device using the power supply service')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1004_0030")
    # end def test_led_behaviour_power_on_and_deep_sleep_disconnected_state

    @features('Feature1004')
    @features('Bluetooth')
    @level('Functionality')
    @services('PowerSupply')
    @services('Debugger')
    @services('LedIndicator')
    def test_led_critical_mode(self):
        """
        Validate the DUT shall turn on the battery status LED when reaching the critical level
        but let it turn off on the following SOC changes.
        """
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Restart the device with input voltage to CRITICAL level and a state_of_charge of '
                  f'{critical_state_of_charge}%')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_critical, cleanup_battery_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for battery_status_event response at critical level')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                                                    self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, critical_state_of_charge),
            "battery_level_critical": (checker.check_critical_battery_level, 1),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.DISCHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.NO_POWER)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery Status LED is turn on when reaching the critical level')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=critical_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from '
                  f'{critical_state_of_charge - self.config.F_StateOfChargeStep}% '
                  f'to 0% by step of {self.config.F_StateOfChargeStep}%')
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(
                critical_state_of_charge - self.config.F_StateOfChargeStep, 0,
                -self.config.F_StateOfChargeStep):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge,
                                                                                   discharge=True)
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for battery_status_event response and check its input fields is valid')
            # ----------------------------------------------------------------------------------------------------------
            battery_status_event, _ = UnifiedBatteryTestUtils.wait_soc_computation(self)
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, state_of_charge)
            checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge, state_of_charge),
                "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3])
            })
            UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
                test_case=self, message=battery_status_event,
                expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery Status LED is NOT turn on on following soc changes')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(state_of_charge=state_of_charge)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1004_0031")
    # end def test_led_critical_mode
# end class UnifiedBatteryFunctionalityTestCase


class UnifiedBatteryFunctionalityMultiHostTestCase(UnifiedBatteryMultiReceiverGenericTest):
    """
    Validates Unified Battery with Multi Receivers TestCases
    """

    @features('Feature1004')
    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    def test_get_capabilities_after_reconnection_by_host_change(self):
        """
        Validate get_capabilities responses after a reconnection triggered by a host change,
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1814)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1814_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=ChangeHost.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send ChangeHost HID++ request to force the reconnection on another host')
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(self, host_index=1)

        # Switch communication channel to receiver on port 1
        status = self.channel_switch(
            device_uid=ChannelIdentifier(port_index=self.host_number_to_port_index(1), device_index=1))
        self.assertTrue(status, msg='The device do not connect on host 1')
        # Empty queue
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Host change succeeded')
        # --------------------------------------------------------------------------------------------------------------
        get_host_info_v1 = GetHostInfoV1(device_index=ChannelUtils.get_device_index(test_case=self),
                                         feature_index=self.feature_1814_index)
        get_host_info_v1_response = ChannelUtils.send(
            test_case=self,
            report=get_host_info_v1,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetHostInfoV1Response)

        self.assertEqual(expected=1,
                         obtained=to_int(get_host_info_v1_response.curr_host),
                         msg='The currHost parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_capabilities request')
        # --------------------------------------------------------------------------------------------------------------
        get_capabilities_response = UnifiedBatteryTestUtils.HIDppHelper.get_capabilities(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_capabilities response and check product-specific constants')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(
            test_case=self, message=get_capabilities_response,
            expected_cls=self.feature_1004.get_capabilities_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send ChangeHost HID++ request to force the reconnection on host 0')
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(self, host_index=0)

        # Switch communication channel to receiver on port 0 and remove notifications from other receivers
        status = self.channel_switch(
            device_uid=ChannelIdentifier(port_index=self.host_number_to_port_index(0), device_index=1))
        self.assertTrue(status, msg='The device do not connect on host 0')

        self.testCaseChecked("FUN_1004_0008#2")
    # end def test_get_capabilities_after_reconnection_by_host_change

    @features('Feature1004')
    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    @services('NoLedIndicator')
    def test_battery_status_event_after_changing_host_no_led(self):
        self.generic_battery_status_event_after_changing_host()

        self.testCaseChecked("FUN_1004_0010#1")
    # end def test_battery_status_event_after_changing_host_no_led

    @features('Feature1004')
    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    @services('LedIndicator')
    def test_battery_status_event_after_changing_host(self):
        self.generic_battery_status_event_after_changing_host()

        self.testCaseChecked("FUN_1004_0010#1")
        self.testCaseChecked("FUN_1004_0010#2")
    # end def test_battery_status_event_after_changing_host
# end class UnifiedBatteryFunctionalityMultiHostTestCase


class UnifiedBatteryFunctionalityGamingTestCase(UnifiedBatteryGamingTest):
    """
    Validate Unified Battery functionality with Gaming TestCases
    """

    @features('Feature1004')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_gaming_soc_decreasing_from_100_to_0_continuously(self):
        """
        Validate gaming device send battery_status_event from 100 to 0% while set voltage from full to cut-off voltage.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set voltage to {self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage + 0.05}v')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(round(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage + 0.05,
                                                     PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SoC start to decreasing from 100%.')
        # --------------------------------------------------------------------------------------------------------------
        expected_soc = 100
        sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
        battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(self)
        self.assertEqual(expected=expected_soc, obtained=to_int(battery_status_event.state_of_charge))
        expected_soc -= 1

        sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over SoC from 99% to 0%')
        # --------------------------------------------------------------------------------------------------------------
        while True:
            battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Check battery status event response is not none.')
            # ----------------------------------------------------------------------------------------------------------
            self.assertIsNotNone(obj=battery_status_event,
                                 msg=f"Battery status event should not be none, miss {expected_soc}% report")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check SoC decreasing continuously from 100% to 0%.')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_soc, obtained=to_int(battery_status_event.state_of_charge))
            expected_soc -= 1
            if expected_soc < 0:
                break
            # end if
            sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
        # end while
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1004_0033")
    # end def test_gaming_soc_decreasing_from_100_to_0_continuously

    @features('Feature1004')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_gaming_soc_update_immediately_after_power_reset_device(self):
        """
        Validate gaming device updates SoC immediately after power restart device at each battery levels.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over battery_level in range [FULL, GOOD, LOW, CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_set_input_voltage = True
        for i in range(len(self.config.F_SupportedLevels)):
            if not self.config.F_SupportedLevels[i]:
                continue
            # end if
            state_of_charge = int(self.config.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Power reset device by starting voltage = {battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the BatteryStatusEvent.SoC = {state_of_charge}')
            # ----------------------------------------------------------------------------------------------------------
            sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
            battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(self)
            adapted_soc = UnifiedBatteryTestUtils.adapt_soc(
                test_case=self, input_soc=battery_status_event.state_of_charge, expected_soc=state_of_charge)
            self.assertEqual(expected=state_of_charge, obtained=adapted_soc)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the GetStatus.SoC = {state_of_charge}')
            # ----------------------------------------------------------------------------------------------------------
            get_status_resp = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)
            adapted_soc = UnifiedBatteryTestUtils.adapt_soc(
                test_case=self, input_soc=get_status_resp.state_of_charge, expected_soc=state_of_charge)
            self.assertEqual(expected=state_of_charge, obtained=adapted_soc)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1004_0034")
    # end def test_gaming_soc_update_immediately_after_power_reset_device

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_charging_diode_effect(self):
        """
        In charging mode, Validate get_status when voltage level decrease slightly and cross the previous threshold.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [CRITICAL .. FULL]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(len(self.config.F_SupportedLevels)):
            supported_level = self.config.F_SupportedLevels[
                len(self.config.F_SupportedLevels) - i - 1]
            if int(supported_level) == -1:
                continue
            # end if

            battery_value_1 = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
                self, int(supported_level), discharge=True)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, f'Restart the device with input voltage {battery_value_1}')
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True,
                       starting_voltage=battery_value_1,
                       cleanup_battery_event=True)
            ChannelUtils.clean_messages(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=WirelessDeviceStatusBroadcastEvent,
                channel=self.current_channel.receiver_channel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request and wait response')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enter charging mode')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

            higher_battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
                self, int(supported_level), discharge=False)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Check {higher_battery_value} is greater than {battery_value_1} to simulate charging')
            # ----------------------------------------------------------------------------------------------------------
            # In order to prevent the set voltage from reaching the fully charged voltage, limit the maximum
            # battery value to F_MaximumVoltage - 20mV
            upper_limit_voltage = round(self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage - 0.02,
                                        PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1)
            if higher_battery_value > upper_limit_voltage:
                higher_battery_value = upper_limit_voltage
            # end if
            if int(supported_level) <= self.constant_v_threshold:
                self.assertGreater(higher_battery_value, battery_value_1,
                                   msg=f"{higher_battery_value} is not greater than {battery_value_1}")
            else:
                self.assertGreater(higher_battery_value, UnifiedBatteryTestUtils.DEFAULT_VOLTAGE_THRESHOLD,
                                   msg=f"{higher_battery_value} is not greater than "
                                       f"{UnifiedBatteryTestUtils.DEFAULT_VOLTAGE_THRESHOLD}")
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Force battery voltage to = {higher_battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(higher_battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for battery_status_event')
            # ----------------------------------------------------------------------------------------------------------
            if to_int(get_status_response.state_of_charge) <= self.constant_v_threshold:
                sleep(UnifiedBatteryTestUtils.TRANSITION_TIME_OF_ENTERING_CHARGING_MODE
                      + UnifiedBatteryTestUtils.CC_SAMPLING_TIME)
                battery_status_event = \
                    UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(self)
            else:
                battery_status_event, elapsed_time = \
                    UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_voltage_charging(
                        self, expected_soc=to_int(get_status_response.state_of_charge), is_first_report=True)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check first battery_status_event reporting time is valid')
                # ------------------------------------------------------------------------------------------------------
                UnifiedBatteryTestUtils.GamingDevicesHelper.check_battery_report_time_interval(
                    test_case=self,
                    state_of_charge=battery_status_event.state_of_charge,
                    elapsed_time=elapsed_time,
                    is_first_report=True)
            # end if

            expected_soc = to_int(battery_status_event.state_of_charge)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response_1 = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Wait for get_status response and check battery_level matches the input = {expected_soc}')
            # ----------------------------------------------------------------------------------------------------------
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, expected_soc)
            checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge, expected_soc),
                "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
                "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
                "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRED)
            })
            UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                test_case=self, message=get_status_response_1,
                expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Decrease the voltage to {battery_value_1}')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for battery_status_event')
            # ----------------------------------------------------------------------------------------------------------
            if to_int(get_status_response.state_of_charge) <= self.constant_v_threshold:
                battery_status_event = \
                    UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(self)
            else:
                battery_status_event, _ = \
                    UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_voltage_charging(
                        self, expected_soc=to_int(get_status_response.state_of_charge))
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no battery_status_event is broadcast')
            # ----------------------------------------------------------------------------------------------------------
            self.assertIsNone(obj=battery_status_event,
                              msg=f"[{self.current_channel}] {HIDDispatcher.QueueName.EVENT} not empty, "
                                  f"received {battery_status_event}")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request and wait response')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response_2 = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are aligned with the first response')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self,
                                                   first_event_response=get_status_response_1,
                                                   second_event_response=get_status_response_2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Exit charging mode')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1004_0035")
    # end def test_charging_diode_effect

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_battery_status_event_under_constant_current_charging(self):
        """
        In charging mode, validate gaming device reports battery_status_event in every 8 seconds and reports with each
        percentage of SoC when the device is under SoC 0-50% or 0-40% of charging mode. ('Synergy' or 'High Power')

        Note:
        The SoC testing range depends on the battery source.

        cf https://docs.google.com/document/d/1ArpYWbkJ2YVWhJLxjY016YT_C718-xCIhWZXoCNAPD0/edit#heading=h.n885m69fgyvk
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        soc_step = self.config.F_StateOfChargeStep
        get_status_response = None
        last_soc = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f'Restart the device with input voltage to {self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage + 0.05}V')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=round(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage + 0.05,
                                          PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1),
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over state_of_charge value from 0-{self.constant_v_threshold}%'
                                 f' by {soc_step}% SoC step')
        # --------------------------------------------------------------------------------------------------------------
        for soc in range(soc_step, self.constant_v_threshold + soc_step, soc_step):
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, soc, discharge=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery value to {battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over state_of_charge each percentage in SoC step value {soc_step}')
            # ----------------------------------------------------------------------------------------------------------
            for each_percentage_soc in range(soc - soc_step + 1, soc + 1):
                if get_status_response is not None:
                    last_soc = get_status_response.state_of_charge
                # end if
                if each_percentage_soc == 1:
                    sleep(UnifiedBatteryTestUtils.TRANSITION_TIME_OF_ENTERING_CHARGING_MODE
                          + UnifiedBatteryTestUtils.CC_SAMPLING_TIME)
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Perform user action to keep the DUT in run mode')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.user_action()

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait and check battery_status_event')
                # ------------------------------------------------------------------------------------------------------
                battery_status_event = \
                    UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                        self, continuously_receive=False)
                self.assertIsNotNone(
                    obj=battery_status_event,
                    msg=f"Miss {each_percentage_soc}% SoC report, battery_status_event should not be None.")
                battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, each_percentage_soc)
                checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "state_of_charge": (checker.check_state_of_charge, each_percentage_soc),
                    "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                    "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                    "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                    "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
                    "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
                    "external_power_status": (checker.check_external_power_status,
                                              UnifiedBattery.ExternalPowerStatus.WIRED)
                })
                UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
                    test_case=self, message=battery_status_event,
                    expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the received SoC values are in increasing order')
                # ------------------------------------------------------------------------------------------------------
                if get_status_response is not None:
                    self.assertEqual(obtained=to_int(battery_status_event.state_of_charge),
                                     expected=to_int(last_soc) + 1,
                                     msg="The state_of_charge parameter is not in increasing order")
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the battery LED indicators when charging')
                # ------------------------------------------------------------------------------------------------------
                self.check_led_behaviour(state_of_charge=each_percentage_soc)

            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Exit charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        self.testCaseChecked('FUN_1004_0036')
    # end def test_battery_status_event_under_constant_current_charging

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_battery_status_event_under_constant_voltage_charging(self):
        """
        In charging mode, validate gaming device reports battery_status_event with each percentage of SoC and check the
        reporting rate is following the table of constant voltage charging when the device is under constant voltage
        charging mode.

        Note:
        The SoC testing range depends on the battery source. For 'Synergy', the range will be 50-99%, but for
        'High Power' the range will be 40-99%

        cf https://docs.google.com/document/d/1ArpYWbkJ2YVWhJLxjY016YT_C718-xCIhWZXoCNAPD0/edit#heading=h.n885m69fgyvk
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        soc_step = self.config.F_StateOfChargeStep
        battery_status_event = None
        set_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, self.constant_v_threshold, discharge=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Restart the device with input voltage {set_voltage}')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=set_voltage,
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent,
            channel=self.current_channel.receiver_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, self.constant_v_threshold, discharge=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set battery value to {battery_value}')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Wait for the {self.constant_v_threshold}% SoC battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.TRANSITION_TIME_OF_ENTERING_CHARGING_MODE
              + UnifiedBatteryTestUtils.CC_SAMPLING_TIME)
        report_soc = 0
        while report_soc < self.constant_v_threshold:
            battery_status_event = \
                UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                    self, continuously_receive=False)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check battery status event is not None')
            # ----------------------------------------------------------------------------------------------------------
            self.assertIsNotNone(battery_status_event,
                                 msg=f'Miss {report_soc + 1}% SoC report, battery_status_event should not be None.')
            report_soc = to_int(battery_status_event.state_of_charge)
        # end while
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status,
                                      UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over state_of_charge value from {self.constant_v_threshold} to 100%'
                                 f' by {soc_step}% SoC step')
        # --------------------------------------------------------------------------------------------------------------
        for soc in range(self.constant_v_threshold, 100, soc_step):
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, soc + soc_step,
                                                                                   discharge=False)
            last_soc = soc
            # In order to prevent the set voltage reaches the voltage of charging completion, so limits the maximum
            # battery value to F_MaximumVoltage - 20mV
            battery_value = battery_value if battery_value < self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage - 0.02 \
                else battery_value - 0.02
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery value to {battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over state_of_charge each percentage in SoC step value {soc_step}')
            # ----------------------------------------------------------------------------------------------------------
            for each_percentage_soc in range(soc + 1, soc + soc_step + 1):
                if each_percentage_soc == 100:
                    break
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Wait for battery_status_event')
                # ------------------------------------------------------------------------------------------------------
                battery_status_event, elapsed_time = \
                    UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_voltage_charging(
                        self, expected_soc=each_percentage_soc)

                # --------------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check reporting time interval of battery_status_event is valid')
                # --------------------------------------------------------------------------------------------------------------
                UnifiedBatteryTestUtils.GamingDevicesHelper.check_battery_report_time_interval(
                    self, battery_status_event.state_of_charge, elapsed_time)
                battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, each_percentage_soc)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check battery_status_event fields are valid')
                # ------------------------------------------------------------------------------------------------------
                checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "state_of_charge": (checker.check_state_of_charge, each_percentage_soc),
                    "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                    "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                    "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                    "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
                    "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
                    "external_power_status": (checker.check_external_power_status,
                                              UnifiedBattery.ExternalPowerStatus.WIRED)
                })
                UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
                    test_case=self, message=battery_status_event,
                    expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send get_status request and wait response')
                # ------------------------------------------------------------------------------------------------------
                get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for get_status response and check all battery properties are '
                                          'synchronized on both response')
                # ------------------------------------------------------------------------------------------------------
                UnifiedBatteryTestUtils.compare_status(self,
                                                       first_event_response=battery_status_event,
                                                       second_event_response=get_status_response)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the received SoC values are in increasing order')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(obtained=to_int(get_status_response.state_of_charge),
                                 expected=last_soc + 1,
                                 msg="The state_of_charge parameter is not in increasing order")
                last_soc = each_percentage_soc

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the battery LED indicators when charging')
                # ------------------------------------------------------------------------------------------------------
                self.check_led_behaviour(state_of_charge=each_percentage_soc)

            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Exit charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        self.testCaseChecked('FUN_1004_0037')
    # end def test_battery_status_event_under_constant_voltage_charging

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_end_of_charging_detection(self):
        """
        In charging mode, validate gaming device end of charge detection and notification.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, f'Restart the device with input voltage {self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage - 0.03}V')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=round(self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage - 0.03,
                                          PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1),
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent,
            channel=self.current_channel.receiver_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set battery value to {self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage + 0.05}')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage + 0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait charging completed battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery_status_event is fully charged')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, 100),
            "battery_level_full": (checker.check_full_battery_level, 1),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGE_COMPLETE),
            "external_power_status": (checker.check_external_power_status,
                                      UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check all battery properties are '
                                  'synchronized on both response')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.compare_status(self,
                                               first_event_response=battery_status_event,
                                               second_event_response=get_status_response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators when charging completed')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Exit charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        self.testCaseChecked('FUN_1004_0038')
    # end def test_end_of_charging_detection

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('WirelessCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_end_of_charging_detection_wireless(self):
        """
        In charging mode, validate the device stops charging when the voltage reaches 4.12V and check the end of charge
        detection and notification.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage 4.0V')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=4.0,
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent,
            channel=self.current_channel.receiver_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self,
                                                           source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery value to 4.10V')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(4.10)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get status response and check charging status = '
                                  f'{UnifiedBattery.ChargingStatus.CHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        checker.check_charging_status(test_case=self,
                                      response=get_status_response,
                                      expected=UnifiedBattery.ChargingStatus.CHARGING)
        checker.check_external_power_status(test_case=self,
                                            response=get_status_response,
                                            expected=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set battery value to {UnifiedBatteryTestUtils.FULL_CHARGE_VOLTAGE_CP} V')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(UnifiedBatteryTestUtils.FULL_CHARGE_VOLTAGE_CP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the charging status is {UnifiedBattery.ChargingStatus.DISCHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        checker.check_charging_status(test_case=self,
                                      response=battery_status_event,
                                      expected=UnifiedBattery.ChargingStatus.DISCHARGING)
        checker.check_external_power_status(test_case=self,
                                            response=battery_status_event,
                                            expected=UnifiedBattery.ExternalPowerStatus.NO_POWER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check charging status = '
                                  f'{UnifiedBattery.ChargingStatus.DISCHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        checker.check_charging_status(test_case=self,
                                      response=get_status_response,
                                      expected=UnifiedBattery.ChargingStatus.DISCHARGING)
        checker.check_external_power_status(test_case=self,
                                            response=get_status_response,
                                            expected=UnifiedBattery.ExternalPowerStatus.NO_POWER)

        self.testCaseChecked('FUN_1004_0039')
    # end def test_end_of_charging_detection_wireless

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('WirelessCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_restart_charging_mechanism_wireless(self):
        """
        In charging mode, validate the device restarts charging when the voltage drops lower than 4.0V.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage 4.10V')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=4.10,
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent,
            channel=self.current_channel.receiver_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self,
                                                           source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get status response and check charging status = '
                                  f'{UnifiedBattery.ChargingStatus.CHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        checker.check_charging_status(test_case=self,
                                      response=get_status_response,
                                      expected=UnifiedBattery.ChargingStatus.CHARGING)
        checker.check_external_power_status(test_case=self,
                                            response=get_status_response,
                                            expected=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set battery value to {UnifiedBatteryTestUtils.FULL_CHARGE_VOLTAGE_CP}V')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(UnifiedBatteryTestUtils.FULL_CHARGE_VOLTAGE_CP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the charging status is {UnifiedBattery.ChargingStatus.DISCHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        checker.check_charging_status(test_case=self,
                                      response=battery_status_event,
                                      expected=UnifiedBattery.ChargingStatus.DISCHARGING)
        checker.check_external_power_status(test_case=self,
                                            response=battery_status_event,
                                            expected=UnifiedBattery.ExternalPowerStatus.NO_POWER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set battery value to {UnifiedBatteryTestUtils.RESTART_CHARGE_VOLTAGE_CP-0.02}V')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(UnifiedBatteryTestUtils.RESTART_CHARGE_VOLTAGE_CP-0.02)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for SoC decreasing')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW * 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                                                                                    self, continuously_receive=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the charging status is {UnifiedBattery.ChargingStatus.CHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        checker.check_charging_status(test_case=self,
                                      response=battery_status_event,
                                      expected=UnifiedBattery.ChargingStatus.CHARGING)
        checker.check_external_power_status(test_case=self,
                                            response=battery_status_event,
                                            expected=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check charging status = '
                                  f'{UnifiedBattery.ChargingStatus.CHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        checker.check_charging_status(test_case=self,
                                      response=get_status_response,
                                      expected=UnifiedBattery.ChargingStatus.CHARGING)
        checker.check_external_power_status(test_case=self,
                                            response=get_status_response,
                                            expected=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        self.testCaseChecked('FUN_1004_0040')
    # end def test_restart_charging_mechanism_wireless
# end class UnifiedBatteryFunctionalityGamingTestCase


class UnifiedBatteryRepeatedBleFunctionalityTestCases(UnifiedBatteryGenericTest):
    """
    Repeated subset of tests from UnifiedBatteryFunctionalityTestCase in ble protocol to ensure validating BLE BAS
    """

    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    @features('Feature1004')
    @features('BLEProtocol')
    @level('Functionality')
    @services('PowerSupply')
    @services('Debugger')
    def test_all_soc_ble(self):
        """
        Verify all state of charge in discharge for BLE protocol
        """
        self.generic_all_soc_ble()

        self.testCaseChecked("FUN_1004_0007#1")
        self.testCaseChecked("FUN_1004_0007#2")
    # end def test_all_soc_ble

    @features('Feature1004')
    @features('BLEProtocol')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Time-consuming')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('NoLedIndicator')
    @services('ChargingWithoutConnection')
    def test_usb_charging_mechanism_no_led(self):
        """
        Verify usb charging mechanism
        """
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRED)
        
        self.testCaseChecked("FUN_1004_0016#1")
    # end def test_usb_charging_mechanism_no_led

    @features('Feature1004')
    @features('BLEProtocol')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Time-consuming')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('LedIndicator')
    @services('ChargingWithoutConnection')
    def test_usb_charging_mechanism(self):
        """
        Verify usb charging mechanism
        """
        self.generic_charging_mechanism(charging_type=UnifiedBattery.ChargingStatus.CHARGING,
                                        source=UnifiedBattery.ExternalPowerStatus.WIRED)

        self.testCaseChecked("FUN_1004_0016#1")
        self.testCaseChecked("FUN_1004_0016#2")
    # end def test_usb_charging_mechanism

    @features('Feature1004')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('ChargingWithoutConnection')
    def test_end_of_charge_mechanism_no_led(self):
        self.generic_end_of_charge_mechanism()

        self.testCaseChecked("FUN_1004_0017#1")
    # end def test_end_of_charge_mechanism_no_led
# end class UnifiedBatteryRepeatedBleFunctionalityTestCases
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
