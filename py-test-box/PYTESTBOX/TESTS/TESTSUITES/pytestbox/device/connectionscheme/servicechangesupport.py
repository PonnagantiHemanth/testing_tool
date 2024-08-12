#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.servicechangesupport
:brief: Validate Service Change Support flowchart
https://app.lucidchart.com/documents/edit/4ec2b55b-188c-4473-b6ec-2cb9ed9513ee/eyl1Z~CmRrKD#?folder_id=home&browser=list
:author: Christophe Roquebert
:date: 2020/10/22
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.core import TYPE_SUCCESS
from pyharness.extensions import level
from pyharness.selector import features, services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControl
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlFactory
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ServiceChangeSupportTestCase(BaseTestCase):
    """
    BLE Pro Service Change Support TestCases
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_force_target_on_application = False
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Backup initial NVS')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x00C3)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_00c3_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SecureDfuControl.FEATURE_ID)

        # Get the feature under test
        self.secure_dfu_control_feature = SecureDfuControlFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.status != TYPE_SUCCESS:
                self.post_requisite_force_target_on_application = True
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reload NVS to its initial state')
                # ------------------------------------------------------------------------------------------------------
                DfuControlTestUtils.load_nvs(test_case=self, backup=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'In case of test failure, the device shall be forced back in Main '
                                                   'Application mode')
                # ------------------------------------------------------------------------------------------------------
                DfuTestUtils.force_target_on_application(test_case=self)
                self.post_requisite_force_target_on_application = False
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_force_target_on_application:
                DfuTestUtils.force_target_on_application(test_case=self)
                self.post_requisite_force_target_on_application = False
            # end if
        # end with
        with self.manage_post_requisite():
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with
        super().tearDown()
    # end def tearDown

    @features('BLEServiceChangeSupport')
    @features('SecureDfuControlAllActionTypes')
    @level('Robustness')
    @services('Debugger')
    def test_device_reset_in_bootloader_after_service_change_start(self):
        """
        Verify the device reconnects on application after a reset occurs during a service change exchange when
        entering in bootloader mode

        Test the persistent re-enumeration flag on the receiver side:
        https://jira.logitech.io/browse/BPRO-284
        """
        # 5ms, 50ms, 100ms and 130ms delays
        delay_list = [5, 50, 100, 130, ]

        for variable_delay in delay_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
            set_dfu_control = self.secure_dfu_control_feature.set_dfu_control_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_00c3_index, 
                enable_dfu=1)
            ChannelUtils.send(
                test_case=self, report=set_dfu_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.secure_dfu_control_feature.set_dfu_control_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU getDfuControl')
            # ----------------------------------------------------------------------------------------------------------
            get_dfu_control = self.secure_dfu_control_feature.get_dfu_control_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_00c3_index)
            get_dfu_control_response = ChannelUtils.send(
                test_case=self, report=get_dfu_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.secure_dfu_control_feature.get_dfu_control_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the device reset with the requested user actions simultaneously')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(
                test_case=self,
                action_type=get_dfu_control_response.dfu_control_action_type,
                action_data=get_dfu_control_response.dfu_control_action_data,
                check_device_reconnection=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to disconnect')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, timeout=4,
                class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should receive a device connection link not established first")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to reconnect')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should then receive a device connection link established")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the service change Start notification')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should finally receive a device connection link not established")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Add a variable delay to cover the service change period')
            # ----------------------------------------------------------------------------------------------------------
            sleep(variable_delay/1000)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Power off / on the device')
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.debugger.stop()
            sleep(3)
            self.memory_manager.debugger.reset(soft_reset=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify the device is able to reconnect')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
                timeout=DevicePairingTestUtils.RECONNECTION_TIMEOUT)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should finally receive a device connection link established")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the device is in Main Application mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                            msg="Device not in application")

            self.button_stimuli_emulator.release_all()
        # end for

        self.testCaseChecked("FNT_BLE_SRV_CHG_0001")
    # end def test_device_reset_in_bootloader_after_service_change_start

    @features('BLEServiceChangeSupport')
    @features('SecureDfuControlAllActionTypes')
    @level('Robustness')
    @services('Debugger')
    def test_device_reset_in_application_after_service_change_start(self):
        """
        Verify the device reconnects on application after a reset occurs during a service change exchange when
        switching back to application mode

        Test the persistent re-enumeration flag on the receiver side:
        https://jira.logitech.io/browse/BPRO-284
        """
        # 5ms, 50ms, 100ms and 200ms delays
        delay_list = [5, 50, 100, 200, ]

        for variable_delay in delay_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
            set_dfu_control = self.secure_dfu_control_feature.set_dfu_control_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_00c3_index, 
                enable_dfu=1)
            ChannelUtils.send(
                test_case=self, report=set_dfu_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.secure_dfu_control_feature.set_dfu_control_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU getDfuControl')
            # ----------------------------------------------------------------------------------------------------------
            get_dfu_control = self.secure_dfu_control_feature.get_dfu_control_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_00c3_index)
            get_dfu_control_response = ChannelUtils.send(
                test_case=self, report=get_dfu_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.secure_dfu_control_feature.get_dfu_control_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the device reset with the requested user actions simultaneously')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(
                test_case=self,
                action_type=get_dfu_control_response.dfu_control_action_type,
                action_data=get_dfu_control_response.dfu_control_action_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the device stays in bootloader mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                            msg="Device not in bootloader")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
            # ----------------------------------------------------------------------------------------------------------
            DfuTestUtils.send_dfu_restart_function(test_case=self, check_device_reconnection=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to disconnect')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, timeout=4,
                class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should receive a device connection link not established first")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to reconnect')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should then receive a device connection link established")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the DeviceConnection notifying the start of the service change')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should finally receive a device connection link not established")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Add a variable delay to cover the service change period')
            # ----------------------------------------------------------------------------------------------------------
            sleep(variable_delay/1000)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Power off / on the device')
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.debugger.stop()
            sleep(3)
            ChannelUtils.clean_messages(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)
            self.memory_manager.debugger.reset(soft_reset=False)

            # Perform a user action to force the device to reconnect
            self.button_stimuli_emulator.user_action()

            # Wait for the Wireless Device Status Broadcast event returned by the device
            CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
                test_case=self, timeout=DevicePairingTestUtils.RECONNECTION_TIMEOUT+1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify the device is able to reconnect')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), timeout=0,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                             obtained=to_int(device_info.device_info_link_status),
                             msg="We should finally receive a device connection link established")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the device is in Main Application mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                            msg="Device not in application")
        # end for

        self.testCaseChecked("FNT_BLE_SRV_CHG_0001")
    # end def test_device_reset_in_application_after_service_change_start

# end class ServiceChangeSupportTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
