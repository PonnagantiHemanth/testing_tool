#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.keyboard.multiplatform
:brief: HID++ 2.0 ``MultiPlatform`` command interface definition
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatform(HidppMessage):
    """
    Multi-Platform devices behave specifically to the host operating system and version, described as platforms.
    This feature reports the Platforms defined and supported by the device, and which Platform is configured per host.
    It does not describe how a Platform affects the device.
    """
    FEATURE_ID = 0x4531
    MAX_FUNCTION_INDEX = 3

    class OsMask:
        """
        Define the possible values supported by the ``GetPlatformDescriptorResponse.os_mask`` field
        """
        WINDOWS = 1
        WIN_EMB = WINDOWS << 1
        LINUX = WIN_EMB << 1
        CHROME_OS = LINUX << 1
        ANDROID = CHROME_OS << 1
        MAC_OS = ANDROID << 1
        IOS = MAC_OS << 1
        WEB_OS = IOS << 1
        TIZEN = WEB_OS << 1
    # end class OsMask

    class PlatformSource:
        """
        Define the possible values supported by the ``GetHostPlatformResponse.platform_source`` field
        """
        DEFAULT = 0
        AUTO = 1
        MANUAL = 2
        SOFTWARE = 3
    # end class PlatformSource

    class Status:
        """
        Define the possible values supported by the ``GetHostPlatformResponse.status`` field
        """
        EMPTY = 0
        PAIRED = 1
    # end class Status

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class MultiPlatform


class CapabilityMask(BitFieldContainerMixin):
    """
    Define ``GetFeatureInfosResponse.CapabilityMask`` field

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved 0                    6
    Set Host Platform             1
    OS Detection                  1
    Reserved 1                    8
    ============================  ==========
    """

    class FID(object):
        """
        Field identifiers
        """
        RESERVED_0 = 0xFF
        SET_HOST_PLATFORM = RESERVED_0 - 1
        OS_DETECTION = SET_HOST_PLATFORM - 1
        RESERVED_1 = OS_DETECTION - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED_0 = 0x6
        SET_HOST_PLATFORM = 0x1
        OS_DETECTION = 0x1
        RESERVED_1 = 0x8
    # end class LEN

    class DEFAULT(object):
        """
        Field default values
        """
        RESERVED_0 = 0
        SET_HOST_PLATFORM = 0
        OS_DETECTION = 0
        RESERVED_1 = 0
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.RESERVED_0, length=LEN.RESERVED_0,
                 title="Reserved0", name="reserved_0",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_0) - 1),),
                 default_value=DEFAULT.RESERVED_0),
        BitField(fid=FID.SET_HOST_PLATFORM, length=LEN.SET_HOST_PLATFORM,
                 title="SetHostPlatform", name="set_host_platform",
                 checks=(CheckInt(0, pow(2, LEN.SET_HOST_PLATFORM) - 1),),
                 default_value=DEFAULT.SET_HOST_PLATFORM),
        BitField(fid=FID.OS_DETECTION, length=LEN.OS_DETECTION,
                 title="OsDetection", name="os_detection",
                 checks=(CheckInt(0, pow(2, LEN.OS_DETECTION) - 1),),
                 default_value=DEFAULT.OS_DETECTION),
        BitField(fid=FID.RESERVED_1, length=LEN.RESERVED_1,
                 title="Reserved1", name="reserved_1",
                 checks=(CheckHexList(LEN.RESERVED_1 // 8),
                         CheckByte(),),
                 default_value=DEFAULT.RESERVED_1),
    )
# end class CapabilityMask


