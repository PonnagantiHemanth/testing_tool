#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.mouse.thumbwheel
:brief: HID++ 2.0 ``Thumbwheel`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
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
class Thumbwheel(HidppMessage):
    """
    A thumbwheel generates natively HID reports that are usually horizontal scroll events.

    This feature gives the possibility to divert these reports (that is to send them in HID++ format instead) or to
    invert the rotation direction.

    Additional info is available in the diverted reports, depending on the capabilities of the device, as proxy
    (proximity) / touch detection, single tap gesture, etc
    """
    FEATURE_ID = 0x2150
    MAX_FUNCTION_INDEX = 2

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

    class DirectionMaskBitMap(BitFieldContainerMixin):
        """
        Define ``DirectionMaskBitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Default Direction             1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            DEFAULT_DIRECTION = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            DEFAULT_DIRECTION = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.DEFAULT_DIRECTION, length=LEN.DEFAULT_DIRECTION,
                     title="DefaultDirection", name="default_direction",
                     checks=(CheckInt(0, pow(2, LEN.DEFAULT_DIRECTION) - 1),)),
        )
    # end class DirectionMaskBitMap

    class CapabilityMaskBitMap(BitFieldContainerMixin):
        """
        Define ``CapabilityMaskBitMap`` information

        Format:
        =============================  ==========
        Name                           Bit count
        =============================  ==========
        Reserved                       4
        Single Tap Gesture Capability  1
        Proximity Capability           1
        Touch Capability               1
        Time Stamp Capability          1
        =============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            SINGLE_TAP_GESTURE_CAPABILITY = RESERVED - 1
            PROXIMITY_CAPABILITY = SINGLE_TAP_GESTURE_CAPABILITY - 1
            TOUCH_CAPABILITY = PROXIMITY_CAPABILITY - 1
            TIME_STAMP_CAPABILITY = TOUCH_CAPABILITY - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x4
            SINGLE_TAP_GESTURE_CAPABILITY = 0x1
            PROXIMITY_CAPABILITY = 0x1
            TOUCH_CAPABILITY = 0x1
            TIME_STAMP_CAPABILITY = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.SINGLE_TAP_GESTURE_CAPABILITY, length=LEN.SINGLE_TAP_GESTURE_CAPABILITY,
                     title="SingleTapGestureCapability", name="single_tap_gesture_capability",
                     checks=(CheckInt(0, pow(2, LEN.SINGLE_TAP_GESTURE_CAPABILITY) - 1),)),
            BitField(fid=FID.PROXIMITY_CAPABILITY, length=LEN.PROXIMITY_CAPABILITY,
                     title="ProximityCapability", name="proximity_capability",
                     checks=(CheckInt(0, pow(2, LEN.PROXIMITY_CAPABILITY) - 1),)),
            BitField(fid=FID.TOUCH_CAPABILITY, length=LEN.TOUCH_CAPABILITY,
                     title="TouchCapability", name="touch_capability",
                     checks=(CheckInt(0, pow(2, LEN.TOUCH_CAPABILITY) - 1),)),
            BitField(fid=FID.TIME_STAMP_CAPABILITY, length=LEN.TIME_STAMP_CAPABILITY,
                     title="TimeStampCapability", name="time_stamp_capability",
                     checks=(CheckInt(0, pow(2, LEN.TIME_STAMP_CAPABILITY) - 1),)),
        )
    # end class CapabilityMaskBitMap

    class StatusMaskBitMap(BitFieldContainerMixin):
        """
        Define ``StatusMaskBitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      5
        Proxy                         1
        Touch                         1
        Invert Direction              1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            PROXY = RESERVED - 1
            TOUCH = PROXY - 1
            INVERT_DIRECTION = TOUCH - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x5
            PROXY = 0x1
            TOUCH = 0x1
            INVERT_DIRECTION = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.PROXY, length=LEN.PROXY,
                     title="Proxy", name="proxy",
                     checks=(CheckInt(0, pow(2, LEN.PROXY) - 1),)),
            BitField(fid=FID.TOUCH, length=LEN.TOUCH,
                     title="Touch", name="touch",
                     checks=(CheckInt(0, pow(2, LEN.TOUCH) - 1),)),
            BitField(fid=FID.INVERT_DIRECTION, length=LEN.INVERT_DIRECTION,
                     title="InvertDirection", name="invert_direction",
                     checks=(CheckInt(0, pow(2, LEN.INVERT_DIRECTION) - 1),)),
        )
    # end class StatusMaskBitMap

    class InvertMaskBitMap(BitFieldContainerMixin):
        """
        Define ``InvertMaskBitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Invert Direction              1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            INVERT_DIRECTION = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            INVERT_DIRECTION = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.INVERT_DIRECTION, length=LEN.INVERT_DIRECTION,
                     title="InvertDirection", name="invert_direction",
                     checks=(CheckInt(0, pow(2, LEN.INVERT_DIRECTION) - 1),)),
        )
    # end class InvertMaskBitMap

    class ThumbwheelStatus(BitFieldContainerMixin):
        """
        Define ``ThumbwheelStatus`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved 0                    4
        Single Tap                    1
        Proxy                         1
        Touch                         1
        Reserved 1                    1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED_0 = 0xFF
            SINGLE_TAP = RESERVED_0 - 1
            PROXY = SINGLE_TAP - 1
            TOUCH = PROXY - 1
            RESERVED_1 = TOUCH - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED_0 = 0x4
            SINGLE_TAP = 0x1
            PROXY = 0x1
            TOUCH = 0x1
            RESERVED_1 = 0x1
        # end class LEN

        FIELDS = (
            BitField(fid=FID.RESERVED_0, length=LEN.RESERVED_0,
                     title="Reserved0", name="reserved_0",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED_0) - 1),)),
            BitField(fid=FID.SINGLE_TAP, length=LEN.SINGLE_TAP,
                     title="SingleTap", name="single_tap",
                     checks=(CheckInt(0, pow(2, LEN.SINGLE_TAP) - 1),)),
            BitField(fid=FID.PROXY, length=LEN.PROXY,
                     title="Proxy", name="proxy",
                     checks=(CheckInt(0, pow(2, LEN.PROXY) - 1),)),
            BitField(fid=FID.TOUCH, length=LEN.TOUCH,
                     title="Touch", name="touch",
                     checks=(CheckInt(0, pow(2, LEN.TOUCH) - 1),)),
            BitField(fid=FID.RESERVED_1, length=LEN.RESERVED_1,
                     title="Reserved1", name="reserved_1",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED_1) - 1),)),
        )
    # end class ThumbwheelStatus

    class ROTATION_STATUS:
        """
        Define values corresponding to rotation status
        """
        INACTIVE = 0
        START = 1
        ACTIVE = 2
        STOP = 3
    # end class ROTATION_STATUS

    class REPORTING_MODE:
        """
        Define ``ThumbWheel`` reporting mode values for HID and HID++ reporting
        """
        HID = 0
        HIDPP = 1
    # end class REPORTING_MODE
