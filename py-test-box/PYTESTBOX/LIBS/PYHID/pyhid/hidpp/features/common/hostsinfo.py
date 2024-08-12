#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.hostsinfo
:brief: HID++ 2.0 Hosts Info command interface definition
:author: Christophe Roquebert
:date: 2021/03/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfo(HidppMessage):
    """
    HostsInfo implementation class

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        24
    ============================  ==========
    """
    FEATURE_ID = 0x1815
    MAX_FUNCTION_INDEX = 8

    class STATUS:
        """
        Status definition
        """
        EMPTY_SLOT = 0
        PAIRED = 1
    # end class STATUS

    class BUSTYPE:
        """
        Bus type definition
        """
        UNDEFINED = 0
        EQUAD = 1
        USB = 2
        BT = 3
        BLE = 4
        BOLT = 5
    # end class BUSTYPE

    @unique
    class HostIndex(IntEnum):
        """
        The Host indexes
        """
        HOST_0 = 0
        HOST_1 = 1
        HOST_2 = 2
    # end class HostIndex

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict`` or ``int``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__

    class CapabilityMaskBitMap(BitFieldContainerMixin):
        """
           BitMap defining which sub-features is supported by the device.
           A bit is 1 if associated capability is available, else it has to be 0.

           Format:

           ============================  ==========
           Name                          Bit count
           ============================  ==========
           Reserved byte 0               3
           Set Os Version                1
           Delete Host                   1
           Move Host                     1
           Set Name                      1
           Get Name                      1
           Reserved byte 1               4
           BLE HD                        1
           BT HD                         1
           USB HD                        1
           eQuad HD                      1
           ============================  ==========
        """
        class FID:
            """
            Field identifiers
            """
            RESERVED_BYTE_0 = 0xFF
            SET_OS_VERSION = RESERVED_BYTE_0 - 1
            DELETE_HOST = SET_OS_VERSION - 1
            MOVE_HOST = DELETE_HOST - 1
            SET_NAME = MOVE_HOST - 1
            GET_NAME = SET_NAME - 1
            RESERVED_BYTE_1 = GET_NAME - 1
            BLE_HD = RESERVED_BYTE_1 - 1
            BT_HD = BLE_HD - 1
            USB_HD = BT_HD - 1
            EQUAD_HD = USB_HD - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            RESERVED_BYTE_0 = 3
            SET_OS_VERSION = 1
            DELETE_HOST = 1
            MOVE_HOST = 1
            SET_NAME = 1
            GET_NAME = 1
            RESERVED_BYTE_1 = 4
            BLE_HD = 1
            BT_HD = 1
            USB_HD = 1
            EQUAD_HD = 1
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            RESERVED_BYTE_0 = 0x00
            SET_OS_VERSION = 0
            DELETE_HOST = 0
            MOVE_HOST = 0
            SET_NAME = 0
            GET_NAME = 0
            RESERVED_BYTE_1 = 0x00
            BLE_HD = 0
            BT_HD = 0
            USB_HD = 0
            EQUAD_HD = 0
        # end class DEFAULT

        FIELDS = (
            BitField(FID.RESERVED_BYTE_0,
                     LEN.RESERVED_BYTE_0,
                     title='ReservedByte0',
                     name='reserved_byte_0',
                     default_value=DEFAULT.RESERVED_BYTE_0,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED_BYTE_0) - 1),)),
            BitField(FID.SET_OS_VERSION,
                     LEN.SET_OS_VERSION,
                     title='SetOsVersion',
                     name='set_os_version',
                     default_value=DEFAULT.SET_OS_VERSION,
                     checks=(CheckInt(0, pow(2, LEN.SET_OS_VERSION) - 1),)),
            BitField(FID.DELETE_HOST,
                     LEN.DELETE_HOST,
                     title='DeleteHost',
                     name='delete_host',
                     default_value=DEFAULT.DELETE_HOST,
                     checks=(CheckInt(0, pow(2, LEN.DELETE_HOST) - 1),)),
            BitField(FID.MOVE_HOST,
                     LEN.MOVE_HOST,
                     title='MoveHost',
                     name='move_host',
                     default_value=DEFAULT.MOVE_HOST,
                     checks=(CheckInt(0, pow(2, LEN.MOVE_HOST) - 1),)),
            BitField(FID.SET_NAME,
                     LEN.SET_NAME,
                     title='SetName',
                     name='set_name',
                     default_value=DEFAULT.SET_NAME,
                     checks=(CheckInt(0, pow(2, LEN.SET_NAME) - 1),)),
            BitField(FID.GET_NAME,
                     LEN.GET_NAME,
                     title='GetName',
                     name='get_name',
                     default_value=DEFAULT.GET_NAME,
                     checks=(CheckInt(0, pow(2, LEN.GET_NAME) - 1),)),
            BitField(FID.RESERVED_BYTE_1,
                     LEN.RESERVED_BYTE_1,
                     title='ReservedByte1',
                     name='reserved_byte_1',
                     default_value=DEFAULT.RESERVED_BYTE_1,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED_BYTE_1) - 1),)),
            BitField(FID.BLE_HD,
                     LEN.BLE_HD,
                     title='BleHd',
                     name='ble_hd',
                     default_value=DEFAULT.BLE_HD,
                     checks=(CheckInt(0, pow(2, LEN.BLE_HD) - 1),)),
            BitField(FID.BT_HD,
                     LEN.BT_HD,
                     title='BtHd',
                     name='bt_hd',
                     default_value=DEFAULT.BT_HD,
                     checks=(CheckInt(0, pow(2, LEN.BT_HD) - 1),)),
            BitField(FID.USB_HD,
                     LEN.USB_HD,
                     title='UsbHd',
                     name='usb_hd',
                     default_value=DEFAULT.USB_HD,
                     checks=(CheckInt(0, pow(2, LEN.USB_HD) - 1),)),
            BitField(FID.EQUAD_HD,
                     LEN.EQUAD_HD,
                     title='EquadHd',
                     name='equad_hd',
                     default_value=DEFAULT.EQUAD_HD,
                     checks=(CheckInt(0, pow(2, LEN.EQUAD_HD) - 1),)),
        )
    # end class CapabilityMaskBitMap
