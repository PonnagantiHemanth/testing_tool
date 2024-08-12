#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hid.mouse.smoothingalgo.business
:brief: Shared Hid mouse smoothing algo business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/07/04
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from statistics import mean

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.mouse import EXCLUDED_BUTTONS
from pytestbox.device.hid.mouse.displacement.functionality import DELAY_1_MS
from pytestbox.device.hid.mouse.displacement.performance import XYDisplacementPerformanceBase
from pytestbox.device.hid.mouse.displacement.performance import _102_PERCENT
from pytestbox.device.hid.mouse.displacement.performance import _105_PERCENT
from pytestbox.device.hid.mouse.displacement.performance import _110_PERCENT
from pytestbox.device.hid.mouse.displacement.performance import _90_PERCENT
from pytestbox.device.hid.mouse.displacement.performance import _95_PERCENT
from pytestbox.device.hid.mouse.displacement.performance import _98_PERCENT
from pytestbox.shared.hid.mouse.smoothingalgo.smoothingalgo import MINIMUM
from pytestbox.shared.hid.mouse.smoothingalgo.smoothingalgo import SKIP_COUNTER
from pytestbox.shared.hid.mouse.smoothingalgo.smoothingalgo import SMOOTH_AVG_BUFF_SIZE
from pytestbox.shared.hid.mouse.smoothingalgo.smoothingalgo import SMOOTH_THRESHOLD_DISABLE
from pytestbox.shared.hid.mouse.smoothingalgo.smoothingalgo import SMOOTH_THRESHOLD_ENABLE
from pytestbox.shared.hid.mouse.smoothingalgo.smoothingalgo import SmoothingAlgoTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedSmoothingAlgoBusinessTestCase(SmoothingAlgoTestCase):
    """
    Validate USB Boost business TestCases
    """
    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_not_active_at_1khz(self):
        """
        Goal: Validate the USB Boost algo can not be activated at 1kHz

        Scenario:
         - configure the reporting rate to 1kHz
         - 1 report with deltaX >= enabling threshold
         - 20 reports with deltaX = 2 and deltaY = 2
        Check the report are NOT split when there is an empty RF slot
        """
        self.force_report_rate_and_start_usb_capture(
            report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_1KHZ)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load deltaX = {SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE, dy=0)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=split_counter, expected=0,
                         msg=f"The split report counter {split_counter} is not equal to 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_1MS * _95_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_1MS * _102_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0001")
    # end def test_not_active_at_1khz

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_not_active_at_2khz(self):
        """
        Goal: Validate the USB Boost algo can not be activated at 2kHz

        Scenario:
         - configure the reporting rate to 2kHz
         - 1 report with deltaX >= enabling threshold
         - 20 reports with deltaX = 2 and deltaY = 2
        Check the report are NOT split when there is an empty RF slot
        """
        self.force_report_rate_and_start_usb_capture(
            report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_2KHZ)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load deltaX = {SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE, dy=0)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=split_counter, expected=0,
                         msg=f"The split report counter {split_counter} is not equal to 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_5MS * _95_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_5MS * _102_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0002")
    # end def test_not_active_at_2khz

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_not_active_at_4khz(self):
        """
        Goal: Validate the USB Boost algo can not be activated at 4kHz

        Scenario:
         - configure the reporting rate to 4kHz
         - 1 report with deltaX >= enabling threshold
         - 20 reports with deltaX = 2 and deltaY = 2
        Check the report are NOT split when there is an empty RF slot
        """
        self.force_report_rate_and_start_usb_capture(
            report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load deltaX = {SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE, dy=0)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=split_counter, expected=0,
                         msg=f"The split report counter {split_counter} is not equal to 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _95_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _102_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0003")
    # end def test_not_active_at_4khz

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_minimum_X_values(self):
        """
        Goal: Validate the USB Boost algo does not split reports if abs(X) = 1 and Y = 0

        Scenario:
         - configure the reporting rate to 8kHz
         - 1 report with deltaX >= enabling threshold
         - 5 reports with deltaX = 1 and deltaY = 0
         - 5 reports with deltaX = -1 and deltaY = 0
        Check the report are NOT split when there is an empty RF slot
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load deltaX = {SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE, dy=0, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE // 2} deltaX = {MINIMUM}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE // 2 - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE // 2} deltaX = -{MINIMUM}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE // 2 - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, _ = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE,
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        split_counter = len(packets) - (SMOOTH_AVG_BUFF_SIZE * 2 + 2)
        self.assertEqual(obtained=split_counter, expected=0,
                         msg=f"The split report counter {split_counter} is not equal to 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _90_PERCENT * 10 ** 3,
                                "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _102_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0004")
    # end def test_minimum_X_values

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_minimum_Y_values(self):
        """
        Goal: Validate the USB Boost algo does not split reports if abs(Y) = 1 and X = 0

        Scenario:
         - configure the reporting rate to 8kHz
         - 1 report with deltaY >= enabling threshold
         - 5 reports with deltaY = 1 and deltaX = 0
         - 5 reports with deltaY = -1 and deltaX = 0
        Check the report are NOT split when there is an empty RF slot
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load deltaY = {SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE // 2} deltaY = {MINIMUM}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE // 2 - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE // 2} deltaY = -{MINIMUM}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=-MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE // 2 - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, _, beagle_accumulated_y, _ = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE,
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        split_counter = len(packets) - (SMOOTH_AVG_BUFF_SIZE * 2 + 2)
        self.assertEqual(obtained=split_counter, expected=0,
                         msg=f"The split report counter {split_counter} is not equal to 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _90_PERCENT * 10 ** 3,
                                "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _102_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0005")
    # end def test_minimum_Y_values

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_enable_sumX_equal_to_threshold(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaX is configured to an average of 3
        over the last 10 reports.

        Scenario:
         - 11 reports with deltaX = 3 and deltaY = 0 (ramp-up)
         - 20 reports with deltaX = 2 and deltaY = 2
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE*2} slot with deltaX = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_ENABLE, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_ENABLE * (SMOOTH_AVG_BUFF_SIZE+1) +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*4,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 2) * 4,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 2) * 4}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _110_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0010")
    # end def test_enable_sumX_equal_to_threshold

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_enable_sumY_equal_to_threshold(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaY is configured to an average of 3
        over the last 10 reports.

        Scenario:
         - 11 reports with deltaY = 3 and deltaY = 0 (ramp-up)
         - 20 reports with deltaX = 2 and deltaY = 2
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE+1} slot with deltaY = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=SMOOTH_THRESHOLD_ENABLE, repetition=SMOOTH_AVG_BUFF_SIZE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaY = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, _, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_ENABLE * (SMOOTH_AVG_BUFF_SIZE+1) +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*4,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 2) * 4,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 2) * 4}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _105_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0011")
    # end def test_enable_sumY_equal_to_threshold

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_enable_sumXY_equal_to_threshold(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaX and deltaY are configured
        to an average of 3 over the last 10 reports.

        Scenario:
         - 10 reports with deltaY = 3 and deltaY = 3 (ramp-up)
         - 20 reports with deltaX = 2 and deltaY = 2
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE} slot with deltaX & Y = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_ENABLE, dy=SMOOTH_THRESHOLD_ENABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX & Y = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(MINIMUM * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_ENABLE * (SMOOTH_AVG_BUFF_SIZE + 1) +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value on deltaX does not match the injected value.")
        self.assertEqual(
            expected=beagle_accumulated_x,
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value on deltaY does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*2,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 2) * 2,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 2) * 2}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _110_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0012")
    # end def test_enable_sumXY_equal_to_threshold

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_enable_negative_sumX_equal_to_threshold(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaX is configured to an average of 3
        over the absolute values of the last 10 reports.

        Scenario:
         - 11 reports with deltaX = -3 and deltaY = 0 (ramp-up)
         - 20 reports with deltaX = -2 and deltaY = -2
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE+1} slot with deltaX = {-SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-SMOOTH_THRESHOLD_ENABLE, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-SMOOTH_THRESHOLD_DISABLE, dy=-SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=-(SMOOTH_THRESHOLD_ENABLE * (SMOOTH_AVG_BUFF_SIZE + 1) +
                       SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*4,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 2) * 4,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 2) * 4}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _105_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0013")
    # end def test_enable_negative_sumX_equal_to_threshold

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_enable_negative_sumY_equal_to_threshold(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaY is configured to an average of 3
        over the absolute values of the last 10 reports.

        Scenario:
         - 11 reports with deltaY = -3 and deltaY = 0 (ramp-up)
         - 20 reports with deltaX = -2 and deltaY = -2
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE+1} slot with deltaY = {-SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=-SMOOTH_THRESHOLD_ENABLE, repetition=SMOOTH_AVG_BUFF_SIZE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaY = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-SMOOTH_THRESHOLD_DISABLE, dy=-SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, _, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=-(SMOOTH_THRESHOLD_ENABLE * (SMOOTH_AVG_BUFF_SIZE+1) +
                       SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*4,
        # but we acknowledge that 3 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 3) * 4,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 3) * 4}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _105_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0014")
    # end def test_enable_negative_sumY_equal_to_threshold

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_enable_negative_sumXY_equal_to_threshold_ramp_up(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaX and deltaY are configured
        to an average of 3 over the absolute values of the last 10 reports.

        Scenario:
         - 10 reports with deltaY = -3 and deltaY = -3 (ramp-up)
         - 20 reports with deltaX = -2 and deltaY = -2
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 then {SMOOTH_AVG_BUFF_SIZE} '
                  'deltaY = 0 to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=-MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=-MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE} slot with deltaX & Y = {-SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-SMOOTH_THRESHOLD_ENABLE, dy=-SMOOTH_THRESHOLD_ENABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX & Y = {-SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-SMOOTH_THRESHOLD_DISABLE, dy=-SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=-(MINIMUM * SMOOTH_AVG_BUFF_SIZE +
                       SMOOTH_THRESHOLD_ENABLE * (SMOOTH_AVG_BUFF_SIZE + 1) +
                       SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value on deltaX does not match the injected value.")
        self.assertEqual(
            expected=beagle_accumulated_x,
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value on deltaY does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*4,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 2) * 4,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 2) * 4}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE * 4:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _110_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0015")
    # end def test_enable_negative_sumXY_equal_to_threshold_ramp_up

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_report_split_every_2_packets(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaX and deltaY are configured
        to an average of 3 over the last 10 reports.

        Scenario:
         - prerequisite: algo shall be enabled (i.e. send 1 packet with dx = dy = enable threshold)
         - 20 reports with deltaX = 2 and deltaY = 2 with an empty packet every 2 reports
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX & Y = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE,
                                       dy=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX & Y = {SMOOTH_THRESHOLD_DISABLE}'
                                 'with an empty packet every 2 reports')
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(SMOOTH_AVG_BUFF_SIZE):
            self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE, repetition=1)
            self.motion_emulator.commit_actions()
            self.motion_emulator.xy_motion(dx=0, dy=0)
            self.motion_emulator.commit_actions()
        # end for
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(MINIMUM * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value on deltaX does not match the injected value.")
        self.assertEqual(
            expected=beagle_accumulated_x,
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value on deltaY does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*2,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 2) * 2,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 2) * 2}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _102_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0020")
    # end def test_report_split_every_2_packets

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_report_split_every_3_packets(self):
        """
        Goal: Verify that the USB boost algorithm enable threshold for deltaX and deltaY are configured
        to an average of 3 over the last 10 reports.

        Scenario:
         - prerequisite: algo shall be enabled (i.e. send 1 packet with dx = dy = enable threshold)
         - 20 reports with deltaX = 2 and deltaY = 2 with an empty packet every 3 reports
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX & Y = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE,
                                       dy=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX & Y = {SMOOTH_THRESHOLD_DISABLE}'
                                 'with an empty packet every 2 reports')
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(SMOOTH_AVG_BUFF_SIZE):
            self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE, repetition=2)
            self.motion_emulator.commit_actions()
            self.motion_emulator.xy_motion(dx=0, dy=0)
            self.motion_emulator.commit_actions()
        # end for
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(MINIMUM * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 3),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value on deltaX does not match the injected value.")
        self.assertEqual(
            expected=beagle_accumulated_x,
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value on deltaY does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*2,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE - 2) * 2,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE - 2) * 2}")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE*2:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _102_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0021")
    # end def test_report_split_every_3_packets

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_2_consecutive_empty_packets(self):
        """
        Goal: Verify that the USB boost algorithm works fine when multiple consecutive empty packets
        (i.e. deltaX & Y = 0) are sent by the device

        Scenario:
         - prerequisite: algo shall be enabled (i.e. send 1 packet with dx = dy = enable threshold)
         - 20 reports with deltaX = 2 and deltaY = 2 interleaved with 2 consecutive empty packets
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX & Y = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE,
                                       dy=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {SMOOTH_AVG_BUFF_SIZE*2} deltaX & Y = {SMOOTH_THRESHOLD_DISABLE}'
                                 'interleaved with 2 consecutive empty packets')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=(SMOOTH_AVG_BUFF_SIZE*2) - 1, skip=2)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(MINIMUM * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE * 2),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value on deltaX does not match the injected value.")
        self.assertEqual(
            expected=beagle_accumulated_x,
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value on deltaY does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(
            a=split_counter, b=SMOOTH_AVG_BUFF_SIZE * 2,
            msg=f"The split report counter {split_counter} is less than {SMOOTH_AVG_BUFF_SIZE * 2}")

        self.testCaseChecked("BUS_HID_USB_BOOST_0022")
    # end def test_2_consecutive_empty_packets

    @features('RcvUSBBoost')
    @level('Business')
    @services('OpticalSensor')
    def test_motion_with_buttons(self):
        """
        Goal: Verify that the USB boost algorithm processing is not impacted by a keystroke on all supported buttons

        Scenario:
         - prerequisite: algo shall be enabled (i.e. send 1 packet with dx = enable threshold)
         - 100 reports with deltaX = 2 and deltaY = 2 sent 250us apart interleaved with keystrokes
           on all supported buttons 500us apart
        Check the report are split when there is an empty RF slot and the ago is enabled
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        # Prepare Optical Sensor Emulator motion sequence
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load deltaX = {SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE, dy=0)
        self.motion_emulator.commit_actions()

        report_counter = SMOOTH_AVG_BUFF_SIZE * 10
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent {report_counter} delta X & Y = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=report_counter - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        self.kosmos.sequencer.offline_mode = True
        # Start Sensor Emulator model update
        self.kosmos.dt.pes.execute(action=self.motion_emulator.module.action_event.START)
        # Add a 2ms delay before pressing the first key
        self.kosmos.pes.delay(delay_ns=2000000)
        self.pressed_key_ids = []
        self.pressed_key_ids.extend([x for x in self.button_stimuli_emulator.get_key_id_list() if x not in
                                     EXCLUDED_BUTTONS and x < KEY_ID.BUTTON_1])
        # Add key press step
        for button_id in self.pressed_key_ids:
            self.button_stimuli_emulator.key_press(key_id=button_id)
            # Add a 500us delay before pressing the next key
            self.kosmos.pes.delay(delay_ns=500000)
        # end for
        # Add a 1ms delay before releasing the first key
        self.kosmos.pes.delay(delay_ns=1000000)
        for button_id in self.pressed_key_ids:
            self.button_stimuli_emulator.key_release(key_id=button_id)
            # Add a 500us delay before releasing the next key
            self.kosmos.pes.delay(delay_ns=500000)
        # end for
        self.kosmos.pes.wait(action=self.motion_emulator.module.resume_event.FIFO_UNDERRUN)
        self.kosmos.pes.delay(delay_ns=DELAY_1_MS)

        # Run test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_ENABLE * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * report_counter),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value on deltaX does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be report_counter*2,
        # but we acknowledge that 12 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(report_counter - 12) * 2,
            msg=f"The split report counter {split_counter} is less than {(report_counter - 12) * 2}")

        average = round(mean(beagle_deltas[-report_counter:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of HID report delta times = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _98_PERCENT * 10 ** 3,
                           "The report rate average is lower than the specification")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _110_PERCENT * 10 ** 3,
                        "The report rate average is greater than the specification")

        self.testCaseChecked("BUS_HID_USB_BOOST_0030")
    # end def test_motion_with_buttons
# end class SharedSmoothingAlgoBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
