#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.test.root_test

@brief  HID++ 2.0 root test module

@author christophe.roquebert

@date   2019/04/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList, RandHexList
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.features.root import RootModel
from pyhid.hidpp.features.root import RootFactory
from pyhid.hidpp.features.root import RootInterface
from pyhid.hidpp.features.root import RootV0
from pyhid.hidpp.features.root import RootV1
from pyhid.hidpp.features.root import RootV2
from pyhid.hidpp.features.root import RootGetFeature
from pyhid.hidpp.features.root import RootGetProtocolVersion
from pyhid.hidpp.features.root import RootGetFeatureResponse
from pyhid.hidpp.features.root import RootGetFeaturev1Response
from pyhid.hidpp.features.root import RootGetFeaturev2Response
from pyhid.hidpp.features.root import RootGetProtocolVersionResponse
from pyhid.hidpp.hidppmessage import HidppMessage
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class RootTestCase(TestCase):
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
    def _function_class_checker(a_class, payload_size):
        """
        Checks some generic attributes from top-level class
        """
        # top-level attribute presence
        RootTestCase._top_level_class_checker(a_class)
        # functionIndex attribute presence
        assert(hasattr(a_class, 'functionIndex') is True)
        # Check payload size
        buffer = HexList(a_class)
        assert(payload_size == len(buffer))
    # end def _function_class_checker

    @staticmethod
    def _short_function_class_checker(a_class):
        """
        Checks some generic attributes from top-level class
        """
        # short payload class verification
        RootTestCase._function_class_checker(a_class, HidppMessage.SHORT_MSG_SIZE)
    # end def _short_function_class_checker

    @staticmethod
    def _long_function_class_checker(a_class):
        """
        Checks some generic attributes from top-level class
        """
        # long payload class verification
        RootTestCase._function_class_checker(a_class, HidppMessage.LONG_MSG_SIZE)
    # end def _long_function_class_checker
# class RootTestCase


class RootClassesTestCase(RootTestCase):
    """
    Root classes testing class
    """
    def test_root(self):
        """
        Tests Root class instantiation
        """
        my_class = Root(device_index=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_root

    def test_root_get_feature(self):
        """
        Tests RootGetFeature class instantiation
        """
        my_class = RootGetFeature(deviceIndex=0,
                                  featureId=0x0001)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_root_get_feature

    def test_root_get_protocol_version(self):
        """
        Tests RootGetProtocolVersion class instantiation
        """
        my_class = RootGetProtocolVersion(deviceIndex=0,
                                          pingData=0xAA)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_root_get_protocol_version

    def test_root_get_feature_response(self):
        """
        Tests RootGetFeatureResponse class instantiation
        """
        my_class = RootGetFeatureResponse(device_index=0, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = RootGetFeatureResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_root_get_feature_response

    def test_root_get_feature_response_v1(self):
        """
        Tests RootGetFeaturev1Response class instantiation
        """
        my_class = RootGetFeaturev1Response(device_index=0, feature_index=0x00, feature_version=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = RootGetFeaturev1Response(device_index=0xFF, feature_index=0xFF, feature_version=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_root_get_feature_response_v1

    def test_root_get_feature_response_v2(self):
        """
        Tests RootGetFeaturev2Response class instantiation
        """
        my_class = RootGetFeaturev2Response(device_index=0, feature_index=0x00, feature_version=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = RootGetFeaturev2Response(device_index=RandHexList(1),
            feature_index=RandHexList(RootGetFeaturev2Response.LEN.FEATURE_INDEX//8),
            feature_version=RandHexList(RootGetFeaturev2Response.LEN.FEATURE_VERSION//8),
            obsolete=False, hidden=False, engineering=False, manuf_deact=False, compl_deact=False)
        RootTestCase._long_function_class_checker(my_class)

        my_class = RootGetFeaturev2Response(device_index=0xFF,
            feature_index=0xFF, feature_version=0xFF, obsolete=True, hidden=True, engineering=True,
            manuf_deact=True, compl_deact=True)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_root_get_feature_response_v2

    def test_root_get_protocol_version_response(self):
        """
        Tests RootGetProtocolVersionResponse class instantiation
        """
        my_class = RootGetProtocolVersionResponse(device_index=0,
                                                  protocol_number=4,
                                                  target_software=5,
                                                  ping_data=0xAA)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_root_get_protocol_version_response
# end class RootClassesTestCase


class RootFactoryTestCase(TestCase):
    """
    Root factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": RootV0,
                "interfaces": {
                    "get_feature_cls": RootGetFeature,
                    "get_protocol_version_cls": RootGetProtocolVersion,
                    "get_feature_response_cls": RootGetFeatureResponse,
                    "get_protocol_version_response_cls": RootGetProtocolVersionResponse,
                },
                "max_function_index": 1
            },
            1: {
                "cls": RootV1,
                "interfaces": {
                    "get_feature_cls": RootGetFeature,
                    "get_protocol_version_cls": RootGetProtocolVersion,
                    "get_feature_response_cls": RootGetFeaturev1Response,
                    "get_protocol_version_response_cls": RootGetProtocolVersionResponse,
                },
                "max_function_index": 1
            },
            2: {
                "cls": RootV2,
                "interfaces": {
                    "get_feature_cls": RootGetFeature,
                    "get_protocol_version_cls": RootGetProtocolVersion,
                    "get_feature_response_cls": RootGetFeaturev2Response,
                    "get_protocol_version_response_cls": RootGetProtocolVersionResponse,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_root_factory(self):
        """
        Tests Root Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(RootFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_root_factory

    def test_root_factory_version_out_of_range(self):
        """
        Tests Root Factory with out of range versions
        """
        for version in [3, 4]:
            with self.assertRaises(KeyError):
                RootFactory.create(version)
            # end with
        # end for
    # end def test_root_factory_version_out_of_range

    def test_root_factory_interfaces(self):
        """
        Check Root Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            root = RootFactory.create(version)
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
            root = RootFactory.create(version)
            self.assertEqual(root.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class RootTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
