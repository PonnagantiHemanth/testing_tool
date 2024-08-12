#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.feature.common.test.managedeactivatablefeaturesauth_test
    :brief: HID++ 2.0 Manage deactivatable features (based on authentication mechanism) test module
    :author: Martin Cryonnet
    :date:   2020/11/10
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import DisableFeatures
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import DisableFeaturesResponse
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import EnableFeatures
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import EnableFeaturesResponse
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import GetInfo
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import GetInfoResponse
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import GetReactInfo
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import GetReactInfoResponse
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthFactory
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthV0
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ManageDeactivatableFeaturesAuthInstantiationTestCase(TestCase):
    """
    ``ManageDeactivatableFeaturesAuth`` testing class
    """

    @staticmethod
    def test_manage_deactivatable_features_auth():
        """
        Tests ``ManageDeactivatableFeaturesAuth`` class instantiation
        """
        my_class = ManageDeactivatableFeaturesAuth(device_index=0, feature_index=0)
        RootTestCase._top_level_class_checker(my_class)

        my_class = ManageDeactivatableFeaturesAuth(device_index=0xFF, feature_index=0xFF)
        RootTestCase._top_level_class_checker(my_class)
    # end def test_manage_deactivatable_features_auth

    @staticmethod
    def test_get_info():
        """
        Tests ``GetInfo`` class instantiation
        """
        my_class = GetInfo(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetInfo(device_index=0xFF, feature_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info

    @staticmethod
    def test_get_info_response():
        """
        Tests ``GetInfoResponse`` class instantiation
        """
        my_class = GetInfoResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse(device_index=0x00, feature_index=0x00, support_all_bit=False, support_gothard=False,
                                   support_compliance=False, support_manufacturing=False,
                                   persistent_all_bit_activation=False, persistent_gothard_activation=False,
                                   persistent_compliance_activation=False,  persistent_manufacturing_activation=False)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse(device_index=0xFF, feature_index=0xFF, support_all_bit=True, support_gothard=True,
                                   support_compliance=True, support_manufacturing=True,
                                   persistent_all_bit_activation=True, persistent_gothard_activation=True,
                                   persistent_compliance_activation=True,  persistent_manufacturing_activation=True)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response

    @staticmethod
    def test_get_info_response_from_hex_list():
        """
        Tests ``GetInfoResponse`` class instantiation from ``HexList``
        """
        my_class = GetInfoResponse.fromHexList(HexList('00' * 20))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse.fromHexList(HexList('FF' * 20))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse.fromHexList(HexList('00' * 4 + '8787' + '00' * 14))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response_from_hex_list

    @staticmethod
    def test_disable_features():
        """
        Tests ``DisableFeatures`` class instantiation
        """
        my_class = DisableFeatures(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = DisableFeatures(device_index=0x00, feature_index=0x00, disable_all_bit=False, disable_gothard=False,
                                   disable_compliance=False, disable_manufacturing=False)
        RootTestCase._long_function_class_checker(my_class)

        my_class = DisableFeatures(device_index=0xFF, feature_index=0xFF, disable_all_bit=True, disable_gothard=True,
                                   disable_compliance=True, disable_manufacturing=True)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_disable_features

    @staticmethod
    def test_disable_features_from_hex_list():
        """
        Tests ``DisableFeatures`` class instantiation from ``HexList``
        """
        my_class = DisableFeatures.fromHexList(HexList('00' * 20))
        RootTestCase._long_function_class_checker(my_class)

        my_class = DisableFeatures.fromHexList(HexList('FF' * 20))
        RootTestCase._long_function_class_checker(my_class)

        my_class = DisableFeatures.fromHexList(HexList('00' * 4 + '87' + '00' * 15))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_disable_features_from_hex_list

    @staticmethod
    def test_disable_features_response():
        """
        Tests ``DisableFeaturesResponse`` class instantiation
        """
        my_class = DisableFeaturesResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = DisableFeaturesResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_disable_features_response

    @staticmethod
    def test_enable_features():
        """
        Tests ``EnableFeatures`` class instantiation
        """
        my_class = EnableFeatures(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableFeatures(device_index=0x00, feature_index=0x00, enable_all_bit=False, enable_gothard=False,
                                  enable_compliance=False, enable_manufacturing=False)
        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableFeatures(device_index=0xFF, feature_index=0xFF, enable_all_bit=True, enable_gothard=True,
                                  enable_compliance=True, enable_manufacturing=True)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_enable_features

    @staticmethod
    def test_enable_features_from_hex_list():
        """
        Tests ``EnableFeatures`` class instantiation from ``HexList``
        """
        my_class = EnableFeatures.fromHexList(HexList('00' * 20))
        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableFeatures.fromHexList(HexList('FF' * 20))
        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableFeatures.fromHexList(HexList('00' * 4 + '87' + '00' * 15))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_enable_features_from_hex_list

    @staticmethod
    def test_enable_features_response():
        """
        Tests ``EnableFeatures`` response class instantiation
        """
        my_class = EnableFeaturesResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableFeaturesResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_enable_features_response

    @staticmethod
    def test_get_react_info():
        """
        Tests ``GetReactInfo`` class instantiation
        """
        my_class = GetReactInfo(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetReactInfo(device_index=0xFF, feature_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_react_info

    @staticmethod
    def test_get_react_info_response():
        """
        Tests ``GetReactInfoResponse`` class instantiation
        """
        my_class = GetReactInfoResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetReactInfoResponse(device_index=0xFF, feature_index=0xFF, auth_feature=0xFFFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_react_info_response
# end class ManageDeactivatableFeaturesAuthInstantiationTestCase


class ManageDeactivatableFeaturesAuthTestCase(TestCase):
    """
    ``ManageDeactivatableFeaturesAuth`` factory model testing class
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": ManageDeactivatableFeaturesAuthV0,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponse,
                    "disable_features_cls": DisableFeatures,
                    "disable_features_response_cls": DisableFeaturesResponse,
                    "enable_features_cls": EnableFeatures,
                    "enable_features_response_cls": EnableFeaturesResponse,
                    "get_reactivation_info_cls": GetReactInfo,
                    "get_reactivation_info_response_cls": GetReactInfoResponse,
                },
                "max_function_index": 3
            },
        }
    # end def setUpClass

    def test_manage_deactivatable_features_factory(self):
        """
        Tests Manage deactivatable features Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ManageDeactivatableFeaturesAuthFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_manage_deactivatable_features_factory

    def test_manage_deactivatable_features_factory_version_out_of_range(self):
        """
        Tests Manage deactivatable features Factory with out of range versions
        """
        for version in [1, 2, 3]:
            with self.assertRaises(KeyError):
                ManageDeactivatableFeaturesAuthFactory.create(version)
            # end with
        # end for
    # end def test_manage_deactivatable_features_factory_version_out_of_range

    def test_manage_deactivatable_features_factory_interfaces(self):
        """
        Check Manage deactivatable features Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            manage_deactivatable_features = ManageDeactivatableFeaturesAuthFactory.create(version)
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
            manage_deactivatable_features = ManageDeactivatableFeaturesAuthFactory.create(version)
            self.assertEqual(manage_deactivatable_features.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class ManageDeactivatableFeaturesTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
