#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.spuriousmotion.functionality
:brief: Hid mouse spurious motion filtering algorithm functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/04/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
# noinspection PyUnresolvedReferences
from pyhid.hid.hidmouse import HidMouse
# noinspection PyUnresolvedReferences
from pyhid.hid.hidmouse import HidMouseNvidiaExtension
from pyhid.hiddispatcher import HIDDispatcher
from pyraspi.services.kosmos.module.optemu import Action
from pyraspi.services.kosmos.module.optemu_sensors import Paw3266Module
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytestbox.device.hid.mouse.spuriousmotion.spuriousmotion import SpuriousMotionTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
Event = HidReportTestUtils.Event
EventId = HidReportTestUtils.EventId


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpuriousMotionFunctionalityTestCase(SpuriousMotionTestCase):
    """
    Validate Mouse spurious motion filtering algorithm functionality TestCases
    """

    @features('Mice')
    @features('Feature1830powerMode', 3)
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_2_consecutive_motions_deep_sleep(self):
        """
        Goals: Verify that multiple consecutive motion events with +1 or -1 increments are not filtered out
        when the DUT wakes up from deep sleep
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate 2 consecutive motions event with deltaX = 1')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion, repetition=1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence(forced_update=True)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the firmware does not filter out these motions and generate an HID "
                                  f"Mouse report with deltaX = {x_motion}")
        # ----------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=2 * x_motion)])

        self.testCaseChecked("FUN_HID_SPURIOUS_0001#1")
    # end def test_2_consecutive_motions_deep_sleep

    @features('Mice')
    @features('Feature1830powerMode', 3)
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_2_consecutive_motions_accumulator(self):
        """
        Goals: Verify that the accumulated motion value is correctly returned after the filter gets deactivated.
        """
        test_inputs = [(0, 0, 1, 2), (0, 1, 2, 0), (1, 2, 0, 0), (2, 0, 0, 1),
                       (0, 0, 2, 1), (0, 2, 1, 0), (2, 1, 0, 0), (1, 0, 0, 2)]
        for dx_0, dx_1, dy_0, dy_1 in test_inputs:

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
            # --------------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate 2 consecutive motions event: first delta (X, Y) = ({dx_0}, {dy_0})'
                                     f'then delta (X, Y) = ({dx_1}, {dy_1})')
            # --------------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=dx_0, dy=dy_0)
            self.motion_emulator.commit_actions()
            self.motion_emulator.xy_motion(dx=dx_1, dy=dy_1)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware does not filter out these motions and generate an HID "
                                      f"Mouse report with the expected accumulated motion")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self,
                events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=dx_0 + dx_1),
                        HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=dy_0 + dy_1)])
        # end for
        self.testCaseChecked("FUN_HID_SPURIOUS_001#2")
    # end def test_2_consecutive_motions_accumulator

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_2_consecutive_motions_sleep(self):
        """
        Goals: Verify that multiple consecutive motion events with +1 or -1 increments are not filtered out
        when the DUT wakes up from sleep.
        Also, verify that the accumulated motion values are correct.
        """
        for x_motion, y_motion in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate 2 consecutive motions event with deltaX = {x_motion} and deltaY = '
                                     f'{y_motion}')
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion, repetition=1)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware does not filter out these motions and generate an HID "
                                      f"Mouse report with deltaX = {x_motion} and deltaY = {y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self,
                events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=2 * x_motion),
                        HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=2 * y_motion)])
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0010")
    # end def test_2_consecutive_motions_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_motions_less_32ms_sleep(self):
        """
        Goals: Verify that multiple motion events less than 32ms apart with +1 or -1 increments are not filtered out
        when the DUT wakes up from sleep.
        Also, verify that the accumulated motion values are correct.
        """
        for x_motion, y_motion in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate 2 motion events with deltaX = {x_motion} and deltaY = '
                                     f'{y_motion} less than 32ms apart')
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
            self.motion_emulator.commit_actions()
            # Add few empty entries which will be polled in 28ms
            self.motion_emulator.xy_motion(dx=0, dy=0, repetition=self.fw_sensor_param.smf_max_count-2)
            self.motion_emulator.commit_actions()
            # Then an entry with an increment which will be polled 32ms after the wake-up
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
            self.motion_emulator.commit_actions()
            # Run test sequence
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware does not filter out these motions and generate an HID "
                                      f"Mouse report with deltaX = {x_motion} and deltaY = {y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self,
                events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=2 * x_motion),
                        HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=2 * y_motion)])
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0011")
    # end def test_motions_less_32ms_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_motions_more_32ms_sleep(self):
        """
        Goals: Verify that multiple motion events more than 32ms apart with +1 or -1 increments are filtered out
        when the DUT wakes up from sleep
        """

        # TODO replace this test skip code by a proper test decorator
        if isinstance(self.motion_emulator.module, Paw3266Module):
            self.skipTest(reason='This test is skipped because the related feature cannot be implemented in DUT '
                                 'firmware. Pixart Paw3266 sensor does not support being forced to enter Rest3 mode, '
                                 'bypassing its internal timer.')
        # end if

        for x_motion, y_motion in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate 2 motion events with deltaX = {x_motion} and deltaY = '
                                     f'{y_motion} more than 32ms apart')
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)  # First motion
            self.motion_emulator.commit_actions()
            # Run test sequence
            self.motion_emulator.prepare_sequence(forced_update=True)

            # Add few empty entries which will be polled in 32ms
            self.motion_emulator.xy_motion(dx=0, dy=0, repetition=self.fw_sensor_param.smf_max_count-1)
            self.motion_emulator.commit_actions()
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)  # Second motion
            self.motion_emulator.commit_actions()
            # Run test sequence
            self.motion_emulator.prepare_sequence(forced_update=True, timeout=self.fw_sensor_param.sensor_REST_3_MODE_TIME_SEC + 1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware filters out these motions and "
                                      "no HID Mouse report is sent")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0012")
    # end def test_motions_more_32ms_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_motions_null_increment_sleep(self):
        """
        Goals: Verify that a single motion with an increment in [+1, -1] then multiple motion events with 0 increment
        are filtered out when the DUT wakes up from sleep
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

        for x_motion, y_motion in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate 1 motion event with deltaX = {x_motion} and deltaY = '
                                     f'{y_motion}, than 7 null-increment updates with status motion bit force-set')
            # ----------------------------------------------------------------------------------------------------------
            # Generate normal displacement
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
            self.motion_emulator.commit_actions()

            # Force status motion bit to 1 while the dx dy registers are null, during few updates
            self.motion_emulator.xy_motion(dx=0, dy=0)
            self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=True)
            self.motion_emulator.commit_actions()
            self.motion_emulator.xy_motion(dx=0, dy=0, repetition=self.fw_sensor_param.smf_max_count-3)
            self.motion_emulator.commit_actions()

            # Reset status motion bit mask
            self.motion_emulator.xy_motion(dx=0, dy=0)
            self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=None)
            self.motion_emulator.commit_actions()
            # Run test sequence
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware filters out these motions and "
                                      "no HID Mouse report is sent")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0013")
    # end def test_motions_null_increment_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_greater_increments_sleep(self):
        """
        Goals: Verify that a single motion event with +2 or -2 increments are not filtered out
        when the DUT wakes up from sleep
        """
        for x_motion, y_motion in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate a single motion event with deltaX = {x_motion} and deltaY = {y_motion}')
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware does not filter out this motion and generate an HID "
                                      f"Mouse report with deltaX = {x_motion} and deltaY = {y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion),
                                        HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=y_motion)])
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0014")
    # end def test_greater_increments_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_sensor_modes_sleep(self):
        """
        Goals: Verify that a single motion event with +1 or -1 increments are not filtered out
        if the sensor is NOT in Rest3 mode when the DUT wakes up from sleep
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

        for i in range(2):

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'[{i}] Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec - .2)  # Note: for this test, the time margin is subtracted

            x_motion = choice([+1, -1])
            y_motion = choice([+1, -1])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'[{i}] Emulate a single motion event with deltaX = {x_motion} and deltaY = '
                                     f'{y_motion}')
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'[{i}] Check that the firmware does not filter out this motion and generate an '
                                      f'HID Mouse report with deltaX = {x_motion} and deltaY = {y_motion}')
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion),
                                        HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=y_motion)])
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0015")
    # end def test_sensor_modes_sleep

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_lift_sleep_mode(self):
        """
        Goals: Verify that setting the lift detected bit disables the filtering algorithm.

        Note: a XY displacement is done at the same time as setting the lift status bit, because only the Motion Status
        is configured to raise the interrupt line to wake up the DUT from sleep.
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
        LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
        # ----------------------------------------------------------------------------------------------------------
        sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

        x_motion = choice([+1, -1])
        y_motion = choice([+1, -1])
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Emulate a single motion event with deltaX = {x_motion} and deltaY = '
                                 f'{y_motion} and lift = True')
        # ----------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion, lift=True)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=0, dy=0, lift=False)
        self.motion_emulator.commit_actions()

        # Run test sequence
        self.motion_emulator.prepare_sequence(forced_update=True)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the firmware does not filter out this motion and generate an HID "
                                  f"Mouse report with deltaX = {x_motion} and deltaY = {y_motion}")
        # ----------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion),
                                    HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=y_motion)])

        # TODO: continue test case: validate no motion is received while lift is true

        self.testCaseChecked("FUN_HID_SPURIOUS_0016")
    # end def test_lift_sleep_mode

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    @services('HardwareReset')
    def test_single_motion_reset(self):
        """
        Goal: Verify that after a DUT power off / on, the filtering algorithm is disabled
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
        LogHelper.log_step(self, 'Reset device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_connection_reset=False,
                   verify_wireless_device_status_broadcast_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device reconnection')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
        ChannelUtils.open_channel(test_case=self)
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate a single Motion event with deltaX = 1')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()

        # Run test sequence
        self.motion_emulator.prepare_sequence()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the firmware does not filter out these motions and generate an HID "
                                  f"Mouse report with deltaX = {x_motion}")
        # ----------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=x_motion)])
        self.testCaseChecked("FUN_HID_SPURIOUS_0017")
    # end def test_single_motion_reset

    @features('Mice')
    @features('Rechargeable')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_single_motion_usb_charging(self):
        """
        Goal: Verify that plugging the USB charging cable has no impact on the motion detection algorithm
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Plug USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unplug_usb_charging_cable = True
        ProtocolManagerUtils.switch_to_usb_channel(test_case=self)

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

        # Run test sequence
        self.motion_emulator.prepare_sequence(forced_update=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the firmware filters it out and that no HID Mouse report are sent")
        # --------------------------------------------------------------------------------------------------------------
        mouse_report_class = globals()[self.f.PRODUCT.HID_REPORT.F_HidMouseType]
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5,
                                       class_type=mouse_report_class)

        self.testCaseChecked("FUN_HID_SPURIOUS_0018")
    # end def test_single_motion_usb_charging

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_delayed_spurious_single_motion(self):
        """
        Goal: Test delayed spurious option. Verify that the spurious motion detection algo ignores the first interrupt
        if deltaX & deltaY values are both equal to 0.
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

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Emulate single motion interrupt with delta X & Y = 0')
        # ----------------------------------------------------------------------------------------------------------
        # Force status motion bit to 1 while the dx dy registers are null
        self.motion_emulator.xy_motion(dx=0, dy=0)
        self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=True)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate a single Motion event with deltaX = 1')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 1
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=None)
        self.motion_emulator.commit_actions()

        # Run test sequence
        self.motion_emulator.prepare_sequence(forced_update=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the firmware filters it out and that no HID Mouse report are sent")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)

        self.testCaseChecked("FUN_HID_SPURIOUS_0019#1")
    # end def test_delayed_spurious_single_motion

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_delayed_spurious_motion_null(self):
        """
        Goal: Test delayed spurious option. Verify that the spurious motion detection algo ignored the first interrupt
        if deltaX & deltaY values are both equal to 0.
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

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Emulate few interrupts without motion')
        # ----------------------------------------------------------------------------------------------------------
        # Force status motion bit to 1 while the dx dy registers are null
        self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=True)
        self.motion_emulator.xy_motion(dx=0, dy=0, repetition=self.fw_sensor_param.smf_max_count)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Emulate a single Motion event with deltaX = 1')
        # --------------------------------------------------------------------------------------------------------------
        x_motion = 1
        self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=False)
        self.motion_emulator.xy_motion(dx=x_motion)
        self.motion_emulator.commit_actions()

        # Run test sequence
        self.motion_emulator.prepare_sequence(forced_update=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the firmware filters it out and that no HID Mouse report are sent")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)

        self.testCaseChecked("FUN_HID_SPURIOUS_0019#2")
    # end def test_delayed_spurious_motion_null

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_delayed_spurious_double_motion(self):
        """
        Goal: Test delayed spurious option. Verify that 2 consecutive motion events with +1 or -1 increments
        are not filtered out when the DUT wakes up from sleep even if the first interrupt contains deltaX & Y = 0.
        Also, verify that the accumulated motion values are correct.
        """
        for x_motion, y_motion in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate single motion interrupt with delta X & Y = 0')
            # ----------------------------------------------------------------------------------------------------------
            # Force status motion bit to 1 while the dx dy registers are null
            self.motion_emulator.xy_motion(dx=0, dy=0)
            self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=True)
            self.motion_emulator.commit_actions()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate 2 consecutive motion events with deltaX = {x_motion} and deltaY = '
                                     f'{y_motion}')
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.set_action(action=Action.STATUS_MOTION, value=None)
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion, repetition=1)
            self.motion_emulator.commit_actions()

            # Run test sequence
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware does not filter out these motions and generate an HID "
                                      f"Mouse report with deltaX = {x_motion} and deltaY = {y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self,
                events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=2 * x_motion),
                        HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=2 * y_motion)])
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0020")
    # end def test_delayed_spurious_double_motion

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_accumulation_in_range(self):
        """
        Goal: Accumulated data. Verify that multiple consecutive motion events with +1 or -1 increments but
        accumulated data in [-1, +1] range are filtered out when the DUT wakes up from sleep
        """
        for x_motion, y_motion in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate few consecutive motion events alternating a positive and negative value')
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.fw_sensor_param.smf_max_count // 2):
                self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
                self.motion_emulator.commit_actions()
                self.motion_emulator.xy_motion(dx=-x_motion, dy=-y_motion)
                self.motion_emulator.commit_actions()
            # end for

            # Run test sequence
            self.motion_emulator.prepare_sequence(forced_update=True)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check that the firmware filters it out and that no HID Mouse report are sent")
            # --------------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0021")
    # end def test_accumulation_in_range

    @features('Mice')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_accumulation_out_of_range(self):
        """
        Goal: Accumulated data. Verify that multiple consecutive motion events with +1 or -1 increments but
        accumulated data out of the [-1, +1] range are not filtered out when the DUT wakes up from sleep.
        Also, verify that the accumulated motion values are correct.
        """
        for x_motion, y_motion in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.fw_sensor_param.rest3_mode_time_sec + .2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate few consecutive motion events alternating a positive and negative value')
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.fw_sensor_param.smf_max_count // 2 - 1):
                self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
                self.motion_emulator.commit_actions()
                self.motion_emulator.xy_motion(dx=-x_motion, dy=-y_motion)
                self.motion_emulator.commit_actions()
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Emulate 2 consecutive motion events with deltaX = {x_motion} and deltaY = '
                                     f'{y_motion}')
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion, repetition=1)
            self.motion_emulator.commit_actions()

            # Run test sequence
            self.motion_emulator.prepare_sequence(forced_update=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that the firmware does not filter out these motions and generate an HID "
                                      f"Mouse report with deltaX = {x_motion} and deltaY = {y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self,
                events=[HidReportTestUtils.Event(HidReportTestUtils.EventId.X_MOTION, value=2 * x_motion),
                        HidReportTestUtils.Event(HidReportTestUtils.EventId.Y_MOTION, value=2 * y_motion)])
        # end for

        self.testCaseChecked("FUN_HID_SPURIOUS_0022")
    # end def test_accumulation_out_of_range

# end class SpuriousMotionFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
