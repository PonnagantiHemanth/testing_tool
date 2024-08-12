#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pylibrary.tools.nvsparser

@brief NVS parser classes

@author Stanislas Cottard

@date   2019/10/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import abc
import copy
import sys
import warnings
from enum import IntEnum
from enum import unique

from Crypto.Cipher import AES
from intelhex import IntelHex
from math import ceil

from pylibrary.mcu.backlightchunks import BacklightChunk
from pylibrary.mcu.connectchunks import BootloaderConnectIdChunk
from pylibrary.mcu.connectchunks import ConnectIdChunk
from pylibrary.mcu.devicefriendlynamechunks import DeviceFriendlyNameIdChunk
from pylibrary.mcu.factorychunks import TdeMfgAccessIdChunk
from pylibrary.mcu.kbdmasktablechunk import KbdMaskTableChunk
from pylibrary.mcu.nrf52.blenvschunks import DeviceBleBondId
from pylibrary.mcu.nrf52.blenvschunks import LastBluetoothAddress
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondId
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondInfoIdV0
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondInfoIdV1
from pylibrary.mcu.nrf52.bleproprepairingchunk import BleProPrePairingNvsChunk
from pylibrary.mcu.nrf52.blesysattrchunks import DeviceBleUserServices
from pylibrary.mcu.securitychunks import DfuCheckFwInfoChunk
from pylibrary.mcu.securitychunks import DfuCtrlChunk
from pylibrary.mcu.securitychunks import DfuRecoveryChunk
from pylibrary.mcu.securitychunks import TdeDeactivationChunk
from pylibrary.system.debugger import Debugger
from pylibrary.tools.aes import Aes
from pylibrary.tools.crc import Crc16ccitt
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
@unique
class MODE(IntEnum):
    """
    Modes values
    """
    DEVICE = 0
    RECEIVER = 1
# end class MODE

# CHUNK_ID_TO_CLASS_MAP = {
#     chunk_name: {
#         chunk_type: (is_encrypted, python representation class),
#         chunk_type: (is_encrypted, python representation class),
#     },


CHUNK_ID_TO_CLASS_MAP = {
    "NVS_TDE_MFG_ACCESS_ID": {
        MODE.DEVICE: (False, TdeMfgAccessIdChunk),
    },
    "NVS_DEVICE_FRIENDLY_NAME_ID": {
        MODE.DEVICE: (False, DeviceFriendlyNameIdChunk)
    },
    "NVS_XEE_DEACT_CNTR_ID": {
        MODE.RECEIVER: (False, TdeDeactivationChunk),
    },
    "NVS_X1E01_CONN_CNTR_ID": {
        MODE.DEVICE: (False, TdeDeactivationChunk),
    },
    "NVS_X1E02_STATE_ID": {
        MODE.DEVICE: (False, TdeDeactivationChunk),
        MODE.RECEIVER: (False, TdeDeactivationChunk),
    },
    "NVS_BLE_PRO_PRE_PAIRING_ID_0": {
        MODE.DEVICE: (True, BleProPrePairingNvsChunk),
    },
    "NVS_BLE_BOND_ID_0": {
        MODE.DEVICE: (True, DeviceBleBondId),
        MODE.RECEIVER: (True, ReceiverBleBondId),
    },
    "NVS_BLE_BOND_ID_1": {
        MODE.DEVICE: (True, DeviceBleBondId),
        MODE.RECEIVER: (True, ReceiverBleBondId),
    },
    "NVS_BLE_BOND_ID_2": {
        MODE.DEVICE: (True, DeviceBleBondId),
        MODE.RECEIVER: (True, ReceiverBleBondId),
    },
    "NVS_BLE_BOND_ID_3": {
        MODE.RECEIVER: (True, ReceiverBleBondId),
    },
    "NVS_BLE_BOND_ID_4": {
        MODE.RECEIVER: (True, ReceiverBleBondId),
    },
    "NVS_BLE_BOND_ID_5": {
        MODE.RECEIVER: (True, ReceiverBleBondId),
    },
    "NVS_BLE_BOND_INFO_ID_V0_0": {
        MODE.RECEIVER: (False, ReceiverBleBondInfoIdV0),
    },
    "NVS_BLE_BOND_INFO_ID_V0_1": {
        MODE.RECEIVER: (False, ReceiverBleBondInfoIdV0),
    },
    "NVS_BLE_BOND_INFO_ID_0": {
        MODE.RECEIVER: (False, ReceiverBleBondInfoIdV1),
    },
    "NVS_BLE_BOND_INFO_ID_1": {
        MODE.RECEIVER: (False, ReceiverBleBondInfoIdV1),
    },
    "NVS_BLE_SYS_ATTR_USR_SRVCS_ID_0": {
        MODE.DEVICE: (False, DeviceBleUserServices),
    },
    "NVS_BLE_SYS_ATTR_USR_SRVCS_ID_1": {
        MODE.DEVICE: (False, DeviceBleUserServices),
    },
    "NVS_BLE_SYS_ATTR_USR_SRVCS_ID_2": {
        MODE.DEVICE: (False, DeviceBleUserServices),
    },
    "NVS_BLE_LAST_GAP_ADDR_USED": {
        MODE.DEVICE: (False, LastBluetoothAddress),
    },
    "NVS_DFU_ID": {
        MODE.DEVICE: (False, DfuCtrlChunk),
        MODE.RECEIVER: (False, DfuCtrlChunk),
    },
    "NVS_DFU_CHECK_ID": {
        MODE.RECEIVER: (False, DfuCheckFwInfoChunk),
    },
    "NVS_BTLDR_CONNECT_ID": {
        MODE.DEVICE: (False, BootloaderConnectIdChunk),
    },
    "NVS_CONNECT_ID": {
        MODE.DEVICE: (False, ConnectIdChunk),
    },
    "NVS_DFU_OUT_OF_RECOVERY_ID": {
        MODE.DEVICE: (False, DfuRecoveryChunk),
    },
    "NVS_LEDBKLT_ID": {
        MODE.DEVICE: (False, BacklightChunk),
    },
    "NVS_KBD_MASK_TABLE_ID": {
        MODE.DEVICE: (False, KbdMaskTableChunk),
    },
}


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class NvsParserInterface(object, metaclass=abc.ABCMeta):
    """
    Defines the NVS parser interface.
    """
    MAX_CHUNK_DATA_SIZE = None
    CHUNK_ADDRESS_MASK = None

    def __init__(self, chunk_id_map):
        """
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
                             It must have at least the keys "ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"
                             which point to the full header, not just the ID.
        :type chunk_id_map: ``dict``
        """
        self.chunk_id_map = chunk_id_map
        self.nvs_word_size = chunk_id_map["NVS_WORD_SIZE"]
        self.nvs_chunk_method = chunk_id_map["NVS_CHUNK_METHOD"]
    # end def __init__

    @staticmethod
    @abc.abstractmethod
    def chunk_from_hex_array(array_to_parse, chunk_id_map):
        """
        Parse the first chunk of an hex array.
        This function is static to then be given to each new NvsChunk to have the right format.

        :param array_to_parse: The hex array to parse to get a chunk.
        :type array_to_parse: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        :param chunk_id_map: Map of chunk ids which also defines the NVS_WORD_SIZE
        :type chunk_id_map: ``dict``

        :return: The chunk object and the array_to_parse minus the chunk.
        :rtype: ``tuple``
        """
        raise NotImplementedError('users must define chunk_from_hex_array to use this base class')
    # end def chunk_from_hex_array

    @staticmethod
    @abc.abstractmethod
    def chunk_to_hex_array(chunk):
        """
        Format a chunk in an hex array.
        This function is static to then be given to each new NvsChunk to have the right format.

        :param chunk: The chunk to format.
        :type chunk: ``NvsChunk``

        :return: The hex array.
        :rtype: ``list``
        """
        raise NotImplementedError('users must define chunk_to_hex_array to use this base class')
    # end def chunk_to_hex_array

    @abc.abstractmethod
    def get_chunk(self, chunk_id, mode=None):
        """
        Get a chunk.

        :param chunk_id: ID of the chunk to get. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param mode: Mode of the owner of the NVS. If None, it will oly get the raw chunks (no decryption or special
                     classes). - OPTIONAL
        :type mode: ``MODE``

        :return: The wanted chunk.
        :rtype: ``NvsChunk`` or ``Chunk BitFieldContainerMixin object``
        """
        raise NotImplementedError('users must define read_chunk to use this base class')
    # end def get_chunk

    @abc.abstractmethod
    def add_new_chunk(self, chunk_id, data):
        """
        Add a new chunk.

        :param chunk_id: ID of the chunk to add. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param data: The chunk data to add.
        :type data: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        """
        raise NotImplementedError('users must define write_chunk to use this base class')
    # end def add_new_chunk

    @abc.abstractmethod
    def delete_chunk(self, chunk_id, data=None):
        """
        Delete a chunk.

        :param chunk_id: ID of the chunk to delete. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param data: The chunk data to delete. If no data are given, the last chunk with chunk_id is deleted. - OPTIONAL
        :type data: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        """
        raise NotImplementedError('users must define write_chunk to use this base class')
    # end def delete_chunk

    @abc.abstractmethod
    def get_chunk_history(self, chunk_id, mode=None, get_all=False, active_bank_only=False):
        """
        Get a chunk history.

        :param chunk_id: ID of the chunk to get. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param mode: Mode of the owner of the NVS. - OPTIONAL
        :type mode: ``MODE``
        :param get_all: Get all the chunks, even the chunk repeated from disabled bank to active bank - OPTIONAL
        :type get_all: ``bool``
        :param active_bank_only: Flag indicating to get the chunk history only from the active bank - OPTIONAL
        :type active_bank_only: ``bool``

        :return: The wanted chunk history.
        :rtype: ``list[NvsChunk|BitFieldContainerMixin]``
        """
        raise NotImplementedError('users must define get_chunk_history to use this base class')
    # end def get_chunk_history

    @abc.abstractmethod
    def is_last_chunk_id(self, chunk_id):
        """
        Check if the last chunk is of the wanted ID.

        :param chunk_id: ID of the wanted chunk. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``

        :return: True if the last chunk is of the wanted ID, False otherwise.
        :rtype: ``bool``
        """
        raise NotImplementedError('users must define is_last_chunk_id to use this base class')
    # end def is_last_chunk_id

    @abc.abstractmethod
    def diff(self, other, active_banks=True, delete=False):
        """
        Compare 2 NVS parsers

        :param other: Other NVS Parser
        :type other: ``NvsParser``
        :param active_banks: Flag to compare active banks only - OPTIONAL
        :type active_banks: ``bool``
        :param delete: Flag indicating if diff is requested after a delete operation - OPTIONAL
        :type delete: ``bool``

        :return: Differences between NVS parsers
        :rtype: ``dict``
        """
        raise NotImplementedError('users must define diff to use this base class')
    # end def diff
