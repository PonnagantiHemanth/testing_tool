#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9205.functionality
:brief: HID++ 2.0 ``MLX903xx`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import choices
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mlx903xxutils import MLX903xxTestUtils
from pytestbox.device.hidpp20.peripheral.feature_9205.mlx903xx import MLX903xxTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_END_TEST_LOOP = "End Test Loop"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MLX903xxFunctionalityTestCase(MLX903xxTestCase):
    """
    Validate ``MLX903xx`` functionality test cases
    """

    @features("Feature9205")
    @level("Functionality")
    def test_read_sensor_registers_across_all_valid_addresses(self):
        """
        Validate the ReadSensorRegister across all valid Register Address

        [0] readSensorRegister(regAddr) -> regVal, RegAddr
        """
        valid_range = []
        valid_range.extend(self.config.F_CustomerAreaUsedRegisters)
        valid_range.extend(self.config.F_CustomerAreaFreeRegisters)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all valid register addresses")
        # --------------------------------------------------------------------------------------------------------------
        for register_address in valid_range:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with register_address: {register_address}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(self, register_address)

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
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9205_0001", _AUTHOR)
    # end def test_read_sensor_registers_across_all_valid_addresses

    @features("Feature9205")
    @level("Functionality")
    def test_write_sensor_registers_across_all_valid_addresses(self):
        """
        Validate the writeSensorRegister across all valid Register Address.

        [0] readSensorRegister(regAddr) -> regVal, RegAddr

        [1] writeSensorRegister(regAddr, regVal)
        """
        valid_range = []
        valid_range.extend(self.config.F_CustomerAreaUsedRegisters)
        valid_range.extend(self.config.F_CustomerAreaFreeRegisters)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all valid register addresses")
        # --------------------------------------------------------------------------------------------------------------
        for register_address in valid_range:
            # Doing a write operaton on registers with address '00', '01', '02' is triggering a hardware reset for
            # some values
            if register_address in ["00", "01", "02"]:
                continue
            # end if

            random_register_value = choices(compute_sup_values(["0000"]), elem_nb=1)[0]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteSensorRegister request with selected register Address "
                                     f"{register_address} and register value {random_register_value}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.write_sensor_register(self, register_address,
                                                                           HexList(random_register_value))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.write_sensor_register_response_cls, {})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with selected register address "
                                     f"{register_address}")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(self, register_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields if register value is same as input")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_address": (checker.check_register_address, register_address),
                "register_value": (checker.check_register_value, random_register_value)
            })
            checker.check_fields(self, response, self.feature_9205.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9205_0002", _AUTHOR)
    # end def test_write_sensor_registers_across_all_valid_addresses

    @features("Feature9205")
    @level("Functionality")
    @services("Thumbwheel")
    def test_monitor_test_returns_correct_number_of_events_requested_with_positive_delta(self):
        """
        Validate Monitor Test returns correct number of events requested with positive Delta V

        [4] monitorTest(count, threshold)
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_monitor_test_returns_correct_number_of_events_requested_with_positive_delta

    @features("Feature9205")
    @level("Functionality")
    @services("Thumbwheel")
    def test_monitor_test_returns_correct_number_of_events_requested_with_negative_delta(self):
        """
        Validate Monitor Test returns correct number of events requested with Negative Delta V

        [4] monitorTest(count, threshold)
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_monitor_test_returns_correct_number_of_events_requested_with_negative_delta

    @features("Feature9205")
    @level("Functionality")
    @bugtracker("Read_Write_Callibration_Format")
    def test_write_calibration_across_multiple_valid_data_ranges(self):
        """
        Validate WriteCalibration across multiple valid data ranges.

        [7] readCalibration() -> calibrationData

        [8] writeCalibration(calibrationData)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send ReadCalibration request to backup existing data")
        # --------------------------------------------------------------------------------------------------------------
        read_calibration_response = MLX903xxTestUtils.HIDppHelper.read_calibration(self)
        nb_turns = read_calibration_response.nb_turns
        max_x = read_calibration_response.max_x
        min_x = read_calibration_response.min_x
        max_y = read_calibration_response.max_y
        min_y = read_calibration_response.min_y

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting values between 0x0000..0xFFFF")
        # --------------------------------------------------------------------------------------------------------------
        for value in compute_inf_values(["FFFF"])[1:-1]:
            value_plus_one = HexList(f"{to_int(value) + 1:04X}")
            value_minus_one = HexList(f"{to_int(value) - 1:04X}")
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send WriteCalibration request with random data in 0x00..0xFFFF, "
                                     "minX/minY=selected Value-1 ,maxX/maxY = selected value+1")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.write_calibration(self, nb_turns=HexList(value)[0],
                                                                       min_x=value_minus_one,
                                                                       max_x=value_plus_one,
                                                                       min_y=value_minus_one,
                                                                       max_y=value_plus_one)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9205.write_calibration_response_cls, {})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ReadCalibration request")
            # ----------------------------------------------------------------------------------------------------------
            response = MLX903xxTestUtils.HIDppHelper.read_calibration(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadCalibrationResponse fields matches with the input values")
            # ----------------------------------------------------------------------------------------------------------
            checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "nb_turns": (checker.check_nb_turns, HexList(value)[0]),
                "min_x": (checker.check_min_x, value_minus_one),
                "max_x": (checker.check_max_x, value_plus_one),
                "min_y": (checker.check_min_y, value_minus_one),
                "max_y": (checker.check_max_y, value_plus_one)
            })
            checker.check_fields(self, response, self.feature_9205.read_calibration_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Send WriteCalibration request to restore original calibration data")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.write_calibration(self, nb_turns=nb_turns, min_x=min_x, max_x=max_x, min_y=min_y,
                                                        max_y=max_y)

        self.testCaseChecked("FUN_9205_0005", _AUTHOR)
    # end def test_write_calibration_across_multiple_valid_data_ranges

    @features("Feature9205")
    @level("Functionality")
    @services("Thumbwheel")
    def test_set_roller_across_multiple_valid_ranges_in_native_mode(self):
        """
        Validate Set Roller Test across multiple valid ranges in native mode.

        [10] setRollerTest(Multiplier, TestMode)
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_set_roller_across_multiple_valid_ranges_in_native_mode

    @features("Feature9205")
    @level("Functionality")
    @services("Thumbwheel")
    def test_set_roller_across_multiple_valid_ranges_in_diverted_mode(self):
        """
        Validate Set Roller Test across multiple valid ranges in diverted mode.

        [10] setRollerTest(Multiplier, TestMode)
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_set_roller_across_multiple_valid_ranges_in_diverted_mode
# end class MLX903xxFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
