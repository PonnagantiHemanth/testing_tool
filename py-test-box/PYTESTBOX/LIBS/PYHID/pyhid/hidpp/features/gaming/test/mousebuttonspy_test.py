#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.test.mousebuttonspy_test
:brief: HID++ 2.0 ``MouseButtonSpy`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.mousebuttonspy import ButtonEvent
from pyhid.hidpp.features.gaming.mousebuttonspy import GetNbOfButtons
from pyhid.hidpp.features.gaming.mousebuttonspy import GetNbOfButtonsResponse
from pyhid.hidpp.features.gaming.mousebuttonspy import GetRemapping
from pyhid.hidpp.features.gaming.mousebuttonspy import GetRemappingResponse
from pyhid.hidpp.features.gaming.mousebuttonspy import MouseButtonSpy
from pyhid.hidpp.features.gaming.mousebuttonspy import MouseButtonSpyFactory
from pyhid.hidpp.features.gaming.mousebuttonspy import MouseButtonSpyV0
from pyhid.hidpp.features.gaming.mousebuttonspy import SetRemapping
from pyhid.hidpp.features.gaming.mousebuttonspy import SetRemappingResponse
from pyhid.hidpp.features.gaming.mousebuttonspy import StartSpy
from pyhid.hidpp.features.gaming.mousebuttonspy import StartSpyResponse
from pyhid.hidpp.features.gaming.mousebuttonspy import StopSpy
from pyhid.hidpp.features.gaming.mousebuttonspy import StopSpyResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MouseButtonSpyInstantiationTestCase(TestCase):
    """
    ``MouseButtonSpy`` testing classes instantiations
    """
    @staticmethod
    def test_mouse_button_spy():
        """
        Tests ``MouseButtonSpy`` class instantiation
        """
        my_class = MouseButtonSpy(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = MouseButtonSpy(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_mouse_button_spy

    @staticmethod
    def test_get_nb_of_buttons():
        """
        Tests ``GetNbOfButtons`` class instantiation
        """
        my_class = GetNbOfButtons(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetNbOfButtons(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_nb_of_buttons

    @staticmethod
    def test_get_nb_of_buttons_response():
        """
        Tests ``GetNbOfButtonsResponse`` class instantiation
        """
        my_class = GetNbOfButtonsResponse(device_index=0, feature_index=0,
                                          nb_buttons=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetNbOfButtonsResponse(device_index=0xff, feature_index=0xff,
                                          nb_buttons=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_nb_of_buttons_response

    @staticmethod
    def test_start_spy():
        """
        Tests ``StartSpy`` class instantiation
        """
        my_class = StartSpy(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StartSpy(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_start_spy

    @staticmethod
    def test_start_spy_response():
        """
        Tests ``StartSpyResponse`` class instantiation
        """
        my_class = StartSpyResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartSpyResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_spy_response

    @staticmethod
    def test_stop_spy():
        """
        Tests ``StopSpy`` class instantiation
        """
        my_class = StopSpy(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StopSpy(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_stop_spy

    @staticmethod
    def test_stop_spy_response():
        """
        Tests ``StopSpyResponse`` class instantiation
        """
        my_class = StopSpyResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StopSpyResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_stop_spy_response

    @staticmethod
    def test_get_remapping():
        """
        Tests ``GetRemapping`` class instantiation
        """
        my_class = GetRemapping(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRemapping(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_remapping

    @staticmethod
    def test_get_remapping_response():
        """
        Tests ``GetRemappingResponse`` class instantiation
        """
        my_class = GetRemappingResponse(device_index=0, feature_index=0,
                                        button_1=0,
                                        button_2=0,
                                        button_3=0,
                                        button_4=0,
                                        button_5=0,
                                        button_6=0,
                                        button_7=0,
                                        button_8=0,
                                        button_9=0,
                                        button_10=0,
                                        button_11=0,
                                        button_12=0,
                                        button_13=0,
                                        button_14=0,
                                        button_15=0,
                                        button_16=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRemappingResponse(device_index=0xff, feature_index=0xff,
                                        button_1=0xff,
                                        button_2=0xff,
                                        button_3=0xff,
                                        button_4=0xff,
                                        button_5=0xff,
                                        button_6=0xff,
                                        button_7=0xff,
                                        button_8=0xff,
                                        button_9=0xff,
                                        button_10=0xff,
                                        button_11=0xff,
                                        button_12=0xff,
                                        button_13=0xff,
                                        button_14=0xff,
                                        button_15=0xff,
                                        button_16=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_remapping_response

    @staticmethod
    def test_set_remapping():
        """
        Tests ``SetRemapping`` class instantiation
        """
        my_class = SetRemapping(device_index=0, feature_index=0,
                                button_1=0,
                                button_2=0,
                                button_3=0,
                                button_4=0,
                                button_5=0,
                                button_6=0,
                                button_7=0,
                                button_8=0,
                                button_9=0,
                                button_10=0,
                                button_11=0,
                                button_12=0,
                                button_13=0,
                                button_14=0,
                                button_15=0,
                                button_16=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRemapping(device_index=0xff, feature_index=0xff,
                                button_1=0xff,
                                button_2=0xff,
                                button_3=0xff,
                                button_4=0xff,
                                button_5=0xff,
                                button_6=0xff,
                                button_7=0xff,
                                button_8=0xff,
                                button_9=0xff,
                                button_10=0xff,
                                button_11=0xff,
                                button_12=0xff,
                                button_13=0xff,
                                button_14=0xff,
                                button_15=0xff,
                                button_16=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_remapping

    @staticmethod
    def test_set_remapping_response():
        """
        Tests ``SetRemappingResponse`` class instantiation
        """
        my_class = SetRemappingResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRemappingResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_remapping_response

    @staticmethod
    def test_button_event():
        """
        Tests ``ButtonEvent`` class instantiation
        """
        my_class = ButtonEvent(device_index=0, feature_index=0,
                               button_1=False,
                               button_2=False,
                               button_3=False,
                               button_4=False,
                               button_5=False,
                               button_6=False,
                               button_7=False,
                               button_8=False,
                               button_9=False,
                               button_10=False,
                               button_11=False,
                               button_12=False,
                               button_13=False,
                               button_14=False,
                               button_15=False,
                               button_16=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ButtonEvent(device_index=0xff, feature_index=0xff,
                               button_1=True,
                               button_2=True,
                               button_3=True,
                               button_4=True,
                               button_5=True,
                               button_6=True,
                               button_7=True,
                               button_8=True,
                               button_9=True,
                               button_10=True,
                               button_11=True,
                               button_12=True,
                               button_13=True,
                               button_14=True,
                               button_15=True,
                               button_16=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_button_event
# end class MouseButtonSpyInstantiationTestCase


class MouseButtonSpyTestCase(TestCase):
    """
    ``MouseButtonSpy`` factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            MouseButtonSpyV0.VERSION: {
                "cls": MouseButtonSpyV0,
                "interfaces": {
                    "get_nb_of_buttons_cls": GetNbOfButtons,
                    "get_nb_of_buttons_response_cls": GetNbOfButtonsResponse,
                    "start_spy_cls": StartSpy,
                    "start_spy_response_cls": StartSpyResponse,
                    "stop_spy_cls": StopSpy,
                    "stop_spy_response_cls": StopSpyResponse,
                    "get_remapping_cls": GetRemapping,
                    "get_remapping_response_cls": GetRemappingResponse,
                    "set_remapping_cls": SetRemapping,
                    "set_remapping_response_cls": SetRemappingResponse,
                    "button_event_cls": ButtonEvent,
                },
                "max_function_index": 4
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Tests ``MouseButtonSpyFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(MouseButtonSpyFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Tests ``MouseButtonSpyFactory`` with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                MouseButtonSpyFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``MouseButtonSpyFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = MouseButtonSpyFactory.create(version)
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
            obj = MouseButtonSpyFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class MouseButtonSpyTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
