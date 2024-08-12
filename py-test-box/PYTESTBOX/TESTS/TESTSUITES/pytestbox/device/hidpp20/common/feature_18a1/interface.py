#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_18a1.interface
:brief: HID++ 2.0 ``LEDTest`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
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
class LEDTestInterfaceTestCase(LEDTestTestCase):
    """
    Validate ``LEDTest`` interface test cases
    """

    @features("Feature18A1")
    @level("Interface")
    def test_get_led_list(self):
        """
        Validate ``GetLEDList`` normal processing

        [0] getLEDList() -> ledMaskPresence1, ledmaskPresence2, ledGenericMaskPresence1, ledGenericMaskPresence2,
        ledGenericMaskPresence3
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLEDList request")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.get_led_list(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLEDListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.GetLEDListResponseChecker
        checker.check_fields(self, response, self.feature_18a1.get_led_list_response_cls)

        self.testCaseChecked("INT_18A1_0001", _AUTHOR)
    # end def test_get_led_list

    @features("Feature18A1")
    @level("Interface")
    def test_get_led_test_mode(self):
        """
        Validate ``GetLEDTestMode`` normal processing

        [1] getLEDTestMode() -> ledMaskState1, ledmaskState2, ledGenericMaskState1, ledGenericMaskState2,
        ledGenericMaskState3
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLEDTestMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLEDTestModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
        checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls)

        self.testCaseChecked("INT_18A1_0002", _AUTHOR)
    # end def test_get_led_test_mode

    @features("Feature18A1")
    @level("Interface")
    def test_set_led_test_mode(self):
        """
        Validate ``SetLEDTestMode`` normal processing

        [2] setLEDTestMode(ledMaskState1, ledMaskState2, ledGenericMaskState1, ledGenericMaskState2,
        ledGenericMaskState3) -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLEDTestMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetLEDTestModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LEDTestTestUtils.SetLEDTestModeResponseChecker
        checker.check_fields(self, response, self.feature_18a1.set_led_test_mode_response_cls)

        self.testCaseChecked("INT_18A1_0003", _AUTHOR)
    # end def test_set_led_test_mode
# end class LEDTestInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