# end class HostsInfo


class HostsInfoModel(FeatureModel):
    """
    Hosts Info feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_FEATURE_INFO = 0
        GET_HOST_INFO = 1
        GET_HOST_DESCRIPTOR = 2
        GET_HOST_FRIENDLY_NAME = 3
        SET_HOST_FRIENDLY_NAME = 4
        MOVE_HOST = 5
        DELETE_HOST = 6
        GET_HOST_OS_VERSION = 7
        SET_HOST_OS_VERSION = 8
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Hosts Info feature data model
        """
        return {
            "feature_base": HostsInfo,
            "versions": {
                HostsInfoV1.VERSION: {
                    "main_cls": HostsInfoV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_FEATURE_INFO: {"request": GetFeatureInfoV1ToV2,
                                                         "response": GetFeatureInfoResponseV1ToV2},
                            cls.INDEX.GET_HOST_INFO: {"request": GetHostInfoV1ToV2,
                                                      "response": GetHostInfoResponseV1},
                            cls.INDEX.GET_HOST_DESCRIPTOR: {"request": GetHostDescriptorV1ToV2,
                                                            "response": GetHostDescriptorResponseV1},
                            cls.INDEX.GET_HOST_FRIENDLY_NAME: {"request": GetHostFriendlyNameV1ToV2,
                                                               "response": GetHostFriendlyNameResponseV1ToV2},
                            cls.INDEX.SET_HOST_FRIENDLY_NAME: {"request": SetHostFriendlyNameV1ToV2,
                                                               "response": SetHostFriendlyNameResponseV1ToV2},
                            cls.INDEX.GET_HOST_OS_VERSION: {"request": GetHostOsVersionV1ToV2,
                                                            "response": GetHostOsVersionResponseV1ToV2},
                            cls.INDEX.SET_HOST_OS_VERSION: {"request": SetHostOsVersionV1ToV2,
                                                            "response": SetHostOsVersionResponseV1ToV2},
                        },
                    },
                },
                HostsInfoV2.VERSION: {
                    "main_cls": HostsInfoV2,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_FEATURE_INFO: {"request": GetFeatureInfoV1ToV2,
                                                         "response": GetFeatureInfoResponseV1ToV2},
                            cls.INDEX.GET_HOST_INFO: {"request": GetHostInfoV1ToV2,
                                                      "response": GetHostInfoResponseV2},
                            cls.INDEX.GET_HOST_DESCRIPTOR: {"request": GetHostDescriptorV1ToV2,
                                                            "response": GetHostDescriptorResponseV2},
                            cls.INDEX.GET_HOST_FRIENDLY_NAME: {"request": GetHostFriendlyNameV1ToV2,
                                                               "response": GetHostFriendlyNameResponseV1ToV2},
                            cls.INDEX.SET_HOST_FRIENDLY_NAME: {"request": SetHostFriendlyNameV1ToV2,
                                                               "response": SetHostFriendlyNameResponseV1ToV2},
                            cls.INDEX.GET_HOST_OS_VERSION: {"request": GetHostOsVersionV1ToV2,
                                                            "response": GetHostOsVersionResponseV1ToV2},
                            cls.INDEX.SET_HOST_OS_VERSION: {"request": SetHostOsVersionV1ToV2,
                                                            "response": SetHostOsVersionResponseV1ToV2},
                        },
                    },
                },
            }
        }
    # end def get_data_model
# end class HostsInfoModel


class HostsInfoFactory(FeatureFactory):
    """
    Hosts Info factory creates a Hosts Info object from a given version
    """
    @staticmethod
    def create(version):
        """
        Hosts Info object creation from version number

        :param version: Hosts Info feature version
        :type version: ``int``
        :return: Hosts Info object
        :rtype: ``HostsInfoInterface``
        """
        return HostsInfoModel.get_main_cls(version)()
    # end def create
# end class HostsInfoFactory


class HostsInfoInterface(FeatureInterface, ABC):
    """
    Interface to Hosts Info feature

    Defines required interfaces for Hosts Info classes
    """
    def __init__(self):
        # Requests
        self.get_feature_info_cls = None
        self.get_host_info_cls = None
        self.get_host_descriptor_cls = None
        self.get_host_friendly_name_cls = None
        self.set_host_friendly_name_cls = None
        self.get_host_os_version_cls = None
        self.set_host_os_version_cls = None

        # Responses
        self.get_feature_info_response_cls = None
        self.get_host_info_response_cls = None
        self.get_host_descriptor_response_cls = None
        self.get_host_friendly_name_response_cls = None
        self.set_host_friendly_name_response_cls = None
        self.get_host_os_version_response_cls = None
        self.set_host_os_version_response_cls = None
    # end def __init__
# end class HostsInfoInterface


