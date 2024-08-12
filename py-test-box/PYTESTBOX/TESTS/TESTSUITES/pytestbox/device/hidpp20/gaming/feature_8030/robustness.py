#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8030.robustness
:brief: HID++ 2.0 ``MacroRecordkey`` robustness test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkey
from pylibrary.emulator.ledid import MACRO_KEYS_LEDS
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.macrorecordkeyutils import MacroRecordkeyTestUtils
from pytestbox.device.hidpp20.gaming.feature_8030.macrorecordkey import MacroRecordkeyTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"
_LOOP_START_ENABLED = "Test loop over enabled range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyRobustnessTestCase(MacroRecordkeyTestCase):
    """
    Validate ``MacroRecordkey`` robustness test cases
    """

    @features("Feature8030")
    @level("Robustness")
    def test_set_led_software_id(self):
        """
        Validate ``SetLED`` software id field is ignored by the firmware

        [0] setLED(enabled) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.enabled.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        enabled = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MacroRecordkey.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetLED request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MacroRecordkeyTestUtils.HIDppHelper.set_led(
                test_case=self,
                enabled=enabled,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetLEDResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MacroRecordkeyTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8030.set_led_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8030_0001", _AUTHOR)
    # end def test_set_led_software_id

    @features("Feature8030")
    @level("Robustness")
    def test_set_led_padding(self):
        """
        Validate ``SetLED`` padding bytes are ignored by the firmware

        [0] setLED(enabled) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.enabled.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        enabled = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8030.set_led_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetLED request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MacroRecordkeyTestUtils.HIDppHelper.set_led(
                test_case=self,
                enabled=enabled,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetLEDResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MacroRecordkeyTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8030.set_led_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8030_0002", _AUTHOR)
    # end def test_set_led_padding

    @features("Feature8030")
    @level("Robustness")
    def test_to_check_the_status_of_led_not_changed_when_setled_enabled_greater_than_1(self):
        """
        Check the status of LED is not change when SetLED.enabled > 1
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLED request - enabled = 0")
        # --------------------------------------------------------------------------------------------------------------
        MacroRecordkeyTestUtils.HIDppHelper.set_led(
            test_case=self,
            enabled=0)

        values = compute_sup_values(255)
        values.remove(0)
        values.remove(1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_ENABLED)
        # --------------------------------------------------------------------------------------------------------------
        for value in values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetLED request - enabled > 1")
            # ----------------------------------------------------------------------------------------------------------
            MacroRecordkeyTestUtils.HIDppHelper.set_led(
                test_case=self,
                enabled=value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check LED OFF")
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=MACRO_KEYS_LEDS)
            sleep(MacroRecordkeyTestCase.LED_TOGGLING_DELAY)
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.MR_LED, state=SchemeType.OFF)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8030_0003", _AUTHOR)
    # end def test_to_check_the_status_of_led_not_changed_when_setled_enabled_greater_than_1
# end class MacroRecordkeyRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
