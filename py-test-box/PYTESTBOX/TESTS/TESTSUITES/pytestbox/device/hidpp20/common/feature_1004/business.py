#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1004.business
:brief: HID++ 2.0 Unified Battery business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from time import time
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pyusb.libusbdriver import ChannelIdentifier
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryGamingTest
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryGenericTest


# ----------------------------------------------------------------------------------------------------------------------
# implementation
class UnifiedBatteryBusinessTestCase(UnifiedBatteryGenericTest):
    """
    Validates Unified Battery business TestCases
    """
    @features('Feature1004')
    @level('Business', 'SmokeTests')
    @services('PowerSupply')
    def test_battery_discharging(self):
        """
        Battery Management Business Case: check the transition between the full to the good level.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

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
        LogHelper.log_step(self, 'Set battery level to a value lower than the current one and still in the valid range')
        # --------------------------------------------------------------------------------------------------------------
        good_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'good')
        # The SoC range of good level is from Good_SoC - 1 to Low_Soc + 1 for gaming devices. Select battery value
        # by Good_SoC - SoCStep for gaming devices to ensure the battery level is in the good range.
        good_state_of_charge = good_state_of_charge if not self.f.PRODUCT.F_IsGaming \
            else good_state_of_charge - self.config.F_StateOfChargeStep
        battery_good = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, good_state_of_charge)
        self.power_supply_emulator.set_voltage(battery_good)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for a minute to be sure a new level measurement occurs.')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.wait_soc_computation(self, check_battery_event_on_core_dut=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)
        get_status_response.state_of_charge = UnifiedBatteryTestUtils.adapt_soc(
            test_case=self, input_soc=get_status_response.state_of_charge, expected_soc=good_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check charging_status = \'discharging\'')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, good_state_of_charge),
            "battery_level_good": (checker.check_good_battery_level, 1)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # Empty event_message_queue from BatteryStatusEvent notifications sent by the device
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
            class_type=self.feature_1004.battery_status_event_cls)

        self.testCaseChecked("BUS_1004_0001")
    # end def test_battery_discharging

    @features('Feature1004')
    @level('Time-consuming')
    @services('PowerSupply')
    def test_get_status_for_all_levels(self):
        """
        Validate get_status.battery_level supplying voltage from highest to lowest possible values.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

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
            LogHelper.log_step(self, 'Wait for 1 minute')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.wait_soc_computation(self, check_battery_event_on_core_dut=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            expected_soc = state_of_charge
            battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(
                self, soc=to_int(get_status_response.state_of_charge))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, 'Wait for get_status response and check battery_level matches the input = '
                      f'{UnifiedBatteryTestUtils.get_battery_level_status(self, soc=expected_soc)}')
            # ----------------------------------------------------------------------------------------------------------
            checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "state_of_charge": (checker.check_state_of_charge_in_range, expected_soc),
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

        self.testCaseChecked("BUS_1004_0002")
    # end def test_get_status_for_all_levels

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_without_batt_without_wp(self):
        """
        A NRWP device without a battery and without a wireless power supply will be inoperable
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the battery power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Check there is a hidpp1.0 device connection notification with link status = 1(not established)')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(obtained=to_int(device_info.device_info_link_status),
                         expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         msg="The connection status differs from the one expected")

        self.testCaseChecked("BUS_1004_0011")
    # end def test_nrwp_without_batt_without_wp

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_without_batt_without_wp_after_1_min_wp(self):
        """
        A NRWP device without a battery and without a wireless power supply will be operable no later than 1 minute
        after wireless power is supplied
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the battery power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Check there is a hidpp1.0 device connection notification with link status = 1(not established)')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(obtained=to_int(device_info.device_info_link_status),
                         expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         msg="The connection status differs from the one expected")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=None)
        start_timestamp = time()
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check there is a hidpp1.0 device connection notification with link status=0'
                                  '(established) no later than 1 minute')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.get_only(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                              queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
                              timeout=UnifiedBatteryTestUtils.MINUTE)
        end_timestamp = time()
        elapsed_timestamp = end_timestamp - start_timestamp

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_data(self, f'Device is connected after wireless power supply for {elapsed_timestamp:.6f} sec')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.BATTERY_STATUS_UPDATE_TIME)
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is removed by 0x1004.get_status response with '
                                  'removable_battery_status=1')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.REMOVED),
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("BUS_1004_0012")
    # end def test_nrwp_without_batt_without_wp_after_1_min_wp

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_with_batt_without_wp(self):
        """
        A NRWP device with a battery and without a wireless power supply will be operable until the battery becomes
        fully discharged
        """
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        batt_critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with starting voltage to critical level voltage')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=batt_critical_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Empty receiver connection event queue')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f'Test Loop over state_of_charge value from {critical_state_of_charge}% to 0% '
                  f'by step of {self.config.F_StateOfChargeStep}')
        # --------------------------------------------------------------------------------------------------------------
        for soc in range(critical_state_of_charge, -self.config.F_StateOfChargeStep, -self.config.F_StateOfChargeStep):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery state of charge to {soc}%')
            # ----------------------------------------------------------------------------------------------------------
            batt_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge=soc)
            self.power_supply_emulator.set_voltage(batt_voltage)
            if soc == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self,
                    'Check there is a hidpp1.0 device connection notification with link status = 1(not established)')
                # ------------------------------------------------------------------------------------------------------
                device_connection = ChannelUtils.get_only(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
                    timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)

                device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                self.assertEqual(obtained=to_int(device_info.device_info_link_status),
                                 expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                                 msg="The connection status differs from the one expected")
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send 0x1004.get_status request')
                # ------------------------------------------------------------------------------------------------------
                get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self,
                                    'Check removable battery status is not removed by 0x1004.get_status response with '
                                    'removable_battery_status=0')
                # ------------------------------------------------------------------------------------------------------
                checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "battery_level_critical": (checker.check_critical_battery_level, 1),
                    "state_of_charge": (checker.check_state_of_charge, soc),
                    "removable_battery_status": (checker.check_removable_battery_status,
                                                 UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED)})
                UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                    test_case=self, message=get_status_response,
                    expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)
            # end if
        # end for

        self.testCaseChecked("BUS_1004_0013")
    # end def test_nrwp_with_batt_without_wp

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_with_batt_without_wp_after_wp(self):
        """
        A NRWP device with a not fully discharged battery and without a wireless power supply will continue to operate
        without interruption and report battery information to the host just as for other types of device after the
        device is powered up by wireless power supply
        """
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        batt_critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with starting voltage to critical level voltage')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=batt_critical_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Empty receiver connection event queue')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery_level is critical and removable battery status is not removed by '
                                  '0x1004.get_status response')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, critical_state_of_charge),
            "battery_level_critical": (checker.check_critical_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED)})
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=None)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there aren't any device connection/disconnection notifications")
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
            timeout=UnifiedBatteryTestUtils.MINUTE, allow_no_message=True)
        self.assertNone(device_connection, f"Got a device connection notification\n{device_connection}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery_level is still critical and removable battery status is not removed by'
                                  ' 0x1004.get_status response')
        # --------------------------------------------------------------------------------------------------------------
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, critical_state_of_charge),
            "battery_level_critical": (checker.check_critical_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED)})

        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("BUS_1004_0014")
    # end def test_nrwp_with_batt_without_wp_after_wp

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_without_batt_with_wp(self):
        """
        A NRWP device without a battery and with a wireless power supply will be operable
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=UnifiedBatteryTestUtils.MINUTE)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the battery power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the last battery_status_event')
        # ----------------------------------------------------------------------------------------------------------
        battery_status_event = UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is removed by 0x1004.get_status response with '
                                  'removable_battery_status=1')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.REMOVED)})
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check all battery properties are synchronized on the response of 0x1004.get_status '
                                  'and battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.compare_status(self, first_event_response=battery_status_event[0],
                                               second_event_response=get_status_response)

        self.testCaseChecked("BUS_1004_0015")
    # end def test_nrwp_without_batt_with_wp

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Time-consuming')
    @services('HardwareReset')
    def test_nrwp_without_batt_with_wp_after_turn_off_wp(self):
        """
        A NRWP device without a battery and with a wireless power supply will continue to operate for a short period of
        time so long as the device is powered up by wireless power supply at least 2 minutes, even if the device is no
        longer powered by the wireless power supply
        """
        device_connection = None
        elapsed_timestamp = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=None)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait 2 minutes')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.MINUTE * 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the battery power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_off_crush_pad_charging_emulator()
        start_timestamp = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.BATTERY_STATUS_UPDATE_TIME)
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is removed by 0x1004.get_status response with '
                                  'removable_battery_status=1')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.REMOVED)})
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Check there is a hidpp1.0 device connection notification with link status=1(not established)')
        # --------------------------------------------------------------------------------------------------------------
        while time() - start_timestamp < UnifiedBatteryTestUtils.MINUTE * 5:
            # Click the left button to speed up the power consumption
            self.button_stimuli_emulator.user_action()

            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
                timeout=0.2, allow_no_message=True)

            if device_connection:
                end_timestamp = time()
                elapsed_timestamp = end_timestamp - start_timestamp
                break
            # end if
        # end while

        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(obtained=to_int(device_info.device_info_link_status),
                         expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         msg="The connection status differs from the one expected")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_data(self, f'Device still operates {elapsed_timestamp:.2f} sec after power off the battery power '
                                 'supply and power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1004_0016")
    # end def test_nrwp_without_batt_with_wp_after_turn_off_wp

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_with_batt_with_wp_after_batt_fully_discharge(self):
        """
        A NRWP device with a battery and with a wireless power supply will be operable even if the battery is discharged
        """
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        batt_critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        voltage_step_mv = 50

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to good level voltage')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=batt_critical_voltage + voltage_step_mv / 1000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Empty receiver connection event queue')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=UnifiedBatteryTestUtils.MINUTE)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over battery_voltage from critical level battery voltage to <= cutoff voltage '
                  f'by step of {voltage_step_mv} mV')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        batt_critical_voltage_mv = round(batt_critical_voltage * UnifiedBatteryTestUtils.V_UNIT_CONVERT)
        batt_cutoff_voltage_mv = round(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage *
                                       UnifiedBatteryTestUtils.V_UNIT_CONVERT)

        for batt_voltage in range(batt_critical_voltage_mv,
                                  batt_cutoff_voltage_mv - voltage_step_mv,
                                  -voltage_step_mv):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery power supply voltage to {batt_voltage} mV')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(round(batt_voltage / UnifiedBatteryTestUtils.V_UNIT_CONVERT,
                                                         PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the last battery_status_event')
            # ----------------------------------------------------------------------------------------------------------
            battery_status_event = UnifiedBatteryTestUtils.wait_soc_computation(self)
            self.assertNotNone(battery_status_event, msg="Should receive a battery status event at least")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send 0x1004.get_status request')
            # ----------------------------------------------------------------------------------------------------------
            get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

            if batt_voltage <= round(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage *
                                     UnifiedBatteryTestUtils.V_UNIT_CONVERT):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check removable battery status is removed by 0x1004.get_status response '
                                          'with removable_battery_status=1')
                # ------------------------------------------------------------------------------------------------------
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "battery_level_full": (checker.check_full_battery_level, 1),
                    "removable_battery_status": (checker.check_removable_battery_status,
                                                 UnifiedBattery.RemovableBatteryStatus.REMOVED)})
                UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                    test_case=self, message=get_status_response,
                    expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)
                break
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check removable battery status is not removed by 0x1004.get_status response '
                                          'with removable_battery_status=0')
                # ------------------------------------------------------------------------------------------------------
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "state_of_charge": (checker.check_state_of_charge, battery_status_event[0].state_of_charge),
                    "battery_level_critical": (checker.check_critical_battery_level, 1),
                    "removable_battery_status": (checker.check_removable_battery_status,
                                                 UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED)})
                UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
                    test_case=self, message=get_status_response,
                    expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'check all battery properties are synchronized on the response of '
                                      '0x1004.get_status and battery_status_event')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.compare_status(self, first_event_response=battery_status_event[0],
                                                   second_event_response=get_status_response)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there aren't any device connection/disconnection notifications")
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
            allow_no_message=True)
        self.assertNone(device_connection, f"Got a device connection notification\n{device_connection}")

        self.testCaseChecked("BUS_1004_0017")
    # end def test_nrwp_with_batt_with_wp_after_batt_fully_discharge

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_with_batt_with_wp_without_discharge_from_batt(self):
        """
        A NRWP device with a battery and with a wireless power supply will be operable without continuing to discharge
        the battery
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get battery_current_with_battery_supply from INA226 when the device is powered up by '
                                 'battery power supply')
        # --------------------------------------------------------------------------------------------------------------
        batt_current_with_batt_supply = self.power_supply_emulator.get_current()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'battery_current_with_battery_supply: {batt_current_with_batt_supply:.3f} mA')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=UnifiedBatteryTestUtils.MINUTE)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is not removed by 0x1004.get_status response with '
                                  'removable_battery_status=0')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED),
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get battery_current_with_playpad_supply from INA226 when the device is powered up by '
                                 'power play pad')
        # --------------------------------------------------------------------------------------------------------------
        batt_current_with_playpad_supply = self.power_supply_emulator.get_current()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'battery_current_with_playpad_supply: {batt_current_with_playpad_supply:.3f} mA')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery_current_with_playpad_supply is less than '
                                  'battery_current_with_battery_supply and close to 0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=(batt_current_with_playpad_supply < batt_current_with_batt_supply))
        self.assertTrue(expr=(round(batt_current_with_playpad_supply) == 0))

        self.testCaseChecked("BUS_1004_0018")
    # end def test_nrwp_with_batt_with_wp_without_discharge_from_batt

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_with_batt_with_wp_after_turn_off_wp(self):
        """
        A NRWP device with a battery and with a wireless power supply will be operable without interruption after the
        wireless power supply is disabled as long as the battery it not fully discharged
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=UnifiedBatteryTestUtils.MINUTE)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is not removed by 0x1004.get_status response with '
                                  'removable_battery_status=0')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED)})
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_off_crush_pad_charging_emulator()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there aren't any device connection/disconnection notifications")
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
            allow_no_message=True)
        self.assertNone(device_connection, f"Got a device connection notification\n{device_connection}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.BATTERY_STATUS_UPDATE_TIME)
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is not removed by 0x1004.get_status response with '
                                  'removable_battery_status=0')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED)})
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("BUS_1004_0019")
    # end def test_nrwp_with_batt_with_wp_after_turn_off_wp

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_with_batt_without_wp_critical_batt_level(self):
        """
        A NRWP device is operating with a battery, the device should report battery level event when battery level is
        critical
        """
        low_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'low')
        battery_low_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, low_state_of_charge)
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        batt_critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to low level voltage')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_low_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery power supply voltage to critical level voltage')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(batt_critical_voltage)
        battery_status_event, _ = UnifiedBatteryTestUtils.wait_soc_computation(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is not removed by 0x1004.get_status response with '
                                  'removable_battery_status=0')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, critical_state_of_charge),
            "battery_level_critical": (checker.check_critical_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.NOT_REMOVED)})
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("BUS_1004_0020")
    # end def test_nrwp_with_batt_without_wp_critical_batt_level

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    def test_nrwp_without_batt_with_wp_batt_status(self):
        """
        A NRWP device is operating without a battery, the device removable battery status is removed, SOC is always
        100% and battery level is "Full"
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=UnifiedBatteryTestUtils.MINUTE)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the battery power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.BATTERY_STATUS_UPDATE_TIME)
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is removed by 0x1004.get_status response with '
                                  'removable_battery_status=1')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.REMOVED)})
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("BUS_1004_0021")
    # end def test_nrwp_without_batt_with_wp_batt_status

    @features('Feature1004v5+')
    @features('Feature1004RemovableBattery')
    @features('WirelessCharging')
    @level('Business')
    @services('HardwareReset')
    @services('LedIndicator')
    @skip("In development")
    def test_nrwp_without_batt_with_wp_batt_led(self):
        """
        A NRWP device is operating without a battery, the battery LED of the device will be OFF
        """
        sleep(BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS / 1000)
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(
            self, led_identifiers=LED_ID.DEVICE_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the power play pad charging emulator')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_on_crush_pad_charging_emulator(delay=UnifiedBatteryTestUtils.MINUTE)
        self.post_requisite_enable_all_usb_ports = True
        self.post_requisite_discharge_super_cap = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the battery power supply')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.BATTERY_STATUS_UPDATE_TIME)
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check removable battery status is removed by 0x1004.get_status response with '
                                  'removable_battery_status=1')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "battery_level_full": (checker.check_full_battery_level, 1),
            "removable_battery_status": (checker.check_removable_battery_status,
                                         UnifiedBattery.RemovableBatteryStatus.REMOVED),
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery LED is off')
        # --------------------------------------------------------------------------------------------------------------
        sleep(BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.DEVICE_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.DEVICE_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS)

        self.testCaseChecked("BUS_1004_0022")
    # end def test_nrwp_without_batt_with_wp_batt_led

    @features('Feature1004v4+')
    @features('Feature1004FastCharging')
    @level('Business')
    @services('HardwareReset')
    @skip("In development")
    def test_fast_charging_batt_status(self):
        """
        A NRWP device is operating without a battery, the battery LED of the device will be OFF
        """
        good_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'good')
        battery_good_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, good_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to good level voltage')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_good_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the charging port with normal charging mode')
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Enable USB charging cable with normal charging mode (5v, 500mA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is in normal charging mode by 0x1004.get_status response with '
                                  'fast_charging=0')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, good_state_of_charge),
            "charging_status": (checker.check_full_battery_level, UnifiedBattery.ChargingStatus.CHARGING),
            "fast_charging": (checker.check_fast_charging_status, UnifiedBattery.FastChargingStatus.NO_FAST_CHARGE)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the charging port with fast charging mode')
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Enable USB charging cable with fast charging mode (>500mA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is in fast charging mode by 0x1004.get_status response with '
                                  'fast_charging=1')
        # --------------------------------------------------------------------------------------------------------------
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, good_state_of_charge),
            "charging_status": (checker.check_full_battery_level, UnifiedBattery.ChargingStatus.CHARGING),
            "fast_charging": (checker.check_fast_charging_status, UnifiedBattery.FastChargingStatus.FAST_CHARGE),
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("BUS_1004_0023")
    # end def test_fast_charging_batt_status

    @features('Feature1004v4+')
    @features('Feature1004FastCharging')
    @level('Business')
    @services('HardwareReset')
    @skip("In development")
    def test_fast_charging_power_consumption(self):
        """
        A fast charging mode should consume more watts than the normal charging mode to complete the charging process
        faster
        """
        good_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'good')
        battery_good_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, good_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to good level voltage')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_good_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the charging port with normal charging mode')
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Enable USB charging cable with normal charging mode (5v, 500mA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is in normal charging mode by 0x1004.get_status response with '
                                  'fast_charging=0')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, good_state_of_charge),
            "charging_status": (checker.check_full_battery_level, UnifiedBattery.ChargingStatus.CHARGING),
            "fast_charging": (checker.check_fast_charging_status, UnifiedBattery.FastChargingStatus.NO_FAST_CHARGE)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get charging voltage and current during normal charging mode')
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Get charging voltage and current during normal charging mode

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the charging port with fast charging mode')
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Enable USB charging cable with fast charging mode (>500mA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1004.get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is in fast charging mode by 0x1004.get_status response with '
                                  'fast_charging=1')
        # --------------------------------------------------------------------------------------------------------------
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, good_state_of_charge),
            "charging_status": (checker.check_full_battery_level, UnifiedBattery.ChargingStatus.CHARGING),
            "fast_charging": (checker.check_fast_charging_status, UnifiedBattery.FastChargingStatus.FAST_CHARGE),
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get charging voltage and current during fast charging mode')
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Get charging voltage and current during fast charging mode

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check charging watts in fast charging mode is greater than normal charging mode')
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check charging watts in fast charging mode is greater than normal charging mode

        self.testCaseChecked("BUS_1004_0024")
    # end def test_fast_charging_power_consumption
