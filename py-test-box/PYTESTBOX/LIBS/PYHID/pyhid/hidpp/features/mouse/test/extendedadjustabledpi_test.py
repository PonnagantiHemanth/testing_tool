#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.mouse.test.extendedadjustabledpi_test
:brief: HID++ 2.0 ``ExtendedAdjustableDpi`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.mouse.extendedadjustabledpi import DpiCalibrationCompletedEvent
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpi
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpiFactory
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpiV0
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetDpiCalibrationInfo
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetDpiCalibrationInfoResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorCapabilities
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorCapabilitiesResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorCount
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorCountResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiList
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiListResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiParameters
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiParametersResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiRanges
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiRangesResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorLodList
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorLodListResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SensorDpiParametersEvent
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SetDpiCalibration
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SetDpiCalibrationResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SetSensorDpiParameters
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SetSensorDpiParametersResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ShowSensorDpiStatus
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ShowSensorDpiStatusResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import StartDpiCalibration
from pyhid.hidpp.features.mouse.extendedadjustabledpi import StartDpiCalibrationResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpiInstantiationTestCase(TestCase):
    """
    Test ``ExtendedAdjustableDpi`` testing classes instantiations
    """

    @staticmethod
    def test_extended_adjustable_dpi():
        """
        Test ``ExtendedAdjustableDpi`` class instantiation
        """
        my_class = ExtendedAdjustableDpi(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ExtendedAdjustableDpi(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_extended_adjustable_dpi

    @staticmethod
    def test_get_sensor_count():
        """
        Test ``GetSensorCount`` class instantiation
        """
        my_class = GetSensorCount(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorCount(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_count

    @staticmethod
    def test_get_sensor_count_response():
        """
        Test ``GetSensorCountResponse`` class instantiation
        """
        my_class = GetSensorCountResponse(device_index=0, feature_index=0, num_sensor=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorCountResponse(device_index=0xff, feature_index=0xff, num_sensor=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_count_response

    @staticmethod
    def test_get_sensor_capabilities():
        """
        Test ``GetSensorCapabilities`` class instantiation
        """
        my_class = GetSensorCapabilities(device_index=0, feature_index=0, sensor_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorCapabilities(device_index=0xff, feature_index=0xff, sensor_idx=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_capabilities

    @staticmethod
    def test_get_sensor_capabilities_response():
        """
        Test ``GetSensorCapabilitiesResponse`` class instantiation
        """
        my_class = GetSensorCapabilitiesResponse(device_index=0, feature_index=0,
                                                 sensor_idx=0,
                                                 num_dpi_levels=0,
                                                 profile_supported=False,
                                                 calibration_supported=False,
                                                 lod_supported=False,
                                                 dpi_y_supported=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorCapabilitiesResponse(device_index=0xff, feature_index=0xff,
                                                 sensor_idx=0xff,
                                                 num_dpi_levels=0xff,
                                                 profile_supported=True,
                                                 calibration_supported=True,
                                                 lod_supported=True,
                                                 dpi_y_supported=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_capabilities_response

    @staticmethod
    def test_get_sensor_dpi_ranges():
        """
        Test ``GetSensorDpiRanges`` class instantiation
        """
        my_class = GetSensorDpiRanges(device_index=0, feature_index=0,
                                      sensor_idx=0,
                                      direction=0,
                                      dpi_range_req_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorDpiRanges(device_index=0xff, feature_index=0xff,
                                      sensor_idx=0xff,
                                      direction=0xff,
                                      dpi_range_req_idx=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_dpi_ranges

    @staticmethod
    def test_get_sensor_dpi_ranges_response():
        """
        Test ``GetSensorDpiRangesResponse`` class instantiation
        """
        my_class = GetSensorDpiRangesResponse(device_index=0, feature_index=0,
                                              sensor_idx=0,
                                              direction=0,
                                              dpi_range_req_idx=0,
                                              dpi_ranges_1=0,
                                              dpi_ranges_2=0,
                                              dpi_ranges_3=0,
                                              dpi_ranges_4=0,
                                              dpi_ranges_5=0,
                                              dpi_ranges_6=0,
                                              dpi_ranges_7_msb=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorDpiRangesResponse(device_index=0xff, feature_index=0xff,
                                              sensor_idx=0xff,
                                              direction=0xff,
                                              dpi_range_req_idx=0xff,
                                              dpi_ranges_1=0xffff,
                                              dpi_ranges_2=0xffff,
                                              dpi_ranges_3=0xffff,
                                              dpi_ranges_4=0xffff,
                                              dpi_ranges_5=0xffff,
                                              dpi_ranges_6=0xffff,
                                              dpi_ranges_7_msb=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_dpi_ranges_response

    @staticmethod
    def test_get_sensor_dpi_list():
        """
        Test ``GetSensorDpiList`` class instantiation
        """
        my_class = GetSensorDpiList(device_index=0, feature_index=0, sensor_idx=0, direction=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorDpiList(device_index=0xff, feature_index=0xff, sensor_idx=0xff, direction=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_dpi_list

    @staticmethod
    def test_get_sensor_dpi_list_response():
        """
        Test ``GetSensorDpiListResponse`` class instantiation
        """
        my_class = GetSensorDpiListResponse(device_index=0, feature_index=0,
                                            sensor_idx=0,
                                            direction=0,
                                            dpi_list_1=0,
                                            dpi_list_2=0,
                                            dpi_list_3=0,
                                            dpi_list_4=0,
                                            dpi_list_5=0,
                                            dpi_list_6=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorDpiListResponse(device_index=0xff, feature_index=0xff,
                                            sensor_idx=0xff,
                                            direction=0xff,
                                            dpi_list_1=0xffff,
                                            dpi_list_2=0xffff,
                                            dpi_list_3=0xffff,
                                            dpi_list_4=0xffff,
                                            dpi_list_5=0xffff,
                                            dpi_list_6=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_dpi_list_response

    @staticmethod
    def test_get_sensor_lod_list():
        """
        Test ``GetSensorLodList`` class instantiation
        """
        my_class = GetSensorLodList(device_index=0, feature_index=0, sensor_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorLodList(device_index=0xff, feature_index=0xff, sensor_idx=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_lod_list

    @staticmethod
    def test_get_sensor_lod_list_response():
        """
        Test ``GetSensorLodListResponse`` class instantiation
        """
        my_class = GetSensorLodListResponse(device_index=0, feature_index=0,
                                            sensor_idx=0,
                                            lod_1=0,
                                            lod_2=0,
                                            lod_3=0,
                                            lod_4=0,
                                            lod_5=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorLodListResponse(device_index=0xff, feature_index=0xff,
                                            sensor_idx=0xff,
                                            lod_1=0xff,
                                            lod_2=0xff,
                                            lod_3=0xff,
                                            lod_4=0xff,
                                            lod_5=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_lod_list_response

    @staticmethod
    def test_get_sensor_dpi_parameters():
        """
        Test ``GetSensorDpiParameters`` class instantiation
        """
        my_class = GetSensorDpiParameters(device_index=0, feature_index=0, sensor_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorDpiParameters(device_index=0xff, feature_index=0xff, sensor_idx=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_dpi_parameters

    @staticmethod
    def test_get_sensor_dpi_parameters_response():
        """
        Test ``GetSensorDpiParametersResponse`` class instantiation
        """
        my_class = GetSensorDpiParametersResponse(device_index=0, feature_index=0,
                                                  sensor_idx=0,
                                                  dpi_x=0,
                                                  default_dpi_x=0,
                                                  dpi_y=0,
                                                  default_dpi_y=0,
                                                  lod=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorDpiParametersResponse(device_index=0xff, feature_index=0xff,
                                                  sensor_idx=0xff,
                                                  dpi_x=0xffff,
                                                  default_dpi_x=0xffff,
                                                  dpi_y=0xffff,
                                                  default_dpi_y=0xffff,
                                                  lod=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_dpi_parameters_response

    @staticmethod
    def test_set_sensor_dpi_parameters():
        """
        Test ``SetSensorDpiParameters`` class instantiation
        """
        my_class = SetSensorDpiParameters(device_index=0, feature_index=0,
                                          sensor_idx=0,
                                          dpi_x=0,
                                          dpi_y=0,
                                          lod=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetSensorDpiParameters(device_index=0xff, feature_index=0xff,
                                          sensor_idx=0xff,
                                          dpi_x=0xffff,
                                          dpi_y=0xffff,
                                          lod=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_sensor_dpi_parameters

    @staticmethod
    def test_set_sensor_dpi_parameters_response():
        """
        Test ``SetSensorDpiParametersResponse`` class instantiation
        """
        my_class = SetSensorDpiParametersResponse(device_index=0, feature_index=0,
                                                  sensor_idx=0,
                                                  dpi_x=0,
                                                  dpi_y=0,
                                                  lod=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetSensorDpiParametersResponse(device_index=0xff, feature_index=0xff,
                                                  sensor_idx=0xff,
                                                  dpi_x=0xffff,
                                                  dpi_y=0xffff,
                                                  lod=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_sensor_dpi_parameters_response

    @staticmethod
    def test_show_sensor_dpi_status():
        """
        Test ``ShowSensorDpiStatus`` class instantiation
        """
        my_class = ShowSensorDpiStatus(device_index=0, feature_index=0,
                                       sensor_idx=0,
                                       dpi_level=0,
                                       led_hold_type=0,
                                       button_num=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShowSensorDpiStatus(device_index=0xff, feature_index=0xff,
                                       sensor_idx=0xff,
                                       dpi_level=0xff,
                                       led_hold_type=0xff,
                                       button_num=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_show_sensor_dpi_status

    @staticmethod
    def test_show_sensor_dpi_status_response():
        """
        Test ``ShowSensorDpiStatusResponse`` class instantiation
        """
        my_class = ShowSensorDpiStatusResponse(device_index=0, feature_index=0,
                                               sensor_idx=0,
                                               dpi_level=0,
                                               led_hold_type=0,
                                               button_num=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShowSensorDpiStatusResponse(device_index=0xff, feature_index=0xff,
                                               sensor_idx=0xff,
                                               dpi_level=0xff,
                                               led_hold_type=0xff,
                                               button_num=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_show_sensor_dpi_status_response

    @staticmethod
    def test_get_dpi_calibration_info():
        """
        Test ``GetDpiCalibrationInfo`` class instantiation
        """
        my_class = GetDpiCalibrationInfo(device_index=0, feature_index=0, sensor_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDpiCalibrationInfo(device_index=0xff, feature_index=0xff, sensor_idx=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_dpi_calibration_info

    @staticmethod
    def test_get_dpi_calibration_info_response():
        """
        Test ``GetDpiCalibrationInfoResponse`` class instantiation
        """
        my_class = GetDpiCalibrationInfoResponse(device_index=0, feature_index=0,
                                                 sensor_idx=0,
                                                 mouse_width=0,
                                                 mouse_length=0,
                                                 calib_dpi_x=0,
                                                 calib_dpi_y=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDpiCalibrationInfoResponse(device_index=0xff, feature_index=0xff,
                                                 sensor_idx=0xff,
                                                 mouse_width=0xff,
                                                 mouse_length=0xffff,
                                                 calib_dpi_x=0xffff,
                                                 calib_dpi_y=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_dpi_calibration_info_response

    @staticmethod
    def test_start_dpi_calibration():
        """
        Test ``StartDpiCalibration`` class instantiation
        """
        my_class = StartDpiCalibration(device_index=0, feature_index=0,
                                       sensor_idx=0,
                                       direction=0,
                                       expected_count=0,
                                       calib_type=0,
                                       calib_start_timeout=0,
                                       calib_hw_process_timeout=0,
                                       calib_sw_process_timeout=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartDpiCalibration(device_index=0xff, feature_index=0xff,
                                       sensor_idx=0xff,
                                       direction=0xff,
                                       expected_count=0xffff,
                                       calib_type=0xff,
                                       calib_start_timeout=0xff,
                                       calib_hw_process_timeout=0xff,
                                       calib_sw_process_timeout=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_dpi_calibration

    @staticmethod
    def test_start_dpi_calibration_response():
        """
        Test ``StartDpiCalibrationResponse`` class instantiation
        """
        my_class = StartDpiCalibrationResponse(device_index=0, feature_index=0,
                                               sensor_idx=0,
                                               direction=0,
                                               expected_count=0,
                                               calib_type=0,
                                               calib_start_timeout=0,
                                               calib_hw_process_timeout=0,
                                               calib_sw_process_timeout=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartDpiCalibrationResponse(device_index=0xff, feature_index=0xff,
                                               sensor_idx=0xff,
                                               direction=0xff,
                                               expected_count=0xffff,
                                               calib_type=0xff,
                                               calib_start_timeout=0xff,
                                               calib_hw_process_timeout=0xff,
                                               calib_sw_process_timeout=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_dpi_calibration_response

    @staticmethod
    def test_set_dpi_calibration():
        """
        Test ``SetDpiCalibration`` class instantiation
        """
        my_class = SetDpiCalibration(device_index=0, feature_index=0,
                                     sensor_idx=0,
                                     direction=0,
                                     calib_cor=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDpiCalibration(device_index=0xff, feature_index=0xff,
                                     sensor_idx=0xff,
                                     direction=0xff,
                                     calib_cor=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_dpi_calibration

    @staticmethod
    def test_set_dpi_calibration_response():
        """
        Test ``SetDpiCalibrationResponse`` class instantiation
        """
        my_class = SetDpiCalibrationResponse(device_index=0, feature_index=0,
                                             sensor_idx=0,
                                             direction=0,
                                             calib_cor=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDpiCalibrationResponse(device_index=0xff, feature_index=0xff,
                                             sensor_idx=0xff,
                                             direction=0xff,
                                             calib_cor=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_dpi_calibration_response

    @staticmethod
    def test_sensor_dpi_parameters_event():
        """
        Test ``SensorDpiParametersEvent`` class instantiation
        """
        my_class = SensorDpiParametersEvent(device_index=0, feature_index=0,
                                            sensor_idx=0,
                                            dpi_x=0,
                                            dpi_y=0,
                                            lod=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SensorDpiParametersEvent(device_index=0xff, feature_index=0xff,
                                            sensor_idx=0xff,
                                            dpi_x=0xffff,
                                            dpi_y=0xffff,
                                            lod=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_sensor_dpi_parameters_event

    @staticmethod
    def test_dpi_calibration_completed_event():
        """
        Test ``DpiCalibrationCompletedEvent`` class instantiation
        """
        my_class = DpiCalibrationCompletedEvent(device_index=0, feature_index=0,
                                                sensor_idx=0,
                                                direction=0,
                                                calib_cor=0,
                                                calib_delta=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DpiCalibrationCompletedEvent(device_index=0xff, feature_index=0xff,
                                                sensor_idx=0xff,
                                                direction=0xff,
                                                calib_cor=0xffff,
                                                calib_delta=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dpi_calibration_completed_event
# end class ExtendedAdjustableDpiInstantiationTestCase


class ExtendedAdjustableDpiTestCase(TestCase):
    """
    Test ``ExtendedAdjustableDpi`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ExtendedAdjustableDpiV0.VERSION: {
                "cls": ExtendedAdjustableDpiV0,
                "interfaces": {
                    "get_sensor_count_cls": GetSensorCount,
                    "get_sensor_count_response_cls": GetSensorCountResponse,
                    "get_sensor_capabilities_cls": GetSensorCapabilities,
                    "get_sensor_capabilities_response_cls": GetSensorCapabilitiesResponse,
                    "get_sensor_dpi_ranges_cls": GetSensorDpiRanges,
                    "get_sensor_dpi_ranges_response_cls": GetSensorDpiRangesResponse,
                    "get_sensor_dpi_list_cls": GetSensorDpiList,
                    "get_sensor_dpi_list_response_cls": GetSensorDpiListResponse,
                    "get_sensor_lod_list_cls": GetSensorLodList,
                    "get_sensor_lod_list_response_cls": GetSensorLodListResponse,
                    "get_sensor_dpi_parameters_cls": GetSensorDpiParameters,
                    "get_sensor_dpi_parameters_response_cls": GetSensorDpiParametersResponse,
                    "set_sensor_dpi_parameters_cls": SetSensorDpiParameters,
                    "set_sensor_dpi_parameters_response_cls": SetSensorDpiParametersResponse,
                    "show_sensor_dpi_status_cls": ShowSensorDpiStatus,
                    "show_sensor_dpi_status_response_cls": ShowSensorDpiStatusResponse,
                    "get_dpi_calibration_info_cls": GetDpiCalibrationInfo,
                    "get_dpi_calibration_info_response_cls": GetDpiCalibrationInfoResponse,
                    "start_dpi_calibration_cls": StartDpiCalibration,
                    "start_dpi_calibration_response_cls": StartDpiCalibrationResponse,
                    "set_dpi_calibration_cls": SetDpiCalibration,
                    "set_dpi_calibration_response_cls": SetDpiCalibrationResponse,
                    "sensor_dpi_parameters_event_cls": SensorDpiParametersEvent,
                    "dpi_calibration_completed_event_cls": DpiCalibrationCompletedEvent,
                },
                "max_function_index": 10
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ExtendedAdjustableDpiFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ExtendedAdjustableDpiFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ExtendedAdjustableDpiFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                ExtendedAdjustableDpiFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ExtendedAdjustableDpiFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ExtendedAdjustableDpiFactory.create(version)
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
            obj = ExtendedAdjustableDpiFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ExtendedAdjustableDpiTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
