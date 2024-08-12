#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2201.robustness
:brief: HID++ 2.0 Adjustable DPI robustness test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.mouse.feature_2201.adjustabledpi import AdjustableDpiTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AdjustableDpiRobustnessTestCase(AdjustableDpiTestCase):
    """
    Validates Adjustable DPI Robustness TestCases
    """
    @features('Feature2201')
    @features('Feature8100')
    @features('PredefinedDPI')
    @level('Robustness')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.BUTTON_1, KEY_ID.BUTTON_2,))
    def test_check_dpi_level_boundary_by_button(self):
        """
        [DPI +/- Button] Validate the DPI level won't be changed by pressed DPI + Button while in the maximum DPI level
        and vice versa.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Remap BUTTON 1 as SELECT_NEXT_DPI and BUTTON 2 as SELECT_PREVIOUS_DPI')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_and_set_function_buttons(
            self, OnboardProfiles.SectorId.PROFILE_START,
            {KEY_ID.BUTTON_1: ProfileButton.FunctionExecution.SELECT_NEXT_DPI,
             KEY_ID.BUTTON_2: ProfileButton.FunctionExecution.SELECT_PREVIOUS_DPI})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get the default DPI level index and DPI levels from settings')
        # --------------------------------------------------------------------------------------------------------------
        default_dpi_level_index = self.default_dpi_level_index
        press_count = self.current_supported_dpi_levels - default_dpi_level_index - 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Over click DPI up button then check result')
        # --------------------------------------------------------------------------------------------------------------
        self.check_over_click_dpi_button((KEY_ID.BUTTON_1, ProfileButton.FunctionExecution.SELECT_NEXT_DPI),
                                         press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Over click DPI down button then check result')
        # --------------------------------------------------------------------------------------------------------------
        self.check_over_click_dpi_button((KEY_ID.BUTTON_2, ProfileButton.FunctionExecution.SELECT_PREVIOUS_DPI),
                                         self.current_supported_dpi_levels - 1)

        self.testCaseChecked("ROB_2201_0001")
    # end def test_check_dpi_level_boundary_by_button

    @features('Feature2201')
    @level('Robustness')
    def test_padding(self):
        """
        Padding bytes shall be ignored by the firmware
        """
        for padding_byte in compute_sup_values(HexList(Numeral(
                self.feature_2201.get_sensor_count_cls.DEFAULT.PADDING,
                self.feature_2201.get_sensor_count_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetSensorCount with padding bytes: {padding_byte}')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_count_req = self.feature_2201.get_sensor_count_cls(device_index=self.deviceIndex,
                                                                          feature_index=self.feature_2201_index)

            get_sensor_count_req.padding = padding_byte
            get_sensor_count_resp = self.send_report_wait_response(
                report=get_sensor_count_req,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=self.feature_2201.get_sensor_count_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetSensorCount response received')
            # ----------------------------------------------------------------------------------------------------------
            AdjustableDpiTestUtils.GetSensorCountResponseChecker.check_fields(
                self, get_sensor_count_resp, self.feature_2201.get_sensor_count_response_cls)
        # end for

        self.testCaseChecked("ROB_2201_0002")
    # end def test_padding

    def check_over_click_dpi_button(self, remapped_button, repeat_count):
        """
        Check over click the DPI Up or Down button shall not get any changes if the DPI level is in
        the lowest or highest boundary already.

        :param remapped_button: The remapped gaming button
        :type remapped_button: ``tuple[KEY_ID, ProfileButton.FunctionExecution]``
        :param repeat_count: The number of button click
        :type repeat_count: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Shift DPI level to the level boundary by click DPI button '
                                 f'{str(remapped_button[0])}, {repeat_count} times')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(remapped_button[0], repeat=repeat_count, delay=.2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi to retrieve current DPI')
        # --------------------------------------------------------------------------------------------------------------
        current_dpi_1 = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Validate the DPI value equals to the corresponding DPI in the predefined DPI level list')
        # --------------------------------------------------------------------------------------------------------------
        predefined_dpi_level_list = AdjustableDpiTestUtils.get_predefined_dpi_levels(self)
        if remapped_button[1] == ProfileButton.FunctionExecution.SELECT_NEXT_DPI:
            expected_dpi = int(predefined_dpi_level_list[-1])
        elif remapped_button[1] == ProfileButton.FunctionExecution.SELECT_PREVIOUS_DPI:
            expected_dpi = int(predefined_dpi_level_list[0])
        else:
            raise ValueError(f'Unexpected input function execution: {str(remapped_button[1])}, '
                             f'the input function execution shall be SELECT_NEXT_DPI/SELECT_PREVIOUS_DPI')
        # end if

        self.assertEqual(expected=expected_dpi, obtained=current_dpi_1,
                         msg=f'Received DPI {current_dpi_1} but expected {expected_dpi}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Click DPI button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(remapped_button[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi to retrieve current DPI')
        # --------------------------------------------------------------------------------------------------------------
        current_dpi_2 = int(Numeral(AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self).dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the DPI value does not be changed')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=current_dpi_1, obtained=current_dpi_2,
                         msg=f'Received DPI {current_dpi_2} but expected {current_dpi_1}.')
    # end def check_over_click_dpi_button
# end class AdjustableDpiRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
