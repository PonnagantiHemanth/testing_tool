#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcuboot.imageformat
:brief: Image format definition
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date:   2022/11/18
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from copy import deepcopy
from enum import IntEnum

from cryptography import x509

from pyhid.bitfield import BitField
from pyhid.bitfield import byte_field_from_hex_list
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.tools.docutils import DocUtils
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
class MagicNumbers(IntEnum):
    """
    Magic Numbers
    """
    IMAGE_MAGIC = 0x96f3b83d
    IMAGE_TLV_INFO_MAGIC = 0x6907
    IMAGE_TLV_PROT_INFO_MAGIC = 0x6908
    BIC_COMM_MAGIC = 0xB00710AD  # Bootloader Image Communication
    KEY_HIERARCHY_MAGIC = 0x5AFEDA7A  # Key Hierarchy Header
# end class MagicNumbers


class ImageHeaderFlags(IntEnum):
    """
    Image header flags
    """
    IMAGE_F_PIC = 0x00000001  # Not supported.
    IMAGE_F_ENCRYPTED_AES128 = 0x00000004  # Encrypted using AES128.
    IMAGE_F_ENCRYPTED_AES256 = 0x00000008  # Encrypted using AES256
    IMAGE_F_NON_BOOTABLE = 0x00000010  # Split image app.
    IMAGE_F_RAM_LOAD = 0x00000020
# end class ImageHeaderFlags


class ImageTrailerTLVTypes(IntEnum):
    """
    Image trailer TLV types.
    """
    IMAGE_TLV_KEYHASH = 0x01  # hash of the public key
    IMAGE_TLV_SHA256 = 0x10  # SHA256 of image hdr and body
    IMAGE_TLV_RSA2048_PSS = 0x20  # RSA2048 of hash output
    IMAGE_TLV_ECDSA224 = 0x21  # ECDSA of hash output
    IMAGE_TLV_ECDSA256 = 0x22  # ECDSA of hash output
    IMAGE_TLV_RSA3072_PSS = 0x23  # RSA3072 of hash output
    IMAGE_TLV_ED25519 = 0x24  # ED25519 of hash output
    IMAGE_TLV_ENC_RSA2048 = 0x30  # Key encrypted with RSA-OAEP-2048
    IMAGE_TLV_ENC_KW = 0x31  # Key encrypted with AES-KW-128 or 256
    IMAGE_TLV_ENC_EC256 = 0x32  # Key encrypted with ECIES-P256
    IMAGE_TLV_ENC_X25519 = 0x33  # Key encrypted with ECIES-X25519
    IMAGE_TLV_DEPENDENCY = 0x40  # Image depends on other image
    IMAGE_TLV_SEC_CNT = 0x50  # security counter
# end class ImageTrailerTLVTypes


# Public key is a point on the P-256 elliptic curve encoded using the uncompressed format defined in SEC 1,
# i.e. composed of a byte equal to 4, followed by the 2 unsigned 32-byte X/Y coordinates in big-endian order.
SEC_1_UNCOMPRESSED_PUBLIC_KEY_SIZE = 1 + 2 * 32


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LittleEndianBitField(BitField):
    """
    BitField with little endian byte order value
    """

    def __init__(self, fid=None, length=0x00, fid_length=0x00, len_length=0x00, default_value=None,
                 title='Undefined Field', name=None, checks=None, conversions=None, aliases=tuple(), optional=None,
                 parser=None, interpreter=None):
        # See ``BitField.__init__
        parser = self.parser if parser is None else parser
        super().__init__(fid=fid, length=length, fid_length=fid_length, len_length=len_length,
                         default_value=default_value, title=title, name=name, checks=checks, conversions=conversions,
                         aliases=aliases, optional=optional, parser=parser, interpreter=interpreter)
    # end def __init__

    @staticmethod
    @DocUtils.copy_doc(byte_field_from_hex_list)
    def parser(container, bit_field, data, offset=0, limit=None, except_on_overflow=True):
        # See ``byte_field_from_hex_list``
        offset, value = byte_field_from_hex_list(container, bit_field, data, offset, limit, except_on_overflow)
        value.reverse()
        return offset, value
    # end def parser

    @staticmethod
    def serializer(value):
        """
        Serialize value

        :param value: Bitfield value to serialize
        :type value: ``int`` or ``HexList``

        :return: Serialized value
        :rtype: ``HexList``
        """
        value = HexList(value)
        value.reverse()
        return value
    # end def serializer
# end class LittleEndianBitField


