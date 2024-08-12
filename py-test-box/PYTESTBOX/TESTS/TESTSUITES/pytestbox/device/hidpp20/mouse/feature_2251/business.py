#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.mouse.feature_2251.business
:brief: HID++ 2.0 ``MouseWheelAnalytics`` business test suite
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
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pyhid.hidpp.features.mouse.thumbwheel import Thumbwheel
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mousewheelanalyticsutils import MouseWheelAnalyticsTestUtils
from pytestbox.device.base.ratchetwheelutils import RatchetWheelTestUtils
from pytestbox.device.base.thumbwheelutils import ThumbwheelTestUtils
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
class MouseWheelAnalyticsBusinessTestCase(MouseWheelAnalyticsTestCase):
    """
    Validate ``MouseWheelAnalytics`` business test cases
    """

    @features("Feature2251")
    @level("Business")
    @services("HardwareReset")
    @services("MainWheel")
    def test_check_get_rotation_data_after_hardware_reset(self):
        """
        Verify all values of wheel movement from Get Rotation Data API response will reset back to zero after a
        device hardware reset
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
        LogHelper.log_step(self, "Emulate up and down movement of main wheel and left and right movement of "
                                 "thumbwheel (if thumbwheel is available in DUT)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a device Hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

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
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields are zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0001", _AUTHOR)
    # end def test_check_get_rotation_data_after_hardware_reset

    @features("Feature2251")
    @features("Feature1802")
    @level("Business")
    @services("MainWheel")
    def test_check_get_rotation_data_after_hidpp_reset(self):
        """
        Verify all values of wheel movement from Get Rotation Data API response will reset back to zero after a
        device hidpp reset
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
        LogHelper.log_step(self, "Emulate up and down movement of main wheel and left and right movement of "
                                 "thumbwheel (if thumbwheel is available in DUT)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a device Hidpp reset")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.ResetHelper.hidpp_reset(self)

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
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields are zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0002", _AUTHOR)
    # end def test_check_get_rotation_data_after_hidpp_reset

    @features("Feature2251")
    @features("SupportWheelModes")
    @level("Business")
    @services("HardwareReset")
    @services("MainWheel")
    def test_check_get_wheel_mode_data_after_hardware_reset(self):
        """
        Verify ratchet to free wheel count, free wheel to ratchet count, smart shift count will reset back to zero
        after a device hardware reset
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
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

        if self.config.F_RatchetFreeCapability and MouseWheelAnalyticsTestUtils.smart_shift_key_connected(self):
            ratchet_button_press_count = randint(2, 10)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press ratchet button {ratchet_button_press_count} times to change wheel mode "
                                     "between ratchet and free wheel mode")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(ratchet_button_press_count):
                self.button_stimuli_emulator.keystroke(KEY_ID.SMART_SHIFT)
            # end for
        # end if

        if self.config.F_SmartShiftCapability:
            smart_shift_count = randint(2, 10)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Use wheel emulator to scroll the main wheel with sufficient speed "
                                     f"{smart_shift_count} times such that smart shift transition occurs")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(smart_shift_count):
                raise NotImplementedError('To be implemented when @services("MainWheel") is available')
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

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
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields are zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0003", _AUTHOR)
    # end def test_check_get_wheel_mode_data_after_hardware_reset

    @features("Feature2251")
    @features("Feature1802")
    @features("SupportWheelModes")
    @level("Business")
    @services("MainWheel")
    def test_check_get_wheel_mode_data_after_hidpp_reset(self):
        """
        Verify ratchet to free wheel count, free wheel to ratchet count, smart shift count will reset back to
        zero after a device hidpp reset
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
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

        if self.config.F_RatchetFreeCapability and MouseWheelAnalyticsTestUtils.smart_shift_key_connected(self):
            ratchet_button_press_count = randint(2, 10)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press ratchet button {ratchet_button_press_count} times to change wheel mode "
                                     "between ratchet and free wheel mode")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(ratchet_button_press_count):
                self.button_stimuli_emulator.keystroke(KEY_ID.SMART_SHIFT)
            # end for
        # end if

        if self.config.F_SmartShiftCapability:
            smart_shift_count = randint(2, 10)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Use wheel emulator to scroll the main wheel with sufficient speed "
                                     f"{smart_shift_count} times such that smart shift transition occurs")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(smart_shift_count):
                raise NotImplementedError('To be implemented when @services("MainWheel") is available')
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a device hidpp reset")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.ResetHelper.hidpp_reset(self)

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
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields are zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0004", _AUTHOR)
    # end def test_check_get_wheel_mode_data_after_hidpp_reset

    @features("Feature2251")
    @level('Business', 'SmokeTests')
    @services("MainWheel")
    def test_main_wheel_up_and_down_movement(self):
        """
        Verify main wheel up and down movement are reported independently of each other
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
        LogHelper.log_step(self, "Emulate up and down movement of main wheel using wheel emulator")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls,  down_scrolls = randint(2, 10), randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields if values for up and down motion corresponds "
                                  "to the main wheel rotation done by wheel emulator")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, up_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)
        down_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, down_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_pos_wheel": (checker.check_acc_pos_wheel, down_scrolls_acc_motion_value),
                "acc_neg_wheel": (checker.check_acc_neg_wheel, up_scrolls_acc_motion_value)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0005", _AUTHOR)
    # end def test_main_wheel_up_and_down_movement

    @features("Feature2251")
    @features("ThumbwheelCapability")
    @level("Business")
    @services("Thumbwheel")
    def test_thumbwheel_right_and_left_movement(self):
        """
        Verify thumbwheel left and right movement are reported independently of each other
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
        LogHelper.log_step(self, "Emulate left and right movement of thumbwheel using wheel emulator")
        # --------------------------------------------------------------------------------------------------------------
        left_scrolls, right_scrolls = randint(2, 10), randint(2, 10)
        raise NotImplementedError('To be implemented when @services("Thumbwheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields corresponds to the thumbwheel rotation done "
                                  "by wheel emulator")
        # --------------------------------------------------------------------------------------------------------------
        left_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, left_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)
        right_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, right_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_pos_thumbwheel": (checker.check_acc_pos_thumbwheel, right_scrolls_acc_motion_value),
                "acc_neg_thumbwheel": (checker.check_acc_neg_thumbwheel, left_scrolls_acc_motion_value)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0006", _AUTHOR)
    # end def test_thumbwheel_right_and_left_movement

    @features("Feature2251")
    @features("ThumbwheelCapability")
    @level("Business")
    @services("MainWheel")
    @services("Thumbwheel")
    def test_get_rotation_data_for_main_wheel_and_thumbwheel(self):
        """
        Verify Get Rotation Data API for response for main wheel up and down motion, thumbwheel left and right motion
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
        LogHelper.log_step(self, "Using wheel emulator, emulate left and right motion of thumbwheel and up and down "
                                 "motion of main wheel ")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls, down_scrolls, left_scrolls, right_scrolls = randint(2, 10), randint(2, 10), randint(2, 10), \
            randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") and @services("Thumbwheel") is '
                                   'available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields corresponds to rotations done by wheel "
                                  "emulator")
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

        self.testCaseChecked("BUS_2251_0007", _AUTHOR)
    # end def test_get_rotation_data_for_main_wheel_and_thumbwheel

    @features("Feature2251")
    @features("RatchetFreeCapability")
    @features("SmartShiftCapability")
    @level("Business")
    @services("MainWheel")
    @services("RequiredKeys", (KEY_ID.SMART_SHIFT,))
    def test_get_wheel_mode_data_for_smartshift_and_ratchet_button_press(self):
        """
        Verify Get Wheel Mode Data API for multiple ratchet button presses and smart shift transitions
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
        LogHelper.log_step(self, "Using wheel emulator, scroll up/down the main wheel with sufficient speed so that"
                                 "smartshift transition occurs")
        # --------------------------------------------------------------------------------------------------------------
        smart_shift_count = randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do multiple presses on ratchet switch to alternate main wheel between ratchet and"
                                 "free wheel mode")
        # --------------------------------------------------------------------------------------------------------------
        tries = randint(2, 10)
        for _ in range(tries):
            self.button_stimuli_emulator.keystroke(KEY_ID.SMART_SHIFT)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields corresponds to the emulated values")
        # --------------------------------------------------------------------------------------------------------------
        ratchet_to_free_wheel_count = tries // 2 + tries % 2
        free_wheel_to_ratchet_count = tries // 2
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "ratchet_to_free_wheel_count": (cls.check_ratchet_to_free_wheel_count, ratchet_to_free_wheel_count),
                "free_wheel_to_ratchet_count": (cls.check_free_wheel_to_ratchet_count, free_wheel_to_ratchet_count),
                "smart_shift_count": (checker.check_smart_shift_count, smart_shift_count)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0008", _AUTHOR)
    # end def test_get_wheel_mode_data_for_smartshift_and_ratchet_button_press

    @features("Feature2251")
    @features("SmartShiftCapability")
    @level("Business")
    @services("MainWheel")
    def test_smart_shift_count_when_main_wheel_spinning_in_free_wheel_mode(self):
        """
        Verify Smart Shift Count when main wheel is spinning in free wheel mode
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
        LogHelper.log_step(self, "Using wheel emulator, scroll up/down the main wheel with sufficient speed so that"
                                 "smartshift transition occurs, and maintain that speed so that wheel continues to"
                                 "spin in free wheel mode")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields if smart shift count is 1")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "smart_shift_count": (checker.check_smart_shift_count, 1)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields if smart shift count is 0")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker.check_fields(
            self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop the main wheel from spinning")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        self.testCaseChecked("BUS_2251_0009", _AUTHOR)
    # end def test_smart_shift_count_when_main_wheel_spinning_in_free_wheel_mode

    @features("Feature2251")
    @features("Feature2130")
    @level("Business")
    @services("MainWheel")
    def test_get_rotation_data_api_when_ratchet_wheel_in_divert_mode(self):
        """
        Verify Get rotation Data API response when ratchet wheel is in divert mode
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2130 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_2130, _, _ = RatchetWheelTestUtils.HIDppHelper.get_parameters(self)

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
        LogHelper.log_step(self, "Using Feature 0x2130, send SetWheelMode request with mode = Divert (HIDPP)")
        # --------------------------------------------------------------------------------------------------------------
        RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, RatchetWheel.DIVERT.HIDPP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetModeStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Use wheel emulator to scroll up and down the main wheel")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls, down_scrolls = randint(2, 10), randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check GetRotationDataResponse fields corresponds to the emulated values "
                                 "for main wheel motion")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, up_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)
        down_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, down_scrolls, MouseWheelAnalytics.Wheel.MAIN_WHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_pos_wheel": (checker.check_acc_pos_wheel, down_scrolls_acc_motion_value),
                "acc_neg_wheel": (checker.check_acc_neg_wheel, up_scrolls_acc_motion_value)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0010", _AUTHOR)
    # end def test_get_rotation_data_api_when_ratchet_wheel_in_divert_mode

    @features("Feature2251")
    @features("Feature2150")
    @features("ThumbwheelCapability")
    @level("Business")
    @services("Thumbwheel")
    def test_get_rotation_data_when_thumbwheel_in_divert_mode(self):
        """
        Verify Get rotation Data API response when thumbwheel is in divert mode
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2150 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_2150, _, _ = ThumbwheelTestUtils.HIDppHelper.get_parameters(self)

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
        LogHelper.log_step(self, "Using Feature 0x2150, send SetThumbwheelReporting request with wheel mode = "
                                 "Divert(HIDPP)")
        # --------------------------------------------------------------------------------------------------------------
        ThumbwheelTestUtils.HIDppHelper.set_thumbwheel_reporting(self, reporting_mode=Thumbwheel.REPORTING_MODE.HIDPP,
                                                                 invert_direction=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate SetThumbwheelReporting response fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ThumbwheelTestUtils.MessageChecker
        check_map = {}
        checker.check_fields(self, response, self.feature_2150.set_thumbwheel_reporting_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Use wheel emulator to scroll left and right the thumbwheel")
        # --------------------------------------------------------------------------------------------------------------
        left_scrolls, right_scrolls = randint(2, 10), randint(2, 10)
        raise NotImplementedError('To be implemented when @services("Thumbwheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check GetRotationDataResponse fields corresponds to emulated values for "
                                 "thumbwheel motion")
        # --------------------------------------------------------------------------------------------------------------
        left_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, left_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)
        right_scrolls_acc_motion_value = MouseWheelAnalyticsTestUtils.scrolls_to_acc_motion_value(
            self, right_scrolls, MouseWheelAnalytics.Wheel.THUMBWHEEL)

        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "acc_pos_thumbwheel": (checker.check_acc_pos_thumbwheel, right_scrolls_acc_motion_value),
                "acc_neg_thumbwheel": (checker.check_acc_neg_thumbwheel, left_scrolls_acc_motion_value)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0011", _AUTHOR)
    # end def test_get_rotation_data_when_thumbwheel_in_divert_mode

    @features("Feature2251")
    @features("SupportWheelModes")
    @level("Business")
    @services("MainWheel")
    def test_get_wheel_mode_data_and_get_rotation_data_called_together(self):
        """
        Verify Get Wheel Mode Data and Get rotation data API called together
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
        ON = MouseWheelAnalytics.AnalyticsMode.On
        left_scrolls = 0
        right_scrolls = 0
        ratchet_button_press_count = 0
        smart_shift_count = 0
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
        LogHelper.log_step(self, "Use wheel emulator to scroll up and down the main wheel")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls, down_scrolls = randint(2, 10), randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        if self.config.F_ThumbwheelCapability:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Use wheel emulator to scroll left and right the thumbwheel")
            # ----------------------------------------------------------------------------------------------------------
            left_scrolls, right_scrolls = randint(2, 10), randint(2, 10)
            raise NotImplementedError('To be implemented when @services("Thumbwheel") is available (if thumbwheel is '
                                      'available in the DUT)')
        # end if

        if self.config.F_SmartShiftCapability:
            smart_shift_count = randint(2, 10)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Use wheel emulator to scroll up/down the main wheel with sufficient speed "
                                     f"{smart_shift_count} times so thatsmartshift transition occurs")
            # ----------------------------------------------------------------------------------------------------------
            raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # end if

        if self.config.F_RatchetFreeCapability:
            ratchet_button_press_count = randint(2, 10)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Do {ratchet_button_press_count} presses on ratchet switch to alternate main "
                                     "wheel between ratchet and free wheel mode")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(ratchet_button_press_count):
                self.button_stimuli_emulator.keystroke(KEY_ID.SMART_SHIFT)
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationDataAPI")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields corresponds to emulated values for thumbwheel "
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields corresponds to emulated values for smart shift"
                                  " count, ratchet to free wheel and free wheel to ratchet transition")
        # --------------------------------------------------------------------------------------------------------------
        ratchet_to_free_wheel_count = ratchet_button_press_count // 2 + ratchet_button_press_count % 2
        free_wheel_to_ratchet_count = ratchet_button_press_count // 2
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "ratchet_to_free_wheel_count": (cls.check_ratchet_to_free_wheel_count, ratchet_to_free_wheel_count),
                "free_wheel_to_ratchet_count": (cls.check_free_wheel_to_ratchet_count, free_wheel_to_ratchet_count),
                "smart_shift_count": (checker.check_smart_shift_count, smart_shift_count)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("BUS_2251_0012", _AUTHOR)
    # end def test_get_wheel_mode_data_and_get_rotation_data_called_together

    @features("Feature2251")
    @features("RatchetFreeCapability")
    @features("SmartShiftCapability")
    @level("Business")
    @services("MainWheel")
    @services("RequiredKeys", (KEY_ID.SMART_SHIFT,))
    def test_get_wheel_mode_data_when_main_wheel_in_free_wheel_mode(self):
        """
        Verify smart shift count, ratchet to free wheel count and free wheel to ratchet count when main wheel is
        spinning in free wheel mode
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
        LogHelper.log_step(self, "Using wheel emulator, scroll up/down the main wheel with sufficient speed so that"
                                 "smartshift transition occurs, and maintain that speed so that wheel continues to"
                                 "spin in free wheel mode")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press ratchet switch twice so that main wheel mode will alternate between ratchet"
                                 "and free wheel mode")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(2):
            self.button_stimuli_emulator.keystroke(KEY_ID.SMART_SHIFT)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse if smart shift count, ratchet to free wheel count and"
                                  " free wheel to ratchet count are 1")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "ratchet_to_free_wheel_count": (checker.check_ratchet_to_free_wheel_count, 1),
                "free_wheel_to_ratchet_count": (checker.check_free_wheel_to_ratchet_count, 1),
                "smart_shift_count": (checker.check_smart_shift_count, 1)
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields if smart shift count, ratchet to free wheel "
                                  "count and free wheel to ratchet count are reset to zero")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop main wheel from spinning")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        self.testCaseChecked("BUS_2251_0013", _AUTHOR)
    # end def test_get_wheel_mode_data_when_main_wheel_in_free_wheel_mode

    @features("Feature2251")
    @level("Business")
    @services("MainWheel")
    def test_multiple_set_analytics_data_calls_does_not_reset_accumulated_rotation_data(self):
        """
        Verify calling Set Analytics Mode API does not reset accumulated value for rotation data
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        left_scrolls = 0
        right_scrolls = 0
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
        LogHelper.log_step(self, "Use wheel emulator to emulate up and down motion of main wheel and left and right"
                                 "motion of thumbwheel (if thumbwheel is available in DUT)")
        # --------------------------------------------------------------------------------------------------------------
        up_scrolls, down_scrolls, left_scrolls, right_scrolls = randint(2, 10), randint(2, 10), randint(2, 10), \
            randint(2, 10)
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send SetAnalyticsMode request with reporting mode = ON multiple times in a row")
        # --------------------------------------------------------------------------------------------------------------
        for i in range(randint(2, 5)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetAnalyticsMode request {i}")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check SetAnalyticsModeResponse fields {i}")
            # ----------------------------------------------------------------------------------------------------------
            checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "reporting_mode": (checker.check_reporting_mode, ON)
                }
            )
            checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotationDataResponse fields corresponds to emulated motion")
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

        self.testCaseChecked("BUS_2251_0014", _AUTHOR)
    # end def test_multiple_set_analytics_data_calls_does_not_reset_accumulated_rotation_data

    @features("Feature2251")
    @features("SupportWheelModes")
    @level("Business")
    @services("MainWheel")
    def test_multiple_set_analytics_data_calls_does_not_reset_accumulated_wheel_mode_data(self):
        """
        Verify calling Set Analytics Mode API does not reset accumulated value for wheel mode data
        """
        self.post_requisite_set_wheel_to_ratchet_mode = True
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        smart_shift_count = 0
        ratchet_button_press_count = 0
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

        if self.config.F_SmartShiftCapability:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self,"Using wheel emulator, scroll up/down the main wheel with sufficient speed"
                                    f"{smart_shift_count} times so that smartshift transition occurs")
            # ----------------------------------------------------------------------------------------------------------
            smart_shift_count = randint(2, 10)
            raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # end if

        if self.config.F_RatchetFreeCapability:
            ratchet_button_press_count = randint(2, 10)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press ratchet switch {ratchet_button_press_count} times so that main wheel mode "
                                     "will alternate between ratchet and free wheel mode")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(ratchet_button_press_count):
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.SMART_SHIFT)
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send SetAnalyticsMode request with reporting mode = ON multiple times in a row")
        # --------------------------------------------------------------------------------------------------------------
        for i in range(randint(2, 5)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetAnalyticsMode request {i}")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check SetAnalyticsModeResponse fields {i}")
            # ----------------------------------------------------------------------------------------------------------
            checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "reporting_mode": (checker.check_reporting_mode, ON)
                }
            )
            checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields corresponds to emulated values")
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

        self.testCaseChecked("BUS_2251_0015", _AUTHOR)
    # end def test_multiple_set_analytics_data_calls_does_not_reset_accumulated_wheel_mode_data
# end class MouseWheelAnalyticsBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
