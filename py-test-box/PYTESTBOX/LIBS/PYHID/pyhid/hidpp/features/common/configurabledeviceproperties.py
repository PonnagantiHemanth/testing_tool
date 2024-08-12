#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.configurabledeviceproperties
:brief: HID++ 2.0 Configurable Device Properties command interface definition
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/01/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurableDeviceProperties(HidppMessage):
    """
    This feature sets in the device non volatile memory configurable attributes for a given model.

    This feature is only available when manufacturing mode is enabled.

    The purpose of this feature is to set the device’s marketing name and properties on the manufacturing line.

    The  device’s marketing name is the one shown on the device’s packaging.

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
    FEATURE_ID = 0x1806
    MAX_FUNCTION_INDEX = 5

    class PropertyIdV6(object):
        """
        Device Properties Layouts
        """
        EXTENDED_MODEL_ID = 1
        KEYBOARD_INTERNATIONAL_LAYOUT = 2
        RGB_LEDBIN_INFORMATION_BACKUP_ZONE0 = 3
        RGB_LEDBIN_INFORMATION_BACKUP_ZONE1 = 4
        EQUAD_SHORT_NAME = 5
        BLE_SHORT_NAME = 6
        BLE_AD_SERVICE_DATA = 7
        BLE_AD_TX_OUTPUT_POWER_DBM = 8
        RGB_LEDBIN_INFORMATION_BACKUP_ZONE2 = 9
        BLE_LONG_NAME = 10

        @classmethod
        def get_max_id(cls):
            """
            Get the maximum of the ids

            :return: Max id of the properties
            :rtype: ``int``
            """
            return cls.BLE_LONG_NAME
        # end def get_max_id

        @classmethod
        def get_all_ids(cls):
            """
            Get all of the ids

            :return: List of ids
            :rtype: ``List``
            """
            return [cls.EXTENDED_MODEL_ID,
                    cls.KEYBOARD_INTERNATIONAL_LAYOUT,
                    cls.RGB_LEDBIN_INFORMATION_BACKUP_ZONE0,
                    cls.RGB_LEDBIN_INFORMATION_BACKUP_ZONE1,
                    cls.EQUAD_SHORT_NAME,
                    cls.BLE_SHORT_NAME,
                    cls.BLE_AD_SERVICE_DATA,
                    cls.BLE_AD_TX_OUTPUT_POWER_DBM,
                    cls.RGB_LEDBIN_INFORMATION_BACKUP_ZONE2,
                    cls.BLE_LONG_NAME]
        # end def get_all_ids
    # end class PropertyIdV6

    class PropertyIdV7(PropertyIdV6):
        """
        Device Properties Layouts
        """
        SERIAL_NUMBER = 11

        @classmethod
        def get_max_id(cls):
            """
            Get the maximum of the ids

            :return: Max id of the properties
            :rtype: ``int``
            """
            return cls.SERIAL_NUMBER
        # end def get_max_id

        @classmethod
        def get_all_ids(cls):
            """
            Get all of the ids

            :return: List of ids
            :rtype: ``List``
            """
            return super().get_all_ids() + [cls.SERIAL_NUMBER]
        # end def get_all_ids
    # end class PropertyIdV7

    class PropertyIdV8(PropertyIdV7):
        """
        Device Properties Layouts
        """
        CAR_SIMULATOR_PEDALS_TYPES = 12

        @classmethod
        def get_max_id(cls):
            """
            Get the maximum of the ids

            :return: Max id of the properties
            :rtype: ``int``
            """
            return cls.CAR_SIMULATOR_PEDALS_TYPES
        # end def get_max_id

        @classmethod
        def get_all_ids(cls):
            """
            Get all of the ids

            :return: List of ids
            :rtype: ``List``
            """
            return super().get_all_ids() + [cls.CAR_SIMULATOR_PEDALS_TYPES]
        # end def get_all_ids
    # end class PropertyIdV8

    class PropertySizeV6(object):
        """
        Device Properties sizes (Bytes)
        """
        EXTENDED_MODEL_ID = 1
        KEYBOARD_INTERNATIONAL_LAYOUT = 1
        RGB_LEDBIN_INFORMATION_BACKUP_ZONE0 = 64
        RGB_LEDBIN_INFORMATION_BACKUP_ZONE1 = 64
        EQUAD_SHORT_NAME = 14
        BLE_SHORT_NAME = 14
        BLE_AD_SERVICE_DATA = 14
        BLE_AD_TX_OUTPUT_POWER_DBM = 1
        RGB_LEDBIN_INFORMATION_BACKUP_ZONE2 = 64
        BLE_LONG_NAME = 18

        @classmethod
        def get_all_sizes(cls):
            return [cls.EXTENDED_MODEL_ID,
                    cls.KEYBOARD_INTERNATIONAL_LAYOUT,
                    cls.RGB_LEDBIN_INFORMATION_BACKUP_ZONE0,
                    cls.RGB_LEDBIN_INFORMATION_BACKUP_ZONE1,
                    cls.EQUAD_SHORT_NAME,
                    cls.BLE_SHORT_NAME,
                    cls.BLE_AD_SERVICE_DATA,
                    cls.BLE_AD_TX_OUTPUT_POWER_DBM,
                    cls.RGB_LEDBIN_INFORMATION_BACKUP_ZONE2,
                    cls.BLE_LONG_NAME]
        # end def get_all_sizes
    # end class PropertySizeV6

    class PropertySizeV7(PropertySizeV6):
        """
        Device Properties sizes (Bytes)
        """
        SERIAL_NUMBER = 12

        @classmethod
        def get_all_sizes(cls):
            return super().get_all_sizes() + [cls.SERIAL_NUMBER]
        # end def get_all_sizes
    # end class PropertySizeV7

    class PropertySizeV8(PropertySizeV7):
        """
        Device Properties sizes (Bytes)
        """
        CAR_SIMULATOR_PEDALS_TYPES = 3

        @classmethod
        def get_all_sizes(cls):
            return super().get_all_sizes() + [cls.CAR_SIMULATOR_PEDALS_TYPES]
        # end def get_all_sizes
    # end class PropertySizeV8

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class ConfigurableDeviceProperties


class ConfigurableDevicePropertiesModel(FeatureModel):
    """
    ConfigurableDeviceProperties feature model
    """
    class INDEX(object):
        """
        Functions index
        """
        GET_DEVICE_NAME_MAX_COUNT = 0
        SET_DEVICE_NAME = 1
        SET_DEVICE_NAME_COMMIT = 2
        SET_DEVICE_EXTEND_MODEL_ID = 3
        SET_DEVICE_PROPERTIES = 4
        GET_DEVICE_PROPERTIES = 5
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        ConfigurableDeviceProperties feature data model
        """
        api_v6_to_v8 = {
                "functions": {
                        cls.INDEX.GET_DEVICE_NAME_MAX_COUNT: {
                                "request": GetDeviceNameMaxCountV6ToV8,
                                "response": GetDeviceNameMaxCountResponseV6ToV8
                        },
                        cls.INDEX.SET_DEVICE_NAME: {
                                "request": SetDeviceNameV6ToV8,
                                "response": SetDeviceNameResponseV6ToV8
                        },
                        cls.INDEX.SET_DEVICE_NAME_COMMIT: {
                                "request": SetDeviceNameCommitV6ToV8,
                                "response": SetDeviceNameCommitResponseV6ToV8
                        },
                        cls.INDEX.SET_DEVICE_EXTEND_MODEL_ID: {
                                "request": SetDeviceExtendModelIdV6ToV8,
                                "response": SetDeviceExtendModelIdResponseV6ToV8
                        },
                        cls.INDEX.SET_DEVICE_PROPERTIES: {
                                "request": SetDevicePropertiesV6ToV8,
                                "response": SetDevicePropertiesResponseV6ToV8
                        },
                        cls.INDEX.GET_DEVICE_PROPERTIES: {
                                "request": GetDevicePropertiesV6ToV8,
                                "response": GetDevicePropertiesResponseV6ToV8
                        },
                }
        }

        return {
                "feature_base": ConfigurableDeviceProperties,
                "versions": {
                        ConfigurableDevicePropertiesV6.VERSION: {
                                "main_cls": ConfigurableDevicePropertiesV6,
                                "api": api_v6_to_v8
                        },
                        ConfigurableDevicePropertiesV7.VERSION: {
                                "main_cls": ConfigurableDevicePropertiesV7,
                                "api": api_v6_to_v8
                        },
                        ConfigurableDevicePropertiesV8.VERSION: {
                                "main_cls": ConfigurableDevicePropertiesV8,
                                "api": api_v6_to_v8
                        },
                }
        }
    # end def _get_data_model
