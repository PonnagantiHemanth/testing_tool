#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.mcuboot.test.imageformat_test
:brief:  Image format test
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase

from pylibrary.mcu.mcuboot.imageformat import ImageHeader
from pylibrary.mcu.mcuboot.imageformat import ImageTlv
from pylibrary.mcu.mcuboot.imageformat import ImageTlvInfo
from pylibrary.mcu.mcuboot.imageformat import ImageTlvKeyHash
from pylibrary.mcu.mcuboot.imageformat import ImageTlvList
from pylibrary.mcu.mcuboot.imageformat import ImageTlvSha256Hash
from pylibrary.mcu.mcuboot.imageformat import ImageTlvSignatureEcdsa256
from pylibrary.mcu.mcuboot.imageformat import ImageTlvSlotHash
from pylibrary.mcu.mcuboot.imageformat import ImageTrailerTLVTypes
from pylibrary.mcu.mcuboot.imageformat import ImageVersion
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ImageFormatTestCase(TestCase):
    """
    Image format testing class
    """

    def test_image_version(self):
        """
        Test image version class instantiation
        """
        image_version_class = ImageVersion(major=0, minor=0, revision=0, build_num=0)
        self.assertEqual(image_version_class.major, HexList('00'))
        self.assertEqual(image_version_class.minor, HexList('00'))
        self.assertEqual(image_version_class.revision, HexList('0000'))
        self.assertEqual(image_version_class.build_num, HexList('00000000'))

        image_version_class = ImageVersion(major=0xFF, minor=0xFF, revision=0xFFFF, build_num=0xFFFFFFFF)
        self.assertEqual(image_version_class.major, HexList('FF'))
        self.assertEqual(image_version_class.minor, HexList('FF'))
        self.assertEqual(image_version_class.revision, HexList('FFFF'))
        self.assertEqual(image_version_class.build_num, HexList('FFFFFFFF'))

        image_version_class = ImageVersion(
            major=HexList('00'), minor=HexList('00'), revision=HexList('0000'), build_num=HexList('00000000'))
        self.assertEqual(image_version_class.major, HexList('00'))
        self.assertEqual(image_version_class.minor, HexList('00'))
        self.assertEqual(image_version_class.revision, HexList('0000'))
        self.assertEqual(image_version_class.build_num, HexList('00000000'))

        image_version_class = ImageVersion(
            major=HexList('FF'), minor=HexList('FF'), revision=HexList('FFFF'), build_num=HexList('FFFFFFFF'))
        self.assertEqual(image_version_class.major, HexList('FF'))
        self.assertEqual(image_version_class.minor, HexList('FF'))
        self.assertEqual(image_version_class.revision, HexList('FFFF'))
        self.assertEqual(image_version_class.build_num, HexList('FFFFFFFF'))
    # end def test_image_version

    def test_image_header(self):
        """
        Test image header class instantiation
        """
        image_version = ImageVersion(major=0, minor=0, revision=0, build_num=0)
        image_header_class = ImageHeader(magic=0,
                                         load_addr=0,
                                         hdr_size=0,
                                         protect_tlv_size=0,
                                         img_size=0,
                                         flags=0,
                                         image_version=image_version,
                                         pad_1=0)
        self.assertEqual(image_header_class.magic, HexList('00000000'))
        self.assertEqual(image_header_class.load_addr, HexList('00000000'))
        self.assertEqual(image_header_class.hdr_size, HexList('0000'))
        self.assertEqual(image_header_class.protect_tlv_size, HexList('0000'))
        self.assertEqual(image_header_class.img_size, HexList('00000000'))
        self.assertEqual(image_header_class.flags, HexList('00000000'))
        self.assertEqual(image_header_class.image_version, image_version)
        self.assertEqual(image_header_class.pad_1, HexList('00000000'))

        image_version = ImageVersion(major=0xFF, minor=0xFF, revision=0xFFFF, build_num=0xFFFFFFFF)
        image_header_class = ImageHeader(magic=0xFFFFFFFF,
                                         load_addr=0xFFFFFFFF,
                                         hdr_size=0xFFFF,
                                         protect_tlv_size=0xFFFF,
                                         img_size=0xFFFFFFFF,
                                         flags=0xFFFFFFFF,
                                         image_version=image_version,
                                         pad_1=0xFFFFFFFF)
        self.assertEqual(image_header_class.magic, HexList('FFFFFFFF'))
        self.assertEqual(image_header_class.load_addr, HexList('FFFFFFFF'))
        self.assertEqual(image_header_class.hdr_size, HexList('FFFF'))
        self.assertEqual(image_header_class.protect_tlv_size, HexList('FFFF'))
        self.assertEqual(image_header_class.img_size, HexList('FFFFFFFF'))
        self.assertEqual(image_header_class.flags, HexList('FFFFFFFF'))
        self.assertEqual(image_header_class.image_version, image_version)
        self.assertEqual(image_header_class.pad_1, HexList('FFFFFFFF'))
    # end def test_image_header

    def test_image_header_from_hexlist(self):
        """
        Test image header class instantiation from HexList
        """
        data = HexList('')
        image_header_class = ImageHeader()
        for field in ImageHeader.FIELDS:
            field_data = RandHexList(field.length // 8)
            if field.name == 'image_version':
                value = ImageVersion.fromHexList(field_data)
            else:
                value = to_int(field_data, little_endian=True)
            # end if
            setattr(image_header_class, field.name, value)
            data += field_data
        # end for
        image_header_class_from_hexlist = ImageHeader.fromHexList(data)
        self.assertEqual(data, HexList(image_header_class_from_hexlist))
        self.assertEqual(data, HexList(image_header_class))
        self.assertEqual(image_header_class_from_hexlist, image_header_class)
    # end def test_image_header_from_hexlist

    def test_image_tlv_info(self):
        """
        Test image TLV Info class instantiation
        """
        image_tlv_info = ImageTlvInfo(magic=0x0000, tlv_tot=0x0000)
        self.assertEqual(image_tlv_info.magic, HexList('0000'))
        self.assertEqual(image_tlv_info.tlv_tot, HexList('0000'))

        image_tlv_info = ImageTlvInfo(magic=0xFFFF, tlv_tot=0xFFFF)
        self.assertEqual(image_tlv_info.magic, HexList('FFFF'))
        self.assertEqual(image_tlv_info.tlv_tot, HexList('FFFF'))
    # end def test_image_tlv_info

    def test_image_tlv_info_from_hexlist(self):
        """
        Test image TLV Info class instantiation from HexList
        """
        data = HexList('')
        image_tlv_info = ImageTlvInfo()
        for field in ImageTlvInfo.FIELDS:
            field_data = RandHexList(field.length // 8)
            setattr(image_tlv_info, field.name, to_int(field_data, little_endian=True))
            data += field_data
        # end for
        image_tlv_info_from_hexlist = ImageTlvInfo.fromHexList(data)
        self.assertEqual(data, HexList(image_tlv_info_from_hexlist))
        self.assertEqual(data, HexList(image_tlv_info))
        self.assertEqual(image_tlv_info_from_hexlist, image_tlv_info)
    # end def test_image_tlv_info_from_hexlist

    def test_image_tlv(self):
        """
        Test image TLV class instantiation
        """
        image_tlv = ImageTlv(type=0x00, length=0x0000)
        self.assertEqual(image_tlv.type, HexList('0000'))
        self.assertEqual(image_tlv.length, HexList('0000'))

        image_tlv = ImageTlv(type=0xFFFF, length=0xFFFF)
        self.assertEqual(image_tlv.type, HexList('FFFF'))
        self.assertEqual(image_tlv.length, HexList('FFFF'))
    # end def test_image_tlv

    def test_image_tlv_from_hexlist(self):
        """
        Test image TLV class instantiation from HexList
        """
        data = HexList('')
        image_tlv = ImageTlv()
        for field in ImageTlv.FIELDS:
            field_data = RandHexList(field.length // 8)
            setattr(image_tlv, field.name, to_int(field_data, little_endian=True))
            data += field_data
        # end for
        image_tlv_from_hexlist = ImageTlv.fromHexList(data)
        self.assertEqual(data, HexList(image_tlv_from_hexlist))
        self.assertEqual(data, HexList(image_tlv))
        self.assertEqual(image_tlv_from_hexlist, image_tlv)
    # end def test_image_tlv_from_hexlist

    def test_image_tlv_sha_256_hash(self):
        """
        Test image TLV Sha 256 Hash class instantiation
        """
        image_tlv_sha_256_hash = ImageTlvSha256Hash(
            type=0x0000, length=0x0000, sha_256_hash=HexList("00" * (ImageTlvSha256Hash.LEN.SHA_256_HASH // 8)))
        self.assertEqual(image_tlv_sha_256_hash.type, HexList('0000'))
        self.assertEqual(image_tlv_sha_256_hash.length, HexList('0000'))
        self.assertEqual(image_tlv_sha_256_hash.sha_256_hash,
                         HexList("00" * (ImageTlvSha256Hash.LEN.SHA_256_HASH // 8)))

        image_tlv_sha_256_hash = ImageTlvSha256Hash(
            type=0xFFFF, length=0xFFFF, sha_256_hash=HexList("FF" * (ImageTlvSha256Hash.LEN.SHA_256_HASH // 8)))
        self.assertEqual(image_tlv_sha_256_hash.type, HexList('FFFF'))
        self.assertEqual(image_tlv_sha_256_hash.length, HexList('FFFF'))
        self.assertEqual(image_tlv_sha_256_hash.sha_256_hash,
                         HexList("FF" * (ImageTlvSha256Hash.LEN.SHA_256_HASH // 8)))
    # end def test_image_tlv_sha_256_hash

    def test_image_tlv_sha_256_hash_from_hexlist(self):
        """
        Test TLV Sha 256 Hash class instantiation from HexList
        """
        data = HexList('')
        image_tlv = ImageTlvSha256Hash()
        for field in ImageTlvSha256Hash.FIELDS:
            field_data = RandHexList(field.length // 8)
            setattr(image_tlv, field.name,
                    to_int(field_data, little_endian=False if field.name == 'sha_256_hash' else True))
            data += field_data
        # end for
        image_tlv_from_hexlist = ImageTlvSha256Hash.fromHexList(data)
        self.assertEqual(data, HexList(image_tlv_from_hexlist))
        self.assertEqual(data, HexList(image_tlv))
        self.assertEqual(image_tlv_from_hexlist, image_tlv)
    # end def test_image_tlv_sha_256_hash_from_hexlist

    def test_image_tlv_key_hash(self):
        """
        Test image TLV key Hash class instantiation
        """
        image_tlv_key_hash = ImageTlvKeyHash(key_hash=HexList("00" * (ImageTlvKeyHash.LEN.SHA_256_HASH // 8)))
        self.assertEqual(to_int(image_tlv_key_hash.type), ImageTrailerTLVTypes.IMAGE_TLV_KEYHASH)
        self.assertEqual(to_int(image_tlv_key_hash.length), ImageTlvKeyHash.DEFAULT.LENGTH)
        self.assertEqual(image_tlv_key_hash.key_hash, HexList("00" * (ImageTlvKeyHash.LEN.SHA_256_HASH // 8)))

        image_tlv_key_hash = ImageTlvKeyHash(key_hash=HexList("FF" * (ImageTlvKeyHash.LEN.SHA_256_HASH // 8)))
        self.assertEqual(to_int(image_tlv_key_hash.type), ImageTrailerTLVTypes.IMAGE_TLV_KEYHASH)
        self.assertEqual(to_int(image_tlv_key_hash.length), ImageTlvKeyHash.DEFAULT.LENGTH)
        self.assertEqual(image_tlv_key_hash.key_hash, HexList("FF" * (ImageTlvKeyHash.LEN.SHA_256_HASH // 8)))
    # end def test_image_tlv_key_hash

    def test_image_tlv_key_hash_from_hexlist(self):
        """
        Test TLV key Hash class instantiation from HexList
        """
        data = HexList('')
        image_tlv = ImageTlvKeyHash()
        for field in ImageTlvKeyHash.FIELDS:
            field_data = RandHexList(field.length // 8)
            setattr(image_tlv, field.name,
                    to_int(field_data, little_endian=False if field.name == 'sha_256_hash' else True))
            data += field_data
        # end for
        image_tlv_from_hexlist = ImageTlvKeyHash.fromHexList(data)
        self.assertEqual(data, HexList(image_tlv_from_hexlist))
        self.assertEqual(data, HexList(image_tlv))
        self.assertEqual(image_tlv_from_hexlist, image_tlv)
    # end def test_image_tlv_key_hash_from_hexlist

    def test_image_tlv_slot_hash(self):
        """
        Test image TLV slot Hash class instantiation
        """
        image_tlv_slot_hash = ImageTlvSlotHash(slot_hash=HexList("00" * (ImageTlvSlotHash.LEN.SHA_256_HASH // 8)))
        self.assertEqual(to_int(image_tlv_slot_hash.type), ImageTrailerTLVTypes.IMAGE_TLV_SHA256)
        self.assertEqual(to_int(image_tlv_slot_hash.length), ImageTlvSlotHash.DEFAULT.LENGTH)
        self.assertEqual(image_tlv_slot_hash.slot_hash, HexList("00" * (ImageTlvSlotHash.LEN.SHA_256_HASH // 8)))

        image_tlv_slot_hash = ImageTlvSlotHash(slot_hash=HexList("FF" * (ImageTlvSlotHash.LEN.SHA_256_HASH // 8)))
        self.assertEqual(to_int(image_tlv_slot_hash.type), ImageTrailerTLVTypes.IMAGE_TLV_SHA256)
        self.assertEqual(to_int(image_tlv_slot_hash.length), ImageTlvSlotHash.DEFAULT.LENGTH)
        self.assertEqual(image_tlv_slot_hash.slot_hash, HexList("FF" * (ImageTlvSlotHash.LEN.SHA_256_HASH // 8)))
    # end def test_image_tlv_slot_hash

    def test_image_tlv_slot_hash_from_hexlist(self):
        """
        Test TLV key Hash class instantiation from HexList
        """
        data = HexList('')
        image_tlv = ImageTlvKeyHash()
        for field in ImageTlvKeyHash.FIELDS:
            field_data = RandHexList(field.length // 8)
            setattr(image_tlv, field.name,
                    to_int(field_data, little_endian=False if field.name == 'sha_256_hash' else True))
            data += field_data
        # end for
        image_tlv_from_hexlist = ImageTlvSlotHash.fromHexList(data)
        self.assertEqual(data, HexList(image_tlv_from_hexlist))
        self.assertEqual(data, HexList(image_tlv))
        self.assertEqual(image_tlv_from_hexlist, image_tlv)
    # end def test_image_tlv_slot_hash_from_hexlist

    def test_image_tlv_signature_ecdsa_256_hash(self):
        """
        Test image TLV Signature ECDSA 256 Hash class instantiation
        """
        image_tlv_signature = ImageTlvSignatureEcdsa256(
            type=HexList("0000"), length=HexList("0000"),
            signature=HexList("00" * (ImageTlvSignatureEcdsa256.LEN.SIGNATURE // 8)))
        self.assertEqual(to_int(image_tlv_signature.type), 0x0000)
        self.assertEqual(to_int(image_tlv_signature.length), 0x0000)
        self.assertEqual(image_tlv_signature.signature, HexList("00" * (ImageTlvSignatureEcdsa256.LEN.SIGNATURE // 8)))

        image_tlv_signature = ImageTlvSignatureEcdsa256(
            type=HexList("FFFF"), length=HexList("FFFF"),
            signature=HexList("FF" * (ImageTlvSignatureEcdsa256.LEN.SIGNATURE // 8)))
        self.assertEqual(to_int(image_tlv_signature.type), 0xFFFF)
        self.assertEqual(to_int(image_tlv_signature.length), 0xFFFF)
        self.assertEqual(image_tlv_signature.signature, HexList("FF" * (ImageTlvSignatureEcdsa256.LEN.SIGNATURE // 8)))
    # end def test_image_tlv_signature_ecdsa_256_hash

    def test_image_tlv_signature_ecdsa_256_from_hexlist(self):
        """
        Test TLV Signature ECDSA 256 class instantiation from HexList
        """
        data = HexList('')
        image_tlv = ImageTlvSignatureEcdsa256()
        for field in ImageTlvSignatureEcdsa256.FIELDS:
            field_data = RandHexList(field.length // 8)
            setattr(image_tlv, field.name,
                    to_int(field_data, little_endian=False if field.name == 'signature' else True))
            data += field_data
        # end for
        image_tlv_from_hexlist = ImageTlvSignatureEcdsa256.fromHexList(data)
        self.assertEqual(data, HexList(image_tlv_from_hexlist))
        self.assertEqual(data, HexList(image_tlv))
        self.assertEqual(image_tlv_from_hexlist, image_tlv)
    # end def test_image_tlv_signature_ecdsa_256_from_hexlist

    def test_image_tlv_list(self):
        """
        Test image TLV list class instantiation
        """
        slot_hash = ImageTlvSlotHash.fromHexList(HexList("00" * (ImageTlvSlotHash.get_total_length() // 8)))
        key_hash = ImageTlvKeyHash.fromHexList(HexList("00" * (ImageTlvKeyHash.get_total_length() // 8)))
        signature = ImageTlvSignatureEcdsa256.fromHexList(
            HexList("00" * (ImageTlvSignatureEcdsa256.get_total_length() // 8)))
        image_tlv_list = ImageTlvList(slot_hash=slot_hash, key_hash=key_hash, signature=signature)
        self.assertEqual(HexList(image_tlv_list.slot_hash), HexList("00" * (ImageTlvSlotHash.get_total_length() // 8)))
        self.assertEqual(HexList(image_tlv_list.key_hash), HexList("00" * (ImageTlvKeyHash.get_total_length() // 8)))
        self.assertEqual(HexList(image_tlv_list.signature),
                         HexList("00" * (ImageTlvSignatureEcdsa256.get_total_length() // 8)))

        slot_hash = ImageTlvSlotHash.fromHexList(HexList("FF" * (ImageTlvSlotHash.get_total_length() // 8)))
        key_hash = ImageTlvKeyHash.fromHexList(HexList("FF" * (ImageTlvKeyHash.get_total_length() // 8)))
        signature = ImageTlvSignatureEcdsa256.fromHexList(
            HexList("FF" * (ImageTlvSignatureEcdsa256.get_total_length() // 8)))
        image_tlv_list = ImageTlvList(slot_hash=slot_hash, key_hash=key_hash, signature=signature)
        self.assertEqual(HexList(image_tlv_list.slot_hash), HexList("FF" * (ImageTlvSlotHash.get_total_length() // 8)))
        self.assertEqual(HexList(image_tlv_list.key_hash), HexList("FF" * (ImageTlvKeyHash.get_total_length() // 8)))
        self.assertEqual(HexList(image_tlv_list.signature),
                         HexList("FF" * (ImageTlvSignatureEcdsa256.get_total_length() // 8)))
    # end def test_image_tlv_list

    def test_image_tlv_list_from_hexlist(self):
        """
        Test TLV List class instantiation from HexList
        """
        slot_hash_data = RandHexList(ImageTlvSlotHash.get_total_length() // 8)
        key_hash_data = RandHexList(ImageTlvKeyHash.get_total_length() // 8)
        signature_data = RandHexList(ImageTlvSignatureEcdsa256.get_total_length() // 8)
        signature_data[:ImageTlvSignatureEcdsa256.LEN.TYPE // 8] = HexList(Numeral(
            ImageTlvSignatureEcdsa256.DEFAULT.TYPE, byteCount=2, littleEndian=True))
        data = slot_hash_data + key_hash_data + signature_data
        image_tlv_list_from_hexlist = ImageTlvList.fromHexList(data)
        slot_hash = ImageTlvSlotHash.fromHexList(slot_hash_data)
        key_hash = ImageTlvKeyHash.fromHexList(key_hash_data)
        signature = ImageTlvSignatureEcdsa256.fromHexList(signature_data)
        image_tlv_list = ImageTlvList(slot_hash=slot_hash, key_hash=key_hash, signature=signature)
        self.assertEqual(data, HexList(image_tlv_list_from_hexlist))
        self.assertEqual(data, HexList(image_tlv_list))
        self.assertEqual(image_tlv_list_from_hexlist, image_tlv_list)
    # end def test_image_tlv_list_from_hexlist
# end class ImageFormatTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
