#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_92e2.robustness
:brief: HID++ 2.0 ``TestKeysDisplay`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features, services
from pyhid.hidpp.features.peripheral.testkeysdisplay import TestKeysDisplay
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values, compute_wrong_range
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.testkeysdisplayutils import TestKeysDisplayTestUtils
from pytestbox.device.hidpp20.peripheral.feature_92e2.testkeysdisplay import TestKeysDisplayTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class TestKeysDisplayRobustnessTestCase(TestKeysDisplayTestCase):
    """
    Validate ``TestKeysDisplay`` robustness test cases
    """

    @features("Feature92E2")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        capabilities = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = TestKeysDisplayTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "capabilities": (checker.check_capabilities, capabilities)
            })
            checker.check_fields(self, response, self.feature_92e2.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature92E2")
    @level("Robustness")
    def test_set_backlight_pwm_duty_cycle_software_id(self):
        """
        Validate ``SetBacklightPWMDutyCycle`` software id field is ignored by the firmware

        [1] setBacklightPWMDutyCycle(dutyPwm) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.DutyPWM.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        duty_pwm = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBacklightPWMDutyCycle request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_backlight_pwm_duty_cycle(
                test_case=self,
                duty_pwm=duty_pwm,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBacklightPWMDutyCycleResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_backlight_pwm_duty_cycle_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#2", _AUTHOR)
    # end def test_set_backlight_pwm_duty_cycle_software_id

    @features("Feature92E2")
    @level("Robustness")
    def test_set_display_rgb_value_software_id(self):
        """
        Validate ``SetDisplayRGBValue`` software id field is ignored by the firmware

        [2] setDisplayRGBValue(rgbValue) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBValue

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        rgb_value = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayRGBValue request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_rgb_value(
                test_case=self,
                rgb_value=rgb_value,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayRGBValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_rgb_value_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#3", _AUTHOR)
    # end def test_set_display_rgb_value_software_id

    @features("Feature92E2")
    @level("Robustness")
    def test_set_display_power_state_software_id(self):
        """
        Validate ``SetDisplayPowerState`` software id field is ignored by the firmware

        [3] setDisplayPowerState(powerState) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PowerState.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        power_state = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayPowerState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_power_state(
                test_case=self,
                power_state=power_state,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayPowerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_power_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#4", _AUTHOR)
    # end def test_set_display_power_state_software_id

    @features("Feature92E2")
    @features("SupportSetKeyIcon")
    @level("Robustness")
    def test_set_key_icon_software_id(self):
        """
        Validate ``SetKeyIcon`` software id field is ignored by the firmware

        [4] setKeyIcon(keyColumn, keyRow, iconIndex) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.KeyColumn.KeyRow.IconIndex

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        key_column = 0x0
        key_row = 0x0
        icon_index = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyIcon request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_icon(
                test_case=self,
                key_column=key_column,
                key_row=key_row,
                icon_index=icon_index,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyIconResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_icon_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#5", _AUTHOR)
    # end def test_set_key_icon_software_id

    @features("Feature92E2")
    @level("Robustness")
    def test_set_key_calibration_offset_software_id(self):
        """
        Validate ``SetKeyCalibrationOffset`` software id field is ignored by the firmware

        [5] setKeyCalibrationOffset(keyColumn, ketRow, xOffset, yOffset) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.KeyColumn.KetRow.XOffset.YOffset.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        key_column = 0x0
        key_row = 0x0
        x_offset = 0x0
        y_offset = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyCalibrationOffset request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset(
                test_case=self, key_column=key_column, key_row=key_row, x_offset=x_offset, y_offset=y_offset,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyCalibrationOffsetResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_calibration_offset_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#6", _AUTHOR)
    # end def test_set_key_calibration_offset_software_id

    @features("Feature92E2")
    @level("Robustness")
    @services("Debugger")
    def test_set_key_calibration_offset_in_flash_software_id(self):
        """
        Validate ``SetKeyCalibrationOffsetInFlash`` software id field is ignored by the firmware

        [6] setKeyCalibrationOffsetInFlash() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyCalibrationOffsetInFlash request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset_in_flash(
                test_case=self, software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyCalibrationOffsetInFlashResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_calibration_offset_in_flash_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#7", _AUTHOR)
    # end def test_set_key_calibration_offset_in_flash_software_id

    @features("Feature92E2")
    @level("Robustness")
    def test_set_display_ageing_mode_state_software_id(self):
        """
        Validate ``SetDisplayAgeingModeState`` software id field is ignored by the firmware

        [7] setDisplayAgeingModeState() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TestKeysDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayAgeingModeState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_ageing_mode_state(
                test_case=self, software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayAgeingModeStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_ageing_mode_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0001#8", _AUTHOR)
    # end def test_set_display_ageing_mode_state_software_id

    @features("Feature92E2")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        capabilities = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_92e2.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.get_capabilities(
                test_case=self, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = TestKeysDisplayTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "capabilities": (checker.check_capabilities, capabilities)
            })
            checker.check_fields(self, response, self.feature_92e2.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature92E2")
    @level("Robustness")
    def test_set_backlight_pwm_duty_cycle_padding(self):
        """
        Validate ``SetBacklightPWMDutyCycle`` padding bytes are ignored by the firmware

        [1] setBacklightPWMDutyCycle(dutyPwm) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.DutyPWM.0xPP

        Padding (PP) boundary values [00..FF]
        """
        duty_pwm = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_92e2.set_backlight_pwm_duty_cycle_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBacklightPWMDutyCycle request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_backlight_pwm_duty_cycle(
                test_case=self, duty_pwm=duty_pwm, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBacklightPWMDutyCycleResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_backlight_pwm_duty_cycle_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0002#2", _AUTHOR)
    # end def test_set_backlight_pwm_duty_cycle_padding

    @features("Feature92E2")
    @level("Robustness")
    def test_set_display_power_state_padding(self):
        """
        Validate ``SetDisplayPowerState`` padding bytes are ignored by the firmware

        [3] setDisplayPowerState(powerState) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PowerState.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        power_state = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_92e2.set_display_power_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayPowerState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_power_state(
                test_case=self, power_state=power_state, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayPowerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_power_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0002#3", _AUTHOR)
    # end def test_set_display_power_state_padding

    @features("Feature92E2")
    @level("Robustness")
    def test_set_key_calibration_offset_padding(self):
        """
        Validate ``SetKeyCalibrationOffset`` padding bytes are ignored by the firmware

        [5] setKeyCalibrationOffset(keyColumn, ketRow, xOffset, yOffset) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.KeyColumn.KetRow.XOffset.YOffset.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        key_column = 0x0
        key_row = 0x0
        x_offset = 0x0
        y_offset = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_92e2.set_key_calibration_offset_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyCalibrationOffset request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset(
                test_case=self, key_column=key_column, key_row=key_row, x_offset=x_offset, y_offset=y_offset,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyCalibrationOffsetResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_calibration_offset_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0002#4", _AUTHOR)
    # end def test_set_key_calibration_offset_padding

    @features("Feature92E2")
    @level("Robustness")
    @services("Debugger")
    def test_set_key_calibration_offset_in_flash_padding(self):
        """
        Validate ``SetKeyCalibrationOffsetInFlash`` padding bytes are ignored by the firmware

        [6] setKeyCalibrationOffsetInFlash() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_92e2.set_key_calibration_offset_in_flash_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyCalibrationOffsetInFlash request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset_in_flash(
                test_case=self, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyCalibrationOffsetInFlashResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_key_calibration_offset_in_flash_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0002#5", _AUTHOR)
    # end def test_set_key_calibration_offset_in_flash_padding

    @features("Feature92E2")
    @level("Robustness")
    def test_set_display_ageing_mode_state_padding(self):
        """
        Validate ``SetDisplayAgeingModeState`` padding bytes are ignored by the firmware

        [7] setDisplayAgeingModeState() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_92e2.set_display_ageing_mode_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayAgeingModeState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_ageing_mode_state(
                test_case=self, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayAgeingModeStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_ageing_mode_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0002#6", _AUTHOR)
    # end def test_set_display_ageing_mode_state_padding

    @features("Feature92E2")
    @level("Robustness")
    def test_set_backlight_pwm_duty_cycle_with_invalid_duty_pwm(self):
        """
        Validate sending Set Backlight PWM Duty Cycle request with an invalid value of duty pwm does not return an
        error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting invalid values of duty pwm values")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_duty_pwm in compute_wrong_range(value=list(range(self.MAX_DUTY_PWM + 1)), max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetBacklightPWMDutyCycle request with selected pwm value")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_backlight_pwm_duty_cycle(
                test_case=self, duty_pwm=invalid_duty_pwm)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBacklightPWMDutyCycleResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_backlight_pwm_duty_cycle_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0003", _AUTHOR)
    # end def test_set_backlight_pwm_duty_cycle_with_invalid_duty_pwm

    @features("Feature92E2")
    @level("Robustness")
    def test_set_display_power_state_with_invalid_power_state(self):
        """
        Sending Set Display Power State with invalid value of power state does not return an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting invalid values of power state")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_power_state in compute_wrong_range(value=list(range(self.POWER_ON + 1)), max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisplayPowerState with selected value of power state = "
                                     f"{invalid_power_state}")
            # ----------------------------------------------------------------------------------------------------------
            response = TestKeysDisplayTestUtils.HIDppHelper.set_display_power_state(
                test_case=self, power_state=invalid_power_state)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisplayPowerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.MessageChecker.check_fields(
                self, response, self.feature_92e2.set_display_power_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_92E2_0004", _AUTHOR)
    # end def test_set_display_power_state_with_invalid_power_state
# end class TestKeysDisplayRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
