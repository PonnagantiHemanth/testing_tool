#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.mcu.nrf52.test.nrf52memorymanager_test
    :brief: NRF52 Memory Manager test module
    :author: Christophe Roquebert
    :date: 2020/06/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedDeviceMemoryManager
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedReceiverMemoryManager
from pylibrary.system.configurationmanager import ConfigurationManagerInterface
from pylibrary.tools.hexlist import HexList
from os.path import join, dirname, realpath
from intelhex import IntelHex
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
dir_path = dirname(realpath(__file__))


class FakeDebugger:
    """
    Implementation of a fake debugger to reserve the first index to device target.
    """
    VERSION = '0.0.1'

    MCU_NAME = 'NRF52'
    NVS_HEX_FILE_NAME = ''

    def __init__(self, number=0):
        """
        Constructor
        """
        self.number = number
        self._dummy = 0
    # end def __init__

    def __str__(self):
        """
        Retrieve debugger's name

        :return: debugger name
        :rtype: ``str``
        """
        name = 'Fake Debugger'
        return name
    # end def __str__

    def getVersion(self):
        """
        Obtain the version of this debugger.

        :return: The debugger version
        :rtype: ``str``
        """
        return self.VERSION
    # end def getVersion

    def open(self, **kwargs):                               # @ReservedAssignment
        """
        Stubbing the actual open function.

        :param \**kwargs: debugger specific parameters
        :type \**kwargs: ``dict``
        """
        pass
    # end def open

    def close(self):
        """
        Stubbing the actual close function.
        """
        pass
    # end def close

    def reset(self, **kwargs):
        """
        Stubbing the actual reset function.
        """
        return self._dummy
    # end def reset

    def readMemory(self, nvs_start_address, nvs_size):
        """
        Stubbing the actual readMemory function.
        """
        # dir_path = dirname(realpath(__file__))
        hex_file = IntelHex(self.NVS_HEX_FILE_NAME)
        addresses_to_parse = hex_file.segments()
        buffer = HexList()
        for (start, stop) in addresses_to_parse:
            if (start <= nvs_start_address <= stop) and (start <= (nvs_start_address+nvs_size) <= stop):
                array_to_parse = hex_file.gets(addr=nvs_start_address, length=nvs_size)
                buffer += HexList(array_to_parse)
                break
        # end if
        return buffer
    # end def reset

    def reload_file(self, firmware_hex_file=None, nvs_hex_file=None):
        """
        Stubbing the actual reload_file function.
        """
        return self._dummy
    # end def reload_file

    def reload_nvs_no_device_reset(self, nvs_hex_file):
        """
        Stubbing the actual reload_file function.
        """
        return self._dummy
    # end def reload_file
# end class FakeDebugger


class FakeDeviceDebugger(FakeDebugger):
    """
    Implementation of a fake debugger pre-loaded with a zaha quark256 NVS configuration.
    """
    NVS_START_ADDRESS = 0x3E000
    NVS_SIZE = 8 * 1024
    NVS_BANK_SIZE = 4 * 1024
    NVS_HEX_FILE_NAME = join(dir_path, 'nvs_uicr_zaha.hex')
# end class FakeDeviceDebugger


class FakeReceiverDebugger(FakeDebugger):
    """
    Implementation of a fake debugger pre-loaded with a mezzy NVS configuration.
    """
    NVS_START_ADDRESS = 0x3C000
    NVS_SIZE = 16 * 1024
    NVS_BANK_SIZE = 8 * 1024
    NVS_HEX_FILE_NAME = join(dir_path, 'nvs_uicr_mezzy.hex')
# end class FakeReceiverDebugger


class FakeConfigurationManager(ConfigurationManagerInterface):
    """
    Implementation of a fake Configuration Manager
    """
    def get_feature(self, feature_id):
        # See ``ConfigurationManagerInterface.get_feature``
        return []
    # end def get_feature

    @staticmethod
    def get_feature_version(feature_config):
        # See ``ConfigurationManagerInterface.get_feature_version``
        return None
    # end get_feature_version
# class FakeConfigurationManager


class Nrf52BasedDeviceMemoryManagerTestCase(TestCase):

    RefClass = Nrf52BasedDeviceMemoryManager
    RefDebugger = FakeDeviceDebugger

    @classmethod
    def _createInstance(cls):
        """
        Create an instance of referenced class

        :return: Instance of referenced class
        """
        return cls.RefClass(cls.RefDebugger(), FakeConfigurationManager())
    # end def _createInstance

    def test_instantiation(self):
        """
        Tests BleProPrepairing class instantiation
        """
        self._createInstance()
    # end def test_instantiation

    def test_invalidate_chunks(self):
        """
        Tests invalidate_chunks method
        """
        my_class = self._createInstance()
        # Empty list
        my_class.invalidate_chunks([])
        # Single element
        my_class.invalidate_chunks(["NVS_BLE_BOND_ID_1"])
        # Multiple elements
        my_class.invalidate_chunks(["NVS_BLE_BOND_ID_2", "NVS_BLE_BOND_INFO_ID_2", ])
    # end def test_invalidate_chunks

    def test_read_nvs(self):
        """
        Tests read_nvs method
        """
        my_class = self._createInstance()
        my_class.read_nvs()
    # end def test_read_nvs

    def test_load_nvs(self):
        """
        Tests load_nvs method
        """
        my_class = self._createInstance()
        # Call load_nvs with nvs_parser not initialized
        my_class.load_nvs()
        # Call load_nvs after nvs_parser initialization
        my_class.read_nvs()
        my_class.load_nvs()
    # end def test_load_nvs

    def test_get_chunks_by_name(self):
        """
        Tests get_chunks_by_name method
        """
        chunk_name_str = f'NVS_BLE_BOND_ID_0'
        my_class = self._createInstance()
        # Call get_chunks_by_name with nvs_parser not initialized
        my_class.get_chunks_by_name(chunk_name_str)
        # Call get_chunks_by_name after nvs_parser initialization
        my_class.read_nvs()
        my_class.get_chunks_by_name(chunk_name_str)
    # end def get_chunks_by_name
# end class Nrf52BasedDeviceMemoryManagerTestCase


class Nrf52BasedReceiverMemoryManagerTestCase(Nrf52BasedDeviceMemoryManagerTestCase):

    RefClass = Nrf52BasedReceiverMemoryManager
    RefDebugger = FakeReceiverDebugger
# end class Nrf52BasedReceiverMemoryManagerTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
