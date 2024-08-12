#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.gaming.perkeylighting
:brief: HID++ 2.0 ``PerKeyLighting`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLighting(HidppMessage):
    """
    This interface defines a mechanism to configure in realtime all RGB light 
    sources on a device.
    """
    FEATURE_ID = 0x8081
    MAX_FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        # noinspection PyTypeChecker
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class PerKeyLighting


class PerKeyLightingModel(FeatureModel):
    """
    Define ``PerKeyLighting`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_INFO = 0
        SET_INDIVIDUAL_RGB_ZONES = 1
        SET_CONSECUTIVE_RGB_ZONES = 2
        SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_5BIT = 3
        SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_4BIT = 4
        SET_RANGE_RGB_ZONES = 5
        SET_RGB_ZONES_SINGLE_VALUE = 6
        FRAME_END = 7
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``PerKeyLighting`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_INFO: {
                    "request": GetInfo,
                    "response": GetInfoResponse
                },
                cls.INDEX.SET_INDIVIDUAL_RGB_ZONES: {
                    "request": SetIndividualRGBZones,
                    "response": SetIndividualRGBZonesResponse
                },
                cls.INDEX.SET_CONSECUTIVE_RGB_ZONES: {
                    "request": SetConsecutiveRGBZones,
                    "response": SetConsecutiveRGBZonesResponse
                },
                cls.INDEX.SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_5BIT: {
                    "request": SetConsecutiveRGBZonesDeltaCompression5bit,
                    "response": SetConsecutiveRGBZonesDeltaCompression5bitResponse
                },
                cls.INDEX.SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_4BIT: {
                    "request": SetConsecutiveRGBZonesDeltaCompression4bit,
                    "response": SetConsecutiveRGBZonesDeltaCompression4bitResponse
                },
                cls.INDEX.SET_RANGE_RGB_ZONES: {
                    "request": SetRangeRGBZones,
                    "response": SetRangeRGBZonesResponse
                },
                cls.INDEX.SET_RGB_ZONES_SINGLE_VALUE: {
                    "request": SetRGBZonesSingleValue,
                    "response": SetRGBZonesSingleValueResponse
                },
                cls.INDEX.FRAME_END: {
                    "request": FrameEnd,
                    "response": FrameEndResponse
                }
            }
        }

        return {
            "feature_base": PerKeyLighting,
            "versions": {
                PerKeyLightingV0.VERSION: {
                    "main_cls": PerKeyLightingV0,
                    "api": function_map_v0
                },
                # TODO: (Gautham S B) function_map_v2 is to be removed when the following bug is fixed
                # See https://jira.logitech.io/browse/NRF52-386
                PerKeyLightingV2.VERSION: {
                    "main_cls": PerKeyLightingV2,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class PerKeyLightingModel


class PerKeyLightingFactory(FeatureFactory):
    """
    Get ``PerKeyLighting`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``PerKeyLighting`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``PerKeyLightingInterface``
        """
        return PerKeyLightingModel.get_main_cls(version)()
    # end def create
# end class PerKeyLightingFactory


class PerKeyLightingInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``PerKeyLighting``
    """

    def __init__(self):
        # Requests
        self.get_info_cls = None
        self.set_individual_rgb_zones_cls = None
        self.set_consecutive_rgb_zones_cls = None
        self.set_consecutive_rgb_zones_delta_compression_5bit_cls = None
        self.set_consecutive_rgb_zones_delta_compression_4bit_cls = None
        self.set_range_rgb_zones_cls = None
        self.set_rgb_zones_single_value_cls = None
        self.frame_end_cls = None

        # Responses
        self.get_info_response_cls = None
        self.set_individual_rgb_zones_response_cls = None
        self.set_consecutive_rgb_zones_response_cls = None
        self.set_consecutive_rgb_zones_delta_compression_5bit_response_cls = None
        self.set_consecutive_rgb_zones_delta_compression_4bit_response_cls = None
        self.set_range_rgb_zones_response_cls = None
        self.set_rgb_zones_single_value_response_cls = None
        self.frame_end_response_cls = None
    # end def __init__
# end class PerKeyLightingInterface


class PerKeyLightingV0(PerKeyLightingInterface):
    """
    Define ``PerKeyLightingV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetInfo(TypeofInfo, Param1) -> TypeofInfo, Param1, ZoneByte0, ZoneByte1, ZoneByte2, ZoneByte3, ZoneByte4,
     ZoneByte5, ZoneByte6, ZoneByte7, ZoneByte8, ZoneByte9, ZoneByte10, ZoneByte11, ZoneByte12, ZoneByte13

    [1] SetIndividualRGBZones(RGBZoneID0, RedIndex0, GreenIndex0, BlueIndex0, RGBZoneID1, RedIndex1, GreenIndex1,
     BlueIndex1, RGBZoneID2, RedIndex2, GreenIndex2, BlueIndex2, RGBZoneID3, RedIndex3, GreenIndex3,
     BlueIndex3) -> RGBZoneID0, RGBZoneID1, RGBZoneID2, RGBZoneID3

    [2] SetConsecutiveRGBZones(RGBZoneID0, RedIndex0, GreenIndex0, BlueIndex0, RedIndex1, GreenIndex1,
     BlueIndex1, RedIndex2, GreenIndex2, BlueIndex2, RedIndex3, GreenIndex3, BlueIndex3, RedIndex4, GreenIndex4,
     BlueIndex4) -> RGBZoneID0

    [3] SetConsecutiveRGBZonesDeltaCompression5bit(RGBZoneID0, RedIndex0, GreenIndex0, BlueIndex0, RedIndex1,
     GreenIndex1, BlueIndex1, RedIndex2, GreenIndex2, BlueIndex2, RedIndex3, GreenIndex3, BlueIndex3, RedIndex4,
     GreenIndex4, BlueIndex4, RedIndex5, GreenIndex5, BlueIndex5, RedIndex6, GreenIndex6, BlueIndex6, RedIndex7,
     GreenIndex7, BlueIndex7) -> RGBZoneID0

    [4] SetConsecutiveRGBZonesDeltaCompression4bit(RGBZoneID0, RedIndex0, GreenIndex0, BlueIndex0, RedIndex1,
     GreenIndex1, BlueIndex1, RedIndex2, GreenIndex2, BlueIndex2, RedIndex3, GreenIndex3, BlueIndex3, RedIndex4,
     GreenIndex4, BlueIndex4, RedIndex5, GreenIndex5, BlueIndex5, RedIndex6, GreenIndex6, BlueIndex6, RedIndex7,
     GreenIndex7, BlueIndex7, RedIndex8, GreenIndex8, BlueIndex8, RedIndex9, GreenIndex9, BlueIndex9) -> RGBZoneID0

    [5] SetRangeRGBZones(RGBFirstZoneID0, RGBLastZoneID0, RedIndex0, GreenIndex0, BlueIndex0, RGBFirstZoneID1,
     RGBLastZoneID1, RedIndex1, GreenIndex1, BlueIndex1, RGBFirstZoneID2, RGBLastZoneID2, RedIndex2, GreenIndex2,
     BlueIndex2) -> RGBFirstZoneID0, RGBFirstZoneID1, RGBFirstZoneID2

    [6] SetRGBZonesSingleValue(RGBZoneRed, RGBZoneGreen, RGBZoneBlue, RGBZoneID0, RGBZoneID1, RGBZoneID2,
     RGBZoneID3, RGBZoneID4, RGBZoneID5, RGBZoneID6, RGBZoneID7, RGBZoneID8, RGBZoneID9, RGBZoneID10, RGBZoneID11,
     RGBZoneID12) -> RGBZoneRed, RGBZoneGreen, RGBZoneBlue, RGBZoneID0

    [7] FrameEnd(Persistence, CurrentFrame, NFramesTillNextChange) -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``PerKeyLighting.__init__``
        super().__init__()
        index = PerKeyLightingModel.INDEX

        # Requests
        self.get_info_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.GET_INFO)
        self.set_individual_rgb_zones_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.SET_INDIVIDUAL_RGB_ZONES)
        self.set_consecutive_rgb_zones_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.SET_CONSECUTIVE_RGB_ZONES)
        self.set_consecutive_rgb_zones_delta_compression_5bit_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_5BIT)
        self.set_consecutive_rgb_zones_delta_compression_4bit_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_4BIT)
        self.set_range_rgb_zones_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.SET_RANGE_RGB_ZONES)
        self.set_rgb_zones_single_value_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.SET_RGB_ZONES_SINGLE_VALUE)
        self.frame_end_cls = PerKeyLightingModel.get_request_cls(
            self.VERSION, index.FRAME_END)

        # Responses
        self.get_info_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.GET_INFO)
        self.set_individual_rgb_zones_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.SET_INDIVIDUAL_RGB_ZONES)
        self.set_consecutive_rgb_zones_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.SET_CONSECUTIVE_RGB_ZONES)
        self.set_consecutive_rgb_zones_delta_compression_5bit_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_5BIT)
        self.set_consecutive_rgb_zones_delta_compression_4bit_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.SET_CONSECUTIVE_RGB_ZONES_DELTA_COMPRESSION_4BIT)
        self.set_range_rgb_zones_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.SET_RANGE_RGB_ZONES)
        self.set_rgb_zones_single_value_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.SET_RGB_ZONES_SINGLE_VALUE)
        self.frame_end_response_cls = PerKeyLightingModel.get_response_cls(
            self.VERSION, index.FRAME_END)
    # end def __init__

    def get_max_function_index(self):
        # See ``PerKeyLightingInterface.get_max_function_index``
        return PerKeyLightingModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class PerKeyLightingV0


# TODO: (Gautham S B) PerKeyLightingV2 is to be removed when the following bug is fixed
# See https://jira.logitech.io/browse/NRF52-386
class PerKeyLightingV2(PerKeyLightingV0):
    # See ``PerKeyLightingV0``
    VERSION = 2
# end class PerKeyLightingV2


class LongEmptyPacketDataFormat(PerKeyLighting):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - FrameEndResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        PADDING = PerKeyLighting.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class RGBZoneIDResponseHead(PerKeyLighting):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - SetConsecutiveRGBZonesResponse
        - SetConsecutiveRGBZonesDeltaCompression5bitResponse
        - SetConsecutiveRGBZonesDeltaCompression4bitResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone ID 0                 8
    Padding                       120
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        PADDING = RGB_ZONE_ID_0 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_ID_0 = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),
    )
# end class RGBZoneIDResponseHead


class GetInfo(PerKeyLighting):
    """
    Define ``GetInfo`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Type of Info                  8
    Param1                        8
    Padding                       8
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        TYPE_OF_INFO = PerKeyLighting.FID.SOFTWARE_ID - 1
        PARAM1 = TYPE_OF_INFO - 1
        PADDING = PARAM1 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        TYPE_OF_INFO = 0x8
        PARAM1 = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.TYPE_OF_INFO, length=LEN.TYPE_OF_INFO,
                 title="TypeOfInfo", name="type_of_info",
                 checks=(CheckHexList(LEN.TYPE_OF_INFO // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM1, length=LEN.PARAM1,
                 title="Param1", name="param1",
                 checks=(CheckHexList(LEN.PARAM1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, type_of_info, param1, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param type_of_info: This parameter defines the type of information requested
        :type type_of_info: ``int | HexList``
        :param param1: These parameters help to further specify the request in some particular cases
        :type param1: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetInfoResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.type_of_info = type_of_info
        self.param1 = param1
    # end def __init__
# end class GetInfo


class GetInfoResponse(PerKeyLighting):
    """
    Define ``GetInfoResponse`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Type of Info                  8
    Param1                        8
    Zone Byte 0                   8
    Zone Byte 1                   8
    Zone Byte 2                   8
    Zone Byte 3                   8
    Zone Byte 4                   8
    Zone Byte 5                   8
    Zone Byte 6                   8
    Zone Byte 7                   8
    Zone Byte 8                   8
    Zone Byte 9                   8
    Zone Byte 10                  8
    Zone Byte 11                  8
    Zone Byte 12                  8
    Zone Byte 13                  8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetInfo,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 0

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        TYPE_OF_INFO = PerKeyLighting.FID.SOFTWARE_ID - 1
        PARAM1 = TYPE_OF_INFO - 1
        ZONE_BYTE_0 = PARAM1 - 1
        ZONE_BYTE_1 = ZONE_BYTE_0 - 1
        ZONE_BYTE_2 = ZONE_BYTE_1 - 1
        ZONE_BYTE_3 = ZONE_BYTE_2 - 1
        ZONE_BYTE_4 = ZONE_BYTE_3 - 1
        ZONE_BYTE_5 = ZONE_BYTE_4 - 1
        ZONE_BYTE_6 = ZONE_BYTE_5 - 1
        ZONE_BYTE_7 = ZONE_BYTE_6 - 1
        ZONE_BYTE_8 = ZONE_BYTE_7 - 1
        ZONE_BYTE_9 = ZONE_BYTE_8 - 1
        ZONE_BYTE_10 = ZONE_BYTE_9 - 1
        ZONE_BYTE_11 = ZONE_BYTE_10 - 1
        ZONE_BYTE_12 = ZONE_BYTE_11 - 1
        ZONE_BYTE_13 = ZONE_BYTE_12 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        TYPE_OF_INFO = 0x8
        PARAM1 = 0x8
        ZONE_BYTE_0 = 0x8
        ZONE_BYTE_1 = 0x8
        ZONE_BYTE_2 = 0x8
        ZONE_BYTE_3 = 0x8
        ZONE_BYTE_4 = 0x8
        ZONE_BYTE_5 = 0x8
        ZONE_BYTE_6 = 0x8
        ZONE_BYTE_7 = 0x8
        ZONE_BYTE_8 = 0x8
        ZONE_BYTE_9 = 0x8
        ZONE_BYTE_10 = 0x8
        ZONE_BYTE_11 = 0x8
        ZONE_BYTE_12 = 0x8
        ZONE_BYTE_13 = 0x8
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.TYPE_OF_INFO, length=LEN.TYPE_OF_INFO,
                 title="TypeOfInfo", name="type_of_info",
                 checks=(CheckHexList(LEN.TYPE_OF_INFO // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM1, length=LEN.PARAM1,
                 title="Param1", name="param1",
                 checks=(CheckHexList(LEN.PARAM1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_0, length=LEN.ZONE_BYTE_0,
                 title="ZoneByte0", name="zone_byte_0",
                 checks=(CheckHexList(LEN.ZONE_BYTE_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_1, length=LEN.ZONE_BYTE_1,
                 title="ZoneByte1", name="zone_byte_1",
                 checks=(CheckHexList(LEN.ZONE_BYTE_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_2, length=LEN.ZONE_BYTE_2,
                 title="ZoneByte2", name="zone_byte_2",
                 checks=(CheckHexList(LEN.ZONE_BYTE_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_3, length=LEN.ZONE_BYTE_3,
                 title="ZoneByte3", name="zone_byte_3",
                 checks=(CheckHexList(LEN.ZONE_BYTE_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_4, length=LEN.ZONE_BYTE_4,
                 title="ZoneByte4", name="zone_byte_4",
                 checks=(CheckHexList(LEN.ZONE_BYTE_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_5, length=LEN.ZONE_BYTE_5,
                 title="ZoneByte5", name="zone_byte_5",
                 checks=(CheckHexList(LEN.ZONE_BYTE_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_6, length=LEN.ZONE_BYTE_6,
                 title="ZoneByte6", name="zone_byte_6",
                 checks=(CheckHexList(LEN.ZONE_BYTE_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_7, length=LEN.ZONE_BYTE_7,
                 title="ZoneByte7", name="zone_byte_7",
                 checks=(CheckHexList(LEN.ZONE_BYTE_7 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_8, length=LEN.ZONE_BYTE_8,
                 title="ZoneByte8", name="zone_byte_8",
                 checks=(CheckHexList(LEN.ZONE_BYTE_8 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_9, length=LEN.ZONE_BYTE_9,
                 title="ZoneByte9", name="zone_byte_9",
                 checks=(CheckHexList(LEN.ZONE_BYTE_9 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_10, length=LEN.ZONE_BYTE_10,
                 title="ZoneByte10", name="zone_byte_10",
                 checks=(CheckHexList(LEN.ZONE_BYTE_10 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_11, length=LEN.ZONE_BYTE_11,
                 title="ZoneByte11", name="zone_byte_11",
                 checks=(CheckHexList(LEN.ZONE_BYTE_11 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_12, length=LEN.ZONE_BYTE_12,
                 title="ZoneByte12", name="zone_byte_12",
                 checks=(CheckHexList(LEN.ZONE_BYTE_12 // 8),
                         CheckByte(),)),
        BitField(fid=FID.ZONE_BYTE_13, length=LEN.ZONE_BYTE_13,
                 title="ZoneByte13", name="zone_byte_13",
                 checks=(CheckHexList(LEN.ZONE_BYTE_13 // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, type_of_info, param1, zone_byte_0, zone_byte_1, zone_byte_2,
                 zone_byte_3, zone_byte_4, zone_byte_5, zone_byte_6, zone_byte_7, zone_byte_8, zone_byte_9,
                 zone_byte_10, zone_byte_11, zone_byte_12, zone_byte_13, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param type_of_info: This parameter defines the type of information requested
        :type type_of_info: ``int | HexList``
        :param param1: These parameters help to further specify the request in some particular cases
        :type param1: ``int | HexList``
        :param zone_byte_0: 1st Byte of ZoneID Payload
        :type zone_byte_0: ``int | HexList``
        :param zone_byte_1: 2nd Byte of ZoneID Payload
        :type zone_byte_1: ``int | HexList``
        :param zone_byte_2: 3rd Byte of ZoneID Payload
        :type zone_byte_2: ``int | HexList``
        :param zone_byte_3: 4th Byte of ZoneID Payload
        :type zone_byte_3: ``int | HexList``
        :param zone_byte_4: 5th Byte of ZoneID Payload
        :type zone_byte_4: ``int | HexList``
        :param zone_byte_5: 6th Byte of ZoneID Payload
        :type zone_byte_5: ``int | HexList``
        :param zone_byte_6: 7th Byte of ZoneID Payload
        :type zone_byte_6: ``int | HexList``
        :param zone_byte_7: 8th Byte of ZoneID Payload
        :type zone_byte_7: ``int | HexList``
        :param zone_byte_8: 9th Byte of ZoneID Payload
        :type zone_byte_8: ``int | HexList``
        :param zone_byte_9: 10th Byte of ZoneID Payload
        :type zone_byte_9: ``int | HexList``
        :param zone_byte_10: 11th Byte of ZoneID Payload
        :type zone_byte_10: ``int | HexList``
        :param zone_byte_11: 12th Byte of ZoneID Payload
        :type zone_byte_11: ``int | HexList``
        :param zone_byte_12: 13th Byte of ZoneID Payload
        :type zone_byte_12: ``int | HexList``
        :param zone_byte_13: 14th Byte of ZoneID Payload
        :type zone_byte_13: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.type_of_info = type_of_info
        self.param1 = param1
        self.zone_byte_0 = zone_byte_0
        self.zone_byte_1 = zone_byte_1
        self.zone_byte_2 = zone_byte_2
        self.zone_byte_3 = zone_byte_3
        self.zone_byte_4 = zone_byte_4
        self.zone_byte_5 = zone_byte_5
        self.zone_byte_6 = zone_byte_6
        self.zone_byte_7 = zone_byte_7
        self.zone_byte_8 = zone_byte_8
        self.zone_byte_9 = zone_byte_9
        self.zone_byte_10 = zone_byte_10
        self.zone_byte_11 = zone_byte_11
        self.zone_byte_12 = zone_byte_12
        self.zone_byte_13 = zone_byte_13
    # end def __init__
# end class GetInfoResponse


class SetIndividualRGBZones(PerKeyLighting):
    """
    Define ``SetIndividualRGBZones`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone ID 0                 8
    Red Index 0                   8
    Green Index 0                 8
    Blue Index 0                  8
    RGB Zone ID 1                 8
    Red Index 1                   8
    Green Index 1                 8
    Blue Index 1                  8
    RGB Zone ID 2                 8
    Red Index 2                   8
    Green Index 2                 8
    Blue Index 2                  8
    RGB Zone ID 3                 8
    Red Index 3                   8
    Green Index 3                 8
    Blue Index 3                  8
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        RED_INDEX_0 = RGB_ZONE_ID_0 - 1
        GREEN_INDEX_0 = RED_INDEX_0 - 1
        BLUE_INDEX_0 = GREEN_INDEX_0 - 1
        RGB_ZONE_ID_1 = BLUE_INDEX_0 - 1
        RED_INDEX_1 = RGB_ZONE_ID_1 - 1
        GREEN_INDEX_1 = RED_INDEX_1 - 1
        BLUE_INDEX_1 = GREEN_INDEX_1 - 1
        RGB_ZONE_ID_2 = BLUE_INDEX_1 - 1
        RED_INDEX_2 = RGB_ZONE_ID_2 - 1
        GREEN_INDEX_2 = RED_INDEX_2 - 1
        BLUE_INDEX_2 = GREEN_INDEX_2 - 1
        RGB_ZONE_ID_3 = BLUE_INDEX_2 - 1
        RED_INDEX_3 = RGB_ZONE_ID_3 - 1
        GREEN_INDEX_3 = RED_INDEX_3 - 1
        BLUE_INDEX_3 = GREEN_INDEX_3 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_ID_0 = 0x8
        RED_INDEX_0 = 0x8
        GREEN_INDEX_0 = 0x8
        BLUE_INDEX_0 = 0x8
        RGB_ZONE_ID_1 = 0x8
        RED_INDEX_1 = 0x8
        GREEN_INDEX_1 = 0x8
        BLUE_INDEX_1 = 0x8
        RGB_ZONE_ID_2 = 0x8
        RED_INDEX_2 = 0x8
        GREEN_INDEX_2 = 0x8
        BLUE_INDEX_2 = 0x8
        RGB_ZONE_ID_3 = 0x8
        RED_INDEX_3 = 0x8
        GREEN_INDEX_3 = 0x8
        BLUE_INDEX_3 = 0x8
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_0, length=LEN.RED_INDEX_0,
                 title="RedIndex0", name="red_index_0",
                 checks=(CheckHexList(LEN.RED_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_0, length=LEN.GREEN_INDEX_0,
                 title="GreenIndex0", name="green_index_0",
                 checks=(CheckHexList(LEN.GREEN_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_0, length=LEN.BLUE_INDEX_0,
                 title="BlueIndex0", name="blue_index_0",
                 checks=(CheckHexList(LEN.BLUE_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_1, length=LEN.RGB_ZONE_ID_1,
                 title="RgbZoneId1", name="rgb_zone_id_1",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_1, length=LEN.RED_INDEX_1,
                 title="RedIndex1", name="red_index_1",
                 checks=(CheckHexList(LEN.RED_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_1, length=LEN.GREEN_INDEX_1,
                 title="GreenIndex1", name="green_index_1",
                 checks=(CheckHexList(LEN.GREEN_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_1, length=LEN.BLUE_INDEX_1,
                 title="BlueIndex1", name="blue_index_1",
                 checks=(CheckHexList(LEN.BLUE_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_2, length=LEN.RGB_ZONE_ID_2,
                 title="RgbZoneId2", name="rgb_zone_id_2",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_2, length=LEN.RED_INDEX_2,
                 title="RedIndex2", name="red_index_2",
                 checks=(CheckHexList(LEN.RED_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_2, length=LEN.GREEN_INDEX_2,
                 title="GreenIndex2", name="green_index_2",
                 checks=(CheckHexList(LEN.GREEN_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_2, length=LEN.BLUE_INDEX_2,
                 title="BlueIndex2", name="blue_index_2",
                 checks=(CheckHexList(LEN.BLUE_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_3, length=LEN.RGB_ZONE_ID_3,
                 title="RgbZoneId3", name="rgb_zone_id_3",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_3, length=LEN.RED_INDEX_3,
                 title="RedIndex3", name="red_index_3",
                 checks=(CheckHexList(LEN.RED_INDEX_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_3, length=LEN.GREEN_INDEX_3,
                 title="GreenIndex3", name="green_index_3",
                 checks=(CheckHexList(LEN.GREEN_INDEX_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_3, length=LEN.BLUE_INDEX_3,
                 title="BlueIndex3", name="blue_index_3",
                 checks=(CheckHexList(LEN.BLUE_INDEX_3 // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, rgb_zone_id_0, red_index_0, green_index_0, blue_index_0,
                 rgb_zone_id_1=0, red_index_1=0, green_index_1=0, blue_index_1=0, rgb_zone_id_2=0, red_index_2=0,
                 green_index_2=0, blue_index_2=0, rgb_zone_id_3=0, red_index_3=0, green_index_3=0, blue_index_3=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param red_index_0: RGB Zone ID [0] R Component
        :type red_index_0: ``int | HexList``
        :param green_index_0: RGB Zone ID [0] G Component
        :type green_index_0: ``int | HexList``
        :param blue_index_0: RGB Zone ID [0] B Component
        :type blue_index_0: ``int | HexList``
        :param rgb_zone_id_1: RGB Zone ID [1] - OPTIONAL
        :type rgb_zone_id_1: ``int | HexList``
        :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
        :type red_index_1: ``int | HexList``
        :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
        :type green_index_1: ``int | HexList``
        :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
        :type blue_index_1: ``int | HexList``
        :param rgb_zone_id_2: RGB Zone ID [2] - OPTIONAL
        :type rgb_zone_id_2: ``int | HexList``
        :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
        :type red_index_2: ``int | HexList``
        :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
        :type green_index_2: ``int | HexList``
        :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
        :type blue_index_2: ``int | HexList``
        :param rgb_zone_id_3: RGB Zone ID [3] - OPTIONAL
        :type rgb_zone_id_3: ``int | HexList``
        :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
        :type red_index_3: ``int | HexList``
        :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
        :type green_index_3: ``int | HexList``
        :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
        :type blue_index_3: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetIndividualRGBZonesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
        self.red_index_0 = red_index_0
        self.green_index_0 = green_index_0
        self.blue_index_0 = blue_index_0
        self.rgb_zone_id_1 = rgb_zone_id_1
        self.red_index_1 = red_index_1
        self.green_index_1 = green_index_1
        self.blue_index_1 = blue_index_1
        self.rgb_zone_id_2 = rgb_zone_id_2
        self.red_index_2 = red_index_2
        self.green_index_2 = green_index_2
        self.blue_index_2 = blue_index_2
        self.rgb_zone_id_3 = rgb_zone_id_3
        self.red_index_3 = red_index_3
        self.green_index_3 = green_index_3
        self.blue_index_3 = blue_index_3
    # end def __init__
# end class SetIndividualRGBZones


class SetIndividualRGBZonesResponse(PerKeyLighting):
    """
    Define ``SetIndividualRGBZonesResponse`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone ID 0                 8
    RGB Zone ID 1                 8
    RGB Zone ID 2                 8
    RGB Zone ID 3                 8
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetIndividualRGBZones,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 1

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        RGB_ZONE_ID_1 = RGB_ZONE_ID_0 - 1
        RGB_ZONE_ID_2 = RGB_ZONE_ID_1 - 1
        RGB_ZONE_ID_3 = RGB_ZONE_ID_2 - 1
        PADDING = RGB_ZONE_ID_3 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_ID_0 = 0x8
        RGB_ZONE_ID_1 = 0x8
        RGB_ZONE_ID_2 = 0x8
        RGB_ZONE_ID_3 = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_1, length=LEN.RGB_ZONE_ID_1,
                 title="RgbZoneId1", name="rgb_zone_id_1",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_2, length=LEN.RGB_ZONE_ID_2,
                 title="RgbZoneId2", name="rgb_zone_id_2",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_3, length=LEN.RGB_ZONE_ID_3,
                 title="RgbZoneId3", name="rgb_zone_id_3",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rgb_zone_id_0, rgb_zone_id_1=0, rgb_zone_id_2=0, rgb_zone_id_3=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param rgb_zone_id_1: RGB Zone ID [1] - OPTIONAL
        :type rgb_zone_id_1: ``int | HexList``
        :param rgb_zone_id_2: RGB Zone ID [2] - OPTIONAL
        :type rgb_zone_id_2: ``int | HexList``
        :param rgb_zone_id_3: RGB Zone ID [3] - OPTIONAL
        :type rgb_zone_id_3: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
        self.rgb_zone_id_1 = rgb_zone_id_1
        self.rgb_zone_id_2 = rgb_zone_id_2
        self.rgb_zone_id_3 = rgb_zone_id_3
    # end def __init__
# end class SetIndividualRGBZonesResponse


class SetConsecutiveRGBZones(PerKeyLighting):
    """
    Define ``SetConsecutiveRGBZones`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone ID 0                 8
    Red Index 0                   8
    Green Index 0                 8
    Blue Index 0                  8
    Red Index 1                   8
    Green Index 1                 8
    Blue Index 1                  8
    Red Index 2                   8
    Green Index 2                 8
    Blue Index 2                  8
    Red Index 3                   8
    Green Index 3                 8
    Blue Index 3                  8
    Red Index 4                   8
    Green Index 4                 8
    Blue Index 4                  8
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        RED_INDEX_0 = RGB_ZONE_ID_0 - 1
        GREEN_INDEX_0 = RED_INDEX_0 - 1
        BLUE_INDEX_0 = GREEN_INDEX_0 - 1
        RED_INDEX_1 = BLUE_INDEX_0 - 1
        GREEN_INDEX_1 = RED_INDEX_1 - 1
        BLUE_INDEX_1 = GREEN_INDEX_1 - 1
        RED_INDEX_2 = BLUE_INDEX_1 - 1
        GREEN_INDEX_2 = RED_INDEX_2 - 1
        BLUE_INDEX_2 = GREEN_INDEX_2 - 1
        RED_INDEX_3 = BLUE_INDEX_2 - 1
        GREEN_INDEX_3 = RED_INDEX_3 - 1
        BLUE_INDEX_3 = GREEN_INDEX_3 - 1
        RED_INDEX_4 = BLUE_INDEX_3 - 1
        GREEN_INDEX_4 = RED_INDEX_4 - 1
        BLUE_INDEX_4 = GREEN_INDEX_4 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_ID_0 = 0x8
        RED_INDEX_0 = 0x8
        GREEN_INDEX_0 = 0x8
        BLUE_INDEX_0 = 0x8
        RED_INDEX_1 = 0x8
        GREEN_INDEX_1 = 0x8
        BLUE_INDEX_1 = 0x8
        RED_INDEX_2 = 0x8
        GREEN_INDEX_2 = 0x8
        BLUE_INDEX_2 = 0x8
        RED_INDEX_3 = 0x8
        GREEN_INDEX_3 = 0x8
        BLUE_INDEX_3 = 0x8
        RED_INDEX_4 = 0x8
        GREEN_INDEX_4 = 0x8
        BLUE_INDEX_4 = 0x8
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_0, length=LEN.RED_INDEX_0,
                 title="RedIndex0", name="red_index_0",
                 checks=(CheckHexList(LEN.RED_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_0, length=LEN.GREEN_INDEX_0,
                 title="GreenIndex0", name="green_index_0",
                 checks=(CheckHexList(LEN.GREEN_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_0, length=LEN.BLUE_INDEX_0,
                 title="BlueIndex0", name="blue_index_0",
                 checks=(CheckHexList(LEN.BLUE_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_1, length=LEN.RED_INDEX_1,
                 title="RedIndex1", name="red_index_1",
                 checks=(CheckHexList(LEN.RED_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_1, length=LEN.GREEN_INDEX_1,
                 title="GreenIndex1", name="green_index_1",
                 checks=(CheckHexList(LEN.GREEN_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_1, length=LEN.BLUE_INDEX_1,
                 title="BlueIndex1", name="blue_index_1",
                 checks=(CheckHexList(LEN.BLUE_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_2, length=LEN.RED_INDEX_2,
                 title="RedIndex2", name="red_index_2",
                 checks=(CheckHexList(LEN.RED_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_2, length=LEN.GREEN_INDEX_2,
                 title="GreenIndex2", name="green_index_2",
                 checks=(CheckHexList(LEN.GREEN_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_2, length=LEN.BLUE_INDEX_2,
                 title="BlueIndex2", name="blue_index_2",
                 checks=(CheckHexList(LEN.BLUE_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_3, length=LEN.RED_INDEX_3,
                 title="RedIndex3", name="red_index_3",
                 checks=(CheckHexList(LEN.RED_INDEX_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_3, length=LEN.GREEN_INDEX_3,
                 title="GreenIndex3", name="green_index_3",
                 checks=(CheckHexList(LEN.GREEN_INDEX_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_3, length=LEN.BLUE_INDEX_3,
                 title="BlueIndex3", name="blue_index_3",
                 checks=(CheckHexList(LEN.BLUE_INDEX_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_4, length=LEN.RED_INDEX_4,
                 title="RedIndex4", name="red_index_4",
                 checks=(CheckHexList(LEN.RED_INDEX_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_4, length=LEN.GREEN_INDEX_4,
                 title="GreenIndex4", name="green_index_4",
                 checks=(CheckHexList(LEN.GREEN_INDEX_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_4, length=LEN.BLUE_INDEX_4,
                 title="BlueIndex4", name="blue_index_4",
                 checks=(CheckHexList(LEN.BLUE_INDEX_4 // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, rgb_zone_id_0, red_index_0, green_index_0, blue_index_0,
                 red_index_1=0, green_index_1=0, blue_index_1=0, red_index_2=0, green_index_2=0, blue_index_2=0,
                 red_index_3=0, green_index_3=0, blue_index_3=0, red_index_4=0, green_index_4=0, blue_index_4=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: Starting Zone ID, RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param red_index_0: RGB Zone ID [0] R Component
        :type red_index_0: ``int | HexList``
        :param green_index_0: RGB Zone ID [0] G Component
        :type green_index_0: ``int | HexList``
        :param blue_index_0: RGB Zone ID [0] B Component
        :type blue_index_0: ``int | HexList``
        :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
        :type red_index_1: ``int | HexList``
        :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
        :type green_index_1: ``int | HexList``
        :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
        :type blue_index_1: ``int | HexList``
        :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
        :type red_index_2: ``int | HexList``
        :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
        :type green_index_2: ``int | HexList``
        :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
        :type blue_index_2: ``int | HexList``
        :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
        :type red_index_3: ``int | HexList``
        :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
        :type green_index_3: ``int | HexList``
        :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
        :type blue_index_3: ``int | HexList``
        :param red_index_4: RGB Zone ID [4] R Component - OPTIONAL
        :type red_index_4: ``int | HexList``
        :param green_index_4: RGB Zone ID [4] G Component - OPTIONAL
        :type green_index_4: ``int | HexList``
        :param blue_index_4: RGB Zone ID [4] B Component - OPTIONAL
        :type blue_index_4: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetConsecutiveRGBZonesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
        self.red_index_0 = red_index_0
        self.green_index_0 = green_index_0
        self.blue_index_0 = blue_index_0
        self.red_index_1 = red_index_1
        self.green_index_1 = green_index_1
        self.blue_index_1 = blue_index_1
        self.red_index_2 = red_index_2
        self.green_index_2 = green_index_2
        self.blue_index_2 = blue_index_2
        self.red_index_3 = red_index_3
        self.green_index_3 = green_index_3
        self.blue_index_3 = blue_index_3
        self.red_index_4 = red_index_4
        self.green_index_4 = green_index_4
        self.blue_index_4 = blue_index_4
    # end def __init__
# end class SetConsecutiveRGBZones


class SetConsecutiveRGBZonesResponse(RGBZoneIDResponseHead):
    """
    Define ``SetConsecutiveRGBZonesResponse`` implementation class for version 0, 2
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetConsecutiveRGBZones,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, rgb_zone_id_0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
    # end def __init__
# end class SetConsecutiveRGBZonesResponse


class SetConsecutiveRGBZonesDeltaCompression5bit(PerKeyLighting):
    """
    Define ``SetConsecutiveRGBZonesDeltaCompression5bit`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone ID 0                 8
    Red Index 0                   5
    Green Index 0                 5
    Blue Index 0                  5
    Red Index 1                   5
    Green Index 1                 5
    Blue Index 1                  5
    Red Index 2                   5
    Green Index 2                 5
    Blue Index 2                  5
    Red Index 3                   5
    Green Index 3                 5
    Blue Index 3                  5
    Red Index 4                   5
    Green Index 4                 5
    Blue Index 4                  5
    Red Index 5                   5
    Green Index 5                 5
    Blue Index 5                  5
    Red Index 6                   5
    Green Index 6                 5
    Blue Index 6                  5
    Red Index 7                   5
    Green Index 7                 5
    Blue Index 7                  5
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        RED_INDEX_0 = RGB_ZONE_ID_0 - 1
        GREEN_INDEX_0 = RED_INDEX_0 - 1
        BLUE_INDEX_0 = GREEN_INDEX_0 - 1
        RED_INDEX_1 = BLUE_INDEX_0 - 1
        GREEN_INDEX_1 = RED_INDEX_1 - 1
        BLUE_INDEX_1 = GREEN_INDEX_1 - 1
        RED_INDEX_2 = BLUE_INDEX_1 - 1
        GREEN_INDEX_2 = RED_INDEX_2 - 1
        BLUE_INDEX_2 = GREEN_INDEX_2 - 1
        RED_INDEX_3 = BLUE_INDEX_2 - 1
        GREEN_INDEX_3 = RED_INDEX_3 - 1
        BLUE_INDEX_3 = GREEN_INDEX_3 - 1
        RED_INDEX_4 = BLUE_INDEX_3 - 1
        GREEN_INDEX_4 = RED_INDEX_4 - 1
        BLUE_INDEX_4 = GREEN_INDEX_4 - 1
        RED_INDEX_5 = BLUE_INDEX_4 - 1
        GREEN_INDEX_5 = RED_INDEX_5 - 1
        BLUE_INDEX_5 = GREEN_INDEX_5 - 1
        RED_INDEX_6 = BLUE_INDEX_5 - 1
        GREEN_INDEX_6 = RED_INDEX_6 - 1
        BLUE_INDEX_6 = GREEN_INDEX_6 - 1
        RED_INDEX_7 = BLUE_INDEX_6 - 1
        GREEN_INDEX_7 = RED_INDEX_7 - 1
        BLUE_INDEX_7 = GREEN_INDEX_7 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_ID_0 = 0x8
        RED_INDEX_0 = 0x5
        GREEN_INDEX_0 = 0x5
        BLUE_INDEX_0 = 0x5
        RED_INDEX_1 = 0x5
        GREEN_INDEX_1 = 0x5
        BLUE_INDEX_1 = 0x5
        RED_INDEX_2 = 0x5
        GREEN_INDEX_2 = 0x5
        BLUE_INDEX_2 = 0x5
        RED_INDEX_3 = 0x5
        GREEN_INDEX_3 = 0x5
        BLUE_INDEX_3 = 0x5
        RED_INDEX_4 = 0x5
        GREEN_INDEX_4 = 0x5
        BLUE_INDEX_4 = 0x5
        RED_INDEX_5 = 0x5
        GREEN_INDEX_5 = 0x5
        BLUE_INDEX_5 = 0x5
        RED_INDEX_6 = 0x5
        GREEN_INDEX_6 = 0x5
        BLUE_INDEX_6 = 0x5
        RED_INDEX_7 = 0x5
        GREEN_INDEX_7 = 0x5
        BLUE_INDEX_7 = 0x5
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_0, length=LEN.RED_INDEX_0,
                 title="RedIndex0", name="red_index_0",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_0) - 1),)),
        BitField(fid=FID.GREEN_INDEX_0, length=LEN.GREEN_INDEX_0,
                 title="GreenIndex0", name="green_index_0",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_0) - 1),)),
        BitField(fid=FID.BLUE_INDEX_0, length=LEN.BLUE_INDEX_0,
                 title="BlueIndex0", name="blue_index_0",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_0) - 1),)),
        BitField(fid=FID.RED_INDEX_1, length=LEN.RED_INDEX_1,
                 title="RedIndex1", name="red_index_1",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_1) - 1),)),
        BitField(fid=FID.GREEN_INDEX_1, length=LEN.GREEN_INDEX_1,
                 title="GreenIndex1", name="green_index_1",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_1) - 1),)),
        BitField(fid=FID.BLUE_INDEX_1, length=LEN.BLUE_INDEX_1,
                 title="BlueIndex1", name="blue_index_1",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_1) - 1),)),
        BitField(fid=FID.RED_INDEX_2, length=LEN.RED_INDEX_2,
                 title="RedIndex2", name="red_index_2",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_2) - 1),)),
        BitField(fid=FID.GREEN_INDEX_2, length=LEN.GREEN_INDEX_2,
                 title="GreenIndex2", name="green_index_2",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_2) - 1),)),
        BitField(fid=FID.BLUE_INDEX_2, length=LEN.BLUE_INDEX_2,
                 title="BlueIndex2", name="blue_index_2",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_2) - 1),)),
        BitField(fid=FID.RED_INDEX_3, length=LEN.RED_INDEX_3,
                 title="RedIndex3", name="red_index_3",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_3) - 1),)),
        BitField(fid=FID.GREEN_INDEX_3, length=LEN.GREEN_INDEX_3,
                 title="GreenIndex3", name="green_index_3",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_3) - 1),)),
        BitField(fid=FID.BLUE_INDEX_3, length=LEN.BLUE_INDEX_3,
                 title="BlueIndex3", name="blue_index_3",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_3) - 1),)),
        BitField(fid=FID.RED_INDEX_4, length=LEN.RED_INDEX_4,
                 title="RedIndex4", name="red_index_4",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_4) - 1),)),
        BitField(fid=FID.GREEN_INDEX_4, length=LEN.GREEN_INDEX_4,
                 title="GreenIndex4", name="green_index_4",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_4) - 1),)),
        BitField(fid=FID.BLUE_INDEX_4, length=LEN.BLUE_INDEX_4,
                 title="BlueIndex4", name="blue_index_4",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_4) - 1),)),
        BitField(fid=FID.RED_INDEX_5, length=LEN.RED_INDEX_5,
                 title="RedIndex5", name="red_index_5",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_5) - 1),)),
        BitField(fid=FID.GREEN_INDEX_5, length=LEN.GREEN_INDEX_5,
                 title="GreenIndex5", name="green_index_5",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_5) - 1),)),
        BitField(fid=FID.BLUE_INDEX_5, length=LEN.BLUE_INDEX_5,
                 title="BlueIndex5", name="blue_index_5",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_5) - 1),)),
        BitField(fid=FID.RED_INDEX_6, length=LEN.RED_INDEX_6,
                 title="RedIndex6", name="red_index_6",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_6) - 1),)),
        BitField(fid=FID.GREEN_INDEX_6, length=LEN.GREEN_INDEX_6,
                 title="GreenIndex6", name="green_index_6",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_6) - 1),)),
        BitField(fid=FID.BLUE_INDEX_6, length=LEN.BLUE_INDEX_6,
                 title="BlueIndex6", name="blue_index_6",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_6) - 1),)),
        BitField(fid=FID.RED_INDEX_7, length=LEN.RED_INDEX_7,
                 title="RedIndex7", name="red_index_7",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_7) - 1),)),
        BitField(fid=FID.GREEN_INDEX_7, length=LEN.GREEN_INDEX_7,
                 title="GreenIndex7", name="green_index_7",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_7) - 1),)),
        BitField(fid=FID.BLUE_INDEX_7, length=LEN.BLUE_INDEX_7,
                 title="BlueIndex7", name="blue_index_7",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_7) - 1),)),
    )

    def __init__(self, device_index, feature_index, rgb_zone_id_0, red_index_0, green_index_0, blue_index_0,
                 red_index_1=0, green_index_1=0, blue_index_1=0, red_index_2=0, green_index_2=0, blue_index_2=0,
                 red_index_3=0, green_index_3=0, blue_index_3=0, red_index_4=0, green_index_4=0, blue_index_4=0,
                 red_index_5=0, green_index_5=0, blue_index_5=0, red_index_6=0, green_index_6=0, blue_index_6=0,
                 red_index_7=0, green_index_7=0, blue_index_7=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: Starting Zone ID, RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param red_index_0: RGB Zone ID [0] R Component
        :type red_index_0: ``int | HexList``
        :param green_index_0: RGB Zone ID [0] G Component
        :type green_index_0: ``int | HexList``
        :param blue_index_0: RGB Zone ID [0] B Component
        :type blue_index_0: ``int | HexList``
        :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
        :type red_index_1: ``int | HexList``
        :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
        :type green_index_1: ``int | HexList``
        :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
        :type blue_index_1: ``int | HexList``
        :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
        :type red_index_2: ``int | HexList``
        :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
        :type green_index_2: ``int | HexList``
        :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
        :type blue_index_2: ``int | HexList``
        :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
        :type red_index_3: ``int | HexList``
        :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
        :type green_index_3: ``int | HexList``
        :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
        :type blue_index_3: ``int | HexList``
        :param red_index_4: RGB Zone ID [4] R Component - OPTIONAL
        :type red_index_4: ``int | HexList``
        :param green_index_4: RGB Zone ID [4] G Component - OPTIONAL
        :type green_index_4: ``int | HexList``
        :param blue_index_4: RGB Zone ID [4] B Component - OPTIONAL
        :type blue_index_4: ``int | HexList``
        :param red_index_5: RGB Zone ID [5] R Component - OPTIONAL
        :type red_index_5: ``int | HexList``
        :param green_index_5: RGB Zone ID [5] G Component - OPTIONAL
        :type green_index_5: ``int | HexList``
        :param blue_index_5: RGB Zone ID [5] B Component - OPTIONAL
        :type blue_index_5: ``int | HexList``
        :param red_index_6: RGB Zone ID [6] R Component - OPTIONAL
        :type red_index_6: ``int | HexList``
        :param green_index_6: RGB Zone ID [6] G Component - OPTIONAL
        :type green_index_6: ``int | HexList``
        :param blue_index_6: RGB Zone ID [6] B Component - OPTIONAL
        :type blue_index_6: ``int | HexList``
        :param red_index_7: RGB Zone ID [7] R Component - OPTIONAL
        :type red_index_7: ``int | HexList``
        :param green_index_7: RGB Zone ID [7] G Component - OPTIONAL
        :type green_index_7: ``int | HexList``
        :param blue_index_7: RGB Zone ID [7] B Component - OPTIONAL
        :type blue_index_7: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetConsecutiveRGBZonesDeltaCompression5bitResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
        self.red_index_0 = red_index_0
        self.green_index_0 = green_index_0
        self.blue_index_0 = blue_index_0
        self.red_index_1 = red_index_1
        self.green_index_1 = green_index_1
        self.blue_index_1 = blue_index_1
        self.red_index_2 = red_index_2
        self.green_index_2 = green_index_2
        self.blue_index_2 = blue_index_2
        self.red_index_3 = red_index_3
        self.green_index_3 = green_index_3
        self.blue_index_3 = blue_index_3
        self.red_index_4 = red_index_4
        self.green_index_4 = green_index_4
        self.blue_index_4 = blue_index_4
        self.red_index_5 = red_index_5
        self.green_index_5 = green_index_5
        self.blue_index_5 = blue_index_5
        self.red_index_6 = red_index_6
        self.green_index_6 = green_index_6
        self.blue_index_6 = blue_index_6
        self.red_index_7 = red_index_7
        self.green_index_7 = green_index_7
        self.blue_index_7 = blue_index_7
    # end def __init__
# end class SetConsecutiveRGBZonesDeltaCompression5bit


class SetConsecutiveRGBZonesDeltaCompression5bitResponse(RGBZoneIDResponseHead):
    """
    Define ``SetConsecutiveRGBZonesDeltaCompression5bitResponse`` implementation class for version 0, 2
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetConsecutiveRGBZonesDeltaCompression5bit,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, rgb_zone_id_0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
    # end def __init__
# end class SetConsecutiveRGBZonesDeltaCompression5bitResponse


class SetConsecutiveRGBZonesDeltaCompression4bit(PerKeyLighting):
    """
    Define ``SetConsecutiveRGBZonesDeltaCompression4bit`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone ID 0                 8
    Red Index 0                   4
    Green Index 0                 4
    Blue Index 0                  4
    Red Index 1                   4
    Green Index 1                 4
    Blue Index 1                  4
    Red Index 2                   4
    Green Index 2                 4
    Blue Index 2                  4
    Red Index 3                   4
    Green Index 3                 4
    Blue Index 3                  4
    Red Index 4                   4
    Green Index 4                 4
    Blue Index 4                  4
    Red Index 5                   4
    Green Index 5                 4
    Blue Index 5                  4
    Red Index 6                   4
    Green Index 6                 4
    Blue Index 6                  4
    Red Index 7                   4
    Green Index 7                 4
    Blue Index 7                  4
    Red Index 8                   4
    Green Index 8                 4
    Blue Index 8                  4
    Red Index 9                   4
    Green Index 9                 4
    Blue Index 9                  4
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        RED_INDEX_0 = RGB_ZONE_ID_0 - 1
        GREEN_INDEX_0 = RED_INDEX_0 - 1
        BLUE_INDEX_0 = GREEN_INDEX_0 - 1
        RED_INDEX_1 = BLUE_INDEX_0 - 1
        GREEN_INDEX_1 = RED_INDEX_1 - 1
        BLUE_INDEX_1 = GREEN_INDEX_1 - 1
        RED_INDEX_2 = BLUE_INDEX_1 - 1
        GREEN_INDEX_2 = RED_INDEX_2 - 1
        BLUE_INDEX_2 = GREEN_INDEX_2 - 1
        RED_INDEX_3 = BLUE_INDEX_2 - 1
        GREEN_INDEX_3 = RED_INDEX_3 - 1
        BLUE_INDEX_3 = GREEN_INDEX_3 - 1
        RED_INDEX_4 = BLUE_INDEX_3 - 1
        GREEN_INDEX_4 = RED_INDEX_4 - 1
        BLUE_INDEX_4 = GREEN_INDEX_4 - 1
        RED_INDEX_5 = BLUE_INDEX_4 - 1
        GREEN_INDEX_5 = RED_INDEX_5 - 1
        BLUE_INDEX_5 = GREEN_INDEX_5 - 1
        RED_INDEX_6 = BLUE_INDEX_5 - 1
        GREEN_INDEX_6 = RED_INDEX_6 - 1
        BLUE_INDEX_6 = GREEN_INDEX_6 - 1
        RED_INDEX_7 = BLUE_INDEX_6 - 1
        GREEN_INDEX_7 = RED_INDEX_7 - 1
        BLUE_INDEX_7 = GREEN_INDEX_7 - 1
        RED_INDEX_8 = BLUE_INDEX_7 - 1
        GREEN_INDEX_8 = RED_INDEX_8 - 1
        BLUE_INDEX_8 = GREEN_INDEX_8 - 1
        RED_INDEX_9 = BLUE_INDEX_8 - 1
        GREEN_INDEX_9 = RED_INDEX_9 - 1
        BLUE_INDEX_9 = GREEN_INDEX_9 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_ID_0 = 0x8
        RED_INDEX_0 = 0x4
        GREEN_INDEX_0 = 0x4
        BLUE_INDEX_0 = 0x4
        RED_INDEX_1 = 0x4
        GREEN_INDEX_1 = 0x4
        BLUE_INDEX_1 = 0x4
        RED_INDEX_2 = 0x4
        GREEN_INDEX_2 = 0x4
        BLUE_INDEX_2 = 0x4
        RED_INDEX_3 = 0x4
        GREEN_INDEX_3 = 0x4
        BLUE_INDEX_3 = 0x4
        RED_INDEX_4 = 0x4
        GREEN_INDEX_4 = 0x4
        BLUE_INDEX_4 = 0x4
        RED_INDEX_5 = 0x4
        GREEN_INDEX_5 = 0x4
        BLUE_INDEX_5 = 0x4
        RED_INDEX_6 = 0x4
        GREEN_INDEX_6 = 0x4
        BLUE_INDEX_6 = 0x4
        RED_INDEX_7 = 0x4
        GREEN_INDEX_7 = 0x4
        BLUE_INDEX_7 = 0x4
        RED_INDEX_8 = 0x4
        GREEN_INDEX_8 = 0x4
        BLUE_INDEX_8 = 0x4
        RED_INDEX_9 = 0x4
        GREEN_INDEX_9 = 0x4
        BLUE_INDEX_9 = 0x4
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_0, length=LEN.RED_INDEX_0,
                 title="RedIndex0", name="red_index_0",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_0) - 1),)),
        BitField(fid=FID.GREEN_INDEX_0, length=LEN.GREEN_INDEX_0,
                 title="GreenIndex0", name="green_index_0",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_0) - 1),)),
        BitField(fid=FID.BLUE_INDEX_0, length=LEN.BLUE_INDEX_0,
                 title="BlueIndex0", name="blue_index_0",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_0) - 1),)),
        BitField(fid=FID.RED_INDEX_1, length=LEN.RED_INDEX_1,
                 title="RedIndex1", name="red_index_1",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_1) - 1),)),
        BitField(fid=FID.GREEN_INDEX_1, length=LEN.GREEN_INDEX_1,
                 title="GreenIndex1", name="green_index_1",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_1) - 1),)),
        BitField(fid=FID.BLUE_INDEX_1, length=LEN.BLUE_INDEX_1,
                 title="BlueIndex1", name="blue_index_1",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_1) - 1),)),
        BitField(fid=FID.RED_INDEX_2, length=LEN.RED_INDEX_2,
                 title="RedIndex2", name="red_index_2",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_2) - 1),)),
        BitField(fid=FID.GREEN_INDEX_2, length=LEN.GREEN_INDEX_2,
                 title="GreenIndex2", name="green_index_2",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_2) - 1),)),
        BitField(fid=FID.BLUE_INDEX_2, length=LEN.BLUE_INDEX_2,
                 title="BlueIndex2", name="blue_index_2",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_2) - 1),)),
        BitField(fid=FID.RED_INDEX_3, length=LEN.RED_INDEX_3,
                 title="RedIndex3", name="red_index_3",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_3) - 1),)),
        BitField(fid=FID.GREEN_INDEX_3, length=LEN.GREEN_INDEX_3,
                 title="GreenIndex3", name="green_index_3",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_3) - 1),)),
        BitField(fid=FID.BLUE_INDEX_3, length=LEN.BLUE_INDEX_3,
                 title="BlueIndex3", name="blue_index_3",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_3) - 1),)),
        BitField(fid=FID.RED_INDEX_4, length=LEN.RED_INDEX_4,
                 title="RedIndex4", name="red_index_4",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_4) - 1),)),
        BitField(fid=FID.GREEN_INDEX_4, length=LEN.GREEN_INDEX_4,
                 title="GreenIndex4", name="green_index_4",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_4) - 1),)),
        BitField(fid=FID.BLUE_INDEX_4, length=LEN.BLUE_INDEX_4,
                 title="BlueIndex4", name="blue_index_4",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_4) - 1),)),
        BitField(fid=FID.RED_INDEX_5, length=LEN.RED_INDEX_5,
                 title="RedIndex5", name="red_index_5",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_5) - 1),)),
        BitField(fid=FID.GREEN_INDEX_5, length=LEN.GREEN_INDEX_5,
                 title="GreenIndex5", name="green_index_5",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_5) - 1),)),
        BitField(fid=FID.BLUE_INDEX_5, length=LEN.BLUE_INDEX_5,
                 title="BlueIndex5", name="blue_index_5",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_5) - 1),)),
        BitField(fid=FID.RED_INDEX_6, length=LEN.RED_INDEX_6,
                 title="RedIndex6", name="red_index_6",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_6) - 1),)),
        BitField(fid=FID.GREEN_INDEX_6, length=LEN.GREEN_INDEX_6,
                 title="GreenIndex6", name="green_index_6",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_6) - 1),)),
        BitField(fid=FID.BLUE_INDEX_6, length=LEN.BLUE_INDEX_6,
                 title="BlueIndex6", name="blue_index_6",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_6) - 1),)),
        BitField(fid=FID.RED_INDEX_7, length=LEN.RED_INDEX_7,
                 title="RedIndex7", name="red_index_7",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_7) - 1),)),
        BitField(fid=FID.GREEN_INDEX_7, length=LEN.GREEN_INDEX_7,
                 title="GreenIndex7", name="green_index_7",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_7) - 1),)),
        BitField(fid=FID.BLUE_INDEX_7, length=LEN.BLUE_INDEX_7,
                 title="BlueIndex7", name="blue_index_7",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_7) - 1),)),
        BitField(fid=FID.RED_INDEX_8, length=LEN.RED_INDEX_8,
                 title="RedIndex8", name="red_index_8",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_8) - 1),)),
        BitField(fid=FID.GREEN_INDEX_8, length=LEN.GREEN_INDEX_8,
                 title="GreenIndex8", name="green_index_8",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_8) - 1),)),
        BitField(fid=FID.BLUE_INDEX_8, length=LEN.BLUE_INDEX_8,
                 title="BlueIndex8", name="blue_index_8",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_8) - 1),)),
        BitField(fid=FID.RED_INDEX_9, length=LEN.RED_INDEX_9,
                 title="RedIndex9", name="red_index_9",
                 checks=(CheckInt(0, pow(2, LEN.RED_INDEX_9) - 1),)),
        BitField(fid=FID.GREEN_INDEX_9, length=LEN.GREEN_INDEX_9,
                 title="GreenIndex9", name="green_index_9",
                 checks=(CheckInt(0, pow(2, LEN.GREEN_INDEX_9) - 1),)),
        BitField(fid=FID.BLUE_INDEX_9, length=LEN.BLUE_INDEX_9,
                 title="BlueIndex9", name="blue_index_9",
                 checks=(CheckInt(0, pow(2, LEN.BLUE_INDEX_9) - 1),)),
    )

    def __init__(self, device_index, feature_index, rgb_zone_id_0, red_index_0, green_index_0, blue_index_0,
                 red_index_1=0, green_index_1=0, blue_index_1=0, red_index_2=0, green_index_2=0, blue_index_2=0,
                 red_index_3=0, green_index_3=0, blue_index_3=0, red_index_4=0, green_index_4=0, blue_index_4=0,
                 red_index_5=0, green_index_5=0, blue_index_5=0, red_index_6=0, green_index_6=0, blue_index_6=0,
                 red_index_7=0, green_index_7=0, blue_index_7=0, red_index_8=0, green_index_8=0, blue_index_8=0,
                 red_index_9=0, green_index_9=0, blue_index_9=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: Starting Zone ID, RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param red_index_0: RGB Zone ID [0] R Component
        :type red_index_0: ``int | HexList``
        :param green_index_0: RGB Zone ID [0] G Component
        :type green_index_0: ``int | HexList``
        :param blue_index_0: RGB Zone ID [0] B Component
        :type blue_index_0: ``int | HexList``
        :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
        :type red_index_1: ``int | HexList``
        :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
        :type green_index_1: ``int | HexList``
        :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
        :type blue_index_1: ``int | HexList``
        :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
        :type red_index_2: ``int | HexList``
        :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
        :type green_index_2: ``int | HexList``
        :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
        :type blue_index_2: ``int | HexList``
        :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
        :type red_index_3: ``int | HexList``
        :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
        :type green_index_3: ``int | HexList``
        :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
        :type blue_index_3: ``int | HexList``
        :param red_index_4: RGB Zone ID [4] R Component - OPTIONAL
        :type red_index_4: ``int | HexList``
        :param green_index_4: RGB Zone ID [4] G Component - OPTIONAL
        :type green_index_4: ``int | HexList``
        :param blue_index_4: RGB Zone ID [4] B Component - OPTIONAL
        :type blue_index_4: ``int | HexList``
        :param red_index_5: RGB Zone ID [5] R Component - OPTIONAL
        :type red_index_5: ``int | HexList``
        :param green_index_5: RGB Zone ID [5] G Component - OPTIONAL
        :type green_index_5: ``int | HexList``
        :param blue_index_5: RGB Zone ID [5] B Component - OPTIONAL
        :type blue_index_5: ``int | HexList``
        :param red_index_6: RGB Zone ID [6] R Component - OPTIONAL
        :type red_index_6: ``int | HexList``
        :param green_index_6: RGB Zone ID [6] G Component - OPTIONAL
        :type green_index_6: ``int | HexList``
        :param blue_index_6: RGB Zone ID [6] B Component - OPTIONAL
        :type blue_index_6: ``int | HexList``
        :param red_index_7: RGB Zone ID [7] R Component - OPTIONAL
        :type red_index_7: ``int | HexList``
        :param green_index_7: RGB Zone ID [7] G Component - OPTIONAL
        :type green_index_7: ``int | HexList``
        :param blue_index_7: RGB Zone ID [7] B Component - OPTIONAL
        :type blue_index_7: ``int | HexList``
        :param red_index_8: RGB Zone ID [8] R Component - OPTIONAL
        :type red_index_8: ``int | HexList``
        :param green_index_8: RGB Zone ID [8] G Component - OPTIONAL
        :type green_index_8: ``int | HexList``
        :param blue_index_8: RGB Zone ID [8] B Component - OPTIONAL
        :type blue_index_8: ``int | HexList``
        :param red_index_9: RGB Zone ID [9] R Component - OPTIONAL
        :type red_index_9: ``int | HexList``
        :param green_index_9: RGB Zone ID [9] G Component - OPTIONAL
        :type green_index_9: ``int | HexList``
        :param blue_index_9: RGB Zone ID [9] B Component - OPTIONAL
        :type blue_index_9: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetConsecutiveRGBZonesDeltaCompression4bitResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
        self.red_index_0 = red_index_0
        self.green_index_0 = green_index_0
        self.blue_index_0 = blue_index_0
        self.red_index_1 = red_index_1
        self.green_index_1 = green_index_1
        self.blue_index_1 = blue_index_1
        self.red_index_2 = red_index_2
        self.green_index_2 = green_index_2
        self.blue_index_2 = blue_index_2
        self.red_index_3 = red_index_3
        self.green_index_3 = green_index_3
        self.blue_index_3 = blue_index_3
        self.red_index_4 = red_index_4
        self.green_index_4 = green_index_4
        self.blue_index_4 = blue_index_4
        self.red_index_5 = red_index_5
        self.green_index_5 = green_index_5
        self.blue_index_5 = blue_index_5
        self.red_index_6 = red_index_6
        self.green_index_6 = green_index_6
        self.blue_index_6 = blue_index_6
        self.red_index_7 = red_index_7
        self.green_index_7 = green_index_7
        self.blue_index_7 = blue_index_7
        self.red_index_8 = red_index_8
        self.green_index_8 = green_index_8
        self.blue_index_8 = blue_index_8
        self.red_index_9 = red_index_9
        self.green_index_9 = green_index_9
        self.blue_index_9 = blue_index_9
    # end def __init__
# end class SetConsecutiveRGBZonesDeltaCompression4bit


class SetConsecutiveRGBZonesDeltaCompression4bitResponse(RGBZoneIDResponseHead):
    """
    Define ``SetConsecutiveRGBZonesDeltaCompression4bitResponse`` implementation class for version 0, 2
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetConsecutiveRGBZonesDeltaCompression4bit,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, rgb_zone_id_0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_id_0: RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_id_0 = rgb_zone_id_0
    # end def __init__
# end class SetConsecutiveRGBZonesDeltaCompression4bitResponse


class SetRangeRGBZones(PerKeyLighting):
    """
    Define ``SetRangeRGBZones`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB First Zone ID 0           8
    RGB Last Zone ID 0            8
    Red Index 0                   8
    Green Index 0                 8
    Blue Index 0                  8
    RGB First Zone ID 1           8
    RGB Last Zone ID 1            8
    Red Index 1                   8
    Green Index 1                 8
    Blue Index 1                  8
    RGB First Zone ID 2           8
    RGB Last Zone ID 2            8
    Red Index 2                   8
    Green Index 2                 8
    Blue Index 2                  8
    Padding                       8
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_FIRST_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        RGB_LAST_ZONE_ID_0 = RGB_FIRST_ZONE_ID_0 - 1
        RED_INDEX_0 = RGB_LAST_ZONE_ID_0 - 1
        GREEN_INDEX_0 = RED_INDEX_0 - 1
        BLUE_INDEX_0 = GREEN_INDEX_0 - 1
        RGB_FIRST_ZONE_ID_1 = BLUE_INDEX_0 - 1
        RGB_LAST_ZONE_ID_1 = RGB_FIRST_ZONE_ID_1 - 1
        RED_INDEX_1 = RGB_LAST_ZONE_ID_1 - 1
        GREEN_INDEX_1 = RED_INDEX_1 - 1
        BLUE_INDEX_1 = GREEN_INDEX_1 - 1
        RGB_FIRST_ZONE_ID_2 = BLUE_INDEX_1 - 1
        RGB_LAST_ZONE_ID_2 = RGB_FIRST_ZONE_ID_2 - 1
        RED_INDEX_2 = RGB_LAST_ZONE_ID_2 - 1
        GREEN_INDEX_2 = RED_INDEX_2 - 1
        BLUE_INDEX_2 = GREEN_INDEX_2 - 1
        PADDING = BLUE_INDEX_2 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_FIRST_ZONE_ID_0 = 0x8
        RGB_LAST_ZONE_ID_0 = 0x8
        RED_INDEX_0 = 0x8
        GREEN_INDEX_0 = 0x8
        BLUE_INDEX_0 = 0x8
        RGB_FIRST_ZONE_ID_1 = 0x8
        RGB_LAST_ZONE_ID_1 = 0x8
        RED_INDEX_1 = 0x8
        GREEN_INDEX_1 = 0x8
        BLUE_INDEX_1 = 0x8
        RGB_FIRST_ZONE_ID_2 = 0x8
        RGB_LAST_ZONE_ID_2 = 0x8
        RED_INDEX_2 = 0x8
        GREEN_INDEX_2 = 0x8
        BLUE_INDEX_2 = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_FIRST_ZONE_ID_0, length=LEN.RGB_FIRST_ZONE_ID_0,
                 title="RgbFirstZoneId0", name="rgb_first_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_FIRST_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_LAST_ZONE_ID_0, length=LEN.RGB_LAST_ZONE_ID_0,
                 title="RgbLastZoneId0", name="rgb_last_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_LAST_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_0, length=LEN.RED_INDEX_0,
                 title="RedIndex0", name="red_index_0",
                 checks=(CheckHexList(LEN.RED_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_0, length=LEN.GREEN_INDEX_0,
                 title="GreenIndex0", name="green_index_0",
                 checks=(CheckHexList(LEN.GREEN_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_0, length=LEN.BLUE_INDEX_0,
                 title="BlueIndex0", name="blue_index_0",
                 checks=(CheckHexList(LEN.BLUE_INDEX_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_FIRST_ZONE_ID_1, length=LEN.RGB_FIRST_ZONE_ID_1,
                 title="RgbFirstZoneId1", name="rgb_first_zone_id_1",
                 checks=(CheckHexList(LEN.RGB_FIRST_ZONE_ID_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_LAST_ZONE_ID_1, length=LEN.RGB_LAST_ZONE_ID_1,
                 title="RgbLastZoneId1", name="rgb_last_zone_id_1",
                 checks=(CheckHexList(LEN.RGB_LAST_ZONE_ID_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_1, length=LEN.RED_INDEX_1,
                 title="RedIndex1", name="red_index_1",
                 checks=(CheckHexList(LEN.RED_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_1, length=LEN.GREEN_INDEX_1,
                 title="GreenIndex1", name="green_index_1",
                 checks=(CheckHexList(LEN.GREEN_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_1, length=LEN.BLUE_INDEX_1,
                 title="BlueIndex1", name="blue_index_1",
                 checks=(CheckHexList(LEN.BLUE_INDEX_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_FIRST_ZONE_ID_2, length=LEN.RGB_FIRST_ZONE_ID_2,
                 title="RgbFirstZoneId2", name="rgb_first_zone_id_2",
                 checks=(CheckHexList(LEN.RGB_FIRST_ZONE_ID_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_LAST_ZONE_ID_2, length=LEN.RGB_LAST_ZONE_ID_2,
                 title="RgbLastZoneId2", name="rgb_last_zone_id_2",
                 checks=(CheckHexList(LEN.RGB_LAST_ZONE_ID_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RED_INDEX_2, length=LEN.RED_INDEX_2,
                 title="RedIndex2", name="red_index_2",
                 checks=(CheckHexList(LEN.RED_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.GREEN_INDEX_2, length=LEN.GREEN_INDEX_2,
                 title="GreenIndex2", name="green_index_2",
                 checks=(CheckHexList(LEN.GREEN_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BLUE_INDEX_2, length=LEN.BLUE_INDEX_2,
                 title="BlueIndex2", name="blue_index_2",
                 checks=(CheckHexList(LEN.BLUE_INDEX_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rgb_first_zone_id_0, rgb_last_zone_id_0, red_index_0, green_index_0,
                 blue_index_0, rgb_first_zone_id_1=0, rgb_last_zone_id_1=0, red_index_1=0, green_index_1=0,
                 blue_index_1=0, rgb_first_zone_id_2=0, rgb_last_zone_id_2=0, red_index_2=0, green_index_2=0,
                 blue_index_2=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_first_zone_id_0: Starting Zone ID [0]
        :type rgb_first_zone_id_0: ``int | HexList``
        :param rgb_last_zone_id_0: Ending Zone ID [0]
        :type rgb_last_zone_id_0: ``int | HexList``
        :param red_index_0: RGB Zone ID [0] R Component
        :type red_index_0: ``int | HexList``
        :param green_index_0: RGB Zone ID [0] G Component
        :type green_index_0: ``int | HexList``
        :param blue_index_0: RGB Zone ID [0] B Component
        :type blue_index_0: ``int | HexList``
        :param rgb_first_zone_id_1: Starting Zone ID [1] - OPTIONAL
        :type rgb_first_zone_id_1: ``int | HexList``
        :param rgb_last_zone_id_1: Ending Zone ID [1] - OPTIONAL
        :type rgb_last_zone_id_1: ``int | HexList``
        :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
        :type red_index_1: ``int | HexList``
        :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
        :type green_index_1: ``int | HexList``
        :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
        :type blue_index_1: ``int | HexList``
        :param rgb_first_zone_id_2: Starting Zone ID [2] - OPTIONAL
        :type rgb_first_zone_id_2: ``int | HexList``
        :param rgb_last_zone_id_2: Ending Zone ID [2] - OPTIONAL
        :type rgb_last_zone_id_2: ``int | HexList``
        :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
        :type red_index_2: ``int | HexList``
        :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
        :type green_index_2: ``int | HexList``
        :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
        :type blue_index_2: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRangeRGBZonesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_first_zone_id_0 = rgb_first_zone_id_0
        self.rgb_last_zone_id_0 = rgb_last_zone_id_0
        self.red_index_0 = red_index_0
        self.green_index_0 = green_index_0
        self.blue_index_0 = blue_index_0
        self.rgb_first_zone_id_1 = rgb_first_zone_id_1
        self.rgb_last_zone_id_1 = rgb_last_zone_id_1
        self.red_index_1 = red_index_1
        self.green_index_1 = green_index_1
        self.blue_index_1 = blue_index_1
        self.rgb_first_zone_id_2 = rgb_first_zone_id_2
        self.rgb_last_zone_id_2 = rgb_last_zone_id_2
        self.red_index_2 = red_index_2
        self.green_index_2 = green_index_2
        self.blue_index_2 = blue_index_2
    # end def __init__
# end class SetRangeRGBZones


class SetRangeRGBZonesResponse(PerKeyLighting):
    """
    Define ``SetRangeRGBZonesResponse`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB First Zone ID 0           8
    RGB First Zone ID 1           8
    RGB First Zone ID 2           8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRangeRGBZones,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 5

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_FIRST_ZONE_ID_0 = PerKeyLighting.FID.SOFTWARE_ID - 1
        RGB_FIRST_ZONE_ID_1 = RGB_FIRST_ZONE_ID_0 - 1
        RGB_FIRST_ZONE_ID_2 = RGB_FIRST_ZONE_ID_1 - 1
        PADDING = RGB_FIRST_ZONE_ID_2 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_FIRST_ZONE_ID_0 = 0x8
        RGB_FIRST_ZONE_ID_1 = 0x8
        RGB_FIRST_ZONE_ID_2 = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_FIRST_ZONE_ID_0, length=LEN.RGB_FIRST_ZONE_ID_0,
                 title="RgbFirstZoneId0", name="rgb_first_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_FIRST_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_FIRST_ZONE_ID_1, length=LEN.RGB_FIRST_ZONE_ID_1,
                 title="RgbFirstZoneId1", name="rgb_first_zone_id_1",
                 checks=(CheckHexList(LEN.RGB_FIRST_ZONE_ID_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_FIRST_ZONE_ID_2, length=LEN.RGB_FIRST_ZONE_ID_2,
                 title="RgbFirstZoneId2", name="rgb_first_zone_id_2",
                 checks=(CheckHexList(LEN.RGB_FIRST_ZONE_ID_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rgb_first_zone_id_0, rgb_first_zone_id_1=0, rgb_first_zone_id_2=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_first_zone_id_0: Starting Zone ID [0]
        :type rgb_first_zone_id_0: ``int | HexList``
        :param rgb_first_zone_id_1: Starting Zone ID [1] - OPTIONAL
        :type rgb_first_zone_id_1: ``int | HexList``
        :param rgb_first_zone_id_2: Starting Zone ID [2] - OPTIONAL
        :type rgb_first_zone_id_2: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_first_zone_id_0 = rgb_first_zone_id_0
        self.rgb_first_zone_id_1 = rgb_first_zone_id_1
        self.rgb_first_zone_id_2 = rgb_first_zone_id_2
    # end def __init__
# end class SetRangeRGBZonesResponse


class SetRGBZonesSingleValue(PerKeyLighting):
    """
    Define ``SetRGBZonesSingleValue`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone Red                  8
    RGB Zone Green                8
    RGB Zone Blue                 8
    RGB Zone ID 0                 8
    RGB Zone ID 1                 8
    RGB Zone ID 2                 8
    RGB Zone ID 3                 8
    RGB Zone ID 4                 8
    RGB Zone ID 5                 8
    RGB Zone ID 6                 8
    RGB Zone ID 7                 8
    RGB Zone ID 8                 8
    RGB Zone ID 9                 8
    RGB Zone ID 10                8
    RGB Zone ID 11                8
    RGB Zone ID 12                8
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_RED = PerKeyLighting.FID.SOFTWARE_ID - 1
        RGB_ZONE_GREEN = RGB_ZONE_RED - 1
        RGB_ZONE_BLUE = RGB_ZONE_GREEN - 1
        RGB_ZONE_ID_0 = RGB_ZONE_BLUE - 1
        RGB_ZONE_ID_1 = RGB_ZONE_ID_0 - 1
        RGB_ZONE_ID_2 = RGB_ZONE_ID_1 - 1
        RGB_ZONE_ID_3 = RGB_ZONE_ID_2 - 1
        RGB_ZONE_ID_4 = RGB_ZONE_ID_3 - 1
        RGB_ZONE_ID_5 = RGB_ZONE_ID_4 - 1
        RGB_ZONE_ID_6 = RGB_ZONE_ID_5 - 1
        RGB_ZONE_ID_7 = RGB_ZONE_ID_6 - 1
        RGB_ZONE_ID_8 = RGB_ZONE_ID_7 - 1
        RGB_ZONE_ID_9 = RGB_ZONE_ID_8 - 1
        RGB_ZONE_ID_10 = RGB_ZONE_ID_9 - 1
        RGB_ZONE_ID_11 = RGB_ZONE_ID_10 - 1
        RGB_ZONE_ID_12 = RGB_ZONE_ID_11 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_RED = 0x8
        RGB_ZONE_GREEN = 0x8
        RGB_ZONE_BLUE = 0x8
        RGB_ZONE_ID_0 = 0x8
        RGB_ZONE_ID_1 = 0x8
        RGB_ZONE_ID_2 = 0x8
        RGB_ZONE_ID_3 = 0x8
        RGB_ZONE_ID_4 = 0x8
        RGB_ZONE_ID_5 = 0x8
        RGB_ZONE_ID_6 = 0x8
        RGB_ZONE_ID_7 = 0x8
        RGB_ZONE_ID_8 = 0x8
        RGB_ZONE_ID_9 = 0x8
        RGB_ZONE_ID_10 = 0x8
        RGB_ZONE_ID_11 = 0x8
        RGB_ZONE_ID_12 = 0x8
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_RED, length=LEN.RGB_ZONE_RED,
                 title="RgbZoneRed", name="rgb_zone_red",
                 checks=(CheckHexList(LEN.RGB_ZONE_RED // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_GREEN, length=LEN.RGB_ZONE_GREEN,
                 title="RgbZoneGreen", name="rgb_zone_green",
                 checks=(CheckHexList(LEN.RGB_ZONE_GREEN // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_BLUE, length=LEN.RGB_ZONE_BLUE,
                 title="RgbZoneBlue", name="rgb_zone_blue",
                 checks=(CheckHexList(LEN.RGB_ZONE_BLUE // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_1, length=LEN.RGB_ZONE_ID_1,
                 title="RgbZoneId1", name="rgb_zone_id_1",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_2, length=LEN.RGB_ZONE_ID_2,
                 title="RgbZoneId2", name="rgb_zone_id_2",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_3, length=LEN.RGB_ZONE_ID_3,
                 title="RgbZoneId3", name="rgb_zone_id_3",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_4, length=LEN.RGB_ZONE_ID_4,
                 title="RgbZoneId4", name="rgb_zone_id_4",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_5, length=LEN.RGB_ZONE_ID_5,
                 title="RgbZoneId5", name="rgb_zone_id_5",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_6, length=LEN.RGB_ZONE_ID_6,
                 title="RgbZoneId6", name="rgb_zone_id_6",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_7, length=LEN.RGB_ZONE_ID_7,
                 title="RgbZoneId7", name="rgb_zone_id_7",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_7 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_8, length=LEN.RGB_ZONE_ID_8,
                 title="RgbZoneId8", name="rgb_zone_id_8",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_8 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_9, length=LEN.RGB_ZONE_ID_9,
                 title="RgbZoneId9", name="rgb_zone_id_9",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_9 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_10, length=LEN.RGB_ZONE_ID_10,
                 title="RgbZoneId10", name="rgb_zone_id_10",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_10 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_11, length=LEN.RGB_ZONE_ID_11,
                 title="RgbZoneId11", name="rgb_zone_id_11",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_11 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_12, length=LEN.RGB_ZONE_ID_12,
                 title="RgbZoneId12", name="rgb_zone_id_12",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_12 // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, rgb_zone_red, rgb_zone_green, rgb_zone_blue, rgb_zone_id_0,
                 rgb_zone_id_1=0, rgb_zone_id_2=0, rgb_zone_id_3=0, rgb_zone_id_4=0, rgb_zone_id_5=0, rgb_zone_id_6=0,
                 rgb_zone_id_7=0, rgb_zone_id_8=0, rgb_zone_id_9=0, rgb_zone_id_10=0, rgb_zone_id_11=0,
                 rgb_zone_id_12=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_red: RGB Zone R Component
        :type rgb_zone_red: ``int | HexList``
        :param rgb_zone_green: RGB Zone G Component
        :type rgb_zone_green: ``int | HexList``
        :param rgb_zone_blue: RGB Zone B Component
        :type rgb_zone_blue: ``int | HexList``
        :param rgb_zone_id_0: RGB Zone ID [0]
        :type rgb_zone_id_0: ``int | HexList``
        :param rgb_zone_id_1: RGB Zone ID [1] - OPTIONAL
        :type rgb_zone_id_1: ``int | HexList``
        :param rgb_zone_id_2: RGB Zone ID [2] - OPTIONAL
        :type rgb_zone_id_2: ``int | HexList``
        :param rgb_zone_id_3: RGB Zone ID [3] - OPTIONAL
        :type rgb_zone_id_3: ``int | HexList``
        :param rgb_zone_id_4: RGB Zone ID [4] - OPTIONAL
        :type rgb_zone_id_4: ``int | HexList``
        :param rgb_zone_id_5: RGB Zone ID [5] - OPTIONAL
        :type rgb_zone_id_5: ``int | HexList``
        :param rgb_zone_id_6: RGB Zone ID [6] - OPTIONAL
        :type rgb_zone_id_6: ``int | HexList``
        :param rgb_zone_id_7: RGB Zone ID [7] - OPTIONAL
        :type rgb_zone_id_7: ``int | HexList``
        :param rgb_zone_id_8: RGB Zone ID [8] - OPTIONAL
        :type rgb_zone_id_8: ``int | HexList``
        :param rgb_zone_id_9: RGB Zone ID [9] - OPTIONAL
        :type rgb_zone_id_9: ``int | HexList``
        :param rgb_zone_id_10: RGB Zone ID [10] - OPTIONAL
        :type rgb_zone_id_10: ``int | HexList``
        :param rgb_zone_id_11: RGB Zone ID [11] - OPTIONAL
        :type rgb_zone_id_11: ``int | HexList``
        :param rgb_zone_id_12: RGB Zone ID [12] - OPTIONAL
        :type rgb_zone_id_12: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRGBZonesSingleValueResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_red = rgb_zone_red
        self.rgb_zone_green = rgb_zone_green
        self.rgb_zone_blue = rgb_zone_blue
        self.rgb_zone_id_0 = rgb_zone_id_0
        self.rgb_zone_id_1 = rgb_zone_id_1
        self.rgb_zone_id_2 = rgb_zone_id_2
        self.rgb_zone_id_3 = rgb_zone_id_3
        self.rgb_zone_id_4 = rgb_zone_id_4
        self.rgb_zone_id_5 = rgb_zone_id_5
        self.rgb_zone_id_6 = rgb_zone_id_6
        self.rgb_zone_id_7 = rgb_zone_id_7
        self.rgb_zone_id_8 = rgb_zone_id_8
        self.rgb_zone_id_9 = rgb_zone_id_9
        self.rgb_zone_id_10 = rgb_zone_id_10
        self.rgb_zone_id_11 = rgb_zone_id_11
        self.rgb_zone_id_12 = rgb_zone_id_12
    # end def __init__
# end class SetRGBZonesSingleValue


class SetRGBZonesSingleValueResponse(PerKeyLighting):
    """
    Define ``SetRGBZonesSingleValueResponse`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Zone Red                  8
    RGB Zone Green                8
    RGB Zone Blue                 8
    RGB Zone ID 0                 8
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRGBZonesSingleValue,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 6

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        RGB_ZONE_RED = PerKeyLighting.FID.SOFTWARE_ID - 1
        RGB_ZONE_GREEN = RGB_ZONE_RED - 1
        RGB_ZONE_BLUE = RGB_ZONE_GREEN - 1
        RGB_ZONE_ID_0 = RGB_ZONE_BLUE - 1
        PADDING = RGB_ZONE_ID_0 - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        RGB_ZONE_RED = 0x8
        RGB_ZONE_GREEN = 0x8
        RGB_ZONE_BLUE = 0x8
        RGB_ZONE_ID_0 = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.RGB_ZONE_RED, length=LEN.RGB_ZONE_RED,
                 title="RgbZoneRed", name="rgb_zone_red",
                 checks=(CheckHexList(LEN.RGB_ZONE_RED // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_GREEN, length=LEN.RGB_ZONE_GREEN,
                 title="RgbZoneGreen", name="rgb_zone_green",
                 checks=(CheckHexList(LEN.RGB_ZONE_GREEN // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_BLUE, length=LEN.RGB_ZONE_BLUE,
                 title="RgbZoneBlue", name="rgb_zone_blue",
                 checks=(CheckHexList(LEN.RGB_ZONE_BLUE // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_ZONE_ID_0, length=LEN.RGB_ZONE_ID_0,
                 title="RgbZoneId0", name="rgb_zone_id_0",
                 checks=(CheckHexList(LEN.RGB_ZONE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rgb_zone_red=0, rgb_zone_green=0, rgb_zone_blue=0, rgb_zone_id_0=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rgb_zone_red: RGB Zone R Component - OPTIONAL
        :type rgb_zone_red: ``int | HexList``
        :param rgb_zone_green: RGB Zone G Component - OPTIONAL
        :type rgb_zone_green: ``int | HexList``
        :param rgb_zone_blue: RGB Zone B Component - OPTIONAL
        :type rgb_zone_blue: ``int | HexList``
        :param rgb_zone_id_0: RGB Zone ID [0] - OPTIONAL
        :type rgb_zone_id_0: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_zone_red = rgb_zone_red
        self.rgb_zone_green = rgb_zone_green
        self.rgb_zone_blue = rgb_zone_blue
        self.rgb_zone_id_0 = rgb_zone_id_0
    # end def __init__
# end class SetRGBZonesSingleValueResponse


class FrameEnd(PerKeyLighting):
    """
    Define ``FrameEnd`` implementation class for version 0, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Persistence                   8
    Current Frame                 16
    N Frames Till Next Change     16
    Padding                       88
    ============================  ==========
    """

    class FID(PerKeyLighting.FID):
        # See ``PerKeyLighting.FID``
        PERSISTENCE = PerKeyLighting.FID.SOFTWARE_ID - 1
        CURRENT_FRAME = PERSISTENCE - 1
        N_FRAMES_TILL_NEXT_CHANGE = CURRENT_FRAME - 1
        PADDING = N_FRAMES_TILL_NEXT_CHANGE - 1
    # end class FID

    class LEN(PerKeyLighting.LEN):
        # See ``PerKeyLighting.LEN``
        PERSISTENCE = 0x8
        CURRENT_FRAME = 0x10
        N_FRAMES_TILL_NEXT_CHANGE = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = PerKeyLighting.FIELDS + (
        BitField(fid=FID.PERSISTENCE, length=LEN.PERSISTENCE,
                 title="Persistence", name="persistence",
                 checks=(CheckHexList(LEN.PERSISTENCE // 8),
                         CheckByte(),)),
        BitField(fid=FID.CURRENT_FRAME, length=LEN.CURRENT_FRAME,
                 title="CurrentFrame", name="current_frame",
                 checks=(CheckHexList(LEN.CURRENT_FRAME // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURRENT_FRAME) - 1),)),
        BitField(fid=FID.N_FRAMES_TILL_NEXT_CHANGE, length=LEN.N_FRAMES_TILL_NEXT_CHANGE,
                 title="NFramesTillNextChange", name="n_frames_till_next_change",
                 checks=(CheckHexList(LEN.N_FRAMES_TILL_NEXT_CHANGE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.N_FRAMES_TILL_NEXT_CHANGE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PerKeyLighting.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, persistence=0, current_frame=0, n_frames_till_next_change=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param persistence: Determines how the effect persists through a power cycle - OPTIONAL
        :type persistence: ``int | HexList``
        :param current_frame: Index of the frame that ends by this command - OPTIONAL
        :type current_frame: ``int | HexList``
        :param n_frames_till_next_change: Realtime information for playback: number of frames until next expected change
        - OPTIONAL
        :type n_frames_till_next_change: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=FrameEndResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.persistence = persistence
        self.current_frame = current_frame
        self.n_frames_till_next_change = n_frames_till_next_change
    # end def __init__
# end class FrameEnd


class FrameEndResponse(LongEmptyPacketDataFormat):
    """
    Define ``FrameEndResponse`` implementation class for version 0, 2
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (FrameEnd,)
    VERSION = (0, 2,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class FrameEndResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
