#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_18a1.business
:brief: HID++ 2.0 ``LEDTest`` business test suite
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
from pytestbox.device.base.devicetestutils import DeviceTestUtils
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
class LEDTestBusinessTestCase(LEDTestTestCase):
    """
    Validate ``LEDTest`` business test cases
    """

    @features("Feature18A1")
    @level("Business")
    @services("HardwareReset")
    @services("LedIndicator")
    def test_led_back_to_default_state_after_hardware_reset(self):
        """
        Check LED state resets to default after hardware reset
        """
        ON = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLEDTestMode request to turn ON any one LED that is available in device")
        # --------------------------------------------------------------------------------------------------------------
        led_presence_map = LEDTestTestUtils.get_led_presence_map(self)
        led_state_map = LEDTestTestUtils.get_led_state_map()
        led_state_map[next(led for led, presence in led_presence_map.items() if presence)] = ON

        response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(self, **led_state_map)

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
        LogHelper.log_check(self, "Check current LED is turned ON in GetLEDTestModeResponse")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
        check_map = checker.get_check_map(self, **led_state_map)
        checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check LED state is ON using LED/I2C spy")
        # --------------------------------------------------------------------------------------------------------------
        led = list(led_state_map.keys())[list(led_state_map.values()).index(ON)]
        # TODO:
        warnings.warn("Check LED that was turned on using LED/I2C spy method not implemented")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_connection_reset=False,
                   verify_wireless_device_status_broadcast_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all LEDs are OFF in GetLEDTestModeResponse")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(self)
        checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
        checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check the LED that was turned on is returned to default state using LED/I2C spy")
        # --------------------------------------------------------------------------------------------------------------
        warnings.warn("Check LED that was turned on is returned to default state using LED/I2C spy method not "
                      "implemented")

        self.testCaseChecked("BUS_18A1_0001", _AUTHOR)
    # end def test_led_back_to_default_state_after_hardware_reset

    @features("Feature18A1")
    @level("Business")
    @services("HardwareReset")
    @services("LedIndicator")
    def test_led_back_to_default_state_after_hidpp_reset(self):
        """
        Check LED state resets to default after hidpp reset
        """
        ON = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLEDTestMode request to turn ON any one LED that is available in device")
        # --------------------------------------------------------------------------------------------------------------
        led_presence_map = LEDTestTestUtils.get_led_presence_map(self)
        led_state_map = LEDTestTestUtils.get_led_state_map()
        led_state_map[next(led for led, presence in led_presence_map.items() if presence)] = ON

        response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(self, **led_state_map)

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
        LogHelper.log_check(self, "Check GetLEDTestModeResponse if current LED is turned ON")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
        check_map = checker.get_check_map(self, **led_state_map)
        checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check current LED is in ON state using LED/I2C spy")
        # --------------------------------------------------------------------------------------------------------------
        led = list(led_state_map.keys())[list(led_state_map.values()).index(ON)]
        warnings.warn("Check LED that was turned on using LED/I2C spy method not implemented")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a device hidpp reset")
        # --------------------------------------------------------------------------------------------------------------
        LEDTestTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLEDTestModeResponse if all LEDs are turned OFF")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(self)
        checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
        checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check the LED that was turned on is returned to default state using LED/I2C spy")
        # --------------------------------------------------------------------------------------------------------------
        # TODO:
        warnings.warn("Check LED that was turned on is returned to default state using LED spy method not implemented")

        self.testCaseChecked("BUS_18A1_0002", _AUTHOR)
    # end def test_led_back_to_default_state_after_hidpp_reset
# end class LEDTestBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