# end class NvsParserInterface


class IdBasedNvsParser(NvsParserInterface):
    """
    Define the Chunk ID Based NVS parser base class which requires the memory to be filled in with chunks.
    """
    ID_SIZE = 1
    LENGTH_SIZE = 1
    CRC_SIZE = 2
    LENGTH_INDEX = 1
    CRC_INDEX = 2
    MAX_CHUNK_DATA_SIZE = 256
    CHUNK_ADDRESS_MASK = 0xFF

    def __init__(self, chunk_id_map, zone_list, nvs_encryption_key=None):
        """
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
        :type chunk_id_map: ``dict``
        :param zone_list: The zone list pof the NVS memory.
        :type zone_list: ``list[NvsZone]``
        :param nvs_encryption_key: NVS AES encryption key. - OPTIONAL
        :type nvs_encryption_key: ``HexList`` or ``None``
        """
        super().__init__(chunk_id_map)

        self.zone_list = zone_list
        self.nvs_encryption_key = nvs_encryption_key
    # end def __init__

    @classmethod
    def from_memory_read(cls, debugger, nvs_start_address, nvs_size, zone_bank_length, chunk_id_map, aes_key=None):
        """
        Construct object from reading the memory of a device.

        :param debugger: The debugger object to use to read memory.
        :type debugger: ``Debugger``
        :param nvs_start_address: The start address of the NVS in memory.
        :type nvs_start_address: ``int``
        :param nvs_size: The size of the NVS in memory.
        :type nvs_size: ``int``
        :param zone_bank_length: The length of each bank in a zone, can be just one number for all zones or a list to
                                 give the length for each zone.
        :type zone_bank_length: ``int`` or ``list of int``
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
                             It must have at least the keys "ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"
                             which point to the full header, not just the ID.
        :type chunk_id_map: ``dict``
        :param aes_key: NVS AES encryption key (optional)
        :type aes_key: ``IntelHex``

        :return: The object created from the file.
        :rtype: ``NvsParser``
        """
        nvs_data = debugger.readMemory(nvs_start_address, nvs_size)
        nvs_addresses = range(nvs_start_address, nvs_start_address + nvs_size)

        return cls.from_hex_file(IntelHex(dict(zip(nvs_addresses, nvs_data))), zone_bank_length, chunk_id_map,
                                 aes_key)
    # end def from_memory_read

    @classmethod
    def from_hex_file(cls, hex_file, zone_bank_length, chunk_id_map, aes_key=None):
        """
        Construct object from file.

        :param hex_file: The hex file to parse, can be either a path or an IntelHex object.
        :type hex_file: ``str`` or ``IntelHex``
        :param zone_bank_length: The length of each bank in a zone, can be just one number for all zones or a list to
                                 give the length for each zone.
        :type zone_bank_length: ``int`` or ``list of int``
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
                             It must have at least the keys "ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"
                             which point to the full header, not just the ID.
        :type chunk_id_map: ``dict``
        :param aes_key: NVS AES encryption key. - OPTIONAL
        :type aes_key: ``IntelHex``

        :return: The object created from the file.
        :rtype: ``NvsParser``
        """
        # IntelHex constructor accept to use another IntelHex as source
        hex_file = IntelHex(hex_file)
        addresses_to_parse = hex_file.segments()
        zone_list = []

        # Every segment is parsed and then padded in NvsBank if needed
        for (start, stop) in addresses_to_parse:
            array_to_parse = hex_file.gets(addr=start, length=stop - start)
            index = 0
            while len(array_to_parse) > 0:
                bank_size = zone_bank_length
                if isinstance(zone_bank_length, list):
                    bank_size = zone_bank_length[index]
                    index += 1
                # end if
                zone, array_to_parse = NvsZone.from_hex_array(
                    array_to_parse=array_to_parse,
                    chunk_from_hex_array_method=cls.chunk_from_hex_array,
                    bank_length=bank_size,
                    zone_number=len(zone_list),
                    start_address=start,
                    chunk_id_map=chunk_id_map)
                zone_list.append(zone)
                start += bank_size * 2
            # end while
        # end for
        return cls(chunk_id_map, zone_list, HexList(aes_key))
    # end def from_hex_file

    def to_hex_file(self):
        """
        Convert this to an IntelHex object.

        :return: The hex_file object.
        :rtype: ``IntelHex``
        """
        hex_file = IntelHex()

        for zone in self.zone_list:
            hex_file.puts(addr=zone.start_address, s=bytes(zone.to_hex_array()))
        # end for
        return hex_file
    # end def to_hex_file

    @classmethod
    def chunk_from_hex_array(cls, array_to_parse, chunk_id_map):
        """
        Parse the first chunk of a hex array.

        :param array_to_parse: The hex array to parse to get a chunk.
        :type array_to_parse: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        :param chunk_id_map: Map of chunk ids which also defines the NVS_WORD_SIZE
        :type chunk_id_map: ``dict``

        :return: The chunk object and the array_to_parse minus the chunk.
        :rtype: ``tuple``
        """
        word_size = chunk_id_map["NVS_WORD_SIZE"]
        return_array = array_to_parse

        chunk_id = return_array[0]

        if (chunk_id & 0xFF) == 0xFF:
            # This is considered a padding chunk
            padding_length = 1
            for i in range(len(return_array) - 1):
                if return_array[i] != 0xFF:
                    break
                # end if
                padding_length += 1
            # end for
            return_array = return_array[padding_length:]
            return NvsChunk.create_a_padding_chunk(padding_length, word_size), return_array
        # end if

        chunk_length = return_array[cls.LENGTH_INDEX]
        chunk_crc = int.from_bytes(return_array[cls.CRC_INDEX:cls.CRC_INDEX + cls.CRC_SIZE],
                                   byteorder="little",
                                   signed=False)
        chunk_data = return_array[word_size:word_size + word_size * ceil(chunk_length / word_size)]
        return_array = return_array[word_size + word_size * ceil(chunk_length / word_size):]

        # The CRC check (would only generate a warning if mismatch) is not done for disabled bank header chunk
        if chunk_id != 0:
            crc_check = Crc16ccitt()
            crc_check.start_crc(list(chunk_data[:chunk_length]) + [chunk_id, chunk_length])
            if chunk_crc != crc_check.crc:
                warnings.warn(f"Error CRC for chunk_id = {hex(chunk_id)}: received = {hex(chunk_crc)} and "
                              f"computed = {hex(crc_check.crc)}")
            # end if
        # end if

        return NvsChunk(cls.chunk_to_hex_array, chunk_id, chunk_length, chunk_crc, chunk_data, word_size), return_array
    # end def chunk_from_hex_array

    @classmethod
    def chunk_to_hex_array(cls, chunk):
        """
        Format a chunk in a hex array.
        This function is static to then be given to each new NvsChunk to have the right format.

        :param chunk: The chunk to format.
        :type chunk: ``NvsChunk``

        :return: The hex array.
        :rtype: ``list``
        """
        return_array = [chunk.chunk_id]

        if chunk.chunk_length != -1 and chunk.chunk_crc != -1:
            return_array.append(chunk.chunk_length)
            return_array.extend(chunk.chunk_crc.to_bytes(cls.CRC_SIZE, byteorder="little", signed=False))
            return_array.extend([0] * (chunk.nvs_word_size - (cls.ID_SIZE + cls.LENGTH_SIZE + cls.CRC_SIZE)))
        # end if
        return_array.extend(chunk.chunk_data)

        return return_array
    # end def chunk_to_hex_array

    def get_chunk(self, chunk_id, mode=None):
        """
        Get the last value of a chunk in its history.

        :param chunk_id: ID of the chunk to get. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param mode: Mode of the owner of the NVS. If None, it will oly get the raw chunks (no decryption or special
                     classes). - OPTIONAL
        :type mode: ``MODE``

        :return: The wanted chunk.
        :rtype: ``NvsChunk``
        """
        chunk_list = self.get_chunk_history(chunk_id, mode)
        if len(chunk_list) > 0:
            return chunk_list[-1]
        else:
            return None
        # end if
    # end def get_chunk

    def _get_chunk_zone(self, chunk_id):
        """
        Get zone number of a chunk

        :param chunk_id: ID of the chunk
        :type chunk_id: ``int``

        :return: Zone number
        :rtype: ``int``
        """
        if len(self.zone_list) > 1:
            zone_number = (chunk_id >> 8) & self.CHUNK_ADDRESS_MASK
            assert zone_number <= len(self.zone_list)
        else:
            zone_number = 0
        # end if
        return zone_number
    # end def _get_chunk_zone

    def _get_encryption_and_class(self, chunk_id, mode=None):
        """
        Get encryption and class of a chunk.

        :param chunk_id: ID of the chunk.
        :type chunk_id: ``str``
        :param mode: Mode of the owner of the NVS. If None, it will only get the raw chunks (no decryption or special
                     classes). - OPTIONAL
        :type mode: ``MODE``

        :return: Chunk's encryption and class. Return default tuple (False, None) if not defined.
        :rtype: ``tuple``
        """
        chunk_name = self._get_chunk_id_name(chunk_id) if isinstance(chunk_id, int) else chunk_id
        return CHUNK_ID_TO_CLASS_MAP.get(chunk_name, {MODE.DEVICE: (False, None)}).get(mode, (False, None))
    # end def _get_encryption_and_class

    def get_chunk_history(self, chunk_id, mode=None, get_all=False, active_bank_only=False):
        """
        Retrieve all the values of a chunk from its history and decrypt the chunk data if it is encrypted

        :param chunk_id: ID of the chunk to get. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param mode: Mode of the owner of the NVS. If None, it will oly get the raw chunks (no decryption or special
                     classes). - OPTIONAL
        :type mode: ``MODE``
        :param get_all: Get all the chunks, even the chunk repeated from disabled bank to active bank - OPTIONAL
        :type get_all: ``bool``
        :param active_bank_only: Flag indicating to get the chunk history only from the active bank - OPTIONAL
        :type active_bank_only: ``bool``

        :return: The wanted chunk history.
        :rtype: ``list[NvsChunk|BitFieldContainerMixin]``
        """
        chunk_id = chunk_id if isinstance(chunk_id, int) else self.chunk_id_map[chunk_id]
        (is_encrypted, chunk_class) = self._get_encryption_and_class(chunk_id, mode)

        zone_number = self._get_chunk_zone(chunk_id)
        chunk_id &= self.CHUNK_ADDRESS_MASK
        active_bank_chunks = self.zone_list[zone_number].get_active_bank().get_chunk_history(chunk_id)

        if active_bank_only:
            chunk_history = active_bank_chunks
        else:
            disabled_bank_chunks = self.zone_list[zone_number].get_disabled_bank().get_chunk_history(chunk_id)
            if (len(disabled_bank_chunks) == 0 or len(active_bank_chunks) == 0 or get_all or
                    disabled_bank_chunks[-1] != active_bank_chunks[0]):
                chunk_history = disabled_bank_chunks + active_bank_chunks
            else:
                chunk_history = disabled_bank_chunks + active_bank_chunks[1:]
            # end if
        # end if

        return [self._get_chunk_bitfield_object_from_chunk(chunk, is_encrypted, chunk_class) for chunk in chunk_history]
    # end def get_chunk_history

    def get_chunk_name(self, chunk_id):
        """
        Get the name of a chunk in the chunk id map

        :param chunk_id: Chunk id
        :type chunk_id: ``int``

        :return: Chunk name
        :rtype: ``str``
        """
        chunk_names = [chunk_name for chunk_name, chunk_value in self.chunk_id_map.items()
                       if isinstance(chunk_value, int) and
                       chunk_value & self.CHUNK_ADDRESS_MASK == chunk_id & self.CHUNK_ADDRESS_MASK]
        return chunk_names[0] if len(chunk_names) > 0 else None
    # end def get_chunk_name

    def add_new_chunk(self, chunk_id, data, is_encrypted=False, iv=None):
        """
        Add a new chunk.

        :param chunk_id: ID of the chunk to add. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param data: The chunk data to add.
        :type data: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        :param is_encrypted: Flag enabling the aes encryption - OPTIONAL
        :type is_encrypted: ``bool``
        :param iv: AES initialization vector - OPTIONAL
        :type iv: ``bytes``
        """
        assert len(data) < self.MAX_CHUNK_DATA_SIZE, "Data too big"
        platform_chunk_id = chunk_id if isinstance(chunk_id, int) else self.chunk_id_map[chunk_id]

        zone_number = self._get_chunk_zone(platform_chunk_id)
        platform_chunk_id &= self.CHUNK_ADDRESS_MASK
        active_bank = self.zone_list[zone_number].get_active_bank()
        new_chunk = NvsChunk(to_hex_array_method=self.chunk_to_hex_array,
                             chunk_id=platform_chunk_id,
                             chunk_length=len(data),
                             chunk_crc=0,
                             chunk_data=data,
                             nvs_word_size=self.nvs_word_size)

        # Manage data encryption
        if is_encrypted and self.nvs_encryption_key is not None:
            new_chunk.iv = iv
            ciphered_data = self.encrypt_chunk(new_chunk, self.nvs_encryption_key)
            new_chunk.chunk_length = len(ciphered_data)
        # end if

        # Compute external crc
        new_chunk_crc = Crc16ccitt()
        new_chunk_crc.start_crc(list(new_chunk.chunk_data) + [platform_chunk_id, len(new_chunk.chunk_data)])
        new_chunk.chunk_crc = new_chunk_crc.crc
        if len(new_chunk.chunk_data) % self.nvs_word_size != 0:
            new_chunk.chunk_data = list(new_chunk.chunk_data) + (
                    [0] * (self.nvs_word_size - (len(new_chunk.chunk_data) % self.nvs_word_size)))
        # end if

        if active_bank.get_current_length() + len(data) + self.nvs_word_size > active_bank.bank_length:
            # The bank is too full to add this new chunk, copy and switch bank
            sys.stdout.write("The bank is too full to add this new chunk\n")
            disabled_bank = self.zone_list[zone_number].get_disabled_bank()

            # Copy all valid chunks including the first chunk with ACTIVE_BANK_HDR
            disabled_bank.chunks = self.get_chunks_to_copy(active_bank, new_chunk)
            disabled_bank.active = True
            disabled_bank.add_padding()

            # Disable the other bank
            active_bank.active = False
            active_bank.chunks[0].chunk_id = self.chunk_id_map["INVALID_BANK_HDR"][0]
            active_bank.chunks[0].chunk_length = self.chunk_id_map["INVALID_BANK_HDR"][1]
            active_bank.chunks[0].chunk_crc = self.chunk_id_map["INVALID_BANK_HDR"][2]
        else:
            active_bank.add_chunk(new_chunk)
        # end if
    # end def add_new_chunk

    def get_chunks_to_copy(self, active_bank, new_chunk):
        """
        Get chunks to copy from active bank to disabled bank when the active bank is too full to add the new chunk and
        a switch of bank is needed.

        :param active_bank: Currently active bank
        :type active_bank: ``NvsBank``
        :param new_chunk: New chunk to add
        :type new_chunk: ``NvsChunk``

        :return: Chunks to copy
        :rtype: ``list[NvsChunk]``
        """
        chunks_to_copy = []
        for chunk in active_bank.chunks:
            if (chunk.chunk_id in [new_chunk.chunk_id, self.chunk_id_map["NVS_INVALID_CHUNK_ID"]]) or \
                    (chunk.chunk_length == -1 and chunk.chunk_crc == -1):
                # Skip the copy if it matches the chunk ID to add, an invalid chunk or the padding
                continue
            # end if

            first_occurrence_id = True
            for i in range(len(chunks_to_copy)):
                if chunk.chunk_id == chunks_to_copy[i].chunk_id:
                    first_occurrence_id = False
                    chunks_to_copy[i] = copy.deepcopy(chunk)
                    break
                # end if
            # end for

            if first_occurrence_id:
                chunks_to_copy.append(copy.deepcopy(chunk))
            # end if
        # end for

        chunks_to_copy.append(new_chunk)
        return chunks_to_copy
    # end def get_chunks_to_copy

    def delete_chunk(self, chunk_id, data=None):
        """
        Delete a chunk. The way to delete a chunk in this platform is to change the chunk_id to NVS_INVALID_CHUNK_ID.

        :param chunk_id: ID of the chunk to delete. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param data: The chunk data to delete. If no data are given, the last chunk with chunk_id is deleted. - OPTIONAL
        :type data: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        """
        if isinstance(chunk_id, int):
            platform_chunk_id = chunk_id
        else:
            platform_chunk_id = self.chunk_id_map[chunk_id]
        # end if

        zone_number = self._get_chunk_zone(platform_chunk_id)
        platform_chunk_id &= self.CHUNK_ADDRESS_MASK
        active_bank = self.zone_list[zone_number].get_active_bank()

        last_chunk_index = None
        for i in range(len(active_bank.chunks)):
            if platform_chunk_id == active_bank.chunks[i].chunk_id:
                last_chunk_index = i

                if data is not None and active_bank.chunks[i].chunk_data == data:
                    active_bank.chunks[i].chunk_id = self.chunk_id_map["NVS_INVALID_CHUNK_ID"]
                    return
                # end if
            # end if
        # end for

        # If the code arrive here, either data=None or the specific chunk has not been found, which should raise
        # an error
        assert data is None, "Could not find chunk with specific data to delete"

        if last_chunk_index is not None:
            active_bank.chunks[last_chunk_index].chunk_id = self.chunk_id_map["NVS_INVALID_CHUNK_ID"]
        # end if
    # end def delete_chunk

    def delete_all_chunks(self, chunk_id):
        """
        Delete all chunks matching the given id. The way to delete a chunk in this platform is to change the
        chunk_id to NVS_INVALID_CHUNK_ID.

        :param chunk_id: ID of the chunk to delete. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        """
        if isinstance(chunk_id, int):
            platform_chunk_id = chunk_id
        else:
            platform_chunk_id = self.chunk_id_map[chunk_id]
        # end if

        zone_number = self._get_chunk_zone(platform_chunk_id)
        platform_chunk_id &= self.CHUNK_ADDRESS_MASK
        active_bank = self.zone_list[zone_number].get_active_bank()
        for i in range(len(active_bank.chunks)):
            if platform_chunk_id == active_bank.chunks[i].chunk_id:
                active_bank.chunks[i].chunk_id = self.chunk_id_map["NVS_INVALID_CHUNK_ID"]
            # end if
        # end for

        disabled_bank = self.zone_list[zone_number].get_disabled_bank()
        for i in range(len(disabled_bank.chunks)):
            if platform_chunk_id == disabled_bank.chunks[i].chunk_id:
                disabled_bank.chunks[i].chunk_id = self.chunk_id_map["NVS_INVALID_CHUNK_ID"]
            # end if
        # end for
    # end def delete_all_chunks

    def copy_chunks(self, other_nvs_parser, chunk_ids):
        """
        Copy chunks from another NVS parser

        :param other_nvs_parser: Other NVS parser
        :type other_nvs_parser: ``NvsParser``
        :param chunk_ids: List of chunk ids to copy
        :type chunk_ids: ``list[int]``
        """
        for zone in other_nvs_parser.zone_list:
            active_bank = zone.get_active_bank()
            for chunk in active_bank.chunks:
                if (chunk.chunk_id & self.CHUNK_ADDRESS_MASK) in chunk_ids:
                    local_chunk = self.get_chunk(self.get_chunk_name(chunk.chunk_id))
                    if local_chunk is not None:
                        local_chunk.chunk_data = chunk.chunk_data
                        local_chunk.chunk_crc = chunk.chunk_crc
                        local_chunk.chunk_length = chunk.chunk_length
                    else:
                        self.add_new_chunk(self.get_chunk_name(chunk.chunk_id), chunk.chunk_data[0:chunk.chunk_length])
                    # end if
                # end if
            # end for
        # end for
    # end def copy_chunks

    def copy_pairing(self, other_nvs_parser):
        """
        Copy EQuad pairing info from another NVS parser

        :param other_nvs_parser: Other NVS parser
        :type other_nvs_parser: ``NvsParser``
        """
        pairing_info_chunk_ids = [
            value & self.CHUNK_ADDRESS_MASK for value in self.chunk_id_map.values() if isinstance(value, int) and
            self.chunk_id_map["NVS_EQUAD_H0_ADDR_ID"] <= value <= self.chunk_id_map["NVS_EQUAD_H7_PAIRING_SRC_ID"]]
        pairing_info_chunk_ids.extend([
            value & self.CHUNK_ADDRESS_MASK for value in self.chunk_id_map.values() if isinstance(value, int) and
            self.chunk_id_map["NVS_BLE_BOND_ID_0"] <= value <= self.chunk_id_map["NVS_BLE_LAST_GAP_ADDR_USED"]])
        pairing_info_chunk_ids.append(self.chunk_id_map["NVS_BTLDR_CONNECT_ID"] & self.CHUNK_ADDRESS_MASK)
        pairing_info_chunk_ids.append(self.chunk_id_map["NVS_CONNECT_ID"] & self.CHUNK_ADDRESS_MASK)
        self.copy_chunks(other_nvs_parser, pairing_info_chunk_ids)
    # end def copy_pairing

    def is_last_chunk_id(self, chunk_id):
        """
        Check if the last chunk is of the wanted ID.

        :param chunk_id: ID of the wanted chunk. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``

        :return: True if the last chunk is of the wanted ID, False otherwise.
        :rtype: ``bool``
        """
        if isinstance(chunk_id, int):
            platform_chunk_id = chunk_id
        else:
            platform_chunk_id = self.chunk_id_map[chunk_id]
        # end if

        zone_number = self._get_chunk_zone(platform_chunk_id)
        platform_chunk_id &= self.CHUNK_ADDRESS_MASK
        chunks = self.zone_list[zone_number].get_active_bank().chunks

        last_chunk = chunks[-1]
        chunks = chunks[:-1]
        while last_chunk.chunk_length == -1 and last_chunk.chunk_crc == -1:
            last_chunk = chunks[-1]
            chunks = chunks[:-1]
        # end while

        return last_chunk.chunk_id == platform_chunk_id
    # end def is_last_chunk_id

    def print_nvs(self, mode=None, log_file_path=None):
        """
        Print the processed NVS.

        :param mode: Mode of the owner of the NVS. If None, it will oly get the raw chunks (no decryption or special
                     classes). - OPTIONAL
        :type mode: ``MODE``
        :param log_file_path: Path to the log file. If None, the NVS will be printed on the console. - OPTIONAL
        :type log_file_path: ``str``
        """
        log_file = None
        default_std_out = sys.stdout

        try:
            if log_file_path is not None:
                log_file = open(log_file_path, "w")
                sys.stdout = log_file
            # end if

            for zone in self.zone_list:
                print(f"==================== Zone {zone.zone_number} at {'0x{:08X}'.format(zone.start_address)} "
                      f"====================")

                active_bank = zone.get_active_bank()
                if active_bank is None:
                    continue
                # end if
                print(f"\t================== Active Bank at {'0x{:08X}'.format(active_bank.start_address)} "
                      f"==================")
                for chunk in active_bank.chunks:
                    # if chunk.chunk_length == -1 and chunk.chunk_crc == -1:
                    #     # Do not print padding
                    #     continue
                    # # end if

                    (is_encrypted, chunk_class) = self._get_encryption_and_class(chunk.chunk_id, mode)

                    chunk_to_print = self._get_chunk_bitfield_object_from_chunk(chunk, is_encrypted, chunk_class)

                    if isinstance(chunk_to_print, NvsChunk):
                        print(f"\t\tChunk ID : {self._get_chunk_id_name(chunk.chunk_id)} " +
                              "(0x{:02X})".format(chunk.chunk_id))
                        print(f"\t\tChunk length : {hex(chunk.chunk_length)}")
                        print(f"\t\tChunk CRC : {hex(chunk.chunk_crc)}")
                        print(f"\t\tChunk data : {list(chunk.chunk_data)}")
                    else:
                        str_to_print = f"\t\tChunk ID : {self._get_chunk_id_name(chunk.chunk_id)} " + \
                                       "(0x{:02X})\n\t\t".format(chunk.chunk_id) + \
                                       str(chunk_to_print).replace('\n', '\n\t\t')
                        print(str_to_print)
                    # end if
                    print("\t\t--------------------\n")
                # end for

                disabled_bank = zone.get_disabled_bank()
                print(f"\t================== Disabled Bank at {'0x{:08X}'.format(disabled_bank.start_address)} "
                      f"==================")
                for chunk in disabled_bank.chunks:
                    # if chunk.chunk_length == -1 and chunk.chunk_crc == -1:
                    #     # Do not print padding
                    #     continue
                    # # end if

                    (is_encrypted, chunk_class) = self._get_encryption_and_class(chunk.chunk_id, mode)

                    chunk_to_print = self._get_chunk_bitfield_object_from_chunk(chunk, is_encrypted, chunk_class)

                    if isinstance(chunk_to_print, NvsChunk):
                        print(f"\t\tChunk ID : {self._get_chunk_id_name(chunk.chunk_id)} " +
                              "(0x{:02X})".format(chunk.chunk_id))
                        print(f"\t\tChunk length : {hex(chunk.chunk_length)}")
                        print(f"\t\tChunk CRC : {hex(chunk.chunk_crc)}")
                        print(f"\t\tChunk data : {list(chunk.chunk_data)}")
                    else:
                        str_to_print = '\t\t' + str(chunk_to_print).replace('\n', '\t\t\n')
                        print(str_to_print)
                    # end if
                    print("\t\t--------------------\n")
                # end for
            # end for
        finally:
            if log_file is not None:
                log_file.close()
                sys.stdout = default_std_out
            # end if
        # end try
    # end def print_nvs

    def _get_chunk_id_name(self, chunk_id):
        """
        Get the name of a chunk from its ID.

        :param chunk_id:  ID of the wanted chunk.
        :type chunk_id: ``int``

        :return: The name of the chunk.
        :rtype: ``str``
        """
        name_index = 0
        for value_id in self.chunk_id_map.values():
            if (isinstance(value_id, int) and
                    (value_id & self.CHUNK_ADDRESS_MASK) == (chunk_id & self.CHUNK_ADDRESS_MASK)):
                return list(self.chunk_id_map.keys())[name_index]
            # end if
            name_index += 1
        # end for

        return "NVS_UNKNOWN_ID"
    # end def _get_chunk_id_name

    def _get_chunk_bitfield_object_from_chunk(self, chunk, is_encrypted, chunk_class):
        """
        Get the Bitfield object of a chunk if possible.

        :param chunk: Chunk to format to a Bitfield object.
        :type chunk: ``NvsChunk``
        :param is_encrypted: True if the chunk is encrypted, False otherwise.
        :type is_encrypted: ``bool``
        :param chunk_class: The Bitfield class to use.
        :type chunk_class: ``BitFieldContainerMixin``

        :return: The Bitfield object if possible or the chunk itself if not.
        :rtype: ``BitFieldContainerMixin``
        """
        if chunk_class is None:
            chunk_to_return = chunk
        elif is_encrypted:
            if self.nvs_encryption_key is not None:
                self.decrypt_chunk(chunk, self.nvs_encryption_key)
                chunk_to_return = chunk_class.fromHexList(HexList(chunk.clear_data[:chunk.chunk_length]))
                chunk_to_return.ref = chunk
            else:
                # If the encryption key is not specified, only the NvsChunk is used
                chunk_to_return = chunk
            # end if
        else:
            chunk_to_return = chunk_class.fromHexList(HexList(chunk.clear_data[:chunk.chunk_length]))
            chunk_to_return.ref = chunk
        # end if

        return chunk_to_return
    # end def _get_chunk_bitfield_object_from_chunk

    @classmethod
    def decrypt_chunk(cls, chunk, aes_key):
        """
        Decrypt the encrypted data.

        :param chunk: chunk to encrypt.
        :type chunk: ``NvsChunk``
        :param aes_key: AES encryption key stored in UICR.
        :type aes_key: ``HexList``

        :return: Decrypted data.
        :rtype: ``HexList``
        """
        chunk.iv = chunk.chunk_data[:AES.block_size]
        if (chunk.chunk_length % 4) != 0:
            chunk.padding_bytes = chunk.chunk_data[-(4 - (chunk.chunk_length % 4)):]
        # end if
        clear_buffer = Aes.aes_cipher(data=HexList(chunk.chunk_data[:chunk.chunk_length]), key=aes_key, encrypt=False)
        clear_data_length = chunk.chunk_length - AES.block_size - cls.CRC_SIZE
        chunk.clear_data = clear_buffer[:clear_data_length]
        chunk.internal_crc = int.from_bytes(clear_buffer[clear_data_length:clear_data_length + cls.CRC_SIZE],
                                            byteorder="little", signed=False)
        crc_check = Crc16ccitt()
        crc_check.start_crc(list(chunk.clear_data))
        if chunk.internal_crc != crc_check.crc:
            warnings.warn(f"Error internal CRC for chunk_id = {hex(chunk.chunk_id)}: received ="
                          f" {hex(chunk.internal_crc)} and computed = {hex(crc_check.crc)}")
        # end if
        return chunk.clear_data
    # end def decrypt_chunk

    @classmethod
    def encrypt_chunk(cls, chunk, aes_key):
        """
        Encrypt the chunk data.

        :param chunk: chunk to encrypt.
        :type chunk: ``NvsChunk``
        :param aes_key: AES encryption key stored in UICR.
        :type aes_key: ``HexList``

        :return: Decrypted data.
        :rtype: ``HexList``
        """
        crc_check = Crc16ccitt()
        crc_check.start_crc(list(chunk.clear_data))
        crc = crc_check.crc.to_bytes(cls.CRC_SIZE, byteorder="little", signed=False)
        clear_buffer = chunk.clear_data + crc
        chunk.chunk_data = Aes.aes_cipher(data=clear_buffer, key=aes_key, encrypt=True, iv=chunk.iv)
        if chunk.padding_bytes is not None:
            chunk.chunk_data += chunk.padding_bytes
        # end if

        return chunk.chunk_data
    # end def encrypt_chunk

    def diff(self, other, active_banks=True, delete=False):
        # See ``NvsParserInterface.diff``
        attrs = ["nvs_encryption_key", "chunk_id_map"]
        attrs_diff = [attr for attr in attrs if getattr(self, attr) != getattr(other, attr)]
        diff = {
            "parsers": (self, other),
            "attrs": attrs_diff,
            "zones": []
        } if attrs_diff else {}

        for zone_index in range(max(len(self.zone_list), len(other.zone_list))):
            my_zone = self.zone_list[zone_index] if zone_index < len(self.zone_list) else None
            other_zone = other.zone_list[zone_index] if zone_index < len(other.zone_list) else None
            if my_zone is not None and other_zone is not None:
                zone_diff = my_zone.diff(other_zone, active_banks, delete=delete)
            else:
                zone_diff = {"zones": (my_zone, other_zone), "attrs": [], "banks": []}
            # end if
            if diff and zone_diff:
                diff["zones"].append(zone_diff)
            elif zone_diff:
                diff = {"parsers": (self, other), "attrs": [], "zones": [zone_diff]}
            # end if
        # end for
        return diff
    # end def diff

    def get_changed_chunks(self, other, delete=False):
        """
        Get chunks which have changed from a NVS Parser to another

        :param other: Other NVS Parser
        :type other: ``NvsParser``
        :param delete: Flag indicating if the method is called after a delete operation - OPTIONAL
        :type delete: ``bool``

        :return: List of changed chunks
        :rtype: ``list[(NvsChunk, NvsChunk)]``
        """
        diff = self.diff(other, delete=delete)
        changed_chunks = []
        for zone_diff in diff["zones"]:
            for bank_diff in zone_diff["banks"]:
                for chunk_diff in bank_diff["chunks"]:
                    changed_chunks.append(chunk_diff["chunks"])
                # end for
            # end for
        # end for
        return changed_chunks
    # end def get_changed_chunks

    def get_active_bank_status(self, chunk_id):
        """
        Get the active bank characterisitcs of the zone in which the given chunk id is found.

        :param chunk_id: ID of the wanted chunk. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``

        :return: The active bank id, used space size and total bank size
        :rtype: ``tuple[int, int, int]``
        """
        platform_chunk_id = chunk_id if isinstance(chunk_id, int) else self.chunk_id_map[chunk_id]

        zone_number = self._get_chunk_zone(platform_chunk_id)
        active_bank = self.zone_list[zone_number].get_active_bank()
        active_bank_id = self.zone_list[zone_number].banks.index(active_bank)
        current_length = active_bank.get_current_length()
        total_length = active_bank.bank_length
        return active_bank_id, current_length, total_length
    # end def get_active_bank_status
