#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.touchpad.touchpadrawxy
:brief: HID++ 2.0 ``TouchpadRawXY`` command interface definition
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/05/11
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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TouchpadRawXY(HidppMessage):
    """
    Touchpad Raw XY implementation class
    """

    FEATURE_ID = 0x6100
    MAX_FUNCTION_INDEX = 4

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


# end class TouchpadRawXY


class TouchpadRawXYModel(FeatureModel):
    """
    Define ``TouchpadRawXY`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_TOUCHPAD_INFO = 0
        GET_RAW_REPORT_STATE = 1
        SET_RAW_REPORT_STATE = 2
        GET_GESTURES_HANDLING_OUTPUT = 3
        SET_GESTURES_HANDLING_OUTPUT = 4

        # Event index
        DUAL_XY_DATA = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``TouchpadRawXY`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_TOUCHPAD_INFO: {
                    "request": GetTouchpadInfo,
                    "response": GetTouchpadInfoResponse
                },
                cls.INDEX.GET_RAW_REPORT_STATE: {
                    "request": GetRawReportState,
                    "response": GetRawReportStateResponse
                },
                cls.INDEX.SET_RAW_REPORT_STATE: {
                    "request": SetRawReportState,
                    "response": SetRawReportStateResponse
                },
                cls.INDEX.GET_GESTURES_HANDLING_OUTPUT: {
                    "request": GetGesturesHandlingOutput,
                    "response": GetGesturesHandlingOutputResponse
                },
                cls.INDEX.SET_GESTURES_HANDLING_OUTPUT: {
                    "request": SetGesturesHandlingOutput,
                    "response": SetGesturesHandlingOutputResponse
                }
            },
            "events": {
                cls.INDEX.DUAL_XY_DATA: {"report": DualXYDataEvent}
            }
        }

        return {
            "feature_base": TouchpadRawXY,
            "versions": {
                TouchpadRawXYV1.VERSION: {
                    "main_cls": TouchpadRawXYV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class TouchpadRawXYModel


class TouchpadRawXYFactory(FeatureFactory):
    """
    Get ``TouchpadRawXY`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``TouchpadRawXY`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``TouchpadRawXYInterface``
        """
        return TouchpadRawXYModel.get_main_cls(version)()
    # end def create
# end class TouchpadRawXYFactory


class TouchpadRawXYInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``TouchpadRawXY``
    """

    def __init__(self):
        # Requests
        self.get_touchpad_info_cls = None
        self.get_raw_report_state_cls = None
        self.set_raw_report_state_cls = None
        self.get_gestures_handling_output_cls = None
        self.set_gestures_handling_output_cls = None

        # Responses
        self.get_touchpad_info_response_cls = None
        self.get_raw_report_state_response_cls = None
        self.set_raw_report_state_response_cls = None
        self.get_gestures_handling_output_response_cls = None
        self.set_gestures_handling_output_response_cls = None

        # Events
        self.dual_xy_data_event_cls = None
    # end def __init__
# end class TouchpadRawXYInterface


class TouchpadRawXYV1(TouchpadRawXYInterface):
    """
    Define ``TouchpadRawXYV1`` feature

    This feature provides model and unit specific information for version 1

    [0] getTouchpadInfo() -> XSize, YSize, ZDataRange, AreaDataRange, TimestampUnits, MaxFingerCount, Origin,
                             PenSupport, RawReportMappingVersion, DPI

    [1] getRawReportState() -> WidthHeightBytes, MajorMinor, NativeGesture, WidthHeight, Enhanced, ForceData, Raw

    [2] setRawReportState(WidthHeightBytes, MajorMinor, NativeGesture, WidthHeight, Enhanced, ForceData, Raw) -> None

    [3] getGesturesHandlingOutput() -> OneFingerClick, OneFingerTap, OneFingerMove, NotDefinedGestures,
                                       OneFingerClickHoldAndOtherFingersMoves, OneFingerClickHoldAndMove,
                                       OneFingerDoubleClick, OneFingerDoubleTap, TwoFingersTap,
                                       OneFingerDoubleTapNotReleaseThe2ndTap, OneFingerOnTheLeftCorner,
                                       OneFingerOnTheRightCorner, ThreeFingersTapAndDrag, TwoFingersSlideLeftRight,
                                       TwoFingersScrollUpDown, TwoFingersClick, ThreeFingersSwipe

    [4] setGesturesHandlingOutput(OneFingerClick, OneFingerTap, OneFingerMove, NotDefinedGestures,
                                  OneFingerClickHoldAndOtherFingersMoves, OneFingerClickHoldAndMove,
                                  OneFingerDoubleClick, OneFingerDoubleTap, TwoFingersTap,
                                  OneFingerDoubleTapNotReleaseThe2ndTap, OneFingerOnTheLeftCorner,
                                  OneFingerOnTheRightCorner, ThreeFingersTapAndDrag, TwoFingersSlideLeftRight,
                                  TwoFingersScrollUpDown, TwoFingersClick, ThreeFingersSwipe) -> None

    [Event 0] dualXYDataEvent -> Timestamp, ContactType1, X1 Coordinate, ContactStatus1, Y1 Coordinate, Z1 Coordinate
                                 Area1, FingerID1, Button, SP1, EndOfFrame, ContactType2, X2 Coordinate, ContactStatus2,
                                 Y2 Coordinate, Z2 Coordinate, Area2, FingerID2, NumberFingers
    """

    VERSION = 1

    def __init__(self):
        # See ``TouchpadRawXY.__init__``
        super().__init__()
        index = TouchpadRawXYModel.INDEX

        # Requests
        self.get_touchpad_info_cls = TouchpadRawXYModel.get_request_cls(
            self.VERSION, index.GET_TOUCHPAD_INFO)
        self.get_raw_report_state_cls = TouchpadRawXYModel.get_request_cls(
            self.VERSION, index.GET_RAW_REPORT_STATE)
        self.set_raw_report_state_cls = TouchpadRawXYModel.get_request_cls(
            self.VERSION, index.SET_RAW_REPORT_STATE)
        self.get_gestures_handling_output_cls = TouchpadRawXYModel.get_request_cls(
            self.VERSION, index.GET_GESTURES_HANDLING_OUTPUT)
        self.set_gestures_handling_output_cls = TouchpadRawXYModel.get_request_cls(
            self.VERSION, index.SET_GESTURES_HANDLING_OUTPUT)

        # Responses
        self.get_touchpad_info_response_cls = TouchpadRawXYModel.get_response_cls(
            self.VERSION, index.GET_TOUCHPAD_INFO)
        self.get_raw_report_state_response_cls = TouchpadRawXYModel.get_response_cls(
            self.VERSION, index.GET_RAW_REPORT_STATE)
        self.set_raw_report_state_response_cls = TouchpadRawXYModel.get_response_cls(
            self.VERSION, index.SET_RAW_REPORT_STATE)
        self.get_gestures_handling_output_response_cls = TouchpadRawXYModel.get_response_cls(
            self.VERSION, index.GET_GESTURES_HANDLING_OUTPUT)
        self.set_gestures_handling_output_response_cls = TouchpadRawXYModel.get_response_cls(
            self.VERSION, index.SET_GESTURES_HANDLING_OUTPUT)

        # Events
        self.dual_xy_data_event_cls = TouchpadRawXYModel.get_report_cls(
            self.VERSION, index.DUAL_XY_DATA)
    # end def __init__

    def get_max_function_index(self):
        # See ``TouchpadRawXYInterface.get_max_function_index``
        return TouchpadRawXYModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class TouchpadRawXYV1


