#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.mouse.feature_2251.interface
:brief: HID++ 2.0 ``MouseWheelAnalytics`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalytics
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mousewheelanalyticsutils import MouseWheelAnalyticsTestUtils
from pytestbox.device.hidpp20.mouse.feature_2251.mousewheelanalytics import MouseWheelAnalyticsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MouseWheelAnalyticsInterfaceTestCase(MouseWheelAnalyticsTestCase):
    """
    Validate ``MouseWheelAnalytics`` interface test cases
    """

    @features("Feature2251")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> capabilities, main_count_per_turn, thumbwheel_count_per_turn
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2251_index)),
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_2251_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature2251")
    @level("Interface")
    def test_get_analytics_mode(self):
        """
        Validate ``GetAnalyticsMode`` normal processing

        [1] getAnalyticsMode() -> reporting_mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAnalyticsMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_analytics_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAnalyticsModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2251_index)),
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_analytics_mode_response_cls, check_map)

        self.testCaseChecked("INT_2251_0002", _AUTHOR)
    # end def test_get_analytics_mode

    @features("Feature2251")
    @level("Interface")
    def test_set_analytics_mode(self):
        """
        Validate ``SetAnalyticsMode`` normal processing

        [2] setAnalyticsMode(reporting_mode) -> reporting_mode
        """
        OFF = MouseWheelAnalytics.AnalyticsMode.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2251_index)),
            }
        )
        checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)

        self.testCaseChecked("INT_2251_0003", _AUTHOR)
    # end def test_set_analytics_mode

    @features("Feature2251")
    @level("Interface")
    def test_get_rotation_data(self):
        """
        Validate ``GetRotaionData`` normal processing

        [3] getRotaionData() -> accPosWheel, accNegWheel, accPosThumbwheel, accNegThumbwheel
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode as ON")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "reporting_mode": (checker.check_reporting_mode, ON)
            }
        )
        checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRotaionData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_rotation_data(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRotaionDataResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetRotationDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2251_index)),
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_rotation_data_response_cls, check_map)

        self.testCaseChecked("INT_2251_0004", _AUTHOR)
    # end def test_get_rotation_data

    @features("Feature2251")
    @features("SupportWheelModes")
    @level("Interface")
    def test_get_wheel_mode_data(self):
        """
        Validate ``GetWheelModeData`` normal processing

        [4] getWheelModeData() -> ratchetToFreeWheelCount, freeWheelToRatchetCount, smartShiftCount
        """
        ON = MouseWheelAnalytics.AnalyticsMode.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalyticsMode as ON")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.set_analytics_mode(self, ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalyticsModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.SetAnalyticsModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "reporting_mode": (checker.check_reporting_mode, ON)
            }
        )
        checker.check_fields(self, response, self.feature_2251.set_analytics_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelModeData request")
        # --------------------------------------------------------------------------------------------------------------
        response = MouseWheelAnalyticsTestUtils.HIDppHelper.get_wheel_mode_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetWheelModeDataResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MouseWheelAnalyticsTestUtils.GetWheelModeDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2251_index)),
            }
        )
        checker.check_fields(self, response, self.feature_2251.get_wheel_mode_data_response_cls, check_map)

        self.testCaseChecked("INT_2251_0005", _AUTHOR)
    # end def test_get_wheel_mode_data
# end class MouseWheelAnalyticsInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
