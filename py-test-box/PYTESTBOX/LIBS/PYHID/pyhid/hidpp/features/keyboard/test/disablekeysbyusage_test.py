#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.keyboard.test.disablekeysbyusage_test

@brief  HID++ 2.0 disable keys by usage test module

@author Roy Luo

@date   2019/05/22
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsage
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsageFactory
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsageV0
from pyhid.hidpp.features.keyboard.disablekeysbyusage import GetCapabilities
from pyhid.hidpp.features.keyboard.disablekeysbyusage import GetCapabilitiesResponse
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeys
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysResponse
from pyhid.hidpp.features.keyboard.disablekeysbyusage import EnableKeys
from pyhid.hidpp.features.keyboard.disablekeysbyusage import EnableKeysResponse
from pyhid.hidpp.features.keyboard.disablekeysbyusage import EnableAllKeys
from pyhid.hidpp.features.keyboard.disablekeysbyusage import EnableAllKeysResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class DisableKeysByUsageInstantiationTestCase(TestCase):
    """
    DisableKeysByUsage testing classes instantiations
    """

    @staticmethod
    def test_disable_keys_by_usage():
        """
        Tests DisableKeysByUsage class instantiation
        """
        my_class = DisableKeysByUsage(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = DisableKeysByUsage(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_disable_keys_by_usage

    @staticmethod
    def test_get_capabilities():
        """
        Tests GetDeviceInfoV1ToV3 class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_capabilities_response():
        """
        Tests GetCapabilitiesResponse class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0,
                                           feature_index=0,
                                           max_disabled_keys=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF,
                                           feature_index=0xFF,
                                           max_disabled_keys=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_disable_keys():
        """
        Tests DisableKeys class instantiation
        """
        key_list = [0]*16
        my_class = DisableKeys(device_index=0, feature_index=0, keys_to_disable=key_list)

        RootTestCase._long_function_class_checker(my_class)

        key_list = [0xFF]*16
        my_class = DisableKeys(device_index=0xFF, feature_index=0xFF, keys_to_disable=key_list)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_disable_keys

    @staticmethod
    def test_disable_keys_response():
        """
        Tests DisableKeysResponse class instantiation
        """
        my_class = DisableKeysResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DisableKeysResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_disable_keys_response

    @staticmethod
    def test_enable_keys():
        """
        Tests EnableKeys class instantiation
        """
        key_list = [0]*16
        my_class = EnableKeys(device_index=0, feature_index=0, keys_to_enable=key_list)

        RootTestCase._long_function_class_checker(my_class)

        key_list = [0xFF]*16
        my_class = EnableKeys(device_index=0xFF, feature_index=0xFF, keys_to_enable=key_list)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_enable_keys

    @staticmethod
    def test_enable_keys_response():
        """
        Tests EnableKeysResponse class instantiation
        """
        my_class = EnableKeysResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableKeysResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_enable_keys_response

    @staticmethod
    def test_enable_all_keys():
        """
        Tests EnableAllKeys class instantiation
        """
        my_class = EnableAllKeys(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = EnableAllKeys(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_enable_all_keys

    @staticmethod
    def test_enable_all_keys_response():
        """
        Tests EnableAllKeysResponse class instantiation
        """
        my_class = EnableAllKeysResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableAllKeysResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_enable_all_keys_response
# end class DisableKeysByUsageInstantiationTestCase

class DisableKeysByUsageTestCase(TestCase):
    """
    Disable keys by usage factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": DisableKeysByUsageV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "disable_keys_cls": DisableKeys,
                    "disable_keys_response_cls": DisableKeysResponse,
                    "enable_keys_cls": EnableKeys,
                    "enable_keys_response_cls": EnableKeysResponse,
                    "enable_all_keys_cls": EnableAllKeys,
                    "enable_all_keys_response_cls": EnableAllKeysResponse,
                },
                "max_function_index": 3
            }
        }
    # end def setUpClass

    def test_disable_keys_by_usage_factory(self):
        """
        Tests DisableKeysByUsageFactory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DisableKeysByUsageFactory.create(version)), expected["cls"])
        # end for
    # end def test_disable_keys_by_usage_factory

    def test_disable_keys_by_usage_factory_version_out_of_range(self):
        """
        Tests DisableKeysByUsageFactory with out of range versions
        """
        for version in [1]:
            with self.assertRaises(KeyError):
                DisableKeysByUsageFactory.create(version)
            # end with
        # end for
    # end def test_disable_keys_by_usage_factory_version_out_of_range

    def test_disable_keys_by_usage_factory_interfaces(self):
        """
        Check DisableKeysByUsageFactory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            disable_keys_by_usage = DisableKeysByUsageFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(disable_keys_by_usage, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(disable_keys_by_usage, interface)
                # end if
            # end for
        # end for
    # end def test_disable_keys_by_usage_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            disable_keys_by_usage = DisableKeysByUsageFactory.create(version)
            self.assertEqual(disable_keys_by_usage.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class DisableKeysByUsageTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
