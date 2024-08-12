#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.touchpadrawxyutils
:brief: Helpers for ``TouchpadRawXY`` feature
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.touchpad.touchpadrawxy import TouchpadRawXY
from pyhid.hidpp.features.touchpad.touchpadrawxy import TouchpadRawXYFactory
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetTouchpadInfoResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetRawReportStateResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetGesturesHandlingOutputResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import SetRawReportStateResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import SetGesturesHandlingOutputResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import DualXYDataEvent
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TouchpadRawXYTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``TouchpadRawXY`` feature
    """

    class GetTouchpadInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetTouchpadInfo`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetTouchpadInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.TOUCHPAD.TOUCHPAD_RAW_XY
            return {
                "x_size": (
                    cls.check_x_size, config.F_XSize),
                "y_size": (
                    cls.check_y_size, config.F_YSize),
                "z_data_range": (
                    cls.check_z_data_range, config.F_ZDataRange),
                "area_data_range": (
                    cls.check_area_data_range, config.F_AreaDataRange),
                "timestamp_units": (
                    cls.check_timestamp_units, config.F_TimestampUnits),
                "max_finger_count": (
                    cls.check_max_finger_count, config.F_MaxFingerCount),
                "origin": (
                    cls.check_origin, config.F_Origin),
                "pen_support": (
                    cls.check_pen_support, config.F_PenSupport),
                "reserved": (
                    cls.check_reserved, 0),
                "raw_report_mapping_version": (
                    cls.check_raw_report_mapping_version, config.F_RawReportMappingVersion),
                "dpi": (
                    cls.check_dpi, config.F_DPI)
            }
        # end def get_default_check_map

        @staticmethod
        def check_x_size(test_case, response, expected):
            """
            Check x_size field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.x_size),
                msg=f"The x_size parameter differs "
                    f"(expected:{expected}, obtained:{response.x_size})")
        # end def check_x_size

        @staticmethod
        def check_y_size(test_case, response, expected):
            """
            Check y_size field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.y_size),
                msg=f"The y_size parameter differs "
                    f"(expected:{expected}, obtained:{response.y_size})")
        # end def check_y_size

        @staticmethod
        def check_z_data_range(test_case, response, expected):
            """
            Check z_data_range field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.z_data_range),
                msg=f"The z_data_range parameter differs "
                    f"(expected:{expected}, obtained:{response.z_data_range})")
        # end def check_z_data_range

        @staticmethod
        def check_area_data_range(test_case, response, expected):
            """
            Check area_data_range field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.area_data_range),
                msg=f"The area_data_range parameter differs "
                    f"(expected:{expected}, obtained:{response.area_data_range})")
        # end def check_area_data_range

        @staticmethod
        def check_timestamp_units(test_case, response, expected):
            """
            Check timestamp_units field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.timestamp_units),
                msg=f"The timestamp_units parameter differs "
                    f"(expected:{expected}, obtained:{response.timestamp_units})")
        # end def check_timestamp_units

        @staticmethod
        def check_max_finger_count(test_case, response, expected):
            """
            Check max_finger_count field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.max_finger_count),
                msg=f"The max_finger_count parameter differs "
                    f"(expected:{expected}, obtained:{response.max_finger_count})")
        # end def check_max_finger_count

        @staticmethod
        def check_origin(test_case, response, expected):
            """
            Check origin field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.origin),
                msg=f"The origin parameter differs "
                    f"(expected:{expected}, obtained:{response.origin})")
        # end def check_origin

        @staticmethod
        def check_pen_support(test_case, response, expected):
            """
            Check pen_support field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.pen_support),
                msg=f"The pen_support parameter differs "
                    f"(expected:{expected}, obtained:{response.pen_support})")
        # end def check_pen_support

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved

        @staticmethod
        def check_raw_report_mapping_version(test_case, response, expected):
            """
            Check raw_report_mapping_version field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.raw_report_mapping_version),
                msg=f"The raw_report_mapping_version parameter differs "
                    f"(expected:{expected}, obtained:{response.raw_report_mapping_version})")
        # end def check_raw_report_mapping_version

        @staticmethod
        def check_dpi(test_case, response, expected):
            """
            Check dpi field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTouchpadInfoResponse to check
            :type response: ``GetTouchpadInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi),
                msg=f"The dpi parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi})")
        # end def check_dpi
    # end class GetTouchpadInfoResponseChecker

    class GetRawReportStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetRawReportState`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetRawReportStateResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.TOUCHPAD.TOUCHPAD_RAW_XY
            return {
                "reserved": (
                    cls.check_reserved, 0),
                "width_height_bytes": (
                    cls.check_width_height_bytes,
                    HexList(config.F_ReportBitmap).testBit(GetRawReportStateResponse.POS.WIDTH_HEIGHT_BYTES)),
                "major_minor": (
                    cls.check_major_minor,
                    HexList(config.F_ReportBitmap).testBit(GetRawReportStateResponse.POS.MAJOR_MINOR)),
                "native_gesture": (
                    cls.check_native_gesture,
                    HexList(config.F_ReportBitmap).testBit(GetRawReportStateResponse.POS.NATIVE_GESTURE)),
                "width_height": (
                    cls.check_width_height,
                    HexList(config.F_ReportBitmap).testBit(GetRawReportStateResponse.POS.WIDTH_HEIGHT)),
                "enhanced": (
                    cls.check_enhanced, HexList(config.F_ReportBitmap).testBit(GetRawReportStateResponse.POS.ENHANCED)),
                "force_data": (
                    cls.check_force_data,
                    HexList(config.F_ReportBitmap).testBit(GetRawReportStateResponse.POS.FORCE_DATA)),
                "raw": (
                    cls.check_raw, HexList(config.F_ReportBitmap).testBit(GetRawReportStateResponse.POS.RAW))
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved

        @staticmethod
        def check_width_height_bytes(test_case, response, expected):
            """
            Check width_height_bytes field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.width_height_bytes),
                msg=f"The width_height_bytes parameter differs "
                    f"(expected:{expected}, obtained:{response.width_height_bytes})")
        # end def check_width_height_bytes

        @staticmethod
        def check_major_minor(test_case, response, expected):
            """
            Check major_minor field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.major_minor),
                msg=f"The major_minor parameter differs "
                    f"(expected:{expected}, obtained:{response.major_minor})")
        # end def check_major_minor

        @staticmethod
        def check_native_gesture(test_case, response, expected):
            """
            Check native_gesture field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.native_gesture),
                msg=f"The native_gesture parameter differs "
                    f"(expected:{expected}, obtained:{response.native_gesture})")
        # end def check_native_gesture

        @staticmethod
        def check_width_height(test_case, response, expected):
            """
            Check width_height field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.width_height),
                msg=f"The width_height parameter differs "
                    f"(expected:{expected}, obtained:{response.width_height})")
        # end def check_width_height

        @staticmethod
        def check_enhanced(test_case, response, expected):
            """
            Check enhanced field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.enhanced),
                msg=f"The enhanced parameter differs "
                    f"(expected:{expected}, obtained:{response.enhanced})")
        # end def check_enhanced

        @staticmethod
        def check_force_data(test_case, response, expected):
            """
            Check force_data field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.force_data),
                msg=f"The force_data parameter differs "
                    f"(expected:{expected}, obtained:{response.force_data})")
        # end def check_force_data

        @staticmethod
        def check_raw(test_case, response, expected):
            """
            Check raw field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetRawReportStateResponse to check
            :type response: ``GetRawReportStateResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.raw),
                msg=f"The raw parameter differs "
                    f"(expected:{expected}, obtained:{response.raw})")
        # end def check_raw
    # end class GetRawReportStateResponseChecker

    class GetGesturesHandlingOutputResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetGesturesHandlingOutput`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetGesturesHandlingOutputResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.TOUCHPAD.TOUCHPAD_RAW_XY
            return {
                "one_finger_click": (
                    cls.check_one_finger_click, config.F_OneFingerClick),
                "one_finger_tap": (
                    cls.check_one_finger_tap, config.F_OneFingerTap),
                "one_finger_move": (
                    cls.check_one_finger_move, config.F_OneFingerMove),
                "not_defined_gestures": (
                    cls.check_not_defined_gestures, 0),
                "one_finger_click_hold_and_other_fingers_moves": (
                    cls.check_one_finger_click_hold_and_other_fingers_moves,
                    config.F_OneFingerClickHoldAndOtherFingersMoves),
                "one_finger_click_hold_and_move": (
                    cls.check_one_finger_click_hold_and_move, config.F_OneFingerClickHoldAndMove),
                "one_finger_double_click": (
                    cls.check_one_finger_double_click, config.F_OneFingerDoubleClick),
                "one_finger_double_tap": (
                    cls.check_one_finger_double_tap, config.F_OneFingerDoubleTap),
                "two_fingers_tap": (
                    cls.check_two_fingers_tap, config.F_TwoFingersTap),
                "one_finger_double_tap_not_release_the_2nd_tap": (
                    cls.check_one_finger_double_tap_not_release_the_2nd_tap,
                    config.F_OneFingerDoubleTapNotReleaseThe2ndTap),
                "one_finger_on_the_left_corner": (
                    cls.check_one_finger_on_the_left_corner, config.F_OneFingerOnTheLeftCorner),
                "one_finger_on_the_right_corner": (
                    cls.check_one_finger_on_the_right_corner, config.F_OneFingerOnTheRightCorner),
                "three_fingers_tap_and_drag": (
                    cls.check_three_fingers_tap_and_drag, config.F_ThreeFingersTapAndDrag),
                "two_fingers_slide_left_right": (
                    cls.check_two_fingers_slide_left_right, config.F_TwoFingersSlideLeftRight),
                "two_fingers_scroll_up_down": (
                    cls.check_two_fingers_scroll_up_down, config.F_TwoFingersScrollUpDown),
                "two_fingers_click": (
                    cls.check_two_fingers_click, config.F_TwoFingersClick),
                "reserved": (
                    cls.check_reserved, 0),
                "three_fingers_swipe": (
                    cls.check_three_fingers_swipe, config.F_ThreeFingersSwipe)
            }
        # end def get_default_check_map

        @staticmethod
        def check_one_finger_click(test_case, response, expected):
            """
            Check one_finger_click field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_click),
                msg=f"The one_finger_click parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_click})")
        # end def check_one_finger_click

        @staticmethod
        def check_one_finger_tap(test_case, response, expected):
            """
            Check one_finger_tap field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_tap),
                msg=f"The one_finger_tap parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_tap})")
        # end def check_one_finger_tap

        @staticmethod
        def check_one_finger_move(test_case, response, expected):
            """
            Check one_finger_move field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_move),
                msg=f"The one_finger_move parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_move})")
        # end def check_one_finger_move

        @staticmethod
        def check_not_defined_gestures(test_case, response, expected):
            """
            Check not_defined_gestures field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.not_defined_gestures),
                msg=f"The not_defined_gestures parameter differs "
                    f"(expected:{expected}, obtained:{response.not_defined_gestures})")
        # end def check_not_defined_gestures

        @staticmethod
        def check_one_finger_click_hold_and_other_fingers_moves(test_case, response, expected):
            """
            Check one_finger_click_hold_and_other_fingers_moves field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_click_hold_and_other_fingers_moves),
                msg=f"The one_finger_click_hold_and_other_fingers_moves parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_click_hold_and_other_fingers_moves})")
        # end def check_one_finger_click_hold_and_other_fingers_moves

        @staticmethod
        def check_one_finger_click_hold_and_move(test_case, response, expected):
            """
            Check one_finger_click_hold_and_move field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_click_hold_and_move),
                msg=f"The one_finger_click_hold_and_move parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_click_hold_and_move})")
        # end def check_one_finger_click_hold_and_move

        @staticmethod
        def check_one_finger_double_click(test_case, response, expected):
            """
            Check one_finger_double_click field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_double_click),
                msg=f"The one_finger_double_click parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_double_click})")
        # end def check_one_finger_double_click

        @staticmethod
        def check_one_finger_double_tap(test_case, response, expected):
            """
            Check one_finger_double_tap field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_double_tap),
                msg=f"The one_finger_double_tap parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_double_tap})")
        # end def check_one_finger_double_tap

        @staticmethod
        def check_two_fingers_tap(test_case, response, expected):
            """
            Check two_fingers_tap field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.two_fingers_tap),
                msg=f"The two_fingers_tap parameter differs "
                    f"(expected:{expected}, obtained:{response.two_fingers_tap})")
        # end def check_two_fingers_tap

        @staticmethod
        def check_one_finger_double_tap_not_release_the_2nd_tap(test_case, response, expected):
            """
            Check one_finger_double_tap_not_release_the_2nd_tap field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_double_tap_not_release_the_2nd_tap),
                msg=f"The one_finger_double_tap_not_release_the_2nd_tap parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_double_tap_not_release_the_2nd_tap})")
        # end def check_one_finger_double_tap_not_release_the_2nd_tap

        @staticmethod
        def check_one_finger_on_the_left_corner(test_case, response, expected):
            """
            Check one_finger_on_the_left_corner field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_on_the_left_corner),
                msg=f"The one_finger_on_the_left_corner parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_on_the_left_corner})")
        # end def check_one_finger_on_the_left_corner

        @staticmethod
        def check_one_finger_on_the_right_corner(test_case, response, expected):
            """
            Check one_finger_on_the_right_corner field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.one_finger_on_the_right_corner),
                msg=f"The one_finger_on_the_right_corner parameter differs "
                    f"(expected:{expected}, obtained:{response.one_finger_on_the_right_corner})")
        # end def check_one_finger_on_the_right_corner

        @staticmethod
        def check_three_fingers_tap_and_drag(test_case, response, expected):
            """
            Check three_fingers_tap_and_drag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.three_fingers_tap_and_drag),
                msg=f"The three_fingers_tap_and_drag parameter differs "
                    f"(expected:{expected}, obtained:{response.three_fingers_tap_and_drag})")
        # end def check_three_fingers_tap_and_drag

        @staticmethod
        def check_two_fingers_slide_left_right(test_case, response, expected):
            """
            Check two_fingers_slide_left_right field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.two_fingers_slide_left_right),
                msg=f"The two_fingers_slide_left_right parameter differs "
                    f"(expected:{expected}, obtained:{response.two_fingers_slide_left_right})")
        # end def check_two_fingers_slide_left_right

        @staticmethod
        def check_two_fingers_scroll_up_down(test_case, response, expected):
            """
            Check two_fingers_scroll_up_down field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.two_fingers_scroll_up_down),
                msg=f"The two_fingers_scroll_up_down parameter differs "
                    f"(expected:{expected}, obtained:{response.two_fingers_scroll_up_down})")
        # end def check_two_fingers_scroll_up_down

        @staticmethod
        def check_two_fingers_click(test_case, response, expected):
            """
            Check two_fingers_click field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.two_fingers_click),
                msg=f"The two_fingers_click parameter differs "
                    f"(expected:{expected}, obtained:{response.two_fingers_click})")
        # end def check_two_fingers_click

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved

        @staticmethod
        def check_three_fingers_swipe(test_case, response, expected):
            """
            Check three_fingers_swipe field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGesturesHandlingOutputResponse to check
            :type response: ``GetGesturesHandlingOutputResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.three_fingers_swipe),
                msg=f"The three_fingers_swipe parameter differs "
                    f"(expected:{expected}, obtained:{response.three_fingers_swipe})")
        # end def check_three_fingers_swipe
    # end class GetGesturesHandlingOutputResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=TouchpadRawXY.FEATURE_ID, factory=TouchpadRawXYFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_touchpad_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetTouchpadInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetTouchpadInfoResponse
            :rtype: ``GetTouchpadInfoResponse``
            """
            feature_6100_index, feature_6100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_6100.get_touchpad_info_cls(
                device_index=device_index,
                feature_index=feature_6100_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
                response_class_type=feature_6100.get_touchpad_info_response_cls)
            return response
        # end def get_touchpad_info

        @classmethod
        def get_raw_report_state(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetRawReportState``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetRawReportStateResponse
            :rtype: ``GetRawReportStateResponse``
            """
            feature_6100_index, feature_6100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_6100.get_raw_report_state_cls(
                device_index=device_index,
                feature_index=feature_6100_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
                response_class_type=feature_6100.get_raw_report_state_response_cls)
            return response
        # end def get_raw_report_state

        @classmethod
        def set_raw_report_state(cls, test_case, width_height_bytes=0, major_minor=0, native_gesture=0, width_height=0,
                                 enhanced=0, force_data=0, raw=0, device_index=None, port_index=None):
            """
            Process ``SetRawReportState``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

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
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRawReportStateResponse
            :rtype: ``SetRawReportStateResponse``
            """
            feature_6100_index, feature_6100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_6100.set_raw_report_state_cls(
                device_index=device_index,
                feature_index=feature_6100_index,
                width_height_bytes=width_height_bytes,
                major_minor=major_minor,
                native_gesture=native_gesture,
                width_height=width_height,
                enhanced=enhanced,
                force_data=force_data,
                raw=raw)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
                response_class_type=feature_6100.set_raw_report_state_response_cls)
            return response
        # end def set_raw_report_state

        @classmethod
        def get_gestures_handling_output(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetGesturesHandlingOutput``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetGesturesHandlingOutputResponse
            :rtype: ``GetGesturesHandlingOutputResponse``
            """
            feature_6100_index, feature_6100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_6100.get_gestures_handling_output_cls(
                device_index=device_index,
                feature_index=feature_6100_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
                response_class_type=feature_6100.get_gestures_handling_output_response_cls)
            return response
        # end def get_gestures_handling_output

        @classmethod
        def set_gestures_handling_output(cls, test_case, one_finger_click=1, one_finger_tap=1, one_finger_move=1,
                                         not_defined_gestures=0, one_finger_click_hold_and_other_fingers_moves=1,
                                         one_finger_click_hold_and_move=1, one_finger_double_click=1,
                                         one_finger_double_tap=1, two_fingers_tap=3,
                                         one_finger_double_tap_not_release_the_2nd_tap=1,
                                         one_finger_on_the_left_corner=2, one_finger_on_the_right_corner=2,
                                         three_fingers_tap_and_drag=0, two_fingers_slide_left_right=3,
                                         two_fingers_scroll_up_down=3, two_fingers_click=3, three_fingers_swipe=0,
                                         device_index=None, port_index=None):
            """
            Process ``SetGesturesHandlingOutput``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
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
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetGesturesHandlingOutputResponse
            :rtype: ``SetGesturesHandlingOutputResponse``
            """
            feature_6100_index, feature_6100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_6100.set_gestures_handling_output_cls(
                device_index=device_index,
                feature_index=feature_6100_index,
                one_finger_click=one_finger_click,
                one_finger_tap=one_finger_tap,
                one_finger_move=one_finger_move,
                not_defined_gestures=not_defined_gestures,
                one_finger_click_hold_and_other_fingers_moves=one_finger_click_hold_and_other_fingers_moves,
                one_finger_click_hold_and_move=one_finger_click_hold_and_move,
                one_finger_double_click=one_finger_double_click,
                one_finger_double_tap=one_finger_double_tap,
                two_fingers_tap=two_fingers_tap,
                one_finger_double_tap_not_release_the_2nd_tap=one_finger_double_tap_not_release_the_2nd_tap,
                one_finger_on_the_left_corner=one_finger_on_the_left_corner,
                one_finger_on_the_right_corner=one_finger_on_the_right_corner,
                three_fingers_tap_and_drag=three_fingers_tap_and_drag,
                two_fingers_slide_left_right=two_fingers_slide_left_right,
                two_fingers_scroll_up_down=two_fingers_scroll_up_down,
                two_fingers_click=two_fingers_click,
                three_fingers_swipe=three_fingers_swipe)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
                response_class_type=feature_6100.set_gestures_handling_output_response_cls)
            return response
        # end def set_gestures_handling_output

        @classmethod
        def dual_xy_data_event(cls, test_case, timeout=2,
                               check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``DualXYDataEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: DualXYDataEvent
            :rtype: ``DualXYDataEvent``
            """
            _, feature_6100, _, _ = cls.get_parameters(test_case)
            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_6100.dual_xy_data_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def dual_xy_data_event
    # end class HIDppHelper
# end class TouchpadRawXYTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
