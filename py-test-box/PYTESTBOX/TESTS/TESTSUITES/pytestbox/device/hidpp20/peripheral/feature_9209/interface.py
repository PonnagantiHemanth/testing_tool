#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9209.interface
:brief: HID++ 2.0 MLX 90393 Multi Sensor interface test suite
:author: Ganesh Thiraviam <gthiraviam@logitech.com>
:date: 2021/03/10
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.mlx90393multisensorutils import MLX90393MultiSensorTestUtils as Utils
from pytestbox.device.hidpp20.peripheral.feature_9209.mlx90393multisensor import Mlx90393MultiSensorTestCase

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
_AUTHOR = "Ganesh Thiraviam"


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Mlx90393MultiSensorInterfaceTestCase(Mlx90393MultiSensorTestCase):
    """
    Validates Mlx90393MultiSensor test cases
    """
    @features("Feature9209")
    @level("Interface")
    def test_read_sensor_register(self):
        """
        Test the ReadSensorRegister request API.
        """

        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            for reg_addr in range(int(Numeral(self.product.F_RegisterCount))):
                reg_value = self.product.F_DefaultRegisterValue[reg_addr]
                response = Utils.ReadSensorRegisterHelper.HIDppHelper.read(self, sensor_id=sensor_id, reg_addr=reg_addr)
                Utils.check_sensor_id(self, response, HexList(sensor_id))
                Utils.check_reg_addr(self, response, reg_addr)
                Utils.check_reg_value(self, response, reg_value)
            # end for
        # end for
        self.testCaseChecked("INT_9209_0001", _AUTHOR)
    # end def test_read_sensor_register

    @features("Feature9209")
    @level("Interface")
    def test_write_sensor_register(self):
        """
        Test the WriteSensorRegister request API.
        """
        self.post_requisite_reload_nvs = True
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            for reg_addr in range(int(Numeral(self.product.F_RegisterCount))):
                reg_value = self.product.F_DefaultRegisterValue[reg_addr]
                response = Utils.WriteSensorRegisterHelper.HIDppHelper.write(
                        self, sensor_id=sensor_id, reg_addr=reg_addr, reg_value=reg_value)
                Utils.check_sensor_id(self, response, HexList(sensor_id))
                Utils.check_reg_addr(self, response, reg_addr)
                Utils.check_reg_value(self, response, reg_value)
            # end for
        # end for
        self.testCaseChecked("INT_9209_0002", _AUTHOR)
    # end def test_write_sensor_register

    @features("Feature9209")
    @level("Interface")
    def test_reset_sensor(self):
        """
        Test the ResetSensor request API.
        """
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            response = Utils.ResetSensorHelper.HIDppHelper.write(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
        # end for
        self.testCaseChecked("INT_9209_0003", _AUTHOR)
    # end def test_reset_sensor

    @features("Feature9209")
    @level("Interface")
    def test_shutdown_sensor(self):
        """
        Test the ShutdownSensor request API.
        """
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            response = Utils.ShutdownSensorHelper.HIDppHelper.write(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
        # end for
        self.testCaseChecked("INT_9209_0004", _AUTHOR)
    # end def test_shutdown_sensor

    @features("Feature9209")
    @level("Interface")
    def test_monitor_test(self):
        """
        Test the MonitorTest request API.
        """
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            # sample monitor count
            count = self.product.F_MonitorTestCount
            # sample threshold
            threshold = self.product.F_MonitorTestThreshold
            response = Utils.MonitorTestHelper.HIDppHelper.read(
                    self, sensor_id=sensor_id, count=count, threshold=threshold)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
            Utils.check_count(self, response, count)
            Utils.check_threshold(self, response, threshold)
        # end for
        self.testCaseChecked("INT_9209_0005", _AUTHOR)
    # end def test_monitor_test

    @features("Feature9209")
    @level("Interface")
    def test_start_calibration(self):
        """
        Test the StartCalibration request API.
        """
        self.post_requisite_reload_nvs = True
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            response = Utils.StartCalibrationHelper.HIDppHelper.write(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
        # end for
        self.testCaseChecked("INT_9209_0006", _AUTHOR)
    # end def test_start_calibration

    @features("Feature9209")
    @level("Interface")
    def test_stop_calibration(self):
        """
        Test the StopCalibration request API.
        """
        self.post_requisite_reload_nvs = True
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            response = Utils.StopCalibrationHelper.HIDppHelper.write(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
            calibration_data = self.product.F_CalibrationData[sensor_id]
            Utils.check_calibration_data(self, response, calibration_data)
        # end for
        self.testCaseChecked("INT_9209_0007", _AUTHOR)
    # end def test_stop_calibration

    @features("Feature9209")
    @level("Interface")
    def test_read_calibration(self):
        """
        Test the ReadCalibration request API.
        """
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            response = Utils.ReadCalibrationHelper.HIDppHelper.read(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
            calibration_data = self.product.F_CalibrationData[sensor_id]
            Utils.check_calibration_data(self, response, calibration_data)
        # end for
        self.testCaseChecked("INT_9209_0008", _AUTHOR)
    # end def test_read_calibration

    @features("Feature9209")
    @level("Interface")
    def test_write_calibration(self):
        """
        Test the WriteCalibration request API.
        """
        self.post_requisite_reload_nvs = True
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            calibration_data = self.product.F_CalibrationData[sensor_id]
            response = Utils.WriteCalibrationHelper.HIDppHelper.write(
                    self, sensor_id=sensor_id, calibration_data=calibration_data)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
            Utils.check_calibration_data(self, response, calibration_data)
        # end for
        self.testCaseChecked("INT_9209_0009", _AUTHOR)
    # end def test_write_calibration

    @features("Feature9209")
    @level("Interface")
    def test_calibrate(self):
        """
        Test the Calibrate request API.
        """
        self.post_requisite_reload_nvs = True
        ref_point_id = 0x0
        ref_point_out_val = 0x0
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            Utils.CalibrateHelper.HIDppHelper.write(
                    self, sensor_id=sensor_id, ref_point_id=ref_point_id, ref_point_out_val=ref_point_out_val)
        # end for
        self.testCaseChecked("INT_9209_0010", _AUTHOR)
    # end def test_calibrate

    @features("Feature9209")
    @level("Interface")
    def test_manage_dyn_call_param(self):
        """
        Test the ManageDynCallParam request API.
        """
        self.post_requisite_reload_nvs = True
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            parameters = self.product.F_Parameters[sensor_id]
            command = 0x0
            response = Utils.ManageDynCallParamHelper.HIDppHelper.write(
                    self, command=command, sensor_id=sensor_id, parameters=parameters)
            Utils.check_command(self, response, command)
            Utils.check_sensor_id(self, response, sensor_id)
        # end for
        self.testCaseChecked("INT_9209_0011", _AUTHOR)
    # end def test_manage_dyn_call_param
# end class Mlx90393MultiSensorInterfaceTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
