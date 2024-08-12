#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.connectchunks
:brief: Device connection NVS chunk definition
:author: Christophe Roquebert
:date: 2020/06/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from enum import unique

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
class ConnectIdChunkData:
    """
    Connect Id Chunk constants
    """
    @unique
    class EVENT(IntEnum):
        """
        Event values
        """
        NO_EVT = 0
        UFY_EVT_BCAST_SUCCEEDED = 1
        UFY_EVT_BCAST_FAILED = 2
        UFY_EVT_GOTHARD_CONNECTED = 3
        UFY_EVT_RECONN_SUCCEEDED = 4
        UFY_EVT_RECONN_FAILED = 5
        UFY_EVT_RECONN_START = 6
        BLE_EVT_BCAST_SUCCEEDED = 7
        BLE_EVT_BCAST_FAILED = 8
        BLE_EVT_RECONN_SUCCEEDED = 9
        BLE_EVT_RECONN_FAILED = 10
        BLE_EVT_RECONN_START = 11
        USB_EVT_READY = 12
        USB_EVT_NOT_READY = 13
        USR_EVT_BCAST_REQUEST = 14
        USR_EVT_BCAST_HOSTID_REQUEST = 15
        USR_EVT_RECONN_REQUEST = 16
        HOST_EVT_RECONN_REQUEST = 17
        SERVICE_EVT = 18
        SERVICE_EVT_BLE_BCAST_FAILED = 19
        SERVICE_EVT_UFY_SILENT_BCAST_FAILED = 20
        PWR_UP_EVT = 21
        WAKE_UP_EVT = 22
        MAX_EVT = 23
    # end class EVENT

    @unique
    class STATUS(IntEnum):
        """
        scheme_te values
        """
        OOB = 0         # Channel is in OOB state
        BLE_PAIRED = 1  # Channel is paired with a BLE host
        UFY_PAIRED = 2  # Channel is paired with a UFY host
        UNPAIRED = 3    # Channel has no valid pairing, all non-active OOB channels become UNPAIRED when an active OOB
                        # reconnects to the factory pre-paired receiver
        MAX_SCHEME = 4
    # end class STATUS

    @unique
    class PairingSrc(IntEnum):
        """
        pairing_source_te values
        """
        NONE = 0  # The slot has no pairing
        USR = 1  # The pairing was done by the user
        MFG = 2  # Pre-pairing
    # end class PairingSrc

    @unique
    class Protocol(IntEnum):
        """
        Bootloader Connect Chunk Protocol values
        """
        NONE = 0
        UNIFYING = 1
        BLE = 2
        USB = 4
    # end class Protocol

    @unique
    class GamingProtocolFlags(IntEnum):
        """
        Define the 'connection flags' field in NVS. cf conn_scheme_all.c in platform codeline
        """
        CONN_USB = 0x01
        CONN_UFY = 0x02
        CONN_CRUSH = 0x04
        CONN_BT = 0x08
        CONN_BLE = 0x10
        CONN_BLE_LS2 = 0x20
        CONN_LS2 = 0x40
    # end class GamingProtocolFlags
# end class ConnectIdChunkData


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BootloaderConnectIdChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_BTLDR_CONNECT_ID chunk

    {
        uint8_t hostIdx;
        uint8_t protocol;
    } cmgr_shared_ts;

    """
    class LEN():
        """
        Field Lengths in bits
        """
        HOST_IDX = 0x08
        PROTOCOL = 0x08
    # end class LEN

    class FID():
        """
        Field Identifiers
        """
        HOST_IDX = 0xFF
        PROTOCOL = 0xFE
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.HOST_IDX,
            length=LEN.HOST_IDX,
            title='HostIdx',
            name='host_idx',
            checks=(CheckHexList(LEN.HOST_IDX // 8), CheckByte(),),),
        BitField(
            fid=FID.PROTOCOL,
            length=LEN.PROTOCOL,
            title='Protocol',
            name='protocol',
            checks=(CheckHexList(LEN.PROTOCOL // 8), CheckByte(),),),
    )

    def __init__(self, host_idx, protocol, ref=None, **kwargs):
        """
        Constructor

        :param host_idx: Host Index
        :type host_idx: ``HexList``
        :param protocol: RF Protocol
        :type protocol: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.host_idx = host_idx
        self.protocol = protocol

    # end def __init__
