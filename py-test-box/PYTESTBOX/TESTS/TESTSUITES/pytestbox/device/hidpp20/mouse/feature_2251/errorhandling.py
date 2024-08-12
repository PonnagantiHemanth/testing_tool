#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.mouse.feature_2251.errorhandling
:brief: HID++ 2.0 ``MouseWheelAnalytics`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mousewheelanalyticsutils import MouseWheelAnalyticsTestUtils
from pytestbox.device.hidpp20.mouse.feature_2251.mousewheelanalytics import MouseWheelAnalyticsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MouseWheelAnalyticsErrorHandlingTestCase(MouseWheelAnalyticsTestCase):
    """
    Validate ``MouseWheelAnalytics`` errorhandling test cases
    """

    @features("Feature2251")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_2251.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            MouseWheelAnalyticsTestUtils.HIDppHelper.get_capabilities_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_2251_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature2251")
    @level("ErrorHandling")
    def test_get_rotation_data_without_enabling_analytics_mode(self):
        """
        Validate NOT_ALLOWED error is raised when GetRotationData API is called without enabling Analytics Mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotationData request and verify NOT_ALLOWED error is returned")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data_and_check_error(self, [Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_2251_0002", _AUTHOR)
    # end def test_get_rotation_data_without_enabling_analytics_mode

    @features("Feature2251")
    @level("ErrorHandling")
    def test_get_wheel_mode_data_without_enabling_analytics_mode(self):
        """
        Validate NOT_ALLOWED error is raised when GetWheelModeData API is called without enabling Analytics Mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request and verify NOT_ALLOWED error is returned")
        # --------------------------------------------------------------------------------------------------------------
        MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data_and_check_error(
            self, [Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_2251_0003", _AUTHOR)
    # end def test_get_wheel_mode_data_without_enabling_analytics_mode
# end class MouseWheelAnalyticsErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
