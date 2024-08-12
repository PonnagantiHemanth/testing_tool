#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.displacement.business
:brief: Hid mouse XY displacement business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytestbox.device.hid.mouse.displacement.xydisplacement import XYDisplacementTestCase


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
Event = HidReportTestUtils.Event
EventId = HidReportTestUtils.EventId


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class XYDisplacementBusinessTestCase(XYDisplacementTestCase):
    """
    Validate Mouse XY displacement business TestCases
    """

    @features('Mice')
    @level('Business', 'SmokeTests')
    @services('OpticalSensor')
    def test_x_motion(self):
        """
        Goals: Verify that X displacement field has a positive value when the mouse moves to the right on X axis
               Verify that X displacement field has a negative value when the mouse moves to the left on X axis
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move right on X axis by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check there is a HID Mouse report with X field set to {x_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(EventId.X_MOTION, value=x_motion)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move left on X axis by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = -1
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check there is a HID Mouse report with X field set to {x_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(EventId.X_MOTION, value=x_motion)])

        self.testCaseChecked("BUS_HID_MOTION_0001")
    # end def test_x_motion

    @features('Mice')
    @level('Business')
    @services('OpticalSensor')
    def test_y_motion(self):
        """
        Goals: Verify that Y displacement field has a positive value when the mouse moves up on Y axis
               Verify that Y displacement field has a negative value when the mouse moves down on Y axis
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move up on Y axis by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        y_motion = 1
        self.motion_emulator.xy_motion(dy=y_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with Y field set to {y_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(EventId.Y_MOTION, value=y_motion)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move down on Y axis by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        y_motion = -1
        self.motion_emulator.xy_motion(dy=y_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with Y field set to {y_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(EventId.Y_MOTION, value=y_motion)])

        self.testCaseChecked("BUS_HID_MOTION_0002")
    # end def test_y_motion

    @features('Mice')
    @level('Business')
    @services('OpticalSensor')
    def test_xy_motion(self):
        """
        Goal: Verify that X and Y displacements could be combined in a single report
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move up and right by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = y_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with X field set to {x_motion} and Y field set to "
                                  f"{y_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(
            test_case=self, events=[Event(EventId.X_MOTION, value=x_motion), Event(EventId.Y_MOTION, value=y_motion)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move down and right by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        y_motion = -1
        self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with X field set to {x_motion} and Y field set to "
                                  f"{y_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(
            test_case=self, events=[Event(EventId.X_MOTION, value=x_motion), Event(EventId.Y_MOTION, value=y_motion)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move down and left by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = -1
        self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with X field set to {x_motion} and Y field set to "
                                  f"{y_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(
            test_case=self, events=[Event(EventId.X_MOTION, value=x_motion), Event(EventId.Y_MOTION, value=y_motion)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move up and left by minimum motion resolution')
        # --------------------------------------------------------------------------------------------------------------
        y_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with X field set to {x_motion} and Y field set to "
                                  f"{y_motion}")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(
            test_case=self, events=[Event(EventId.X_MOTION, value=x_motion), Event(EventId.Y_MOTION, value=y_motion)])

        self.testCaseChecked("BUS_HID_MOTION_0003")
    # end def test_xy_motion
# end class XYDisplacementBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
