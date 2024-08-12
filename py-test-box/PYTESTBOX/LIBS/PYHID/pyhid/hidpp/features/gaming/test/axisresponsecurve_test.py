#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.test.axisresponsecurve_test
:brief: HID++ 2.0 ``AxisResponseCurve`` test module
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/03/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurve
from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurveFactory
from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurveV0
from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurveV1
from pyhid.hidpp.features.gaming.axisresponsecurve import GetAxisInfo
from pyhid.hidpp.features.gaming.axisresponsecurve import GetAxisInfoResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import GetAxisPoints
from pyhid.hidpp.features.gaming.axisresponsecurve import GetAxisPointsResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import GetCalculatedValue
from pyhid.hidpp.features.gaming.axisresponsecurve import GetCalculatedValueResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import GetInfo
from pyhid.hidpp.features.gaming.axisresponsecurve import GetInfoResponseV0
from pyhid.hidpp.features.gaming.axisresponsecurve import GetInfoResponseV1
from pyhid.hidpp.features.gaming.axisresponsecurve import ResetAxis
from pyhid.hidpp.features.gaming.axisresponsecurve import ResetAxisResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import SetAxisPoints
from pyhid.hidpp.features.gaming.axisresponsecurve import SetAxisPointsResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import StartUpdate
from pyhid.hidpp.features.gaming.axisresponsecurve import StartUpdateResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import StopUpdate
from pyhid.hidpp.features.gaming.axisresponsecurve import StopUpdateResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import SaveToNVS
from pyhid.hidpp.features.gaming.axisresponsecurve import SaveToNVSResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import ReloadFromNVS
from pyhid.hidpp.features.gaming.axisresponsecurve import ReloadFromNVSResponse
from pyhid.hidpp.features.gaming.axisresponsecurve import SaveCompleteEvent
from pyhid.hidpp.features.gaming.axisresponsecurve import ReloadCompleteEvent
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AxisResponseCurveInstantiationTestCase(TestCase):
    """
    Test ``AxisResponseCurve`` testing classes instantiations
    """

    @staticmethod
    def test_axis_response_curve():
        """
        Test ``AxisResponseCurve`` class instantiation
        """
        my_class = AxisResponseCurve(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = AxisResponseCurve(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_axis_response_curve

    @staticmethod
    def test_get_info():
        """
        Test ``GetInfo`` class instantiation
        """
        my_class = GetInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info

    @staticmethod
    def test_get_info_response_V0():
        """
        Test ``GetInfoResponseV0`` class instantiation
        """
        my_class = GetInfoResponseV0(device_index=0, feature_index=0,
                                     axis_count=0,
                                     max_get_point_count=0,
                                     max_set_point_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponseV0(device_index=0xff, feature_index=0xff,
                                     axis_count=0xff,
                                     max_get_point_count=0xff,
                                     max_set_point_count=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response_V0

    @staticmethod
    def test_get_info_response_V1():
        """
        Test ``GetInfoResponseV1`` class instantiation
        """
        my_class = GetInfoResponseV1(device_index=0, feature_index=0,
                                     axis_count=0,
                                     max_get_point_count=0,
                                     max_set_point_count=0,
                                     capabilities=False
                                     )

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponseV1(device_index=0xff, feature_index=0xff,
                                     axis_count=0xff,
                                     max_get_point_count=0xff,
                                     max_set_point_count=0xff,
                                     capabilities=True
                                     )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response_V1

    @staticmethod
    def test_get_axis_info():
        """
        Test ``GetAxisInfo`` class instantiation
        """
        my_class = GetAxisInfo(device_index=0, feature_index=0,
                               axis_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetAxisInfo(device_index=0xff, feature_index=0xff,
                               axis_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_axis_info

    @staticmethod
    def test_get_axis_info_response():
        """
        Test ``GetAxisInfoResponse`` class instantiation
        """
        my_class = GetAxisInfoResponse(device_index=0, feature_index=0,
                                       axis_index=0,
                                       hid_usage_page=0,
                                       hid_usage=0,
                                       axis_resolution=0,
                                       active_point_count=0,
                                       max_point_count=0,
                                       properties=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAxisInfoResponse(device_index=0xff, feature_index=0xff,
                                       axis_index=0xff,
                                       hid_usage_page=0xffff,
                                       hid_usage=0xffff,
                                       axis_resolution=0xff,
                                       active_point_count=0xffff,
                                       max_point_count=0xffff,
                                       properties=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_axis_info_response

    @staticmethod
    def test_get_axis_points():
        """
        Test ``GetAxisPoints`` class instantiation
        """
        my_class = GetAxisPoints(device_index=0, feature_index=0,
                                 axis_index=0,
                                 point_index=0,
                                 point_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAxisPoints(device_index=0xff, feature_index=0xff,
                                 axis_index=0xff,
                                 point_index=0xffff,
                                 point_count=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_axis_points

    @staticmethod
    def test_get_axis_points_response():
        """
        Test ``GetAxisPointsResponse`` class instantiation
        """
        my_class = GetAxisPointsResponse(device_index=0, feature_index=0,
                                         axis_index=0,
                                         point_index=0,
                                         point_count=0,
                                         axis_points=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetAxisPointsResponse(device_index=0xff, feature_index=0xff,
                                         axis_index=0xff,
                                         point_index=0xffff,
                                         point_count=0xff,
                                         axis_points=0xffffffffffffffffffffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_axis_points_response

    @staticmethod
    def test_start_update():
        """
        Test ``StartUpdate`` class instantiation
        """
        my_class = StartUpdate(device_index=0, feature_index=0,
                               axis_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StartUpdate(device_index=0xff, feature_index=0xff,
                               axis_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_start_update

    @staticmethod
    def test_start_update_response():
        """
        Test ``StartUpdateResponse`` class instantiation
        """
        my_class = StartUpdateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartUpdateResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_update_response

    @staticmethod
    def test_set_axis_points():
        """
        Test ``SetAxisPoints`` class instantiation
        """
        my_class = SetAxisPoints(device_index=0, feature_index=0,
                                 point_count=0,
                                 axis_points=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetAxisPoints(device_index=0xff, feature_index=0xff,
                                 point_count=0xff,
                                 axis_points=0xffffffffffffffffffffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_axis_points

    @staticmethod
    def test_set_axis_points_response():
        """
        Test ``SetAxisPointsResponse`` class instantiation
        """
        my_class = SetAxisPointsResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetAxisPointsResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_axis_points_response

    @staticmethod
    def test_stop_update():
        """
        Test ``StopUpdate`` class instantiation
        """
        my_class = StopUpdate(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StopUpdate(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_stop_update

    @staticmethod
    def test_stop_update_response():
        """
        Test ``StopUpdateResponse`` class instantiation
        """
        my_class = StopUpdateResponse(device_index=0, feature_index=0,
                                      axis_index=0,
                                      status=0,
                                      active_point_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StopUpdateResponse(device_index=0xff, feature_index=0xff,
                                      axis_index=0xff,
                                      status=0xff,
                                      active_point_count=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_stop_update_response

    @staticmethod
    def test_reset_axis():
        """
        Test ``ResetAxis`` class instantiation
        """
        my_class = ResetAxis(device_index=0, feature_index=0,
                             axis_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ResetAxis(device_index=0xff, feature_index=0xff,
                             axis_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reset_axis

    @staticmethod
    def test_reset_axis_response():
        """
        Test ``ResetAxisResponse`` class instantiation
        """
        my_class = ResetAxisResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ResetAxisResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reset_axis_response

    @staticmethod
    def test_get_calculated_value():
        """
        Test ``GetCalculatedValue`` class instantiation
        """
        my_class = GetCalculatedValue(device_index=0, feature_index=0,
                                      axis_index=0,
                                      input_value=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCalculatedValue(device_index=0xff, feature_index=0xff,
                                      axis_index=0xff,
                                      input_value=0xffff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_calculated_value

    @staticmethod
    def test_get_calculated_value_response():
        """
        Test ``GetCalculatedValueResponse`` class instantiation
        """
        my_class = GetCalculatedValueResponse(device_index=0, feature_index=0,
                                              axis_index=0,
                                              input_value=0,
                                              calculated_value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCalculatedValueResponse(device_index=0xff, feature_index=0xff,
                                              axis_index=0xff,
                                              input_value=0xffff,
                                              calculated_value=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_calculated_value_response

    @staticmethod
    def test_save_to_nvs():
        """
        Test ``SaveToNvs`` class instantiation
        """
        my_class = SaveToNVS(device_index=0, feature_index=0, axis_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SaveToNVS(device_index=0xff, feature_index=0xff, axis_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_save_to_nvs

    @staticmethod
    def test_save_to_nvs_response():
        """
        Test ``SaveToNvsResponse`` class instantiation
        """
        my_class = SaveToNVSResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SaveToNVSResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_save_to_nvs_response

    @staticmethod
    def test_reload_from_nvs():
        """
        Test ``ReloadFromNvs`` class instantiation
        """
        my_class = ReloadFromNVS(device_index=0, feature_index=0, axis_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReloadFromNVS(device_index=0xff, feature_index=0xff, axis_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reload_from_nvs

    @staticmethod
    def test_reload_from_nvs_response():
        """
        Test ``ReloadFromNvsResponse`` class instantiation
        """
        my_class = ReloadFromNVSResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReloadFromNVSResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reload_from_nvs_response

    @staticmethod
    def test_save_complete_event():
        """
        Test ``SaveCompleteEvent`` class instantiation
        """
        my_class = SaveCompleteEvent(device_index=0, feature_index=0, axis_index=0, status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SaveCompleteEvent(device_index=0xff, feature_index=0xff, axis_index=0xff, status=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_save_complete_event

    @staticmethod
    def test_reload_complete_event():
        """
        Test ``ReloadCompleteEvent`` class instantiation
        """
        my_class = ReloadCompleteEvent(device_index=0, feature_index=0, axis_index=0, status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReloadCompleteEvent(device_index=0xff, feature_index=0xff, axis_index=0xff, status=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reload_complete_event
# end class AxisResponseCurveInstantiationTestCase


class AxisResponseCurveTestCase(TestCase):
    """
    Test ``AxisResponseCurve`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            AxisResponseCurveV0.VERSION: {
                "cls": AxisResponseCurveV0,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponseV0,
                    "get_axis_info_cls": GetAxisInfo,
                    "get_axis_info_response_cls": GetAxisInfoResponse,
                    "get_axis_points_cls": GetAxisPoints,
                    "get_axis_points_response_cls": GetAxisPointsResponse,
                    "start_update_cls": StartUpdate,
                    "start_update_response_cls": StartUpdateResponse,
                    "set_axis_points_cls": SetAxisPoints,
                    "set_axis_points_response_cls": SetAxisPointsResponse,
                    "stop_update_cls": StopUpdate,
                    "stop_update_response_cls": StopUpdateResponse,
                    "reset_axis_cls": ResetAxis,
                    "reset_axis_response_cls": ResetAxisResponse,
                    "get_calculated_value_cls": GetCalculatedValue,
                    "get_calculated_value_response_cls": GetCalculatedValueResponse,
                },
                "max_function_index": 7
            },
            AxisResponseCurveV1.VERSION: {
                "cls": AxisResponseCurveV1,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponseV1,
                    "get_axis_info_cls": GetAxisInfo,
                    "get_axis_info_response_cls": GetAxisInfoResponse,
                    "get_axis_points_cls": GetAxisPoints,
                    "get_axis_points_response_cls": GetAxisPointsResponse,
                    "start_update_cls": StartUpdate,
                    "start_update_response_cls": StartUpdateResponse,
                    "set_axis_points_cls": SetAxisPoints,
                    "set_axis_points_response_cls": SetAxisPointsResponse,
                    "stop_update_cls": StopUpdate,
                    "stop_update_response_cls": StopUpdateResponse,
                    "reset_axis_cls": ResetAxis,
                    "reset_axis_response_cls": ResetAxisResponse,
                    "get_calculated_value_cls": GetCalculatedValue,
                    "get_calculated_value_response_cls": GetCalculatedValueResponse,
                    "save_to_nvs_cls": SaveToNVS,
                    "save_to_nvs_response_cls": SaveToNVSResponse,
                    "reload_from_nvs_cls": ReloadFromNVS,
                    "reload_from_nvs_response_cls": ReloadFromNVSResponse,
                    "save_complete_event_cls": SaveCompleteEvent,
                    "reload_complete_event_cls": ReloadCompleteEvent,

                },
                "max_function_index": 9
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``AxisResponseCurveFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(AxisResponseCurveFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``AxisResponseCurveFactory`` using out of range versions
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                AxisResponseCurveFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``AxisResponseCurveFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = AxisResponseCurveFactory.create(version)
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
            obj = AxisResponseCurveFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class AxisResponseCurveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
