#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.small_services.errorhandling
:brief: Validate Gatt small services Error handling test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from copy import deepcopy
from unittest import expectedFailure

from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.logiconstants import LogitechVendorUuid
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_endian_list
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattSmallServiceErrorHandling(DeviceBaseTestCase):
    """
    BLE OS Gatt Small Service Error Handling Test Cases Common class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_backup_nvs = False
        self.post_requisite_restart_in_main_application = False
        self.current_ble_device = None
        self.ble_context = None
        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        self.memory_manager.backup_nvs_parser = deepcopy(self.memory_manager.nvs_parser)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
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
            if self.current_ble_device is not None:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Delete bond from direct BLE device")
                # ------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.current_ble_device)
            # end if
        # end with

        with self.manage_post_requisite():
            LogHelper.log_post_requisite(self, "Clean WirelessDeviceStatusBroadcastEvent messages")
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with

        super().tearDown()
    # end def tearDown

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_gap_security_level_too_low(self):
        """
        Verify that operations on gap's characteristics requiring authentication fail when no authentication is present
        """
        value = HexList.fromString("Hello")
        service_uuid = BleUuid(BleUuidStandardService.GENERIC_ACCESS)
        characteristic_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try writing on device name characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_write_permission(self, service_uuid, characteristic_uuid, value)

        self.testCaseChecked("ERR_BLE_GATT_SSRV_0001", _AUTHOR)
    # end def test_gap_security_level_too_low

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    @expectedFailure  # https://jira.logitech.io/browse/BT-460
    def test_gatt_security_level_too_low(self):
        """
        Verify that operations on gatt's characteristics requiring authentication fail when no authentication is present
        Note expected failure due to issue https://jira.logitech.io/browse/BT-460
        """
        service_uuid = BleUuid(BleUuidStandardService.GENERIC_ATTRIBUTE)
        characteristic_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.SERVICE_CHANGED)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try subscribing to service changed characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_indication_permission(self, service_uuid, characteristic_uuid)

        self.testCaseChecked("ERR_BLE_GATT_SSRV_0002", _AUTHOR)
    # end def test_gatt_security_level_too_low
# end class GattSmallServiceErrorHandling


class GattSmallServicesApplicationErrorHandlingTestCase(GattSmallServiceErrorHandling):
    """
    BLE OS Gatt Small Service Error Handling Test Cases application class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disconnect by entering pairing mode")
        # ------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        self.post_requisite_backup_nvs = True

        DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Connect to the device without the authentication")
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = BleProtocolTestUtils.scan_for_current_device(self,
                                                                               scan_timeout=2,
                                                                               send_scan_request=True)
        self.ble_context = BleProtocolTestUtils.get_ble_context(self)
        self.ble_context_device_used = self.current_ble_device
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.ble_context_device_used)
    # end def setUp

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_bas_security_level_too_low(self):
        """
        Verify that operations on bas characteristics requiring authentication fail when no authentication is done
        """
        service_uuid = BleUuid(BleUuidStandardService.BATTERY_SERVICE)
        characteristic_battery_level_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL)
        characteristic_battery_level_status_uuid = \
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL_STATUS)
        characteristic_battery_information_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_INFORMATION)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try reading the battery level characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_read_permission(self, service_uuid, characteristic_battery_level_uuid)
        
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try subscribing to the battery level characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_notification_permission(self, service_uuid, characteristic_battery_level_uuid)

        if self.hasFeature("BAS1.1"):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Try reading the battery level status characteristic")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.check_read_permission(self, service_uuid, characteristic_battery_level_status_uuid)
            
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Try subscribing to the battery level status characteristic")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.check_notification_permission(self, service_uuid,
                                                               characteristic_battery_level_status_uuid)
                                                               
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Try reading the battery information characteristic")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.check_read_permission(self, service_uuid, characteristic_battery_information_uuid)
            
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Try subscribing to the battery information characteristic")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.check_indication_permission(self, service_uuid,
                                                               characteristic_battery_information_uuid)
        # end if
        self.testCaseChecked("ERR_BLE_GATT_SSRV_0003", _AUTHOR)

    # end def test_bas_security_level_too_low

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_security_level_too_low(self):
        """
        Verify that operations on ble++ application service's characteristics requiring authentication
        fail when no authentication is present
        """
        service_uuid = BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_SERVICE)
        characteristic_uuid = BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_CHARACTERISTIC)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try reading the hid++ characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_read_permission(self, service_uuid, characteristic_uuid)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try writing on the hid++ characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_write_permission(self, service_uuid, characteristic_uuid,
                                                    HexList(to_endian_list(0, byte_count=18)))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try subscribing to the hid++ characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_notification_permission(self, service_uuid, characteristic_uuid)

        self.testCaseChecked("ERR_BLE_GATT_SSRV_0004", _AUTHOR)
    # end def test_blepp_security_level_too_low
# end class GattSmallServicesApplicationErrorHandlingTestCase


@features.class_decorator("BootloaderBLESupport")
class GattSmallServicesBootloaderErrorHandlingTestCase(GattSmallServiceErrorHandling):
    """
    BLE OS Gatt Small Service Error Handling Test Cases bootloader class
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter bootloader mode, without automatic reconnection")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restart_in_main_application = True
        self.post_requisite_backup_nvs = True

        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=False)
        self.debugger.stop()
        ChannelUtils.wait_usb_ble_channel_connection_state(
            test_case=self, channel=self.current_channel, connection_state=False)
        self.debugger.run()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Connect to the device without the authentication")
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = self.current_channel.get_ble_context_device()
        self.ble_context = BleProtocolTestUtils.get_ble_context(self)
        self.ble_context_device_used = self.current_ble_device
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.ble_context_device_used)
    # end def setUp

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_bas_security_level_too_low(self):
        """
        Verify that operations on bas characteristics requiring authentication fail when no authentication is done
        """
        service_uuid = BleUuid(BleUuidStandardService.BATTERY_SERVICE)
        characteristic_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Try reading the battery lever characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.check_read_permission(self, service_uuid, characteristic_uuid)

        if self.f.PRODUCT.PROTOCOLS.BLE.F_BAS_Version is None:
            # before versioning of BAS, battery was able to notify in bootloader
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Try subscribing to the battery lever characteristic")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.check_notification_permission(self, service_uuid, characteristic_uuid)
        # end if
        self.testCaseChecked("ERR_BLE_GATT_SSRV_0003", _AUTHOR)
    # end def test_bas_security_level_too_low

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_security_level_too_low(self):
        """
        Verify that operations on ble++ bootloader service's characteristics requiring authentication 
        fail when no authentication is present
        """
        service_uuid = BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BOOTLOADER_SERVICE)
        characteristic_uuid = BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BOOTLOADER_CHARACTERISTIC)
        BleProtocolTestUtils.check_read_permission(self, service_uuid, characteristic_uuid)
        BleProtocolTestUtils.check_write_permission(self, service_uuid, characteristic_uuid,
                                                    HexList(to_endian_list(0, byte_count=18)))
        BleProtocolTestUtils.check_notification_permission(self, service_uuid, characteristic_uuid)

        self.testCaseChecked("ERR_BLE_GATT_SSRV_0005", _AUTHOR)
    # end def test_blepp_security_level_too_low
# end class GattSmallServicesBootloaderErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
