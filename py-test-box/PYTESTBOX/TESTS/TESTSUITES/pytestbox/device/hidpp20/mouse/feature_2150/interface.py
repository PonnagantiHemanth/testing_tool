#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2150.interface
:brief: HID++ 2.0 ``Thumbwheel`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.mouse.thumbwheel import Thumbwheel
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.thumbwheelutils import ThumbwheelTestUtils
from pytestbox.device.hidpp20.mouse.feature_2150.thumbwheel import ThumbwheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ThumbwheelInterfaceTestCase(ThumbwheelTestCase):
    """
    Validate ``Thumbwheel`` interface test cases
    """

    @features("Feature2150")
    @level("Interface")
    def test_get_thumbwheel_info(self):
        """
        Validate ``GetThumbwheelInfo`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetThumbwheelInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = ThumbwheelTestUtils.HIDppHelper.get_thumbwheel_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetThumbwheelInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ThumbwheelTestUtils.GetThumbwheelInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_2150_index))})
        checker.check_fields(self, response, self.feature_2150.get_thumbwheel_info_response_cls, check_map)

        self.testCaseChecked("INT_2150_0001", _AUTHOR)
    # end def test_get_thumbwheel_info

    @features("Feature2150")
    @level("Interface")
    def test_get_thumbwheel_status(self):
        """
        Validate ``GetThumbwheelStatus`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetThumbwheelStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ThumbwheelTestUtils.HIDppHelper.get_thumbwheel_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetThumbwheelStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ThumbwheelTestUtils.GetThumbwheelStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_2150_index)),
        })
        checker.check_fields(self, response, self.feature_2150.get_thumbwheel_status_response_cls, check_map)

        self.testCaseChecked("INT_2150_0002", _AUTHOR)
    # end def test_get_thumbwheel_status

    @features("Feature2150")
    @level("Interface")
    def test_set_thumbwheel_reporting(self):
        """
        Validate ``SetThumbwheelReporting`` interface
        """
        reporting_mode = Thumbwheel.REPORTING_MODE.HIDPP
        invert_direction = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetThumbwheelReporting request")
        # --------------------------------------------------------------------------------------------------------------
        response = ThumbwheelTestUtils.HIDppHelper.set_thumbwheel_reporting(self, reporting_mode, invert_direction)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetThumbwheelReportingResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_2150_index)),
        }
        checker.check_fields(self, response, self.feature_2150.set_thumbwheel_reporting_response_cls, check_map)

        self.testCaseChecked("INT_2150_0003", _AUTHOR)
    # end def test_set_thumbwheel_reporting
# end class ThumbwheelInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