class ImageVersion(BitFieldContainerMixin):
    """
    Define format of image version

    Source: bootloader/logi_mcuboot/external/mcuboot/docs/design.md

    struct image_version {
        uint8_t iv_major;
        uint8_t iv_minor;
        uint16_t iv_revision;
        uint32_t iv_build_num;
    };
    """

    class LEN:
        """
        Field lengths in bits
        """
        MAJOR = 8
        MINOR = 8
        REVISION = 16
        BUILD_NUM = 32
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        MAJOR = 0xFF
        MINOR = MAJOR - 1
        REVISION = MINOR - 1
        BUILD_NUM = REVISION - 1
    # end class FID

    FIELDS = (
        LittleEndianBitField(
            fid=FID.MAJOR,
            length=LEN.MAJOR,
            title='Major',
            name='major',
            aliases=('iv_major',),
            checks=(CheckHexList(LEN.MAJOR // 8), CheckInt(0, pow(2, LEN.MAJOR) - 1),)),
        LittleEndianBitField(
            fid=FID.MINOR,
            length=LEN.MINOR,
            title='Minor',
            name='minor',
            aliases=('iv_minor',),
            checks=(CheckHexList(LEN.MINOR // 8), CheckInt(0, pow(2, LEN.MINOR) - 1),)),
        LittleEndianBitField(
            fid=FID.REVISION,
            length=LEN.REVISION,
            title='Revision',
            name='revision',
            aliases=('iv_revision',),
            checks=(CheckHexList(LEN.REVISION // 8), CheckInt(0, pow(2, LEN.REVISION) - 1),)),
        LittleEndianBitField(
            fid=FID.BUILD_NUM,
            length=LEN.BUILD_NUM,
            title='BuildNum',
            name='build_num',
            aliases=('build_number', 'iv_build_num'),
            checks=(CheckHexList(LEN.BUILD_NUM // 8), CheckInt(0, pow(2, LEN.BUILD_NUM) - 1),)),
    )

    def __gt__(self, other):
        # See __gt__
        # Leverage built-in tuple comparison to compare fields
        self_tuple = tuple([self.getValue(field.fid) for field in self.FIELDS])
        other_tuple = tuple([other.getValue(field.fid) for field in other.FIELDS])
        return self_tuple > other_tuple
    # end def __gt__

    def __ge__(self, other):
        # See __ge__
        return self == other or self > other
    # end def __ge__
# end class ImageVersion


class ImageHeader(BitFieldContainerMixin):
    """
    Define image header

    Source: bootloader/logi_mcuboot/external/mcuboot/docs/design.md

    All fields are in little endian byte order
    struct image_header {
        uint32_t ih_magic;
        uint32_t ih_load_addr;
        uint16_t ih_hdr_size;           /* Size of image header (bytes). */
        uint16_t ih_protect_tlv_size;   /* Size of protected TLV area (bytes). */
        uint32_t ih_img_size;           /* Does not include header. */
        uint32_t ih_flags;              /* IMAGE_F_[...]. */
        struct image_version ih_ver;
        uint32_t _pad1;
    };
    """

    class LEN:
        """
        Field lengths in bits
        """
        MAGIC = 32
        LOAD_ADDR = 32
        HEADER_SIZE = 16
        PROTECT_TLV_SIZE = 16
        IMAGE_SIZE = 32
        FLAGS = 32
        IMAGE_VERSION = ImageVersion.get_total_length()
        PAD1 = 32
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        MAGIC = 0xFF
        LOAD_ADDR = MAGIC - 1
        HEADER_SIZE = LOAD_ADDR - 1
        PROTECT_TLV_SIZE = HEADER_SIZE - 1
        IMAGE_SIZE = PROTECT_TLV_SIZE - 1
        FLAGS = IMAGE_SIZE - 1
        IMAGE_VERSION = FLAGS - 1
        PAD1 = IMAGE_VERSION - 1
    # end class FID

    FIELDS = (
        LittleEndianBitField(
            fid=FID.MAGIC,
            length=LEN.MAGIC,
            title='Magic',
            name='magic',
            aliases=('ih_magic',),
            checks=(CheckHexList(LEN.MAGIC // 8), CheckInt(0, pow(2, LEN.MAGIC) - 1),),
            default_value=HexList('{:02X}'.format(MagicNumbers.IMAGE_MAGIC))),
        LittleEndianBitField(
            fid=FID.LOAD_ADDR,
            length=LEN.LOAD_ADDR,
            title='LoadAddr',
            name='load_addr',
            aliases=('ih_load_addr',),
            checks=(CheckHexList(LEN.LOAD_ADDR // 8), CheckInt(0, pow(2, LEN.LOAD_ADDR) - 1),)),
        LittleEndianBitField(
            fid=FID.HEADER_SIZE,
            length=LEN.HEADER_SIZE,
            title='HeaderSize',
            name='header_size',
            aliases=('hdr_size', 'ih_hdr_size',),
            checks=(CheckHexList(LEN.HEADER_SIZE // 8), CheckInt(0, pow(2, LEN.HEADER_SIZE) - 1),)),
        LittleEndianBitField(
            fid=FID.PROTECT_TLV_SIZE,
            length=LEN.PROTECT_TLV_SIZE,
            title='ProtectTlvSize',
            name='protect_tlv_size',
            aliases=('ih_protect_tlv_size',),
            checks=(CheckHexList(LEN.PROTECT_TLV_SIZE // 8), CheckInt(0, pow(2, LEN.PROTECT_TLV_SIZE) - 1),)),
        LittleEndianBitField(
            fid=FID.IMAGE_SIZE,
            length=LEN.IMAGE_SIZE,
            title='ImageSize',
            name='image_size',
            aliases=('ih_img_size', 'img_size'),
            checks=(CheckHexList(LEN.IMAGE_SIZE // 8), CheckInt(0, pow(2, LEN.IMAGE_SIZE) - 1),)),
        LittleEndianBitField(
            fid=FID.FLAGS,
            length=LEN.FLAGS,
            title='Flags',
            name='flags',
            aliases=('ih_flags',),
            checks=(CheckHexList(LEN.FLAGS // 8), CheckInt(0, pow(2, LEN.FLAGS) - 1),)),
        BitField(
            fid=FID.IMAGE_VERSION,
            length=LEN.IMAGE_VERSION,
            title='ImageVersion',
            name='image_version',
            aliases=('ih_image_version',),
            checks=(CheckHexList(LEN.IMAGE_VERSION // 8), CheckInt(0, pow(2, LEN.IMAGE_VERSION) - 1)),
            parser=ImageVersion.fromHexList),
        LittleEndianBitField(
            fid=FID.PAD1,
            length=LEN.PAD1,
            title='Pad1',
            name='pad_1',
            aliases=('_pad1',),
            checks=(CheckHexList(LEN.PAD1 // 8), CheckInt(0, pow(2, LEN.PAD1) - 1),),
            default_value=HexList("00" * (LEN.PAD1 // 8)),)
    )
# end class ImageHeader


class KeyHierarchyPairInterface(BitFieldContainerMixin):
    """
    Define public-key/signature pair in the key hierarchy
    """
    class FID:
        """
        Field Identifiers
        """
        PUBLIC_KEY = 0xFF
        SIGNATURE = PUBLIC_KEY - 1
    # end class FID

    class LEN:
        """
        Field lengths in bits
        """
        # Key size placeholder
        PUBLIC_KEY = 0
        SIGNATURE = 0
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.PUBLIC_KEY,
            length=LEN.PUBLIC_KEY,
            title='PublicKey',
            name='public_key',
        ),
        BitField(
            fid=FID.SIGNATURE,
            length=LEN.SIGNATURE,
            title='Signature',
            name='signature',
        ),
    )
# end class KeyHierarchyPairInterface


class KeyHierarchyHeader(BitFieldContainerMixin):
    """
    Define key hierarchy header format
    """

    class EcPair(KeyHierarchyPairInterface):
        """
        Define public-key/signature EC pair in the key hierarchy
        """
        class LEN(KeyHierarchyPairInterface.LEN):
            # See ``KeyHierarchyPairInterface.LEN``

            PUBLIC_KEY = SEC_1_UNCOMPRESSED_PUBLIC_KEY_SIZE * 8
            # Each ECDSA-P-256 signature [7], using SHA-256 hash [6], shall be encoded in raw format. That is, it is
            # composed of the 2 unsigned 32-byte R and S values in big-endian order.
            SIGNATURE = 64 * 8
        # end class LEN

        FIELDS = deepcopy(KeyHierarchyPairInterface.FIELDS)
        [hash for hash in FIELDS if hash.name == 'public_key'][0].length = LEN.PUBLIC_KEY
        [hash for hash in FIELDS if hash.name == 'public_key'][0].checks = (
            CheckHexList(LEN.PUBLIC_KEY // 8), CheckInt(0, pow(2, LEN.PUBLIC_KEY) - 1),)
        [hash for hash in FIELDS if hash.name == 'signature'][0].length = LEN.SIGNATURE
        [hash for hash in FIELDS if hash.name == 'signature'][0].checks = (
            CheckHexList(LEN.SIGNATURE // 8), CheckInt(0, pow(2, LEN.SIGNATURE) - 1),)
    # end class EcPair

    class Rsa2048Pair(KeyHierarchyPairInterface):
        """
        Define public-key/signature RSA 2048 pair in the key hierarchy
        """

        class LEN(KeyHierarchyPairInterface.LEN):
            # See ``KeyHierarchyPairInterface.LEN``

            # Each public key shall contain only the key modulus, given as a byte array in big-endian order.  The
            # modulus length is "cfg_SIGN_RSA_KEY_LGTH" bits, therefore, the array size is the same value divided by
            # 8. The public-key exponent is hard-coded and given by the macro "cfg_SIGN_RSA_KEY_EXP" (same exponent
            # for all RSA public keys).
            PUBLIC_KEY = 8 * 256
            # Each RSA-PSS signature [4], using SHA-256 hash [6], shall be given in raw format.  That is,
            # it is an unsigned value of the same size as the modulus, in big-endian order.  The SHA-256 function
            # shall be used for all hash operations: message hashing, salted-hash hashing, and for the MGF. The salt
            # size shall be equal to the hash size (32 bytes).
            SIGNATURE = PUBLIC_KEY
        # end class LEN

        FIELDS = deepcopy(KeyHierarchyPairInterface.FIELDS)
        [hash for hash in FIELDS if hash.name == 'public_key'][0].length = LEN.PUBLIC_KEY
        [hash for hash in FIELDS if hash.name == 'public_key'][0].checks = (
            CheckHexList(LEN.PUBLIC_KEY // 8), CheckInt(0, pow(2, LEN.PUBLIC_KEY) - 1),)
        [hash for hash in FIELDS if hash.name == 'signature'][0].length = LEN.SIGNATURE
        [hash for hash in FIELDS if hash.name == 'signature'][0].checks = (
            CheckHexList(LEN.SIGNATURE // 8), CheckInt(0, pow(2, LEN.SIGNATURE) - 1),)
    # end class Rsa2048Pair

    class Rsa3072Pair(KeyHierarchyPairInterface):
        """
        Define public-key/signature RSA 3072 pair in the key hierarchy
        """

        class LEN(KeyHierarchyPairInterface.LEN):
            # See ``KeyHierarchyPairInterface.LEN``

            # Each public key shall contain only the key modulus, given as a byte array in big-endian order.  The
            # modulus length is "cfg_SIGN_RSA_KEY_LGTH" bits, therefore, the array size is the same value divided by
            # 8. The public-key exponent is hard-coded and given by the macro "cfg_SIGN_RSA_KEY_EXP" (same exponent
            # for all RSA public keys).
            PUBLIC_KEY = 8 * 384
            # Each RSA-PSS signature [4], using SHA-256 hash [6], shall be given in raw format.  That is,
            # it is an unsigned value of the same size as the modulus, in big-endian order.  The SHA-256 function
            # shall be used for all hash operations: message hashing, salted-hash hashing, and for the MGF. The salt
            # size shall be equal to the hash size (32 bytes).
            SIGNATURE = PUBLIC_KEY
        # end class LEN

        FIELDS = deepcopy(KeyHierarchyPairInterface.FIELDS)
        [hash for hash in FIELDS if hash.name == 'public_key'][0].length = LEN.PUBLIC_KEY
        [hash for hash in FIELDS if hash.name == 'public_key'][0].checks = (
            CheckHexList(LEN.PUBLIC_KEY // 8), CheckInt(0, pow(2, LEN.PUBLIC_KEY) - 1),)
        [hash for hash in FIELDS if hash.name == 'signature'][0].length = LEN.SIGNATURE
        [hash for hash in FIELDS if hash.name == 'signature'][0].checks = (
            CheckHexList(LEN.SIGNATURE // 8), CheckInt(0, pow(2, LEN.SIGNATURE) - 1),)
    # end class Rsa3072Pair

    class PairsTable(list):
        """
        Define public-key/signature pairs table in the key hierarchy table
        """

        @classmethod
        def from_hex_list(cls, hex_list, pair_class):
            """
            Parsing from HexList instance

            :param hex_list: Raw pairs table
            :type hex_list: ``HexList``
            :param pair_class: Pair type
            :type pair_class: ``KeyHierarchyHeader.Pair``

            :return: Class instance
            :rtype: ``PairsTable``
            """
            pairs_table = []
            pair_len = sum([field.length for field in pair_class.FIELDS]) // 8
            pair_start = 0
            pair_end = pair_start + pair_len
            while pair_end <= len(hex_list):
                pairs_table.append(pair_class.fromHexList(hex_list[pair_start:pair_end]))
                pair_start = pair_end
                pair_end = pair_start + pair_len
            # end while
            return cls(pairs_table)
        # end def from_hex_list
    # end class PairsTable

    class EcPairsTable(PairsTable):
        """
        Define EC public-key/signature pairs table in the key hierarchy table
        """

        @staticmethod
        # Keep the same naming as ``BitFieldContainerMixin``
        def fromHexList(hex_list):
            """
            Parsing from HexList instance

            :param hex_list: Raw pairs table
            :type hex_list: ``HexList``

            :return: Class instance
            :rtype: ``PairsTable``
            """
            return KeyHierarchyHeader.PairsTable.from_hex_list(hex_list, KeyHierarchyHeader.EcPair)
        # end def fromHexList
    # end class EcPairsTable

    class Rsa2048PairsTable(PairsTable):
        """
        Define RSA 2048 public-key/signature pairs table in the key hierarchy table
        """

        @staticmethod
        # Keep the same naming as ``BitFieldContainerMixin``
        def fromHexList(hex_list):
            """
            Parsing from HexList instance

            :param hex_list: Raw pairs table
            :type hex_list: ``HexList``

            :return: Class instance
            :rtype: ``PairsTable``
            """
            return KeyHierarchyHeader.PairsTable.from_hex_list(hex_list, KeyHierarchyHeader.Rsa2048Pair)
        # end def fromHexList
    # end class Rsa2048PairsTable

    class Rsa3072PairsTable(PairsTable):
        """
        Define RSA 3072 public-key/signature pairs table in the key hierarchy table
        """

        @staticmethod
        # Keep the same naming as ``BitFieldContainerMixin``
        def fromHexList(hex_list):
            """
            Parsing from HexList instance

            :param hex_list: Raw pairs table
            :type hex_list: ``HexList``

            :return: Class instance
            :rtype: ``PairsTable``
            """
            return KeyHierarchyHeader.PairsTable.from_hex_list(hex_list, KeyHierarchyHeader.Rsa3072Pair)
        # end def fromHexList
    # end class Rsa3072PairsTable

    class X509CertificateKeyHierarchyEntry:
        def __init__(self, raw, certificate):
            """
            :param raw: Raw certificate, as stored in key hierarchy table
            :type raw: ``HexList``
            :param certificate: The certificate
            :type certificate: ``x509.Certificate``
            """
            self.raw = raw
            self.certificate = certificate
            self.public_key = self.certificate.public_key()
            self.signature = self.certificate.signature
        # end def __init__

        def __hexlist__(self):
            """
            Convert the current object to an ``HexList``

            :return: The ``HexList`` representation of the current object.
            :rtype: ``HexList``
            """
            return self.raw
        # end def __hexlist__
    # end class X509CertificateKeyHierarchyEntry

    class X509CertificatesTable(list):
        """
        Define X509 Certificates in the key hierarchy table when Elliptic Curve is used
        """

        @classmethod
        # Keep the same naming as ``BitFieldContainerMixin``
        def fromHexList(cls, hex_list):
            """
            Parsing from HexList instance

            :param hex_list: Raw pairs table
            :type hex_list: ``HexList``

            :return: Class instance
            :rtype: ``PairsTable``
            """

            table = []
            start_index = 0
            for end_index in range(len(hex_list) - 1):
                try:
                    cert = x509.load_der_x509_certificate(bytes(hex_list[start_index:end_index]))
                    entry = KeyHierarchyHeader.X509CertificateKeyHierarchyEntry(raw=hex_list[start_index:end_index],
                                                                                certificate=cert)
                    table.append(entry)
                    start_index = end_index
                except ValueError:
                    if hex_list[start_index:] == HexList("FF" * len(hex_list[start_index:])):
                        break
                    else:
                        continue
                    # end if
                # end try
            # end for
            return cls(table)
        # end def fromHexList
    # end class X509CertificatesTable

    class FID:
        """
        Field Identifiers
        """
        MAGIC_NUMBER = 0xFF
        ROOT_OF_TRUST_INDEX = MAGIC_NUMBER - 1
        KEY_COUNT = ROOT_OF_TRUST_INDEX - 1
        RESERVED = KEY_COUNT - 1
    # end class FID

    class LEN:
        """
        Field lengths in bits
        """
        MAGIC_NUMBER = 4 * 8
        ROOT_OF_TRUST_INDEX = 8
        KEY_COUNT = 8
        RESERVED = 2 * 8
    # end class LEN

    class DEFAULT:
        """
        Default values
        """
        RESERVED = 0x0000
    # end class DEFAULT

    FIELDS = (
        LittleEndianBitField(
            fid=FID.MAGIC_NUMBER,
            length=LEN.MAGIC_NUMBER,
            title='MagicNumber',
            name='magic_number',
            checks=(CheckHexList(LEN.MAGIC_NUMBER // 8), CheckInt(0, pow(2, LEN.MAGIC_NUMBER) - 1),)),
        LittleEndianBitField(
            fid=FID.ROOT_OF_TRUST_INDEX,
            length=LEN.ROOT_OF_TRUST_INDEX,
            title='RootOfTrustIndex',
            name='root_of_trust_index',
            checks=(CheckHexList(LEN.ROOT_OF_TRUST_INDEX // 8), CheckInt(0, pow(2, LEN.ROOT_OF_TRUST_INDEX) - 1),)),
        LittleEndianBitField(
            fid=FID.KEY_COUNT,
            length=LEN.KEY_COUNT,
            title='KeyCount',
            name='key_count',
            checks=(CheckHexList(LEN.KEY_COUNT // 8), CheckInt(0, pow(2, LEN.KEY_COUNT) - 1),)),
        LittleEndianBitField(
            fid=FID.RESERVED,
            length=LEN.RESERVED,
            title='Reserved',
            name='reserved',
            default_value=DEFAULT.RESERVED,
            checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
    )
# end class KeyHierarchyHeader


class ImageTlvInfo(BitFieldContainerMixin):
    """
    Define Image TLV header format

    Source: bootloader/logi_mcuboot/external/mcuboot/docs/design.md

    All fields in little endian
    struct image_tlv_info {
        uint16_t it_magic;
        uint16_t it_tlv_tot;  /* size of TLV area (including tlv_info header) */
    };
    """

    class LEN:
        """
        Field lengths in bits
        """
        MAGIC = 16
        TLV_TOT = 16
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        MAGIC = 0xFF
        TLV_TOT = MAGIC - 1
    # end class FID

    FIELDS = (
        LittleEndianBitField(
            fid=FID.MAGIC,
            length=LEN.MAGIC,
            title='Magic',
            name='magic',
            aliases=('it_magic',),
            checks=(CheckHexList(LEN.MAGIC // 8), CheckInt(0, pow(2, LEN.MAGIC) - 1),)),
        LittleEndianBitField(
            fid=FID.TLV_TOT,
            length=LEN.TLV_TOT,
            title='TlvTot',
            name='tlv_tot',
            aliases=('it_tlv_tot',),
            checks=(CheckHexList(LEN.TLV_TOT // 8), CheckInt(0, pow(2, LEN.TLV_TOT) - 1),)),
    )
# end class ImageTlvInfo


class ImageTlv(BitFieldContainerMixin):
    """
    Define Image trailer TLV format

    Source: bootloader/logi_mcuboot/external/mcuboot/docs/design.md

    struct image_tlv {
        uint8_t  it_type;   /* IMAGE_TLV_[...]. */
        uint8_t  _pad;
        uint16_t it_len;    /* Data length (not including TLV header). */
    };

    But according to the implementation in
    bootloader\logi_mcuboot\external\mcuboot\boot\bootutil\include\bootutil\image.h:

    struct image_tlv {
        uint16_t it_type;   /* IMAGE_TLV_[...]. */
        uint16_t it_len;    /* Data length (not including TLV header). */
    };

    So we choose to follow the implemented structure with type on 16 bits
    """

    class LEN:
        """
        Field lengths in bits
        """
        TYPE = 16
        LENGTH = 16
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        TYPE = 0xFF
        LENGTH = TYPE - 1
    # end class FID

    FIELDS = (
        LittleEndianBitField(
            fid=FID.TYPE,
            length=LEN.TYPE,
            title='Type',
            name='type',
            aliases=('it_type',),
            checks=(CheckHexList(LEN.TYPE // 8), CheckInt(0, pow(2, LEN.TYPE) - 1),)),
        LittleEndianBitField(
            fid=FID.LENGTH,
            length=LEN.LENGTH,
            title='Length',
            name='length',
            aliases=('it_len',),
            checks=(CheckHexList(LEN.LENGTH // 8), CheckInt(0, pow(2, LEN.LENGTH) - 1),)),
    )
# end class ImageTlv


class ImageTlvSha256Hash(ImageTlv):
    """
    Generic TLV SHA-256 Hash class
    """

    class LEN(ImageTlv.LEN):
        # See ``ImageTlv.LEN``
        SHA_256_HASH = 8 * 32
    # end class LEN

    class FID(ImageTlv.FID):
        # See ``ImageTlv.FID``
        SHA_256_HASH = ImageTlv.FID.LENGTH - 1
    # end class FID

    FIELDS = ImageTlv.FIELDS + (
        BitField(
            fid=FID.SHA_256_HASH,
            length=LEN.SHA_256_HASH,
            title='Sha256Hash',
            name='sha_256_hash',
            aliases=('value',),
            checks=(CheckHexList(LEN.SHA_256_HASH // 8), CheckInt(0, pow(2, LEN.SHA_256_HASH) - 1),)),
    )
# end class ImageTlvSha256Hash


class ImageTlvKeyHash(ImageTlvSha256Hash):
    """
    SHA-256 hash [1] of the public signature key.  This hash is represented in big-endian format.

    +----------------------------------+
    | Type: 0x0001 (2 bytes)           | IMAGE_TLV_KEYHASH
    +- - - - - - - - - - - - - - - - - +
    | Length: 32 (2 bytes)             |
    +- - - - - - - - - - - - - - - - - +
    | Value: SHA-256 hash (32 bytes)   |
    +----------------------------------+
    """
    class DEFAULT:
        """
        Field default values
        """
        TYPE = ImageTrailerTLVTypes.IMAGE_TLV_KEYHASH
        LENGTH = 32
    # end class DEFAULT

    FIELDS = deepcopy(ImageTlvSha256Hash.FIELDS)
    [hash for hash in FIELDS if hash.name == 'type'][0].default_value = DEFAULT.TYPE
    [hash for hash in FIELDS if hash.name == 'length'][0].default_value = DEFAULT.LENGTH
    [hash for hash in FIELDS if hash.name == 'sha_256_hash'][0].aliases += ('key_hash',)
# end class ImageTlvKeyHash


class ImageTlvSlotHash(ImageTlvSha256Hash):
    """
    SHA-256 hash [1] of the slot header (incl. padding), the slot image, and the protected TLV list. This hash is
    represented in big-endian format.

    +----------------------------------+
    | Type: 0x0010 (2 bytes)           | IMAGE_TLV_SHA256
    +- - - - - - - - - - - - - - - - - +
    | Length: 32 (2 bytes)             |
    +- - - - - - - - - - - - - - - - - +
    | Value: SHA-256 hash (32 bytes)   |
    +----------------------------------+
    """
    class DEFAULT:
        """
        Field default values
        """
        TYPE = ImageTrailerTLVTypes.IMAGE_TLV_SHA256
        LENGTH = 32
    # end class DEFAULT

    FIELDS = deepcopy(ImageTlvSha256Hash.FIELDS)
    [hash for hash in FIELDS if hash.name == 'type'][0].default_value = DEFAULT.TYPE
    [hash for hash in FIELDS if hash.name == 'length'][0].default_value = DEFAULT.LENGTH
    [hash for hash in FIELDS if hash.name == 'sha_256_hash'][0].aliases += ('slot_hash',)
# end class ImageTlvSlotHash


class ImageTlvSignatureEcdsa256(ImageTlv):
    """
    ECDSA-P-256 signature [2], using SHA-256 hash [1], of the slot header
    (incl. padding), the slot image, and the protected TLV list.  This
    signature is represented in distinguished encoding rule (DER) format (all
    numbers are in big-endian format).

    +----------------------------------+
    | Type: 0x0022 (2 bytes)           | IMAGE_TLV_ECDSA256
    +- - - - - - - - - - - - - - - - - +
    | Length: 70-72 (2 bytes)          |
    +- - - - - - - - - - - - - - - - - +
    | Value: signature (70-72 bytes)   |
    +----------------------------------+
    """
    class LEN(ImageTlv.LEN):
        # See ``ImageTlv.LEN``
        MIN_SIGNATURE = 8 * 70
        MAX_SIGNATURE = 8 * 72
        SIGNATURE = MAX_SIGNATURE
    # end class LEN

    class FID(ImageTlv.FID):
        # See ``ImageTlv.FID``
        SIGNATURE = ImageTlv.FID.LENGTH - 1
    # end class FID

    class DEFAULT:
        """
        Field default values
        """
        TYPE = ImageTrailerTLVTypes.IMAGE_TLV_ECDSA256
    # end class DEFAULT

    FIELDS = ImageTlv.FIELDS + (
        BitField(
            fid=FID.SIGNATURE,
            length=LEN.SIGNATURE,
            title='Signature',
            name='signature',
            aliases=('ecdsa_p_256_signature',),
            checks=(CheckHexList(max_length=(LEN.MAX_SIGNATURE // 8), min_length=(LEN.MIN_SIGNATURE // 8)),
                    CheckInt(0, pow(2, LEN.SIGNATURE) - 1),)),
    )
# end class ImageTlvSignatureEcdsa256


class ImageTlvSignatureRsa3072(ImageTlv):
    """
    PKCS #1 RSA-PSS signature [1], using a 3072-bit key and SHA-256 hash [2],
    of the slot header (incl. padding), the slot image, and the protected TLV
    list.  The SHA-256 function shall be used for all hash operations: message
    hashing, salted-hash hashing, and for the mask generation function (MGF).
    The salt size shall be equal to the hash size (32 bytes).  This signature
    is represented in big-endian order.

    +----------------------------------+
    | Type: 0x0023 (2 bytes)           | IMAGE_TLV_RSA3072_PSS
    +- - - - - - - - - - - - - - - - - +
    | Length: 384 (2 bytes)            |
    +- - - - - - - - - - - - - - - - - +
    | Value: signature (384 bytes)     |
    +----------------------------------+
    """
    class LEN(ImageTlv.LEN):
        # See ``ImageTlv.LEN``
        SIGNATURE = 8 * 384
    # end class LEN

    class FID(ImageTlv.FID):
        # See ``ImageTlv.FID``
        SIGNATURE = ImageTlv.FID.LENGTH - 1
    # end class FID

    class DEFAULT:
        """
        Field default values
        """
        TYPE = ImageTrailerTLVTypes.IMAGE_TLV_RSA3072_PSS
    # end class DEFAULT

    FIELDS = ImageTlv.FIELDS + (
        BitField(
            fid=FID.SIGNATURE,
            length=LEN.SIGNATURE,
            title='Signature',
            name='signature',
            aliases=('rsa_3072_signature',),
            checks=(CheckHexList(LEN.SIGNATURE // 8), CheckInt(0, pow(2, LEN.SIGNATURE) - 1),)),
    )
# end class ImageTlvSignatureRsa3072


class ImageTlvSignatureRsa2048(ImageTlv):
    """
    PKCS #1 RSA-PSS signature [4], using a 2048-bit key and SHA-256 hash [7],
   of the slot header (incl. padding), the slot image, and the protected TLV
   list.  The SHA-256 function shall be used for all hash operations: message
   hashing, salted-hash hashing, and for the MGF.  The salt size shall be
   equal to the hash size (32 bytes).  This signature is represented in
   big-endian order.

    +----------------------------------+
    | Type: 0x0020 (2 bytes)           | IMAGE_TLV_RSA2048_PSS
    +- - - - - - - - - - - - - - - - - +
    | Length: 256 (2 bytes)            |
    +- - - - - - - - - - - - - - - - - +
    | Value: signature (256 bytes)     |
    +----------------------------------+
    """
    class LEN(ImageTlv.LEN):
        # See ``ImageTlv.LEN``
        SIGNATURE = 8 * 256
    # end class LEN

    class FID(ImageTlv.FID):
        # See ``ImageTlv.FID``
        SIGNATURE = ImageTlv.FID.LENGTH - 1
    # end class FID

    class DEFAULT:
        """
        Field default values
        """
        TYPE = ImageTrailerTLVTypes.IMAGE_TLV_RSA2048_PSS
    # end class DEFAULT

    FIELDS = ImageTlv.FIELDS + (
        BitField(
            fid=FID.SIGNATURE,
            length=LEN.SIGNATURE,
            title='Signature',
            name='signature',
            aliases=('rsa_2048_signature',),
            checks=(CheckHexList(LEN.SIGNATURE // 8), CheckInt(0, pow(2, LEN.SIGNATURE) - 1),)),
    )
# end class ImageTlvSignatureRsa2048


class ImageTlvList(BitFieldContainerMixin):
    """
    Define list of TLV structures
    """

    class LEN:
        """
        Field lengths in bits
        """
        SLOT_HASH = ImageTlvSlotHash.get_total_length()
        KEY_HASH = ImageTlvKeyHash.get_total_length()
        MIN_SIGNATURE = ImageTlv.get_total_length() + ImageTlvSignatureEcdsa256.LEN.MIN_SIGNATURE
        MAX_SIGNATURE = ImageTlvSignatureRsa3072.get_total_length()
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        SLOT_HASH = 0xFF
        KEY_HASH = SLOT_HASH - 1
        SIGNATURE = KEY_HASH - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.SLOT_HASH,
            length=LEN.SLOT_HASH,
            title='SlotHash',
            name='slot_hash',
            checks=(CheckHexList(LEN.SLOT_HASH // 8), CheckInt(0, pow(2, LEN.SLOT_HASH) - 1),)),
        BitField(
            fid=FID.KEY_HASH,
            length=LEN.KEY_HASH,
            title='KeyHash',
            name='key_hash',
            checks=(CheckHexList(LEN.KEY_HASH // 8), CheckInt(0, pow(2, LEN.KEY_HASH) - 1),)),
        BitField(
            fid=FID.SIGNATURE,
            length=LEN.MAX_SIGNATURE,
            title='Signature',
            name='signature',
            checks=(CheckHexList(min_length=(LEN.MIN_SIGNATURE // 8), max_length=(LEN.MAX_SIGNATURE // 8)),)),
    )

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``ImageTlvList``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.slot_hash = ImageTlvSlotHash.fromHexList(
            HexList(inner_field_container_mixin.slot_hash))
        inner_field_container_mixin.key_hash = ImageTlvKeyHash.fromHexList(
            HexList(inner_field_container_mixin.key_hash))

        signature_type = to_int(ImageTlv.fromHexList(inner_field_container_mixin.signature).type)

        type_to_class = {
            int(ImageTlvSignatureEcdsa256.DEFAULT.TYPE): ImageTlvSignatureEcdsa256,
            int(ImageTlvSignatureRsa3072.DEFAULT.TYPE): ImageTlvSignatureRsa3072,
            int(ImageTlvSignatureRsa2048.DEFAULT.TYPE): ImageTlvSignatureRsa2048,
        }

        assert signature_type in type_to_class, f"Signature type {hex(signature_type)} should match a supported type"

        inner_field_container_mixin.signature = type_to_class[signature_type].fromHexList(
            HexList(inner_field_container_mixin.signature))

        return inner_field_container_mixin
    # end def fromHexList
# end class ImageTlvList


class BootImageCommunication(BitFieldContainerMixin):
    """
    Define format of Bootloader Image Communication Structure

    Source: bootloader/logi_mcuboot/ReadMe.txt
    """

    class LEN:
        """
        Field lengths in bits
        """
        MAGIC_NUMBER = 8 * 4
        VERSION = 8
        PREFIX = 8 * 3
        FW_NUMBER = 8
        FW_VERSION = 8
        FW_BUILD_NUMBER = 8 * 2
        GIT_HASH = 8 * 4
        BUILD_FLAGS = 8
        RESERVED = 8 * 3
        BL_TO_IMG_FLAGS = 8 * 2
        IMG_TO_BL_FLAGS = 8 * 2
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        MAGIC_NUMBER = 0xFF
        VERSION = MAGIC_NUMBER - 1
        PREFIX = VERSION - 1
        FW_NUMBER = PREFIX - 1
        FW_VERSION = FW_NUMBER - 1
        FW_BUILD_NUMBER = FW_VERSION - 1
        GIT_HASH = FW_BUILD_NUMBER - 1
        BUILD_FLAGS = GIT_HASH - 1
        RESERVED = BUILD_FLAGS - 1
        BL_TO_IMG_FLAGS = RESERVED - 1
        IMG_TO_BL_FLAGS = BL_TO_IMG_FLAGS - 1
    # end class FID

    FIELDS = (
        LittleEndianBitField(
            fid=FID.MAGIC_NUMBER,
            length=LEN.MAGIC_NUMBER,
            title='MagicNumber',
            name='magic_number',
            checks=(CheckHexList(LEN.MAGIC_NUMBER // 8), CheckInt(0, pow(2, LEN.MAGIC_NUMBER) - 1),)),
        LittleEndianBitField(
            fid=FID.VERSION,
            length=LEN.VERSION,
            title='Version',
            name='version',
            checks=(CheckHexList(LEN.VERSION // 8), CheckInt(0, pow(2, LEN.VERSION) - 1),)),
        LittleEndianBitField(
            fid=FID.PREFIX,
            length=LEN.PREFIX,
            title='Prefix',
            name='prefix',
            checks=(CheckHexList(LEN.PREFIX // 8), CheckInt(0, pow(2, LEN.PREFIX) - 1),)),
        LittleEndianBitField(
            fid=FID.FW_NUMBER,
            length=LEN.FW_NUMBER,
            title='FwNumber',
            name='fw_number',
            checks=(CheckHexList(LEN.FW_NUMBER // 8), CheckInt(0, pow(2, LEN.FW_NUMBER) - 1),)),
        LittleEndianBitField(
            fid=FID.FW_VERSION,
            length=LEN.FW_VERSION,
            title='FwVersion',
            name='fw_version',
            checks=(CheckHexList(LEN.FW_VERSION // 8), CheckInt(0, pow(2, LEN.FW_VERSION) - 1),)),
        LittleEndianBitField(
            fid=FID.FW_BUILD_NUMBER,
            length=LEN.FW_BUILD_NUMBER,
            title='FwBuildNumber',
            name='fw_build_number',
            checks=(CheckHexList(LEN.FW_BUILD_NUMBER // 8), CheckInt(0, pow(2, LEN.FW_BUILD_NUMBER) - 1),)),
        LittleEndianBitField(
            fid=FID.GIT_HASH,
            length=LEN.GIT_HASH,
            title='GitHash',
            name='git_hash',
            checks=(CheckHexList(LEN.GIT_HASH // 8), CheckInt(0, pow(2, LEN.GIT_HASH) - 1),)),
        LittleEndianBitField(
            fid=FID.BUILD_FLAGS,
            length=LEN.BUILD_FLAGS,
            title='BuildFlags',
            name='build_flags',
            checks=(CheckHexList(LEN.BUILD_FLAGS // 8), CheckInt(0, pow(2, LEN.BUILD_FLAGS) - 1),)),
        LittleEndianBitField(
            fid=FID.RESERVED,
            length=LEN.RESERVED,
            title='Reserved',
            name='reserved',
            default_value=HexList("000000"),
            checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
        LittleEndianBitField(
            fid=FID.BL_TO_IMG_FLAGS,
            length=LEN.BL_TO_IMG_FLAGS,
            title='BlToImgFlags',
            name='bl_to_img_flags',
            checks=(CheckHexList(LEN.BL_TO_IMG_FLAGS // 8), CheckInt(0, pow(2, LEN.BL_TO_IMG_FLAGS) - 1),)),
        LittleEndianBitField(
            fid=FID.IMG_TO_BL_FLAGS,
            length=LEN.IMG_TO_BL_FLAGS,
            title='ImgToBlFlags',
            name='img_to_bl_flags',
            checks=(CheckHexList(LEN.IMG_TO_BL_FLAGS // 8), CheckInt(0, pow(2, LEN.IMG_TO_BL_FLAGS) - 1),)),
    )

    class BuildFlags(BitFieldContainerMixin):
        """
        Build Flags:
            * Dirty build Flag (bit 0)
            * Debug build Flag (bit 1)
            * Development credentials flag (bit 3)
        """
        class FID:
            """
            Field identifiers
            """
            RESERVED_4_7 = 0x0FF
            DEVELOPMENT_CREDENTIALS = RESERVED_4_7 - 1
            RESERVED_2 = DEVELOPMENT_CREDENTIALS - 1
            DEBUG_BUILD = RESERVED_2 - 1
            DIRTY_BUILD = DEBUG_BUILD - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            RESERVED_4_7 = 4
            DEVELOPMENT_CREDENTIALS = 1
            RESERVED_2 = 1
            DEBUG_BUILD = 1
            DIRTY_BUILD = 1
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            RESERVED_4_7 = 0x00
            DEVELOPMENT_CREDENTIALS = 0
            RESERVED_2 = 0
            DEBUG_BUILD = 0
            DIRTY_BUILD = 0
        # end class DEFAULT

        FIELDS = (
            BitField(FID.RESERVED_4_7,
                     LEN.RESERVED_4_7,
                     title='Reserved47',
                     name='reserved_4_7',
                     default_value=DEFAULT.RESERVED_4_7,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED_4_7) - 1),)),
            BitField(FID.DEVELOPMENT_CREDENTIALS,
                     LEN.DEVELOPMENT_CREDENTIALS,
                     title='DevelopmentCredentials',
                     name='development_credentials',
                     default_value=DEFAULT.DEVELOPMENT_CREDENTIALS,
                     checks=(CheckInt(0, pow(2, LEN.DEVELOPMENT_CREDENTIALS) - 1),)),
            BitField(FID.RESERVED_2,
                     LEN.RESERVED_2,
                     title='Reserved2',
                     name='reserved_2',
                     default_value=DEFAULT.RESERVED_2,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED_2) - 1),)),
            BitField(FID.DEBUG_BUILD,
                     LEN.DEBUG_BUILD,
                     title='DebugBuild',
                     name='debug_build',
                     default_value=DEFAULT.DEBUG_BUILD,
                     checks=(CheckInt(0, pow(2, LEN.DEBUG_BUILD) - 1),)),
            BitField(FID.DIRTY_BUILD,
                     LEN.DIRTY_BUILD,
                     title='DirtyBuild',
                     name='dirty_build',
                     default_value=DEFAULT.DIRTY_BUILD,
                     checks=(CheckInt(0, pow(2, LEN.DIRTY_BUILD) - 1),)),
        )
    # end class BuildFlags

    class BlToImgFlags(BitFieldContainerMixin):
        """
        Build Flags:
            * Current boot type (bit 0)
            * Currently booted slot (bit 1)
            * Slot availability (bit 2)
        """
        class FID:
            """
            Field identifiers
            """
            RESERVED = 0xFF
            SLOT_AVAILABILITY = RESERVED - 1
            BOOTED_SLOT = SLOT_AVAILABILITY - 1
            BOOT_TYPE = BOOTED_SLOT - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            RESERVED = 13
            SLOT_AVAILABILITY = 1
            BOOTED_SLOT = 1
            BOOT_TYPE = 1
        # end class LEN

        class BootType(IntEnum):
            """
            Boot Type values
            """
            WARM_BOOT = 0
            COLD_BOOT = 1
        # end class BootType

        class BootedSlot(IntEnum):
            """
            Booted Slot values
            """
            DEFAULT_SLOT = 0
            ALTERNATE_SLOT = 1
        # end class BootedSlot

        class DEFAULT:
            """
            Field default values
            """
            RESERVED = 0x0000
            SLOT_AVAILABILITY = 0
            BOOTED_SLOT = 0
            BOOT_TYPE = 0
        # end class DEFAULT

        FIELDS = (
            BitField(FID.RESERVED,
                     LEN.RESERVED,
                     title='Reserved',
                     name='reserved',
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(FID.SLOT_AVAILABILITY,
                     LEN.SLOT_AVAILABILITY,
                     title='SlotAvailability',
                     name='slot_availability',
                     default_value=DEFAULT.SLOT_AVAILABILITY,
                     checks=(CheckInt(0, pow(2, LEN.SLOT_AVAILABILITY) - 1),)),
            BitField(FID.BOOTED_SLOT,
                     LEN.BOOTED_SLOT,
                     title='BootedSlot',
                     name='booted_slot',
                     default_value=DEFAULT.BOOTED_SLOT,
                     checks=(CheckInt(0, pow(2, LEN.BOOTED_SLOT) - 1),)),
            BitField(FID.BOOT_TYPE,
                     LEN.BOOT_TYPE,
                     title='BootType',
                     name='boot_type',
                     default_value=DEFAULT.BOOT_TYPE,
                     checks=(CheckInt(0, pow(2, LEN.BOOT_TYPE) - 1),)),
        )
    # end class BlToImgFlags

    class ImgToBlFlags(BitFieldContainerMixin):
        """
        Build Flags:
            * Cold-boot request (bit 0)
            * Alternate-slot request (bit 1)
        """
        class FID:
            """
            Field identifiers
            """
            RESERVED = 0xFF
            ALTERNATE_SLOT_REQUEST = RESERVED - 1
            COLD_BOOT_REQUEST = ALTERNATE_SLOT_REQUEST - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            RESERVED = 14
            ALTERNATE_SLOT_REQUEST = 1
            COLD_BOOT_REQUEST = 1
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            RESERVED = 0x0000
            ALTERNATE_SLOT_REQUEST = 0
            COLD_BOOT_REQUEST = 0
        # end class DEFAULT

        FIELDS = (
            BitField(FID.RESERVED,
                     LEN.RESERVED,
                     title='Reserved',
                     name='reserved',
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(FID.ALTERNATE_SLOT_REQUEST,
                     LEN.ALTERNATE_SLOT_REQUEST,
                     title='AlternateSlotRequest',
                     name='alternate_slot_request',
                     default_value=DEFAULT.ALTERNATE_SLOT_REQUEST,
                     checks=(CheckInt(0, pow(2, LEN.ALTERNATE_SLOT_REQUEST) - 1),)),
            BitField(FID.COLD_BOOT_REQUEST,
                     LEN.COLD_BOOT_REQUEST,
                     title='ColdBootRequest',
                     name='cold_boot_request',
                     default_value=DEFAULT.COLD_BOOT_REQUEST,
                     checks=(CheckInt(0, pow(2, LEN.COLD_BOOT_REQUEST) - 1),)),
        )
    # end class ImgToBlFlags
# end class BootImageCommunication


class BootImageCommunicationWithRootOfTrust(BootImageCommunication):
    """
    Define format of Bootloader Image Communication Structure with Root of Trust

    Source: bootloader/logi_mcuboot/ReadMe.txt
    """

    class LEN(BootImageCommunication.LEN):
        """
        Field lengths in bits
        """
        RESERVED = 8 * 2
        ROOT_OF_TRUST_COUNT = 8
        ROOT_OF_TRUST_ADDR = 8 * 4
    # end class LEN

    class FID(BootImageCommunication.FID):
        """
        Field Identifiers
        """
        ROOT_OF_TRUST_COUNT = BootImageCommunication.FID.RESERVED - 1
        ROOT_OF_TRUST_ADDR = ROOT_OF_TRUST_COUNT - 1
        BL_TO_IMG_FLAGS = ROOT_OF_TRUST_ADDR - 1
        IMG_TO_BL_FLAGS = BL_TO_IMG_FLAGS - 1
    # end class FID

    FIELDS = BootImageCommunication.FIELDS[:FID.MAGIC_NUMBER - FID.RESERVED] + (
        LittleEndianBitField(
            fid=FID.RESERVED,
            length=LEN.RESERVED,
            title='Reserved',
            name='reserved',
            default_value=HexList("00" * (LEN.RESERVED // 8)),
            checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
        LittleEndianBitField(
            fid=FID.ROOT_OF_TRUST_COUNT,
            length=LEN.ROOT_OF_TRUST_COUNT,
            title='RootOfTrustCount',
            name='root_of_trust_count',
            checks=(CheckHexList(LEN.ROOT_OF_TRUST_COUNT // 8), CheckInt(0, pow(2, LEN.ROOT_OF_TRUST_COUNT) - 1),)),
        LittleEndianBitField(
            fid=FID.ROOT_OF_TRUST_ADDR,
            length=LEN.ROOT_OF_TRUST_ADDR,
            title='RootOfTrustAddr',
            name='root_of_trust_addr',
            checks=(CheckHexList(LEN.ROOT_OF_TRUST_ADDR // 8), CheckInt(0, pow(2, LEN.ROOT_OF_TRUST_ADDR) - 1),)),
        LittleEndianBitField(
            fid=FID.BL_TO_IMG_FLAGS,
            length=LEN.BL_TO_IMG_FLAGS,
            title='BlToImgFlags',
            name='bl_to_img_flags',
            checks=(CheckHexList(LEN.BL_TO_IMG_FLAGS // 8), CheckInt(0, pow(2, LEN.BL_TO_IMG_FLAGS) - 1),)),
        LittleEndianBitField(
            fid=FID.IMG_TO_BL_FLAGS,
            length=LEN.IMG_TO_BL_FLAGS,
            title='ImgToBlFlags',
            name='img_to_bl_flags',
            checks=(CheckHexList(LEN.IMG_TO_BL_FLAGS // 8), CheckInt(0, pow(2, LEN.IMG_TO_BL_FLAGS) - 1),)),
    )
# end class BootImageCommunicationWithRootOfTrust


class RootOfTrust(BitFieldContainerMixin):
    """
    Define format of Root Of Trust Structure

    Source: bootloader/logi_mcuboot/ReadMe.txt
    """

    class LEN:
        """
        Field lengths in bits
        """
        ENCODED_FLAGS = 4 * 8
        PUBLIC_KEY_ADDRESS = 4 * 8
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        ENCODED_FLAGS = 0xFF
        PUBLIC_KEY_ADDRESS = ENCODED_FLAGS - 1
    # end class FID

    class EncodedFlags(BitFieldContainerMixin):
        """
        The root-of-trust flags
        """

        class FID:
            """
            Field identifiers
            """
            RESERVED = 0xFF
            VALIDITY = RESERVED - 1
            TYPE = VALIDITY - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            RESERVED = 30
            VALIDITY = 1
            TYPE = 1
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            RESERVED = 0
            VALIDITY = 0
            TYPE = 0
        # end class DEFAULT

        class Validity(IntEnum):
            """
            Root-of-trust validity
            """
            VALID = 0
            INVALID = 1
        # end class Validity

        class Type(IntEnum):
            """
            Root-of-trust type
            """
            DEVELOPMENT = 0
            PRODUCTION = 1
        # end class Type

        FIELDS = (
            BitField(FID.RESERVED,
                     LEN.RESERVED,
                     title='Reserved',
                     name='reserved',
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(FID.VALIDITY,
                     LEN.VALIDITY,
                     title='Validity',
                     name='validity',
                     default_value=DEFAULT.VALIDITY,
                     checks=(CheckInt(0, pow(2, LEN.VALIDITY) - 1),)),
            BitField(FID.TYPE,
                     LEN.TYPE,
                     title='Type',
                     name='type',
                     default_value=DEFAULT.TYPE,
                     checks=(CheckInt(0, pow(2, LEN.TYPE) - 1),)),
        )
    # end class EncodedFlags

    FIELDS = (
        LittleEndianBitField(
            FID.ENCODED_FLAGS,
            LEN.ENCODED_FLAGS,
            title='EncodedFlags',
            name='encoded_flags',
            checks=(CheckHexList(LEN.ENCODED_FLAGS // 8), CheckInt(0, pow(2, LEN.ENCODED_FLAGS) - 1),)),
        LittleEndianBitField(
            FID.PUBLIC_KEY_ADDRESS,
            LEN.PUBLIC_KEY_ADDRESS,
            title='PublicKeyAddress',
            name='public_key_address',
            checks=(CheckHexList(LEN.PUBLIC_KEY_ADDRESS // 8), CheckInt(0, pow(2, LEN.PUBLIC_KEY_ADDRESS) - 1),)),
    )
# end class RootOfTrust


class RootOfTrustTable(list):
    """
    Root of trust table
    """

    # noinspection PyPep8Naming
    # Keep the same naming as ``BitFieldContainerMixin``
    @staticmethod
    def fromHexList(hex_list):
        """
        Parsing from ``HexList`` instance

        :param hex_list: Raw root of trust table
        :type hex_list: ``HexList``

        :return: Class instance
        :rtype: ``list[RootOfTrust]``
        """
        rot_table = []
        rot_len = sum([field.length for field in RootOfTrust.FIELDS]) // 8
        rot_start = 0
        rot_end = rot_start + rot_len
        while rot_end <= len(hex_list):
            rot_table.append(RootOfTrust.fromHexList(hex_list[rot_start:rot_end]))
            rot_start = rot_end
            rot_end = rot_start + rot_len
        # end while
        return rot_table
    # end def fromHexList
# end class RootOfTrustTable
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
