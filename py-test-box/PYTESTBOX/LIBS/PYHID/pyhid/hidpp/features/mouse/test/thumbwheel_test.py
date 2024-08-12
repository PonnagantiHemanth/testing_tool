#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.mouse.test.thumbwheel_test
:brief: HID++ 2.0 ``Thumbwheel`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.mouse.thumbwheel import GetThumbwheelInfo
from pyhid.hidpp.features.mouse.thumbwheel import GetThumbwheelInfoResponse
from pyhid.hidpp.features.mouse.thumbwheel import GetThumbwheelStatus
from pyhid.hidpp.features.mouse.thumbwheel import GetThumbwheelStatusResponse
from pyhid.hidpp.features.mouse.thumbwheel import SetThumbwheelReporting
from pyhid.hidpp.features.mouse.thumbwheel import SetThumbwheelReportingResponse
from pyhid.hidpp.features.mouse.thumbwheel import Thumbwheel
from pyhid.hidpp.features.mouse.thumbwheel import ThumbwheelEvent
from pyhid.hidpp.features.mouse.thumbwheel import ThumbwheelFactory
from pyhid.hidpp.features.mouse.thumbwheel import ThumbwheelV0
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ThumbwheelInstantiationTestCase(TestCase):
    """
    Test ``Thumbwheel`` testing classes instantiations
    """

    @staticmethod
    def test_thumbwheel():
        """
        Test ``Thumbwheel`` class instantiation
        """
        my_class = Thumbwheel(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = Thumbwheel(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_thumbwheel

    @staticmethod
    def test_get_thumbwheel_info():
        """
        Test ``GetThumbwheelInfo`` class instantiation
        """
        my_class = GetThumbwheelInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetThumbwheelInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_thumbwheel_info

    @staticmethod
    def test_get_thumbwheel_info_response():
        """
        Test ``GetThumbwheelInfoResponse`` class instantiation
        """
        my_class = GetThumbwheelInfoResponse(device_index=0, feature_index=0,
                                             native_resolution=0,
                                             diverted_resolution=0,
                                             default_direction=False,
                                             single_tap_gesture_capability=False,
                                             proximity_capability=False,
                                             touch_capability=False,
                                             time_stamp_capability=False,
                                             time_unit=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetThumbwheelInfoResponse(device_index=0xff, feature_index=0xff,
                                             native_resolution=0xffff,
                                             diverted_resolution=0xffff,
                                             default_direction=True,
                                             single_tap_gesture_capability=True,
                                             proximity_capability=True,
                                             touch_capability=True,
                                             time_stamp_capability=True,
                                             time_unit=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_thumbwheel_info_response

    @staticmethod
    def test_get_thumbwheel_status():
        """
        Test ``GetThumbwheelStatus`` class instantiation
        """
        my_class = GetThumbwheelStatus(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetThumbwheelStatus(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_thumbwheel_status

    @staticmethod
    def test_get_thumbwheel_status_response():
        """
        Test ``GetThumbwheelStatusResponse`` class instantiation
        """
        my_class = GetThumbwheelStatusResponse(device_index=0, feature_index=0,
                                               reporting_mode=0,
                                               proxy=False,
                                               touch=False,
                                               invert_direction=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetThumbwheelStatusResponse(device_index=0xff, feature_index=0xff,
                                               reporting_mode=0xff,
                                               proxy=True,
                                               touch=True,
                                               invert_direction=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_thumbwheel_status_response

    @staticmethod
    def test_set_thumbwheel_reporting():
        """
        Test ``SetThumbwheelReporting`` class instantiation
        """
        my_class = SetThumbwheelReporting(device_index=0, feature_index=0,
                                          reporting_mode=0,
                                          invert_direction=False)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetThumbwheelReporting(device_index=0xff, feature_index=0xff,
                                          reporting_mode=0xff,
                                          invert_direction=True)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_thumbwheel_reporting

    @staticmethod
    def test_set_thumbwheel_reporting_response():
        """
        Test ``SetThumbwheelReportingResponse`` class instantiation
        """
        my_class = SetThumbwheelReportingResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetThumbwheelReportingResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_thumbwheel_reporting_response

    @staticmethod
    def test_thumbwheel_event():
        """
        Test ``ThumbwheelEvent`` class instantiation
        """
        my_class = ThumbwheelEvent(device_index=0, feature_index=0,
                                   rotation=0,
                                   time_stamp=0,
                                   rotation_status=0,
                                   single_tap=False,
                                   proxy=False,
                                   touch=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ThumbwheelEvent(device_index=0xff, feature_index=0xff,
                                   rotation=0xffff,
                                   time_stamp=0xffff,
                                   rotation_status=0xff,
                                   single_tap=True,
                                   proxy=True,
                                   touch=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_thumbwheel_event
# end class ThumbwheelInstantiationTestCase


class ThumbwheelTestCase(TestCase):
    """
    Test ``Thumbwheel`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ThumbwheelV0.VERSION: {
                "cls": ThumbwheelV0,
                "interfaces": {
                    "get_thumbwheel_info_cls": GetThumbwheelInfo,
                    "get_thumbwheel_info_response_cls": GetThumbwheelInfoResponse,
                    "get_thumbwheel_status_cls": GetThumbwheelStatus,
                    "get_thumbwheel_status_response_cls": GetThumbwheelStatusResponse,
                    "set_thumbwheel_reporting_cls": SetThumbwheelReporting,
                    "set_thumbwheel_reporting_response_cls": SetThumbwheelReportingResponse,
                    "thumbwheel_event_cls": ThumbwheelEvent,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ThumbwheelFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ThumbwheelFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ThumbwheelFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                ThumbwheelFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ThumbwheelFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ThumbwheelFactory.create(version)
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
            obj = ThumbwheelFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ThumbwheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
