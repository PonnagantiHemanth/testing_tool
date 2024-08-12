#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.imageformat.imageformattestutils
:brief: Helpers for ImageFormat feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import abstractmethod
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from os.path import join

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives.hashes import SHA256

from pylibrary.mcu.mcuboot.imageformat import ImageHeader
from pylibrary.mcu.mcuboot.imageformat import ImageTlvInfo
from pylibrary.mcu.mcuboot.imageformat import ImageTlvList
from pylibrary.mcu.mcuboot.imageformat import KeyHierarchyHeader
from pylibrary.mcu.mcuboot.imageformat import RootOfTrust
from pylibrary.mcu.mcuboot.imageformat import SEC_1_UNCOMPRESSED_PUBLIC_KEY_SIZE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import NotImplementedAbstractMethodError
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.bootloaderimagecommunicationtestutils import \
    BootloaderImageCommunicationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ImageFormatTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ImageFormat feature
    """

    @staticmethod
    def get_slot_index(test_case, pc_reg_val):
        """
        Get slot index from PC register value

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param pc_reg_val: Value of the PC register
        :type pc_reg_val: ``int``

        :return: Initial slot index
        :rtype: ``int``
        """
        slot_ranges = [
            (to_int(test_case.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[i]),
             to_int(test_case.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[i] + test_case.f.PRODUCT.DUAL_BANK.SLOTS.F_ImageSize[i]))
            for i in range(len(test_case.f.PRODUCT.DUAL_BANK.SLOTS.F_Base))]
        is_in_slots = [slot_ranges[i][0] <= pc_reg_val <= slot_ranges[i][1] for i in range(len(slot_ranges))]
        if True not in is_in_slots:
            raise ValueError(f"PC value {pc_reg_val} is not in any expected slot range")
        # end if
        initial_slot_index = is_in_slots.index(True)
        return initial_slot_index
    # end def get_slot_index

    @staticmethod
    def check_pc(test_case, pc_reg_val, slot_index):
        """
        Check that the PC register value is in the expected range

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param pc_reg_val: Value of the PC register
        :type pc_reg_val: ``int``
        :param slot_index: Slot index
        :type slot_index: ``int``
        """
        test_case.assertGreaterEqual(
            pc_reg_val,
            to_int(test_case.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[slot_index]),
            f"PC should be in slot {slot_index} range"
        )
        test_case.assertLessEqual(
            pc_reg_val,
            to_int(test_case.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[slot_index]
                   + test_case.f.PRODUCT.DUAL_BANK.SLOTS.F_ImageSize[slot_index]),
            f"PC should be in slot {slot_index} range"
        )
    # end def check_pc

    @staticmethod
    def hash_data(data):
        """
        Get SHA-256 hash of data.

        :param data: Data to hash
        :type data: ``bytes``

        :return: Hash
        :rtype: ``HexList``
        """
        digest = Hash(SHA256())
        digest.update(data)
        hash_hex = HexList(digest.finalize())
        return hash_hex
    # end def hash_data

    @staticmethod
    def get_private_key_from_path(key_path):
        """
        Get private key from key path

        :param key_path: Key path
        :type key_path: ``str``

        :return: Private key
        :rtype: ``cryptography.hazmat.primitives.asymmetric.types.PRIVATE_KEY_TYPES``
        """
        with open(key_path, 'rb') as key_file:
            raw_pem = key_file.read()
        # end with
        return serialization.load_pem_private_key(raw_pem, password=None)
    # end def get_private_key_from_path

    class RootOfTrust:
        """
        Help for root of trust
        """

        def __init__(self, test_case):
            """
            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            self.test_case = test_case
        # end def __init__

        @staticmethod
        def get_private_key_from_path(key_path):
            """
            Get private key from key path

            :param key_path: Key path
            :type key_path: ``str``

            :return: Private key
            :rtype: ``cryptography.hazmat.primitives.asymmetric.types.PRIVATE_KEY_TYPES``
            """
            return ImageFormatTestUtils.get_private_key_from_path(key_path)
        # end def get_private_key_from_path

        @classmethod
        def check_root_of_trust_public_key(cls, key_path, key_address, development_credentials, key_type):
            """
            Get public key as encoded in the root of trust table

            :param key_path: Private Key path
            :type key_path: ``str``
            :param key_address: Public key address
            :type key_address: ``int``
            :param development_credentials: Development credentials
            :type development_credentials: ``bool``
            :param key_type: Key type
            :type key_type: ``RootOfTrust.EncodedFlags.Type``

            :raise ``TestException``: If data at key address do not match expected data
            """
            raise NotImplementedAbstractMethodError()
        # end def check_root_of_trust_public_key
    # end class RootOfTrust

    class EcRootOfTrust(RootOfTrust):
        """
        Help for EC root of trust
        """

        def check_root_of_trust_public_key(self, key_path, key_address, development_credentials, key_type):
            # See ``RootOfTrust.check_root_of_trust_public_key``
            private_key = self.get_private_key_from_path(key_path)
            pub_key = self.test_case.memory_manager.debugger.readMemory(key_address, SEC_1_UNCOMPRESSED_PUBLIC_KEY_SIZE)
            public_encoding = serialization.Encoding.X962
            public_format = serialization.PublicFormat.UncompressedPoint
            exp_pub_key = (
                HexList(private_key.public_key().public_bytes(encoding=public_encoding, format=public_format))
                if (development_credentials | (key_type == RootOfTrust.EncodedFlags.Type.PRODUCTION))
                else HexList("00" * SEC_1_UNCOMPRESSED_PUBLIC_KEY_SIZE))
            self.test_case.assertEqual(exp_pub_key, pub_key,
                                       f"Public key at address {key_address} should be as expected")
        # end def check_root_of_trust_public_key
    # end class EcRootOfTrust

    class RsaRootOfTrust(RootOfTrust):
        """
        Help for RSA root of trust
        """

        def check_root_of_trust_public_key(self, key_path, key_address, development_credentials, key_type):
            # See ``RootOfTrust.check_root_of_trust_public_key``
            private_key = self.get_private_key_from_path(key_path)
            pub_key = self.test_case.memory_manager.debugger.readMemory(key_address, private_key.key_size // 8)
            exp_pub_key = (private_key.public_key().public_numbers().n
                           if (development_credentials | (key_type == RootOfTrust.EncodedFlags.Type.PRODUCTION))
                           else to_int(HexList("00" * (private_key.key_size // 8))))
            self.test_case.assertEqual(exp_pub_key, to_int(pub_key),
                                       f"Public key at address {hex(key_address)} should be as expected")
        # end def check_root_of_trust_public_key
    # end class RsaRootOfTrust

    class RootOfTrustFactory:
        """
        Create root of trust
        """

        @staticmethod
        def create(test_case):
            """
            Create root of test

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Root of trust instance
            :rtype: ``ImageFormatTestUtils.RootOfTrust``
            """
            rot_class = {
                "ECDSA_P256": ImageFormatTestUtils.EcRootOfTrust,
                "RSA_2048": ImageFormatTestUtils.RsaRootOfTrust,
                "RSA_3072": ImageFormatTestUtils.RsaRootOfTrust,
            }
            return rot_class[test_case.f.PRODUCT.DUAL_BANK.F_SignType](test_case)
        # end def create
    # end class RootOfTrustFactory

    class Slot:
        """
        Characterize a slot, with all related attributes (header, trailer, ...) and specific methods to read or
        compute values.
        """
        def __init__(self, test_case):
            """
            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            self.test_case = test_case

            self.base_address = None
            self.sign_type = self.test_case.f.PRODUCT.DUAL_BANK.F_SignType

            self.header_raw = None
            self.mcu_boot_header = None
            self.key_hierarchy_header = None
            self.key_hierarchy_table = None
            self.key_pairs_type = None
            self.key_hierarchy_table_type = None

            self.image = None

            self.trailer_start_address = None
            self.trailer = None
            self.tlv_info_raw = None
            self.tlv_info = None
            self.tlv_list_start_address = None
            self.tlv_list_end_address = None
            self.tlv_list_raw = None
            self.tlv_list = None

            self.public_signature_key_size = None
            self.public_signature_key = None
            self.private_signature_key = None
        # end def __init__

        def init_header(self):
            """
            Init full header, including MCU boot header and key hierarchy if enabled
            """
            self.init_mcu_boot_header()
            self.header_raw = self.test_case.memory_manager.debugger.readMemory(
                self.base_address, to_int(self.mcu_boot_header.ih_hdr_size))
            if self.test_case.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_Enabled:
                self.init_key_hierarchy_header()
                self.init_key_hierarchy_table()
            # end if
        # end def init_header

        def init_mcu_boot_header(self):
            """
            Init MCU boot header with the value from device memory
            """
            mcu_boot_header_size = sum([field.length for field in ImageHeader.FIELDS]) // 8
            mcu_boot_header_raw = self.test_case.memory_manager.debugger.readMemory(self.base_address,
                                                                                    mcu_boot_header_size)
            self.mcu_boot_header = ImageHeader.fromHexList(mcu_boot_header_raw)
        # end def init_mcu_boot_header

        def init_key_hierarchy_header(self):
            """
            Init key hierarchy header with the value from device memory
            """
            mcu_boot_header_size = sum([field.length for field in ImageHeader.FIELDS]) // 8
            start_addr = self.base_address + mcu_boot_header_size
            size = sum([field.length for field in KeyHierarchyHeader.FIELDS]) // 8
            key_hierarchy_header_raw = self.test_case.memory_manager.debugger.readMemory(start_addr, size)
            self.key_hierarchy_header = KeyHierarchyHeader.fromHexList(key_hierarchy_header_raw)
        # end def init_key_hierarchy_header

        def init_key_hierarchy_table(self):
            """
            Init key hierarchy table with the value from device memory
            """
            mcu_boot_header_size = sum([field.length for field in ImageHeader.FIELDS]) // 8
            header_start = self.base_address + mcu_boot_header_size
            key_hierarchy_header_size = sum([field.length for field in KeyHierarchyHeader.FIELDS]) // 8
            table_start = header_start + key_hierarchy_header_size
            # If certificates are used, we are not able to anticipate the actual size of the key hierarchy table,
            # so we need to read the full allocated header size. If key pairs are used, we can optimize by reading
            # less memory.
            if self.key_hierarchy_table_type is KeyHierarchyHeader.X509CertificatesTable:
                table_size = to_int(self.mcu_boot_header.header_size) - mcu_boot_header_size - key_hierarchy_header_size
            else:
                pair_size = sum([field.length for field in self.key_pairs_type.FIELDS]) // 8
                table_size = to_int(self.key_hierarchy_header.key_count) * pair_size
            # end if
            table_raw = self.test_case.memory_manager.debugger.readMemory(table_start, table_size)
            self.key_hierarchy_table = self.key_hierarchy_table_type.fromHexList(table_raw)
        # end def init_key_hierarchy_table

        def init_image(self):
            """
            Init application image
            """
            self.image = self.test_case.memory_manager.debugger.readMemory(
                self.base_address + to_int(self.mcu_boot_header.ih_hdr_size), to_int(self.mcu_boot_header.ih_img_size))
        # end def init_image

        def init_trailer(self):
            """
            Init trailer
            """
            self.trailer_start_address = (self.base_address
                                          + to_int(self.mcu_boot_header.ih_hdr_size)
                                          + to_int(self.mcu_boot_header.ih_img_size))
            self.tlv_info_raw = self.test_case.memory_manager.debugger.readMemory(self.trailer_start_address,
                                                                                  ImageTlvInfo.get_total_length() // 8)
            self.tlv_info = ImageTlvInfo.fromHexList(self.tlv_info_raw)
            self.tlv_list_start_address = self.trailer_start_address + ImageTlvInfo.get_total_length() // 8
            self.tlv_list_end_address = (self.tlv_list_start_address
                                         + to_int(self.tlv_info.tlv_tot)
                                         - ImageTlvInfo.get_total_length() // 8)
            self.tlv_list_raw = self.test_case.memory_manager.debugger.readMemory(
                self.tlv_list_start_address, self.tlv_list_end_address - self.tlv_list_start_address)
            self.tlv_list = ImageTlvList.fromHexList(self.tlv_list_raw)
        # end def init_trailer

        @staticmethod
        def get_private_key_from_path(key_path):
            """
            Get private key from key path

            :param key_path: Key path
            :type key_path: ``str``

            :return: Private key
            :rtype: ``cryptography.hazmat.primitives.asymmetric.types.PRIVATE_KEY_TYPES``
            """
            return ImageFormatTestUtils.get_private_key_from_path(key_path)
        # end def get_private_key_from_path

        def init_private_key_from_path(self, key_path):
            """
            Init private key from key path

            :param key_path: Key path
            :type key_path: ``str``
            """
            self.private_signature_key = self.get_private_key_from_path(key_path)
        # end def init_private_key_from_path

        def init_public_signature_key(self):
            """
            Init public key corresponding to the key used to sign the slot. It can be obtained from:
                * key hierarchy
                * root of trust
                * path
            """
            if self.test_case.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_Enabled and \
                    to_int(self.key_hierarchy_header.key_count) > 0:
                public_signature_key = self.key_hierarchy_table[-1].public_key
                self.public_signature_key = self.get_public_key_from_key_hierarchy(public_signature_key)
            elif self.test_case.f.PRODUCT.DUAL_BANK.ROOT_OF_TRUST_TABLE.F_Enabled:
                public_signature_key_address = to_int(BootloaderImageCommunicationTestUtils.get_root_of_trust_table(
                    self.test_case)[to_int(self.key_hierarchy_header.root_of_trust_index)].public_key_address)
                public_signature_key = self.test_case.memory_manager.debugger.readMemory(public_signature_key_address,
                                                                                         self.public_signature_key_size)
                self.public_signature_key = self.get_public_key_from_root_of_trust(public_signature_key)
            else:
                key_path = str(join(TESTS_PATH, 'DFU_FILES', self.test_case.f.PRODUCT.DUAL_BANK.F_Key))
                self.init_private_key_from_path(key_path)
                self.public_signature_key = self.private_signature_key.public_key()
            # end if
        # end def init_public_signature_key

        def get_public_signature_key_hash(self):
            """
            Get hash of the public key corresponding to the key used to sign

            :return: Hash
            :rtype: ``HexList``
            """
            return ImageFormatTestUtils.hash_data(self.get_public_signature_key_bytes(self.public_signature_key))
        # end def get_public_signature_key_hash

        def get_full_header(self):
            """
            Get full header, including key hierarchy if enabled.

            :return: Header
            :rtype: ``HexList``
            """
            header = HexList(self.mcu_boot_header)
            if self.test_case.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_Enabled:
                header += HexList(self.key_hierarchy_header) + HexList(self.key_hierarchy_table)
            # end if
            header.addPadding(size=to_int(self.mcu_boot_header.ih_hdr_size), pattern=0xFF, fromLeft=False)
            return header
        # end def get_full_header

        def get_slot_data(self):
            """
            Get data to sign and/or hash

            :return: Slot data
            :rtype: ``bytes``
            """
            header = self.get_full_header()
            protected_tlv_list = HexList('')
            if to_int(self.mcu_boot_header.protect_tlv_size) > 0x0000:
                # TODO : Manage case where protected TLV list is not None
                raise RuntimeError("TODO : protected TLV list support not implemented yet")
            # end if
            return bytes(header + self.image + protected_tlv_list)
        # end def get_slot_data

        def check_signature(self, public_key, signature, data):
            """
            Check signature

            :param public_key: Public Key
            :type public_key: ``cryptography.hazmat.primitives.asymmetric.types.PUBLIC_KEY_TYPES``
            :param signature: Signature
            :type signature: ``HexList``
            :param data: Data
            :type data: ``bytes``
            """
            valid_signature = self.verify_signature(public_key, signature, data)
            self.test_case.assertTrue(valid_signature, "Signature should be valid")
        # end def check_signature

        @abstractmethod
        def get_public_key_from_root_of_trust(self, root_of_trust_public_key):
            """
            Get public key from root of trust public key value

            :param root_of_trust_public_key: Public key from root of trust
            :type root_of_trust_public_key: ``HexList``

            :return: Root of trust public key
            :rtype: ``cryptography.hazmat.primitives.asymmetric.types.PUBLIC_KEY_TYPES``
            """
            raise NotImplementedAbstractMethodError()
        # end def get_public_key_from_root_of_trust

        @abstractmethod
        def get_public_key_from_key_hierarchy(self, key_hierarchy_public_key):
            """
            Get public key from key hierarchy public key value

            :param key_hierarchy_public_key: Public key from key hierarchy
            :type key_hierarchy_public_key: ``HexList``

            :return: Key hierarchy public key
            :rtype: ``cryptography.hazmat.primitives.asymmetric.types.PUBLIC_KEY_TYPES``
            """
            raise NotImplementedAbstractMethodError()
        # end def get_public_key_from_key_hierarchy

        @abstractmethod
        def get_public_signature_key_bytes(self, public_signature_key):
            """
            Get serialized public signature key to bytes

            :param public_signature_key: Public signature key
            :type public_signature_key: ``cryptography.hazmat.primitives.asymmetric.types.PUBLIC_KEY_TYPES``

            :return: Public signature key bytes
            :rtype: ``bytes``
            """
            raise NotImplementedAbstractMethodError()
        # end def get_public_signature_key_bytes

        @abstractmethod
        def get_key_hierarchy_public_key_bytes(self, key_hierarchy_public_key):
            """
            Get serialized public key from key hierarchy to bytes

            :param key_hierarchy_public_key: Public key from key hierarchy
            :type key_hierarchy_public_key: ``cryptography.hazmat.primitives.asymmetric.types.PUBLIC_KEY_TYPES``

            :return: Key hierarchy public key bytes
            :rtype: ``bytes``
            """
            raise NotImplementedAbstractMethodError()
        # end def get_key_hierarchy_public_key_bytes

        @abstractmethod
        def get_key_hierarchy_signature(self, signature):
            """
            Get signature in key hierarchy signature format

            :param signature: Signature
            :type signature: ``bytes``

            :return: Key hierarchy signature
            :rtype: ``HexList``
            """
            raise NotImplementedAbstractMethodError()
        # end def get_key_hierarchy_signature

        @abstractmethod
        def get_signature_from_key_hierarchy(self, key_hierarchy_signature):
            """
            Get signature from key hierarchy

            :param key_hierarchy_signature: Signature from key hierarchy
            :type key_hierarchy_signature: ``HexList``

            :return: Signature
            :rtype: ``bytes``
            """
            raise NotImplementedAbstractMethodError()
        # end def get_signature_from_key_hierarchy

        @abstractmethod
        def verify_signature(self, public_key, signature, data):
            """
            Verify data was signed by the private key associated with this public key

            :param public_key: Public Key
            :type public_key: ``cryptography.hazmat.primitives.asymmetric.types.PUBLIC_KEY_TYPES``
            :param signature: Signature
            :type signature: ``HexList``
            :param data: Data
            :type data: ``bytes``

            :return: Valid signature status
            :rtype: ``bool``
            """
            raise NotImplementedAbstractMethodError()
        # end def verify_signature

        @abstractmethod
        def sign(self, private_key, data):
            """
            Sign data with private key

            :param private_key: Private key
            :type private_key: ``cryptography.hazmat.primitives.asymmetric.types.PRIVATE_KEY_TYPES``
            :param data: Data to sign
            :type data: ``bytes``

            :return: Signature
            :rtype: ``bytes``
            """
            raise NotImplementedAbstractMethodError()
        # end def sign

        @abstractmethod
        def generate_private_key(self):
            """
            Generate private key

            :return: Private key
            :rtype: ``cryptography.hazmat.primitives.asymmetric.types.PRIVATE_KEY_TYPES``
            """
            raise NotImplementedAbstractMethodError()
        # end def generate_private_key

        @abstractmethod
        def update_key_hierarchy_entry(self, index, new_public_key, signing_key):
            """
            Update an entry in the key hierarchy table

            :param index: Index in the key hierarchy
            :type index: ``int``
            :param new_public_key: New public key for the entry
            :type new_public_key: ``cryptography.hazmat.primitives.asymmetric.types.PUBLIC_KEY_TYPES``
            :param signing_key: Key to sign the entry
            :type signing_key: ``cryptography.hazmat.primitives.asymmetric.types.PRIVATE_KEY_TYPES``
            """
            raise NotImplementedAbstractMethodError()
        # end def update_key_hierarchy_entry

        def get_key_hierarchy_entry_signed_data(self, index):
            """
            Get the signed data for an entry in the key hierarchy table

            :param index: Index in the key hierarchy
            :type index: ``int``

            :return: Signed data for the entry in the key hierarchy
            :rtype: ``bytes``
            """
            raise NotImplementedAbstractMethodError()
        # end def get_key_hierarchy_entry_signed_data
    # end class Slot

    class EcSlot(Slot):
        """
        Characterize a slot when ECDSA-P-256 is used
        """

        def __init__(self, test_case):
            # See ``Slot.__init__``
            super().__init__(test_case)
            self.public_signature_key_size = SEC_1_UNCOMPRESSED_PUBLIC_KEY_SIZE
            self.key_pairs_type = KeyHierarchyHeader.EcPair
            self.key_hierarchy_table_type = KeyHierarchyHeader.EcPairsTable
        # end def __init__

        def get_public_key_from_root_of_trust(self, root_of_trust_public_key):
            # See ``Slot.get_public_key_from_root_of_trust``
            return EllipticCurvePublicKey.from_encoded_point(SECP256R1(), bytes(root_of_trust_public_key))
        # end def get_public_key_from_root_of_trust

        def get_public_key_from_key_hierarchy(self, key_hierarchy_public_key):
            # See ``Slot.get_public_key_from_key_hierarchy``
            return EllipticCurvePublicKey.from_encoded_point(SECP256R1(), bytes(key_hierarchy_public_key))
        # end def get_public_key_from_key_hierarchy

        def get_public_signature_key_bytes(self, public_signature_key):
            # See ``Slot.get_public_signature_key_bytes``
            return public_signature_key.public_bytes(encoding=serialization.Encoding.DER,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo)
        # end def get_public_signature_key_bytes

        def get_key_hierarchy_public_key_bytes(self, key_hierarchy_public_key):
            # See ``Slot.get_key_hierarchy_public_key_bytes``
            return key_hierarchy_public_key.public_bytes(encoding=serialization.Encoding.X962,
                                                         format=serialization.PublicFormat.UncompressedPoint)
        # end def get_key_hierarchy_public_key_bytes

        def get_key_hierarchy_signature(self, signature):
            # See ``Slot.get_key_hierarchy_signature``
            signature_r, signature_s = decode_dss_signature(signature)
            signature_r = "{:X}".format(signature_r)
            signature_r = signature_r if len(signature_r) % 2 == 0 else "0" + signature_r
            signature_s = "{:X}".format(signature_s)
            signature_s = signature_s if len(signature_s) % 2 == 0 else "0" + signature_s
            signature = HexList(HexList(signature_r) + HexList(signature_s))
            signature_pad = deepcopy(signature)
            signature_pad.addPadding(
                size=self.key_pairs_type.LEN.SIGNATURE // 8, pattern=0xFF, fromLeft=False)
            return signature_pad
        # end def get_key_hierarchy_signature

        def get_signature_from_key_hierarchy(self, key_hierarchy_signature):
            # See ``Slot.get_signature_from_key_hierarchy``
            r = key_hierarchy_signature[: ((self.key_pairs_type.LEN.SIGNATURE // 8) // 2)]
            s = key_hierarchy_signature[((self.key_pairs_type.LEN.SIGNATURE // 8) // 2):]
            return HexList(encode_dss_signature(to_int(r), to_int(s)))
        # end def get_signature_from_key_hierarchy

        def verify_signature(self, public_key, signature, data):
            # See ``Slot.verify_signature``
            try:
                public_key.verify(
                    bytes(signature),
                    data,
                    ec.ECDSA(SHA256())
                )
                return True
            except InvalidSignature:
                return False
            # end try
        # end def verify_signature

        def sign(self, private_key, data):
            # See ``Slot.sign``
            return private_key.sign(data=data, signature_algorithm=ec.ECDSA(SHA256()))
        # end def sign

        def generate_private_key(self):
            # See ``Slot.generate_private_key``
            return ec.generate_private_key(ec.SECP256R1())
        # end def generate_private_key

        def update_key_hierarchy_entry(self, index, new_public_key, signing_key):
            # See ``Slot.update_key_hierarchy_entry``
            new_public_key_bytes = self.get_key_hierarchy_public_key_bytes(new_public_key)
            new_signature = self.sign(signing_key, new_public_key_bytes)
            self.check_signature(
                signing_key.public_key(), new_signature, new_public_key_bytes)
            key_hierarchy_signature = self.get_key_hierarchy_signature(new_signature)
            self.key_hierarchy_table[index] = self.key_pairs_type(public_key=HexList(new_public_key_bytes),
                                                                  signature=key_hierarchy_signature)
        # end def update_key_hierarchy_entry

        def get_key_hierarchy_entry_signed_data(self, index):
            # See ``Slot.get_key_hierarchy_entry_signed_data``
            return bytes(self.key_hierarchy_table[index].public_key)
        # end def get_key_hierarchy_entry_signed_data
    # end class EcSlot

    class RsaSlot(Slot):
        """
        Characterize a slot when RSA is used
        """

        def __init__(self, test_case):
            # See ``Slot.__init__``
            super().__init__(test_case)
            self.public_signature_key_size = self.test_case.f.PRODUCT.DUAL_BANK.F_RSAKeyLength // 8
            if self.test_case.f.PRODUCT.DUAL_BANK.F_SignType == "RSA_2048":
                self.key_pairs_type = KeyHierarchyHeader.Rsa2048Pair
                self.key_hierarchy_table_type = KeyHierarchyHeader.Rsa2048PairsTable
            elif self.test_case.f.PRODUCT.DUAL_BANK.F_SignType == "RSA_3072":
                self.key_pairs_type = KeyHierarchyHeader.Rsa3072Pair
                self.key_hierarchy_table_type = KeyHierarchyHeader.Rsa3072PairsTable
            else:
                raise ValueError("RSA key length not supported")
            # end if
        # end def __init__

        def get_public_key_from_root_of_trust(self, root_of_trust_public_key):
            # See ``Slot.get_public_key_from_root_of_trust``
            return rsa.RSAPublicNumbers(e=self.test_case.f.PRODUCT.DUAL_BANK.F_RSAKeyExp,
                                        n=to_int(HexList(bytes(root_of_trust_public_key)))).public_key()
        # end def get_public_key_from_root_of_trust

        def get_public_key_from_key_hierarchy(self, key_hierarchy_public_key):
            # See ``Slot.get_public_key_from_key_hierarchy``
            return rsa.RSAPublicNumbers(e=self.test_case.f.PRODUCT.DUAL_BANK.F_RSAKeyExp,
                                        n=to_int(HexList(bytes(key_hierarchy_public_key)))).public_key()
        # end def get_public_key_from_key_hierarchy

        def get_public_signature_key_bytes(self, public_signature_key):
            # See ``Slot.get_public_signature_key_bytes``
            return public_signature_key.public_bytes(encoding=serialization.Encoding.DER,
                                                     format=serialization.PublicFormat.PKCS1)
        # end def get_public_signature_key_bytes

        def get_key_hierarchy_public_key_bytes(self, key_hierarchy_public_key):
            # See ``Slot.get_key_hierarchy_public_key_bytes``
            return key_hierarchy_public_key.public_numbers().n.to_bytes(length=self.public_signature_key_size,
                                                                        byteorder='big')
        # end def get_key_hierarchy_public_key_bytes

        def get_key_hierarchy_signature(self, signature):
            # See ``Slot.get_key_hierarchy_signature``
            return HexList(signature)
        # end def get_key_hierarchy_signature

        def get_signature_from_key_hierarchy(self, key_hierarchy_signature):
            # See ``Slot.get_signature_from_key_hierarchy``
            return key_hierarchy_signature
        # end def get_signature_from_key_hierarchy

        def verify_signature(self, public_key, signature, data):
            # See ``Slot.verify_signature``
            try:
                public_key.verify(
                    bytes(signature),
                    data,
                    padding.PSS(mgf=padding.MGF1(SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
                    SHA256()
                )
                return True
            except InvalidSignature:
                return False
            # end try
        # end def verify_signature

        def sign(self, private_key, data):
            # See ``Slot.sign``
            return private_key.sign(
                data=data,
                padding=padding.PSS(mgf=padding.MGF1(SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
                algorithm=SHA256())
        # end def sign

        def generate_private_key(self):
            # See ``Slot.generate_private_key``
            return rsa.generate_private_key(public_exponent=self.test_case.f.PRODUCT.DUAL_BANK.F_RSAKeyExp,
                                            key_size=self.test_case.f.PRODUCT.DUAL_BANK.F_RSAKeyLength)
        # end def generate_private_key

        def update_key_hierarchy_entry(self, index, new_public_key, signing_key):
            # See ``Slot.update_key_hierarchy_entry``
            new_public_key_bytes = self.get_key_hierarchy_public_key_bytes(new_public_key)
            new_signature = self.sign(signing_key, new_public_key_bytes)
            self.check_signature(
                signing_key.public_key(), new_signature, new_public_key_bytes)
            key_hierarchy_signature = self.get_key_hierarchy_signature(new_signature)
            self.key_hierarchy_table[index] = self.key_pairs_type(public_key=HexList(new_public_key_bytes),
                                                                  signature=key_hierarchy_signature)
        # end def update_key_hierarchy_entry

        def get_key_hierarchy_entry_signed_data(self, index):
            # See ``Slot.get_key_hierarchy_entry_signed_data``
            return bytes(self.key_hierarchy_table[index].public_key)
        # end def get_key_hierarchy_entry_signed_data
    # end class RsaSlot

    class ECX509CertificateSlot(EcSlot):
        """
        Characterize a slot when X.509 certificates and ECDSA-P-256 is used
        """
        def __init__(self, test_case):
            # See ``Slot.__init__``
            super().__init__(test_case)
            self.key_hierarchy_table_type = KeyHierarchyHeader.X509CertificatesTable
        # end def __init__

        def get_public_key_from_key_hierarchy(self, key_hierarchy_public_key):
            # See ``Slot.get_public_key_from_key_hierarchy``
            return key_hierarchy_public_key
        # end def get_public_key_from_key_hierarchy

        def get_signature_from_key_hierarchy(self, key_hierarchy_signature):
            # See ``Slot.get_signature_from_key_hierarchy``
            return HexList(key_hierarchy_signature)
        # end def get_signature_from_key_hierarchy

        def update_key_hierarchy_entry(self, index, new_public_key, signing_key):
            # See ``Slot.update_key_hierarchy_entry``
            cert = x509.CertificateBuilder().subject_name(x509.Name([])).issuer_name(x509.Name([])).public_key(
                new_public_key).serial_number(1).not_valid_before(
                datetime.now(timezone.utc)).not_valid_after(
                datetime.now(timezone.utc) + timedelta(days=3653)).sign(
                signing_key, SHA256())

            self.key_hierarchy_table[index] = KeyHierarchyHeader.X509CertificateKeyHierarchyEntry(
                raw=HexList(cert.public_bytes(serialization.Encoding.DER)), certificate=cert)
        # end def update_key_hierarchy_entry

        def get_key_hierarchy_entry_signed_data(self, index):
            # See ``Slot.get_key_hierarchy_entry_signed_data``
            return bytes(self.key_hierarchy_table[index].certificate.tbs_certificate_bytes)
        # end def get_key_hierarchy_entry_signed_data
    # end class ECX509CertificateSlot

    class RsaX509CertificateSlot(RsaSlot):
        """
        Characterize a slot when X.509 certificates and RSA is used
        """
        def __init__(self, test_case):
            # See ``Slot.__init__``
            super().__init__(test_case)
            self.key_hierarchy_table_type = KeyHierarchyHeader.X509CertificatesTable
        # end def __init__

        def get_public_key_from_key_hierarchy(self, key_hierarchy_public_key):
            # See ``Slot.get_public_key_from_key_hierarchy``
            return key_hierarchy_public_key
        # end def get_public_key_from_key_hierarchy

        def update_key_hierarchy_entry(self, index, new_public_key, signing_key):
            # See ``Slot.update_key_hierarchy_entry``
            cert = x509.CertificateBuilder().subject_name(x509.Name([])).issuer_name(x509.Name([])).public_key(
                new_public_key).serial_number(1).not_valid_before(
                datetime.now(timezone.utc)).not_valid_after(
                datetime.now(timezone.utc) + timedelta(days=3653)).sign(
                signing_key, SHA256(),
                rsa_padding=padding.PSS(mgf=padding.MGF1(SHA256()), salt_length=padding.PSS.DIGEST_LENGTH))

            self.key_hierarchy_table[index] = KeyHierarchyHeader.X509CertificateKeyHierarchyEntry(
                raw=HexList(cert.public_bytes(serialization.Encoding.DER)), certificate=cert)
        # end def update_key_hierarchy_entry

        def get_key_hierarchy_entry_signed_data(self, index):
            # See ``Slot.get_key_hierarchy_entry_signed_data``
            return bytes(self.key_hierarchy_table[index].certificate.tbs_certificate_bytes)
        # end def get_key_hierarchy_entry_signed_data
    # end class RsaX509CertificateSlot

    class SlotFactory:
        """
        Create Slot
        """
        @staticmethod
        def create(test_case):
            """
            Create slot

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Slot instance
            :rtype: ``ImageFormatTestUtils.Slot``
            """
            slot_class = {
                ("ECDSA_P256", False): ImageFormatTestUtils.EcSlot,
                ("RSA_2048", False): ImageFormatTestUtils.RsaSlot,
                ("RSA_3072", False): ImageFormatTestUtils.RsaSlot,
                ("ECDSA_P256", True): ImageFormatTestUtils.ECX509CertificateSlot,
                ("RSA_2048", True): ImageFormatTestUtils.RsaX509CertificateSlot,
                ("RSA_3072", True): ImageFormatTestUtils.RsaX509CertificateSlot,
            }
            return slot_class[(test_case.f.PRODUCT.DUAL_BANK.F_SignType,
                               test_case.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_UseX509Certificate)](test_case)
        # end def create
    # end class SlotFactory
# end class ImageFormatTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
