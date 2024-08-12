#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8030.interface
:brief: HID++ 2.0 ``MacroRecordkey`` interface test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.macrorecordkeyutils import MacroRecordkeyTestUtils
from pytestbox.device.hidpp20.gaming.feature_8030.macrorecordkey import MacroRecordkeyTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyInterfaceTestCase(MacroRecordkeyTestCase):
    """
    Validate ``MacroRecordkey`` interface test cases
    """

    @features("Feature8030")
    @level("Interface")
    def test_set_led(self):
        """
        Validate ``SetLED`` normal processing

        [0] setLED(enabled) -> None
        """
        enabled = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLED request")
        # --------------------------------------------------------------------------------------------------------------
        response = MacroRecordkeyTestUtils.HIDppHelper.set_led(
            test_case=self,
            enabled=enabled)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetLEDResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MacroRecordkeyTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8030_index))
        }
        checker.check_fields(self, response, self.feature_8030.set_led_response_cls, check_map)

        self.testCaseChecked("INT_8030_0001", _AUTHOR)
    # end def test_set_led
# end class MacroRecordkeyInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
