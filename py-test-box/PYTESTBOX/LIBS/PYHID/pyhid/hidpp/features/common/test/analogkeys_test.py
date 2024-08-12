#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.analogkeys_test
:brief: HID++ 2.0 ``AnalogKeys`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.analogkeys import AnalogKeys
from pyhid.hidpp.features.common.analogkeys import AnalogKeysFactory
from pyhid.hidpp.features.common.analogkeys import AnalogKeysV0
from pyhid.hidpp.features.common.analogkeys import GetCapabilities
from pyhid.hidpp.features.common.analogkeys import GetCapabilitiesResponse
from pyhid.hidpp.features.common.analogkeys import GetRapidTriggerState
from pyhid.hidpp.features.common.analogkeys import GetRapidTriggerStateResponse
from pyhid.hidpp.features.common.analogkeys import KeyTravelChangeEvent
from pyhid.hidpp.features.common.analogkeys import SetKeyTravelEventState
from pyhid.hidpp.features.common.analogkeys import SetKeyTravelEventStateResponse
from pyhid.hidpp.features.common.analogkeys import SetRapidTriggerState
from pyhid.hidpp.features.common.analogkeys import SetRapidTriggerStateResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysInstantiationTestCase(TestCase):
    """
    Test ``AnalogKeys`` testing classes instantiations
    """

    @staticmethod
    def test_analog_keys():
        """
        Test ``AnalogKeys`` class instantiation
        """
        my_class = AnalogKeys(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = AnalogKeys(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_analog_keys

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
    def test_get_rapid_trigger_state():
        """
        Test ``GetRapidTriggerState`` class instantiation
        """
        my_class = GetRapidTriggerState(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRapidTriggerState(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_rapid_trigger_state

    @staticmethod
    def test_set_rapid_trigger_state():
        """
        Test ``SetRapidTriggerState`` class instantiation
        """
        my_class = SetRapidTriggerState(device_index=0, feature_index=0, rapid_trigger_state=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetRapidTriggerState(device_index=0xFF, feature_index=0xFF, rapid_trigger_state=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_rapid_trigger_state

    @staticmethod
    def test_set_key_travel_event_state():
        """
        Test ``SetKeyTravelEventState`` class instantiation
        """
        my_class = SetKeyTravelEventState(device_index=0, feature_index=0, key_travel_event_state=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetKeyTravelEventState(device_index=0xFF, feature_index=0xFF, key_travel_event_state=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_key_travel_event_state

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           analog_key_config_file_ver=0,
                                           analog_key_config_file_maxsize=0,
                                           analog_key_level_resolution=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           analog_key_config_file_ver=0xFF,
                                           analog_key_config_file_maxsize=0xFFFF,
                                           analog_key_level_resolution=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_rapid_trigger_state_response():
        """
        Test ``GetRapidTriggerStateResponse`` class instantiation
        """
        my_class = GetRapidTriggerStateResponse(device_index=0, feature_index=0, rapid_trigger_state=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRapidTriggerStateResponse(device_index=0xFF, feature_index=0xFF, rapid_trigger_state=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_rapid_trigger_state_response

    @staticmethod
    def test_set_rapid_trigger_state_response():
        """
        Test ``SetRapidTriggerStateResponse`` class instantiation
        """
        my_class = SetRapidTriggerStateResponse(device_index=0, feature_index=0, rapid_trigger_state=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRapidTriggerStateResponse(device_index=0xFF, feature_index=0xFF, rapid_trigger_state=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rapid_trigger_state_response

    @staticmethod
    def test_set_key_travel_event_state_response():
        """
        Test ``SetKeyTravelEventStateResponse`` class instantiation
        """
        my_class = SetKeyTravelEventStateResponse(device_index=0, feature_index=0, key_travel_event_state=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetKeyTravelEventStateResponse(device_index=0xFF, feature_index=0xFF, key_travel_event_state=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_key_travel_event_state_response

    @staticmethod
    def test_key_travel_change_event():
        """
        Test ``KeyTravelChangeEvent`` class instantiation
        """
        my_class = KeyTravelChangeEvent(device_index=0, feature_index=0, key_cidx=0, key_travel=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = KeyTravelChangeEvent(device_index=0xFF, feature_index=0xFF, key_cidx=0xFF, key_travel=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_key_travel_change_event
# end class AnalogKeysInstantiationTestCase


class AnalogKeysTestCase(TestCase):
    """
    Test ``AnalogKeys`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            AnalogKeysV0.VERSION: {
                "cls": AnalogKeysV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_rapid_trigger_state_cls": GetRapidTriggerState,
                    "get_rapid_trigger_state_response_cls": GetRapidTriggerStateResponse,
                    "set_rapid_trigger_state_cls": SetRapidTriggerState,
                    "set_rapid_trigger_state_response_cls": SetRapidTriggerStateResponse,
                    "set_key_travel_event_state_cls": SetKeyTravelEventState,
                    "set_key_travel_event_state_response_cls": SetKeyTravelEventStateResponse,
                    "key_travel_change_event_cls": KeyTravelChangeEvent,
                },
                "max_function_index": 3
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``AnalogKeysFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(AnalogKeysFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``AnalogKeysFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                AnalogKeysFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``AnalogKeysFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = AnalogKeysFactory.create(version)
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
            obj = AnalogKeysFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
