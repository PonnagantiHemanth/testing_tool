#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.propertyaccess
:brief: HID++ 2.0 ``PropertyAccess`` command interface definition
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.field import CheckList
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PropertyAccess(HidppMessage):
    """
    The purpose of this feature is to provide read access to some properties of the device
    """
    FEATURE_ID = 0x0011
    MAX_FUNCTION_INDEX_V0 = 2

    PropertyId = ConfigurableProperties.PropertyId

    PropertyDefaultSize = ConfigurableProperties.PropertyDefaultSize

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    FlagsMaskBitMap = ConfigurableProperties.FlagsMaskBitMap
# end class PropertyAccess


# noinspection DuplicatedCode
class PropertyAccessModel(FeatureModel):
    """
    Define ``PropertyAccess`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_PROPERTY_INFO = 0
        SELECT_PROPERTY = 1
        READ_PROPERTY = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``PropertyAccess`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_PROPERTY_INFO: {
                    "request": GetPropertyInfo,
                    "response": GetPropertyInfoResponse
                },
                cls.INDEX.SELECT_PROPERTY: {
                    "request": SelectProperty,
                    "response": SelectPropertyResponse
                },
                cls.INDEX.READ_PROPERTY: {
                    "request": ReadProperty,
                    "response": ReadPropertyResponse
                }
            }
        }

        return {
            "feature_base": PropertyAccess,
            "versions": {
                PropertyAccessV0.VERSION: {
                    "main_cls": PropertyAccessV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class PropertyAccessModel


class PropertyAccessFactory(FeatureFactory):
    """
    Get ``PropertyAccess`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``PropertyAccess`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``PropertyAccessInterface``
        """
        return PropertyAccessModel.get_main_cls(version)()
    # end def create
# end class PropertyAccessFactory


class PropertyAccessInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``PropertyAccess``
    """

    def __init__(self):
        # Requests
        self.get_property_info_cls = None
        self.select_property_cls = None
        self.read_property_cls = None

        # Responses
        self.get_property_info_response_cls = None
        self.select_property_response_cls = None
        self.read_property_response_cls = None
    # end def __init__
# end class PropertyAccessInterface


class PropertyAccessV0(PropertyAccessInterface):
    """
    Define ``PropertyAccessV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getPropertyInfo(propertyId) -> flags, size

    [1] selectProperty(propertyId, rdOffset) -> None

    [2] readProperty() -> data
    """
    VERSION = 0

    def __init__(self):
        # See ``PropertyAccess.__init__``
        super().__init__()
        index = PropertyAccessModel.INDEX

        # Requests
        self.get_property_info_cls = PropertyAccessModel.get_request_cls(
            self.VERSION, index.GET_PROPERTY_INFO)
        self.select_property_cls = PropertyAccessModel.get_request_cls(
            self.VERSION, index.SELECT_PROPERTY)
        self.read_property_cls = PropertyAccessModel.get_request_cls(
            self.VERSION, index.READ_PROPERTY)

        # Responses
        self.get_property_info_response_cls = PropertyAccessModel.get_response_cls(
            self.VERSION, index.GET_PROPERTY_INFO)
        self.select_property_response_cls = PropertyAccessModel.get_response_cls(
            self.VERSION, index.SELECT_PROPERTY)
        self.read_property_response_cls = PropertyAccessModel.get_response_cls(
            self.VERSION, index.READ_PROPERTY)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``PropertyAccessInterface.get_max_function_index``
        return PropertyAccessModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class PropertyAccessV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(PropertyAccess):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - ReadProperty

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(PropertyAccess.FID):
        # See ``PropertyAccess.FID``
        PADDING = PropertyAccess.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PropertyAccess.LEN):
        # See ``PropertyAccess.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = PropertyAccess.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PropertyAccess.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(PropertyAccess):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SelectPropertyResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(PropertyAccess.FID):
        # See ``PropertyAccess.FID``
        PADDING = PropertyAccess.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PropertyAccess.LEN):
        # See ``PropertyAccess.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = PropertyAccess.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PropertyAccess.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


