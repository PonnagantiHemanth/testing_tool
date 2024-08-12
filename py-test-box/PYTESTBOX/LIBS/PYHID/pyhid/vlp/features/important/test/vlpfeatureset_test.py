#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.vlp.features.important.test.vlpfeatureset_test
:brief: VLP 1.0 ``VLPFeatureSet`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2024/05/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.vlp.features.important.vlpfeatureset import GetAllFeatureIDs
from pyhid.vlp.features.important.vlpfeatureset import GetAllFeatureIDsResponsePayloadMixin
from pyhid.vlp.features.important.vlpfeatureset import GetAllFeatureIDsResponse
from pyhid.vlp.features.important.vlpfeatureset import GetCount
from pyhid.vlp.features.important.vlpfeatureset import GetCountResponse
from pyhid.vlp.features.important.vlpfeatureset import GetFeatureID
from pyhid.vlp.features.important.vlpfeatureset import GetFeatureIDResponse
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSet
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSetFactory
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSetV0
from pyhid.vlp.features.test.vlp_root_test import VLPRootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class VLPFeatureSetInstantiationTestCase(TestCase):
    """
    Test ``VLPFeatureSet`` testing classes instantiations
    """

    @staticmethod
    def test_vlp_feature_set():
        """
        Test ``VLPFeatureSet`` class instantiation
        """
        my_class = VLPFeatureSet(device_index=0, feature_index=0)

        VLPRootTestCase._top_level_class_checker(my_class)

        my_class = VLPFeatureSet(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._top_level_class_checker(my_class)
    # end def test_vlp_feature_set

    @staticmethod
    def test_get_count():
        """
        Test ``GetCount`` class instantiation
        """
        my_class = GetCount(device_index=0, feature_index=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetCount(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_count

    @staticmethod
    def test_get_feature_id():
        """
        Test ``GetFeatureID`` class instantiation
        """
        my_class = GetFeatureID(device_index=0, feature_index=0, feature_idx=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetFeatureID(
            device_index=0xFF, feature_index=0xFF, feature_idx=HexList("FF" * (GetFeatureID.LEN.FEATURE_IDX // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_feature_id

    @staticmethod
    def test_get_all_feature_ids():
        """
        Test ``GetAllFeatureIDs`` class instantiation
        """
        my_class = GetAllFeatureIDs(device_index=0, feature_index=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetAllFeatureIDs(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_all_feature_ids

    @staticmethod
    def test_get_count_response():
        """
        Test ``GetCountResponse`` class instantiation
        """
        my_class = GetCountResponse(device_index=0, feature_index=0, count=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetCountResponse(device_index=0xFF, feature_index=0xFF, count=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_count_response

    @staticmethod
    def test_get_feature_id_response():
        """
        Test ``GetFeatureIDResponse`` class instantiation
        """
        my_class = GetFeatureIDResponse(
            device_index=0, feature_index=0,
            feature_idx=HexList(0),
            feature_id=HexList("00" * (GetFeatureIDResponse.LEN.FEATURE_ID // 8)),
            feature_hidden=False,
            feature_version=0,
            feature_max_memory=HexList("00" * (GetFeatureIDResponse.LEN.FEATURE_MAX_MEMORY // 8)))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetFeatureIDResponse(
            device_index=0xFF, feature_index=0xFF,
            feature_idx=HexList("FF" * (GetFeatureIDResponse.LEN.FEATURE_IDX // 8)),
            feature_id=HexList("FF" * (GetFeatureIDResponse.LEN.FEATURE_ID // 8)),
            feature_hidden=True,
            feature_version=0xFF,
            feature_max_memory=HexList("FF" * (GetFeatureIDResponse.LEN.FEATURE_MAX_MEMORY // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_feature_id_response

    @staticmethod
    def test_get_all_feature_ids_response():
        """
        Test ``GetAllFeatureIDsResponse`` class instantiation
        """
        my_class = GetAllFeatureIDsResponse(device_index=0, feature_index=0, vlp_payload=HexList("00"))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetAllFeatureIDsResponse(device_index=0xFF, feature_index=0xFF, vlp_payload=HexList("FF"))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_all_feature_ids_response

    @staticmethod
    def test_get_all_feature_ids_response_payload_mixin():
        """
        Test ``GetAllFeatureIDsResponsePayloadMixin`` class instantiation
        """
        my_class = GetAllFeatureIDsResponsePayloadMixin(
            feature_records_count=HexList("01"), feature_records_size=HexList("01"), feature_records=HexList("00"))

        assert HexList(my_class) == HexList("01", "01", "00")

        my_class = GetAllFeatureIDsResponsePayloadMixin(
            feature_records_count=HexList("FF"), feature_records_size=HexList("FF"),
            feature_records=HexList("FF") * 0xFF)

        assert HexList(my_class) == HexList("FF", "FF", "FF" * 0xFF)
    # end def test_get_all_feature_ids_response_payload_mixin
# end class VLPFeatureSetInstantiationTestCase


class VLPFeatureSetTestCase(TestCase):
    """
    Test ``VLPFeatureSet`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            VLPFeatureSetV0.VERSION: {
                "cls": VLPFeatureSetV0,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_count_response_cls": GetCountResponse,
                    "get_feature_id_cls": GetFeatureID,
                    "get_feature_id_response_cls": GetFeatureIDResponse,
                    "get_all_feature_ids_cls": GetAllFeatureIDs,
                    "get_all_feature_ids_response_cls": GetAllFeatureIDsResponse,
                },
                "max_function_index": 2
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``VLPFeatureSetFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(VLPFeatureSetFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``VLPFeatureSetFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                VLPFeatureSetFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``VLPFeatureSetFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = VLPFeatureSetFactory.create(version)
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
            obj = VLPFeatureSetFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class VLPFeatureSetTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
