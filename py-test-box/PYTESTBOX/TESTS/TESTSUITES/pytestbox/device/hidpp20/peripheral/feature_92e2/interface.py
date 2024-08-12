#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_92e2.interface
:brief: HID++ 2.0 ``TestKeysDisplay`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
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
class TestKeysDisplayInterfaceTestCase(TestKeysDisplayTestCase):
    """
    Validate ``TestKeysDisplay`` interface test cases
    """

    @features("Feature92E2")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> capabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
            }
        )
        checker.check_fields(self, response, self.feature_92e2.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature92E2")
    @level("Interface")
    def test_set_backlight_pwm_duty_cycle(self):
        """
        Validate ``SetBacklightPWMDutyCycle`` normal processing

        [1] setBacklightPWMDutyCycle(dutyPwm) -> None
        """
        duty_pwm = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetBacklightPWMDutyCycle request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.set_backlight_pwm_duty_cycle(test_case=self, duty_pwm=duty_pwm)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetBacklightPWMDutyCycleResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
        }
        checker.check_fields(self, response, self.feature_92e2.set_backlight_pwm_duty_cycle_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0002", _AUTHOR)
    # end def test_set_backlight_pwm_duty_cycle

    @features("Feature92E2")
    @level("Interface")
    def test_set_display_rgb_value(self):
        """
        Validate ``SetDisplayRGBValue`` normal processing

        [2] setDisplayRGBValue(rgbValue) -> None
        """
        rgb_value = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDisplayRGBValue request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.set_display_rgb_value(test_case=self, rgb_value=rgb_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisplayRGBValueResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
        }
        checker.check_fields(self, response, self.feature_92e2.set_display_rgb_value_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0003", _AUTHOR)
    # end def test_set_display_rgb_value

    @features("Feature92E2")
    @level("Interface")
    def test_set_display_power_state(self):
        """
        Validate ``SetDisplayPowerState`` normal processing

        [3] setDisplayPowerState(powerState) -> None
        """
        power_state = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDisplayPowerState request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.set_display_power_state(test_case=self, power_state=power_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisplayPowerStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
        }
        checker.check_fields(self, response, self.feature_92e2.set_display_power_state_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0004", _AUTHOR)
    # end def test_set_display_power_state

    @features("Feature92E2")
    @features("SupportSetKeyIcon")
    @level("Interface")
    def test_set_key_icon(self):
        """
        Validate ``SetKeyIcon`` normal processing

        [4] setKeyIcon(keyColumn, keyRow, iconIndex) -> None
        """
        key_column = 0
        key_row = 0
        icon_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetKeyIcon request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.set_key_icon(test_case=self, key_column=key_column,
                                                                     key_row=key_row, icon_index=icon_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetKeyIconResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
        }
        checker.check_fields(self, response, self.feature_92e2.set_key_icon_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0005", _AUTHOR)
    # end def test_set_key_icon

    @features("Feature92E2")
    @level("Interface")
    def test_set_key_calibration_offset(self):
        """
        Validate ``SetKeyCalibrationOffset`` normal processing

        [5] setKeyCalibrationOffset(keyColumn, ketRow, xOffset, yOffset) -> None
        """
        key_column = 0
        key_row = 0
        x_offset = 0
        y_offset = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetKeyCalibrationOffset request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset(
            test_case=self, key_column=key_column, key_row=key_row, x_offset=x_offset, y_offset=y_offset)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetKeyCalibrationOffsetResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
        }
        checker.check_fields(self, response, self.feature_92e2.set_key_calibration_offset_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0006", _AUTHOR)
    # end def test_set_key_calibration_offset

    @features("Feature92E2")
    @level("Interface")
    @services("Debugger")
    def test_set_key_calibration_offset_in_flash(self):
        """
        Validate ``SetKeyCalibrationOffsetInFlash`` normal processing

        [6] setKeyCalibrationOffsetInFlash() -> None
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetKeyCalibrationOffsetInFlash request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset_in_flash(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetKeyCalibrationOffsetInFlashResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
        }
        checker.check_fields(
            self, response, self.feature_92e2.set_key_calibration_offset_in_flash_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0007", _AUTHOR)
    # end def test_set_key_calibration_offset_in_flash

    @features("Feature92E2")
    @level("Interface")
    def test_set_display_ageing_mode_state(self):
        """
        Validate ``SetDisplayAgeingModeState`` normal processing

        [7] setDisplayAgeingModeState() -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDisplayAgeingModeState request")
        # --------------------------------------------------------------------------------------------------------------
        response = TestKeysDisplayTestUtils.HIDppHelper.set_display_ageing_mode_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisplayAgeingModeStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TestKeysDisplayTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_92e2_index))
        }
        checker.check_fields(self, response, self.feature_92e2.set_display_ageing_mode_state_response_cls, check_map)

        self.testCaseChecked("INT_92E2_0008", _AUTHOR)
    # end def test_set_display_ageing_mode_state
# end class TestKeysDisplayInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
