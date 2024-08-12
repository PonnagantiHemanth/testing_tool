#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_18b0.interface
:brief: HID++ 2.0 ``MonitorMode`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorMode
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.staticmonitormodeutils import StaticMonitorModeTestUtils
from pytestbox.device.hidpp20.common.feature_18b0.staticmonitormode import StaticMonitorModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class StaticMonitorModeInterfaceTestCase(StaticMonitorModeTestCase):
    """
    Validate ``StaticMonitorMode`` interface test cases
    """

    @features("Feature18B0")
    @level("Interface")
    def test_set_monitor_mode(self):
        """
        Validate ``SetMonitorMode`` interface
        """
        mode = StaticMonitorMode.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_18b0_index)),
            }
        )
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls, check_map)

        self.testCaseChecked("INT_18B0_0001", _AUTHOR)
    # end def test_set_monitor_mode
# end class StaticMonitorModeInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
