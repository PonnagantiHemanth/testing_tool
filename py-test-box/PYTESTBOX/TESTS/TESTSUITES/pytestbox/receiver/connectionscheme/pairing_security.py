#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.connectionscheme.pairing_security
:brief: Validates 'device pairing' feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/04/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.pairing_security import SharedPairingSecurityTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingSecurityTestCase(SharedPairingSecurityTestCase, ReceiverBaseTestCase):
    """
    Receiver Pairing Security TestCases
    """

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_data_validation(self):
        """
        Pairing data in the receiver and device NVS shall match: Check the keys and addresses values

        Check receiver specific information p
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Roll out the Pairing sequence and retrieve the pairing slot')
        # ---------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # ---------------------------------------------------------------------------
        self.logTitle2('''Test Check 1: Check data in BLE Bond Id NVS chunk''')
        # --------------------------------------------------------------------------
        bluetooth_address = DevicePairingTestUtils.PairingChecker.get_bluetooth_address(self)
        DevicePairingTestUtils.NvsManager.check_receiver_pairing_data(self, pairing_slot, bluetooth_address,
            entropy=HexList(SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX),
            auth_method=HexList(DevicePairingTestUtils.get_authentication_method(self)))

        self.testCaseChecked("FNT_DEV_PAIR_0044")
    # end def test_nvs_chunk_data_validation

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_long_term_key_usage(self):
        """
        The Long Term Key stored in the BLE Bond ID chunk shall be used to encrypt the communication between the
        receiver and the device.
        Check that the link is not established if the LTK is changed in the receiver memory.
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Roll out the Pairing sequence and retrieve the pairing slot')
        # ---------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # ---------------------------------------------------------------------------
        self.logTitle2('''Test Step 2: Retrieve the last receiver BLE Bond Id chunk and corrupt its long term key''')
        # --------------------------------------------------------------------------
        bluetooth_address = DevicePairingTestUtils.PairingChecker.get_bluetooth_address(self)
        # Dump receiver NVS
        self.memory_manager.read_nvs()
        # Extract the latest BLE pairing chunk
        chunk_id = f'NVS_BLE_BOND_ID_{int(Numeral(pairing_slot)) - 1}'
        receiver_data_list = self.memory_manager.get_chunks_by_name(chunk_id)
        # Long Term Key corruption
        receiver_data_list[-1].remote_ble_gap_enc_info.enc_info_long_term_key.invertBit(0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id, HexList(receiver_data_list[-1]), is_encrypted=True,
                                                     iv=receiver_data_list[-1].ref.iv)
        CommonBaseTestUtils.load_nvs(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Power off/on the receiver')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        # Re-enable HID++ reporting
        self.enable_hidpp_reporting()

        # Get HID Descriptor enabling report parsing
        self.get_device_descriptors()
        # Wake-up the device
        DevicePairingTestUtils.generate_user_action(self)
        sleep(.5)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check no HID report is received when a user action is performed')
        # ---------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('''Test Step 4: Fix the long term key in the last receiver BLE Bond Id chunk''')
        # --------------------------------------------------------------------------
        # Long Term Key fix back
        receiver_data_list[-1].remote_ble_gap_enc_info.enc_info_long_term_key.invertBit(0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id, HexList(receiver_data_list[-1]), is_encrypted=True,
                                                     iv=receiver_data_list[-1].ref.iv)
        CommonBaseTestUtils.load_nvs(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Power off/on the receiver')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        # Re-enable HID++ reporting
        self.enable_hidpp_reporting()

        # Wake-up the device
        DevicePairingTestUtils.generate_user_action(self)
        sleep(.5)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Verify an HID report can be received')
        # ---------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.memory_manager.read_nvs()
        # ---------------------------------------------------------------------------
        self.logTitle2('''Test Check 3: Check two BLE Bond Id chunks have been added in the NVS''')
        # --------------------------------------------------------------------------
        second_receiver_data_list = self.memory_manager.get_chunks_by_name(chunk_id)
        self.assertEqual(len(second_receiver_data_list), (len(receiver_data_list)+2), "Wrong number of chunks")

        self.testCaseChecked("FNT_DEV_PAIR_0045")
    # end def test_long_term_key_usage

# end class PairingSecurityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
