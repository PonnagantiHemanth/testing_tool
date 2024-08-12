#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.mousewheelanalyticsutils
:brief: Helpers for ``MouseWheelAnalytics`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetAnalyticsModeResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetCapabilitiesResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetRotationDataResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetWheelModeDataResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalytics
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalyticsFactory
from pyhid.hidpp.features.mouse.mousewheelanalytics import SetAnalyticsModeResponse
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MouseWheelAnalyticsTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``MouseWheelAnalytics`` feature
    """

    class CapabilitiesChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``Capabilities``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.MOUSE_WHEEL_ANALYTICS
            return {
                "reserved": (cls.check_reserved, 0),
                "c_thumbwheel": (cls.check_c_thumbwheel, config.F_ThumbwheelCapability),
                "c_smartshift": (cls.check_c_smartshift, config.F_SmartShiftCapability),
                "c_ratchet_free": (cls.check_c_ratchet_free, config.F_RatchetFreeCapability),
                "c_main_wheel": (cls.check_c_main_wheel, config.F_MainWheelCapability)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MouseWheelAnalytics.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(expected, msg="The reserved shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_c_thumbwheel(test_case, bitmap, expected):
            """
            Check c_thumbwheel field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MouseWheelAnalytics.Capabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert c_thumbwheel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The c_thumbwheel shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.c_thumbwheel),
                msg="The c_thumbwheel parameter differs from the one expected")
        # end def check_c_thumbwheel

        @staticmethod
        def check_c_smartshift(test_case, bitmap, expected):
            """
            Check c_smartshift field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MouseWheelAnalytics.Capabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert c_smartshift that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The c_smartshift shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.c_smartshift),
                msg="The c_smartshift parameter differs from the one expected")
        # end def check_c_smartshift

        @staticmethod
        def check_c_ratchet_free(test_case, bitmap, expected):
            """
            Check c_ratchet_free field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MouseWheelAnalytics.Capabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert c_ratchet_free that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The c_ratchet_free shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.c_ratchet_free),
                msg="The c_ratchet_free parameter differs from the one expected")
        # end def check_c_ratchet_free

        @staticmethod
        def check_c_main_wheel(test_case, bitmap, expected):
            """
            Check c_main_wheel field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MouseWheelAnalytics.Capabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert c_main_wheel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The c_main_wheel shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.c_main_wheel),
                msg="The c_main_wheel parameter differs from the one expected")
        # end def check_c_main_wheel
    # end class CapabilitiesChecker

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.MOUSE_WHEEL_ANALYTICS
            return {
                "capabilities": (cls.check_capabilities,
                                 MouseWheelAnalyticsTestUtils.CapabilitiesChecker.get_default_check_map(test_case)),
                "main_count_per_turn": (cls.check_main_count_per_turn, config.F_MainWheelCountPerTurn),
                "thumbwheel_count_per_turn": (cls.check_thumbwheel_count_per_turn, config.F_ThumbwheelCountPerTurn)
            }
        # end def get_default_check_map

        @staticmethod
        def check_capabilities(test_case, message, expected):
            """
            Check ``capabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MouseWheelAnalyticsTestUtils.CapabilitiesChecker.check_fields(
                test_case, message.capabilities, MouseWheelAnalytics.Capabilities, expected)
        # end def check_capabilities

        @staticmethod
        def check_main_count_per_turn(test_case, response, expected):
            """
            Check main_count_per_turn field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``str | int``

            :raise ``AssertionError``: Assert main_count_per_turn that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The main_count_per_turn shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=int(expected),
                obtained=to_int(response.main_count_per_turn),
                msg="The main_count_per_turn parameter differs from the one expected")
        # end def check_main_count_per_turn

        @staticmethod
        def check_thumbwheel_count_per_turn(test_case, response, expected):
            """
            Check thumbwheel_count_per_turn field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``AssertionError``: Assert thumbwheel_count_per_turn that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The thumbwheel_count_per_turn shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=int(expected),
                obtained=to_int(response.thumbwheel_count_per_turn),
                msg="The thumbwheel_count_per_turn parameter differs from the one expected")
        # end def check_thumbwheel_count_per_turn
    # end class GetCapabilitiesResponseChecker

    class GetAnalyticsModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetAnalyticsModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reporting_mode": (cls.check_reporting_mode, MouseWheelAnalytics.AnalyticsMode.OFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reporting_mode(test_case, response, expected):
            """
            Check reporting_mode field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetAnalyticsModeResponse to check
            :type response: ``GetAnalyticsModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reporting_mode that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reporting_mode shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reporting_mode),
                msg="The reporting_mode parameter differs from the one expected")
        # end def check_reporting_mode
    # end class GetAnalyticsModeResponseChecker

    class SetAnalyticsModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetAnalyticsModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reporting_mode": (cls.check_reporting_mode, MouseWheelAnalytics.AnalyticsMode.OFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reporting_mode(test_case, response, expected):
            """
            Check reporting_mode field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetAnalyticsModeResponse to check
            :type response: ``SetAnalyticsModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reporting_mode that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reporting_mode shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reporting_mode),
                msg="The reporting_mode parameter differs from the one expected")
        # end def check_reporting_mode
    # end class SetAnalyticsModeResponseChecker

    class GetRotationDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetRotationDataResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "acc_pos_wheel": (cls.check_acc_pos_wheel, 0),
                "acc_neg_wheel": (cls.check_acc_neg_wheel, 0),
                "acc_pos_thumbwheel": (cls.check_acc_pos_thumbwheel, 0),
                "acc_neg_thumbwheel": (cls.check_acc_neg_thumbwheel, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_acc_pos_wheel(test_case, response, expected):
            """
            Check acc_pos_wheel field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRotationDataResponse to check
            :type response: ``GetRotationDataResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert acc_pos_wheel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The acc_pos_wheel shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.acc_pos_wheel),
                msg="The acc_pos_wheel parameter differs from the one expected")
        # end def check_acc_pos_wheel

        @staticmethod
        def check_acc_neg_wheel(test_case, response, expected):
            """
            Check acc_neg_wheel field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRotationDataResponse to check
            :type response: ``GetRotationDataResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert acc_neg_wheel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The acc_neg_wheel shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.acc_neg_wheel),
                msg="The acc_neg_wheel parameter differs from the one expected")
        # end def check_acc_neg_wheel

        @staticmethod
        def check_acc_pos_thumbwheel(test_case, response, expected):
            """
            Check acc_pos_thumbwheel field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRotationDataResponse to check
            :type response: ``GetRotationDataResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert acc_pos_thumbwheel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The acc_pos_thumbwheel shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.acc_pos_thumbwheel),
                msg="The acc_pos_thumbwheel parameter differs from the one expected")
        # end def check_acc_pos_thumbwheel

        @staticmethod
        def check_acc_neg_thumbwheel(test_case, response, expected):
            """
            Check acc_neg_thumbwheel field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRotationDataResponse to check
            :type response: ``GetRotationDataResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert acc_neg_thumbwheel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The acc_neg_thumbwheel shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.acc_neg_thumbwheel),
                msg="The acc_neg_thumbwheel parameter differs from the one expected")
        # end def check_acc_neg_thumbwheel
    # end class GetRotationDataResponseChecker

    class GetWheelModeDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetWheelModeDataResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "ratchet_to_free_wheel_count": (cls.check_ratchet_to_free_wheel_count, 0),
                "free_wheel_to_ratchet_count": (cls.check_free_wheel_to_ratchet_count, 0),
                "smart_shift_count": (cls.check_smart_shift_count, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_ratchet_to_free_wheel_count(test_case, response, expected):
            """
            Check ratchet_to_free_wheel_count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetWheelModeDataResponse to check
            :type response: ``GetWheelModeDataResponse``
            :param expected: Expected value
            :type expected: ``HexList | int``

            :raise ``AssertionError``: Assert ratchet_to_free_wheel_count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The ratchet_to_free_wheel_count shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.ratchet_to_free_wheel_count),
                msg="The ratchet_to_free_wheel_count parameter differs from the one expected")
        # end def check_ratchet_to_free_wheel_count

        @staticmethod
        def check_free_wheel_to_ratchet_count(test_case, response, expected):
            """
            Check free_wheel_to_ratchet_count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetWheelModeDataResponse to check
            :type response: ``GetWheelModeDataResponse``
            :param expected: Expected value
            :type expected: ``HexList | int``

            :raise ``AssertionError``: Assert free_wheel_to_ratchet_count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The free_wheel_to_ratchet_count shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.free_wheel_to_ratchet_count),
                msg="The free_wheel_to_ratchet_count parameter differs from the one expected")
        # end def check_free_wheel_to_ratchet_count

        @staticmethod
        def check_smart_shift_count(test_case, response, expected):
            """
            Check smart_shift_count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetWheelModeDataResponse to check
            :type response: ``GetWheelModeDataResponse``
            :param expected: Expected value
            :type expected: ``HexList | int``

            :raise ``AssertionError``: Assert smart_shift_count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The smart_shift_count shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.smart_shift_count),
                msg="The smart_shift_count parameter differs from the one expected")
        # end def check_smart_shift_count
    # end class GetWheelModeDataResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=MouseWheelAnalytics.FEATURE_ID,
                           factory=MouseWheelAnalyticsFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetCapabilitiesResponse
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2251.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def get_analytics_mode(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetAnalyticsMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetAnalyticsModeResponse
            :rtype: ``GetAnalyticsModeResponse``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_analytics_mode_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2251.get_analytics_mode_response_cls)
        # end def get_analytics_mode

        @classmethod
        def get_analytics_mode_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetAnalyticsMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_analytics_mode_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_analytics_mode_and_check_error

        @classmethod
        def set_analytics_mode(cls, test_case, reporting_mode, device_index=None, port_index=None, software_id=None,
                               padding=None):
            """
            Process ``SetAnalyticsMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param reporting_mode: The reporting mode to be set
            :type reporting_mode: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetAnalyticsModeResponse
            :rtype: ``SetAnalyticsModeResponse``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.set_analytics_mode_cls(
                device_index=device_index,
                feature_index=feature_2251_index,
                reporting_mode=HexList(reporting_mode))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2251.set_analytics_mode_response_cls)
        # end def set_analytics_mode

        @classmethod
        def set_analytics_mode_and_check_error(
                cls, test_case, error_codes, reporting_mode, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``SetAnalyticsMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param reporting_mode: Reporting_Mode
            :type reporting_mode: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.set_analytics_mode_cls(
                device_index=device_index,
                feature_index=feature_2251_index,
                reporting_mode=HexList(reporting_mode))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_analytics_mode_and_check_error

        @classmethod
        def get_rotation_data(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetRotationData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetRotationDataResponse
            :rtype: ``GetRotationDataResponse``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_rotation_data_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2251.get_rotation_data_response_cls)
        # end def get_rotation_data

        @classmethod
        def get_rotation_data_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetRotationData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_rotation_data_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_rotation_data_and_check_error

        @classmethod
        def get_wheel_mode_data(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetWheelModeData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetWheelModeDataResponse
            :rtype: ``GetWheelModeDataResponse``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_wheel_mode_data_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2251.get_wheel_mode_data_response_cls)
        # end def get_wheel_mode_data

        @classmethod
        def get_wheel_mode_data_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetWheelModeData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_2251_index, feature_2251, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2251.get_wheel_mode_data_cls(
                device_index=device_index,
                feature_index=feature_2251_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_wheel_mode_data_and_check_error
    # end class HIDppHelper

    @classmethod
    def scrolls_to_acc_motion_value(cls, test_case, scrolls, wheel_type):
        """
        Convert scroll action to accumulated motion value (for Main wheel and Thumbwheel)

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param scrolls: The number of scrolls done
        :type scrolls: ``int``
        :param wheel_type: The type of scroll wheel (Main wheel or Thumbwheel)
        :type wheel_type: ``MouseWheelAnalytics.Wheel``

        :return: The accumulated wheel motion value
        :rtype: ``HexList``
        """
        if wheel_type == MouseWheelAnalytics.Wheel.MAIN_WHEEL:
            main_wheel_count_per_turn = int(test_case.config.F_MainWheelCountPerTurn)
            return HexList(Numeral(source=scrolls * main_wheel_count_per_turn, byteCount=8))
        elif wheel_type == MouseWheelAnalytics.Wheel.THUMBWHEEL:
            thumbwheel_count_per_turn = int(test_case.config.F_ThumbwheelCountPerTurn)
            return HexList(Numeral(source=scrolls * thumbwheel_count_per_turn, byteCount=8))
        # end if
    # end def scrolls_to_acc_motion_value

    @classmethod
    def smart_shift_key_connected(cls, test_case):
        """
        Check if Smart Shift key is connected in test setup

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        """
        if KEY_ID.SMART_SHIFT in test_case.button_stimuli_emulator.get_key_id_list():
            return True
        else:
            warnings.warn("KEY_ID.SMART_SHIFT not available in test setup, skipping steps related to smart shift key "
                          "press")
            return False
        # end if
    # end def smart_shift_key_connected
# end class MouseWheelAnalyticsTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
