#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.mouse.feature_2251.robustness
:brief: HID++ 2.0 ``MouseWheelAnalytics`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalytics
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mousewheelanalyticsutils import MouseWheelAnalyticsTestUtils
from pytestbox.device.hidpp20.mouse.feature_2251.mousewheelanalytics import MouseWheelAnalyticsTestCase

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
class MouseWheelAnalyticsRobustnessTestCase(MouseWheelAnalyticsTestCase):
    """
    Validate ``MouseWheelAnalytics`` robustness test cases
    """

    @features("Feature2251")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> capabilities, main_count_per_turn, thumbwheel_count_per_turn

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MouseWheelAnalytics.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_2251.get_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature2251")
    @level("Robustness")
    def test_get_analytics_mode_software_id(self):
        """
        Validate ``GetAnalyticsMode`` software id field is ignored by the firmware

        [1] getAnalyticsMode() -> reporting_mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MouseWheelAnalytics.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAnalyticsMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_analytics_mode(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAnalyticsModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetAnalyticsModeResponseChecker.check_fields(
                self, response, self.feature_2251.get_analytics_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0001#2", _AUTHOR)
    # end def test_get_analytics_mode_software_id

    @features("Feature2251")
    @level("Robustness")
    def test_set_analytics_mode_software_id(self):
        """
        Validate ``SetAnalyticsMode`` software id field is ignored by the firmware

        [2] setAnalyticsMode(reporting_mode) -> reporting_mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Reporting_Mode.0xPP.0xPP

        SwID boundary values [0..F]
        """
        OFF = MouseWheelAnalytics.AnalyticsMode.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MouseWheelAnalytics.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetAnalyticsMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(
                test_case=self,
                reporting_mode=OFF,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker.check_fields(
                self, response, self.feature_2251.set_analytics_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0001#3", _AUTHOR)
    # end def test_set_analytics_mode_software_id

    @features("Feature2251")
    @level("Robustness")
    def test_get_rotation_data_software_id(self):
        """
        Validate ``GetRotaionData`` software id field is ignored by the firmware

        [3] getRotaionData() -> accPosWheel, accNegWheel, accPosThumbwheel, accNegThumbwheel

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode as ON")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(
            test_case=self, reporting_mode=MouseWheelAnalytics.AnalyticsMode.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MouseWheelAnalytics.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRotaionData request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRotaionDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker.check_fields(
                self, response, self.feature_2251.get_rotation_data_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0001#4", _AUTHOR)
    # end def test_get_rotation_data_software_id

    @features("Feature2251")
    @level("Robustness")
    def test_get_wheel_mode_data_software_id(self):
        """
        Validate ``GetWheelModeData`` software id field is ignored by the firmware

        [4] getWheelModeData() -> ratchetToFreeWheelCount, freeWheelToRatchetCount, smartShiftCount

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode as ON")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(
            test_case=self, reporting_mode=MouseWheelAnalytics.AnalyticsMode.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MouseWheelAnalytics.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetWheelModeData request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetWheelModeDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker.check_fields(
                self, response, self.feature_2251.get_wheel_mode_data_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0001#5", _AUTHOR)
    # end def test_get_wheel_mode_data_software_id

    @features("Feature2251")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> capabilities, main_count_per_turn, thumbwheel_count_per_turn

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2251.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_2251.get_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature2251")
    @level("Robustness")
    def test_get_analytics_mode_padding(self):
        """
        Validate ``GetAnalyticsMode`` padding bytes are ignored by the firmware

        [1] getAnalyticsMode() -> reporting_mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2251.get_analytics_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAnalyticsMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_analytics_mode(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAnalyticsModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetAnalyticsModeResponseChecker.check_fields(
                self, response, self.feature_2251.get_analytics_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0002#2", _AUTHOR)
    # end def test_get_analytics_mode_padding

    @features("Feature2251")
    @level("Robustness")
    def test_set_analytics_mode_padding(self):
        """
        Validate ``SetAnalyticsMode`` padding bytes are ignored by the firmware

        [2] setAnalyticsMode(reporting_mode) -> reporting_mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Reporting_Mode.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        OFF = MouseWheelAnalytics.AnalyticsMode.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2251.set_analytics_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetAnalyticsMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(
                test_case=self,
                reporting_mode=OFF,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker.check_fields(
                self, response, self.feature_2251.set_analytics_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0002#3", _AUTHOR)
    # end def test_set_analytics_mode_padding

    @features("Feature2251")
    @level("Robustness")
    def test_get_rotation_data_padding(self):
        """
        Validate ``GetRotaionData`` padding bytes are ignored by the firmware

        [3] getRotaionData() -> accPosWheel, accNegWheel, accPosThumbwheel, accNegThumbwheel

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode as ON")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(
            test_case=self, reporting_mode=MouseWheelAnalytics.AnalyticsMode.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2251.get_rotation_data_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRotaionData request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRotaionDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker.check_fields(
                self, response, self.feature_2251.get_rotation_data_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0002#4", _AUTHOR)
    # end def test_get_rotation_data_padding

    @features("Feature2251")
    @level("Robustness")
    def test_get_wheel_mode_data_padding(self):
        """
        Validate ``GetWheelModeData`` padding bytes are ignored by the firmware

        [4] getWheelModeData() -> ratchetToFreeWheelCount, freeWheelToRatchetCount, smartShiftCount

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode as ON")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(
            test_case=self, reporting_mode=MouseWheelAnalytics.AnalyticsMode.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2251.get_wheel_mode_data_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetWheelModeData request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetWheelModeDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker.check_fields(
                self, response, self.feature_2251.get_wheel_mode_data_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2251_0002#5", _AUTHOR)
    # end def test_get_wheel_mode_data_padding

    @features("Feature2251")
    @level("Robustness")
    @services("MainWheel")
    def test_wheel_motion_done_before_turning_on_analytic_mode(self):
        """
        Validate main wheel and thumbwheel motion done before setting analytics mode to ON is still being reported
        correctly by Get Rotation Data API
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        left_scrolls = 0
        right_scrolls = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Use wheel emulator to scroll up and down the main wheel")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls = randint(2, 10)
        down_scrolls = randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        if self.config.F_ThumbwheelCapability:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Use wheel emualtor to scroll left and right the thumbwheel")
            # ----------------------------------------------------------------------------------------------------------
            left_scrolls = randint(2, 10)
            right_scrolls = randint(2, 10)
            raise NotImplementedError('To be implemented when @services("Thumbwheel") (if thumbwheel is available in '
                                      'the DUT)')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode request with reporting mode = ON")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "reporting_mode": (checker.check_reporting_mode, ON)
            }
        )
        checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationDataAPI request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fiedls corresponds to emulated values for thumbwheel"
                                  "and main wheel motion")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, up_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)
        down_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, down_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)
        left_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, left_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)
        right_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, right_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_pos_wheel": (checker.check_acc_pos_wheel, down_scrolls_acc_motion_value),
                "acc_neg_wheel": (checker.check_acc_neg_wheel, up_scrolls_acc_motion_value),
                "acc_pos_thumbwheel": (checker.check_acc_pos_thumbwheel, right_scrolls_acc_motion_value),
                "acc_neg_thumbwheel": (checker.check_acc_neg_thumbwheel, left_scrolls_acc_motion_value)
            }
        )

        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("ROB_2251_0003", _AUTHOR)
    # end def test_wheel_motion_done_before_turning_on_analytic_mode

    @features("Feature2251")
    @features("SupportWheelModes")
    @level("Robustness")
    @services("MainWheel")
    @services("RequiredKeys", (KEY_ID.SMART_SHIFT,))
    def test_wheel_mode_actions_done_before_turning_on_analytic_mode(self):
        """
        Validate ratchet button presses, smart shift transitions done before setting analytics mode to ON is still
        being reported correctly by Get Wheel Mode Data API
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        ratchet_button_press_count = 0
        smart_shift_count = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Main wheel is in ratchet mode")
        # --------------------------------------------------------------------------------------------------------------
        self.set_wheel_mode(MouseWheelAnalytics.WheelMode.RATCHET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Using wheel emulator, scroll up/down the main wheel with sufficient speed multiple "
                                 "times so that smartshift transition occurs")
        # --------------------------------------------------------------------------------------------------------------
        if self.config.F_SmartShiftCapability:
            smart_shift_count = randint(2, 10)
            raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do multiple presses on ratchet switch to alternate main wheel between ratchet and "
                                 "free wheel mode")
        # --------------------------------------------------------------------------------------------------------------
        if self.config.F_RatchetFreeCapability:
            ratchet_button_press_count = randint(2, 10)
            for _ in range(ratchet_button_press_count):
                self.button_stimuli_emulator.keystroke(KEY_ID.SMART_SHIFT)
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode request with reporting mode = ON")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "reporting_mode": (checker.check_reporting_mode, ON)
            }
        )
        checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationDataAPI request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields corresponds to emulated values for thumbwheel"
                                  "and main wheel motion")
        # --------------------------------------------------------------------------------------------------------------
        ratchet_to_free_wheel_count = ratchet_button_press_count // 2 + ratchet_button_press_count % 2
        free_wheel_to_ratchet_count = ratchet_button_press_count // 2
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "ratchet_to_free_wheel_count": (checker.check_ratchet_to_free_wheel_count, ratchet_to_free_wheel_count),
                "free_wheel_to_ratchet_count": (checker.check_free_wheel_to_ratchet_count, free_wheel_to_ratchet_count),
                "smart_shift_count": (checker.check_smart_shift_count, smart_shift_count)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("ROB_2251_0004", _AUTHOR)
    # end def test_wheel_mode_actions_done_before_turning_on_analytic_mode
# end class MouseWheelAnalyticsRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
