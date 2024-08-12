#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.axisresponsecurve
:brief: HID++ 2.0 ``AxisResponseCurve`` command interface definition
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/03/10
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
class AxisResponseCurve(HidppMessage):
    """
    Define Axis Response Curve feature which is used to set the level of force required to reach the maximum axis value.
    """

    FEATURE_ID = 0x80A4
    MAX_FUNCTION_INDEX_V0 = 7
    MAX_FUNCTION_INDEX_V1 = 9

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
# end class AxisResponseCurve


class AxisResponseCurveModel(FeatureModel):
    """
    Define ``AxisResponseCurve`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_INFO = 0
        GET_AXIS_INFO = 1
        GET_AXIS_POINTS = 2
        START_UPDATE = 3
        SET_AXIS_POINTS = 4
        STOP_UPDATE = 5
        RESET_AXIS = 6
        GET_CALCULATED_VALUE = 7
        SAVE_TO_NVS = 8
        RELOAD_FROM_NVS = 9

        # Event index
        SAVE_COMPLETE = 0
        RELOAD_COMPLETE = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``AxisResponseCurve`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_INFO: {
                    "request": GetInfo,
                    "response": GetInfoResponseV0
                },
                cls.INDEX.GET_AXIS_INFO: {
                    "request": GetAxisInfo,
                    "response": GetAxisInfoResponse
                },
                cls.INDEX.GET_AXIS_POINTS: {
                    "request": GetAxisPoints,
                    "response": GetAxisPointsResponse
                },
                cls.INDEX.START_UPDATE: {
                    "request": StartUpdate,
                    "response": StartUpdateResponse
                },
                cls.INDEX.SET_AXIS_POINTS: {
                    "request": SetAxisPoints,
                    "response": SetAxisPointsResponse
                },
                cls.INDEX.STOP_UPDATE: {
                    "request": StopUpdate,
                    "response": StopUpdateResponse
                },
                cls.INDEX.RESET_AXIS: {
                    "request": ResetAxis,
                    "response": ResetAxisResponse
                },
                cls.INDEX.GET_CALCULATED_VALUE: {
                    "request": GetCalculatedValue,
                    "response": GetCalculatedValueResponse
                }
            },
            "events": {}
        }
        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_INFO: {
                    "request": GetInfo,
                    "response": GetInfoResponseV1
                },
                cls.INDEX.GET_AXIS_INFO: {
                    "request": GetAxisInfo,
                    "response": GetAxisInfoResponse
                },
                cls.INDEX.GET_AXIS_POINTS: {
                    "request": GetAxisPoints,
                    "response": GetAxisPointsResponse
                },
                cls.INDEX.START_UPDATE: {
                    "request": StartUpdate,
                    "response": StartUpdateResponse
                },
                cls.INDEX.SET_AXIS_POINTS: {
                    "request": SetAxisPoints,
                    "response": SetAxisPointsResponse
                },
                cls.INDEX.STOP_UPDATE: {
                    "request": StopUpdate,
                    "response": StopUpdateResponse
                },
                cls.INDEX.RESET_AXIS: {
                    "request": ResetAxis,
                    "response": ResetAxisResponse
                },
                cls.INDEX.GET_CALCULATED_VALUE: {
                    "request": GetCalculatedValue,
                    "response": GetCalculatedValueResponse
                },
                cls.INDEX.SAVE_TO_NVS: {
                    "request": SaveToNVS,
                    "response": SaveToNVSResponse
                },
                cls.INDEX.RELOAD_FROM_NVS: {
                    "request": ReloadFromNVS,
                    "response": ReloadFromNVSResponse
                }
            },
            "events": {
                cls.INDEX.SAVE_COMPLETE: {"report": SaveCompleteEvent},
                cls.INDEX.RELOAD_COMPLETE: {"report": ReloadCompleteEvent}
            }
        }

        return {
            "feature_base": AxisResponseCurve,
            "versions": {
                AxisResponseCurveV0.VERSION: {
                    "main_cls": AxisResponseCurveV0,
                    "api": function_map_v0
                },
                AxisResponseCurveV1.VERSION: {
                    "main_cls": AxisResponseCurveV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class AxisResponseCurveModel


class AxisResponseCurveFactory(FeatureFactory):
    """
    Get ``AxisResponseCurve`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``AxisResponseCurve`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``AxisResponseCurveInterface``
        """
        return AxisResponseCurveModel.get_main_cls(version)()
    # end def create
# end class AxisResponseCurveFactory


class AxisResponseCurveInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``AxisResponseCurve``
    """

    def __init__(self):
        # Requests
        self.get_info_cls = None
        self.get_axis_info_cls = None
        self.get_axis_points_cls = None
        self.start_update_cls = None
        self.set_axis_points_cls = None
        self.stop_update_cls = None
        self.reset_axis_cls = None
        self.get_calculated_value_cls = None
        self.save_to_nvs_cls = None
        self.reload_from_nvs_cls = None

        # Responses
        self.get_info_response_cls = None
        self.get_axis_info_response_cls = None
        self.get_axis_points_response_cls = None
        self.start_update_response_cls = None
        self.set_axis_points_response_cls = None
        self.stop_update_response_cls = None
        self.reset_axis_response_cls = None
        self.get_calculated_value_response_cls = None
        self.save_to_nvs_response_cls = None
        self.reload_from_nvs_response_cls = None

        # Events
        self.save_complete_event_cls = None
        self.reload_complete_event_cls = None
    # end def __init__
