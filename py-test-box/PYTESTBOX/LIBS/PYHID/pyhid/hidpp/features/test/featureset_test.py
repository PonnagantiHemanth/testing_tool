#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.test.featureset_test

@brief  HID++ 2.0 FeatureSet test module

@author christophe.roquebert

@date   2019/04/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.features.featureset import FeatureSet
from pyhid.hidpp.features.featureset import FeatureSetModel
from pyhid.hidpp.features.featureset import FeatureSetInterface
from pyhid.hidpp.features.featureset import FeatureSetFactory
from pyhid.hidpp.features.featureset import FeatureSetV0
from pyhid.hidpp.features.featureset import FeatureSetV1
from pyhid.hidpp.features.featureset import FeatureSetV2
from pyhid.hidpp.features.featureset import GetFeatureID
from pyhid.hidpp.features.featureset import GetCount
from pyhid.hidpp.features.featureset import GetFeatureIDResponse
from pyhid.hidpp.features.featureset import GetFeatureIDv1Response
from pyhid.hidpp.features.featureset import GetFeatureIDv2Response
from pyhid.hidpp.features.featureset import GetCountResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class FeatureSetTestCase(TestCase):
    """
    FeatureSet testing class
    """

    def test_feature_set(self):
        """
        Tests FeatureSet class instantiation
        """
        my_class = FeatureSet(deviceIndex=0,
                              featureIndex=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_feature_set

    def test_get_feature_id(self):
        """
        Tests GetFeatureID class instantiation
        """
        my_class = GetFeatureID(deviceIndex=0,
                                featureId=0,
                                feature_index_to_get=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_root_get_feature

    def test_get_count(self):
        """
        Tests GetCount class instantiation
        """
        my_class = GetCount(deviceIndex=0,
                            featureId=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_count

    def test_get_feature_id_response(self):
        """
        Tests GetFeatureID class instantiation
        """
        my_class = GetFeatureIDResponse(deviceIndex=0,
                                        featureId=0,
                                        feature_id=0,
                                        obsolete=0,
                                        sw_hidden=0,
                                        engineering_hidden=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_feature_id_response

    def test_get_feature_id_v1_response(self):
        """
        Tests GetFeatureID class instantiation
        """
        my_class = GetFeatureIDv1Response(deviceIndex=0,
                                          featureId=0,
                                          feature_id=0,
                                          obsolete=0,
                                          sw_hidden=0,
                                          engineering_hidden=0,
                                          feature_version=0)

        RootTestCase._long_function_class_checker(my_class)
        # CheckHexList part of the checks list
        my_class.feature_id = HexList('1E00')
    # end def test_get_feature_id_v1_response

    def test_get_count_response(self):
        """
        Tests GetCount class instantiation
        """
        my_class = GetCountResponse(deviceIndex=0,
                                    featureId=0,
                                    count=0x99
                                    )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_count_response

# end class FeatureSetTestCase


class FeatureSetFactoryTestCase(TestCase):
    """
    FeatureSet factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": FeatureSetV0,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_feature_id_cls": GetFeatureID,
                    "get_count_response_cls": GetCountResponse,
                    "get_feature_id_response_cls": GetFeatureIDResponse,
                },
                "max_function_index": 1
            },
            1: {
                "cls": FeatureSetV1,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_feature_id_cls": GetFeatureID,
                    "get_count_response_cls": GetCountResponse,
                    "get_feature_id_response_cls": GetFeatureIDv1Response,
                },
                "max_function_index": 1
            },
            2: {
                "cls": FeatureSetV2,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_feature_id_cls": GetFeatureID,
                    "get_count_response_cls": GetCountResponse,
                    "get_feature_id_response_cls": GetFeatureIDv2Response,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_feature_set_factory(self):
        """
        Tests FeatureSet Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(FeatureSetFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_feature_set_factory

    def test_feature_set_factory_version_out_of_range(self):
        """
        Tests FeatureSet Factory with out of range versions
        """
        for version in [3, 4]:
            with self.assertRaises(KeyError):
                FeatureSetFactory.create(version)
            # end with
        # end for
    # end def test_feature_set_factory_version_out_of_range

    def test_feature_set_factory_interfaces(self):
        """
        Check FeatureSet Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            feature_set = FeatureSetFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(feature_set, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(feature_set, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_feature_set_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            feature_set = FeatureSetFactory.create(version)
            self.assertEqual(feature_set.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class FeatureSetFactoryTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