class HostsInfoV1(HostsInfoInterface):
    """
    HostsInfo
    This feature provides host information on devices with multihost capabilities

    [0] getFeatureInfo() -> capabilityMask, numHosts, currentHost
    [1] getHostInfo(hostIndex) -> hostIndex, status, busType, numPages, nameLen, nameMaxLen
    [2] getHostDescriptor(hostIndex, pageIndex) -> hostDescriptor
    [3] getHostFriendlyName(hostIndex, byteIndex) -> string
    [4] setHostFriendlyName(hostIndex, byteIndex, nameChunk) -> hostIndex, nameLen
    [5] moveHost(hostIndex, newIndex) -> void
    [6] deleteHost(hostIndex) -> void
    [7] getHostOsVersion(hostIndex) -> hostIndex, OsType, OsVersion, OsRevision, OsBuild
    [8] setHostOsVersion(hostIndex, OsType, OsVersion, OsRevision, OsBuild) -> void
    """
    VERSION = 1

    def __init__(self):
        """
        See :any:`HostsInfo.__init__`
        """
        super().__init__()
        self.get_feature_info_cls = HostsInfoModel.get_request_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_FEATURE_INFO)
        self.get_host_info_cls = HostsInfoModel.get_request_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_INFO)
        self.get_host_descriptor_cls = HostsInfoModel.get_request_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_DESCRIPTOR)
        self.get_host_friendly_name_cls = HostsInfoModel.get_request_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_FRIENDLY_NAME)
        self.set_host_friendly_name_cls = HostsInfoModel.get_request_cls(
            self.VERSION, HostsInfoModel.INDEX.SET_HOST_FRIENDLY_NAME)
        self.get_host_os_version_cls = HostsInfoModel.get_request_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_OS_VERSION)
        self.set_host_os_version_cls = HostsInfoModel.get_request_cls(
            self.VERSION, HostsInfoModel.INDEX.SET_HOST_OS_VERSION)

        self.get_feature_info_response_cls = HostsInfoModel.get_response_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_FEATURE_INFO)
        self.get_host_info_response_cls = HostsInfoModel.get_response_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_INFO)
        self.get_host_descriptor_response_cls = HostsInfoModel.get_response_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_DESCRIPTOR)
        self.get_host_friendly_name_response_cls = HostsInfoModel.get_response_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_FRIENDLY_NAME)
        self.set_host_friendly_name_response_cls = HostsInfoModel.get_response_cls(
            self.VERSION, HostsInfoModel.INDEX.SET_HOST_FRIENDLY_NAME)
        self.get_host_os_version_response_cls = HostsInfoModel.get_response_cls(
            self.VERSION, HostsInfoModel.INDEX.GET_HOST_OS_VERSION)
        self.set_host_os_version_response_cls = HostsInfoModel.get_response_cls(
            self.VERSION, HostsInfoModel.INDEX.SET_HOST_OS_VERSION)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`HostsInfoInterface.get_max_function_index`
        """
        return HostsInfoModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class HostsInfoV1


class HostsInfoV2(HostsInfoV1):
    """
    HostsInfo
    Version 2: Add BLE Pro busType.
    """
    VERSION = 2
# end class HostsInfoV2


class GetFeatureInfoV1ToV2(HostsInfo):
    """
        HostsInfo GetFeatureInfo implementation class for version 1 & 2

        This function allows to get the number of hosts in the registry and the currently active host index.
        It also returns a capability_mask for the device.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        Padding                       24
        ============================  ==========
    """
    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        PADDING = HostsInfo.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=HostsInfo.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetFeatureInfoResponseV1ToV2.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetFeatureInfoV1ToV2


class GetFeatureInfoResponseV1ToV2(HostsInfo):
    """
        HostsInfo GetFeatureInfo Response implementation class for version 1 & 2

        This function allows to get the number of hosts in the registry and the currently active host index.
        It also returns a capability_mask for the device.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        CapabilityMask                16
        NumHosts                      8
        CurrentHost                   8
        Padding                       96
        ============================  ==========
    """
    REQUEST_LIST = (GetFeatureInfoV1ToV2,)
    VERSION = (1, 2,)
    FUNCTION_INDEX = 0
    MSG_TYPE = TYPE.RESPONSE

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        CAPABILITY_MASK = HostsInfo.FID.SOFTWARE_ID - 1
        NUM_HOSTS = CAPABILITY_MASK - 1
        CURRENT_HOST = NUM_HOSTS - 1
        PADDING = CURRENT_HOST - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        CAPABILITY_MASK = 0x10
        NUM_HOSTS = 0x08
        CURRENT_HOST = 0x08
        PADDING = 0x60
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.CAPABILITY_MASK,
                 length=LEN.CAPABILITY_MASK,
                 title='CapabilityMask',
                 name='capability_mask',
                 checks=(CheckHexList(LEN.CAPABILITY_MASK // 8), ), ),
        BitField(fid=FID.NUM_HOSTS,
                 length=LEN.NUM_HOSTS,
                 title='NumHosts',
                 name='num_hosts',
                 checks=(CheckHexList(LEN.NUM_HOSTS // 8), CheckByte(),), ),
        BitField(fid=FID.CURRENT_HOST,
                 length=LEN.CURRENT_HOST,
                 title='CurrentHost',
                 name='current_host',
                 checks=(CheckHexList(LEN.CURRENT_HOST // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, set_os_version=False, set_name=False, get_name=False,
                 ble_hd=False, num_hosts=0, current_host=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param set_os_version: getHostOsVersion() and setHostOsVersion() supported by the device.
        :type set_os_version: ``int`` or ``bool``
        :param set_name: setHostFriendlyName() command is supported.
        :type set_name: ``int`` or ``bool``
        :param get_name: getHostFriendlyName() command is supported.
        :type get_name: ``int`` or ``bool``
        :param ble_hd: getHostDescriptor() can return a BLE descriptor.
        :type ble_hd: ``int`` or ``bool``
        :param num_hosts: The number of hosts / channels, including paired and unpaired.
        :type num_hosts: ``int``
        :param current_host: The current host channel index [0..numHosts - 1].
        :type current_host: ``int``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=self.DEFAULT.REPORT_ID_LONG, functionIndex=self.FUNCTION_INDEX, **kwargs)
        self.capability_mask = self.CapabilityMaskBitMap(set_os_version=set_os_version, set_name=set_name,
                                                         get_name=get_name, ble_hd=ble_hd)
        self.num_hosts = num_hosts
        self.current_host = current_host
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetFeatureInfoResponseV1ToV2``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capability_mask = cls.CapabilityMaskBitMap.fromHexList(
            inner_field_container_mixin.capability_mask)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetFeatureInfoResponseV1ToV2


class GetHostInfoV1ToV2(HostsInfo):
    """
        HostsInfo GetHostInfo implementation class for version 1 & 2

        This function allows to get a particular host basic information.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        Padding                       16
        ============================  ==========
    """
    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        PADDING = HOST_INDEX - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetHostInfoResponseV1.FUNCTION_INDEX,
                         **kwargs)
        self.host_index = host_index
    # end def __init__
# end class GetHostInfoV1ToV2


class GetHostInfoResponseV1(HostsInfo):
    """
        HostsInfo GetHostInfoResponse implementation class for version 1

        This function allows to get a particular host basic information.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        Status                        8
        BusType                       8
        NumPages                      8
        NameLen                       8
        NameMaxLen                    8
        Padding                       80
        ============================  ==========
    """
    REQUEST_LIST = (GetHostInfoV1ToV2,)
    VERSION = (1, )
    FUNCTION_INDEX = 1
    MSG_TYPE = TYPE.RESPONSE

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        STATUS = HOST_INDEX - 1
        BUS_TYPE = STATUS - 1
        NUM_PAGES = BUS_TYPE - 1
        NAME_LEN = NUM_PAGES - 1
        NAME_MAX_LEN = NAME_LEN - 1
        PADDING = NAME_MAX_LEN - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        STATUS = 0x08
        BUS_TYPE = 0x08
        NUM_PAGES = 0x08
        NAME_LEN = 0x08
        NAME_MAX_LEN = 0x08
        PADDING = 0x50
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.STATUS,
                 length=LEN.STATUS,
                 title='Status',
                 name='status',
                 checks=(CheckHexList(LEN.STATUS // 8), CheckByte(),), ),
        BitField(fid=FID.BUS_TYPE,
                 length=LEN.BUS_TYPE,
                 title='BusType',
                 name='bus_type',
                 checks=(CheckHexList(LEN.BUS_TYPE // 8), CheckByte(),), ),
        BitField(fid=FID.NUM_PAGES,
                 length=LEN.NUM_PAGES,
                 title='NumPages',
                 name='num_pages',
                 checks=(CheckHexList(LEN.NUM_PAGES // 8), CheckByte(),), ),
        BitField(fid=FID.NAME_LEN,
                 length=LEN.NAME_LEN,
                 title='NameLen',
                 name='name_len',
                 checks=(CheckHexList(LEN.NAME_LEN // 8), CheckByte(),), ),
        BitField(fid=FID.NAME_MAX_LEN,
                 length=LEN.NAME_MAX_LEN,
                 title='NameMaxLen',
                 name='name_max_len',
                 checks=(CheckHexList(LEN.NAME_MAX_LEN // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, host_index=0, status=0, bus_type=0, num_pages=0, name_len=0,
                 name_max_len=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: host index.
        :type host_index: ``int``
        :param status: Pairing status (0=empty slot, 1=paired)
        :type status: ``int``
        :param bus_type: The host bus type can be:
                            0 - Undefined: the Host entry is unused.
                            1 - eQuad
                            2 - USB
                            3 - BT
                            4 - BLE
        :type bus_type: ``int``
        :param num_pages: Number of Host Descriptor pages available for the host, depending on busType:
                            Undefined: always 0.
                            eQuad: always 0.
                            USB: Reserved for futur use.
                            BT: 2 pages with data collected from Device ID Service Record.
                            BLE: 2 or more pages with data collected from GATT, GAP and DIS services.
        :type num_pages: ``int``
        :param name_len: The byte length of the host friendly name (without null terminator).
        :type name_len: ``int``
        :param name_max_len: The maximum byte length of the host friendly name (without null terminator).
        :type name_max_len: ``int``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=self.DEFAULT.REPORT_ID_LONG, functionIndex=self.FUNCTION_INDEX, **kwargs)
        self.host_index = host_index
        self.status = status
        self.bus_type = bus_type
        self.num_pages = num_pages
        self.name_len = name_len
        self.name_max_len = name_max_len
    # end def __init__
# end class GetHostInfoResponseV1


class GetHostInfoResponseV2(GetHostInfoResponseV1):
    """
        HostsInfo GetHostInfoResponse implementation class for version 2

        Add BLE Pro busType.
    """
    VERSION = (2,)
# end class GetHostInfoResponseV2


class GetHostDescriptorV1ToV2(HostsInfo):
    """
        HostsInfo GetHostDescriptor implementation class for version 1 & 2

        This function allows to get a host host descriptor page.
        The host descriptor is the collection of data describing the host profile (VendorID, Version),
        collected from its transport channel and (BT, USB..) and depending on it.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        PageIndex                     8
        Padding                       8
        ============================  ==========
    """
    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        PAGE_INDEX = HOST_INDEX - 1
        PADDING = PAGE_INDEX - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        PAGE_INDEX = 0x08
        PADDING = 0x08
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.PAGE_INDEX,
                 length=LEN.PAGE_INDEX,
                 title='PageIndex',
                 name='page_index',
                 checks=(CheckHexList(LEN.PAGE_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, page_index=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param page_index: Index of the host descriptor page to query (0..numPages returned by getHostInfo()).
        :type page_index: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetHostDescriptorResponseV1.FUNCTION_INDEX,
                         **kwargs)
        self.host_index = host_index
        self.page_index = page_index
    # end def __init__
# end class GetHostDescriptorV1ToV2


class GetHostDescriptorResponseV1(HostsInfo):
    """
        HostsInfo GetHostDescriptor Response implementation class for version 1

        This function allows to get a host host descriptor page.
        The host descriptor is the collection of data describing the host profile (VendorID, Version),
        collected from its transport channel and (BT, USB..) and depending on it.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        BusType                       3
        PageIndex                     5
        HostDescriptor                112
        ============================  ==========
    """
    REQUEST_LIST = (GetHostDescriptorV1ToV2,)
    VERSION = (1,)
    FUNCTION_INDEX = 2
    MSG_TYPE = TYPE.RESPONSE

    FULL_DESCRIPTOR_DATA = None

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        BUS_TYPE = HOST_INDEX - 1
        PAGE_INDEX = BUS_TYPE - 1
        HOST_DESCRIPTOR = PAGE_INDEX - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        BUS_TYPE = 0x03
        PAGE_INDEX = 0x05
        HOST_DESCRIPTOR = 0x70
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.BUS_TYPE,
                 length=LEN.BUS_TYPE,
                 title='BusType',
                 name='bus_type',
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BUS_TYPE) - 1),), ),
        BitField(fid=FID.PAGE_INDEX,
                 length=LEN.PAGE_INDEX,
                 title='PageIndex',
                 name='page_index',
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PAGE_INDEX) - 1),), ),
        BitField(fid=FID.HOST_DESCRIPTOR,
                 length=LEN.HOST_DESCRIPTOR,
                 title='HostDescriptor',
                 name='host_descriptor',
                 checks=(CheckHexList(LEN.HOST_DESCRIPTOR // 8),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, bus_type=0, page_index=0, host_descriptor=None,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param bus_type: RF protocol definition
        :type bus_type: ``int`` or ``HexList``
        :param page_index: Index of the host descriptor page to query (0..numPages returned by getHostInfo()).
        :type page_index: ``int`` or ``HexList``
        :param host_descriptor: BLE Descriptor pages
        :type host_descriptor: ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
        self.host_index = host_index
        self.bus_type = bus_type
        self.page_index = page_index
        if host_descriptor is not None:
            self.host_descriptor = host_descriptor
        # end if
    # end def __init__
# end class GetHostDescriptorResponseV1


class GetHostDescriptorResponseV2(GetHostDescriptorResponseV1):
    """
        HostsInfo GetHostDescriptorResponse implementation class for version 2

        Add BLE Pro busType.
    """
    VERSION = (2,)
# end class GetHostDescriptorResponseV2


class BLEDescriptorPage0(BitFieldContainerMixin):
    """
    This class defines the format of BT & BLE Descriptor Page 0.

    Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Valid Address                 1
        Bluetooth Address             48
        Padding                       56
        ============================  ==========
    """

    class FID:
        """
        Field Identifiers
        """
        RESERVED = 0xFF
        VALID_ADDRESS = RESERVED - 1
        BLUETOOTH_ADDRESS = VALID_ADDRESS - 1
        PADDING = BLUETOOTH_ADDRESS - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        RESERVED = 0x07
        VALID_ADDRESS = 0x01
        BLUETOOTH_ADDRESS = 0x30
        PADDING = 0x38
    # end class LEN

    class DEFAULT:
        """
        Field default value
        """
        RESERVED = 0x00
    # end class DEFAULT

    FIELDS = (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 default_value=DEFAULT.RESERVED,
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),), ),
        BitField(FID.VALID_ADDRESS,
                 LEN.VALID_ADDRESS,
                 title='ValidAddress',
                 name='valid_address',
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.VALID_ADDRESS) - 1),), ),
        BitField(FID.BLUETOOTH_ADDRESS,
                 LEN.BLUETOOTH_ADDRESS,
                 title='BluetoothAddress',
                 name='bluetooth_address',
                 checks=(CheckHexList(LEN.BLUETOOTH_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BLUETOOTH_ADDRESS) - 1),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),), ),
    )
# end class BLEDescriptorPage0


class BLEDescriptorPage1Header(BitFieldContainerMixin):
    """
    This class defines the format of BLE Descriptor Page  1 header.

    Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Number of uuids               8
        uuids total byte size         16
        uuid 0                        16
        size 0                        8
        ============================  ==========
    """

    class FID:
        """
        Field Identifiers
        """
        NUMBER_OF_UUIDS = 0xFF
        UUIDS_TOTAL_BYTE_SIZE = NUMBER_OF_UUIDS - 1
        UUID_0 = UUIDS_TOTAL_BYTE_SIZE - 1
        SIZE_0 = UUID_0 - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        NUMBER_OF_UUIDS = 0x08
        UUIDS_TOTAL_BYTE_SIZE = 0x10
        UUID_0 = 0x10
        SIZE_0 = 0x08
    # end class LEN

    FIELDS = (
        BitField(FID.NUMBER_OF_UUIDS,
                 LEN.NUMBER_OF_UUIDS,
                 title='NumberOfUuids',
                 name='number_of_uuids',
                 checks=(CheckHexList(LEN.NUMBER_OF_UUIDS // 8), CheckByte(),), ),
        BitField(FID.UUIDS_TOTAL_BYTE_SIZE,
                 LEN.UUIDS_TOTAL_BYTE_SIZE,
                 title='UuidsTotalByteSize',
                 name='uuids_total_byte_size',
                 checks=(CheckHexList(LEN.UUIDS_TOTAL_BYTE_SIZE // 8),), ),
        BitField(FID.UUID_0,
                 LEN.UUID_0,
                 title='Uuid0',
                 name='uuid_0',
                 checks=(CheckHexList(LEN.UUID_0 // 8),), ),
        BitField(FID.SIZE_0,
                 LEN.SIZE_0,
                 title='Size0',
                 name='size_0',
                 checks=(CheckHexList(LEN.SIZE_0 // 8), CheckByte(),), ),
    )
# end class BLEDescriptorPage1Header


class BLEDescriptorPage1SingleUuid(BLEDescriptorPage1Header):
    """
    This class defines the format of BLE Descriptor Page 1 with a single Uuid.

    Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Number of uuids               8
        uuids total byte size         16
        uuid 0                        16
        size 0                        8
        data 0                        size 0
        ============================  ==========
    """

    class FID(BLEDescriptorPage1Header.FID):
        """
        Field Identifiers
        """
        DATA_0 = BLEDescriptorPage1Header.FID.SIZE_0 - 1
    # end class FID

    class LEN(BLEDescriptorPage1Header.LEN):
        """
        Field Lengths in bits
        """
        DATA_0 = 0x00
    # end class LEN

    FIELDS = BLEDescriptorPage1Header.FIELDS + (
        BitField(FID.DATA_0,
                 LEN.DATA_0,
                 title='Data0',
                 name='data_0',),
    )
# end class BLEDescriptorPage1SingleUuid


class BLEDescriptorPage1DualUuid(BLEDescriptorPage1SingleUuid):
    """
    This class defines the format of BLE Descriptor Page 1 with dual Uuads.

    Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Number of uuids               8
        uuids total byte size         16
        uuid 0                        16
        size 0                        8
        data 0                        size 0
        uuid 1                        16
        size 1                        8
        data 1                        size 1
        ============================  ==========
    """

    class FID(BLEDescriptorPage1SingleUuid.FID):
        """
        Field Identifiers
        """
        UUID_1 = BLEDescriptorPage1SingleUuid.FID.DATA_0 - 1
        SIZE_1 = UUID_1 - 1
        DATA_1 = SIZE_1 - 1
    # end class FID

    class LEN(BLEDescriptorPage1SingleUuid.LEN):
        """
        Field Lengths in bits
        """
        UUID_1 = 0x10
        SIZE_1 = 0x08
        DATA_1 = 0x00
    # end class LEN

    FIELDS = BLEDescriptorPage1SingleUuid.FIELDS + (
        BitField(FID.UUID_1,
                 LEN.UUID_1,
                 title='Uuid1',
                 name='uuid_1',
                 checks=(CheckHexList(max_length=LEN.UUID_1 // 8),)),
        BitField(FID.SIZE_1,
                 LEN.SIZE_1,
                 title='Size1',
                 name='size_1',
                 checks=(CheckHexList(max_length=LEN.SIZE_1 // 8), CheckByte(),), ),
        BitField(FID.DATA_1,
                 LEN.DATA_1,
                 title='Data1',
                 name='data_1',),
    )
# end class BLEDescriptorPage1DualUuid


class BLEDescriptorPage1TripleUuid(BLEDescriptorPage1DualUuid):
    """
    This class defines the format of BLE Descriptor Page 1 with triple Uuids.

    Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Number of uuids               8
        uuids total byte size         16
        uuid 0                        16
        size 0                        8
        data 0                        size 0
        uuid 1                        16
        size 1                        8
        data 1                        size 1
        uuid 2                        16
        size 2                        8
        data 2                        size 2
        ============================  ==========
    """

    class FID(BLEDescriptorPage1DualUuid.FID):
        """
        Field Identifiers
        """
        UUID_2 = BLEDescriptorPage1DualUuid.FID.DATA_1 - 1
        SIZE_2 = UUID_2 - 1
        DATA_2 = SIZE_2 - 1
    # end class FID

    class LEN(BLEDescriptorPage1DualUuid.LEN):
        """
        Field Lengths in bits
        """
        UUID_2 = 0x10
        SIZE_2 = 0x08
        DATA_2 = 0x00
    # end class LEN

    FIELDS = BLEDescriptorPage1DualUuid.FIELDS + (
        BitField(FID.UUID_2,
                 LEN.UUID_2,
                 title='Uuid2',
                 name='uuid_2',
                 checks=(CheckHexList(max_length=LEN.UUID_2 // 8, ),)),
        BitField(FID.SIZE_2,
                 LEN.SIZE_2,
                 title='Size2',
                 name='size_2',
                 checks=(CheckHexList(max_length=LEN.SIZE_2 // 8, ), CheckByte(),), ),
        BitField(FID.DATA_2,
                 LEN.DATA_2,
                 title='Data2',
                 name='data_2',),
    )
# end class BLEDescriptorPage1TripleUuid


class GetHostFriendlyNameV1ToV2(HostsInfo):
    """
        HostsInfo GetHostFriendlyName implementation class for version 1 & 2

        This function allows to get a Host Friendly Name chunk.
        Can be null if the host channel is not paired.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        ByteIndex                     8
        Padding                       8
        ============================  ==========
    """
    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        BYTE_INDEX = HOST_INDEX - 1
        PADDING = BYTE_INDEX - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        BYTE_INDEX = 0x08
        PADDING = 0x08
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.BYTE_INDEX,
                 length=LEN.BYTE_INDEX,
                 title='ByteIndex',
                 name='byte_index',
                 checks=(CheckHexList(LEN.BYTE_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, byte_index=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param byte_index: Index of the first host name byte to copy (0..strlen-1).
        :type byte_index: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetHostFriendlyNameResponseV1ToV2.FUNCTION_INDEX,
                         **kwargs)
        self.host_index = host_index
        self.byte_index = byte_index
    # end def __init__
# end class GetHostFriendlyNameV1ToV2


class GetHostFriendlyNameResponseV1ToV2(HostsInfo):
    """
        HostsInfo GetFriendlyName Response implementation class for version 1 & 2

        This function allows to get a Host Friendly Name chunk.
        Can be null if the host channel is not paired.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        ByteIndex                     8
        NameChunk                     112
        ============================  ==========
    """
    REQUEST_LIST = (GetHostFriendlyNameV1ToV2,)
    VERSION = (1, 2, )
    FUNCTION_INDEX = 3
    MSG_TYPE = TYPE.RESPONSE

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        BYTE_INDEX = HOST_INDEX - 1
        NAME_CHUNK = BYTE_INDEX - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        BYTE_INDEX = 0x08
        NAME_CHUNK = 0x70
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.BYTE_INDEX,
                 length=LEN.BYTE_INDEX,
                 title='ByteIndex',
                 name='byte_index',
                 checks=(CheckHexList(LEN.BYTE_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.NAME_CHUNK,
                 length=LEN.NAME_CHUNK,
                 title='NameChunk',
                 name='name_chunk',
                 checks=(CheckHexList(LEN.NAME_CHUNK // 8),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, byte_index=0, name_chunk=None, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param byte_index: Index of the first host name byte to copy (0..strlen-1).
        :type byte_index: ``int`` or ``HexList``
        :param name_chunk: The host name chunk, copied from full host name byteIndex?th byte,
                            padded with null bytes '\0' if the copied string is shorter than the payload size
                            (HPPLong: 16 bytes).
        :type name_chunk: ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
        self.host_index = host_index
        self.byte_index = byte_index
        self.name_chunk = name_chunk
        # end if
    # end def __init__
# end class GetHostFriendlyNameResponseV1ToV2


class SetHostFriendlyNameV1ToV2(HostsInfo):
    """
        HostsInfo SetHostFriendlyName implementation class for version 1 & 2

        Write a host name chunk, starting at byteIndex.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        ByteIndex                     8
        NameChunk                     112
        ============================  ==========
    """
    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        BYTE_INDEX = HOST_INDEX - 1
        NAME_CHUNK = BYTE_INDEX - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        BYTE_INDEX = 0x08
        NAME_CHUNK = 0x70
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.BYTE_INDEX,
                 length=LEN.BYTE_INDEX,
                 title='ByteIndex',
                 name='byte_index',
                 checks=(CheckHexList(LEN.BYTE_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.NAME_CHUNK,
                 length=LEN.NAME_CHUNK,
                 title='NameChunk',
                 name='name_chunk',
                 checks=(CheckHexList(LEN.NAME_CHUNK // 8),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, byte_index=0, name_chunk=None, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param byte_index: Index of the first host name byte to copy (0..strlen-1).
        :type byte_index: ``int`` or ``HexList``
        :param name_chunk: The host name chunk to write, padded with null bytes '\0'
                            if it is shorter than the payload size (HPPLong: 16 bytes).
        :type name_chunk: ``HexList`` or ``str``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=SetHostFriendlyNameResponseV1ToV2.FUNCTION_INDEX,
                         **kwargs)

        # Request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.host_index = host_index
        self.byte_index = byte_index
        name_chunk = HexList.fromString(name_chunk) if isinstance(name_chunk, str) else name_chunk
        name_chunk.addPadding(SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8, fromLeft=False)
        self.name_chunk = name_chunk
    # end def __init__
# end class SetHostFriendlyNameV1ToV2


class SetHostFriendlyNameResponseV1ToV2(HostsInfo):
    """
        HostsInfo SetFriendlyName Response implementation class for version 1 & 2

        Write a host name chunk, starting at byteIndex.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        NameLen                       8
        Padding                       112
        ============================  ==========
    """
    REQUEST_LIST = (SetHostFriendlyNameV1ToV2,)
    VERSION = (1, 2, )
    FUNCTION_INDEX = 4
    MSG_TYPE = TYPE.RESPONSE

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        NAME_LEN = HOST_INDEX - 1
        PADDING = NAME_LEN - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        NAME_LEN = 0x08
        PADDING = 0x70
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.NAME_LEN,
                 length=LEN.NAME_LEN,
                 title='NameLen',
                 name='name_len',
                 checks=(CheckHexList(LEN.NAME_LEN // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, name_len=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param name_len: Resulting name len.
        :type name_len: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict`` or ``int``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
        self.host_index = host_index
        self.name_len = name_len
        # end if
    # end def __init__
# end class SetHostFriendlyNameResponseV1ToV2


class GetHostOsVersionV1ToV2(HostsInfo):
    """
        HostsInfo GetHostOsVersion implementation class for version 1 & 2

        This function allows to read Host OS Type and Version, saved previously by SW. Can be null.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        Padding                       16
        ============================  ==========
    """
    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        PADDING = HOST_INDEX - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Channel / host index [0..numHosts-1]. 0xFF = Current Host.
        :type host_index: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict`` or ``int``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetHostOsVersionResponseV1ToV2.FUNCTION_INDEX,
                         **kwargs)
        self.host_index = host_index
    # end def __init__
# end class GetHostOsVersionV1ToV2


class GetHostOsVersionResponseV1ToV2(HostsInfo):
    """
        HostsInfo GetHostOsVersionResponse implementation class for version 1 & 2

        This function allows to read Host OS Type and Version, saved previously by SW. Can be null.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        OsType                        8
        OsVersion                     8
        OsRevision                    16
        OsBuild                       16
        Padding                       72
        ============================  ==========
    """
    REQUEST_LIST = (GetHostOsVersionV1ToV2,)
    VERSION = (1, 2, )
    FUNCTION_INDEX = HostsInfoModel.INDEX.GET_HOST_OS_VERSION
    MSG_TYPE = TYPE.RESPONSE

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        OS_TYPE = HOST_INDEX - 1
        OS_VERSION = OS_TYPE - 1
        OS_REVISION = OS_VERSION - 1
        OS_BUILD = OS_REVISION - 1
        PADDING = OS_BUILD - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        OS_TYPE = 0x08
        OS_VERSION = 0x08
        OS_REVISION = 0x10
        OS_BUILD = 0x10
        PADDING = 0x48
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.OS_TYPE,
                 length=LEN.OS_TYPE,
                 title='OsType',
                 name='os_type',
                 checks=(CheckHexList(LEN.OS_TYPE // 8), CheckByte(),), ),
        BitField(fid=FID.OS_VERSION,
                 length=LEN.OS_VERSION,
                 title='OsVersion',
                 name='os_version',
                 checks=(CheckHexList(LEN.OS_VERSION // 8), CheckByte(),), ),
        BitField(fid=FID.OS_REVISION,
                 length=LEN.OS_REVISION,
                 title='OsRevision',
                 name='os_revision',
                 checks=(CheckHexList(LEN.OS_REVISION // 8),
                         CheckInt(0, pow(2, LEN.OS_REVISION) - 1),), ),
        BitField(fid=FID.OS_BUILD,
                 length=LEN.OS_BUILD,
                 title='OsBuild',
                 name='os_build',
                 checks=(CheckHexList(LEN.OS_BUILD // 8),
                         CheckInt(0, pow(2, LEN.OS_BUILD) - 1),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, host_index=0, os_type=0, os_version=0, os_revision=0, os_build=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: host index.
        :type host_index: ``int``
        :param os_type: Enumerated values (defined in the same order as x4531 Platform Descriptor OS bit field):
                        0: Unknown
                        1: Windows
                        2: WinEmb
                        3: Linux
                        4: Chrome
                        5: Android
                        6: MacOS
                        7: IOS
        :type os_type: ``int``
        :param os_version: Os 1st Version number.
        :type os_version: ``int``
        :param os_revision: Os 2nd Version number [Big Endian].
        :type os_revision: ``int`` or ``HexList``
        :param os_build: Os 3rd Version number [Big Endian].
        :type os_build: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict`` or ``int``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=self.DEFAULT.REPORT_ID_LONG, functionIndex=self.FUNCTION_INDEX, **kwargs)
        self.host_index = host_index
        self.os_type = os_type
        self.os_version = os_version
        self.os_revision = os_revision
        self.os_build = os_build
    # end def __init__
# end class GetHostOsVersionResponseV1ToV2


class SetHostOsVersionV1ToV2(HostsInfo):
    """
        HostsInfo SetHostOsVersion implementation class for version 1 & 2

        This function allows to read Host OS Type and Version, saved previously by SW. Can be null.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        HostIndex                     8
        OsType                        8
        OsVersion                     8
        OsRevision                    16
        OsBuild                       16
        Padding                       72
        ============================  ==========
    """

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        HOST_INDEX = HostsInfo.FID.SOFTWARE_ID - 1
        OS_TYPE = HOST_INDEX - 1
        OS_VERSION = OS_TYPE - 1
        OS_REVISION = OS_VERSION - 1
        OS_BUILD = OS_REVISION - 1
        PADDING = OS_BUILD - 1

    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        HOST_INDEX = 0x08
        OS_TYPE = 0x08
        OS_VERSION = 0x08
        OS_REVISION = 0x10
        OS_BUILD = 0x10
        PADDING = 0x48
    # end class LEN

    class TYPE:
        """
        OS type enumerated values (defined in the same order as x4531 Platform Descriptor OS bit field)
        """
        UNKNOWN = 0x00
        WINDOWS = 0x01
        WIN_EMB = 0x02
        LINUX = 0x03
        CHROME = 0x04
        ANDROID = 0x05
        MACOS = 0x06
        IOS = 0x07
        RESERVED = 0x08
    # end class TYPE

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.HOST_INDEX,
                 length=LEN.HOST_INDEX,
                 title='HostIndex',
                 name='host_index',
                 checks=(CheckHexList(LEN.HOST_INDEX // 8), CheckByte(),), ),
        BitField(fid=FID.OS_TYPE,
                 length=LEN.OS_TYPE,
                 title='OsType',
                 name='os_type',
                 checks=(CheckHexList(LEN.OS_TYPE // 8), CheckByte(),), ),
        BitField(fid=FID.OS_VERSION,
                 length=LEN.OS_VERSION,
                 title='OsVersion',
                 name='os_version',
                 checks=(CheckHexList(LEN.OS_VERSION // 8), CheckByte(),), ),
        BitField(fid=FID.OS_REVISION,
                 length=LEN.OS_REVISION,
                 title='OsRevision',
                 name='os_revision',
                 checks=(CheckHexList(LEN.OS_REVISION // 8),
                         CheckInt(0, pow(2, LEN.OS_REVISION) - 1), ), ),
        BitField(fid=FID.OS_BUILD,
                 length=LEN.OS_BUILD,
                 title='OsBuild',
                 name='os_build',
                 checks=(CheckHexList(LEN.OS_BUILD // 8),
                         CheckInt(0, pow(2, LEN.OS_BUILD) - 1), ), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, device_index, feature_index, host_index=0, os_type=0, os_version=0, os_revision=0, os_build=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: host index.
        :type host_index: ``int``
        :param os_type: Enumerated values (defined in the same order as x4531 Platform Descriptor OS bit field):
                        0: Unknown
                        1: Windows
                        2: WinEmb
                        3: Linux
                        4: Chrome
                        5: Android
                        6: MacOS
                        7: IOS
        :type os_type: ``int``
        :param os_version: Os 1st Version number.
        :type os_version: ``int``
        :param os_revision: Os 2nd Version number [Big Endian].
        :type os_revision: ``int`` or ``HexList``
        :param os_build: Os 3rd Version number [Big Endian].
        :type os_build: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict`` or ``int``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=SetHostOsVersionResponseV1ToV2.FUNCTION_INDEX,
                         **kwargs)

        # Request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.host_index = host_index
        self.os_type = os_type
        self.os_version = os_version
        self.os_revision = os_revision
        self.os_build = os_build
    # end def __init__
# end class SetHostOsVersionV1ToV2


class SetHostOsVersionResponseV1ToV2(HostsInfo):
    """
        HostsInfo SetHostOsVersionResponse implementation class for version 1 & 2

        This function allows to read Host OS Type and Version, saved previously by SW. Can be null.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        Padding                       128
        ============================  ==========
    """
    REQUEST_LIST = (SetHostOsVersionV1ToV2,)
    VERSION = (1, 2, )
    FUNCTION_INDEX = HostsInfoModel.INDEX.SET_HOST_OS_VERSION
    MSG_TYPE = TYPE.RESPONSE

    class FID(HostsInfo.FID):
        """
        Field identifiers
        """
        PADDING = HostsInfo.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(HostsInfo.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = HostsInfo.FIELDS + (
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=HostsInfo.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),), ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict`` or ``int``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetHostOsVersionResponseV1ToV2.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class SetHostOsVersionResponseV1ToV2

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