# end class IdBasedNvsParser


class AddressBasedNvsParser(IdBasedNvsParser):
    """
    Define the Address based NVS parser base class which requires the memory to be filled in with data and CRC.
    """
    CRC_SIZE = 2
    CHUNK_ADDRESS_MASK = 0xFFF

    def __init__(self, chunk_id_map, zone_list, nvs_encryption_key=None):
        """
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
        :type chunk_id_map: ``dict``
        :param zone_list: The zone list pof the NVS memory.
        :type zone_list: ``list[NvsZone]``
        :param nvs_encryption_key: NVS AES encryption key. - OPTIONAL
        :type nvs_encryption_key: ``HexList`` or ``None``
        """
        super().__init__(chunk_id_map, zone_list, nvs_encryption_key)

        self.zone_list = zone_list
        self.nvs_encryption_key = nvs_encryption_key
    # end def __init__

    def _get_chunk_id_name(self, chunk_id):
        """
        Get the name of a chunk from its ID.

        :param chunk_id:  ID of the wanted chunk.
        :type chunk_id: ``int``

        :return: The name of the chunk.
        :rtype: ``str``
        """
        name_index = 0
        for value_id in self.chunk_id_map.values():
            if (isinstance(value_id, list) and
                    isinstance(value_id[0], int) and
                    (value_id[0] & self.CHUNK_ADDRESS_MASK) == (chunk_id & self.CHUNK_ADDRESS_MASK)):
                return list(self.chunk_id_map.keys())[name_index]
            # end if
            name_index += 1
        # end for

        return "NVS_UNKNOWN_ID"
    # end def _get_chunk_id_name

    def _get_encryption_and_class(self, chunk_id, mode=None):
        """
        Get encryption and class of a chunk.

        :param chunk_id: ID of the chunk.
        :type chunk_id: ``str``
        :param mode: Mode of the owner of the NVS. If None, it will only get the raw chunks (no decryption or special
                     classes). - OPTIONAL
        :type mode: ``MODE``

        :return: Chunk's encryption and class. Return default tuple (False, None) if not defined.
        :rtype: ``tuple``
        """
        chunk_name = self._get_chunk_id_name(chunk_id) if isinstance(chunk_id, int) else chunk_id
        return CHUNK_ID_TO_CLASS_MAP.get(chunk_name, {MODE.DEVICE: (False, None)}).get(mode, (False, None))
    # end def _get_encryption_and_class

    @classmethod
    def from_hex_file(cls, hex_file, zone_bank_length, chunk_id_map, aes_key=None):
        """
        Construct object from file.

        :param hex_file: The hex file to parse, can be either a path or an IntelHex object.
        :type hex_file: ``str`` or ``IntelHex``
        :param zone_bank_length: The length of each bank in a zone, can be just one number for all zones or a list to
                                 give the length for each zone.
        :type zone_bank_length: ``int`` or ``list of int``
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
                             It must have at least the keys "ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"
                             which point to the full header, not just the ID.
        :type chunk_id_map: ``dict``
        :param aes_key: NVS AES encryption key. - OPTIONAL
        :type aes_key: ``IntelHex``

        :return: The object created from the file.
        :rtype: ``NvsParser``
        """
        # IntelHex constructor accept to use another IntelHex as source
        hex_file = IntelHex(hex_file)
        addresses_to_parse = hex_file.segments()
        zone_list = []

        # Every segment is parsed and then padded in NvsBank if needed
        for (start, stop) in addresses_to_parse:
            array_to_parse = hex_file.gets(addr=start, length=stop - start)
            index = 0
            bank_size = zone_bank_length
            if isinstance(zone_bank_length, list):
                bank_size = zone_bank_length[index]
                index += 1
            # end if
            zone, array_to_parse = NvsZone.from_hex_array(
                array_to_parse=array_to_parse,
                chunk_from_hex_array_method=cls.chunk_from_hex_array,
                bank_length=bank_size,
                zone_number=len(zone_list),
                start_address=start,
                chunk_id_map=chunk_id_map)
            zone_list.append(zone)
        # end for
        return cls(chunk_id_map, zone_list, HexList(aes_key))
    # end def from_hex_file

    def to_hex_file(self):
        """
        Convert this to an IntelHex object.

        :return: The hex_file object.
        :rtype: ``IntelHex``
        """
        hex_file = IntelHex()
        for zone in self.zone_list:
            if zone is not None:
                hex_file.puts(addr=zone.start_address, s=bytes(zone.to_hex_array()))
            # end if
        # end for
        return hex_file
    # end def to_hex_file

    @classmethod
    def chunk_from_hex_array(cls, array_to_parse, chunk_id_map):
        """
        Parse the first chunk of a hex array.

        :param array_to_parse: The hex array to parse to get a chunk.
        :type array_to_parse: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        :param chunk_id_map: Map of chunk ids which also defines the NVS_WORD_SIZE
        :type chunk_id_map: ``dict``

        :return: The chunk object and the array_to_parse minus the chunk.
        :rtype: ``tuple``
        """
        word_size = chunk_id_map["NVS_WORD_SIZE"]
        chunks = []
        prev_chunk_crc_end_address = 0
        filtered_dict = {k: v for k, v in chunk_id_map.items() if
                         k not in ["NVS_CHUNK_METHOD", "NVS_WORD_SIZE", "NVS_ACTIVE_BANK_ID", "NVS_EMPTY_CHUNK_ID",
                                   "NVS_INVALID_CHUNK_ID", "ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"]}

        for nvs_name, (chunk_start_address, chunk_crc_start_address) in filtered_dict.items():
            chunk_length = chunk_crc_start_address - chunk_start_address
            chunk_crc = int.from_bytes(array_to_parse[chunk_crc_start_address:chunk_crc_start_address + cls.CRC_SIZE],
                                       byteorder="little",
                                       signed=False)
            chunk_data = array_to_parse[chunk_start_address:chunk_start_address + chunk_length]
            if 0 < prev_chunk_crc_end_address < chunk_start_address:
                # This is treated as a padding chunk, and we add 1 to the length to adjust for the missing chunk header
                padding_length = chunk_start_address - prev_chunk_crc_end_address + 1
                chunks.append(NvsChunk.create_zero_padding_chunk(padding_length, word_size))
            # end if
            chunks.append(NvsChunk(
                cls.chunk_to_hex_array, chunk_start_address, chunk_length, chunk_crc, chunk_data, word_size))
            # end if
            prev_chunk_crc_end_address = chunk_crc_start_address + cls.CRC_SIZE
        # end for
        if prev_chunk_crc_end_address < len(array_to_parse):
            padding_length = len(array_to_parse) - prev_chunk_crc_end_address
            chunks.append(NvsChunk.create_zero_padding_chunk(padding_length, word_size))
        # end if
        return chunks, []
    # end def chunk_from_hex_array

    @classmethod
    def chunk_to_hex_array(cls, chunk):
        """
        Format a chunk in a hex array.
        This function is static to then be given to each new NvsChunk to have the right format.

        :param chunk: The chunk to format.
        :type chunk: ``NvsChunk``

        :return: The hex array.
        :rtype: ``list``
        """
        return_array = []
        if chunk.chunk_length != -1 and chunk.chunk_crc != -1:
            return_array.extend(chunk.chunk_data)
            return_array.extend(chunk.chunk_crc.to_bytes(cls.CRC_SIZE, byteorder="little", signed=False))
        # end if

        return return_array
    # end def chunk_to_hex_array

    def get_chunk_history(self, chunk_id, mode=None, get_all=False, active_bank_only=False):
        """
        Retrieve all the values of a chunk from its history and decrypt the chunk data if it is encrypted

        :param chunk_id: ID of the chunk to get. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param mode: Mode of the owner of the NVS. If None, it will oly get the raw chunks (no decryption or special
                     classes). - OPTIONAL
        :type mode: ``MODE``
        :param get_all: Get all the chunks, even the chunk repeated from disabled bank to active bank - OPTIONAL
        :type get_all: ``bool``
        :param active_bank_only: Flag indicating to get the chunk history only from the active bank - OPTIONAL
        :type active_bank_only: ``bool``

        :return: The wanted chunk history.
        :rtype: ``list[NvsChunk|BitFieldContainerMixin]``
        """
        chunk_id = chunk_id if isinstance(chunk_id, int) else self.chunk_id_map[chunk_id][0]
        (is_encrypted, chunk_class) = self._get_encryption_and_class(chunk_id, mode)

        zone_number = self._get_chunk_zone(chunk_id)
        chunk_id &= self.CHUNK_ADDRESS_MASK
        active_bank_chunks = self.zone_list[zone_number].get_active_bank().get_chunk_history(chunk_id)

        if len(self.zone_list[zone_number].get_valid_banks()) > 1 and not active_bank_only:
            disabled_bank_chunks = self.zone_list[zone_number].get_disabled_bank().get_chunk_history(chunk_id)
            if (len(disabled_bank_chunks) == 0 or len(active_bank_chunks) == 0 or get_all or
                    disabled_bank_chunks[-1] != active_bank_chunks[0]):
                chunk_history = disabled_bank_chunks + active_bank_chunks
            else:
                chunk_history = disabled_bank_chunks + active_bank_chunks[1:]
            # end if
        else:
            chunk_history = active_bank_chunks
        # end if

        return [self._get_chunk_bitfield_object_from_chunk(chunk, is_encrypted, chunk_class) for chunk in chunk_history]
    # end def get_chunk_history

    def add_new_chunk(self, chunk_id, data, is_encrypted=False, iv=None):
        """
        Add a new chunk.

        :param chunk_id: ID of the chunk to add. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param data: The chunk data to add.
        :type data: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        :param is_encrypted: Flag enabling the aes encryption - OPTIONAL
        :type is_encrypted: ``bool``
        :param iv: AES initialization vector - OPTIONAL
        :type iv: ``bytes``
        """
        assert len(data) < self.MAX_CHUNK_DATA_SIZE, "Data too big"
        platform_chunk_address, platform_chunk_length = (chunk_id, len(data)) if isinstance(chunk_id, int) \
        else (self.chunk_id_map[chunk_id][0], self.chunk_id_map[chunk_id][1]-self.chunk_id_map[chunk_id][0])
        data.extend([0] * (platform_chunk_length - len(data)))
        zone_number = self._get_chunk_zone(platform_chunk_address)
        platform_chunk_address &= self.CHUNK_ADDRESS_MASK
        active_bank = self.zone_list[zone_number].get_active_bank()
        new_chunk = NvsChunk(to_hex_array_method=self.chunk_to_hex_array,
                             chunk_id=platform_chunk_address,
                             chunk_length=platform_chunk_length,
                             chunk_crc=0,
                             chunk_data=data,
                             nvs_word_size=self.nvs_word_size)

        # Manage data encryption
        if is_encrypted and self.nvs_encryption_key is not None:
            new_chunk.iv = iv
            ciphered_data = self.encrypt_chunk(new_chunk, self.nvs_encryption_key)
            new_chunk.chunk_length = len(ciphered_data)
        # end if

        # Compute external crc
        new_chunk_crc = Crc16ccitt()
        new_chunk_crc.start_crc(list(new_chunk.chunk_data) + [platform_chunk_address, len(new_chunk.chunk_data)])
        new_chunk.chunk_crc = new_chunk_crc.crc

        if active_bank.get_current_length() + len(data) + self.nvs_word_size > active_bank.bank_length:
            # The bank is too full to add this new chunk, copy and switch bank
            sys.stdout.write("The bank is too full to add this new chunk\n")
            disabled_bank = self.zone_list[zone_number].get_disabled_bank()

            # Copy all valid chunks including the first chunk with ACTIVE_BANK_HDR
            disabled_bank.chunks = self.get_chunks_to_copy(active_bank, new_chunk)
            disabled_bank.active = True
            disabled_bank.add_padding()

            # Disable the other bank
            active_bank.active = False
            active_bank.chunks[0].chunk_id = self.chunk_id_map["INVALID_BANK_HDR"][0]
            active_bank.chunks[0].chunk_length = self.chunk_id_map["INVALID_BANK_HDR"][1]
            active_bank.chunks[0].chunk_crc = self.chunk_id_map["INVALID_BANK_HDR"][2]
        else:
            active_bank.add_chunk(new_chunk)
        # end if
    # end def add_new_chunk

    def delete_chunk(self, chunk_id, data=None):
        """
        Delete a chunk. The way to delete a chunk in this platform is to write 0xFF

        :param chunk_id: ID of the chunk to delete. It can be the int value or the name.
        :type chunk_id: ``int`` or ``str``
        :param data: The chunk data to delete. If no data are given, the last chunk with chunk_id is deleted. - OPTIONAL
        :type data: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
        """
        if isinstance(chunk_id, int):
            platform_chunk_address, platform_chunk_length = (chunk_id, len(data))
        else:
            platform_chunk_address, platform_chunk_length = (self.chunk_id_map[chunk_id][0],
                                                        self.chunk_id_map[chunk_id][1] - self.chunk_id_map[chunk_id][0])
        # end if

        zone_number = self._get_chunk_zone(platform_chunk_address)
        platform_chunk_address &= self.CHUNK_ADDRESS_MASK
        active_bank = self.zone_list[zone_number].get_active_bank()

        last_chunk_index = None
        for i in range(len(active_bank.chunks)):
            if platform_chunk_address == active_bank.chunks[i].chunk_id:
                last_chunk_index = i
                if data is not None and active_bank.chunks[i].chunk_data == data:
                    active_bank.chunks[i].chunk_data = [0xFF] * platform_chunk_length
                    return
                # end if
            # end if
        # end for

        # If the code arrive here, either data=None or the specific chunk has not been found, which should raise
        # an error
        assert data is None, "Could not find chunk with specific data to delete"

        if last_chunk_index is not None:
            active_bank.chunks[last_chunk_index].chunk_data = [0xFF] * platform_chunk_length
        # end if
    # end def delete_chunk

    def diff(self, other, active_banks=True, delete=False):
        # See ``NvsParserInterface.diff``
        attrs = ["nvs_encryption_key", "chunk_id_map"]
        attrs_diff = [attr for attr in attrs if getattr(self, attr) != getattr(other, attr)]
        diff = {
            "parsers": (self, other),
            "attrs": attrs_diff,
            "zones": []
        } if attrs_diff else {}

        for zone_index in range(max(len(self.zone_list), len(other.zone_list))):
            my_zone = self.zone_list[zone_index] if zone_index < len(self.zone_list) else None
            other_zone = other.zone_list[zone_index] if zone_index < len(other.zone_list) else None
            if my_zone is not None and other_zone is not None:
                zone_diff = my_zone.diff(other_zone, active_banks, delete=delete)
            else:
                zone_diff = {"zones": (my_zone, other_zone), "attrs": [], "banks": []}
            # end if
            if diff and zone_diff:
                diff["zones"].append(zone_diff)
            elif zone_diff:
                diff = {"parsers": (self, other), "attrs": [], "zones": [zone_diff]}
            # end if
        # end for
        return diff
    # end def diff
