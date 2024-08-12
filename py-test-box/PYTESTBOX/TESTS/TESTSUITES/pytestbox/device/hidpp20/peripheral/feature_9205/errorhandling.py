#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9205.errorhandling
:brief: HID++ 2.0 ``MLX903xx`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.mlx903xxutils import MLX903xxTestUtils
from pytestbox.device.hidpp20.peripheral.feature_9205.mlx903xx import MLX903xxTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_DISABLE_MANUF_FEATURES = "Disable TDE Manufacturing Feature"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"
_VALIDATE_NOT_ALLOWED_ERROR_CODE_IS_RETURNED = "Validate NOT_ALLOWED error code is returned"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MLX903xxErrorHandlingTestCase(MLX903xxTestCase):
    """
    Validate ``MLX903xx`` errorhandling test cases
    """

    @features("Feature9205")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        register_address = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_9205.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            MLX903xxTestUtils.HIDppHelper.read_sensor_register_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                register_address=register_address,
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_9205_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature9205")
    @level("ErrorHandling")
    def test_read_sensor_register_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [0] readSensorRegister(regAddr) -> regVal, RegAddr
        """
        register_address = HexList(self.config.F_CustomerAreaUsedRegisters[0])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadSensorRegister request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.read_sensor_register_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED],
            register_address=register_address)

        self.testCaseChecked("ERR_9205_0002#1", _AUTHOR)
    # end def test_read_sensor_register_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_write_sensor_register_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [1] writeSensorRegister(regAddr, regVal)
        """
        register_address = self.config.F_CustomerAreaUsedRegisters[0]
        register_value = HexList(0xFF)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteSensorRegister request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.write_sensor_register_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED],
            register_address=register_address,
            register_value=register_value)

        self.testCaseChecked("ERR_9205_0002#2", _AUTHOR)
    # end def test_write_sensor_register_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_reset_sensor_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [2] resetSensor()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ResetSensor request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.reset_sensor_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9205_0002#3", _AUTHOR)
    # end def test_reset_sensor_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_shutdown_sensor_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [3] shutdownSensor()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ShutdownSensor request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.shutdown_sensor_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9205_0002#4", _AUTHOR)
    # end def test_shutdown_sensor_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_monitor_test_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [4] monitorTest(count, threshold)
        """
        count = 0x0
        threshold = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send MonitorTest request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.monitor_test_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED],
            count=count,
            threshold=threshold)

        self.testCaseChecked("ERR_9205_0002#5", _AUTHOR)
    # end def test_monitor_test_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_start_calibration_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [5] startCalibration()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.start_calibration_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9205_0002#6", _AUTHOR)
    # end def test_start_calibration_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_stop_calibration_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [6] stopCalibration() -> calibrationData
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StopCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.stop_calibration_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9205_0002#7", _AUTHOR)
    # end def test_stop_calibration_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_read_calibration_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [7] readCalibration() -> calibrationData
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.read_calibration_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9205_0002#8", _AUTHOR)
    # end def test_read_calibration_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_write_calibration_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [8] writeCalibration(calibrationData)
        """
        nb_turns = 0xFF
        min_x = HexList(0x0)
        max_x = HexList(0x0)
        min_y = HexList(0x0)
        max_y = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.write_calibration_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED],
            nb_turns=nb_turns,
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y)

        self.testCaseChecked("ERR_9205_0002#9", _AUTHOR)
    # end def test_write_calibration_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_read_touch_status_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [9] readTouchStatus() -> status
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadTouchStatus request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.read_touch_status_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9205_0002#10", _AUTHOR)
    # end def test_read_touch_status_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    def test_set_roller_test_without_enabling_manufacturing_features(self):
        """
        Validate the api returns NOT_ALLOWED error when manufacturing feature is disabled

        [10] setRollerTest(Multiplier, TestMode)
        """
        multiplier = 0x0
        test_mode = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _DISABLE_MANUF_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRollerTest request")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.HIDppHelper.set_roller_test_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED],
            multiplier=multiplier,
            test_mode=test_mode)

        self.testCaseChecked("ERR_9205_0002#11", _AUTHOR)
    # end def test_set_roller_test_without_enabling_manufacturing_features

    @features("Feature9205")
    @level("ErrorHandling")
    @bugtracker("WriteSensorRegisterErrorCode_NotReturned")
    def test_write_function_on_invalid_register_returns_an_error(self):
        """
        Validate Invalid Register written through Write Sensor always returns 0x00 when read back

        [1] writeSensorRegister(regAddr, regVal)
        """
        register_value = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over invalid register addresses")
        # --------------------------------------------------------------------------------------------------------------
        for register_address in compute_sup_values([self.config.F_CustomerAreaFreeRegisters[-1]])[1:]:
            if register_address.toString not in self.config.F_EpmIqs624Registers:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send WriteSensorRegister request with register_address: {register_address} "
                                         f"and register_value: {register_value}")
                # ------------------------------------------------------------------------------------------------------
                MLX903xxTestUtils.HIDppHelper.write_sensor_register_and_check_error(
                    test_case=self,
                    error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED],
                    register_address=register_address,
                    register_value=register_value)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_9205_0003", _AUTHOR)
    # end def test_write_function_on_invalid_register_returns_an_error
# end class MLX903xxErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
