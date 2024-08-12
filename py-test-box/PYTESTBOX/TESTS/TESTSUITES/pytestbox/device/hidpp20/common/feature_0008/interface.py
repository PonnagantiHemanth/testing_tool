#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0008.interface
:brief: HID++ 2.0 ``KeepAlive`` interface test suite
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keepaliveutils import KeepAliveTestUtils
from pytestbox.device.hidpp20.common.feature_0008.keepalive import KeepAliveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "HARISH KUMAR D"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class KeepAliveInterfaceTestCase(KeepAliveTestCase):
    """
    Validate ``KeepAlive`` interface test cases
    """

    @features("Feature0008")
    @level("Interface")
    def test_get_timeout_range(self):
        """
        Validate ``GetTimeoutRange`` normal processing

        [0] getTimeoutRange() -> timeoutMinimum, timeoutMaximum
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetTimeoutRange request")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.get_timeout_range(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetTimeoutRangeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = KeepAliveTestUtils.GetTimeoutRangeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0008_index)),
        })
        checker.check_fields(self, response, self.feature_0008.get_timeout_range_response_cls, check_map)

        self.testCaseChecked("INT_0008_0001", _AUTHOR)
    # end def test_get_timeout_range

    @features("Feature0008")
    @level("Interface")
    def test_keep_alive(self):
        """
        Validate ``KeepAlive`` normal processing

        [1] keepAlive(requestedTimeout) -> finalTimeout
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send KeepAlive request")
        # --------------------------------------------------------------------------------------------------------------
        timeout = self.max_timeout
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check KeepAliveResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = KeepAliveTestUtils.KeepAliveResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0008_index)),
            "final_timeout": (checker.check_final_timeout, timeout)
        })
        checker.check_fields(self, response, self.feature_0008.keep_alive_response_cls, check_map)

        self.testCaseChecked("INT_0008_0002", _AUTHOR)
    # end def test_keep_alive

    @features("Feature0008")
    @level("Interface")
    def test_terminate(self):
        """
        Validate ``Terminate`` normal processing

        [2] terminate() -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Terminate request")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check TerminateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = KeepAliveTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0008_index))
        }
        checker.check_fields(self, response, self.feature_0008.terminate_response_cls, check_map)

        self.testCaseChecked("INT_0008_0003", _AUTHOR)
    # end def test_terminate
# end class KeepAliveInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
