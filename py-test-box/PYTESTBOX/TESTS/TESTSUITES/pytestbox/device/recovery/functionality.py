#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.recovery.functionality
:brief: Device recovery functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.recovery.recovery import DeviceRecoveryTestCase
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.recoveryutils import DisconnectMethod
from pytestbox.shared.base.recoveryutils import RecoveryTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceRecoveryFunctionalityTestCase(DeviceRecoveryTestCase):
    """
    Validate ``DeviceRecovery`` functionality test cases
    """

    @features('DeviceRecovery')
    @level('Functionality')
    @services('Debugger')
    def test_no_hid_reports_in_recovery(self):
        """
        Validate that there is no HID reports in recovery mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action that would trigger an HID message')
        # --------------------------------------------------------------------------------------------------------------
        # Empty HID queue first to remove the HID messages from the application before jumping on bootloader
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # Recovery actions in application typically trigger HID,
        # if used in recovery it should not trigger an HID message
        RecoveryTestUtils.perform_pre_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'No HID message has been received')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(test_case=self, text='Release post-reset button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_post_reset_actions(test_case=self)

        self.testCaseChecked("FUN_DEV_RECV_0001")
    # end def test_no_hid_reports_in_recovery

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_disconnect_before_dfu_start(self):
        """
        Validate that disconnection in recovery mode before starting DFU restart the device in application
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disconnect before starting a DFU')
        # --------------------------------------------------------------------------------------------------------------
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel.receiver_channel)
        self._disconnect_device(disconnect_method=DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING)
        RecoveryTestUtils.verify_recovery_disconnection(
            test_case=self,
            recovery_device_index=self.recovery_device_index,
            application_device_index=self.original_device_index,
            disconnection_method_used=DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING)
        sleep(1)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        self.testCaseChecked("FUN_DEV_RECV_0002")
    # end def test_disconnect_before_dfu_start

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    @skip("BLE Stack Emulator needed")
    def test_no_bonding_in_recovery(self):
        """
        Validate no bonding credential are stored in recovery mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read bonding credential chunk history in NVS')
        # --------------------------------------------------------------------------------------------------------------
        nvs_ble_bond_ids = DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect with pairing')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader(pairing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no new bonding credential has been added in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=nvs_ble_bond_ids,
                         obtained=DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self),
                         msg="New bonding credential created when it should not")

        self.testCaseChecked("FUN_DEV_RECV_0003")
    # end def test_no_bonding_in_recovery

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_bonding_credential_not_erased_after_dfu_start(self):
        """
        Validate the bonding credential of the application are Not deleted after DFU process starts
        and that a specific chunk is written by the bootloader when a DFU occurs in recovery mode
        Change Request: https://jira.logitech.io/browse/BPRO-294

        The deletion of all pairing credentials and CCCDs is done in Application if NVS_DFU_OUT_OF_RECOVERY_ID bit set
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Save initial pairing history')
        # --------------------------------------------------------------------------------------------------------------
        initial_nvs_ble_bond_ids = DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the first command of DFU: DfuStart')
        # --------------------------------------------------------------------------------------------------------------
        self._perform_first_command_of_dfu()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify all bonding credentials have been preserved in the NVS')
        # --------------------------------------------------------------------------------------------------------------
        # Force NVS read operation
        self.memory_manager.nvs_parser = None
        new_nvs_ble_bond_ids = DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self)
        self.assertEqual(expected=initial_nvs_ble_bond_ids,
                         obtained=new_nvs_ble_bond_ids,
                         msg=f"Some bonding credentials have been deleted: {initial_nvs_ble_bond_ids} vs "
                             f"{new_nvs_ble_bond_ids}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 'NVS_DFU_OUT_OF_RECOVERY_ID' chunk is written in NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.check_dfu_out_of_recovery(self, self.memory_manager)

        self.testCaseChecked("FUN_DEV_RECV_0004")
    # end def test_bonding_credential_not_erased_after_dfu_start

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_disconnect_after_dfu_start(self):
        """
        Validate that disconnection in recovery mode after starting DFU restart the device still in recovery mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the first command of DFU: DfuStart')
        # --------------------------------------------------------------------------------------------------------------
        self._perform_first_command_of_dfu()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disconnect after starting a DFU')
        # --------------------------------------------------------------------------------------------------------------
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel.receiver_channel)
        self._disconnect_device(disconnect_method=DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING)
        RecoveryTestUtils.verify_recovery_disconnection(
            test_case=self,
            disconnection_method_used=DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING,
            recovery_device_index=self.recovery_device_index,
            application_device_index=self.original_device_index,
            check_application_connection=False)
        sleep(1)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self)
        self.recovery_device_index = self.current_channel.device_index

        self.testCaseChecked("FUN_DEV_RECV_0005")
    # end def test_disconnect_after_dfu_start

    @features('DeviceRecovery')
    @features('Feature00D0SoftDevice')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_complete_recovery_last_slot(self):
        """
        Validate the device could be paired in recovery mode on the last receiver pairing slot.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Initialize the authentication method parameter")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Pair the device on all pairing slots except the last one")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unpairing = True
        self._complete_dfu_business(pairing=False, soft_device=True)

        self.testCaseChecked("FUN_DEV_RECV_0006")
    # end def test_complete_recovery_last_slot

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Time-consuming')
    @services('Debugger')
    @services('PowerSupply')
    @skip("In development")
    def test_restart_to_exit_deep_sleep(self):
        """
        Validate that exiting deep sleep in recovery mode is done by power off/on the device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Erase \"Application Valid\" flag')
        # --------------------------------------------------------------------------------------------------------------
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel.receiver_channel)
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(self.HID_PP_TIMEOUT + 1) // 60}min{(self.HID_PP_TIMEOUT + 1) % 60}s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.HID_PP_TIMEOUT + 1)
        RecoveryTestUtils.verify_recovery_disconnection(
            test_case=self,
            disconnection_method_used=DisconnectMethod.DEVICE_DEEP_SLEEP,
            recovery_device_index=self.recovery_device_index,
            application_device_index=self.original_device_index)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        # TODO This check will always fail because the device is in deep sleep
        RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self)
        self.recovery_device_index = self.current_channel.device_index

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send command to get current value from power supply')
        # --------------------------------------------------------------------------------------------------------------
        current_value = self._get_current_consumption()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the current value is in the expected range for deep sleep')
        # --------------------------------------------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(expected=True,
                         obtained=(current_value < f.PRODUCT.FEATURES.COMMON.POWER_MODES.F_CurrentThresholdDeepSleep),
                         msg='The current value (%d uA) shall be below the Deep Sleep threshold (%d uA)' %
                             (current_value, f.PRODUCT.FEATURES.COMMON.POWER_MODES.F_CurrentThresholdDeepSleep))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off/on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform DFU')
        # --------------------------------------------------------------------------------------------------------------
        self._perform_dfu()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Device shall be in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        self.testCaseChecked("FUN_DEV_RECV_0007")
    # end def test_restart_to_exit_deep_sleep

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    @skip("BLE Stack Emulator needed")
    def test_complete_recovery_dfu_business_pairing(self):
        """
        Validate the business case with pairing of the DFU process in recovery mode
        """
        self._complete_dfu_business(pairing=True)

        self.testCaseChecked("FUN_DEV_RECV_0008#1")
    # end def test_complete_recovery_dfu_business_pairing

    @features('DeviceRecovery')
    @features('Feature00D0SoftDevice')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    @skip("BLE Stack Emulator needed")
    def test_complete_recovery_soft_device_dfu_business_pairing(self):
        """
        Validate the business case with pairing of the soft device DFU process in recovery mode
        """
        self._complete_dfu_business(pairing=True, soft_device=True)

        self.testCaseChecked("FUN_DEV_RECV_0008#2")
    # end def test_complete_recovery_soft_device_dfu_business_pairing
# end class DeviceRecoveryFunctionalityTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
