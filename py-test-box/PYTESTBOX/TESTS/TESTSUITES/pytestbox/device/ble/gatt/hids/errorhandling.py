#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.hids.errorhandling
:brief: Validate Gatt HIDS Error handling test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/03/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from copy import deepcopy

from pychannel import blechannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.hexlist import HexList
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


class PropertyToCheck:
    """
    set of flag indicating if a property should be checked for unauthorized access.
    """
    def __init__(self, read=False, write=False, write_wo_resp=False, notify=False, indicate=False):
        """
        :param read: Flag indicating if the read property need to be checked for unauthorized access
        :type read: ``bool``
        :param write: Flag indicating if the write property need to be checked for unauthorized access
        :type write: ``bool``
        :param write_wo_resp: Flag indicating if the write_wo_resp property need to be checked for unauthorized access
        :type write_wo_resp: ``bool``
        :param notify: Flag indicating if the notify property need to be checked for unauthorized access
        :type notify: ``bool``
        :param indicate: Flag indicating if the indicate property need to be checked for unauthorized access
        :type indicate: ``bool``
        """
        self.read = read
        self.write = write
        self.write_wo_resp = write_wo_resp
        self.notify = notify
        self.indicate = indicate
    # end def __init__
# end class PropertyToCheck


CHARACTERISTIC_TO_CHECK = {
    BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_INPUT_REPORT):
        PropertyToCheck(read=True, notify=True),
    BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_OUTPUT_REPORT):
        PropertyToCheck(read=True, write=True, write_wo_resp=True),
    BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_MOUSE_INPUT_REPORT):
        PropertyToCheck(read=True, notify=True),
    BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_INFORMATION):
        PropertyToCheck(read=True),
    BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT_MAP):
        PropertyToCheck(read=True),
    BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_CONTROL_POINT):
        PropertyToCheck(write_wo_resp=True),
    BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT):
        PropertyToCheck(read=True),
    BleUuid(BleUuidStandardCharacteristicAndObjectType.PROTOCOL_MODE):
        PropertyToCheck(read=True, write_wo_resp=True),
}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattHIDSServiceErrorHandling(DeviceBaseTestCase):
    """
    BLE OS Gatt Human Interface Device Service Error Handling Test Cases Common class
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
                DfuTestUtils.force_target_on_application(self, check_required=False, hard_force=True)

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

    def _check_security_level(self):
        """
        common testing method checking the security level of the characteristics in the HIDS
        """
        service_uuid = BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)
        service = self.ble_context.get_service(ble_context_device=self.ble_context_device_used, uuid=service_uuid)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop on characteristics")
        # --------------------------------------------------------------------------------------------------------------
        for characteristic in service.characteristics:
            characteristic_uuid = characteristic.uuid
            param = CHARACTERISTIC_TO_CHECK[characteristic_uuid]
            if param.read:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Try reading the characteristic {characteristic_uuid}")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.check_read_permission(self, service_uuid, characteristic_uuid)
            # end if
            if param.write:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Try writing the characteristic {characteristic_uuid}")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.check_write_permission(self, service_uuid, characteristic_uuid, HexList(0x0))
            # end if
            if param.write_wo_resp:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Try writing without response the characteristic {characteristic_uuid}")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.check_write_wo_resp_permission(self, service_uuid, characteristic_uuid,
                                                                    HexList(0x0))
            # end if
            if param.notify:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Try reading the characteristic {characteristic_uuid}")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.check_notification_permission(self, service_uuid, characteristic_uuid)
            # end if
            if param.indicate:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Try reading the characteristic {characteristic_uuid}")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.check_indication_permission(self, service_uuid, characteristic_uuid)
            # end if
        # end for
    # end def _check_security_level
# end class GattHIDSServiceErrorHandling


class GattHIDSApplicationErrorHandlingTestCase(GattHIDSServiceErrorHandling):
    """
    BLE OS Gatt Human Interface Device Service Error Handling Test Cases application class
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
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.current_ble_device)

        self.ble_context = BleProtocolTestUtils.get_ble_context(self)
        self.ble_context_device_used = self.current_ble_device
    # end def setUp

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_hids_security_level_too_low(self):
        """
        Verify that operations on HIDS application service's characteristics requiring authentication
        fail when no authentication is present
        """
        self._check_security_level()
        self.testCaseChecked("ERR_BLE_GATT_HIDS_0001", _AUTHOR)
    # end def test_hids_security_level_too_low
# end class GattHIDSApplicationErrorHandlingTestCase


@features.class_decorator("BootloaderBLESupport")
class GattHIDSBootloaderErrorHandlingTestCase(GattHIDSServiceErrorHandling):
    """
    BLE OS Gatt Human Interface Device Service Error Handling Test Cases bootloader class
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
        ChannelUtils.wait_usb_ble_channel_connection_state(
            test_case=self, channel=self.current_channel, connection_state=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Connect to the device without the authentication")
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = self.current_channel.get_ble_context_device()
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.current_ble_device)

        self.ble_context = BleProtocolTestUtils.get_ble_context(self)
        self.ble_context_device_used = self.current_ble_device
    # end def setUp

    @features('BLEProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_hids_security_level_too_low(self):
        """
        Verify that operations on HIDS application service's characteristics requiring authentication
        fail when no authentication is present
        """
        self._check_security_level()
        self.testCaseChecked("ERR_BLE_GATT_HIDS_0002", _AUTHOR)
    # end def test_hids_security_level_too_low
# end class GattHIDSBootloaderErrorHandlingTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
