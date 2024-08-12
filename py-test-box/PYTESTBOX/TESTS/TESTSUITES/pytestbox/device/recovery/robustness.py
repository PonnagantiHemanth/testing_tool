#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.recovery.functionality
:brief: Device recovery robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.dfu import Restart
from pyhid.hidpp.features.common.dfu import RestartResponse
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuCmdDataXData
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.productdata import PRE_RESET_ACTIONS
from pytestbox.base.productdata import POST_RESET_ACTIONS
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.recovery.recovery import DeviceRecoveryTestCase
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.recoveryutils import DisconnectMethod
from pytestbox.shared.base.recoveryutils import RecoveryTestUtils
from pytransport.transportcontext import TransportContextException
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceRecoveryRobustnessTestCase(DeviceRecoveryTestCase):
    """
    Validate ``DeviceRecovery`` robustness test cases
    """

    @features('DeviceRecoveryActions', PRE_RESET_ACTIONS)
    @level('Robustness')
    @services('Debugger')
    def test_release_first_button_key_before_restart(self):
        """
        Validate the device does not restart on recovery if the first button/key is released before restarting the
        device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press pre-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_pre_reset_actions(test_case=self)
        sleep(.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release first button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        (key_id, _) = RecoveryTestUtils.get_pre_reset_actions(test_case=self)[0]
        RecoveryTestUtils.filter_and_perform_actions(test_case=self, action_list=[(key_id, 'break')])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch off/on the device')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_restart_action_for_recovery(test_case=self)
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release post-reset button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_post_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("ROB_DEV_RECV_0001")
    # end def test_release_first_button_key_before_restart

    @features('DeviceRecoveryActions', PRE_RESET_ACTIONS, 2)
    @level('Robustness')
    @services('Debugger')
    def test_release_second_button_key_before_restart(self):
        """
        Validate the device does not restart on recovery if the second button/key is released before restarting the
        device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press pre-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_pre_reset_actions(test_case=self)
        sleep(.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release second button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        (key_id, _) = RecoveryTestUtils.get_pre_reset_actions(test_case=self)[1]
        RecoveryTestUtils.filter_and_perform_actions(test_case=self, action_list=[(key_id, 'break')])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch off/on the device')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_restart_action_for_recovery(test_case=self)
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release post-reset button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_post_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("ROB_DEV_RECV_0002")
    # end def test_release_second_button_key_before_restart

    @features('DeviceRecoveryActions', PRE_RESET_ACTIONS)
    @level('Robustness')
    @services('PowerSupply')
    def test_release_first_button_key_after_power_off_before_power_on(self):
        """
        Validate the device does not restart on recovery if the first button/key is released before powering on the
        device
        """
        self.post_requisite_device_restart_in_main_application = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press pre-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_pre_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off device')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release first button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        (key_id, _) = RecoveryTestUtils.get_pre_reset_actions(test_case=self)[0]
        RecoveryTestUtils.filter_and_perform_actions(test_case=self, action_list=[(key_id, 'break')])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on device')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_on()
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release post-reset button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_post_reset_actions(test_case=self)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        self.testCaseChecked("ROB_DEV_RECV_0003")
    # end def test_release_first_button_key_after_power_off_before_power_on

    @features('DeviceRecoveryActions', PRE_RESET_ACTIONS, 2)
    @level('Robustness')
    @services('PowerSupply')
    def test_release_second_button_key_after_power_off_before_power_on(self):
        """
        Validate the device does not restart on recovery if the second button/key is released before powering on the
        device
        """
        self.post_requisite_device_restart_in_main_application = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press pre-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_pre_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off device')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release second button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        (key_id, _) = RecoveryTestUtils.get_pre_reset_actions(test_case=self)[1]
        RecoveryTestUtils.filter_and_perform_actions(test_case=self, action_list=[(key_id, 'break')])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on device')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_on()
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release post-reset button/key for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_post_reset_actions(test_case=self)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        self.testCaseChecked("ROB_DEV_RECV_0004")
    # end def test_release_second_button_key_after_power_off_before_power_on

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @features('Mice')
    @level('Robustness')
    @services('Debugger')
    @services('OpticalSensor')
    def test_xy_displacement_robustness(self):
        """
        Validate the device restart on recovery even if there are some xy displacement
        """
        self.post_requisite_device_restart_in_main_application = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press pre-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_pre_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Generate XY displacements')
        # --------------------------------------------------------------------------------------------------------------
        # We add some repetitions to have displacement throughout the restart of the device
        self.motion_emulator.xy_motion(dx=5, dy=5, repetition=9, skip=1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off/on device')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_restart_action_for_recovery(test_case=self)
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release post-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_post_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self, pairing=False)
        self.recovery_device_index = self.current_channel.device_index

        self.testCaseChecked("ROB_DEV_RECV_0005")
    # end def test_xy_displacement_robustness

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @features('Mice')
    @level('Robustness')
    @services('Debugger')
    @services('MainWheel')
    @skip("In development")
    def test_wheel_rotation_robustness(self):
        """
        Validate the device restart on recovery even if there are some wheel rotation
        """
        self.post_requisite_device_restart_in_main_application = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press pre-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_pre_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Generate wheel rotation')
        # --------------------------------------------------------------------------------------------------------------
        # We add some repetitions to have rotations throughout the restart of the device
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off/on device')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_restart_action_for_recovery(test_case=self)
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Release post-reset buttons/keys for recovery')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.perform_post_reset_actions(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self, pairing=False)
        self.recovery_device_index = self.current_channel.device_index

        self.testCaseChecked("ROB_DEV_RECV_0006")
    # end def test_wheel_rotation_robustness

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Time-consuming')
    @services('Debugger')
    def test_connect_before_timeout_robustness(self):
        """
        Validate the connection timeout by connecting right before its end
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_device_restart_in_main_application = True
        RecoveryTestUtils.perform_user_actions_for_recovery(
            test_case=self, current_device_index=ChannelUtils.get_device_index(test_case=self))

        connection_timeout = self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_BootloaderRecoveryAdvertisingCompleteWindowS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(connection_timeout - (self.TIME_MARGIN + 1)) // 60}min'
                                 f'{(connection_timeout - (self.TIME_MARGIN + 1)) % 60}s '
                                 f'(connection can take up to {self.TIME_MARGIN} seconds)')
        # --------------------------------------------------------------------------------------------------------------
        sleep(connection_timeout - (self.TIME_MARGIN + 1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self)
        self.recovery_device_index = self.current_channel.device_index

        self.testCaseChecked("ROB_DEV_RECV_0007")
    # end def test_connect_before_timeout_robustness

    @features('DeviceRecovery')
    @level('Time-consuming')
    @services('Debugger')
    @skip('connect timeout is 2h')
    def test_connect_after_timeout_robustness(self):
        """
        Validate the connection timeout by connecting right after its end
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_device_restart_in_main_application = True
        RecoveryTestUtils.perform_user_actions_for_recovery(
            test_case=self, current_device_index=ChannelUtils.get_device_index(test_case=self))

        connection_timeout = self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_BootloaderRecoveryAdvertisingCompleteWindowS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(connection_timeout + 1) // 60}min{(connection_timeout + 1) % 60}s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(connection_timeout + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        self.testCaseChecked("ROB_DEV_RECV_0008")
    # end def test_connect_after_timeout_robustness

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Time-consuming')
    @services('Debugger')
    @services('PowerSupply')
    @skip("In development")
    def test_connect_before_timeout_robustness_deep_sleep(self):
        """
        Validate the connection timeout by connecting right before its end when application not valid
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_device_restart_in_main_application = True
        RecoveryTestUtils.perform_user_actions_for_recovery(
            test_case=self, current_device_index=ChannelUtils.get_device_index(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Erase \"Application Valid\" flag')
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        connection_timeout = self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_BootloaderRecoveryAdvertisingCompleteWindowS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(connection_timeout - (self.TIME_MARGIN + 1)) // 60}min'
                                 f'{(connection_timeout - (self.TIME_MARGIN + 1)) % 60}s '
                                 f'(connection can take up to {self.TIME_MARGIN} seconds)')
        # --------------------------------------------------------------------------------------------------------------
        sleep(connection_timeout - (self.TIME_MARGIN + 1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Connect to device in recovery mode')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self)
        self.recovery_device_index = self.current_channel.device_index

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send command to get current value from power supply')
        # --------------------------------------------------------------------------------------------------------------
        current_value = self._get_current_consumption()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate if the current is bigger than 100uA, '
                                  'implying that it is not in deep sleep')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=True,
                         obtained=(current_value > 0.1),
                         msg='The current value shall be bigger than 100uA')

        self.testCaseChecked("ROB_DEV_RECV_0009")
    # end def test_connect_before_timeout_robustness_deep_sleep

    @features('DeviceRecovery')
    @level('Time-consuming')
    @services('Debugger')
    @services('PowerSupply')
    @bugtracker('Consumption_higher_with_debugger')
    @skip("In development")
    def test_connect_after_timeout_robustness_deep_sleep(self):
        """
        Validate the connection timeout by not connecting after its end when application not valid
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_device_restart_in_main_application = True
        RecoveryTestUtils.perform_user_actions_for_recovery(
            test_case=self, current_device_index=ChannelUtils.get_device_index(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Erase \"Application Valid\" flag')
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        connection_timeout = self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_BootloaderRecoveryAdvertisingCompleteWindowS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(connection_timeout + 1) // 60}min{(connection_timeout + 1) % 60}s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(connection_timeout + 1)

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

        self.testCaseChecked("ROB_DEV_RECV_0010")
    # end def test_connect_after_timeout_robustness_deep_sleep

    @features('DeviceRecovery')
    @level('Time-consuming')
    @services('Debugger')
    def test_first_hidpp_command_before_timeout_robustness(self):
        """
        Validate the HID++ command DFU timeout by sending the first HID++ command right before its end
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(self.HID_PP_TIMEOUT - 2) // 60}min{(self.HID_PP_TIMEOUT - 2) % 60}s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.HID_PP_TIMEOUT - 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send HID++ command: GetFwInfo to verify device on bootloader')
        # --------------------------------------------------------------------------------------------------------------
        DeviceInformationTestUtils.check_active_entity_type(
            test_case=self,
            device_index=self.recovery_device_index,
            entity_type=DeviceInformation.EntityTypeV1.BOOTLOADER)

        self.testCaseChecked("ROB_DEV_RECV_0011")
    # end def test_first_hidpp_command_before_timeout_robustness

    @features('DeviceRecovery')
    @level('Time-consuming')
    @services('Debugger')
    def test_in_between_hidpp_command_before_timeout_robustness(self):
        """
        Validate the HID++ command DFU timeout by sending the second HID++ command right before its end
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send HID++ command: GetFwInfo')
        # --------------------------------------------------------------------------------------------------------------
        DeviceInformationTestUtils.HIDppHelper.get_fw_info(
            test_case=self, entity_index=0, device_index=self.recovery_device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(self.HID_PP_TIMEOUT - 2) // 60}min{(self.HID_PP_TIMEOUT - 2) % 60}s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.HID_PP_TIMEOUT - 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send HID++ command: GetFwInfo to verify device on bootloader')
        # --------------------------------------------------------------------------------------------------------------
        DeviceInformationTestUtils.check_active_entity_type(
            test_case=self,
            device_index=self.recovery_device_index,
            entity_type=DeviceInformation.EntityTypeV1.BOOTLOADER)

        self.testCaseChecked("ROB_DEV_RECV_0012")
    # end def test_in_between_hidpp_command_before_timeout_robustness

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Time-consuming')
    @services('Debugger')
    def test_first_hidpp_command_after_timeout_robustness(self):
        """
        Validate the HID++ command DFU timeout by sending the first HID++ command right after its end
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {self.HID_PP_TIMEOUT // 60}min{self.HID_PP_TIMEOUT % 60}s (error '
                                 f'margin = {3 * self.TIME_MARGIN}s)')
        # --------------------------------------------------------------------------------------------------------------
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel.receiver_channel)
        sleep(self.HID_PP_TIMEOUT + 3 * self.TIME_MARGIN)
        RecoveryTestUtils.verify_recovery_disconnection(
            test_case=self,
            disconnection_method_used=DisconnectMethod.DEVICE_DEEP_SLEEP,
            recovery_device_index=self.recovery_device_index,
            application_device_index=self.original_device_index)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send HID++ command: GetFwInfo to verify device on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        self.testCaseChecked("ROB_DEV_RECV_0013")
    # end def test_first_hidpp_command_after_timeout_robustness

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Time-consuming')
    @services('Debugger')
    def test_in_between_hidpp_command_after_timeout_robustness(self):
        """
        Validate the HID++ command DFU timeout by sending the second HID++ command right after its end
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send HID++ command: GetFwInfo')
        # --------------------------------------------------------------------------------------------------------------
        DeviceInformationTestUtils.HIDppHelper.get_fw_info(
            test_case=self, entity_index=0, device_index=self.recovery_device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {(self.HID_PP_TIMEOUT + 1) // 60}min{(self.HID_PP_TIMEOUT + 1) % 60}s '
                                 f'(error margin = {3 * self.TIME_MARGIN}s)')
        # --------------------------------------------------------------------------------------------------------------
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel.receiver_channel)
        sleep(self.HID_PP_TIMEOUT + 3 * self.TIME_MARGIN)
        RecoveryTestUtils.verify_recovery_disconnection(
            test_case=self,
            disconnection_method_used=DisconnectMethod.DEVICE_DEEP_SLEEP,
            recovery_device_index=self.recovery_device_index,
            application_device_index=self.original_device_index)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send HID++ command: GetFwInfo to verify device on application')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        self.testCaseChecked("ROB_DEV_RECV_0014")
    # end def test_in_between_hidpp_command_after_timeout_robustness

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Robustness')
    @services('Debugger')
    def test_bonding_credential_not_erased_after_restart(self):
        """
        Validate the bonding credential of the application are not deleted after DFU Restart command without DfuStart
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read bonding credential chunk history in NVS')
        # --------------------------------------------------------------------------------------------------------------
        nvs_ble_bond_ids = DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU Restart command')
        # --------------------------------------------------------------------------------------------------------------
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel.receiver_channel)
        self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=Dfu.FEATURE_ID,
            channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.recovery_device_index)))

        restart = Restart(device_index=self.recovery_device_index,
                          feature_index=self.bootloader_dfu_feature_id,
                          fw_entity=0xFF)
        try:
            ChannelUtils.send_only(test_case=self, report=restart)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        """
        According to Restart specification:
        "This function may return an empty response or no response (device reset)."
        So we check that if there is a message it is a RestartResponse
        https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x00d0_dfu_v3.adoc#5-restartfwentity--pktnb-status-param
        """
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, class_type=RestartResponse, timeout=.4,
            check_first_message=False, allow_no_message=True)
        RecoveryTestUtils.verify_recovery_disconnection(
            test_case=self,
            disconnection_method_used=DisconnectMethod.DFU_RESTART,
            recovery_device_index=self.recovery_device_index,
            application_device_index=self.original_device_index)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify bonding credentials have not been deleted in the NVS')
        # --------------------------------------------------------------------------------------------------------------
        new_nvs_ble_bond_ids = DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self)
        for i in range(len(nvs_ble_bond_ids)):
            self.assertEqual(expected=nvs_ble_bond_ids[i],
                             obtained=new_nvs_ble_bond_ids[i],
                             msg=f"The bonding credential for slot {i} are deleted (or corrupted)")
        # end for

        self.testCaseChecked("ROB_DEV_RECV_0015")
    # end def test_bonding_credential_not_erased_after_restart

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Robustness')
    @services('Debugger')
    def test_bonding_credential_not_erased_after_dfu_cmd_data_x(self):
        """
        Validate the bonding credential of the application are not deleted after DFU CmdDataX command without DfuStart
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Jump on recovery bootloader and connect')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read bonding credential chunk history in NVS')
        # --------------------------------------------------------------------------------------------------------------
        nvs_ble_bond_ids = DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the possible function index for CmdDataX')
        # --------------------------------------------------------------------------------------------------------------
        self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=Dfu.FEATURE_ID,
            channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.recovery_device_index)))
        for i in range(4):
            # Change the first data byte to emulate CMD 1, 2 and 3
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU CmdDataX command')
            # ----------------------------------------------------------------------------------------------------------
            dfu_cmd_data_x_data = DfuCmdDataXData(device_index=self.recovery_device_index,
                                                  feature_index=self.bootloader_dfu_feature_id,
                                                  function_index=i,
                                                  data=HexList([i]) + HexList(
                                                      [0] * ((DfuCmdDataXData.LEN.DATA // 8) - 1)))
            ChannelUtils.send(
                test_case=self, report=dfu_cmd_data_x_data, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify bonding credentials have not been deleted in the NVS')
        # --------------------------------------------------------------------------------------------------------------
        new_nvs_ble_bond_ids = DevicePairingTestUtils.NvsManager.get_device_pairing_data_history(test_case=self)
        for i in range(len(nvs_ble_bond_ids)):
            self.assertEqual(expected=nvs_ble_bond_ids[i],
                             obtained=new_nvs_ble_bond_ids[i],
                             msg=f"The bonding credential for slot {i} are deleted (or corrupted)")
        # end for

        self.testCaseChecked("ROB_DEV_RECV_0016")
    # end def test_bonding_credential_not_erased_after_dfu_cmd_data_x

    @features('DeviceRecoveryActions', POST_RESET_ACTIONS)
    @level('Robustness')
    @services('Debugger')
    def test_less_post_reset_actions_robustness(self):
        """
        Validate the device does not restart on recovery if post reset actions are not completed
        """
        post_reset_actions = RecoveryTestUtils.get_post_reset_actions(test_case=self)

        for ignore_index in range(1, len(post_reset_actions)):
            self.post_requisite_device_restart_in_main_application = True
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press pre-reset buttons/keys for recovery')
            # ----------------------------------------------------------------------------------------------------------
            RecoveryTestUtils.perform_pre_reset_actions(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Power off/on device')
            # ----------------------------------------------------------------------------------------------------------
            RecoveryTestUtils.perform_restart_action_for_recovery(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Generate some post reset actions')
            # ----------------------------------------------------------------------------------------------------------
            RecoveryTestUtils.perform_post_reset_actions(test_case=self, ignore_action_indexes=[*range(ignore_index)])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check device on application')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")
        # end for

        self.testCaseChecked("ROB_DEV_RECV_0017")
    # end def test_less_post_reset_actions_robustness

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Robustness')
    @services('Debugger')
    def test_pairing_recovery_failed_no_empty_slot(self):
        """
        Validate the device could not be paired in recovery mode if all receiver pairing slots are used.
        """
        device_index = ChannelUtils.get_device_index(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Initialize the authentication method parameter")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
        # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
        self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
            test_case=self, memory_manager=self.device_memory_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Pair the device on all receiver pairing slots")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unpairing = True
        DevicePairingTestUtils.multiple_pairing(
            self, number_of_pairing=DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT)

        self.post_requisite_device_restart_in_main_application = True
        RecoveryTestUtils.perform_user_actions_for_recovery(test_case=self, current_device_index=device_index)

        bluetooth_address = RecoveryTestUtils.discover_recovery_bootloader(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with all authentication method to 0')
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=bluetooth_address)
        write_device_connect_response = ChannelUtils.send(
            test_case=self, report=write_device_connect, response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID++ 1.0 ERR_TOO_MANY_DEVICES (5) Error Code returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=Hidpp1ErrorCodes.ERR_TOO_MANY_DEVICES,
                         obtained=int(Numeral(write_device_connect_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ROB_DEV_RECV_0018")
    # end def test_pairing_recovery_failed_no_empty_slot
# end class DeviceRecoveryRobustnessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