# end class Thumbwheel


class ThumbwheelModel(FeatureModel):
    """
    Define ``Thumbwheel`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_THUMBWHEEL_INFO = 0
        GET_THUMBWHEEL_STATUS = 1
        SET_THUMBWHEEL_REPORTING = 2

        # Event index
        THUMBWHEEL = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``Thumbwheel`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_THUMBWHEEL_INFO: {
                    "request": GetThumbwheelInfo,
                    "response": GetThumbwheelInfoResponse
                },
                cls.INDEX.GET_THUMBWHEEL_STATUS: {
                    "request": GetThumbwheelStatus,
                    "response": GetThumbwheelStatusResponse
                },
                cls.INDEX.SET_THUMBWHEEL_REPORTING: {
                    "request": SetThumbwheelReporting,
                    "response": SetThumbwheelReportingResponse
                }
            },
            "events": {
                cls.INDEX.THUMBWHEEL: {"report": ThumbwheelEvent}
            }
        }

        return {
            "feature_base": Thumbwheel,
            "versions": {
                ThumbwheelV0.VERSION: {
                    "main_cls": ThumbwheelV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class ThumbwheelModel


class ThumbwheelFactory(FeatureFactory):
    """
    Get ``Thumbwheel`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``Thumbwheel`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ThumbwheelInterface``
        """
        return ThumbwheelModel.get_main_cls(version)()
    # end def create
# end class ThumbwheelFactory


class ThumbwheelInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``Thumbwheel``
    """

    def __init__(self):
        # Requests
        self.get_thumbwheel_info_cls = None
        self.get_thumbwheel_status_cls = None
        self.set_thumbwheel_reporting_cls = None

        # Responses
        self.get_thumbwheel_info_response_cls = None
        self.get_thumbwheel_status_response_cls = None
        self.set_thumbwheel_reporting_response_cls = None

        # Events
        self.thumbwheel_event_cls = None
    # end def __init__