# end class AddressBasedNvsParser


class NvsZone(object):

    def __init__(self, zone_number, banks, start_address):
        """
        :param zone_number: The number of the zone.
        :type zone_number: ``int``
        :param banks: The bank list of the zone, it should be 2 banks, one active and one disabled.
        :type banks: ``list of NvsBank``
        :param start_address: The start address in memory of the zone.
        :type start_address: ``int``
        """
        assert len(banks) == 2, "There should be 2 banks"

        self.zone_number = zone_number
        self.banks = banks
        self.start_address = start_address
    # end def __init__

    @classmethod
    def from_hex_array(cls, array_to_parse, chunk_from_hex_array_method, bank_length, zone_number, start_address,
                       chunk_id_map):
        """
        Parse an array to get the first chunk possible. It will return the array minus the chunk taken.

        :param array_to_parse: The hex array to parse to get a bank
        :type array_to_parse: ``list or HexList or tuple or bytearray``
        :param chunk_from_hex_array_method: The method to use to convert an hex array to a chunk object
        :type chunk_from_hex_array_method: ``function``
        :param bank_length: The length of the bank
        :type bank_length: ``int``
        :param zone_number: The number of the zone
        :type zone_number: ``int``
        :param start_address: The start address in memory of the zone
        :type start_address: ``int``
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
                             It must have at least the keys "ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"
                             which point to the full header, not just the ID.
        :type chunk_id_map: ``dict``

        :return: a tuple with the zone object and array_to_parse minus the zone taken
        :rtype: ``tuple``
        """
        banks = [None, None]
        bank_start_address = start_address

        for i in range(2):
            banks[i], array_to_parse = NvsBank.from_hex_array(
                array_to_parse=array_to_parse,
                chunk_from_hex_array_method=chunk_from_hex_array_method,
                start_address=bank_start_address,
                bank_length=bank_length,
                chunk_id_map=chunk_id_map)
            if chunk_id_map["NVS_CHUNK_METHOD"]:
                bank_start_address += bank_length
            else:
                break
            # end if
        # end for

        return cls(zone_number, banks, start_address), array_to_parse
    # end def from_hex_array

    def to_hex_array(self):
        """
        Convert this to an hex array.

        :return: the hex array form of the chunk
        :rtype: ``list``
        """
        return_array = []

        for bank in self.banks:
            if bank is not None:
                # To have a good representation of the zone in hex array format the padding in the bank is needed
                return_array.extend(bank.to_hex_array())
            # end if
        # end for

        return return_array
    # end def to_hex_array

    def to_hex_file(self, no_padding=False):
        """
        Convert this to an IntelHex object.

        :param no_padding: Request not to add the padding chunk in the hex file (optional).
                           By default it will add the padding.
        :type no_padding: ``bool``

        :return: The hex_file object
        :rtype: ``IntelHex``
        """
        hex_file = IntelHex()

        for bank in self.banks:
            hex_file.puts(addr=bank.start_address, s=bytes(bank.to_hex_array(no_padding)))
        # end for

        return hex_file
    # end def to_hex_file

    def get_active_bank(self):
        """
        Get the active bank of the zone.

        :return: Active bank
        :rtype: ``NvsBank``
        """
        for bank in self.banks:
            if bank.active:
                return bank
            # end if
        # end for

        # No active bank is supported in multi-zone
        return None
    # end def get_active_bank

    def get_valid_banks(self):
        """
        Get the valid banks of the zone.

        :return: Active and disabled banks
        :rtype: ``tuple[NvsBank]``
        """
        return tuple(bank for bank in self.banks if bank is not None)
    # end def get_valid_banks

    def get_disabled_bank(self):
        """
        Get the disabled bank of the zone.

        :return: Active bank
        :rtype: ``NvsBank``
        """
        for bank in self.banks:
            if bank is not None and not bank.active:
                return bank
            # end if
        # end for

        # Not suppose to arrive here
        assert False, "No disabled bank detected"
    # end def get_disabled_bank

    def __eq__(self, other):
        """
        Redefinition of the "==" action.

        :param other: other chunk to compare
        :type other: ``NvsZone``

        :return: True is chunks are equals, False otherwise.
        :rtype: ``bool``
        """
        return (self.zone_number == other.zone_number and self.start_address == other.start_address
                and self.banks == other.banks)
    # end def __eq__

    def diff(self, other, active_banks=True, delete=False):
        """
        Compare 2 NVS Zones

        :param other: Other zone
        :type other: ``NvsZone``
        :param active_banks: Flag to compare active banks only - OPTIONAL
        :type active_banks: ``bool``
        :param delete: Flag indicating if diff is requested after a delete operation - OPTIONAL
        :type delete: ``bool``

        :return: Differences between zones
        :rtype: ``dict``
        """
        attrs = ["zone_number", "start_address"]
        attrs_diff = [attr for attr in attrs if getattr(self, attr) != getattr(other, attr)]
        diff = {
            "zones": (self, other),
            "attrs": attrs_diff,
            "banks": []
        } if attrs_diff else {}

        active_bank = self.get_active_bank()
        other_active_bank = other.get_active_bank()
        if active_banks and active_bank.start_address != other_active_bank.start_address:
            expected_bank = self.get_expected_bank_on_switch(active_bank, other_active_bank, delete=delete)
            bank_diff = expected_bank.diff(other_active_bank)
            if bank_diff:
                if diff:
                    diff["banks"].append(bank_diff)
                else:
                    diff = {"zones": (self, other), "attrs": [], "banks": [bank_diff]}
                # end if
            # end if
        else:
            for bank_index in range(max(len(self.banks), len(other.banks))):
                my_bank = self.banks[bank_index] if bank_index < len(self.banks) else None
                other_bank = other.banks[bank_index] if bank_index < len(other.banks) else None
                if my_bank is not None and other_bank is not None:
                    bank_diff = my_bank.diff(other_bank)
                else:
                    bank_diff = {"banks": (my_bank, other_bank), "attrs": [], "chunks": []}
                # end if
                if diff and bank_diff:
                    diff["banks"].append(bank_diff)
                elif bank_diff:
                    diff = {"zones": (self, other), "attrs": [], "banks": [bank_diff]}
                # end if
            # end for
        # end if
        return diff
    # end def diff

    @staticmethod
    def get_expected_bank_on_switch(bank_1, bank_2, nvs_invalid_chunk_id=0x00, delete=False):
        """
        Get the expected bank when a bank switch is triggered by writing a new chunk

        :param bank_1: First bank
        :type bank_1: ``NvsBank``
        :param bank_2: Second bank
        :type bank_2: ``NvsBank``
        :param nvs_invalid_chunk_id: NVS invalid chunk id - OPTIONAL
        :type nvs_invalid_chunk_id: ``int``
        :param delete: Flag indicating if bank switch is triggered by a delete operation - OPTIONAL
        :type delete: ``bool``

        :return: Expected new bank
        :rtype: ``NvsBank``
        """
        chunk_ids = [chunk.chunk_id for chunk in bank_1.chunks if chunk.chunk_id != nvs_invalid_chunk_id]
        # Mimic the algorithm in firmware to get the same chunks order : keep only last occurrence of a chunk id
        chunk_ids = [chunk_id for index, chunk_id in enumerate(chunk_ids) if chunk_id not in chunk_ids[index + 1:]]
        if not delete and bank_2.chunks[-2].chunk_id in chunk_ids:
            # Remove last chunk id of the new bank (-1 is padding, -2 is the last added chunk) because it is the
            # chunk which triggered the bank switch, so it is new and should not be copied from previous bank.
            # If bank switch was triggered to delete a chunk, then there is no chunk id to remove.
            chunk_ids.remove(bank_2.chunks[-2].chunk_id)
        # end if
        if bank_2.chunks[-1].chunk_id in chunk_ids:
            chunk_ids.remove(bank_2.chunks[-1].chunk_id)
        # end if
        expected_chunks = []
        for chunk_id in chunk_ids:
            expected_chunks.append(bank_1.get_chunk_history(chunk_id)[-1])
        # end for
        expected_bank = NvsBank(active=True,
                                start_address=bank_2.start_address,
                                bank_length=bank_2.bank_length,
                                chunks=expected_chunks,
                                nvs_word_size=bank_2.nvs_word_size)
        return expected_bank
    # end def get_expected_bank_on_switch
