#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.vlp.features.important.vlpfeatureset
:brief: VLP 1.0 ``VLPFeatureSet`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/18
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
from pyhid.hidpp.hidppmessage import TYPE
from pyhid.vlp.vlpmessage import VlpMessage, VlpMessageRawPayload
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class VLPFeatureSet(VlpMessage):
    """
    This feature allows the host to enumerate all the features present on a device without prior knowledge of which
    features are supported.
    """
    FEATURE_ID = 0x0103
    MAX_FUNCTION_INDEX_V0 = 2
    # VLP Feature Set feature index hardcoded at 1
    FEATURE_INDEX = 0x01

    # noinspection DuplicatedCode
    class FeatureType(BitFieldContainerMixin):
        """
        Define ``FeatureType`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved 1                    6
        Feature Hidden                1
        Reserved 2                    1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED_1 = 0xFF
            FEATURE_HIDDEN = RESERVED_1 - 1
            RESERVED_2 = FEATURE_HIDDEN - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED_1 = 0x6
            FEATURE_HIDDEN = 0x1
            RESERVED_2 = 0x1
        # end class LEN

        FIELDS = (
            BitField(fid=FID.RESERVED_1, length=LEN.RESERVED_1,
                     title="Reserved1", name="reserved_1",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED_1) - 1),),
                     default_value=VlpMessage.DEFAULT.RESERVED),
            BitField(fid=FID.FEATURE_HIDDEN, length=LEN.FEATURE_HIDDEN,
                     title="FeatureHidden", name="feature_hidden",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FEATURE_HIDDEN) - 1),)),
            BitField(fid=FID.RESERVED_2, length=LEN.RESERVED_2,
                     title="Reserved2", name="reserved_2",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED_2) - 1),),
                     default_value=VlpMessage.DEFAULT.RESERVED),
        )
    # end class FeatureType
# end class VLPFeatureSet


# noinspection DuplicatedCode
class VLPFeatureSetModel(FeatureModel):
    """
    Define ``VLPFeatureSet`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_COUNT = 0
        GET_FEATURE_ID = 1
        GET_ALL_FEATURE_IDS = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``VLPFeatureSet`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_COUNT: {
                    "request": GetCount,
                    "response": GetCountResponse
                },
                cls.INDEX.GET_FEATURE_ID: {
                    "request": GetFeatureID,
                    "response": GetFeatureIDResponse
                },
                cls.INDEX.GET_ALL_FEATURE_IDS: {
                    "request": GetAllFeatureIDs,
                    "response": GetAllFeatureIDsResponse
                }
            }
        }

        return {
            "feature_base": VLPFeatureSet,
            "versions": {
                VLPFeatureSetV0.VERSION: {
                    "main_cls": VLPFeatureSetV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class VLPFeatureSetModel


class VLPFeatureSetFactory(FeatureFactory):
    """
    Get ``VLPFeatureSet`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``VLPFeatureSet`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``VLPFeatureSetInterface``
        """
        return VLPFeatureSetModel.get_main_cls(version)()
    # end def create
# end class VLPFeatureSetFactory


class VLPFeatureSetInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``VLPFeatureSet``
    """

    def __init__(self):
        # Requests
        self.get_count_cls = None
        self.get_feature_id_cls = None
        self.get_all_feature_ids_cls = None

        # Responses
        self.get_count_response_cls = None
        self.get_feature_id_response_cls = None
        self.get_all_feature_ids_response_cls = None
    # end def __init__
# end class VLPFeatureSetInterface


