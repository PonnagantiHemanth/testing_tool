#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.batterylevelscalibration_test

@brief  HID++ 2.0 BatteryLevelsCalibration test module

@author Stanislas Cottard

@date   2019/04/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationFactory
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationV0
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationV1
from pyhid.hidpp.features.common.batterylevelscalibration import CutOffControl
from pyhid.hidpp.features.common.batterylevelscalibration import CutOffControlResponse
from pyhid.hidpp.features.common.batterylevelscalibration import GetBattCalibrationInfo
from pyhid.hidpp.features.common.batterylevelscalibration import GetBattCalibrationInfoResponse
from pyhid.hidpp.features.common.batterylevelscalibration import MeasureBattery
from pyhid.hidpp.features.common.batterylevelscalibration import MeasureBatteryResponse
from pyhid.hidpp.features.common.batterylevelscalibration import ReadCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import ReadCalibrationResponse
from pyhid.hidpp.features.common.batterylevelscalibration import SetBatterySourceInfo
from pyhid.hidpp.features.common.batterylevelscalibration import SetBatterySourceInfoResponse
from pyhid.hidpp.features.common.batterylevelscalibration import StoreCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import StoreCalibrationResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class BatteryLevelsCalibrationInstantiationTestCase(TestCase):
    """
    ``BatteryLevelsCalibration`` testing class
    """

    @staticmethod
    def test_battery_levels_calibration():
        """
        Tests BatteryLevelsCalibration class instantiation
        """
        my_class = BatteryLevelsCalibration(device_index=0,
                                            feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = BatteryLevelsCalibration(device_index=0xFF,
                                            feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_battery_levels_calibration

    @staticmethod
    def test_get_batt_calibration_info():
        """
        Tests GetBattCalibrationInfo class instantiation
        """
        my_class = GetBattCalibrationInfo(device_index=0,
                                          feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetBattCalibrationInfo(device_index=0xFF,
                                          feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_batt_calibration_info

    @staticmethod
    def test_measure_battery():
        """
        Tests MeasureBattery class instantiation
        """
        my_class = MeasureBattery(device_index=0,
                                  feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = MeasureBattery(device_index=0xFF,
                                  feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_measure_battery

    @staticmethod
    def test_store_calibration():
        """
        Tests StoreCalibration class instantiation
        """
        my_class = StoreCalibration(device_index=0,
                                    feature_index=0,
                                    calibration_points_nb=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StoreCalibration(device_index=0xFF,
                                    feature_index=0xFF,
                                    calibration_points_nb=7,
                                    calibration_point_0=0xFF,
                                    calibration_point_1=0xFF,
                                    calibration_point_2=0xFF,
                                    calibration_point_3=0xFF,
                                    calibration_point_4=0xFF,
                                    calibration_point_5=0xFF,
                                    calibration_point_6=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_store_calibration

    @staticmethod
    def test_read_calibration():
        """
        Tests ReadCalibration class instantiation
        """
        my_class = ReadCalibration(device_index=0,
                                   feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadCalibration(device_index=0xFF,
                                   feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_calibration

    @staticmethod
    def test_cutoff_control():
        """
        Tests CutOffControl class instantiation
        """
        my_class = CutOffControl(device_index=0,
                                 feature_index=0,
                                 cutoff_change_state_requested=False,
                                 cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_ENABLE)

        RootTestCase._short_function_class_checker(my_class)

        my_class = CutOffControl(device_index=0xFF,
                                 feature_index=0xFF,
                                 cutoff_change_state_requested=True,
                                 cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_cutoff_control

    @staticmethod
    def test_get_batt_calibration_info_response():
        """
        Tests GetBattCalibrationInfoResponse class instantiation
        """
        my_class = GetBattCalibrationInfoResponse(device_index=0,
                                                  feature_index=0,
                                                  calibration_points_nb=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBattCalibrationInfoResponse(device_index=0xFF,
                                                  feature_index=0xFF,
                                                  calibration_points_nb=7,
                                                  calibration_point_0=0xFF,
                                                  calibration_point_1=0xFF,
                                                  calibration_point_2=0xFF,
                                                  calibration_point_3=0xFF,
                                                  calibration_point_4=0xFF,
                                                  calibration_point_5=0xFF,
                                                  calibration_point_6=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_batt_calibration_info_response

    @staticmethod
    def test_measure_battery_response():
        """
        Tests MeasureBatteryResponse class instantiation
        """
        my_class = MeasureBatteryResponse(device_index=0,
                                          feature_index=0,
                                          measure=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = MeasureBatteryResponse(device_index=0xFF,
                                          feature_index=0xFF,
                                          measure=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_measure_battery_response

    @staticmethod
    def test_store_calibration_response():
        """
        Tests StoreCalibrationResponse class instantiation
        """
        my_class = StoreCalibrationResponse(device_index=0,
                                            feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StoreCalibrationResponse(device_index=0xFF,
                                            feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_store_calibration_response

    @staticmethod
    def test_read_calibration_response():
        """
        Tests ReadCalibrationResponse class instantiation
        """
        my_class = ReadCalibrationResponse(device_index=0,
                                           feature_index=0,
                                           calibration_points_nb=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadCalibrationResponse(device_index=0xFF,
                                           feature_index=0xFF,
                                           calibration_points_nb=7,
                                           calibration_point_0=0xFF,
                                           calibration_point_1=0xFF,
                                           calibration_point_2=0xFF,
                                           calibration_point_3=0xFF,
                                           calibration_point_4=0xFF,
                                           calibration_point_5=0xFF,
                                           calibration_point_6=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_calibration_response

    @staticmethod
    def test_cutoff_control_response():
        """
        Tests CutOffControlResponse class instantiation
        """
        my_class = CutOffControlResponse(device_index=0,
                                         feature_index=0,
                                         cutoff_state=BatteryLevelsCalibration.CUTOFF_ENABLE)

        RootTestCase._long_function_class_checker(my_class)

        my_class = CutOffControlResponse(device_index=0xFF,
                                         feature_index=0xFF,
                                         cutoff_state=BatteryLevelsCalibration.CUTOFF_DISABLE)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_cutoff_control_response

    @staticmethod
    def test_set_battery_source_info():
        """
        Tests SetBatterySourceInfo class instantiation
        """
        my_class = SetBatterySourceInfo(device_index=0, feature_index=0, battery_source_index=0)
        RootTestCase._short_function_class_checker(my_class)

        my_class = SetBatterySourceInfo(device_index=0xFF, feature_index=0xFF, battery_source_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_battery_source_info

    @staticmethod
    def test_set_battery_source_info_response():
        """
        Tests SetBatterySourceInfoResponse class instantiation
        """
        my_class = SetBatterySourceInfoResponse(device_index=0,
                                                feature_index=0,
                                                battery_source_index=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetBatterySourceInfoResponse(device_index=0xFF,
                                                feature_index=0xFF,
                                                battery_source_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_battery_source_info_response
# end class BatteryLevelsCalibrationInstantiationTestCase


class BatteryLevelsCalibrationTestCase(TestCase):
    """
    ``BatteryLevelsCalibration`` factory model testing class
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": BatteryLevelsCalibrationV0,
                "interfaces": {
                    "get_battery_calibration_info_cls": GetBattCalibrationInfo,
                    "get_battery_calibration_info_response_cls": GetBattCalibrationInfoResponse,
                    "measure_battery_cls": MeasureBattery,
                    "measure_battery_response_cls": MeasureBatteryResponse,
                    "store_calibration_cls": StoreCalibration,
                    "store_calibration_response_cls": StoreCalibrationResponse,
                    "read_calibration_cls": ReadCalibration,
                    "read_calibration_response_cls": ReadCalibrationResponse,
                    "cut_off_control_cls": CutOffControl,
                    "cut_off_control_response_cls": CutOffControlResponse,
                },
                "max_function_index": 4
            },
            1: {
                "cls": BatteryLevelsCalibrationV1,
                "interfaces": {
                    "get_battery_calibration_info_cls": GetBattCalibrationInfo,
                    "get_battery_calibration_info_response_cls": GetBattCalibrationInfoResponse,
                    "measure_battery_cls": MeasureBattery,
                    "measure_battery_response_cls": MeasureBatteryResponse,
                    "store_calibration_cls": StoreCalibration,
                    "store_calibration_response_cls": StoreCalibrationResponse,
                    "read_calibration_cls": ReadCalibration,
                    "read_calibration_response_cls": ReadCalibrationResponse,
                    "cut_off_control_cls": CutOffControl,
                    "cut_off_control_response_cls": CutOffControlResponse,
                    "set_battery_source_info_cls": SetBatterySourceInfo,
                    "set_battery_source_info_response_cls": SetBatterySourceInfoResponse,
                },
                "max_function_index": 5
            },
        }
    # end def setUpClass

    def test_battery_levels_calibration_factory(self):
        """
        Tests battery levels calibration Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(BatteryLevelsCalibrationFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_battery_levels_calibration_factory

    def test_battery_levels_calibration_factory_version_out_of_range(self):
        """
        Tests battery levels calibration Factory with out of range versions
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                BatteryLevelsCalibrationFactory.create(version)
            # end with
        # end for
    # end def test_battery_levels_calibration_factory_version_out_of_range

    def test_battery_levels_calibration_factory_interfaces(self):
        """
        Check the battery levels calibration Factory returns its expected interfaces
        """
        for version, cls_map in self.expected.items():
            battery_levels_calibration = BatteryLevelsCalibrationFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(battery_levels_calibration, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(battery_levels_calibration, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_battery_levels_calibration_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            battery_levels_calibration = BatteryLevelsCalibrationFactory.create(version)
            self.assertEqual(battery_levels_calibration.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class BatteryLevelsCalibrationTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
