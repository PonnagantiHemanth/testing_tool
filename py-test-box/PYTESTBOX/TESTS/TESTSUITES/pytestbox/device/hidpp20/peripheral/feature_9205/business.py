#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9205.business
:brief: HID++ 2.0 ``MLX903xx`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.peripheral.mlx903xx import WriteSensorRegister
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import choices
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
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
class MLX903xxBusinessTestCase(MLX903xxTestCase):
    """
    Validate ``MLX903xx`` business test cases
    """

    @features("Feature9205")
    @level("Business")
    @services("HardwareReset")
    def test_read_and_write_sensor_register_for_used_registers(self):
        """
        Validate Read and Write Sensor Register API of Used Registers

        [0] readSensorRegister(regAddr) -> regVal, RegAddr

        [1] writeSensorRegister(regAddr, regVal)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over customer area used register addresses")
        # --------------------------------------------------------------------------------------------------------------
        for register_address in self.config.F_CustomerAreaUsedRegisters:
            # Doing a write operaton on registers with address '00', '01', '02' is triggering a hardware reset for
            # some values
            if register_address in ["00", "01", "02"]:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over several interesting values in 0x0000..0xFFFF")
            # ----------------------------------------------------------------------------------------------------------
            for register_value in compute_sup_values(HexList(Numeral(0, WriteSensorRegister.LEN.REGISTER_VALUE//8))):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send WriteSensorRegister request with register_address = {register_address} "
                                         f"and register_value = {register_value}")
                # ------------------------------------------------------------------------------------------------------
                response = MLX903xxTestUtils.HIDppHelper.write_sensor_register(self, register_address,
                                                                               HexList(register_value))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
                # ------------------------------------------------------------------------------------------------------
                MLX903xxTestUtils.MessageChecker.check_fields(
                    self, response, self.feature_9205.write_sensor_register_response_cls, {})

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send ReadSensorRegister request for the selected register_address "
                                         f"{register_address}")
                # ------------------------------------------------------------------------------------------------------
                response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(self, register_address)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
                # ------------------------------------------------------------------------------------------------------
                checker = MLX903xxTestUtils.ReadSensorRegisterResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "register_address": (checker.check_register_address, register_address),
                    "register_value": (checker.check_register_value, register_value)
                })
                checker.check_fields(self, response, self.feature_9205.read_sensor_register_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9205_0001", _AUTHOR)
    # end def test_read_and_write_sensor_register_for_used_registers

    @features("Feature9205")
    @level("Business")
    def test_read_and_write_sensor_register_for_free_registers(self):
        """
        Validate Read and Write Sensor Register API of Free Registers

        [0] readSensorRegister(regAddr) -> regVal, RegAddr

        [1] writeSensorRegister(regAddr, regVal)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over customer area free registers")
        # --------------------------------------------------------------------------------------------------------------
        for register_address in self.config.F_CustomerAreaFreeRegisters:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over several interesting values in 0x0000..0xFFFF")
            # ----------------------------------------------------------------------------------------------------------
            for register_value in compute_sup_values(HexList(Numeral(0, WriteSensorRegister.LEN.REGISTER_VALUE//8))):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send WriteSensorRegister request with register_address={register_address} "
                                         f"and register_value={register_value}")
                # ------------------------------------------------------------------------------------------------------
                response = MLX903xxTestUtils.HIDppHelper.write_sensor_register(self, register_address,
                                                                               HexList(register_value))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
                # ------------------------------------------------------------------------------------------------------
                MLX903xxTestUtils.MessageChecker.check_fields(
                    self, response, self.feature_9205.write_sensor_register_response_cls, {})

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send ReadSensorRegister request for the selected register_address "
                                         f"{register_address}")
                # ------------------------------------------------------------------------------------------------------
                response = MLX903xxTestUtils.HIDppHelper.read_sensor_register(self, register_address)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
                # ------------------------------------------------------------------------------------------------------
                checker = MLX903xxTestUtils.ReadSensorRegisterResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "register_address": (checker.check_register_address, register_address),
                    "register_value": (checker.check_register_value, register_value)
                })
                checker.check_fields(self, response, self.feature_9205.read_sensor_register_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9205_0002", _AUTHOR)
    # end def test_read_and_write_sensor_register_for_free_registers

    @features("Feature9205")
    @features("Feature2110")
    @level("Business")
    @services("Thumbwheel")
    def test_reset_sensor_stops_monitor_test_report_while_in_smart_shift_mode(self):
        """
        Validate Reset Sensor stops Monitor Test Report while in smart shift mode

        [2] resetSensor()

        [4] monitorTest(count, threshold)

        require 0x2110 feature
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_reset_sensor_stops_monitor_test_report_while_in_smart_shift_mode

    @features("Feature9205")
    @features("Feature2110")
    @level("Business")
    @services("Thumbwheel")
    def test_reset_sensor_stops_monitor_test_report_while_in_free_wheel_mode(self):
        """
        Validate Reset Sensor stops Monitor Test Report while in free wheel mode

        [2] resetSensor()

        [4] monitorTest(count, threshold)

        require 0x2110 feature
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_reset_sensor_stops_monitor_test_report_while_in_free_wheel_mode

    @features("Feature9205")
    @level("Business")
    @services("Ratchet")
    def test_ratchet_wheel_after_shutdown_sensor_and_reset_sensor(self):
        """
        Validate Ratchet wheel doesn't work after shutdown sensor and works after reset Sensor

        [2] resetSensor()

        [3] shutdownSensor()
        """
        raise NotImplementedError("To be implemented when @services('Ratchet') is available")
    # end def test_ratchet_wheel_after_shutdown_sensor_and_reset_sensor

    @features("Feature9205")
    @level("Business")
    @services("Ratchet")
    def test_ratchet_wheel_behaviour_when_shutdown_during_monitor_report(self):
        """
        Validate Ratchet wheel behaviour when shutdown during monitor report

        [3] shutdownSensor()

        [4] monitorTest(count, threshold)
        """
        raise NotImplementedError("To be implemented when @services('Ratchet') is available")
    # end def test_ratchet_wheel_behaviour_when_shutdown_during_monitor_report

    @features("Feature9205")
    @level("Business")
    @services("Thumbwheel")
    def test_sensor_calibration(self):
        """
        Validate Calibration of the sensor

        [5] startCalibration()

        [6] stopCalibration() -> calibrationData

        [7] readCalibration() -> calibrationData
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_sensor_calibration

    @features("Feature9205")
    @level("Business")
    @services("Thumbwheel")
    def test_calibration_data_after_new_calibration(self):
        """
        Validate Calibration data stored after new calibration.

        [5] startCalibration()

        [6] stopCalibration() -> calibrationData

        [7] readCalibration() -> calibrationData
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_calibration_data_after_new_calibration

    @features("Feature9205")
    @level("Business")
    @services("HardwareReset")
    @bugtracker("Read_Write_Callibration_Format")
    def test_calibration_data_stored_after_power_cycle(self):
        """
        Validate Calibration data stored across power cycle.

        [7] readCalibration() -> calibrationData

        [8] writeCalibration(calibrationData)

        require PowerSupply
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send ReadCalibration request to backup existing data")
        # --------------------------------------------------------------------------------------------------------------
        read_calibration_response = MLX903xxTestUtils.HIDppHelper.read_calibration(self)
        nb_turns = read_calibration_response.nb_turns
        min_x = read_calibration_response.min_x
        max_x = read_calibration_response.max_x
        min_y = read_calibration_response.min_y
        max_y = read_calibration_response.max_y

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, read_calibration_response, self.feature_9205.read_calibration_response_cls,
                             check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteCalibration request with random values")
        # --------------------------------------------------------------------------------------------------------------
        value = choices(compute_sup_values(["0000"]), 1)[0]
        new_nb_turns = choices(compute_sup_values(["00"]), 1)[0]
        new_max_x = value
        new_min_x = value
        new_max_y = value
        new_min_y = value
        write_calibration_response = MLX903xxTestUtils.HIDppHelper.write_calibration(self,
                                                                                     nb_turns=new_nb_turns,
                                                                                     max_x=new_max_x,
                                                                                     min_x=new_min_x,
                                                                                     max_y=new_max_y,
                                                                                     min_y=new_min_y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.MessageChecker.check_fields(
            self, write_calibration_response, self.feature_9205.write_calibration_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Hardware Reset the DUT")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.ResetHelper.hardware_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        read_calibration_response = MLX903xxTestUtils.HIDppHelper.read_calibration(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "nb_turns": (checker.check_nb_turns, new_nb_turns),
            "min_x": (checker.check_min_x, new_min_x),
            "max_x": (checker.check_max_x, new_max_x),
            "min_y": (checker.check_min_y, new_min_y),
            "max_y": (checker.check_max_y, new_max_y)
        })
        checker.check_fields(self, read_calibration_response, self.feature_9205.read_calibration_response_cls,
                             check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Send WriteCalibration request to restore original calibration data")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.write_calibration(self,
                                                        nb_turns=nb_turns,
                                                        max_x=max_x,
                                                        min_x=min_x,
                                                        max_y=max_y,
                                                        min_y=min_y)

        self.testCaseChecked("BUS_9205_0009", _AUTHOR)
    # end def test_calibration_data_stored_after_power_cycle

    @features("Feature9205")
    @features("Feature1802")
    @level("Business")
    @bugtracker("Read_Write_Callibration_Format")
    def test_calibration_data_stored_after_forced_device_reset_cycle(self):
        """
        Validate Calibration data stored after force device reset

        [7] readCalibration() -> calibrationData

        [8] writeCalibration(calibrationData)

        require 0x1802 feature
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send ReadCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        read_calibration_response = MLX903xxTestUtils.HIDppHelper.read_calibration(self)
        nb_turns = read_calibration_response.nb_turns
        min_x = read_calibration_response.min_x
        max_x = read_calibration_response.max_x
        min_y = read_calibration_response.min_y
        max_y = read_calibration_response.max_y

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, read_calibration_response, self.feature_9205.read_calibration_response_cls,
                             check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteCalibration request with random values")
        # --------------------------------------------------------------------------------------------------------------
        value = choices(compute_sup_values(["0000"]), 1)[0]
        new_nb_turns = choices(compute_sup_values(["00"]), 1)[0]
        new_max_x = value
        new_min_x = value
        new_max_y = value
        new_min_y = value
        write_calibration_response = MLX903xxTestUtils.HIDppHelper.write_calibration(self,
                                                                                     nb_turns=new_nb_turns,
                                                                                     max_x=new_max_x,
                                                                                     min_x=new_min_x,
                                                                                     max_y=new_max_y,
                                                                                     min_y=new_min_y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.MessageChecker
        check_map = {}
        checker.check_fields(self, write_calibration_response,
                             self.feature_9205.write_calibration_response_cls,
                             check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ForceDeviceReset via 0x1802 HID++ feature")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        read_calibration_response = MLX903xxTestUtils.HIDppHelper.read_calibration(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MLX903xxTestUtils.ReadCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "nb_turns": (checker.check_nb_turns, new_nb_turns),
            "min_x": (checker.check_min_x, new_min_x),
            "max_x": (checker.check_max_x, new_max_x),
            "min_y": (checker.check_min_y, new_min_y),
            "max_y": (checker.check_max_y, new_max_y)
        })
        checker.check_fields(self, read_calibration_response, self.feature_9205.read_calibration_response_cls,
                             check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Send WriteCalibration request to restore original calibration data")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.write_calibration(self,
                                                        nb_turns=nb_turns,
                                                        max_x=max_x,
                                                        min_x=min_x,
                                                        max_y=max_y,
                                                        min_y=min_y)

        self.testCaseChecked("BUS_9205_0010", _AUTHOR)
    # end def test_calibration_data_stored_after_forced_device_reset_cycle

    @features("Feature9205")
    @level("Business")
    @services("Debugger")
    @skip("Require NVS_MLX903_CALIBRATION_ID")
    def test_calibration_data_returned_after_written_in_chunk(self):
        """
        Validate Calibration data returned successfully after written in chunk.

        [7] readCalibration() -> calibrationData

        require Debugger
        """
        raise NotImplementedError("To be implemented when NVS_MLX903_CALIBRATION_ID is available")
    # end def test_calibration_data_returned_after_written_in_chunk

    @features("Feature9205")
    @level("Business")
    @services("Thumbwheel")
    def test_calibration_data_stored_successfully_in_chunk(self):
        """
        Validate Calibration data stored successfully in chunk.

        [5] startCalibration()

        [6] stopCalibration() -> calibrationData
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_calibration_data_stored_successfully_in_chunk

    @features("Feature9205")
    @features("Feature2201")
    @level("Business")
    @services("Thumbwheel")
    def test_monitor_mode_report_when_dpi_changed_via_2201_during_report_duration(self):
        """
        Validate Monitor Report is sent when DPI is changed during Report duration

        [4] monitorTest(count, threshold)

        require 0x2201 feature
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_monitor_mode_report_when_dpi_changed_via_2201_during_report_duration

    @features("Feature9205")
    @features("Feature2202")
    @level("Business")
    @services("Thumbwheel")
    def test_monitor_mode_report_when_dpi_changed_via_2202_during_report_duration(self):
        """
        Validate Monitor Report is sent when DPI is changed during Report duration

        [4] monitorTest(count, threshold)

        require 0x2202 feature
        """
        raise NotImplementedError("To be implemented when @services('Thumbwheel') is available")
    # end def test_monitor_mode_report_when_dpi_changed_via_2202_during_report_duration
# end class MLX903xxBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
