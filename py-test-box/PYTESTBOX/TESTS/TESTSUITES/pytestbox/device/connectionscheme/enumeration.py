#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.enumeration
:brief: Validate paired device enumeration feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/02/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from math import ceil
from math import floor
from random import randint

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.nvsparser import MODE
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.connectionscheme.enumeration import SharedEnumerationTestCase
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class EnumerationTestCase(SharedEnumerationTestCase, DeviceBaseTestCase):
    """
    Validate Enumeration TestCases in Device mode
    """

    @features('BLEDevicePairing')
    @level('Robustness')
    @services('Debugger')
    @bugtracker('BLE_Enumeration_Memory_Access_Issue')
    def test_enumeration_nvs_full(self):
        """
        Validate that the device will not try to fetch data outside the flash area when collecting chunks located
        at the end of the NVS second bank.

        cf out-of-bank memory access firmware issue
        https://goldenpass.logitech.com:8443/c/ccp_fw/lfa/+/10042
        """
        pairing_slot = 0
        ChannelUtils.close_channel(test_case=self)
        self.post_requisite_reload_device_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get the last system attribute user services chunk')
        # --------------------------------------------------------------------------------------------------------------
        self.device_memory_manager.read_nvs()
        sys_attr_user_services_chunk_id = f'NVS_BLE_SYS_ATTR_USR_SRVCS_ID_{pairing_slot}'
        sys_attr_user_services_chunk_history = self.device_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=sys_attr_user_services_chunk_id, mode=MODE.DEVICE)
        usr_services_chunk_length = len(sys_attr_user_services_chunk_history[-1].ref.to_hex_array())

        last_gap_address_chunk = self.memory_manager.nvs_parser.get_chunk_history(
            chunk_id='NVS_BLE_LAST_GAP_ADDR_USED')[-1]
        last_gap_address_chunk_length = len(last_gap_address_chunk.to_hex_array())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Compute the number of BLE address chunk that can be inserted at the end of the '
                                 'bank 1')
        # --------------------------------------------------------------------------------------------------------------
        loop_count = floor(usr_services_chunk_length / last_gap_address_chunk_length)
        for loop_index in range(loop_count):
            active_bank_id, current_length, total_length = self.device_memory_manager.nvs_parser.get_active_bank_status(
                chunk_id=sys_attr_user_services_chunk_id)
            if active_bank_id == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Loop {loop_index + 1} / {loop_count}: If bank 0 is active, fill it in '
                                         'with copies of the user services chunk to force the switch to bank 1 '
                                         'at next reset')
                # ------------------------------------------------------------------------------------------------------
                full_bank0_chunk_count = floor((total_length - current_length) / usr_services_chunk_length)
                for _ in range(full_bank0_chunk_count-1):
                    self.memory_manager.nvs_parser.add_new_chunk(chunk_id=sys_attr_user_services_chunk_id,
                                                                 data=HexList(sys_attr_user_services_chunk_history[-1]))
                # end for
                # Force a service changed by reloading an empty chunk NVS_BLE_SYS_ATTR_USR_SRVCS_ID_0.
                self.device_memory_manager.nvs_parser.add_new_chunk(
                    chunk_id='NVS_BLE_SYS_ATTR_USR_SRVCS_ID_0', data=HexList([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
                self.memory_manager.load_nvs()

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Reset the device to force the switch to bank 1')
                # ------------------------------------------------------------------------------------------------------
                DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)

                DeviceManagerUtils.set_channel(test_case=self, new_channel_id=ChannelIdentifier(
                    port_index=ChannelUtils.get_port_index(test_case=self), device_index=1), open_channel=False)
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=self, device_connection_optional=True, ble_service_changed_required=True,
                    wireless_broadcast_event_required=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check bank 1 is active")
                # ------------------------------------------------------------------------------------------------------
                self.device_memory_manager.read_nvs()
                active_bank_id, current_length, total_length = \
                    self.device_memory_manager.nvs_parser.get_active_bank_status(
                        chunk_id=sys_attr_user_services_chunk_id)
                self.assertEqual(active_bank_id, 1, "Bank 1 should be active")
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Fill in bank 1 with copies of the last user services chunk but keep the space '
                                     'to a last one at the end')
            # ----------------------------------------------------------------------------------------------------------
            sys_attr_user_services_chunk_history = self.device_memory_manager.nvs_parser.get_chunk_history(
                chunk_id=sys_attr_user_services_chunk_id, mode=MODE.DEVICE)
            bank1_chunk_count = floor((total_length - current_length) / usr_services_chunk_length) - 1
            for _ in range(bank1_chunk_count):
                self.memory_manager.nvs_parser.add_new_chunk(chunk_id=sys_attr_user_services_chunk_id,
                                                             data=HexList(sys_attr_user_services_chunk_history[-1]))
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Fill part of the left space by an incremented number of BLE address chunk')
            # ----------------------------------------------------------------------------------------------------------
            active_bank_id, current_length, total_length = self.device_memory_manager.nvs_parser.get_active_bank_status(
                chunk_id=sys_attr_user_services_chunk_id)
            min_ble_address_chunk_count = ceil((total_length - current_length - usr_services_chunk_length) /
                                               last_gap_address_chunk_length)
            for _ in range(min_ble_address_chunk_count + loop_index):
                self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_BLE_LAST_GAP_ADDR_USED',
                                                             data=HexList(last_gap_address_chunk.chunk_data))
            # end for

            free_space = total_length - current_length - (
                    (min_ble_address_chunk_count + loop_index) * last_gap_address_chunk_length)
            chunk_size = randint(4, free_space)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Finally add a truncated user services chunk (chunk size = {chunk_size}'
                                     f' and nvs free space = {free_space}')
            # ----------------------------------------------------------------------------------------------------------
            chunk_header_size = 4
            self.memory_manager.nvs_parser.add_new_chunk(
                chunk_id=sys_attr_user_services_chunk_id,
                data=HexList(sys_attr_user_services_chunk_history[-1])[:chunk_size - chunk_header_size])
            self.memory_manager.load_nvs()
            self.device_memory_manager.nvs_parser.get_active_bank_status(chunk_id=sys_attr_user_services_chunk_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Reset the device to force the firmware to verify the chunks in NVS')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify the device reconnects to the receiver')
            # ----------------------------------------------------------------------------------------------------------
            DeviceManagerUtils.set_channel(test_case=self, new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=1), open_channel=False)
            CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                test_case=self, device_connection_optional=True, ble_service_changed_required=True,
                wireless_broadcast_event_required=True)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Test the connection by sending the enable Manufacturing Features')
            # --------------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            ChannelUtils.close_channel(test_case=self)
            self.device_memory_manager.read_nvs()
        # end for

        self.testCaseChecked("FUN_ENUM_0030")
    # end def test_enumeration_nvs_full

# end class EnumerationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
