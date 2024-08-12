#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.tools.dfufileparser
:brief: DFU file parser class
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/08/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from io import BufferedReader
from typing import BinaryIO
from warnings import warn

from math import ceil

from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd1or2
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd3
from pyhid.hidpp.features.common.dfu import DfuCmdDataXData
from pyhid.hidpp.features.common.dfu import DfuStartV0
from pyhid.hidpp.features.common.dfu import DfuStartV1
from pyhid.hidpp.features.common.dfu import DfuStartV2
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.tools.defaultdfufileparser import DefaultDfuFileParser
from pyhid.tools.lexenddfufileparser import LexendDfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DfuFileParser(object):
    """
    Defines the DFU file parser class.
    """
    @classmethod
    def parse_dfu_file(cls, dfu_file_path, device_index, dfu_feature_index, dfu_feature_version):
        """
        Construct object from file.

        :param dfu_file_path: Path to the DFU file to parse
        :type dfu_file_path: ``str``
        :param device_index: Device Index
        :type device_index: ``int``
        :param dfu_feature_index: DFU feature (0x00D0) index
        :type dfu_feature_index: ``int``
        :param dfu_feature_version: DFU feature (0x00D0) version
        :type dfu_feature_version: ``int``

        :return: object created from file
        :rtype: ``DfuFileParser``
        """

        header_bytes = [Dfu.DEFAULT.REPORT_ID_LONG, device_index, dfu_feature_index, 0x0F]

        with open(dfu_file_path, "rb") as dfu_file:
            # Get StartDfu command
            block_bytes = cls._get_block_bytes_from_file(dfu_file, DfuStatusResponse.FUNCTION_INDEX[4], header_bytes)

            if dfu_feature_version == 0:
                dfu_start_command = DfuStartV0.fromHexList(HexList(block_bytes))
            elif dfu_feature_version == 1:
                dfu_start_command = DfuStartV1.fromHexList(HexList(block_bytes))
            elif dfu_feature_version == 2 or dfu_feature_version == 3:
                dfu_start_command = DfuStartV2.fromHexList(HexList(block_bytes))
            else:
                assert False, "dfu_feature_version parameter (%d) not in accepted version %s" % (dfu_feature_version,
                                                                                                 str(Dfu.VERSIONS_LIST))
            # end if

            sequence_number = 1
            command_1 = []
            command_2 = []
            command_3 = None
            while True:
                # Get the next command
                block_bytes = cls._get_block_bytes_from_file(dfu_file, sequence_number % 4, header_bytes)

                # Check is file ended
                if block_bytes is None:
                    break
                # end if

                if block_bytes[len(header_bytes)] == Dfu.CommandId.SUPPLY_PROGRAM_DATA:
                    # Get Command 1
                    command_1_cmd = DfuCmdDataXCmd1or2.fromHexList(HexList(block_bytes))
                    sequence_number += 1

                    # Get program data blocks
                    number_of_program_data_packets = sequence_number + \
                        cls.get_number_of_program_data_packets(dfu_start_command, command_1_cmd)
                    program_data_list = []
                    while sequence_number < number_of_program_data_packets:
                        block_bytes = cls._get_block_bytes_from_file(dfu_file, sequence_number % 4, header_bytes)
                        program_data_list.append(DfuCmdDataXData.fromHexList(HexList(block_bytes)))
                        sequence_number += 1
                    # end while

                    command_1.append((command_1_cmd, program_data_list))
                elif block_bytes[len(header_bytes)] == Dfu.CommandId.SUPPLY_CHECK_DATA:
                    # Get Command 2
                    command_2_cmd = DfuCmdDataXCmd1or2.fromHexList(HexList(block_bytes))
                    sequence_number += 1

                    # Get check data blocks
                    sequence_number_before_data = sequence_number
                    check_data_list = []
                    while sequence_number < (sequence_number_before_data + ceil(command_2_cmd.size.toLong() / 16)):
                        block_bytes = cls._get_block_bytes_from_file(dfu_file, sequence_number % 4, header_bytes)
                        check_data_list.append(DfuCmdDataXData.fromHexList(HexList(block_bytes)))
                        sequence_number += 1
                    # end while

                    command_2.append((command_2_cmd, check_data_list))
                elif block_bytes[len(header_bytes)] == Dfu.CommandId.CHECK_AND_VALIDATE_FIRMWARE:
                    # Get Command 3
                    command_3 = DfuCmdDataXCmd3.fromHexList(HexList(block_bytes))
                    sequence_number += 1
                # end if
            # end while
        # end with

        parser_cls = (LexendDfuFileParser if dfu_start_command.magic_str.ascii_converter() in ["U166_D0A", "U166_IMAGE"]
                      else DefaultDfuFileParser)
        parser_object = parser_cls(dfu_start_command, command_1, command_2, command_3)
        parser_object.dfu_file_path = dfu_file_path
        return parser_object
    # end def parse_dfu_file

    @staticmethod
    def _get_block_bytes_from_file(dfu_file, function_index, header_bytes):
        """
        Get a data or command block of 16 bytes from a file.

        :param dfu_file: File to parse
        :type dfu_file: ``BufferedReader or BinaryIO``
        :param function_index: Function index to use in header
        :type function_index: ``int``

        :return: block of bytes
        :rtype: ``bytes``
        """
        block_bytes = dfu_file.read(16)
        if block_bytes is None:
            return None
        elif len(block_bytes) == 0:
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

        :return: block of bytes
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
    # end def _get_block_bytes_from_file

    @staticmethod
    def get_number_of_program_data_packets(dfu_start_command, command_1_cmd):
        return ceil(command_1_cmd.size.toLong() / 16) + \
                        (1 if int(Numeral(dfu_start_command.encrypt)) in (Dfu.EncryptionMode.AES_OFB,
                                                                          Dfu.EncryptionMode.AES_CFB,
                                                                          Dfu.EncryptionMode.AES_CBC)
                         else 0)
    # end def get_number_of_program_data_packets
# end class DfuFileParser

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