# end class ConfigurableDevicePropertiesModel


class ConfigurableDevicePropertiesFactory(FeatureFactory):
    """
    ConfigurableDeviceProperties factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        ConfigurableDeviceProperties object creation from version number

        :param version: ConfigurableDeviceProperties feature version
        :type version: ``int``

        :return: ConfigurableDeviceProperties object
        :rtype: ``ConfigurableDevicePropertiesInterface``
        """
        return ConfigurableDevicePropertiesModel.get_main_cls(version)()
    # end def create
# end class ConfigurableDevicePropertiesFactory


class ConfigurableDevicePropertiesInterface(FeatureInterface, ABC):
    """
    Defines required interfaces for ConfigurableDeviceProperties classes
    """
    def __init__(self):
        # Requests
        self.get_device_name_max_count_cls = None
        self.set_device_name_cls = None
        self.set_device_name_commit_cls = None
        self.set_device_extended_model_id_cls = None
        self.set_device_properties_cls = None
        self.get_device_properties_cls = None

        # Responses
        self.get_device_name_max_count_response_cls = None
        self.set_device_name_response_cls = None
        self.set_device_name_commit_response_cls = None
        self.set_device_extended_model_id_response_cls = None
        self.set_device_properties_response_cls = None
        self.get_device_properties_response_cls = None
    # end def __init__