# end class UnifiedBatteryBusinessTestCase


class UnifiedBatteryBusinessGamingTestCase(UnifiedBatteryGamingTest):
    """
    Validates Unified Battery business with Gaming devices TestCases
    """

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Business')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_battery_charging_on_gaming_device_wired(self):
        """
        Validate gaming device charging mechanism and battery status event report for each SoC from 0% to 99%.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        soc_step = self.config.F_StateOfChargeStep
        last_soc = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
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
        LogHelper.log_info(self, f'Test Loop over state_of_charge value from 0-100% by {soc_step}% SoC step')
        # --------------------------------------------------------------------------------------------------------------
        for soc in range(soc_step, 100 + soc_step, soc_step):
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, soc, discharge=False)
            # In order to prevent the set voltage from reaching the fully charged voltage, limit the maximum
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
            for each_percentage_soc in range(soc - soc_step + 1, soc + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Wait for battery_status_event')
                # ------------------------------------------------------------------------------------------------------
                if each_percentage_soc <= self.constant_v_threshold:
                    if each_percentage_soc == 1:
                        sleep(UnifiedBatteryTestUtils.TRANSITION_TIME_OF_ENTERING_CHARGING_MODE
                              + UnifiedBatteryTestUtils.CC_SAMPLING_TIME)
                    # end if
                    battery_status_event = \
                        UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                            self, continuously_receive=False)
                elif each_percentage_soc == 100:
                    break
                else:
                    battery_status_event, elapsed_time = \
                        UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_voltage_charging(
                            self, expected_soc=each_percentage_soc)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Check reporting time interval of battery_status_event is valid')
                    # --------------------------------------------------------------------------------------------------
                    UnifiedBatteryTestUtils.GamingDevicesHelper.check_battery_report_time_interval(
                        self, battery_status_event.state_of_charge, elapsed_time)
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check battery_status_event fields are valid')
                # ------------------------------------------------------------------------------------------------------
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
                self.assertEqual(obtained=to_int(battery_status_event.state_of_charge),
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

        self.testCaseChecked("BUS_1004_0003")
    # end def test_battery_charging_on_gaming_device_wired

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Business')
    @services('PowerSupply')
    @services('PowerSwitch')
    @services('Rechargeable')
    def test_soc_start_to_updating_after_current_soc_bigger_than_internal_soc(self):
        """
        Validate SoC starts to updating when the current SoC is bigger than the internal SoC.

        Note:
        The key steps to check the behavior:
        1) Plugged USB charging cable then
        2) power off/on DUT by power switch

        cf https://docs.google.com/document/d/1ArpYWbkJ2YVWhJLxjY016YT_C718-xCIhWZXoCNAPD0/edit#heading=h.n885m69fgyvk
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        set_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, state_of_charge=self.constant_v_threshold + 5, discharge=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Restart the device with input voltage {set_voltage} '
                                         f'(SoC: {self.constant_v_threshold} + 5%)')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=set_voltage,
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
        LogHelper.log_step(self, 'Send get_status request and wait response')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)
        expected_soc = self.constant_v_threshold + 5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check inputs fields')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, expected_soc)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, expected_soc),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery LED indicators')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=expected_soc)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power switch OFF->ON DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.reset()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event, elapsed_time = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_voltage_charging(
                self, expected_soc=expected_soc + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check reporting time interval of battery_status_event is valid')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GamingDevicesHelper.check_battery_report_time_interval(
            self, battery_status_event.state_of_charge, elapsed_time)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery_status_event fields are valid')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, expected_soc + 1)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, expected_soc + 1),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery LED indicators')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        self.testCaseChecked("BUS_1004_0004")
    # end def test_soc_start_to_updating_after_current_soc_bigger_than_internal_soc

    @features('Feature1004')
    @features('Feature1830')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Business')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_diode_effect_when_returning_from_deep_sleep(self):
        """
        Validate the current SoC is not greater than last SoC when the DUT is returning from deep-sleep mode.
        """
        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, self.constant_v_threshold)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Restart the device with input voltage to "{self.constant_v_threshold}" SoC')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=round(battery_value, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1),
                   cleanup_battery_event=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request and wait response')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response_1 = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check inputs fields')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3])
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response_1,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Let device enter deep-sleep mode by 0x1830.setPowerMode')
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform an user action to wake-up the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request and wait response')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response_2 = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check get_status response input fields in its valid range')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3])
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response_2,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check current SoC is not greater than last SoC')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLessEqual(to_int(get_status_response_2.state_of_charge),
                             to_int(get_status_response_1.state_of_charge),
                             'The current SoC is greater than last SoC when the DUT is returning from deep-sleep mode')

        self.testCaseChecked("BUS_1004_0005")
    # end def test_diode_effect_when_returning_from_deep_sleep

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('USBCharging')
    @level('Business')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_charging_report_time_interval(self):
        """
        Validate the timer starts from the corresponding 5 segment time interval, when plug the charging cable with a
        SoC between 50-99% or 40-99% ('Synergy' or 'High Power' battery)

        Note:
        The report rate depends on the battery source and SoC value.

        cf https://docs.google.com/document/d/1ArpYWbkJ2YVWhJLxjY016YT_C718-xCIhWZXoCNAPD0/edit#heading=h.n885m69fgyvk
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
        set_soc = 60
        set_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, state_of_charge=set_soc, discharge=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Restart the device with input voltage {set_voltage}')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=set_voltage,
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
        LogHelper.log_step(self, f'Set battery value to {self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage - 0.02}V')
        # --------------------------------------------------------------------------------------------------------------
        # In order to prevent the set voltage from reaching the fully charged voltage, limit the maximum
        # battery value to F_MaximumVoltage - 20mV
        self.power_supply_emulator.set_voltage(self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage - 0.02)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request and wait response')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event')
        # --------------------------------------------------------------------------------------------------------------
        sleep(UnifiedBatteryTestUtils.TRANSITION_TIME_OF_ENTERING_CHARGING_MODE
              + UnifiedBatteryTestUtils.CC_SAMPLING_TIME)
        battery_status_event, elapsed_time = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_voltage_charging(
                self, expected_soc=set_soc, is_first_report=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check reporting time interval of battery_status_event is valid')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GamingDevicesHelper.check_battery_report_time_interval(
            self, state_of_charge=battery_status_event.state_of_charge, elapsed_time=elapsed_time, is_first_report=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all battery properties are synchronized on both response and the SoC '
                                  'is in increasing order')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response.state_of_charge = to_int(get_status_response.state_of_charge) + 1
        UnifiedBatteryTestUtils.compare_status(self,
                                               first_event_response=get_status_response,
                                               second_event_response=battery_status_event)

        self.testCaseChecked("BUS_1004_0006")
    # end def test_charging_report_time_interval

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('WirelessCharging')
    @level('Business')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_battery_charging_on_gaming_device_wireless(self):
        """
        Validate gaming device charging mechanism and battery status event report for each SoC. (The FW stops charging
        once the voltage reach the full charge voltage of wireless charging 4.12V)
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
        soc_step = self.config.F_StateOfChargeStep
        last_soc = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
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
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self,
                                                           source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
            class_type=self.feature_1004.battery_status_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over state_of_charge value from 0-100% by {soc_step}% SoC step')
        # --------------------------------------------------------------------------------------------------------------
        for soc in range(soc_step, 100 + soc_step, soc_step):
            if last_soc == 100:
                break
            # end if
            battery_value = round(
                UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, soc, discharge=True) +
                UnifiedBatteryTestUtils.WIRELESS_CHARGING_VOLTAGE_OFFSET,
                PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1)
            i = 0
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over state_of_charge each percentage in SoC step value {soc_step}')
            # ----------------------------------------------------------------------------------------------------------
            for each_percentage_soc in range(soc - soc_step + 1, soc + 1):
                self.power_supply_emulator.set_voltage(round(battery_value + (i * 0.005), 3))
                i += 1
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Wait for battery_status_event')
                # ------------------------------------------------------------------------------------------------------
                if each_percentage_soc == 1:
                    sleep(UnifiedBatteryTestUtils.TRANSITION_TIME_OF_ENTERING_CHARGING_MODE
                          + UnifiedBatteryTestUtils.CC_SAMPLING_TIME)
                # end if
                battery_status_event = \
                    UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                        self, continuously_receive=False,
                        external_power_status=UnifiedBattery.ExternalPowerStatus.WIRELESS)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check battery_status_event fields are valid')
                # ------------------------------------------------------------------------------------------------------
                self.assertIsNotNone(
                    obj=battery_status_event,
                    msg=f"Miss {each_percentage_soc}% SoC report, battery_status_event should not be None.")
                if to_int(battery_status_event.state_of_charge) == 100:
                    if round(battery_value + (i * 0.005), 3) < UnifiedBatteryTestUtils.FULL_CHARGE_VOLTAGE_CP - 0.005:
                        self.assertFalse(expr=(round(battery_value + (i * 0.005), 3) <
                                               (UnifiedBatteryTestUtils.FULL_CHARGE_VOLTAGE_CP - 0.005)),
                                         msg="Unexpected charge completed before reach FULL_CHARGE_VOLTAGE_CP: "
                                             f"{UnifiedBatteryTestUtils.FULL_CHARGE_VOLTAGE_CP}")
                    # end if
                    each_percentage_soc = 100
                    battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, each_percentage_soc)
                    checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
                    check_map = checker.get_default_check_map(self)
                    check_map.update({
                        "state_of_charge": (checker.check_state_of_charge, each_percentage_soc),
                        "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
                        "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
                        "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
                        "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
                        "charging_status": (checker.check_charging_status,
                                            UnifiedBattery.ChargingStatus.CHARGE_COMPLETE),
                        "external_power_status": (checker.check_external_power_status,
                                                  UnifiedBattery.ExternalPowerStatus.WIRELESS)
                    })
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Check the received SoC values are in increasing order')
                    # --------------------------------------------------------------------------------------------------
                    self.assertEqual(obtained=to_int(battery_status_event.state_of_charge),
                                     expected=last_soc + 1,
                                     msg="The state_of_charge parameter is not in increasing order")

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
                                                  UnifiedBattery.ExternalPowerStatus.WIRELESS)
                    })
                # end if
                UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
                    test_case=self, message=battery_status_event,
                    expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)
                last_soc = each_percentage_soc

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the battery LED indicators when charging')
                # ------------------------------------------------------------------------------------------------------
                self.check_led_behaviour(state_of_charge=each_percentage_soc)

                if to_int(battery_status_event.state_of_charge) == 100:
                    break
                # end if
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
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self,
                                                          source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        self.testCaseChecked("BUS_1004_0007")
    # end def test_battery_charging_on_gaming_device_wireless

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('WirelessCharging')
    @level('Business')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_charging_state_change_wireless(self):
        """
        Validate the device switches to discharging mode when the device moves out from the valid charging zone of
        Crush Pad over the debouncing time

        Note: Turning off the power for the test pad of Crush Pad charging on the DUT can simulate the behavior that
        the dut moves out of the valid charging zone of Crush Pad
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, self.constant_v_threshold)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to "Constant V threshold" SoC')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=round(battery_value,
                                          PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1),
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self,
                                                           source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event response')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                test_case=self, continuously_receive=False,
                external_power_status=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the charging status is {UnifiedBattery.ChargingStatus.CHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self,
                                                                                self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status,
                                      UnifiedBattery.ExternalPowerStatus.WIRELESS)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check inputs fields')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRELESS)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators when charging')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=self.constant_v_threshold)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Exit charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self,
                                                          source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for 1 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event response')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                test_case=self, continuously_receive=False,
                external_power_status=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the charging status is {UnifiedBattery.ChargingStatus.DISCHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self,
                                                                                self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.DISCHARGING),
            "external_power_status": (checker.check_external_power_status,
                                      UnifiedBattery.ExternalPowerStatus.NO_POWER)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators are off')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_led_on_off(wait_on=False, timeout=0.1)

        self.testCaseChecked("BUS_1004_0008")
    # end def test_charging_state_change_wireless

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('WirelessCharging')
    @level('Business')
    @services('PowerSupply')
    @services('Rechargeable')
    @skip('The time (2 sec) of turning OFF USB port is longer than the debouncing time (0.5 sec)')
    def test_charging_state_not_change_wireless(self):
        """
        Validate the device switches to discharging mode when the device moves out and in from the valid charging zone
        of Crush Pad within the debouncing time
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, self.constant_v_threshold)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to "Constant V threshold" SoC')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=round(battery_value,
                                          PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1),
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self,
                                                           source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check inputs fields')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRELESS)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators when charging')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=self.constant_v_threshold)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Exit charging mode withing debouncing time')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self,
                                                          source=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for 0.5 seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(0.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self,
                                                           source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
        self.device.turn_on_crush_pad_charging_emulator()
        self.post_requisite_enable_all_usb_ports = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no battery status event is broadcast')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                test_case=self, continuously_receive=False)
        self.assertIsNone(battery_status_event,
                          msg=f"[{self.current_channel}] {HIDDispatcher.QueueName.EVENT} not empty, "
                              f"received {battery_status_event}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the charging status is {UnifiedBattery.ChargingStatus.CHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self,
                                                                                self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRELESS)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators when charging')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=self.constant_v_threshold)

        self.testCaseChecked("BUS_1004_0009")
    # end def test_charging_state_not_change_wireless

    @features('Feature1004')
    @features('Rechargeable')
    @features('GamingDevice')
    @features('WirelessCharging')
    @level('Business')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_external_power_source_transition(self):
        """
        Validate the device under Crush Pad charging mode is going to switch to USB charging mode when the USB
        charging cable is plugging.
        """
        self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
        battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, self.constant_v_threshold)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to "Constant V threshold" SoC')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True,
                   starting_voltage=round(battery_value,
                                          PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1),
                   cleanup_battery_event=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter charging mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self,
                                                           source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=UnifiedBattery.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for battery_status_event response')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                test_case=self, continuously_receive=True,
                external_power_status=UnifiedBattery.ExternalPowerStatus.WIRELESS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the charging status is {UnifiedBattery.ChargingStatus.CHARGING}')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self,
                                                                                self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status,
                                      UnifiedBattery.ExternalPowerStatus.WIRELESS)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check external_power_status = '
                                  f'{UnifiedBattery.ExternalPowerStatus.WIRELESS}')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRELESS)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators when charging')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=self.constant_v_threshold)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power-on the USB cable')
        # --------------------------------------------------------------------------------------------------------------
        usb_channel = None
        if (self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb and
                not ProtocolManagerUtils.is_corded_device_only(test_case=self)):
            usb_channel_id = ChannelIdentifier(
                port_index=self.device.CHARGING_PORT_NUMBER, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER)
            usb_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=usb_channel_id)
            if self.device.is_usb_channel_on_hub(usb_channel):
                self.device.turn_on_usb_charging_cable()
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check battery status event is broadcast')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = \
            UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation_const_current_charging(
                test_case=self, continuously_receive=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the external power status is {UnifiedBattery.ExternalPowerStatus.WIRED}')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to USB channel")
        # --------------------------------------------------------------------------------------------------------------
        if usb_channel is not None:
            ProtocolManagerUtils.switch_to_usb_channel(test_case=self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_status response and check external_power_status = '
                                  f'{UnifiedBattery.ExternalPowerStatus.WIRED}')
        # --------------------------------------------------------------------------------------------------------------
        battery_level_status = UnifiedBatteryTestUtils.get_battery_level_status(self, self.constant_v_threshold)
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge_in_range, self.constant_v_threshold),
            "battery_level_full": (checker.check_full_battery_level, battery_level_status[0]),
            "battery_level_good": (checker.check_good_battery_level, battery_level_status[1]),
            "battery_level_low": (checker.check_low_battery_level, battery_level_status[2]),
            "battery_level_critical": (checker.check_critical_battery_level, battery_level_status[3]),
            "charging_status": (checker.check_charging_status, UnifiedBattery.ChargingStatus.CHARGING),
            "external_power_status": (checker.check_external_power_status, UnifiedBattery.ExternalPowerStatus.WIRED)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the battery LED indicators when charging')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(state_of_charge=self.constant_v_threshold)

        self.testCaseChecked("BUS_1004_0010")
    # end def test_external_power_source_transition
# end class UnifiedBatteryBusinessGamingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
