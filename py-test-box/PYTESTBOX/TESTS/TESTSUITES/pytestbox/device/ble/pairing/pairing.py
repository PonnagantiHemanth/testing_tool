#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.pairing.pairing
:brief: Validate BLE pairing test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/10/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PairingTestCases(DeviceBaseTestCase):
    """
    BLE pairing Test Cases class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.ble_context = None
        self.current_device = None
        self.ble_channel = None
        self.post_requisite_reload_nvs = False
        self.post_requisite_turn_off_usb_charging_cable = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter pairing mode")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
        ChannelUtils.close_channel(test_case=self)
        DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Scan for current device")
        # --------------------------------------------------------------------------------------------------------------
        self.current_device = BleProtocolTestUtils.scan_for_current_device(
            test_case=self, scan_timeout=2, send_scan_request=True)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.ble_channel is not None:
                if self.ble_channel.is_open:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Close BLE channel")
                    # --------------------------------------------------------------------------------------------------
                    self.ble_channel.close()
                # end if
                self.ble_channel = None
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_device is not None and self.current_device.connected:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Disconnect device")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.disconnect_device(test_case=self, ble_context_device=self.current_device)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_device is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Delete device bond")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.current_device)
                self.current_device = None
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_turn_off_usb_charging_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Stop device charging")
                # ------------------------------------------------------------------------------------------------------
                if self.power_supply_emulator is not None:
                    self.power_supply_emulator.recharge(enable=False)
                # end if
                self.device.turn_off_usb_charging_cable()
                self.post_requisite_turn_off_usb_charging_cable = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload device initial NVS")
                # ------------------------------------------------------------------------------------------------------
                self.memory_manager.load_nvs(backup=True)
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
                # There is an extra event that happen before the end of the method
                # wait_for_channel_device_to_be_connected, so we need to wait for both events
                for _ in range(2):
                    ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                          class_type=WirelessDeviceStatusBroadcastEvent, timeout=1,
                                          check_first_message=False, allow_no_message=True)
                # end for
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class PairingTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