# end class AxisResponseCurveInterface


class AxisResponseCurveV0(AxisResponseCurveInterface):
    """
    Define ``AxisResponseCurveV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getInfo() -> axisCount, maxGetPointCount, maxSetPointCount

    [1] getAxisInfo(axisIndex) -> axisIndex, hidUsagePage, hidUsage, axisResolution, activePointCount, maxPointCount,
    properties

    [2] getAxisPoints(axisIndex, pointIndex, pointCount) -> axisIndex, pointIndex, pointCount, axisPoints

    [3] startUpdate(axisIndex) -> None

    [4] setAxisPoints(pointCount, axisPoints) -> None

    [5] stopUpdate() -> axisIndex, status, activePointCount

    [6] resetAxis(axisIndex) -> None

    [7] getCalculatedValue(axisIndex, inputValue) -> axisIndex, inputValue, calculatedValue
    """

    VERSION = 0

    def __init__(self):
        # See ``AxisResponseCurve.__init__``
        super().__init__()
        index = AxisResponseCurveModel.INDEX

        # Requests
        self.get_info_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.GET_INFO)
        self.get_axis_info_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.GET_AXIS_INFO)
        self.get_axis_points_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.GET_AXIS_POINTS)
        self.start_update_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.START_UPDATE)
        self.set_axis_points_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.SET_AXIS_POINTS)
        self.stop_update_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.STOP_UPDATE)
        self.reset_axis_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.RESET_AXIS)
        self.get_calculated_value_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.GET_CALCULATED_VALUE)

        # Responses
        self.get_info_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.GET_INFO)
        self.get_axis_info_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.GET_AXIS_INFO)
        self.get_axis_points_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.GET_AXIS_POINTS)
        self.start_update_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.START_UPDATE)
        self.set_axis_points_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.SET_AXIS_POINTS)
        self.stop_update_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.STOP_UPDATE)
        self.reset_axis_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.RESET_AXIS)
        self.get_calculated_value_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.GET_CALCULATED_VALUE)
    # end def __init__

    def get_max_function_index(self):
        # See ``AxisResponseCurveInterface.get_max_function_index``
        return AxisResponseCurveModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class AxisResponseCurveV0


