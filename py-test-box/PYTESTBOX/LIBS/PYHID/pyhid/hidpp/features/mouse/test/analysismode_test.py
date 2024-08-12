#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.mouse.test.analysismode_test
:brief: HID++ 2.0 ``AnalysisMode`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2023/08/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pyhid.hidpp.features.mouse.analysismode import AnalysisModeFactory
from pyhid.hidpp.features.mouse.analysismode import AnalysisModeV0
from pyhid.hidpp.features.mouse.analysismode import AnalysisModeV1
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisDataV0
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisDataV1
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisDataV0Response
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisDataV1Response
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisModeV0
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisModeV1
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisModeV0Response
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisModeV1Response
from pyhid.hidpp.features.mouse.analysismode import SetAnalysisModeV0
from pyhid.hidpp.features.mouse.analysismode import SetAnalysisModeV1
from pyhid.hidpp.features.mouse.analysismode import SetAnalysisModeV0Response
from pyhid.hidpp.features.mouse.analysismode import SetAnalysisModeV1Response
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisModeInstantiationTestCase(TestCase):
    """
    Test ``AnalysisMode`` testing classes instantiations
    """

    @staticmethod
    def test_analysis_mode():
        """
        Test ``AnalysisMode`` class instantiation
        """
        my_class = AnalysisMode(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = AnalysisMode(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_analysis_mode

    @staticmethod
    def test_get_analysis_mode_v0():
        """
        Test ``GetAnalysisModeV0`` class instantiation
        """
        my_class = GetAnalysisModeV0(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetAnalysisModeV0(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_analysis_mode_v0

    @staticmethod
    def test_get_analysis_mode_v1():
        """
        Test ``GetAnalysisModeV1`` class instantiation
        """
        my_class = GetAnalysisModeV1(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetAnalysisModeV1(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_analysis_mode_v1

    @staticmethod
    def test_set_analysis_mode_v0():
        """
        Test ``SetAnalysisModeV0`` class instantiation
        """
        my_class = SetAnalysisModeV0(device_index=0, feature_index=0,
                                   mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetAnalysisModeV0(device_index=0xFF, feature_index=0xFF,
                                   mode=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_analysis_mode_v0

    @staticmethod
    def test_set_analysis_mode_v1():
        """
        Test ``SetAnalysisModeV1`` class instantiation
        """
        my_class = SetAnalysisModeV1(device_index=0, feature_index=0, mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetAnalysisModeV1(device_index=0xFF, feature_index=0xFF, mode=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_analysis_mode_v1

    @staticmethod
    def test_get_analysis_data_v0():
        """
        Test ``GetAnalysisDataV0`` class instantiation
        """
        my_class = GetAnalysisDataV0(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetAnalysisDataV0(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_analysis_data_v0

    @staticmethod
    def test_get_analysis_data_v1():
        """
        Test ``GetAnalysisDataV1`` class instantiation
        """
        my_class = GetAnalysisDataV1(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetAnalysisDataV1(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_analysis_data_v1

    @staticmethod
    def test_get_analysis_mode_v0_response():
        """
        Test ``GetAnalysisModeV0Response`` class instantiation
        """
        my_class = GetAnalysisModeV0Response(device_index=0, feature_index=0, mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAnalysisModeV0Response(device_index=0xFF, feature_index=0xFF, mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_analysis_mode_v0_response

    @staticmethod
    def test_get_analysis_mode_v1_response():
        """
        Test ``GetAnalysisModeV1Response`` class instantiation
        """
        my_class = GetAnalysisModeV1Response(device_index=0, feature_index=0, mode=0, overflow=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAnalysisModeV1Response(device_index=0xFF, feature_index=0xFF, mode=0xFF, overflow=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_analysis_mode_v1_response

    @staticmethod
    def test_set_analysis_mode_v0_response():
        """
        Test ``SetAnalysisModeV0Response`` class instantiation
        """
        my_class = SetAnalysisModeV0Response(device_index=0, feature_index=0, mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetAnalysisModeV0Response(device_index=0xFF, feature_index=0xFF, mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_analysis_mode_v0_response

    @staticmethod
    def test_set_analysis_mode_v1_response():
        """
        Test ``SetAnalysisModeV1Response`` class instantiation
        """
        my_class = SetAnalysisModeV1Response(device_index=0, feature_index=0, mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetAnalysisModeV1Response(device_index=0xFF, feature_index=0xFF, mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_analysis_mode_v1_response

    @staticmethod
    def test_get_analysis_data_v0_response():
        """
        Test ``GetAnalysisDataV0Response`` class instantiation
        """
        my_class = GetAnalysisDataV0Response(device_index=0, feature_index=0, data=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAnalysisDataV0Response(device_index=0xFF, feature_index=0xFF,
                                             data=HexList("FF" * (GetAnalysisDataV0Response.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_analysis_data_v0_response

    @staticmethod
    def test_get_analysis_data_v1_response():
        """
        Test ``GetAnalysisDataV1Response`` class instantiation
        """
        my_class = GetAnalysisDataV1Response(device_index=0, feature_index=0, data=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAnalysisDataV1Response(device_index=0xFF, feature_index=0xFF,
                                             data=HexList("FF" * (GetAnalysisDataV0Response.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_analysis_data_v1_response
# end class AnalysisModeInstantiationTestCase


class AnalysisModeTestCase(TestCase):
    """
    Test ``AnalysisMode`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            AnalysisModeV0.VERSION: {
                "cls": AnalysisModeV0,
                "interfaces": {
                    "get_analysis_mode_cls": GetAnalysisModeV0,
                    "get_analysis_mode_response_cls": GetAnalysisModeV0Response,
                    "set_analysis_mode_cls": SetAnalysisModeV0,
                    "set_analysis_mode_response_cls": SetAnalysisModeV0Response,
                    "get_analysis_data_cls": GetAnalysisDataV0,
                    "get_analysis_data_response_cls": GetAnalysisDataV0Response,
                },
                "max_function_index": 2
            },
            AnalysisModeV1.VERSION: {
                "cls": AnalysisModeV1,
                "interfaces": {
                    "get_analysis_mode_cls": GetAnalysisModeV1,
                    "get_analysis_mode_response_cls": GetAnalysisModeV1Response,
                    "set_analysis_mode_cls": SetAnalysisModeV1,
                    "set_analysis_mode_response_cls": SetAnalysisModeV1Response,
                    "get_analysis_data_cls": GetAnalysisDataV1,
                    "get_analysis_data_response_cls": GetAnalysisDataV1Response,
                },
                "max_function_index": 2
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``AnalysisModeFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(AnalysisModeFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``AnalysisModeFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                AnalysisModeFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``AnalysisModeFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = AnalysisModeFactory.create(version)
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
            obj = AnalysisModeFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class AnalysisModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