# end class BootloaderConnectIdChunk


class ConnectIdChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_CONNECT_ID chunk
    """

    class LEN(IntEnum):
        """
        Field Lengths in bits
        """
        CONNECT_ID_BLE_PRO_1_HOST_DATA = 0x18
        CONNECT_ID_BLE_PRO_2_HOSTS_DATA = 0x28
        CONNECT_ID_BLE_PRO_3_HOSTS_DATA = 0x38
        CONNECT_ID_GAMING_1_HOST_DATA = 0x20
        CONNECT_ID_GAMING_2_HOSTS_DATA = 0x30
        CONNECT_ID_GAMING_3_HOSTS_DATA = 0x40
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        CONNECT_ID_DATA = 0xFF
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.CONNECT_ID_DATA,
            length=max(LEN),
            title='Data',
            name='data',
            checks=(CheckHexList(max_length=(max(LEN) // 8), min_length=(min(LEN) // 8), ),)),
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
        if len(inner_field_container_mixin.data) == (cls.LEN.CONNECT_ID_BLE_PRO_1_HOST_DATA // 8):
            inner_field_container_mixin.data = ConnectIdBlePro1HostChunk.fromHexList(inner_field_container_mixin.data)
        elif len(inner_field_container_mixin.data) == (cls.LEN.CONNECT_ID_BLE_PRO_2_HOSTS_DATA // 8):
            inner_field_container_mixin.data = ConnectIdBlePro2HostsChunk.fromHexList(inner_field_container_mixin.data)
        elif len(inner_field_container_mixin.data) == (cls.LEN.CONNECT_ID_BLE_PRO_3_HOSTS_DATA // 8):
            inner_field_container_mixin.data = ConnectIdBlePro3HostsChunk.fromHexList(inner_field_container_mixin.data)
        elif len(inner_field_container_mixin.data) == (cls.LEN.CONNECT_ID_GAMING_1_HOST_DATA // 8):
            inner_field_container_mixin.data = ConnectIdGaming1HostChunk.fromHexList(inner_field_container_mixin.data)
        elif len(inner_field_container_mixin.data) == (cls.LEN.CONNECT_ID_GAMING_2_HOSTS_DATA // 8):
            inner_field_container_mixin.data = ConnectIdGaming2HostsChunk.fromHexList(inner_field_container_mixin.data)
        elif len(inner_field_container_mixin.data) == (cls.LEN.CONNECT_ID_GAMING_3_HOSTS_DATA // 8):
            inner_field_container_mixin.data = ConnectIdGaming3HostsChunk.fromHexList(inner_field_container_mixin.data)
        else:
            raise ValueError("Unknown Connect Id chunk structure")
        # end if

        return inner_field_container_mixin
    # end def fromHexList
# end class ConnectIdChunk


class ConnectIdDualChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_CONNECT_ID chunk

    {
        /* If true, then the user requested a new pairing (ble or ufy) */
        bool bcast_pending;
        /* The current or last active radio host */
        uint8_t hostIdx;
        /* The initial state handler (a.k.a connect scheme) for each of the radio host */
        scheme_te scheme[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class LEN():
        """
        Field Lengths in bits
        """
        BCAST_PENDING = 0x08
        HOST_INDEX = 0x08
        SCHEME_HOST_0 = 0x08
        SCHEME_HOST_1 = 0x08
        SCHEME_HOST_2 = 0x08
    # end class LEN

    class FID():
        """
        Field Identifiers
        """
        BCAST_PENDING = 0xFF
        HOST_INDEX = BCAST_PENDING - 1
        SCHEME_HOST_0 = HOST_INDEX - 1
        SCHEME_HOST_1 = SCHEME_HOST_0 - 1
        SCHEME_HOST_2 = SCHEME_HOST_1 - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.BCAST_PENDING,
            length=LEN.BCAST_PENDING,
            title='BcastPending',
            name='bcast_pending',
            checks=(CheckHexList(LEN.BCAST_PENDING // 8), CheckByte(),),),
        BitField(
            fid=FID.HOST_INDEX,
            length=LEN.HOST_INDEX,
            title='HostIndex',
            name='host_index',
            checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_0,
            length=LEN.SCHEME_HOST_0,
            title='SchemeHost0',
            name='scheme_host_0',
            checks=(CheckHexList(LEN.SCHEME_HOST_0 // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_1,
            length=LEN.SCHEME_HOST_1,
            title='SchemeHost1',
            name='scheme_host_1',
            checks=(CheckHexList(LEN.SCHEME_HOST_1 // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_2,
            length=LEN.SCHEME_HOST_2,
            title='SchemeHost2',
            name='scheme_host_2',
            checks=(CheckHexList(LEN.SCHEME_HOST_2 // 8), CheckByte(),),),
    )

    def __init__(self, bcast_pending, host_index, scheme_host_0, scheme_host_1, scheme_host_2, ref=None, **kwargs):
        """
        Constructor

        :param bcast_pending: If true, then the user requested a new pairing (ble or ufy)
        :type bcast_pending: ``HexList``
        :param host_index: The current or last active radio host
        :type host_index: ``HexList``
        :param scheme_host_0: The initial state handler (a.k.a connect scheme) for radio host 0
        :type scheme_host_0: ``HexList``
        :param scheme_host_1: The initial state handler (a.k.a connect scheme) for radio host 1
        :type scheme_host_1: ``HexList``
        :param scheme_host_2: The initial state handler (a.k.a connect scheme) for radio host 2
        :type scheme_host_2: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.bcast_pending = bcast_pending
        self.host_index = host_index
        self.scheme_host_0 = scheme_host_0
        self.scheme_host_1 = scheme_host_1
        self.scheme_host_2 = scheme_host_2
    # end def __init__