class AxisResponseCurveV1(AxisResponseCurveV0):
    """
    Define ``AxisResponseCurveV1`` feature

    This feature provides model and unit specific information for version 1

    [0] getInfo() -> axisCount, maxGetPointCount, maxSetPointCount, capabilities

    [1] getAxisInfo(axisIndex) -> axisIndex, hidUsagePage, hidUsage, axisResolution, activePointCount,
    maxPointCount, properties

    [2] getAxisPoints(axisIndex, pointIndex, pointCount) -> axisIndex, pointIndex, pointCount, axisPoints

    [3] startUpdate(axisIndex) -> None

    [4] setAxisPoints(pointCount, axisPoints) -> None

    [5] stopUpdate() -> axisIndex, status, activePointCount

    [6] resetAxis(axisIndex) -> None

    [7] getCalculatedValue(axisIndex, inputValue) -> axisIndex, inputValue, calculatedValue

    [8] saveToNVS(axisIndex) -> None

    [9] reloadFromNVS(axisIndex) -> None

    [Event 0] SaveCompleteEvent -> axisIndex, status

    [Event 1] ReloadCompleteEvent -> axisIndex, status
    """
    VERSION = 1

    def __init__(self):
        # See ``AxisResponseCurve.__init__``
        super().__init__()
        index = AxisResponseCurveModel.INDEX

        # Requests
        self.save_to_nvs_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.SAVE_TO_NVS)
        self.reload_from_nvs_cls = AxisResponseCurveModel.get_request_cls(
            self.VERSION, index.RELOAD_FROM_NVS)

        # Responses
        self.save_to_nvs_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.SAVE_TO_NVS)
        self.reload_from_nvs_response_cls = AxisResponseCurveModel.get_response_cls(
            self.VERSION, index.RELOAD_FROM_NVS)

        # Events
        self.save_complete_event_cls = AxisResponseCurveModel.get_report_cls(
            self.VERSION, index.SAVE_COMPLETE)
        self.reload_complete_event_cls = AxisResponseCurveModel.get_report_cls(
            self.VERSION, index.RELOAD_COMPLETE)
    # end def __init__

    def get_max_function_index(self):
        # See ``AxisResponseCurveInterface.get_max_function_index``
        return AxisResponseCurveModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class AxisResponseCurveV1


