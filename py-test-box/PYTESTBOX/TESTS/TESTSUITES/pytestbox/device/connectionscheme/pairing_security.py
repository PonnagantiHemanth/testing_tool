#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.pairing_security
:brief: Validate "device pairing" feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/06/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.pairing_security import SharedPairingSecurityTestCase
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingSecurityTestCase(SharedPairingSecurityTestCase, DeviceBaseTestCase):
    """
    Device Pairing Security TestCases
    """

    @features("BLEDevicePairing")
    @level("Functionality")
    @services("Debugger")
    def test_nvs_chunk_data_validation(self):
        """
        Test that pairing data in the receiver and device NVS shall match: Check the keys and addresses values. Check
        device specific pairing information
        """
        device_pairing_slot = 1 if self.f.PRODUCT.DEVICE.F_NbHosts > 1 else 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Pairing sequence and retrieve the pairing slot")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check data in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DevicePairingTestUtils.PairingChecker.get_bluetooth_address(self)
        DevicePairingTestUtils.NvsManager.check_device_pairing_data(self, device_pairing_slot + 1, bluetooth_address)

        self.testCaseChecked("FNT_DEV_PAIR_0044")
    # end def test_nvs_chunk_data_validation

    @features("BLEDevicePairing")
    @level("Functionality")
    @services("Debugger")
    def test_long_term_key_usage(self):
        """
        Test that the Long Term Key stored in the BLE Bond ID chunk shall be used to encrypt the communication between
        the receiver and the device. Check that the link is not established if the LTK is changed in the device memory.
        """
        device_pairing_slot = 1 if self.f.PRODUCT.DEVICE.F_NbHosts > 1 else 0
        ReceiverTestUtils.switch_to_receiver(self, ChannelUtils.get_port_index(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Pairing sequence and retrieve the pairing slot")
        # --------------------------------------------------------------------------------------------------------------
        device_index = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)
        new_paired_channel = DeviceManagerUtils.get_channel(
            test_case=self,
            channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self),
                device_index=device_index))
        assert new_paired_channel is not None and isinstance(new_paired_channel, ThroughReceiverChannel), \
            "A channel should have been created for the new paired device and it should be a " \
            f"ThroughReceiverChannel, new_paired_channel = {new_paired_channel} is not matching those requirements"

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check data in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------------------------------------------
        # Clean all DeviceConnection prior to corrupt the NVS chunk
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
        DevicePairingTestUtils.PairingChecker.get_bluetooth_address(self)
        # Dump receiver NVS
        self.memory_manager.read_nvs()
        # Extract the latest BLE pairing chunk
        chunk_id = f"NVS_BLE_BOND_ID_{device_pairing_slot}"
        device_data_list = self.memory_manager.get_chunks_by_name(chunk_id)
        # Long Term Key corruption
        device_data_list[-1].local_ble_gap_enc_info.enc_info_long_term_key.invertBit(0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id, HexList(device_data_list[-1]), is_encrypted=True)
        self.memory_manager.load_nvs()
        # A device reset is triggered by load_nvs so a disconnection will occur
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=new_paired_channel, link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
            device_index=device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no DeviceConnection with link established is received during 1s")
        # --------------------------------------------------------------------------------------------------------------
        message = ChannelUtils.get_only(
            test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection, timeout=1, check_first_message=False, allow_no_message=True,
            skip_error_message=True)
        if message is not None:
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(message)
            packet_link_status = to_int(
                device_info_class.fromHexList(HexList(message.information)).device_info_link_status)
            packet_device_index = to_int(message.device_index)
            if (isinstance(self.current_channel, ThroughReceiverChannel) and
                    packet_device_index == self.current_channel.device_index):
                assert packet_link_status == DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED, \
                    'DeviceConnection with Link established shall not be received'
            # end if
        # end if

        # Long Term Key fix back
        device_data_list[-1].local_ble_gap_enc_info.enc_info_long_term_key.invertBit(0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id, HexList(device_data_list[-1]), is_encrypted=True)
        self.memory_manager.load_nvs()
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=new_paired_channel, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            device_index=device_index)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=new_paired_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify an HID report can be received")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.memory_manager.read_nvs()
        # Extract the latest BLE pairing chunk
        second_device_data_list = self.memory_manager.get_chunks_by_name(chunk_id)
        self.assertEqual(len(second_device_data_list), (len(device_data_list)+2), "Wrong number of chunks")

        self.testCaseChecked("FNT_DEV_PAIR_0045")
    # end def test_long_term_key_usage

    @features("BLELatencyRemoval")
    @features("BLEDevicePairing")
    @level("Functionality")
    @services("Debugger")
    def test_latency_removal_attribute(self):
        """
        Test the peripheral supporting the latency removal feature. Check BLE Pro Attributes bit 1 in Device
        BLE BOND ID pairing information.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Pairing sequence and retrieve the pairing slot")
        # --------------------------------------------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Latency removal bit in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_bluetooth_address(self)
        DevicePairingTestUtils.NvsManager.check_latency_removal_bit(self, pairing_slot)

        self.testCaseChecked("FNT_DEV_PAIR_0046")
    # end def test_latency_removal_attribute

    @features("BLEProOsDetection")
    @features("BLEDevicePairing")
    @level("Functionality")
    @services("Debugger")
    def test_ble_pro_receiver_detection(self):
        """
        Test the peripheral supporting the BLE PRO OS Detection feature. Check OS detection byte in Device
        BLE BOND ID pairing information.
        
        cf https://jira.logitech.io/browse/BPRO-153
        """
        device_pairing_slot = 2 if self.f.PRODUCT.DEVICE.F_NbHosts > 1 else 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Pairing sequence and retrieve the pairing slot")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check BLE PRO OS Detection byte in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_bluetooth_address(self)
        DevicePairingTestUtils.NvsManager.check_os_detected(
            self, pairing_slot=device_pairing_slot, expected_os_type=BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO)

        self.testCaseChecked("FNT_DEV_PAIR_0047")
    # end def test_ble_pro_receiver_detection
# end class PairingSecurityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
