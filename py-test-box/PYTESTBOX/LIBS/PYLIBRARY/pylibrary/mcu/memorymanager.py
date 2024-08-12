#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.memorymanager
:brief: MCU memory manager base classes.
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/08/31
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from copy import deepcopy
from enum import IntEnum

from pylibrary.mcu.connectchunks import BootloaderConnectIdChunk
from pylibrary.mcu.connectchunks import ConnectIdBlePro3HostsChunk
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.mcu.memoryinterface import NvsManagerInterface
from pylibrary.system.configurationmanager import ConfigurationManagerInterface
from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_QUARK_CORE
from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_QUARK_GAMING
from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_RECEIVER
from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_STM32H7
from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_STM32L052
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.nvsparser import AddressBasedNvsParser
from pylibrary.tools.nvsparser import CHUNK_ID_TO_CLASS_MAP
from pylibrary.tools.nvsparser import IdBasedNvsParser
from pylibrary.tools.nvsparser import MODE


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MemoryManager(NvsManagerInterface):
    """
    Memory Manager Implementation.
    """

    class ADDRESS:
        """
        Address in memory map
        """
        NVS_ENCRYPTION_KEY = None
    # end class ADDRESS

    class SIZE(IntEnum):
        """
        Data Size
        """
        NVS_ENCRYPTION_KEY = 0
    # end class SIZE

    def __init__(self, debugger):
        """
        :param debugger: The debugger object to use to read memory
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        """
        self.chunk_type = None
        self.pairing_slot_count = None
        self.debugger = debugger
        self.nvs_parser = None
        self.backup_nvs_parser = None
        self.chunk_id_map = None
        self.nvs_encryption_key = None if self.ADDRESS.NVS_ENCRYPTION_KEY is None else self._set_nvs_encryption_key()
    # end def __init__

    def read_nvs(self, backup=False):
        """
        Read NVS content using the debugger and create an NVS Parser object, skipped if zero NVS size

        :param backup: Flag enabling to save a copy of the initial NVS - OPTIONAL
        :type backup: ``bool``
        """
        if backup:
            self.backup_nvs_parser = self.nvs_parser
        # end if

        # If the NVS size is 0, do not read the NVS
        if self.debugger.NVS_SIZE == 0:
            return
        # end if

        if self.chunk_id_map["NVS_CHUNK_METHOD"]:
            self.nvs_parser = IdBasedNvsParser.from_memory_read(debugger=self.debugger,
                                                         nvs_start_address=self.debugger.NVS_START_ADDRESS,
                                                         nvs_size=self.debugger.NVS_SIZE,
                                                         zone_bank_length=self.debugger.NVS_BANK_SIZE,
                                                         chunk_id_map=self.chunk_id_map,
                                                         aes_key=self.nvs_encryption_key)
        else:
            self.nvs_parser = AddressBasedNvsParser.from_memory_read(debugger=self.debugger,
                                                                 nvs_start_address=self.debugger.NVS_START_ADDRESS,
                                                                 nvs_size=self.debugger.NVS_SIZE,
                                                                 zone_bank_length=self.debugger.NVS_BANK_SIZE,
                                                                 chunk_id_map=self.chunk_id_map,
                                                                 aes_key=self.nvs_encryption_key)
        # end if
        if backup and self.backup_nvs_parser is None:
            self.backup_nvs_parser = deepcopy(self.nvs_parser)
        # end if
    # end def read_nvs

    def load_nvs(self, backup=False, no_reset=False, **kwargs):
        """
        Store the modified NVS content on the target using the debugger

        :param backup: Flag enabling to reload the copy of the initial NVS - OPTIONAL
        :type backup: ``bool``
        :param no_reset: Flag enabling to reload the NVS without resetting the device, only stop and run - OPTIONAL
        :type no_reset: ``bool``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        if backup and self.backup_nvs_parser is not None:
            if not no_reset:
                self.debugger.reload_file(nvs_hex_file=self.backup_nvs_parser.to_hex_file())
            else:
                self.debugger.reload_nvs_no_device_reset(nvs_hex_file=self.backup_nvs_parser.to_hex_file())
            # end if
        elif self.nvs_parser is not None:
            if not no_reset:
                self.debugger.reload_file(nvs_hex_file=self.nvs_parser.to_hex_file())
            else:
                self.debugger.reload_nvs_no_device_reset(nvs_hex_file=self.nvs_parser.to_hex_file())
            # end if
        # end if
    # end def load_nvs

    def reset(self, **kwargs):
        """
        Reset the device using the debugger.

        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        self.debugger.reset(**kwargs)
    # end def reset

    def invalidate_chunks(self, chunk_names=None, **kwargs):
        """
        Invalidate the chunk based on their names

        :param chunk_names: list of chunk names as defined in the chunk id map. If None, return 0 - OPTIONAL
        :type chunk_names: ``list[str] | None``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``

        :return: Number of invalidated chunk or None (if ``get_chunk_history()`` is not called)
        :rtype: ``int`` or ``None``
        """
        if chunk_names is None:
            chunk_names = []
        # end if

        if self.nvs_parser is None:
            return None
        # end if

        invalidated_chunk_count = 0
        for chunk_name in chunk_names:
            if chunk_name not in self.chunk_id_map:
                continue
            # end if
            chunks = self.nvs_parser.get_chunk_history(chunk_name, get_all=True)
            for chunk in chunks:
                chunk.chunk_id = self.chunk_id_map["NVS_INVALID_CHUNK_ID"]
                invalidated_chunk_count += 1
            # end for
        # end for
        return invalidated_chunk_count
    # end def invalidate_chunks

    def get_active_chunk_by_name(self, chunk_name, active_bank_only=False, **kwargs):
        """
        Retrieve the current active chunk matching the given name and cast it into its python representation (if any)

        :param chunk_name: Chunk name as defined in the chunk id map
        :type chunk_name: ``str``
        :param active_bank_only: Flag indicating to retrieve the chunk history in the active bank only - OPTIONAL
        :type active_bank_only: ``bool``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``

        :return: python chunk representation
        :rtype: ``NvsChunk`` or ``None``
        """
        nvs_chunks = self.get_chunks_by_name(chunk_name=chunk_name, active_bank_only=active_bank_only)

        return nvs_chunks[-1] if len(nvs_chunks) > 0 else None
    # end def get_active_chunk_by_name

    def get_chunks_by_name(self, chunk_name, active_bank_only=False, **kwargs):
        """
        Retrieve a list of chunks matching the given name and cast it into its python representation (if any)

        :param chunk_name: Chunk name as defined in the chunk id map
        :type chunk_name: ``str``
        :param active_bank_only: Flag indicating to retrieve the chunk history in the active bank only - OPTIONAL
        :type active_bank_only: ``bool``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``

        :return: list of python chunk representation
        :rtype: ``list[NvsChunk]`` or ``None``
        """
        if (self.nvs_parser is None or
                chunk_name not in CHUNK_ID_TO_CLASS_MAP or
                self.chunk_type not in CHUNK_ID_TO_CLASS_MAP[chunk_name]):
            return None
        # end if

        return self.nvs_parser.get_chunk_history(
            chunk_id=chunk_name, mode=self.chunk_type, active_bank_only=active_bank_only)
    # end def get_chunks_by_name

    def get_ble_bond_id_chunks(self, pairing_slot=0, bluetooth_address=None, active_bank_only=False, **kwargs):
        """
        Retrieve the NVS_BLE_BOND_ID chunks list from NVS by pairing slot and bluetooth address

        :param pairing_slot: device index - OPTIONAL
        :type pairing_slot: ``int | None``
        :param bluetooth_address: central or peripheral bluetooth address - OPTIONAL
        :type bluetooth_address: ``HexList``
        :param active_bank_only: Flag indicating to retrieve the chunk history in the active bank only - OPTIONAL
        :type active_bank_only: ``bool``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``

        :return: The wanted chunk history
        :rtype: ``list[NvsChunk|BitFieldContainerMixin]``
        """
        if pairing_slot is None:
            chunk_list = []
            # Loop over the number of available pairing slots
            for i in range(self.pairing_slot_count):
                ble_bond_id_str = f'NVS_BLE_BOND_ID_{i}'
                # Search for all the chunks matching the name
                chunks = self.get_chunks_by_name(ble_bond_id_str, active_bank_only)
                if chunks is not None:
                    chunk_list.extend(chunks)
                # end if
            # end for
        else:
            # Search for all the chunks matching the given pairing slot
            ble_bond_id_str = f'NVS_BLE_BOND_ID_{pairing_slot}'
            chunk_list = self.get_chunks_by_name(ble_bond_id_str, active_bank_only)
        # end if
        if bluetooth_address is not None:
            for chunk in reversed(chunk_list):
                if chunk.bluetooth_low_energy_address.device_bluetooth_address != bluetooth_address:
                    chunk_list.remove(chunk)
                # end if
            # end for
        # end if
        return chunk_list
    # end def get_ble_bond_id_chunks

    def get_bluetooth_addresses(self, pairing_slots=None, **kwargs):
        """
        Retrieve the bluetooth addresses for a given pairing slot list

        :param pairing_slots: pairing slots - OPTIONAL
        :type pairing_slots: ``list[int]`` or ``None``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``

        :return: List of tuple (slot, bluetooth address (LSB))
        :rtype: ``list[tuple[int, HexList]]``
        """
        if pairing_slots is None:
            pairing_slots = [0, 1, 2, 3, 4, 5]
        # end if

        pairing_data = []
        for pairing_slot in pairing_slots:
            if pairing_slot == self.pairing_slot_count:
                break
            # end if
            ble_bond_id_chunks = self.get_ble_bond_id_chunks(pairing_slot)
            for chunk in ble_bond_id_chunks:
                pairing_data.append((pairing_slot, chunk.bluetooth_low_energy_address.device_bluetooth_address))
            # end for
        # end for
        return pairing_data
    # end def get_bluetooth_addresses

    def clean_pairing_data(self):
        # See ``NvsManagerInterface.clean_pairing_data``
        super().clean_pairing_data()
    # end def clean_pairing_data

    def switch_to_host_id(self, host_id=0, is_test_setup=True, force_oob=False):
        # See ``NvsManagerInterface.switch_to_host_id``
        bootloader_connect_id_chunk_list = self.get_chunks_by_name('NVS_BTLDR_CONNECT_ID')
        connect_id_chunk_list = self.get_chunks_by_name('NVS_CONNECT_ID')
        if bootloader_connect_id_chunk_list is not None and len(bootloader_connect_id_chunk_list) > 0:
            btldr_data = bootloader_connect_id_chunk_list[-1]
            btldr_data.host_idx = host_id
        else:
            btldr_data = BootloaderConnectIdChunk(host_id, ConnectIdChunkData.Protocol.BLE)
        # end if

        if connect_id_chunk_list is not None and len(connect_id_chunk_list) > 0:
            data = connect_id_chunk_list[-1].data
            data.host_index = host_id
            if is_test_setup:
                if hasattr(data, 'pairing_src_1'):
                    data.pairing_src_1 = ConnectIdChunkData.PairingSrc.NONE
                # end if
                if hasattr(data, 'scheme_host_1'):
                    data.scheme_host_1 = ConnectIdChunkData.STATUS.OOB
                # end if
                if hasattr(data, 'pairing_src_2'):
                    data.pairing_src_2 = ConnectIdChunkData.PairingSrc.NONE
                # end if
                if hasattr(data, 'scheme_host_2'):
                    data.scheme_host_2 = ConnectIdChunkData.STATUS.OOB
                # end if
            elif hasattr(data, f'pairing_src_{host_id}') and force_oob:
                setattr(data, f'pairing_src_{host_id}', ConnectIdChunkData.PairingSrc.NONE)
                setattr(data, f'scheme_host_{host_id}', ConnectIdChunkData.STATUS.OOB)
            # end if
        else:
            data = ConnectIdBlePro3HostsChunk(host_id,
                                              ConnectIdChunkData.PairingSrc.USR,
                                              ConnectIdChunkData.PairingSrc.NONE,
                                              ConnectIdChunkData.PairingSrc.NONE,
                                              ConnectIdChunkData.STATUS.BLE_PAIRED,
                                              ConnectIdChunkData.STATUS.OOB,
                                              ConnectIdChunkData.STATUS.OOB)
        # end if
        self.nvs_parser.add_new_chunk(chunk_id='NVS_BTLDR_CONNECT_ID', data=HexList(btldr_data))
        self.nvs_parser.add_new_chunk(chunk_id='NVS_CONNECT_ID', data=HexList(data))
    # end def switch_to_host_id

    def is_nvs_encrypted(self):
        """
        Check the presence of a local NVS AES encryption key.
        """
        return True if self.nvs_encryption_key is not None else False
    # end def is_nvs_encrypted

    def _set_nvs_encryption_key(self):
        """
        Extract the local NVS AES encryption key.
        """
        aes_local_key = self.debugger.readMemory(self.ADDRESS.NVS_ENCRYPTION_KEY, self.SIZE.NVS_ENCRYPTION_KEY)
        return aes_local_key if aes_local_key != HexList("FF" * self.SIZE.NVS_ENCRYPTION_KEY) else None
    # end def _set_nvs_encryption_key

    def get_nvs_encryption_key(self):
        """
        Return the local NVS AES encryption key.
        """
        return self.nvs_encryption_key
    # end def get_nvs_encryption_key

    def _customize_chunk_id_map(self, config_mgr):
        """
        Overload the content of the chunk id map used by a product

        :param config_mgr: Data manager from configuration file depending on context
        :type config_mgr: ``ConfigurationManagerInterface``
        """
        for index in range(len(config_mgr.get_feature(ConfigurationManagerInterface.ID.CHUNK_ID_NAMES))):
            name = config_mgr.get_feature(ConfigurationManagerInterface.ID.CHUNK_ID_NAMES)[index]
            self.chunk_id_map[name] = config_mgr.get_feature(ConfigurationManagerInterface.ID.CHUNK_ID_VALUES)[index]
        # end for
    # end def _customize_chunk_id_map
