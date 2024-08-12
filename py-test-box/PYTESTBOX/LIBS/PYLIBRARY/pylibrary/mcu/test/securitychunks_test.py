#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.mcu.test.securitychunks_test
    :brief:  Security chunks test module
    :author: Christophe Roquebert
    :date: 2020/06/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.mcu.securitychunks import DfuCtrlChunk
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedDeviceMemoryManager
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeConfigurationManager
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeDebugger
from pylibrary.tools.hexlist import HexList
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


class DfuCtrlChunkTestCase(TestCase):
    """
    Device connect Chunks testing class
    """
    RefDeviceClass = Nrf52BasedDeviceMemoryManager
    RefDeviceDebugger = FakeConnectDebugger

    def test_dfu_ctrl_chunk(self):
        """
        Tests DfuCtrlChunk class instantiation
        """
        my_memory_manager = self.RefDeviceClass(self.RefDeviceDebugger(), FakeConfigurationManager())
        param = 0
        my_chunk = DfuCtrlChunk(enable=DfuCtrlChunk.STATE.DFU_ENABLED, param=param)
        # Call get_chunks_by_name after nvs_parser initialization
        my_memory_manager.read_nvs()
        my_memory_manager.nvs_parser.add_new_chunk('NVS_DFU_ID', HexList(my_chunk))
        my_chunks = my_memory_manager.get_chunks_by_name(f'NVS_DFU_ID')
        assert(my_chunks[0].enable == HexList(DfuCtrlChunk.STATE.DFU_ENABLED))
        assert(my_chunks[0].param == HexList(param))
    # end def test_dfu_ctrl_chunk
# end class DfuCtrlChunkTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