class OSMaskV0(BitFieldContainerMixin):
    """
    Define ``OSMask`` information for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved 0                    1
    iOS                           1
    Mac OS                        1
    Android                       1
    Chrome                        1
    Linux                         1
    Win Emb                       1
    Windows                       1
    Reserved 1                    8
    ============================  ==========
    """

    class FID(object):
        """
        Field identifiers
        """
        RESERVED_0 = 0xFF
        IOS = RESERVED_0 - 1
        MAC_OS = IOS - 1
        ANDROID = MAC_OS - 1
        CHROME = ANDROID - 1
        LINUX = CHROME - 1
        WIN_EMB = LINUX - 1
        WINDOWS = WIN_EMB - 1
        RESERVED_1 = WINDOWS - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED_0 = 0x1
        IOS = 0x1
        MAC_OS = 0x1
        ANDROID = 0x1
        CHROME = 0x1
        LINUX = 0x1
        WIN_EMB = 0x1
        WINDOWS = 0x1
        RESERVED_1 = 0x8
    # end class LEN

    class DEFAULT(object):
        """
        Field default values
        """
        RESERVED_0 = 0
        IOS = 0
        MAC_OS = 0
        ANDROID = 0
        CHROME = 0
        LINUX = 0
        WIN_EMB = 0
        WINDOWS = 0
        RESERVED_1 = 0
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.RESERVED_0, length=LEN.RESERVED_0,
                 title="Reserved0", name="reserved_0",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_0) - 1),),
                 default_value=DEFAULT.RESERVED_0),
        BitField(fid=FID.IOS, length=LEN.IOS,
                 title="Ios", name="ios",
                 checks=(CheckInt(0, pow(2, LEN.IOS) - 1),),
                 default_value=DEFAULT.IOS),
        BitField(fid=FID.MAC_OS, length=LEN.MAC_OS,
                 title="MacOs", name="mac_os",
                 checks=(CheckInt(0, pow(2, LEN.MAC_OS) - 1),),
                 default_value=DEFAULT.MAC_OS),
        BitField(fid=FID.ANDROID, length=LEN.ANDROID,
                 title="Android", name="android",
                 checks=(CheckInt(0, pow(2, LEN.ANDROID) - 1),),
                 default_value=DEFAULT.ANDROID),
        BitField(fid=FID.CHROME, length=LEN.CHROME,
                 title="Chrome", name="chrome",
                 checks=(CheckInt(0, pow(2, LEN.CHROME) - 1),),
                 default_value=DEFAULT.CHROME),
        BitField(fid=FID.LINUX, length=LEN.LINUX,
                 title="Linux", name="linux",
                 checks=(CheckInt(0, pow(2, LEN.LINUX) - 1),),
                 default_value=DEFAULT.LINUX),
        BitField(fid=FID.WIN_EMB, length=LEN.WIN_EMB,
                 title="WinEmb", name="win_emb",
                 checks=(CheckInt(0, pow(2, LEN.WIN_EMB) - 1),),
                 default_value=DEFAULT.WIN_EMB),
        BitField(fid=FID.WINDOWS, length=LEN.WINDOWS,
                 title="Windows", name="windows",
                 checks=(CheckInt(0, pow(2, LEN.WINDOWS) - 1),),
                 default_value=DEFAULT.WINDOWS),
        BitField(fid=FID.RESERVED_1, length=LEN.RESERVED_1,
                 title="Reserved1", name="reserved_1",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_1) - 1),),
                 default_value=DEFAULT.RESERVED_1),
    )
# end class OSMaskV0


class OSMaskV1(OSMaskV0):
    """
    Define ``OSMask`` information for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Web OS                        1
    iOS                           1
    Mac OS                        1
    Android                       1
    Chrome                        1
    Linux                         1
    Win Emb                       1
    Windows                       1
    Reserved                      7
    Tizen                         1
    ============================  ==========
    """

    class FID(OSMaskV0):
        """
        Field identifiers
        """
        WEB_OS = 0xFF
        RESERVED = OSMaskV0.FID.WINDOWS - 1
        TIZEN = RESERVED - 1
    # end class FID

    class LEN(OSMaskV0):
        """
        Field lengths in bits
        """
        WEB_OS = 0x1
        RESERVED = 0x7
        TIZEN = 0x1
    # end class LEN

    class DEFAULT(OSMaskV0):
        """
        Field default values
        """
        WEB_OS = 0
        RESERVED = 0
        TIZEN = 0
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.WEB_OS, length=LEN.WEB_OS,
                 title="WebOs", name="web_os",
                 checks=(CheckInt(0, pow(2, LEN.WEB_OS) - 1),),
                 default_value=DEFAULT.WEB_OS),
        ) + OSMaskV0.FIELDS[1: -1] + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=DEFAULT.RESERVED),
        BitField(fid=FID.TIZEN, length=LEN.TIZEN,
                 title="Tizen", name="tizen",
                 checks=(CheckInt(0, pow(2, LEN.TIZEN) - 1),),
                 default_value=DEFAULT.TIZEN),
    )
# end class OSMaskV1


