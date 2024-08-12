#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1004.unifiedbattery
:brief: HID++ 2.0 Unified Battery test case
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/10/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue
from copy import copy
from time import sleep

from pychannel.blechannel import BleChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.core import TYPE_SUCCESS
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidmouse import HidMouse
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.changehost import ChangeHost
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.oobstate import OobStateFactory
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryFactory
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.numeral import to_int
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceState:
    """
    Define the possible device states
    """
    OFF = 0
    RUN = 1
    SLEEP = 2
    DEEP_SLEEP = 3
    RESTARTING = 4
    DISCONNECTED = 5
    RECONNECTION = 6
    MOVING = 7
    LIFTED = 8
    DPI_UPDATED = 9
# end class DeviceState


class UnifiedBatteryGenericTest(BaseTestCase):
    """
    Common Unified Battery Test Class
    """
    # Timing during which the battery measurement are done from 80% to 100%
    BATTERY_MEASURE_END_OF_CHARGE_WINDOW = 210  # 200s on Zaha
    # Power supply board resolution is 10mV
    POWER_BOARD_RESOLUTION = 10

    def setUp(self):
        """
        Handle test prerequisites.

        :raise ``ValueError``: If the battery source index is not supported
        """
        self.post_requisite_set_input_voltage = False
        self.post_requisite_disable_ble = False
        self.post_requisite_enable_all_usb_ports = False
        # If post_requisite_nvs_parser not None, the Parser object trigger the reloading of the NVS data in tearDown()
        self.post_requisite_nvs_parser = None
        self.post_requisite_rechargeable = False
        self.post_requisite_discharge_super_cap = False
        # The SoC threshold between constant current charging mode and constant voltage charging mode
        self.constant_v_threshold = 0
        self.external_power_source = None
        # In BLE direct mode activate extra checks on BAS battery service alignment with the 0x1004 feature
        self.check_ble_bas_service = False
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1D4B)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1d4b =\
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1004)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1004_index = ChannelUtils.update_feature_mapping(test_case=self,
                                                                      feature_id=UnifiedBattery.FEATURE_ID)
        self.config = self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY
        self.feature_1004 = UnifiedBatteryFactory.create(self.config_manager.get_feature_version(self.config))

        # Empty event_message_queue from BatteryStatus & WirelessDeviceStatusBroadcast notifications sent by the device
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
            class_type=(self.feature_1004.battery_status_event_cls, WirelessDeviceStatusBroadcastEvent))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable LED monitoring on battery indicator')
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # Set constant voltage threshold
        if self.config.F_BatterySourceIndex == 1:
            # Synergy battery constant voltage threshold
            self.constant_v_threshold = 50
        elif self.config.F_BatterySourceIndex == 2:
            # High Power battery constant voltage threshold
            self.constant_v_threshold = 40
        elif self.config.F_BatterySourceIndex != 0:
            raise ValueError('Unsupported index of battery source:'
                             f' {self.config.F_BatterySourceIndex}')
        # end if

        if isinstance(self.current_channel, BleChannel) and self.hasFeature("BAS1.1"):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Subscribe to BAS notifications")
            # ----------------------------------------------------------------------------------------------------------
            self.check_ble_bas_service = True
            self.bas_level_notification = BleProtocolTestUtils.subscribe_notification(
                test_case=self,
                ble_context_device=self.current_channel.get_ble_context_device(),
                service_uuid=BleUuid(BleUuidStandardService.BATTERY_SERVICE),
                characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL))
            self.bas_status_notification = BleProtocolTestUtils.subscribe_notification(
                test_case=self,
                ble_context_device=self.current_channel.get_ble_context_device(),
                service_uuid=BleUuid(BleUuidStandardService.BATTERY_SERVICE),
                characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL_STATUS))
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_rechargeable:
                self.power_supply_emulator.recharge(enable=False)
                if self.external_power_source is not None:
                    DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self,
                                                                      source=self.external_power_source)
                # end if
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_nvs_parser is not None:
                if self.post_requisite_disable_ble:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(
                        self, 'Disable the connection with the BLE Pro receiver (i.e.: load the UFY pairing config '
                              'into NVS)')
                    # --------------------------------------------------------------------------------------------------
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, 'Reload current NVS')
                    # --------------------------------------------------------------------------------------------------
                # end if
                self.debugger.reload_file(nvs_hex_file=self.post_requisite_nvs_parser.to_hex_file())
                self.post_requisite_nvs_parser = None
            # end if
        # end with

        with self.manage_kosmos_post_requisite():
            if self.post_requisite_set_input_voltage:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Set input voltage to its maximum value')
                # ------------------------------------------------------------------------------------------------------
                self.power_supply_emulator.set_voltage(self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

                self.post_requisite_set_input_voltage = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_enable_all_usb_ports:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Turn on all the receivers usb ports to restore the device '
                                                   'in a "connected" state')
                # ------------------------------------------------------------------------------------------------------
                self.device.enable_all_usb_ports()

                self.post_requisite_enable_all_usb_ports = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.backup_dut_channel.protocol in LogitechProtocol.gaming_protocols() and \
                    self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(
                    self, f"Power off USB Port {self.device.CHARGING_PORT_NUMBER} and switch to receiver channel")
                # ------------------------------------------------------------------------------------------------------
                # Leave from USB channel if the DUT is a gaming device, otherwise do nothing
                ProtocolManagerUtils.exit_usb_channel(self)
                self.cleanup_battery_event_from_queue()
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_discharge_super_cap:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Discharge the supercap')
                # ------------------------------------------------------------------------------------------------------
                self.device.turn_off_crush_pad_charging_emulator()
                self.power_supply_emulator.turn_on(voltage=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage)
                sleep(UnifiedBatteryTestUtils.DISCHARGE_SUPERCAP_TIME)
                self.post_requisite_discharge_super_cap = False
            # end if
        # end with

        # End with super tearDown()
        super().tearDown()
    # end def tearDown

    def generic_all_soc_ufy(self):
        """
        Validate get_status.state_of_charge for each level (cf state_of_charge step) when connected thru Unifying
        protocol.
        Check event sent at each level change and data match actual measurement.
        Check LED indicator.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from '
                  f'{100 - self.config.F_StateOfChargeStep}% to 10% by step of '
                  f'{self.config.F_StateOfChargeStep}%')
        # --------------------------------------------------------------------------------------------------------------
        state_of_charge = 100
        for battery_value in self.config.F_DischargeSOCmV[:-1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(round(int(battery_value) / UnifiedBatteryTestUtils.V_UNIT_CONVERT,
                                                   PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for battery_status_event response and check '
                                      f'state_of_charge matches the input = {state_of_charge}')
            # ----------------------------------------------------------------------------------------------------------
            battery_status_event, _ = UnifiedBatteryTestUtils.wait_soc_computation(self)
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(
                                                              self, battery_status_event.state_of_charge)
            battery_status_event.state_of_charge = \
                UnifiedBatteryTestUtils.adapt_soc(test_case=self, input_soc=battery_status_event.state_of_charge,
                                                  expected_soc=state_of_charge)

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
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)
            get_status_response.state_of_charge = \
                UnifiedBatteryTestUtils.adapt_soc(test_case=self, input_soc=get_status_response.state_of_charge,
                                                  expected_soc=state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check state_of_charge '
                                      f'matches the input = {state_of_charge}')
            # ----------------------------------------------------------------------------------------------------------
            checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge, state_of_charge),
                "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
                "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.DISCHARGING),
                "external_power_status": (checker.check_external_power_status,
                                          UnifiedBattery.ExternalPowerStatus.NO_POWER)
            })
            UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                test_case=self, message=get_status_response,
                expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED '
                                      'Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(state_of_charge=state_of_charge)

            state_of_charge -= self.config.F_StateOfChargeStep
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification for  critical level')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(critical=True)
    # end def generic_all_soc_ufy

    def generic_all_soc_ble(self):
        """
        Validate get_status.state_of_charge for each level when connected thru BLE protocol.
        Check event sent at each level change and data match actual measurement.
        Check LED indicator.

        :raise ``tuple``: [``AssertionError``] If the battery notification was not received or
                          [``AttributeError``] If the battery state of charge is not correct
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch to the Host matching the BLE receiver')
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from 100% to 5% by step of '
                  f'{self.config.F_StateOfChargeStep}%')
        # --------------------------------------------------------------------------------------------------------------
        state_of_charge = 100
        skip_next_battery_value = False
        discharging_soc_voltage_list = [voltage for voltage in self.config.F_DischargeSOCmV[:-1]]
        retry_count = 0 if self.f.PRODUCT.F_IsGaming else 1
        decrease_5mv = False
        previous_voltage = None
        while len(discharging_soc_voltage_list) > 0:
            if decrease_5mv:
                # PWS devices allow to retry once with decreasing 5mV
                battery_value = previous_voltage - 5
                decrease_5mv = False
            else:
                battery_value = discharging_soc_voltage_list.pop(0)
            # end if
            if skip_next_battery_value:
                # Battery notification already sent by the DUT
                skip_next_battery_value = False
                continue
            # end if
            try:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
                # ------------------------------------------------------------------------------------------------------
                self.power_supply_emulator.set_voltage(
                    round(int(battery_value) / UnifiedBatteryTestUtils.V_UNIT_CONVERT,
                          PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for battery_status_event response and check '
                                          f'state_of_charge matches the input = {state_of_charge}')
                # ------------------------------------------------------------------------------------------------------
                battery_status_event, penultimate_event = UnifiedBatteryTestUtils.wait_soc_computation(self)
                # make a no adapted copy for ble check
                battery_status_event_copy = copy(battery_status_event)
                battery_status_event.state_of_charge = UnifiedBatteryTestUtils.adapt_soc(
                    test_case=self, input_soc=battery_status_event.state_of_charge, expected_soc=state_of_charge)
                checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
                check_map = checker.get_default_check_map(self)
                if penultimate_event is not None:
                    # This is the case when we receive 2 notifications for a single voltage decrement
                    battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, state_of_charge)
                    check_map.update({
                        "state_of_charge": (checker.check_state_of_charge, state_of_charge),
                        "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                        "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                        "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                        "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3])
                    })
                    UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
                        test_case=self, message=penultimate_event,
                        expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)
                    # Update the state of charge to validate the second notification
                    state_of_charge -= self.config.F_StateOfChargeStep
                    LogHelper.log_info(self, 'Warning: 2 battery notifications received in a single voltage decrement')
                    skip_next_battery_value = True
                # end if
                battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(
                    self, battery_status_event_copy.state_of_charge)
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

                self.check_ble_notifications(battery_status_event_copy)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send get_status request')
                # ------------------------------------------------------------------------------------------------------
                get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)
                # make a no adapted copy for ble check
                get_status_response_copy = copy(get_status_response)
                get_status_response.state_of_charge = UnifiedBatteryTestUtils.adapt_soc(
                    test_case=self, input_soc=get_status_response.state_of_charge, expected_soc=state_of_charge)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for get_status response and check state_of_charge '
                                          f'matches the input = {state_of_charge}')
                # ------------------------------------------------------------------------------------------------------
                checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "state_of_charge": (checker.check_state_of_charge, state_of_charge),
                    "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                    "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                    "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                    "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3])
                })
                UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                    test_case=self, message=get_status_response,
                    expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

                self.check_ble_read(get_status_response_copy)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED '
                                          'Guidelines specification')
                # ------------------------------------------------------------------------------------------------------
                self.check_led_behaviour(state_of_charge=state_of_charge)

                # Update parameters for the next run
                state_of_charge -= self.config.F_StateOfChargeStep
                retry_count = 0 if self.f.PRODUCT.F_IsGaming else 1
            except (AssertionError, AttributeError):
                if retry_count:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, 'Decrease 5mV and retry again....')
                    # --------------------------------------------------------------------------------------------------
                    decrease_5mv = True
                    previous_voltage = int(battery_value)
                    retry_count = 0
                else:
                    raise
                # end if
            # end try
        # end while
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification for critical level')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(critical=True)
        # Empty hid_message_queue from HidMouse and HidKeyboard notifications sent by the receiver
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.HID,
            class_type=(HidMouse, HidKeyboard))

    # end def generic_all_soc_ble

    def generic_battery_event_link_loss(self):
        """
        Validate battery_status_event notification and get_status.battery_level after a reconnection triggered by a
        receiver link loss. Check event data match actual measurement.
        Check LED indicator.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the device at a CRITICAL battery level')
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self, starting_voltage=battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch off all the UFY receivers usb ports')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_enable_all_usb_ports = True
        if ChannelUtils.get_port_index(test_case=self) != LibusbDriver.CHARGING_PORT_NUMBER:
            ChannelUtils.close_channel(test_case=self)
        # end if
        self.device.disable_all_usb_ports()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification at disconnection (No change on LED\'s)')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=critical_state_of_charge,
                                 device_state=DeviceState.DISCONNECTED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch on all the UFY receivers usb ports')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_all_usb_ports()
        self.post_requisite_enable_all_usb_ports = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wake up DUT by button clicking')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        self.channel_switch(device_uid=ChannelIdentifier(port_index=self.host_number_to_port_index(0), device_index=1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                                                    self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check all battery properties '
                                  'are synchronized on both responses')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.compare_status(self,
                                               first_event_response=battery_status_event,
                                               second_event_response=get_status_response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification at reconnection (No change on LED\'s)')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=critical_state_of_charge,
                                 device_state=DeviceState.RECONNECTION)
    # end def generic_battery_event_link_loss

    def generic_battery_status_event_after_changing_host(self):
        """
        Validate battery_status_event notification and get_status.battery_level after a reconnection triggered by a
        ChangeHost request.
        Check event data match actual measurement.
        Check LED indicator.
        """
        disabled_host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1814)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1814_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=ChangeHost.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Disable the next receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_enable_all_usb_ports = True
        self.channel_disable(self.host_number_to_port_index(disabled_host_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a ChangeHost request to switch to the disabled receiver '
                                 'then wait for the device to come back to the current host')
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=self.deviceIndex, host_index=disabled_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        # Empty event_message_queue from BatteryLevelStatusBroadcastEvent notifications sent by the device
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent)
        battery_status_event, _ = UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check all battery properties '
                                  'are synchronized on both responses')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.compare_status(self,
                                               first_event_response=battery_status_event,
                                               second_event_response=get_status_response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification at reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Switch on the next receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(self.host_number_to_port_index(disabled_host_index))
        self.post_requisite_enable_all_usb_ports = False
    # end def generic_battery_status_event_after_changing_host

    def generic_battery_event_restart(self):
        """
        Validate battery_status_event notification and get_status.battery_level after a power off / on using the power
        supply (to emulate a battery change).
        Check event data match actual measurement.
        Check LED indicator.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device using the power supply service')
        # --------------------------------------------------------------------------------------------------------------
        nominal_voltage = self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self, starting_voltage=nominal_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                                                    self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check all battery properties '
                                  'are synchronized on both responses')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.compare_status(self,
                                               first_event_response=battery_status_event,
                                               second_event_response=get_status_response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification at restart')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage,
                                 device_state=DeviceState.RESTARTING)
    # end def generic_battery_event_restart

    def generic_battery_event_power_switch(self):
        """
        Validate battery_status_event notification and get_status.battery_level after a power off / on using the
        power slider.
        Check event data match actual measurement and LED indicators in every possible battery_level.
        Check LED behaviors while device is turned off.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the device using the power switch')
        # --------------------------------------------------------------------------------------------------------------
        # TODO use PowerSwitch

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [FULL..CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(len(self.config.F_SupportedLevels)):
            if int(self.config.F_SupportedLevels[i]) == -1:
                continue
            # end if
            state_of_charge = int(self.config.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {battery_value}V')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Power on the device using the power switch service')
            # ----------------------------------------------------------------------------------------------------------
            # TODO use PowerSwitch

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for battery_status_event')
            # ----------------------------------------------------------------------------------------------------------
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
            LogHelper.log_step(self, 'Wait for the LED to light up')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_led_on_off(wait_on=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn off the device')
            # ----------------------------------------------------------------------------------------------------------
            # TODO use PowerSwitch

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check LED turns off immediately')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_led_on_off(wait_on=False, timeout=.1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn on the device')
            # ----------------------------------------------------------------------------------------------------------
            # TODO use PowerSwitch

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED '
                                      'Guidelines specification at restart')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(state_of_charge=state_of_charge, device_state=DeviceState.RESTARTING)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Power off the device using the power switch service')
            # ----------------------------------------------------------------------------------------------------------
            # TODO use PowerSwitch
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the device with voltage below cut-off value')
        # --------------------------------------------------------------------------------------------------------------
        # TODO use PowerSwitch
        self.reset(hardware_reset=True, starting_voltage=self.f.PRODUCT.DEVICE.BATTERY.F_CutoffVoltage - 0.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all LEDs are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False)
    # end def generic_battery_event_power_switch

    def generic_battery_event_deep_sleep(self):
        """
        Validate get_status when returning from Deep Sleep with battery level from highest to lowest.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [FULL..CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_set_input_voltage = True
        for i in range(len(self.config.F_SupportedLevels)):
            if not self.config.F_SupportedLevels[i]:
                continue
            # end if
            state_of_charge = int(self.config.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter deep sleep')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Force battery voltage to enter the targeted battery_level = {battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wake up DUT by button clicking')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
            if self.f.PRODUCT.F_IsGaming:
                UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation(self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED '
                                      'Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(state_of_charge=state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            expected_soc = to_int(get_status_response.state_of_charge)
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, soc=expected_soc)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Wait for get_status response and check battery level matches {battery_level_status}')
            # ----------------------------------------------------------------------------------------------------------
            checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge, expected_soc),
                "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3])
            })
            UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                test_case=self, message=get_status_response,
                expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_battery_event_deep_sleep

    def generic_battery_diode_effect(self):
        """
        Validate get_status when battery level increases slightly and cross the previous threshold
        (Enforce the diode effect mechanism). Check every possible transition.

        :raise ``AssertionError``: if the supported levels list is empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [GOOD .. CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_set_input_voltage = True
        first_index_to_parse = -1
        previous_level = -1
        for i in range(len(self.config.F_SupportedLevels)):
            if self.config.F_SupportedLevels[i]:
                previous_level = i
                first_index_to_parse = i + 1
                break
            # end if
        # end for
        assert first_index_to_parse > 0 and previous_level >= 0, "No supported level found, should not happen"

        for i in range(first_index_to_parse, len(self.config.F_SupportedLevels)):
            if int(self.config.F_SupportedLevels[i]) == -1:
                continue
            # end if
            state_of_charge = int(self.config.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Force battery voltage to enter the targeted battery_level = {battery_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait soc up-to-date')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.wait_soc_computation(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response_1 = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            expected_soc = to_int(get_status_response_1.state_of_charge)
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, soc=expected_soc)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Wait for get_status response and check battery_level matches the input={battery_level_status}')
            # ----------------------------------------------------------------------------------------------------------
            checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge, expected_soc),
                "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3])
            })
            UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                test_case=self, message=get_status_response_1,
                expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

            # Empty event_message_queue from BatteryStatusEvent notifications sent by the device
            ChannelUtils.clean_messages(
                test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
                class_type=self.feature_1004.battery_status_event_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Increase the voltage to cross the threshold to the closest higher level')
            # ----------------------------------------------------------------------------------------------------------
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
                self, state_of_charge + self.config.F_StateOfChargeStep)
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no battery_status_event is broadcast')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(
                test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
                timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW,
                class_type=self.feature_1004.battery_status_event_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response_2 = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are aligned with the first response')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self,
                                                   first_event_response=get_status_response_1,
                                                   second_event_response=get_status_response_2)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_battery_diode_effect

    def generic_measurement_timing(self):
        """
        Check the firmware always take less than a minute to trigger a battery level measurement in run mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable to J-Link RTT monitoring service')
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from 100% to 10% by step of '
                  f'{self.config.F_StateOfChargeStep}%')
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(100, 9, -self.config.F_StateOfChargeStep):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for 1 minute')
            # ----------------------------------------------------------------------------------------------------------
            sleep(UnifiedBatteryTestUtils.MINUTE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check a battery level measurement has been done by the firmware')
            # ----------------------------------------------------------------------------------------------------------
            # TODO
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_measurement_timing

    def generic_charging_mechanism(self, charging_type, source):
        """
        Validate device charging mechanism and battery level from lowest to highest.
        OR
        Test PowerPlay wireless charging system and validate 'wireless charging' charging status is correctly handled.
        OR
        Simulate an ineffective charging system and validate 'charging at slow rate' charging status is returned
        Test the use case  when the battery is being charged but the external power source cannot supply the full
        charge current that device can accept.

        Check LED indicators.

        :param charging_type: Charging status reported by the ``UnifiedBattery`` feature
        :type charging_type: ``UnifiedBattery.ChargingStatus``
        :param source: Power status reported by the ``UnifiedBattery`` feature
        :type source: ``UnifiedBattery.ExternalPowerStatus``

        :raise ``ValueError``: If the charging type is not supported by the DUT
        :raise ``AssertionError``: If the charging_type is not known
        """
        self.post_requisite_rechargeable = True
        self.power_supply_emulator.recharge(enable=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to CRITICAL level '
                                         'and a state_of_charge of 10%')
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.reset(hardware_reset=True, starting_voltage=battery_critical, cleanup_battery_event=True)

        if charging_type == UnifiedBattery.ChargingStatus.CHARGING and \
                source == UnifiedBattery.ExternalPowerStatus.WIRED:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enter charging mode (i.e. connect USB cable)')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
            if self.f.PRODUCT.F_IsGaming:
                ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)
            # end if
        elif charging_type == UnifiedBattery.ChargingStatus.CHARGING and \
                source == UnifiedBattery.ExternalPowerStatus.WIRELESS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enter wireless charging mode (i.e. emulate PowerPlay current supply)')
            # ----------------------------------------------------------------------------------------------------------
            # TODO
        elif charging_type == UnifiedBattery.ChargingStatus.CHARGING_AT_SLOW_RATE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate an ineffective charging system (i.e. low current supply)')
            # ----------------------------------------------------------------------------------------------------------
            # TODO
        else:
            assert False, f"charging_type = {charging_type} not recognised"
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f'Test Loop over state_of_charge value from {critical_state_of_charge}% to 80% by step of '
                  f'{self.config.F_StateOfChargeStep}%')
        battery_critical_charge = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self,
                                                                                         critical_state_of_charge,
                                                                                         discharge=False)
        battery_80p_charge = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, 80, discharge=False)
        previous_battery_status_event = None
        # --------------------------------------------------------------------------------------------------------------
        for voltage in range(int(battery_critical_charge*UnifiedBatteryTestUtils.V_UNIT_CONVERT),
                             int(battery_80p_charge*UnifiedBatteryTestUtils.V_UNIT_CONVERT), 10):
            battery_value = round(voltage / UnifiedBatteryTestUtils.V_UNIT_CONVERT, 3)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery value to {battery_value}%')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for battery_status_event response')
            # ----------------------------------------------------------------------------------------------------------
            battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                                                self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            self.check_ble_notifications(battery_status_event)
            self.check_ble_read(get_status_response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are synchronized on both responses')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self,
                                                   first_event_response=battery_status_event,
                                                   second_event_response=get_status_response,
                                                   previous_event_response=previous_battery_status_event)

            external_power_status = UnifiedBattery.ExternalPowerStatus.NO_POWER
            if charging_type == UnifiedBattery.ChargingStatus.CHARGING and \
                    source == UnifiedBattery.ExternalPowerStatus.WIRED:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check charging_status = "charging"')
                external_power_status = UnifiedBattery.ExternalPowerStatus.WIRED
                # ------------------------------------------------------------------------------------------------------
            elif charging_type == UnifiedBattery.ChargingStatus.CHARGING and \
                    source == UnifiedBattery.ExternalPowerStatus.WIRELESS:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check charging_status = "wireless charging"')
                external_power_status = UnifiedBattery.ExternalPowerStatus.WIRELESS
                # ------------------------------------------------------------------------------------------------------
            elif charging_type == UnifiedBattery.ChargingStatus.CHARGING_AT_SLOW_RATE:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check charging_status = "charging at slow rate"')
                # ------------------------------------------------------------------------------------------------------
            else:
                raise ValueError(f"Unsupported charging type {charging_type}")
            # end if
            expected_soc = to_int(get_status_response.state_of_charge)
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, expected_soc)
            checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge, expected_soc),
                "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
                "charging_status": (checker.check_charging_status, charging_type),
                "external_power_status": (checker.check_external_power_status, external_power_status)
            })
            UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                test_case=self, message=get_status_response,
                expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(charging=charging_type)
        # end for

        self.power_supply_emulator.recharge(enable=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_charging_mechanism

    def generic_end_of_charge_mechanism(self):
        """
        Validate device end of charge detection and notification.
        Check LED indicators.
        """
        self.post_requisite_rechargeable = True
        self.power_supply_emulator.recharge(enable=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to GOOD level and '
                                         'a state_of_charge of 90%')
        # --------------------------------------------------------------------------------------------------------------
        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, 90, discharge=True)
        self.reset(hardware_reset=True, starting_voltage=battery_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode (i.e. connect USB cable)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        if self.f.PRODUCT.F_IsGaming:
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check charging_status = "charging"')
        # --------------------------------------------------------------------------------------------------------------
        expected_soc = to_int(get_status_response.state_of_charge)
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
            "external_power_status": (checker.check_external_power_status,
                                      UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.check_ble_notifications(get_status_response)
        self.check_ble_read(get_status_response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines specification')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from 90% to 100% by step of '
                  f'{self.config.F_StateOfChargeStep}%')
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(90, 101, self.config.F_StateOfChargeStep):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self,
                                                                                   state_of_charge,
                                                                                   discharge=False)
            # Ensure the DUT can reach completed charging voltage
            if state_of_charge == 100:
                battery_value = self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage + 0.05
            # end if
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for battery_status_event response')
            # ----------------------------------------------------------------------------------------------------------
            battery_status_event, _ = UnifiedBatteryTestUtils.wait_soc_computation(
                self, timeout_for_core_dut=(self.BATTERY_MEASURE_END_OF_CHARGE_WINDOW *
                                            self.config.F_StateOfChargeStep))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are synchronized on both responses')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self, first_event_response=battery_status_event,
                                                   second_event_response=get_status_response)

            self.check_ble_notifications(battery_status_event)
            self.check_ble_read(get_status_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.recharge(enable=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check charging_status = "charge complete"')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, 100),
            "battery_level_full": (checker.check_full_battery_level, 1),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGE_COMPLETE),
            "external_power_status": (checker.check_external_power_status,
                                      UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines '
                                  'specification for end of charge')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGE_COMPLETE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Exit charging mode (i.e. unplug the USB cable)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the Battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=.2)
    # end def generic_end_of_charge_mechanism

    def generic_charging_mechanism_oob(self):
        """
        Validate charging mechanism with device in OOB state. Keep power slider switch ON and call to get_status
        with level from lowest to highest.
        Check LED indicators.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1805)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=OobState.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to CRITICAL level '
                                         'and a state_of_charge of 10%')
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.reset(hardware_reset=True, starting_voltage=battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Dump current NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_nvs_parser = self.get_dut_nvs_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)

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
            LogHelper.log_step(self, 'Wait for battery_status_event response')
            # ----------------------------------------------------------------------------------------------------------
            battery_status_event, _ = UnifiedBatteryTestUtils.wait_soc_computation(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are synchronized on both responses')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self, first_event_response=battery_status_event,
                                                   second_event_response=get_status_response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check charging_status is "charging"')
            # ----------------------------------------------------------------------------------------------------------
            expected_soc = to_int(get_status_response.state_of_charge)
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
                "external_power_status": (checker.check_external_power_status,
                                          UnifiedBattery.ExternalPowerStatus.WIRED)
            })
            UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                test_case=self, message=get_status_response,
                expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED '
                                      'Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGING)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_charging_mechanism_oob

    def generic_charging_mechanism_deep_sleep_oob(self):
        """
        Validate charging mechanism with device in OOB state and returning from deep sleep. Keep power slider switch
        ON and call to get_status with level from lowest to highest.
        Check LED indicators.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1805)')
        # --------------------------------------------------------------------------------------------------------------
        feature_1805_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=OobState.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to CRITICAL level and a '
                                         'state_of_charge of 10%')
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.reset(hardware_reset=True, starting_voltage=battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Dump current NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_nvs_parser = self.get_dut_nvs_parser()

        # Get the 0x1805 feature main class
        feature_1805 = OobStateFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.OOB_STATE))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        set_oob_state = feature_1805.set_oob_state_cls(device_index=self.deviceIndex, feature_index=feature_1805_index)
        ChannelUtils.send(
            test_case=self,
            report=set_oob_state,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=feature_1805.set_oob_state_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over state_of_charge value from 20% to 90% by step of10%')
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(20, 91, 10):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for deep sleep')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge,
                                                                                   discharge=False)
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enter charging mode (i.e. connect USB cable) to wake up the device')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
            if self.f.PRODUCT.F_IsGaming:
                ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response and check all battery '
                                      'properties are synchronized on both responses')
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_status response ; check charging_status = '
                                      f'"charging" and state_of_charge matches {state_of_charge}%')
            # ----------------------------------------------------------------------------------------------------------
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, state_of_charge)
            checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge, state_of_charge),
                "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
                "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
                "external_power_status": (checker.check_external_power_status,
                                          UnifiedBattery.ExternalPowerStatus.WIRED)
            })
            UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                test_case=self, message=get_status_response,
                expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED '
                                      'Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(charging=UnifiedBattery.ChargingStatus.CHARGING)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Exit charging mode (i.e. disconnect USB cable)')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_charging_mechanism_deep_sleep_oob

    def generic_battery_insertion_and_removal(self):
        """
        Validate Battery insertion and removal use cases
         - at a good and low battery level
         - when power slider is off
        Check LED indicator.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the device using the power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [FULL..CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(len(self.config.F_SupportedLevels)):
            if int(self.config.F_SupportedLevels[i]) == -1:
                continue
            # end if
            state_of_charge = int(self.config.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn on the device using the power supply service with '
                                     f'voltage to {battery_value}V')
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
            UnifiedBatteryTestUtils.compare_status(self, first_event_response=battery_status_event,
                                                   second_event_response=get_status_response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED Guidelines specification')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(battery_value=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn off the device using the power switch and the power supply services')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(0)
            # TODO use PowerSwitch

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn on the device using the power supply service with '
                                     f'voltage to {battery_value}V')
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Battery LED indicators comply with the LED '
                                      'Guidelines specification at reconnection')
            # ----------------------------------------------------------------------------------------------------------
            self.check_led_behaviour(battery_value=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn off the device using the power supply')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Turn on the device using the power switch')
            # ----------------------------------------------------------------------------------------------------------
            # TODO use PowerSwitch
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all LEDs are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=.1)
    # end def generic_battery_insertion_and_removal

    def check_ble_notifications(self, battery_status_event):
        """
        Get the latest notification from the BLE bas service queue and ensure
        they match with the latest battery status event

        :param battery_status_event: Battery Status Event coming from HIDPP pipe
        :type battery_status_event: ``BatteryStatusEventV0ToV3``

        :raise ``AssertionError``: if the battery level notification or the battery level status notification
                                   are missing
        """
        if self.check_ble_bas_service:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get last received BLE BAS notification")
            # ----------------------------------------------------------------------------------------------------------
            ble_level = None
            ble_status = None

            while True:
                try:
                    ble_level = self.bas_level_notification.get(timeout=1)
                except queue.Empty:
                    break
                # end try
            # end while
            while True:
                try:
                    ble_status = self.bas_status_notification.get(timeout=0.5)
                except queue.Empty:
                    break
                # end try
            # end while

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the values notified on the BAS"
                                      " notification correspond to the battery_status_event status")
            # ----------------------------------------------------------------------------------------------------------
            self.assertNotNone(ble_level, "Battery Level notification not received")
            self.assertNotNone(ble_status, "Battery Level Status notification not received")
            UnifiedBatteryTestUtils.check_bas_alignment(test_case=self,
                                                        status_1004=battery_status_event,
                                                        ble_bas_status_message=ble_status,
                                                        ble_bas_level_message=ble_level)
        # end if
    # end def check_ble_notifications

    def check_ble_read(self, get_status_response):
        """
        Read the values from the BLE bas service queue and ensure they match with the latest status response

        :param get_status_response: Get Status response  coming from HIDPP pipe
        :type get_status_response: ``GetStatusV0ToV5``
        """
        if self.check_ble_bas_service:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Read BLE BAS characteristics ")
            # ----------------------------------------------------------------------------------------------------------
            ble_level = BleProtocolTestUtils.read_characteristics(
                test_case=self,
                ble_context_device=self.current_channel.get_ble_context_device(),
                service_uuid=BleUuid(BleUuidStandardService.BATTERY_SERVICE),
                characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL))[0]
            ble_status = BleProtocolTestUtils.read_characteristics(
                test_case=self,
                ble_context_device=self.current_channel.get_ble_context_device(),
                service_uuid=BleUuid(BleUuidStandardService.BATTERY_SERVICE),
                characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL_STATUS))[0]

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the values notified on the BAS"
                                      " notification correspond to the battery_status_event status")
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.check_bas_alignment(test_case=self,
                                                        status_1004=get_status_response,
                                                        ble_bas_status_message=ble_status,
                                                        ble_bas_level_message=ble_level)
        # end if
    # end def check_ble_read

    # Next comment is for Pycharm to remove unused warning
    # noinspection PyUnusedLocal
    def check_led_behaviour(self, state_of_charge=-1, battery_value=-1.0, critical=False,
                            charging=UnifiedBattery.ChargingStatus.DISCHARGING, device_state=DeviceState.RUN):
        """
        Placeholder to any LED state verification

        :param state_of_charge: battery percentage - OPTIONAL
        :type state_of_charge: ``float``
        :param battery_value: battery value in Volt - OPTIONAL
        :type battery_value: ``float``
        :param critical: Flag indicating if the battery has reached its critical level - OPTIONAL
        :type critical: ``bool``
        :param charging: Charging status reported by the ``UnifiedBattery`` feature - OPTIONAL
        :type charging: ``UnifiedBattery.ChargingStatus``
        :param device_state: Device power mode state (i.e. ``DeviceState``) - OPTIONAL
        :type device_state: ``int``

        """
        self.logTrace(msg="No LED, check skipped")
    # end def check_led_behaviour

    # Next comment is for Pycharm to remove unused warning
    # noinspection PyUnusedLocal
    def wait_led_on_off(self, wait_on, timeout=1.0):
        """
        Placeholder to LED on or off transition verification

        :param wait_on: Flag indicating if we shall expect a switch on or off transition
        :type wait_on: ``bool``
        :param timeout: maximum timing to wait to verify the transition - OPTIONAL
        :type timeout: ``float``
        """
        self.logTrace(msg="No LED, check skipped")
    # end def wait_led_on_off
# end class UnifiedBatteryGenericTest


class UnifiedBatteryMultiReceiverGenericTest(UnifiedBatteryGenericTest):
    """
    Common Unified Battery Multi Receivers Test Class
    """

    def setUp(self):
        """
        Handle test prerequisites.

        :raise ``AssertionError``: If the setup does not detect enough receivers to perform multi pairing
        """
        super().setUp()

        if self.f.SHARED.PAIRING.F_BLEDevicePairing:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Backup initial NVS")
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.backup_nvs(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Pair device to a second dongle')
            # ----------------------------------------------------------------------------------------------------------
            # Cleanup all pairing slots except the first one
            CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)

            # Initialize the authentication method parameter
            DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

            self.ble_pro_receiver_port_indexes = ReceiverTestUtils.get_receiver_port_indexes(
                self,
                ReceiverTestUtils.USB_PID_MEZZY_BLE_PRO,
                skip=[ChannelUtils.get_port_index(test_case=self)])

            assert len(self.ble_pro_receiver_port_indexes) > 0, \
                "Cannot perform multi receiver tests if not enough receivers"
            DevicePairingTestUtils.pair_device_slot_to_other_receiver(
                    test_case=self,
                    device_slot=1,
                    other_receiver_port_index=self.ble_pro_receiver_port_indexes[0],
                    hid_dispatcher_to_dump=self.current_channel.hid_dispatcher)

            # Reconnect with the first receiver
            ReceiverTestUtils.switch_to_receiver(
                self, receiver_port_index=ChannelUtils.get_port_index(test_case=self, channel=self.backup_dut_channel))

            # Change host on Device
            DevicePairingTestUtils.change_host_by_link_state(
                self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.

        :raise ``AssertionError``: If the device does not reconnect to host 0
        """
        with self.manage_post_requisite():
            if self.f.SHARED.PAIRING.F_BLEDevicePairing:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.status != TYPE_SUCCESS:
                # Switch communication channel to receiver on port 0
                status = self.channel_switch(
                    device_uid=ChannelIdentifier(port_index=self.host_number_to_port_index(0), device_index=1))
                self.assertTrue(status, msg='The device do not connect on host 0')
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class UnifiedBatteryMultiReceiverGenericTest


class UnifiedBatteryGamingTest(UnifiedBatteryGenericTest):
    """
    Gaming Unified Battery Test Class
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.backup_dut_channel.protocol in LogitechProtocol.unifying_protocols():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(
                    self, f"Power off USB Port {self.device.CHARGING_PORT_NUMBER} and switch to receiver channel")
                # ------------------------------------------------------------------------------------------------------
                # Leave from USB channel if the DUT is a gaming device, otherwise do nothing
                ProtocolManagerUtils.exit_usb_channel(self)
            # end if
        # end with

        # End with super tearDown()
        super().tearDown()
    # end def tearDown
# end class UnifiedBatteryGamingTest

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
