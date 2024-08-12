#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.forcesensingbutton_test
:brief: HID++ 2.0 ``ForceSensingButton`` test module
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2024/08/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.forcesensingbutton import ForceSensingButton
from pyhid.hidpp.features.common.forcesensingbutton import ForceSensingButtonFactory
from pyhid.hidpp.features.common.forcesensingbutton import ForceSensingButtonV0
from pyhid.hidpp.features.common.forcesensingbutton import GetButtonCapabilities
from pyhid.hidpp.features.common.forcesensingbutton import GetButtonCapabilitiesResponse
from pyhid.hidpp.features.common.forcesensingbutton import GetButtonConfig
from pyhid.hidpp.features.common.forcesensingbutton import GetButtonConfigResponse
from pyhid.hidpp.features.common.forcesensingbutton import GetCapabilities
from pyhid.hidpp.features.common.forcesensingbutton import GetCapabilitiesResponse
from pyhid.hidpp.features.common.forcesensingbutton import SetButtonConfig
from pyhid.hidpp.features.common.forcesensingbutton import SetButtonConfigResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ForceSensingButtonInstantiationTestCase(TestCase):
    """
    Test ``ForceSensingButton`` testing classes instantiations
    """

    @staticmethod
    def test_force_sensing_button():
        """
        Test ``ForceSensingButton`` class instantiation
        """
        my_class = ForceSensingButton(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ForceSensingButton(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_force_sensing_button

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
    def test_get_button_capabilities():
        """
        Test ``GetButtonCapabilities`` class instantiation
        """
        my_class = GetButtonCapabilities(device_index=0, feature_index=0,
                                         button_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetButtonCapabilities(device_index=0xFF, feature_index=0xFF,
                                         button_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_button_capabilities

    @staticmethod
    def test_get_button_config():
        """
        Test ``GetButtonConfig`` class instantiation
        """
        my_class = GetButtonConfig(device_index=0, feature_index=0,
                                   button_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetButtonConfig(device_index=0xFF, feature_index=0xFF,
                                   button_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_button_config

    @staticmethod
    def test_set_button_config():
        """
        Test ``SetButtonConfig`` class instantiation
        """
        my_class = SetButtonConfig(device_index=0, feature_index=0,
                                   button_id=0,
                                   new_force=HexList(0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetButtonConfig(device_index=0xFF, feature_index=0xFF,
                                   button_id=0xFF,
                                   new_force=HexList("FF" * (SetButtonConfig.LEN.NEW_FORCE // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_button_config

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           number_of_buttons=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           number_of_buttons=HexList("FF" * (GetCapabilitiesResponse.LEN.NUMBER_OF_BUTTONS // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_button_capabilities_response():
        """
        Test ``GetButtonCapabilitiesResponse`` class instantiation
        """
        my_class = GetButtonCapabilitiesResponse(
            device_index=0,
            feature_index=0,
            customizable_force=False,
            default_force=HexList(0),
            max_force=HexList(0),
            min_force=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetButtonCapabilitiesResponse(
            device_index=0xFF,
            feature_index=0xFF,
            customizable_force=True,
            default_force=HexList("FF" * (GetButtonCapabilitiesResponse.ButtonCapabilities.LEN.DEFAULT_FORCE // 8)),
            max_force=HexList("FF" * (GetButtonCapabilitiesResponse.ButtonCapabilities.LEN.MAX_FORCE // 8)),
            min_force=HexList("FF" * (GetButtonCapabilitiesResponse.ButtonCapabilities.LEN.MIN_FORCE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_button_capabilities_response

    @staticmethod
    def test_get_button_config_response():
        """
        Test ``GetButtonConfigResponse`` class instantiation
        """
        my_class = GetButtonConfigResponse(device_index=0, feature_index=0,
                                           current_force=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetButtonConfigResponse(device_index=0xFF, feature_index=0xFF,
                                           current_force=HexList("FF" * (GetButtonConfigResponse.LEN.CURRENT_FORCE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_button_config_response

    @staticmethod
    def test_set_button_config_response():
        """
        Test ``SetButtonConfigResponse`` class instantiation
        """
        my_class = SetButtonConfigResponse(device_index=0, feature_index=0,
                                           button_id=0,
                                           current_force=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetButtonConfigResponse(device_index=0xFF, feature_index=0xFF,
                                           button_id=0xFF,
                                           current_force=HexList("FF" * (SetButtonConfigResponse.LEN.CURRENT_FORCE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_button_config_response
# end class ForceSensingButtonInstantiationTestCase


class ForceSensingButtonTestCase(TestCase):
    """
    Test ``ForceSensingButton`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ForceSensingButtonV0.VERSION: {
                "cls": ForceSensingButtonV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_button_capabilities_cls": GetButtonCapabilities,
                    "get_button_capabilities_response_cls": GetButtonCapabilitiesResponse,
                    "get_button_config_cls": GetButtonConfig,
                    "get_button_config_response_cls": GetButtonConfigResponse,
                    "set_button_config_cls": SetButtonConfig,
                    "set_button_config_response_cls": SetButtonConfigResponse,
                },
                "max_function_index": 3
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ForceSensingButtonFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ForceSensingButtonFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ForceSensingButtonFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                ForceSensingButtonFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ForceSensingButtonFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ForceSensingButtonFactory.create(version)
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
            obj = ForceSensingButtonFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ForceSensingButtonTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