class ShortEmptyPacketDataFormat(TouchpadRawXY):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetTouchpadInfo
        - GetRawReportState
        - GetGesturesHandlingOutput

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(TouchpadRawXY.FID):
        # See ``TouchpadRawXY.FID``
        PADDING = TouchpadRawXY.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TouchpadRawXY.LEN):
        # See ``TouchpadRawXY.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = TouchpadRawXY.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TouchpadRawXY.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(TouchpadRawXY):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - SetRawReportStateResponse
        - SetGesturesHandlingOutputResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(TouchpadRawXY.FID):
        # See ``TouchpadRawXY.FID``
        PADDING = TouchpadRawXY.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TouchpadRawXY.LEN):
        # See ``TouchpadRawXY.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = TouchpadRawXY.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TouchpadRawXY.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class ReportBitmap(TouchpadRawXY):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - GetRawReportStateResponse
        - SetRawReportState

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      1
    WidthHeightBytes              1
    MajorMinor                    1
    NativeGesture                 1
    WidthHeight                   1
    Enhanced                      1
    ForceData                     1
    Raw                           1
    Padding                       120
    ============================  ==========
    """

    class FID(TouchpadRawXY.FID):
        # See ``TouchpadRawXY.FID``
        RESERVED = TouchpadRawXY.FID.SOFTWARE_ID - 1
        WIDTH_HEIGHT_BYTES = RESERVED - 1
        MAJOR_MINOR = WIDTH_HEIGHT_BYTES - 1
        NATIVE_GESTURE = MAJOR_MINOR - 1
        WIDTH_HEIGHT = NATIVE_GESTURE - 1
        ENHANCED = WIDTH_HEIGHT - 1
        FORCE_DATA = ENHANCED - 1
        RAW = FORCE_DATA - 1
        PADDING = RAW - 1
    # end class FID

    class LEN(TouchpadRawXY.LEN):
        # See ``TouchpadRawXY.LEN``
        RESERVED = 0x1
        WIDTH_HEIGHT_BYTES = 0x1
        MAJOR_MINOR = 0x1
        NATIVE_GESTURE = 0x1
        WIDTH_HEIGHT = 0x1
        ENHANCED = 0x1
        FORCE_DATA = 0x1
        RAW = 0x1
        PADDING = 0x78
    # end class LEN

    class POS(object):
        """
        Report Bitmap field position
        """
        RESERVED = 7
        WIDTH_HEIGHT_BYTES = 6
        MAJOR_MINOR = 5
        NATIVE_GESTURE = 4
        WIDTH_HEIGHT = 3
        ENHANCED = 2
        FORCE_DATA = 1
        RAW = 0
    # end class POS

    class STATE:
        """
        ReportBitmap state
        """
        ENABLED = 1
        DISABLED = 0
    #end class STATE

    FIELDS = TouchpadRawXY.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=TouchpadRawXY.DEFAULT.RESERVED),
        BitField(fid=FID.WIDTH_HEIGHT_BYTES, length=LEN.WIDTH_HEIGHT_BYTES,
                 title="WidthHeightBytes", name="width_height_bytes",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.WIDTH_HEIGHT_BYTES) - 1),)),
        BitField(fid=FID.MAJOR_MINOR, length=LEN.MAJOR_MINOR,
                 title="MajorMinor", name="major_minor",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.MAJOR_MINOR) - 1),)),
        BitField(fid=FID.NATIVE_GESTURE, length=LEN.NATIVE_GESTURE,
                 title="NativeGesture", name="native_gesture",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.NATIVE_GESTURE) - 1),)),
        BitField(fid=FID.WIDTH_HEIGHT, length=LEN.WIDTH_HEIGHT,
                 title="WidthHeight", name="width_height",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.WIDTH_HEIGHT) - 1),)),
        BitField(fid=FID.ENHANCED, length=LEN.ENHANCED,
                 title="Enhanced", name="enhanced",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ENHANCED) - 1),)),
        BitField(fid=FID.FORCE_DATA, length=LEN.FORCE_DATA,
                 title="ForceData", name="force_data",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.FORCE_DATA) - 1),)),
        BitField(fid=FID.RAW, length=LEN.RAW,
                 title="Raw", name="raw",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RAW) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TouchpadRawXY.DEFAULT.PADDING),
    )
# end class ReportBitmap


class GesturesHandlingOutput(TouchpadRawXY):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - GetGesturesHandlingOutputResponse
        - SetGesturesHandlingOutput

    Format:
    =============================================  ==========
    Name                                           Bit count
    =============================================  ==========
    OneFingerClick                                 2
    OneFingerTap                                   2
    OneFingerMove                                  2
    NotDefinedGestures                             2
    OneFingerClickHoldAndOtherFingersMoves         2
    OneFingerClickHoldAndMove                      2
    OneFingerDoubleClick                           2
    OneFingerDoubleTap                             2
    TwoFingersTap                                  2
    OneFingerDoubleTapNotReleaseThe2ndTap          2
    OneFingerOnTheLeftCorner                       2
    OneFingerOnTheRightCorner                      2
    ThreeFingersTapAndDrag                         2
    TwoFingersSlideLeftRight                       2
    TwoFingersScrollUpDown                         2
    TwoFingersClick                                2
    Reserved                                       6
    ThreeFingersSwipe                              2
    Padding                                        88
    =============================================  ==========
    """

    class FID(TouchpadRawXY.FID):
        # See ``TouchpadRawXY.FID``
        ONE_FINGER_CLICK = TouchpadRawXY.FID.SOFTWARE_ID - 1
        ONE_FINGER_TAP = ONE_FINGER_CLICK - 1
        ONE_FINGER_MOVE = ONE_FINGER_TAP - 1
        NOT_DEFINED_GESTURES = ONE_FINGER_MOVE - 1
        ONE_FINGER_CLICK_HOLD_AND_OTHER_FINGERS_MOVES = NOT_DEFINED_GESTURES - 1
        ONE_FINGER_CLICK_HOLD_AND_MOVE = ONE_FINGER_CLICK_HOLD_AND_OTHER_FINGERS_MOVES - 1
        ONE_FINGER_DOUBLE_CLICK = ONE_FINGER_CLICK_HOLD_AND_MOVE - 1
        ONE_FINGER_DOUBLE_TAP = ONE_FINGER_DOUBLE_CLICK - 1
        TWO_FINGERS_TAP = ONE_FINGER_DOUBLE_TAP - 1
        ONE_FINGER_DOUBLE_TAP_NOT_RELEASE_THE_2ND_TAP = TWO_FINGERS_TAP - 1
        ONE_FINGER_ON_THE_LEFT_CORNER = ONE_FINGER_DOUBLE_TAP_NOT_RELEASE_THE_2ND_TAP - 1
        ONE_FINGER_ON_THE_RIGHT_CORNER = ONE_FINGER_ON_THE_LEFT_CORNER - 1
        THREE_FINGERS_TAP_AND_DRAG = ONE_FINGER_ON_THE_RIGHT_CORNER - 1
        TWO_FINGERS_SLIDE_LEFT_RIGHT = THREE_FINGERS_TAP_AND_DRAG - 1
        TWO_FINGERS_SCROLL_UP_DOWN = TWO_FINGERS_SLIDE_LEFT_RIGHT - 1
        TWO_FINGERS_CLICK = TWO_FINGERS_SCROLL_UP_DOWN - 1
        RESERVED = TWO_FINGERS_CLICK - 1
        THREE_FINGERS_SWIPE = RESERVED - 1
        PADDING = THREE_FINGERS_SWIPE - 1
    # end class FID

    class LEN(TouchpadRawXY.LEN):
        # See ``TouchpadRawXY.LEN``
        ONE_FINGER_CLICK = 0x2
        ONE_FINGER_TAP = 0x2
        ONE_FINGER_MOVE = 0x2
        NOT_DEFINED_GESTURES = 0x2
        ONE_FINGER_CLICK_HOLD_AND_OTHER_FINGERS_MOVES = 0x2
        ONE_FINGER_CLICK_HOLD_AND_MOVE = 0x2
        ONE_FINGER_DOUBLE_CLICK = 0x2
        ONE_FINGER_DOUBLE_TAP = 0x2
        TWO_FINGERS_TAP = 0x2
        ONE_FINGER_DOUBLE_TAP_NOT_RELEASE_THE_2ND_TAP = 0x2
        ONE_FINGER_ON_THE_LEFT_CORNER = 0x2
        ONE_FINGER_ON_THE_RIGHT_CORNER = 0x2
        THREE_FINGERS_TAP_AND_DRAG = 0x2
        TWO_FINGERS_SLIDE_LEFT_RIGHT = 0x2
        TWO_FINGERS_SCROLL_UP_DOWN = 0x2
        TWO_FINGERS_CLICK = 0x2
        RESERVED = 0x6
        THREE_FINGERS_SWIPE = 0x2
        PADDING = 0x58
    # end class LEN

    FIELDS = TouchpadRawXY.FIELDS + (
        BitField(fid=FID.ONE_FINGER_CLICK, length=LEN.ONE_FINGER_CLICK,
                 title="OneFingerClick", name="one_finger_click",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_CLICK) - 1),)),
        BitField(fid=FID.ONE_FINGER_TAP, length=LEN.ONE_FINGER_TAP,
                 title="OneFingerTap", name="one_finger_tap",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_TAP) - 1),)),
        BitField(fid=FID.ONE_FINGER_MOVE, length=LEN.ONE_FINGER_MOVE,
                 title="OneFingerMove", name="one_finger_move",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_MOVE) - 1),)),
        BitField(fid=FID.NOT_DEFINED_GESTURES, length=LEN.NOT_DEFINED_GESTURES,
                 title="NotDefinedGestures", name="not_defined_gestures",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.NOT_DEFINED_GESTURES) - 1),)),
        BitField(fid=FID.ONE_FINGER_CLICK_HOLD_AND_OTHER_FINGERS_MOVES,
                 length=LEN.ONE_FINGER_CLICK_HOLD_AND_OTHER_FINGERS_MOVES,
                 title="OneFingerClickHoldAndOtherFingersMoves", name="one_finger_click_hold_and_other_fingers_moves",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_CLICK_HOLD_AND_OTHER_FINGERS_MOVES) - 1),)),
        BitField(fid=FID.ONE_FINGER_CLICK_HOLD_AND_MOVE, length=LEN.ONE_FINGER_CLICK_HOLD_AND_MOVE,
                 title="OneFingerClickHoldAndMove", name="one_finger_click_hold_and_move",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_CLICK_HOLD_AND_MOVE) - 1),)),
        BitField(fid=FID.ONE_FINGER_DOUBLE_CLICK, length=LEN.ONE_FINGER_DOUBLE_CLICK,
                 title="OneFingerDoubleClick", name="one_finger_double_click",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_DOUBLE_CLICK) - 1),)),
        BitField(fid=FID.ONE_FINGER_DOUBLE_TAP, length=LEN.ONE_FINGER_DOUBLE_TAP,
                 title="OneFingerDoubleTap", name="one_finger_double_tap",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_DOUBLE_TAP) - 1),)),
        BitField(fid=FID.TWO_FINGERS_TAP, length=LEN.TWO_FINGERS_TAP,
                 title="TwoFingersTap", name="two_fingers_tap",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.TWO_FINGERS_TAP) - 1),)),
        BitField(fid=FID.ONE_FINGER_DOUBLE_TAP_NOT_RELEASE_THE_2ND_TAP,
                 length=LEN.ONE_FINGER_DOUBLE_TAP_NOT_RELEASE_THE_2ND_TAP,
                 title="OneFingerDoubleTapNotReleaseThe2ndTap", name="one_finger_double_tap_not_release_the_2nd_tap",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_DOUBLE_TAP_NOT_RELEASE_THE_2ND_TAP) - 1),)),
        BitField(fid=FID.ONE_FINGER_ON_THE_LEFT_CORNER, length=LEN.ONE_FINGER_ON_THE_LEFT_CORNER,
                 title="OneFingerOnTheLeftCorner", name="one_finger_on_the_left_corner",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_ON_THE_LEFT_CORNER) - 1),)),
        BitField(fid=FID.ONE_FINGER_ON_THE_RIGHT_CORNER, length=LEN.ONE_FINGER_ON_THE_RIGHT_CORNER,
                 title="OneFingerOnTheRightCorner", name="one_finger_on_the_right_corner",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ONE_FINGER_ON_THE_RIGHT_CORNER) - 1),)),
        BitField(fid=FID.THREE_FINGERS_TAP_AND_DRAG, length=LEN.THREE_FINGERS_TAP_AND_DRAG,
                 title="ThreeFingersTapAndDrag", name="three_fingers_tap_and_drag",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.THREE_FINGERS_TAP_AND_DRAG) - 1),)),
        BitField(fid=FID.TWO_FINGERS_SLIDE_LEFT_RIGHT, length=LEN.TWO_FINGERS_SLIDE_LEFT_RIGHT,
                 title="TwoFingersSlideLeftRight", name="two_fingers_slide_left_right",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.TWO_FINGERS_SLIDE_LEFT_RIGHT) - 1),)),
        BitField(fid=FID.TWO_FINGERS_SCROLL_UP_DOWN, length=LEN.TWO_FINGERS_SCROLL_UP_DOWN,
                 title="TwoFingersScrollUpDown", name="two_fingers_scroll_up_down",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.TWO_FINGERS_SCROLL_UP_DOWN) - 1),)),
        BitField(fid=FID.TWO_FINGERS_CLICK, length=LEN.TWO_FINGERS_CLICK,
                 title="TwoFingersClick", name="two_fingers_click",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.TWO_FINGERS_CLICK) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=TouchpadRawXY.DEFAULT.RESERVED),
        BitField(fid=FID.THREE_FINGERS_SWIPE, length=LEN.THREE_FINGERS_SWIPE,
                 title="ThreeFingersSwipe", name="three_fingers_swipe",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.THREE_FINGERS_SWIPE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TouchpadRawXY.DEFAULT.PADDING),
    )