# end class ThumbwheelInterface


class ThumbwheelV0(ThumbwheelInterface):
    """
    Define ``ThumbwheelV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetThumbwheelInfo() -> NativeResolution, DivertedResolution, DirectionMaskBitMap, CapabilityMaskBitMap,
     TimeUnit

    [1] GetThumbwheelStatus() -> ReportingMode, StatusMaskBitMap

    [2] SetThumbwheelReporting(ReportingMode, InvertMaskBitMap) -> None

    [Event 0] ThumbwheelEvent -> Rotation, TimeStamp, RotationStatus, ThumbwheelStatus
    """
    VERSION = 0

    def __init__(self):
        # See ``Thumbwheel.__init__``
        super().__init__()
        index = ThumbwheelModel.INDEX

        # Requests
        self.get_thumbwheel_info_cls = ThumbwheelModel.get_request_cls(
            self.VERSION, index.GET_THUMBWHEEL_INFO)
        self.get_thumbwheel_status_cls = ThumbwheelModel.get_request_cls(
            self.VERSION, index.GET_THUMBWHEEL_STATUS)
        self.set_thumbwheel_reporting_cls = ThumbwheelModel.get_request_cls(
            self.VERSION, index.SET_THUMBWHEEL_REPORTING)

        # Responses
        self.get_thumbwheel_info_response_cls = ThumbwheelModel.get_response_cls(
            self.VERSION, index.GET_THUMBWHEEL_INFO)
        self.get_thumbwheel_status_response_cls = ThumbwheelModel.get_response_cls(
            self.VERSION, index.GET_THUMBWHEEL_STATUS)
        self.set_thumbwheel_reporting_response_cls = ThumbwheelModel.get_response_cls(
            self.VERSION, index.SET_THUMBWHEEL_REPORTING)

        # Events
        self.thumbwheel_event_cls = ThumbwheelModel.get_report_cls(
            self.VERSION, index.THUMBWHEEL)
    # end def __init__

    def get_max_function_index(self):
        # See ``ThumbwheelInterface.get_max_function_index``
        return ThumbwheelModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ThumbwheelV0


class ShortEmptyPacketDataFormat(Thumbwheel):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetThumbwheelInfo
        - GetThumbwheelStatus

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(Thumbwheel.FID):
        # See ``Thumbwheel.FID``
        PADDING = Thumbwheel.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(Thumbwheel.LEN):
        # See ``Thumbwheel.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = Thumbwheel.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Thumbwheel.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(Thumbwheel):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetThumbwheelReportingResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(Thumbwheel.FID):
        # See ``Thumbwheel.FID``
        PADDING = Thumbwheel.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(Thumbwheel.LEN):
        # See ``Thumbwheel.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = Thumbwheel.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Thumbwheel.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetThumbwheelInfo(ShortEmptyPacketDataFormat):
    """
    Define ``GetThumbwheelInfo`` implementation class for version 0
    """

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
                         function_index=GetThumbwheelInfoResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetThumbwheelInfo


class GetThumbwheelInfoResponse(Thumbwheel):
    """
    Define ``GetThumbwheelInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Native Resolution             16
    Diverted Resolution           16
    Direction Mask Bit Map        8
    Capability Mask Bit Map       8
    Time Unit                     16
    Padding                       64
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetThumbwheelInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(Thumbwheel.FID):
        # See ``Thumbwheel.FID``
        NATIVE_RESOLUTION = Thumbwheel.FID.SOFTWARE_ID - 1
        DIVERTED_RESOLUTION = NATIVE_RESOLUTION - 1
        DIRECTION_MASK_BIT_MAP = DIVERTED_RESOLUTION - 1
        CAPABILITY_MASK_BIT_MAP = DIRECTION_MASK_BIT_MAP - 1
        TIME_UNIT = CAPABILITY_MASK_BIT_MAP - 1
        PADDING = TIME_UNIT - 1
    # end class FID

    class LEN(Thumbwheel.LEN):
        # See ``Thumbwheel.LEN``
        NATIVE_RESOLUTION = 0x10
        DIVERTED_RESOLUTION = 0x10
        DIRECTION_MASK_BIT_MAP = 0x8
        CAPABILITY_MASK_BIT_MAP = 0x8
        TIME_UNIT = 0x10
        PADDING = 0x40
    # end class LEN

    FIELDS = Thumbwheel.FIELDS + (
        BitField(fid=FID.NATIVE_RESOLUTION, length=LEN.NATIVE_RESOLUTION,
                 title="NativeResolution", name="native_resolution",
                 checks=(CheckHexList(LEN.NATIVE_RESOLUTION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NATIVE_RESOLUTION) - 1),)),
        BitField(fid=FID.DIVERTED_RESOLUTION, length=LEN.DIVERTED_RESOLUTION,
                 title="DivertedResolution", name="diverted_resolution",
                 checks=(CheckHexList(LEN.DIVERTED_RESOLUTION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DIVERTED_RESOLUTION) - 1),)),
        BitField(fid=FID.DIRECTION_MASK_BIT_MAP, length=LEN.DIRECTION_MASK_BIT_MAP,
                 title="DirectionMaskBitMap", name="direction_mask_bit_map",
                 checks=(CheckHexList(LEN.DIRECTION_MASK_BIT_MAP // 8),
                         CheckByte(),)),
        BitField(fid=FID.CAPABILITY_MASK_BIT_MAP, length=LEN.CAPABILITY_MASK_BIT_MAP,
                 title="CapabilityMaskBitMap", name="capability_mask_bit_map",
                 checks=(CheckHexList(LEN.CAPABILITY_MASK_BIT_MAP // 8),
                         CheckByte(),)),
        BitField(fid=FID.TIME_UNIT, length=LEN.TIME_UNIT,
                 title="TimeUnit", name="time_unit",
                 checks=(CheckHexList(LEN.TIME_UNIT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIME_UNIT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Thumbwheel.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, native_resolution, diverted_resolution, default_direction,
                 single_tap_gesture_capability, proximity_capability, touch_capability, time_stamp_capability,
                 time_unit, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param native_resolution: The number of ratchets generated by revolution when in native (HID) mode
        :type native_resolution: ``int | HexList``
        :param diverted_resolution: The number of rotation increments generated by revolution when in diverted (HID++)
        mode
        :type diverted_resolution: ``int | HexList``
        :param default_direction: Original (not inverted) rotation direction
                                  0 = positive when moving to the left or back of the device
                                  1 = positive when moving to the right or front of the device
        :type default_direction: ``bool | HexList``
        :param single_tap_gesture_capability: Single tap gesture capability (1 = supported)
        :type single_tap_gesture_capability: ``bool | HexList``
        :param proximity_capability: Proxy capability (1 = supported)
        :type proximity_capability: ``bool | HexList``
        :param touch_capability: Touch capability (1 = supported)
        :type touch_capability: ``bool | HexList``
        :param time_stamp_capability: Time stamp capability (1 = supported)
        :type time_stamp_capability: ``bool | HexList``
        :param time_unit: If time stamp is supported, it gives the unit in us (micro second); otherwise, set to 0
        :type time_unit: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.native_resolution = native_resolution
        self.diverted_resolution = diverted_resolution
        self.direction_mask_bit_map = self.DirectionMaskBitMap(default_direction=default_direction)
        self.capability_mask_bit_map = self.CapabilityMaskBitMap(single_tap_gesture_capability=
                                                                 single_tap_gesture_capability,
                                                                 proximity_capability=proximity_capability,
                                                                 touch_capability=touch_capability,
                                                                 time_stamp_capability=time_stamp_capability)
        self.time_unit = time_unit
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
        :rtype: ``GetThumbwheelInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.direction_mask_bit_map = cls.DirectionMaskBitMap.fromHexList(
            inner_field_container_mixin.direction_mask_bit_map)
        inner_field_container_mixin.capability_mask_bit_map = cls.CapabilityMaskBitMap.fromHexList(
            inner_field_container_mixin.capability_mask_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetThumbwheelInfoResponse


class GetThumbwheelStatus(ShortEmptyPacketDataFormat):
    """
    Define ``GetThumbwheelStatus`` implementation class for version 0
    """

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
                         function_index=GetThumbwheelStatusResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetThumbwheelStatus


class GetThumbwheelStatusResponse(Thumbwheel):
    """
    Define ``GetThumbwheelStatusResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reporting Mode                8
    Status Mask Bit Map           8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetThumbwheelStatus,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(Thumbwheel.FID):
        # See ``Thumbwheel.FID``
        REPORTING_MODE = Thumbwheel.FID.SOFTWARE_ID - 1
        STATUS_MASK_BIT_MAP = REPORTING_MODE - 1
        PADDING = STATUS_MASK_BIT_MAP - 1
    # end class FID

    class LEN(Thumbwheel.LEN):
        # See ``Thumbwheel.LEN``
        REPORTING_MODE = 0x8
        STATUS_MASK_BIT_MAP = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = Thumbwheel.FIELDS + (
        BitField(fid=FID.REPORTING_MODE, length=LEN.REPORTING_MODE,
                 title="ReportingMode", name="reporting_mode",
                 checks=(CheckHexList(LEN.REPORTING_MODE // 8),
                         CheckByte(),)),
        BitField(fid=FID.STATUS_MASK_BIT_MAP, length=LEN.STATUS_MASK_BIT_MAP,
                 title="StatusMaskBitMap", name="status_mask_bit_map",
                 checks=(CheckHexList(LEN.STATUS_MASK_BIT_MAP // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Thumbwheel.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, reporting_mode, proxy, touch, invert_direction, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param reporting_mode: Native (HID only) = 0
                               Diverted (HID++ only) = 1 In Diverted mode,[event0] is sent in HID++
        :type reporting_mode: ``int | HexList``
        :param proxy: 1 = user is close to the thumbwheel
        :type proxy: ``bool | HexList``
        :param touch: 1 = user is touching the thumbwheel
        :type touch: ``bool | HexList``
        :param invert_direction: 1 = the rotation direction is inverted (relatively to default_dir)
        :type invert_direction: ``bool | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.reporting_mode = reporting_mode
        self.status_mask_bit_map = self.StatusMaskBitMap(proxy=proxy,
                                                         touch=touch,
                                                         invert_direction=invert_direction)
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
        :rtype: ``GetThumbwheelStatusResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.status_mask_bit_map = cls.StatusMaskBitMap.fromHexList(
            inner_field_container_mixin.status_mask_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetThumbwheelStatusResponse


class SetThumbwheelReporting(Thumbwheel):
    """
    Define ``SetThumbwheelReporting`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reporting Mode                8
    Invert Mask Bit Map           8
    Padding                       8
    ============================  ==========
    """

    class FID(Thumbwheel.FID):
        # See ``Thumbwheel.FID``
        REPORTING_MODE = Thumbwheel.FID.SOFTWARE_ID - 1
        INVERT_MASK_BIT_MAP = REPORTING_MODE - 1
        PADDING = INVERT_MASK_BIT_MAP - 1
    # end class FID

    class LEN(Thumbwheel.LEN):
        # See ``Thumbwheel.LEN``
        REPORTING_MODE = 0x8
        INVERT_MASK_BIT_MAP = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = Thumbwheel.FIELDS + (
        BitField(fid=FID.REPORTING_MODE, length=LEN.REPORTING_MODE,
                 title="ReportingMode", name="reporting_mode",
                 checks=(CheckHexList(LEN.REPORTING_MODE // 8),
                         CheckByte(),)),
        BitField(fid=FID.INVERT_MASK_BIT_MAP, length=LEN.INVERT_MASK_BIT_MAP,
                 title="InvertMaskBitMap", name="invert_mask_bit_map",
                 checks=(CheckHexList(LEN.INVERT_MASK_BIT_MAP // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Thumbwheel.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, reporting_mode, invert_direction, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param reporting_mode: Native (HID) = 0, Diverted (HID++) = 1 In Diverted mode, [event0] is sent in HID++
        :type reporting_mode: ``int | HexList``
        :param invert_direction: 1 = invert the rotation direction (relatively to default_dir). This setting applies in
            both native and diverted modes
        :type invert_direction: ``bool | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetThumbwheelReportingResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.reporting_mode = reporting_mode
        self.invert_mask_bit_map = self.InvertMaskBitMap(invert_direction=invert_direction)
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
        :rtype: ``SetThumbwheelReporting``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.invert_mask_bit_map = cls.InvertMaskBitMap.fromHexList(
            inner_field_container_mixin.invert_mask_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetThumbwheelReporting


class SetThumbwheelReportingResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetThumbwheelReportingResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetThumbwheelReporting,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

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
# end class SetThumbwheelReportingResponse


class ThumbwheelEvent(Thumbwheel):
    """
    Define ``ThumbwheelEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Rotation                      16
    Time Stamp                    16
    Rotation Status               8
    Thumbwheel status             8
    Padding                       80
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(Thumbwheel.FID):
        # See ``Thumbwheel.FID``
        ROTATION = Thumbwheel.FID.SOFTWARE_ID - 1
        TIME_STAMP = ROTATION - 1
        ROTATION_STATUS = TIME_STAMP - 1
        THUMBWHEEL_STATUS = ROTATION_STATUS - 1
        PADDING = THUMBWHEEL_STATUS - 1
    # end class FID

    class LEN(Thumbwheel.LEN):
        # See ``Thumbwheel.LEN``
        ROTATION = 0x10
        TIME_STAMP = 0x10
        ROTATION_STATUS = 0x8
        THUMBWHEEL_STATUS = 0x8
        PADDING = 0x50
    # end class LEN

    FIELDS = Thumbwheel.FIELDS + (
        BitField(fid=FID.ROTATION, length=LEN.ROTATION,
                 title="Rotation", name="rotation",
                 checks=(CheckHexList(LEN.ROTATION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ROTATION) - 1),)),
        BitField(fid=FID.TIME_STAMP, length=LEN.TIME_STAMP,
                 title="TimeStamp", name="time_stamp",
                 checks=(CheckHexList(LEN.TIME_STAMP // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIME_STAMP) - 1),)),
        BitField(fid=FID.ROTATION_STATUS, length=LEN.ROTATION_STATUS,
                 title="RotationStatus", name="rotation_status",
                 checks=(CheckHexList(LEN.ROTATION_STATUS // 8),
                         CheckByte(),)),
        BitField(fid=FID.THUMBWHEEL_STATUS, length=LEN.THUMBWHEEL_STATUS,
                 title="ThumbwheelStatus", name="thumbwheel_status",
                 checks=(CheckHexList(LEN.THUMBWHEEL_STATUS // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Thumbwheel.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rotation, time_stamp, rotation_status, single_tap, proxy, touch,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param rotation: Relative wheel rotation (signed integer).
        :type rotation: ``int | HexList``
        :param time_stamp: Time elapsed between the current and the previous rotation report, expressed in
            time_unit. time_stamp is zero if not supported or for the very first rotation report
        :type time_stamp: ``int | HexList``
        :param rotation_status: It applies to wheel rotation. The following values are possible,
            Inactive (no rotation) = 0, Start(first rotation report) = 1, Active(next rotation reports) = 2,
            Stop (release, no touch) = 3
        :type rotation_status: ``int | HexList``
        :param single_tap: 1 = single tap gesture detected; 0 = no tap gesture or not supported
        :type single_tap: ``bool | HexList``
        :param proxy: 1 = user is close to the thumbwheel; 0 = user is not in proximity or proxy not supported
        :type proxy: ``bool | HexList``
        :param touch: 1 = user is touching the thumbwheel; 0 = no touch or touch not supported
        :type touch: ``bool | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rotation = rotation
        self.time_stamp = time_stamp
        self.rotation_status = rotation_status
        self.thumbwheel_status = self.ThumbwheelStatus(single_tap=single_tap,
                                                       proxy=proxy,
                                                       touch=touch)
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
        :rtype: ``ThumbwheelEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.thumbwheel_status = cls.ThumbwheelStatus.fromHexList(
            inner_field_container_mixin.thumbwheel_status)
        return inner_field_container_mixin
    # end def fromHexList
# end class ThumbwheelEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