# end class NvsZone


class NvsBank(object):

    def __init__(self, active, start_address, bank_length, chunks, nvs_word_size=4):
        """
        :param active: Is the bank the active one
        :type active: ``bool``
        :param start_address: The start address in memory of the bank
        :type start_address: ``int``
        :param bank_length: The length of the bank
        :type bank_length: ``int``
        :param chunks: The chunk list of the bank
        :type chunks: ``list[NvsChunk]``
        :param nvs_word_size: NVS word size. Default is 4 bytes as in NRF52 - OPTIONAL
        :type nvs_word_size: ``int``
        """
        self.active = active
        self.start_address = start_address
        self.bank_length = bank_length
        self.chunks = chunks
        self.nvs_word_size = nvs_word_size

        assert self.bank_length >= self.get_current_length(), \
            f"The current length of the bank " \
            f"({self.get_current_length()}) is higher than " \
            f"bank_length specified ({self.bank_length})"

        self.add_padding()
    # end def __init__

    @classmethod
    def from_hex_array(cls, array_to_parse, chunk_from_hex_array_method, start_address, bank_length,
                       chunk_id_map):
        """
        Parse an array to get the first chunk possible. It will return the array minus the chunk taken.

        :param array_to_parse: The hex array to parse to get a bank
        :type array_to_parse: ``list or HexList or tuple or bytearray``
        :param chunk_from_hex_array_method: The method to use to convert an hex array to a chunk
        :type chunk_from_hex_array_method: ``function``
        :param start_address: The start address in memory of the bank
        :type start_address: ``int``
        :param bank_length: The length of the bank
        :type bank_length: ``int``
        :param chunk_id_map: The map to get the right chunk ID for the platform/project. The keys should be strings.
                             You can find examples in pylibrary/tools/chunkidmaps.py.
                             It must have at least the keys "ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"
                             which point to the full header, not just the ID.
        :type chunk_id_map: ``dict``

        :return: a tuple with the bank object and array_to_parse minus the bank taken
        :rtype: ``tuple``
        """
        bank_array_to_parse = array_to_parse[:bank_length]
        chunks = []
        while len(bank_array_to_parse) > 0:
            chunk, bank_array_to_parse = chunk_from_hex_array_method(bank_array_to_parse, chunk_id_map)
            if isinstance(chunk, list):
                chunks = chunk
            else:
                chunks.append(chunk)
            # end if
        # end while

        if len(chunks) == 0:
            active = False
        elif chunk_id_map["NVS_CHUNK_METHOD"]:
            # Check if first chunk ID is a valid bank information chunk ID (0xFF is used for erased chunk, it is
            # possible that it is equal to one of the other 3 header chunk ID.
            assert chunks[0].chunk_id in (
                    [0xFF] + [chunk_id_map[i][0] for i in ["ACTIVE_BANK_HDR", "TEMP_BANK_HDR", "INVALID_BANK_HDR"]]
                    ), f"Invalid first chunk id in bank: {chunks[0].chunk_id}"

            if [chunks[0].chunk_id, chunks[0].chunk_length, chunks[0].chunk_crc] == chunk_id_map["ACTIVE_BANK_HDR"]:
                active = True
            elif [chunks[0].chunk_id, chunks[0].chunk_length, chunks[0].chunk_crc] == chunk_id_map["TEMP_BANK_HDR"] \
                    or [chunks[0].chunk_id, chunks[0].chunk_length,
                        chunks[0].chunk_crc] == chunk_id_map["INVALID_BANK_HDR"] \
                    or [chunks[0].chunk_id, chunks[0].chunk_length,
                        chunks[0].chunk_crc] == [0xFF, -1, -1]:
                active = False
            else:
                assert False, "Invalid first chunk header in bank"
            # end if
        else:
            active = True
        # end if

        return (cls(active, start_address, bank_length, chunks, chunk_id_map["NVS_WORD_SIZE"]),
                array_to_parse[bank_length:])
    # end def from_hex_array

    def to_hex_array(self, no_padding=False):
        """
        Convert this to a hex array.

        :param no_padding: Request not to add the padding chunk in the array. Add the padding by default.- OPTIONAL
        :type no_padding: ``bool``

        :return: the hex array form of the chunk
        :rtype: ``list``
        """
        return_array = []

        for chunk in self.chunks:
            if no_padding and chunk.chunk_length == -1 and chunk.chunk_crc == -1:
                # No padding is requested and the padding chunk is reached
                break
            # end if
            return_array.extend(chunk.to_hex_array())
        # end for
        return return_array
    # end def to_hex_array

    def to_hex_file(self, no_padding=False):
        """
        Convert this to an IntelHex object.

        :param no_padding: Request not to add the padding chunk in the array. Add the padding by default.- OPTIONAL
        :type no_padding: ``bool``

        :return: The hex_file object
        :rtype: ``IntelHex``
        """
        hex_file = IntelHex()
        hex_file.puts(addr=self.start_address, s=bytes(self.to_hex_array(no_padding)))
        return hex_file
    # end def to_hex_file

    def add_chunk(self, chunk_to_add):
        """
        Add a new chunk in the bank.

        :param chunk_to_add: The chunk to add
        :type chunk_to_add: ``NvsChunk``
        """
        assert self.get_current_length() + len(chunk_to_add.to_hex_array()) <= self.bank_length, \
            "Cannot add chunk because it would overflow the bank"

        if self.chunks[-1].chunk_length == -1 and self.chunks[-1].chunk_crc == -1:
            self.chunks[-1] = chunk_to_add
        else:
            self.chunks.append(chunk_to_add)
        # end if

        self.add_padding()
    # end def add_chunk

    def add_padding(self):
        """
        Add a padding chunk.
        """
        parsed_length = len(self.to_hex_array())
        if parsed_length == 0:
            self.chunks.append(NvsChunk.create_a_padding_chunk(
                    padding_length=self.bank_length - parsed_length, nvs_word_size=self.nvs_word_size))
        elif parsed_length < self.bank_length:
            if self.chunks[-1].chunk_length == -1 and self.chunks[-1].chunk_crc == -1:
                self.chunks[-1].chunk_data.extend([0xFF] * (self.bank_length - parsed_length))
            else:
                self.chunks.append(NvsChunk.create_a_padding_chunk(
                        padding_length=self.bank_length - parsed_length, nvs_word_size=self.nvs_word_size))
            # end if
        # end if
    # end def add_padding

    def get_current_length(self):
        """
        Get the current length taken in the bank (padding excluded).

        :return: current length of the bank
        :rtype: ``int``
        """
        return len(self.to_hex_array(no_padding=True))
    # end def get_current_length

    def __eq__(self, other):
        """
        Redefinition of the "==" action.

        :param other: other bank to compare
        :type other: ``NvsBank``

        :return: True is banks are equals, False otherwise.
        :rtype: ``bool``
        """
        # Do not use padding chunk to compare
        if self.chunks[-1].chunk_length == -1 and self.chunks[-1].chunk_crc == -1:
            chunks_1 = self.chunks[:-1]
        else:
            chunks_1 = self.chunks
        # end if

        if other.chunks[-1].chunk_length == -1 and other.chunks[-1].chunk_crc == -1:
            chunks_2 = other.chunks[:-1]
        else:
            chunks_2 = other.chunks
        # end if

        return (self.active == other.active and self.start_address == other.start_address
                and self.bank_length == other.bank_length and chunks_1 == chunks_2)
    # end def __eq__

    def diff(self, other):
        """
        Compare 2 NVS Banks

        :param other: Other NVS Bank
        :type other: ``NvsBank``

        :return: Differences between NVS Banks
        :rtype: ``dict``
        """
        attrs = ["active", "start_address", "bank_length"]
        attrs_diff = [attr for attr in attrs if getattr(self, attr) != getattr(other, attr)]
        diff = {
            "banks": (self, other),
            "attrs": attrs_diff,
            "chunks": []
        } if attrs_diff else {}

        for chunk_index in range(max(len(self.chunks), len(other.chunks))):
            my_chunk = self.chunks[chunk_index] if chunk_index < len(self.chunks) else None
            other_chunk = other.chunks[chunk_index] if chunk_index < len(other.chunks) else None
            if my_chunk is not None and other_chunk is not None:
                chunk_diff = my_chunk.diff(other_chunk)
            else:
                chunk_diff = {"chunks": (my_chunk, other_chunk), "attrs": []}
            # end if
            if diff and chunk_diff:
                diff["chunks"].append(chunk_diff)
            elif chunk_diff:
                diff = {"banks": (self, other), "attrs": [], "chunks": [chunk_diff]}
            # end if
        # end for
        return diff
    # end def diff

    def get_chunk_history(self, chunk_id):
        """
        Get all the values of a chunk in its history in the bank.

        :param chunk_id: ID of the chunk to get.
        :type chunk_id: ``int``

        :return: The wanted chunk.
        :rtype: ``list of NvsChunk``
        """
        chunk_history = []
        for chunk in self.chunks:
            if chunk.chunk_id == chunk_id:
                chunk_history.append(chunk)
            # end if
        # end for
        return chunk_history
    # end def get_chunk_history