# end class GesturesHandlingOutput


class GetTouchpadInfo(ShortEmptyPacketDataFormat):
    """
    Define ``GetTouchpadInfo`` implementation class for version 1
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
                         functionIndex=GetTouchpadInfoResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetTouchpadInfo


class GetTouchpadInfoResponse(TouchpadRawXY):
    """
    Define ``GetTouchpadInfoResponse`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    XSize                         16
    YSize                         16
    ZDataRange                    8
    AreaDataRange                 8
    TimestampUnits                8
    MaxFingerCount                8
    Origin                        8
    PenSupport                    8
    Reserved                      16
    RawReportMappingVersion       8
    DPI                           16
    Padding                       8
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetTouchpadInfo,)
    VERSION = (1,)
    FUNCTION_INDEX = 0

    class FID(TouchpadRawXY.FID):
        # See ``TouchpadRawXY.FID``
        X_SIZE = TouchpadRawXY.FID.SOFTWARE_ID - 1
        Y_SIZE = X_SIZE - 1
        Z_DATA_RANGE = Y_SIZE - 1
        AREA_DATA_RANGE = Z_DATA_RANGE - 1
        TIMESTAMP_UNITS = AREA_DATA_RANGE - 1
        MAX_FINGER_COUNT = TIMESTAMP_UNITS - 1
        ORIGIN = MAX_FINGER_COUNT - 1
        PEN_SUPPORT = ORIGIN - 1
        RESERVED = PEN_SUPPORT - 1
        RAW_REPORT_MAPPING_VERSION = RESERVED - 1
        DPI = RAW_REPORT_MAPPING_VERSION - 1
        PADDING = DPI - 1
    # end class FID

    class LEN(TouchpadRawXY.LEN):
        # See ``TouchpadRawXY.LEN``
        X_SIZE = 0x10
        Y_SIZE = 0x10
        Z_DATA_RANGE = 0x8
        AREA_DATA_RANGE = 0x8
        TIMESTAMP_UNITS = 0x8
        MAX_FINGER_COUNT = 0x8
        ORIGIN = 0x8
        PEN_SUPPORT = 0x8
        RESERVED = 0x10
        RAW_REPORT_MAPPING_VERSION = 0x8
        DPI = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = TouchpadRawXY.FIELDS + (
        BitField(fid=FID.X_SIZE, length=LEN.X_SIZE,
                 title="XSize", name="x_size",
                 checks=(CheckHexList(LEN.X_SIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.X_SIZE) - 1),)),
        BitField(fid=FID.Y_SIZE, length=LEN.Y_SIZE,
                 title="YSize", name="y_size",
                 checks=(CheckHexList(LEN.Y_SIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.Y_SIZE) - 1),)),
        BitField(fid=FID.Z_DATA_RANGE, length=LEN.Z_DATA_RANGE,
                 title="ZDataRange", name="z_data_range",
                 checks=(CheckHexList(LEN.Z_DATA_RANGE // 8),
                         CheckByte(),)),
        BitField(fid=FID.AREA_DATA_RANGE, length=LEN.AREA_DATA_RANGE,
                 title="AreaDataRange", name="area_data_range",
                 checks=(CheckHexList(LEN.AREA_DATA_RANGE // 8),
                         CheckByte(),)),
        BitField(fid=FID.TIMESTAMP_UNITS, length=LEN.TIMESTAMP_UNITS,
                 title="TimestampUnits", name="timestamp_units",
                 checks=(CheckHexList(LEN.TIMESTAMP_UNITS // 8),
                         CheckByte(),)),
        BitField(fid=FID.MAX_FINGER_COUNT, length=LEN.MAX_FINGER_COUNT,
                 title="MaxFingerCount", name="max_finger_count",
                 checks=(CheckHexList(LEN.MAX_FINGER_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.ORIGIN, length=LEN.ORIGIN,
                 title="Origin", name="origin",
                 checks=(CheckHexList(LEN.ORIGIN // 8),
                         CheckByte(),)),
        BitField(fid=FID.PEN_SUPPORT, length=LEN.PEN_SUPPORT,
                 title="PenSupport", name="pen_support",
                 checks=(CheckHexList(LEN.PEN_SUPPORT // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=TouchpadRawXY.DEFAULT.RESERVED),
        BitField(fid=FID.RAW_REPORT_MAPPING_VERSION, length=LEN.RAW_REPORT_MAPPING_VERSION,
                 title="RawReportMappingVersion", name="raw_report_mapping_version",
                 checks=(CheckHexList(LEN.RAW_REPORT_MAPPING_VERSION // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI, length=LEN.DPI,
                 title="DPI", name="dpi",
                 checks=(CheckHexList(LEN.DPI // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TouchpadRawXY.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 x_size, y_size, z_data_range, area_data_range, timestamp_units, max_finger_count, origin, pen_support,
                 raw_report_mapping_version, dpi, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param x_size: The extent of the touch pad coordinates, in native resolution.
        :type x_size: ``int`` or ``HexList``
        :param y_size: The extent of the touch pad coordinates, in native resolution.
        :type y_size: ``int`` or ``HexList``
        :param z_data_range: 0x00 means no range, 0x0f means 16-bit. Other values are reserved.
        :type z_data_range: ``int`` or ``HexList``
        :param area_data_range: 0x0f means 16-bit. Other values are reserved.
        :type area_data_range: ``int`` or ``HexList``
        :param timestamp_units: Number of 0.1 milliseconds per timestamp increment.
        :type timestamp_units: ``int`` or ``HexList``
        :param max_finger_count: Maximum number of fingers that can be tracked.
        :type max_finger_count: ``int`` or ``HexList``
        :param origin: Position of the origin
        :type origin: ``int`` or ``HexList``
        :param pen_support: 0x00 = no support, 0x01 = support.
        :type pen_support: ``int`` or ``HexList``
        :param raw_report_mapping_version: Raw Report Mapping Version
        :type raw_report_mapping_version: ``int`` or ``HexList``
        :param dpi: DPI
        :type dpi: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.x_size = x_size
        self.y_size = y_size
        self.z_data_range = z_data_range
        self.area_data_range = area_data_range
        self.timestamp_units = timestamp_units
        self.max_finger_count = max_finger_count
        self.origin = origin
        self.pen_support = pen_support
        self.raw_report_mapping_version = raw_report_mapping_version
        self.dpi = dpi
    # end def __init__
# end class GetTouchpadInfoResponse


class GetRawReportState(ShortEmptyPacketDataFormat):
    """
    Define ``GetRawReportState`` implementation class for version 1
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
                         functionIndex=GetRawReportStateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetRawReportState


class GetRawReportStateResponse(ReportBitmap):
    """
    Define ``GetRawReportStateResponse`` implementation class for version 1
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRawReportState,)
    VERSION = (1,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, width_height_bytes, major_minor, native_gesture, width_height,
                enhanced, force_data, raw, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param width_height_bytes: Flag indicating that the width and height bytes reporting is enabled
        :type width_height_bytes: ``bool`` or ``HexList``
        :param major_minor: Flag indicating that the the Major/Minor/Orientation reporting is enabled
        :type major_minor: ``bool`` or ``HexList``
        :param native_gesture: Flag indicating that the native gesture reporting is enabled
        :type native_gesture: ``bool`` or ``HexList``
        :param width_height: Flag indicating that the bit Width/Height reporting is enabled
        :type width_height: ``bool`` or ``HexList``
        :param enhanced: Flag indicating that the enhanced reporting is enabled
        :type enhanced: ``bool`` or ``HexList``
        :param force_data: Flag indicating that the force data reporting is enabled
        :type force_data: ``bool`` or ``HexList``
        :param raw: Flag indicating that the raw reporting is enabled
        :type raw: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.width_height_bytes = width_height_bytes
        self.major_minor = major_minor
        self.native_gesture = native_gesture
        self.width_height = width_height
        self.enhanced = enhanced
        self.force_data = force_data
        self.raw = raw
    # end def __init__
# end class GetRawReportStateResponse


class SetRawReportState(ReportBitmap):
    """
    Define ``SetRawReportState`` implementation class for version 1
    """

    def __init__(self, device_index, feature_index, width_height_bytes, major_minor, native_gesture, width_height,
                enhanced, force_data, raw, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param width_height_bytes: Flag indicating that the width and height bytes reporting is enabled
        :type width_height_bytes: ``bool`` or ``HexList``
        :param major_minor: Flag indicating that the the Major/Minor/Orientation reporting is enabled
        :type major_minor: ``bool`` or ``HexList``
        :param native_gesture: Flag indicating that the native gesture reporting is enabled
        :type native_gesture: ``bool`` or ``HexList``
        :param width_height: Flag indicating that the bit Width/Height reporting is enabled
        :type width_height: ``bool`` or ``HexList``
        :param enhanced: Flag indicating that the enhanced reporting is enabled
        :type enhanced: ``bool`` or ``HexList``
        :param force_data: Flag indicating that the force data reporting is enabled
        :type force_data: ``bool`` or ``HexList``
        :param raw: Flag indicating that the raw reporting is enabled
        :type raw: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetRawReportStateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.width_height_bytes = width_height_bytes
        self.major_minor = major_minor
        self.native_gesture = native_gesture
        self.width_height = width_height
        self.enhanced = enhanced
        self.force_data = force_data
        self.raw = raw
    # end def __init__
# end class SetRawReportState


class SetRawReportStateResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetRawReportStateResponse`` implementation class for version 1
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRawReportState,)
    VERSION = (1,)
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
# end class SetRawReportStateResponse


class GetGesturesHandlingOutput(ShortEmptyPacketDataFormat):
    """
    Define ``GetGesturesHandlingOutput`` implementation class for version 1
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
                         functionIndex=GetGesturesHandlingOutputResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetGesturesHandlingOutput


class GetGesturesHandlingOutputResponse(GesturesHandlingOutput):
    """
    Define ``GetGesturesHandlingOutputResponse`` implementation class for version 1
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetGesturesHandlingOutput,)
    VERSION = (1,)
    FUNCTION_INDEX = 3

    class HandlingOutput:
        """
        Define ``HandlingOutput`` constant variables for GetGesturesHandlingOutput
        """
        NOT_SUPPORTED = 0
        SUPPORTED_AND_HID = 1
        SUPPORTED_BUT_NO_HID = 2
        SUPPORTED_AND_HIDPP = 3
    # end class HandlingOutput

    def __init__(self, device_index, feature_index,
                 one_finger_click, one_finger_tap, one_finger_move, not_defined_gestures,
                 one_finger_click_hold_and_other_fingers_moves, one_finger_click_hold_and_move, one_finger_double_click,
                 one_finger_double_tap, two_fingers_tap, one_finger_double_tap_not_release_the_2nd_tap,
                 one_finger_on_the_left_corner, one_finger_on_the_right_corner, three_fingers_tap_and_drag,
                 two_fingers_slide_left_right, two_fingers_scroll_up_down, two_fingers_click, three_fingers_swipe,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param one_finger_click: 1-finger click handling output
        :type one_finger_click: ``int`` or ``HexList``
        :param one_finger_tap: 1-finger tap handling output
        :type one_finger_tap: ``int`` or ``HexList``
        :param one_finger_move: 1-finger move handling output
        :type one_finger_move: ``int`` or ``HexList``
        :param not_defined_gestures: Not defined gestures handling output
        :type not_defined_gestures: ``int`` or ``HexList``
        :param one_finger_click_hold_and_other_fingers_moves: 1-finger click, hold and other fingers moves
                                                              handling output
        :type one_finger_click_hold_and_other_fingers_moves: ``int`` or ``HexList``
        :param one_finger_click_hold_and_move: 1-finger click, hold and move handling output
        :type one_finger_click_hold_and_move: ``int`` or ``HexList``
        :param one_finger_double_click: 1-finger double click handling output
        :type one_finger_double_click: ``int`` or ``HexList``
        :param one_finger_double_tap: 1-finger double tap handling output
        :type one_finger_double_tap: ``int`` or ``HexList``
        :param two_fingers_tap: 2-fingers tap handling output
        :type two_fingers_tap: ``int`` or ``HexList``
        :param one_finger_double_tap_not_release_the_2nd_tap: 1-finger double tap (not release the second tap), then
                                                              move handling output
        :type one_finger_double_tap_not_release_the_2nd_tap: ``int`` or ``HexList``
        :param one_finger_on_the_left_corner: 1-finger on the left corner handling output
        :type one_finger_on_the_left_corner: ``int`` or ``HexList``
        :param one_finger_on_the_right_corner: 1-finger on the left corner handling output
        :type one_finger_on_the_right_corner: ``int`` or ``HexList``
        :param three_fingers_tap_and_drag: 3-fingers tap and drag handling output
        :type three_fingers_tap_and_drag: ``int`` or ``HexList``
        :param two_fingers_slide_left_right: 2-fingers slide left/right handling output
        :type two_fingers_slide_left_right: ``int`` or ``HexList``
        :param two_fingers_scroll_up_down: 2-fingers scroll up/down handling output
        :type two_fingers_scroll_up_down: ``int`` or ``HexList``
        :param two_fingers_click: 2-fingers click handling output
        :type two_fingers_click: ``int`` or ``HexList``
        :param three_fingers_swipe: 3-fingers swipe handling output
        :type three_fingers_swipe: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.one_finger_click = one_finger_click
        self.one_finger_tap = one_finger_tap
        self.one_finger_move = one_finger_move
        self.not_defined_gestures = not_defined_gestures
        self.one_finger_click_hold_and_other_fingers_moves = one_finger_click_hold_and_other_fingers_moves
        self.one_finger_click_hold_and_move = one_finger_click_hold_and_move
        self.one_finger_double_click = one_finger_double_click
        self.one_finger_double_tap = one_finger_double_tap
        self.two_fingers_tap = two_fingers_tap
        self.one_finger_double_tap_not_release_the_2nd_tap = one_finger_double_tap_not_release_the_2nd_tap
        self.one_finger_on_the_left_corner = one_finger_on_the_left_corner
        self.one_finger_on_the_right_corner = one_finger_on_the_right_corner
        self.three_fingers_tap_and_drag = three_fingers_tap_and_drag
        self.two_fingers_slide_left_right = two_fingers_slide_left_right
        self.two_fingers_scroll_up_down = two_fingers_scroll_up_down
        self.two_fingers_click = two_fingers_click
        self.three_fingers_swipe = three_fingers_swipe
    # end def __init__
# end class GetGesturesHandlingOutputResponse


class SetGesturesHandlingOutput(GesturesHandlingOutput):
    """
    Define ``SetGesturesHandlingOutput`` implementation class for version 1
    """

    class HandlingOutput:
        """
        Define ``HandlingOutput`` constant variables for SetGesturesHandlingOutput
        """
        NOT_ALLOWED_0 = 0
        SUPPORTED_AND_HID = 1
        SUPPORTED_BUT_NO_HID = 2
        NOT_ALLOWED_3 = 3
    # end class HandlingOutput

    def __init__(self, device_index, feature_index,
                 one_finger_click, one_finger_tap, one_finger_move, not_defined_gestures,
                 one_finger_click_hold_and_other_fingers_moves, one_finger_click_hold_and_move, one_finger_double_click,
                 one_finger_double_tap, two_fingers_tap, one_finger_double_tap_not_release_the_2nd_tap,
                 one_finger_on_the_left_corner, one_finger_on_the_right_corner, three_fingers_tap_and_drag,
                 two_fingers_slide_left_right, two_fingers_scroll_up_down, two_fingers_click, three_fingers_swipe,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param one_finger_click: One Finger Click
        :type one_finger_click: ``int`` or ``HexList``
        :param one_finger_tap: One Finger Tap
        :type one_finger_tap: ``int`` or ``HexList``
        :param one_finger_move: One Finger Move
        :type one_finger_move: ``int`` or ``HexList``
        :param not_defined_gestures: Not Defined Gestures
        :type not_defined_gestures: ``int`` or ``HexList``
        :param one_finger_click_hold_and_other_fingers_moves: One Finger Click Hold And Other Fingers Moves
        :type one_finger_click_hold_and_other_fingers_moves: ``int`` or ``HexList``
        :param one_finger_click_hold_and_move: One Finger Click Hold And Move
        :type one_finger_click_hold_and_move: ``int`` or ``HexList``
        :param one_finger_double_click: One Finger Double Click
        :type one_finger_double_click: ``int`` or ``HexList``
        :param one_finger_double_tap: One Finger Double Tap
        :type one_finger_double_tap: ``int`` or ``HexList``
        :param two_fingers_tap: Two Fingers Tap
        :type two_fingers_tap: ``int`` or ``HexList``
        :param one_finger_double_tap_not_release_the_2nd_tap: One Finger Double Tap Not Release The 2nd Tap
        :type one_finger_double_tap_not_release_the_2nd_tap: ``int`` or ``HexList``
        :param one_finger_on_the_left_corner: One Finger On The Left Corner
        :type one_finger_on_the_left_corner: ``int`` or ``HexList``
        :param one_finger_on_the_right_corner: One Finger On The Right Corner
        :type one_finger_on_the_right_corner: ``int`` or ``HexList``
        :param three_fingers_tap_and_drag: Three Fingers Tap And Drag
        :type three_fingers_tap_and_drag: ``int`` or ``HexList``
        :param two_fingers_slide_left_right: Two Fingers Slide Left Right
        :type two_fingers_slide_left_right: ``int`` or ``HexList``
        :param two_fingers_scroll_up_down: Two Fingers Scroll Up Down
        :type two_fingers_scroll_up_down: ``int`` or ``HexList``
        :param two_fingers_click: Two Fingers Click
        :type two_fingers_click: ``int`` or ``HexList``
        :param three_fingers_swipe: Three Fingers Swipe
        :type three_fingers_swipe: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetGesturesHandlingOutputResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.one_finger_click = one_finger_click
        self.one_finger_tap = one_finger_tap
        self.one_finger_move = one_finger_move
        self.not_defined_gestures = not_defined_gestures
        self.one_finger_click_hold_and_other_fingers_moves = one_finger_click_hold_and_other_fingers_moves
        self.one_finger_click_hold_and_move = one_finger_click_hold_and_move
        self.one_finger_double_click = one_finger_double_click
        self.one_finger_double_tap = one_finger_double_tap
        self.two_fingers_tap = two_fingers_tap
        self.one_finger_double_tap_not_release_the_2nd_tap = one_finger_double_tap_not_release_the_2nd_tap
        self.one_finger_on_the_left_corner = one_finger_on_the_left_corner
        self.one_finger_on_the_right_corner = one_finger_on_the_right_corner
        self.three_fingers_tap_and_drag = three_fingers_tap_and_drag
        self.two_fingers_slide_left_right = two_fingers_slide_left_right
        self.two_fingers_scroll_up_down = two_fingers_scroll_up_down
        self.two_fingers_click = two_fingers_click
        self.three_fingers_swipe = three_fingers_swipe
    # end def __init__
# end class SetGesturesHandlingOutput


class SetGesturesHandlingOutputResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetGesturesHandlingOutputResponse`` implementation class for version 1
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetGesturesHandlingOutput,)
    VERSION = (1,)
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
# end class SetGesturesHandlingOutputResponse


class DualXYDataEvent(TouchpadRawXY):
    """
    Define ``DualXYDataEvent`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Timestamp                     16
    ContactType1                  2
    X1 Coordinate                 14
    ContactStatus1                2
    Y1 Coordinate                 14
    Z1 Coordinate                 8
    Area1                         8
    FingerID1                     4
    Reserved                      1
    Button                        1
    SP1                           1
    EndOfFrame                    1
    ContactType2                  2
    X2 Coordinate                 14
    ContactStatus2                2
    Y2 Coordinate                 14
    Z2 Coordinate                 8
    Area2                         8
    FingerID2                     4
    NumberFingers                 4
    ============================  ==========
    """

    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 0

    class FID(TouchpadRawXY.FID):
        # See ``TouchpadRawXY.FID``
        TIMESTAMP = TouchpadRawXY.FID.SOFTWARE_ID - 1
        CONTACT_TYPE_1 = TIMESTAMP - 1
        X1_COORDINATE = CONTACT_TYPE_1 - 1
        CONTACT_STATUS_1 = X1_COORDINATE - 1
        Y1_COORDINATE = CONTACT_STATUS_1 - 1
        Z1_COORDINATE = Y1_COORDINATE - 1
        AREA_1 = Z1_COORDINATE - 1
        FINGER_ID_1 = AREA_1 - 1
        RESERVED = FINGER_ID_1 - 1
        BUTTON = RESERVED - 1
        SP_1 = BUTTON - 1
        END_OF_FRAME = SP_1 - 1
        CONTACT_TYPE_2 = END_OF_FRAME - 1
        X2_COORDINATE = CONTACT_TYPE_2 - 1
        CONTACT_STATUS_2 = X2_COORDINATE - 1
        Y2_COORDINATE = CONTACT_STATUS_2 - 1
        Z2_COORDINATE = Y2_COORDINATE - 1
        AREA_2 = Z2_COORDINATE - 1
        FINGER_ID_2 = AREA_2 - 1
        NUMBER_FINGERS = FINGER_ID_2 - 1

    # end class FID

    class LEN(TouchpadRawXY.LEN):
        # See ``TouchpadRawXY.LEN``
        TIMESTAMP = 0x10
        CONTACT_TYPE_1 = 0x2
        X1_COORDINATE = 0xe
        CONTACT_STATUS_1 = 0x2
        Y1_COORDINATE = 0xe
        Z1_COORDINATE = 0x8
        AREA_1 = 0x8
        FINGER_ID_1 = 0x4
        RESERVED = 0x1
        BUTTON = 0x1
        SP_1 = 0x1
        END_OF_FRAME = 0x1
        CONTACT_TYPE_2 = 0x2
        X2_COORDINATE = 0xe
        CONTACT_STATUS_2 = 0x2
        Y2_COORDINATE = 0xe
        Z2_COORDINATE = 0x8
        AREA_2 = 0x8
        FINGER_ID_2 = 0x4
        NUMBER_FINGERS = 0x4
    # end class LEN

    FIELDS = TouchpadRawXY.FIELDS + (
        BitField(fid=FID.TIMESTAMP, length=LEN.TIMESTAMP,
                 title="Timestamp", name="timestamp",
                 checks=(CheckHexList(LEN.TIMESTAMP // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIMESTAMP) - 1),)),
        BitField(fid=FID.CONTACT_TYPE_1, length=LEN.CONTACT_TYPE_1,
                 title="ContactType1", name="contact_type_1",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CONTACT_TYPE_1) - 1),)),
        BitField(fid=FID.X1_COORDINATE, length=LEN.X1_COORDINATE,
                 title="X1 Coordinate", name="x1_coordinate",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.X1_COORDINATE) - 1),)),
        BitField(fid=FID.CONTACT_STATUS_1, length=LEN.CONTACT_STATUS_1,
                 title="ContactStatus1", name="contact_status_1",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CONTACT_STATUS_1) - 1),)),
        BitField(fid=FID.Y1_COORDINATE, length=LEN.Y1_COORDINATE,
                 title="Y1 Coordinate", name="y1_coordinate",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.Y1_COORDINATE) - 1),)),
        BitField(fid=FID.Z1_COORDINATE, length=LEN.Z1_COORDINATE,
                 title="Z1 Coordinate", name="z1_coordinate",
                 checks=(CheckHexList(LEN.Z1_COORDINATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.AREA_1, length=LEN.AREA_1,
                 title="Area1", name="area_1",
                 checks=(CheckHexList(LEN.AREA_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.FINGER_ID_1, length=LEN.FINGER_ID_1,
                 title="FingerID1", name="finger_id_1",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.FINGER_ID_1) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=TouchpadRawXY.DEFAULT.RESERVED),
        BitField(fid=FID.BUTTON, length=LEN.BUTTON,
                 title="Button", name="button",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON) - 1),)),
        BitField(fid=FID.SP_1, length=LEN.SP_1,
                 title="SP1", name="sp_1",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.SP_1) - 1),)),
        BitField(fid=FID.END_OF_FRAME, length=LEN.END_OF_FRAME,
                 title="EndOfFrame", name="end_of_frame",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.END_OF_FRAME) - 1),)),
        BitField(fid=FID.CONTACT_TYPE_2, length=LEN.CONTACT_TYPE_2,
                 title="ContactType2", name="contact_type_2",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CONTACT_TYPE_2) - 1),)),
        BitField(fid=FID.X2_COORDINATE, length=LEN.X2_COORDINATE,
                 title="X2 Coordinate", name="x2_coordinate",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.X2_COORDINATE) - 1),)),
        BitField(fid=FID.CONTACT_STATUS_2, length=LEN.CONTACT_STATUS_2,
                 title="ContactStatus2", name="contact_status_2",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CONTACT_STATUS_2) - 1),)),
        BitField(fid=FID.Y2_COORDINATE, length=LEN.Y2_COORDINATE,
                 title="Y2 Coordinate", name="y2_coordinate",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.Y2_COORDINATE) - 1),)),
        BitField(fid=FID.Z2_COORDINATE, length=LEN.Z2_COORDINATE,
                 title="Z2 Coordinate", name="z2_coordinate",
                 checks=(CheckHexList(LEN.Z2_COORDINATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.AREA_2, length=LEN.AREA_2,
                 title="Area2", name="area_2",
                 checks=(CheckHexList(LEN.AREA_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.FINGER_ID_2, length=LEN.FINGER_ID_2,
                 title="FingerID2", name="finger_id_2",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.FINGER_ID_2) - 1),)),
        BitField(fid=FID.NUMBER_FINGERS, length=LEN.NUMBER_FINGERS,
                 title="NumberFingers", name="number_fingers",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.NUMBER_FINGERS) - 1),)),
    )

    def __init__(self, device_index, feature_index,
                 timestamp, contact_type_1, x1_coordinate, contact_status_1, y1_coordinate, z1_coordinate, area_1,
                 finger_id_1, button, sp_1, end_of_frame, contact_type_2, x2_coordinate, contact_status_2,
                 y2_coordinate, z2_coordinate, area_2, finger_id_2, number_fingers, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param timestamp: A running timestamp for the touch frame. Note that the value is encoded in Big-Endian
        :type timestamp: ``int`` or ``HexList``
        :param contact_type_1: Contact Type for touch 1/2. 0b00 = finger, 0b01/0b10/0b11 = reserved.
        :type contact_type_1: ``int`` or ``HexList``
        :param x1_coordinate: The coordinates in device units of the center of the touch point.
        :type x1_coordinate: ``int`` or ``HexList``
        :param contact_status_1: Contact Status for touch 1/2. 0b00 = hover, 0b01 = touch, 0b10/0b11 = reserved.
        :type contact_status_1: ``int`` or ``HexList``
        :param y1_coordinate: The coordinates in device units of the center of the touch point.
        :type y1_coordinate: ``int`` or ``HexList``
        :param z1_coordinate: The Z coordinate of the touch point. This is roughly the distance of the finger from
                           the surface.
        :type z1_coordinate: ``int`` or ``HexList``
        :param area_1: The area of the touch point in arbitrary units.
        :type area_1: ``int`` or ``HexList``
        :param finger_id_1: A unique finger ID per touch point.
        :type finger_id_1: ``int`` or ``HexList``
        :param button: Indicates whether the pysical switch underneath the touch surface is being pressed or not.
                    0b0 = not pressed, 0b1 = pressed.
        :type button: ``bool`` or ``HexList``
        :param sp_1: SP 1
        :type sp_1: ``bool`` or ``HexList``
        :param end_of_frame: End of frame flag. 0b0 = there are more reports for this frame that follow, 0b1 = this is
                    the last event for this frame
        :type end_of_frame: ``bool`` or ``HexList``
        :param contact_type_2: Contact Type for touch 1/2. 0b00 = finger, 0b01/0b10/0b11 = reserved.
        :type contact_type_2: ``int`` or ``HexList``
        :param x2_coordinate: The coordinates in device units of the center of the touch point.
        :type x2_coordinate: ``int`` or ``HexList``
        :param contact_status_2: Contact Status for touch 1/2. 0b00 = hover, 0b01 = touch, 0b10/0b11 = reserved.
        :type contact_status_2: ``int`` or ``HexList``
        :param y2_coordinate: The coordinates in device units of the center of the touch point.
        :type y2_coordinate: ``int`` or ``HexList``
        :param z2_coordinate: The Z coordinate of the touch point. This is roughly the distance of the finger from
                            the surface.
        :type z2_coordinate: ``int`` or ``HexList``
        :param area_2: The area of the touch point in arbitrary units.
        :type area_2: ``int`` or ``HexList``
        :param finger_id_2: A unique finger ID per touch point.
        :type finger_id_2: ``int`` or ``HexList``
        :param number_fingers: The total number of fingers in the frame.
        :type number_fingers: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.timestamp = timestamp
        self.contact_type_1 = contact_type_1
        self.x1_coordinate = x1_coordinate
        self.contact_status_1 = contact_status_1
        self.y1_coordinate = y1_coordinate
        self.z1_coordinate = z1_coordinate
        self.area_1 = area_1
        self.finger_id_1 = finger_id_1
        self.button = button
        self.sp_1 = sp_1
        self.end_of_frame = end_of_frame
        self.contact_type_2 = contact_type_2
        self.x2_coordinate = x2_coordinate
        self.contact_status_2 = contact_status_2
        self.y2_coordinate = y2_coordinate
        self.z2_coordinate = z2_coordinate
        self.area_2 = area_2
        self.finger_id_2 = finger_id_2
        self.number_fingers = number_fingers
    # end def __init__
# end class DualXYDataEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
