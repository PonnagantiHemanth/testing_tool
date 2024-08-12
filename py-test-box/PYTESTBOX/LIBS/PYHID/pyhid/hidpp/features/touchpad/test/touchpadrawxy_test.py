#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.touchpad.test.touchpadrawxy_test
:brief: HID++ 2.0 ``TouchpadRawXY`` test module
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.touchpad.touchpadrawxy import DualXYDataEvent
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetGesturesHandlingOutput
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetGesturesHandlingOutputResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetRawReportState
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetRawReportStateResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetTouchpadInfo
from pyhid.hidpp.features.touchpad.touchpadrawxy import GetTouchpadInfoResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import SetGesturesHandlingOutput
from pyhid.hidpp.features.touchpad.touchpadrawxy import SetGesturesHandlingOutputResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import SetRawReportState
from pyhid.hidpp.features.touchpad.touchpadrawxy import SetRawReportStateResponse
from pyhid.hidpp.features.touchpad.touchpadrawxy import TouchpadRawXY
from pyhid.hidpp.features.touchpad.touchpadrawxy import TouchpadRawXYFactory
from pyhid.hidpp.features.touchpad.touchpadrawxy import TouchpadRawXYV1
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TouchpadRawXYInstantiationTestCase(TestCase):
    """
    Test ``TouchpadRawXY`` testing classes instantiations
    """

    @staticmethod
    def test_touchpad_raw_xy():
        """
        Test ``TouchpadRawXY`` class instantiation
        """
        my_class = TouchpadRawXY(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = TouchpadRawXY(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_touchpad_raw_xy

    @staticmethod
    def test_get_touchpad_info():
        """
        Test ``GetTouchpadInfo`` class instantiation
        """
        my_class = GetTouchpadInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetTouchpadInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_touchpad_info

    @staticmethod
    def test_get_touchpad_info_response():
        """
        Test ``GetTouchpadInfoResponse`` class instantiation
        """
        my_class = GetTouchpadInfoResponse(device_index=0, feature_index=0,
                                           x_size=0,
                                           y_size=0,
                                           z_data_range=0,
                                           area_data_range=0,
                                           timestamp_units=0,
                                           max_finger_count=0,
                                           origin=0,
                                           pen_support=0,
                                           raw_report_mapping_version=0,
                                           dpi=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetTouchpadInfoResponse(device_index=0xff, feature_index=0xff,
                                           x_size=0xffff,
                                           y_size=0xffff,
                                           z_data_range=0xff,
                                           area_data_range=0xff,
                                           timestamp_units=0xff,
                                           max_finger_count=0xff,
                                           origin=0xff,
                                           pen_support=0xff,
                                           raw_report_mapping_version=0xff,
                                           dpi=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_touchpad_info_response

    @staticmethod
    def test_get_raw_report_state():
        """
        Test ``GetRawReportState`` class instantiation
        """
        my_class = GetRawReportState(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRawReportState(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_raw_report_state

    @staticmethod
    def test_get_raw_report_state_response():
        """
        Test ``GetRawReportStateResponse`` class instantiation
        """
        my_class = GetRawReportStateResponse(device_index=0, feature_index=0,
                                             width_height_bytes=False,
                                             major_minor=False,
                                             native_gesture=False,
                                             width_height=False,
                                             enhanced=False,
                                             force_data=False,
                                             raw=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRawReportStateResponse(device_index=0xff, feature_index=0xff,
                                             width_height_bytes=True,
                                             major_minor=True,
                                             native_gesture=True,
                                             width_height=True,
                                             enhanced=True,
                                             force_data=True,
                                             raw=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_raw_report_state_response

    @staticmethod
    def test_set_raw_report_state():
        """
        Test ``SetRawReportState`` class instantiation
        """
        my_class = SetRawReportState(device_index=0, feature_index=0,
                                     width_height_bytes=False,
                                     major_minor=False,
                                     native_gesture=False,
                                     width_height=False,
                                     enhanced=False,
                                     force_data=False,
                                     raw=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRawReportState(device_index=0xff, feature_index=0xff,
                                     width_height_bytes=True,
                                     major_minor=True,
                                     native_gesture=True,
                                     width_height=True,
                                     enhanced=True,
                                     force_data=True,
                                     raw=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_raw_report_state

    @staticmethod
    def test_set_raw_report_state_response():
        """
        Test ``SetRawReportStateResponse`` class instantiation
        """
        my_class = SetRawReportStateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRawReportStateResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_raw_report_state_response

    @staticmethod
    def test_get_gestures_handling_output():
        """
        Test ``GetGesturesHandlingOutput`` class instantiation
        """
        my_class = GetGesturesHandlingOutput(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetGesturesHandlingOutput(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_gestures_handling_output

    @staticmethod
    def test_get_gestures_handling_output_response():
        """
        Test ``GetGesturesHandlingOutputResponse`` class instantiation
        """
        my_class = GetGesturesHandlingOutputResponse(device_index=0, feature_index=0,
                                                     one_finger_click=0,
                                                     one_finger_tap=0,
                                                     one_finger_move=0,
                                                     not_defined_gestures=0,
                                                     one_finger_click_hold_and_other_fingers_moves=0,
                                                     one_finger_click_hold_and_move=0,
                                                     one_finger_double_click=0,
                                                     one_finger_double_tap=0,
                                                     two_fingers_tap=0,
                                                     one_finger_double_tap_not_release_the_2nd_tap=0,
                                                     one_finger_on_the_left_corner=0,
                                                     one_finger_on_the_right_corner=0,
                                                     three_fingers_tap_and_drag=0,
                                                     two_fingers_slide_left_right=0,
                                                     two_fingers_scroll_up_down=0,
                                                     two_fingers_click=0,
                                                     three_fingers_swipe=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetGesturesHandlingOutputResponse(device_index=0xff, feature_index=0xff,
                                                     one_finger_click=0x3,
                                                     one_finger_tap=0x3,
                                                     one_finger_move=0x3,
                                                     not_defined_gestures=0x3,
                                                     one_finger_click_hold_and_other_fingers_moves=0x3,
                                                     one_finger_click_hold_and_move=0x3,
                                                     one_finger_double_click=0x3,
                                                     one_finger_double_tap=0x3,
                                                     two_fingers_tap=0x3,
                                                     one_finger_double_tap_not_release_the_2nd_tap=0x3,
                                                     one_finger_on_the_left_corner=0x3,
                                                     one_finger_on_the_right_corner=0x3,
                                                     three_fingers_tap_and_drag=0x3,
                                                     two_fingers_slide_left_right=0x3,
                                                     two_fingers_scroll_up_down=0x3,
                                                     two_fingers_click=0x3,
                                                     three_fingers_swipe=0x3)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_gestures_handling_output_response

    @staticmethod
    def test_set_gestures_handling_output():
        """
        Test ``SetGesturesHandlingOutput`` class instantiation
        """
        my_class = SetGesturesHandlingOutput(device_index=0, feature_index=0,
                                             one_finger_click=0,
                                             one_finger_tap=0,
                                             one_finger_move=0,
                                             not_defined_gestures=0,
                                             one_finger_click_hold_and_other_fingers_moves=0,
                                             one_finger_click_hold_and_move=0,
                                             one_finger_double_click=0,
                                             one_finger_double_tap=0,
                                             two_fingers_tap=0,
                                             one_finger_double_tap_not_release_the_2nd_tap=0,
                                             one_finger_on_the_left_corner=0,
                                             one_finger_on_the_right_corner=0,
                                             three_fingers_tap_and_drag=0,
                                             two_fingers_slide_left_right=0,
                                             two_fingers_scroll_up_down=0,
                                             two_fingers_click=0,
                                             three_fingers_swipe=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetGesturesHandlingOutput(device_index=0xff, feature_index=0xff,
                                             one_finger_click=0x3,
                                             one_finger_tap=0x3,
                                             one_finger_move=0x3,
                                             not_defined_gestures=0x3,
                                             one_finger_click_hold_and_other_fingers_moves=0x3,
                                             one_finger_click_hold_and_move=0x3,
                                             one_finger_double_click=0x3,
                                             one_finger_double_tap=0x3,
                                             two_fingers_tap=0x3,
                                             one_finger_double_tap_not_release_the_2nd_tap=0x3,
                                             one_finger_on_the_left_corner=0x3,
                                             one_finger_on_the_right_corner=0x3,
                                             three_fingers_tap_and_drag=0x3,
                                             two_fingers_slide_left_right=0x3,
                                             two_fingers_scroll_up_down=0x3,
                                             two_fingers_click=0x3,
                                             three_fingers_swipe=0x3)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_gestures_handling_output

    @staticmethod
    def test_set_gestures_handling_output_response():
        """
        Test ``SetGesturesHandlingOutputResponse`` class instantiation
        """
        my_class = SetGesturesHandlingOutputResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetGesturesHandlingOutputResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_gestures_handling_output_response

    @staticmethod
    def test_dual_xy_data_event():
        """
        Test ``DualXYDataEvent`` class instantiation
        """
        my_class = DualXYDataEvent(device_index=0, feature_index=0,
                                   tstamp=0,
                                   cpt_1=0,
                                   x_1=0,
                                   cts_1=0,
                                   y_1=0,
                                   z1_force_1=0,
                                   area_1=0,
                                   fid_1=0,
                                   btn=False,
                                   sp_1=False,
                                   eof=False,
                                   cpt_2=0,
                                   x_2=0,
                                   cts_2=0,
                                   y_2=0,
                                   z_2_force_2=0,
                                   area_2=0,
                                   fid_2=0,
                                   numfing=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DualXYDataEvent(device_index=0xff, feature_index=0xff,
                                   tstamp=0xffff,
                                   cpt_1=0x3,
                                   x_1=0x3fff,
                                   cts_1=0x3,
                                   y_1=0x3fff,
                                   z1_force_1=0xff,
                                   area_1=0xff,
                                   fid_1=0xf,
                                   btn=True,
                                   sp_1=True,
                                   eof=True,
                                   cpt_2=0x3,
                                   x_2=0x3fff,
                                   cts_2=0x3,
                                   y_2=0x3fff,
                                   z_2_force_2=0xff,
                                   area_2=0xff,
                                   fid_2=0xf,
                                   numfing=0xf)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dual_xy_data_event
# end class TouchpadRawXYInstantiationTestCase


class TouchpadRawXYTestCase(TestCase):
    """
    Test ``TouchpadRawXY`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            TouchpadRawXYV1.VERSION: {
                "cls": TouchpadRawXYV1,
                "interfaces": {
                    "get_touchpad_info_cls": GetTouchpadInfo,
                    "get_touchpad_info_response_cls": GetTouchpadInfoResponse,
                    "get_raw_report_state_cls": GetRawReportState,
                    "get_raw_report_state_response_cls": GetRawReportStateResponse,
                    "set_raw_report_state_cls": SetRawReportState,
                    "set_raw_report_state_response_cls": SetRawReportStateResponse,
                    "get_gestures_handling_output_cls": GetGesturesHandlingOutput,
                    "get_gestures_handling_output_response_cls": GetGesturesHandlingOutputResponse,
                    "set_gestures_handling_output_cls": SetGesturesHandlingOutput,
                    "set_gestures_handling_output_response_cls": SetGesturesHandlingOutputResponse,
                    "dual_xy_data_event_cls": DualXYDataEvent,
                },
                "max_function_index": 4
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``TouchpadRawXYFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(TouchpadRawXYFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``TouchpadRawXYFactory`` using out of range versions
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                TouchpadRawXYFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``TouchpadRawXYFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = TouchpadRawXYFactory.create(version)
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
        """
        for version, expected in self.expected.items():
            obj = TouchpadRawXYFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class TouchpadRawXYTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
