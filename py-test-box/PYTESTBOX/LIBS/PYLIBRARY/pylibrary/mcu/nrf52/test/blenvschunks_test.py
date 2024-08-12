#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.mcu.nrf52.test.blenvschunks_test
    :brief:  NVS BLE chunk test module
    :author: Christophe Roquebert
    :date: 2020/06/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.mcu.nrf52.blenvschunks import DeviceBleBondId
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedDeviceMemoryManager
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedReceiverMemoryManager
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeConfigurationManager
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeDeviceDebugger
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeReceiverDebugger
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleNvsChunksTestCase(TestCase):
    """
    Ble Nvs Chunks testing class
    """
    RefDeviceClass = Nrf52BasedDeviceMemoryManager
    RefReceiverClass = Nrf52BasedReceiverMemoryManager
    RefDeviceDebugger = FakeDeviceDebugger
    RefReceiverDebugger = FakeReceiverDebugger

    def test_device_ble_bond_id(self):
        """
        Tests Device Ble BondId class instantiation
        """
        my_class = DeviceBleBondId.fromHexList(HexList(
            "01000000000C0F0003021BAFEBF076A4C8450B98F4AED741847E4300000000000000000000008626E5913DE2F5DC5C68D19FF373ABC40210C17E5A5FDD000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000C14AFF3881C571AE77E0D1B21D8DD41B02A729A69E0FCB000000000000000000000000000000000002A729A69E0FCB000000000000000210C17E5A5FDD00"))
        assert(my_class.ble_gap_evt_auth_status.local_kdist_long_term_key == 1)
        assert(my_class.local_ble_gap_enc_info.enc_info_long_term_key == HexList("1BAFEBF076A4C8450B98F4AED741847E"))
        assert (my_class.local_gap_master_identification.enc_id_random == HexList("0000000000000000"))
        assert(my_class.bluetooth_low_energy_address.device_bluetooth_address == HexList("10C17E5A5FDD"))
    # end def test_device_ble_bond_id

    def test_receiver_ble_bond_id(self):
        """
        Tests Receiver Ble BondId class instantiation
        """
        my_memory_manager = self.RefReceiverClass(self.RefReceiverDebugger(), FakeConfigurationManager())
        # Call get_chunks_by_name after nvs_parser initialization
        my_memory_manager.read_nvs()
        my_chunk = my_memory_manager.get_chunks_by_name(f'NVS_BLE_BOND_ID_0')[0]
        assert(my_chunk.bluetooth_low_energy_address.device_bluetooth_address == HexList("F5C07E5A5FDD"))
        assert(my_chunk.ble_gap_evt_auth_status.local_kdist_long_term_key == 1)
        assert(my_chunk.local_gap_master_identification.enc_id_ediv == HexList("0000"))
        assert(my_chunk.local_identity_key.identity_resolving_key == HexList("C41BED292DD4218275CAB4BDC8876924"))
        assert(my_chunk.remote_ble_gap_enc_info.enc_info_long_term_key == HexList("B9F2036F1FA50EB18733BA47C084FD78"))
        assert(my_chunk.entropy == HexList("14"))
        assert(my_chunk.ble_pro_auth_control == HexList("02"))
    # end def test_receiver_ble_bond_id

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
