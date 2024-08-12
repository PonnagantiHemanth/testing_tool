#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_92e2.business
:brief: HID++ 2.0 ``TestKeysDisplay`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint

from pyharness.extensions import level
from pyharness.selector import features, services
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.testkeysdisplayutils import TestKeysDisplayTestUtils
from pytestbox.device.hidpp20.peripheral.feature_92e2.testkeysdisplay import TestKeysDisplayTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class TestKeysDisplayBusinessTestCase(TestKeysDisplayTestCase):
    """
    Validate ``TestKeysDisplay`` business test cases
    """

    @features("Feature92E2")
    @level("Business")
    def test_set_backlight_duty_pwm(self):
        """
        Validate setting different values for duty pwm parameter in Set Backlight PWM Duty Cycle API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting values for duty pwm parameter")
        # --------------------------------------------------------------------------------------------------------------
        for duty_pwm in compute_inf_values(HexList(Numeral(
                self.MAX_DUTY_PWM, self.feature_92e2.set_backlight_pwm_duty_cycle_cls.LEN.DUTY_PWM // 8)),
                is_equal=True):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBacklightPWMDutyCycle request with selected duty pwm = {duty_pwm}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_backlight_pwm_duty_cycle(self, duty_pwm)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBacklightPWMDutyCycleResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_backlight_pwm_duty_cycle_response_cls, check_map={})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_92E2_0001", _AUTHOR)
    # end def test_set_backlight_duty_pwm

    @features("Feature92E2")
    @level("Business")
    def test_set_random_color_values_for_set_display_rgb(self):
        """
        Validate setting random values for color in Set Display RGB Value API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting values of color")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(self.DEFAULT_VALUE_COUNT):
            color = HexList([randint(0, 255) for _ in range(3)])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayRGBValue request with selected color = {color}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_rgb_value(self, color)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayRGBValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_rgb_value_response_cls, check_map={})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_92E2_0002", _AUTHOR)
    # end def test_set_random_color_values_for_set_display_rgb

    @features("Feature92E2")
    @features("SupportSetKeyIcon")
    @level("Business")
    def test_set_key_icon_for_random_key_and_icon_indexes(self):
        """
        Validate Set Key Icon request can be called for random keys and icon indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting random row and column values")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(self.DEFAULT_VALUE_COUNT):
            row_index = randint(0, self.config.F_RowCount - 1)
            column_index = randint(0, self.config.F_ColumnCount - 1)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over several interesting random values of icon index")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.DEFAULT_VALUE_COUNT):
                icon_index = randint(0, self.config.F_IconCount - 1)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetKeyIcon request with selected value of row index = "
                                         f"{row_index}, column index = {column_index} and icon index = {icon_index}")
                # ------------------------------------------------------------------------------------------------------
                response = TestKeysDisplayTestUtils.HIDppHelper.set_key_icon(
                    test_case=self, key_row=row_index, key_column=column_index, icon_index=icon_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetKeyIconResponse fields")
                # ------------------------------------------------------------------------------------------------------
                checker = TestKeysDisplayTestUtils.MessageChecker
                checker.check_fields(self, response, self.feature_92e2.set_key_icon_response_cls, {})
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_92E2_0003", _AUTHOR)
    # end def test_set_key_icon_for_random_key_and_icon_indexes

    @features("Feature92E2")
    @level("Business")
    def test_set_key_calibration_offset_for_random_keys(self):
        """
        Validate Set Keys Calibration Offset  API can be called for keys selected at random
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting random values of row and column index")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(self.DEFAULT_VALUE_COUNT):
            row_index = randint(0, self.config.F_RowCount - 1)
            column_index = randint(0, self.config.F_ColumnCount - 1)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over several interesting random values of x and y offset in "
                                     "range 0x80 to 0xFF (-128 to -1) and 0x00 to 0x7F (0 to 127)")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.DEFAULT_VALUE_COUNT):
                x_offset = HexList(randint(0, 255))
                y_offset = HexList(randint(0, 255))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetKeyCalibrationOffset request with selected values of "
                                         f"row index = {row_index} column index = {column_index}, "
                                         f"x offset = {x_offset} and y offset = {y_offset}")
                # ------------------------------------------------------------------------------------------------------
                response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset(
                    self, key_row=row_index, key_column=column_index, x_offset=x_offset, y_offset=y_offset)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetKeysCalibrationOffsetResponse fields")
                # ------------------------------------------------------------------------------------------------------
                TestKeysDisplayTestUtils.MessageChecker.check_fields(
                    self, response, self.feature_92e2.set_key_calibration_offset_response_cls, check_map={})
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_92E2_0004", _AUTHOR)
    # end def test_set_key_calibration_offset_for_random_keys

    @features("Feature92E2")
    @level("Business")
    @services("Debugger")
    def test_set_key_calibration_offset_in_flash_for_random_keys_and_offset_values(self):
        """
        Validate sending Set Key Calibration Offset In Flash API after Sending Set Key Calibration Offset in Flash
        with different values of x and y offset in valid range
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting random values of row and column indexes")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(self.DEFAULT_VALUE_COUNT):
            row_index = randint(0, self.config.F_RowCount - 1)
            column_index = randint(0, self.config.F_ColumnCount - 1)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over several interesting values of x and y offset in range "
                                     "0x80 to 0xFF (-128 to -1) and 0x00 to 0x7F (0 to 127)")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.DEFAULT_VALUE_COUNT):
                x_offset = HexList(randint(0, 255))
                y_offset = HexList(randint(0, 255))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetKeyCalibrationOffset request with selected values of "
                                         f"row index = {row_index} column index = {column_index}, "
                                         f"x offset = {x_offset} and y offset = {y_offset}")
                # ------------------------------------------------------------------------------------------------------
                response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset(
                    self, key_row=row_index, key_column=column_index, x_offset=x_offset, y_offset=y_offset)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetKeyCalibrationOffsetResponse fields")
                # ------------------------------------------------------------------------------------------------------
                TestKeysDisplayTestUtils.MessageChecker.check_fields(
                    self, response, self.feature_92e2.set_key_calibration_offset_response_cls, check_map={})

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send SetKeyCalibrationOffsetInFlash request")
                # ------------------------------------------------------------------------------------------------------
                response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset_in_flash(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetKeyCalibrationOffsetInFlashResponse fields")
                # ------------------------------------------------------------------------------------------------------
                TestKeysDisplayTestUtils.MessageChecker.check_fields(
                    self, response, self.feature_92e2.set_key_calibration_offset_in_flash_response_cls, check_map={})
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_92E2_0005", _AUTHOR)
    # end def test_set_key_calibration_offset_in_flash_for_random_keys_and_offset_values

    @features("Feature92E2")
    @level("Business")
    def test_key_press_event_for_random_keys(self):
        """
        Validate pressing random keys on the device sends a key press event
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting random values of row and column indexes")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(self.DEFAULT_VALUE_COUNT):
            row_index = randint(0, self.config.F_RowCount - 1)
            col_index = randint(0, self.config.F_ColumnCount - 1)
            key = self.key_matrix[row_index][col_index]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Do a key press on the key {key.name} with row index = {row_index} and "
                                     f"column index = {col_index}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the KeyPressEvent received for key press")
            # ----------------------------------------------------------------------------------------------------------
            event = TestKeysDisplayTestUtils.HIDppHelper.key_press_event(self)
            checker = TestKeysDisplayTestUtils.KeyPressEventChecker
            check_map = checker.get_default_check_map(self)
            button_index = row_index * self.config.F_ColumnCount + col_index
            check_map.update(
                {
                    f"btn{button_index}": (getattr(checker, f"check_btn{button_index}"), True)
                }
            )
            checker.check_fields(self, event, self.feature_92e2.key_press_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Do a key release on the key {key.name} with row index = {row_index} and "
                                     f"column index = {col_index}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the KeyPressEvent received for key release")
            # ----------------------------------------------------------------------------------------------------------
            event = TestKeysDisplayTestUtils.HIDppHelper.key_press_event(self)
            checker = TestKeysDisplayTestUtils.KeyPressEventChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, event, self.feature_92e2.key_press_event_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_92E2_0006", _AUTHOR)
    # end def test_key_press_event_for_random_keys
# end class TestKeysDisplayBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
