#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.peripheral.mlx90393multisensor_test
:brief: HID++ 2.0 MLX Multi Sensor command test definition
:author: Ganesh Thiraviam <gthiraviam@logitech.com>
:date: 2021/03/10
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.peripheral.mlx90393multisensor import Calibrate
from pyhid.hidpp.features.peripheral.mlx90393multisensor import CalibrateResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ManageDynCallParam
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ManageDynCallParamResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MLX90393MultiSensor
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MLX90393MultiSensorFactory
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MLX90393MultiSensorV0
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MonitorReportEvent
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MonitorTest
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MonitorTestResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ReadCalibration
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ReadCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ReadSensorRegister
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ReadSensorRegisterResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ResetSensor
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ResetSensorResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ShutdownSensor
from pyhid.hidpp.features.peripheral.mlx90393multisensor import ShutdownSensorResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import StartCalibration
from pyhid.hidpp.features.peripheral.mlx90393multisensor import StartCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import StopCalibration
from pyhid.hidpp.features.peripheral.mlx90393multisensor import StopCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import WriteCalibration
from pyhid.hidpp.features.peripheral.mlx90393multisensor import WriteCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx90393multisensor import WriteSensorRegister
from pyhid.hidpp.features.peripheral.mlx90393multisensor import WriteSensorRegisterResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MLX90393MultiSensorInstantiationTestCase(TestCase):
    """
    MLX90393MultiSensor testing classes instantiations
    """
    @staticmethod
    def test_mlx90393_multisensor():
        """
        Tests MLX90393MultiSensor class instantiation
        """
        my_class = MLX90393MultiSensor(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = MLX90393MultiSensor(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_mlx90393_multisensor

    @staticmethod
    def test_read_sensor_register():
        """
        Tests MLX90393MultiSensor Read Sensor Register class instantiation
        """
        my_class = ReadSensorRegister(device_index=0, feature_index=0, sensor_id=0, reg_addr=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadSensorRegister(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, reg_addr=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_sensor_register

    @staticmethod
    def test_read_sensor_register_response():
        """
        Tests ReadSensorRegisterResponse class instantiation
        """
        my_class = ReadSensorRegisterResponse(device_index=0, feature_index=0, sensor_id=0, reg_addr=0,
                                              reg_value=HexList("00" * (ReadSensorRegisterResponse.LEN.REG_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadSensorRegisterResponse(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, reg_addr=0xFF,
                                              reg_value=HexList("FF" * (ReadSensorRegisterResponse.LEN.REG_VALUE // 8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_sensor_register_response

    @staticmethod
    def test_write_sensor_register():
        """
        Tests WriteSensorRegister class instantiation
        """
        my_class = WriteSensorRegister(device_index=0, feature_index=0, sensor_id=0, reg_addr=0,
                                       reg_value=HexList("00" * (WriteSensorRegister.LEN.REG_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteSensorRegister(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, reg_addr=0xFF,
                                       reg_value=HexList("FF" * (WriteSensorRegister.LEN.REG_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_sensor_register

    @staticmethod
    def test_write_sensor_register_response():
        """
        Tests WriteSensorRegisterResponse class instantiation
        """
        my_class = WriteSensorRegisterResponse(
                device_index=0, feature_index=0, sensor_id=0, reg_addr=0,
                reg_value=HexList("00" * (WriteSensorRegisterResponse.LEN.REG_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteSensorRegisterResponse(
                device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, reg_addr=0xFF,
                reg_value=HexList("FF" * (WriteSensorRegisterResponse.LEN.REG_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_sensor_register_response

    @staticmethod
    def test_reset_sensor():
        """
        Tests ResetSensor class instantiation
        """
        my_class = ResetSensor(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ResetSensor(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reset_sensor

    @staticmethod
    def test_reset_sensor_response():
        """
        Tests ResetSensorResponse class instantiation
        """
        my_class = ResetSensorResponse(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ResetSensorResponse(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reset_sensor_response

    @staticmethod
    def test_shutdown_sensor():
        """
        Tests ShutdownSensor class instantiation
        """
        my_class = ShutdownSensor(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ShutdownSensor(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_shutdown_sensor

    @staticmethod
    def test_shutdown_sensor_response():
        """
        Tests ShutdownSensorResponse class instantiation
        """
        my_class = ShutdownSensorResponse(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShutdownSensorResponse(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_shutdown_sensor_response

    @staticmethod
    def test_monitor_test():
        """
        Tests MonitorTest class instantiation
        """
        my_class = MonitorTest(device_index=0, feature_index=0, sensor_id=0,
                               count=HexList("00" * (MonitorTest.LEN.COUNT // 8)),
                               threshold=HexList("00" * (MonitorTest.LEN.THRESHOLD // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = MonitorTest(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF,
                               count=HexList("FF" * (MonitorTest.LEN.COUNT // 8)),
                               threshold=HexList("FF" * (MonitorTest.LEN.THRESHOLD // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_monitor_test

    @staticmethod
    def test_monitor_test_response():
        """
        Tests MonitorTestResponse class instantiation
        """
        my_class = MonitorTestResponse(device_index=0, feature_index=0, sensor_id=0,
                                       count=HexList("00" * (MonitorTest.LEN.COUNT // 8)),
                                       threshold=HexList("00" * (MonitorTest.LEN.THRESHOLD // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = MonitorTestResponse(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF,
                                       count=HexList("FF" * (MonitorTest.LEN.COUNT // 8)),
                                       threshold=HexList("FF" * (MonitorTest.LEN.THRESHOLD // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_monitor_test

    @staticmethod
    def test_start_calibration():
        """
        Tests StartCalibration class instantiation
        """
        my_class = StartCalibration(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StartCalibration(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_start_calibration

    @staticmethod
    def test_start_calibration_response():
        """
        Tests StartCalibrationResponse class instantiation
        """
        my_class = StartCalibrationResponse(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartCalibrationResponse(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_calibration_response

    @staticmethod
    def test_stop_calibration():
        """
        Tests StopCalibration class instantiation
        """
        my_class = StopCalibration(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StopCalibration(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_stop_calibration

    @staticmethod
    def test_stop_calibration_response():
        """
        Tests StopCalibrationResponse class instantiation
        """
        my_class = StopCalibrationResponse(device_index=0, feature_index=0, sensor_id=0, calibration_data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StopCalibrationResponse(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, calibration_data=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_stop_calibration_response

    @staticmethod
    def test_read_calibration():
        """
        Tests ReadCalibration class instantiation
        """
        my_class = ReadCalibration(device_index=0, feature_index=0, sensor_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadCalibration(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_calibration

    @staticmethod
    def test_read_calibration_response():
        """
        Tests ReadCalibrationResponse class instantiation
        """
        my_class = ReadCalibrationResponse(device_index=0, feature_index=0, sensor_id=0, calibration_data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadCalibrationResponse(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, calibration_data=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_calibration_responses

    @staticmethod
    def test_write_calibration():
        """
        Tests WriteCalibration class instantiation
        """
        my_class = WriteCalibration(device_index=0, feature_index=0, sensor_id=0, calibration_data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteCalibration(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, calibration_data=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_calibration

    @staticmethod
    def test_write_calibration_response():
        """
        Tests WriteCalibrationResponse class instantiation
        """
        my_class = WriteCalibrationResponse(device_index=0, feature_index=0, sensor_id=0, calibration_data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteCalibrationResponse(device_index=0xFF, feature_index=0xFF,
                                            sensor_id=0xFF, calibration_data=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_calibration_response

    @staticmethod
    def test_calibrate():
        """
        Tests Calibrate class instantiation
        """
        my_class = Calibrate(device_index=0, feature_index=0, sensor_id=0, ref_point_id=0, ref_point_out_value=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = Calibrate(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF, ref_point_id=0xFF,
                             ref_point_out_value=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_calibrate

    @staticmethod
    def test_calibrate_response():
        """
        Tests CalibrateResponse class instantiation
        """
        my_class = CalibrateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = CalibrateResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_calibrate_response

    @staticmethod
    def test_manage_dyn_call_param():
        """
        Tests write class instantiation
        """
        my_class = ManageDynCallParam(device_index=0, feature_index=0, command=0, sensor_id=0, parameters=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageDynCallParam(
                device_index=0xFF, feature_index=0xFF, command=0x1, sensor_id=0x1,
                parameters=HexList("FF" * (ManageDynCallParam.LEN.PARAMETERS // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_dyn_call_param

    @staticmethod
    def test_manage_dyn_call_param_response():
        """
        Tests ManageDynCallParamResponse class instantiation
        """
        my_class = ManageDynCallParamResponse(device_index=0, feature_index=0, command=0, sensor_id=0, parameters=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ManageDynCallParamResponse(
                device_index=0xFF, feature_index=0xFF, command=0x0, sensor_id=0x1,
                parameters=HexList("FF" * (ManageDynCallParamResponse.LEN.PARAMETERS // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_manage_dyn_call_param_response

    @staticmethod
    def test_monitor_report():
        """
        Tests MonitorReportEvent class instantiation
        """
        my_class = MonitorReportEvent(device_index=0, feature_index=0, sensor_id=0,
                                      axis_value_x=0, axis_value_y=0, axis_value_z=0,
                                      temperature_value=0, arc_tangent_value=0, counter=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = MonitorReportEvent(device_index=0xFF, feature_index=0xFF, sensor_id=0xFF,
                                      axis_value_x=0xFF, axis_value_y=0xFF, axis_value_z=0xFF,
                                      temperature_value=0xFF, arc_tangent_value=0xFF, counter=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_monitor_report
# end class MLX90393MultiSensorInstantiationTestCase


class MLX90393MultiSensorTestCase(TestCase):
    """
    MLX90393MultiSensor factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
                MLX90393MultiSensorV0.VERSION: {
                        "cls": MLX90393MultiSensorV0,
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
                                "calibrate_cls": Calibrate,
                                "calibrate_response_cls": CalibrateResponse,
                                "manage_dyn_call_param_cls": ManageDynCallParam,
                                "manage_dyn_call_param_response_cls": ManageDynCallParamResponse,
                        },
                        "max_function_index": 10
                },
        }
    # end def setUpClass

    def test_mlx_multisensor_factory(self):
        """
        Tests MLX90393MultiSensorFactory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(MLX90393MultiSensorFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_mlx_multisensor_factory

    def test_mlx_multisensor_factory_version_out_of_range(self):
        """
        Tests MLX90393MultiSensorFactory with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                MLX90393MultiSensorFactory.create(version)
    # end def test_mlx_multisensor_factory_version_out_of_range

    def test_mlx_multisensor_factory_interfaces(self):
        """
        Check MLX90393MultiSensorFactory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            mlx_multisensor = MLX90393MultiSensorFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(mlx_multisensor, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(mlx_multisensor, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_mlx_multisensor_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            mlx_multisensor = MLX90393MultiSensorFactory.create(version)
            self.assertEqual(mlx_multisensor.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class MLX90393MultiSensorTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
