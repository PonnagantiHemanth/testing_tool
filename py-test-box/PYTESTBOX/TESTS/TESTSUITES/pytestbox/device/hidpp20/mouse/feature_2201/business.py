#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2201.business
:brief: HID++ 2.0 Adjustable DPI business test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.mouse.feature_2201.adjustabledpi import AdjustableDpiTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AdjustableDpiBusinessTestCase(AdjustableDpiTestCase):
    """
    Validates Adjustable DPI Business TestCases
    """
    @features('Feature2201')
    @level('Business')
    def test_get_dpi_list_for_each_sensor(self):
        """
        Validate DpiList can be retrieved from each sensor
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f'Test Loop over sensor_idx in range [0..{self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount}]')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_list_check_map = \
            AdjustableDpiTestUtils.GetSensorDpiListResponseChecker.get_default_check_map(self)
        for s in range(int(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getSensorDpiList with sensor_idx={s}')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_list_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_list(self, sensor_idx=s)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the response from getSensorDpiList')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_list_check_map['sensor_idx'] = \
                (AdjustableDpiTestUtils.GetSensorDpiListResponseChecker.check_sensor_idx, s)
            AdjustableDpiTestUtils.GetSensorDpiListResponseChecker.check_fields(
                self, get_sensor_dpi_list_resp, self.feature_2201.get_sensor_dpi_list_response_cls,
                check_map=get_sensor_dpi_list_check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0001")
    # end def test_get_dpi_list_for_each_sensor

    @features('Feature2201')
    @level('Business')
    def test_get_dpi_for_each_sensor(self):
        """
        Validate DPI value can be retrieved from each sensor
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f'Test Loop over sensor_idx in range [0..{self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount}]')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_check_map = AdjustableDpiTestUtils.GetSensorDpiResponseChecker.get_default_check_map(self)
        for s in range(int(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getSensorDpi with sensor_idx={s}')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self, sensor_idx=s)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the response from getSensorDpi')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_check_map['dpi'] = (AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_dpi,
                                               self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiDefault)
            AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_fields(
                self, get_sensor_dpi_resp, self.feature_2201.get_sensor_dpi_response_cls,
                check_map=get_sensor_dpi_check_map)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0002")
    # end def test_get_dpi_for_each_sensor

    @features('Feature2201')
    @level('Business', 'SmokeTests')
    @bugtracker('Footloose_SetDpiForEachSensor_Dpi')
    def test_set_dpi_for_each_sensor(self):
        """
        Validate all possible DPI values can be set successfully to each sensor
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Get all possible dpi values from DpiListReportRange or DpiListReportList')
        # --------------------------------------------------------------------------------------------------------------
        valid_dpi_list = AdjustableDpiTestUtils.generate_valid_dpi_list(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f'Test Loop over sensor_idx in range [0..{self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount}]')
        # --------------------------------------------------------------------------------------------------------------
        set_sensor_dpi_check_map = AdjustableDpiTestUtils.SetSensorDpiResponseChecker.get_default_check_map(self)
        get_sensor_dpi_check_map = AdjustableDpiTestUtils.GetSensorDpiResponseChecker.get_default_check_map(self)
        for s in range(int(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount)):
            for d in valid_dpi_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f'Send setSensorDpi with sensor_idx={s}, dpi={d} and the other fields set to 0')
                # ------------------------------------------------------------------------------------------------------
                set_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(
                    self, sensor_idx=s, dpi=d, dpi_level=0)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the response from setSensorDpi')
                # ------------------------------------------------------------------------------------------------------
                set_sensor_dpi_check_map['sensor_idx'] = \
                    (AdjustableDpiTestUtils.SetSensorDpiResponseChecker.check_sensor_idx, s)
                set_sensor_dpi_check_map['dpi'] = (AdjustableDpiTestUtils.SetSensorDpiResponseChecker.check_dpi, d)
                AdjustableDpiTestUtils.SetSensorDpiResponseChecker.check_fields(
                    self, set_sensor_dpi_resp, self.feature_2201.set_sensor_dpi_response_cls,
                    check_map=set_sensor_dpi_check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send getSensorDpi with sensor_idx={s}')
                # ------------------------------------------------------------------------------------------------------
                get_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self, sensor_idx=s)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the response from getSensorDpi')
                # ------------------------------------------------------------------------------------------------------
                adjusted_dpi = AdjustableDpiTestUtils.adjust_dpi_by_high_speed_threshold(self, int(d))
                get_sensor_dpi_check_map['sensor_idx'] = \
                    (AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_sensor_idx, s)
                get_sensor_dpi_check_map['dpi'] = \
                    (AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_dpi, adjusted_dpi)
                AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_fields(
                    self, get_sensor_dpi_resp, self.feature_2201.get_sensor_dpi_response_cls,
                    check_map=get_sensor_dpi_check_map)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0003")
    # end def test_set_dpi_for_each_sensor

    @features('Feature2201v2+')
    @features('PredefinedDPI')
    @level('Business')
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_set_dpi_value_from_predefined_dpi_list(self):
        """
        Validate user can set a maximum of 5 DPI levels, each of this DPI level has a specific color assignment
        (White, Orange, Teal, Yellow, Magenta). If device has immersive lighting, validate the color on it also.

        NB: The LED color displays for 5sec and then fades
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get the predefined DPI value list from settings')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over dpi_level_index in range(dpiLevels)')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_check_map = AdjustableDpiTestUtils.GetSensorDpiResponseChecker.get_default_check_map(self)
        for dpi_level_index in range(self.current_supported_dpi_levels):
            dpi = int(predefined_dpi_levels[dpi_level_index])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Send setSensorDpi with dpi={dpi}, '
                      f'dpi level index = {dpi_level_index} and set 0 to the other fields')
            # ----------------------------------------------------------------------------------------------------------
            AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(
                    self, sensor_idx=0, dpi=dpi, dpi_level=dpi_level_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi with sensorIdx = 0')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self, sensor_idx=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Validate the DPI value shall be the same as {dpi}')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_check_map['dpi'] = (AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_dpi, dpi)
            AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_fields(
                self, get_sensor_dpi_resp, self.feature_2201.get_sensor_dpi_response_cls,
                check_map=get_sensor_dpi_check_map)

            expected_dpi_color = AdjustableDpiTestUtils.DPI_LEVEL_COLORS[dpi_level_index]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Validate LED color shall be {expected_dpi_color} and check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Validate the immersive lighting color shall be {expected_dpi_color} '
                      'and check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0004")
    # end def test_set_dpi_value_from_predefined_dpi_list

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_set_dpi_value_from_predefined_dpi_list_by_dpi_cycling_button(self):
        """
        Validate there are 5 DPI levels can be changed cycling by DPI cycling button. Check the DPI value and LED color
        in each DPI level. If device has immersive lighting, validate the color on it also.

        NB: The LED color displays for 5sec and then fades
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as DPI_CYCLING_BUTTON')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get the predefined DPI value list from settings')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi_level_index = self.default_dpi_level_index

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f'Test Loop over dpi_level_shift_count in [1..{self.current_supported_dpi_levels}]')
        # --------------------------------------------------------------------------------------------------------------
        for dpi_level_index in range(1, self.current_supported_dpi_levels + 1):
            actual_dpi_level_index = (default_dpi_level_index + dpi_level_index) % self.current_supported_dpi_levels
            expected_dpi_level = int(predefined_dpi_levels[actual_dpi_level_index])
            expected_dpi_color = AdjustableDpiTestUtils.DPI_LEVEL_COLORS[actual_dpi_level_index]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Click DPI cycling button to the DPI level {actual_dpi_level_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_2, duration=0.1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be the same as {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Validate LED color shall be {expected_dpi_color} and check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the immersive lighting color shall be {expected_dpi_color} and '
                                      'check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0005")
    # end def test_set_dpi_value_from_predefined_dpi_list_by_dpi_cycling_button

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_1, KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_set_dpi_value_from_predefined_dpi_list_by_dpi_up_down_button(self):
        """
        Validate there are 5 DPI levels can be changed cycling by DPI +/- button. Check the DPI value and LED color
        in each DPI level. If device has immersive lighting, validate the color on it also.

        NB: The LED color displays for 5sec and then fades
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 1 as SELECT_PREVIOUS_DPI and BUTTON 2 as SELECT_NEXT_DPI')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_1: ProfileButton.FunctionExecution.SELECT_PREVIOUS_DPI,
             KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.SELECT_NEXT_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get the predefined DPI value list from settings')
        # ---------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi_level_index = self.default_dpi_level_index

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Shift DPI level to the lowest DPI level by click DPI - button')
        # --------------------------------------------------------------------------------------------------------------
        repeat_count = self.current_supported_dpi_levels - default_dpi_level_index - 1
        self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_1, repeat=repeat_count, delay=.2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over dpi_level in [2..{self.current_supported_dpi_levels}]')
        # --------------------------------------------------------------------------------------------------------------
        for dpi_level_index in range(1, self.current_supported_dpi_levels):
            expected_dpi_level = int(predefined_dpi_levels[dpi_level_index])
            expected_dpi_color = AdjustableDpiTestUtils.DPI_LEVEL_COLORS[dpi_level_index]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Click DPI + button to the DPI level {dpi_level_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be the same as {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Validate LED color shall be {expected_dpi_color} and check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the immersive lighting color shall be {expected_dpi_color} and '
                                      'check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over dpi_level in [{self.current_supported_dpi_levels - 1}..1]')
        # --------------------------------------------------------------------------------------------------------------
        for dpi_level_index in range(self.current_supported_dpi_levels - 2, -1, -1):
            expected_dpi_level = int(predefined_dpi_levels[dpi_level_index])
            expected_dpi_color = AdjustableDpiTestUtils.DPI_LEVEL_COLORS[dpi_level_index]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Click DPI - button to the DPI level {dpi_level_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be the same as {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Validate LED color shall be {expected_dpi_color} and check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the immersive lighting color shall be {expected_dpi_color} and '
                                      'check the duration and state as expected')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0006")
    # end def test_set_dpi_value_from_predefined_dpi_list_by_dpi_up_down_button

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_1, KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_dpi_shift_button_change_dpi_level_temporary_with_dpi_cycling_button(self):
        """
        Validate each DPI level can be changed to the lowest DPI level while pressing the DPI shift button and then
        the DPI value is back to original DPI level after user released the DPI shift button.

        Also, check there is no LED color effect while holding DPI shift button.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 1 as CYCLE_THROUGH_DPI and BUTTON 2 as DPI_SHIFT')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_1: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI,
             KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.DPI_SHIFT})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get the predefined DPI value list from settings')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi_level_index = self.default_dpi_level_index

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f'Test Loop over dpi_level_shift_count in [1..{self.current_supported_dpi_levels}]')
        # --------------------------------------------------------------------------------------------------------------
        for dpi_level_index in range(1, self.current_supported_dpi_levels + 1):
            actual_dpi_level_index = (default_dpi_level_index + dpi_level_index) % self.current_supported_dpi_levels
            expected_dpi_level = int(predefined_dpi_levels[actual_dpi_level_index])
            lowest_dpi_in_dpi_level = int(predefined_dpi_levels[0])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Click DPI cycling button to the DPI level {actual_dpi_level_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be the same as {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press and hold DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            sniper_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be {lowest_dpi_in_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=lowest_dpi_in_dpi_level, obtained=sniper_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check there is no DPI LED status displayed ')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Release DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_2)
            sleep(.2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall equal to {expected_dpi_level }')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0007")
    # end def test_dpi_shift_button_change_dpi_level_temporary_with_dpi_cycling_button

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2, KEY_ID.BUTTON_4, KEY_ID.BUTTON_5,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_dpi_shift_button_change_dpi_level_temporary_with_dpi_up_down_button(self):
        """
        Validate each DPI level can be changed to the lowest DPI level while pressing the DPI shift button and then
        the DPI value is back to original DPI level after user released the DPI shift button.

        Also, check there is no LED color effect while holding DPI shift button.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Remap BUTTON 2 as DPI_SHIFT, BUTTON 4 as SELECT_PREVIOUS_DPI, BUTTON 5 as SELECT_NEXT_DPI')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.DPI_SHIFT,
             KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.SELECT_PREVIOUS_DPI,
             KEY_ID.BUTTON_5: ProfileButton.FunctionExecution.SELECT_NEXT_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get the predefined DPI value list from settings')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi_level_index = self.default_dpi_level_index

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Shift DPI level to the lowest DPI level by click DPI - button')
        # --------------------------------------------------------------------------------------------------------------
        repeat_count = self.current_supported_dpi_levels - default_dpi_level_index - 1
        self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_4, repeat=repeat_count, delay=.2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over dpi_level in [2..{self.current_supported_dpi_levels}]')
        # --------------------------------------------------------------------------------------------------------------
        for dpi_level_index in range(1, self.current_supported_dpi_levels):
            expected_dpi_level = int(predefined_dpi_levels[dpi_level_index])
            lowest_dpi_in_dpi_level = int(predefined_dpi_levels[0])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Click DPI + button to the DPI level {dpi_level_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_5)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be the same as {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press and hold DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            sniper_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be {lowest_dpi_in_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=lowest_dpi_in_dpi_level, obtained=sniper_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check there is no DPI LED status displayed ')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Release DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_2)
            sleep(.2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall equal to {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over dpi_level in [{self.current_supported_dpi_levels - 1}..1]')
        # --------------------------------------------------------------------------------------------------------------
        for dpi_level_index in range(self.current_supported_dpi_levels - 2, -1, -1):
            expected_dpi_level = int(predefined_dpi_levels[dpi_level_index])
            lowest_dpi_in_dpi_level = int(predefined_dpi_levels[0])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Click DPI - button to the DPI level {dpi_level_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.BUTTON_4)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be the same as {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press and hold DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            sniper_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall be {lowest_dpi_in_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=lowest_dpi_in_dpi_level, obtained=sniper_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check there is no DPI LED status displayed ')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: LED color check required not available yet

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Release DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_2)
            sleep(.2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall equal to {expected_dpi_level}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2201_0008")
    # end def test_dpi_shift_button_change_dpi_level_temporary_with_dpi_up_down_button

    @features('Feature2201')
    @features('Feature1004')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('PowerSupply')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_prioritize_led_for_dpi_and_battery_by_dpi_cycling_button(self):
        """
        Validate the DPI LED has higher priority than Battery LED notification. Click on the DPI button while the
        device new battery level LED is still on.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as DPI_CYCLING_BUTTON')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI})

        self.check_prioritize_led_for_dpi_and_battery(dpi_button=KEY_ID.BUTTON_2)
        self.testCaseChecked("BUS_2201_0009#1")
    # end def test_prioritize_led_for_dpi_and_battery_by_dpi_cycling_button

    @features('Feature2201')
    @features('Feature1004')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('PowerSupply')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_prioritize_led_for_dpi_and_battery_by_dpi_up_button(self):
        """
        Validate the DPI LED has higher priority than Battery LED notification. Click on the DPI button while the
        device new battery level LED is still on.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as SELECT_NEXT_DPI')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.SELECT_NEXT_DPI})

        self.check_prioritize_led_for_dpi_and_battery(dpi_button=KEY_ID.BUTTON_2)
        self.testCaseChecked("BUS_2201_0009#2")
    # end def test_prioritize_led_for_dpi_and_battery_by_dpi_up_button

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_prioritize_led_for_dpi_and_connectivity_by_dpi_shift_button(self):
        """
        Validate the DPI LED has higher priority than Connectivity notification. Click on the DPI button while the
        device reconnection LED is still on.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as CYCLE_THROUGH_DPI')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI})

        self.check_prioritize_led_for_dpi_and_connectivity(dpi_button=KEY_ID.BUTTON_2)
        self.testCaseChecked("BUS_2201_0010#1")
    # end def test_prioritize_led_for_dpi_and_connectivity_by_dpi_shift_button

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_prioritize_led_for_dpi_and_connectivity_by_dpi_up_button(self):
        """
        Validate the DPI LED has higher priority than Connectivity notification. Click on the DPI button while the
        device reconnection LED is still on.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as CYCLE_THROUGH_DPI')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.SELECT_NEXT_DPI})

        self.check_prioritize_led_for_dpi_and_connectivity(dpi_button=KEY_ID.BUTTON_2)
        self.testCaseChecked("BUS_2201_0010#2")
    # end def test_prioritize_led_for_dpi_and_connectivity_by_dpi_up_button

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2, KEY_ID.BUTTON_4,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_prioritize_led_for_dpi_and_profile_change_by_dpi_shift_button(self):
        """
        Validate the DPI LED has the same high priority than Profile change LED notification. Click on the DPI button
        then request a Profile change while the DPI LED is still on.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as CYCLE_THROUGH_DPI and BUTTON 4 as CYCLE_THROUGH_PROFILE')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI,
             KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.CYCLE_THROUGH_PROFILE})

        self.check_prioritize_led_for_dpi_and_profile_change(dpi_button=KEY_ID.BUTTON_2, profile_button=KEY_ID.BUTTON_4)
        self.testCaseChecked("BUS_2201_0011#1")
    # end def test_prioritize_led_for_dpi_and_profile_change_by_dpi_shift_button

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Business')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2, KEY_ID.BUTTON_4,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_prioritize_led_for_dpi_and_profile_change_by_dpi_up_button(self):
        """
        Validate the DPI LED has the same high priority than Profile change LED notification. Click on the DPI button
        then request a Profile change while the DPI LED is still on.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as SELECT_NEXT_DPI and BUTTON 4 as CYCLE_THROUGH_PROFILE')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.SELECT_NEXT_DPI,
             KEY_ID.BUTTON_4: ProfileButton.FunctionExecution.CYCLE_THROUGH_PROFILE})

        self.check_prioritize_led_for_dpi_and_profile_change(dpi_button=KEY_ID.BUTTON_2, profile_button=KEY_ID.BUTTON_4)
        self.testCaseChecked("BUS_2201_0011#2")
    # end def test_prioritize_led_for_dpi_and_profile_change_by_dpi_up_button

    def check_prioritize_led_for_dpi_and_battery(self, dpi_button):
        """
        Validate the DPI LED has higher priority than Battery LED notification. Click on the DPI button while the
        device new battery level LED is still on.

        :param dpi_button: The KEY_ID of DPI buttons
        :type dpi_button: ``KEY_ID``
        """
        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical'))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set voltage to critical level {critical_voltage}')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(critical_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Quick check the battery critical LED color in 2 seconds')
        # --------------------------------------------------------------------------------------------------------------
        # TODO : LED color check required not available yet

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Click DPI button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(dpi_button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the LED color, state, duration as expected')
        # --------------------------------------------------------------------------------------------------------------
        # TODO : LED color check required not available yet

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi to get current DPI')
        # --------------------------------------------------------------------------------------------------------------
        current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the DPI value shall be on the next DPI level')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi_level_index = self.default_dpi_level_index
        expected_dpi_level = int(predefined_dpi_levels[default_dpi_level_index + 1])
        self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)
    # end def test_prioritize_led_for_dpi_and_battery

    def check_prioritize_led_for_dpi_and_connectivity(self, dpi_button):
        """
        Validate the DPI LED has higher priority than Connectivity notification. Click on the DPI button while the
        device reconnection LED is still on.

        :param dpi_button: The KEY_ID of DPI buttons
        :type dpi_button: ``KEY_ID``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off receiver 2 seconds then power on receiver')
        # --------------------------------------------------------------------------------------------------------------
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(usb_port_index=port_index)
        sleep(2)
        self.channel_enable(usb_port_index=port_index, wait_device_notification=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Quick check the connectivity LED color in 2 seconds')
        # --------------------------------------------------------------------------------------------------------------
        # TODO : LED color check required not available yet

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Click DPI button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(dpi_button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the DPI LED color, state, duration as expected')
        # --------------------------------------------------------------------------------------------------------------
        # TODO : LED color check required not available yet

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi to get current DPI')
        # --------------------------------------------------------------------------------------------------------------
        current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the DPI value shall be on the next DPI level')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi_level_index = self.default_dpi_level_index
        expected_dpi_level = int(predefined_dpi_levels[default_dpi_level_index + 1])
        self.assertEqual(expected=expected_dpi_level, obtained=current_dpi)
    # end def check_prioritize_led_for_dpi_and_connectivity

    def check_prioritize_led_for_dpi_and_profile_change(self, dpi_button, profile_button):
        """
        Validate the DPI LED has the same high priority than Profile change LED notification. Click on the DPI button
        then request a Profile change while the DPI LED is still on.

        :param dpi_button: The KEY_ID of DPI buttons
        :type dpi_button: ``KEY_ID``
        :param profile_button: The KEY_ID of Profile button
        :type profile_button: ``KEY_ID``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Click DPI button')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.button_stimuli_emulator.keystroke(dpi_button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Quick check the DPI LED color in 2 seconds')
        # --------------------------------------------------------------------------------------------------------------
        # TODO : LED color check required not available yet

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Click Profile button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(profile_button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the DPI LED color, state, duration as expected')
        # --------------------------------------------------------------------------------------------------------------
        # TODO : LED color check required not available yet

    # end def check_prioritize_led_for_dpi_and_profile_change
# end class AdjustableDpiBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
