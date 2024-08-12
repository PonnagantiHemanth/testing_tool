#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.test.extendedadjustablereportrate_test
:brief: HID++ 2.0 ``ExtendedAdjustableReportRate`` test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRateFactory
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRateV0
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import GetActualReportRateList
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import GetActualReportRateListResponse
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import GetDeviceCapabilities
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import GetDeviceCapabilitiesResponse
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import GetReportRate
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import GetReportRateResponse
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ReportRateInfoEvent
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import SetReportRate
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import SetReportRateResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableReportRateInstantiationTestCase(TestCase):
    """
    Test ``ExtendedAdjustableReportRate`` testing classes instantiations
    """

    @staticmethod
    def test_extended_adjustable_report_rate():
        """
        Test ``ExtendedAdjustableReportRate`` class instantiation
        """
        my_class = ExtendedAdjustableReportRate(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ExtendedAdjustableReportRate(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_extended_adjustable_report_rate

    @staticmethod
    def test_get_device_capabilities():
        """
        Test ``GetDeviceCapabilities`` class instantiation
        """
        my_class = GetDeviceCapabilities(device_index=0, feature_index=0,
                                         connection_type=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDeviceCapabilities(device_index=0xff, feature_index=0xff,
                                         connection_type=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_device_capabilities

    @staticmethod
    def test_get_device_capabilities_response():
        """
        Test ``GetDeviceCapabilitiesResponse`` class instantiation
        """
        my_class = GetDeviceCapabilitiesResponse(device_index=0, feature_index=0,
                                                 rate_8khz=False,
                                                 rate_4khz=False,
                                                 rate_2khz=False,
                                                 rate_1khz=False,
                                                 rate_500hz=False,
                                                 rate_250hz=False,
                                                 rate_125hz=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceCapabilitiesResponse(device_index=0xff, feature_index=0xff,
                                                 rate_8khz=True,
                                                 rate_4khz=True,
                                                 rate_2khz=True,
                                                 rate_1khz=True,
                                                 rate_500hz=True,
                                                 rate_250hz=True,
                                                 rate_125hz=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_capabilities_response

    @staticmethod
    def test_get_actual_report_rate_list():
        """
        Test ``GetActualReportRateList`` class instantiation
        """
        my_class = GetActualReportRateList(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetActualReportRateList(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_actual_report_rate_list

    @staticmethod
    def test_get_actual_report_rate_list_response():
        """
        Test ``GetActualReportRateListResponse`` class instantiation
        """
        my_class = GetActualReportRateListResponse(device_index=0, feature_index=0,
                                                   rate_8khz=False,
                                                   rate_4khz=False,
                                                   rate_2khz=False,
                                                   rate_1khz=False,
                                                   rate_500hz=False,
                                                   rate_250hz=False,
                                                   rate_125hz=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetActualReportRateListResponse(device_index=0xff, feature_index=0xff,
                                                   rate_8khz=True,
                                                   rate_4khz=True,
                                                   rate_2khz=True,
                                                   rate_1khz=True,
                                                   rate_500hz=True,
                                                   rate_250hz=True,
                                                   rate_125hz=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_actual_report_rate_list_response

    @staticmethod
    def test_get_report_rate():
        """
        Test ``GetReportRate`` class instantiation
        """
        my_class = GetReportRate(device_index=0, feature_index=0,
                                 connection_type=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetReportRate(device_index=0xff, feature_index=0xff,
                                 connection_type=0xff)

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

    @staticmethod
    def test_report_rate_info_event():
        """
        Test ``ReportRateInfoEvent`` class instantiation
        """
        my_class = ReportRateInfoEvent(device_index=0, feature_index=0,
                                       connection_type=0,
                                       report_rate=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReportRateInfoEvent(device_index=0xff, feature_index=0xff,
                                       connection_type=0xff,
                                       report_rate=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_report_rate_info_event
# end class ExtendedAdjustableReportRateInstantiationTestCase


class ExtendedAdjustableReportRateTestCase(TestCase):
    """
    Test ``ExtendedAdjustableReportRate`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ExtendedAdjustableReportRateV0.VERSION: {
                "cls": ExtendedAdjustableReportRateV0,
                "interfaces": {
                    "get_device_capabilities_cls": GetDeviceCapabilities,
                    "get_device_capabilities_response_cls": GetDeviceCapabilitiesResponse,
                    "get_actual_report_rate_list_cls": GetActualReportRateList,
                    "get_actual_report_rate_list_response_cls": GetActualReportRateListResponse,
                    "get_report_rate_cls": GetReportRate,
                    "get_report_rate_response_cls": GetReportRateResponse,
                    "set_report_rate_cls": SetReportRate,
                    "set_report_rate_response_cls": SetReportRateResponse,
                    "report_rate_info_event_cls": ReportRateInfoEvent,
                },
                "max_function_index": 3
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ExtendedAdjustableReportRateFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ExtendedAdjustableReportRateFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ExtendedAdjustableReportRateFactory`` using out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                ExtendedAdjustableReportRateFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ExtendedAdjustableReportRateFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = ExtendedAdjustableReportRateFactory.create(version)
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
            obj = ExtendedAdjustableReportRateFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ExtendedAdjustableReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
