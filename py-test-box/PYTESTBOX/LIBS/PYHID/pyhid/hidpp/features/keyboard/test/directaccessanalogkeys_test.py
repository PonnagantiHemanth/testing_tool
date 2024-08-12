#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.keyboard.test.directaccessanalogkeys_test
:brief: HID++ 2.0 ``DirectAccessAnalogKeys`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.keyboard.directaccessanalogkeys import DirectAccessAnalogKeys
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import DirectAccessAnalogKeysFactory
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import DirectAccessAnalogKeysV0
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import GetCapabilities
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import GetCapabilitiesResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetAnalogKeyMode
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetAnalogKeyModeResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetMultiAction
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetMultiActionResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetNormalTrigger
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetNormalTriggerResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetRapidTrigger
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetRapidTriggerResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DirectAccessAnalogKeysInstantiationTestCase(TestCase):
    """
    Test ``DirectAccessAnalogKeys`` testing classes instantiations
    """

    @staticmethod
    def test_direct_access_analog_keys():
        """
        Test ``DirectAccessAnalogKeys`` class instantiation
        """
        my_class = DirectAccessAnalogKeys(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = DirectAccessAnalogKeys(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_direct_access_analog_keys

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
    def test_set_analog_key_mode():
        """
        Test ``SetAnalogKeyMode`` class instantiation
        """
        my_class = SetAnalogKeyMode(device_index=0, feature_index=0,
                                    trigger_cidx=0,
                                    analog_mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetAnalogKeyMode(device_index=0xFF, feature_index=0xFF,
                                    trigger_cidx=0xFF,
                                    analog_mode=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_analog_key_mode

    @staticmethod
    def test_set_normal_trigger():
        """
        Test ``SetNormalTrigger`` class instantiation
        """
        my_class = SetNormalTrigger(device_index=0, feature_index=0,
                                    trigger_cidx=0,
                                    actuation_point=0,
                                    hysteresis=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetNormalTrigger(device_index=0xFF, feature_index=0xFF,
                                    trigger_cidx=0xFF,
                                    actuation_point=0xFF,
                                    hysteresis=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_normal_trigger

    @staticmethod
    def test_set_rapid_trigger():
        """
        Test ``SetRapidTrigger`` class instantiation
        """
        my_class = SetRapidTrigger(device_index=0, feature_index=0,
                                   trigger_cidx=0,
                                   actuation_point=0,
                                   sensitivity=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetRapidTrigger(device_index=0xFF, feature_index=0xFF,
                                   trigger_cidx=0xFF,
                                   actuation_point=0xFF,
                                   sensitivity=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_rapid_trigger

    @staticmethod
    def test_set_multi_action():
        """
        Test ``SetMultiAction`` class instantiation
        """
        my_class = SetMultiAction(device_index=0, feature_index=0,
                                  trigger_cidx=0,
                                  actuation_point_msb=0,
                                  actuation_point_lsb=0,
                                  assignment_0=0,
                                  assignment_1=0,
                                  assignment_2=0,
                                  assignment_3=0,
                                  assignment_0_event_1=0,
                                  assignment_0_event_0=0,
                                  assignment_0_event_3=0,
                                  assignment_0_event_2=0,
                                  assignment_1_event_1=0,
                                  assignment_1_event_0=0,
                                  assignment_1_event_3=0,
                                  assignment_1_event_2=0,
                                  assignment_2_event_1=0,
                                  assignment_2_event_0=0,
                                  assignment_2_event_3=0,
                                  assignment_2_event_2=0,
                                  assignment_3_event_1=0,
                                  assignment_3_event_0=0,
                                  assignment_3_event_3=0,
                                  assignment_3_event_2=0,
                                  mode=0,
                                  hysteresis=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetMultiAction(device_index=0xFF, feature_index=0xFF,
                                  trigger_cidx=0xFF,
                                  actuation_point_msb=0xFF,
                                  actuation_point_lsb=0xFF,
                                  assignment_0=0xFF,
                                  assignment_1=0xFF,
                                  assignment_2=0xFF,
                                  assignment_3=0xFF,
                                  assignment_0_event_1=0xF,
                                  assignment_0_event_0=0xF,
                                  assignment_0_event_3=0xF,
                                  assignment_0_event_2=0xF,
                                  assignment_1_event_1=0xF,
                                  assignment_1_event_0=0xF,
                                  assignment_1_event_3=0xF,
                                  assignment_1_event_2=0xF,
                                  assignment_2_event_1=0xF,
                                  assignment_2_event_0=0xF,
                                  assignment_2_event_3=0xF,
                                  assignment_2_event_2=0xF,
                                  assignment_3_event_1=0xF,
                                  assignment_3_event_0=0xF,
                                  assignment_3_event_3=0xF,
                                  assignment_3_event_2=0xF,
                                  mode=0xF,
                                  hysteresis=0xF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_multi_action

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           multi_action=0,
                                           rapid_trigger=0,
                                           normal_trigger=0,
                                           analog_key_number=0,
                                           analog_resolution=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           multi_action=0x1,
                                           rapid_trigger=0x1,
                                           normal_trigger=0x1,
                                           analog_key_number=0xFF,
                                           analog_resolution=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_set_analog_key_mode_response():
        """
        Test ``SetAnalogKeyModeResponse`` class instantiation
        """
        my_class = SetAnalogKeyModeResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetAnalogKeyModeResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_analog_key_mode_response

    @staticmethod
    def test_set_normal_trigger_response():
        """
        Test ``SetNormalTriggerResponse`` class instantiation
        """
        my_class = SetNormalTriggerResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetNormalTriggerResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_normal_trigger_response

    @staticmethod
    def test_set_rapid_trigger_response():
        """
        Test ``SetRapidTriggerResponse`` class instantiation
        """
        my_class = SetRapidTriggerResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRapidTriggerResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rapid_trigger_response

    @staticmethod
    def test_set_multi_action_response():
        """
        Test ``SetMultiActionResponse`` class instantiation
        """
        my_class = SetMultiActionResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetMultiActionResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_multi_action_response
# end class DirectAccessAnalogKeysInstantiationTestCase


class DirectAccessAnalogKeysTestCase(TestCase):
    """
    Test ``DirectAccessAnalogKeys`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            DirectAccessAnalogKeysV0.VERSION: {
                "cls": DirectAccessAnalogKeysV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "set_analog_key_mode_cls": SetAnalogKeyMode,
                    "set_analog_key_mode_response_cls": SetAnalogKeyModeResponse,
                    "set_normal_trigger_cls": SetNormalTrigger,
                    "set_normal_trigger_response_cls": SetNormalTriggerResponse,
                    "set_rapid_trigger_cls": SetRapidTrigger,
                    "set_rapid_trigger_response_cls": SetRapidTriggerResponse,
                    "set_multi_action_cls": SetMultiAction,
                    "set_multi_action_response_cls": SetMultiActionResponse,
                },
                "max_function_index": 4
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``DirectAccessAnalogKeysFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DirectAccessAnalogKeysFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``DirectAccessAnalogKeysFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                DirectAccessAnalogKeysFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``DirectAccessAnalogKeysFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = DirectAccessAnalogKeysFactory.create(version)
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
            obj = DirectAccessAnalogKeysFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class DirectAccessAnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
