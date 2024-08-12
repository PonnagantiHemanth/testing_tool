#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.mcu.nrf52.blenvschunks
    :brief: NVS BLE chunk definition
    :author: Christophe Roquebert
    :date: 2020/06/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import abc
from enum import IntEnum
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleNvsChunks(BitFieldContainerMixin, metaclass=abc.ABCMeta):
    """
    Define the format of the common NVS_BLE_BOND_ID sections

    """
    # @brief GAP Security Random Number Length.
    BLE_GAP_SEC_RAND_LEN = 8

    # @brief GAP Security Key Length.
    BLE_GAP_SEC_KEY_LEN = 16

    class BluetoothLowEnergyAddress(BitFieldContainerMixin):
        """
        Define the format of the Bluetooth Low Energy address section

         @brief Bluetooth Low Energy address.
        {
          uint8_t addr_id_peer : 1;       /**< Only valid for peer addresses.
                                               This bit is set by the SoftDevice to indicate whether the address has been resolved from
                                               a Resolvable Private Address (when the peer is using privacy).
                                               If set to 1, @ref addr and @ref addr_type refer to the identity address of the resolved address.

                                               This bit is ignored when a variable of type @ref ble_gap_addr_t is used as input to API functions. */
          uint8_t addr_type    : 7;       /**< See @ref BLE_GAP_ADDR_TYPES. */
          uint8_t addr[BLE_GAP_ADDR_LEN]; /**< 48-bit address, LSB format.
                                               @ref addr is not used if @ref addr_type is @ref BLE_GAP_ADDR_TYPE_ANONYMOUS. */
        } ble_gap_addr_t;
        """
        class LEN:
            """
            Field Lengths in bits
            """
            #   Address Type (1 byte)
            DEVICE_ADDRESS_TYPE = 0x07
            #   Resolvable Private Address
            DEVICE_RESOLVABLE_PRIVATE_ADDRESS_FLAG = 0x01
            #   Bluetooth address (6 bytes)
            DEVICE_BLUETOOTH_ADDRESS = 0x30
        # end class LEN

        class FID:
            """
            Field Identifiers
            """
            DEVICE_ADDRESS_TYPE = 0xFF
            DEVICE_RESOLVABLE_PRIVATE_ADDRESS_FLAG = DEVICE_ADDRESS_TYPE - 1
            DEVICE_BLUETOOTH_ADDRESS = DEVICE_RESOLVABLE_PRIVATE_ADDRESS_FLAG - 1
        # end class FID

        FIELDS = (
            BitField(
                fid=FID.DEVICE_ADDRESS_TYPE,
                length=LEN.DEVICE_ADDRESS_TYPE,
                title='DeviceAddressType',
                name='device_address_type',
                checks=(CheckInt(0, pow(2, LEN.DEVICE_ADDRESS_TYPE) - 1), )),
            BitField(
                fid=FID.DEVICE_RESOLVABLE_PRIVATE_ADDRESS_FLAG,
                length=LEN.DEVICE_RESOLVABLE_PRIVATE_ADDRESS_FLAG,
                title='DeviceResolvablePrivateAddressFlag',
                name='device_resolvable_private_address_flag',
                checks=(CheckInt(0, pow(2, LEN.DEVICE_RESOLVABLE_PRIVATE_ADDRESS_FLAG) - 1), )),
            BitField(
                fid=FID.DEVICE_BLUETOOTH_ADDRESS,
                length=LEN.DEVICE_BLUETOOTH_ADDRESS,
                title='DeviceBluetoothAddress',
                name='device_bluetooth_address',
                checks=(CheckHexList(LEN.DEVICE_BLUETOOTH_ADDRESS // 8),), ),
        )
    # end class BluetoothLowEnergyAddress

    class BleGapEvtAuthStatus(BitFieldContainerMixin):
        """
        Define the format of the BLE_GAP_EVT_AUTH_STATUS section

        @brief Event structure for @ref BLE_GAP_EVT_AUTH_STATUS.
        {
          uint8_t               auth_status;            /**< Authentication status, see @ref BLE_GAP_SEC_STATUS. */
          uint8_t               error_src : 2;          /**< On error, source that caused the failure, see @ref BLE_GAP_SEC_STATUS_SOURCES. */
          uint8_t               bonded : 1;             /**< Procedure resulted in a bond. */
          uint8_t               lesc : 1;               /**< Procedure resulted in a LE Secure Connection. */
          ble_gap_sec_levels_t  sm1_levels;             /**< Levels supported in Security Mode 1. */
          ble_gap_sec_levels_t  sm2_levels;             /**< Levels supported in Security Mode 2. */
          ble_gap_sec_kdist_t   kdist_own;              /**< Bitmap stating which keys were exchanged (distributed) by the local device. If bonding with LE Secure Connections, the enc bit will be always set. */
          ble_gap_sec_kdist_t   kdist_peer;             /**< Bitmap stating which keys were exchanged (distributed) by the remote device. If bonding with LE Secure Connections, the enc bit will never be set. */
        } ble_gap_evt_auth_status_t;

        @brief Security levels supported.
        {
          uint8_t lv1 : 1;                              /**< If 1: Level 1 is supported. */
          uint8_t lv2 : 1;                              /**< If 1: Level 2 is supported. */
          uint8_t lv3 : 1;                              /**< If 1: Level 3 is supported. */
          uint8_t lv4 : 1;                              /**< If 1: Level 4 is supported. */
        } ble_gap_sec_levels_t;

        @brief Keys that can be exchanged during a bonding procedure.
        {
          uint8_t enc     : 1;                        /**< Long Term Key and Master Identification. */
          uint8_t id      : 1;                        /**< Identity Resolving Key and Identity Address Information. */
          uint8_t sign    : 1;                        /**< Connection Signature Resolving Key. */
          uint8_t link    : 1;                        /**< Derive the Link Key from the LTK. */
        } ble_gap_sec_kdist_t;
        """

        class LEN:
            """
            Field Lengths in bits
            """
            AUTHENTICATION_STATUS = 0x08
            AUTH_STATUS_RESERVED = 0x04
            LESC = 0x01
            BONDED = 0x01
            ERROR_SOURCE = 0x02
            #   Levels supported in Security Mode 1. (8 bits)
            SECURITY_MODE1_RESERVED = 0x04
            SECURITY_MODE1_LEVEL4 = 0x01
            SECURITY_MODE1_LEVEL3 = 0x01
            SECURITY_MODE1_LEVEL2 = 0x01
            SECURITY_MODE1_LEVEL1 = 0x01
            #   Levels supported in Security Mode 2. (8 bits)
            SECURITY_MODE2_RESERVED = 0x04
            SECURITY_MODE2_LEVEL4 = 0x01
            SECURITY_MODE2_LEVEL3 = 0x01
            SECURITY_MODE2_LEVEL2 = 0x01
            SECURITY_MODE2_LEVEL1 = 0x01
            #   Bitmap stating which keys were exchanged (distributed) by the local device. (8 bits)
            LOCAL_KDIST_RESERVED = 0x04
            LOCAL_KDIST_LINK_KEY = 0x01
            LOCAL_KDIST_CSRK = 0x01
            LOCAL_KDIST_IRK = 0x01
            LOCAL_KDIST_LONG_TERM_KEY = 0x01
            #   Bitmap stating which keys were exchanged (distributed) by the remote device. (8 bits)
            REMOTE_KDIST_RESERVED = 0x04
            REMOTE_KDIST_LINK_KEY = 0x01
            REMOTE_KDIST_CSRK = 0x01
            REMOTE_KDIST_IRK = 0x01
            REMOTE_KDIST_LONG_TERM_KEY = 0x01
        # end class LEN

        class FID:
            """
            Field Identifiers
            """
            AUTHENTICATION_STATUS = 0xFF
            AUTH_STATUS_RESERVED = AUTHENTICATION_STATUS - 1
            LESC = AUTH_STATUS_RESERVED - 1
            BONDED = LESC - 1
            ERROR_SOURCE = BONDED - 1
            SECURITY_MODE1_RESERVED = ERROR_SOURCE - 1
            SECURITY_MODE1_LEVEL4 = SECURITY_MODE1_RESERVED - 1
            SECURITY_MODE1_LEVEL3 = SECURITY_MODE1_LEVEL4 - 1
            SECURITY_MODE1_LEVEL2 = SECURITY_MODE1_LEVEL3 - 1
            SECURITY_MODE1_LEVEL1 = SECURITY_MODE1_LEVEL2 - 1
            SECURITY_MODE2_RESERVED = SECURITY_MODE1_LEVEL1 - 1
            SECURITY_MODE2_LEVEL4 = SECURITY_MODE2_RESERVED - 1
            SECURITY_MODE2_LEVEL3 = SECURITY_MODE2_LEVEL4 - 1
            SECURITY_MODE2_LEVEL2 = SECURITY_MODE2_LEVEL3 - 1
            SECURITY_MODE2_LEVEL1 = SECURITY_MODE2_LEVEL2 - 1
            LOCAL_KDIST_RESERVED = SECURITY_MODE2_LEVEL1 - 1
            LOCAL_KDIST_LINK_KEY = LOCAL_KDIST_RESERVED - 1
            LOCAL_KDIST_CSRK = LOCAL_KDIST_LINK_KEY - 1
            LOCAL_KDIST_IRK = LOCAL_KDIST_CSRK - 1
            LOCAL_KDIST_LONG_TERM_KEY = LOCAL_KDIST_IRK - 1
            REMOTE_KDIST_RESERVED = LOCAL_KDIST_LONG_TERM_KEY - 1
            REMOTE_KDIST_LINK_KEY = REMOTE_KDIST_RESERVED - 1
            REMOTE_KDIST_CSRK = REMOTE_KDIST_LINK_KEY - 1
            REMOTE_KDIST_IRK = REMOTE_KDIST_CSRK - 1
            REMOTE_KDIST_LONG_TERM_KEY = REMOTE_KDIST_IRK - 1
        # end class FID

        FIELDS = (
            BitField(
                fid=FID.AUTHENTICATION_STATUS,
                length=LEN.AUTHENTICATION_STATUS,
                title='AuthenticationStatus',
                name='authentication_status',
                checks=(CheckHexList(LEN.AUTHENTICATION_STATUS // 8), CheckByte(),),),
            BitField(
                fid=FID.AUTH_STATUS_RESERVED,
                length=LEN.AUTH_STATUS_RESERVED,
                title='AuthStatusReserved',
                name='auth_status_reserved',
                checks=(CheckInt(0, pow(2, LEN.AUTH_STATUS_RESERVED) - 1), )),
            BitField(
                fid=FID.LESC,
                length=LEN.LESC,
                title='Lesc',
                name='lesc',
                checks=(CheckInt(0, pow(2, LEN.LESC) - 1), )),
            BitField(
                fid=FID.BONDED,
                length=LEN.BONDED,
                title='Bonded',
                name='bonded',
                checks=(CheckInt(0, pow(2, LEN.BONDED) - 1), )),
            BitField(
                fid=FID.ERROR_SOURCE,
                length=LEN.ERROR_SOURCE,
                title='ErrorSource',
                name='error_source',
                checks=(CheckInt(0, pow(2, LEN.ERROR_SOURCE) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE1_RESERVED,
                length=LEN.SECURITY_MODE1_RESERVED,
                title='SecurityMode1Reserved',
                name='security_mode1_reserved',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE1_RESERVED) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE1_LEVEL4,
                length=LEN.SECURITY_MODE1_LEVEL4,
                title='SecurityMode1Level4',
                name='security_mode1_level4',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE1_LEVEL4) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE1_LEVEL3,
                length=LEN.SECURITY_MODE1_LEVEL3,
                title='SecurityMode1Level3',
                name='security_mode1_level3',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE1_LEVEL3) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE1_LEVEL2,
                length=LEN.SECURITY_MODE1_LEVEL2,
                title='SecurityMode1Level2',
                name='security_mode1_level2',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE1_LEVEL2) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE1_LEVEL1,
                length=LEN.SECURITY_MODE1_LEVEL1,
                title='SecurityMode1Level1',
                name='security_mode1_level1',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE1_LEVEL1) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE2_RESERVED,
                length=LEN.SECURITY_MODE2_RESERVED,
                title='SecurityMode2Reserved',
                name='security_mode2_reserved',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE2_RESERVED) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE2_LEVEL4,
                length=LEN.SECURITY_MODE2_LEVEL4,
                title='SecurityMode2Level4',
                name='security_mode2_level4',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE2_LEVEL4) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE2_LEVEL3,
                length=LEN.SECURITY_MODE2_LEVEL3,
                title='SecurityMode2Level3',
                name='security_mode2_level3',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE2_LEVEL3) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE2_LEVEL2,
                length=LEN.SECURITY_MODE2_LEVEL2,
                title='SecurityMode2Level2',
                name='security_mode2_level2',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE2_LEVEL2) - 1), )),
            BitField(
                fid=FID.SECURITY_MODE2_LEVEL1,
                length=LEN.SECURITY_MODE2_LEVEL1,
                title='SecurityMode2Level1',
                name='security_mode2_level1',
                checks=(CheckInt(0, pow(2, LEN.SECURITY_MODE2_LEVEL1) - 1), )),
            BitField(
                fid=FID.LOCAL_KDIST_RESERVED,
                length=LEN.LOCAL_KDIST_RESERVED,
                title='LocalKdistReserved',
                name='local_kdist_reserved',
                checks=(CheckInt(0, pow(2, LEN.LOCAL_KDIST_RESERVED) - 1), )),
            BitField(
                fid=FID.LOCAL_KDIST_LINK_KEY,
                length=LEN.LOCAL_KDIST_LINK_KEY,
                title='LocalKdistLinkKey',
                name='local_kdist_link_key',
                checks=(CheckInt(0, pow(2, LEN.LOCAL_KDIST_LINK_KEY) - 1), )),
            BitField(
                fid=FID.LOCAL_KDIST_CSRK,
                length=LEN.LOCAL_KDIST_CSRK,
                title='LocalKdistCsrk',
                name='local_kdist_csrk',
                checks=(CheckInt(0, pow(2, LEN.LOCAL_KDIST_CSRK) - 1), )),
            BitField(
                fid=FID.LOCAL_KDIST_IRK,
                length=LEN.LOCAL_KDIST_IRK,
                title='LocalKdistIrk',
                name='local_kdist_irk',
                checks=(CheckInt(0, pow(2, LEN.LOCAL_KDIST_IRK) - 1), )),
            BitField(
                fid=FID.LOCAL_KDIST_LONG_TERM_KEY,
                length=LEN.LOCAL_KDIST_LONG_TERM_KEY,
                title='LocalKdistLongTermKey',
                name='local_kdist_long_term_key',
                checks=(CheckInt(0, pow(2, LEN.LOCAL_KDIST_LONG_TERM_KEY) - 1), )),
            BitField(
                fid=FID.REMOTE_KDIST_RESERVED,
                length=LEN.REMOTE_KDIST_RESERVED,
                title='RemoteKdistReserved',
                name='remote_kdist_reserved',
                checks=(CheckInt(0, pow(2, LEN.REMOTE_KDIST_RESERVED) - 1), )),
            BitField(
                fid=FID.REMOTE_KDIST_LINK_KEY,
                length=LEN.REMOTE_KDIST_LINK_KEY,
                title='RemoteKdistLinkKey',
                name='remote_kdist_link_key',
                checks=(CheckInt(0, pow(2, LEN.REMOTE_KDIST_LINK_KEY) - 1), )),
            BitField(
                fid=FID.REMOTE_KDIST_CSRK,
                length=LEN.REMOTE_KDIST_CSRK,
                title='RemoteKdistCsrk',
                name='remote_kdist_csrk',
                checks=(CheckInt(0, pow(2, LEN.REMOTE_KDIST_CSRK) - 1), )),
            BitField(
                fid=FID.REMOTE_KDIST_IRK,
                length=LEN.REMOTE_KDIST_IRK,
                title='RemoteKdistIrk',
                name='remote_kdist_irk',
                checks=(CheckInt(0, pow(2, LEN.REMOTE_KDIST_IRK) - 1), )),
            BitField(
                fid=FID.REMOTE_KDIST_LONG_TERM_KEY,
                length=LEN.REMOTE_KDIST_LONG_TERM_KEY,
                title='RemoteKdistLongTermKey',
                name='remote_kdist_long_term_key',
                checks=(CheckInt(0, pow(2, LEN.REMOTE_KDIST_LONG_TERM_KEY) - 1), )),
        )
    # end class BleGapEvtAuthStatus

    class BleGapEncInfo(BitFieldContainerMixin):
        """
        Define the format of the GAP Encryption Information section

        @brief GAP Encryption Information.
        {
          uint8_t   ltk[BLE_GAP_SEC_KEY_LEN];   /**< Long Term Key. */
          uint8_t   lesc : 1;                   /**< Key generated using LE Secure Connections. */
          uint8_t   auth : 1;                   /**< Authenticated Key. */
          uint8_t   ltk_len : 6;                /**< LTK length in octets. */
        } ble_gap_enc_info_t;
        """

        class LEN:
            """
            Field Lengths in bits
            """
            #     Encryption Information (17 bytes)
            #       Long Term Key (16 bytes)
            ENC_INFO_LONG_TERM_KEY = 0x80
            #       LTK length in octets
            ENC_INFO_LTK_LEN = 0x06
            #       Authenticated Key Presence
            ENC_INFO_AUTH_FLAG = 0x01
            #       LESC Flag (i.e. Key generated using LE Secure Connections)
            ENC_INFO_LESC_FLAG = 0x01
        # end class LEN

        class FID:
            """
            Field Identifiers
            """
            ENC_INFO_LONG_TERM_KEY = 0xFF
            ENC_INFO_LTK_LEN = ENC_INFO_LONG_TERM_KEY - 1
            ENC_INFO_AUTH_FLAG = ENC_INFO_LTK_LEN - 1
            ENC_INFO_LESC_FLAG = ENC_INFO_AUTH_FLAG - 1

        # end class FID

        FIELDS = (
            BitField(
                fid=FID.ENC_INFO_LONG_TERM_KEY,
                length=LEN.ENC_INFO_LONG_TERM_KEY,
                title='EncInfoLongTermKey',
                name='enc_info_long_term_key',
                checks=(CheckHexList(LEN.ENC_INFO_LONG_TERM_KEY // 8),),),
            BitField(
                fid=FID.ENC_INFO_LTK_LEN,
                length=LEN.ENC_INFO_LTK_LEN,
                title='EncInfoLtkLen',
                name='enc_info_ltk_len',
                checks=(CheckInt(0, pow(2, LEN.ENC_INFO_LTK_LEN) - 1), )),
            BitField(
                fid=FID.ENC_INFO_AUTH_FLAG,
                length=LEN.ENC_INFO_AUTH_FLAG,
                title='EncInfoAuthFlag',
                name='enc_info_auth_flag',
                checks=(CheckInt(0, pow(2, LEN.ENC_INFO_AUTH_FLAG) - 1), )),
            BitField(
                fid=FID.ENC_INFO_LESC_FLAG,
                length=LEN.ENC_INFO_LESC_FLAG,
                title='EncInfoLescFlag',
                name='enc_info_lesc_flag',
                checks=(CheckInt(0, pow(2, LEN.ENC_INFO_LESC_FLAG) - 1), )),

        )
    # end class BleGapEncInfo

    class GapMasterIdentification(BitFieldContainerMixin):
        """
        Define the format of the GAP Master Identification section


        @brief GAP Master Identification.
        {
          uint16_t  ediv;                       /**< Encrypted Diversifier. */
          uint8_t   rand[BLE_GAP_SEC_RAND_LEN]; /**< Random Number. */
        } ble_gap_master_id_t;
        """
        class LEN:
            """
            Field Lengths in bits
            """
            #     Master Identification (10 bytes)
            #       Encrypted Diversifier (2 bytes)
            ENC_ID_EDIV = 0x10
            #       Random Number (8 bytes)
            ENC_ID_RANDOM = 0x40
        # end class LEN

        class FID:
            """
            Field Identifiers
            """
            ENC_ID_EDIV = 0xFF
            ENC_ID_RANDOM = ENC_ID_EDIV - 1
        # end class FID

        FIELDS = (
            BitField(
                fid=FID.ENC_ID_EDIV,
                length=LEN.ENC_ID_EDIV,
                title='EncIdEdiv',
                name='enc_id_ediv',
                checks=(CheckHexList(LEN.ENC_ID_EDIV // 8),),),
            BitField(
                fid=FID.ENC_ID_RANDOM,
                length=LEN.ENC_ID_RANDOM,
                title='EncIdRandom',
                name='enc_id_random',
                checks=(CheckHexList(LEN.ENC_ID_RANDOM // 8),),),
        )
    # end class BluetoothLowEnergyAddress

    class IdentityKey(BitFieldContainerMixin):
        """
        Define the format of the Identity Key section

        @brief Identity Key.
        {
          ble_gap_irk_t         id_info;              /**< Identity Resolving Key. */
          ble_gap_addr_t        id_addr_info;         /**< Identity Address. */
        } ble_gap_id_key_t;

        @brief Identity Resolving Key.
        {
          uint8_t irk[BLE_GAP_SEC_KEY_LEN];   /**< Array containing IRK. */
        } ble_gap_irk_t;
        """
        class LEN:
            """
            Field Lengths in bits
            """
            #   Peripheral Identity Key (23 bytes)
            #     Identity Resolving Key (16 bytes)
            IDENTITY_RESOLVING_KEY = 0x80
            #     Identity Address (7 bytes)
            #       Address Type (1 byte)
            IDENTITY_ADDRESS_TYPE = 0x07
            #       Resolvable Private Address
            IDENTITY_RESOLVABLE_PRIVATE_ADDRESS_FLAG = 0x01
            #       Bluetooth address (6 bytes)
            BLUETOOTH_ADDRESS = 0x30
        # end class LEN

        class FID:
            """
            Field Identifiers
            """
            IDENTITY_RESOLVING_KEY = 0xFF
            IDENTITY_ADDRESS_TYPE = IDENTITY_RESOLVING_KEY - 1
            IDENTITY_RESOLVABLE_PRIVATE_ADDRESS_FLAG = IDENTITY_ADDRESS_TYPE - 1
            BLUETOOTH_ADDRESS = IDENTITY_RESOLVABLE_PRIVATE_ADDRESS_FLAG - 1
        # end class FID

        FIELDS = (
            BitField(
                fid=FID.IDENTITY_RESOLVING_KEY,
                length=LEN.IDENTITY_RESOLVING_KEY,
                title='IdentityResolvinKey',
                name='identity_resolving_key',
                checks=(CheckHexList(LEN.IDENTITY_RESOLVING_KEY // 8),),),
            BitField(
                fid=FID.IDENTITY_ADDRESS_TYPE,
                length=LEN.IDENTITY_ADDRESS_TYPE,
                title='IdentityAddressType',
                name='identity_address_type',
                checks=(CheckInt(0, pow(2, LEN.IDENTITY_ADDRESS_TYPE) - 1), )),
            BitField(
                fid=FID.IDENTITY_RESOLVABLE_PRIVATE_ADDRESS_FLAG,
                length=LEN.IDENTITY_RESOLVABLE_PRIVATE_ADDRESS_FLAG,
                title='IdentityResolvablePrivateAddressFlag',
                name='identity_resolvable_private_address_flag',
                checks=(CheckInt(0, pow(2, LEN.IDENTITY_RESOLVABLE_PRIVATE_ADDRESS_FLAG) - 1), )),
            BitField(
                fid=FID.BLUETOOTH_ADDRESS,
                length=LEN.BLUETOOTH_ADDRESS,
                title='BluetoothAddress',
                name='bluetooth_address',
                checks=(CheckHexList(LEN.BLUETOOTH_ADDRESS // 8),),),
        )
    # end class IdentityKey

    class OsDetectedType(IntEnum):
        """
        Define the constants applicable to the os detection type field
        """
        UNKNOWN = 0  # OS not detected yet
        UNDETERMINED = 1  # OS has not been determined (other than Apple)
        OSX = 2  # Apple OS -> might be OSx
        IOS = 3  # Apple OS -> might be IOS
        LOGITECH_BLE_PRO = 4  # Logitech BLE Pro (Bolt) receiver
        LOGITECH_UNDETERMINED = 5  # Undetermined Logitech host
        CHROME = 6   # Chrome OS
        ANDROID = 7   # Android OS
        LINUX = 8   # LINUX OS
        WEBOS = 9   # Web OS
        TIZENTV = 10  # TIZEN TV
    # end class OsDetectedType
# end class BleNvsChunks


class DeviceBleBondIdV1(BleNvsChunks):  # pylint:disable=W0223
    """
    Define the format of the NVS_BLE_BOND_ID chunk version 1

    master_bond_t format:
    {
        int32_t                        is_master_paired;                    /**< Master's paired flag(0 mean no pairing) (NOTE: Size is 32 bits just to make struct size dividable by 4). */
        ble_gap_evt_auth_status_t      auth_status;                         /**< Master authentication data. */
        bond_key_t                     bond_key;                            /**< Master encryption keys. */
        ble_gap_addr_t                 master_addr;                         /**< Master's address. */
        uint32_t                       os_detected_type;                    /**< Host OS detected + Make sure address is aligned. */
        ble_gap_addr_t                 device_addr;                         /**< Device's address. */
    } master_bond_t;

    @brief Encryption Key.
    {
      ble_gap_enc_info_t    enc_info;             /**< Encryption Information. */
      ble_gap_master_id_t   master_id;            /**< Master Identification. */
    } ble_gap_enc_key_t;

    @brief GAP Signing Information.
    {
      uint8_t   csrk[BLE_GAP_SEC_KEY_LEN];        /**< Connection Signature Resolving Key. */
    } ble_gap_sign_info_t;

    """

    class LEN:
        """
        Field Lengths in bits
        """
        # master_bond_t structure (158 bytes)
        # ------------------------
        # Master Paired Flag (4 bytes)
        # ------------------------
        IS_MASTER_PAIRED = 0x20
        # ------------------------
        # Master Authentication (6 bytes)
        # ------------------------
        BLE_GAP_EVT_AUTH_STATUS = 0x30
        # ------------------------
        # Master encryption keys (132 bytes)
        # ------------------------
        #   Peripheral Encryption Key (28 bytes)
        #     Encryption Information (17 bytes)
        LOCAL_BLE_GAP_ENC_INFO = 0x88
        #     Word alignment due to the following uint16_t (1 byte)
        LOCAL_ENC_PADDING = 0x08
        #     Master Identification (10 bytes)
        LOCAL_GAP_MASTER_IDENTIFICATION = 0x50
        #   Peripheral Identity Key (23 bytes)
        LOCAL_IDENTITY_KEY = 0xB8
        #   Peripheral Signing Key (16 bytes)
        LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY = 0x80
        #   Central Encryption Key (28 bytes)
        #     Encryption Information (17 bytes)
        REMOTE_BLE_GAP_ENC_INFO = 0x88
        #     Word alignment due to the following uint16_t (2 bytes)
        REMOTE_ENC_PADDING = 0x10
        #     Master Identification (10 bytes)
        REMOTE_GAP_MASTER_IDENTIFICATION = 0x50
        #   Central Identity Key (23 bytes)
        REMOTE_IDENTITY_KEY = 0xB8
        #   Central Signing Key (16 bytes)
        REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY = 0x80
        #   Word alignment (1 byte)
        MASTER_KEYS_PADDING = 0x08
        # ------------------------
        # Master Address (10 bytes)
        # ------------------------
        #   Address Type (1 byte)
        MASTER_ADDRESS_TYPE = 0x07
        #   Resolvable Private Address
        MASTER_RESOLVABLE_PRIVATE_ADDRESS_FLAG = 0x01
        #   Bluetooth address (6 bytes)
        MASTER_BLUETOOTH_ADDRESS = 0x30
        #   Word alignment due to the following uint32_t (3 bytes)
        MASTER_ADDRESS_PADDING = 0x18
        # ------------------------
        # OS Detected Type (4 bytes)
        # ------------------------
        OS_DETECTED_TYPE = 0x08
        OS_DETECTED_TYPE_RESERVED = 0x18
        # ------------------------
        # Device Address (7 bytes)
        # ------------------------
        BLUETOOTH_LOW_ENERGY_ADDRESS = 0x38
        #   Word alignment of the whole structure (1 byte)
        END_PADDING = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        IS_MASTER_PAIRED = 0xFF
        BLE_GAP_EVT_AUTH_STATUS = IS_MASTER_PAIRED - 1
        LOCAL_BLE_GAP_ENC_INFO = BLE_GAP_EVT_AUTH_STATUS - 1
        LOCAL_ENC_PADDING = LOCAL_BLE_GAP_ENC_INFO - 1
        LOCAL_GAP_MASTER_IDENTIFICATION = LOCAL_ENC_PADDING - 1
        LOCAL_IDENTITY_KEY = LOCAL_GAP_MASTER_IDENTIFICATION - 1
        LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY = LOCAL_IDENTITY_KEY - 1
        REMOTE_BLE_GAP_ENC_INFO = LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY - 1
        REMOTE_ENC_PADDING = REMOTE_BLE_GAP_ENC_INFO - 1
        REMOTE_GAP_MASTER_IDENTIFICATION = REMOTE_ENC_PADDING - 1
        REMOTE_IDENTITY_KEY = REMOTE_GAP_MASTER_IDENTIFICATION - 1
        REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY = REMOTE_IDENTITY_KEY - 1
        MASTER_KEYS_PADDING = REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY - 1
        MASTER_ADDRESS_TYPE = MASTER_KEYS_PADDING - 1
        MASTER_RESOLVABLE_PRIVATE_ADDRESS_FLAG = MASTER_ADDRESS_TYPE - 1
        MASTER_BLUETOOTH_ADDRESS = MASTER_RESOLVABLE_PRIVATE_ADDRESS_FLAG - 1
        MASTER_ADDRESS_PADDING = MASTER_BLUETOOTH_ADDRESS - 1
        OS_DETECTED_TYPE = MASTER_ADDRESS_PADDING - 1
        OS_DETECTED_TYPE_RESERVED = OS_DETECTED_TYPE - 1
        BLUETOOTH_LOW_ENERGY_ADDRESS = OS_DETECTED_TYPE_RESERVED - 1
        END_PADDING = BLUETOOTH_LOW_ENERGY_ADDRESS - 1
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.IS_MASTER_PAIRED,
            length=LEN.IS_MASTER_PAIRED,
            title='MasterPairedFlag',
            name='is_master_paired',
            checks=(CheckHexList(LEN.IS_MASTER_PAIRED // 8),),),
        BitField(
            fid=FID.BLE_GAP_EVT_AUTH_STATUS,
            length=LEN.BLE_GAP_EVT_AUTH_STATUS,
            title='BleGapEvtAuthStatus',
            name='ble_gap_evt_auth_status',),
        BitField(
            fid=FID.LOCAL_BLE_GAP_ENC_INFO,
            length=LEN.LOCAL_BLE_GAP_ENC_INFO,
            title='LocalBleGapEncInfo',
            name='local_ble_gap_enc_info',),
        BitField(
            fid=FID.LOCAL_ENC_PADDING,
            length=LEN.LOCAL_ENC_PADDING,
            title='LocalEncPadding',
            name='local_enc_padding',
            checks=(CheckHexList(LEN.LOCAL_ENC_PADDING // 8), CheckByte(),),),
        BitField(
            fid=FID.LOCAL_GAP_MASTER_IDENTIFICATION,
            length=LEN.LOCAL_GAP_MASTER_IDENTIFICATION,
            title='GapMasterIdentification',
            name='local_gap_master_identification',),
        BitField(
            fid=FID.LOCAL_IDENTITY_KEY,
            length=LEN.LOCAL_IDENTITY_KEY,
            title='LocalIdentityKey',
            name='local_identity_key',),
        BitField(
            fid=FID.LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY,
            length=LEN.LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY,
            title='LocalConnectionSignatureResolvinKey',
            name='local_connection_signature_resolving_key',
            checks=(CheckHexList(LEN.LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY // 8),),),
        BitField(
            fid=FID.REMOTE_BLE_GAP_ENC_INFO,
            length=LEN.REMOTE_BLE_GAP_ENC_INFO,
            title='RemoteBleGapEncInfo',
            name='remote_ble_gap_enc_info',),
        BitField(
            fid=FID.REMOTE_ENC_PADDING,
            length=LEN.REMOTE_ENC_PADDING,
            title='RemoteEncPadding',
            name='remote_enc_padding',
            checks=(CheckHexList(LEN.REMOTE_ENC_PADDING // 8), ),),
        BitField(
            fid=FID.REMOTE_GAP_MASTER_IDENTIFICATION,
            length=LEN.REMOTE_GAP_MASTER_IDENTIFICATION,
            title='RemoteGapMasterIdentification',
            name='remote_gap_master_identification',),
        BitField(
            fid=FID.REMOTE_IDENTITY_KEY,
            length=LEN.REMOTE_IDENTITY_KEY,
            title='RemoteIdentityKey',
            name='remote_identity_key',),
        BitField(
            fid=FID.REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY,
            length=LEN.REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY,
            title='RemoteConnectionSignatureResolvinKey',
            name='remote_connection_signature_resolving_key',
            checks=(CheckHexList(LEN.REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY // 8),), ),
        BitField(
            fid=FID.MASTER_KEYS_PADDING,
            length=LEN.MASTER_KEYS_PADDING,
            title='MasterKeysPadding',
            name='master_keys_padding',
            checks=(CheckHexList(LEN.MASTER_KEYS_PADDING // 8), CheckByte(),), ),
        BitField(
            fid=FID.MASTER_ADDRESS_TYPE,
            length=LEN.MASTER_ADDRESS_TYPE,
            title='MasterAddressType',
            name='master_address_type',
            checks=(CheckInt(0, pow(2, LEN.MASTER_ADDRESS_TYPE) - 1), )),
        BitField(
            fid=FID.MASTER_RESOLVABLE_PRIVATE_ADDRESS_FLAG,
            length=LEN.MASTER_RESOLVABLE_PRIVATE_ADDRESS_FLAG,
            title='MasterResolvablePrivateAddressFlag',
            name='master_resolvable_private_address_flag',
            checks=(CheckInt(0, pow(2, LEN.MASTER_RESOLVABLE_PRIVATE_ADDRESS_FLAG) - 1), )),
        BitField(
            fid=FID.MASTER_BLUETOOTH_ADDRESS,
            length=LEN.MASTER_BLUETOOTH_ADDRESS,
            title='MasterBluetoothAddress',
            name='master_bluetooth_address',
            checks=(CheckHexList(LEN.MASTER_BLUETOOTH_ADDRESS // 8),), ),
        BitField(
            fid=FID.MASTER_ADDRESS_PADDING,
            length=LEN.MASTER_ADDRESS_PADDING,
            title='MasterAddressPadding',
            name='master_address_padding',
            checks=(CheckHexList(LEN.MASTER_ADDRESS_PADDING // 8),), ),
        BitField(
            fid=FID.OS_DETECTED_TYPE,
            length=LEN.OS_DETECTED_TYPE,
            title='OsDetectedType',
            name='os_detected_type',
            checks=(CheckHexList(LEN.OS_DETECTED_TYPE // 8),), ),
        BitField(
            fid=FID.OS_DETECTED_TYPE_RESERVED,
            length=LEN.OS_DETECTED_TYPE_RESERVED,
            title='OsDetectedTypeReserved',
            name='os_detected_type_reserved',
            checks=(CheckHexList(LEN.OS_DETECTED_TYPE_RESERVED // 8),), ),
        BitField(
            fid=FID.BLUETOOTH_LOW_ENERGY_ADDRESS,
            length=LEN.BLUETOOTH_LOW_ENERGY_ADDRESS,
            title='BluetoothLowEnergyAddress',
            name='bluetooth_low_energy_address',),
        BitField(
            fid=FID.END_PADDING,
            length=LEN.END_PADDING,
            title='EndPadding',
            name='end_padding',
            checks=(CheckHexList(LEN.END_PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, bluetooth_low_energy_address, ble_gap_evt_auth_status, local_ble_gap_enc_info,
                 local_gap_master_identification, local_identity_key, remote_ble_gap_enc_info,
                 remote_gap_master_identification, remote_identity_key, os_detected_type, ref=None, **kwargs):
        """
        :param bluetooth_low_energy_address: Bluetooth Low Energy Address
        :type bluetooth_low_energy_address: ``HexList`` or ``BluetoothLowEnergyAddress``
        :param ble_gap_evt_auth_status: Authentication status, see @ref BLE_GAP_SEC_STATUS.
        :type ble_gap_evt_auth_status: ``HexList`` or ``BleGapEvtAuthStatus``
        :param local_ble_gap_enc_info: Peripheral Ble Gap Encryption Info
        :type local_ble_gap_enc_info: ``HexList`` or ``BleGapEncInfo``
        :param local_gap_master_identification: Peripheral Gap Master Identification
        :type local_gap_master_identification: ``HexList`` or ``GapMasterIdentification``
        :param local_identity_key: Peripheral Identity Resolving Key and Address
        :type local_identity_key: ``HexList`` or ``IdentityKey``
        :param remote_ble_gap_enc_info: Central Ble Gap Encryption Info
        :type remote_ble_gap_enc_info: ``HexList`` or ``BleGapEncInfo``
        :param remote_gap_master_identification: Central Gap Master Identification
        :type remote_gap_master_identification: ``HexList`` or ``GapMasterIdentification``
        :param remote_identity_key: Central Identity Resolving Key and Address
        :type remote_identity_key: ``HexList`` or ``IdentityKey``
        :param os_detected_type: Constant related to the OS detection mechanism
        :type os_detected_type: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.bluetooth_low_energy_address = bluetooth_low_energy_address
        self.ble_gap_evt_auth_status = ble_gap_evt_auth_status
        self.local_ble_gap_enc_info = local_ble_gap_enc_info
        self.local_gap_master_identification = local_gap_master_identification
        self.local_identity_key = local_identity_key
        self.remote_ble_gap_enc_info = remote_ble_gap_enc_info
        self.remote_gap_master_identification = remote_gap_master_identification
        self.remote_identity_key = remote_identity_key
        self.os_detected_type = os_detected_type
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return:  parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.ble_gap_evt_auth_status = BleNvsChunks.BleGapEvtAuthStatus.fromHexList(
                inner_field_container_mixin.ble_gap_evt_auth_status)
        inner_field_container_mixin.local_ble_gap_enc_info = BleNvsChunks.BleGapEncInfo.fromHexList(
                inner_field_container_mixin.local_ble_gap_enc_info)
        inner_field_container_mixin.local_gap_master_identification = BleNvsChunks.GapMasterIdentification.fromHexList(
                inner_field_container_mixin.local_gap_master_identification)
        inner_field_container_mixin.local_identity_key = BleNvsChunks.IdentityKey.fromHexList(
                inner_field_container_mixin.local_identity_key)
        inner_field_container_mixin.remote_ble_gap_enc_info = BleNvsChunks.BleGapEncInfo.fromHexList(
                inner_field_container_mixin.remote_ble_gap_enc_info)
        inner_field_container_mixin.remote_gap_master_identification = BleNvsChunks.GapMasterIdentification.fromHexList(
                inner_field_container_mixin.remote_gap_master_identification)
        inner_field_container_mixin.remote_identity_key = BleNvsChunks.IdentityKey.fromHexList(
                inner_field_container_mixin.remote_identity_key)
        inner_field_container_mixin.bluetooth_low_energy_address = BleNvsChunks.BluetoothLowEnergyAddress.fromHexList(
                inner_field_container_mixin.bluetooth_low_energy_address)
        return inner_field_container_mixin
    # end def fromHexList
# end class DeviceBleBondIdV1


class DeviceBleBondIdV2(DeviceBleBondIdV1):
    """
    Define the format of the NVS_BLE_BOND_ID chunk version 2 including the 4 bytes long BLE Pro attributes parameter

    master_bond_t format:
    {
        int32_t                        is_master_paired;                    /**< Master's paired flag(0 mean no pairing) (NOTE: Size is 32 bits just to make struct size dividable by 4). */
        ble_gap_evt_auth_status_t      auth_status;                         /**< Master authentication data. */
        bond_key_t                     bond_key;                            /**< Master encryption keys. */
        ble_gap_addr_t                 master_addr;                         /**< Master's address. */
        uint32_t                       os_detected_type;                    /**< Host OS detected + Make sure address is aligned. */
        ble_gap_addr_t                 device_addr;                         /**< Device's address. */
        ble_pro_attribute_t            ble_pro_attributes;                  /**< BLE Pro Attributes. */
    } master_bond_t;
    """

    class BlProAttributes(BitFieldContainerMixin):
        """
        Define the format of the ble_pro_attribute_t section
        """

        class LEN:
            """
            Field Lengths in bits
            """
            BLE_PRO_ATTR_LSB_BYTE_RESERVED = 0x07
            BLE_PRO_ATTR_SUPPRESS_FIRST_REPORT_LATENCY_BIT = 0x01
            BLE_PRO_ATTR_BYTE_1_TO_3 = 0x18

        # end class LEN

        class FID(DeviceBleBondIdV1.FID):
            """
            Field Identifiers
            """
            BLE_PRO_ATTR_LSB_BYTE_RESERVED = 0xFF
            BLE_PRO_ATTR_SUPPRESS_FIRST_REPORT_LATENCY_BIT = BLE_PRO_ATTR_LSB_BYTE_RESERVED - 1
            BLE_PRO_ATTR_BYTE_1_TO_3 = BLE_PRO_ATTR_SUPPRESS_FIRST_REPORT_LATENCY_BIT - 1

        # end class FID

        FIELDS = (
            BitField(
                fid=FID.BLE_PRO_ATTR_LSB_BYTE_RESERVED,
                length=LEN.BLE_PRO_ATTR_LSB_BYTE_RESERVED,
                title='BLEProAttrLsbByteReserved',
                name='ble_pro_attr_lsb_byte_reserved',
                checks=(CheckInt(0, pow(2, LEN.BLE_PRO_ATTR_LSB_BYTE_RESERVED) - 1), )),
            BitField(
                fid=FID.BLE_PRO_ATTR_SUPPRESS_FIRST_REPORT_LATENCY_BIT,
                length=LEN.BLE_PRO_ATTR_SUPPRESS_FIRST_REPORT_LATENCY_BIT,
                title='BLEProAttrSuppressFirstReportLatencyBit',
                name='ble_pro_attr_suppress_first_report_latency_bit',
                checks=(CheckInt(0, pow(2, LEN.BLE_PRO_ATTR_SUPPRESS_FIRST_REPORT_LATENCY_BIT) - 1), )),
            BitField(
                fid=FID.BLE_PRO_ATTR_BYTE_1_TO_3,
                length=LEN.BLE_PRO_ATTR_BYTE_1_TO_3,
                title='BLEProAttrByte1To3',
                name='ble_pro_attr_byte_1_to_3',
                checks=(CheckHexList(LEN.BLE_PRO_ATTR_BYTE_1_TO_3 // 8), )),
        )
    # end class BlProAttributes

    class LEN(DeviceBleBondIdV1.LEN):
        """
        Field Lengths in bits
        """
        #   BLE Pro attributes (4 bytes)
        BLE_PRO_ATTRIBUTES = 0x20
    # end class LEN

    class FID(DeviceBleBondIdV1.FID):
        """
        Field Identifiers
        """
        BLE_PRO_ATTRIBUTES = DeviceBleBondIdV1.FID.END_PADDING
        END_PADDING = BLE_PRO_ATTRIBUTES - 1
    # end class FID

    FIELDS = DeviceBleBondIdV1.FIELDS[:-1] + (
        BitField(
            fid=FID.BLE_PRO_ATTRIBUTES,
            length=LEN.BLE_PRO_ATTRIBUTES,
            title='BLEProAttributes',
            name='ble_pro_attributes',
            checks=(CheckHexList(LEN.BLE_PRO_ATTRIBUTES // 8),), ),
        BitField(
            fid=FID.END_PADDING,
            length=LEN.END_PADDING,
            title='EndPadding',
            name='end_padding',
            checks=(CheckHexList(LEN.END_PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, bluetooth_low_energy_address, ble_gap_evt_auth_status, local_ble_gap_enc_info,
                 local_gap_master_identification, local_identity_key, remote_ble_gap_enc_info,
                 remote_gap_master_identification, remote_identity_key, os_detected_type,
                 ble_pro_attributes, ref=None, **kwargs):
        """
        :param bluetooth_low_energy_address: Bluetooth Low Energy Address
        :type bluetooth_low_energy_address: ``HexList`` or ``BluetoothLowEnergyAddress``
        :param ble_gap_evt_auth_status: Authentication status, see @ref BLE_GAP_SEC_STATUS.
        :type ble_gap_evt_auth_status: ``HexList`` or ``BleGapEvtAuthStatus``
        :param local_ble_gap_enc_info: Peripheral Ble Gap Encryption Info
        :type local_ble_gap_enc_info: ``HexList`` or ``BleGapEncInfo``
        :param local_gap_master_identification: Peripheral Gap Master Identification
        :type local_gap_master_identification: ``HexList`` or ``GapMasterIdentification``
        :param local_identity_key: Peripheral Identity Resolving Key and Address
        :type local_identity_key: ``HexList`` or ``IdentityKey``
        :param remote_ble_gap_enc_info: Central Ble Gap Encryption Info
        :type remote_ble_gap_enc_info: ``HexList`` or ``BleGapEncInfo``
        :param remote_gap_master_identification: Central Gap Master Identification
        :type remote_gap_master_identification: ``HexList`` or ``GapMasterIdentification``
        :param remote_identity_key: Central Identity Resolving Key and Address
        :type remote_identity_key: ``HexList`` or ``IdentityKey``
        :param os_detected_type: Constant related to the OS detection mechanism
        :type os_detected_type: ``int``
        :param ble_pro_attributes: BLE Pro attributes
        :type ble_pro_attributes: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(bluetooth_low_energy_address, ble_gap_evt_auth_status, local_ble_gap_enc_info,
                         local_gap_master_identification, local_identity_key, remote_ble_gap_enc_info,
                         remote_gap_master_identification, remote_identity_key, os_detected_type, ref=ref, **kwargs)

        # Parameters initialization
        self.ble_pro_attributes = ble_pro_attributes
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return:  parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.ble_pro_attributes = DeviceBleBondIdV2.BlProAttributes.fromHexList(
                inner_field_container_mixin.ble_pro_attributes)
        return inner_field_container_mixin
    # end def fromHexList
# end class DeviceBleBondIdV2


class DeviceBleBondId(BitFieldContainerMixin):
    """
    Define the format of the Device Ble BondId chunk
    """

    class LEN:
        """
        Field Lengths in bits
        """
        # version 1 is 168 bytes long
        DEVICE_BLE_BOND_ID_DATA_V1 = 0x540
        # version 2 is 172 bytes long
        DEVICE_BLE_BOND_ID_DATA_V2 = 0x560
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        DEVICE_BLE_BOND_ID_DATA = 0xFF
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.DEVICE_BLE_BOND_ID_DATA,
            length=LEN.DEVICE_BLE_BOND_ID_DATA_V2,
            title='Data',
            name='data',
            checks=(CheckHexList(max_length=(LEN.DEVICE_BLE_BOND_ID_DATA_V2 // 8),
                                 min_length=(LEN.DEVICE_BLE_BOND_ID_DATA_V1 // 8), ),)),
    )

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return:  parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        if len(inner_field_container_mixin.data) == (cls.LEN.DEVICE_BLE_BOND_ID_DATA_V1 // 8):
            return DeviceBleBondIdV1.fromHexList(inner_field_container_mixin.data)
        elif len(inner_field_container_mixin.data) == (cls.LEN.DEVICE_BLE_BOND_ID_DATA_V2 // 8):
            return DeviceBleBondIdV2.fromHexList(inner_field_container_mixin.data)
        else:
            raise ValueError("Unknown Device Ble BondId chunk structure")
        # end if
    # end def fromHexList
# end class DeviceBleBondId


class ReceiverBleBondId(BleNvsChunks):
    """
    Define the format of the receiver NVS_BLE_BOND_ID chunk

    peer_bond_t format:
    {
        ble_gap_addr_t                 addr;
        ble_gap_evt_auth_status_t      auth_status;                         /**< Authentication status. */
        ble_gap_enc_key_t              keys_periph_enc_key;                 /**< Encryption Key, or NULL. */
        ble_gap_id_key_t               keys_periph_id_key;                  /**< Identity Key, or NULL. */
        ble_gap_enc_key_t              keys_central_enc_key;                /**< Encryption Key, or NULL. */
        ble_gap_id_key_t               keys_central_id_key;                 /**< Identity Key, or NULL. */
        uint8_t                        entropy;
        ble_pro_authen_control_t       blepro_auth_control;
    } peer_bond_t;

    @brief Encryption Key.
    {
      ble_gap_enc_info_t    enc_info;             /**< Encryption Information. */
      ble_gap_master_id_t   master_id;            /**< Master Identification. */
    } ble_gap_enc_key_t;

    """
    class LEN:
        """
        Field Lengths in bits
        """
        # peer_bond_t structure (120 bytes)
        # ------------------------
        # Device Address (7 bytes)
        # ------------------------
        BLUETOOTH_LOW_ENERGY_ADDRESS = 0x38
        #   Word alignment ?? (1 byte)
        UNKNOWN = 0x08
        # ------------------------
        # Master Authentication (6 bytes)
        # ------------------------
        BLE_GAP_EVT_AUTH_STATUS = 0x30
        #   Peripheral Encryption Key (28 bytes)
        #     Encryption Information (17 bytes)
        LOCAL_BLE_GAP_ENC_INFO = 0x88
        #     Word alignment due to the following uint16_t (1 byte)
        LOCAL_ENC_PADDING = 0x08
        #     Master Identification (10 bytes)
        LOCAL_GAP_MASTER_IDENTIFICATION = 0x50
        #   Peripheral Identity Key (23 bytes)
        LOCAL_IDENTITY_KEY = 0xB8
        #     Word alignment (1 byte)
        LOCAL_IDENTITY_PADDING = 0x08
        #   Central Encryption Key (28 bytes)
        #     Encryption Information (17 bytes)
        REMOTE_BLE_GAP_ENC_INFO = 0x88
        #     Word alignment due to the following uint16_t (1 byte)
        REMOTE_ENC_PADDING = 0x08
        #     Master Identification (10 bytes)
        REMOTE_GAP_MASTER_IDENTIFICATION = 0x50
        #   Central Identity Key (23 bytes)
        REMOTE_IDENTITY_KEY = 0xB8
        #   Word alignment of the whole structure (3 bytes)
        END_PADDING = 0x08
        #   Entropy (1 byte)
        ENTROPY = 0x08
        #   Ble Pro auth control (1 byte)
        BLE_PRO_AUTH_CONTROL = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        BLUETOOTH_LOW_ENERGY_ADDRESS = 0xFF
        UNKNOWN = BLUETOOTH_LOW_ENERGY_ADDRESS - 1
        BLE_GAP_EVT_AUTH_STATUS = UNKNOWN - 1
        LOCAL_BLE_GAP_ENC_INFO = BLE_GAP_EVT_AUTH_STATUS - 1
        LOCAL_ENC_PADDING = LOCAL_BLE_GAP_ENC_INFO - 1
        LOCAL_GAP_MASTER_IDENTIFICATION = LOCAL_ENC_PADDING - 1
        LOCAL_IDENTITY_KEY = LOCAL_GAP_MASTER_IDENTIFICATION - 1
        LOCAL_IDENTITY_PADDING = LOCAL_IDENTITY_KEY - 1
        REMOTE_BLE_GAP_ENC_INFO = LOCAL_IDENTITY_PADDING - 1
        REMOTE_ENC_PADDING = REMOTE_BLE_GAP_ENC_INFO - 1
        REMOTE_GAP_MASTER_IDENTIFICATION = REMOTE_ENC_PADDING - 1
        REMOTE_IDENTITY_KEY = REMOTE_GAP_MASTER_IDENTIFICATION - 1
        END_PADDING = REMOTE_IDENTITY_KEY - 1
        ENTROPY = END_PADDING - 1
        BLE_PRO_AUTH_CONTROL = ENTROPY - 1
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.BLUETOOTH_LOW_ENERGY_ADDRESS,
            length=LEN.BLUETOOTH_LOW_ENERGY_ADDRESS,
            title='BluetoothLowEnergyAddress',
            name='bluetooth_low_energy_address',),
        BitField(
            fid=FID.UNKNOWN,
            length=LEN.UNKNOWN,
            title='Unknown',
            name='unknown',
            checks=(CheckHexList(LEN.UNKNOWN // 8), CheckByte(),),),
        BitField(
            fid=FID.BLE_GAP_EVT_AUTH_STATUS,
            length=LEN.BLE_GAP_EVT_AUTH_STATUS,
            title='BleGapEvtAuthStatus',
            name='ble_gap_evt_auth_status',),
        BitField(
            fid=FID.LOCAL_BLE_GAP_ENC_INFO,
            length=LEN.LOCAL_BLE_GAP_ENC_INFO,
            title='LocalBleGapEncInfo',
            name='local_ble_gap_enc_info',),
        BitField(
            fid=FID.LOCAL_ENC_PADDING,
            length=LEN.LOCAL_ENC_PADDING,
            title='LocalEncPadding',
            name='local_enc_padding',
            checks=(CheckHexList(LEN.LOCAL_ENC_PADDING // 8), CheckByte(),),),
        BitField(
            fid=FID.LOCAL_GAP_MASTER_IDENTIFICATION,
            length=LEN.LOCAL_GAP_MASTER_IDENTIFICATION,
            title='LocalGapMasterIdentification',
            name='local_gap_master_identification',),
        BitField(
            fid=FID.LOCAL_IDENTITY_KEY,
            length=LEN.LOCAL_IDENTITY_KEY,
            title='LocalIdentityKey',
            name='local_identity_key',),
        BitField(
            fid=FID.LOCAL_IDENTITY_PADDING,
            length=LEN.LOCAL_IDENTITY_PADDING,
            title='LocalIdentityPadding',
            name='local_identity_padding',
            checks=(CheckHexList(LEN.LOCAL_IDENTITY_PADDING // 8), CheckByte(),), ),
        BitField(
            fid=FID.REMOTE_BLE_GAP_ENC_INFO,
            length=LEN.REMOTE_BLE_GAP_ENC_INFO,
            title='RemoteBleGapEncInfo',
            name='remote_ble_gap_enc_info',),
        BitField(
            fid=FID.REMOTE_ENC_PADDING,
            length=LEN.REMOTE_ENC_PADDING,
            title='RemoteEncPadding',
            name='remote_enc_padding',
            checks=(CheckHexList(LEN.REMOTE_ENC_PADDING // 8), CheckByte(),),),
        BitField(
            fid=FID.REMOTE_GAP_MASTER_IDENTIFICATION,
            length=LEN.REMOTE_GAP_MASTER_IDENTIFICATION,
            title='RemoteGapMasterIdentification',
            name='remote_gap_master_identification',),
        BitField(
            fid=FID.REMOTE_IDENTITY_KEY,
            length=LEN.REMOTE_IDENTITY_KEY,
            title='RemoteIdentityKey',
            name='remote_identity_key',),
        BitField(
            fid=FID.END_PADDING,
            length=LEN.END_PADDING,
            title='EndPadding',
            name='end_padding',
            checks=(CheckHexList(LEN.END_PADDING // 8), CheckByte(),), ),
        BitField(
            fid=FID.ENTROPY,
            length=LEN.ENTROPY,
            title='Entropy',
            name='entropy',
            checks=(CheckHexList(LEN.ENTROPY // 8), CheckByte(),), ),
        BitField(
            fid=FID.BLE_PRO_AUTH_CONTROL,
            length=LEN.BLE_PRO_AUTH_CONTROL,
            title='BleProAuthControl',
            name='ble_pro_auth_control',
            checks=(CheckHexList(LEN.BLE_PRO_AUTH_CONTROL // 8), CheckByte(),), ),
    )

    def __init__(self, bluetooth_low_energy_address, ble_gap_evt_auth_status, local_ble_gap_enc_info,
                 local_gap_master_identification, local_identity_key, remote_ble_gap_enc_info,
                 remote_gap_master_identification, remote_identity_key, entropy, ble_pro_auth_control, ref=None,
                 **kwargs):
        """
        :param bluetooth_low_energy_address: Bluetooth Low Energy Address
        :type bluetooth_low_energy_address: ``HexList`` or ``BluetoothLowEnergyAddress``
        :param ble_gap_evt_auth_status: Authentication status, see @ref BLE_GAP_SEC_STATUS.
        :type ble_gap_evt_auth_status: ``HexList`` or ``BleGapEvtAuthStatus``
        :param local_ble_gap_enc_info: Peripheral Ble Gap Encryption Info
        :type local_ble_gap_enc_info: ``HexList`` or ``BleGapEncInfo``
        :param local_gap_master_identification: Peripheral Gap Master Identification
        :type local_gap_master_identification: ``HexList`` or ``GapMasterIdentification``
        :param local_identity_key: Peripheral Identity Resolving Key and Address
        :type local_identity_key: ``HexList`` or ``IdentityKey``
        :param remote_ble_gap_enc_info: Central Ble Gap Encryption Info
        :type remote_ble_gap_enc_info: ``HexList`` or ``BleGapEncInfo``
        :param remote_gap_master_identification: Central Gap Master Identification
        :type remote_gap_master_identification: ``HexList`` or ``GapMasterIdentification``
        :param remote_identity_key: Central Identity Resolving Key and Address
        :type remote_identity_key: ``HexList`` or ``IdentityKey``
        :param entropy: Pass Key Entropy
        :type entropy: ``int`` or ``HexList``
        :param ble_pro_auth_control: Authentication method bitmap
        :type ble_pro_auth_control: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.bluetooth_low_energy_address = bluetooth_low_energy_address
        self.ble_gap_evt_auth_status = ble_gap_evt_auth_status
        self.local_ble_gap_enc_info = local_ble_gap_enc_info
        self.local_gap_master_identification = local_gap_master_identification
        self.local_identity_key = local_identity_key
        self.remote_ble_gap_enc_info = remote_ble_gap_enc_info
        self.remote_gap_master_identification = remote_gap_master_identification
        self.remote_identity_key = remote_identity_key
        self.entropy = entropy
        self.ble_pro_auth_control = ble_pro_auth_control
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return:  parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.bluetooth_low_energy_address = BleNvsChunks.BluetoothLowEnergyAddress.fromHexList(
                inner_field_container_mixin.bluetooth_low_energy_address)
        inner_field_container_mixin.ble_gap_evt_auth_status = BleNvsChunks.BleGapEvtAuthStatus.fromHexList(
                inner_field_container_mixin.ble_gap_evt_auth_status)
        inner_field_container_mixin.local_ble_gap_enc_info = BleNvsChunks.BleGapEncInfo.fromHexList(
                inner_field_container_mixin.local_ble_gap_enc_info)
        inner_field_container_mixin.local_gap_master_identification = BleNvsChunks.GapMasterIdentification.fromHexList(
                inner_field_container_mixin.local_gap_master_identification)
        inner_field_container_mixin.local_identity_key = BleNvsChunks.IdentityKey.fromHexList(
                inner_field_container_mixin.local_identity_key)
        inner_field_container_mixin.remote_ble_gap_enc_info = BleNvsChunks.BleGapEncInfo.fromHexList(
                inner_field_container_mixin.remote_ble_gap_enc_info)
        inner_field_container_mixin.remote_gap_master_identification = BleNvsChunks.GapMasterIdentification.fromHexList(
                inner_field_container_mixin.remote_gap_master_identification)
        inner_field_container_mixin.remote_identity_key = BleNvsChunks.IdentityKey.fromHexList(
                inner_field_container_mixin.remote_identity_key)
        return inner_field_container_mixin
    # end def fromHexList
# end class ReceiverBleBondId


class ReceiverBleBondInfoIdV0(BitFieldContainerMixin, metaclass=abc.ABCMeta):
    """
    Define the format of the receiver NVS_BLE_BOND_INFO_ID chunk version 0

    typedef struct
    {
        /* General information */
        bool                        vPairingValid;

        /* From GATT client */
        uint16_t                    wServiceChangedHandle;

        /* From connection parameter module */
        ble_gap_conn_params_t       stConnParams;

        /* From DIS client */
        cli_dis_info_t              stDisInfo;

        /* From GAP client */
        cli_gap_info_t              stGapInfo;

        /* From HID client */
        cli_hid_dvc_rpt_map_v0_t    stDvcRptMapV0;

        /* From blepp client */
        cli_blepp_report_device_ts  stBlepp;

        /* From ble pro client */
        uint8_t                      bBleProServiceVersion;
        ble_pro_device_information_t bleProDeviceInformation;
        ble_pro_attribute_t          bleProAttributes;

        /* From HID client */
        enum
        {
            STATE_BTLDR_RECOVERY   = 0x00, /* No hid service found, device is in btldr recovery mode */
            STATE_APP_RECONNECTION = 0x01  /* Hid service found, device is in app or bootloader reconnection mode */
        } device_state;

        bool                         vEnumerationPending;
    } bond_info_t;

    typedef struct
    {
      uint16_t min_conn_interval;         /**< Minimum Connection Interval in 1.25 ms units */
      uint16_t max_conn_interval;         /**< Maximum Connection Interval in 1.25 ms units */
      uint16_t slave_latency;             /**< Slave Latency in number of connection events */
      uint16_t conn_sup_timeout;          /**< Connection Supervision Timeout in 10 ms units */
    } ble_gap_conn_params_t;

    typedef struct
    {
        char              szManufacturerName[BLE_DIS_CLI_STRING_SIZE]; with BLE_DIS_CLI_STRING_SIZE = 24 bytes
        char              szSerialNumber[BLE_DIS_CLI_STRING_SIZE]; with BLE_DIS_CLI_STRING_SIZE = 24 bytes
        ble_dis_pnp_id_t  stPnpIdCharValue;
    } cli_dis_info_t;

    typedef struct
    {
        uint8_t  vendor_id_source;                                  /**< Vendor ID Source. */
        uint16_t vendor_id;                                         /**< Vendor ID. */
        uint16_t product_id;                                        /**< Product ID. */
        uint16_t product_version;                                   /**< Product Version. */
    } ble_dis_pnp_id_t;

    typedef struct
    {
        char                 szDeviceName[BLE_GAP_CLI_NAME_SIZE]; with BLE_GAP_CLI_NAME_SIZE = 24 bytes
        uint16_t             wAppearance;
    } cli_gap_info_t;

    typedef struct
    {
        uint16_t                   version;
        cli_hid_rpt_ref_t          report[HIDC_REPORT_REF_COUNT]; with HIDC_REPORT_REF_COUNT=10
        cli_hid_cp_t               control_point[1];
        cli_hid_info_dev_t         info_dev;
    } cli_hid_dvc_rpt_map_v0_t;

    typedef struct
    {
        uint16_t                   handle;
        HidReportReference         stReportRefDevice;
    } cli_hid_rpt_ref_t;

    typedef struct
    {
        uint8_t         bReportId;
        uint8_t         bReportType;
    } HidReportReference;

    typedef struct
    {
        uint16_t                   handle;
    } cli_hid_cp_t;

    typedef struct
    {
        HidReportFeatureOutput_t   stHidReportFeaturePeriph;
        HidReportFeatureOutput_t   stHidReportFeatureActivated;
    } cli_hid_info_dev_t;

    typedef struct
    {
        uint32_t     dwAttr;
    } HidReportFeatureOutput_t;

    typedef struct
    {
        uint16_t bleppCharacteristicHandle;

    } cli_blepp_report_device_ts;

    typedef struct
    {
        union
        {
            device_type_t as_bits;
            uint8_t value;
        } device_type;
        uint8_t prod_specific_data;
    } ble_pro_device_information_t;

    typedef union
    {
        uint8_t bytes[4];
        uint32_t value;
    } ble_pro_attribute_t;

    """
    BITFIELD_LENGTH = 158  # 158 bytes

    class LEN:
        """
        FIELDS length
        """
        PAIRING_VALID = 0x08
        PADDING = 0x08
        SERVICE_CHANGED_HANDLE = 0x10
        MIN_CONN_INTERVAL = 0x10
        MAX_CONN_INTERVAL = 0x10
        SLAVE_LATENCY = 0x10
        CONN_SUP_TIMEOUT = 0x10
        DIS_MANUFACTURER_NAME = 0xC0
        DIS_SERIAL_NUMBER = 0xC0
        DIS_PNP_VENDOR_ID_SOURCE = 0x08
        DIS_PNP_VENDOR_ID = 0x10
        DIS_PNP_PRODUCT_ID = 0x10
        DIS_PNP_PRODUCT_VERSION = 0x10
        PADDING_2 = 0x08
        GAP_DEVICE_NAME = 0xC0
        GAP_APPEARANCE = 0x10
        HID_VERSION = 0x10
        HID_REPORT_MAP = 0x140
        HID_CONTROL_POINT_V0 = 0x10
        HID_REPORT_FEATURE_PERIPH = 0x20
        HID_REPORT_FEATURE_ACTIVATED = 0x20
        BLEPP_CHARACTERISTIC_HANDLE = 0x10
        BLE_PRO_SERVICE_VERSION = 0x08
        BLE_PRO_DEVICE_TYPE = 0x08
        BLE_PRO_VALUE = 0x08
        BLE_PRO_ATTRIBUTES = 0x20
        DEVICE_STATE = 0x08
        ENUMERATION_PENDING = 0x08
        PADDING_3 = 0x08

    # end class LEN

    class FID:
        """
        FIELDS identifier
        """
        PAIRING_VALID = 0xFF
        PADDING = PAIRING_VALID - 1
        SERVICE_CHANGED_HANDLE = PADDING - 1
        MIN_CONN_INTERVAL = SERVICE_CHANGED_HANDLE - 1
        MAX_CONN_INTERVAL = MIN_CONN_INTERVAL - 1
        SLAVE_LATENCY = MAX_CONN_INTERVAL - 1
        CONN_SUP_TIMEOUT = SLAVE_LATENCY - 1
        MANUFACTURER_NAME = CONN_SUP_TIMEOUT - 1
        SERIAL_NUMBER = MANUFACTURER_NAME - 1
        VENDOR_ID_SOURCE = SERIAL_NUMBER - 1
        VENDOR_ID = VENDOR_ID_SOURCE - 1
        PRODUCT_ID = VENDOR_ID - 1
        PRODUCT_VERSION = PRODUCT_ID - 1
        PADDING_2 = PRODUCT_VERSION - 1
        DEVICE_NAME = PADDING_2 - 1
        APPEARANCE = DEVICE_NAME - 1
        HID_VERSION = APPEARANCE - 1
        HID_REPORT_MAP = HID_VERSION - 1
        HID_CONTROL_POINT = HID_REPORT_MAP - 1
        HID_REPORT_FEATURE_PERIPH = HID_CONTROL_POINT - 1
        HID_REPORT_FEATURE_ACTIVATED = HID_REPORT_FEATURE_PERIPH - 1
        BLEPP_CHARACTERISTIC_HANDLE = HID_REPORT_FEATURE_ACTIVATED - 1
        BLE_PRO_SERVICE_VERSION = BLEPP_CHARACTERISTIC_HANDLE - 1
        BLE_PRO_DEVICE_TYPE = BLE_PRO_SERVICE_VERSION - 1
        BLE_PRO_VALUE = BLE_PRO_DEVICE_TYPE - 1
        BLE_PRO_ATTRIBUTES = BLE_PRO_VALUE - 1
        DEVICE_STATE = BLE_PRO_ATTRIBUTES - 1
        ENUMERATION_PENDING = DEVICE_STATE - 1
        PADDING_3 = ENUMERATION_PENDING - 1

    # end class FID

    class DEFAULT(object):
        """
        Fields Default values
        """
        PADDING = 0x00
    # end class DEFAULT

    class ENUMERATION:
        """
        vEnumerationPending field possible value
        """
        DISABLED = 0
        ENABLED = 1
    # end class ENUMERATION

    FIELDS = (
        BitField(
            fid=FID.PAIRING_VALID,
            length=LEN.PAIRING_VALID,
            title='Pairing Valid',
            name='pairing_valid',
            checks=(CheckHexList(LEN.PAIRING_VALID // 8), CheckByte(),),),
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
            default_value=DEFAULT.PADDING),
        BitField(
            fid=FID.SERVICE_CHANGED_HANDLE,
            length=LEN.SERVICE_CHANGED_HANDLE,
            title='Service Changed Handle',
            name='service_changed_handle',
            checks=(CheckHexList(LEN.SERVICE_CHANGED_HANDLE // 8), ),),
        BitField(
            fid=FID.MIN_CONN_INTERVAL,
            length=LEN.MIN_CONN_INTERVAL,
            title='Min Conn Interval',
            name='min_conn_interval',
            checks=(CheckHexList(LEN.MIN_CONN_INTERVAL // 8), ),),
        BitField(
            fid=FID.MAX_CONN_INTERVAL,
            length=LEN.MAX_CONN_INTERVAL,
            title='Max Conn Interval',
            name='max_conn_interval',
            checks=(CheckHexList(LEN.MAX_CONN_INTERVAL // 8), ),),
        BitField(
            fid=FID.SLAVE_LATENCY,
            length=LEN.SLAVE_LATENCY,
            title='Slave Latency',
            name='slave_latency',
            checks=(CheckHexList(LEN.SLAVE_LATENCY // 8), ),),
        BitField(
            fid=FID.CONN_SUP_TIMEOUT,
            length=LEN.CONN_SUP_TIMEOUT,
            title='Conn Sup Timeout',
            name='conn_sup_timeout',
            checks=(CheckHexList(LEN.CONN_SUP_TIMEOUT // 8), ),),
        BitField(
            fid=FID.MANUFACTURER_NAME,
            length=LEN.DIS_MANUFACTURER_NAME,
            title='Manufacturer Name',
            name='manufacturer_name',
            checks=(CheckHexList(LEN.DIS_MANUFACTURER_NAME // 8),),),
        BitField(
            fid=FID.SERIAL_NUMBER,
            length=LEN.DIS_SERIAL_NUMBER,
            title='Serial Number',
            name='serial_number',
            checks=(CheckHexList(LEN.DIS_SERIAL_NUMBER // 8),),),
        BitField(
            fid=FID.VENDOR_ID_SOURCE,
            length=LEN.DIS_PNP_VENDOR_ID_SOURCE,
            title='DIS PnP Vendor Id Source',
            name='dis_pnp_vendor_id_source',
            checks=(CheckHexList(LEN.DIS_PNP_VENDOR_ID_SOURCE // 8), CheckByte(),),),
        BitField(
            fid=FID.VENDOR_ID,
            length=LEN.DIS_PNP_VENDOR_ID,
            title='DIS PnP Vendor Id',
            name='dis_pnp_vendor_id',
            checks=(CheckHexList(LEN.DIS_PNP_VENDOR_ID // 8),),),
        BitField(
            fid=FID.PRODUCT_ID,
            length=LEN.DIS_PNP_PRODUCT_ID,
            title='DIS PnP Product Id',
            name='dis_pnp_product_id',
            checks=(CheckHexList(LEN.DIS_PNP_PRODUCT_ID // 8),),),
        BitField(
            fid=FID.PRODUCT_VERSION,
            length=LEN.DIS_PNP_PRODUCT_VERSION,
            title='DIS PnP Product Version',
            name='dis_pnp_product_version',
            checks=(CheckHexList(LEN.DIS_PNP_PRODUCT_VERSION // 8),),),
        BitField(
            fid=FID.PADDING_2,
            length=LEN.PADDING_2,
            title='Padding 2',
            name='padding_2',
            checks=(CheckHexList(LEN.PADDING_2 // 8), CheckByte(),),
            default_value=DEFAULT.PADDING),
        BitField(
            fid=FID.DEVICE_NAME,
            length=LEN.GAP_DEVICE_NAME,
            title='GAP Device Name',
            name='gap_device_name',
            checks=(CheckHexList(LEN.GAP_DEVICE_NAME // 8),),),
        BitField(
            fid=FID.APPEARANCE,
            length=LEN.GAP_APPEARANCE,
            title='GAP Appearance',
            name='gap_appearance',
            checks=(CheckHexList(LEN.GAP_APPEARANCE // 8),),),
        BitField(
            fid=FID.HID_VERSION,
            length=LEN.HID_VERSION,
            title='HID Version',
            name='hid_version',
            checks=(CheckHexList(LEN.HID_VERSION // 8),),),
        BitField(
            fid=FID.HID_REPORT_MAP,
            length=LEN.HID_REPORT_MAP,
            title='HID Report Map',
            name='hid_report_map',
            checks=(CheckHexList(LEN.HID_REPORT_MAP // 8),),),
        BitField(
            fid=FID.HID_CONTROL_POINT,
            length=LEN.HID_CONTROL_POINT_V0,
            title='HID Control Point',
            name='hid_control_point',
            checks=(CheckHexList(LEN.HID_CONTROL_POINT_V0 // 8),),),
        BitField(
            fid=FID.HID_REPORT_FEATURE_PERIPH,
            length=LEN.HID_REPORT_FEATURE_PERIPH,
            title='HID Report Feature Periph',
            name='hid_report_feature_periph',
            checks=(CheckHexList(LEN.HID_REPORT_FEATURE_PERIPH // 8),),),
        BitField(
            fid=FID.HID_REPORT_FEATURE_ACTIVATED,
            length=LEN.HID_REPORT_FEATURE_ACTIVATED,
            title='HID Report Feature Activated',
            name='hid_report_feature_activated',
            checks=(CheckHexList(LEN.HID_REPORT_FEATURE_ACTIVATED // 8),),),
        BitField(
            fid=FID.BLEPP_CHARACTERISTIC_HANDLE,
            length=LEN.BLEPP_CHARACTERISTIC_HANDLE,
            title='BLEPP Characteristic Handle',
            name='blepp_characteristic_handle',
            checks=(CheckHexList(LEN.BLEPP_CHARACTERISTIC_HANDLE // 8),),),
        BitField(
            fid=FID.BLE_PRO_SERVICE_VERSION,
            length=LEN.BLE_PRO_SERVICE_VERSION,
            title='BLE PRO Service Version',
            name='ble_pro_service_version',
            checks=(CheckHexList(LEN.BLE_PRO_SERVICE_VERSION // 8),),),
        BitField(
            fid=FID.BLE_PRO_DEVICE_TYPE,
            length=LEN.BLE_PRO_DEVICE_TYPE,
            title='BLE PRO Device Type',
            name='ble_pro_device_type',
            checks=(CheckHexList(LEN.BLE_PRO_DEVICE_TYPE // 8),),),
        BitField(
            fid=FID.BLE_PRO_VALUE,
            length=LEN.BLE_PRO_VALUE,
            title='BLE PRO Value',
            name='ble_pro_value',
            checks=(CheckHexList(LEN.BLE_PRO_VALUE // 8),),),
        BitField(
            fid=FID.BLE_PRO_ATTRIBUTES,
            length=LEN.BLE_PRO_ATTRIBUTES,
            title='BLE PRO Attributes',
            name='ble_pro_attributes',
            checks=(CheckHexList(LEN.BLE_PRO_ATTRIBUTES // 8),),),
        BitField(
            fid=FID.DEVICE_STATE,
            length=LEN.DEVICE_STATE,
            title='Device State',
            name='device_state',
            checks=(CheckHexList(LEN.DEVICE_STATE // 8),),),
        BitField(
            fid=FID.ENUMERATION_PENDING,
            length=LEN.ENUMERATION_PENDING,
            title='Enumeration Pending Flag',
            name='enumeration_pending',
            checks=(CheckHexList(LEN.ENUMERATION_PENDING // 8),),),
        BitField(
            fid=FID.PADDING_3,
            length=LEN.PADDING_3,
            title='Padding 3',
            name='padding_3',
            checks=(CheckHexList(LEN.PADDING_3 // 8), CheckByte(),),
            default_value=DEFAULT.PADDING),
    )

    def __init__(self, pairing_valid, service_changed_handle, min_conn_interval, max_conn_interval, slave_latency,
                 conn_sup_timeout, manufacturer_name, serial_number, dis_pnp_vendor_id_source, dis_pnp_vendor_id,
                 dis_pnp_product_id, dis_pnp_product_version, gap_device_name, gap_appearance, hid_version,
                 hid_report_map, hid_control_point, hid_report_feature_periph, hid_report_feature_activated,
                 blepp_characteristic_handle, ble_pro_service_version, ble_pro_device_type, ble_pro_value,
                 ble_pro_attributes, device_state, enumeration_pending, **kwargs):
        """
        :param pairing_valid: Pairing valid flag
        :type pairing_valid: ``HexList`` or ``int``
        :param service_changed_handle: Service changed handle
        :type service_changed_handle: ``HexList``
        :param min_conn_interval: Minimum connection interval
        :type min_conn_interval: ``HexList``
        :param max_conn_interval: Maximum connection interval
        :type max_conn_interval: ``HexList``
        :param slave_latency: Slave latency
        :type slave_latency: ``HexList``
        :param conn_sup_timeout: Connection supervision timeout
        :type conn_sup_timeout: ``HexList``
        :param manufacturer_name: Manufacturer name
        :type manufacturer_name: ``HexList``
        :param serial_number: Serial number
        :type serial_number: ``HexList``
        :param dis_pnp_vendor_id_source: DIS information Vendor ID source
        :type dis_pnp_vendor_id_source: ``HexList`` or ``int``
        :param dis_pnp_vendor_id: DIS information Vendor ID
        :type dis_pnp_vendor_id: ``HexList``
        :param dis_pnp_product_id: DIS information Product ID
        :type dis_pnp_product_id: ``HexList``
        :param dis_pnp_product_version: DIS information Product version
        :type dis_pnp_product_version: ``HexList``
        :param gap_device_name: GAP service information Device name
        :type gap_device_name: ``HexList``
        :param gap_appearance: GAP service information Appearance
        :type gap_appearance: ``HexList``
        :param hid_version: HID report information version
        :type hid_version: ``HexList``
        :param hid_report_map: HID Report map
        :type hid_report_map: ``HexList``
        :param hid_control_point: Control point map
        :type hid_control_point: ``HexList``
        :param hid_report_feature_periph: HID feature report support
        :type hid_report_feature_periph: ``HexList``
        :param hid_report_feature_activated: HID feature report activation
        :type hid_report_feature_activated: ``HexList``
        :param blepp_characteristic_handle: BLEPP characteristic value handle
        :type blepp_characteristic_handle: ``HexList``
        :param ble_pro_service_version: BLE Pro service version
        :type ble_pro_service_version: ``HexList`` or ``int``
        :param ble_pro_device_type: Device type
        :type ble_pro_device_type: ``HexList`` or ``int``
        :param ble_pro_value: Product specific data
        :type ble_pro_value: ``HexList``
        :param ble_pro_attributes: Bitfield showing the BLE Pro attributes that have been activated on the device
                                    Bit 0: Reporting delay suppression
        :type ble_pro_attributes: ``HexList``
        :param device_state: Device mode during last enumeration: 0x00 = recovery bootloader / 0x01 = application
        :type device_state: ``HexList`` or ``int``
        :param enumeration_pending: Flag indicating if re-enumeration is required or not
        :type enumeration_pending: ``HexList`` or ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.pairing_valid = pairing_valid
        self.service_changed_handle = service_changed_handle
        self.min_conn_interval = min_conn_interval
        self.max_conn_interval = max_conn_interval
        self.slave_latency = slave_latency
        self.conn_sup_timeout = conn_sup_timeout
        self.manufacturer_name = manufacturer_name
        self.serial_number = serial_number
        self.dis_pnp_vendor_id_source = dis_pnp_vendor_id_source
        self.dis_pnp_vendor_id = dis_pnp_vendor_id
        self.dis_pnp_product_id = dis_pnp_product_id
        self.dis_pnp_product_version = dis_pnp_product_version
        self.gap_device_name = gap_device_name
        self.gap_appearance = gap_appearance
        self.hid_version = hid_version
        self.hid_report_map = hid_report_map
        self.hid_control_point = hid_control_point
        self.hid_report_feature_periph = hid_report_feature_periph
        self.hid_report_feature_activated = hid_report_feature_activated
        self.blepp_characteristic_handle = blepp_characteristic_handle
        self.ble_pro_service_version = ble_pro_service_version
        self.ble_pro_device_type = ble_pro_device_type
        self.ble_pro_value = ble_pro_value
        self.ble_pro_attributes = ble_pro_attributes
        self.device_state = device_state
        self.enumeration_pending = enumeration_pending
    # end def __init__
# end class ReceiverBleBondInfoIdV0


class ReceiverBleBondInfoIdV1(ReceiverBleBondInfoIdV0):
    """
    Define the format of the receiver NVS_BLE_BOND_INFO_ID chunk version 1

    /* From HID client */
    cli_hid_dvc_rpt_map_t       stDvcRptMap;

    typedef struct
    {
        uint16_t                   version;
        cli_hid_rpt_ref_t          report[HIDC_REPORT_REF_COUNT];
        cli_hid_cp_t               control_point[HIDC_CONTROL_POINT_COUNT]; with HIDC_CONTROL_POINT_COUNT=10
        cli_hid_info_dev_t         info_dev;
    } cli_hid_dvc_rpt_map_t;
    """
    BITFIELD_LENGTH = 166  # 166 Bytes

    class LEN(ReceiverBleBondInfoIdV0.LEN):
        # See ``ReceiverBleBondInfoIdV0.LEN``
        HID_CONTROL_POINT_V1 = 0x50
    # end class LEN

    FIELDS = \
        ReceiverBleBondInfoIdV0.FIELDS[:(ReceiverBleBondInfoIdV0.FID.PAIRING_VALID -
                                         ReceiverBleBondInfoIdV0.FID.HID_CONTROL_POINT)] + \
        (
            BitField(
                fid=ReceiverBleBondInfoIdV0.FID.HID_CONTROL_POINT,
                length=LEN.HID_CONTROL_POINT_V1,
                title='HID Control Point',
                name='hid_control_point',
                checks=(CheckHexList(LEN.HID_CONTROL_POINT_V1 // 8),),),
        ) + \
        ReceiverBleBondInfoIdV0.FIELDS[(ReceiverBleBondInfoIdV0.FID.PAIRING_VALID -
                                        ReceiverBleBondInfoIdV0.FID.HID_CONTROL_POINT + 1):]

    def convert_to_v0(self):
        """
        Return the HexList representation compatible with NVS_BLE_BOND_INFO_V0_ID_0 = 0x28 to
        NVS_BLE_BOND_INFO_V0_ID_7 = 0x2F chunk data

        :return: The conversion of the Bond Info chunk in its version 0 format
        :rtype: ``HexList``
        """
        bond_info_v0 = ReceiverBleBondInfoIdV0(
            pairing_valid=self.pairing_valid,
            service_changed_handle=self.service_changed_handle,
            min_conn_interval=self.min_conn_interval,
            max_conn_interval=self.max_conn_interval,
            slave_latency=self.slave_latency,
            conn_sup_timeout=self.conn_sup_timeout,
            manufacturer_name=self.manufacturer_name,
            serial_number=self.serial_number,
            dis_pnp_vendor_id_source=self.dis_pnp_vendor_id_source,
            dis_pnp_vendor_id=self.dis_pnp_vendor_id,
            dis_pnp_product_id=self.dis_pnp_product_id,
            dis_pnp_product_version=self.dis_pnp_product_version,
            gap_device_name=self.gap_device_name,
            gap_appearance=self.gap_appearance,
            hid_version=self.hid_version,
            hid_report_map=self.hid_report_map,
            hid_control_point=self.hid_control_point[:ReceiverBleBondInfoIdV0.LEN.HID_CONTROL_POINT_V0 // 8],
            hid_report_feature_periph=self.hid_report_feature_periph,
            hid_report_feature_activated=self.hid_report_feature_activated,
            blepp_characteristic_handle=self.blepp_characteristic_handle,
            ble_pro_service_version=self.ble_pro_service_version,
            ble_pro_device_type=self.ble_pro_device_type,
            ble_pro_value=self.ble_pro_value,
            ble_pro_attributes=self.ble_pro_attributes,
            device_state=self.device_state,
            enumeration_pending=self.enumeration_pending
        )
        return HexList(bond_info_v0)
        # end def convert_to_v0
# end class ReceiverBleBondInfoIdV1


class LastBluetoothAddress(BleNvsChunks.BluetoothLowEnergyAddress):
    """
    Define the format of the NVS_BLE_LAST_GAP_ADDR_USED chunk
    """

    def __init__(self, device_address_type, device_resolvable_private_address_flag, device_bluetooth_address,
                 ref=None, **kwargs):
        """
        :param device_address_type: BLE_GAP_ADDR_TYPES Constant
        :type device_address_type: ``int``
        :param device_resolvable_private_address_flag: is the Private Address Resolvable
        :type device_resolvable_private_address_flag: ``bool``
        :param device_bluetooth_address: Bluetooth Low Energy Address
        :type device_bluetooth_address: ``HexList or BluetoothLowEnergyAddress``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.device_address_type = device_address_type
        self.device_resolvable_private_address_flag = device_resolvable_private_address_flag
        self.device_bluetooth_address = device_bluetooth_address
    # end def __init__
# end class LastBluetoothAddress

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