# end class MemoryManager


class DeviceMemoryManager(MemoryManager):
    """
    Device Memory Manager Implementation.
    """
    def __init__(self, debugger, config_mgr):
        """
        :param debugger: The debugger object to use to read memory
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        :param config_mgr: Data manager from configuration file depending on context
        :type config_mgr: ``ConfigurationManagerInterface``
        """
        super().__init__(debugger)

        self.chunk_type = MODE.DEVICE
        if debugger.MCU_NAME.startswith('STM32H7'):
            self.chunk_id_map = CHUNK_ID_MAP_STM32H7
        elif debugger.MCU_NAME.startswith('STM32L052'):
            self.chunk_id_map = CHUNK_ID_MAP_STM32L052
        else:
            self.chunk_id_map = CHUNK_ID_MAP_QUARK_GAMING if config_mgr.get_feature(
                ConfigurationManagerInterface.ID.CHUNK_ID_VARIANT) else CHUNK_ID_MAP_QUARK_CORE
        # end if
        self._customize_chunk_id_map(config_mgr)
        self.pairing_slot_count = 3
    # end def __init__

    def clean_pairing_data(self):
        # See ``MemoryManager.clean_pairing_data``
        self.read_nvs()
        chunk_name_list = ['NVS_BLE_PRO_PRE_PAIRING_ID_0']
        for pairing_slot in range(1, self.pairing_slot_count):
            chunk_name_list.append(f'NVS_BLE_BOND_ID_{pairing_slot}')
        # end for
        invalidated_chunk_count = self.invalidate_chunks(chunk_name_list)
        # Add new Connect_id and bootloader_connect_id chunks at the end of the NVS
        self.switch_to_host_id()
        invalidated_chunk_count += 2
        if invalidated_chunk_count > 0:
            self.load_nvs()
            return True
        # end if

        return False
    # end def clean_pairing_data