class VLPFeatureSetV0(VLPFeatureSetInterface):
    """
    Define ``VLPFeatureSetV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCount() -> count

    [1] getFeatureID(featureIdx) -> featureIdx, featureId, featureVersion, featureMaxMemory

    [2] getAllFeatureIDs() -> featureRecordsCount, featureRecordsSize, featureIdx, featureId, featureType,
    featureVersion, featureMaxMemory
    """
    VERSION = 0

    def __init__(self):
        # See ``VLPFeatureSet.__init__``
        super().__init__()
        index = VLPFeatureSetModel.INDEX

        # Requests
        self.get_count_cls = VLPFeatureSetModel.get_request_cls(
            self.VERSION, index.GET_COUNT)
        self.get_feature_id_cls = VLPFeatureSetModel.get_request_cls(
            self.VERSION, index.GET_FEATURE_ID)
        self.get_all_feature_ids_cls = VLPFeatureSetModel.get_request_cls(
            self.VERSION, index.GET_ALL_FEATURE_IDS)

        # Responses
        self.get_count_response_cls = VLPFeatureSetModel.get_response_cls(
            self.VERSION, index.GET_COUNT)
        self.get_feature_id_response_cls = VLPFeatureSetModel.get_response_cls(
            self.VERSION, index.GET_FEATURE_ID)
        self.get_all_feature_ids_response_cls = VLPFeatureSetModel.get_response_cls(
            self.VERSION, index.GET_ALL_FEATURE_IDS)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``VLPFeatureSetInterface.get_max_function_index``
        return VLPFeatureSetModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class VLPFeatureSetV0


