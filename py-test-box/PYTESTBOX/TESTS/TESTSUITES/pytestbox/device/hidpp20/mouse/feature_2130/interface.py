#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2130.interface
:brief: HID++ 2.0 ``RatchetWheel`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/11/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ratchetwheelutils import RatchetWheelTestUtils
from pytestbox.device.hidpp20.mouse.feature_2130.ratchetwheel import RatchetWheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RatchetWheelInterfaceTestCase(RatchetWheelTestCase):
    """
    Validate ``RatchetWheel`` interface test cases
    """

    @features("Feature2130")
    @level("Interface")
    def test_get_wheel_mode(self):
        """
        Validate ``GetWheelMode`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelMode")
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate GetWheelMode.divert value")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_2130_index)),
        })
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        self.testCaseChecked("INT_2130_0001", _AUTHOR)
    # end def test_get_wheel_mode

    @features("Feature2130")
    @level("Interface")
    def test_set_mode_status(self):
        """
        Validate ``SetModeStatus`` interface
        """
        divert = RatchetWheel.DIVERT.HID
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetWheelMode with divert = {divert}")
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, divert)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetModeStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_2130_index)),
        })
        checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)

        self.testCaseChecked("INT_2130_0002", _AUTHOR)
    # end def test_set_mode_status
# end class RatchetWheelInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
