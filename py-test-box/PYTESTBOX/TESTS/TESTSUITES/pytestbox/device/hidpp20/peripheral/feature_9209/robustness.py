#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9209.robustness
:brief: HID++ 2.0 MLX 90393 Multi Sensor robustness test suite
:author: Ganesh Thiraviam <gthiraviam@logitech.com>
:date: 2021/03/10
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.device.base.mlx90393multisensorutils import MLX90393MultiSensorTestUtils as Utils
from pytestbox.device.hidpp20.peripheral.feature_9209.mlx90393multisensor import Mlx90393MultiSensorTestCase

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
_AUTHOR = "Ganesh Thiraviam"


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Mlx90393MultiSensorRobustnessTestCase(Mlx90393MultiSensorTestCase):
    """
    Validates Mlx90393MultiSensor robustness test cases
    """
    @features("Feature9209")
    @level("Robustness")
    def test_read_sensor_register_padding(self):
        """
        Validates ReadSensorRegister padding bytes are ignored by the firmware.

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.RegisterAddress.0xPP
        """
        Utils.ReadSensorRegisterHelper.HIDppHelper.padding(self, sensor_id=0x0, reg_addr=0x0, reg_value="003C")
        self.testCaseChecked("ROB_9209_0001", _AUTHOR)
    # end def test_read_sensor_register_padding

    @features("Feature9209")
    @level("Robustness")
    def test_write_sensor_register_padding(self):
        """
        Validates WriteSensorRegister padding bytes are ignored by the firmware.

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.RegisterAddress.RegisterValue.RegisterValue.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP
        """
        self.post_requisite_reload_nvs = True
        Utils.WriteSensorRegisterHelper.HIDppHelper.padding(self, sensor_id=0x0, reg_addr=0x0, reg_value="003C")
        self.testCaseChecked("ROB_9209_0002", _AUTHOR)
    # end def test_write_sensor_register_padding

    @features("Feature9209")
    @level("Robustness")
    def test_reset_sensor_padding(self):
        """
        Validates ResetSensor padding bytes are ignored by the firmware.

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.0xPP.0xPP
        """
        Utils.ResetSensorHelper.HIDppHelper.padding(self, sensor_id=0x0)
        self.testCaseChecked("ROB_9209_0003", _AUTHOR)
    # end def test_reset_sensor_padding

    @features("Feature9209")
    @level("Robustness")
    def test_shutdown_sensor_padding(self):
        """
        Validates ShutdownSensor padding bytes are ignored by the firmware.

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.0xPP.0xPP
        """
        Utils.ShutdownSensorHelper.HIDppHelper.padding(self, sensor_id=0x0)
        self.testCaseChecked("ROB_9209_0004", _AUTHOR)
    # end def test_shutdown_sensor_padding

    @features("Feature9209")
    @level("Robustness")
    def test_monitor_test_padding(self):
        """
        Validates MonitorTest padding bytes are ignored by the firmware.

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.Count.Count.Threshold.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP
        """
        Utils.MonitorTestHelper.HIDppHelper.padding(self, sensor_id=0x0, count="0000", threshold="00")
        self.testCaseChecked("ROB_9209_0005", _AUTHOR)
    # end def test_monitor_test_padding

    @features("Feature9209")
    @level("Robustness")
    def test_start_calibration_padding(self):
        """
        Validates StartCalibration padding bytes are ignored by the firmware.

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.0xPP.0xPP
        """
        self.post_requisite_reload_nvs = True
        Utils.StartCalibrationHelper.HIDppHelper.padding(self, sensor_id=0x0)
        self.testCaseChecked("ROB_9209_0006", _AUTHOR)
    # end def test_start_calibration_padding

    @features("Feature9209")
    @level("Robustness")
    def test_stop_calibration_padding(self):
        """
        Validates StopCalibration padding bytes are ignored by the firmware.

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.0xPP.0xPP
        """
        self.post_requisite_reload_nvs = True
        Utils.StopCalibrationHelper.HIDppHelper.padding(self, sensor_id=0x0)
        self.testCaseChecked("ROB_9209_0007", _AUTHOR)
    # end def test_stop_calibration_padding

    @features("Feature9209")
    @level("Robustness")
    def test_read_calibration_padding(self):
        """
        Validates ReadCalibration padding bytes are ignored by the firmware.

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.SensorId.0xPP.0xPP
        """
        Utils.ReadCalibrationHelper.HIDppHelper.padding(self, sensor_id=0x0)
        self.testCaseChecked("ROB_9209_0008", _AUTHOR)
    # end def test_read_calibration_padding

    @features("Feature9209")
    @level("Robustness")
    def test_write_calibration_padding(self):
        """
        Validates WriteCalibration padding bytes are ignored by the firmware.

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex.
        SensorId.CalibrationData.CalibrationData.CalibrationData.CalibrationData.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP
        """
        self.post_requisite_reload_nvs = True
        sensor_id = 0x0
        calibration_data = self.product.F_CalibrationData[sensor_id]
        Utils.WriteCalibrationHelper.HIDppHelper.padding(self, sensor_id=sensor_id, calibration_data=calibration_data)
        self.testCaseChecked("ROB_9209_0009", _AUTHOR)
    # end def test_write_calibration_padding

    @features("Feature9209")
    @level("Robustness")
    def test_manage_dyn_call_param_padding(self):
        """
        Validates ManageDynCallParam padding bytes are ignored by the firmware.

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex.
        Command/SensorId/Reserved.Parameters.Parameters.Parameters.Parameters.Parameters.Parameters.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP
        """
        self.post_requisite_reload_nvs = True
        sensor_id = 0x0
        Utils.ManageDynCallParamHelper.HIDppHelper.padding(self, command=0x1, sensor_id=sensor_id,
                                                           parameters=self.product.F_Parameters[sensor_id])
        self.testCaseChecked("ROB_9209_0010", _AUTHOR)
    # end def test_manage_dyn_call_param_padding
# end class Mlx90393MultiSensorRobustnessTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
