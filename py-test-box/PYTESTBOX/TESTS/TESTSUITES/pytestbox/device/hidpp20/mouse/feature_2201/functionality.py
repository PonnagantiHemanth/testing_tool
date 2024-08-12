#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2201.functionality
:brief: HID++ 2.0 Adjustable DPI functionality test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccess
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.tools.numeral import Numeral
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.spidirectaccessutils import HERO_SENSOR_HIGH_SPEED_THRESHOLD
from pytestbox.device.base.spidirectaccessutils import OpticalSensorName
from pytestbox.device.base.spidirectaccessutils import SPIDirectAccessTestUtils
from pytestbox.device.hidpp20.mouse.feature_2201.adjustabledpi import AdjustableDpiTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AdjustableDpiFunctionalityTestCase(AdjustableDpiTestCase):
    """
    Validates Adjustable DPI Functionality TestCases
    """
    @features('Feature2201')
    @features('Feature1E22')
    @level('Functionality')
    def test_set_min_max_dpi_value_and_check_by_x1e22(self):
        """
        Validate the minimum and maximum valid DPI values can be set as expected. Verify results from getSensorDpi
        and 0x1E22 shall be the same.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature 0x1E22 index')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1e22_index = DeviceBaseTestUtils.HIDppHelper.get_feature_index(self, SPIDirectAccess.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           'Get the minimum and maximum DPI values from DpiListReport_RANGE or DpiListReport_LIST')
        # --------------------------------------------------------------------------------------------------------------
        valid_dpi_list = AdjustableDpiTestUtils.generate_valid_dpi_list(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check set sensor DPI result by get sensor DPI and 0x1E22 optical sensor command')
        # --------------------------------------------------------------------------------------------------------------
        self.set_sensor_dpi_then_check_by_x2201_and_1e22([valid_dpi_list[0], valid_dpi_list[-1]])

        self.testCaseChecked("FUN_2201_0001")
    # end def test_set_min_max_dpi_value_and_check_by_x1e22

    @features('Feature2201')
    @features('Feature1E22')
    @features("RequiredOpticalSensors", (OpticalSensorName.HERO,))
    @level('Functionality')
    def test_set_dpi_adjacent_high_speed_threshold(self):
        """
        Validate DPI values that are adjacent the high speed threshold can be set as expected. Verify results
        from getSensorDpi and 0x1E22 shall be the same.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature 0x1E22 index')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1e22_index = DeviceBaseTestUtils.HIDppHelper.get_feature_index(self, SPIDirectAccess.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Select 3 DPI values near the high speed threshold '
                  '[high_resolution_threshold - step, high_resolution_threshold, high_resolution_threshold + step]')
        # --------------------------------------------------------------------------------------------------------------
        high_speed_dpi_threshold = HERO_SENSOR_HIGH_SPEED_THRESHOLD
        dpi_step = int(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiStep)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check set sensor DPI result by get sensor DPI and 0x1E22 optical sensor command')
        # --------------------------------------------------------------------------------------------------------------
        self.set_sensor_dpi_then_check_by_x2201_and_1e22(
            [high_speed_dpi_threshold - dpi_step, high_speed_dpi_threshold, high_speed_dpi_threshold + dpi_step])

        self.testCaseChecked("FUN_2201_0002")
    # end def test_set_dpi_adjacent_high_speed_threshold

    @features('Feature2201')
    @features('NoUSBOnly')
    @level('Functionality')
    @services('PowerSupply')
    def test_check_dpi_after_power_reset_device(self):
        """
        Change DPI by setSensorDPI then power restart device. Validate the DPI value returns to default settings.
        """
        if self.current_channel.protocol == LogitechProtocol.USB:
            self.skipTest('The test supports running on wireless mode only!')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Send setSensorDpi with the highest DPI value from DpiListReport_RANGE or DpiListReport_LIST')
        # --------------------------------------------------------------------------------------------------------------
        valid_dpi_list = AdjustableDpiTestUtils.generate_valid_dpi_list(self)
        AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(self, sensor_idx=0, dpi=int(valid_dpi_list[-1]), dpi_level=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi with sensor_idx=0')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self, sensor_idx=0)
        adjusted_dpi = AdjustableDpiTestUtils.adjust_dpi_by_high_speed_threshold(self, int(valid_dpi_list[-1]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the DPI value equals to the highest DPI value {adjusted_dpi}')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_check_map = AdjustableDpiTestUtils.GetSensorDpiResponseChecker.get_default_check_map(self)
        get_sensor_dpi_check_map['dpi'] = (AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_dpi, adjusted_dpi)
        AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_fields(
            self, get_sensor_dpi_resp, self.feature_2201.get_sensor_dpi_response_cls,
            check_map=get_sensor_dpi_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power restart DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensor Dpi')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate DPI shall return to default value')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_check_map['dpi'] = (AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_dpi,
                                           self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiDefault)
        AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_fields(
            self, get_sensor_dpi_resp, self.feature_2201.get_sensor_dpi_response_cls,
            check_map=get_sensor_dpi_check_map)

        self.testCaseChecked("FUN_2201_0003")
    # end def test_check_dpi_after_power_reset_device

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Functionality')
    @services('Debugger')
    @services('PowerSupply')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    def test_change_dpi_level_by_dpi_cycling_button_be_kept_after_power_cycle(self):
        """
        Change DPI by DPI cycling button then power restart device. Validate the DPI value and level be kept
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as DPI_CYCLING_BUTTON')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI})

        self.check_dpi_settings_by_dpi_button_after_power_cycle(KEY_ID.BUTTON_2)
        self.testCaseChecked("FUN_2201_0004#1")
    # end def test_change_dpi_level_by_dpi_cycling_button_be_kept_after_power_cycle

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Functionality')
    @services('Debugger')
    @services('PowerSupply')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    def test_change_dpi_level_by_dpi_up_down_button_be_kept_after_power_cycle(self):
        """
        Change DPI by DPI +/- button then power restart device. Validate the DPI value and level be kept
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as SELECT_NEXT_DPI')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.SELECT_NEXT_DPI})

        self.check_dpi_settings_by_dpi_button_after_power_cycle(KEY_ID.BUTTON_2)
        self.testCaseChecked("FUN_2201_0004#2")
    # end def test_change_dpi_level_by_dpi_up_down_button_be_kept_after_power_cycle

    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Functionality')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_2,))
    # TODO : Add @services('LedIndicator') when LED service is available
    def test_dpi_shift_button_change_dpi_temporary_for_all_possible_dpi(self):
        """
        Validate pressing shift button temporary changes DPI value to the lowest DPI level with all possible
        DPI values.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 2 as DPI_SHIFT_BUTTON')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.DPI_SHIFT})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get all possible dpi values from DpiListReport_RANGE or DpiListReport_LIST')
        # --------------------------------------------------------------------------------------------------------------
        valid_dpi_list = AdjustableDpiTestUtils.generate_valid_dpi_list(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the dpi in the valid_dpi_list')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi = int(predefined_dpi_levels[self.default_dpi_level_index])
        lowest_dpi_in_dpi_level = int(predefined_dpi_levels[0])
        for dpi in valid_dpi_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setSensorDpi by dpi = {dpi} and the other fields set to 0')
            # ----------------------------------------------------------------------------------------------------------
            AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(self, sensor_idx=0, dpi=int(dpi), dpi_level=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall equal to {dpi}')
            # ----------------------------------------------------------------------------------------------------------
            adjusted_dpi = AdjustableDpiTestUtils.adjust_dpi_by_high_speed_threshold(self, int(dpi))
            self.assertEqual(expected=adjusted_dpi, obtained=current_dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press and hold DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_2)
            sleep(.1)

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
            # TODO: check LED color by LED analyzer

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Release DPI shift button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_2)
            sleep(.1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getSensorDpi to get DPI')
            # ----------------------------------------------------------------------------------------------------------
            current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the DPI value shall equal to {default_dpi}')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=default_dpi, obtained=current_dpi)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2201_0005")
    # end def test_dpi_shift_button_change_dpi_temporary_for_all_possible_dpi

    def set_sensor_dpi_then_check_by_x2201_and_1e22(self, dpi_list):
        """
        Validate DPI values can be set as expected. Verify results from getSensorDpi and 0x1E22 shall be the same.

        :param dpi_list: The valid DPI list
        :type dpi_list: ``list``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over DPI in the DPI list')
        # --------------------------------------------------------------------------------------------------------------
        for dpi in dpi_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setSensorDpi with dpi={dpi} and the other fields set to 0')
            # ----------------------------------------------------------------------------------------------------------
            AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(self, sensor_idx=0, dpi=int(dpi), dpi_level=0)
            dpi_from_fw = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SPIDirectAccess with optical sensor command to get DPI from optical sensor')
            # ----------------------------------------------------------------------------------------------------------
            dpi_from_optical_sensor = SPIDirectAccessTestUtils.get_dpi(self, dpi)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the DPI value from x2201 and x1E22.')
            # ----------------------------------------------------------------------------------------------------------
            adjusted_dpi = AdjustableDpiTestUtils.adjust_dpi_by_high_speed_threshold(self, int(dpi))
            self.assertNotNone(dpi_from_optical_sensor)
            self.assertEqual(expected=adjusted_dpi, obtained=dpi_from_fw)
            self.assertTrue(adjusted_dpi - 1 <= dpi_from_optical_sensor['x'] <= adjusted_dpi + 1,
                            f'X DPI from optical sensor ({dpi_from_optical_sensor["x"]}) should be between '
                            f'{adjusted_dpi - 1} and {adjusted_dpi + 1}')
            self.assertTrue(adjusted_dpi - 1 <= dpi_from_optical_sensor['y'] <= adjusted_dpi + 1,
                            f'Y DPI from optical sensor ({dpi_from_optical_sensor["y"]}) should be between '
                            f'{adjusted_dpi - 1} and {adjusted_dpi + 1}')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def set_sensor_dpi_then_check_by_x2201_and_1e22

    def check_dpi_settings_by_dpi_button_after_power_cycle(self, dpi_button):
        """
        Change DPI by pressing the DPI button then power restart the device. Validate the DPI and level values
        are unchanged.

        :param dpi_button: The KEY_ID of DPI buttons
                           The possible values are KEY_ID.DPI_SHIFT_BUTTON or KEY_ID.DPI_UP_BUTTON
        :type dpi_button: ``KEY_ID``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Click DPI button to the next DPI level')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(dpi_button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi with sensorIdx = 0')
        # --------------------------------------------------------------------------------------------------------------
        current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the DPI equals to {predefined_dpi_list[current_level+1]}')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        default_dpi_level_index = self.default_dpi_level_index
        self.assertEqual(expected=int(predefined_dpi_levels[default_dpi_level_index + 1]), obtained=current_dpi,
                         msg=f'Received DPI {current_dpi} but expected '
                             f'{int(predefined_dpi_levels[default_dpi_level_index + 1])}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power restart DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi with sensorIdx = 0')
        # --------------------------------------------------------------------------------------------------------------
        current_dpi = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the DPI equals to {predefined_dpi_list[current_level+1]}')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=int(predefined_dpi_levels[default_dpi_level_index + 1]), obtained=current_dpi,
                         msg=f'Received DPI {current_dpi} but expected '
                             f'{int(predefined_dpi_levels[default_dpi_level_index + 1])}.')
    # end def check_dpi_settings_by_dpi_button_after_power_cycle
# end class AdjustableDpiFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
