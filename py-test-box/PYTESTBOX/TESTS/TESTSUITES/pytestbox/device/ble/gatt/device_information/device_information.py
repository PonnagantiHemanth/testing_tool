#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.device_information
:brief: Validate BLE GATT Device Information service test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/01/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattDeviceInformationServiceTestCases(DeviceBaseTestCase):
    """
    BLE OS Gatt Device Information Service Test Cases common class
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_disconnect_device = False
        self.post_requisite_delete_bond = False
        self.post_requisite_reload_nvs = True
        self.reset_channel_before_restart = False
        self.post_requisite_restart_in_main_application = False
        self.current_ble_device = None
        self.ble_context = None
        self.notifications_queues = {}
        self.indications_queues = {}
        self.feature_1807_index = None
        self.feature_1807 = None
        self.feature_0003_index = None
        self.feature_0003 = None
        super().setUp()
        
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get the BLE context here")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
    # end def setUp
    
    def _get_feature_0003_index(self):
        """
        get the feature index for feature 0x0003
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            test_case=self, update_test_case=True)
    # end def _get_feature_0003_index
    
    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.reset_channel_before_restart:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case=self, msg="Reset the channel")
                # ------------------------------------------------------------------------------------------------------
                # Reset the channel because subscription to the entire GATT table occured during the test
                self.current_channel.close()
                self.current_channel.open()

                self.reset_channel_before_restart = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_restart_in_main_application:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Restart in Main Application mode")
                # ------------------------------------------------------------------------------------------------------
                DfuTestUtils.force_target_on_application(test_case=self, check_required=False)
                self.post_requisite_restart_in_main_application = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_disconnect_device:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Disconnect device")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.disconnect_device(test_case=self, ble_context_device=self.current_ble_device)
                self.post_requisite_disconnect_device = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_channel != self.backup_dut_channel:
                ChannelUtils.close_channel(test_case=self)
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_delete_bond:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Delete device bond")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.current_ble_device)
                self.post_requisite_delete_bond = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def prerequisite_feature1807(self):
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1807_index, self.feature_1807, _, _ = ConfigurablePropertiesTestUtils.HIDppHelper.get_parameters(
            test_case=self,
            feature_id=ConfigurableProperties.FEATURE_ID,
            factory=ConfigurablePropertiesFactory)
    # end def prerequisite_feature1807
# end class GattDeviceInformationServiceTestCases


class GattDeviceInformationServiceApplicationTestCases(GattDeviceInformationServiceTestCases):
    """
    BLE Device Information Service Test Cases common class for application mode tests
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        self.current_ble_device = self.current_channel._ble_context_device
        self.post_requisite_disconnect_device = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get the set the used ble context device")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context_device_used = self.current_ble_device
    # end def setUp
# end class GattDeviceInformationServiceApplicationTestCases


class GattDeviceInformationServiceBootloaderTestCases(GattDeviceInformationServiceTestCases):
    """
    BLE Device Information Service Test Cases common class for bootloader mode tests
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """

        # Post requisite flags definition
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Open device in BLE bootloader mode")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=True)
        self.post_requisite_restart_in_main_application = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify device is running in bootloader mode")
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(DfuTestUtils.verify_device_on_fw_type(
            test_case=self, fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER), msg=f"Bootloader not activated")

        self.current_ble_device = self.current_channel.get_ble_context_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set the used ble context device")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context_device_used = self.current_ble_device
    # end def setUp
# end class GattDeviceInformationServiceBootloaderTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
