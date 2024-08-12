#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.hids.hids
:brief: Validate BLE GATT human interface device service test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/03/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import Enum

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
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
class ReportType(Enum):
    """
    Type of reports, as used in report descriptors
    """
    INPUT_REPORT = 1
    OUTPUT_REPORT = 2
    FEATURE_REPORT = 3
# end class ReportType


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class GattHIDSTestCases(DeviceBaseTestCase):
    """
    BLE OS Gatt HIDS Test Cases common class
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
        self.gatt_table = None
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get the BLE context here")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
    # end def setUp

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

    def _prerequisite_feature1807(self):
        """
        prerequisite for usage of the HID++ feature 1807, enables manufacturing features and get the index
        """
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
    # end def _prerequisite_feature1807

    def _prerequisite_feature_0003_index(self):
        """
        get the feature index for feature 0x0003
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def _prerequisite_feature_0003_index

    def _prerequisite_gatt_table(self):
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get the whole gatt table")
        # --------------------------------------------------------------------------------------------------------------
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.current_ble_device)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Gatt table read = {BleProtocolTestUtils.gatt_table_to_string(self.gatt_table)}")
        # --------------------------------------------------------------------------------------------------------------
    # end def _prerequisite_gatt_table

    def _prerequisite_subscribe_to_input_report(self):
        """
        subscribe to all input reports notification, their keys for their queue in
        notification_queue dict are theirs the report reference

        :return: list of keys added by this subscription process
        :rtype: ``list``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Subscribe to all input reports")
        # --------------------------------------------------------------------------------------------------------------
        hids = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                        BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE))
        reports = [char for char in hids.characteristics if
                   char.uuid == BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT)]

        keys = []
        for report in reports:
            report_reference = BleProtocolTestUtils.read_descriptor(
                self, self.current_ble_device, report, BleUuid(BleUuidStandardDescriptor.REPORT_REFERENCE)).data

            if report_reference[1] == ReportType.INPUT_REPORT.value:
                new_queue = BleProtocolTestUtils.direct_subscribe_notification(test_case=self,
                                                                               ble_context_device=self.current_ble_device,
                                                                               characteristic=report)
                ref = report_reference.toLong()
                self.notifications_queues[ref] = new_queue
                keys.append(ref)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Subscribed to  report with reference {ref:04x}")
                # ------------------------------------------------------------------------------------------------------
            # end if
        # end for
        return keys
    # end def _prerequisite_subscribe_to_input_report

    def _prerequisite_subscribe_to_boot_mouse_input_report(self):
        """
        subscribe to the boot mouse input report notification, the keys for the queue in
        is the Uuid service, characteristic pair
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Subscribe to boot mouse input report")
        # --------------------------------------------------------------------------------------------------------------
        char_uid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_MOUSE_INPUT_REPORT)
        hids_uid = BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)
        try:
            service = next(service for service in self.gatt_table if service.uuid == hids_uid)
            characteristic = next(characteristic for characteristic
                                  in service.characteristics if characteristic.uuid == char_uid)
        except StopIteration:
            self.fail(msg=f"Service HIDS or characteristic Boot Mouse Input Report not found in gatt table")
        # end try
        new_queue = BleProtocolTestUtils.direct_subscribe_notification(test_case=self,
                                                                       ble_context_device=self.ble_context_device_used,
                                                                       characteristic=characteristic)
        self.notifications_queues[(hids_uid, char_uid)] = new_queue
    # end def _prerequisite_subscribe_to_boot_mouse_input_report

    def _prerequisite_subscribe_to_boot_keyboard_input_report(self):
        """
        subscribe to the keyboard mouse input report notification, the keys for the queue in
        is the Uuid service, characteristic pair
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Subscribe to boot keyboard input report")
        # --------------------------------------------------------------------------------------------------------------
        char_uid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_INPUT_REPORT)
        hids_uid = BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)
        try:
            service = next(service for service in self.gatt_table if service.uuid == hids_uid)
            characteristic = next(characteristic for characteristic
                                  in service.characteristics if characteristic.uuid == char_uid)
        except StopIteration:
            self.fail(msg=f"Service HIDS or characteristic Boot Keyboard Input Report not found in gatt table")
        # end try
        new_queue = BleProtocolTestUtils.direct_subscribe_notification(test_case=self,
                                                                       ble_context_device=self.ble_context_device_used,
                                                                       characteristic=characteristic)
        self.notifications_queues[(hids_uid, char_uid)] = new_queue
    # end def _prerequisite_subscribe_to_boot_keyboard_input_report

    def _empty_notification_queues(self):
        """
        Empty the test's notification queue
        """
        for queue in self.notifications_queues.values():
            while not queue.empty():
                _ = queue.get()
            # end while
        # end for
    # end def _empty_notification_queues

    def _get_report(self, report_reference):
        """
        Get a report characteristic from the gatt table based on the report reference
        :param report_reference: the report reference
        :type report_reference: ``HexList``
        :return: the report
        :rtype: ``BleCharacteristic``
        """
        hids = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                        BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE))
        reports = [char for char in hids.characteristics if
                   char.uuid == BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT)]
        for report in reports:
            report_reference_read = BleProtocolTestUtils.read_descriptor(
                self, self.current_ble_device, report, BleUuid(BleUuidStandardDescriptor.REPORT_REFERENCE)).data
            if report_reference_read == report_reference:
                return report
            # end if
        # end for
    # end def _get_report
# end class GattHIDSTestCases


class GattHIDSApplicationTestCases(GattHIDSTestCases):
    """
    BLE HIDS Test Cases common class for application mode tests
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
# end class GattHIDSApplicationTestCases


class GattHIDSBootloaderTestCases(GattHIDSTestCases):
    """
    BLE HIDS Test Cases common class for bootloader mode tests
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
# end class GattHIDSBootloaderTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
