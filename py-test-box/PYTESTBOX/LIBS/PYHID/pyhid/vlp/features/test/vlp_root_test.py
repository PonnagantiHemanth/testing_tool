#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.test.keydisplay_test
:brief: VLP 1.0 ``KeyDisplay`` test module
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/10/05
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.vlp.features.important.vlproot import VLPRoot
from pyhid.vlp.features.important.vlproot import VLPRootFactory
from pyhid.vlp.features.important.vlproot import VLPRootV0
from pyhid.vlp.features.important.vlproot import GetFeatureIndex
from pyhid.vlp.features.important.vlproot import GetProtocolCapabilities
from pyhid.vlp.features.important.vlproot import GetPingData
from pyhid.vlp.features.important.vlproot import GetFeatureIndexResponse
from pyhid.vlp.features.important.vlproot import GetProtocolCapabilitiesResponse
from pyhid.vlp.features.important.vlproot import GetPingDataResponse
from pyhid.vlp.vlpmessage import VlpMessage
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class VLPRootTestCase(TestCase):
    """
    Root testing class
    """
    @staticmethod
    def _top_level_class_checker(a_class):
        """
        Checks some generic attributes from top-level class
        """
        # FEATURE_ID attribute presence
        assert(hasattr(a_class, 'FEATURE_ID') is True)
        # VERSION attribute presence
        assert(hasattr(a_class, 'VERSION') is True)
    # end def _top_level_class_checker

    @staticmethod
    def _function_class_checker(a_class):
        """
        Checks some generic attributes from top-level class
        """
        # top-level attribute presence
        VLPRootTestCase._top_level_class_checker(a_class)
        # functionIndex attribute presence
        assert(hasattr(a_class, 'function_index') is True)
    # end def _function_class_checker
# class VLPRootTestCase


class VLPRootClassesTestCase(VLPRootTestCase):
    """
    Root classes testing class
    """
    def test_root(self):
        """
        Tests Root class instantiation
        """
        my_class = VLPRoot(device_index=0)

        VLPRootTestCase._top_level_class_checker(my_class)
    # end def test_root

    def test_root_get_feature_index(self):
        """
        Tests GetFeatureIndex class instantiation
        """
        my_class = GetFeatureIndex(device_index=0,
                                  feature_id=0x0102)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_root_get_feature_index

    def test_root_get_protocol_capabilities(self):
        """
        Tests GetProtocolCapabilities class instantiation
        """
        my_class = GetProtocolCapabilities(device_index=0, feature_index=0)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_root_get_protocol_capabilities

    def test_root_get_feature_response(self):
        """
        Tests RootGetFeatureResponse class instantiation
        """
        my_class = GetFeatureIndexResponse(device_index=0, feature_index=0, feature_idx=0x00, feature_id=0x0102,
                                           feature_version=0, feature_max_memory=0x00)
        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetFeatureIndexResponse(device_index=0xFF, feature_index=0xFF, feature_idx=0xFF, feature_id=0xFFFF,
                                           feature_version=0xFF, feature_max_memory=0xFF)
        VLPRootTestCase._function_class_checker(my_class)
    # end def test_root_get_feature_response

    def test_root_get_protocol_capabilities_response(self):
        """
        Tests GetProtocolCapabilitiesResponse class instantiation
        """
        my_class = GetProtocolCapabilitiesResponse(device_index=0, feature_index=0,
                                                   protocol_major=0, protocol_minor=0,
                                                   available_total_memory=0xAA)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_root_get_protocol_capabilities_response
# end class VLPRootClassesTestCase


class RootFactoryTestCase(TestCase):
    """
    Root factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": VLPRootV0,
                "interfaces": {
                    "get_feature_index_cls": GetFeatureIndex,
                    "get_protocol_capabilities_cls": GetProtocolCapabilities,
                    "get_ping_data_cls": GetPingData,
                    "get_feature_index_response_cls": GetFeatureIndexResponse,
                    "get_protocol_capabilities_response_cls": GetProtocolCapabilitiesResponse,
                    "get_ping_data_response_cls": GetPingDataResponse,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_root_factory(self):
        """
        Tests Root Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(VLPRootFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_root_factory

    def test_root_factory_version_out_of_range(self):
        """
        Tests Root Factory with out of range versions
        """
        for version in [3, 4]:
            with self.assertRaises(KeyError):
                VLPRootFactory.create(version)
            # end with
        # end for
    # end def test_root_factory_version_out_of_range

    def test_root_factory_interfaces(self):
        """
        Check Root Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            root = VLPRootFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(root, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(root, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_root_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            root = VLPRootFactory.create(version)
            self.assertEqual(root.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class VLPRootTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------