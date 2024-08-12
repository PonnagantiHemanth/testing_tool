#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.tools.defaultdfufileparser
:brief: Default DFU file parser class
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2024/01/31
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from glob import glob
from io import BufferedReader
from os.path import join
from typing import BinaryIO
from warnings import warn

import pysetup
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from array import array
from math import ceil

from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd3
from pyhid.hidpp.features.common.dfu import DfuCmdDataXData
from pyhid.hidpp.features.common.dfu import DfuStartV0
from pyhid.hidpp.features.common.dfu import DfuStartV1
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.aes import Aes
from pylibrary.tools.crc import Crc32Stm32
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DefaultDfuFileParser:
    """
    Define the DFU file parser class.
    """

    def __init__(self, dfu_start_command, command_1, command_2, command_3):
        """
        :param dfu_start_command: DfuStart command of the DFU file
        :type dfu_start_command: ``DfuStartV0|DfuStartV1``
        :param command_1: Tuples of Command 1 of the DFU file and its associated program data
        :type command_1: ``list[tuple]``
        :param command_2: Tuples of Command 2 of the DFU file and its associated check data
        :type command_2: ``list[tuple]``
        :param command_3: Command 3 of the DFU file
        :type command_3: ``DfuCmdDataXCmd3``
        """

        self.dfu_start_command = dfu_start_command
        self.command_1 = command_1
        self.command_2 = command_2
        self.command_3 = command_3
        self.dfu_file_path = None
    # end def __init__

    def create_dfu_file(self, dfu_file_path=None):
        """
        Construct DFU file from object.

        :param dfu_file_path: Path to the DFU file to create, use the one in the object if `None` - OPTIONAL
        :type dfu_file_path: ``str``
        """
        assert (self.dfu_file_path is not None) or (dfu_file_path is not None), "No path given to create DFU file"

        if dfu_file_path is None:
            dfu_file_path = self.dfu_file_path
        # end if

        with open(dfu_file_path, "wb") as dfu_file:
            # Write StartDfu command
            dfu_file.write(self._get_block_bytes_from_hidpp_message(self.dfu_start_command))

            # Write Command 1
            for cmd_1, program_data_list in self.command_1:
                dfu_file.write(self._get_block_bytes_from_hidpp_message(cmd_1))

                # Write program data blocks
                for program_data in program_data_list:
                    dfu_file.write(self._get_block_bytes_from_hidpp_message(program_data))
                # end for
            # end for

            # Write Command 2
            for cmd_2, check_data_list in self.command_2:
                dfu_file.write(self._get_block_bytes_from_hidpp_message(cmd_2))

                # Write check data blocks
                for check_data in check_data_list:
                    dfu_file.write(self._get_block_bytes_from_hidpp_message(check_data))
                # end for
            # end for

            # Write Command 3
            if self.command_3 is not None:
                dfu_file.write(self._get_block_bytes_from_hidpp_message(self.command_3))
            # end if
        # end with
    # end def create_dfu_file

    def compute_signature(self, priv_key_file, max_app_address, min_app_address=None, additional_auth=False):
        """
        Compute the dfu signature based on dfu start parameters and program data.
        Store the result in check data field.

        :param priv_key_file: The private RSA key in PEM format, file path
        :type priv_key_file: ``str``
        :param max_app_address: The maximum application address
        :type max_app_address: ``int``
        :param min_app_address: The minimum application address. If `None` (default) it will not be used - OPTIONAL
        :type min_app_address: ``int``
        :param additional_auth: Add additional authentication data to the signature. `False` by default - OPTIONAL
        :type additional_auth: ``bool``

        :return: `True` if the signature computation succeeded. `False` otherwise
        :rtype: ``bool``
        """
        # Load RSA private key
        priv_key = RSA.import_key(open(priv_key_file).read())

        # Sort command 1 by address
        def custom_sort(element):
            return int(Numeral(element[0].address))
        # end def custom_sort
        self.command_1.sort(key=custom_sort)

        # Extract application size and start address from dfu program data command
        app_address = int(Numeral(self.command_1[0][0].address))
        app_size = 0
        for (cmd_1, _) in self.command_1:
            app_size += int(Numeral(cmd_1.size))
        # end for

        # Extract Application code from dfu program data content
        app_chunk = HexList()
        previous_address = int(Numeral(self.command_1[0][0].address))
        previous_size = 0
        middle_padding_length = 0
        for (cmd_1, program_data_list) in self.command_1:
            current_middle_padding_length = int(Numeral(cmd_1.address)) - (previous_address + previous_size)
            middle_padding_length += current_middle_padding_length
            app_chunk += HexList('FF' * current_middle_padding_length)
            for program_data in program_data_list[:(int(Numeral(cmd_1.size)) // 16)]:
                app_chunk += program_data.data
            # end for
            if (int(Numeral(cmd_1.size)) % 16) != 0:
                app_chunk += program_data_list[(int(Numeral(cmd_1.size)) // 16)].data[:(int(Numeral(cmd_1.size)) % 16)]
            # end if
            previous_address = int(Numeral(cmd_1.address))
            previous_size = int(Numeral(cmd_1.size))
        # end for

        # Compute the size of memory that stays in erased state.
        back_padding_length = (max_app_address - app_address - app_size - middle_padding_length)

        if min_app_address is not None:
            front_padding_length = app_address - min_app_address
        else:
            front_padding_length = 0
        # end if

        # Build the signature payload (i.e. SHA256 input)
        if additional_auth:
            additional_authentication_data = (HexList(self.dfu_start_command.fw_entity) +
                                              HexList(self.dfu_start_command.magic_str))
            if hasattr(self.dfu_start_command, 'flag'):
                additional_authentication_data += HexList(self.dfu_start_command.flag)
            # end if
            if hasattr(self.dfu_start_command, 'secur_lvl'):
                additional_authentication_data += HexList(self.dfu_start_command.secur_lvl)
            # end if
            additional_authentication_data.addPadding(64, fromLeft=False)
            dfu_mem_view_buf = memoryview(array('B', additional_authentication_data) +
                                          array('B', HexList('FF' * front_padding_length)) +
                                          array('B', app_chunk) +
                                          array('B', HexList('FF' * back_padding_length)))
        else:
            dfu_mem_view_buf = memoryview(array('B', HexList('FF' * front_padding_length)) +
                                          array('B', app_chunk) +
                                          array('B', HexList('FF' * back_padding_length)))
        # end if

        # PKCS#1 v1.5 signature scheme
        h = SHA256.new(dfu_mem_view_buf)
        signature = pkcs1_15.new(priv_key).sign(h)
        little_endian_signature = HexList(signature[:: -1])

        # Signature verification
        try:
            pkcs1_15.new(priv_key).verify(h, signature)
            # The signature is valid.
            status = True
        except (ValueError, TypeError):
            # The signature is not valid.
            status = False
        # end try

        signature_size = 0
        for (cmd_2, _) in self.command_2:
            signature_size += int(Numeral(cmd_2.size))
        # end for

        new_cmd_2 = self.command_2[0][0]
        new_cmd_2.size = signature_size
        header_bytes = [int(Numeral(new_cmd_2.reportId)), int(Numeral(new_cmd_2.deviceIndex)),
                        int(Numeral(new_cmd_2.featureIndex)), int(Numeral(new_cmd_2.softwareId))]
        sequence_number = new_cmd_2.functionIndex + 1
        # Store result in check data
        check_data_list = []
        for i in range(ceil(signature_size / 16)):
            header_bytes[3] = ((sequence_number % 4) << 4) + int(Numeral(new_cmd_2.softwareId))
            block_bytes = bytes(header_bytes) + bytes(little_endian_signature[(i*16):((i+1)*16)])
            check_data_list.append(DfuCmdDataXData.fromHexList(HexList(block_bytes)))
            sequence_number += 1
        # end for
        self.command_2 = [(new_cmd_2, check_data_list)]
        self.command_3.functionIndex = sequence_number % 4
        return status
    # end def compute_signature

    def encrypt_decrypt_command_1(self, encrypt=True):
        """
        Encrypt or Decrypt the command 1 program data using the AES algorithm.

        :param encrypt: `True` for encryption (default), `False` for decryption - OPTIONAL
        :type encrypt: ``bool``
        """
        assert int(Numeral(self.dfu_start_command.encrypt)) != Dfu.EncryptionMode.INVALID, \
            "Invalid encryption mode in DfuStart command"

        if int(Numeral(self.dfu_start_command.encrypt)) != Dfu.EncryptionMode.CLEAR_TEXT:
            # Fetch key file
            key_file_path = glob(join(pysetup.TESTS_PATH, 'DFU_FILES', 'dfu_*_key.txt'))
            assert len(key_file_path) > 0, "No key file to encrypt/decrypt the DFU data has been found"

            if len(key_file_path) > 1:
                warn(f"Too many AES key files: {key_file_path}")
            # end if

            with open(key_file_path[0]) as f:
                key = HexList(f.read(32))
            # end with
        # end if

        function_index = self.command_1[0][0].functionIndex
        header = HexList(self.command_1[0][0])[:4]
        for (cmd_1, program_data_list) in self.command_1:
            buffer = HexList()
            for program_data in program_data_list:
                buffer += HexList(program_data.data)
            # end for

            if int(Numeral(self.dfu_start_command.encrypt)) != Dfu.EncryptionMode.CLEAR_TEXT:
                transformed_buffer = Aes.aes_cipher(
                    data=buffer, key=key, encrypt=encrypt,
                    mode=Dfu.AES_ENCRYPTION_MODE_MAPPING[int(Numeral(self.dfu_start_command.encrypt))])
            else:
                transformed_buffer = buffer
            # end if

            cmd_1.functionIndex = function_index
            function_index = (function_index + 1) % 4
            program_data_list.clear()
            while len(transformed_buffer) > 0:
                new_program_data = DfuCmdDataXData.fromHexList(header + transformed_buffer[:16])
                transformed_buffer = transformed_buffer[16:]

                new_program_data.functionIndex = function_index
                function_index = (function_index + 1) % 4

                program_data_list.append(new_program_data)
            # end while
        # end for

        # Adjust function indexes for command 2 and check data
        for (cmd_2, check_data_list) in self.command_2:
            cmd_2.functionIndex = function_index
            function_index = (function_index + 1) % 4

            for check_data in check_data_list:
                check_data.functionIndex = function_index
                function_index = (function_index + 1) % 4
            # end for
        # end for

        # Adjust function index for command 3
        self.command_3.functionIndex = function_index
    # end def encrypt_decrypt_command_1

    @staticmethod
    def _get_block_bytes_from_file(dfu_file, function_index, header_bytes):
        """
        Get a data or command block of 16 bytes from a file.

        :param dfu_file: File to parse
        :type dfu_file: ``BufferedReader|BinaryIO``
        :param function_index: Function index to use in header
        :type function_index: ``int``

        :return: block of ``bytes``
        :rtype: ``bytes``
        """
        block_bytes = dfu_file.read(16)
        if block_bytes is None or len(block_bytes) == 0:
            return None
        # end if
        header_bytes[3] = (function_index << 4) | 0x0F
        return bytes(header_bytes) + block_bytes
    # end def _get_block_bytes_from_file

    @staticmethod
    def _get_block_bytes_from_hidpp_message(message):
        """
        Get a block of byte to write in a dfu file from a HID++ message.

        :param message: Message to get the block from
        :type message: ``HidppMessage``

        :return: block of ``bytes``
        :rtype: ``bytes``
        """
        hex_str = str(HexList(message))
        block_bytes = b''
        for i in range(4, len(hex_str)//2):
            block_bytes += bytes([int(hex_str[2*i:2*(i+1)], 16)])
        # end for

        if len(block_bytes) != 16:
            warn("Block length is %d, it should be 16" % len(block_bytes))
        # end if

        return block_bytes
    # end def _get_block_bytes_from_hidpp_message

    def get_chunk_with_crc(self, crc_address, crc_size):
        """
        Get the address and the data of the chunk which contains the given CRC

        :param crc_address: CRC storage address
        :type crc_address: ``int``
        :param crc_size: CRC size in bytes
        :type crc_size: ``int``

        :return: Address and data of the chunk containing the CRC
        :rtype: ``tuple[int,HexList]``
        """
        data_map = self.get_data_map()
        for addr, data in data_map.items():
            if addr <= crc_address and crc_address + crc_size <= addr + len(data):
                return addr, data
            # end if
        # end for
    # end def get_chunk_with_crc

    def get_crc(self, crc_address, crc_size):
        """
        Get CRC of the DFU

        :param crc_address: CRC storage address
        :type crc_address: ``int``
        :param crc_size: CRC size
        :type crc_size: ``int``

        :return: CRC value
        :rtype: ``HexList``
        """
        addr, data = self.get_chunk_with_crc(crc_address, crc_size)
        return data[crc_address - addr: crc_address - addr + crc_size]
    # end def get_crc

    def set_crc(self, crc_address, crc_data):
        """
        Set CRC of the DFU

        :param crc_address: CRC storage address
        :type crc_address: ``int``
        :param crc_data: CRC value
        :type crc_data: ``HexList``
        """
        addr, data = self.get_chunk_with_crc(crc_address, len(crc_data))
        data[crc_address - addr: crc_address - addr + len(crc_data)] = crc_data
    # end def set_crc

    def get_data_map(self):
        """
        Get a map of address to data contained in the DFU file

        :return: DFU address to data map
        :rtype: ``dict[int, HexList]``
        """
        data_map = {}
        for cmd_1, data_packets in self.command_1:
            data_map = {
                **data_map,
                **{int(Numeral(cmd_1.address)) + index * len(data_packet.data): data_packet.data
                   for index, data_packet in enumerate(data_packets)}
            }
        # end for
        return data_map
    # end def get_data_map

    def get_app_data(self, start_address, end_address, fill="FF"):
        """
        Get application data with missing addresses filled

        :param start_address: Application start address
        :type start_address: ``int``
        :param end_address: Application end address
        :type end_address: ``int``
        :param fill: Filling pattern - OPTIONAL
        :type fill: ``str``

        :return: Application data
        :rtype: ``HexList``
        """
        app_data = HexList('')
        data_map = self.get_data_map()
        data_packet_size = len(list(data_map.values())[0])
        size = end_address - start_address
        size = size if size % data_packet_size == 0 else size + data_packet_size - size % data_packet_size
        for addr in range(start_address, start_address + size, data_packet_size):
            if addr in data_map:
                if len(data_map[addr]) == data_packet_size:
                    app_data += data_map[addr]
                elif len(data_map[addr]) < data_packet_size:
                    app_data += data_map[addr] + HexList(fill * (data_packet_size - len(data_map[addr])))
                else:
                    raise ValueError("Data too long")
                # end if
            else:
                app_data += HexList(fill * data_packet_size)
            # end if
        # end for
        return app_data[:end_address - start_address]
    # end def get_app_data

    def compute_stm32_crc(self, start_address, end_address):
        """
        Compute STM32 DFU CRC

        :param start_address: Application start address
        :type start_address: ``int``
        :param end_address: Application end address
        :type end_address: ``int``

        :return: CRC value
        :rtype: ``HexList``
        """
        app_data = self.get_app_data(start_address, end_address)
        crc32_stm32 = Crc32Stm32().calculate_crc(app_data)
        return crc32_stm32
    # end def compute_stm32_crc
# end class DefaultDfuFileParser

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
