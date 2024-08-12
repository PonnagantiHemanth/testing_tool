#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.mouse.feature_2202.errorhandling
:brief: HID++ 2.0 ``ExtendedAdjustableDpi`` error handling test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpi
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.extendedadjustabledpiutils import ExtendedAdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.mouse.feature_2202.extendedadjustabledpi import ExtendedAdjustableDpiTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpiErrorHandlingTestCase(ExtendedAdjustableDpiTestCase):
    """
    Validate ``ExtendedAdjustableDpi`` errorhandling test cases
    """

    @features("Feature2202")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Set invalid function index shall raise a HID++ 2.0 error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over invalid_func_idx in invalid_func_idx_lis")
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_2202.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorCount request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_sensor_count_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index)
            report.functionIndex = function_index

            ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_2202_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("ErrorHandling")
    def test_wrong_sensor_index(self):
        """
        Set unsupported sensorIdx shall raise a HID++ 2.0 error
        """
        wrong_sensor_idx = to_int(self.config.F_NumSensor)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSensorCapabilities with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_capabilities_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSensorDpiRanges with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        direction = ExtendedAdjustableDpi.Direction.X
        dpi_range_req_idx = 0
        report = self.feature_2202.get_sensor_dpi_ranges_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx,
            direction=direction,
            dpi_range_req_idx=dpi_range_req_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSensorDpiList with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_dpi_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx,
            direction=direction)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSensorLodList with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_lod_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSensorDpiParameters with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_dpi_parameters_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setSensorDpiParameters with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        dpi_x = self.config.F_DefaultDpiX
        dpi_y = self.config.F_DefaultDpiY
        lod = self.config.F_DefaultLod
        report = self.feature_2202.set_sensor_dpi_parameters_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx,
            dpi_x=dpi_x,
            dpi_y=dpi_y,
            lod=lod)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send showSensorDpiStatus with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        dpi_level = 1
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.TIMER_BASED
        button_num = 0
        report = self.feature_2202.show_sensor_dpi_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx,
            dpi_level=dpi_level,
            led_hold_type=led_hold_type,
            button_num=button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getDpiCalibrationInfo with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_dpi_calibration_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        direction = ExtendedAdjustableDpi.Direction.X
        expected_count = ExtendedAdjustableDpiTestUtils.compute_expected_count(
            self, ExtendedAdjustableDpi.Direction.X, self.config.F_MouseLength)
        calib_type = ExtendedAdjustableDpi.CalibType.HW
        calib_start_timeout = 0
        calib_hw_process_timeout = 0
        calib_sw_process_timeout = 0
        report = self.feature_2202.start_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx,
            direction=direction,
            expected_count=expected_count,
            calib_type=calib_type,
            calib_start_timeout=calib_start_timeout,
            calib_hw_process_timeout=calib_hw_process_timeout,
            calib_sw_process_timeout=calib_sw_process_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setDpiCalibration with invalid sensor_idx {wrong_sensor_idx}")
        # --------------------------------------------------------------------------------------------------------------
        calib_cor = ExtendedAdjustableDpi.RevertCommand.TO_OOB_PROFILE
        report = self.feature_2202.set_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=wrong_sensor_idx,
            direction=direction,
            calib_cor=calib_cor)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_2202_0002", _AUTHOR)
    # end def test_wrong_sensor_index

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("ErrorHandling")
    def test_unsupported_direction(self):
        """
        Set unsupported direction shall raise a HID++ 2.0 error
        """
        sensor_idx = 0
        unsupported_direction = ExtendedAdjustableDpi.Direction.Y + 1 \
            if self.config.F_DpiYSupported else ExtendedAdjustableDpi.Direction.Y
        dpi_range_req_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSensorDpiRanges with invalid direction {unsupported_direction}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_dpi_ranges_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=unsupported_direction,
            dpi_range_req_idx=dpi_range_req_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSensorDpiList with invalid direction {unsupported_direction}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_dpi_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=unsupported_direction)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with invalid direction {unsupported_direction}")
        # --------------------------------------------------------------------------------------------------------------
        expected_count = ExtendedAdjustableDpiTestUtils.compute_expected_count(
            self, ExtendedAdjustableDpi.Direction.X, self.config.F_MouseLength)
        calib_type = ExtendedAdjustableDpi.CalibType.HW
        calib_start_timeout = 0
        calib_hw_process_timeout = 0
        calib_sw_process_timeout = 0
        report = self.feature_2202.start_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=unsupported_direction,
            expected_count=expected_count,
            calib_type=calib_type,
            calib_start_timeout=calib_start_timeout,
            calib_hw_process_timeout=calib_hw_process_timeout,
            calib_sw_process_timeout=calib_sw_process_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setDpiCalibration with invalid direction {unsupported_direction}")
        # --------------------------------------------------------------------------------------------------------------
        calib_cor = ExtendedAdjustableDpi.RevertCommand.TO_OOB_PROFILE
        report = self.feature_2202.set_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=unsupported_direction,
            calib_cor=calib_cor)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_2202_0003", _AUTHOR)
    # end def test_unsupported_direction

    @features("Feature2202")
    @features("NoProfileSupported")
    @level("ErrorHandling")
    def test_dpi_level_and_lod_but_not_supported_profile(self):
        """
        Send profile related requests to device shall raise a HID++ 2.0 error if the profileSupported = 0
        """
        sensor_idx = 0
        direction = ExtendedAdjustableDpi.Direction.X
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSensorDpiList with valid inputs")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_dpi_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=direction)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error NOT_ALLOWED(5)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSensorLodList with valid inputs")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_sensor_lod_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error NOT_ALLOWED(5)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_2202_0004", _AUTHOR)
    # end def test_dpi_level_and_lod_but_not_supported_profile

    @features("Feature2202")
    @features("Feature8100")
    @level("ErrorHandling")
    def test_unsupported_dpi_and_lod(self):
        """
        Set out-of-range DPI or unsupported LOD for setSensorDpiParameters shall raise a HID++ 2.0 error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        sensor_idx = 0
        dpi_min = int(self.f.PRODUCT.FEATURES.MOUSE.F_DpiMinMax[0])
        dpi_max = int(self.f.PRODUCT.FEATURES.MOUSE.F_DpiMinMax[1])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over dpi in [min_dpi - 1, max_dpi + 1]")
        # --------------------------------------------------------------------------------------------------------------
        for dpi in [dpi_min - 1, dpi_max + 1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setSensorDpiParameters with dpi = {dpi}")
            # ----------------------------------------------------------------------------------------------------------
            invalid_dpi_x = dpi
            invalid_dpi_y = dpi
            lod = self.config.F_DefaultLod
            report = self.feature_2202.set_sensor_dpi_parameters_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                dpi_x=invalid_dpi_x,
                dpi_y=invalid_dpi_y,
                lod=lod)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        invalid_lod = ExtendedAdjustableDpi.LodLevel.HIGH + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setSensorDpiParameters with invalid Lod {invalid_lod}")
        # --------------------------------------------------------------------------------------------------------------
        dpi_x = self.config.F_DefaultDpiX
        dpi_y = self.config.F_DefaultDpiY
        report = self.feature_2202.set_sensor_dpi_parameters_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            dpi_x=dpi_x,
            dpi_y=dpi_y,
            lod=invalid_lod)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_2202_0005", _AUTHOR)
    # end def test_unsupported_dpi_and_lod

    @features("Feature2202")
    @features("Feature8100")
    @level("ErrorHandling")
    def test_show_sensor_dpi_status_invalid_input(self):
        """
        Set unsupported input values for showSensorDpiStatus shall raise a HID++ 2.0 error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        sensor_idx = 0
        dpi_level = 1
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.TIMER_BASED
        button_num = 0
        invalid_dpi_level = to_int(self.config.F_NumDpiLevels) + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send showSensorDpiStatus with invalid dpiLevel {invalid_dpi_level}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.show_sensor_dpi_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            dpi_level=invalid_dpi_level,
            led_hold_type=led_hold_type,
            button_num=button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        invalid_led_hold_type = ExtendedAdjustableDpi.LedHoldType.SW_CONTROL_OFF + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send showSensorDpiStatus with invalid ledHoldType {invalid_led_hold_type}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.show_sensor_dpi_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            dpi_level=dpi_level,
            led_hold_type=invalid_led_hold_type,
            button_num=button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        led_hold_type = ExtendedAdjustableDpi.LedHoldType.EVENT_BASED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send showSensorDpiStatus with invalid numButton {button_num}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.show_sensor_dpi_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            dpi_level=dpi_level,
            led_hold_type=led_hold_type,
            button_num=button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_2202_0006", _AUTHOR)
    # end def test_show_sensor_dpi_status_invalid_input

    @features("Feature2202")
    @level("ErrorHandling")
    def test_show_sensor_dpi_status_in_onboard_mode(self):
        """
        Send showSensorDpiStatus request in Onboard mode shall raise a HID++ 2.0 error
        """
        sensor_idx = 0
        dpi_level = 1
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.TIMER_BASED
        button_num = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send showSensorDpiStatus with valid inputs")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.show_sensor_dpi_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            dpi_level=dpi_level,
            led_hold_type=led_hold_type,
            button_num=button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error NOT_ALLOWED(5)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_2202_0007", _AUTHOR)
    # end def test_show_sensor_dpi_status_in_onboard_mode

    @features("Feature2202")
    @features("Feature8100")
    @features("NoDpiCalibrationSupported")
    @level("ErrorHandling")
    def test_dpi_calibration_but_device_not_supported(self):
        """
        Send calibration related requests to device shall raise a HID++ 2.0 error if the calibrationSupported = 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getDpiCalibrationInfo with valid inputs")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.get_dpi_calibration_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error NOT_ALLOWED(5)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send startDpiCalibration with valid inputs")
        # --------------------------------------------------------------------------------------------------------------
        direction = ExtendedAdjustableDpi.Direction.X
        expected_count = ExtendedAdjustableDpiTestUtils.compute_expected_count(
            self, ExtendedAdjustableDpi.Direction.X, self.config.F_MouseLength)
        calib_type = ExtendedAdjustableDpi.CalibType.HW
        calib_start_timeout = 0
        calib_hw_process_timeout = 0
        calib_sw_process_timeout = 0
        report = self.feature_2202.start_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=direction,
            expected_count=expected_count,
            calib_type=calib_type,
            calib_start_timeout=calib_start_timeout,
            calib_hw_process_timeout=calib_hw_process_timeout,
            calib_sw_process_timeout=calib_sw_process_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error NOT_ALLOWED(5)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setDpiCalibration with valid inputs")
        # --------------------------------------------------------------------------------------------------------------
        calib_cor = ExtendedAdjustableDpi.RevertCommand.TO_OOB_PROFILE
        report = self.feature_2202.set_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=direction,
            calib_cor=calib_cor)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error NOT_ALLOWED(5)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_2202_0008", _AUTHOR)
    # end def test_dpi_calibration_but_device_not_supported

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("ErrorHandling")
    def test_start_dpi_calibration_with_invalid_input(self):
        """
        Set expectedCount, calibType and timeouts in error range to device shall raise a HID++ 2.0 error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        sensor_idx = 0
        direction = ExtendedAdjustableDpi.Direction.X
        expected_count_min = ExtendedAdjustableDpiTestUtils.compute_expected_count(self, direction, min=True)
        expected_count_max = ExtendedAdjustableDpiTestUtils.compute_expected_count(self, direction, max=True)
        calib_type = ExtendedAdjustableDpi.CalibType.HW
        calib_start_timeout = 0
        calib_hw_process_timeout = 0
        calib_sw_process_timeout = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over expect_count = [min - 1, max + 1]")
        # --------------------------------------------------------------------------------------------------------------
        for expected_count in [expected_count_min - 1, expected_count_max + 1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send startDpiCalibration with expectedCount = {expected_count}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.start_dpi_calibration_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction,
                expected_count=expected_count,
                calib_type=calib_type,
                calib_start_timeout=calib_start_timeout,
                calib_hw_process_timeout=calib_hw_process_timeout,
                calib_sw_process_timeout=calib_sw_process_timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        invalid_calib_type = ExtendedAdjustableDpi.CalibType.SW + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with calibType = {invalid_calib_type}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.start_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=direction,
            expected_count=expected_count_min,
            calib_type=invalid_calib_type,
            calib_start_timeout=calib_start_timeout,
            calib_hw_process_timeout=calib_hw_process_timeout,
            calib_sw_process_timeout=calib_sw_process_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        invalid_timeout = 61
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with calibStartTimeout = {invalid_timeout}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.start_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=direction,
            expected_count=expected_count_min,
            calib_type=calib_type,
            calib_start_timeout=invalid_timeout,
            calib_hw_process_timeout=calib_hw_process_timeout,
            calib_sw_process_timeout=calib_sw_process_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with calibHWProcessTimeout = {invalid_timeout}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.start_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=direction,
            expected_count=expected_count_min,
            calib_type=calib_type,
            calib_start_timeout=calib_start_timeout,
            calib_hw_process_timeout=invalid_timeout,
            calib_sw_process_timeout=calib_sw_process_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with calibSWProcessTimeout = {invalid_timeout}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_2202.start_dpi_calibration_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_2202_index,
            sensor_idx=sensor_idx,
            direction=direction,
            expected_count=expected_count_min,
            calib_type=ExtendedAdjustableDpi.CalibType.SW,
            calib_start_timeout=calib_start_timeout,
            calib_hw_process_timeout=calib_hw_process_timeout,
            calib_sw_process_timeout=invalid_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_2202_0009", _AUTHOR)
    # end def test_start_dpi_calibration_with_invalid_input
# end class ExtendedAdjustableDpiErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
