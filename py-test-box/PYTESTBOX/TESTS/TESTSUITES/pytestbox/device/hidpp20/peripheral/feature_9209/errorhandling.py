#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9209.errorhandling
:brief: HID++ 2.0 MLX 90393 Multi Sensor error handling test suite
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
class Mlx90393MultiSensorErrorHandlingTestCase(Mlx90393MultiSensorTestCase):
    """
    Validates Mlx90393MultiSensor error handling test cases
    """
    @features("Feature9209")
    @level("ErrorHandling")
    def test_read_sensor_register_wrong_function_index(self):
        """
        Validates function index
        """
        Utils.ReadSensorRegisterHelper.HIDppHelper.wrong_index(self, sensor_id=0x0, reg_addr=0x0)
        self.testCaseChecked("ERR_9209_0001", _AUTHOR)
    # end def test_read_sensor_register_wrong_function_index
# end class Mlx90393MultiSensorErrorHandlingTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
