#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.functionality
:brief: HID++ 2.0  Device Secure DFU control functionality test suite
:author: Stanislas Cottard <scottard@logitech.com>, Kevin Dayet <kdayet@logitech.com>
:date: 2020/09/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep
from time import time

from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.securedfucontrol import DfuCancelEventV1
from pyhid.hidpp.features.common.securedfucontrol import GetDfuControlResponseV0
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_00c3.securedfucontrol import DeviceSecureDfuControlTestCase
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceSecureDfuControlFunctionalityTestCase(DeviceSecureDfuControlTestCase):
    """
    Validate Secure DFU Control functionality testcases for the device (feature 0x00C3).
    """
    @features('SecureDfuControlActionTypeNot0')
    @level('Functionality')
    @services('Debugger')
    def test_perform_action_when_dfu_disabled(self):
        """
        DFU Control use case when enable DFU mode is NOT requested. Check device stays in application mode after a
        reset is performed with the requested user actions.
        """
        self.generic_perform_action_when_dfu_disabled()

        self.testCaseChecked("FUN_00C3_0001")
    # end def test_perform_action_when_dfu_disabled

    @features('SecureDfuControlActionTypeNot0')
    @level('Functionality')
    @services('Debugger')
    def test_perform_action_when_dfu_enabled_then_disabled(self):
        """
        Cancel a previous enable DFU request. Check device stays in application mode after a reset is performed with
        the requested user actions.
        """
        self.generic_perform_action_when_dfu_enabled_then_disabled()

        self.testCaseChecked("FUN_00C3_0002")
    # end def test_perform_action_when_dfu_enabled_then_disabled

    @features('SecureDfuControlActionTypeNot0')
    @level('Time-consuming')
    @services('Debugger')
    def test_perform_action_when_just_before_timeout(self):
        """
        DFU Control Timeout: Enable DFU mode is requested and reset is performed just before the end of the DFU control
        timeout. Check device is in bootloader mode after a reset is performed with the requested user actions.
        """
        self.generic_perform_action_when_just_before_timeout()

        self.testCaseChecked("FUN_00C3_0003")
    # end def test_perform_action_when_just_before_timeout

    @features('SecureDfuControlActionTypeNot0')
    @level('Time-consuming')
    @services('Debugger')
    def test_perform_action_when_just_after_timeout(self):
        """
        DFU Control Timeout: Enable DFU mode is requested and reset is performed just after the DFU control
        timeout. Check device is in bootloader mode after a reset is performed with the requested user actions.
        """
        self.generic_perform_action_when_just_after_timeout()

        self.testCaseChecked("FUN_00C3_0004")
    # end def test_perform_action_when_just_after_timeout

    @features('SecureDfuControlActionTypeNot0')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_perform_action_when_just_before_timeout_after_restarting_it(self):
        """
        DFU Control Timeout restart: Send multiple enable DFU mode requests and validate the DFU control timeout
        restarts each time from zero. Check device is in bootloader mode after the reset performed with the requested
        user actions.
        """
        self.generic_perform_action_when_just_before_timeout_after_restarting_it()

        self.testCaseChecked("FUN_00C3_0005")
    # end def test_perform_action_when_just_before_timeout_after_restarting_it

    @features('SecureDfuControlUseNVS')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_perform_action_when_just_after_timeout_after_restarting_it(self):
        """
        DFU Control Timeout restart: Send multiple enable Dfu mode requests and validate the timeout notification is
        returned after the correct delay following the last request
        """
        self.generic_perform_action_when_just_after_timeout_after_restarting_it()

        self.testCaseChecked("FUN_00C3_0006")
    # end def test_perform_action_when_just_after_timeout_after_restarting_it

    @features('SecureDfuControlActionTypeNot0')
    @level('Time-consuming')
    @services('Debugger')
    def test_get_dfu_control_do_not_influence_timeout(self):
        """
         DFU Control Timeout: Send multiple getDfuControl requests and validate the DFU control timeout does NOT
         restart each time from zero. Check device stays in application mode after the reset performed with the
         requested user actions.
        """
        self.generic_get_dfu_control_do_not_influence_timeout()

        self.testCaseChecked("FUN_00C3_0007")
    # end def test_get_dfu_control_do_not_influence_timeout

    @features('SecureDfuControlAllActionTypes')
    @level('Functionality')
    @services('Debugger')
    def test_dfu_control_param_values(self):
        """
        DFU Control Param: DFU Control business case with several DFU Control Param values. Check device is in
        bootloader mode after a reset is performed with the requested user actions.
        """
        self.post_requisite_force_reload_nvs = True

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test loop over some interesting dfuControlParam value in its valid '
                                 'range')
        # ---------------------------------------------------------------------------
        for dfu_control_param in compute_sup_values(0):
            self._perform_business_case(dfu_control_param=dfu_control_param)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FUN_00C3_0008")
    # end def test_dfu_control_param_values

    @features('SecureDfuControlAtLeast1ActionData')
    @level('Functionality')
    @services('Debugger')
    def test_first_action_not_done(self):
        """
        DFU Control Action Data: Enable DFU mode is requested but the first requested user action is not done during
        the next reset. Check device stays in application mode.
        """
        self._ignore_action_index_test(action_to_ignore_index=0)

        self.testCaseChecked("FUN_00C3_0009")
    # end def test_first_action_not_done

    @features('SecureDfuControlAtLeast2ActionData')
    @level('Functionality')
    @services('Debugger')
    def test_second_action_not_done(self):
        """
        DFU Control Action Data: Enable DFU mode is requested but the second requested user action is not done during
        the next reset. Check device stays in application mode.
        """
        self._ignore_action_index_test(action_to_ignore_index=1)

        self.testCaseChecked("FUN_00C3_0010")
    # end def test_second_action_not_done

    @features('SecureDfuControlAtLeast3ActionData')
    @level('Functionality')
    @services('Debugger')
    def test_third_action_not_done(self):
        """
        DFU Control Action Data: Enable DFU mode is requested but the third requested user action is not done during
        the next reset. Check device stays in application mode.
        """
        self._ignore_action_index_test(action_to_ignore_index=2)

        self.testCaseChecked("FUN_00C3_0011")
    # end def test_third_action_not_done

    @features('SecureDfuControlActionTypeNot0')
    @level('Functionality')
    @services('Debugger')
    def test_add_1_more_user_action(self):
        """
        DFU Control Action Data: Follow the business case sequence plus add another user action during the device
        reset. Check device is in bootloader mode after the reset performed with the requested user actions.
        """
        self._perform_business_case(add_user_action=True)

        self.testCaseChecked("FUN_00C3_0012")
    # end def test_add_1_more_user_action

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_soft_reset_do_not_jump_on_bootloader(self):
        """
        DFU Control reset type. Check device stays in application mode after a Soft reset is performed with the
        requested user actions. Check the DFU enable NVS state is not modified by a soft reset.
        """
        self.generic_soft_reset_do_not_jump_on_bootloader()

        self.testCaseChecked("FUN_00C3_0013")
    # end def test_soft_reset_do_not_jump_on_bootloader

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_disabled_to_enabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU enabled when DFU disabled in NVS
        """
        self.generic_nvs_chunk_dfu_disabled_to_enabled()

        self.testCaseChecked("FUN_00C3_0014")
    # end def test_nvs_chunk_dfu_disabled_to_enabled

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_enabled_to_disabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU disabled when DFU enabled in NVS
        """
        self.generic_nvs_chunk_dfu_enabled_to_disabled()

        self.testCaseChecked("FUN_00C3_0015")
    # end def test_nvs_chunk_dfu_enabled_to_disabled

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_enabled_to_enable(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU enabled when DFU already enabled in NVS
        """
        self.generic_nvs_chunk_dfu_enabled_to_enable()

        self.testCaseChecked("FUN_00C3_0016")
    # end def test_nvs_chunk_dfu_enabled_to_enable

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_disabled_to_disabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU disabled when DFU already disabled in NVS
        """
        self.generic_nvs_chunk_dfu_disabled_to_disabled()

        self.testCaseChecked("FUN_00C3_0017")
    # end def test_nvs_chunk_dfu_disabled_to_disabled

    @features('SecureDfuControlUseNVS')
    @features('Feature1802')
    @features('Feature1E00')
    @level('Functionality')
    @services('Debugger')
    def test_force_reset_do_not_jump_on_bootloader(self):
        """
        DFU Control reset type. Check device stays in application mode after a ForceReset (0x1802) is performed with
        the requested user actions. Check the DFU enable NVS state is not modified by a ForceReset (0x1802).
        """
        self.post_requisite_force_reload_nvs = True
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1802)')
        # ---------------------------------------------------------------------------
        device_reset_feature_id = ChannelUtils.update_feature_mapping(test_case=self, feature_id=DeviceReset.FEATURE_ID)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # ---------------------------------------------------------------------------
        set_dfu_control = self.feature_under_test.set_dfu_control_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id, enable_dfu=1)
        ChannelUtils.send(test_case=self, report=set_dfu_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=self.feature_under_test.set_dfu_control_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # ---------------------------------------------------------------------------
        get_dfu_control = self.feature_under_test.get_dfu_control_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id)
        get_dfu_control_response = ChannelUtils.send(
            test_case=self, report=get_dfu_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_under_test.get_dfu_control_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Feature')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a ForceReset (0x1802) with all the requested user actions')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(
            test_case=self,
            action_type=get_dfu_control_response.dfu_control_action_type,
            action_data=get_dfu_control_response.dfu_control_action_data,
            device_reset_feature_id=device_reset_feature_id)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device stays in Main Application mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
            msg="Device not in application")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and check enable byte is 1')
        # ---------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
        self.assertEqual(expected=1,
                         obtained=to_int(dfu_chunk.enable),
                         msg='The enable parameter differs from the expected one')

        self.testCaseChecked("FUN_00C3_0018")
    # end def test_force_reset_do_not_jump_on_bootloader

    @features('SecureDfuControlOtherActionType')
    @features('SecureDfuControlReloadActionType', 0)
    @level('Functionality')
    @services('Debugger')
    def test_dfu_control_business_action_type_00(self):
        """
        DFU Control business case when enable DFU mode is requested for firmware with action type equals 0 (no action).
        Check device is in bootloader mode after a reset is performed with the requested user actions. Check 0xD0
        feature is advertised in bootloader mode. Check DFU status LED starts blinking when entering bootloader mode
        and stops immediately when it leaves this mode.
        """
        self._test_other_action_type(action_type=GetDfuControlResponseV0.ACTION.NO_ACTION)

        self.testCaseChecked("FUN_00C3_0019")
    # end def test_dfu_control_business_action_type_00

    @features('SecureDfuControlOtherActionType')
    @features('SecureDfuControlReloadActionType', 1)
    @level('Business')
    @services('Debugger')
    def test_dfu_control_business_action_type_01(self):
        """
        DFU Control business case when enable DFU mode is requested for firmware with action type equals 1 (Off/On).
        Check device is in bootloader mode after a reset is performed with the requested user actions. Check 0xD0
        feature is advertised in bootloader mode. Check DFU status LED starts blinking when entering bootloader mode
        and stops immediately when it leaves this mode.
        """
        self._test_other_action_type(action_type=GetDfuControlResponseV0.ACTION.OFF_ON)

        self.testCaseChecked("FUN_00C3_0020")
    # end def test_dfu_control_business_action_type_01

    @features('SecureDfuControlOtherActionType')
    @features('SecureDfuControlReloadActionType', 2)
    @level('Functionality')
    @services('Debugger')
    def test_dfu_control_business_action_type_02(self):
        """
        DFU Control business case when enable DFU mode is requested for firmware with action type equals 2 (Off/On +
        keyboard keys). Check device is in bootloader mode after a reset is performed with the requested user actions.
        Check 0xD0 feature is advertised in bootloader mode. Check DFU status LED starts blinking when entering
        bootloader mode and stops immediately when it leaves this mode.
        """
        self._test_other_action_type(action_type=GetDfuControlResponseV0.ACTION.OFF_ON_KBD_KEYS)

        self.testCaseChecked("FUN_00C3_0021")
    # end def test_dfu_control_business_action_type_02

    @features('SecureDfuControlOtherActionType')
    @features('SecureDfuControlReloadActionType', 3)
    @level('Functionality')
    @services('Debugger')
    def test_dfu_control_business_action_type_03(self):
        """
        DFU Control business case when enable DFU mode is requested for firmware with action type equals 2 (Off/On +
        mouse clicks). Check device is in bootloader mode after a reset is performed with the requested user actions.
        Check 0xD0 feature is advertised in bootloader mode. Check DFU status LED starts blinking when entering
        bootloader mode and stops immediately when it leaves this mode.
        """
        self._test_other_action_type(action_type=GetDfuControlResponseV0.ACTION.OFF_ON_MSE_CLICKS)

        self.testCaseChecked("FUN_00C3_0022")
    # end def test_dfu_control_business_action_type_03

    @features('SecureDfuControlActionTypeNot0')
    @features('ConnectButton')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.CONNECT_BUTTON,))
    @services('Debugger')
    def test_set_dfu_control_press_connect_button_after_timeout(self):
        """
        Validate Connect button keystrokes are ignored if set dfu control timeout is ongoing

        cf Patchset#6197 - conn_manager, prevent changing host when DFU is requested
        http://goldenpass.logitech.com:8080/c/ccp_fw/quark/+/6197
        """
        get_dfu_control_response = self.generic_set_get_dfu_control()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for the duration of the timeout plus 5 second')
        # ---------------------------------------------------------------------------
        sleep(to_int(get_dfu_control_response.dfu_control_timeout)+5)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a short press on the Connect button')
        # ---------------------------------------------------------------------------
        # First key press to turn on the connectivity status LED then second press to switch to CH2
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON, repeat=3)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # ---------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Verify the link is not re-established')
        # ----------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall not be established if device is in deep sleep mode")

        self.testCaseChecked("FUN_00C3_0023")
    # end def test_set_dfu_control_press_connect_button_after_timeout

    @features('SecureDfuControlActionTypeNot0')
    @features('ConnectButton')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.CONNECT_BUTTON,))
    @services('Debugger')
    def test_cancel_dfu_control_press_connect_button(self):
        """
        Validate Connect button keystrokes are processed if we cancel an ongoing dfu control sequence

        cf Patchset#6197 - conn_manager, prevent changing host when DFU is requested
        http://goldenpass.logitech.com:8080/c/ccp_fw/quark/+/6197
        """
        self.generic_set_get_dfu_control()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=0')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=0)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a short press on the Connect button')
        # ---------------------------------------------------------------------------
        # First key press to turn on the connectivity status LED then second press to switch to CH2
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON, repeat=3)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # ---------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Verify the link is not re-established')
        # ----------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall not be established if device is in deep sleep mode")

        self.testCaseChecked("FUN_00C3_0024")
    # end def test_cancel_dfu_control_press_connect_button

    @features('SecureDfuControlActionTypeNot0')
    @features('MultipleEasySwitchButtons')
    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    @services('MultiHost')
    def test_set_dfu_control_easyswitch_buttons_ignored(self):
        """
        Validate Easyswitch buttons keystrokes are ignored if set dfu control timeout is ongoing

        cf Patchset#6197 - conn_manager, prevent changing host when DFU is requested
        http://goldenpass.logitech.com:8080/c/ccp_fw/quark/+/6197
        """
        self.post_requisite_program_mcu_initial_state = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on CH2 & CH3 slots')
        # ---------------------------------------------------------------------------
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

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force back the device in CH1')
        # ---------------------------------------------------------------------------
        # Reconnect with the first receiver
        ReceiverTestUtils.switch_to_receiver(
            self, receiver_port_index=ChannelUtils.get_port_index(test_case=self, channel=self.backup_dut_channel))

        # Change host on Device
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        test_actions_list = [(self.button_stimuli_emulator.change_host, HOST.CH2),
                             (self.button_stimuli_emulator.enter_pairing_mode, HOST.CH2),
                             (self.button_stimuli_emulator.change_host, HOST.CH3),
                             (self.button_stimuli_emulator.enter_pairing_mode, HOST.CH3)]

        for (test_method, param) in test_actions_list:
            # Enable DFU mode immediately
            get_dfu_control_response = self.generic_set_get_dfu_control()

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform a short or long key press on the Connect button')
            # ---------------------------------------------------------------------------
            # First key press to turn on the connectivity status LED
            self.button_stimuli_emulator.change_host()
            # Second press to switch to CH2
            test_method(host_index=param)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the device reset with the requested user actions simultaneously')
            # ---------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(
                test_case=self,
                action_type=get_dfu_control_response.dfu_control_action_type,
                action_data=get_dfu_control_response.dfu_control_action_data)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the device is in Bootloader mode')
            # ---------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                msg="Device not in bootloader")

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
            # ---------------------------------------------------------------------------
            DfuTestUtils.send_dfu_restart_function(test_case=self)
        # end for

        self.testCaseChecked("FUN_00C3_0025")
    # end def test_set_dfu_control_easyswitch_buttons_ignored

    @features('SecureDfuControlActionTypeNot0')
    @features('ConnectButton')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.CONNECT_BUTTON,))
    @services('Debugger')
    def test_set_dfu_control_press_connect_button_ignored(self):
        """
        Validate Connect button keystrokes are ignored if set dfu control timeout is ongoing

        cf Patchset#6197 - conn_manager, prevent changing host when DFU is requested
        http://goldenpass.logitech.com:8080/c/ccp_fw/quark/+/6197
        """
        # Enable DFU mode immediately
        get_dfu_control_response = self.generic_set_get_dfu_control()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a short press on the Connect button')
        # ---------------------------------------------------------------------------
        # First key press to turn on the connectivity status LED then second press to switch to CH2
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON, repeat=3)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the device reset with the requested user actions simultaneously')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(
            test_case=self,
            action_type=get_dfu_control_response.dfu_control_action_type,
            action_data=get_dfu_control_response.dfu_control_action_data)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device is in Bootloader mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
            msg="Device not in bootloader")

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
        # ---------------------------------------------------------------------------
        DfuTestUtils.send_dfu_restart_function(test_case=self)

        self.testCaseChecked("FUN_00C3_0026")
    # end def test_set_dfu_control_press_connect_button_ignored

    @features('SecureDfuControlActionTypeNot0')
    @features('ConnectButton')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.CONNECT_BUTTON,))
    @services('Debugger')
    def test_set_dfu_control_press_connect_button_ignored_just_before_timeout(self):
        """
        Validate Connect button keystrokes are ignored if set dfu control timeout is ongoing

        cf Patchset#6197 - conn_manager, prevent changing host when DFU is requested
        http://goldenpass.logitech.com:8080/c/ccp_fw/quark/+/6197
        """
        delay_start = time()
        # Enable DFU mode immediately
        get_dfu_control_response = self.generic_set_get_dfu_control()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for the duration of the timeout minus 5 second')
        # ---------------------------------------------------------------------------
        # It is mandatory to check that the delay wanted has not already been exceeded before arriving here
        delay_time = time() - delay_start
        self.assertGreater(a=to_int(get_dfu_control_response.dfu_control_timeout) - 5,
                           b=delay_time,
                           msg="The delay to wait has been exceeded before we arrive here")
        sleep(to_int(get_dfu_control_response.dfu_control_timeout) - 5 - delay_time)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a short press on the Connect button')
        # ---------------------------------------------------------------------------
        # First key press to turn on the connectivity status LED then second press to switch to CH2
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON, repeat=3)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the device reset with the requested user '
                                 'actions simultaneously')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(
            test_case=self,
            action_type=get_dfu_control_response.dfu_control_action_type,
            action_data=get_dfu_control_response.dfu_control_action_data)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device is in Bootloader mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
            msg="Device not in bootloader")

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
        # ---------------------------------------------------------------------------
        DfuTestUtils.send_dfu_restart_function(test_case=self)

        self.testCaseChecked("FUN_00C3_0027")
    # end def test_set_dfu_control_press_connect_button_ignored_just_before_timeout
# end class DeviceSecureDfuControlFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