class ShortEmptyPacketDataFormat(AxisResponseCurve):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetInfo
        - StopUpdate

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        PADDING = AxisResponseCurve.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(AxisResponseCurve):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - StartUpdateResponse
        - SetAxisPointsResponse
        - ResetAxisResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        PADDING = AxisResponseCurve.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class AxisIndexPacket(AxisResponseCurve):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - GetAxisInfo
        - StartUpdate
        - ResetAxis

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisIndex                     8
    Padding                       16
    ============================  ==========
    """

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        PADDING = AXIS_INDEX - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_INDEX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )
# end class AxisIndexPacket


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
                         functionIndex=GetInfoResponseV0.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetInfo


class GetInfoResponseV0(AxisResponseCurve):
    """
    Define ``GetInfoResponseV0`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisCount                     8
    MaxGetPointCount              8
    MaxSetPointCount              8
    Padding                       104
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_COUNT = AxisResponseCurve.FID.SOFTWARE_ID - 1
        MAX_GET_POINT_COUNT = AXIS_COUNT - 1
        MAX_SET_POINT_COUNT = MAX_GET_POINT_COUNT - 1
        PADDING = MAX_SET_POINT_COUNT - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_COUNT = 0x8
        MAX_GET_POINT_COUNT = 0x8
        MAX_SET_POINT_COUNT = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_COUNT, length=LEN.AXIS_COUNT,
                 title="AxisCount", name="axis_count",
                 checks=(CheckHexList(LEN.AXIS_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.MAX_GET_POINT_COUNT, length=LEN.MAX_GET_POINT_COUNT,
                 title="MaxGetPointCount", name="max_get_point_count",
                 checks=(CheckHexList(LEN.MAX_GET_POINT_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.MAX_SET_POINT_COUNT, length=LEN.MAX_SET_POINT_COUNT,
                 title="MaxSetPointCount", name="max_set_point_count",
                 checks=(CheckHexList(LEN.MAX_SET_POINT_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, axis_count, max_get_point_count, max_set_point_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_count: Number of axes
        :type axis_count: ``int`` or ``HexList``
        :param max_get_point_count: The maximum number of points that the firmware supports for getting axis points
        :type max_get_point_count: ``int`` or ``HexList``
        :param max_set_point_count: The maximum number of points that the firmware supports for setting axis points
        :type max_set_point_count: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_count = axis_count
        self.max_get_point_count = max_get_point_count
        self.max_set_point_count = max_set_point_count
    # end def __init__
# end class GetInfoResponseV0


class GetInfoResponseV1(GetInfoResponseV0):
    """
    Define ``GetInfoResponseV1`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisCount                     8
    MaxGetPointCount              8
    MaxSetPointCount              8
    Reserved                      7
    Capabilities                  1
    Padding                       96
    ============================  ==========
    """
    VERSION = (1,)

    class FID(GetInfoResponseV0.FID):
        """
        Define field identifier(s)
        """
        RESERVED = GetInfoResponseV0.FID.MAX_SET_POINT_COUNT - 1
        CAPABILITIES = RESERVED - 1
        PADDING = CAPABILITIES - 1
    # end class FID

    class LEN(GetInfoResponseV0.LEN):
        """
        Define field length(s)
        """
        RESERVED = 0x7
        CAPABILITIES = 0x1
        PADDING = 0x60
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_COUNT, length=LEN.AXIS_COUNT,
                 title="AxisCount", name="axis_count",
                 checks=(CheckHexList(LEN.AXIS_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.MAX_GET_POINT_COUNT, length=LEN.MAX_GET_POINT_COUNT,
                 title="MaxGetPointCount", name="max_get_point_count",
                 checks=(CheckHexList(LEN.MAX_GET_POINT_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.MAX_SET_POINT_COUNT, length=LEN.MAX_SET_POINT_COUNT,
                 title="MaxSetPointCount", name="max_set_point_count",
                 checks=(CheckHexList(LEN.MAX_SET_POINT_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, axis_count, max_get_point_count, max_set_point_count, capabilities,
                 **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param axis_count: Number of axes
        :type axis_count: ``int | HexList``
        :param max_get_point_count: The maximum number of points that the firmware supports for getting axis points
        :type max_get_point_count: ``int | HexList``
        :param max_set_point_count: The maximum number of points that the firmware supports for setting axis points
        :type max_set_point_count: ``int | HexList``
        :param capabilities: Supported capabilities. bit 0 => nvCapability  (0=> Not supported, 1=> supported). bit 1 ..
                             7=> Reserved.
        :type capabilities: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         axis_count=axis_count,
                         max_get_point_count=max_get_point_count,
                         max_set_point_count=max_set_point_count,
                         **kwargs)
        self.axis_count = axis_count
        self.max_get_point_count = max_get_point_count
        self.max_set_point_count = max_set_point_count
        self.capabilities = capabilities
    # end def __init__
# end class GetInfoResponseV1


class GetAxisInfo(AxisIndexPacket):
    """
    Define ``GetAxisInfo`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, axis_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetAxisInfoResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.axis_index = axis_index
    # end def __init__
# end class GetAxisInfo


class GetAxisInfoResponse(AxisResponseCurve):
    """
    Define ``GetAxisInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisIndex                     8
    HidUsagePage                  16
    HidUsage                      16
    AxisResolution                8
    ActivePointCount              16
    MaxPointCount                 16
    Properties                    8
    Padding                       40
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAxisInfo,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        HID_USAGE_PAGE = AXIS_INDEX - 1
        HID_USAGE = HID_USAGE_PAGE - 1
        AXIS_RESOLUTION = HID_USAGE - 1
        ACTIVE_POINT_COUNT = AXIS_RESOLUTION - 1
        MAX_POINT_COUNT = ACTIVE_POINT_COUNT - 1
        PROPERTIES = MAX_POINT_COUNT - 1
        PADDING = PROPERTIES - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_INDEX = 0x8
        HID_USAGE_PAGE = 0x10
        HID_USAGE = 0x10
        AXIS_RESOLUTION = 0x8
        ACTIVE_POINT_COUNT = 0x10
        MAX_POINT_COUNT = 0x10
        PROPERTIES = 0x8
        PADDING = 0x28
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.HID_USAGE_PAGE, length=LEN.HID_USAGE_PAGE,
                 title="HidUsagePage", name="hid_usage_page",
                 checks=(CheckHexList(LEN.HID_USAGE_PAGE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HID_USAGE_PAGE) - 1),)),
        BitField(fid=FID.HID_USAGE, length=LEN.HID_USAGE,
                 title="HidUsage", name="hid_usage",
                 checks=(CheckHexList(LEN.HID_USAGE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HID_USAGE) - 1),)),
        BitField(fid=FID.AXIS_RESOLUTION, length=LEN.AXIS_RESOLUTION,
                 title="AxisResolution", name="axis_resolution",
                 checks=(CheckHexList(LEN.AXIS_RESOLUTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.ACTIVE_POINT_COUNT, length=LEN.ACTIVE_POINT_COUNT,
                 title="ActivePointCount", name="active_point_count",
                 checks=(CheckHexList(LEN.ACTIVE_POINT_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACTIVE_POINT_COUNT) - 1),)),
        BitField(fid=FID.MAX_POINT_COUNT, length=LEN.MAX_POINT_COUNT,
                 title="MaxPointCount", name="max_point_count",
                 checks=(CheckHexList(LEN.MAX_POINT_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_POINT_COUNT) - 1),)),
        BitField(fid=FID.PROPERTIES, length=LEN.PROPERTIES,
                 title="Properties", name="properties",
                 checks=(CheckHexList(LEN.PROPERTIES // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 axis_index, hid_usage_page, hid_usage, axis_resolution, active_point_count, max_point_count,
                 properties, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param hid_usage_page: The HID page of the axis. For non-HID axes this is an arbitrary 16-bit value
        :type hid_usage_page: ``int`` or ``HexList``
        :param hid_usage: The HID usage of the axis. For non-HID axes this is an arbitrary 32-bit value
        :type hid_usage: ``int`` or ``HexList``
        :param axis_resolution: The resolution of the axis in bits
        :type axis_resolution: ``int`` or ``HexList``
        :param active_point_count: The number of data point active on the axis
        :type active_point_count: ``int`` or ``HexList``
        :param max_point_count: The number of data points that the curve can support
        :type max_point_count: ``int`` or ``HexList``
        :param properties: Bit mask containing the axis properties, Can be Non-Centred(0) or Centred(1)
        :type properties: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_index = axis_index
        self.hid_usage_page = hid_usage_page
        self.hid_usage = hid_usage
        self.axis_resolution = axis_resolution
        self.active_point_count = active_point_count
        self.max_point_count = max_point_count
        self.properties = properties
    # end def __init__
# end class GetAxisInfoResponse


class GetAxisPoints(AxisResponseCurve):
    """
    Define ``GetAxisPoints`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisIndex                     8
    PointIndex                    16
    PointCount                    8
    Padding                       96
    ============================  ==========
    """

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        POINT_INDEX = AXIS_INDEX - 1
        POINT_COUNT = POINT_INDEX - 1
        PADDING = POINT_COUNT - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_INDEX = 0x8
        POINT_INDEX = 0x10
        POINT_COUNT = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.POINT_INDEX, length=LEN.POINT_INDEX,
                 title="PointIndex", name="point_index",
                 checks=(CheckHexList(LEN.POINT_INDEX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.POINT_INDEX) - 1),)),
        BitField(fid=FID.POINT_COUNT, length=LEN.POINT_COUNT,
                 title="PointCount", name="point_count",
                 checks=(CheckHexList(LEN.POINT_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, axis_index, point_index, point_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param point_index: The maximum number of points that the firmware supports for getting axis points
        :type point_index: ``int`` or ``HexList``
        :param point_count: The maximum number of points that the firmware supports for setting axis points
        :type point_count: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetAxisPointsResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_index = axis_index
        self.point_index = point_index
        self.point_count = point_count
    # end def __init__
# end class GetAxisPoints


class GetAxisPointsResponse(AxisResponseCurve):
    """
    Define ``GetAxisPointsResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisIndex                     8
    PointIndex                    16
    PointCount                    8
    AxisPoints                    96
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAxisPoints,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        POINT_INDEX = AXIS_INDEX - 1
        POINT_COUNT = POINT_INDEX - 1
        AXIS_POINTS = POINT_COUNT - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_INDEX = 0x8
        POINT_INDEX = 0x10
        POINT_COUNT = 0x8
        AXIS_POINTS = 0x60
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.POINT_INDEX, length=LEN.POINT_INDEX,
                 title="PointIndex", name="point_index",
                 checks=(CheckHexList(LEN.POINT_INDEX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.POINT_INDEX) - 1),)),
        BitField(fid=FID.POINT_COUNT, length=LEN.POINT_COUNT,
                 title="PointCount", name="point_count",
                 checks=(CheckHexList(LEN.POINT_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.AXIS_POINTS, length=LEN.AXIS_POINTS,
                 title="AxisPoints", name="axis_points",
                 checks=(CheckHexList(LEN.AXIS_POINTS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.AXIS_POINTS) - 1),)),
    )

    def __init__(self, device_index, feature_index, axis_index, point_index, point_count, axis_points, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param point_index: The points start at 0 and end at pointCount - 1
        :type point_index: ``int`` or ``HexList``
        :param point_count: The number of items returned
        :type point_count: ``int`` or ``HexList``
        :param axis_points: Data for PointIndices
        :type axis_points: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_index = axis_index
        self.point_index = point_index
        self.point_count = point_count
        self.axis_points = axis_points
    # end def __init__
# end class GetAxisPointsResponse


class StartUpdate(AxisIndexPacket):
    """
    Define ``StartUpdate`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, axis_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=StartUpdateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.axis_index = axis_index
    # end def __init__
# end class StartUpdate


class StartUpdateResponse(LongEmptyPacketDataFormat):
    """
    Define ``StartUpdateResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartUpdate,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 3

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
# end class StartUpdateResponse


class SetAxisPoints(AxisResponseCurve):
    """
    Define ``SetAxisPoints`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    PointCount                    8
    AxisPoints                    96
    Padding                       24
    ============================  ==========
    """

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        POINT_COUNT = AxisResponseCurve.FID.SOFTWARE_ID - 1
        AXIS_POINTS = POINT_COUNT - 1
        PADDING = AXIS_POINTS - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        POINT_COUNT = 0x8
        AXIS_POINTS = 0x60
        PADDING = 0x18
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.POINT_COUNT, length=LEN.POINT_COUNT,
                 title="PointCount", name="point_count",
                 checks=(CheckHexList(LEN.POINT_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.AXIS_POINTS, length=LEN.AXIS_POINTS,
                 title="AxisPoints", name="axis_points",
                 checks=(CheckHexList(LEN.AXIS_POINTS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.AXIS_POINTS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, point_count, axis_points, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param point_count: The number of items contained in the packet
        :type point_count: ``int`` or ``HexList``
        :param axis_points: An array of axisPoints to set
        :type axis_points: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetAxisPointsResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.point_count = point_count
        self.axis_points = axis_points
    # end def __init__
# end class SetAxisPoints


class SetAxisPointsResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetAxisPointsResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetAxisPoints,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 4

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
# end class SetAxisPointsResponse


class StopUpdate(ShortEmptyPacketDataFormat):
    """
    Define ``StopUpdate`` implementation class for version 0
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
                         functionIndex=StopUpdateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class StopUpdate


class StopUpdateResponse(AxisResponseCurve):
    """
    Define ``StopUpdateResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisIndex                     8
    Status                        8
    ActivePointCount              16
    Padding                       96
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StopUpdate,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 5

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        STATUS = AXIS_INDEX - 1
        ACTIVE_POINT_COUNT = STATUS - 1
        PADDING = ACTIVE_POINT_COUNT - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_INDEX = 0x8
        STATUS = 0x8
        ACTIVE_POINT_COUNT = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.STATUS, length=LEN.STATUS,
                 title="Status", name="status",
                 checks=(CheckHexList(LEN.STATUS // 8),
                         CheckByte(),)),
        BitField(fid=FID.ACTIVE_POINT_COUNT, length=LEN.ACTIVE_POINT_COUNT,
                 title="ActivePointCount", name="active_point_count",
                 checks=(CheckHexList(LEN.ACTIVE_POINT_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACTIVE_POINT_COUNT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, axis_index, status, active_point_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param status: Contains an error if there was an issue with the uploaded data

            0 - No error, the data was good and the axis response curve is active.

            1 - Not enough data was sent to create a curve i.e. 0 or 1 points received.

            2 - Data for axis minimum was not found. This must always be the first data point sent.

            3 - Data for axis maximum not found. This must always be the last data point sent.
        :type status: ``int`` or ``HexList``
        :param active_point_count: The number of data point active on the axis
        :type active_point_count: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_index = axis_index
        self.status = status
        self.active_point_count = active_point_count
    # end def __init__
# end class StopUpdateResponse


class ResetAxis(AxisIndexPacket):
    """
    Define ``ResetAxis`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, axis_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ResetAxisResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.axis_index = axis_index
    # end def __init__
# end class ResetAxis


class ResetAxisResponse(LongEmptyPacketDataFormat):
    """
    Define ``ResetAxisResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ResetAxis,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 6

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
# end class ResetAxisResponse


class GetCalculatedValue(AxisResponseCurve):
    """
    Define ``GetCalculatedValue`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisIndex                     8
    InputValue                    16
    ============================  ==========
    """

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        INPUT_VALUE = AXIS_INDEX - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_INDEX = 0x8
        INPUT_VALUE = 0x10
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.INPUT_VALUE, length=LEN.INPUT_VALUE,
                 title="InputValue", name="input_value",
                 checks=(CheckHexList(LEN.INPUT_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.INPUT_VALUE) - 1),)),
    )

    def __init__(self, device_index, feature_index, axis_index, input_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param input_value: A value representing a value from the ADC to be put through the curve algorithm
        :type input_value: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetCalculatedValueResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.axis_index = axis_index
        self.input_value = input_value
    # end def __init__
# end class GetCalculatedValue


class GetCalculatedValueResponse(AxisResponseCurve):
    """
    Define ``GetCalculatedValueResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    AxisIndex                     8
    InputValue                    16
    CalculatedValue               16
    Padding                       88
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCalculatedValue,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 7

    class FID(AxisResponseCurve.FID):
        """
        Define field identifier(s)
        """
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        INPUT_VALUE = AXIS_INDEX - 1
        CALCULATED_VALUE = INPUT_VALUE - 1
        PADDING = CALCULATED_VALUE - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        """
        Define field length(s)
        """
        AXIS_INDEX = 0x8
        INPUT_VALUE = 0x10
        CALCULATED_VALUE = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.INPUT_VALUE, length=LEN.INPUT_VALUE,
                 title="InputValue", name="input_value",
                 checks=(CheckHexList(LEN.INPUT_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.INPUT_VALUE) - 1),)),
        BitField(fid=FID.CALCULATED_VALUE, length=LEN.CALCULATED_VALUE,
                 title="CalculatedValue", name="calculated_value",
                 checks=(CheckHexList(LEN.CALCULATED_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CALCULATED_VALUE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, axis_index, input_value, calculated_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param axis_index: The index of the axis
        :type axis_index: ``int`` or ``HexList``
        :param input_value: A value representing a value from the ADC to be put through the curve algorithm
        :type input_value: ``int`` or ``HexList``
        :param calculated_value: A value representing what the current axis would report given the input value
        :type calculated_value: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_index = axis_index
        self.input_value = input_value
        self.calculated_value = calculated_value
    # end def __init__
# end class GetCalculatedValueResponse


class SaveToNVS(AxisIndexPacket):
    """
    Define ``SaveToNVS`` implementation class
    """

    def __init__(self, device_index, feature_index, axis_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param axis_index: The index of the axis that will be saved.
        :type axis_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SaveToNVSResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.axis_index = axis_index
    # end def __init__
# end class SaveToNVS


class SaveToNVSResponse(LongEmptyPacketDataFormat):
    """
    Define ``SaveToNVSResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SaveToNVS,)
    VERSION = (1,)
    FUNCTION_INDEX = 8

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
# end class SaveToNVSResponse


class ReloadFromNVS(AxisIndexPacket):
    """
    Define ``ReloadFromNVS`` implementation class
    """

    def __init__(self, device_index, feature_index, axis_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param axis_index: The index of the axis that will be reloaded.
        :type axis_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ReloadFromNVSResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.axis_index = axis_index
    # end def __init__
# end class ReloadFromNVS


class ReloadFromNVSResponse(LongEmptyPacketDataFormat):
    """
    Define ``ReloadFromNVSResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReloadFromNVS,)
    VERSION = (1,)
    FUNCTION_INDEX = 9

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ReloadFromNVSResponse


class SaveCompleteEvent(AxisResponseCurve):
    """
    Define ``SaveCompleteEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Axis index                    8
    Status                        8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 0

    class FID(AxisResponseCurve.FID):
        # See ``AxisResponseCurve.FID``
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        STATUS = AXIS_INDEX - 1
        PADDING = STATUS - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        # See ``AxisResponseCurve.LEN``
        AXIS_INDEX = 0x8
        STATUS = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8), CheckByte(),)),
        BitField(fid=FID.STATUS, length=LEN.STATUS,
                 title="Status", name="status",
                 checks=(CheckHexList(LEN.STATUS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, axis_index, status, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param axis_index: Axis index
        :type axis_index: ``int | HexList``
        :param status: Status
        :type status: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_index = axis_index
        self.status = status
    # end def __init__
# end class SaveCompleteEvent


class ReloadCompleteEvent(AxisResponseCurve):
    """
    Define ``ReloadCompleteEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Axis index                    8
    Status                        8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 1

    class FID(AxisResponseCurve.FID):
        # See ``AxisResponseCurve.FID``
        AXIS_INDEX = AxisResponseCurve.FID.SOFTWARE_ID - 1
        STATUS = AXIS_INDEX - 1
        PADDING = STATUS - 1
    # end class FID

    class LEN(AxisResponseCurve.LEN):
        # See ``AxisResponseCurve.LEN``
        AXIS_INDEX = 0x8
        STATUS = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = AxisResponseCurve.FIELDS + (
        BitField(fid=FID.AXIS_INDEX, length=LEN.AXIS_INDEX,
                 title="AxisIndex", name="axis_index",
                 checks=(CheckHexList(LEN.AXIS_INDEX // 8), CheckByte(),)),
        BitField(fid=FID.STATUS, length=LEN.STATUS,
                 title="Status", name="status",
                 checks=(CheckHexList(LEN.STATUS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AxisResponseCurve.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, axis_index, status, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param axis_index: Axis index
        :type axis_index: ``int | HexList``
        :param status: Status
        :type status: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.axis_index = axis_index
        self.status = status
    # end def __init__
# end class ReloadCompleteEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