# end class ConfigurableDevicePropertiesInterface


class ConfigurableDevicePropertiesUpToV5(ConfigurableDevicePropertiesInterface):
    """
    ConfigurableDeviceProperties

    This feature sets in the device non volatile memory configurable attributes for a given
    model. This feature is only available when manufacturing mode is enabled.

    [0] getDeviceNameMaxCount() -> deviceNameMaxCount
    [1] setDeviceName(charIndex, deviceName)
    [2] setDeviceNameCommit(length)
    [3] setDeviceExtendModelID(extendedModelId)
    [4] setDeviceProperties(propertyId, flag, subDataIndex, propertyData)
    [5] getDeviceProperties(propertyId, flag, subDataIndex) -> propertyId, subDataIndex,propertyData
    """

    def __init__(self):
        super().__init__()
        index = ConfigurableDevicePropertiesModel.INDEX

        # Requests
        self.get_device_name_max_count_cls = ConfigurableDevicePropertiesModel.get_request_cls(
                self.VERSION, index.GET_DEVICE_NAME_MAX_COUNT)
        self.set_device_name_cls = ConfigurableDevicePropertiesModel.get_request_cls(
                self.VERSION, index.SET_DEVICE_NAME)
        self.set_device_name_commit_cls = ConfigurableDevicePropertiesModel.get_request_cls(
                self.VERSION, index.SET_DEVICE_NAME_COMMIT)
        self.set_device_extended_model_id_cls = ConfigurableDevicePropertiesModel.get_request_cls(
                self.VERSION, index.SET_DEVICE_EXTEND_MODEL_ID)
        self.set_device_properties_cls = ConfigurableDevicePropertiesModel.get_request_cls(
                self.VERSION, index.SET_DEVICE_PROPERTIES)
        self.get_device_properties_cls = ConfigurableDevicePropertiesModel.get_request_cls(
                self.VERSION, index.GET_DEVICE_PROPERTIES)

        # Responses
        self.get_device_name_max_count_response_cls = ConfigurableDevicePropertiesModel.get_response_cls(
                self.VERSION, index.GET_DEVICE_NAME_MAX_COUNT)
        self.set_device_name_response_cls = ConfigurableDevicePropertiesModel.get_response_cls(
                self.VERSION, index.SET_DEVICE_NAME)
        self.set_device_name_commit_response_cls = ConfigurableDevicePropertiesModel.get_response_cls(
                self.VERSION, index.SET_DEVICE_NAME_COMMIT)
        self.set_device_extended_model_id_response_cls = ConfigurableDevicePropertiesModel.get_response_cls(
                self.VERSION, index.SET_DEVICE_EXTEND_MODEL_ID)
        self.set_device_properties_response_cls = ConfigurableDevicePropertiesModel.get_response_cls(
                self.VERSION, index.SET_DEVICE_PROPERTIES)
        self.get_device_properties_response_cls = ConfigurableDevicePropertiesModel.get_response_cls(
                self.VERSION, index.GET_DEVICE_PROPERTIES)
    # end def __init__

    def get_max_function_index(self):
        # See ``ConfigurableDevicePropertiesInterface.get_max_function_index``
        return ConfigurableDevicePropertiesModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ConfigurableDevicePropertiesUpToV5


