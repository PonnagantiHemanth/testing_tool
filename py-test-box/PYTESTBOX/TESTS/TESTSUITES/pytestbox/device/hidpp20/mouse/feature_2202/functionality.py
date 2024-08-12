#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.mouse.feature_2202.functionality
:brief: HID++ 2.0 ``ExtendedAdjustableDpi`` functionality test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import perf_counter_ns
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpi
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.tools.numeral import to_int
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustabledpiutils import ExtendedAdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.spidirectaccessutils import SPIDirectAccessTestUtils
from pytestbox.device.hidpp20.mouse.feature_2202.extendedadjustabledpi import ExtendedAdjustableDpiTestCase
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpiFunctionalityTestCase(ExtendedAdjustableDpiTestCase):
    """
    Validate ``ExtendedAdjustableDpi`` functionality test cases
    """

    @features("Feature2202")
    @features("Feature8100")
    @features("Feature1E22")
    @level("Functionality")
    def test_set_min_medium_max_dpi(self):
        """
        Verify the min, medium and max supported DPI can be set successfully.
        """
        sensor_idx = 0
        dpi_min_medium_max = [int(x) for x in self.f.PRODUCT.FEATURES.MOUSE.F_DpiMinMax]
        dpi_medium = int(dpi_min_medium_max[1] / 2)
        if dpi_medium % 100:
            dpi_medium += 100 - dpi_medium % 100
        # end if
        dpi_min_medium_max.insert(1, dpi_medium)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over dpi in [min, medium, max] {dpi_min_medium_max}")
        # --------------------------------------------------------------------------------------------------------------
        for dpi in dpi_min_medium_max:
            dpi_x = dpi
            dpi_y = dpi if self.config.F_DpiYSupported else 0
            lod = self.config.F_DefaultLod if self.config.F_LodSupported else \
                ExtendedAdjustableDpi.LodLevel.NOT_SUPPORTED

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Change DPI to {dpi}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
                test_case=self, sensor_idx=sensor_idx, dpi_x=dpi_x, dpi_y=dpi_y, lod=lod)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(
                test_case=self, check_first_message=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the DPI has been changed to {dpi} by getSensorDpiParameters")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
            expected_dpi_x, expected_dpi_y = ExtendedAdjustableDpiTestUtils.compute_expected_dpi(self, dpi_x, dpi_y)
            checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['dpi_x'] = (checker.check_dpi_x, expected_dpi_x)
            check_map['dpi_y'] = (checker.check_dpi_y, expected_dpi_y)
            checker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the DPI has been changed to {dpi} by 0x1E22")
            # ----------------------------------------------------------------------------------------------------------
            dpi_from_optical_sensor = SPIDirectAccessTestUtils.get_dpi(self, dpi)
            self.assertEqual(expected_dpi_x, dpi_from_optical_sensor['x'])
            if self.config.F_DpiYSupported:
                self.assertEqual(dpi, dpi_from_optical_sensor['y'])
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2202_0001", _AUTHOR)
    # end def test_set_min_medium_max_dpi

    @features("Feature2202")
    @features("Feature8100")
    @features("Feature1E22")
    @features("NoReportDpiByRanges")
    @level("Functionality")
    def test_individual_dpi_value_in_dpi_ranges(self):
        """
        Verify all supported DPI values reported by DPI Ranges can be set successfully.
        """
        dpi_values_x = [int(dpi, 16) for dpi in self.config.F_DpiRangesX]
        dpi_values_y = []
        direction_list = [ExtendedAdjustableDpi.Direction.X]
        sensor_idx = 0
        dpi_x = self.config.F_DefaultDpiX
        dpi_y = 0
        if self.config.F_DpiYSupported:
            dpi_y = self.config.F_DefaultDpiY
            dpi_values_y = [int(dpi, 16) for dpi in self.config.F_DpiRangesY]
            direction_list.append(ExtendedAdjustableDpi.Direction.Y)
        # end if
        lod = self.config.F_DefaultLod if self.config.F_LodSupported else ExtendedAdjustableDpi.LodLevel.NOT_SUPPORTED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over direction in {direction_list}")
        # --------------------------------------------------------------------------------------------------------------
        for direction in direction_list:
            dpi_values = dpi_values_x if direction == ExtendedAdjustableDpi.Direction.X else dpi_values_y
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over dpi in DPI ranges")
            # ----------------------------------------------------------------------------------------------------------
            temp_dpi_x = dpi_x
            temp_dpi_y = dpi_y
            for dpi in dpi_values:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Change DPI to {dpi} for the direction {direction}")
                # ------------------------------------------------------------------------------------------------------
                if direction == ExtendedAdjustableDpi.Direction.X:
                    temp_dpi_x = dpi
                else:
                    temp_dpi_y = dpi
                # end if
                ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
                    test_case=self, sensor_idx=sensor_idx, dpi_x=temp_dpi_x, dpi_y=temp_dpi_y, lod=lod)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
                # ------------------------------------------------------------------------------------------------------
                ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(
                    test_case=self, check_first_message=False)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check the DPI has been changed to {dpi} by getSensorDpiParameters")
                # ------------------------------------------------------------------------------------------------------
                response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
                checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map['dpi_x'] = (checker.check_dpi_x, temp_dpi_x)
                check_map['dpi_y'] = (checker.check_dpi_y, temp_dpi_y)
                checker.check_fields(
                    self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check the DPI has been changed to {dpi} by 0x1E22")
                # ------------------------------------------------------------------------------------------------------
                dpi_from_optical_sensor = SPIDirectAccessTestUtils.get_dpi(self, dpi)
                self.assertEqual(temp_dpi_x, dpi_from_optical_sensor['x'])
                self.assertEqual(temp_dpi_y, dpi_from_optical_sensor['y'])
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2202_0002", _AUTHOR)
    # end def test_individual_dpi_value_in_dpi_ranges

    @features("Feature2202")
    @features("Feature8100")
    @features("Feature1E22")
    @features("ReportDpiByRanges")
    @level("Functionality")
    def test_closest_dpi(self):
        """
        Verify the device shall calculate the closest DPI value to the sensor according to the applicable range.
        """
        dpi_ranges_x = [int(dpi, 16) for dpi in self.config.F_DpiRangesX]
        dpi_ranges_y = []
        direction_list = [ExtendedAdjustableDpi.Direction.X]
        sensor_idx = 0
        dpi_x = self.config.F_DefaultDpiX
        dpi_y = 0
        if self.config.F_DpiYSupported:
            dpi_y = self.config.F_DefaultDpiY
            dpi_ranges_y = [int(dpi, 16) for dpi in self.config.F_DpiRangesY]
            direction_list.append(ExtendedAdjustableDpi.Direction.Y)
        # end if
        lod = self.config.F_DefaultLod if self.config.F_LodSupported else ExtendedAdjustableDpi.LodLevel.NOT_SUPPORTED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over direction in {direction_list}")
        # --------------------------------------------------------------------------------------------------------------
        for direction in direction_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over dpi in DPI ranges")
            # ----------------------------------------------------------------------------------------------------------
            dpi_ranges = dpi_ranges_x if direction == ExtendedAdjustableDpi.Direction.X else dpi_ranges_y
            dpi_ranges_len = len(dpi_ranges)
            temp_dpi_x = dpi_x
            temp_dpi_y = dpi_y
            if direction == ExtendedAdjustableDpi.Direction.X:
                if temp_dpi_y == self.config.F_DefaultDpiY:
                    # Test X direction, set DPI Y to the smallest DPI
                    temp_dpi_y = dpi_ranges[0]
                # end if
            else:
                # Test Y direction, set DPI X to the smallest DPI
                temp_dpi_x = dpi_ranges[0]
            # end if
            for boundary_dpi_idx in range(0, dpi_ranges_len, 2):
                dpi = dpi_ranges[boundary_dpi_idx]
                left_step = 0
                right_step = 0
                if boundary_dpi_idx == 0:
                    right_step = dpi_ranges[1] - 0xE000
                elif boundary_dpi_idx == dpi_ranges_len - 1:
                    left_step = dpi_ranges[boundary_dpi_idx - 1] - 0xE000
                else:
                    left_step = dpi_ranges[boundary_dpi_idx - 1] - 0xE000
                    right_step = dpi_ranges[boundary_dpi_idx + 1] - 0xE000
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self,
                                   f"Change DPI {dpi} - (left step {left_step} - 1) (exclude the first boundary dpi)")
                # ------------------------------------------------------------------------------------------------------
                if boundary_dpi_idx > 0:
                    if direction == ExtendedAdjustableDpi.Direction.X:
                        temp_dpi_x = dpi - (left_step - 1)
                    else:
                        temp_dpi_y = dpi - (left_step - 1)
                    # end if
                # end if

                ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
                    test_case=self, sensor_idx=sensor_idx, dpi_x=temp_dpi_x, dpi_y=temp_dpi_y, lod=lod)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
                # ------------------------------------------------------------------------------------------------------
                ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(
                    test_case=self, check_first_message=False)

                expected_dpi_x, expected_dpi_y = ExtendedAdjustableDpiTestUtils.compute_expected_dpi(
                    self, temp_dpi_x, temp_dpi_y)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check the DPI has been changed to ({expected_dpi_x}, {expected_dpi_y}) "
                                          "by getSensorDpiParameters")
                # ------------------------------------------------------------------------------------------------------
                response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
                checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map['dpi_x'] = (checker.check_dpi_x, expected_dpi_x)
                check_map['dpi_y'] = (checker.check_dpi_y, expected_dpi_y)
                checker.check_fields(
                    self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check the DPI has been changed to ({expected_dpi_x}, {expected_dpi_y}) by 0x1E22")
                # ------------------------------------------------------------------------------------------------------
                dpi_from_optical_sensor = SPIDirectAccessTestUtils.get_dpi(self, dpi)
                self.assertEqual(expected_dpi_x, dpi_from_optical_sensor['x'])
                if self.config.F_DpiYSupported:
                    self.assertEqual(expected_dpi_y, dpi_from_optical_sensor['y'])
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Change DPI {dpi} + right step {right_step} - 1 (exclude the last boundary dpi)")
                # ------------------------------------------------------------------------------------------------------
                if boundary_dpi_idx < dpi_ranges_len - 1:
                    if direction == ExtendedAdjustableDpi.Direction.X:
                        temp_dpi_x = dpi + (right_step - 1)
                    else:
                        temp_dpi_y = dpi + (right_step - 1)
                    # end if
                # end if

                ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
                    test_case=self, sensor_idx=sensor_idx, dpi_x=temp_dpi_x, dpi_y=temp_dpi_y, lod=lod)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
                # ------------------------------------------------------------------------------------------------------
                ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(
                    test_case=self, check_first_message=False)

                expected_dpi_x, expected_dpi_y = ExtendedAdjustableDpiTestUtils.compute_expected_dpi(
                    self, temp_dpi_x, temp_dpi_y)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check the DPI has been changed to ({expected_dpi_x}, {expected_dpi_y}) "
                                          "by getSensorDpiParameters")
                # ------------------------------------------------------------------------------------------------------
                response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
                checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map['dpi_x'] = (checker.check_dpi_x, expected_dpi_x)
                check_map['dpi_y'] = (checker.check_dpi_y, expected_dpi_y)
                checker.check_fields(
                    self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check the DPI has been changed to ({expected_dpi_x}, {expected_dpi_y}) by 0x1E22")
                # ------------------------------------------------------------------------------------------------------
                dpi_from_optical_sensor = SPIDirectAccessTestUtils.get_dpi(self, dpi)
                self.assertEqual(expected_dpi_x, dpi_from_optical_sensor['x'])
                if self.config.F_DpiYSupported:
                    self.assertEqual(expected_dpi_y, dpi_from_optical_sensor['y'])
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2202_0003", _AUTHOR)
    # end def test_closest_dpi

    @features("Feature2202")
    @features("Feature8100")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.BUTTON_4,))
    def test_led_hold_type(self):
        """
        Verify each ledHoldType works as expected
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Show DPI status with timerBased timeout = 2 and DPI Level = 1")
        # --------------------------------------------------------------------------------------------------------------
        sensor_index = 0
        dpi_level = 1
        button_num = 4
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.TIMER_BASED
        ExtendedAdjustableDpiTestUtils.HIDppHelper.show_sensor_dpi_status(
            self, sensor_index, dpi_level, led_hold_type, button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED color = White and check the duration")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check LED color by LED analyzer

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Onboard Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.ONBOARD_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Assign DPI Shift button to button 4")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START, {KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.DPI_SHIFT})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Show DPI status with eventBased and DPI Level = 2")
        # --------------------------------------------------------------------------------------------------------------
        dpi_level = 2
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.EVENT_BASED
        ExtendedAdjustableDpiTestUtils.HIDppHelper.show_sensor_dpi_status(
            self, sensor_index, dpi_level, led_hold_type, button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Onboard Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.ONBOARD_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press and hold DPI shift button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED color = Orange")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check LED color by LED analyzer

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release DPI Shift button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Show DPI status with swControlOn and DPI Level = 3")
        # --------------------------------------------------------------------------------------------------------------
        dpi_level = 3
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.SW_CONTROL_ON
        ExtendedAdjustableDpiTestUtils.HIDppHelper.show_sensor_dpi_status(
            self, sensor_index, dpi_level, led_hold_type, button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED color = Teal")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check LED color by LED analyzer

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Show DPI status with swControlOff and DPI Level = 3")
        # --------------------------------------------------------------------------------------------------------------
        dpi_level = 3
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.SW_CONTROL_OFF
        ExtendedAdjustableDpiTestUtils.HIDppHelper.show_sensor_dpi_status(
            self, sensor_index, dpi_level, led_hold_type, button_num)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED turned off")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check LED color by LED analyzer

        self.testCaseChecked("FUN_2202_0004", _AUTHOR)
    # end def test_led_hold_type

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Functionality")
    @services("OpticalSensor")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_start_hw_calibration_before_timeout(self):
        """
        When the user presses the Left button before calibStartTimeout expiration, the device shall:

        Set sensor to calibration DPI,
        Start calibration
        Manage Timers (Stop calibStartTimeout and Start calibHWProcessTimeout)
        """
        start_timeout = 6
        hw_timeout = 10
        expected_count = 2000
        direction = ExtendedAdjustableDpi.Direction.X
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Start DPI calibration by HW process and HWProcessTimeout = {hw_timeout}")
        # --------------------------------------------------------------------------------------------------------------
        start_time = perf_counter_ns()
        ExtendedAdjustableDpiTestUtils.HIDppHelper.start_dpi_calibration(
            test_case=self, sensor_idx=0, direction=direction, expected_count=expected_count,
            calib_type=ExtendedAdjustableDpi.CalibType.HW, calib_start_timeout=start_timeout,
            calib_hw_process_timeout=hw_timeout, calib_sw_process_timeout=hw_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Add delay until total time consuming = 5.9 seconds")
        # --------------------------------------------------------------------------------------------------------------
        sleep(5.9 - ((perf_counter_ns() - start_time)/1000000000))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press and hold mouse left button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Move mouse in X direction with properly distance")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Move mouse by optical sensor emulator

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release mouse left button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the dpiCalibrationCompletedEvent and check calibCor != 0x8000")
        # --------------------------------------------------------------------------------------------------------------
        event = ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(self)
        self.assertNotEqual(ExtendedAdjustableDpi.CALIBRATION_FAILED, to_int(event.calib_cor))

        self.testCaseChecked("FUN_2202_0005", _AUTHOR)
    # end def test_start_hw_calibration_before_timeout

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Functionality")
    @services("OpticalSensor")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_stop_hw_calibration_before_timeout(self):
        """
        When the user presses the Left button before calibStartTimeout expiration, the device shall:

        Set sensor to calibration DPI,
        Start calibration
        Manage Timers (Stop calibStartTimeout and Start calibHWProcessTimeout)
        """
        start_timeout = 6
        hw_timeout = 10
        expected_count = 2000
        direction = ExtendedAdjustableDpi.Direction.X
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Start DPI calibration by HW process and HWProcessTimeout = {hw_timeout}")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.start_dpi_calibration(
            test_case=self, sensor_idx=0, direction=direction, expected_count=expected_count,
            calib_type=ExtendedAdjustableDpi.CalibType.HW, calib_start_timeout=start_timeout,
            calib_hw_process_timeout=hw_timeout, calib_sw_process_timeout=hw_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press and hold mouse left button")
        # --------------------------------------------------------------------------------------------------------------
        start_time = perf_counter_ns()
        self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Move mouse in X direction with properly distance in 2 seconds")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Move mouse by optical sensor emulator

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Add delay until total time consuming = 9.9 seconds")
        # --------------------------------------------------------------------------------------------------------------
        sleep(9.9 - ((perf_counter_ns() - start_time) / 1000000000))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release mouse left button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check dpiCalibrationCompletedEvent.calibCor != 0x8000 and check calibDelta")
        # --------------------------------------------------------------------------------------------------------------
        event = ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(self)
        self.assertNotEqual(ExtendedAdjustableDpi.CALIBRATION_FAILED, to_int(event.calib_cor))

        self.testCaseChecked("FUN_2202_0006", _AUTHOR)
    # end def test_stop_hw_calibration_before_timeout

    @features("Feature2202")
    @features("Feature1805")
    @features("Feature1E00")
    @features("ProfileSupported")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.BUTTON_4,))
    def test_oob_default_settings(self):
        """
        Verify DPI configuration parameters are all back to OOB default settings when my device is in OOB (Out-Of-Box)
        state and if it supports an onboard profile.
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Assign DPI cycling button to the button 4")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Click DPI cycling button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.BUTTON_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DPI has been switch to the next DPI level")
        # --------------------------------------------------------------------------------------------------------------
        sensor_idx = 0
        oob_profile_dpi_xy_list = self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DPI_XY_LIST)[0]
        oob_profile_default_dpi_index = self.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[0]
        dpi_x = oob_profile_dpi_xy_list[oob_profile_default_dpi_index + 1][0]
        dpi_y = oob_profile_dpi_xy_list[oob_profile_default_dpi_index + 1][1]
        lod = oob_profile_dpi_xy_list[oob_profile_default_dpi_index + 1][2]
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
        checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['dpi_x'] = (checker.check_dpi_x, dpi_x)
        check_map['dpi_y'] = (checker.check_dpi_y, dpi_y)
        check_map['lod'] = (checker.check_lod, lod)
        checker.check_fields(
            self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Let device in OOB state")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair device and receiver")
        # --------------------------------------------------------------------------------------------------------------
        EQuadDeviceConnectionUtils.new_device_connection_and_pre_pairing(
            test_case=self, unit_ids=self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_UnitId, disconnect=True)
        self.post_requisite_reload_nvs = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DPI parameters are all back to OOB default settings")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
        ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker.check_fields(
            self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls)

        self.testCaseChecked("FUN_2202_0007", _AUTHOR)
    # end def test_oob_default_settings
# end class ExtendedAdjustableDpiFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
