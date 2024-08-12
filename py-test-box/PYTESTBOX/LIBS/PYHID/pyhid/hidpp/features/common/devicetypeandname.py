#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.devicetypeandname
:brief: HID++ 2.0 ``DeviceTypeAndName`` command interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum

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
from pylibrary.tools.util import ContainsEnumMeta


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceTypeAndName(HidppMessage):
    """
    This feature retrieves the device display name as well as the device type
    """

    FEATURE_ID = 0x0005
    MAX_FUNCTION_INDEX = 2

    class TYPE(IntEnum, metaclass=ContainsEnumMeta):
        # Device Type
        KEYBOARD = 0
        REMOTECONTROL = 1
        NUMPAD = 2
        MOUSE = 3
        TRACKPAD = 4
        TRACKBALL = 5
        PRESENTER = 6
        RECEIVER = 7
        HEADSET = 8
        WEBCAM = 9
        STEERINGWHEEL = 10
        JOYSTICK = 11
        GAMEPAD = 12
        DOCK = 13
        SPEAKER = 14
        MICROPHONE = 15
        # Types added in version 1
        ILLUMINATION_LIGHT = 16
        PROGRAMMABLE_CONTROLLER = 17
        CAR_SIM_PEDALS = 18
        # Types added in version 2
        ADAPTER = 19
        # Types added in version 3
        WHEEL_RIM = 20
        MOTOR_DRIVE = 21
        HANDBRAKE = 22
        SHIFTER = 23
        # Types added in version 4
        DIAL = 24
        CONTEXTUAL_KEYS = 25
        # Types added in version 5
        DRIFTER = 26
    # end class TYPE

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class DeviceTypeAndName


class DeviceTypeAndNameModel(FeatureModel):
    """
    Define ``DeviceTypeAndName`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_DEVICE_NAME_COUNT = 0
        GET_DEVICE_NAME = 1
        GET_DEVICE_TYPE = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``DeviceTypeAndName`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0_to_v5 = {
            "functions": {
                cls.INDEX.GET_DEVICE_NAME_COUNT: {
                    "request": GetDeviceNameCount,
                    "response": GetDeviceNameCountResponse
                },
                cls.INDEX.GET_DEVICE_NAME: {
                    "request": GetDeviceName,
                    "response": GetDeviceNameResponse
                },
                cls.INDEX.GET_DEVICE_TYPE: {
                    "request": GetDeviceType,
                    "response": GetDeviceTypeResponse
                }
            }
        }

        return {
            "feature_base": DeviceTypeAndName,
            "versions": {
                DeviceTypeAndNameV0.VERSION: {
                    "main_cls": DeviceTypeAndNameV0,
                    "api": function_map_v0_to_v5
                },
                DeviceTypeAndNameV1.VERSION: {
                    "main_cls": DeviceTypeAndNameV1,
                    "api": function_map_v0_to_v5
                },
                DeviceTypeAndNameV2.VERSION: {
                    "main_cls": DeviceTypeAndNameV2,
                    "api": function_map_v0_to_v5
                },
                DeviceTypeAndNameV3.VERSION: {
                    "main_cls": DeviceTypeAndNameV3,
                    "api": function_map_v0_to_v5
                },
                DeviceTypeAndNameV4.VERSION: {
                    "main_cls": DeviceTypeAndNameV4,
                    "api": function_map_v0_to_v5
                },
                DeviceTypeAndNameV5.VERSION: {
                    "main_cls": DeviceTypeAndNameV5,
                    "api": function_map_v0_to_v5
                },
            }
        }
    # end def _get_data_model
# end class DeviceTypeAndNameModel


class DeviceTypeAndNameFactory(FeatureFactory):
    """
    Get ``DeviceTypeAndName`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``DeviceTypeAndName`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``DeviceTypeAndNameInterface``
        """
        return DeviceTypeAndNameModel.get_main_cls(version)()
    # end def create
# end class DeviceTypeAndNameFactory


class DeviceTypeAndNameInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``DeviceTypeAndName``
    """

    def __init__(self):
        # Requests
        self.get_device_name_count_cls = None
        self.get_device_name_cls = None
        self.get_device_type_cls = None

        # Responses
        self.get_device_name_count_response_cls = None
        self.get_device_name_response_cls = None
        self.get_device_type_response_cls = None
    # end def __init__