class ConfigurableDevicePropertiesV6(ConfigurableDevicePropertiesUpToV5):
    # See ``ConfigurableDevicePropertiesUpToV5``
    VERSION = 6

    def __init__(self):
        super().__init__()

        self.property_id = ConfigurableDevicePropertiesModel.get_base_cls().PropertyIdV6
        self.property_size = ConfigurableDevicePropertiesModel.get_base_cls().PropertySizeV6
    # end def __init__
# end class ConfigurableDevicePropertiesV6


class ConfigurableDevicePropertiesV7(ConfigurableDevicePropertiesV6):
    # See ``ConfigurableDevicePropertiesUpToV5``
    VERSION = 7

    def __init__(self):
        super().__init__()

        self.property_id = ConfigurableDevicePropertiesModel.get_base_cls().PropertyIdV7
        self.property_size = ConfigurableDevicePropertiesModel.get_base_cls().PropertySizeV7
    # end def __init__
# end class ConfigurableDevicePropertiesV7


class ConfigurableDevicePropertiesV8(ConfigurableDevicePropertiesV7):
    # See ``ConfigurableDevicePropertiesUpToV5``
    VERSION = 8

    def __init__(self):
        super().__init__()

        self.property_id = ConfigurableDevicePropertiesModel.get_base_cls().PropertyIdV8
        self.property_size = ConfigurableDevicePropertiesModel.get_base_cls().PropertySizeV8
    # end def __init__
# end class ConfigurableDevicePropertiesV8


class EmptyShortPacket(ConfigurableDeviceProperties):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """
    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        PADDING = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ConfigurableDeviceProperties.FIELDS + (
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),)
# end class EmptyShortPacket


class EmptyLongPacket(ConfigurableDeviceProperties):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """
    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        PADDING = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = ConfigurableDeviceProperties.FIELDS + (
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),)
# end class EmptyLongPacket


