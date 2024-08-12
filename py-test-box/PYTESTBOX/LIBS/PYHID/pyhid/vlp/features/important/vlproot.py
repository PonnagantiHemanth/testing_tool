#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.vlp.features.important.vlproot
:brief: VLP 1.0 ``VLPRoot`` command interface definition
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.hidppmessage import TYPE
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.vlp.vlpmessage import VlpMessage
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class VLPRoot(VlpMessage):
    """
    This is a VLP feature. The maximum size of function and event payloads are defined per device and declared via this feature.
    """
    FEATURE_ID = 0x0102
    # IRoot feature index hard coded at 0
    FEATURE_INDEX = 0x00
    MAX_FUNCTION_INDEX_V0 = 2

    FEATURE_NOT_FOUND = 0x00
    UNKNOWN_PROTOCOL = 0x01

    def __init__(self, device_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, **kwargs)

        self.device_index = device_index
        self.feature_index = self.FEATURE_INDEX
    # end def __init__
# end class VLPRoot


# noinspection DuplicatedCode
class VLPRootModel(FeatureModel):
    """
    Define ``VLPRoot`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_FEATURE_INDEX = 0
        GET_PROTOCOL_CAPABILITIES = 1
        GET_PING_DATA = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``VLPRoot`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_FEATURE_INDEX: {
                    "request": GetFeatureIndex,
                    "response": GetFeatureIndexResponse
                },
                cls.INDEX.GET_PROTOCOL_CAPABILITIES: {
                    "request": GetProtocolCapabilities,
                    "response": GetProtocolCapabilitiesResponse
                },
                cls.INDEX.GET_PING_DATA: {
                    "request": GetPingData,
                    "response": GetPingDataResponse
                }
            }
        }

        return {
            "feature_base": VLPRoot,
            "versions": {
                VLPRootV0.VERSION: {
                    "main_cls": VLPRootV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class VLPRootModel


class VLPRootFactory(FeatureFactory):
    """
    Get ``VLPRoot`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``VLPRoot`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``VLPRootInterface``
        """
        return VLPRootModel.get_main_cls(version)()
    # end def create
# end class VLPRootFactory


class VLPRootInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``VLPRoot``
    """

    def __init__(self):
        # Requests
        self.get_feature_index_cls = None
        self.get_protocol_capabilities_cls = None
        self.get_ping_data_cls = None

        # Responses
        self.get_feature_index_response_cls = None
        self.get_protocol_capabilities_response_cls = None
        self.get_ping_data_response_cls = None
    # end def __init__
# end class VLPRootInterface


class VLPRootV0(VLPRootInterface):
    """
    Define ``VLPRootV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getFeatureIndex(featureId) -> featureId, featureIndex, featureVersion, featureMaxMemory

    [1] getProtocolCapabilities() -> protocolMajor, protocolMinor, availableTotalMemory

    [2] getPingData(pingData) -> pingData
    """
    VERSION = 0

    def __init__(self):
        # See ``VLPRoot.__init__``
        super().__init__()
        index = VLPRootModel.INDEX

        # Requests
        self.get_feature_index_cls = VLPRootModel.get_request_cls(
            self.VERSION, index.GET_FEATURE_INDEX)
        self.get_protocol_capabilities_cls = VLPRootModel.get_request_cls(
            self.VERSION, index.GET_PROTOCOL_CAPABILITIES)
        self.get_ping_data_cls = VLPRootModel.get_request_cls(
            self.VERSION, index.GET_PING_DATA)

        # Responses
        self.get_feature_index_response_cls = VLPRootModel.get_response_cls(
            self.VERSION, index.GET_FEATURE_INDEX)
        self.get_protocol_capabilities_response_cls = VLPRootModel.get_response_cls(
            self.VERSION, index.GET_PROTOCOL_CAPABILITIES)
        self.get_ping_data_response_cls = VLPRootModel.get_response_cls(
            self.VERSION, index.GET_PING_DATA)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``VLPRootInterface.get_max_function_index``
        return VLPRootModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class VLPRootV0


