#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.mcu.nrf52.bleproprepairingchunk
    :brief: NVS BLE Pro pre-pairing chunk definition
    :author: Christophe Roquebert
    :date: 2020/06/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import abc
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pylibrary.tools.numeral import Numeral
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleProPreIrkKeys(BitFieldContainerMixin):
    """
    This class defines the format of the following structure

    struct{
        uint8_t address[6];
        uint8_t irk[16];
    } local;
    struct{
        uint8_t address[6];
        uint8_t irk[16];
    } remote;
    """

    class LEN():
        """
        Field Lengths in bits
        """
        LOCAL_ADDRESS = 0x30
        LOCAL_IDENTITY_RESOLVING_KEY = 0x80
        REMOTE_ADDRESS = 0x30
        REMOTE_IDENTITY_RESOLVING_KEY = 0x80
        DATA = LOCAL_ADDRESS + LOCAL_IDENTITY_RESOLVING_KEY + REMOTE_ADDRESS + REMOTE_IDENTITY_RESOLVING_KEY
    # end class LEN

    class FID():
        """
        Field Identifiers
        """
        LOCAL_ADDRESS = 0xFF
        LOCAL_IDENTITY_RESOLVING_KEY = LOCAL_ADDRESS - 1
        REMOTE_ADDRESS = LOCAL_IDENTITY_RESOLVING_KEY - 1
        REMOTE_IDENTITY_RESOLVING_KEY = REMOTE_ADDRESS - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.LOCAL_ADDRESS,
            length=LEN.LOCAL_ADDRESS,
            title='LocalAddress',
            name='local_address',
            checks=(CheckHexList(LEN.LOCAL_ADDRESS // 8),)),
        BitField(
            fid=FID.LOCAL_IDENTITY_RESOLVING_KEY,
            length=LEN.LOCAL_IDENTITY_RESOLVING_KEY,
            title='LocalIdentityResolvingKey',
            name='local_identity_resolving_key',
            checks=(CheckHexList(LEN.LOCAL_IDENTITY_RESOLVING_KEY // 8),)),
        BitField(
            fid=FID.REMOTE_ADDRESS,
            length=LEN.REMOTE_ADDRESS,
            title='RemoteAddress',
            name='remote_address',
            checks=(CheckHexList(LEN.REMOTE_ADDRESS // 8),)),
        BitField(
            fid=FID.REMOTE_IDENTITY_RESOLVING_KEY,
            length=LEN.REMOTE_IDENTITY_RESOLVING_KEY,
            title='RemoteIdentityResolvingKey',
            name='remote_identity_resolving_key',
            checks=(CheckHexList(LEN.REMOTE_IDENTITY_RESOLVING_KEY // 8),)),
    )

    def __init__(self, local_address=None, local_identity_resolving_key=None, remote_address=None,
                 remote_identity_resolving_key=None, **kwargs):
        """
        Constructor
        :param local_address: Device Bluetooth address
        :type local_address: ``HexList``
        :param local_identity_resolving_key: Device IRK Key (optional)
        :type local_identity_resolving_key: ``HexList``
        :param remote_address: Receiver Bluetooth address
        :type remote_address: ``HexList``
        :param local_identity_resolving_key: Device IRK Key (optional)
        :type local_identity_resolving_key: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        if local_address is not None:
            self.local_address = local_address
        # end if
        if local_identity_resolving_key is not None:
            self.local_identity_resolving_key = local_identity_resolving_key
        # end if
        if remote_address is not None:
            self.remote_address = remote_address
        # end if
        if remote_identity_resolving_key is not None:
            self.remote_identity_resolving_key = remote_identity_resolving_key
        # end if
    # end def __init__
# end class BleProPreIrkKeys


class BleProPreIrkAndCsrkKeys(BleProPreIrkKeys):
    """
    This class defines the format of the following structure

    struct{
        uint8_t address[6];
        uint8_t irk[16];
        uint8_t csrk[16];
    } local;

    struct{
        uint8_t address[6];
        uint8_t irk[16];
        uint8_t csrk[16];
    } remote;
    """

    class LEN(BleProPreIrkKeys.LEN):
        """
        Field Lengths in bits
        """
        LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY = 0x80
        REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY = 0x80
        DATA = BleProPreIrkKeys.LEN.DATA + LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY + \
               REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY
    # end class LEN

    class FID(BleProPreIrkKeys.FID):
        """
        Field Identifiers
        """
        LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY = BleProPreIrkKeys.FID.LOCAL_IDENTITY_RESOLVING_KEY - 1
        REMOTE_ADDRESS = LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY - 1
        REMOTE_IDENTITY_RESOLVING_KEY = REMOTE_ADDRESS - 1
        REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY = REMOTE_IDENTITY_RESOLVING_KEY - 1

    # end class FID

    FIELDS = BleProPreIrkKeys.FIELDS[:2] + (
        BitField(
            fid=FID.LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY,
            length=LEN.LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY,
            title='LocalConnectionSignatureResolvingKey',
            name='local_connection_signature_resolving_key',
            checks=(CheckHexList(LEN.LOCAL_CONNECTION_SIGNATURE_RESOLVING_KEY // 8),)),
        BitField(
            fid=FID.REMOTE_ADDRESS,
            length=LEN.REMOTE_ADDRESS,
            title='RemoteAddress',
            name='remote_address',
            checks=(CheckHexList(LEN.REMOTE_ADDRESS // 8),)),
        BitField(
            fid=FID.REMOTE_IDENTITY_RESOLVING_KEY,
            length=LEN.REMOTE_IDENTITY_RESOLVING_KEY,
            title='RemoteIdentityResolvingKey',
            name='remote_identity_resolving_key',
            checks=(CheckHexList(LEN.REMOTE_IDENTITY_RESOLVING_KEY // 8),)),
         BitField(
             fid=FID.REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY,
             length=LEN.REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY,
             title='RemoteConnectionSignatureResolvingKey',
             name='remote_connection_signature_resolving_key',
             checks=(CheckHexList(LEN.REMOTE_CONNECTION_SIGNATURE_RESOLVING_KEY // 8),)),
             )

    def __init__(self, local_address=None, local_identity_resolving_key=None,
                 local_connection_signature_resolving_key=None, remote_address=None,
                 remote_identity_resolving_key=None, remote_connection_signature_resolving_key=None, **kwargs):
        """
        Constructor
        :param local_address: Device Bluetooth address
        :type local_address: ``HexList``
        :param local_identity_resolving_key: Device IRK Key (optional)
        :type local_identity_resolving_key: ``HexList``
        :param local_connection_signature_resolving_key: Device CSRK Key (optional)
        :type local_connection_signature_resolving_key: ``HexList``
        :param remote_address: Receiver Bluetooth address
        :type remote_address: ``HexList``
        :param local_identity_resolving_key: Device IRK Key (optional)
        :type local_identity_resolving_key: ``HexList``
        :param local_connection_signature_resolving_key: Device CSRK Key (optional)
        :type local_connection_signature_resolving_key: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(local_address, local_identity_resolving_key, remote_address,
                         remote_identity_resolving_key, **kwargs)

        # Parameters initialization
        if local_connection_signature_resolving_key is not None:
            self.local_connection_signature_resolving_key = local_connection_signature_resolving_key
        # end if
        if remote_connection_signature_resolving_key is not None:
            self.remote_connection_signature_resolving_key = remote_connection_signature_resolving_key
        # end if
    # end def __init__
# end class BleProPreIrkAndCsrkKeys


class BleProPrePairingNvsChunk(BitFieldContainerMixin):
    """
    This class defines the format of the xxx structure

    {
        uint8_t keyMap;
        uint8_t ltk[16];
        #endif
        struct{
            uint8_t address[6];
            uint8_t irk[16];
            uint8_t csrk[16];
        } local;

        struct{
            uint8_t address[6];
            uint8_t irk[16];
            uint8_t csrk[16];
        } remote;
    } x1816_prepairing_ts;
    """

    class KEYMAP():
        """
        Keys presence bitmap
        """
        KEY_LTK = 0x01
        KEY_LOCAL_ADDR = 0x02
        KEY_LOCAL_IRK = 0x04
        KEY_LOCAL_CSRK = 0x08
        KEY_REMOTE_ADDR = 0x20
        KEY_REMOTE_IRK = 0x40
        KEY_REMOTE_CSRK = 0x80
        KEYS_IRK = 0x44
        KEYS_CSRK = 0x88
    # class KEYMAP


    class LEN():
        """
        Field Lengths in bits
        """
        KEY_MAP = 0x08
        LONG_TERM_KEY = 0x80
        IRK_KEYS_STRUCT = 0x160
        IRK_AND_CSRK_KEYS_STRUCT = 0x260
    # end class LEN

    class FID():
        """
        Field Identifiers
        """
        KEY_MAP = 0xFF
        LONG_TERM_KEY = KEY_MAP - 1
        KEYS = LONG_TERM_KEY - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.KEY_MAP,
            length=LEN.KEY_MAP,
            title='KeyMap',
            name='key_map',
            checks=(CheckHexList(LEN.KEY_MAP // 8), CheckByte(),),),
        BitField(
            fid=FID.LONG_TERM_KEY,
            length=LEN.LONG_TERM_KEY,
            title='LongTermKey',
            name='long_term_key',
            checks=(CheckHexList(LEN.LONG_TERM_KEY // 8),)),
        BitField(
            fid=FID.KEYS,
            length=LEN.IRK_AND_CSRK_KEYS_STRUCT,
            title='Keys',
            name='keys',
            checks=(CheckHexList(max_length=(LEN.IRK_AND_CSRK_KEYS_STRUCT // 8),
                                 min_length=(LEN.IRK_KEYS_STRUCT // 8), ),)),
    )

    def __init__(self, key_map, long_term_key, local_address, local_identity_resolving_key=None,
                 local_connection_signature_resolving_key=None, remote_address=None,
                 remote_identity_resolving_key=None, remote_connection_signature_resolving_key=None, **kwargs):
        """
        Constructor
        :param key_map: Key Bitmap
                KEY_LTK             0x01
                KEY_LOCAL_ADDR      0x02
                KEY_LOCAL_IRK       0x04
                KEY_LOCAL_CSRK      0x08
                KEY_REMOTE_ADDR     0x20
                KEY_REMOTE_IRK      0x40
                KEY_REMOTE_CSRK     0x80
        :type key_map: ``int or HexList``
        :param long_term_key: Device Long Term Key
        :type long_term_key: ``HexList``
        :param local_address: Device Bluetooth address
        :type local_address: ``HexList``
        :param local_identity_resolving_key: Device IRK Key (optional)
        :type local_identity_resolving_key: ``HexList``
        :param local_connection_signature_resolving_key: Device CSRK Key (optional)
        :type local_connection_signature_resolving_key: ``HexList``
        :param remote_address: Receiver Bluetooth address
        :type remote_address: ``HexList``
        :param local_identity_resolving_key: Device IRK Key (optional)
        :type local_identity_resolving_key: ``HexList``
        :param local_connection_signature_resolving_key: Device CSRK Key (optional)
        :type local_connection_signature_resolving_key: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.key_map = key_map
        self.long_term_key = long_term_key
        if (self.key_map & self.KEYMAP.KEYS_CSRK) == self.KEYMAP.KEYS_CSRK:
            self.keys = self.BleProPreIrkAndCsrkKeys(local_address, local_identity_resolving_key,
                 local_connection_signature_resolving_key, remote_address, remote_identity_resolving_key,
                 remote_connection_signature_resolving_key)
        else:
            self.keys = self.BleProPreIrkKeys(local_address, local_identity_resolving_key, remote_address,
                remote_identity_resolving_key)
        # end if
    # end def __init__


    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param \*args: List of arguments
        :type \*args: list
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict

        :return:  parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        if len(inner_field_container_mixin.keys) == (BleProPreIrkAndCsrkKeys.LEN.DATA // 8):
            inner_field_container_mixin.keys = BleProPreIrkAndCsrkKeys.fromHexList(inner_field_container_mixin.keys)
        elif len(inner_field_container_mixin.keys) == (BleProPreIrkKeys.LEN.DATA // 8):
            inner_field_container_mixin.keys = BleProPreIrkKeys.fromHexList(inner_field_container_mixin.keys)
        else:
            raise ValueError(f"Unknown Ble Pro Pre-Pairing Key structure (len={len(inner_field_container_mixin.keys)})")
        # end if

        return inner_field_container_mixin
    # end def fromHexList
# end class BleProPrePairingNvsChunk

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
