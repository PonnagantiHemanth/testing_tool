#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8030.business
:brief: HID++ 2.0 ``MacroRecordkey`` business test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.emulator.ledid import MACRO_KEYS_LEDS
from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.macrorecordkeyutils import MacroRecordkeyTestUtils
from pytestbox.device.hidpp20.gaming.feature_8030.macrorecordkey import MacroRecordkeyTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyBusinessTestCase(MacroRecordkeyTestCase):
    """
    Validate ``MacroRecordkey`` business test cases
    """

    @features("Feature8030")
    @level('Business', 'SmokeTests')
    def test_to_check_led_on_when_set_led_enabled(self):
        """
        Check that LED is turned ON when SetLED(enabled)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLED request")
        # --------------------------------------------------------------------------------------------------------------
        MacroRecordkeyTestUtils.HIDppHelper.set_led(
            test_case=self,
            enabled=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check LED ON")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=MACRO_KEYS_LEDS)
        sleep(MacroRecordkeyTestCase.LED_TOGGLING_DELAY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.MR_LED, state=SchemeType.STEADY)

        self.testCaseChecked("BUS_8030_0001", _AUTHOR)
    # end def test_to_check_led_on_when_set_led_enabled

    @features("Feature8030")
    @level("Business")
    def test_to_check_led_off_when_set_led_disabled(self):
        """
        Check that LED is turned ON when SetLED(disabled)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLED request")
        # --------------------------------------------------------------------------------------------------------------
        MacroRecordkeyTestUtils.HIDppHelper.set_led(
            test_case=self,
            enabled=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check LED OFF")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=MACRO_KEYS_LEDS)
        sleep(MacroRecordkeyTestCase.LED_TOGGLING_DELAY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.MR_LED, state=SchemeType.OFF)

        self.testCaseChecked("BUS_8030_0002", _AUTHOR)
    # end def test_to_check_led_off_when_set_led_disabled
# end class MacroRecordkeyBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
