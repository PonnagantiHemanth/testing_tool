#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.test.reportrate_test
:brief: HID++ 2.0 ``ReportRate`` test module
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2022/04/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.reportrate import GetReportRate
from pyhid.hidpp.features.gaming.reportrate import GetReportRateList
from pyhid.hidpp.features.gaming.reportrate import GetReportRateListResponse
from pyhid.hidpp.features.gaming.reportrate import GetReportRateResponse
from pyhid.hidpp.features.gaming.reportrate import ReportRate
from pyhid.hidpp.features.gaming.reportrate import ReportRateFactory
from pyhid.hidpp.features.gaming.reportrate import ReportRateV0
from pyhid.hidpp.features.gaming.reportrate import SetReportRate
from pyhid.hidpp.features.gaming.reportrate import SetReportRateResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReportRateInstantiationTestCase(TestCase):
    """
    Test ``ReportRate`` testing classes instantiations
    """

    @staticmethod
    def test_report_rate():
        """
        Test ``ReportRate`` class instantiation
        """
        my_class = ReportRate(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ReportRate(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_report_rate

    @staticmethod
    def test_get_report_rate_list():
        """
        Test ``GetReportRateList`` class instantiation
        """
        my_class = GetReportRateList(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetReportRateList(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_report_rate_list

    @staticmethod
    def test_get_report_rate_list_response():
        """
        Test ``GetReportRateListResponse`` class instantiation
        """
        my_class = GetReportRateListResponse(device_index=0, feature_index=0,
                                             report_rate_list=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetReportRateListResponse(device_index=0xff, feature_index=0xff,
                                             report_rate_list=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_report_rate_list_response

    @staticmethod
    def test_get_report_rate():
        """
        Test ``GetReportRate`` class instantiation
        """
        my_class = GetReportRate(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetReportRate(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_report_rate

    @staticmethod
    def test_get_report_rate_response():
        """
        Test ``GetReportRateResponse`` class instantiation
        """
        my_class = GetReportRateResponse(device_index=0, feature_index=0,
                                         report_rate=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetReportRateResponse(device_index=0xff, feature_index=0xff,
                                         report_rate=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_report_rate_response

    @staticmethod
    def test_set_report_rate():
        """
        Test ``SetReportRate`` class instantiation
        """
        my_class = SetReportRate(device_index=0, feature_index=0,
                                 report_rate=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetReportRate(device_index=0xff, feature_index=0xff,
                                 report_rate=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_report_rate

    @staticmethod
    def test_set_report_rate_response():
        """
        Test ``SetReportRateResponse`` class instantiation
        """
        my_class = SetReportRateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetReportRateResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_report_rate_response
# end class ReportRateInstantiationTestCase


class ReportRateTestCase(TestCase):
    """
    Test ``ReportRate`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ReportRateV0.VERSION: {
                "cls": ReportRateV0,
                "interfaces": {
                    "get_report_rate_list_cls": GetReportRateList,
                    "get_report_rate_list_response_cls": GetReportRateListResponse,
                    "get_report_rate_cls": GetReportRate,
                    "get_report_rate_response_cls": GetReportRateResponse,
                    "set_report_rate_cls": SetReportRate,
                    "set_report_rate_response_cls": SetReportRateResponse,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ReportRateFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ReportRateFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ReportRateFactory`` using out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                ReportRateFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ReportRateFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = ReportRateFactory.create(version)
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
        """
        for version, expected in self.expected.items():
            obj = ReportRateFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