# end class DeviceMemoryManager


class ReceiverMemoryManager(MemoryManager):
    """
    Receiver Memory Manager Implementation.
    """
    def __init__(self, debugger, config_mgr):
        """
        :param debugger: The debugger object to use to read memory
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        :param config_mgr: Data manager from configuration file depending on context
        :type config_mgr: ``ConfigurationManagerInterface``
        """
        super().__init__(debugger)

        self.chunk_type = MODE.RECEIVER
        self.chunk_id_map = CHUNK_ID_MAP_RECEIVER
        self._customize_chunk_id_map(config_mgr)
        self.pairing_slot_count = 6
    # end def __init__

    def clean_pairing_data(self):
        # See ``MemoryManager.clean_pairing_data``
        self.read_nvs()
        chunk_name_list = []
        for pairing_slot in range(1, self.pairing_slot_count):
            chunk_name_list.append(f'NVS_BLE_BOND_ID_{pairing_slot}')
            chunk_name_list.append(f'NVS_BLE_BOND_INFO_ID_V0_{pairing_slot}')
            chunk_name_list.append(f'NVS_BLE_SYS_INFO_ID_{pairing_slot}')
            chunk_name_list.append(f'NVS_BLE_BOND_INFO_ID_{pairing_slot}')
        # end for
        invalidated_chunk_count = self.invalidate_chunks(chunk_name_list)
        if invalidated_chunk_count > 0:
            self.load_nvs()
            return True
        # end if

        return False
    # end def clean_pairing_data
# end class ReceiverMemoryManager


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
