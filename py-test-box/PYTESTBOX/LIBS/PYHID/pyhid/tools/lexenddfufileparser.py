#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.tools.lexenddfufileparser
:brief: DFU file parser class for Lexend
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2024/01/29
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from copy import deepcopy

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives.hashes import SHA256

from pyhid.tools.defaultdfufileparser import DefaultDfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SECP256R1Parameters:
    """
    See https://www.secg.org/sec2-v2.pdf - 2.4.2 Recommended Parameters secp256r1
    The verifiably random elliptic curve domain parameters over Fp secp256r1 are specified by the
    sextuple T = (p, a, b, G, n, h) where the finite field Fp is defined by:
    """
    # noinspection PyPep8Naming
    p = HexList("FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF")
    a = HexList("FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC")
    b = HexList("5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B")
    Gx = HexList("6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296")
    Gy = HexList("4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5")
    n = HexList("FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551")
    h = HexList("01")
# end class SECP256R1Parameters


class LexendDfuFileParser(DefaultDfuFileParser):
    """
    Define DFU file parser class specific for Lexend DFU and signature format
    https://drive.google.com/file/d/1yNHBokTcRLQ99Oq4FeODwBnanTd9HCEH/view
    """

    ADDITIONAL_AUTHENTICATION_SIZE = 64 # bytes
    SIGNATURE_SIZE = 64 # bytes
    VALID_FLAG_SIZE = 16 # bytes
    PROGRAM_DATA_APPLICATION_INDEX = 0
    PROGRAM_DATA_VALID_FLAG_INDEX = 1
    CHECK_DATA_SIGNATURE_INDEX = 0
    COMMAND_1_OR_2_COMMAND_INDEX = 0
    COMMAND_1_OR_2_DATA_PACKETS_INDEX = 1

    def __init__(self, dfu_start_command, command_1, command_2, command_3):
        # See ``DfuFileParser.__init__``
        super().__init__(dfu_start_command=dfu_start_command,
                         command_1=command_1,
                         command_2=command_2,
                         command_3=command_3)
        self.program_data = None
        self.prv_key = None
        self.hash_algorithm = SHA256()
    # end def __init__

    def init_prv_key(self, prv_key_path):
        """
        Initialize private key from key file

        :param prv_key_path: path to private key file
        :type prv_key_path: ``str``
        """
        with open(prv_key_path, 'rb') as key_file:
            prv_raw_pem = key_file.read()
        # end with
        self.prv_key = serialization.load_pem_private_key(prv_raw_pem, password=None)
    # end def init_prv_key

    def get_hash(self, data):
        """
        Get hash value of data

        :param data: data to hash
        :type data: ``HexList``

        :return: hash value
        :rtype: ``HexList``
        """
        hasher = Hash(self.hash_algorithm)
        hasher.update(bytes(data))
        dgst = hasher.finalize()
        return HexList(dgst)
    # end def get_hash

    def sign(self, data, prehashed=False):
        """
        Sign data

        :param data: data to sign
        :type data: ``HexList``
        :param prehashed: Disable hashing if data have been prehashed - OPTIONAL
        :type prehashed: ``bool``

        :return: Signature (ASN.1 encoded)
        :rtype: ``HexList``
        """
        signature_algorithm = ec.ECDSA(Prehashed(self.hash_algorithm)) if prehashed else ec.ECDSA(self.hash_algorithm)
        return HexList(self.prv_key.sign(data=bytes(data), signature_algorithm=signature_algorithm))
    # end def sign

    @staticmethod
    def signature_to_raw(signature):
        """
        Get ECDSA-P-256 signature, using SHA-256 hash, encoded in raw format, i.e. composed of the 2 unsigned 32-bytes
        R and S values in big-endian order.

        :param signature: ASN.1 encoded signature
        :type signature: ``HexList``

        :return: Signature in raw format
        :rtype: ``HexList``
        """
        signature_r, signature_s = decode_dss_signature(bytes(signature))
        signature_r = "{:X}".format(signature_r)
        signature_r = signature_r if len(signature_r) % 2 == 0 else "0" + signature_r
        signature_s = "{:X}".format(signature_s)
        signature_s = signature_s if len(signature_s) % 2 == 0 else "0" + signature_s
        return HexList(HexList(signature_r) + HexList(signature_s))
    # end def signature_to_raw

    def compute_signature(self, priv_key_file, max_app_address, min_app_address=None, additional_auth=False):
        # See ``DfuFileParser.compute_signature``

        # Get data to sign
        data_to_sign = self.get_data_to_sign(min_app_address, max_app_address)

        # Sign and get check data
        self.init_prv_key(priv_key_file)
        signature = self.sign(data=data_to_sign)

        # Signature verification
        try:
            self.prv_key.public_key().verify(bytes(signature), bytes(data_to_sign), ec.ECDSA(self.hash_algorithm))
            status = True
        except InvalidSignature:
            return False
        # end try

        signature = self.signature_to_raw(signature)
        check_data = self.signature_to_check_data(signature)

        self.command_2 = check_data
        sequence_number = self.command_2[
            self.CHECK_DATA_SIGNATURE_INDEX][self.COMMAND_1_OR_2_COMMAND_INDEX].functionIndex + 1

        check_data_packets = self.command_2[self.CHECK_DATA_SIGNATURE_INDEX][self.COMMAND_1_OR_2_DATA_PACKETS_INDEX]
        for check_data_packet in check_data_packets:
            check_data_packet.functionIndex = sequence_number % 4
            sequence_number += 1
        # end for

        self.command_3.functionIndex = sequence_number % 4

        return status
    # end def compute_signature

    def encrypt_decrypt_command_1(self, encrypt=True):
        # See ``DfuFileParser.encrypt_decrypt_command_1``
        # No encryption
        pass
    # end def encrypt_decrypt_command_1

    def get_chunk_with_crc(self, crc_address, crc_size):
        # See ``DfuFileParser.get_chunk_with_crc``
        raise NotImplementedError("Not applicable")
    # end def get_chunk_with_crc

    def get_crc(self, crc_address, crc_size):
        # See ``DfuFileParser.get_crc``
        raise NotImplementedError("Not applicable")
    # end def get_crc

    def set_crc(self, crc_address, crc_data):
        # See ``DfuFileParser.set_crc``
        raise NotImplementedError("Not applicable")
    # end def set_crc

    def get_additional_authentication_data(self, fill="00"):
        """
        Get additional authentication data from DFU Start command

        :param fill: Pattern to fill the padding - OPTIONAL
        :type fill: ``str``
        """
        auth_data = (HexList(self.dfu_start_command.fw_entity)
                     + HexList(self.dfu_start_command.magic_str)
                     + HexList(self.dfu_start_command.flag)
                     + HexList(self.dfu_start_command.secur_lvl))
        auth_data.addPadding(size=self.ADDITIONAL_AUTHENTICATION_SIZE, pattern=fill, fromLeft=False)
        return auth_data
    # end def get_additional_authentication_data

    def refresh_program_data(self):
        """
        Refresh program data, read from command 1 and stored in program data attribute
        """
        self.program_data = {}
        for cmd1, data_packets_list in self.command_1:
            addr = to_int(cmd1.address)
            size = to_int(cmd1.size)
            program_data = HexList()
            for data_packet in data_packets_list:
                program_data += data_packet.data
            # end for
            program_data = program_data[:size]
            self.program_data[addr] = program_data
        # end for
    # end def refresh_program_data

    def get_program_data(self):
        """
        Get program data

        :return: Dictionary, where addresses are associated with program data
        :rtype: ``dict``
        """
        if self.program_data is None:
            self.refresh_program_data()
        # end if
        return self.program_data
    # end def get_program_data

    def get_app_data(self, start_address, end_address, fill="FF"):
        # See ``DfuFileParser.get_app_data``
        addr_data_dict = self.get_program_data()
        start_address = start_address if start_address is not None else list(addr_data_dict.keys())[0]
        app_data = list(addr_data_dict.values())[0]
        left_padding = HexList("FF" * (list(addr_data_dict.keys())[0] - start_address))
        right_padding = HexList("FF" * (end_address - start_address - len(left_padding) - len(app_data)))
        app_data = left_padding + app_data + right_padding
        return app_data
    # end def get_app_data

    def get_valid_flag_data(self, fill="FF"):
        """
        Get valid flag data

        :param fill: Pattern to fill padding - OPTIONAL
        :type fill: ``str``

        :return: Valid flag data
        :rtype: ``HexList``
        """
        addr_data_dict = self.get_program_data()
        if len(list(addr_data_dict.values())) > self.PROGRAM_DATA_VALID_FLAG_INDEX:
            valid_flag_data = list(addr_data_dict.values())[self.PROGRAM_DATA_VALID_FLAG_INDEX]
            valid_flag_data.addPadding(size=self.VALID_FLAG_SIZE, pattern=fill, fromLeft=False)
        else:
            valid_flag_data = HexList(fill * self.VALID_FLAG_SIZE)
        # end if
        return valid_flag_data
    # end def get_valid_flag_data

    def get_data_to_sign(self, app_start_address, app_end_address):
        """
        Get data to sign

        :param app_start_address: Start address of application data
        :type app_start_address: ``int``
        :param app_start_address: End address of application data
        :type app_start_address: ``int``
        """
        return (self.get_additional_authentication_data()
                + self.get_app_data(start_address=app_start_address, end_address=app_end_address)
                + self.get_valid_flag_data())
    # end def get_data_to_sign

    def signature_to_check_data(self, signature):
        """
        Copy signature to check data in command 2

        :param signature: Signature in raw format
        :type signature: ``HexList``

        :return: Check data in command 2 format with the signature in the data
        :rtype: ``list[tuple]``
        """
        data_packet_data_length = len(self.command_2[0][1][0].data)
        signature.addPadding(size=4 * data_packet_data_length)
        check_data = deepcopy(self.command_2)
        check_data[0][1][0].data = signature[0 * data_packet_data_length:1 * data_packet_data_length]
        check_data[0][1][1].data = signature[1 * data_packet_data_length:2 * data_packet_data_length]
        check_data[0][1][2].data = signature[2 * data_packet_data_length:3 * data_packet_data_length]
        check_data[0][1][3].data = signature[3 * data_packet_data_length:4 * data_packet_data_length]
        return check_data
    # end def signature_to_check_data

    def signature_from_check_data(self):
        """
        Get signature from check data in command 2

        :return: Signature in raw format
        :rtype: ``HexList``
        """
        check_data = deepcopy(self.command_2)
        signature_data = [cmd.data for cmd in check_data[0][1]]
        signature = HexList()
        for data in signature_data:
            signature += data
        # end for
        return signature
    # end def signature_from_check_data

    def compute_stm32_crc(self, start_address, end_address):
        # See ``DfuFileParser.compute_stm32_crc``
        raise NotImplementedError("Not applicable")
    # end def compute_stm32_crc
# end class LexendDfuFileParser

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
