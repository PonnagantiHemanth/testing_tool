#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.mouse.feature_2202.business
:brief: HID++ 2.0 ``ExtendedAdjustableDpi`` business test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpi
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.extendedadjustabledpiutils import ExtendedAdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.spidirectaccessutils import SPIDirectAccessTestUtils
from pytestbox.device.hidpp20.mouse.feature_2202.extendedadjustabledpi import ExtendedAdjustableDpiTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpiBusinessTestCase(ExtendedAdjustableDpiTestCase):
    """
    Validate ``ExtendedAdjustableDpi`` business test cases
    """

    @features("Feature2202")
    @level("Business")
    def test_get_all_sensors_capabilities(self):
        """
        Verify the sensor capabilities for each sensor
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over sensor_idx in range[0..{self.config.F_NumSensor}]")
        # --------------------------------------------------------------------------------------------------------------
        for sensor_idx in range(self.config.F_NumSensor):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorCapabilities request with sensor_idx = {sensor_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_capabilities(
                test_case=self, sensor_idx=sensor_idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.GetSensorCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['sensor_idx'] = (checker.check_sensor_idx, sensor_idx)
            checker.check_fields(
                self, response, self.feature_2202.get_sensor_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0001", _AUTHOR)
    # end def test_get_all_sensors_capabilities

    @features("Feature2202")
    @level("Business")
    def test_get_all_sensors_dpi_ranges(self):
        """
        Verify the DPI ranges for each direction and for each sensor
        """
        direction_list = [ExtendedAdjustableDpi.Direction.X, ExtendedAdjustableDpi.Direction.Y] \
            if self.config.F_DpiYSupported else [ExtendedAdjustableDpi.Direction.X]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over sensor_idx in range[{self.config.F_NumSensor}]")
        # --------------------------------------------------------------------------------------------------------------
        for sensor_idx in range(self.config.F_NumSensor):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Sub Loop over direction in {direction_list}")
            # ----------------------------------------------------------------------------------------------------------
            for direction in direction_list:
                dpi_range_req_idx = 0
                stop = False
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Test Sub Loop until reached the end of DPI ranges")
                # ------------------------------------------------------------------------------------------------------
                while not stop:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Send GetSensorDpiRanges request with sensor_idx = {sensor_idx}, "
                              f"direction = {direction}, dpi_range_req_idx={dpi_range_req_idx}")
                    # --------------------------------------------------------------------------------------------------
                    response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_ranges(
                        test_case=self, sensor_idx=sensor_idx, direction=direction, dpi_range_req_idx=dpi_range_req_idx)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check GetSensorDpiRangesResponse fields")
                    # --------------------------------------------------------------------------------------------------
                    checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiRangesResponseChecker
                    check_map = checker.get_default_check_map_by_req_idx(
                        test_case=self, sensor_idx=sensor_idx, direction=direction, dpi_range_req_idx=dpi_range_req_idx)
                    checker.check_fields(
                        self, response, self.feature_2202.get_sensor_dpi_ranges_response_cls, check_map)

                    # Stop the loop if dpi_ranges_n = 0x0000
                    if to_int(response.dpi_ranges_6) == 0:
                        stop = True
                    else:
                        dpi_range_req_idx += 1
                    # end if
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Sub Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Sub Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0002", _AUTHOR)
    # end def test_get_all_sensors_dpi_ranges

    @features("Feature2202")
    @features("ProfileSupported")
    @level("Business")
    def test_get_all_sensors_dpi_list(self):
        """
        Verify the DPI list for each direction and for each sensor
        """
        direction_list = [ExtendedAdjustableDpi.Direction.X, ExtendedAdjustableDpi.Direction.Y] \
            if self.config.F_DpiYSupported else [ExtendedAdjustableDpi.Direction.X]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over sensor_idx in range[{self.config.F_NumSensor}]")
        # --------------------------------------------------------------------------------------------------------------
        for sensor_idx in range(self.config.F_NumSensor):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Sub Loop over direction in {direction_list}")
            # ----------------------------------------------------------------------------------------------------------
            for direction in direction_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Send GetSensorDpiList request with sensor_idx = {sensor_idx}, direction = {direction}")
                # ------------------------------------------------------------------------------------------------------
                response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_list(
                    test_case=self, sensor_idx=sensor_idx, direction=direction)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check GetSensorDpiListResponse fields")
                # ------------------------------------------------------------------------------------------------------
                checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiListResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map['sensor_idx'] = (checker.check_sensor_idx, sensor_idx)
                check_map['direction'] = (checker.check_direction, direction)
                checker.check_fields(
                    self, response, self.feature_2202.get_sensor_dpi_list_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Sub Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0003", _AUTHOR)
    # end def test_get_all_sensors_dpi_list

    @features("Feature2202")
    @features("ProfileSupported")
    @level("Business")
    def test_get_all_sensors_lod_list(self):
        """
        Verify the LOD list for each sensor
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over sensor_idx in range[{self.config.F_NumSensor}]")
        # --------------------------------------------------------------------------------------------------------------
        for sensor_idx in range(self.config.F_NumSensor):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorLodList request with sensor_idx = {sensor_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_lod_list(
                test_case=self, sensor_idx=sensor_idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorLodListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.GetSensorLodListResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['sensor_idx'] = (checker.check_sensor_idx, sensor_idx)
            checker.check_fields(
                self, response, self.feature_2202.get_sensor_lod_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0004", _AUTHOR)
    # end def test_get_all_sensors_lod_list

    @features("Feature2202")
    @level("Business")
    def test_get_all_sensors_dpi_parameters(self):
        """
        Verify the current DPI, default DPI and LOD settings for each sensor
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over sensor_idx in range[{self.config.F_NumSensor}]")
        # --------------------------------------------------------------------------------------------------------------
        for sensor_idx in range(self.config.F_NumSensor):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorDpiParameters request with sensor_idx = {sensor_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(
                test_case=self, sensor_idx=sensor_idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorDpiParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['sensor_idx'] = (checker.check_sensor_idx, sensor_idx)
            checker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0005", _AUTHOR)
    # end def test_get_all_sensors_dpi_parameters

    @features("Feature2202")
    @features("Feature8100")
    @level('Business', 'SmokeTests')
    def test_set_dpi_parameters_for_all_sensors(self):
        """
        Change DPI X, Y by a value different from the default one for each sensor
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over sensor_idx in range[{self.config.F_NumSensor}]")
        # --------------------------------------------------------------------------------------------------------------
        dpi_x, dpi_y, lod = ExtendedAdjustableDpiTestUtils.get_none_default_dpi_parameters(self)
        expected_dpi_x, expected_dpi_y = ExtendedAdjustableDpiTestUtils.compute_expected_dpi(self, dpi_x, dpi_y)
        for sensor_idx in range(self.config.F_NumSensor):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetSensorDpiParameters request with sensor_idx = {sensor_idx} "
                                     "and set DPI and Lod with none default settings")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
                test_case=self, sensor_idx=sensor_idx, dpi_x=dpi_x, dpi_y=dpi_y, lod=lod)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.SetSensorDpiParametersResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['sensor_idx'] = (checker.check_sensor_idx, sensor_idx)
            check_map['dpi_x'] = (checker.check_dpi_x, expected_dpi_x)
            check_map['dpi_y'] = (checker.check_dpi_y, expected_dpi_y)
            check_map['lod'] = (checker.check_lod, lod)
            checker.check_fields(
                self, response, self.feature_2202.set_sensor_dpi_parameters_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0006", _AUTHOR)
    # end def test_set_dpi_parameters_for_all_sensors

    @features("Feature2202")
    @features("Feature8100")
    @features("ProfileSupported")
    @level("Business")
    def test_dpi_level_and_led_indicator(self):
        """
        Verify the device shall inform the DPI modification to the user through a LED effect while the DPI level is
        changed by SW UI in the host mode.
        """
        sensor_idx = 0
        button_num = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over dpi_level in range[{self.config.F_NumDpiLevels}]")
        # --------------------------------------------------------------------------------------------------------------
        for dpi_level_idx in range(1, self.config.F_NumDpiLevels + 1):
            dpi_x_level = int(self.config.F_DpiListX[dpi_level_idx - 1])
            dpi_y_level = int(self.config.F_DpiListY[dpi_level_idx - 1]) if self.config.F_DpiYSupported else 0
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Change DPI to the dpi_x_level: {dpi_x_level} and dpi_y_level: {dpi_y_level}")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
                test_case=self, sensor_idx=sensor_idx, dpi_x=dpi_x_level,
                dpi_y=dpi_y_level, lod=self.config.F_DefaultLod)
            self.assertEqual(dpi_x_level, to_int(response.dpi_x))
            self.assertEqual(dpi_y_level, to_int(response.dpi_y))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Show the DPI level Led to the corresponding DPI value with swControlOn")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.show_sensor_dpi_status(
                test_case=self, sensor_idx=sensor_idx, dpi_level=dpi_level_idx,
                led_hold_type=ExtendedAdjustableDpi.LedHoldType.SW_CONTROL_ON, button_num=button_num)
            self.assertEqual(dpi_level_idx, to_int(response.dpi_level))
            self.assertEqual(ExtendedAdjustableDpi.LedHoldType.SW_CONTROL_ON, to_int(response.led_hold_type))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the Led color")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Check LED color by LED analyzer

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Turn off the Led by swControlOff")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.show_sensor_dpi_status(
                test_case=self, sensor_idx=sensor_idx, dpi_level=dpi_level_idx,
                led_hold_type=ExtendedAdjustableDpi.LedHoldType.SW_CONTROL_OFF, button_num=button_num)
            self.assertEqual(dpi_level_idx, to_int(response.dpi_level))
            self.assertEqual(ExtendedAdjustableDpi.LedHoldType.SW_CONTROL_OFF, to_int(response.led_hold_type))

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0007", _AUTHOR)
    # end def test_dpi_level_and_led_indicator

    @features("Feature2202")
    @features("ProfileSupported")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_4,))
    def test_dpi_level_and_led_indicator_by_dpi_button(self):
        """
        Verify the device shall inform the DPI modification to the user through a LED effect while the DPI level is
        changed by DPI button.
        """
        self.post_requisite_reload_nvs = True
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Assign DPI cycling button to the button 4")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over dpi_level in range[{self.config.F_NumDpiLevels}]")
        # --------------------------------------------------------------------------------------------------------------
        dpi_list = [int(x) for x in self.config.F_DpiListX]
        dpi_index = dpi_list.index(to_int(self.config.F_DefaultDpiX))
        for _ in range(self.config.F_NumDpiLevels):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Click the DPI cycling button")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.BUTTON_4)
            dpi_index += 1
            if dpi_index == self.config.F_NumDpiLevels:
                dpi_index = 0
            # end if
            expected_dpi = dpi_list[dpi_index]

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check DPI level through GetSensorDpiParameters")
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_parameters_response = \
                ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
            self.assertEqual(expected_dpi, to_int(get_sensor_dpi_parameters_response.dpi_x))
            if self.config.F_DpiYSupported:
                self.assertEqual(expected_dpi, to_int(get_sensor_dpi_parameters_response.dpi_y))
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the Led color")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Check LED color by LED analyzer

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the DPI index through ActiveProfileResolutionChangedEvent")
            # ----------------------------------------------------------------------------------------------------------
            active_profile_resolution_changed_event = \
                OnboardProfilesTestUtils.HIDppHelper.active_profile_resolution_changed_event(self)
            self.assertEqual(dpi_index, to_int(active_profile_resolution_changed_event.resolution_index))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check DPI level through SetSensorDpiParametersEvent")
            # ----------------------------------------------------------------------------------------------------------
            dpi_event = ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)
            self.assertEqual(expected_dpi, to_int(dpi_event.dpi_x))
            if self.config.F_DpiYSupported:
                self.assertEqual(expected_dpi, to_int(dpi_event.dpi_y))
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0008", _AUTHOR)
    # end def test_dpi_level_and_led_indicator_by_dpi_button

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Business")
    def test_get_all_sensors_calibration_info(self):
        """
        Verify the device shall provide calibration information to SW for each sensor.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over sensor_idx in range[{self.config.F_NumSensor}]")
        # --------------------------------------------------------------------------------------------------------------
        for sensor_idx in range(self.config.F_NumSensor):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDpiCalibrationInfo request with sensor_idx = {sensor_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_dpi_calibration_info(
                test_case=self, sensor_idx=sensor_idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDpiCalibrationInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.GetDpiCalibrationInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['sensor_idx'] = (checker.check_sensor_idx, sensor_idx)
            checker.check_fields(
                self, response, self.feature_2202.get_dpi_calibration_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0009", _AUTHOR)
    # end def test_get_all_sensors_calibration_info

    @features("Feature2202")
    @features("Feature8100")
    @level("Business")
    @services("OpticalSensor")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_dpi_calibration_hw_process(self):
        """
        Verify the device supports to do DPI calibration by HW process (Single Mouse)
        """
        direction_list = [ExtendedAdjustableDpi.Direction.X, ExtendedAdjustableDpi.Direction.Y] \
            if self.config.F_DpiYSupported else [ExtendedAdjustableDpi.Direction.X]
        hw_timeout = 10
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over direction in {direction_list}")
        # --------------------------------------------------------------------------------------------------------------
        for direction in direction_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Move mouse in {direction} direction with distance = MouseLength + 10mm")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: move mouse by optical sensor emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Compute the Delta movement from HID mouse report")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: finish the implementation after optical sensor is ready

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Calculate Expected Count with MouseLength + 10mm")
            # ----------------------------------------------------------------------------------------------------------
            expected_count = ExtendedAdjustableDpiTestUtils.compute_expected_count(
                self, direction, self.config.F_MouseLength + 10)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Start DPI calibration by HW process and HWProcessTimeout = {hw_timeout}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.start_dpi_calibration(
                test_case=self, sensor_idx=0, direction=direction, expected_count=expected_count,
                calib_type=ExtendedAdjustableDpi.CalibType.HW, calib_start_timeout=hw_timeout,
                calib_hw_process_timeout=hw_timeout, calib_sw_process_timeout=hw_timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press and hold mouse left button")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Move mouse in {direction} direction with distance = MouseLength + 10mm")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: move mouse by optical sensor emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Release mouse left button")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check result through dpiCalibrationCompletedEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set the DPI calibration result to device")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: finish the implementation after optical sensor is ready

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Move mouse in {direction} direction with distance = MouseLength + 10mm")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: move mouse by optical sensor emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the new Delta movement is more closed to the Expected Count")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: finish the implementation after optical sensor is ready

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0010", _AUTHOR)
    # end def test_dpi_calibration_hw_process

    @features("Feature2202")
    @features("Feature8100")
    @features("Feature1E22")
    @features("ProfileFormatV6")
    @features("DpiCalibrationSupported")
    @level("Business")
    def test_revert_dpi_to_current_profile(self):
        """
        Verify the device supports to revert DPI calibration to the setting stored in the current profile
        """
        self.post_requisite_reload_nvs = True
        direction_list = [ExtendedAdjustableDpi.Direction.X, ExtendedAdjustableDpi.Direction.Y] \
            if self.config.F_DpiYSupported else [ExtendedAdjustableDpi.Direction.X]
        dpi_delta_x = 0xC8
        dpi_delta_y = 0xC9
        calib_cor_none_default = 0x3E8
        calib_cor_revert_profile = 0x8000
        res_cor_oob = SPIDirectAccessTestUtils._get_dpi_calibration_correction(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a user profile from OOB profile 1 but change the DPI_Delta X and Y to "
                                 "none default value")
        # --------------------------------------------------------------------------------------------------------------
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        OnboardProfilesTestUtils.Profile.create_default_profiles(
            self, {'dpi_delta_x': dpi_delta_x, 'dpi_delta_y': dpi_delta_y})
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(self, profile_id=profile_1)

        # Empty message queues
        sleep(1)
        ChannelUtils.empty_queues(test_case=self)

        # Check ResCor has been changed from Optical Sensor
        res_cor_profile = SPIDirectAccessTestUtils._get_dpi_calibration_correction(self)
        self.assertNotEqual(res_cor_profile, res_cor_oob)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over direction in {direction_list}")
        # --------------------------------------------------------------------------------------------------------------
        for direction in direction_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setDpiCalibration calibCor = none default value")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_dpi_calibration(
                test_case=self, sensor_idx=0,
                direction=direction, calib_cor=HexList(calib_cor_none_default.to_bytes(2, 'big')))
            self.assertEqual(calib_cor_none_default, to_int(response.calib_cor))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

            # Check ResCor has been changed from Optical Sensor
            res_cor = SPIDirectAccessTestUtils._get_dpi_calibration_correction(self)
            self.assertNotEqual(res_cor, res_cor_profile)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setDpiCalibration with calibCor = 0x8000")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_dpi_calibration(
                test_case=self, sensor_idx=0,
                direction=direction, calib_cor=HexList(calib_cor_revert_profile.to_bytes(2, 'big')))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the calibCor has been reverted")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.SetDpiCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['direction'] = (checker.check_direction, direction)
            check_map['calib_cor'] = (checker.check_calib_cor, calib_cor_revert_profile)
            checker.check_fields(
                self, response, self.feature_2202.set_dpi_calibration_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

            # Check ResCor has been reverted to profile default setting
            res_cor = SPIDirectAccessTestUtils._get_dpi_calibration_correction(self)
            self.assertEqual(res_cor, res_cor_profile)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0011", _AUTHOR)
    # end def test_revert_dpi_to_current_profile

    @features("Feature2202")
    @features("Feature8100")
    @features("Feature1E22")
    @features("ProfileFormatV6")
    @features("DpiCalibrationSupported")
    @level("Business")
    def test_revert_dpi_to_oob_profile(self):
        """
        Verify the device supports to revert DPI calibration to the OOB setting stored in the OOB profile
        """
        res_cor_oob = SPIDirectAccessTestUtils._get_dpi_calibration_correction(self)
        calib_cor_none_default = 0x64
        calib_cor_revert_oob = 0x0
        direction_list = [ExtendedAdjustableDpi.Direction.X, ExtendedAdjustableDpi.Direction.Y] \
            if self.config.F_DpiYSupported else [ExtendedAdjustableDpi.Direction.X]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over direction in {direction_list}")
        # --------------------------------------------------------------------------------------------------------------
        for direction in direction_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setDpiCalibration calibCor = none default value")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_dpi_calibration(
                test_case=self, sensor_idx=0,
                direction=direction, calib_cor=HexList(calib_cor_none_default.to_bytes(2, 'big')))
            self.assertEqual(calib_cor_none_default, to_int(response.calib_cor))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

            # Check ResCor has been changed from Optical Sensor
            res_cor = SPIDirectAccessTestUtils._get_dpi_calibration_correction(self)
            self.assertNotEqual(res_cor, res_cor_oob)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setDpiCalibration with calibCor = 0x0000")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_dpi_calibration(
                test_case=self, sensor_idx=0,
                direction=direction, calib_cor=HexList(calib_cor_revert_oob.to_bytes(2, 'big')))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the calibCor has been reverted")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.SetDpiCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['direction'] = (checker.check_direction, direction)
            checker.check_fields(
                self, response, self.feature_2202.set_dpi_calibration_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

            # Check ResCor has been reverted to OOB default
            res_cor = SPIDirectAccessTestUtils._get_dpi_calibration_correction(self)
            self.assertEqual(res_cor, res_cor_oob)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0012", _AUTHOR)
    # end def test_revert_dpi_to_oob_profile

    @features("Feature2202")
    @features("Feature8100")
    @features("ProfileSupported")
    @features("ProfileFormatV6")
    @level("Business")
    def test_set_dpi_from_dpi_list(self):
        """
        Verify the device supports to set DPI values from the DPI List
        """
        oob_profile_dpi_list = self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DPI_XY_LIST)[0]
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over dpi in DPI List")
        # --------------------------------------------------------------------------------------------------------------
        for dpi in oob_profile_dpi_list:
            dpi_x = dpi[0]
            dpi_y = dpi[1] if self.config.F_DpiYSupported else 0
            lod = dpi[2] if self.config.F_LodSupported else 0
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Change DPI to {dpi} for direction X and Y")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
                test_case=self, sensor_idx=sensor_idx, dpi_x=dpi_x, dpi_y=dpi_y, lod=lod)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSenorDpiParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(test_case=self,
                                                                                            sensor_idx=sensor_idx)
            checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['dpi_x'] = (checker.check_dpi_x, dpi_x)
            check_map['dpi_y'] = (checker.check_dpi_y, dpi_y)
            check_map['lod'] = (checker.check_lod, lod)
            checker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0013", _AUTHOR)
    # end def test_set_dpi_from_dpi_list

    @features("Feature2202")
    @features("ProfileSupported")
    @features("ProfileFormatV6")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_4,))
    def test_change_dpi_by_dpi_cycling_button(self):
        """
        Verify the device supports to change current DPI slot through DPI cycling button
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Assign DPI cycling button to the button 4")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Click DPI cycling button multiple times until received the DPI value that had have already")
        # --------------------------------------------------------------------------------------------------------------
        dpi_slot = []
        for _ in range(6):
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.BUTTON_4)
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, 0)
            dpi = [to_int(response.dpi_x), to_int(response.dpi_y), to_int(response.lod)]
            if dpi not in dpi_slot:
                dpi_slot.append(dpi)
            else:
                break
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Compare the collected DPI values are the same as in DPLevelList")
        # --------------------------------------------------------------------------------------------------------------
        oob_profile_dpi_list = self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DPI_XY_LIST)[0]
        self.assertEqual(expected=len(oob_profile_dpi_list), obtained=len(dpi_slot))
        for oob_dpi in oob_profile_dpi_list:
            self.assertIn(member=oob_dpi, container=dpi_slot)
        # end for

        self.testCaseChecked("BUS_2202_0014", _AUTHOR)
    # end def test_change_dpi_by_dpi_cycling_button

    @features("Feature2202")
    @features("ProfileSupported")
    @features("ProfileFormatV6")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_4, KEY_ID.BUTTON_5,))
    def test_change_dpi_by_dpi_up_down_button(self):
        """
        Verify the device supports to change current DPI slot through DPI up/down buttons
        """
        self.post_requisite_reload_nvs = True
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Assign DPI Down and Up button to button 4 and 5")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.SELECT_PREVIOUS_DPI,
             KEY_ID.BUTTON_5: ProfileButton.FunctionExecution.SELECT_NEXT_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Click DPI Down button multiple times until DPI unchanged")
        # --------------------------------------------------------------------------------------------------------------
        previous_dpi = None
        for _ in range(self.config.F_NumDpiLevels + 1):
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.BUTTON_4)
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
            dpi = [to_int(response.dpi_x), to_int(response.dpi_y), to_int(response.lod)]
            if dpi != previous_dpi:
                previous_dpi = dpi
            else:
                break
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the received DPI value equals the DPI value in the first DPI slot")
        # --------------------------------------------------------------------------------------------------------------
        oob_profile_dpi_list = self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DPI_XY_LIST)[0]
        self.assertEqual(oob_profile_dpi_list[0], obtained=previous_dpi)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Click DPI Up button multiple times until DPI unchanged")
        # --------------------------------------------------------------------------------------------------------------
        previous_dpi = None
        for _ in range(self.config.F_NumDpiLevels + 1):
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.BUTTON_5)
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
            dpi = [to_int(response.dpi_x), to_int(response.dpi_y), to_int(response.lod)]
            if dpi != previous_dpi:
                previous_dpi = dpi
            else:
                break
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the received DPI value equals the DPI value in the first DPI slot")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(oob_profile_dpi_list[-1], obtained=previous_dpi)

        self.testCaseChecked("BUS_2202_0015", _AUTHOR)
    # end def test_change_dpi_by_dpi_up_down_button

    @features("Feature2202")
    @features("ProfileSupported")
    @features("ProfileFormatV6")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_4,))
    def test_change_dpi_by_dpi_shift_button(self):
        """
        Verify the device supports to shift DPI by DPI shift button
        """
        self.post_requisite_reload_nvs = True
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Assign DPI Shift button to button 4")
        # --------------------------------------------------------------------------------------------------------------
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, profile_1, {KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.DPI_SHIFT})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over dpi_level in range[{self.config.F_NumDpiLevels}]")
        # --------------------------------------------------------------------------------------------------------------
        dpi_list_x = [int(dpi) for dpi in self.config.F_DpiListX]
        dpi_list_y = [int(dpi) for dpi in self.config.F_DpiListY]
        dpi_lod_list = [int(lod, 16) for lod in self.config.F_DpiLodList]
        for dpi_level_idx in range(self.config.F_NumDpiLevels):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Change DPI Shift index to {dpi_level_idx}")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.Profile.modify_user_profile(self, profile_1, {'shift_dpi_index': dpi_level_idx})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press and hold DPI Shift button")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.BUTTON_4)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the DPI has been shift to the DPI Level {dpi_level}")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
            checker = ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['dpi_x'] = (checker.check_dpi_x, dpi_list_x[dpi_level_idx])
            check_map['dpi_y'] = (checker.check_dpi_y, dpi_list_y[dpi_level_idx])
            check_map['lod'] = (checker.check_lod, dpi_lod_list[dpi_level_idx])
            checker.check_fields(self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the LED color changes to the color corresponding to the DPI slot")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Check LED color by LED analyzer

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Release DPI Shift button")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.BUTTON_4)
            sleep(.1)  # Wait device to take the change

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the LED color returns to the color corresponding to the DPI slot")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Check LED color by LED analyzer

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check DPI return to the default value")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(self, sensor_idx)
            ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2202_0016", _AUTHOR)
    # end def test_change_dpi_by_dpi_shift_button
# end class ExtendedAdjustableDpiBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
