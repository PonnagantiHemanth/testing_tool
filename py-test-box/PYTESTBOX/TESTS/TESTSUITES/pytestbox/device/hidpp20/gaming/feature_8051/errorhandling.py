#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8051.errorhandling
:brief: HID++ 2.0 ``LogiModifiers`` error handling test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.logimodifiersutils import LogiModifiersTestUtils
from pytestbox.device.hidpp20.gaming.feature_8051.logimodifiers import LogiModifiersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class LogiModifiersErrorHandlingTestCase(LogiModifiersTestCase):
    """
    Validate ``LogiModifiers`` errorhandling test cases
    """

    @features("Feature8051")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8051.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8051.get_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8051_index)
            report.function_index = function_index

            LogiModifiersTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8051_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature8051")
    @features("NoFeature8051FnForceable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_forced_pressed_state_fn(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if force pressing a modifier that is not force pressable for setForcedPressedState().
        """
        self.verify_invalid_parameter_for_set_forced_pressed_state(fn=True)
        self.testCaseChecked("ERR_8051_0002#1", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_forced_pressed_state_fn

    @features("Feature8051")
    @features("NoFeature8051GShiftForceable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_forced_pressed_state_gshift(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if force pressing a modifier that is not force pressable for setForcedPressedState().
        """
        self.verify_invalid_parameter_for_set_forced_pressed_state(g_shift=True)
        self.testCaseChecked("ERR_8051_0002#2", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_forced_pressed_state_gshift

    @features("Feature8051")
    @features("NoFeature8051LeftCtrlGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_left_ctrl(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(left_ctrl=True)
        self.testCaseChecked("ERR_8051_0003#1", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_left_ctrl

    @features("Feature8051")
    @features("NoFeature8051LeftShiftGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_left_shift(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(left_shift=True)
        self.testCaseChecked("ERR_8051_0003#2", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_left_shift

    @features("Feature8051")
    @features("NoFeature8051LeftAltGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_left_alt(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(left_alt=True)
        self.testCaseChecked("ERR_8051_0003#3", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_left_alt

    @features("Feature8051")
    @features("NoFeature8051LeftGuiGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_left_gui(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(left_gui=True)
        self.testCaseChecked("ERR_8051_0003#4", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_left_gui

    @features("Feature8051")
    @features("NoFeature8051RightCtrlGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_right_ctrl(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(right_ctrl=True)
        self.testCaseChecked("ERR_8051_0003#5", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_right_ctrl

    @features("Feature8051")
    @features("NoFeature8051RightShiftGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_right_shift(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(right_shift=True)
        self.testCaseChecked("ERR_8051_0003#6", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_right_shift

    @features("Feature8051")
    @features("NoFeature8051RightAltGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_right_alt(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(right_alt=True)
        self.testCaseChecked("ERR_8051_0003#7", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_right_alt

    @features("Feature8051")
    @features("NoFeature8051RightGuiGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_right_gui(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(right_gui=True)
        self.testCaseChecked("ERR_8051_0003#8", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_right_gui

    @features("Feature8051")
    @features("NoFeature8051FnGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_fn(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(fn=True)
        self.testCaseChecked("ERR_8051_0003#9", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_fn

    @features("Feature8051")
    @features("NoFeature8051GShiftGettable")
    @level("ErrorHandling")
    def test_invalid_argument_shall_raise_error_for_set_press_events_gshift(self):
        """
        Check an HID++ error code HIDPP_ERR_INVALID_ARGUMENT is raised
        if enabling reporting for a modifier that is not gettable for setPressEvents().
        """
        self.verify_invalid_parameter_for_set_press_events(g_shift=True)
        self.testCaseChecked("ERR_8051_0003#10", _AUTHOR)
    # end def test_invalid_argument_shall_raise_error_for_set_press_events_gshift

    def verify_invalid_parameter_for_set_forced_pressed_state(self, g_shift=False, fn=False):
        """
        Verify the specific invalid parameter for setForcedPressedState().

        :param g_shift: set the press state of g-shift key -- optional
        :type g_shift: ``bool``
        :param fn: the flag to set the press state of fn key -- optional
        :type fn: ``bool``
        """
        params = {
            "g_shift": g_shift,
            "fn": fn,
        }

        report = self.feature_8051.set_forced_pressed_state_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8051_index,
            **params)

        LogiModifiersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])
    # end def verify_parameter_for_set_forced_pressed_state

    def verify_invalid_parameter_for_set_press_events(self, g_shift=False, fn=False, right_gui=False, right_alt=False,
                                                      right_shift=False, right_ctrl=False, left_gui=False,
                                                      left_alt=False, left_shift=False, left_ctrl=False):
        """
        Verify the specific invalid parameter for setPressEvents().

        :param g_shift: set the press state of g-shift key -- optional
        :type g_shift: ``bool``
        :param fn: the flag to set the press state of fn key -- optional
        :type fn: ``bool``
        :param right_gui: the flag to set the press state of fn key -- optional
        :type right_gui: ``bool``
        :param right_alt: the flag to set the press state of fn key -- optional
        :type right_alt: ``bool``
        :param right_shift: the flag to set the press state of fn key -- optional
        :type right_shift: ``bool``
        :param right_ctrl: the flag to set the press state of fn key -- optional
        :type right_ctrl: ``bool``
        :param left_gui: the flag to set the press state of fn key -- optional
        :type left_gui: ``bool``
        :param left_alt: the flag to set the press state of fn key -- optional
        :type left_alt: ``bool``
        :param left_shift: the flag to set the press state of fn key -- optional
        :type left_shift: ``bool``
        :param left_ctrl: the flag to set the press state of fn key -- optional
        :type left_ctrl: ``bool``
        """
        params = {
            "g_shift": g_shift,
            "fn": fn,
            "right_gui": right_gui,
            "right_alt": right_alt,
            "right_shift": right_shift,
            "right_ctrl": right_ctrl,
            "left_gui": left_gui,
            "left_alt": left_alt,
            "left_shift": left_shift,
            "left_ctrl": left_ctrl,
        }

        report = self.feature_8051.set_press_events_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8051_index,
            **params)

        LogiModifiersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])
    # end def verify_parameter_for_set_press_events
# end class LogiModifiersErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
