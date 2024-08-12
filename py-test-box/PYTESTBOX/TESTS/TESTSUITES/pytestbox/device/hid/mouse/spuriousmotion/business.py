#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.spuriousmotion.business
:brief: Hid mouse spurious motion filtering algorithm business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/04/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytestbox.device.hid.mouse.spuriousmotion.spuriousmotion import SpuriousMotionTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
Event = HidReportTestUtils.Event
EventId = HidReportTestUtils.EventId


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SpuriousMotionBusinessTestCase(SpuriousMotionTestCase):
    """
    Validate Mouse spurious motion filtering algorithm business TestCases
    """

    @features('Mice')
    @features('Feature1830powerMode', 3)
    @features('NoGamingDevice')
    @level('Business')
    @services('OpticalSensor')
    def test_single_in_range_motion_deep_sleep(self):
        """
        Goals: Verify that the spurious motion detection algo is enabled when the DUT wakes up from deep sleep
        and that a single motion event with deltaX = 1 is filtered out.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a single Motion event, to begin the test with DUT sleep timer reset')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 3
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion)])

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
        # ----------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate a single Motion event with deltaX = 1')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence(forced_update=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the firmware filters it out and that no HID Mouse report are sent")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)

        self.testCaseChecked("BUS_HID_SPURIOUS_0001#1")
    # end def test_single_in_range_motion_deep_sleep

    @features('Mice')
    @features('Feature1830powerMode', 3)
    @features('NoGamingDevice')
    @level('Business')
    @services('OpticalSensor')
    def test_single_out_of_range_motion_deep_sleep(self):
        """
        Goals: Verify that the spurious motion detection algo is disabled when the DUT wakes up from deep sleep
        and that a single motion event with deltaX = 2 is not filtered out.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a single Motion event, to begin the test with DUT sleep timer reset')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 3
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion)])

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
        # ----------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate a single Motion event with deltaX = 2')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 2
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence(forced_update=True)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the firmware does not filter out this motion and generate an HID "
                                  f"Mouse report with deltaX = {x_motion}")
        # ----------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion)])

        self.testCaseChecked("BUS_HID_SPURIOUS_0001#2")
    # end def test_single_out_of_range_motion_deep_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Business')
    @services('OpticalSensor')
    def test_single_in_range_motion_sleep(self):
        """
        Goals: Verify that the spurious motion detection algo is enabled when the DUT wakes up from sleep
        and that a single motion event with deltaX = 1 is filtered out.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a single Motion event, to begin the test with DUT sleep timer reset')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 3
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate a single Motion event with deltaX = 1')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence(forced_update=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the firmware filters it out and that no HID Mouse report are sent")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)

        self.testCaseChecked("BUS_HID_SPURIOUS_0002#1")
    # end def test_single_in_range_motion_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Business')
    @services('OpticalSensor')
    def test_single_out_of_range_motion_sleep(self):
        """
        Goals: Verify that the spurious motion detection algo is disabled when the DUT wakes up from sleep
        and that a single motion event with deltaX = 2 is not filtered out.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a single Motion event, to begin the test with DUT sleep timer reset')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 3
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate a single Motion event with deltaX = 2')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 2
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence(forced_update=True)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the firmware does not filter out this motion and generate an HID "
                                  f"Mouse report with deltaX = {x_motion}")
        # ----------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion)])

        self.testCaseChecked("BUS_HID_SPURIOUS_0002#2")
    # end def test_single_out_of_range_motion_sleep

# end class SpuriousMotionBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
