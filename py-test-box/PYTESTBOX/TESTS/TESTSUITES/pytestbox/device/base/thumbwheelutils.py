#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.thumbwheelutils
:brief: Helpers for ``Thumbwheel`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.thumbwheel import Thumbwheel
from pyhid.hidpp.features.mouse.thumbwheel import ThumbwheelFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ThumbwheelTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``Thumbwheel`` feature
    """
    DEFAULT_DIR = 0
    INVERTED_DIR = 1

    class DirectionMaskBitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``DirectionMaskBitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.THUMBWHEEL
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "default_direction": (
                    cls.check_default_direction,
                    ThumbwheelTestUtils.DEFAULT_DIR)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: DirectionMaskBitMap to check
            :type bitmap: ``Thumbwheel.DirectionMaskBitMap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_default_direction(test_case, bitmap, expected):
            """
            Check default_direction field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: DirectionMaskBitMap to check
            :type bitmap: ``Thumbwheel.DirectionMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert default_direction that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="DefaultDirection shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.default_direction),
                msg="The default_direction parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.default_direction})")
        # end def check_default_direction
    # end class DirectionMaskBitMapChecker

    class CapabilityMaskBitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``CapabilityMaskBitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.THUMBWHEEL
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "single_tap_gesture_capability": (
                    cls.check_single_tap_gesture_capability,
                    config.F_SingleTapCapability),
                "proximity_capability": (
                    cls.check_proximity_capability,
                    config.F_ProxyCapability),
                "touch_capability": (
                    cls.check_touch_capability,
                    config.F_TouchCapability),
                "time_stamp_capability": (
                    cls.check_time_stamp_capability,
                    config.F_TimeStampCapability)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMaskBitMap to check
            :type bitmap: ``Thumbwheel.CapabilityMaskBitMap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_single_tap_gesture_capability(test_case, bitmap, expected):
            """
            Check single_tap_gesture_capability field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMaskBitMap to check
            :type bitmap: ``Thumbwheel.CapabilityMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert single_tap_gesture_capability that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="SingleTapGestureCapability shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.single_tap_gesture_capability),
                msg="The single_tap_gesture_capability parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.single_tap_gesture_capability})")
        # end def check_single_tap_gesture_capability

        @staticmethod
        def check_proximity_capability(test_case, bitmap, expected):
            """
            Check proximity_capability field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMaskBitMap to check
            :type bitmap: ``Thumbwheel.CapabilityMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert proximity_capability that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ProximityCapability shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.proximity_capability),
                msg="The proximity_capability parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.proximity_capability})")
        # end def check_proximity_capability

        @staticmethod
        def check_touch_capability(test_case, bitmap, expected):
            """
            Check touch_capability field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMaskBitMap to check
            :type bitmap: ``Thumbwheel.CapabilityMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert touch_capability that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="TouchCapability shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.touch_capability),
                msg="The touch_capability parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.touch_capability})")
        # end def check_touch_capability

        @staticmethod
        def check_time_stamp_capability(test_case, bitmap, expected):
            """
            Check time_stamp_capability field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMaskBitMap to check
            :type bitmap: ``Thumbwheel.CapabilityMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert time_stamp_capability that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="TimeStampCapability shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.time_stamp_capability),
                msg="The time_stamp_capability parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.time_stamp_capability})")
        # end def check_time_stamp_capability
    # end class CapabilityMaskBitMapChecker

    class GetThumbwheelInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetThumbwheelInfoResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.THUMBWHEEL
            return {
                "native_resolution": (
                    cls.check_native_resolution,
                    config.F_NativeRes),
                "diverted_resolution": (
                    cls.check_diverted_resolution,
                    config.F_DivertedRes),
                "direction_mask_bit_map": (
                    cls.check_direction_mask_bit_map,
                    ThumbwheelTestUtils.DirectionMaskBitMapChecker.get_default_check_map(test_case)),
                "capability_mask_bit_map": (
                    cls.check_capability_mask_bit_map,
                    ThumbwheelTestUtils.CapabilityMaskBitMapChecker.get_default_check_map(test_case)),
                "time_unit": (
                    cls.check_time_unit,
                    config.F_TimeUnit)
            }
        # end def get_default_check_map

        @staticmethod
        def check_native_resolution(test_case, response, expected):
            """
            Check native_resolution field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetThumbwheelInfoResponse to check
            :type response: ``pyhid.hidpp.features.mouse.thumbwheel.GetThumbwheelInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert native_resolution that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="NativeResolution shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.native_resolution),
                msg="The native_resolution parameter differs "
                    f"(expected:{expected}, obtained:{response.native_resolution})")
        # end def check_native_resolution

        @staticmethod
        def check_diverted_resolution(test_case, response, expected):
            """
            Check diverted_resolution field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetThumbwheelInfoResponse to check
            :type response: ``pyhid.hidpp.features.mouse.thumbwheel.GetThumbwheelInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert diverted_resolution that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="DivertedResolution shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.diverted_resolution),
                msg="The diverted_resolution parameter differs "
                    f"(expected:{expected}, obtained:{response.diverted_resolution})")
        # end def check_diverted_resolution

        @staticmethod
        def check_direction_mask_bit_map(test_case, message, expected):
            """
            Check ``direction_mask_bit_map``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetThumbwheelInfoResponse to check
            :type message: ``pyhid.hidpp.features.mouse.thumbwheel.GetThumbwheelInfoResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ThumbwheelTestUtils.DirectionMaskBitMapChecker.check_fields(
                test_case, message.direction_mask_bit_map, Thumbwheel.DirectionMaskBitMap, expected)
        # end def check_direction_mask_bit_map

        @staticmethod
        def check_capability_mask_bit_map(test_case, message, expected):
            """
            Check ``capability_mask_bit_map``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetThumbwheelInfoResponse to check
            :type message: ``pyhid.hidpp.features.mouse.thumbwheel.GetThumbwheelInfoResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ThumbwheelTestUtils.CapabilityMaskBitMapChecker.check_fields(
                test_case, message.capability_mask_bit_map, Thumbwheel.CapabilityMaskBitMap, expected)
        # end def check_capability_mask_bit_map

        @staticmethod
        def check_time_unit(test_case, response, expected):
            """
            Check time_unit field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetThumbwheelInfoResponse to check
            :type response: ``pyhid.hidpp.features.mouse.thumbwheel.GetThumbwheelInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert time_unit that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="TimeUnit shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.time_unit),
                msg="The time_unit parameter differs "
                    f"(expected:{expected}, obtained:{response.time_unit})")
        # end def check_time_unit
    # end class GetThumbwheelInfoResponseChecker

    class StatusMaskBitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``StatusMaskBitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case=test_case)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, proxy=0, touch=0, invert_dir=0):
            """
            Get check map for different values of proxy, touch and invert_dir

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param proxy: Proximity flag value - OPTIONAL
            :type proxy: ``int``
            :param touch: Touch flag value  - OPTIONAL
            :type touch: ``int``
            :param invert_dir: Invert direction flag value - OPTIONAL
            :type proxy: ``int``

            :return: Check map
            :rtype: ``dict``
            """

            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "proxy": (
                    cls.check_proxy,
                    proxy),
                "touch": (
                    cls.check_touch,
                    touch),
                "invert_direction": (
                    cls.check_invert_direction,
                    invert_dir)
            }
        # end get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: StatusMaskBitMap to check
            :type bitmap: ``Thumbwheel.StatusMaskBitMap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_proxy(test_case, bitmap, expected):
            """
            Check proxy field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: StatusMaskBitMap to check
            :type bitmap: ``Thumbwheel.StatusMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert proxy that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Proxy shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.proxy),
                msg="The proxy parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.proxy})")
        # end def check_proxy

        @staticmethod
        def check_touch(test_case, bitmap, expected):
            """
            Check touch field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: StatusMaskBitMap to check
            :type bitmap: ``Thumbwheel.StatusMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert touch that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Touch shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.touch),
                msg="The touch parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.touch})")
        # end def check_touch

        @staticmethod
        def check_invert_direction(test_case, bitmap, expected):
            """
            Check invert_direction field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: StatusMaskBitMap to check
            :type bitmap: ``Thumbwheel.StatusMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert invert_direction that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="InvertDirection shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.invert_direction),
                msg="The invert_direction parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.invert_direction})")
        # end def check_invert_direction
    # end class StatusMaskBitMapChecker

    class GetThumbwheelStatusResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetThumbwheelStatusResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, proxy=0, touch=0, invert_dir=0):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param proxy: Proximity flag value - OPTIONAL
            :type proxy: ``int``
            :param touch: Touch flag value - OPTIONAL
            :type touch: ``int``
            :param invert_dir: Invert direction flag value - OPTIONAL
            :type proxy: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "reporting_mode": (
                    cls.check_reporting_mode,
                    Thumbwheel.REPORTING_MODE.HID),
                "status_mask_bit_map": (
                    cls.check_status_mask_bit_map,
                    ThumbwheelTestUtils.StatusMaskBitMapChecker.get_check_map(test_case, proxy, touch, invert_dir))
            }
        # end def get_default_check_map

        @staticmethod
        def check_reporting_mode(test_case, response, expected):
            """
            Check reporting_mode field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetThumbwheelStatusResponse to check
            :type response: ``pyhid.hidpp.features.mouse.thumbwheel.GetThumbwheelStatusResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reporting_mode that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ReportingMode shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reporting_mode),
                msg="The reporting_mode parameter differs "
                    f"(expected:{expected}, obtained:{response.reporting_mode})")
        # end def check_reporting_mode

        @staticmethod
        def check_status_mask_bit_map(test_case, message, expected):
            """
            Check ``status_mask_bit_map``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetThumbwheelStatusResponse to check
            :type message: ``pyhid.hidpp.features.mouse.thumbwheel.GetThumbwheelStatusResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ThumbwheelTestUtils.StatusMaskBitMapChecker.check_fields(
                test_case, message.status_mask_bit_map, Thumbwheel.StatusMaskBitMap, expected)
        # end def check_status_mask_bit_map
    # end class GetThumbwheelStatusResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=Thumbwheel.FEATURE_ID, factory=ThumbwheelFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_thumbwheel_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetThumbwheelInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetThumbwheelInfoResponse
            :rtype: ``GetThumbwheelInfoResponse``
            """
            feature_2150_index, feature_2150, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2150.get_thumbwheel_info_cls(
                device_index=device_index,
                feature_index=feature_2150_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2150.get_thumbwheel_info_response_cls)
            return response
        # end def get_thumbwheel_info

        @classmethod
        def get_thumbwheel_status(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetThumbwheelStatus``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetThumbwheelStatusResponse
            :rtype: ``GetThumbwheelStatusResponse``
            """
            feature_2150_index, feature_2150, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2150.get_thumbwheel_status_cls(
                device_index=device_index,
                feature_index=feature_2150_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2150.get_thumbwheel_status_response_cls)
            return response
        # end def get_thumbwheel_status

        @classmethod
        def set_thumbwheel_reporting(cls, test_case, reporting_mode, invert_direction, device_index=None,
                                     port_index=None):
            """
            Process ``SetThumbwheelReporting``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param reporting_mode: Native (HID) = 0 Diverted (HID++) = 1 In Divertedmode, [event0] is sent in HID++
            :type reporting_mode: ``int | HexList``
            :param invert_direction: 1 = invert the rotation direction (relatively to default_dir).
                                         This setting applies in both native and diverted modes
            :type invert_direction: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetThumbwheelReportingResponse
            :rtype: ``SetThumbwheelReportingResponse``
            """
            feature_2150_index, feature_2150, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2150.set_thumbwheel_reporting_cls(
                device_index=device_index,
                feature_index=feature_2150_index,
                reporting_mode=HexList(reporting_mode),
                invert_direction=invert_direction)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2150.set_thumbwheel_reporting_response_cls)
            return response
        # end def set_thumbwheel_reporting

        @classmethod
        def thumbwheel_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                             check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``ThumbwheelEvent``: get notification from event queue

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

            :return: ThumbwheelEvent
            :rtype: ``ThumbwheelEvent``
            """
            _, feature_2150, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_2150.thumbwheel_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def thumbwheel_event
    # end class HIDppHelper
# end class ThumbwheelTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
