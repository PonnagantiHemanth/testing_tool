#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9205.robustness
:brief: HID++ 2.0 ``MLX903xx`` robustness test suite
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
from pyhid.hidpp.features.peripheral.mlx903xx import ReadSensorRegister
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mlx903xxutils import MLX903xxTestUtils
from pytestbox.device.hidpp20.peripheral.feature_9205.mlx903xx import MLX903xxTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MLX903xxRobustnessTestCase(MLX903xxTestCase):
    """
    Validate ``MLX903xx`` robustness test cases
    """

    @features("Feature9205")
    @level("Robustness")
    def test_read_sensor_register_software_id(self):
        """
        Validate ``ReadSensorRegister`` software id field is ignored by the firmware

        [0] readSensorRegister(registerAddress) -> registerAddress, registerValue

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterAddress.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        register_address = self.config.F_CustomerAreaUsedRegisters[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=register_address,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_address": (checker.check_register_address, register_address)
            })
            checker.check_fields(self, response, self.feature_9205.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#1", _AUTHOR)
    # end def test_read_sensor_register_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_write_sensor_register_software_id(self):
        """
        Validate ``WriteSensorRegister`` software id field is ignored by the firmware

        [1] writeSensorRegister(registerAddress, registerValue) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterAddress.RegisterValue

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        register_address = self.config.F_CustomerAreaUsedRegisters[0]
        register_value = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteSensorRegister request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=register_address,
                register_value=register_value,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.write_sensor_register_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#2", _AUTHOR)
    # end def test_write_sensor_register_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_reset_sensor_software_id(self):
        """
        Validate ``ResetSensor`` software id field is ignored by the firmware

        [2] resetSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetSensor request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.reset_sensor(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ResetSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.reset_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#3", _AUTHOR)
    # end def test_reset_sensor_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_shutdown_sensor_software_id(self):
        """
        Validate ``ShutdownSensor`` software id field is ignored by the firmware

        [3] shutdownSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ShutdownSensor request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.shutdown_sensor(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.shutdown_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#4", _AUTHOR)
    # end def test_shutdown_sensor_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_monitor_test_software_id(self):
        """
        Validate ``MonitorTest`` software id field is ignored by the firmware

        [4] monitorTest(count, threshold) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Count.Threshold

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        count = 0x0
        threshold = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send MonitorTest request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.monitor_test(
                test_case=self,
                count=count,
                threshold=threshold,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorTestResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.monitor_test_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#5", _AUTHOR)
    # end def test_monitor_test_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_start_calibration_software_id(self):
        """
        Validate ``StartCalibration`` software id field is ignored by the firmware

        [5] startCalibration() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartCalibration request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.start_calibration(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.start_calibration_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#6", _AUTHOR)
    # end def test_start_calibration_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_stop_calibration_software_id(self):
        """
        Validate ``StopCalibration`` software id field is ignored by the firmware

        [6] stopCalibration() -> nbTurns, minX, maxX, minY, maxY

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StopCalibration request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.stop_calibration(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.StopCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_9205.stop_calibration_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#7", _AUTHOR)
    # end def test_stop_calibration_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_read_calibration_software_id(self):
        """
        Validate ``ReadCalibration`` software id field is ignored by the firmware

        [7] readCalibration() -> nbTurns, minX, maxX, minY, maxY

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadCalibration request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_calibration(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_9205.read_calibration_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#8", _AUTHOR)
    # end def test_read_calibration_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_write_calibration_software_id(self):
        """
        Validate ``WriteCalibration`` software id field is ignored by the firmware

        [8] writeCalibration(nbTurns, minX, maxX, minY, maxY) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.NbTurns.MinX.MaxX.MinY.MaxY.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        nb_turns = 0x0
        min_x = HexList(0x0)
        max_x = HexList(0x0)
        min_y = HexList(0x0)
        max_y = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteCalibration request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.write_calibration(
                test_case=self,
                nb_turns=nb_turns,
                min_x=min_x,
                max_x=max_x,
                min_y=min_y,
                max_y=max_y,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.write_calibration_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#9", _AUTHOR)
    # end def test_write_calibration_software_id

    @features("Feature9205")
    @level("Robustness")
    @bugtracker("Unexpected_ReadTouchStatus_Response")
    def test_read_touch_status_software_id(self):
        """
        Validate ``ReadTouchStatus`` software id field is ignored by the firmware

        [9] readTouchStatus() -> status

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadTouchStatus request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_touch_status(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadTouchStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadTouchStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_9205.read_touch_status_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#10", _AUTHOR)
    # end def test_read_touch_status_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_set_roller_test_software_id(self):
        """
        Validate ``SetRollerTest`` software id field is ignored by the firmware

        [10] setRollerTest(multiplier, testMode) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Multiplier.TestMode.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        multiplier = 0x0
        test_mode = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MLX903xx.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetRollerTest request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.set_roller_test(
                test_case=self,
                multiplier=multiplier,
                test_mode=test_mode,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRollerTestResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.set_roller_test_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0001#11", _AUTHOR)
    # end def test_set_roller_test_software_id

    @features("Feature9205")
    @level("Robustness")
    def test_read_sensor_register_padding(self):
        """
        Validate ``ReadSensorRegister`` padding bytes are ignored by the firmware

        [0] readSensorRegister(registerAddress) -> registerAddress, registerValue

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterAddress.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        register_address = self.config.F_CustomerAreaUsedRegisters[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.read_sensor_register_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=register_address,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_address": (checker.check_register_address, register_address)
            })
            checker.check_fields(self, response, self.feature_9205.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#1", _AUTHOR)
    # end def test_read_sensor_register_padding

    @features("Feature9205")
    @level("Robustness")
    def test_reset_sensor_padding(self):
        """
        Validate ``ResetSensor`` padding bytes are ignored by the firmware

        [2] resetSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.reset_sensor_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetSensor request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.reset_sensor(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ResetSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.reset_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#2", _AUTHOR)
    # end def test_reset_sensor_padding

    @features("Feature9205")
    @level("Robustness")
    def test_shutdown_sensor_padding(self):
        """
        Validate ``ShutdownSensor`` padding bytes are ignored by the firmware

        [3] shutdownSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.shutdown_sensor_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ShutdownSensor request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.shutdown_sensor(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.shutdown_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#3", _AUTHOR)
    # end def test_shutdown_sensor_padding

    @features("Feature9205")
    @level("Robustness")
    def test_start_calibration_padding(self):
        """
        Validate ``StartCalibration`` padding bytes are ignored by the firmware

        [5] startCalibration() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.start_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.start_calibration(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.start_calibration_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#4", _AUTHOR)
    # end def test_start_calibration_padding

    @features("Feature9205")
    @level("Robustness")
    def test_stop_calibration_padding(self):
        """
        Validate ``StopCalibration`` padding bytes are ignored by the firmware

        [6] stopCalibration() -> nbTurns, minX, maxX, minY, maxY

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.stop_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StopCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.stop_calibration(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.StopCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_9205.stop_calibration_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#5", _AUTHOR)
    # end def test_stop_calibration_padding

    @features("Feature9205")
    @level("Robustness")
    @bugtracker("Read_Write_Callibration_Format")
    def test_read_calibration_padding(self):
        """
        Validate ``ReadCalibration`` padding bytes are ignored by the firmware

        [7] readCalibration() -> nbTurns, minX, maxX, minY, maxY

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.read_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_calibration(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_9205.read_calibration_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#6", _AUTHOR)
    # end def test_read_calibration_padding

    @features("Feature9205")
    @level("Robustness")
    def test_write_calibration_padding(self):
        """
        Validate ``WriteCalibration`` padding bytes are ignored by the firmware

        [8] writeCalibration(nbTurns, minX, maxX, minY, maxY) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.NbTurns.MinX.MaxX.MinY.MaxY.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        nb_turns = 0x0
        min_x = HexList(0x0)
        max_x = HexList(0x0)
        min_y = HexList(0x0)
        max_y = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.write_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.write_calibration(
                test_case=self,
                nb_turns=nb_turns,
                min_x=min_x,
                max_x=max_x,
                min_y=min_y,
                max_y=max_y,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.write_calibration_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#7", _AUTHOR)
    # end def test_write_calibration_padding

    @features("Feature9205")
    @level("Robustness")
    @bugtracker("Unexpected_ReadTouchStatus_Response")
    def test_read_touch_status_padding(self):
        """
        Validate ``ReadTouchStatus`` padding bytes are ignored by the firmware

        [9] readTouchStatus() -> status

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.read_touch_status_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadTouchStatus request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_touch_status(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadTouchStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadTouchStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_9205.read_touch_status_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#8", _AUTHOR)
    # end def test_read_touch_status_padding

    @features("Feature9205")
    @level("Robustness")
    def test_set_roller_test_padding(self):
        """
        Validate ``SetRollerTest`` padding bytes are ignored by the firmware

        [10] setRollerTest(multiplier, testMode) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Multiplier.TestMode.0xPP

        Padding (PP) boundary values [00..FF]
        """
        multiplier = 0x0
        test_mode = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9205.set_roller_test_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetRollerTest request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.set_roller_test(
                test_case=self,
                multiplier=multiplier,
                test_mode=test_mode,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRollerTestResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.set_roller_test_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0002#9", _AUTHOR)
    # end def test_set_roller_test_padding

    @features("Feature9205")
    @level("Robustness")
    def test_free_registers_read_through_read_register_always_returns_0_before_writing(self):
        """
        Free register will always return 0 before writing

        [0] readSensorRegister(regAddr) -> regVal, RegAddr
        """
        register_value = HexList(0x0)
        register_value.addPadding(ReadSensorRegister.LEN.REGISTER_ADDRESS // 8)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over free register addresses [0x0A..0x1F]")
        # --------------------------------------------------------------------------------------------------------------
        for register_address in self.config.F_CustomerAreaFreeRegisters:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request for the selected register {register_address}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=register_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields will have register value 0")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_address": (checker.check_register_address, register_address),
                "register_value": (checker.check_register_value, register_value)
            })
            checker.check_fields(self, response, self.feature_9205.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9205_0003", _AUTHOR)
    # end def test_free_registers_read_through_read_register_always_returns_0_before_writing
# end class MLX903xxRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
