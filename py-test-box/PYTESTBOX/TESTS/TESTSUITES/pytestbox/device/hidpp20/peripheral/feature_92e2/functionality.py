#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_92e2.functionality
:brief: HID++ 2.0 ``TestKeysDisplay`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from itertools import product
from random import randint

from pyharness.extensions import level
from pyharness.selector import features, services
from pylibrary.tools.hexlist import HexList
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
class TestKeysDisplayFunctionalityTestCase(TestKeysDisplayTestCase):
    """
    Validate ``TestKeysDisplay`` functionality test cases
    """

    @features("Feature92E2")
    @level("Functionality")
    def test_set_display_rgb_value(self):
        """
        Validate setting color values: red, green, blue, black and white  using Set Display RGB Value API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over hex values of colors: red(0xFF0000), green(0x00FF00),"
                                 "blue(0x0000FF), black(0x000000), white(0xFFFFFF)")
        # --------------------------------------------------------------------------------------------------------------
        for color in [self.RED, self.GREEN, self.BLUE, self.BLACK, self.WHITE]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayRGBValue request with selected color value = {color}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_rgb_value(self, color)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayRGBValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_rgb_value_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_92E2_0001", _AUTHOR)
    # end def test_set_display_rgb_value

    @features("Feature92E2")
    @level("Functionality")
    def test_set_display_power_on_power_off_state(self):
        """
        Validate setting power on and power off states using Set Display Power State API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over power modes: power on and power off")
        # --------------------------------------------------------------------------------------------------------------
        for power_mode in [self.POWER_OFF, self.POWER_ON]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayPowerState request with selected power mode = {power_mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_power_state(self, power_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayPowerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_power_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_92E2_0002", _AUTHOR)
    # end def test_set_display_power_on_power_off_state

    @features("Feature92E2")
    @features("SupportSetKeyIcon")
    @level("Functionality")
    def test_set_key_icon_for_all_key_and_icon_index(self):
        """
        Validate Set Key Icon API can be called for all keys and all icon indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all row, column and icon indexes")
        # --------------------------------------------------------------------------------------------------------------
        for row, column, icon in list(product(range(self.config.F_RowCount), range(self.config.F_ColumnCount),
                                              range(self.config.F_IconCount))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyIcon request with selected value for row index = {row}, "
                                     f"column index = {column} and icon index = {icon}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_icon(
                self, key_row=row, key_column=column, icon_index=icon)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyIconResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_icon_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_92E2_0003", _AUTHOR)
    # end def test_set_key_icon_for_all_key_and_icon_index

    @features("Feature92E2")
    @level("Functionality")
    def test_set_key_calibration_offset_for_all_row_and_col_index(self):
        """
        Validate sending Set Key Calibration Offset request with different values of x and y offset can be sent for
        all row and col indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all row, column indexes")
        # --------------------------------------------------------------------------------------------------------------
        for row, column, _ in list(product(range(self.config.F_RowCount), range(self.config.F_ColumnCount),
                                           range(self.DEFAULT_VALUE_COUNT))):
            x = HexList(randint(0, 255))
            y = HexList(randint(0, 255))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetKeyCalibrationOffset request with selected values for row index ="
                                     f" {row}, column index = {column} x offset = {x} and y offset = {y}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset(
                self, key_row=row, key_column=column, x_offset=x, y_offset=y)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyCalibrationOffsetResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_calibration_offset_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_92E2_0004", _AUTHOR)
    # end def test_set_key_calibration_offset_for_all_row_and_col_index

    @features("Feature92E2")
    @level("Functionality")
    @services("Debugger")
    def test_set_key_calibration_offset_in_flash(self):
        """
        Validate sending Set Key Calibration Offset In Flash request after Sending Set Key Calibration Offset request
        with different values of x and y offset in valid range
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all row, column indexes")
        # --------------------------------------------------------------------------------------------------------------
        for row, column, _ in list(product(range(self.config.F_RowCount), range(self.config.F_ColumnCount),
                                           range(self.DEFAULT_VALUE_COUNT))):
            x = HexList(randint(0, 255))
            y = HexList(randint(0, 255))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetKeyCalibrationOffset request with selected values for row index = "
                                     f"{row}, column index = {column} x offset = {x} and y offset = {y}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset(
                self, key_row=row, key_column=column, x_offset=x, y_offset=y)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyCalibrationOffsetResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_calibration_offset_response_cls, {})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetKeyCalibrationOffsetInFlash request")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset_in_flash(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyCalibrationOffsetInFlashResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_calibration_offset_in_flash_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_92E2_0005", _AUTHOR)
    # end def test_set_key_calibration_offset_in_flash

    @features("Feature92E2")
    @level("Functionality")
    def test_all_keys_send_key_press_event_when_pressed_simultaneously(self):
        """
        Validate pressing all keys on the device sends a key press event
        """
        checker = TestKeysDisplayTestUtils.KeyPressEventChecker
        check_map = checker.get_default_check_map(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all row and column indexes")
        # --------------------------------------------------------------------------------------------------------------
        for row, column in list(product(range(self.config.F_RowCount), range(self.config.F_ColumnCount))):
            key = self.key_matrix[row][column]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Do a key press on the key {key.name} with the selected row index = "
                                     f"{row} and column index = {column}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the KeyPressEvent received for key press")
            # ----------------------------------------------------------------------------------------------------------
            event = TestKeysDisplayTestUtils.HIDppHelper.key_press_event(self)
            button_index = row * self.config.F_ColumnCount + column
            check_map.update(
                {
                    f"btn{button_index}": (getattr(checker, f"check_btn{button_index}"), True)
                }
            )
            checker.check_fields(self, event, self.feature_92e2.key_press_event_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all row, column indexes")
        # --------------------------------------------------------------------------------------------------------------
        for row, column in list(product(range(self.config.F_RowCount), range(self.config.F_ColumnCount))):
            key = self.key_matrix[row][column]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Do a key release on the key {key.name} with the selected row index = "
                                     f"{row} and column index = {column}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the KeyPressEvent received for key release")
            # ----------------------------------------------------------------------------------------------------------
            event = TestKeysDisplayTestUtils.HIDppHelper.key_press_event(self)
            button_index = row * self.config.F_ColumnCount + column
            check_map.update(
                {
                    f"btn{button_index}": (getattr(checker, f"check_btn{button_index}"), False)
                }
            )
            checker.check_fields(self, event, self.feature_92e2.key_press_event_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_92E2_0006", _AUTHOR)
    # end def test_all_keys_send_key_press_event_when_pressed_simultaneously

    @features("Feature92E2")
    @level("Business")
    def test_all_keys_send_key_press_event_when_pressed(self):
        """
        Validate pressing all keys on the device sends a key press event
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all row, column indexes")
        # --------------------------------------------------------------------------------------------------------------
        for row, column in list(product(range(self.config.F_RowCount), range(self.config.F_ColumnCount))):
            key = self.key_matrix[row][column]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Do a key press on the key {key.name} with the selected row index = "
                                     f"{row} and column index = {column}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the KeyPressEvent received for key press")
            # ----------------------------------------------------------------------------------------------------------
            checker = TestKeysDisplayTestUtils.KeyPressEventChecker
            check_map = checker.get_default_check_map(self)
            event = TestKeysDisplayTestUtils.HIDppHelper.key_press_event(self)
            button_index = row * self.config.F_ColumnCount + column
            check_map.update(
                {
                    f"btn{button_index}": (getattr(checker, f"check_btn{button_index}"), True)
                }
            )
            checker.check_fields(self, event, self.feature_92e2.key_press_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Do a key release on the key {key.name} with the selected row index = "
                                     f"{row} and column index = {column}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the KeyPressEvent received for key release")
            # ----------------------------------------------------------------------------------------------------------
            checker = TestKeysDisplayTestUtils.KeyPressEventChecker
            check_map = checker.get_default_check_map(self)
            event = TestKeysDisplayTestUtils.HIDppHelper.key_press_event(self)
            checker.check_fields(self, event, self.feature_92e2.key_press_event_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_92E2_0007", _AUTHOR)
    # end def test_all_keys_send_key_press_event_when_pressed
# end class TestKeysDisplayFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
