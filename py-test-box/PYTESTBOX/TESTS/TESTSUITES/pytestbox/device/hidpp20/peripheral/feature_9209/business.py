#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9209.business
:brief: HID++ 2.0 MLX 90393 Multi Sensor business test suite
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
class Mlx90393MultiSensorBusinessTestCase(Mlx90393MultiSensorTestCase):
    """
    Validates Mlx90393MultiSensor business test cases
    """
    @features("Feature9209")
    @level("Business")
    def test_write_and_read_sensor_register(self):
        """
        Validates WriteSensorRegister/ReadSensorRegister
        """
        self.post_requisite_reload_nvs = True
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            for reg_addr in range(int(Numeral(self.product.F_RegisterCount))):
                reg_value = self.product.F_DefaultRegisterValue[reg_addr]

                # write
                response = Utils.WriteSensorRegisterHelper.HIDppHelper.write(
                    self, sensor_id=sensor_id, reg_addr=reg_addr, reg_value=reg_value)
                Utils.check_sensor_id(self, response, HexList(sensor_id))
                Utils.check_reg_addr(self, response, reg_addr)
                Utils.check_reg_value(self, response, reg_value)

                # read
                response = Utils.ReadSensorRegisterHelper.HIDppHelper.read(self, sensor_id=sensor_id, reg_addr=reg_addr)
                Utils.check_sensor_id(self, response, HexList(sensor_id))
                Utils.check_reg_addr(self, response, reg_addr)
                Utils.check_reg_value(self, response, reg_value)
            # end for
        # end for

        self.testCaseChecked("BUS_9209_0001", _AUTHOR)
    # end def test_write_sensor_register

    @features("Feature9209")
    @level("Business")
    def test_reset_sensor(self):
        """
        Validates ResetSensor
        """
        self.post_requisite_reload_nvs = True
        reg_addr = 0x0
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            # write value
            reg_value = self.product.F_DefaultRegisterValue[reg_addr]
            Utils.WriteSensorRegisterHelper.HIDppHelper.write(
                    self, sensor_id=sensor_id, reg_addr=reg_addr, reg_value=reg_value)

            # read written value
            response = Utils.ReadSensorRegisterHelper.HIDppHelper.read(self, sensor_id=sensor_id, reg_addr=reg_addr)
            Utils.check_reg_value(self, response, reg_value)

            # reset value
            response = Utils.ResetSensorHelper.HIDppHelper.write(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))

            # read default value
            reg_value = self.product.F_DefaultRegisterValue[reg_addr]
            response = Utils.ReadSensorRegisterHelper.HIDppHelper.read(self, sensor_id=sensor_id, reg_addr=reg_addr)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
            Utils.check_reg_addr(self, response, reg_addr)
            Utils.check_reg_value(self, response, reg_value)
        # end for
        self.testCaseChecked("BUS_9209_0002", _AUTHOR)
    # end def test_reset_sensor

    @features("Feature9209")
    @level("Business")
    def test_shutdown_sensor(self):
        """
        Validates ShutdownSensor
        """
        self.post_requisite_reload_nvs = True
        reg_addr = 0x0
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            # write
            response = Utils.ShutdownSensorHelper.HIDppHelper.write(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))

            # read
            reg_value = self.product.F_DefaultRegisterValue[reg_addr]
            response = Utils.ReadSensorRegisterHelper.HIDppHelper.read(self, sensor_id=sensor_id, reg_addr=reg_addr)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
            Utils.check_reg_addr(self, response, reg_addr)
            Utils.check_reg_value(self, response, reg_value)
        # end for
        self.testCaseChecked("BUS_9209_0003", _AUTHOR)
    # end def test_shutdown_sensor

    @features("Feature9209")
    @level("Business")
    def test_calibrate(self):
        """
        Validates Calibrate
        """
        self.post_requisite_reload_nvs = True
        ref_point_id = 0x0
        ref_point_out_val = 0x0
        for sensor_id in range(int(Numeral(self.product.F_SensorCount))):
            # write
            Utils.CalibrateHelper.HIDppHelper.write(
                    self, sensor_id=sensor_id, ref_point_id=ref_point_id, ref_point_out_val=ref_point_out_val)

            # read
            response = Utils.ReadCalibrationHelper.HIDppHelper.read(self, sensor_id=sensor_id)
            Utils.check_sensor_id(self, response, HexList(sensor_id))
            calibration_data = self.product.F_CalibrationData[sensor_id]
            Utils.check_calibration_data(self, response, calibration_data)
        # end for
        self.testCaseChecked("BUS_9209_0004", _AUTHOR)
    # end def test_calibrate
# end class Mlx90393MultiSensorBusinessTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