class GetDeviceNameMaxCountV6ToV8(EmptyShortPacket):
    """
    GetDeviceNameMaxCount implementation class for version 6, 7, 8
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetDeviceNameMaxCountResponseV6ToV8.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetDeviceNameMaxCountV6ToV8


class GetDeviceNameMaxCountResponseV6ToV8(ConfigurableDeviceProperties):
    """
    GetDeviceNameMaxCountResponse implementation class for version 6, 7, 8

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    DeviceNameMaxCount            8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceNameMaxCountV6ToV8,)
    VERSION = (6, 7, 8,)
    FUNCTION_INDEX = 0

    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        DEVICE_NAME_MAX_COUNT = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
        PADDING = DEVICE_NAME_MAX_COUNT - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        DEVICE_NAME_MAX_COUNT = 0x08
        PADDING = 0x78
    # end class LEN

    class DEFAULT(ConfigurableDeviceProperties.DEFAULT):
        """
        Fields Default values
        """
        DEVICE_NAME_MAX_COUNT = 0x00
    # end class DEFAULT

    FIELDS = ConfigurableDeviceProperties.FIELDS + (
            BitField(fid=FID.DEVICE_NAME_MAX_COUNT, length=LEN.DEVICE_NAME_MAX_COUNT,
                     title="DeviceNameMaxCount", name="device_name_max_count",
                     checks=(CheckHexList(LEN.DEVICE_NAME_MAX_COUNT // 8), CheckByte(),),
                     default_value=DEFAULT.DEVICE_NAME_MAX_COUNT),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index, device_name_max_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param device_name_max_count: Total size in bytes of the device name
        :type device_name_max_count: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.device_name_max_count = device_name_max_count
    # end def __init__
# end class GetDeviceNameMaxCountResponseV6ToV8


class SetDeviceNameV6ToV8(ConfigurableDeviceProperties):
    """
    SetDeviceName implementation class for version 6, 7, 8

    Format:
    ============================  ===========
    Name                          Bit count
    ============================  ===========
    CharIndex                     8
    DeviceName                    n * 8
    Padding                       120 - n * 8
    ============================  ===========
    """

    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        CHAR_INDEX = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
        DEVICE_NAME = CHAR_INDEX - 1
        PADDING = DEVICE_NAME - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        CHAR_INDEX = 0x08
        DEVICE_NAME = 0x00
        PADDING = 0x78
    # end class LEN

    class DEFAULT(ConfigurableDeviceProperties.DEFAULT):
        """
        Fields Default values
        """
        CHAR_INDEX = 0x00
    # end class DEFAULT

    def __init__(self, device_index, feature_index, char_index, device_name, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param char_index: Zero based index from which to append the remaining characters
        :type char_index: ``int`` or ``HexList``
        :param device_name: device name chunk starting at start index
        :type device_name: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        self.LEN.DEVICE_NAME = len(device_name) * 8
        self.LEN.PADDING = 0x78 - self.LEN.DEVICE_NAME

        self.FIELDS = ConfigurableDeviceProperties.FIELDS + (
                BitField(fid=self.FID.CHAR_INDEX, length=self.LEN.CHAR_INDEX,
                         title="CharIndex", name="char_index",
                         checks=(CheckHexList(self.LEN.CHAR_INDEX // 8), CheckByte(),),
                         default_value=self.DEFAULT.CHAR_INDEX),
                BitField(fid=self.FID.DEVICE_NAME, length=self.LEN.DEVICE_NAME,
                         title="DeviceName", name="device_name",
                         checks=(CheckHexList(self.LEN.DEVICE_NAME // 8), CheckByte(),)),
        )

        if self.LEN.PADDING > 0:
            self.FIELDS = self.FIELDS + (
                    BitField(fid=self.FID.PADDING, length=self.LEN.PADDING,
                             title="Padding", name="padding",
                             checks=(CheckHexList(self.LEN.PADDING // 8), CheckByte(),),
                             default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),
            )
        # end if

        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=SetDeviceNameResponseV6ToV8.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.char_index = char_index
        self.device_name = device_name
    # end def __init__
# end class SetDeviceNameV6ToV8


class SetDeviceNameResponseV6ToV8(EmptyLongPacket):
    """
    SetDeviceNameResponse implementation class for version 6, 7, 8
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDeviceNameV6ToV8,)
    VERSION = (6, 7, 8,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDeviceNameResponseV6ToV8


class SetDeviceNameCommitV6ToV8(ConfigurableDeviceProperties):
    """
    SetDeviceNameCommit implementation class for version 6, 7, 8

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Length                        8
    Padding                       16
    ============================  ==========
    """

    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        LENGTH = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
        PADDING = LENGTH - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        LENGTH = 0x08
        PADDING = 0x10
    # end class LEN

    class DEFAULT(ConfigurableDeviceProperties.DEFAULT):
        """
        Fields Default values
        """
        LENGTH = 0x00
    # end class DEFAULT

    FIELDS = ConfigurableDeviceProperties.FIELDS + (
            BitField(fid=FID.LENGTH, length=LEN.LENGTH,
                     title="Length", name="length",
                     checks=(CheckHexList(LEN.LENGTH // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                     default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index, length, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param length: Number of bytes to be written in the device's non volatile memory.
        :type length: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=SetDeviceNameCommitResponseV6ToV8.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.length = length
    # end def __init__
# end class SetDeviceNameCommitV6ToV8


class SetDeviceNameCommitResponseV6ToV8(EmptyLongPacket):
    """
    SetDeviceNameCommitResponse implementation class for version 6, 7, 8
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDeviceNameCommitV6ToV8,)
    VERSION = (6, 7, 8,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDeviceNameCommitResponseV6ToV8


class SetDeviceExtendModelIdV6ToV8(ConfigurableDeviceProperties):
    """
    SetDeviceExtendModelId implementation class for version 6, 7, 8

    It is a set only function, the extendedModelId can be read in feature x0003 by SW.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ExtendedModelId               8
    Padding                       120
    ============================  ==========
    """

    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        EXTENDED_MODEL_ID = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
        PADDING = EXTENDED_MODEL_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        EXTENDED_MODEL_ID = 0x08
        PADDING = 0x78
    # end class LEN

    class DEFAULT(ConfigurableDeviceProperties.DEFAULT):
        """
        Fields Default values
        """
        EXTENDED_MODEL_ID = 0x00
    # end class DEFAULT

    FIELDS = ConfigurableDeviceProperties.FIELDS + (
            BitField(fid=FID.EXTENDED_MODEL_ID, length=LEN.EXTENDED_MODEL_ID,
                     title="ExtendedModelId", name="extended_model_id",
                     checks=(CheckHexList(LEN.EXTENDED_MODEL_ID // 8), CheckByte(),),
                     default_value=DEFAULT.EXTENDED_MODEL_ID),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index, extended_model_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param extended_model_id: A 8 bit value that represents a configurable attribute of the
        device (on the production line) for a given modelId (e.g. colour of the device).
        :type extended_model_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=SetDeviceExtendModelIdResponseV6ToV8.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.extended_model_id = extended_model_id
    # end def __init__
# end class SetDeviceExtendModelIdV6ToV8


class SetDeviceExtendModelIdResponseV6ToV8(EmptyLongPacket):
    """
    SetDeviceExtendModelIdResponse implementation class for version 6, 7, 8
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDeviceExtendModelIdV6ToV8,)
    VERSION = (6, 7, 8,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDeviceExtendModelIdResponseV6ToV8


class SetDevicePropertiesV6ToV8(ConfigurableDeviceProperties):
    """
    SetDeviceProperties implementation class for version 6, 7, 8

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    PropertyID                    8
    Flag                          1
    SubDataIndex                  7
    PropertyData                  n * 8
    Padding                       112 - n * 8
    ============================  ==========
    """
    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        PROPERTY_ID = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
        FLAG = PROPERTY_ID - 1
        SUB_DATA_INDEX = FLAG - 1
        PROPERTY_DATA = SUB_DATA_INDEX - 1
        PADDING = PROPERTY_DATA - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        PROPERTY_ID = 0x08
        FLAG = 0x01
        SUB_DATA_INDEX = 0x07
        PROPERTY_DATA = 0x00
        PADDING = 0x70
    # end class LEN

    class DEFAULT(ConfigurableDeviceProperties.DEFAULT):
        """
        Fields Default values
        """
        PROPERTY_ID = 0x00
        FLAG = 0x00
        SUB_DATA_INDEX = 0x00
        PROPERTY_DATA = 0x00
    # end class DEFAULT

    def __init__(self, device_index, feature_index, property_id, flag, sub_data_index, property_data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param property_id: Index of the property
        :type property_id: ``int`` or ``HexList``
        :param flag: Indicates if there are indexes including in the propertyId memory space
        :type flag: ``int`` or ``HexList``
        :param sub_data_index: Index number to look up the offset and size
        :type sub_data_index: ``int`` or ``HexList``
        :param property_data: The properties data to write into non-volatile memory.
        :type property_data: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        self.LEN.PROPERTY_DATA = len(property_data) * 8
        self.LEN.PADDING = 0x70 - self.LEN.PROPERTY_DATA

        self.FIELDS = ConfigurableDeviceProperties.FIELDS + (
                BitField(fid=self.FID.PROPERTY_ID, length=self.LEN.PROPERTY_ID,
                         title="PropertyId", name="property_id",
                         checks=(CheckHexList(self.LEN.PROPERTY_ID // 8), CheckByte(),),
                         default_value=self.DEFAULT.PROPERTY_ID),
                BitField(fid=self.FID.FLAG, length=self.LEN.FLAG,
                         title="Flag", name="flag",
                         checks=(CheckInt(0, pow(2, self.LEN.FLAG) - 1),),
                         default_value=self.DEFAULT.FLAG),
                BitField(fid=self.FID.SUB_DATA_INDEX, length=self.LEN.SUB_DATA_INDEX,
                         title="SubDataIndex", name="sub_data_index",
                         checks=(CheckInt(0, pow(2, self.LEN.SUB_DATA_INDEX) - 1),),
                         default_value=self.DEFAULT.SUB_DATA_INDEX),
                BitField(fid=self.FID.PROPERTY_DATA, length=self.LEN.PROPERTY_DATA,
                         title="PropertyData", name="property_data",
                         checks=(CheckHexList(self.LEN.PROPERTY_DATA // 8), CheckByte(),),
                         default_value=self.DEFAULT.PROPERTY_DATA),
        )

        if self.LEN.PADDING > 0:
            self.FIELDS = self.FIELDS + (
                    BitField(fid=self.FID.PADDING, length=self.LEN.PADDING,
                             title="Padding", name="padding",
                             checks=(CheckHexList(self.LEN.PADDING // 8), CheckByte(),),
                             default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),
            )
        # end if

        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=SetDevicePropertiesResponseV6ToV8.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.property_id = property_id
        self.flag = flag
        self.sub_data_index = sub_data_index
        self.property_data = property_data
    # end def __init__
# end class SetDevicePropertiesV6ToV8


class SetDevicePropertiesResponseV6ToV8(EmptyLongPacket):
    """
    SetDevicePropertiesResponse implementation class for version 6, 7, 8
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDevicePropertiesV6ToV8,)
    VERSION = (6, 7, 8,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDevicePropertiesResponseV6ToV8


class GetDevicePropertiesV6ToV8(ConfigurableDeviceProperties):
    """
    GetDeviceProperties implementation class for version 6, 7, 8

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    PropertyID                    8
    Flag                          1
    SubDataIndex                  7
    Padding                       8
    ============================  ==========
    """
    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        PROPERTY_ID = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
        FLAG = PROPERTY_ID - 1
        SUB_DATA_INDEX = FLAG - 1
        PADDING = SUB_DATA_INDEX - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        PROPERTY_ID = 0x08
        FLAG = 0x01
        SUB_DATA_INDEX = 0x07
        PADDING = 0x08
    # end class LEN

    class DEFAULT(ConfigurableDeviceProperties.DEFAULT):
        """
        Fields Default values
        """
        PROPERTY_ID = 0x00
        FLAG = 0x00
        SUB_DATA_INDEX = 0x00
    # end class DEFAULT

    FIELDS = ConfigurableDeviceProperties.FIELDS + (
            BitField(fid=FID.PROPERTY_ID, length=LEN.PROPERTY_ID,
                     title="PropertyId", name="property_id",
                     checks=(CheckHexList(LEN.PROPERTY_ID // 8), CheckByte(),),
                     default_value=DEFAULT.PROPERTY_ID),
            BitField(fid=FID.FLAG, length=LEN.FLAG,
                     title="Flag", name="flag",
                     checks=(CheckHexList(LEN.FLAG // 8), CheckByte(),),
                     default_value=DEFAULT.FLAG),
            BitField(fid=FID.SUB_DATA_INDEX, length=LEN.SUB_DATA_INDEX,
                     title="SubDataIndex", name="sub_data_index",
                     checks=(CheckHexList(LEN.SUB_DATA_INDEX // 8), CheckByte(),),
                     default_value=DEFAULT.SUB_DATA_INDEX),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=ConfigurableDeviceProperties.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index, property_id, flag, sub_data_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param property_id: The index of property. Property data will get from non-volatile memory.
        :type property_id: ``int`` or ``HexList``
        :param flag: Indicates if there are indexes including in the propertyId memory space
        :type flag: ``int`` or ``HexList``
        :param sub_data_index: Index number to look up the offset and size
        :type sub_data_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetDevicePropertiesResponseV6ToV8.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.property_id = property_id
        self.flag = flag
        self.sub_data_index = sub_data_index
    # end def __init__
# end class GetDevicePropertiesV6ToV8


class GetDevicePropertiesResponseV6ToV8(ConfigurableDeviceProperties):
    """
    GetDevicePropertiesResponse implementation class for version 6, 7, 8

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    PropertyID                    8
    SubDataIndex                  8
    PropertyData                  n * 8
    Padding                       112 - n * 8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDevicePropertiesV6ToV8,)
    VERSION = (6, 7, 8,)
    FUNCTION_INDEX = 5

    class FID(ConfigurableDeviceProperties.FID):
        """
        Field Identifiers
        """
        PROPERTY_ID = ConfigurableDeviceProperties.FID.SOFTWARE_ID - 1
        SUB_DATA_INDEX = PROPERTY_ID - 1
        PROPERTY_DATA = SUB_DATA_INDEX - 1
        PADDING = PROPERTY_DATA - 1
    # end class FID

    class LEN(ConfigurableDeviceProperties.LEN):
        """
        Field Lengths in bits
        """
        PROPERTY_ID = 0x08
        SUB_DATA_INDEX = 0x08
        PROPERTY_DATA = 0x70
        PADDING = 0x00
    # end class LEN

    class DEFAULT(ConfigurableDeviceProperties.DEFAULT):
        """
        Fields Default values
        """
        PROPERTY_ID = 0x00
        SUB_DATA_INDEX = 0x00
        PROPERTY_DATA = 0x00
    # end class DEFAULT

    FIELDS = ConfigurableDeviceProperties.FIELDS + (
            BitField(fid=FID.PROPERTY_ID, length=LEN.PROPERTY_ID,
                     title="PropertyId", name="property_id",
                     checks=(CheckHexList(LEN.PROPERTY_ID // 8), CheckByte(),),
                     default_value=DEFAULT.PROPERTY_ID),
            BitField(fid=FID.SUB_DATA_INDEX, length=LEN.SUB_DATA_INDEX,
                     title="SubDataIndex", name="sub_data_index",
                     checks=(CheckHexList(LEN.SUB_DATA_INDEX // 8), CheckByte(),),
                     default_value=DEFAULT.SUB_DATA_INDEX),
            BitField(fid=FID.PROPERTY_DATA, length=LEN.PROPERTY_DATA,
                     title="PropertyData", name="property_data",
                     checks=(CheckHexList(LEN.PROPERTY_DATA // 8), CheckByte(),),
                     default_value=DEFAULT.PROPERTY_DATA),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, property_id, sub_data_index, property_data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param property_id: Index of the property
        :type property_id: ``int`` or ``HexList``
        :param sub_data_index: Index number to look up the offset and size
        :type sub_data_index: ``int`` or ``HexList``
        :param property_data: The properties data to be read from non-volatile memory
        :type property_data: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        sizes = ConfigurableDeviceProperties.PropertySizeV8.get_all_sizes()
        pid = int(Numeral(property_id))
        size = int(Numeral(sizes[pid - 1])) * 8
        if size > 0x70:
            self.LEN.PROPERTY_DATA = 0x70
            self.LEN.PADDING = 0x00
        else:
            self.LEN.PROPERTY_DATA = size
            self.LEN.PADDING = 0x70 - size
        # end if

        self.FIELDS = self.FIELDS[:-2] + (
                BitField(fid=self.FID.PROPERTY_DATA, length=self.LEN.PROPERTY_DATA,
                         title="PropertyData", name="property_data",
                         checks=(CheckHexList(self.LEN.PROPERTY_DATA // 8), CheckByte(),),
                         default_value=self.DEFAULT.PROPERTY_DATA),
        )

        if self.LEN.PADDING > 0:
            self.FIELDS = self.FIELDS + (
                    BitField(fid=self.FID.PADDING, length=self.LEN.PADDING,
                             title="Padding", name="padding",
                             checks=(CheckHexList(self.LEN.PADDING // 8), CheckByte(),),
                             default_value=self.DEFAULT.PADDING),
            )
        # end if

        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.property_id = property_id
        self.sub_data_index = sub_data_index
        self.property_data = property_data
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``List``
        :param kwargs: Dictionary of arguments
        :type kwargs: ``dict``

        :return: parsed object
        :rtype ``GetDevicePropertiesResponseV6ToV8``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        sizes = ConfigurableDeviceProperties.PropertySizeV8.get_all_sizes()
        pid = int(Numeral(inner_field_container_mixin.property_id))
        size = int(Numeral(sizes[pid - 1])) * 8
        # Update of the respective lengths of the 'property_data' & 'padding' fields
        inner_field_container_mixin.LEN.PROPERTY_DATA = min(size, 0x70)
        inner_field_container_mixin.LEN.PADDING = max(0x70 - size, 0x00)
        # Recreate the FIELDS structure based on the sizes computed above
        inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS[:-2] + (
            BitField(fid=inner_field_container_mixin.FID.PROPERTY_DATA,
                     length=inner_field_container_mixin.LEN.PROPERTY_DATA,
                     title="PropertyData", name="property_data",
                     checks=(CheckHexList(inner_field_container_mixin.LEN.PROPERTY_DATA // 8), CheckByte(),),
                     default_value=inner_field_container_mixin.DEFAULT.PROPERTY_DATA),
            BitField(fid=inner_field_container_mixin.FID.PADDING,
                     length=inner_field_container_mixin.LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(inner_field_container_mixin.LEN.PADDING // 8), CheckByte(),),
                     default_value=inner_field_container_mixin.DEFAULT.PADDING),
        )
        # Assign the new values to the different fields
        inner_field_container_mixin.padding = inner_field_container_mixin.property_data[size // 8:]
        inner_field_container_mixin.property_data = inner_field_container_mixin.property_data[:size // 8]
        # end if

        return inner_field_container_mixin
    # end def fromHexList
# end class GetDevicePropertiesResponseV6ToV8

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