class MultiPlatformModel(FeatureModel):
    """
    Define ``MultiPlatform`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_FEATURE_INFOS = 0
        GET_PLATFORM_DESCRIPTOR = 1
        GET_HOST_PLATFORM = 2
        SET_HOST_PLATFORM = 3

        # Event index
        PLATFORM_CHANGE = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``MultiPlatform`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_FEATURE_INFOS: {
                    "request": GetFeatureInfos,
                    "response": GetFeatureInfosResponse
                },
                cls.INDEX.GET_PLATFORM_DESCRIPTOR: {
                    "request": GetPlatformDescriptor,
                    "response": GetPlatformDescriptorResponseV0
                },
                cls.INDEX.GET_HOST_PLATFORM: {
                    "request": GetHostPlatform,
                    "response": GetHostPlatformResponse
                },
                cls.INDEX.SET_HOST_PLATFORM: {
                    "request": SetHostPlatform,
                    "response": SetHostPlatformResponse
                }
            },
            "events": {
                cls.INDEX.PLATFORM_CHANGE: {"report": PlatformChangeEvent}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_FEATURE_INFOS: {
                    "request": GetFeatureInfos,
                    "response": GetFeatureInfosResponse
                },
                cls.INDEX.GET_PLATFORM_DESCRIPTOR: {
                    "request": GetPlatformDescriptor,
                    "response": GetPlatformDescriptorResponseV1
                },
                cls.INDEX.GET_HOST_PLATFORM: {
                    "request": GetHostPlatform,
                    "response": GetHostPlatformResponse
                },
                cls.INDEX.SET_HOST_PLATFORM: {
                    "request": SetHostPlatform,
                    "response": SetHostPlatformResponse
                }
            },
            "events": {
                cls.INDEX.PLATFORM_CHANGE: {"report": PlatformChangeEvent}
            }
        }

        return {
            "feature_base": MultiPlatform,
            "versions": {
                MultiPlatformV0.VERSION: {
                    "main_cls": MultiPlatformV0,
                    "api": function_map_v0
                },
                MultiPlatformV1.VERSION: {
                    "main_cls": MultiPlatformV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class MultiPlatformModel


class MultiPlatformFactory(FeatureFactory):
    """
    Get ``MultiPlatform`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``MultiPlatform`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``MultiPlatformInterface``
        """
        return MultiPlatformModel.get_main_cls(version)()
    # end def create
# end class MultiPlatformFactory


class MultiPlatformInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``MultiPlatform``
    """

    def __init__(self):
        # Requests
        self.get_feature_infos_cls = None
        self.get_platform_descriptor_cls = None
        self.get_host_platform_cls = None
        self.set_host_platform_cls = None

        # Responses
        self.get_feature_infos_response_cls = None
        self.get_platform_descriptor_response_cls = None
        self.get_host_platform_response_cls = None
        self.set_host_platform_response_cls = None

        # Events
        self.platform_change_event_cls = None
    # end def __init__
# end class MultiPlatformInterface


class MultiPlatformV0(MultiPlatformInterface):
    """
    Define ``MultiPlatformV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetFeatureInfos() -> capabilityMask, numPlatforms, numPlatformDescriptor, numHosts, currentHost,
     currentHostPlatform

    [1] GetPlatformDescriptor(platformDescriptorIndex) -> platformIndex, platformDescriptorIndex, oSMask,
     fromVersion, fromRevision, toVersion, toRevision

    [2] GetHostPlatform(hostIndex) -> hostIndex, status, platformIndex, platformSource, autoPlatform, autoDescriptor

    [3] SetHostPlatform(hostIndex, platformIndex) -> hostIndex, platformIndex

    [Event 0] PlatformChangeEvent -> hostIndex, platformIndex, platformSource
    """
    VERSION = 0

    def __init__(self):
        # See ``MultiPlatform.__init__``
        super().__init__()
        index = MultiPlatformModel.INDEX

        # Requests
        self.get_feature_infos_cls = MultiPlatformModel.get_request_cls(
            self.VERSION, index.GET_FEATURE_INFOS)
        self.get_platform_descriptor_cls = MultiPlatformModel.get_request_cls(
            self.VERSION, index.GET_PLATFORM_DESCRIPTOR)
        self.get_host_platform_cls = MultiPlatformModel.get_request_cls(
            self.VERSION, index.GET_HOST_PLATFORM)
        self.set_host_platform_cls = MultiPlatformModel.get_request_cls(
            self.VERSION, index.SET_HOST_PLATFORM)

        # Responses
        self.get_feature_infos_response_cls = MultiPlatformModel.get_response_cls(
            self.VERSION, index.GET_FEATURE_INFOS)
        self.get_platform_descriptor_response_cls = MultiPlatformModel.get_response_cls(
            self.VERSION, index.GET_PLATFORM_DESCRIPTOR)
        self.get_host_platform_response_cls = MultiPlatformModel.get_response_cls(
            self.VERSION, index.GET_HOST_PLATFORM)
        self.set_host_platform_response_cls = MultiPlatformModel.get_response_cls(
            self.VERSION, index.SET_HOST_PLATFORM)

        # Events
        self.platform_change_event_cls = MultiPlatformModel.get_report_cls(
            self.VERSION, index.PLATFORM_CHANGE)
    # end def __init__

    def get_max_function_index(self):
        # See ``MultiPlatformInterface.get_max_function_index``
        return MultiPlatformModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class MultiPlatformV0