# end class ConnectIdDualChunk


class ConnectIdDualKeyboardChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_CONNECT_ID Keyboard chunk

    {
        /* If true, then the user requested a new pairing (ble or ufy) */
        bool bcast_pending;
        /* The current or last active radio host */
        uint8_t hostIdx;
        /* store the previous host idx if we need to return */
        uint8_t prevHostIdx;
        /* The initial state handler (a.k.a connect scheme) for each of the radio host */
        scheme_te scheme[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class LEN():
        """
        Field Lengths in bits
        """
        BCAST_PENDING = 0x08
        HOST_INDEX = 0x08
        PREVIOUS_HOST_INDEX = 0x08
        SCHEME_HOST_0 = 0x08
        SCHEME_HOST_1 = 0x08
        SCHEME_HOST_2 = 0x08
    # end class LEN

    class FID():
        """
        Field Identifiers
        """
        BCAST_PENDING = 0xFF
        HOST_INDEX = BCAST_PENDING - 1
        PREVIOUS_HOST_INDEX = HOST_INDEX - 1
        SCHEME_HOST_0 = PREVIOUS_HOST_INDEX - 1
        SCHEME_HOST_1 = SCHEME_HOST_0 - 1
        SCHEME_HOST_2 = SCHEME_HOST_1 - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.BCAST_PENDING,
            length=LEN.BCAST_PENDING,
            title='BcastPending',
            name='bcast_pending',
            checks=(CheckHexList(LEN.BCAST_PENDING // 8), CheckByte(),),),
        BitField(
            fid=FID.HOST_INDEX,
            length=LEN.HOST_INDEX,
            title='HostIndex',
            name='host_index',
            checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),),),
        BitField(
            fid=FID.PREVIOUS_HOST_INDEX,
            length=LEN.PREVIOUS_HOST_INDEX,
            title='PreviousHostIndex',
            name='previous_host_index',
            checks=(CheckHexList(LEN.PREVIOUS_HOST_INDEX // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_0,
            length=LEN.SCHEME_HOST_0,
            title='SchemeHost0',
            name='scheme_host_0',
            checks=(CheckHexList(LEN.SCHEME_HOST_0 // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_1,
            length=LEN.SCHEME_HOST_1,
            title='SchemeHost1',
            name='scheme_host_1',
            checks=(CheckHexList(LEN.SCHEME_HOST_1 // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_2,
            length=LEN.SCHEME_HOST_2,
            title='SchemeHost2',
            name='scheme_host_2',
            checks=(CheckHexList(LEN.SCHEME_HOST_2 // 8), CheckByte(),),),
    )

    def __init__(self, bcast_pending, host_index, previous_host_index, scheme_host_0, scheme_host_1, scheme_host_2,
                 ref=None, **kwargs):
        """
        Constructor

        :param bcast_pending: If true, then the user requested a new pairing (ble or ufy)
        :type bcast_pending: ``HexList``
        :param host_index: The current or last active radio host
        :type host_index: ``HexList``
        :param previous_host_index: The previous host idx if we need to return
        :type previous_host_index: ``HexList``
        :param scheme_host_0: The initial state handler (a.k.a connect scheme) for radio host 0
        :type scheme_host_0: ``HexList``
        :param scheme_host_1: The initial state handler (a.k.a connect scheme) for radio host 1
        :type scheme_host_1: ``HexList``
        :param scheme_host_2: The initial state handler (a.k.a connect scheme) for radio host 2
        :type scheme_host_2: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.bcast_pending = bcast_pending
        self.host_index = host_index
        self.previous_host_index = previous_host_index
        self.scheme_host_0 = scheme_host_0
        self.scheme_host_1 = scheme_host_1
        self.scheme_host_2 = scheme_host_2
    # end def __init__
# end class ConnectIdDualKeyboardChunk


class ConnectIdBlePro1HostChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_CONNECT_ID chunk used on BLE Pro Products supporting 1 host

    {
        /* The current or last active radio host */
        uint8_t hostIdx;
        pairing_source_te pairing_source[conn_scheme_MAX_HOST];
        /* The initial state handler (a.k.a connect scheme) for each of the radio host */
        scheme_te scheme[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class LEN:
        """
        Field Lengths in bits
        """
        HOST_INDEX = 0x08
        PAIRING_SRC_0 = 0x08
        SCHEME_HOST_0 = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        HOST_INDEX = 0xFF
        PAIRING_SRC_0 = HOST_INDEX - 1
        SCHEME_HOST_0 = PAIRING_SRC_0 - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.HOST_INDEX,
            length=LEN.HOST_INDEX,
            title='HostIndex',
            name='host_index',
            checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),),),
        BitField(
            fid=FID.PAIRING_SRC_0,
            length=LEN.PAIRING_SRC_0,
            title='PairingSrc0',
            name='pairing_src_0',
            checks=(CheckHexList(LEN.PAIRING_SRC_0 // 8), CheckByte(),), ),
        BitField(
            fid=FID.SCHEME_HOST_0,
            length=LEN.SCHEME_HOST_0,
            title='SchemeHost0',
            name='scheme_host_0',
            checks=(CheckHexList(LEN.SCHEME_HOST_0 // 8), CheckByte(),),),
    )

    def __init__(self, host_index, pairing_src_0, scheme_host_0, **kwargs):
        """
        Constructor

        :param host_index: The current or last active radio host
        :type host_index: ``HexList``
        :param pairing_src_0: Pairing source for host 0
        :type pairing_src_0: ``HexList or int``
        :param scheme_host_0: The initial state handler (a.k.a connect scheme) for radio host 0
        :type scheme_host_0: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.host_index = host_index
        self.pairing_src_0 = pairing_src_0
        self.scheme_host_0 = scheme_host_0
    # end def __init__
# end class ConnectIdBlePro1HostChunk


class ConnectIdBlePro2HostsChunk(ConnectIdBlePro1HostChunk):
    """
    This class defines the format of the NVS_CONNECT_ID chunk used on BLE Pro Products supporting 2 hosts

    {
        /* The current or last active radio host */
        uint8_t hostIdx;
        pairing_source_te pairing_source[conn_scheme_MAX_HOST];
        /* The initial state handler (a.k.a connect scheme) for each of the radio host */
        scheme_te scheme[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class LEN(ConnectIdBlePro1HostChunk.LEN):
        """
        Field Lengths in bits
        """
        PAIRING_SRC_1 = 0x08
        SCHEME_HOST_1 = 0x08
    # end class LEN

    class FID(ConnectIdBlePro1HostChunk.FID):
        """
        Field Identifiers
        """
        PAIRING_SRC_1 = ConnectIdBlePro1HostChunk.FID.PAIRING_SRC_0 - 1
        SCHEME_HOST_0 = PAIRING_SRC_1 - 1
        SCHEME_HOST_1 = SCHEME_HOST_0 - 1
    # end class FID

    FIELDS = ConnectIdBlePro1HostChunk.FIELDS[:-1] + (
        BitField(
            fid=FID.PAIRING_SRC_1,
            length=LEN.PAIRING_SRC_1,
            title='PairingSrc1',
            name='pairing_src_1',
            checks=(CheckHexList(LEN.PAIRING_SRC_1 // 8), CheckByte(),), ),
        BitField(
            fid=FID.SCHEME_HOST_0,
            length=LEN.SCHEME_HOST_0,
            title='SchemeHost0',
            name='scheme_host_0',
            checks=(CheckHexList(LEN.SCHEME_HOST_0 // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_1,
            length=LEN.SCHEME_HOST_1,
            title='SchemeHost1',
            name='scheme_host_1',
            checks=(CheckHexList(LEN.SCHEME_HOST_1 // 8), CheckByte(),),),
    )

    def __init__(self, host_index, pairing_src_0, pairing_src_1, scheme_host_0, scheme_host_1, **kwargs):
        """
        Constructor

        :param host_index: The current or last active radio host
        :type host_index: ``HexList``
        :param pairing_src_0: Pairing source for host 0
        :type pairing_src_0: ``HexList or int``
        :param pairing_src_1: Pairing source for host 1
        :type pairing_src_1: ``HexList or int``
        :param scheme_host_0: The initial state handler (a.k.a connect scheme) for radio host 0
        :type scheme_host_0: ``HexList``
        :param scheme_host_1: The initial state handler (a.k.a connect scheme) for radio host 1
        :type scheme_host_1: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(host_index, pairing_src_0, scheme_host_0, **kwargs)

        # Parameters initialization
        self.pairing_src_1 = pairing_src_1
        self.scheme_host_1 = scheme_host_1
    # end def __init__
# end class ConnectIdBlePro2HostsChunk


class ConnectIdBlePro3HostsChunk(ConnectIdBlePro2HostsChunk):
    """
    This class defines the format of the NVS_CONNECT_ID chunk used on BLE Pro Products supporting 3 hosts

    {
        /* The current or last active radio host */
        uint8_t hostIdx;
        pairing_source_te pairing_source[conn_scheme_MAX_HOST];
        /* The initial state handler (a.k.a connect scheme) for each of the radio host */
        scheme_te scheme[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class LEN(ConnectIdBlePro2HostsChunk.LEN):
        """
        Field Lengths in bits
        """
        PAIRING_SRC_2 = 0x08
        SCHEME_HOST_2 = 0x08
    # end class LEN

    class FID(ConnectIdBlePro2HostsChunk.FID):
        """
        Field Identifiers
        """
        PAIRING_SRC_2 = ConnectIdBlePro2HostsChunk.FID.PAIRING_SRC_1 - 1
        SCHEME_HOST_0 = PAIRING_SRC_2 - 1
        SCHEME_HOST_1 = SCHEME_HOST_0 - 1
        SCHEME_HOST_2 = SCHEME_HOST_1 - 1
    # end class FID

    FIELDS = ConnectIdBlePro2HostsChunk.FIELDS[:-2] + (
        BitField(
            fid=FID.PAIRING_SRC_2,
            length=LEN.PAIRING_SRC_2,
            title='PairingSrc2',
            name='pairing_src_2',
            checks=(CheckHexList(LEN.PAIRING_SRC_2 // 8), CheckByte(),), ),
        BitField(
            fid=FID.SCHEME_HOST_0,
            length=LEN.SCHEME_HOST_0,
            title='SchemeHost0',
            name='scheme_host_0',
            checks=(CheckHexList(LEN.SCHEME_HOST_0 // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_1,
            length=LEN.SCHEME_HOST_1,
            title='SchemeHost1',
            name='scheme_host_1',
            checks=(CheckHexList(LEN.SCHEME_HOST_1 // 8), CheckByte(),),),
        BitField(
            fid=FID.SCHEME_HOST_2,
            length=LEN.SCHEME_HOST_2,
            title='SchemeHost2',
            name='scheme_host_2',
            checks=(CheckHexList(LEN.SCHEME_HOST_2 // 8), CheckByte(),),),
    )

    def __init__(self, host_index, pairing_src_0, pairing_src_1, pairing_src_2, scheme_host_0, scheme_host_1,
                 scheme_host_2, **kwargs):
        """
        Constructor

        :param host_index: The current or last active radio host
        :type host_index: ``HexList``
        :param pairing_src_0: Pairing source for host 0
        :type pairing_src_0: ``HexList or int``
        :param pairing_src_1: Pairing source for host 1
        :type pairing_src_1: ``HexList or int``
        :param pairing_src_2: Pairing source for host 2
        :type pairing_src_2: ``HexList or int``
        :param scheme_host_0: The initial state handler (a.k.a connect scheme) for radio host 0
        :type scheme_host_0: ``HexList``
        :param scheme_host_1: The initial state handler (a.k.a connect scheme) for radio host 1
        :type scheme_host_1: ``HexList``
        :param scheme_host_2: The initial state handler (a.k.a connect scheme) for radio host 2
        :type scheme_host_2: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(host_index, pairing_src_0, pairing_src_1, scheme_host_0, scheme_host_1, **kwargs)

        # Parameters initialization
        self.pairing_src_2 = pairing_src_2
        self.scheme_host_2 = scheme_host_2
    # end def __init__
# end class ConnectIdBlePro3HostsChunk


class ConnectIdGaming1HostChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_CONNECT_ID chunk used on Gaming Products supporting 1 host

    typedef struct
    {
        // If true, then the user requested a new pairing (ble or ufy)
        bool bcast_pending;
        // The currently active host idx
        uint8_t hostIdx;
        // If true, the alternate mode is selected
        bool altMode[conn_scheme_MAX_HOST];
        uint8_t connFlags[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class LEN:
        """
        Field Lengths in bits
        """
        BCAST_PENDING = 0x08
        HOST_INDEX = 0x08
        ALT_MODE = 0x08
        CONN_FLAGS = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        BCAST_PENDING = 0xFF
        HOST_INDEX = BCAST_PENDING - 1
        ALT_MODE_0 = HOST_INDEX - 1
        CONN_FLAGS_0 = ALT_MODE_0 - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.BCAST_PENDING,
            length=LEN.BCAST_PENDING,
            title='BCastPending',
            name='bcast_pending',
            checks=(CheckHexList(LEN.BCAST_PENDING // 8), CheckByte(),),),
        BitField(
            fid=FID.HOST_INDEX,
            length=LEN.HOST_INDEX,
            title='HostIndex',
            name='host_index',
            checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(
            fid=FID.ALT_MODE_0,
            length=LEN.ALT_MODE,
            title='AltMode0',
            name='alt_mode_0',
            checks=(CheckHexList(LEN.ALT_MODE // 8), CheckByte(),),),
        BitField(
            fid=FID.CONN_FLAGS_0,
            length=LEN.CONN_FLAGS,
            title='ConnFlags0',
            name='conn_flags_0',
            checks=(CheckHexList(LEN.CONN_FLAGS // 8), CheckByte(),), ),
    )

    def __init__(self, bcast_pending, host_index, alt_mode_0, conn_flags_0, **kwargs):
        """
        :param bcast_pending: If true, then the user requested a new pairing (ble or ufy)
        :type bcast_pending: ``HexList`` or ``int`` or ``bool``
        :param host_index: The currently active host idx
        :type host_index: ``HexList``
        :param alt_mode_0: If true, the alternate mode is selected for host 0
        :type alt_mode_0: ``HexList`` or ``int`` or ``bool``
        :param conn_flags_0: Protocol Flags for host 0
        :type conn_flags_0: ``HexList`` or ``int`` or ``GamingProtocolFlags``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.bcast_pending = bcast_pending
        self.host_index = host_index
        self.alt_mode_0 = alt_mode_0
        self.conn_flags_0 = conn_flags_0
    # end def __init__
# end class ConnectIdGaming1HostChunk


class ConnectIdGaming2HostsChunk(ConnectIdGaming1HostChunk):
    """
    This class defines the format of the NVS_CONNECT_ID chunk used on Gaming Products supporting 2 hosts

    typedef struct
    {
        // If true, then the user requested a new pairing (ble or ufy)
        bool bcast_pending;
        // The currently active host idx
        uint8_t hostIdx;
        // If true, the alternate mode is selected
        bool altMode[conn_scheme_MAX_HOST];
        uint8_t connFlags[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class FID(ConnectIdGaming1HostChunk.FID):
        # See ``ConnectIdGaming1HostChunk.FID``
        ALT_MODE_1 = ConnectIdGaming1HostChunk.FID.ALT_MODE_0 - 1
        CONN_FLAGS_0 = ALT_MODE_1 - 1
        CONN_FLAGS_1 = CONN_FLAGS_0 - 1
    # end class FID

    FIELDS = ConnectIdGaming1HostChunk.FIELDS[:-1] + (
        BitField(
            fid=FID.ALT_MODE_1,
            length=ConnectIdGaming1HostChunk.LEN.ALT_MODE,
            title='AltMode1',
            name='alt_mode_1',
            checks=(CheckHexList(ConnectIdGaming1HostChunk.LEN.ALT_MODE // 8), CheckByte(),), ),
        BitField(
            fid=FID.CONN_FLAGS_0,
            length=ConnectIdGaming1HostChunk.LEN.CONN_FLAGS,
            title='ConnFlags0',
            name='conn_flags_0',
            checks=(CheckHexList(ConnectIdGaming1HostChunk.LEN.CONN_FLAGS // 8), CheckByte(),), ),
        BitField(
            fid=FID.CONN_FLAGS_1,
            length=ConnectIdGaming1HostChunk.LEN.CONN_FLAGS,
            title='ConnFlags1',
            name='conn_flags_1',
            checks=(CheckHexList(ConnectIdGaming1HostChunk.LEN.CONN_FLAGS // 8), CheckByte(),), ),
    )

    def __init__(self, bcast_pending, host_index, alt_mode_0, alt_mode_1, conn_flags_0, conn_flags_1, **kwargs):
        """
        :param bcast_pending: If true, then the user requested a new pairing (ble or ufy)
        :type bcast_pending: ``HexList`` or ``int`` or ``bool``
        :param host_index: The currently active host idx
        :type host_index: ``HexList``
        :param alt_mode_0: If true, the alternate mode is selected for host 0
        :type alt_mode_0: ``HexList`` or ``int`` or ``bool``
        :param alt_mode_1: If true, the alternate mode is selected for host 1
        :type alt_mode_1: ``HexList`` or ``int`` or ``bool``
        :param conn_flags_0: Protocol Flags  for host 0
        :type conn_flags_0: ``HexList`` or ``int`` or ``GamingProtocolFlags``
        :param conn_flags_1: Protocol Flags for host 1
        :type conn_flags_1: ``HexList`` or ``int`` or ``GamingProtocolFlags``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(bcast_pending, host_index, alt_mode_0, conn_flags_0, **kwargs)

        # Parameters initialization
        self.alt_mode_1 = alt_mode_1
        self.conn_flags_1 = conn_flags_1
    # end def __init__
# end class ConnectIdGaming2HostsChunk


class ConnectIdGaming3HostsChunk(ConnectIdGaming2HostsChunk):
    """
    This class defines the format of the NVS_CONNECT_ID chunk used on Gaming Products supporting 3 hosts

    typedef struct
    {
        // If true, then the user requested a new pairing (ble or ufy)
        bool bcast_pending;
        // The currently active host idx
        uint8_t hostIdx;
        // If true, the alternate mode is selected
        bool altMode[conn_scheme_MAX_HOST];
        uint8_t connFlags[conn_scheme_MAX_HOST];
    } cmgr_nvm_data_ts;
    """

    class FID(ConnectIdGaming2HostsChunk.FID):
        # See ``ConnectIdGaming2HostsChunk.FID``
        ALT_MODE_2 = ConnectIdGaming2HostsChunk.FID.ALT_MODE_1 - 1
        CONN_FLAGS_0 = ALT_MODE_2 - 1
        CONN_FLAGS_1 = CONN_FLAGS_0 - 1
        CONN_FLAGS_2 = CONN_FLAGS_1 - 1
    # end class FID

    FIELDS = ConnectIdGaming2HostsChunk.FIELDS[:-2] + (
        BitField(
            fid=FID.ALT_MODE_2,
            length=ConnectIdGaming1HostChunk.LEN.ALT_MODE,
            title='AltMode2',
            name='alt_mode_2',
            checks=(CheckHexList(ConnectIdGaming1HostChunk.LEN.ALT_MODE // 8), CheckByte(),), ),
        BitField(
            fid=FID.CONN_FLAGS_0,
            length=ConnectIdGaming1HostChunk.LEN.CONN_FLAGS,
            title='ConnFlags0',
            name='conn_flags_0',
            checks=(CheckHexList(ConnectIdGaming1HostChunk.LEN.CONN_FLAGS // 8), CheckByte(),), ),
        BitField(
            fid=FID.CONN_FLAGS_1,
            length=ConnectIdGaming1HostChunk.LEN.CONN_FLAGS,
            title='ConnFlags1',
            name='conn_flags_1',
            checks=(CheckHexList(ConnectIdGaming1HostChunk.LEN.CONN_FLAGS // 8), CheckByte(),), ),
        BitField(
            fid=FID.CONN_FLAGS_2,
            length=ConnectIdGaming1HostChunk.LEN.CONN_FLAGS,
            title='ConnFlags2',
            name='conn_flags_2',
            checks=(CheckHexList(ConnectIdGaming1HostChunk.LEN.CONN_FLAGS // 8), CheckByte(),), ),
    )

    def __init__(self, bcast_pending, host_index, alt_mode_0, alt_mode_1, alt_mode_2, conn_flags_0, conn_flags_1,
                 conn_flags_2, **kwargs):
        """
        :param bcast_pending: If true, then the user requested a new pairing (ble or ufy)
        :type bcast_pending: ``HexList`` or ``int`` or ``bool``
        :param host_index: The currently active host idx
        :type host_index: ``HexList``
        :param alt_mode_0: If true, the alternate mode is selected for host 0
        :type alt_mode_0: ``HexList`` or ``int`` or ``bool``
        :param alt_mode_1: If true, the alternate mode is selected for host 1
        :type alt_mode_1: ``HexList`` or ``int`` or ``bool``
        :param alt_mode_2: If true, the alternate mode is selected for host 2
        :type alt_mode_2: ``HexList`` or ``int`` or ``bool``
        :param conn_flags_0: Protocol Flags  for host 0
        :type conn_flags_0: ``HexList`` or ``int`` or ``GamingProtocolFlags``
        :param conn_flags_1: Protocol Flags for host 1
        :type conn_flags_1: ``HexList`` or ``int`` or ``GamingProtocolFlags``
        :param conn_flags_2: Protocol Flags for host 2
        :type conn_flags_2: ``HexList`` or ``int`` or ``GamingProtocolFlags``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(bcast_pending, host_index, alt_mode_0, alt_mode_1, conn_flags_0, conn_flags_1, **kwargs)

        # Parameters initialization
        self.alt_mode_2 = alt_mode_2
        self.conn_flags_2 = conn_flags_2
    # end def __init__
# end class ConnectIdGaming3HostsChunk
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