# noinspection DuplicatedCode
class GetPropertyInfo(PropertyAccess):
    """
    Define ``GetPropertyInfo`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Property Id                   8
    Padding                       16
    ============================  ==========
    """

    class FID(PropertyAccess.FID):
        # See ``PropertyAccess.FID``
        PROPERTY_ID = PropertyAccess.FID.SOFTWARE_ID - 1
        PADDING = PROPERTY_ID - 1
    # end class FID

    class LEN(PropertyAccess.LEN):
        # See ``PropertyAccess.LEN``
        PROPERTY_ID = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = PropertyAccess.FIELDS + (
        BitField(fid=FID.PROPERTY_ID, length=LEN.PROPERTY_ID,
                 title="PropertyId", name="property_id",
                 checks=(CheckHexList(LEN.PROPERTY_ID // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PropertyAccess.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, property_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param property_id: Property identifier
        :type property_id: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetPropertyInfoResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.property_id = HexList(Numeral(property_id, self.LEN.PROPERTY_ID // 8))
    # end def __init__
# end class GetPropertyInfo


class SelectProperty(PropertyAccess):
    """
    Define ``SelectProperty`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Property Id                   8
    Rd Offset                     16
    ============================  ==========
    """

    class FID(PropertyAccess.FID):
        # See ``PropertyAccess.FID``
        PROPERTY_ID = PropertyAccess.FID.SOFTWARE_ID - 1
        RD_OFFSET = PROPERTY_ID - 1
    # end class FID

    class LEN(PropertyAccess.LEN):
        # See ``PropertyAccess.LEN``
        PROPERTY_ID = 0x8
        RD_OFFSET = 0x10
    # end class LEN

    FIELDS = PropertyAccess.FIELDS + (
        BitField(fid=FID.PROPERTY_ID, length=LEN.PROPERTY_ID,
                 title="PropertyId", name="property_id",
                 checks=(CheckHexList(LEN.PROPERTY_ID // 8), CheckByte(),)),
        BitField(fid=FID.RD_OFFSET, length=LEN.RD_OFFSET,
                 title="RdOffset", name="rd_offset",
                 checks=(CheckHexList(LEN.RD_OFFSET // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RD_OFFSET) - 1),)),
    )

    def __init__(self, device_index, feature_index, property_id, rd_offset, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param property_id: Property identifier [1 to 255] or 0 to deselect all properties
        :type property_id: ``int | HexList``
        :param rd_offset: Property read offset in bytes
        :type rd_offset: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SelectPropertyResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.property_id = HexList(Numeral(property_id, self.LEN.PROPERTY_ID // 8))
        self.rd_offset = HexList(Numeral(rd_offset, self.LEN.RD_OFFSET // 8))
    # end def __init__
# end class SelectProperty


class ReadProperty(ShortEmptyPacketDataFormat):
    """
    Define ``ReadProperty`` implementation class
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
                         function_index=ReadPropertyResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ReadProperty


# noinspection DuplicatedCode
class GetPropertyInfoResponse(PropertyAccess):
    """
    Define ``GetPropertyInfoResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Flags                         8
    Size                          16
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPropertyInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(PropertyAccess.FID):
        # See ``PropertyAccess.FID``
        FLAGS = PropertyAccess.FID.SOFTWARE_ID - 1
        SIZE = FLAGS - 1
        PADDING = SIZE - 1
    # end class FID

    class LEN(PropertyAccess.LEN):
        # See ``PropertyAccess.LEN``
        FLAGS = 0x8
        SIZE = 0x10
        PADDING = 0x68
    # end class LEN

    FIELDS = PropertyAccess.FIELDS + (
        BitField(fid=FID.FLAGS, length=LEN.FLAGS,
                 title="Flags", name="flags",
                 checks=(CheckHexList(LEN.FLAGS // 8), CheckByte(),)),
        BitField(fid=FID.SIZE, length=LEN.SIZE,
                 title="Size", name="size",
                 checks=(CheckHexList(LEN.SIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SIZE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PropertyAccess.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, corrupted=0, present=0, supported=0, size=0, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param corrupted: Corrupted property. When set to 1, the property is corrupted. When set to 0, it is valid -
                          OPTIONAL.
        :type corrupted: ``bool | HexList``
        :param present: Present property. When set to 1, the property is present. When set to 0, it does not exist -
                        OPTIONAL.
        :type present: ``bool | HexList``
        :param supported: Supported property. When set to 1, the property is supported. When set to 0, it is not
                          supported - OPTIONAL.
        :type supported: ``bool | HexList``
        :param size: Property size in bytes - OPTIONAL
        :type size: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.flags = self.FlagsMaskBitMap(corrupted=corrupted,
                                          present=present,
                                          supported=supported)
        self.size = HexList(Numeral(size, self.LEN.SIZE // 8))
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
        :rtype: ``GetPropertyInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.flags = cls.FlagsMaskBitMap.fromHexList(
            inner_field_container_mixin.flags)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetPropertyInfoResponse


class SelectPropertyResponse(LongEmptyPacketDataFormat):
    """
    Define ``SelectPropertyResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SelectProperty,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

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
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SelectPropertyResponse


class ReadPropertyResponse(PropertyAccess):
    """
    Define ``ReadPropertyResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Data                          128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadProperty,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(PropertyAccess.FID):
        # See ``PropertyAccess.FID``
        DATA = PropertyAccess.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PropertyAccess.LEN):
        # See ``PropertyAccess.LEN``
        DATA = 0x80
    # end class LEN

    FIELDS = PropertyAccess.FIELDS + (
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),
                         CheckList(length=LEN.DATA // 8),)),
    )

    def __init__(self, device_index, feature_index, data, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param data: Property data
        :type data: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data = HexList(Numeral(data, self.LEN.DATA // 8))
    # end def __init__
# end class ReadPropertyResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