class MultiPlatformV1(MultiPlatformV0):
    """
    Define ``MultiPlatformV1`` feature

    This feature provides model and unit specific information for version 1

    [0] GetFeatureInfos() -> capabilityMask, numPlatforms, numPlatformDescriptor, numHosts, currentHost,
     currentHostPlatform

    [1] GetPlatformDescriptor(platformDescriptorIndex) -> platformIndex, platformDescriptorIndex, oSMask,
     fromVersion, fromRevision, toVersion, toRevision

    [2] GetHostPlatform(hostIndex) -> hostIndex, status, platformIndex, platformSource, autoPlatform, autoDescriptor

    [3] SetHostPlatform(hostIndex, platformIndex) -> hostIndex, platformIndex

    [Event 0] PlatformChangeEvent -> hostIndex, platformIndex, platformSource
    """
    VERSION = 1
# end class MultiPlatformV1


class ShortEmptyPacketDataFormat(MultiPlatform):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetFeatureInfos

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        PADDING = MultiPlatform.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class GetFeatureInfos(ShortEmptyPacketDataFormat):
    """
    Define ``GetFeatureInfos`` implementation class for version 0, 1
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetFeatureInfosResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetFeatureInfos


class GetFeatureInfosResponse(MultiPlatform):
    """
    Define ``GetFeatureInfosResponse`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Capability Mask               16
    Num Platforms                 8
    Num Platform Descriptor       8
    Num Hosts                     8
    Current Host                  8
    Current Host Platform         8
    Padding                       72
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFeatureInfos,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        CAPABILITY_MASK = MultiPlatform.FID.SOFTWARE_ID - 1
        NUM_PLATFORMS = CAPABILITY_MASK - 1
        NUM_PLATFORM_DESCRIPTOR = NUM_PLATFORMS - 1
        NUM_HOSTS = NUM_PLATFORM_DESCRIPTOR - 1
        CURRENT_HOST = NUM_HOSTS - 1
        CURRENT_HOST_PLATFORM = CURRENT_HOST - 1
        PADDING = CURRENT_HOST_PLATFORM - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        CAPABILITY_MASK = 0x10
        NUM_PLATFORMS = 0x8
        NUM_PLATFORM_DESCRIPTOR = 0x8
        NUM_HOSTS = 0x8
        CURRENT_HOST = 0x8
        CURRENT_HOST_PLATFORM = 0x8
        PADDING = 0x48
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.CAPABILITY_MASK, length=LEN.CAPABILITY_MASK,
                 title="CapabilityMask", name="capability_mask",
                 checks=(CheckHexList(LEN.CAPABILITY_MASK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CAPABILITY_MASK) - 1),)),
        BitField(fid=FID.NUM_PLATFORMS, length=LEN.NUM_PLATFORMS,
                 title="NumPlatforms", name="num_platforms",
                 checks=(CheckHexList(LEN.NUM_PLATFORMS // 8),
                         CheckByte(),)),
        BitField(fid=FID.NUM_PLATFORM_DESCRIPTOR, length=LEN.NUM_PLATFORM_DESCRIPTOR,
                 title="NumPlatformDescriptor", name="num_platform_descriptor",
                 checks=(CheckHexList(LEN.NUM_PLATFORM_DESCRIPTOR // 8),
                         CheckByte(),)),
        BitField(fid=FID.NUM_HOSTS, length=LEN.NUM_HOSTS,
                 title="NumHosts", name="num_hosts",
                 checks=(CheckHexList(LEN.NUM_HOSTS // 8),
                         CheckByte(),)),
        BitField(fid=FID.CURRENT_HOST, length=LEN.CURRENT_HOST,
                 title="CurrentHost", name="current_host",
                 checks=(CheckHexList(LEN.CURRENT_HOST // 8),
                         CheckByte(),)),
        BitField(fid=FID.CURRENT_HOST_PLATFORM, length=LEN.CURRENT_HOST_PLATFORM,
                 title="CurrentHostPlatform", name="current_host_platform",
                 checks=(CheckHexList(LEN.CURRENT_HOST_PLATFORM // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, set_host_platform, os_detection, num_platforms,
                 num_platform_descriptor, num_hosts, current_host, current_host_platform, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param set_host_platform: Set Host Platform
        :type set_host_platform: ``bool`` or ``HexList``
        :param os_detection: OS Detection
        :type os_detection: ``bool`` or ``HexList``
        :param num_platforms: Num Platforms
        :type num_platforms: ``int`` or ``HexList``
        :param num_platform_descriptor: Num Platform Descriptor
        :type num_platform_descriptor: ``int`` or ``HexList``
        :param num_hosts: Num Hosts
        :type num_hosts: ``int`` or ``HexList``
        :param current_host: Current Host
        :type current_host: ``int`` or ``HexList``
        :param current_host_platform: Current Host Platform
        :type current_host_platform: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.capability_mask = CapabilityMask(set_host_platform=set_host_platform,
                                              os_detection=os_detection)
        self.num_platforms = num_platforms
        self.num_platform_descriptor = num_platform_descriptor
        self.num_hosts = num_hosts
        self.current_host = current_host
        self.current_host_platform = current_host_platform
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetFeatureInfosResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capability_mask = CapabilityMask.fromHexList(
            inner_field_container_mixin.capability_mask)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetFeatureInfosResponse


class GetPlatformDescriptor(MultiPlatform):
    """
    Define ``GetPlatformDescriptor`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Platform Descriptor Index     8
    Padding                       16
    ============================  ==========
    """

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        PLATFORM_DESCRIPTOR_INDEX = MultiPlatform.FID.SOFTWARE_ID - 1
        PADDING = PLATFORM_DESCRIPTOR_INDEX - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        PLATFORM_DESCRIPTOR_INDEX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.PLATFORM_DESCRIPTOR_INDEX, length=LEN.PLATFORM_DESCRIPTOR_INDEX,
                 title="PlatformDescriptorIndex", name="platform_descriptor_index",
                 checks=(CheckHexList(LEN.PLATFORM_DESCRIPTOR_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, platform_descriptor_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param platform_descriptor_index: Platform Descriptor Index
        :type platform_descriptor_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetPlatformDescriptorResponseV0.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.platform_descriptor_index = platform_descriptor_index
    # end def __init__
# end class GetPlatformDescriptor


class GetPlatformDescriptorResponseV0(MultiPlatform):
    """
    Define ``GetPlatformDescriptorResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Platform Index                8
    Platform Descriptor Index     8
    OS Mask                       16
    From Version                  8
    From Revision                 8
    To Version                    8
    To Revision                   8
    Padding                       64
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPlatformDescriptor,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        PLATFORM_INDEX = MultiPlatform.FID.SOFTWARE_ID - 1
        PLATFORM_DESCRIPTOR_INDEX = PLATFORM_INDEX - 1
        OS_MASK = PLATFORM_DESCRIPTOR_INDEX - 1
        FROM_VERSION = OS_MASK - 1
        FROM_REVISION = FROM_VERSION - 1
        TO_VERSION = FROM_REVISION - 1
        TO_REVISION = TO_VERSION - 1
        PADDING = TO_REVISION - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        PLATFORM_INDEX = 0x8
        PLATFORM_DESCRIPTOR_INDEX = 0x8
        OS_MASK = 0x10
        FROM_VERSION = 0x8
        FROM_REVISION = 0x8
        TO_VERSION = 0x8
        TO_REVISION = 0x8
        PADDING = 0x40
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.PLATFORM_INDEX, length=LEN.PLATFORM_INDEX,
                 title="PlatformIndex", name="platform_index",
                 checks=(CheckHexList(LEN.PLATFORM_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PLATFORM_DESCRIPTOR_INDEX, length=LEN.PLATFORM_DESCRIPTOR_INDEX,
                 title="PlatformDescriptorIndex", name="platform_descriptor_index",
                 checks=(CheckHexList(LEN.PLATFORM_DESCRIPTOR_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.OS_MASK, length=LEN.OS_MASK,
                 title="OsMask", name="os_mask",
                 checks=(CheckHexList(LEN.OS_MASK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OS_MASK) - 1),)),
        BitField(fid=FID.FROM_VERSION, length=LEN.FROM_VERSION,
                 title="FromVersion", name="from_version",
                 checks=(CheckHexList(LEN.FROM_VERSION // 8),
                         CheckByte(),)),
        BitField(fid=FID.FROM_REVISION, length=LEN.FROM_REVISION,
                 title="FromRevision", name="from_revision",
                 checks=(CheckHexList(LEN.FROM_REVISION // 8),
                         CheckByte(),)),
        BitField(fid=FID.TO_VERSION, length=LEN.TO_VERSION,
                 title="ToVersion", name="to_version",
                 checks=(CheckHexList(LEN.TO_VERSION // 8),
                         CheckByte(),)),
        BitField(fid=FID.TO_REVISION, length=LEN.TO_REVISION,
                 title="ToRevision", name="to_revision",
                 checks=(CheckHexList(LEN.TO_REVISION // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, platform_index, platform_descriptor_index, ios, mac_os,
                 android, chrome, linux, win_emb, windows, from_version, from_revision, to_version, to_revision,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param platform_index: Platform Index
        :type platform_index: ``int`` or ``HexList``
        :param platform_descriptor_index: Platform Descriptor Index
        :type platform_descriptor_index: ``int`` or ``HexList``
        :param ios: iOS
        :type ios: ``bool`` or ``HexList``
        :param mac_os: Mac OS
        :type mac_os: ``bool`` or ``HexList``
        :param android: Android
        :type android: ``bool`` or ``HexList``
        :param chrome: Chrome
        :type chrome: ``bool`` or ``HexList``
        :param linux: Linux
        :type linux: ``bool`` or ``HexList``
        :param win_emb: Win Emb
        :type win_emb: ``bool`` or ``HexList``
        :param windows: Windows
        :type windows: ``bool`` or ``HexList``
        :param from_version: From Version
        :type from_version: ``int`` or ``HexList``
        :param from_revision: From Revision
        :type from_revision: ``int`` or ``HexList``
        :param to_version: To Version
        :type to_version: ``int`` or ``HexList``
        :param to_revision: To Revision
        :type to_revision: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.platform_index = platform_index
        self.platform_descriptor_index = platform_descriptor_index
        self.os_mask = OSMaskV0(ios=ios,
                                mac_os=mac_os,
                                android=android,
                                chrome=chrome,
                                linux=linux,
                                win_emb=win_emb,
                                windows=windows)
        self.from_version = from_version
        self.from_revision = from_revision
        self.to_version = to_version
        self.to_revision = to_revision
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetPlatformDescriptorResponseV0``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.os_mask = OSMaskV0.fromHexList(
            inner_field_container_mixin.os_mask)
        return inner_field_container_mixin
    # end def fromHexList

    @staticmethod
    def get_os_mask_cls():
        """
        Get the os mask class

        :return: Os Mask class
        :rtype: ``OSMaskV0``
        """
        return OSMaskV0
    # end def get_os_mask_cls
# end class GetPlatformDescriptorResponseV0


class GetPlatformDescriptorResponseV1(GetPlatformDescriptorResponseV0):
    """
    Define ``GetPlatformDescriptorResponse`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Platform Index                8
    Platform Descriptor Index     8
    OS Mask                       16
    From Version                  8
    From Revision                 8
    To Version                    8
    To Revision                   8
    Padding                       64
    ============================  ==========
    """
    VERSION = (1,)

    def __init__(self, device_index, feature_index, platform_index, platform_descriptor_index, web_os, ios, mac_os,
                 android, chrome, linux, win_emb, windows, tizen, from_version, from_revision, to_version, to_revision,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param platform_index: Platform Index
        :type platform_index: ``int`` or ``HexList``
        :param platform_descriptor_index: Platform Descriptor Index
        :type platform_descriptor_index: ``int`` or ``HexList``
        :param web_os: Web OS
        :type web_os: ``bool`` or ``HexList``
        :param ios: iOS
        :type ios: ``bool`` or ``HexList``
        :param mac_os: Mac OS
        :type mac_os: ``bool`` or ``HexList``
        :param android: Android
        :type android: ``bool`` or ``HexList``
        :param chrome: Chrome
        :type chrome: ``bool`` or ``HexList``
        :param linux: Linux
        :type linux: ``bool`` or ``HexList``
        :param win_emb: Win Emb
        :type win_emb: ``bool`` or ``HexList``
        :param windows: Windows
        :type windows: ``bool`` or ``HexList``
        :param tizen: Tizen
        :type tizen: ``bool`` or ``HexList``
        :param from_version: From Version
        :type from_version: ``int`` or ``HexList``
        :param from_revision: From Revision
        :type from_revision: ``int`` or ``HexList``
        :param to_version: To Version
        :type to_version: ``int`` or ``HexList``
        :param to_revision: To Revision
        :type to_revision: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         platform_index=platform_index, platform_descriptor_index=platform_descriptor_index,
                         ios=ios, mac_os=mac_os, android=android, chrome=chrome, linux=linux, win_emb=win_emb,
                         windows=windows, from_version=from_version, from_revision=from_revision, to_version=to_version,
                         to_revision=to_revision, **kwargs)
        self.os_mask = OSMaskV1(web_os=web_os,
                                ios=ios,
                                mac_os=mac_os,
                                android=android,
                                chrome=chrome,
                                linux=linux,
                                win_emb=win_emb,
                                windows=windows,
                                tizen=tizen)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetPlatformDescriptorResponseV1``
        """
        inner_field_container_mixin = super(MultiPlatform, cls).fromHexList(*args, **kwargs)
        inner_field_container_mixin.os_mask = OSMaskV1.fromHexList(
            inner_field_container_mixin.os_mask)
        return inner_field_container_mixin
    # end def fromHexList

    @staticmethod
    def get_os_mask_cls():
        # See ``GetPlatformDescriptorResponseV0``
        return OSMaskV1
    # end def get_os_mask_cls
# end class GetPlatformDescriptorResponseV1


class GetHostPlatform(MultiPlatform):
    """
    Define ``GetHostPlatform`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Host Index                    8
    Padding                       16
    ============================  ==========
    """

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        HOST_INDEX = MultiPlatform.FID.SOFTWARE_ID - 1
        PADDING = HOST_INDEX - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        HOST_INDEX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Host Index
        :type host_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetHostPlatformResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.host_index = host_index
    # end def __init__
# end class GetHostPlatform


class GetHostPlatformResponse(MultiPlatform):
    """
    Define ``GetHostPlatformResponse`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Host Index                    8
    Status                        8
    Platform Index                8
    Platform Source               8
    Auto Platform                 8
    Auto Descriptor               8
    Padding                       80
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetHostPlatform,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        HOST_INDEX = MultiPlatform.FID.SOFTWARE_ID - 1
        STATUS = HOST_INDEX - 1
        PLATFORM_INDEX = STATUS - 1
        PLATFORM_SOURCE = PLATFORM_INDEX - 1
        AUTO_PLATFORM = PLATFORM_SOURCE - 1
        AUTO_DESCRIPTOR = AUTO_PLATFORM - 1
        PADDING = AUTO_DESCRIPTOR - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        HOST_INDEX = 0x8
        STATUS = 0x8
        PLATFORM_INDEX = 0x8
        PLATFORM_SOURCE = 0x8
        AUTO_PLATFORM = 0x8
        AUTO_DESCRIPTOR = 0x8
        PADDING = 0x50
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.STATUS, length=LEN.STATUS,
                 title="Status", name="status",
                 checks=(CheckHexList(LEN.STATUS // 8),
                         CheckByte(),)),
        BitField(fid=FID.PLATFORM_INDEX, length=LEN.PLATFORM_INDEX,
                 title="PlatformIndex", name="platform_index",
                 checks=(CheckHexList(LEN.PLATFORM_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PLATFORM_SOURCE, length=LEN.PLATFORM_SOURCE,
                 title="PlatformSource", name="platform_source",
                 checks=(CheckHexList(LEN.PLATFORM_SOURCE // 8),
                         CheckByte(),)),
        BitField(fid=FID.AUTO_PLATFORM, length=LEN.AUTO_PLATFORM,
                 title="AutoPlatform", name="auto_platform",
                 checks=(CheckHexList(LEN.AUTO_PLATFORM // 8),
                         CheckByte(),)),
        BitField(fid=FID.AUTO_DESCRIPTOR, length=LEN.AUTO_DESCRIPTOR,
                 title="AutoDescriptor", name="auto_descriptor",
                 checks=(CheckHexList(LEN.AUTO_DESCRIPTOR // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, status, platform_index, platform_source, auto_platform,
                 auto_descriptor, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Host Index
        :type host_index: ``int`` or ``HexList``
        :param status: Status
        :type status: ``int`` or ``HexList``
        :param platform_index: Platform Index
        :type platform_index: ``int`` or ``HexList``
        :param platform_source: Platform Source
        :type platform_source: ``int`` or ``HexList``
        :param auto_platform: Auto Platform
        :type auto_platform: ``int`` or ``HexList``
        :param auto_descriptor: Auto Descriptor
        :type auto_descriptor: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.host_index = host_index
        self.status = status
        self.platform_index = platform_index
        self.platform_source = platform_source
        self.auto_platform = auto_platform
        self.auto_descriptor = auto_descriptor
    # end def __init__
# end class GetHostPlatformResponse


class SetHostPlatform(MultiPlatform):
    """
    Define ``SetHostPlatform`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Host Index                    8
    Platform Index                8
    Padding                       8
    ============================  ==========
    """

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        HOST_INDEX = MultiPlatform.FID.SOFTWARE_ID - 1
        PLATFORM_INDEX = HOST_INDEX - 1
        PADDING = PLATFORM_INDEX - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        HOST_INDEX = 0x8
        PLATFORM_INDEX = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PLATFORM_INDEX, length=LEN.PLATFORM_INDEX,
                 title="PlatformIndex", name="platform_index",
                 checks=(CheckHexList(LEN.PLATFORM_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, platform_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Host Index
        :type host_index: ``int`` or ``HexList``
        :param platform_index: Platform Index
        :type platform_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetHostPlatformResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.host_index = host_index
        self.platform_index = platform_index
    # end def __init__
# end class SetHostPlatform


class SetHostPlatformResponse(MultiPlatform):
    """
    Define ``SetHostPlatformResponse`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Host Index                    8
    Platform Index                8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetHostPlatform,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 3

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        HOST_INDEX = MultiPlatform.FID.SOFTWARE_ID - 1
        PLATFORM_INDEX = HOST_INDEX - 1
        PADDING = PLATFORM_INDEX - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        HOST_INDEX = 0x8
        PLATFORM_INDEX = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PLATFORM_INDEX, length=LEN.PLATFORM_INDEX,
                 title="PlatformIndex", name="platform_index",
                 checks=(CheckHexList(LEN.PLATFORM_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, platform_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Host Index
        :type host_index: ``int`` or ``HexList``
        :param platform_index: Platform Index
        :type platform_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.host_index = host_index
        self.platform_index = platform_index
    # end def __init__
# end class SetHostPlatformResponse


class PlatformChangeEvent(MultiPlatform):
    """
    Define ``PlatformChangeEvent`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Host Index                    8
    Platform Index                8
    Platform Source               8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(MultiPlatform.FID):
        # See ``MultiPlatform.FID``
        HOST_INDEX = MultiPlatform.FID.SOFTWARE_ID - 1
        PLATFORM_INDEX = HOST_INDEX - 1
        PLATFORM_SOURCE = PLATFORM_INDEX - 1
        PADDING = PLATFORM_SOURCE - 1
    # end class FID

    class LEN(MultiPlatform.LEN):
        # See ``MultiPlatform.LEN``
        HOST_INDEX = 0x8
        PLATFORM_INDEX = 0x8
        PLATFORM_SOURCE = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = MultiPlatform.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PLATFORM_INDEX, length=LEN.PLATFORM_INDEX,
                 title="PlatformIndex", name="platform_index",
                 checks=(CheckHexList(LEN.PLATFORM_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PLATFORM_SOURCE, length=LEN.PLATFORM_SOURCE,
                 title="PlatformSource", name="platform_source",
                 checks=(CheckHexList(LEN.PLATFORM_SOURCE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiPlatform.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, platform_index, platform_source, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: Host Index
        :type host_index: ``int`` or ``HexList``
        :param platform_index: Platform Index
        :type platform_index: ``int`` or ``HexList``
        :param platform_source: Platform Source
        :type platform_source: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.host_index = host_index
        self.platform_index = platform_index
        self.platform_source = platform_source
    # end def __init__
# end class PlatformChangeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
