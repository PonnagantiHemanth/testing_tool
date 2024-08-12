#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4540.interface
:brief: HID++ 2.0 ``KeyboardInternationalLayouts`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keyboardinternationallayoutsutils import KeyboardInternationalLayoutsTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4540.keyboardinternationallayouts \
    import KeyboardInternationalLayoutsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardInternationalLayoutsInterfaceTestCase(KeyboardInternationalLayoutsTestCase):
    """
    Validate ``KeyboardInternationalLayouts`` interface test cases
    """

    @features("Feature4540")
    @level("Interface")
    @services("Debugger")
    def test_get_keyboard_layout(self):
        """
        Validate ``GetKeyboardLayout`` interface
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetKeyboardLayout request")
        # --------------------------------------------------------------------------------------------------------------
        response = KeyboardInternationalLayoutsTestUtils.HIDppHelper.get_keyboard_layout(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetKeyboardLayoutResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = KeyboardInternationalLayoutsTestUtils.GetKeyboardLayoutResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4540_index)),
        })
        checker.check_fields(self, response, self.feature_4540.get_keyboard_layout_response_cls, check_map)

        self.testCaseChecked("INT_4540_0001", _AUTHOR)
    # end def test_get_keyboard_layout
# end class KeyboardInternationalLayoutsInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
