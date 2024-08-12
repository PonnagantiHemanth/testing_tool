#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.test.logimodifiers_test
:brief: HID++ 2.0 ``LogiModifiers`` test module
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.logimodifiers import GetCapabilities
from pyhid.hidpp.features.gaming.logimodifiers import GetCapabilitiesResponse
from pyhid.hidpp.features.gaming.logimodifiers import GetForcedPressedState
from pyhid.hidpp.features.gaming.logimodifiers import GetForcedPressedStateResponse
from pyhid.hidpp.features.gaming.logimodifiers import GetLocallyPressedState
from pyhid.hidpp.features.gaming.logimodifiers import GetLocallyPressedStateResponse
from pyhid.hidpp.features.gaming.logimodifiers import GetPressEvents
from pyhid.hidpp.features.gaming.logimodifiers import GetPressEventsResponse
from pyhid.hidpp.features.gaming.logimodifiers import LogiModifiers
from pyhid.hidpp.features.gaming.logimodifiers import LogiModifiersFactory
from pyhid.hidpp.features.gaming.logimodifiers import LogiModifiersV0
from pyhid.hidpp.features.gaming.logimodifiers import PressEvent
from pyhid.hidpp.features.gaming.logimodifiers import SetForcedPressedState
from pyhid.hidpp.features.gaming.logimodifiers import SetForcedPressedStateResponse
from pyhid.hidpp.features.gaming.logimodifiers import SetPressEvents
from pyhid.hidpp.features.gaming.logimodifiers import SetPressEventsResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiModifiersInstantiationTestCase(TestCase):
    """
    Test ``LogiModifiers`` testing classes instantiations
    """

    @staticmethod
    def test_logi_modifiers():
        """
        Test ``LogiModifiers`` class instantiation
        """
        my_class = LogiModifiers(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = LogiModifiers(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_logi_modifiers

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
    def test_get_locally_pressed_state():
        """
        Test ``GetLocallyPressedState`` class instantiation
        """
        my_class = GetLocallyPressedState(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetLocallyPressedState(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_locally_pressed_state

    @staticmethod
    def test_set_forced_pressed_state():
        """
        Test ``SetForcedPressedState`` class instantiation
        """
        my_class = SetForcedPressedState(device_index=0, feature_index=0,
                                         g_shift=0,
                                         fn=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetForcedPressedState(device_index=0xFF, feature_index=0xFF,
                                         g_shift=0x1,
                                         fn=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_forced_pressed_state

    @staticmethod
    def test_set_press_events():
        """
        Test ``SetPressEvents`` class instantiation
        """
        my_class = SetPressEvents(device_index=0, feature_index=0,
                                  g_shift=0,
                                  fn=0,
                                  right_gui=0,
                                  right_alt=0,
                                  right_shift=0,
                                  right_ctrl=0,
                                  left_gui=0,
                                  left_alt=0,
                                  left_shift=0,
                                  left_ctrl=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetPressEvents(device_index=0xFF, feature_index=0xFF,
                                  g_shift=0x1,
                                  fn=0x1,
                                  right_gui=0x1,
                                  right_alt=0x1,
                                  right_shift=0x1,
                                  right_ctrl=0x1,
                                  left_gui=0x1,
                                  left_alt=0x1,
                                  left_shift=0x1,
                                  left_ctrl=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_press_events

    @staticmethod
    def test_get_forced_pressed_state():
        """
        Test ``GetForcedPressedState`` class instantiation
        """
        my_class = GetForcedPressedState(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetForcedPressedState(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_forced_pressed_state

    @staticmethod
    def test_get_press_events():
        """
        Test ``GetPressEvents`` class instantiation
        """
        my_class = GetPressEvents(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetPressEvents(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_press_events

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           gm_g_shift=0,
                                           gm_fn=0,
                                           gm_right_gui=0,
                                           gm_right_alt=0,
                                           gm_right_shift=0,
                                           gm_right_ctrl=0,
                                           gm_left_gui=0,
                                           gm_left_alt=0,
                                           gm_left_shift=0,
                                           gm_left_ctrl=0,
                                           fm_g_shift=0,
                                           fm_fn=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           gm_g_shift=0x1,
                                           gm_fn=0x1,
                                           gm_right_gui=0x1,
                                           gm_right_alt=0x1,
                                           gm_right_shift=0x1,
                                           gm_right_ctrl=0x1,
                                           gm_left_gui=0x1,
                                           gm_left_alt=0x1,
                                           gm_left_shift=0x1,
                                           gm_left_ctrl=0x1,
                                           fm_g_shift=0x1,
                                           fm_fn=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_locally_pressed_state_response():
        """
        Test ``GetLocallyPressedStateResponse`` class instantiation
        """
        my_class = GetLocallyPressedStateResponse(device_index=0, feature_index=0,
                                                  g_shift=0,
                                                  fn=0,
                                                  right_gui=0,
                                                  right_alt=0,
                                                  right_shift=0,
                                                  right_ctrl=0,
                                                  left_gui=0,
                                                  left_alt=0,
                                                  left_shift=0,
                                                  left_ctrl=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetLocallyPressedStateResponse(device_index=0xFF, feature_index=0xFF,
                                                  g_shift=0x1,
                                                  fn=0x1,
                                                  right_gui=0x1,
                                                  right_alt=0x1,
                                                  right_shift=0x1,
                                                  right_ctrl=0x1,
                                                  left_gui=0x1,
                                                  left_alt=0x1,
                                                  left_shift=0x1,
                                                  left_ctrl=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_locally_pressed_state_response

    @staticmethod
    def test_set_forced_pressed_state_response():
        """
        Test ``SetForcedPressedStateResponse`` class instantiation
        """
        my_class = SetForcedPressedStateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetForcedPressedStateResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_forced_pressed_state_response

    @staticmethod
    def test_set_press_events_response():
        """
        Test ``SetPressEventsResponse`` class instantiation
        """
        my_class = SetPressEventsResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPressEventsResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_press_events_response

    @staticmethod
    def test_get_forced_pressed_state_response():
        """
        Test ``GetForcedPressedStateResponse`` class instantiation
        """
        my_class = GetForcedPressedStateResponse(device_index=0, feature_index=0,
                                                 g_shift=0,
                                                 fn=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetForcedPressedStateResponse(device_index=0xFF, feature_index=0xFF,
                                                 g_shift=0x1,
                                                 fn=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_forced_pressed_state_response

    @staticmethod
    def test_get_press_events_response():
        """
        Test ``GetPressEventsResponse`` class instantiation
        """
        my_class = GetPressEventsResponse(device_index=0, feature_index=0,
                                          g_shift=0,
                                          fn=0,
                                          right_gui=0,
                                          right_alt=0,
                                          right_shift=0,
                                          right_ctrl=0,
                                          left_gui=0,
                                          left_alt=0,
                                          left_shift=0,
                                          left_ctrl=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPressEventsResponse(device_index=0xFF, feature_index=0xFF,
                                          g_shift=0x1,
                                          fn=0x1,
                                          right_gui=0x1,
                                          right_alt=0x1,
                                          right_shift=0x1,
                                          right_ctrl=0x1,
                                          left_gui=0x1,
                                          left_alt=0x1,
                                          left_shift=0x1,
                                          left_ctrl=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_press_events_response

    @staticmethod
    def test_press_event():
        """
        Test ``PressEvent`` class instantiation
        """
        my_class = PressEvent(device_index=0, feature_index=0,
                              g_shift=0,
                              fn=0,
                              right_gui=0,
                              right_alt=0,
                              right_shift=0,
                              right_ctrl=0,
                              left_gui=0,
                              left_alt=0,
                              left_shift=0,
                              left_ctrl=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = PressEvent(device_index=0xFF, feature_index=0xFF,
                              g_shift=0x1,
                              fn=0x1,
                              right_gui=0x1,
                              right_alt=0x1,
                              right_shift=0x1,
                              right_ctrl=0x1,
                              left_gui=0x1,
                              left_alt=0x1,
                              left_shift=0x1,
                              left_ctrl=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_press_event
# end class LogiModifiersInstantiationTestCase


class LogiModifiersTestCase(TestCase):
    """
    Test ``LogiModifiers`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            LogiModifiersV0.VERSION: {
                "cls": LogiModifiersV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_locally_pressed_state_cls": GetLocallyPressedState,
                    "get_locally_pressed_state_response_cls": GetLocallyPressedStateResponse,
                    "set_forced_pressed_state_cls": SetForcedPressedState,
                    "set_forced_pressed_state_response_cls": SetForcedPressedStateResponse,
                    "set_press_events_cls": SetPressEvents,
                    "set_press_events_response_cls": SetPressEventsResponse,
                    "get_forced_pressed_state_cls": GetForcedPressedState,
                    "get_forced_pressed_state_response_cls": GetForcedPressedStateResponse,
                    "get_press_events_cls": GetPressEvents,
                    "get_press_events_response_cls": GetPressEventsResponse,
                    "press_event_cls": PressEvent,
                },
                "max_function_index": 5
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``LogiModifiersFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(LogiModifiersFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``LogiModifiersFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                LogiModifiersFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``LogiModifiersFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = LogiModifiersFactory.create(version)
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
            obj = LogiModifiersFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class LogiModifiersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