# end class NvsBank


class NvsChunk(object):
    """
    NvsChunk class supporting clear and encrypted payload
    """

    def __init__(self, to_hex_array_method, chunk_id, chunk_length, chunk_crc, chunk_data,
                 nvs_word_size=4, default_parser=True):
        """
        :param to_hex_array_method: The method to use to convert this chunk in hex array
        :type to_hex_array_method: ``function``
        :param chunk_id: The ID of the chunk
        :type chunk_id: The type is dependent on the platform/project
        :param chunk_length: The length of the chunk
        :type chunk_length: ``int``
        :param chunk_crc: The CRC of the chunk
        :type chunk_crc: ``int``
        :param chunk_data: The data array of the chunk
        :type chunk_data: ``list or HexList or tuple or bytearray``
        :param nvs_word_size: NVS word size. Default is 4 bytes as in NRF52 - OPTIONAL
        :type nvs_word_size: ``int``
        """
        self.to_hex_array_method = to_hex_array_method
        self.chunk_id = chunk_id
        self.chunk_length = chunk_length
        self.chunk_crc = chunk_crc
        self.chunk_data = chunk_data
        self.clear_data = chunk_data
        self.nvs_word_size = nvs_word_size
        self.default_parser = default_parser
        # Some chunks data  are encrypted using the AES algorithm and an internal crc 16 is added at the end.
        # The chunk_data match the following structure:
        #     {
        #         uint8_t iv[16];
        #         uint8_t data[chunk_length - 16 - 2]
        #         uint16_t crc_16ccitt_t
        #     } encrChunk_ts;
        self.iv = None
        self.internal_crc = None
        self.padding_bytes = None
    # end def __init__

    @classmethod
    def create_a_padding_chunk(cls, padding_length, nvs_word_size=4):
        """
        Create a padding NvsChunk.

        A padding NvsChunk is represented by one of the padding byte (0xFF) is in chunk_id and the rest in chunk_data,
        chunk_length and chunk_crc being both equal to -1

        :param padding_length: The length of the padding
        :type padding_length: ``int``
        :param nvs_word_size: NVS word size. Default is 4 bytes as in NRF52 - OPTIONAL
        :type nvs_word_size: ``int``

        :return: the hex array form of the chunk
        :rtype: ``NvsChunk``
        """
        return cls(to_hex_array_method=NvsChunk.padding_chunk_to_hex_array,
                   chunk_id=0xFF,
                   chunk_length=-1,
                   chunk_crc=-1,
                   default_parser=True,
                   chunk_data=[0xFF] * (padding_length - 1),
                   nvs_word_size=nvs_word_size)
    # end def create_a_padding_chunk

    @classmethod
    def create_zero_padding_chunk(cls, padding_length, nvs_word_size=4):
        """
        See ``create_a_padding_chunk`` but with default chunk_data as 0x00 instead of 0xFF.
        """
        return cls(to_hex_array_method=NvsChunk.padding_chunk_to_hex_array,
                   chunk_id=0xFF,
                   chunk_length=-1,
                   chunk_crc=-1,
                   default_parser=False,
                   chunk_data=[0x00] * (padding_length - 1),
                   nvs_word_size=nvs_word_size)
    # end def create_zero_padding_chunk

    @staticmethod
    def padding_chunk_to_hex_array(chunk):
        """
        Format a chunk in an hex array.
        This function is static to then be given to each new NvsChunk to have the right format.

        :param chunk: The chunk to format
        :type chunk: ``NvsChunk``

        :return: The hex array
        :rtype: ``list``
        """
        assert chunk.chunk_length == -1 and chunk.chunk_crc == -1, \
            "This function should only be used for padding chunks"
        if chunk.default_parser:
            return [chunk.chunk_id] + chunk.chunk_data
        else:
            return chunk.chunk_data
        # end if
    # end def padding_chunk_to_hex_array

    def to_hex_array(self):
        """
        Parse an array to get the first chunk possible. It will return the array minus the chunk taken.

        :return: The hex array form of the chunk
        :rtype: ``list``
        """
        return self.to_hex_array_method(self)
    # end def to_hex_array

    def to_hex_file(self, address_in_memory):
        """
        Convert this to an IntelHex object.

        :param address_in_memory: The address in memory to put this chunk
        :type address_in_memory: ``int``

        :return: The hex_file object
        :rtype: ``IntelHex``
        """
        hex_file = IntelHex()

        hex_file.puts(addr=address_in_memory, s=bytes(self.to_hex_array()))
        return hex_file
    # end def to_hex_file

    def __eq__(self, other):
        """
        Redefinition of the "==" action.

        :param other: other chunk to compare
        :type other: ``NvsChunk``

        :return: True is chunks are equal, False otherwise.
        :rtype: ``bool``
        """
        if (other is None) or not isinstance(other, NvsChunk):
            return False
        # end if

        return (self.chunk_id == other.chunk_id and self.chunk_length == other.chunk_length
                and self.chunk_crc == other.chunk_crc and self.chunk_data == other.chunk_data)
    # end def __eq__

    def __ne__(self, other):
        """
        Redefinition of the "!=" action.

        :param other: other chunk to compare
        :type other: ``NvsChunk``

        :return: True is chunks are not equal, False otherwise.
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

    def diff(self, other):
        """
        Compare 2 NVS chunks

        :param other: Other NVS Chunk
        :type other: ``NvsChunk``

        :return: Differences between the 2 chunks
        :rtype: ``dict``
        """
        attrs = ["chunk_id", "chunk_length", "chunk_crc", "chunk_data", "clear_data", "iv", "internal_crc",
                 "padding_bytes"]
        attrs_diff = [attr for attr in attrs if getattr(self, attr) != getattr(other, attr)]
        diff = {
            "chunks": (self, other),
            "attrs": attrs_diff,
        } if attrs_diff else {}

        return diff
    # end def diff
# end class NvsChunk

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
