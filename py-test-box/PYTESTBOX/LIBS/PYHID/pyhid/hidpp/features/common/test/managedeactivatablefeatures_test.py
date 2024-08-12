#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.feature.common.test.managedeactivatablefeatures_test
    :brief: HID++ 2.0 Manage deactivatable features test module
    :author: Christophe Roquebert
    :date:   2020/06/08
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.managedeactivatablefeatures import GetReactInfo
from pyhid.hidpp.features.common.managedeactivatablefeatures import GetReactInfoResponse
from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeaturesFactory
from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeaturesV0
from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeatures
from pyhid.hidpp.features.common.managedeactivatablefeatures import GetCounters
from pyhid.hidpp.features.common.managedeactivatablefeatures import GetCountersResponse
from pyhid.hidpp.features.common.managedeactivatablefeatures import SetCounters
from pyhid.hidpp.features.common.managedeactivatablefeatures import SetCountersResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import RandHexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ManageDeactivatableFeaturesInstantiationTestCase(TestCase):
    """
    ManageDeactivatableFeatures testing class
    """

    @staticmethod
    def test_manage_deactivatable_features():
        """
        Tests ManageDeactivatableFeatures class instantiation
        """
        my_class = ManageDeactivatableFeatures(device_index=0, feature_index=0)
        RootTestCase._top_level_class_checker(my_class)

        my_class = ManageDeactivatableFeatures(device_index=0xFF, feature_index=0xFF)
        RootTestCase._top_level_class_checker(my_class)
    # end def test_manage_deactivatable_features

    @staticmethod
    def test_get_counters():
        """
        Tests GetCounters class instantiation
        """
        my_class = GetCounters(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCounters(device_index=RandHexList(1), feature_index=RandHexList(1))
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCounters(device_index=0xFF, feature_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_counters

    @staticmethod
    def test_get_counters_response():
        """
        Tests GetCounters response class instantiation
        """
        my_class = GetCountersResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCountersResponse(device_index=RandHexList(1), feature_index=RandHexList(1), all_bit=False,
                                       gothard=False, compl_hidpp=False, manuf_hidpp=False, manuf_hidpp_counter=0x00,
                                       compl_hidpp_counter=0x00, gothard_counter=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCountersResponse(device_index=0xFF, feature_index=0xFF, all_bit=True, gothard=True,
                                       compl_hidpp=True, manuf_hidpp=True, manuf_hidpp_counter=0xFF,
                                       compl_hidpp_counter=0xFF, gothard_counter=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_counters_response

    @staticmethod
    def test_set_counters():
        """
        Tests SetCounters class instantiation
        """
        my_class = SetCounters(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCounters(device_index=RandHexList(1), feature_index=RandHexList(1), all_bit=False, gothard=False,
                               compl_hidpp=False, manuf_hidpp=False, manuf_hidpp_counter=0x00,
                               compl_hidpp_counter=0x00, gothard_counter=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCounters(device_index=0xFF, feature_index=0xFF, all_bit=True, gothard=True, compl_hidpp=True,
                               manuf_hidpp=True, manuf_hidpp_counter=0xFF, compl_hidpp_counter=0xFF,
                               gothard_counter=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_counters

    @staticmethod
    def test_set_counters_response():
        """
        Tests SetCounters response class instantiation
        """
        my_class = SetCountersResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCountersResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_counters_response

    @staticmethod
    def test_get_react_info():
        """
        Tests GetReactInfo class instantiation
        """
        my_class = GetReactInfo(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetReactInfo(device_index=RandHexList(1), feature_index=RandHexList(1))
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetReactInfo(device_index=0xFF, feature_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_react_info

    @staticmethod
    def test_get_react_info_response():
        """
        Tests GetCounters response class instantiation
        """
        my_class = GetReactInfoResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetReactInfoResponse(device_index=RandHexList(1), feature_index=RandHexList(1), auth_feature=0x0000)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetReactInfoResponse(device_index=0xFF, feature_index=0xFF, auth_feature=0xFFFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_react_info_response
# end class ManageDeactivatableFeaturesInstantiationTestCase


class ManageDeactivatableFeaturesTestCase(TestCase):
    """
    Dfu Control factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": ManageDeactivatableFeaturesV0,
                "interfaces": {
                    "get_counters_cls": GetCounters,
                    "get_counters_response_cls": GetCountersResponse,
                    "set_counters_cls": SetCounters,
                    "set_counters_response_cls": SetCountersResponse,
                    "get_react_info_cls": GetReactInfo,
                    "get_react_info_response_cls": GetReactInfoResponse,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_manage_deactivatable_features_factory(self):
        """
        Tests Manage deactivatable features Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ManageDeactivatableFeaturesFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_manage_deactivatable_features_factory

    def test_manage_deactivatable_features_factory_version_out_of_range(self):
        """
        Tests Manage deactivatable features Factory with out of range versions
        """
        for version in [1, 2, 3]:
            with self.assertRaises(KeyError):
                ManageDeactivatableFeaturesFactory.create(version)
            # end with
        # end for
    # end def test_manage_deactivatable_features_factory_version_out_of_range

    def test_manage_deactivatable_features_factory_interfaces(self):
        """
        Check Manage deactivatable features Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            manage_deactivatable_features = ManageDeactivatableFeaturesFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(manage_deactivatable_features, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(manage_deactivatable_features, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_manage_deactivatable_features_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            manage_deactivatable_features = ManageDeactivatableFeaturesFactory.create(version)
            self.assertEqual(manage_deactivatable_features.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class ManageDeactivatableFeaturesTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
