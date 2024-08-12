#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.mcu.test.connectchunks_test
    :brief:  connect chunks test module
    :author: Christophe Roquebert
    :date: 2020/06/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedDeviceMemoryManager
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeConfigurationManager
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeDebugger
from pylibrary.tools.hexlist import HexList, RandHexList
from os.path import join, dirname, realpath
from unittest import TestCase
dir_path = dirname(realpath(__file__))


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class FakeConnectDebugger(FakeDebugger):
    """
    Implementation of a fake debugger pre-loaded with a zaha quark256 NVS configuration.
    """
    NVS_START_ADDRESS = 0x3E000
    NVS_SIZE = 8 * 1024
    NVS_BANK_SIZE = 4 * 1024
    NVS_HEX_FILE_NAME = join(dir_path, 'nvs_uicr_connect.hex')
# end class FakeConnectDebugger


class ConnectChunksTestCase(TestCase):
    """
    Device connect Chunks testing class
    """
    RefDeviceClass = Nrf52BasedDeviceMemoryManager
    RefDeviceDebugger = FakeConnectDebugger

    def test_bootloader_connect_id_chunk(self):
        """
        Tests BootloaderConnectIdChunk class instantiation
        """
        my_memory_manager = self.RefDeviceClass(self.RefDeviceDebugger(), FakeConfigurationManager())
        # Call get_chunks_by_name after nvs_parser initialization
        my_memory_manager.read_nvs()
        my_chunks = my_memory_manager.get_chunks_by_name(f'NVS_BTLDR_CONNECT_ID')
        assert(my_chunks[0].host_idx == HexList("00"))
        assert(my_chunks[0].protocol == HexList("02"))
        assert(my_chunks[1].host_idx == HexList("01"))
        assert(my_chunks[1].protocol == HexList("02"))
    # end def test_bootloader_connect_id_chunk

    def _test_connect_id_dual_chunk(self):
        """
        Tests ConnectIdDualChunk class instantiation is deprecated
        """
        my_memory_manager = self.RefDeviceClass(self.RefDeviceDebugger())
        # Call get_chunks_by_name after nvs_parser initialization
        my_memory_manager.read_nvs()
        my_chunks = my_memory_manager.get_chunks_by_name(f'NVS_CONNECT_ID')
        assert(my_chunks[0].data.bcast_pending == HexList("00"))
        assert(my_chunks[0].data.host_index == HexList("00"))
        assert(my_chunks[0].data.scheme_host_0 == HexList(ConnectIdChunkData.STATUS.UNPAIRED))
        assert(my_chunks[0].data.scheme_host_1 == HexList(ConnectIdChunkData.STATUS.UNPAIRED))
        assert(my_chunks[0].data.scheme_host_2 == HexList(ConnectIdChunkData.STATUS.UNPAIRED))

        assert(my_chunks[1].data.bcast_pending == HexList("00"))
        assert(my_chunks[1].data.host_index == HexList("00"))
        assert(my_chunks[1].data.scheme_host_0 == HexList(ConnectIdChunkData.STATUS.BLE_PAIRED))
        assert(my_chunks[1].data.scheme_host_1 == HexList(ConnectIdChunkData.STATUS.UNPAIRED))
        assert(my_chunks[1].data.scheme_host_2 == HexList(ConnectIdChunkData.STATUS.UNPAIRED))

        assert(my_chunks[2].data.bcast_pending == HexList("00"))
        assert(my_chunks[2].data.host_index == HexList("01"))
        assert(my_chunks[2].data.scheme_host_0 == HexList(ConnectIdChunkData.STATUS.BLE_PAIRED))
        assert(my_chunks[2].data.scheme_host_1 == HexList(ConnectIdChunkData.STATUS.UNPAIRED))
        assert(my_chunks[2].data.scheme_host_2 == HexList(ConnectIdChunkData.STATUS.UNPAIRED))
    # end def test_connect_id_chunk

    def test_connect_id_ble_chunk(self):
        """
        Tests ConnectIdBlePro3HostsChunk class instantiation
        """
        my_debugger = self.RefDeviceDebugger()
        my_debugger.NVS_HEX_FILE_NAME = join(dir_path, 'nvs_uicr_connect_ble.hex')
        my_memory_manager = self.RefDeviceClass(my_debugger, FakeConfigurationManager())
        # Call get_chunks_by_name after nvs_parser initialization
        my_memory_manager.read_nvs()
        my_chunks = my_memory_manager.get_chunks_by_name(f'NVS_CONNECT_ID')

        assert(my_chunks[0].data.host_index == HexList("00"))
        assert (my_chunks[0].data.pairing_src_0 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[0].data.pairing_src_1 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[0].data.pairing_src_2 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[0].data.scheme_host_0 == HexList(ConnectIdChunkData.STATUS.OOB))
        assert (my_chunks[0].data.scheme_host_1 == HexList(ConnectIdChunkData.STATUS.OOB))
        assert (my_chunks[0].data.scheme_host_2 == HexList(ConnectIdChunkData.STATUS.OOB))

        assert (my_chunks[1].data.host_index == HexList("00"))
        assert (my_chunks[1].data.pairing_src_0 == HexList(ConnectIdChunkData.PairingSrc.USR))
        assert (my_chunks[1].data.pairing_src_1 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[1].data.pairing_src_2 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[1].data.scheme_host_0 == HexList(ConnectIdChunkData.STATUS.BLE_PAIRED))
        assert (my_chunks[1].data.scheme_host_1 == HexList(ConnectIdChunkData.STATUS.OOB))
        assert (my_chunks[1].data.scheme_host_2 == HexList(ConnectIdChunkData.STATUS.OOB))

        assert (my_chunks[2].data.host_index == HexList("01"))
        assert (my_chunks[2].data.pairing_src_0 == HexList(ConnectIdChunkData.PairingSrc.USR))
        assert (my_chunks[2].data.pairing_src_1 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[2].data.pairing_src_2 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[2].data.scheme_host_0 == HexList(ConnectIdChunkData.STATUS.BLE_PAIRED))
        assert (my_chunks[2].data.scheme_host_1 == HexList(ConnectIdChunkData.STATUS.OOB))
        assert (my_chunks[2].data.scheme_host_2 == HexList(ConnectIdChunkData.STATUS.OOB))

        assert (my_chunks[3].data.host_index == HexList("01"))
        assert (my_chunks[3].data.pairing_src_0 == HexList(ConnectIdChunkData.PairingSrc.USR))
        assert (my_chunks[3].data.pairing_src_1 == HexList(ConnectIdChunkData.PairingSrc.MFG))
        assert (my_chunks[3].data.pairing_src_2 == HexList(ConnectIdChunkData.PairingSrc.NONE))
        assert (my_chunks[3].data.scheme_host_0 == HexList(ConnectIdChunkData.STATUS.BLE_PAIRED))
        assert (my_chunks[3].data.scheme_host_1 == HexList(ConnectIdChunkData.STATUS.BLE_PAIRED))
        assert (my_chunks[3].data.scheme_host_2 == HexList(ConnectIdChunkData.STATUS.OOB))
    # end def test_connect_id_chunk

# end class ConnectChunksTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