# end class DeviceTypeAndNameInterface


class DeviceTypeAndNameV0(DeviceTypeAndNameInterface):
    """
    Define ``DeviceTypeAndNameV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getDeviceNameCount() -> deviceNameCount

    [1] getDeviceName(charIndex) -> deviceName

    [2] getDeviceType() -> deviceType
    """

    VERSION = 0

    def __init__(self):
        # See ``DeviceTypeAndName.__init__``
        super().__init__()
        index = DeviceTypeAndNameModel.INDEX

        # Requests
        self.get_device_name_count_cls = DeviceTypeAndNameModel.get_request_cls(
            self.VERSION, index.GET_DEVICE_NAME_COUNT)
        self.get_device_name_cls = DeviceTypeAndNameModel.get_request_cls(
            self.VERSION, index.GET_DEVICE_NAME)
        self.get_device_type_cls = DeviceTypeAndNameModel.get_request_cls(
            self.VERSION, index.GET_DEVICE_TYPE)

        # Responses
        self.get_device_name_count_response_cls = DeviceTypeAndNameModel.get_response_cls(
            self.VERSION, index.GET_DEVICE_NAME_COUNT)
        self.get_device_name_response_cls = DeviceTypeAndNameModel.get_response_cls(
            self.VERSION, index.GET_DEVICE_NAME)
        self.get_device_type_response_cls = DeviceTypeAndNameModel.get_response_cls(
            self.VERSION, index.GET_DEVICE_TYPE)
    # end def __init__

    def get_max_function_index(self):
        # See ``DeviceTypeAndNameInterface.get_max_function_index``
        return DeviceTypeAndNameModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class DeviceTypeAndNameV0


class DeviceTypeAndNameV1(DeviceTypeAndNameV0):
    # See ``DeviceTypeAndNameV0``
    VERSION = 1
# end class DeviceTypeAndNameV1


class DeviceTypeAndNameV2(DeviceTypeAndNameV1):
    # See ``DeviceTypeAndNameV1``
    VERSION = 2
# end class DeviceTypeAndNameV2


class DeviceTypeAndNameV3(DeviceTypeAndNameV2):
    # See ``DeviceTypeAndNameV0``
    VERSION = 3
# end class DeviceTypeAndNameV3


class DeviceTypeAndNameV4(DeviceTypeAndNameV3):
    # See ``DeviceTypeAndNameV0``
    VERSION = 4
# end class DeviceTypeAndNameV4


class DeviceTypeAndNameV5(DeviceTypeAndNameV4):
    # See ``DeviceTypeAndNameV4``
    VERSION = 5
# end class DeviceTypeAndNameV5


