#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.keyboard.test.multiroller_test
:brief: HID++ 2.0 ``MultiRoller`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.keyboard.multiroller import GetCapabilities
from pyhid.hidpp.features.keyboard.multiroller import GetCapabilitiesResponse
from pyhid.hidpp.features.keyboard.multiroller import GetMode
from pyhid.hidpp.features.keyboard.multiroller import GetModeResponse
from pyhid.hidpp.features.keyboard.multiroller import GetRollerCapabilitiesResponseV0
from pyhid.hidpp.features.keyboard.multiroller import GetRollerCapabilitiesResponseV1
from pyhid.hidpp.features.keyboard.multiroller import GetRollerCapabilities
from pyhid.hidpp.features.keyboard.multiroller import MultiRoller
from pyhid.hidpp.features.keyboard.multiroller import MultiRollerFactory
from pyhid.hidpp.features.keyboard.multiroller import MultiRollerV0
from pyhid.hidpp.features.keyboard.multiroller import MultiRollerV1
from pyhid.hidpp.features.keyboard.multiroller import RotationEventV0
from pyhid.hidpp.features.keyboard.multiroller import RotationEventV1
from pyhid.hidpp.features.keyboard.multiroller import SetMode
from pyhid.hidpp.features.keyboard.multiroller import SetModeResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerInstantiationTestCase(TestCase):
    """
    Test ``MultiRoller`` testing classes instantiations
    """

    @staticmethod
    def test_multi_roller():
        """
        Test ``MultiRoller`` class instantiation
        """
        my_class = MultiRoller(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = MultiRoller(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_multi_roller

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
    def test_get_roller_capabilities():
        """
        Test ``GetRollerCapabilities`` class instantiation
        """
        my_class = GetRollerCapabilities(device_index=0, feature_index=0,
                                         roller_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRollerCapabilities(device_index=0xFF, feature_index=0xFF,
                                         roller_id=0xF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_roller_capabilities

    @staticmethod
    def test_get_mode():
        """
        Test ``GetMode`` class instantiation
        """
        my_class = GetMode(device_index=0, feature_index=0,
                           roller_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetMode(device_index=0xFF, feature_index=0xFF,
                           roller_id=0xF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_mode

    @staticmethod
    def test_set_mode():
        """
        Test ``SetMode`` class instantiation
        """
        my_class = SetMode(device_index=0, feature_index=0,
                           roller_id=0,
                           divert=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetMode(device_index=0xFF, feature_index=0xFF,
                           roller_id=0xF,
                           divert=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_mode

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           num_rollers=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           num_rollers=0xF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_roller_capabilities_response_v0():
        """
        Test ``GetRollerCapabilitiesResponseV0`` class instantiation
        """
        my_class = GetRollerCapabilitiesResponseV0(device_index=0, feature_index=0,
                                                   increments_per_rotation=0,
                                                   increments_per_ratchet=0,
                                                   lightbar_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRollerCapabilitiesResponseV0(device_index=0xFF, feature_index=0xFF,
                                                   increments_per_rotation=0xFF,
                                                   increments_per_ratchet=0xFF,
                                                   lightbar_id=0xF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_roller_capabilities_response_v0

    @staticmethod
    def test_get_roller_capabilities_response_v1():
        """
        Test ``GetRollerCapabilitiesResponseV1`` class instantiation
        """
        my_class = GetRollerCapabilitiesResponseV1(device_index=0, feature_index=0,
                                                   increments_per_rotation=0,
                                                   increments_per_ratchet=0,
                                                   timestamp_report=0,
                                                   lightbar_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRollerCapabilitiesResponseV1(device_index=0xFF, feature_index=0xFF,
                                                   increments_per_rotation=0xFF,
                                                   increments_per_ratchet=0xFF,
                                                   timestamp_report=0x1,
                                                   lightbar_id=0xF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_roller_capabilities_response_v1

    @staticmethod
    def test_get_mode_response():
        """
        Test ``GetModeResponse`` class instantiation
        """
        my_class = GetModeResponse(device_index=0, feature_index=0,
                                   divert=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetModeResponse(device_index=0xFF, feature_index=0xFF,
                                   divert=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_mode_response

    @staticmethod
    def test_set_mode_response():
        """
        Test ``SetModeResponse`` class instantiation
        """
        my_class = SetModeResponse(device_index=0, feature_index=0,
                                   roller_id=0, divert=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetModeResponse(device_index=0xFF, feature_index=0xFF,
                                   roller_id=0xF, divert=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_mode_response

    @staticmethod
    def test_rotation_event_v0():
        """
        Test ``RotationEventV0`` class instantiation
        """
        my_class = RotationEventV0(device_index=0, feature_index=0,
                                   roller_id=0,
                                   delta=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RotationEventV0(device_index=0xFF, feature_index=0xFF,
                                   roller_id=0xF,
                                   delta=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rotation_event_v0

    @staticmethod
    def test_rotation_event_v1():
        """
        Test ``RotationEventV1`` class instantiation
        """
        my_class = RotationEventV1(device_index=0, feature_index=0,
                                   roller_id=0,
                                   delta=0,
                                   report_timestamp=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = RotationEventV1(device_index=0xFF, feature_index=0xFF,
                                   roller_id=0xF,
                                   delta=0xFF,
                                   report_timestamp=HexList("FF" * (RotationEventV1.LEN.REPORT_TIMESTAMP // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rotation_event_v1
# end class MultiRollerInstantiationTestCase


class MultiRollerTestCase(TestCase):
    """
    Test ``MultiRoller`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            MultiRollerV0.VERSION: {
                "cls": MultiRollerV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_roller_capabilities_cls": GetRollerCapabilities,
                    "get_roller_capabilities_response_cls": GetRollerCapabilitiesResponseV0,
                    "get_mode_cls": GetMode,
                    "get_mode_response_cls": GetModeResponse,
                    "set_mode_cls": SetMode,
                    "set_mode_response_cls": SetModeResponse,
                    "rotation_event_cls": RotationEventV0,
                },
                "max_function_index": 3
            },
            MultiRollerV1.VERSION: {
                "cls": MultiRollerV1,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_roller_capabilities_cls": GetRollerCapabilities,
                    "get_roller_capabilities_response_cls": GetRollerCapabilitiesResponseV1,
                    "get_mode_cls": GetMode,
                    "get_mode_response_cls": GetModeResponse,
                    "set_mode_cls": SetMode,
                    "set_mode_response_cls": SetModeResponse,
                    "rotation_event_cls": RotationEventV1,
                },
                "max_function_index": 3
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``MultiRollerFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(MultiRollerFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``MultiRollerFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                MultiRollerFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``MultiRollerFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = MultiRollerFactory.create(version)
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
            obj = MultiRollerFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class MultiRollerTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
