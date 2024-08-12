#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.peripheral.test.ads1231_test
:brief: HID++ 2.0 ``Ads1231`` test module
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/07/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.peripheral.ads1231 import Ads1231
from pyhid.hidpp.features.peripheral.ads1231 import Ads1231Factory
from pyhid.hidpp.features.peripheral.ads1231 import Ads1231V0
from pyhid.hidpp.features.peripheral.ads1231 import Calibrate
from pyhid.hidpp.features.peripheral.ads1231 import CalibrateResponse
from pyhid.hidpp.features.peripheral.ads1231 import ManageDynamicCalibrationParameters
from pyhid.hidpp.features.peripheral.ads1231 import ManageDynamicCalibrationParametersResponse
from pyhid.hidpp.features.peripheral.ads1231 import MonitorReportEvent
from pyhid.hidpp.features.peripheral.ads1231 import ReadCalibration
from pyhid.hidpp.features.peripheral.ads1231 import ReadCalibrationResponse
from pyhid.hidpp.features.peripheral.ads1231 import ReadOtherNvsData
from pyhid.hidpp.features.peripheral.ads1231 import ReadOtherNvsDataResponse
from pyhid.hidpp.features.peripheral.ads1231 import ResetSensor
from pyhid.hidpp.features.peripheral.ads1231 import ResetSensorResponse
from pyhid.hidpp.features.peripheral.ads1231 import SetMonitorMode
from pyhid.hidpp.features.peripheral.ads1231 import SetMonitorModeResponse
from pyhid.hidpp.features.peripheral.ads1231 import ShutdownSensor
from pyhid.hidpp.features.peripheral.ads1231 import ShutdownSensorResponse
from pyhid.hidpp.features.peripheral.ads1231 import WriteCalibration
from pyhid.hidpp.features.peripheral.ads1231 import WriteCalibrationResponse
from pyhid.hidpp.features.peripheral.ads1231 import WriteOtherNvsData
from pyhid.hidpp.features.peripheral.ads1231 import WriteOtherNvsDataResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ads1231InstantiationTestCase(TestCase):
    """
    Test ``Ads1231`` testing classes instantiations
    """

    @staticmethod
    def test_ads_1231():
        """
        Test ``Ads1231`` class instantiation
        """
        my_class = Ads1231(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = Ads1231(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_ads_1231

    @staticmethod
    def test_reset_sensor():
        """
        Test ``ResetSensor`` class instantiation
        """
        my_class = ResetSensor(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ResetSensor(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reset_sensor

    @staticmethod
    def test_reset_sensor_response():
        """
        Test ``ResetSensorResponse`` class instantiation
        """
        my_class = ResetSensorResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ResetSensorResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reset_sensor_response

    @staticmethod
    def test_shutdown_sensor():
        """
        Test ``ShutdownSensor`` class instantiation
        """
        my_class = ShutdownSensor(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ShutdownSensor(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_shutdown_sensor

    @staticmethod
    def test_shutdown_sensor_response():
        """
        Test ``ShutdownSensorResponse`` class instantiation
        """
        my_class = ShutdownSensorResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShutdownSensorResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_shutdown_sensor_response

    @staticmethod
    def test_set_monitor_mode():
        """
        Test ``SetMonitorMode`` class instantiation
        """
        my_class = SetMonitorMode(device_index=0, feature_index=0,
                                  count=0,
                                  threshold=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetMonitorMode(device_index=0xff, feature_index=0xff,
                                  count=0xffff,
                                  threshold=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_monitor_mode

    @staticmethod
    def test_set_monitor_mode_response():
        """
        Test ``SetMonitorModeResponse`` class instantiation
        """
        my_class = SetMonitorModeResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetMonitorModeResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_monitor_mode_response

    @staticmethod
    def test_calibrate():
        """
        Test ``Calibrate`` class instantiation
        """
        my_class = Calibrate(device_index=0, feature_index=0,
                             ref_point_index=0,
                             ref_point_out_value=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = Calibrate(device_index=0xff, feature_index=0xff,
                             ref_point_index=0xff,
                             ref_point_out_value=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_calibrate

    @staticmethod
    def test_calibrate_response():
        """
        Test ``CalibrateResponse`` class instantiation
        """
        my_class = CalibrateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = CalibrateResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_calibrate_response

    @staticmethod
    def test_read_calibration():
        """
        Test ``ReadCalibration`` class instantiation
        """
        my_class = ReadCalibration(device_index=0, feature_index=0,
                                   ref_point_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadCalibration(device_index=0xff, feature_index=0xff,
                                   ref_point_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_calibration

    @staticmethod
    def test_read_calibration_response():
        """
        Test ``ReadCalibrationResponse`` class instantiation
        """
        my_class = ReadCalibrationResponse(device_index=0, feature_index=0,
                                           ref_point_index=0,
                                           ref_point_out_value=0,
                                           ref_point_cal_value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadCalibrationResponse(device_index=0xff, feature_index=0xff,
                                           ref_point_index=0xff,
                                           ref_point_out_value=0xff,
                                           ref_point_cal_value=0xffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_calibration_response

    @staticmethod
    def test_write_calibration():
        """
        Test ``WriteCalibration`` class instantiation
        """
        my_class = WriteCalibration(device_index=0, feature_index=0,
                                    ref_point_index=0,
                                    ref_point_out_value=0,
                                    ref_point_cal_value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteCalibration(device_index=0xff, feature_index=0xff,
                                    ref_point_index=0xff,
                                    ref_point_out_value=0xff,
                                    ref_point_cal_value=0xffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_calibration

    @staticmethod
    def test_write_calibration_response():
        """
        Test ``WriteCalibrationResponse`` class instantiation
        """
        my_class = WriteCalibrationResponse(device_index=0, feature_index=0,
                                            ref_point_index=0,
                                            ref_point_out_value=0,
                                            ref_point_cal_value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteCalibrationResponse(device_index=0xff, feature_index=0xff,
                                            ref_point_index=0xff,
                                            ref_point_out_value=0xff,
                                            ref_point_cal_value=0xffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_calibration_response

    @staticmethod
    def test_read_other_nvs_data():
        """
        Test ``ReadOtherNvsData`` class instantiation
        """
        my_class = ReadOtherNvsData(device_index=0, feature_index=0,
                                    data_field_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadOtherNvsData(device_index=0xff, feature_index=0xff,
                                    data_field_id=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_other_nvs_data

    @staticmethod
    def test_read_other_nvs_data_response():
        """
        Test ``ReadOtherNvsDataResponse`` class instantiation
        """
        my_class = ReadOtherNvsDataResponse(device_index=0, feature_index=0,
                                            data_field_id=0,
                                            data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadOtherNvsDataResponse(device_index=0xff, feature_index=0xff,
                                            data_field_id=0xff,
                                            data=0xffffffffffffffffffffffffffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_other_nvs_data_response

    @staticmethod
    def test_write_other_nvs_data():
        """
        Test ``WriteOtherNvsData`` class instantiation
        """
        my_class = WriteOtherNvsData(device_index=0, feature_index=0,
                                     data_field_id=0,
                                     data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteOtherNvsData(device_index=0xff, feature_index=0xff,
                                     data_field_id=0xff,
                                     data=0xffffffffffffffffffffffffffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_other_nvs_data

    @staticmethod
    def test_write_other_nvs_data_response():
        """
        Test ``WriteOtherNvsDataResponse`` class instantiation
        """
        my_class = WriteOtherNvsDataResponse(device_index=0, feature_index=0,
                                             data_field_id=0,
                                             data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteOtherNvsDataResponse(device_index=0xff, feature_index=0xff,
                                             data_field_id=0xff,
                                             data=0xffffffffffffffffffffffffffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_other_nvs_data_response

    @staticmethod
    def test_manage_dynamic_calibration_parameters():
        """
        Test ``ManageDynamicCalibrationParameters`` class instantiation
        """
        my_class = ManageDynamicCalibrationParameters(device_index=0, feature_index=0,
                                                      command=0,
                                                      offset_extension=0,
                                                      offset_adjustment_count=0,
                                                      dynamic_threshold=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageDynamicCalibrationParameters(device_index=0xff, feature_index=0xff,
                                                      command=0xff,
                                                      offset_extension=0xff,
                                                      offset_adjustment_count=0xffff,
                                                      dynamic_threshold=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_dynamic_calibration_parameters

    @staticmethod
    def test_manage_dynamic_calibration_parameters_response():
        """
        Test ``ManageDynamicCalibrationParametersResponse`` class instantiation
        """
        my_class = ManageDynamicCalibrationParametersResponse(device_index=0, feature_index=0,
                                                              command=0,
                                                              offset_extension=0,
                                                              offset_adjustment_count=0,
                                                              dynamic_threshold=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageDynamicCalibrationParametersResponse(device_index=0xff, feature_index=0xff,
                                                              command=0xff,
                                                              offset_extension=0xff,
                                                              offset_adjustment_count=0xffff,
                                                              dynamic_threshold=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_dynamic_calibration_parameters_response

    @staticmethod
    def test_monitor_report_event():
        """
        Test ``MonitorReportEvent`` class instantiation
        """
        my_class = MonitorReportEvent(device_index=0, feature_index=0,
                                      out_data_sample=0,
                                      offset_calibration=0,
                                      counter=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = MonitorReportEvent(device_index=0xff, feature_index=0xff,
                                      out_data_sample=0xffffff,
                                      offset_calibration=0xffffff,
                                      counter=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_monitor_report_event
# end class Ads1231InstantiationTestCase


class Ads1231TestCase(TestCase):
    """
    Test ``Ads1231`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            Ads1231V0.VERSION: {
                "cls": Ads1231V0,
                "interfaces": {
                    "reset_sensor_cls": ResetSensor,
                    "reset_sensor_response_cls": ResetSensorResponse,
                    "shutdown_sensor_cls": ShutdownSensor,
                    "shutdown_sensor_response_cls": ShutdownSensorResponse,
                    "set_monitor_mode_cls": SetMonitorMode,
                    "set_monitor_mode_response_cls": SetMonitorModeResponse,
                    "calibrate_cls": Calibrate,
                    "calibrate_response_cls": CalibrateResponse,
                    "read_calibration_cls": ReadCalibration,
                    "read_calibration_response_cls": ReadCalibrationResponse,
                    "write_calibration_cls": WriteCalibration,
                    "write_calibration_response_cls": WriteCalibrationResponse,
                    "read_other_nvs_data_cls": ReadOtherNvsData,
                    "read_other_nvs_data_response_cls": ReadOtherNvsDataResponse,
                    "write_other_nvs_data_cls": WriteOtherNvsData,
                    "write_other_nvs_data_response_cls": WriteOtherNvsDataResponse,
                    "manage_dynamic_calibration_parameters_cls": ManageDynamicCalibrationParameters,
                    "manage_dynamic_calibration_parameters_response_cls": ManageDynamicCalibrationParametersResponse,
                    "monitor_report_event_cls": MonitorReportEvent,
                },
                "max_function_index": 8
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``Ads1231Factory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(Ads1231Factory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``Ads1231Factory`` with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                Ads1231Factory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``Ads1231Factory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = Ads1231Factory.create(version)
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
            obj = Ads1231Factory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class Ads1231TestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
