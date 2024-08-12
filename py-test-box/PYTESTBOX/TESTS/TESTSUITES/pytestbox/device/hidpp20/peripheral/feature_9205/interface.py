#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9205.interface
:brief: HID++ 2.0 ``MLX903xx`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hidpp.features.peripheral.mlx903xx import MLX903xx
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mlx903xxutils import MLX903xxTestUtils
from pytestbox.device.hidpp20.peripheral.feature_9205.mlx903xx import MLX903xxTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MLX903xxInterfaceTestCase(MLX903xxTestCase):
    """
    Validate ``MLX903xx`` interface test cases
    """

    @features("Feature9205")
    @level("Interface")
    def test_read_sensor_register(self):
        """
        Validate ``ReadSensorRegister`` normal processing

        [0] readSensorRegister(registerAddress) -> registerAddress, registerValue
        """
        register_address = self.config.F_CustomerAreaUsedRegisters[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadSensorRegister request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(
            test_case=self,
            register_address=register_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.ReadSensorRegisterResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index)),
            "register_address": (checker.check_register_address, register_address)
        })
        checker.check_fields(self, response, self.feature_9205.read_sensor_register_response_cls, check_map)

        self.testCaseChecked("INT_9205_0001", _AUTHOR)
    # end def test_read_sensor_register

    @features("Feature9205")
    @level("Interface")
    def test_write_sensor_register(self):
        """
        Validate ``WriteSensorRegister`` normal processing

        [1] writeSensorRegister(registerAddress, registerValue) -> None
        """
        register_address = self.config.F_CustomerAreaUsedRegisters[3]
        register_value = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteSensorRegister request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.write_sensor_register(
            test_case=self,
            register_address=register_address,
            register_value=register_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        }
        checker.check_fields(self, response, self.feature_9205.write_sensor_register_response_cls, check_map)

        self.testCaseChecked("INT_9205_0002", _AUTHOR)
    # end def test_write_sensor_register

    @features("Feature9205")
    @level("Interface")
    def test_reset_sensor(self):
        """
        Validate ``ResetSensor`` normal processing

        [2] resetSensor() -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ResetSensor request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.reset_sensor(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ResetSensorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        }
        checker.check_fields(self, response, self.feature_9205.reset_sensor_response_cls, check_map)

        self.testCaseChecked("INT_9205_0003", _AUTHOR)
    # end def test_reset_sensor

    @features("Feature9205")
    @level("Interface")
    def test_shutdown_sensor(self):
        """
        Validate ``ShutdownSensor`` normal processing

        [3] shutdownSensor() -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ShutdownSensor request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.shutdown_sensor(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        }
        checker.check_fields(self, response, self.feature_9205.shutdown_sensor_response_cls, check_map)

        self.testCaseChecked("INT_9205_0004", _AUTHOR)
    # end def test_shutdown_sensor

    @features("Feature9205")
    @level("Interface")
    def test_monitor_test(self):
        """
        Validate ``MonitorTest`` normal processing

        [4] monitorTest(count, threshold) -> None
        """
        count = 0x0
        threshold = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send MonitorTest request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.monitor_test(
            test_case=self,
            count=count,
            threshold=threshold)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorTestResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        }
        checker.check_fields(self, response, self.feature_9205.monitor_test_response_cls, check_map)

        self.testCaseChecked("INT_9205_0005", _AUTHOR)
    # end def test_monitor_test

    @features("Feature9205")
    @level("Interface")
    def test_start_calibration(self):
        """
        Validate ``StartCalibration`` normal processing

        [5] startCalibration() -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.start_calibration(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check StartCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        }
        checker.check_fields(self, response, self.feature_9205.start_calibration_response_cls, check_map)

        self.testCaseChecked("INT_9205_0006", _AUTHOR)
    # end def test_start_calibration

    @features("Feature9205")
    @level("Interface")
    def test_stop_calibration(self):
        """
        Validate ``StopCalibration`` normal processing

        [6] stopCalibration() -> nbTurns, minX, maxX, minY, maxY
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StopCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.stop_calibration(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check StopCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.StopCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        })
        checker.check_fields(self, response, self.feature_9205.stop_calibration_response_cls, check_map)

        self.testCaseChecked("INT_9205_0007", _AUTHOR)
    # end def test_stop_calibration

    @features("Feature9205")
    @level("Interface")
    def test_read_calibration(self):
        """
        Validate ``ReadCalibration`` normal processing

        [7] readCalibration() -> nbTurns, minX, maxX, minY, maxY
        """
        nb_turns = 0x0
        min_x = HexList(0x0)
        max_x = HexList(0x0)
        min_y = HexList(0x0)
        max_y = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.write_calibration(test_case=self, nb_turns=nb_turns, min_x=min_x, max_x=max_x,
                                                        min_y=min_y, max_y=max_y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.read_calibration(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index)),
        })
        checker.check_fields(self, response, self.feature_9205.read_calibration_response_cls, check_map)

        self.testCaseChecked("INT_9205_0008", _AUTHOR)
    # end def test_read_calibration

    @features("Feature9205")
    @level("Interface")
    def test_write_calibration(self):
        """
        Validate ``WriteCalibration`` normal processing

        [8] writeCalibration(nbTurns, minX, maxX, minY, maxY) -> None
        """
        nb_turns = 0x0
        min_x = HexList(0x0)
        max_x = HexList(0x0)
        min_y = HexList(0x0)
        max_y = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.write_calibration(
            test_case=self,
            nb_turns=nb_turns,
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        }
        checker.check_fields(self, response, self.feature_9205.write_calibration_response_cls, check_map)

        self.testCaseChecked("INT_9205_0009", _AUTHOR)
    # end def test_write_calibration

    @features("Feature9205")
    @level("Interface")
    @bugtracker("Unexpected_ReadTouchStatus_Response")
    def test_read_touch_status(self):
        """
        Validate ``ReadTouchStatus`` normal processing

        [9] readTouchStatus() -> status
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadTouchStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.read_touch_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadTouchStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.ReadTouchStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index)),
        })
        checker.check_fields(self, response, self.feature_9205.read_touch_status_response_cls, check_map)

        self.testCaseChecked("INT_9205_0010", _AUTHOR)
    # end def test_read_touch_status

    @features("Feature9205")
    @level("Interface")
    def test_set_roller_test(self):
        """
        Validate ``SetRollerTest`` normal processing

        [10] setRollerTest(multiplier, testMode) -> None
        """
        multiplier = 0x0
        test_mode = MLX903xx.TestMode.NATIVE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRollerTest request")
        # --------------------------------------------------------------------------------------------------------------
        response = MLX903xxTestUtils.HIDppHelper.set_roller_test(
            test_case=self,
            multiplier=multiplier,
            test_mode=test_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetRollerTestResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9205_index))
        }
        checker.check_fields(self, response, self.feature_9205.set_roller_test_response_cls, check_map)

        self.testCaseChecked("INT_9205_0011", _AUTHOR)
    # end def test_set_roller_test
# end class MLX903xxInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