# noinspection DuplicatedCode
class GetCount(VLPFeatureSet):
    """
    Define ``GetCount`` implementation class
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
                         function_index=GetCountResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class GetCount


class GetFeatureID(VLPFeatureSet):
    """
    Define ``GetFeatureID`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Feature Idx                   8
    ============================  ==========
    """

    class FID(VLPFeatureSet.FID):
        # See ``VLPFeatureSet.FID``
        FEATURE_IDX = VLPFeatureSet.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    class LEN(VLPFeatureSet.LEN):
        # See ``VLPFeatureSet.LEN``
        FEATURE_IDX = 0x8
    # end class LEN

    FIELDS = VLPFeatureSet.FIELDS + (
        BitField(fid=FID.FEATURE_IDX, length=LEN.FEATURE_IDX,
                 title="FeatureIdx", name="feature_idx",
                 checks=(CheckHexList(LEN.FEATURE_IDX // 8), CheckByte(),)),)

    def __init__(self, device_index, feature_index, feature_idx, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param feature_idx: Feature Idx
        :type feature_idx: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetFeatureIDResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        feature_idx = HexList(feature_idx)
        self.feature_idx = feature_idx
    # end def __init__
# end class GetFeatureID


class GetAllFeatureIDs(VLPFeatureSet):
    """
    Define ``GetAllFeatureIDs`` implementation class
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
                         function_index=GetAllFeatureIDsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class GetAllFeatureIDs


class GetCountResponse(VLPFeatureSet):
    """
    Define ``GetCountResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Count                         8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCount,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(VLPFeatureSet.FID):
        # See ``VLPFeatureSet.FID``
        COUNT = VLPFeatureSet.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    class LEN(VLPFeatureSet.LEN):
        # See ``VLPFeatureSet.LEN``
        COUNT = 0x8
    # end class LEN

    FIELDS = VLPFeatureSet.FIELDS + (
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, count, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
        self.count = count
    # end def __init__
# end class GetCountResponse


# noinspection DuplicatedCode
class GetFeatureIDResponse(VLPFeatureSet):
    """
    Define ``GetFeatureIDResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Feature Idx                   8
    Feature ID                    16
    Feature Type                  8
    Feature Version               8
    Feature Max Memory            32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFeatureID,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(VLPFeatureSet.FID):
        # See ``VLPFeatureSet.FID``
        FEATURE_IDX = VLPFeatureSet.FID.VLP_SEQUENCE_NUMBER - 1
        FEATURE_ID = FEATURE_IDX - 1
        FEATURE_TYPE = FEATURE_ID - 1
        FEATURE_VERSION = FEATURE_TYPE - 1
        FEATURE_MAX_MEMORY = FEATURE_VERSION - 1
    # end class FID

    class LEN(VLPFeatureSet.LEN):
        # See ``VLPFeatureSet.LEN``
        FEATURE_IDX = 0x8
        FEATURE_ID = 0x10
        FEATURE_TYPE = 0x8
        FEATURE_VERSION = 0x8
        FEATURE_MAX_MEMORY = 0x20
    # end class LEN

    FIELDS = VLPFeatureSet.FIELDS + (
        BitField(fid=FID.FEATURE_IDX, length=LEN.FEATURE_IDX,
                 title="FeatureIdx", name="feature_idx",
                 checks=(CheckHexList(LEN.FEATURE_IDX // 8), CheckByte(),)),
        BitField(fid=FID.FEATURE_ID, length=LEN.FEATURE_ID,
                 title="FeatureId", name="feature_id",
                 checks=(CheckHexList(LEN.FEATURE_ID // 8),)),
        BitField(fid=FID.FEATURE_TYPE, length=LEN.FEATURE_TYPE,
                 title="FeatureType", name="feature_type",),
        BitField(fid=FID.FEATURE_VERSION, length=LEN.FEATURE_VERSION,
                 title="FeatureVersion", name="feature_version",),
        BitField(fid=FID.FEATURE_MAX_MEMORY, length=LEN.FEATURE_MAX_MEMORY,
                 title="FeatureMaxMemory", name="feature_max_memory",
                 checks=(CheckHexList(LEN.FEATURE_MAX_MEMORY // 8),)),
    )

    def __init__(self, device_index, feature_index, feature_idx, feature_id, feature_hidden, feature_version,
                 feature_max_memory, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param feature_idx: Feature Idx
        :type feature_idx: ``HexList``
        :param feature_id: Feature ID
        :type feature_id: ``HexList``
        :param feature_hidden: Feature Hidden
        :type feature_hidden: ``bool | HexList``
        :param feature_version: Feature Version
        :type feature_version: ``int | HexList``
        :param feature_max_memory: Feature Max Memory
        :type feature_max_memory: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        self.feature_idx = feature_idx
        self.feature_id = feature_id
        self.feature_type = self.FeatureType(feature_hidden=feature_hidden)
        self.feature_version = HexList(Numeral(feature_version, self.LEN.FEATURE_VERSION // 8))
        self.feature_max_memory = feature_max_memory
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetFeatureIDResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.feature_type = cls.FeatureType.fromHexList(inner_field_container_mixin.feature_type)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetFeatureIDResponse


class GetAllFeatureIDsResponse(VlpMessageRawPayload):
    """
    Define ``GetAllFeatureIDsResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Variable payload              Variable length
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAllFeatureIDs,)
    VERSION = (0,)
    FUNCTION_INDEX = 2
    FEATURE_ID = 0x0103
# end class GetAllFeatureIDsResponse


# noinspection DuplicatedCode
class GetAllFeatureIDsResponsePayloadMixin(BitFieldContainerMixin):
    """
    Define ``GetAllFeatureIDsResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Feature Records Count         8
    Feature Records Size          8
    Feature Records 1..N          FeatureRecordsSize * FeatureRecordsCount
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAllFeatureIDs,)
    VERSION = (0,)
    FUNCTION_INDEX = 2
    FEATURE_ID = 0x0103

    class FID:
        """
        Field identifiers
        """
        FEATURE_RECORDS_COUNT = 0xFF
        FEATURE_RECORDS_SIZE = FEATURE_RECORDS_COUNT - 1
        FEATURE_RECORDS = FEATURE_RECORDS_SIZE - 1
    # end class FID

    class LEN:
        """
        Field lengths in bits
        """
        FEATURE_RECORDS_COUNT = 0x8
        FEATURE_RECORDS_SIZE = 0x8
        FEATURE_IDX = 0x8
        FEATURE_ID = 0x10
        FEATURE_TYPE = 0x8
        FEATURE_VERSION = 0x8
        FEATURE_MAX_MEMORY = 0x20
    # end class LEN

    FIELDS = (
        BitField(fid=FID.FEATURE_RECORDS_COUNT, length=LEN.FEATURE_RECORDS_COUNT,
                 title="FeatureRecordsCount", name="feature_records_count",
                 checks=(CheckHexList(LEN.FEATURE_RECORDS_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.FEATURE_RECORDS_SIZE, length=LEN.FEATURE_RECORDS_SIZE,
                 title="FeatureRecordsSize", name="feature_records_size",
                 checks=(CheckHexList(LEN.FEATURE_RECORDS_SIZE // 8), CheckByte(),)),
        BitField(fid=FID.FEATURE_RECORDS, title="FeatureRecords", name="feature_records",),)

    def __init__(self, feature_records_count, feature_records_size, **kwargs):
        """
        :param feature_records_count: Feature Records Count
        :type feature_records_count: ``int | HexList``
        :param feature_records_size: Feature Records Size
        :type feature_records_size: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(**kwargs)
        self.feature_records_count = feature_records_count
        self.feature_records_size = feature_records_size
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetAllFeatureIDsResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        # Get the feature count and size from VLP response fields
        feature_records_count = to_int(inner_field_container_mixin.feature_records_count)
        feature_records_size = to_int(inner_field_container_mixin.feature_records_size)
        inner_field_container_mixin.get_field_from_name('feature_records').length = (
                feature_records_size * cls.LEN.FEATURE_RECORDS_SIZE * feature_records_count)
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        # Get feature records information
        feature_records = HexList(str(inner_field_container_mixin.feature_records))
        # Delete the feature_records field
        inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS[:-1]
        current_fid = inner_field_container_mixin.get_field_from_name('feature_records_size').fid
        message_field_start_index = 0
        message_field_end_index = cls.LEN.FEATURE_RECORDS_SIZE // 8

        for feature_idx in range(1, feature_records_count + 1):
            inner_field_container_mixin.FIELDS += (
                BitField(fid=current_fid - 1,
                         length=cls.LEN.FEATURE_IDX,
                         title=f"FeatureIdx{feature_idx}",
                         name=f"feature_idx_{feature_idx}",
                         checks=(CheckHexList(cls.LEN.FEATURE_IDX // 8), CheckByte(),)),
                BitField(fid=current_fid - 2,
                         length=cls.LEN.FEATURE_ID,
                         title=f"FeatureId{feature_idx}",
                         name=f"feature_id_{feature_idx}",
                         checks=(CheckHexList(cls.LEN.FEATURE_ID // 8), CheckByte(),)),
                BitField(fid=current_fid - 3,
                         length=cls.LEN.FEATURE_TYPE,
                         title=f"FeatureType{feature_idx}",
                         name=f"feature_type_{feature_idx}",
                         checks=(CheckHexList(cls.LEN.FEATURE_TYPE // 8), CheckByte(),)),
                BitField(fid=current_fid - 4,
                         length=cls.LEN.FEATURE_VERSION,
                         title=f"FeatureVersion{feature_idx}",
                         name=f"feature_version_{feature_idx}",
                         checks=(CheckHexList(cls.LEN.FEATURE_VERSION // 8), CheckByte(),)),
                BitField(fid=current_fid - 5,
                         length=cls.LEN.FEATURE_MAX_MEMORY,
                         title=f"FeatureMaxMemory{feature_idx}",
                         name=f"feature_max_memory_{feature_idx}",
                         checks=(CheckHexList(cls.LEN.FEATURE_MAX_MEMORY // 8), CheckByte(),))
            )
            current_fid -= 5
            feature_idx_value = feature_records[message_field_start_index: message_field_end_index]
            inner_field_container_mixin.__setattr__(f"feature_idx_{feature_idx}", feature_idx_value)
            message_field_start_index = message_field_end_index
            message_field_end_index += cls.LEN.FEATURE_ID // 8

            feature_id_value = feature_records[message_field_start_index: message_field_end_index]
            inner_field_container_mixin.__setattr__(f"feature_id_{feature_idx}", feature_id_value)
            message_field_start_index = message_field_end_index
            message_field_end_index += cls.LEN.FEATURE_TYPE // 8

            feature_type_value = feature_records[message_field_start_index: message_field_end_index]
            inner_field_container_mixin.__setattr__(f"feature_type_{feature_idx}",
                                                    VLPFeatureSet.FeatureType.fromHexList(feature_type_value))
            message_field_start_index = message_field_end_index
            message_field_end_index += cls.LEN.FEATURE_VERSION // 8

            feature_version_value = feature_records[message_field_start_index: message_field_end_index]
            inner_field_container_mixin.__setattr__(f"feature_version_{feature_idx}", feature_version_value)
            message_field_start_index = message_field_end_index
            message_field_end_index += cls.LEN.FEATURE_MAX_MEMORY // 8

            feature_max_memory_value = feature_records[message_field_start_index: message_field_end_index]
            inner_field_container_mixin.__setattr__(f"feature_max_memory_{feature_idx}", feature_max_memory_value)
            message_field_start_index = message_field_end_index
            message_field_end_index += cls.LEN.FEATURE_IDX // 8
        # end for

        return inner_field_container_mixin
    # end def fromHexList
# end class GetAllFeatureIDsResponsePayloadMixin

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
