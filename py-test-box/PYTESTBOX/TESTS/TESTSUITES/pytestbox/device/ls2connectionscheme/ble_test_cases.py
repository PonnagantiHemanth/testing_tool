#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.ble_test_cases
:brief: Validate LS2/UHS connection scheme for BLE test cases
:author: Zane Lu <zlu@logitech.com>
:date: 2024/04/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.ls2connectionscheme.protocol_switch import ProtocolSwitchTestCases
from pytransport.ble.bleconstants import BleAdvertisingPduType


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BleTestCases(ProtocolSwitchTestCases):
    """
    LS2 connection scheme - BLE Test Cases
    """
    DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT = 3 * 60

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "BLE channel is selected")
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        super().tearDown()
    # end def tearDown

    def press_connect_button(self, long_press=False):
        """
        Press the connect button.
        """
        if self.f.PRODUCT.F_IsMice:
            self.assertTrue(expr=KEY_ID.CONNECT_BUTTON in self.button_stimuli_emulator.connected_key_ids,
                            msg="No connect button.")
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                                   duration=ButtonStimuliInterface.LONG_PRESS_DURATION if long_press
                                                   else ButtonStimuliInterface.DEFAULT_DURATION)
        else:
            if KEY_ID.LS2_BLE_CONNECTION_TOGGLE in self.button_stimuli_emulator.connected_key_ids:
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.LS2_BLE_CONNECTION_TOGGLE,
                                                       duration=ButtonStimuliInterface.LONG_PRESS_DURATION if long_press
                                                       else ButtonStimuliInterface.DEFAULT_DURATION)
            else:
                self.assertTrue(expr=KEY_ID.BLE_CONNECTION in self.button_stimuli_emulator.connected_key_ids,
                                msg="No BLE connection button.")
                self.button_stimuli_emulator.keystroke(
                    key_id=KEY_ID.BLE_CONNECTION,
                    duration=ButtonStimuliInterface.LONG_PRESS_DURATION if long_press
                    else ButtonStimuliInterface.DEFAULT_DURATION)
            # end if
        # end if
    # end def press_connect_button

    def verify_enter_ble_pairing_mode(self):
        """
        Verify the device enters BLE pairing mode if the BLE channel is selected but unpaired,
        search for a BLE host and pair with it.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the advertising type')
        # --------------------------------------------------------------------------------------------------------------
        ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                  send_scan_request=True)
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User action')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the HID event')
        # --------------------------------------------------------------------------------------------------------------
        self.check_hid_input(count=1, ble_notification_queue=self.ble_notification_queue)
    # end def verify_enter_ble_pairing_mode

    def verify_ble_channel_reconnection(self):
        """
        Verify the device enters BLE reconnection if the BLE channel is selected and paired,
        and the device reconnects to the host
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the advertising type')
        # --------------------------------------------------------------------------------------------------------------
        ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                  send_scan_request=True)
        self.assertEqual(
            obtained=ble_device.advertising_type,
            expected=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
            msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_DIRECTED.name}. "
                f"Got {ble_device.advertising_type}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reconnect the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User action')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the HID event')
        # --------------------------------------------------------------------------------------------------------------
        self.check_hid_input(count=1, ble_notification_queue=self.ble_notification_queue)
    # end def verify_ble_channel_reconnection

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Business')
    @services('PowerSupply')
    def test_enter_ble_pairing_mode_if_ble_channel_is_selected_but_unpaired_at_power_on(self):
        """
        [with Connect Button] At power on, the device shall enter BLE pairing mode
        if the BLE channel is selected but unpaired, search for a BLE host and pair with it.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device enters BLE pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_enter_ble_pairing_mode()

        self.testCaseChecked("BUS_BLE_INIT_0001")
    # end def test_enter_ble_pairing_mode_if_ble_channel_is_selected_but_unpaired_at_power_on

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_ble_pairing_mode_if_ble_channel_is_selected_but_unpaired_at_wake_up(self):
        """
        [with Connect Button] At wake-up, the device shall enter BLE pairing mode
        if the BLE channel is selected but unpaired, search for a BLE host and pair with it.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter deep sleep mode from BLE channel")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT)
        self.verify_deep_sleep_current_consumption()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wake up the device')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device enters BLE pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_enter_ble_pairing_mode()

        self.testCaseChecked("FUN_BLE_INIT_0002")
    # end def test_enter_ble_pairing_mode_if_ble_channel_is_selected_but_unpaired_at_wake_up

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Business')
    @services('PowerSupply')
    def test_enter_ble_reconnection_if_ble_channel_is_selected_and_paired_at_power_on(self):
        """
        [with Connect Button] At power on, the device shall enter 'BLE reconnection' and end up in 'Connected' mode
        if the BLE channel is selected and paired and the device reconnects to the host.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Reset the device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device enters BLE reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_channel_reconnection()

        self.testCaseChecked("BUS_BLE_INIT_0003")
    # end def test_enter_ble_reconnection_if_ble_channel_is_selected_and_paired_at_power_on

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_ble_reconnection_if_ble_channel_is_selected_and_paired_at_wake_up(self):
        """
        [with Connect Button] At wake-up, the device shall enter 'BLE reconnection' and end up in 'Connected' mode
        if the BLE channel is selected and paired and the device reconnects to the host.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Reset the device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter deep sleep mode from BLE channel")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT)
        self.verify_deep_sleep_current_consumption()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wake up the device')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device enters BLE reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_channel_reconnection()

        self.testCaseChecked("FUN_BLE_INIT_0004")
    # end def test_enter_ble_reconnection_if_ble_channel_is_selected_and_paired_at_wake_up

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Business')
    @services('PowerSupply')
    def test_device_shall_connect_to_host_2_with_long_presss_connect_button_while_host_1_is_connected(self):
        """
        [with Connect Button] While connected to Host 1 in BLE, the device shall move to BLE pairing
        when the user does a long press on the Connect/Bluetooth button and be able to connect to a Host 2.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'BLE channel paired with the host 1')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        target_ble_address = BleProtocolTestUtils.increment_address(test_case=self)
        BleProtocolTestUtils.start_scan_for_devices(
            test_case=self, ble_addresses=[target_ble_address],
            scan_timeout=15, send_scan_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device is BLE-discoverable')
        # --------------------------------------------------------------------------------------------------------------
        ble_devices = BleProtocolTestUtils.get_scanning_result(test_case=self, timeout=10)
        self.assertTrue(expr=len(ble_devices) > 0, msg=f"Could not find the device with param: {[target_ble_address]}")

        ble_device = ble_devices[0]
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        self.ble_channel.close()
        BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connects to the host 2')
        # --------------------------------------------------------------------------------------------------------------
        # Treat the BLE host as an another one
        self.ble_device = ble_device
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User action')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the HID event')
        # --------------------------------------------------------------------------------------------------------------
        self.check_hid_input(count=1, ble_notification_queue=self.ble_notification_queue)

        self.testCaseChecked("BUS_BLE_PAIRING_0001")
    # end def test_device_shall_connect_to_host_2_with_long_presss_connect_button_while_host_1_is_connected

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_shall_ignore_any_long_press_on_the_connect_button_when_in_pairing_mode(self):
        """
        [with Connect Button] BLE Pairing - When in pairing mode,
        the device shall ignore any long press action on the Connect or Bluetooth button.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'BLE channel paired with the host 1')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        target_ble_address = BleProtocolTestUtils.increment_address(test_case=self)
        BleProtocolTestUtils.start_scan_for_devices(
            test_case=self, ble_addresses=[target_ble_address],
            scan_timeout=15, send_scan_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device is BLE-discoverable')
        # --------------------------------------------------------------------------------------------------------------
        ble_devices = BleProtocolTestUtils.get_scanning_result(test_case=self, timeout=10)
        self.assertTrue(expr=len(ble_devices) > 0, msg=f"Could not find the device with param: {[target_ble_address]}")

        ble_device = ble_devices[0]
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'long-press the connect button again')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        self.ble_channel.close()
        BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connects to the host 2')
        # --------------------------------------------------------------------------------------------------------------
        # Treat the BLE host as an another one
        self.ble_device = ble_device
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User action')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the HID event')
        # --------------------------------------------------------------------------------------------------------------
        self.check_hid_input(count=1, ble_notification_queue=self.ble_notification_queue)

        self.testCaseChecked("FUN_BLE_PAIRING_0002")
    # end def test_device_shall_ignore_any_long_press_on_the_connect_button_when_in_pairing_mode

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_shall_reconnect_to_the_previous_ble_host_after_existing_pairing_mode_by_reset_device(self):
        """
        [with Connect Button] BLE Pairing - The device will exit the pairing mode
        if the user does a device power off / on and reconnect to the previous BLE Host.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'BLE channel paired with a host')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 3 minutes-timeout')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device reconnects to BLE host')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_channel_reconnection()

        self.testCaseChecked("FUN_BLE_PAIRING_0003")
    # end def test_device_shall_reconnect_to_the_previous_ble_host_after_existing_pairing_mode_by_reset_device

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_shall_return_in_reconnection_mode_if_short_press_on_the_connect_button_while_pairing(self):
        """
        [with Connect Button] BLE Pairing - The device will return in Reconnection mode
        if the user does a short press on the Connect or Bluetooth button.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'BLE channel paired with a host')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Short-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device reconnects to BLE host')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_channel_reconnection()

        self.testCaseChecked("FUN_BLE_PAIRING_0004")
    # end def test_device_shall_return_in_reconnection_mode_if_short_press_on_the_connect_button_while_pairing

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_shall_enter_in_deep_sleep_mode_for_unpaired_channel_if_3_minutes_timeout_occurs_in_pairing(self):
        """
        BLE Pairing - While in pairing mode in BLE and the channel is unpaired,
        the device shall enter in deep sleep mode if the 3 minutes device pairing timeout occurs.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device is BLE-discoverable')
        # --------------------------------------------------------------------------------------------------------------
        ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                  send_scan_request=True)
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 3 minutes-timeout')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device enters in deep sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_deep_sleep_current_consumption()

        self.testCaseChecked("FUN_BLE_PAIRING_0005")
    # end def test_device_shall_enter_in_deep_sleep_mode_for_unpaired_channel_if_3_minutes_timeout_occurs_in_pairing

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_shall_return_in_reconnection_mode_for_paired_channel_if_3_minutes_timeout_occurs_in_pairing(self):
        """
        BLE Pairing - While in pairing mode in BLE and the channel is paired,
        the device shall return in reconnection mode if the 3 minutes device pairing timeout occurs.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'BLE channel paired with a host')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        target_ble_address = BleProtocolTestUtils.increment_address(test_case=self)
        BleProtocolTestUtils.start_scan_for_devices(
            test_case=self, ble_addresses=[target_ble_address],
            scan_timeout=15, send_scan_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device is BLE-discoverable')
        # --------------------------------------------------------------------------------------------------------------
        ble_devices = BleProtocolTestUtils.get_scanning_result(test_case=self, timeout=10)
        self.assertTrue(expr=len(ble_devices) > 0, msg=f"Could not find the device with param: {[target_ble_address]}")

        ble_device = ble_devices[0]
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 3 minutes-timeout')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device reconnects to BLE host')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_channel_reconnection()

        self.testCaseChecked("FUN_BLE_PAIRING_0006")
    # end def test_device_shall_return_in_reconnection_mode_for_paired_channel_if_3_minutes_timeout_occurs_in_pairing

    """
    'FUN_BLE_PAIRING_0007':
    test_device_shall_return_in_pairing_mode_while_ble_pairing_sequence_failed
    (PENDING: Given technological limitations, currently not available to put devices in a failed paring mode,
     because they default to Just Works authentication and it's done entirely by the bluetooth stack on the dev kit.)
    """

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Functionality')
    @services('PowerSupply')
    def test_reconnect_to_a_known_host_but_failed(self):
        """
        [with Connect Button] When trying to reconnect to a known host, the device shall go into Deep sleep mode
        if the BLE channel is selected and paired but the device could not reconnect to the host.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        target_ble_address = BleProtocolTestUtils.increment_address(test_case=self)
        BleProtocolTestUtils.start_scan_for_devices(
            test_case=self, ble_addresses=[target_ble_address],
            scan_timeout=15, send_scan_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device is BLE-discoverable')
        # --------------------------------------------------------------------------------------------------------------
        ble_devices = BleProtocolTestUtils.get_scanning_result(test_case=self, timeout=10)
        self.assertTrue(expr=len(ble_devices) > 0, msg=f"Could not find the device with param: {[target_ble_address]}")

        ble_device = ble_devices[0]
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Wait timeout-fail')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device enters in deep sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_deep_sleep_current_consumption()

        self.testCaseChecked("FUN_BLE_RECONNECT_0001")
    # end def test_reconnect_to_a_known_host_but_failed

    @features('LS2BleTest')
    @features('GamingDevice')
    @level('Business')
    @services('PowerSupply')
    def test_reconnect_to_a_known_host_and_succeed(self):
        """
        [with Connect Button] When trying to reconnect to a known host, the device shall end up in 'Connected' mode
        if the BLE channel is selected and paired and the device is able to reconnect to the host.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Long-press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.press_connect_button(long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Wait timeout-fail')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.DURATION_OF_NO_CONNECTION_PAIRING_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Reconnect the device')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the HID event')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        self.check_hid_input(count=1, ble_notification_queue=self.ble_notification_queue)

        self.testCaseChecked("BUS_BLE_RECONNECT_0002")
    # end def test_reconnect_to_a_known_host_and_succeed


# end class BleTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
