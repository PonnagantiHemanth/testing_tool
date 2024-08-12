#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.peripheral.test.mlx903xx_test
:brief: HID++ 2.0 ``MLX903xx`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.peripheral.mlx903xx import MLX903xx
from pyhid.hidpp.features.peripheral.mlx903xx import MLX903xxFactory
from pyhid.hidpp.features.peripheral.mlx903xx import MLX903xxV0
from pyhid.hidpp.features.peripheral.mlx903xx import MonitorReportEvent
from pyhid.hidpp.features.peripheral.mlx903xx import MonitorTest
from pyhid.hidpp.features.peripheral.mlx903xx import MonitorTestResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadCalibration
from pyhid.hidpp.features.peripheral.mlx903xx import ReadCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadEPMIQS624Register
from pyhid.hidpp.features.peripheral.mlx903xx import ReadEPMIQS624RegisterResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadSensorRegister
from pyhid.hidpp.features.peripheral.mlx903xx import ReadSensorRegisterResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadTouchStatus
from pyhid.hidpp.features.peripheral.mlx903xx import ReadTouchStatusResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ResetSensor
from pyhid.hidpp.features.peripheral.mlx903xx import ResetSensorResponse
from pyhid.hidpp.features.peripheral.mlx903xx import RollerTestEvent
from pyhid.hidpp.features.peripheral.mlx903xx import SetRollerTest
from pyhid.hidpp.features.peripheral.mlx903xx import SetRollerTestResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ShutdownSensor
from pyhid.hidpp.features.peripheral.mlx903xx import ShutdownSensorResponse
from pyhid.hidpp.features.peripheral.mlx903xx import StartCalibration
from pyhid.hidpp.features.peripheral.mlx903xx import StartCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import StopCalibration
from pyhid.hidpp.features.peripheral.mlx903xx import StopCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import WriteCalibration
from pyhid.hidpp.features.peripheral.mlx903xx import WriteCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import WriteSensorRegister
from pyhid.hidpp.features.peripheral.mlx903xx import WriteSensorRegisterResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MLX903xxInstantiationTestCase(TestCase):
    """
    Test ``MLX903xx`` testing classes instantiations
    """

    @staticmethod
    def test_mlx903xx():
        """
        Test ``MLX903xx`` class instantiation
        """
        my_class = MLX903xx(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = MLX903xx(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_mlx903xx

    @staticmethod
    def test_read_sensor_register():
        """
        Test ``ReadSensorRegister`` class instantiation
        """
        my_class = ReadSensorRegister(device_index=0, feature_index=0,
                                      register_address=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadSensorRegister(device_index=0xFF, feature_index=0xFF,
                                      register_address=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_sensor_register

    @staticmethod
    def test_write_sensor_register():
        """
        Test ``WriteSensorRegister`` class instantiation
        """
        my_class = WriteSensorRegister(device_index=0, feature_index=0,
                                       register_address=0,
                                       register_value=HexList(0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = WriteSensorRegister(device_index=0xFF, feature_index=0xFF,
                                       register_address=0xFF,
                                       register_value=HexList("FF" * (WriteSensorRegister.LEN.REGISTER_VALUE // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_write_sensor_register

    @staticmethod
    def test_reset_sensor():
        """
        Test ``ResetSensor`` class instantiation
        """
        my_class = ResetSensor(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ResetSensor(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reset_sensor

    @staticmethod
    def test_shutdown_sensor():
        """
        Test ``ShutdownSensor`` class instantiation
        """
        my_class = ShutdownSensor(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ShutdownSensor(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_shutdown_sensor

    @staticmethod
    def test_monitor_test():
        """
        Test ``MonitorTest`` class instantiation
        """
        my_class = MonitorTest(device_index=0, feature_index=0,
                               count=0,
                               threshold=HexList(0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = MonitorTest(device_index=0xFF, feature_index=0xFF,
                               count=0xFFFF,
                               threshold=HexList("FF" * (MonitorTest.LEN.THRESHOLD // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_monitor_test

    @staticmethod
    def test_start_calibration():
        """
        Test ``StartCalibration`` class instantiation
        """
        my_class = StartCalibration(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StartCalibration(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_start_calibration

    @staticmethod
    def test_stop_calibration():
        """
        Test ``StopCalibration`` class instantiation
        """
        my_class = StopCalibration(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StopCalibration(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_stop_calibration

    @staticmethod
    def test_read_calibration():
        """
        Test ``ReadCalibration`` class instantiation
        """
        my_class = ReadCalibration(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadCalibration(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_calibration

    @staticmethod
    def test_write_calibration():
        """
        Test ``WriteCalibration`` class instantiation
        """
        my_class = WriteCalibration(device_index=0, feature_index=0,
                                    nb_turns=0,
                                    min_x=HexList(0),
                                    max_x=HexList(0),
                                    min_y=HexList(0),
                                    max_y=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteCalibration(device_index=0xFF, feature_index=0xFF,
                                    nb_turns=0xFF,
                                    min_x=HexList("FF" * (WriteCalibration.LEN.MIN_X // 8)),
                                    max_x=HexList("FF" * (WriteCalibration.LEN.MAX_X // 8)),
                                    min_y=HexList("FF" * (WriteCalibration.LEN.MIN_Y // 8)),
                                    max_y=HexList("FF" * (WriteCalibration.LEN.MAX_Y // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_calibration

    @staticmethod
    def test_read_touch_status():
        """
        Test ``ReadTouchStatus`` class instantiation
        """
        my_class = ReadTouchStatus(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadTouchStatus(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_touch_status

    @staticmethod
    def test_set_roller_test():
        """
        Test ``SetRollerTest`` class instantiation
        """
        my_class = SetRollerTest(device_index=0, feature_index=0,
                                 multiplier=0,
                                 test_mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetRollerTest(device_index=0xFF, feature_index=0xFF,
                                 multiplier=0xFF,
                                 test_mode=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_roller_test

    @staticmethod
    def test_read_epm_iqs624_register():
        """
        Test ``ReadEPMIQS624Register`` class instantiation
        """
        my_class = ReadEPMIQS624Register(device_index=0, feature_index=0,
                                         register_address=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadEPMIQS624Register(device_index=0xFF, feature_index=0xFF,
                                         register_address=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_epm_iqs624_register

    @staticmethod
    def test_read_sensor_register_response():
        """
        Test ``ReadSensorRegisterResponse`` class instantiation
        """
        my_class = ReadSensorRegisterResponse(device_index=0, feature_index=0,
                                              register_address=0,
                                              register_value=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadSensorRegisterResponse(
            device_index=0xFF, feature_index=0xFF, register_address=0xFF,
            register_value=HexList("FF" * (ReadSensorRegisterResponse.LEN.REGISTER_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_sensor_register_response

    @staticmethod
    def test_write_sensor_register_response():
        """
        Test ``WriteSensorRegisterResponse`` class instantiation
        """
        my_class = WriteSensorRegisterResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteSensorRegisterResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_sensor_register_response

    @staticmethod
    def test_reset_sensor_response():
        """
        Test ``ResetSensorResponse`` class instantiation
        """
        my_class = ResetSensorResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ResetSensorResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reset_sensor_response

    @staticmethod
    def test_shutdown_sensor_response():
        """
        Test ``ShutdownSensorResponse`` class instantiation
        """
        my_class = ShutdownSensorResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShutdownSensorResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_shutdown_sensor_response

    @staticmethod
    def test_monitor_test_response():
        """
        Test ``MonitorTestResponse`` class instantiation
        """
        my_class = MonitorTestResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = MonitorTestResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_monitor_test_response

    @staticmethod
    def test_start_calibration_response():
        """
        Test ``StartCalibrationResponse`` class instantiation
        """
        my_class = StartCalibrationResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartCalibrationResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_calibration_response

    @staticmethod
    def test_stop_calibration_response():
        """
        Test ``StopCalibrationResponse`` class instantiation
        """
        my_class = StopCalibrationResponse(device_index=0, feature_index=0,
                                           nb_turns=0,
                                           min_x=HexList(0),
                                           max_x=HexList(0),
                                           min_y=HexList(0),
                                           max_y=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = StopCalibrationResponse(device_index=0xFF, feature_index=0xFF,
                                           nb_turns=0xFF,
                                           min_x=HexList("FF" * (StopCalibrationResponse.LEN.MIN_X // 8)),
                                           max_x=HexList("FF" * (StopCalibrationResponse.LEN.MAX_X // 8)),
                                           min_y=HexList("FF" * (StopCalibrationResponse.LEN.MIN_Y // 8)),
                                           max_y=HexList("FF" * (StopCalibrationResponse.LEN.MAX_Y // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_stop_calibration_response

    @staticmethod
    def test_read_calibration_response():
        """
        Test ``ReadCalibrationResponse`` class instantiation
        """
        my_class = ReadCalibrationResponse(device_index=0, feature_index=0,
                                           nb_turns=0,
                                           min_x=HexList(0),
                                           max_x=HexList(0),
                                           min_y=HexList(0),
                                           max_y=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadCalibrationResponse(device_index=0xFF, feature_index=0xFF,
                                           nb_turns=0xFF,
                                           min_x=HexList("FF" * (ReadCalibrationResponse.LEN.MIN_X // 8)),
                                           max_x=HexList("FF" * (ReadCalibrationResponse.LEN.MAX_X // 8)),
                                           min_y=HexList("FF" * (ReadCalibrationResponse.LEN.MIN_Y // 8)),
                                           max_y=HexList("FF" * (ReadCalibrationResponse.LEN.MAX_Y // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_calibration_response

    @staticmethod
    def test_write_calibration_response():
        """
        Test ``WriteCalibrationResponse`` class instantiation
        """
        my_class = WriteCalibrationResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteCalibrationResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_calibration_response

    @staticmethod
    def test_read_touch_status_response():
        """
        Test ``ReadTouchStatusResponse`` class instantiation
        """
        my_class = ReadTouchStatusResponse(device_index=0, feature_index=0,
                                           status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadTouchStatusResponse(device_index=0xFF, feature_index=0xFF,
                                           status=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_touch_status_response

    @staticmethod
    def test_set_roller_test_response():
        """
        Test ``SetRollerTestResponse`` class instantiation
        """
        my_class = SetRollerTestResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRollerTestResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_roller_test_response

    @staticmethod
    def test_read_epm_iqs624_register_response():
        """
        Test ``ReadEPMIQS624RegisterResponse`` class instantiation
        """
        my_class = ReadEPMIQS624RegisterResponse(device_index=0, feature_index=0,
                                                 register_address=0,
                                                 register_value=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadEPMIQS624RegisterResponse(
            device_index=0xFF, feature_index=0xFF, register_address=0xFF,
            register_value=HexList("FF" * (ReadEPMIQS624RegisterResponse.LEN.REGISTER_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_epm_iqs624_register_response

    @staticmethod
    def test_monitor_report_event():
        """
        Test ``MonitorReportEvent`` class instantiation
        """
        my_class = MonitorReportEvent(device_index=0, feature_index=0,
                                      field_x=0,
                                      field_y=0,
                                      field_z=0,
                                      temperature=0,
                                      angle=HexList(0),
                                      slot=HexList(0),
                                      ratchet=HexList(0),
                                      angle_offset=HexList(0),
                                      angle_ratchet_number=HexList(0),
                                      counter=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = MonitorReportEvent(
            device_index=0xFF,
            feature_index=0xFF,
            field_x=0xFFFF,
            field_y=0xFFFF,
            field_z=0xFFFF,
            temperature=0xFFFF,
            angle=HexList("FF" * (MonitorReportEvent.LEN.ANGLE // 8)),
            slot=HexList("FF" * (MonitorReportEvent.LEN.SLOT // 8)),
            ratchet=HexList("FF" * (MonitorReportEvent.LEN.RATCHET // 8)),
            angle_offset=HexList("FF" * (MonitorReportEvent.LEN.ANGLE_OFFSET // 8)),
            angle_ratchet_number=HexList("FF" * (MonitorReportEvent.LEN.ANGLE_RATCHET_NUMBER // 8)),
            counter=HexList("FF" * (MonitorReportEvent.LEN.COUNTER // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_monitor_report_event

    @staticmethod
    def test_roller_test_event():
        """
        Test ``RollerTestEvent`` class instantiation
        """
        my_class = RollerTestEvent(device_index=0, feature_index=0,
                                   accumulator=HexList(0),
                                   timestamp_value=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = RollerTestEvent(device_index=0xFF, feature_index=0xFF,
                                   accumulator=HexList("FF" * (RollerTestEvent.LEN.ACCUMULATOR // 8)),
                                   timestamp_value=HexList("FF" * (RollerTestEvent.LEN.TIMESTAMP_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_roller_test_event
# end class MLX903xxInstantiationTestCase


class MLX903xxTestCase(TestCase):
    """
    Test ``MLX903xx`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            MLX903xxV0.VERSION: {
                "cls": MLX903xxV0,
                "interfaces": {
                    "read_sensor_register_cls": ReadSensorRegister,
                    "read_sensor_register_response_cls": ReadSensorRegisterResponse,
                    "write_sensor_register_cls": WriteSensorRegister,
                    "write_sensor_register_response_cls": WriteSensorRegisterResponse,
                    "reset_sensor_cls": ResetSensor,
                    "reset_sensor_response_cls": ResetSensorResponse,
                    "shutdown_sensor_cls": ShutdownSensor,
                    "shutdown_sensor_response_cls": ShutdownSensorResponse,
                    "monitor_test_cls": MonitorTest,
                    "monitor_test_response_cls": MonitorTestResponse,
                    "start_calibration_cls": StartCalibration,
                    "start_calibration_response_cls": StartCalibrationResponse,
                    "stop_calibration_cls": StopCalibration,
                    "stop_calibration_response_cls": StopCalibrationResponse,
                    "read_calibration_cls": ReadCalibration,
                    "read_calibration_response_cls": ReadCalibrationResponse,
                    "write_calibration_cls": WriteCalibration,
                    "write_calibration_response_cls": WriteCalibrationResponse,
                    "read_touch_status_cls": ReadTouchStatus,
                    "read_touch_status_response_cls": ReadTouchStatusResponse,
                    "set_roller_test_cls": SetRollerTest,
                    "set_roller_test_response_cls": SetRollerTestResponse,
                    "read_epm_iqs624_register_cls": ReadEPMIQS624Register,
                    "read_epm_iqs624_register_response_cls": ReadEPMIQS624RegisterResponse,
                    "monitor_report_event_cls": MonitorReportEvent,
                    "roller_test_event_cls": RollerTestEvent,
                },
                "max_function_index": 11
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``MLX903xxFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(MLX903xxFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``MLX903xxFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                MLX903xxFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``MLX903xxFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = MLX903xxFactory.create(version)
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
            obj = MLX903xxFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class MLX903xxTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
