#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.test.monitormode_test
:brief: HID++ 2.0 ``MonitorMode`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import MonitorModeBroadcastEvent
from pyhid.hidpp.features.common.staticmonitormode import SetMonitorMode
from pyhid.hidpp.features.common.staticmonitormode import SetMonitorModeResponse
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorMode
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorModeFactory
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorModeV0
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorModeV1
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import MouseModeEvent


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class StaticMonitorModeInstantiationTestCase(TestCase):
    """
    Test ``StaticMonitorMode`` testing classes instantiations
    """

    @staticmethod
    def test_static_monitor_mode():
        """
        Test ``StaticMonitorMode`` class instantiation
        """
        my_class = StaticMonitorMode(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = StaticMonitorMode(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_static_monitor_mode

    @staticmethod
    def test_set_monitor_mode():
        """
        Test ``SetMonitorMode`` class instantiation
        """
        my_class = SetMonitorMode(device_index=0, feature_index=0,
                                  mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetMonitorMode(device_index=0xFF, feature_index=0xFF,
                                  mode=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_monitor_mode

    @staticmethod
    def test_set_monitor_mode_response():
        """
        Test ``SetMonitorModeResponse`` class instantiation
        """
        my_class = SetMonitorModeResponse(device_index=0, feature_index=0,
                                          mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetMonitorModeResponse(device_index=0xFF, feature_index=0xFF,
                                          mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_monitor_mode_response

    @staticmethod
    def test_monitor_mode_broadcast_event():
        """
        Test ``MonitorModeBroadcastEvent`` class instantiation
        """
        my_class = MonitorModeBroadcastEvent(device_index=0, feature_index=0,
                                             mode_specific_monitor_report=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = MonitorModeBroadcastEvent(
            device_index=0xFF, feature_index=0xFF,
            mode_specific_monitor_report=HexList("FF" * (
                MonitorModeBroadcastEvent.LEN.MODE_SPECIFIC_MONITOR_REPORT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_monitor_mode_broadcast_event

    @staticmethod
    def test_keyboard_mode_event():
        """
        Test ``KeyboardModeEvent`` class instantiation
        """
        my_class = KeyboardModeEvent(device_index=0, feature_index=0,
                                     row_col_code=0,
                                     break_or_make_info=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = KeyboardModeEvent(device_index=0xFF, feature_index=0xFF,
                                     row_col_code=0xFF,
                                     break_or_make_info=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_keyboard_mode_event

    @staticmethod
    def test_mouse_mode_event():
        """
        Test ``MouseModeEvent`` class instantiation
        """
        my_class = MouseModeEvent(device_index=0, feature_index=0,
                                  x_value=0,
                                  y_value=0,
                                  tilt_left_or_right_analog_value=0,
                                  back_and_forward_analog_values=0,
                                  roller_value=0,
                                  time_between_ratchets=0,
                                  switches=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = MouseModeEvent(device_index=0xFF, feature_index=0xFF,
                                  x_value=0xFFFF,
                                  y_value=0xFFFF,
                                  tilt_left_or_right_analog_value=0xFF,
                                  back_and_forward_analog_values=0xFF,
                                  roller_value=0xFF,
                                  time_between_ratchets=0xFF,
                                  switches=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_mouse_mode_event

    @staticmethod
    def test_enhanced_keyboard_mode_event():
        """
        Test ``EnhancedKeyboardModeEvent`` class instantiation
        """
        my_class = EnhancedKeyboardModeEvent(device_index=0, feature_index=0,
                                             row_col_code_0=0,
                                             row_col_code_1=0,
                                             row_col_code_2=0,
                                             row_col_code_3=0,
                                             row_col_code_4=0,
                                             row_col_code_5=0,
                                             row_col_code_6=0,
                                             row_col_code_7=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EnhancedKeyboardModeEvent(device_index=0xFF, feature_index=0xFF,
                                             row_col_code_0=0xFF,
                                             row_col_code_1=0xFF,
                                             row_col_code_2=0xFF,
                                             row_col_code_3=0xFF,
                                             row_col_code_4=0xFF,
                                             row_col_code_5=0xFF,
                                             row_col_code_6=0xFF,
                                             row_col_code_7=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_enhanced_keyboard_mode_event

    @staticmethod
    def test_keyboard_with_larger_matrix_mode_event_v1():
        """
        Test ``KeyboardWithLargerMatrixModeEvent`` class instantiation
        """
        my_class = KeyboardWithLargerMatrixModeEvent(device_index=0, feature_index=0,
                                                     row_code=0,
                                                     col_code=0,
                                                     break_or_make_info=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = KeyboardWithLargerMatrixModeEvent(device_index=0xFF, feature_index=0xFF,
                                                     row_code=0xFF,
                                                     col_code=0xFF,
                                                     break_or_make_info=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_keyboard_with_larger_matrix_mode_event_v1

    @staticmethod
    def test_enhanced_keyboard_with_larger_matrix_mode_event_v1():
        """
        Test ``EnhancedKeyboardWithLargerMatrixModeEvent`` class instantiation
        """
        my_class = EnhancedKeyboardWithLargerMatrixModeEvent(device_index=0, feature_index=0,
                                                             row_code_0=0,
                                                             col_code_0=0,
                                                             row_code_1=0,
                                                             col_code_1=0,
                                                             row_code_2=0,
                                                             col_code_2=0,
                                                             row_code_3=0,
                                                             col_code_3=0,
                                                             row_code_4=0,
                                                             col_code_4=0,
                                                             row_code_5=0,
                                                             col_code_5=0,
                                                             row_code_6=0,
                                                             col_code_6=0,
                                                             row_code_7=0,
                                                             col_code_7=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EnhancedKeyboardWithLargerMatrixModeEvent(device_index=0xFF, feature_index=0xFF,
                                                             row_code_0=0xFF,
                                                             col_code_0=0xFF,
                                                             row_code_1=0xFF,
                                                             col_code_1=0xFF,
                                                             row_code_2=0xFF,
                                                             col_code_2=0xFF,
                                                             row_code_3=0xFF,
                                                             col_code_3=0xFF,
                                                             row_code_4=0xFF,
                                                             col_code_4=0xFF,
                                                             row_code_5=0xFF,
                                                             col_code_5=0xFF,
                                                             row_code_6=0xFF,
                                                             col_code_6=0xFF,
                                                             row_code_7=0xFF,
                                                             col_code_7=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_enhanced_keyboard_with_larger_matrix_mode_event_v1
# end class StaticMonitorModeInstantiationTestCase


class StaticMonitorModeTestCase(TestCase):
    """
    Test ``StaticMonitorMode`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            StaticMonitorModeV0.VERSION: {
                "cls": StaticMonitorModeV0,
                "interfaces": {
                    "set_monitor_mode_cls": SetMonitorMode,
                    "set_monitor_mode_response_cls": SetMonitorModeResponse,
                    "monitor_mode_broadcast_event_cls": MonitorModeBroadcastEvent,
                },
                "max_function_index": 0
            },
            StaticMonitorModeV1.VERSION: {
                "cls": StaticMonitorModeV1,
                "interfaces": {
                    "set_monitor_mode_cls": SetMonitorMode,
                    "set_monitor_mode_response_cls": SetMonitorModeResponse,
                    "monitor_mode_broadcast_event_cls": MonitorModeBroadcastEvent,
                },
                "max_function_index": 0
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``StaticMonitorModeFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(StaticMonitorModeFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``StaticMonitorModeFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                StaticMonitorModeFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``StaticMonitorModeFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = StaticMonitorModeFactory.create(version)
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
            obj = StaticMonitorModeFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class StaticMonitorModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
