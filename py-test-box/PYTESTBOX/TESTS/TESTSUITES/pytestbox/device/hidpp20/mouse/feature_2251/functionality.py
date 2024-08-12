#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.mouse.feature_2251.functionality
:brief: HID++ 2.0 ``MouseWheelAnalytics`` functionality test suite
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
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mousewheelanalyticsutils import MouseWheelAnalyticsTestUtils
from pytestbox.device.hidpp20.mouse.feature_2251.mousewheelanalytics import MouseWheelAnalyticsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MouseWheelAnalyticsFunctionalityTestCase(MouseWheelAnalyticsTestCase):
    """
    Validate ``MouseWheelAnalytics`` functionality test cases
    """

    @features("Feature2251")
    @level("Functionality")
    @services("MainWheel")
    @services("MainWheelContinuousMotion")
    def test_main_wheel_up_movement_data_resets_after_overflow(self):
        """
        Verify vertical up movement data for main wheel will reset to 0 after overflow
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
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
        LogHelper.log_step(self, "Using wheel emulator, produce a scroll up action until there is an overflow and "
                                 "reset on acc_neg_wheel register")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotaionDataResponse fields if acc_neg_wheel is zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0001", _AUTHOR)
    # end def test_main_wheel_up_movement_data_resets_after_overflow

    @features("Feature2251")
    @level("Functionality")
    @services("MainWheel")
    @services("MainWheelContinuousMotion")
    def test_main_wheel_down_movement_data_resets_after_overflow(self):
        """
        Verify vertical down movement data for main wheel will reset to 0 after overflow
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
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
        LogHelper.log_step(self, "Using wheel emulator, produce a scroll down action until there is an overflow and "
                                 "reset on acc_pos_wheel register")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotaionDataResponse fields if acc_pos_wheel is zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0002", _AUTHOR)
    # end def test_main_wheel_down_movement_data_resets_after_overflow

    @features("Feature2251")
    @features("ThumbwheelCapability")
    @level("Functionality")
    @services("Thumbwheel")
    @services("ThumbwheelContinuousMotion")
    def test_thumbwheel_right_movement_data_resets_after_overflow(self):
        """
        Verify right movement data for thumbwheel motion will reset to 0 after overflow
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode request with reporting mode  = ON")
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
        LogHelper.log_step(self, "Using wheel emulator, produce a scroll right action of thumbwheel until "
                                 "there is an overflow and reset on acc_pos_thumbwheel register")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("Thumbwheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotaionDataResponse fields if acc_pos_thumbwheel is zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0003", _AUTHOR)
    # end def test_thumbwheel_right_movement_data_reset_after_overflow

    @features("Feature2251")
    @features("ThumbwheelCapability")
    @level("Functionality")
    @services("Thumbwheel")
    @services("ThumbwheelContinuousMotion")
    def test_thumbwheel_left_movement_data_resets_after_overflow(self):
        """
        Verify left movement data for thumbwheel motion will reset to 0 after overflow
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode request with reporting mode  = ON")
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
        LogHelper.log_step(self, "Using wheel emulator, produce a scroll left action of thumbwheel until there is an "
                                 "overflow and reset on acc_neg_thumbwheel register")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("Thumbwheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotaionDataResponse fields if acc_neg_thumbwheel is zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0004", _AUTHOR)
    # end def test_thumbwheel_left_movement_data_resets_after_overflow

    @features("Feature2251")
    @features("SmartShiftCapability")
    @level("Functionality")
    @services("MainWheel")
    @services("MainWheelContinuousMotion")
    def test_smartshift_count_resets_after_overflow(self):
        """
        Verify smartshift count will reset back to 0 after overflow
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Main wheel is in ratchet mode")
        # --------------------------------------------------------------------------------------------------------------
        self.set_wheel_mode(MouseWheelAnalytics.WheelMode.RATCHET)

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
        LogHelper.log_step(self, "Using wheel emulator, emulate main wheel spins at sufficient speed for required "
                                 "number of times until there is an overflow and reset on smart_shift_count register")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Chek GetWheelModeDataResponse fields if smart_shift_count is zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0005", _AUTHOR)
    # end def test_smartshift_count_resets_after_overflow

    @features("Feature2251")
    @features("RatchetFreeCapability")
    @level("Functionality")
    @services("ExtensiveButtonPresses")
    def test_racthet_to_free_wheel_and_free_wheel_to_ratchet_count_reset_after_overflow(self):
        """
        Verify ratchet to free whel count and free wheel to ratchet count will reset back to 0 after overflow
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Main wheel is in ratchet mode")
        # --------------------------------------------------------------------------------------------------------------
        self.set_wheel_mode(MouseWheelAnalytics.WheelMode.RATCHET)

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
        LogHelper.log_step(self, "Using button emulator, press the ratchet switch repeatedly unitl overflow and reset "
                                 "occurs on ratchet_to_free_wheel_count and free_wheel_to_ratchet_count_registers")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: To be implemented when hardware supports a very large number of button presses in a short
        #  period of time

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # -------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields if ractchet_to_free_wheel_count and "
                                  "free_wheel_to_ratchet count are zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0006", _AUTHOR)
    # end def test_racthet_to_free_wheel_and_free_wheel_to_ratchet_count_reset_after_overflow

    @features("Feature2251")
    @level("Functionality")
    @services("MainWheel")
    def test_main_wheel_vertical_down_movement(self):
        """
        Verify vertical down movement data of main wheel returned by Get Rotation Data API
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
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
        LogHelper.log_step(self, "Using wheel emulator, emulate vertical down movement of main wheel")
        # --------------------------------------------------------------------------------------------------------------
        down_scrolls = randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields if the value of acc_pos_wheel_data = "
                                  "main wheel count per turn * number of full rotations of main wheel")
        # --------------------------------------------------------------------------------------------------------------
        down_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, down_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_pos_wheel": (checker.check_acc_pos_wheel, down_scrolls_acc_motion_value),
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0007", _AUTHOR)
    # end def test_main_wheel_vertical_down_movement

    @features("Feature2251")
    @level("Functionality")
    @services("MainWheel")
    def test_main_wheel_vertical_up_movement(self):
        """
        Verify vertical up movement data of main wheel returned by Get Rotation Data API
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
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
        LogHelper.log_step(self, "Using wheel emulator, emulate vertical up movement of main wheel")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls = randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the value of acc_neg_wheel_data = main wheel count per turn * number of full"
                                  "rotations of main wheel")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, up_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_neg_wheel": (checker.check_acc_neg_wheel, up_scrolls_acc_motion_value)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0008", _AUTHOR)
    # end def test_main_wheel_vertical_up_movement

    @features("Feature2251")
    @features("ThumbwheelCapability")
    @level("Functionality")
    @services("Thumbwheel")
    def test_thumbwheel_right_movement(self):
        """
        Verify right movement data of thumbwheel returned by Get Rotation Data API
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
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
        LogHelper.log_step(self, "Use wheel emulator to emulate scroll right movements of thumbwheel")
        # --------------------------------------------------------------------------------------------------------------
        right_scrolls = randint(2, 10)
        raise NotImplementedError('To be implemented when @services("Thumbwheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the value of acc_pos_thumbwheel = thumbwheel count per turn * number of full"
                                  "rotations of thumbwheel")
        # --------------------------------------------------------------------------------------------------------------
        right_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, right_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_pos_thumbwheel": (checker.check_acc_pos_thumbwheel, right_scrolls_acc_motion_value)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0009", _AUTHOR)
    # end def test_thumbwheel_right_movement

    @features("Feature2251")
    @features("ThumbwheelCapability")
    @level("Functionality")
    @services("Thumbwheel")
    def test_thumbwheel_left_movement(self):
        """
        Verify left movement data of thumbwhel returned by Get Rotation Data API
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
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
        LogHelper.log_step(self, "Use wheel emulator to emulate scroll left movements of thumbwheel")
        # --------------------------------------------------------------------------------------------------------------
        left_scroll = randint(2, 10)
        raise NotImplementedError('To be implemented when @services("Thumbwheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the value of acc_neg_thumbwheel = thumbwheel count per turn * number of full"
                                  "rotations of thumbwheel")
        # --------------------------------------------------------------------------------------------------------------
        left_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, left_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_neg_thumbwheel": (checker.check_acc_neg_thumbwheel, left_scrolls_acc_motion_value)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0010", _AUTHOR)
    # end def test_thumbwheel_left_movement

    @features("Feature2251")
    @features("RatchetFreeCapability")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.SMART_SHIFT,))
    def test_ratchet_to_free_wheel_count(self):
        """
        Verify ratchet to free wheel count reported correctly by Get Wheel Mode Data API
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Main wheel is set to ratchet mode")
        # --------------------------------------------------------------------------------------------------------------
        self.set_wheel_mode(MouseWheelAnalytics.WheelMode.RATCHET)

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
        LogHelper.log_step(self, "Press ratchet buton once to change wheel mode from ratchet to free wheel mode")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.SMART_SHIFT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields if ratchet to free wheel count is 1")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "ratchet_to_free_wheel_count": (checker.check_ratchet_to_free_wheel_count, 1),
            }
        )

        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0011", _AUTHOR)
    # end def test_ratchet_to_free_wheel_count

    @features("Feature2251")
    @features("RatchetFreeCapability")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.SMART_SHIFT,))
    def test_free_wheel_to_ratchet_count(self):
        """
        Verify free wheel to ratchet count reported correctly by Get Wheel Mode Data API
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Main wheel is set to free wheel mode")
        # --------------------------------------------------------------------------------------------------------------
        self.set_wheel_mode(MouseWheelAnalytics.WheelMode.FREE_SPIN)

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
        LogHelper.log_step(self, "Press ratchet buton once to change wheel mode from free wheel to ratchet mode")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.SMART_SHIFT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields if free wheel to ratchet count is 1")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "free_wheel_to_ratchet_count": (checker.check_free_wheel_to_ratchet_count, 1),
            }
        )

        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0012", _AUTHOR)
    # end def test_free_wheel_to_ratchet_count

    @features("Feature2251")
    @features("SmartShiftCapability")
    @level("Functionality")
    @services("MainWheel")
    def test_smartshift_count(self):
        """
        Verify smart shift count reported correctly by Get Wheel Mode Data API
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Main wheel is set to ratchet mode")
        # --------------------------------------------------------------------------------------------------------------
        self.set_wheel_mode(MouseWheelAnalytics.WheelMode.RATCHET)

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
        LogHelper.log_step(self, "Using wheel emulator, scroll UP/DOWN the main wheel with sufficient speed such that "
                                 "main wheel goes into free wheel mode once")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields if smart_shift_count is 1")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "smart_shift_count": (checker.check_smart_shift_count, 1),
            }
        )

        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0013", _AUTHOR)
    # end def test_smartshift_count

    @features("Feature2251")
    @level("Functionality")
    def test_analytics_mode(self):
        """
        Verify current value of analytics mode can be retreived by Get Analytics Mode API
        """
        OFF = MouseWheelAnalytics.AnalyticsMode.OFF
        ON = MouseWheelAnalytics.AnalyticsMode.ON
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
        LogHelper.log_step(self, "Send GetAnalyticsMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_analytics_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAnalyticsModeResponse fields if reporting mode is returned as ON")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "reporting_mode": (checker.check_reporting_mode, ON)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_analytics_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode with reporting mode = OFF")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAnalyticsMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_analytics_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAnalyticsModeResponse fields if reporting mode is returned as OFF")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_analytics_mode_response_cls, check_map)

        self.testCaseChecked("FUN_2251_0014", _AUTHOR)
    # end def test_analytics_mode

    @features("Feature2251")
    @level("Functionality")
    @services("MainWheel")
    def test_rotation_data_resets_after_every_get_rotation_data_api_call(self):
        """
        Verify rotation data resets to zero after calling Get Rotation data API
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode with reporting mode = ON")
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
        LogHelper.log_step(self, "Use wheel emulator to emulate scroll up and scroll down motion of main wheel"
                                 "and scroll left and scroll right movement of thumbwheel(if available)")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls, down_scrolls, left_scrolls, right_scrolls = randint(2, 10), randint(2, 10), randint(2, 10), \
            randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") and @services("Thumbwheel") is '
                                  'available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send GetRotationData request two times")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(2):
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields are zero")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker.check_fields(
            self, response, self.feature_2251.get_rotation_data_response_cls)

        self.testCaseChecked("FUN_2251_0015", _AUTHOR)
    # end def test_rotation_data_resets_after_every_get_rotation_data_api_call

    @features("Feature2251")
    @features("SupportWheelModes")
    @level("Functionality")
    @services("MainWheel")
    def test_wheel_mode_data_resets_after_every_get_wheel_mode_data_api_call(self):
        """
        Verify wheel mode data resets to zero after calling Get Wheel Mode data API
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode with reporting mode = ON")
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
        LogHelper.log_step(self, "Use wheel emulator to scroll up/down the main wheel with sufficient speed "
                                 "multiple times such that main wheel goes into free wheel mode and smart shift "
                                 "tramsition occurs")
        # --------------------------------------------------------------------------------------------------------------
        if self.config.F_SmartShiftCapability:
            smart_shift_count = randint(2, 10)
            raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press ratchet switch multiple times to change wheel mode from ratchet to free wheel"
                                 "mode and vice versa")
        # --------------------------------------------------------------------------------------------------------------
        if self.config.F_RatchetFreeCapability and MouseWheelAnalyticsTestUtils.smart_shift_key_connected(self):
            ratchet_button_press_count = randint(2, 10)
            for _ in range(ratchet_button_press_count):
                self.button_stimuli_emulator.keystroke(KEY_ID.SMART_SHIFT)
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request two times")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(2):
            response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check GetWheelModedataResponse is zero")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker.check_fields(
            self, response, self.feature_2251.get_wheel_mode_data_response_cls)

        self.testCaseChecked("FUN_2251_0016", _AUTHOR)
    # end def test_wheel_mode_data_resets_after_every_get_wheel_mode_data_api_call
# end class MouseWheelAnalyticsFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
