#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.brakeforce
:brief: HID++ 2.0 ``BrakeForce`` command interface definition
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/26
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
class BrakeForce(HidppMessage):
    """
    This feature is used to set the level of force required to reach the maximum axis value.

    When the value is set to 0xffff the amount of pressure on the brake needed to reach maximum axis output is equal
    to the maximum load in (KG) reported by the getInfo() function. When the value is set to 0x0000 the axis will
    report its maximum value all of the time.
    """

    FEATURE_ID = 0x8134
    MAX_FUNCTION_INDEX = 2

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
# end class BrakeForce


class BrakeForceModel(FeatureModel):
    """
    Define ``BrakeForce`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """

        # Function index
        GET_INFO = 0
        GET_MAX_LOAD_POINT = 1
        SET_MAX_LOAD_POINT = 2

        # Event index
        MAX_LOAD_POINT_CHANGED = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``BrakeForce`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_INFO: {
                    "request": GetInfo,
                    "response": GetInfoResponse
                },
                cls.INDEX.GET_MAX_LOAD_POINT: {
                    "request": GetMaxLoadPoint,
                    "response": GetMaxLoadPointResponse
                },
                cls.INDEX.SET_MAX_LOAD_POINT: {
                    "request": SetMaxLoadPoint,
                    "response": SetMaxLoadPointResponse
                }
            },
            "events": {
                cls.INDEX.MAX_LOAD_POINT_CHANGED: {"report": MaxLoadPointChangedEvent}
            }
        }

        return {
            "feature_base": BrakeForce,
            "versions": {
                BrakeForceV0.VERSION: {
                    "main_cls": BrakeForceV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class BrakeForceModel


class BrakeForceFactory(FeatureFactory):
    """
    Get ``BrakeForce`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``BrakeForce`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``BrakeForceInterface``
        """
        return BrakeForceModel.get_main_cls(version)()
    # end def create
# end class BrakeForceFactory


class BrakeForceInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``BrakeForce`` classes
    """

    def __init__(self):
        # Requests
        self.get_info_cls = None
        self.get_max_load_point_cls = None
        self.set_max_load_point_cls = None

        # Responses
        self.get_info_response_cls = None
        self.get_max_load_point_response_cls = None
        self.set_max_load_point_response_cls = None

        # Events
        self.max_load_point_changed_event_cls = None
    # end def __init__
# end class BrakeForceInterface


class BrakeForceV0(BrakeForceInterface):
    """
    Define ``BrakeForceV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getInfo() -> maximumKgLoad

    [1] getMaxLoadPoint() -> maximumLoadPoint

    [2] setMaxLoadPoint(maximumLoadPoint) -> None

    [Event 0] maxLoadPointChangedEvent -> maximumLoadPoint
    """

    VERSION = 0

    def __init__(self):
        # See ``BrakeForce.__init__``
        super().__init__()
        index = BrakeForceModel.INDEX

        # Requests
        self.get_info_cls = BrakeForceModel.get_request_cls(
            self.VERSION, index.GET_INFO)
        self.get_max_load_point_cls = BrakeForceModel.get_request_cls(
            self.VERSION, index.GET_MAX_LOAD_POINT)
        self.set_max_load_point_cls = BrakeForceModel.get_request_cls(
            self.VERSION, index.SET_MAX_LOAD_POINT)

        # Responses
        self.get_info_response_cls = BrakeForceModel.get_response_cls(
            self.VERSION, index.GET_INFO)
        self.get_max_load_point_response_cls = BrakeForceModel.get_response_cls(
            self.VERSION, index.GET_MAX_LOAD_POINT)
        self.set_max_load_point_response_cls = BrakeForceModel.get_response_cls(
            self.VERSION, index.SET_MAX_LOAD_POINT)

        # Events
        self.max_load_point_changed_event_cls = BrakeForceModel.get_report_cls(
            self.VERSION, index.MAX_LOAD_POINT_CHANGED)
    # end def __init__

    def get_max_function_index(self):
        # See ``BrakeForceInterface.get_max_function_index``
        return BrakeForceModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class BrakeForceV0


class ShortEmptyPacketDataFormat(BrakeForce):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetInfo
        - GetMaxLoadPoint

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(BrakeForce.FID):
        """
        Define field identifier(s)
        """

        PADDING = BrakeForce.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(BrakeForce.LEN):
        """
        Define field length(s)
        """

        PADDING = 0x18
    # end class LEN

    FIELDS = BrakeForce.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrakeForce.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(BrakeForce):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - SetMaxLoadPointResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(BrakeForce.FID):
        """
        Define field identifier(s)
        """

        PADDING = BrakeForce.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(BrakeForce.LEN):
        """
        Define field length(s)
        """

        PADDING = 0x80
    # end class LEN

    FIELDS = BrakeForce.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrakeForce.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class MixedContainer1(BrakeForce):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - GetMaxLoadPointResponse
        - MaxLoadPointChangedEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    MaximumLoadPoint              16
    Padding                       112
    ============================  ==========
    """

    class FID(BrakeForce.FID):
        """
        Define field identifier(s)
        """

        MAXIMUM_LOAD_POINT = BrakeForce.FID.SOFTWARE_ID - 1
        PADDING = MAXIMUM_LOAD_POINT - 1
    # end class FID

    class LEN(BrakeForce.LEN):
        """
        Define field length(s)
        """

        MAXIMUM_LOAD_POINT = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = BrakeForce.FIELDS + (
        BitField(fid=FID.MAXIMUM_LOAD_POINT, length=LEN.MAXIMUM_LOAD_POINT,
                 title="MaximumLoadPoint", name="maximum_load_point",
                 checks=(CheckHexList(LEN.MAXIMUM_LOAD_POINT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAXIMUM_LOAD_POINT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrakeForce.DEFAULT.PADDING),
    )
# end class MixedContainer1


class GetInfo(ShortEmptyPacketDataFormat):
    """
    Define ``GetInfo`` implementation class for version 0
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
                         functionIndex=GetInfoResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetInfo


class GetInfoResponse(BrakeForce):
    """
    Define ``GetInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    MaximumKgLoad                 8
    Padding                       120
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(BrakeForce.FID):
        """
        Define field identifier(s)
        """

        MAXIMUM_KG_LOAD = BrakeForce.FID.SOFTWARE_ID - 1
        PADDING = MAXIMUM_KG_LOAD - 1
    # end class FID

    class LEN(BrakeForce.LEN):
        """
        Define field length(s)
        """

        MAXIMUM_KG_LOAD = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = BrakeForce.FIELDS + (
        BitField(fid=FID.MAXIMUM_KG_LOAD, length=LEN.MAXIMUM_KG_LOAD,
                 title="MaximumKgLoad", name="maximum_kg_load",
                 checks=(CheckHexList(LEN.MAXIMUM_KG_LOAD // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrakeForce.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, maximum_kg_load, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param maximum_kg_load: maximum load in Kg
        :type maximum_kg_load: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.maximum_kg_load = maximum_kg_load
    # end def __init__
# end class GetInfoResponse


class GetMaxLoadPoint(ShortEmptyPacketDataFormat):
    """
    Define ``GetMaxLoadPoint`` implementation class for version 0
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
                         functionIndex=GetMaxLoadPointResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetMaxLoadPoint


class GetMaxLoadPointResponse(MixedContainer1):
    """
    Define ``GetMaxLoadPointResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetMaxLoadPoint,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, maximum_load_point, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param maximum_load_point: Current value of the maximum load point
        :type maximum_load_point: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.maximum_load_point = maximum_load_point
    # end def __init__
# end class GetMaxLoadPointResponse


class SetMaxLoadPoint(BrakeForce):
    """
    Define ``SetMaxLoadPoint`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    MaximumLoadPoint              16
    Padding                       8
    ============================  ==========
    """

    class FID(BrakeForce.FID):
        """
        Define field identifier(s)
        """

        MAXIMUM_LOAD_POINT = BrakeForce.FID.SOFTWARE_ID - 1
        PADDING = MAXIMUM_LOAD_POINT - 1
    # end class FID

    class LEN(BrakeForce.LEN):
        """
        Define field length(s)
        """

        MAXIMUM_LOAD_POINT = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = BrakeForce.FIELDS + (
        BitField(fid=FID.MAXIMUM_LOAD_POINT, length=LEN.MAXIMUM_LOAD_POINT,
                 title="MaximumLoadPoint", name="maximum_load_point",
                 checks=(CheckHexList(LEN.MAXIMUM_LOAD_POINT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAXIMUM_LOAD_POINT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrakeForce.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, maximum_load_point, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param maximum_load_point: Maximum load point value of the loadcell
        :type maximum_load_point: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetMaxLoadPointResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.maximum_load_point = maximum_load_point
    # end def __init__
# end class SetMaxLoadPoint


class SetMaxLoadPointResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetMaxLoadPointResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetMaxLoadPoint,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetMaxLoadPointResponse


class MaxLoadPointChangedEvent(MixedContainer1):
    """
    Define ``MaxLoadPointChangedEvent`` implementation class for version 0
    """

    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, maximum_load_point, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param maximum_load_point: Changed maximum load point value
        :type maximum_load_point: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.maximum_load_point = maximum_load_point
    # end def __init__
# end class MaxLoadPointChangedEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
