#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.mouse.test.mousewheelanalytics_test
:brief: HID++ 2.0 ``MouseWheelAnalytics`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2023/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.mouse.mousewheelanalytics import GetAnalyticsMode
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetAnalyticsModeResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetCapabilities
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetCapabilitiesResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetRotationData
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetRotationDataResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetWheelModeData
from pyhid.hidpp.features.mouse.mousewheelanalytics import GetWheelModeDataResponse
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalytics
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalyticsFactory
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalyticsV0
from pyhid.hidpp.features.mouse.mousewheelanalytics import SetAnalyticsMode
from pyhid.hidpp.features.mouse.mousewheelanalytics import SetAnalyticsModeResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MouseWheelAnalyticsInstantiationTestCase(TestCase):
    """
    Test ``MouseWheelAnalytics`` testing classes instantiations
    """

    @staticmethod
    def test_mouse_wheel_analytics():
        """
        Test ``MouseWheelAnalytics`` class instantiation
        """
        my_class = MouseWheelAnalytics(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = MouseWheelAnalytics(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_mouse_wheel_analytics

    @staticmethod
    def test_get_capabilities():
        """
        Test ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_analytics_mode():
        """
        Test ``GetAnalyticsMode`` class instantiation
        """
        my_class = GetAnalyticsMode(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetAnalyticsMode(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_analytics_mode

    @staticmethod
    def test_set_analytics_mode():
        """
        Test ``SetAnalyticsMode`` class instantiation
        """
        my_class = SetAnalyticsMode(device_index=0, feature_index=0,
                                    reporting_mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetAnalyticsMode(device_index=0xFF, feature_index=0xFF,
                                    reporting_mode=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_analytics_mode

    @staticmethod
    def test_get_rotation_data():
        """
        Test ``GetRotationData`` class instantiation
        """
        my_class = GetRotationData(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRotationData(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_rotation_data

    @staticmethod
    def test_get_wheel_mode_data():
        """
        Test ``GetWheelModeData`` class instantiation
        """
        my_class = GetWheelModeData(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetWheelModeData(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_wheel_mode_data

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           c_thumbwheel=False,
                                           c_smartshift=False,
                                           c_ratchet_free=False,
                                           c_main_wheel=False,
                                           main_count_per_turn=HexList(0),
                                           thumbwheel_count_per_turn=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(
            device_index=0xFF, feature_index=0xFF, c_thumbwheel=True, c_smartshift=True, c_ratchet_free=True,
            c_main_wheel=True,
            main_count_per_turn=HexList("FF" * (GetCapabilitiesResponse.LEN.MAIN_COUNT_PER_TURN // 8)),
            thumbwheel_count_per_turn=HexList("FF" * (GetCapabilitiesResponse.LEN.THUMBWHEEL_COUNT_PER_TURN // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_analytics_mode_response():
        """
        Test ``GetAnalyticsModeResponse`` class instantiation
        """
        my_class = GetAnalyticsModeResponse(device_index=0, feature_index=0,
                                            reporting_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAnalyticsModeResponse(device_index=0xFF, feature_index=0xFF,
                                            reporting_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_analytics_mode_response

    @staticmethod
    def test_set_analytics_mode_response():
        """
        Test ``SetAnalyticsModeResponse`` class instantiation
        """
        my_class = SetAnalyticsModeResponse(device_index=0, feature_index=0,
                                            reporting_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetAnalyticsModeResponse(device_index=0xFF, feature_index=0xFF,
                                            reporting_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_analytics_mode_response

    @staticmethod
    def test_get_rotation_data_response():
        """
        Test ``GetRotationDataResponse`` class instantiation
        """
        my_class = GetRotationDataResponse(device_index=0, feature_index=0,
                                           acc_pos_wheel=HexList(0),
                                           acc_neg_wheel=HexList(0),
                                           acc_pos_thumbwheel=HexList(0),
                                           acc_neg_thumbwheel=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRotationDataResponse(
            device_index=0xFF, feature_index=0xFF,
            acc_pos_wheel=HexList("FF" * (GetRotationDataResponse.LEN.ACC_POS_WHEEL // 8)),
            acc_neg_wheel=HexList("FF" * (GetRotationDataResponse.LEN.ACC_NEG_WHEEL // 8)),
            acc_pos_thumbwheel=HexList("FF" * (GetRotationDataResponse.LEN.ACC_POS_THUMBWHEEL // 8)),
            acc_neg_thumbwheel=HexList("FF" * (GetRotationDataResponse.LEN.ACC_NEG_THUMBWHEEL // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_rotation_data_response

    @staticmethod
    def test_get_wheel_mode_data_response():
        """
        Test ``GetWheelModeDataResponse`` class instantiation
        """
        my_class = GetWheelModeDataResponse(device_index=0, feature_index=0,
                                            ratchet_to_free_wheel_count=HexList(0),
                                            free_wheel_to_ratchet_count=HexList(0),
                                            smart_shift_count=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetWheelModeDataResponse(
            device_index=0xFF, feature_index=0xFF,
            ratchet_to_free_wheel_count=HexList("FF" * (GetWheelModeDataResponse.LEN.RATCHET_TO_FREE_WHEEL_COUNT // 8)),
            free_wheel_to_ratchet_count=HexList("FF" * (GetWheelModeDataResponse.LEN.FREE_WHEEL_TO_RATCHET_COUNT // 8)),
            smart_shift_count=HexList("FF" * (GetWheelModeDataResponse.LEN.SMART_SHIFT_COUNT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_wheel_mode_data_response
# end class MouseWheelAnalyticsInstantiationTestCase


class MouseWheelAnalyticsTestCase(TestCase):
    """
    Test ``MouseWheelAnalytics`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            MouseWheelAnalyticsV0.VERSION: {
                "cls": MouseWheelAnalyticsV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_analytics_mode_cls": GetAnalyticsMode,
                    "get_analytics_mode_response_cls": GetAnalyticsModeResponse,
                    "set_analytics_mode_cls": SetAnalyticsMode,
                    "set_analytics_mode_response_cls": SetAnalyticsModeResponse,
                    "get_rotation_data_cls": GetRotationData,
                    "get_rotation_data_response_cls": GetRotationDataResponse,
                    "get_wheel_mode_data_cls": GetWheelModeData,
                    "get_wheel_mode_data_response_cls": GetWheelModeDataResponse,
                },
                "max_function_index": 4
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``MouseWheelAnalyticsFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(MouseWheelAnalyticsFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``MouseWheelAnalyticsFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                MouseWheelAnalyticsFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``MouseWheelAnalyticsFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = MouseWheelAnalyticsFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = MouseWheelAnalyticsFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class MouseWheelAnalyticsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