class ShortEmptyPacketDataFormat(DeviceTypeAndName):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetDeviceNameCount
        - GetDeviceType

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(DeviceTypeAndName.FID):
        """
        Define field identifier(s)
        """
        PADDING = DeviceTypeAndName.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DeviceTypeAndName.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = DeviceTypeAndName.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DeviceTypeAndName.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class GetDeviceNameCount(ShortEmptyPacketDataFormat):
    """
    Define ``GetDeviceNameCount`` implementation class for version 0
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
                         functionIndex=GetDeviceNameCountResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetDeviceNameCount


class GetDeviceNameCountResponse(DeviceTypeAndName):
    """
    Define ``GetDeviceNameCountResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    DeviceNameCount               8
    Padding                       120
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceNameCount,)
    VERSION = (0, 1, 2, 3, 4, 5)
    FUNCTION_INDEX = 0

    class FID(DeviceTypeAndName.FID):
        """
        Define field identifier(s)
        """
        DEVICE_NAME_COUNT = DeviceTypeAndName.FID.SOFTWARE_ID - 1
        PADDING = DEVICE_NAME_COUNT - 1
    # end class FID

    class LEN(DeviceTypeAndName.LEN):
        """
        Define field length(s)
        """
        DEVICE_NAME_COUNT = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = DeviceTypeAndName.FIELDS + (
        BitField(fid=FID.DEVICE_NAME_COUNT, length=LEN.DEVICE_NAME_COUNT,
                 title="DeviceNameCount", name="device_name_count",
                 checks=(CheckHexList(LEN.DEVICE_NAME_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DeviceTypeAndName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, device_name_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param device_name_count: Total size in single byte characters of the device name.
        :type device_name_count: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.device_name_count = device_name_count
    # end def __init__
# end class GetDeviceNameCountResponse


class GetDeviceName(DeviceTypeAndName):
    """
    Define ``GetDeviceName`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    CharIndex                     8
    Padding                       16
    ============================  ==========
    """

    class FID(DeviceTypeAndName.FID):
        """
        Define field identifier(s)
        """
        CHAR_INDEX = DeviceTypeAndName.FID.SOFTWARE_ID - 1
        PADDING = CHAR_INDEX - 1
    # end class FID

    class LEN(DeviceTypeAndName.LEN):
        """
        Define field length(s)
        """
        CHAR_INDEX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = DeviceTypeAndName.FIELDS + (
        BitField(fid=FID.CHAR_INDEX, length=LEN.CHAR_INDEX,
                 title="CharIndex", name="char_index",
                 checks=(CheckHexList(LEN.CHAR_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DeviceTypeAndName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, char_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param char_index: Zero based index. The function will retrieve as many remaining characters as the payload will allow.
        :type char_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetDeviceNameResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.char_index = char_index
    # end def __init__
# end class GetDeviceName


class GetDeviceNameResponse(DeviceTypeAndName):
    """
    Define ``GetDeviceNameResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    DeviceName                    128
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceName,)
    VERSION = (0, 1, 2, 3, 4, 5,)
    FUNCTION_INDEX = 1

    class FID(DeviceTypeAndName.FID):
        """
        Define field identifier(s)
        """
        DEVICE_NAME = DeviceTypeAndName.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DeviceTypeAndName.LEN):
        """
        Define field length(s)
        """
        DEVICE_NAME = 0x80
    # end class LEN

    FIELDS = DeviceTypeAndName.FIELDS + (
        BitField(fid=FID.DEVICE_NAME, length=LEN.DEVICE_NAME,
                 title="DeviceName", name="device_name",
                 checks=(CheckHexList(LEN.DEVICE_NAME // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_NAME) - 1),)),
    )

    def __init__(self, device_index, feature_index, device_name, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param device_name: device name chunk starting at charindex.
        :type device_name: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.device_name = device_name
    # end def __init__
# end class GetDeviceNameResponse


class GetDeviceType(ShortEmptyPacketDataFormat):
    """
    Define ``GetDeviceType`` implementation class for version 0
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
                         functionIndex=GetDeviceTypeResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetDeviceType


class GetDeviceTypeResponse(DeviceTypeAndName):
    """
    Define ``GetDeviceTypeResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    DeviceType                    8
    Padding                       120
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceType,)
    VERSION = (0, 1, 2, 3, 4, 5,)
    FUNCTION_INDEX = 2

    class FID(DeviceTypeAndName.FID):
        """
        Define field identifier(s)
        """
        DEVICE_TYPE = DeviceTypeAndName.FID.SOFTWARE_ID - 1
        PADDING = DEVICE_TYPE - 1
    # end class FID

    class LEN(DeviceTypeAndName.LEN):
        """
        Define field length(s)
        """
        DEVICE_TYPE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = DeviceTypeAndName.FIELDS + (
        BitField(fid=FID.DEVICE_TYPE, length=LEN.DEVICE_TYPE,
                 title="DeviceType", name="device_type",
                 checks=(CheckHexList(LEN.DEVICE_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DeviceTypeAndName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, device_type, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param device_type: device type best associated with the device
        :type device_type: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.device_type = device_type
    # end def __init__
# end class GetDeviceTypeResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
