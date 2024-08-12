#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.osdetection
:brief: Validates BLE OS detection test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/07/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from copy import deepcopy
from time import sleep

from pyharness.extensions import WarningLevel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.multiplatformutils import MultiPlatformTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
# small delay before reading os detection, measured as smallest working on all reference setups, may need adjusting
OS_DETECT_DELAY = 0.8

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class OsDetectionTestCases(DeviceBaseTestCase):
    """
    BLE OS detection Test Cases common class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_backup_nvs = False
        self.current_ble_device = None
        self.associated_channels = dict() # A dictionary of associated channel for specified ble devices
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
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self, channel=self.backup_dut_channel)
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
            for channel in self.associated_channels:
                if channel is not self.current_channel and channel.open:
                    # ------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Close other associated channel")
                    # ------------------------------------------------------
                    channel.close()
                # end if
            # end for
        # end with

        with self.manage_post_requisite():
            # ------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reset host GATT table")
            # ------------------------------------------------------
            BleProtocolTestUtils.get_ble_context(test_case=self).reset_central_gatt_table()
        # end with

        with self.manage_post_requisite():
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with

        super().tearDown()
    # end def tearDown

    def simple_os_detection(self, os_wanted):
        """
        Verify the OS detected in NVS is the wanted one when the host present the minimum requirement in its GATT table.

        :param os_wanted: OS to emulate to check it on the device after detection
        :type os_wanted: ``BleNvsChunks.OsDetectedType``
        """
        BleProtocolTestUtils.change_host_os_emulation(test_case=self, os_emulation_type=os_wanted)

        self._scan_connect_encrypt_and_read_detected_os(os_wanted)
    # end def simple_os_detection

    def _reset_os_detection_test(self):
        """
        Reset the test to a state where a new os detection can be run, call this when a testcase repeats multiple tests
        """
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Readies the device to a new os detection test")
        # ----------------------------------------------------------------------------------------------------------
        if self.current_ble_device is not None:
            BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.current_ble_device)
        # end if

        if self.f.PRODUCT.F_IsGaming:
            # Use connection buttons in all cases for gaming device as we are already in BLE mode when reaching
            # this point repeating tests.
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=self, msg="Gaming device: Enter BLE pairing mode with buttons")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.F_IsMice:
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON)
            else:
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.BLE_CONNECTION,
                                                       duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
            # end if
            self.memory_manager.read_nvs(backup=False) # read the nvs to get the up-to-date advertising address
        else:
            BleProtocolTestUtils.enter_pairing_mode_ble(self)
        # end if
    # end def _reset_os_detection_test

    def _scan_connect_encrypt_and_read_detected_os(self, os_wanted):
        """
        Scan for the device, connect and encrypt the communication device then read the detected OS

        :param os_wanted: OS to emulate to check it on the device after detection
        :type os_wanted: ``BleNvsChunks.OsDetectedType``
        """
        self._scan_connect_and_encrypt()
        # Add a small delay to let the device perform OS detection
        sleep(OS_DETECT_DELAY)

        self.read_os_detection(os_wanted)
    # end def _scan_connect_encrypt_and_read_detected_os

    def _scan_connect_and_encrypt(self):
        """
        Scann for the device, connect to it and encrypt communication
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text='Scan, connect and encrypt')
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = BleProtocolTestUtils.scan_for_current_device(
            test_case=self, scan_timeout=5, send_scan_request=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg=f"Found device: {self.current_ble_device}")
        # --------------------------------------------------------------------------------------------------------------
        self._connect_and_encrypt()
    # end def _scan_connect_and_encrypt

    def _connect_and_encrypt(self, open_channel=False):
        """
        connect to the device and encrypt communication (with bonding if necessary)

        :param open_channel: Flag indicating if a channel must be opened
        :type open_channel: ``bool``
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg='Connect and bond/encrypt to the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        # connection is done with log_gatt_table=False because some os detection test using
        # this method repeat connection, this allows more readable test logs, device gatt table is of lesser importance
        # for this testsuite.
        if self.hasFeature("Feature4531") or open_channel:
            # open a channel to enable the feature 0x4531 check during the os detection read step.
            if self.current_ble_device not in self.associated_channels.keys():
                # new device, create a new channel for it
                self.current_channel = BleProtocolTestUtils.create_new_ble_channel(
                    test_case=self, ble_context_device=self.current_ble_device, log_gatt_table=False)
                self.associated_channels[self.current_ble_device] = self.current_channel
            else:
                channel = self.associated_channels[self.current_ble_device]
                channel.open()
                if self.current_channel is not channel:
                    self.current_channel = channel
                # end if
            # end if
        else:
            BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.current_ble_device,
                                                         log_gatt_table=False)
        # end if
    # end def _connect_and_encrypt

    def read_os_detection(self, os_wanted):
        """
        Read the detected OS

        :param os_wanted: OS to emulate to check it on the device after detection
        :type os_wanted: ``BleNvsChunks.OsDetectedType``
        """
        self.memory_manager.read_nvs()
        connect_id_chunk = self.memory_manager.get_active_chunk_by_name('NVS_CONNECT_ID')
        host_index = to_int(connect_id_chunk.data.host_index)
        # Extract the latest BLE pairing chunk
        device_chunk = self.memory_manager.get_active_chunk_by_name(f'NVS_BLE_BOND_ID_{host_index}')
        # Check the OS detected byte is matching
        self.assertEqual(
            obtained=BleNvsChunks.OsDetectedType(to_int(device_chunk.os_detected_type)),
            expected=os_wanted,
            msg="OS detected type from NVS BLE Bond Id chunk is not correct")

        if self.hasFeature("Feature4531"):
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)
            response = MultiPlatformTestUtils.HIDppHelper.get_platform_descriptor(
                test_case=self, platform_descriptor_index=response.platform_index)

            os_detection = response.os_mask

            min_expected_mask = response.get_os_mask_cls()()
            if os_wanted == BleNvsChunks.OsDetectedType.IOS:
                min_expected_mask.ios = True
            elif os_wanted == BleNvsChunks.OsDetectedType.OSX:
                min_expected_mask.mac_os = True
            elif os_wanted == BleNvsChunks.OsDetectedType.CHROME:
                min_expected_mask.chrome = True
            elif os_wanted in [BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO,
                               BleNvsChunks.OsDetectedType.UNDETERMINED]:
                min_expected_mask.windows = True
            elif os_wanted == BleNvsChunks.OsDetectedType.ANDROID:
                min_expected_mask.android = True
            elif os_wanted == BleNvsChunks.OsDetectedType.LINUX:
                min_expected_mask.linux = True
            else:
                self.fail("No support parameter for os wanted in test script")
            # end if

            device_masks = []
            for mask in self.f.PRODUCT.FEATURES.KEYBOARD.MULTI_PLATFORM.F_OsMask:
                mask_hex = HexList(int(mask))
                mask_hex.addPadding(2, fromLeft=False)
                mask_bit_field = response.get_os_mask_cls().fromHexList(mask_hex)
                device_masks.append(mask_bit_field)
            # end for

            corresponding_masks = []
            for mask in device_masks:
                if HexList(mask) & HexList(min_expected_mask) != HexList("0000"):
                    # ----------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, f"Compatible OsMask {mask}")
                    # ----------------------------------------------------------------------------------------------
                    corresponding_masks.append(mask)
                # end if
            # end for

            if len(corresponding_masks) == 0:
                expected_mask = device_masks[0]  # if no mask correspond, the first mask defined is used
            else:
                if len(corresponding_masks) > 1:
                    self.log_warning(f"multiple os masks corresponding to {os_wanted} found, using the first",
                                     WarningLevel.ROBUSTNESS)
                # end if
                expected_mask = corresponding_masks[0]
            # end if

            self.assertEqual(
                obtained=os_detection,
                expected=expected_mask,
                msg="OS detected type from multi plateform feature is not correct")
        # end if
    # end def read_os_detection

    def _prerequisite_set_ios(self, reconnect=True, back_to_osx=True, open_channel=True):
        """
        Test prerequisites when verifying the NVS chunk isn't regenerated:
         - perform os detection with an IOS configuration (Mandatory)
         - reload OSX configuration (Optionally)
         - reconnect to the device (Optionally)
         - open channel (Optionally)

        :param reconnect: Flag indicating if we need to reconnect to the device after the read - OPTIONAL
        :type reconnect: ``bool``
        :param back_to_osx: Flag indicating if we change the parameters to the OSX after reconnection
        or detection - OPTIONAL
        :type back_to_osx: ``bool``
        :param open_channel: Flag indicating if we need to open a channel to the device after the read - OPTIONAL
        :type open_channel: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to IOS")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.change_host_os_emulation(self, os_emulation_type=BleNvsChunks.OsDetectedType.IOS)
        self._scan_connect_and_encrypt()
        # Add a small delay to let the device perform OS detection
        sleep(OS_DETECT_DELAY)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text=f"Check os detected is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self.read_os_detection(BleNvsChunks.OsDetectedType.IOS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Disconnect from the device")
        # --------------------------------------------------------------------------------------------------------------

        ble_context = BleProtocolTestUtils.get_ble_context(self)
        if self.current_channel.is_open:
            self.current_channel.close()
        # end if
        ble_context.disconnect(self.current_ble_device)
        if back_to_osx:  # The change of host os need to be done before the reconnection because it creates
            # errors otherwise. A real host would not change like this anyway
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text=f"Change host OS emulation to OSX")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.change_host_os_emulation(self, os_emulation_type=BleNvsChunks.OsDetectedType.OSX)
        # end if
        if reconnect:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text=f"Reconnect to the device")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            self._connect_and_encrypt(open_channel)
        # end if
    # end def _prerequisite_set_ios
# end class OsDetectionTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
