#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.small_services.small_services
:brief: Validates BLE OS small services of the GATT test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/11/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue
from copy import deepcopy

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.ble.base.bleppserviceutils import BleppServiceUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattSmallServiceTestCase(DeviceBaseTestCase):
    """
    BLE OS Gatt Small Services Test Cases common class
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_backup_nvs = False
        self.post_requisite_disconnect_device = False
        self.post_requisite_delete_bond = False
        self.reset_channel_before_restart = False
        self.post_requisite_restart_in_main_application = False
        self.post_requisite_turn_off_usb_charging_cable = False
        self.feature_0003_index = None
        self.feature_0003 = None
        self.current_ble_device = None
        self.ble_context = None
        self.notifications_queues = {}
        self.indications_queues = {}
        super().setUp()
        self.post_requisite_reload_nvs = True

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
            if self.post_requisite_turn_off_usb_charging_cable:
                # --------------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "exit charge mode")
                # --------------------------------------------------------------------------------------------------------------
                DeviceTestUtils.ChargingHelper.exit_charging_mode(self)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.reset_channel_before_restart:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Reset the channel")
                # ------------------------------------------------------------------------------------------------------
                # Reset the channel to clean-up subscription to the whole GATT table
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
                DfuTestUtils.force_target_on_application(self, check_required=False)

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

        with self.manage_post_requisite():
            if self.post_requisite_backup_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(test_case=self)
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self, channel=self.backup_dut_channel)
                self.post_requisite_backup_nvs = False
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Clean Battery Status messages")
            # ----------------------------------------------------------------------------------------------------------
            self.cleanup_battery_event_from_queue()
        # end with
        super().tearDown()
    # end def tearDown

    def _get_feature_0003_index(self):
        """
        get the feature index for feature 0x0003
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def _get_feature_0003_index

    def _subscribe_to_all(self, gatt_table):
        """
        Subscribe to all the notifications and indications in the given gatt table
        Fill the attributes notifications_queues and indications_queues with in a dictionary indexed by the UUID of the
        given characteristic

        :param gatt_table: the gat table to use
        :type gatt_table: ``list``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Subscribe to all notification and indication on device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset_channel_before_restart = True  # The following subscriptions break the channel for the teardown
        for service in gatt_table:
            for characteristic in service.characteristics:
                self._direct_characteristic_subscribe(characteristic, service)
                # end if
            # end for
        # end for
    # end def _subscribe_to_all

    def _subscribe_characteristic(self, service_uuid, characteristic_uuid, gatt_table=None):
        """
        Subscribe to notification or indications of a specific characteristic on the current ble device

        :param service_uuid: The uuid of the service to use
        :type service_uuid: ``BleUUID``
        :param characteristic_uuid: the uuid of the characteristic to subscribe to
        :type characteristic_uuid: ``BleUUID``
        :param gatt_table: The gatt table to use  - OPTIONAL
        :type gatt_table: ``List`` or ``None``
        """

        if gatt_table is None:
            gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
        # end if
        try:
            service = next(service for service in gatt_table if service.uuid == service_uuid)
            characteristic = next(characteristic for characteristic in service.characteristics if
                                  characteristic.uuid == characteristic_uuid)
        except StopIteration:
            self.fail(msg=f"Service{service_uuid} or characteristic{characteristic_uuid} not found in gatt table")
        # end try
        self._direct_characteristic_subscribe(characteristic, service)
    # end def _subscribe_characteristic

    def _direct_characteristic_subscribe(self, characteristic, service):
        """
        Automatically subscribe to a characteristic notification or indication when declared in its properties

        :param characteristic: The characteristic to subscribe to
        :type characteristic: ``BleCharacteristic``
        :param service: The service containing the characteristic
        :type service: ``BleService``
        """
        if characteristic.properties.notify == 1:
            new_queue = BleProtocolTestUtils.direct_subscribe_notification(test_case=self,
                                                                           ble_context_device=self.ble_context_device_used,
                                                                           characteristic=characteristic)
            self.notifications_queues[(service.uuid, characteristic.uuid)] = new_queue

        # end if
        if characteristic.properties.indicate == 1:
            new_queue = BleProtocolTestUtils.direct_subscribe_indication(test_case=self,
                                                                         ble_context_device=self.ble_context_device_used,
                                                                         characteristic=characteristic)
            self.indications_queues[(service.uuid, characteristic.uuid)] = new_queue
        # end if

    # end def _direct_characteristic_subscribe

    def _check_hidpp_communication_enabled(self, blepp_service, hidpp_characteristic):
        """
        Check that the HID++ communication is enabled

        :param blepp_service: Bluetooth UUID of the ble++ service (application or bootloader mode)
        :type blepp_service: ``BleUuid``
        :param hidpp_characteristic: Bluetooth UUID of the hid++ characteristic (application or bootloader mode)
        :type hidpp_characteristic: ``BleUuid``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write on HID++ feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        get_fw_info_report = self.feature_0003.get_fw_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index,
            entity_index=0)

        blepp_message = BleppServiceUtils.convert_hidpp_to_blepp_message(get_fw_info_report)

        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=blepp_service,
                                                  characteristic_uuid=hidpp_characteristic,
                                                  value=blepp_message)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ notification is received")
        # --------------------------------------------------------------------------------------------------------------
        received = False
        tries = 0
        # repeat the check because another notification can be in the queue on some devices
        while not received and tries < 3:
            try:
                ble_notification = self.notifications_queues[(blepp_service, hidpp_characteristic)].get(
                    timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            except queue.Empty:
                self.fail(msg="No notification received in time")
            except KeyError:
                self.fail(msg="BLE++ service or HID++ characteristic not found in the GATT table")
            # end try

            feature_index = BleppServiceUtils.extract_feature_index_from_blepp_notification(ble_notification)
            if feature_index == self.feature_0003_index:
                received = True
            else:
                tries += 1
            # end if
        # end while
        self.assertTrue(received, msg="No notification from HID++ feature 0x0003 received")
    # end def _check_hidpp_communication_enabled

    def _check_gatt_table_attribute_presence(self, gatt_table):
        """
        Check the presence of some small services attributes in the gatt table

        :param gatt_table: the GATT table to check
        :type gatt_table: ``list``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Name and Appearance are in GAP service")
        # ---------------------------------------------------------------------------
        BleProtocolTestUtils.check_presence_attribute(
            test_case=self,
            gatt_table=gatt_table,
            service_uuid=BleUuid(BleUuidStandardService.GENERIC_ACCESS),
            characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME),
            service_name="GAP",
            characteristic_name="Device Name")
        BleProtocolTestUtils.check_presence_attribute(
            test_case=self,
            gatt_table=gatt_table,
            service_uuid=BleUuid(BleUuidStandardService.GENERIC_ACCESS),
            characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.APPEARANCE),
            service_name="GAP",
            characteristic_name="Appearance")
        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Battery Level is in BAS service")
        # ---------------------------------------------------------------------------
        BleProtocolTestUtils.check_presence_attribute(
            test_case=self,
            gatt_table=gatt_table, service_uuid=BleUuid(BleUuidStandardService.BATTERY_SERVICE),
            characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL),
            service_name="BAS",
            characteristic_name="Battery Level")
    # end def _check_gatt_table_attribute_presence
# end class GattSmallServiceTestCase


class GattSmallServiceApplicationTestCase(GattSmallServiceTestCase):
    """
    BLE OS Gatt Small Service Test Cases application class for application mode tests
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

# end class GattSmallServiceApplicationTestCase


class GattSmallServiceBootloaderTestCase(GattSmallServiceTestCase):
    """
    BLE OS Gatt Small Service Test Cases bootloader class for bootloader mode tests
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
        LogHelper.log_prerequisite(self, "Verify device is running in bootloader mode")
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(DfuTestUtils.verify_device_on_fw_type(
                test_case=self, fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER), msg=f"Bootloader not activated")

        self.current_ble_device = self.current_channel.get_ble_context_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Backup the ble context device")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context_device_used = self.current_ble_device

    # end def setUp

# end class GattSmallServiceBootloaderTestCase


class GattSmallServiceAdvertisingTestCases(DeviceBaseTestCase):
    """
    BLE OS Gatt Small Service Test Cases common class for tests starting during the advertisement procedure
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_backup_nvs = False
        self.current_ble_device = None

        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        self.memory_manager.backup_nvs_parser = deepcopy(self.memory_manager.nvs_parser)

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disconnect by entering pairing mode")
        # ------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        self.post_requisite_backup_nvs = True

        DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=self)

    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_backup_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(test_case=self)
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self,
                                                                     channel=self.backup_dut_channel)
                self.post_requisite_backup_nvs = False
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_ble_device is not None:
                # ------------------------------------------------------
                LogHelper.log_info(self, "Delete bond from direct BLE device")
                # ------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.current_ble_device)
            # end if
        # end with

        with self.manage_post_requisite():
            ChannelUtils.clean_messages(test_case=self,
                                        queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with

        super().tearDown()
    # end def tearDown
# end class GattSmallServiceAdvertisingTestCases
