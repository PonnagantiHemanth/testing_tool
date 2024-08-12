#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_18a1.functionality
:brief: HID++ 2.0 ``LEDTest`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ledtestutils import LEDTestTestUtils
from pytestbox.device.hidpp20.common.feature_18a1.ledtest import LEDTestTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class LEDTestFunctionalityTestCase(LEDTestTestCase):
    """
    Validate ``LEDTest`` functionality test cases
    """

    @features("Feature18A1")
    @level("Functionality")
    @services("LedIndicator")
    def test_turning_on_and_off_all_supported_leds_at_once(self):
        """
        Check turning on and off of all available LEDs in the device at once works as expected
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLEDTestMode request with all available LEDs in the device set to ON state")
        # --------------------------------------------------------------------------------------------------------------
        led_presence_map = LEDTestTestUtils.get_led_presence_map(self)
        response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(self, **led_presence_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetLEDTestModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.SetLEDTestModeResponseChecker
        checker.check_fields(self, response, self.feature_18a1.set_led_test_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLEDTestMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLEDTestModeResponse fields if all available LEDs are shown to be in ON"
                                  "state")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
        check_map = checker.get_check_map(self, **led_presence_map)
        checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all available LEDs are in ON state using LED/I2C spy")
        # --------------------------------------------------------------------------------------------------------------
        for led, presence in LEDTestTestUtils.get_led_presence_map(self).items():
            if presence:
                # TODO:
                warnings.warn("Check standard LED is in ON state to be implemented using LED/I2C Spy")
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLEDTestMode request with all available LEDs in the device set to OFF state")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetLEDTestModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.SetLEDTestModeResponseChecker
        checker.check_fields(self, response, self.feature_18a1.set_led_test_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLEDTestMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLEDTestModeResponse fields if all available LEDs are shown to be in OFF"
                                  "state")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
        checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all available LEDs are in OFF state using LED spy")
        # --------------------------------------------------------------------------------------------------------------
        for led, presence in LEDTestTestUtils.get_led_presence_map(self).items():
            if presence:
                # TODO:
                warnings.warn("Check current LED is in OFF state to be implemented using LED/I2C Spy")
            # end if
        # end for

        self.testCaseChecked("FUN_18A1_0001", _AUTHOR)
    # end def test_turning_on_and_off_all_supported_leds_at_once

    @features("Feature18A1")
    @level("Functionality")
    @services("LedIndicator")
    def test_turning_on_and_off_all_leds_one_after_the_other(self):
        """
        Check turning on and off all available LEDs in the device one by one works as expected
        """
        ON = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available generic LEDs")
        # --------------------------------------------------------------------------------------------------------------
        for led, presence in LEDTestTestUtils.get_led_presence_map(self).items():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetLEDTestMode request with current LED set to ON state")
            # ----------------------------------------------------------------------------------------------------------
            led_state_map = LEDTestTestUtils.get_led_state_map()
            if presence:
                led_state_map[led] = ON
            else:
                continue
            # end if

            response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(self, **led_state_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetLEDTestModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.SetLEDTestModeResponseChecker
            checker.check_fields(self, response, self.feature_18a1.set_led_test_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetLEDTestMode request")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLEDTestModeResponse if current LED is shown to be in ON state")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
            check_map = checker.get_check_map(self, **led_state_map)
            checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check curent LED is in ON state using LED/I2C spy")
            # ----------------------------------------------------------------------------------------------------------
            # TODO:
            warnings.warn("Check current LED is in ON state to be implemented using LED/I2C Spy")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetLEDTestMode request with current LED set to OFF state")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetLEDTestModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.SetLEDTestModeResponseChecker
            checker.check_fields(self, response, self.feature_18a1.set_led_test_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetLEDTestMode request")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLEDTestModeResponse if current LED is shown to be in OFF state")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
            checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check current LED is in OFF state using LED/I2C spy")
            # ----------------------------------------------------------------------------------------------------------
            # TODO:
            warnings.warn("Check current LED is in OFF state to be implemented using LED/I2C Spy")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_18A1_0002", _AUTHOR)
    # end def test_turning_on_and_off_all_generic_leds_one_after_the_other
# end class LEDTestFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