class GetFeatureIndex(VLPRoot):
    """
    Define ``GetFeatureIndex`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Feature ID                    16
    ============================  ==========
    """

    class FID(VLPRoot.FID):
        # See ``VLPRoot.FID``
        FEATURE_ID = VLPRoot.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    class LEN(VLPRoot.LEN):
        # See ``VLPRoot.LEN``
        FEATURE_ID = 0x10
    # end class LEN

    FIELDS = VLPRoot.FIELDS + (
        BitField(fid=FID.FEATURE_ID, length=LEN.FEATURE_ID,
                 title="FeatureId", name="feature_id",
                 checks=(CheckHexList(LEN.FEATURE_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FEATURE_ID) - 1),)),
    )

    def __init__(self, device_index, feature_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param feature_id: Feature ID
        :type feature_id: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index,
                         function_index=GetFeatureIndexResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        self.feature_id = feature_id
    # end def __init__
# end class GetFeatureIndex


class GetProtocolCapabilities(VLPRoot):
    """
    Define ``GetProtocolCapabilities`` implementation class
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetProtocolCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class GetProtocolCapabilities


class GetPingData(VLPRoot):
    """
    Define ``GetPingData`` implementation class
    """
    class FID(VLPRoot.FID):
        # See ``VLPRoot.FID``
        PING_DATA = VLPRoot.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    class LEN(VLPRoot.LEN):
        # See ``VLPRoot.LEN``
        PING_DATA = 0x40
    # end class LEN

    class DEFAULT(VLPRoot.DEFAULT):
        # See ``VLPRoot.DEFAULT``
        PING_DATA = 0x0000000000000000
    # end class LEN

    FIELDS = VLPRoot.FIELDS + (
        BitField(fid=FID.PING_DATA, length=LEN.PING_DATA,
                 title="ping_data", name="ping_data",
                 checks=(CheckHexList(LEN.PING_DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PING_DATA) - 1),),
                 conversions  = {HexList : Numeral},),
    )

    def __init__(self, device_index, feature_index, ping_data, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param ping_data: Ping Data
        :type ping_data: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetPingDataResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        self.ping_data = ping_data
    # end def __init__
# end class GetPingData


class GetFeatureIndexResponse(VLPRoot):
    """
    Define ``GetFeatureIndexResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Feature ID                    16
    Feature Index                 8
    Reserved 0                    6
    Hidden                        1
    Reserved 1                    1
    Feature Version               8
    Feature Max Memory            32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFeatureIndex,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(VLPRoot.FID):
        # See ``VLPRoot.FID``
        FEATURE_ID = VLPRoot.FID.VLP_SEQUENCE_NUMBER - 1
        FEATURE_INDEX = FEATURE_ID - 1
        RESERVED_0 = FEATURE_INDEX - 1
        HIDDEN = RESERVED_0 - 1
        RESERVED_1 = HIDDEN - 1
        FEATURE_VERSION = RESERVED_1 - 1
        FEATURE_MAX_MEMORY = FEATURE_VERSION - 1
    # end class FID

    class LEN(VLPRoot.LEN):
        # See ``VLPRoot.LEN``
        FEATURE_ID = 0x10
        FEATURE_INDEX = 0x8
        RESERVED_0 = 0x6
        HIDDEN = 0x01
        RESERVED_1 = 0x1
        FEATURE_VERSION = 0x8
        FEATURE_MAX_MEMORY = 0x20
    # end class LEN

    FIELDS = VLPRoot.FIELDS + (
        BitField(fid=FID.FEATURE_ID, length=LEN.FEATURE_ID,
                 title="FeatureId", name="feature_id",
                 checks=(CheckHexList(LEN.FEATURE_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FEATURE_ID) - 1),)),
        BitField(fid=FID.FEATURE_INDEX, length=LEN.FEATURE_INDEX,
                 title="FeatureIndex", name="feature_idx",
                 checks=(CheckHexList(LEN.FEATURE_INDEX // 8), CheckByte(),),
                 conversions={HexList: Numeral},),
        BitField(fid=FID.RESERVED_0, length=LEN.RESERVED_0,
                 title="Reserved0", name="reserved_0",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED_0) - 1),),
                 default_value=VLPRoot.DEFAULT.PADDING),
        BitField(fid=FID.HIDDEN, length=LEN.HIDDEN,
                 title="Hidden", name="hidden",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.HIDDEN) - 1),),
                 default_value=VLPRoot.DEFAULT.PADDING),
        BitField(fid=FID.RESERVED_1, length=LEN.RESERVED_1,
                 title="Reserved1", name="reserved_1",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED_1) - 1),),
                 default_value=VLPRoot.DEFAULT.PADDING),
        BitField(fid=FID.FEATURE_VERSION, length=LEN.FEATURE_VERSION,
                 title="FeatureVersion", name="feature_version",
                 checks=(CheckHexList(LEN.FEATURE_VERSION // 8), CheckByte(),)),
        BitField(fid=FID.FEATURE_MAX_MEMORY, length=LEN.FEATURE_MAX_MEMORY,
                 title="FeatureMaxMemory", name="feature_max_memory",
                 checks=(CheckHexList(LEN.FEATURE_MAX_MEMORY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FEATURE_MAX_MEMORY) - 1),)),
    )

    def __init__(self, device_index, feature_index, feature_id, feature_version, feature_max_memory,
                 **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param feature_id: Feature ID
        :type feature_id: ``HexList``
        :param feature_version: Feature Version
        :type feature_version: ``HexList``
        :param feature_max_memory: Feature Max Memory
        :type feature_max_memory: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        self.feature_id = feature_id
        self.feature_index = feature_index
        self.feature_version = feature_version
        self.feature_max_memory = feature_max_memory
    # end def __init__
# end class GetFeatureIndexResponse


class GetProtocolCapabilitiesResponse(VLPRoot):
    """
    Define ``GetProtocolCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Protocol Major                8
    Protocol Minor                8
    Available Total Memory        32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetProtocolCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(VLPRoot.FID):
        # See ``VLPRoot.FID``
        PROTOCOL_MAJOR = VLPRoot.FID.VLP_SEQUENCE_NUMBER - 1
        PROTOCOL_MINOR = PROTOCOL_MAJOR - 1
        AVAILABLE_TOTAL_MEMORY = PROTOCOL_MINOR - 1
    # end class FID

    class LEN(VLPRoot.LEN):
        # See ``VLPRoot.LEN``
        PROTOCOL_MAJOR = 0x8
        PROTOCOL_MINOR = 0x8
        AVAILABLE_TOTAL_MEMORY = 0x20
    # end class LEN

    FIELDS = VLPRoot.FIELDS + (
        BitField(fid=FID.PROTOCOL_MAJOR, length=LEN.PROTOCOL_MAJOR,
                 title="ProtocolMajor", name="protocol_major",
                 checks=(CheckHexList(LEN.PROTOCOL_MAJOR // 8), CheckByte(),)),
        BitField(fid=FID.PROTOCOL_MINOR, length=LEN.PROTOCOL_MINOR,
                 title="ProtocolMinor", name="protocol_minor",
                 checks=(CheckHexList(LEN.PROTOCOL_MINOR // 8), CheckByte(),)),
        BitField(fid=FID.AVAILABLE_TOTAL_MEMORY, length=LEN.AVAILABLE_TOTAL_MEMORY,
                 title="AvailableTotalMemory", name="available_total_memory",
                 checks=(CheckHexList(LEN.AVAILABLE_TOTAL_MEMORY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.AVAILABLE_TOTAL_MEMORY) - 1),)),
    )

    def __init__(self, device_index, feature_index, protocol_major, protocol_minor, available_total_memory, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param protocol_major: Protocol Major
        :type protocol_major: ``HexList``
        :param protocol_minor: Protocol Minor
        :type protocol_minor: ``HexList``
        :param available_total_memory: Available Total Memory
        :type available_total_memory: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        self.protocol_major = protocol_major
        self.protocol_minor = protocol_minor
        self.available_total_memory = available_total_memory
    # end def __init__
# end class GetProtocolCapabilitiesResponse


class GetPingDataResponse(VLPRoot):
    """
    Define ``GetPingDataResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Ping Data                     64
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPingData,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(VLPRoot.FID):
        # See ``VLPRoot.FID``
        PING_DATA = VLPRoot.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    class LEN(VLPRoot.LEN):
        # See ``VLPRoot.LEN``
        PING_DATA = 0x40
    # end class LEN

    FIELDS = VLPRoot.FIELDS + (
        BitField(fid=FID.PING_DATA, length=LEN.PING_DATA,
                 title="PingData", name="ping_data",
                 checks=(CheckHexList(LEN.PING_DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PING_DATA) - 1),)),
    )

    def __init__(self, device_index, feature_index, ping_data, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param ping_data: Ping Data
        :type ping_data: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        self.ping_data = ping_data
    # end def __init__
# end class GetPingDataResponse


class VLPFeatureIniConfigInfo(object):
    """
    Define the VLP feature information required by tests in 0x0102 test suite.
    """
    def __init__(self, category=None, name=None, version=None, class_name=None, class_import_path=None):
        """
        :param category: feature category - OPTIONAL
        :type category: ``str``
        :param name: feature name - OPTIONAL
        :type name: ``str``
        :param version: feature version - OPTIONAL
        :type version: ``str | int``
        :param class_name: feature class name - OPTIONAL
        :type class_name: ``str``
        :param class_import_path: feature import path for feature class - OPTIONAL
        :type class_import_path: ``str``
        """
        self.category = category
        self.name = name
        self.version = version
        self.class_name = class_name
        self.class_import_path = class_import_path
    # end def __init__

    def __str__(self):
        return f"(category: {self.category}, name: {self.name}, version: {self.version}," \
               f" class_name: {self.class_name}, class_import_path: {self.class_import_path})"
    # end def __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def get_class_name(self):
        """
        Find the right feature class name given the feature name
        """
        # Some special class name handling
        if self.name == "ROOT":
            self.class_name = "VLPRoot"
        else:
            self.class_name = ''.join(word.capitalize() for word in self.name.split('_'))
        # end if
    # end def get_class_name

    def get_class_import_path(self):
        """
        Get the right feature class import path given the feature category and name
        """
        category_path = self.category.lower() + '.'
        self.class_import_path = \
            f"pyhid.vlp.features.{category_path}{self.class_name.replace('_', '').lower()}"
    # end def get_class_import_path
# end class VLPFeatureIniConfigInfo
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
