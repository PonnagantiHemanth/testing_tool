#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.configurableproperties
:brief: HID++ 2.0 ``ConfigurableProperties`` command interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.field import CheckList
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurableProperties(HidppMessage):
    """
    The purpose of this feature is to configure some properties of the device
    during production.  It is meant to replace HID++ Feature 0x1806.
    """
    FEATURE_ID = 0x1807
    MAX_FUNCTION_INDEX_V0 = 4
    MAX_FUNCTION_INDEX_V1 = 4
    MAX_FUNCTION_INDEX_V2 = 4
    MAX_FUNCTION_INDEX_V3 = 4
    MAX_FUNCTION_INDEX_V4 = 4

    class PropertyId(IntEnum):
        """
        Property identifiers
        """
        # since v0
        EXTENDED_MODEL_ID = 1
        KEYBOARD_LAYOUT = 2
        RGB_LED_BIN_INFORMATION_ZONE0 = 3
        RGB_LED_BIN_INFORMATION_ZONE1 = 4
        EQUAD_DEVICE_NAME = 5
        RESERVED_1 = 6
        BLE_GAP_ADV_SERVICE_DATA = 7
        BLE_GAP_ADV_OUTPUT_POWER = 8
        RGB_LED_BIN_INFORMATION_ZONE2 = 9
        RESERVED_2 = 10
        SERIAL_NUMBER = 11
        CAR_SIMULATOR_PEDALS_TYPES = 12
        RGB_LED_ZONE_INTENSITY = 13
        RGB_LED_DRIVER_ID = 14
        HIDPP_DEVICE_NAME = 31
        EQUAD_ID = 32
        USB_VID = 33
        USB_BL_PID = 34
        USB_APP_PID = 35
        USB_MANUFACTURER_STRING = 36
        USB_BL_PRODUCT_STRING = 37
        USB_APP_PRODUCT_STRING = 38
        BLE_GAP_BL_NAME = 39
        BLE_GAP_APP_NAME = 40
        BLE_GAP_BL_ADV_NAME_SIZE = 41
        BLE_GAP_APP_ADV_NAME_SIZE = 42
        BLE_GAP_BL_SR_NAME_SIZE = 43
        BLE_GAP_APP_SR_NAME_SIZE = 44
        BLE_DIS_VID = 45
        BLE_DIS_BL_PID = 46
        BLE_DIS_APP_PID = 47
        BLE_DIS_MANUFACTURER_NAME = 48
        BLE_DIS_BL_MODEL_NUMBER = 49
        BLE_DIS_APP_MODEL_NUMBER = 50
        HW_VERSION = 51
        SOFTWARE_EXTRA_INFORMATION = 52

        # since v1
        PART_NUMBER = 53
        REGULATORY_MODEL_NUMBER = 54

        # since v2
        RGB_LED_BIN_INFORMATION_ZONE3 = 55
        RGB_LED_BIN_INFORMATION_ZONE4 = 56

        # since v3
        DISABLE_EASY_PAIRING = 57

        # since v4
        HARDWARE_BUILD = 58
        FIRMWARE_EXTRA_INFORMATION = 59
        GAMING_WIRELESS_REPORT_RATE = 60

        # Reserved (not yet used) 15 to 30
        # Reserved (not yet used) 58 to 255

        # general values
        INVALID = 0
        DESELECT_ALL = 0
        MIN = EXTENDED_MODEL_ID
        MAX = 255
    # end class PropertyId

    class PropertyIdV0(object):
        RESERVED_1 = 6
        RESERVED_2 = 10
        RESERVED_RANGE_1_START = 15
        RESERVED_RANGE_1_END = 30
        RESERVED_RANGE_2_START = 53
        RESERVED_RANGE_2_END = 255
    # end class PropertyIdV0

    class PropertyIdV1(PropertyIdV0):
        RESERVED_RANGE_2_START = 55
    # end class PropertyIdV1

    class PropertyIdV2(PropertyIdV1):
        RESERVED_RANGE_2_START = 57
    # end class PropertyIdV2

    class PropertyIdV3(PropertyIdV2):
        RESERVED_RANGE_2_START = 58
    # end class PropertyIdV3

    class PropertyIdV4(PropertyIdV3):
        RESERVED_RANGE_2_START = 61
    # end class PropertyIdV4

    class PropertyDefaultSize(IntEnum):
        """
        Property default sizes, if defined (in Bytes)
        """
        MIN = 1
        EXTENDED_MODEL_ID = 1
        KEYBOARD_LAYOUT = 1
        RGB_LED_BIN_INFORMATION_ZONE0 = 64
        RGB_LED_BIN_INFORMATION_ZONE1 = 64
        EQUAD_DEVICE_NAME = 14
        BLE_GAP_ADV_SERVICE_DATA = 14
        BLE_GAP_ADV_OUTPUT_POWER = 1
        RGB_LED_BIN_INFORMATION_ZONE2 = 64
        SERIAL_NUMBER = 12
        CAR_SIMULATOR_PEDALS_TYPES = 3
        RGB_LED_ZONE_INTENSITY = 64
        RGB_LED_DRIVER_ID = 1
        EQUAD_ID = 2
        USB_PRODUCT_ID = 2
        BLE_GAP_ADV_NAME = 14
        BLE_DIS_PRODUCT_ID = 2
        USB_VID = 2
        USB_BL_PID = 2
        USB_APP_PID = 2
        BLE_GAP_BL_ADV_NAME_SIZE = 1
        BLE_GAP_APP_ADV_NAME_SIZE = 1
        BLE_GAP_BL_SR_NAME_SIZE = 1
        BLE_GAP_APP_SR_NAME_SIZE = 1
        BLE_DIS_VID = 2
        BLE_DIS_BL_PID = 2
        BLE_DIS_APP_PID = 2
        HW_VERSION = 2
        PART_NUMBER = 10
        REGULATORY_MODEL_NUMBER = 6
        RGB_LED_BIN_INFORMATION_ZONE3 = 64
        RGB_LED_BIN_INFORMATION_ZONE4 = 64
        DISABLE_EASY_PAIRING = 1
        HARDWARE_BUILD = 2
        GAMING_WIRELESS_REPORT_RATE = 2
    # end class PropertyDefaultSize

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

    # noinspection DuplicatedCode
    class FlagsMaskBitMap(BitFieldContainerMixin):
        """
        Define ``FlagsMaskBitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      5
        Corrupted                     1
        Present                       1
        Supported                     1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            CORRUPTED = RESERVED - 1
            PRESENT = CORRUPTED - 1
            SUPPORTED = PRESENT - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x5
            CORRUPTED = 0x1
            PRESENT = 0x1
            SUPPORTED = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            CORRUPTED = 0x0
            PRESENT = 0x0
            SUPPORTED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.CORRUPTED, length=LEN.CORRUPTED,
                     title="Corrupted", name="corrupted",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.CORRUPTED) - 1),),
                     default_value=DEFAULT.CORRUPTED),
            BitField(fid=FID.PRESENT, length=LEN.PRESENT,
                     title="Present", name="present",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRESENT) - 1),),
                     default_value=DEFAULT.PRESENT),
            BitField(fid=FID.SUPPORTED, length=LEN.SUPPORTED,
                     title="Supported", name="supported",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.SUPPORTED) - 1),),
                     default_value=DEFAULT.SUPPORTED),
        )
    # end class FlagsMaskBitMap
# end class ConfigurableProperties


# noinspection DuplicatedCode
class ConfigurablePropertiesModel(FeatureModel):
    """
    Define ``ConfigurableProperties`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_PROPERTY_INFO = 0
        SELECT_PROPERTY = 1
        READ_PROPERTY = 2
        WRITE_PROPERTY = 3
        DELETE_PROPERTY = 4
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ConfigurableProperties`` feature data model

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
                },
                cls.INDEX.WRITE_PROPERTY: {
                    "request": WriteProperty,
                    "response": WritePropertyResponse
                },
                cls.INDEX.DELETE_PROPERTY: {
                    "request": DeleteProperty,
                    "response": DeletePropertyResponse
                }
            }
        }

        return {
            "feature_base": ConfigurableProperties,
            "versions": {
                ConfigurablePropertiesV0.VERSION: {
                    "main_cls": ConfigurablePropertiesV0,
                    "api": function_map
                },
                ConfigurablePropertiesV1.VERSION: {
                    "main_cls": ConfigurablePropertiesV1,
                    "api": function_map
                },
                ConfigurablePropertiesV2.VERSION: {
                    "main_cls": ConfigurablePropertiesV2,
                    "api": function_map
                },
                ConfigurablePropertiesV3.VERSION: {
                    "main_cls": ConfigurablePropertiesV3,
                    "api": function_map
                },
                ConfigurablePropertiesV4.VERSION: {
                    "main_cls": ConfigurablePropertiesV4,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class ConfigurablePropertiesModel


class ConfigurablePropertiesFactory(FeatureFactory):
    """
    Get ``ConfigurableProperties`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ConfigurableProperties`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``ConfigurablePropertiesInterface``
        """
        return ConfigurablePropertiesModel.get_main_cls(version)()
    # end def create
# end class ConfigurablePropertiesFactory


class ConfigurablePropertiesInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ConfigurableProperties``
    """

    def __init__(self):
        # Requests
        self.get_property_info_cls = None
        self.select_property_cls = None
        self.read_property_cls = None
        self.write_property_cls = None
        self.delete_property_cls = None

        # Responses
        self.get_property_info_response_cls = None
        self.select_property_response_cls = None
        self.read_property_response_cls = None
        self.write_property_response_cls = None
        self.delete_property_response_cls = None
    # end def __init__
# end class ConfigurablePropertiesInterface


class ConfigurablePropertiesV0(ConfigurablePropertiesInterface):
    """
    Define ``ConfigurablePropertiesV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getPropertyInfo(propertyId) -> flags, size

    [1] selectProperty(propertyId, rdOffset, wrOffset) -> None

    [2] readProperty() -> data

    [3] writeProperty(data) -> None

    [4] deleteProperty(propertyId) -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``ConfigurableProperties.__init__``
        super().__init__()
        index = ConfigurablePropertiesModel.INDEX

        # Requests
        self.get_property_info_cls = ConfigurablePropertiesModel.get_request_cls(
            self.VERSION, index.GET_PROPERTY_INFO)
        self.select_property_cls = ConfigurablePropertiesModel.get_request_cls(
            self.VERSION, index.SELECT_PROPERTY)
        self.read_property_cls = ConfigurablePropertiesModel.get_request_cls(
            self.VERSION, index.READ_PROPERTY)
        self.write_property_cls = ConfigurablePropertiesModel.get_request_cls(
            self.VERSION, index.WRITE_PROPERTY)
        self.delete_property_cls = ConfigurablePropertiesModel.get_request_cls(
            self.VERSION, index.DELETE_PROPERTY)

        # Responses
        self.get_property_info_response_cls = ConfigurablePropertiesModel.get_response_cls(
            self.VERSION, index.GET_PROPERTY_INFO)
        self.select_property_response_cls = ConfigurablePropertiesModel.get_response_cls(
            self.VERSION, index.SELECT_PROPERTY)
        self.read_property_response_cls = ConfigurablePropertiesModel.get_response_cls(
            self.VERSION, index.READ_PROPERTY)
        self.write_property_response_cls = ConfigurablePropertiesModel.get_response_cls(
            self.VERSION, index.WRITE_PROPERTY)
        self.delete_property_response_cls = ConfigurablePropertiesModel.get_response_cls(
            self.VERSION, index.DELETE_PROPERTY)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ConfigurablePropertiesInterface.get_max_function_index``
        return ConfigurablePropertiesModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class ConfigurablePropertiesV0


class ConfigurablePropertiesV1(ConfigurablePropertiesV0):
    """
    Define ``ConfigurablePropertiesV1`` feature

    This feature provides model and unit specific information for version 1
    """
    VERSION = 1

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ConfigurablePropertiesInterface.get_max_function_index``
        return ConfigurablePropertiesModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class ConfigurablePropertiesV1


class ConfigurablePropertiesV2(ConfigurablePropertiesV1):
    """
    Define ``ConfigurablePropertiesV2`` feature

    This feature provides model and unit specific information for version 2
    """
    VERSION = 2

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ConfigurablePropertiesInterface.get_max_function_index``
        return ConfigurablePropertiesModel.get_base_cls().MAX_FUNCTION_INDEX_V2
    # end def get_max_function_index
# end class ConfigurablePropertiesV2


class ConfigurablePropertiesV3(ConfigurablePropertiesV2):
    """
    Define ``ConfigurablePropertiesV3`` feature

    This feature provides model and unit specific information for version 3
    """
    VERSION = 3

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ConfigurablePropertiesInterface.get_max_function_index``
        return ConfigurablePropertiesModel.get_base_cls().MAX_FUNCTION_INDEX_V3
    # end def get_max_function_index
# end class ConfigurablePropertiesV3


class ConfigurablePropertiesV4(ConfigurablePropertiesV3):
    """
    Define ``ConfigurablePropertiesV4`` feature

    This feature provides model and unit specific information for version 4
    """
    VERSION = 4

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ConfigurablePropertiesInterface.get_max_function_index``
        return ConfigurablePropertiesModel.get_base_cls().MAX_FUNCTION_INDEX_V4
    # end def get_max_function_index
# end class ConfigurablePropertiesV4


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(ConfigurableProperties):
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

    class FID(ConfigurableProperties.FID):
        # See ``ConfigurableProperties.FID``
        PADDING = ConfigurableProperties.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableProperties.LEN):
        # See ``ConfigurableProperties.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ConfigurableProperties.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableProperties.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(ConfigurableProperties):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - DeletePropertyResponse
        - SelectPropertyResponse
        - WritePropertyResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(ConfigurableProperties.FID):
        # See ``ConfigurableProperties.FID``
        PADDING = ConfigurableProperties.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableProperties.LEN):
        # See ``ConfigurableProperties.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ConfigurableProperties.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableProperties.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class PropertyIdWithPaddingContainer(ConfigurableProperties):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - DeleteProperty
        - GetPropertyInfo

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Property Id                   8
    Padding                       16
    ============================  ==========
    """

    class FID(ConfigurableProperties.FID):
        # See ``ConfigurableProperties.FID``
        PROPERTY_ID = ConfigurableProperties.FID.SOFTWARE_ID - 1
        PADDING = PROPERTY_ID - 1
    # end class FID

    class LEN(ConfigurableProperties.LEN):
        # See ``ConfigurableProperties.LEN``
        PROPERTY_ID = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ConfigurableProperties.FIELDS + (
        BitField(fid=FID.PROPERTY_ID, length=LEN.PROPERTY_ID,
                 title="PropertyId", name="property_id",
                 checks=(CheckHexList(LEN.PROPERTY_ID // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableProperties.DEFAULT.PADDING),
    )
# end class PropertyIdWithPaddingContainer


class DataContainer(ConfigurableProperties):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - ReadPropertyResponse
        - WriteProperty

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Data                          128
    ============================  ==========
    """

    class FID(ConfigurableProperties.FID):
        # See ``ConfigurableProperties.FID``
        DATA = ConfigurableProperties.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableProperties.LEN):
        # See ``ConfigurableProperties.LEN``
        DATA = 0x80
    # end class LEN

    FIELDS = ConfigurableProperties.FIELDS + (
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),
                         CheckList(length=LEN.DATA // 8),)),
    )
# end class DataContainer


# noinspection DuplicatedCode
class GetPropertyInfo(PropertyIdWithPaddingContainer):
    """
    Define ``GetPropertyInfo`` implementation class
    """

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


class SelectProperty(ConfigurableProperties):
    """
    Define ``SelectProperty`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Property Id                   8
    Rd Offset                     16
    Wr Offset                     16
    Padding                       88
    ============================  ==========
    """

    class FID(ConfigurableProperties.FID):
        # See ``ConfigurableProperties.FID``
        PROPERTY_ID = ConfigurableProperties.FID.SOFTWARE_ID - 1
        RD_OFFSET = PROPERTY_ID - 1
        WR_OFFSET = RD_OFFSET - 1
        PADDING = WR_OFFSET - 1
    # end class FID

    class LEN(ConfigurableProperties.LEN):
        # See ``ConfigurableProperties.LEN``
        PROPERTY_ID = 0x8
        RD_OFFSET = 0x10
        WR_OFFSET = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = ConfigurableProperties.FIELDS + (
        BitField(fid=FID.PROPERTY_ID, length=LEN.PROPERTY_ID,
                 title="PropertyId", name="property_id",
                 checks=(CheckHexList(LEN.PROPERTY_ID // 8), CheckByte(),)),
        BitField(fid=FID.RD_OFFSET, length=LEN.RD_OFFSET,
                 title="RdOffset", name="rd_offset",
                 checks=(CheckHexList(LEN.RD_OFFSET // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RD_OFFSET) - 1),)),
        BitField(fid=FID.WR_OFFSET, length=LEN.WR_OFFSET,
                 title="WrOffset", name="wr_offset",
                 checks=(CheckHexList(LEN.WR_OFFSET // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.WR_OFFSET) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableProperties.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, property_id, rd_offset=0, wr_offset=0, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param property_id: Property identifier [1 to 255] or 0 to deselect all properties
        :type property_id: ``int | HexList``
        :param rd_offset: Property read offset in bytes - OPTIONAL
        :type rd_offset: ``int | HexList``
        :param wr_offset: Property write offset in bytes - OPTIONAL
        :type wr_offset: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SelectPropertyResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.property_id = HexList(Numeral(property_id, self.LEN.PROPERTY_ID // 8))
        self.rd_offset = HexList(Numeral(rd_offset, self.LEN.RD_OFFSET // 8))
        self.wr_offset = HexList(Numeral(wr_offset, self.LEN.WR_OFFSET // 8))
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


class WriteProperty(DataContainer):
    """
    Define ``WriteProperty`` implementation class
    """

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
                         function_index=WritePropertyResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data = HexList(Numeral(data, self.LEN.DATA // 8))
    # end def __init__
# end class WriteProperty


class DeleteProperty(PropertyIdWithPaddingContainer):
    """
    Define ``DeleteProperty`` implementation class
    """

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
                         function_index=DeletePropertyResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.property_id = HexList(Numeral(property_id, self.LEN.PROPERTY_ID // 8))
    # end def __init__
# end class DeleteProperty


# noinspection DuplicatedCode
class GetPropertyInfoResponse(ConfigurableProperties):
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
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 0

    class FID(ConfigurableProperties.FID):
        # See ``ConfigurableProperties.FID``
        FLAGS = ConfigurableProperties.FID.SOFTWARE_ID - 1
        SIZE = FLAGS - 1
        PADDING = SIZE - 1
    # end class FID

    class LEN(ConfigurableProperties.LEN):
        # See ``ConfigurableProperties.LEN``
        FLAGS = 0x8
        SIZE = 0x10
        PADDING = 0x68
    # end class LEN

    FIELDS = ConfigurableProperties.FIELDS + (
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
                 default_value=ConfigurableProperties.DEFAULT.PADDING),
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
    VERSION = (0, 1, 2, 3, 4,)
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


class ReadPropertyResponse(DataContainer):
    """
    Define ``ReadPropertyResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadProperty,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 2

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


class WritePropertyResponse(LongEmptyPacketDataFormat):
    """
    Define ``WritePropertyResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteProperty,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 3

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
# end class WritePropertyResponse


class DeletePropertyResponse(LongEmptyPacketDataFormat):
    """
    Define ``DeletePropertyResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (DeleteProperty,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 4

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
# end class DeletePropertyResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
