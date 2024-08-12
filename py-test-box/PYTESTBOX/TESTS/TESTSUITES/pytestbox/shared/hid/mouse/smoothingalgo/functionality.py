#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hid.mouse.smoothingalgo.functionality
:brief: Shared Hid mouse smoothing algo functionality test suite
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
from pyraspi.services.kosmos.module.model.optemu.base import OptEmu16BitsRegisterMapBase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.base.hidreportutils import to_signed_int
from pytestbox.device.hid.mouse.displacement.performance import XYDisplacementPerformanceBase
from pytestbox.device.hid.mouse.displacement.performance import _102_PERCENT
from pytestbox.device.hid.mouse.displacement.performance import _110_PERCENT
from pytestbox.device.hid.mouse.displacement.performance import _90_PERCENT
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
class SharedSmoothingAlgoFunctionalityTestCase(SmoothingAlgoTestCase):
    """
    Validate USB Boost functionality TestCases
    """

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_enable_sumX_equal_to_threshold_one_shot(self):
        """
        Goal: Verify that smoothing algo enable threshold is configured to 3 as an average over the last 10 reports

        Scenario:
         - 1 report with a deltaX = 30 to match the enabling criteria in one shot
         - 10 reports with deltaX = 2 and deltaY = 2
        Check the report split over the last 10 reports
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE, dy=0)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE + SMOOTH_THRESHOLD_DISABLE),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*2,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE-2)*2,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE-2)*2}")

        average = round(mean(beagle_deltas[-(SMOOTH_AVG_BUFF_SIZE*2):]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of data = {average}")
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

        self.testCaseChecked("FUN_HID_USB_BOOST_0001")
    # end def test_enable_sumX_equal_to_threshold_one_shot

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_enable_max_deltaXY(self):
        """
        Goal: Verify that smoothing algo enable threshold is configured to 3 as an average over the last 10 reports

        Scenario:
         - 10 report with a deltaX = max supported value
         - 10 reports with deltaX = 2 and deltaY = 2
        Check the report split over the last 10 reports
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=OptEmu16BitsRegisterMapBase.Limits.DELTA_UNSIGNED_MAX,
                                       dy=OptEmu16BitsRegisterMapBase.Limits.DELTA_UNSIGNED_MAX,
                                       repetition=SMOOTH_AVG_BUFF_SIZE - 1, skip=2)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE - 1, skip=2)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(OptEmu16BitsRegisterMapBase.Limits.DELTA_UNSIGNED_MAX * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_DISABLE),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        # NB: ideally the expected value shall be SMOOTH_AVG_BUFF_SIZE*2,
        # but we acknowledge that 2 reports will not be split if the internal queue is not empty
        self.assertGreaterEqual(
            a=split_counter, b=(SMOOTH_AVG_BUFF_SIZE-2)*2,
            msg=f"The split report counter {split_counter} is less than {(SMOOTH_AVG_BUFF_SIZE-2)*2}")

        self.testCaseChecked("FUN_HID_USB_BOOST_0003")
    # end def test_enable_max_deltaXY

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_not_enable_sumX_below_enable_threshold(self):
        """
        Goal: Verify that smoothing algo is not enabled when sum of last 10 deltaX values is equal to
              enabling threshold minus 1

        Scenario:
         - 10 reports with deltaX = 2 and deltaY = 0
         - 1 report with a deltaX = 11 => sumX = 29 < enabling criteria (i.e. 30)
         - 11 reports with deltaX = 2 and deltaY = 2
        Check the report are not split over the last 11 reports
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE} slot with deltaX = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"""Sent deltaX = {SMOOTH_AVG_BUFF_SIZE*(SMOOTH_THRESHOLD_ENABLE-SMOOTH_THRESHOLD_DISABLE)+1}""")
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(
            dx=SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE - SMOOTH_THRESHOLD_DISABLE) + 1,
            dy=0)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE +
                      (SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE - SMOOTH_THRESHOLD_DISABLE) + 1) +
                      SMOOTH_THRESHOLD_DISABLE * (SMOOTH_AVG_BUFF_SIZE + 1)),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=0, obtained=split_counter,
            msg=f"The split report counter {split_counter} shall be 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of data = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _90_PERCENT * 10 ** 3,
                                "The report rate average is lower than the specification")

        self.testCaseChecked("FUN_HID_USB_BOOST_0010")
    # end def test_not_enable_sumX_below_enable_threshold

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_not_enable_sumY_below_enable_threshold(self):
        """
        Goal: Verify that smoothing algo enable threshold is configured to 3 as an average of deltaY values
        over the last 10 reports

        Scenario:
         - 10 reports with deltaY = 2 and deltaY = 0
         - 1 report with a deltaY = 11 => sumX = 29 < enabling criteria (i.e. 30)
         - 11 reports with deltaX = 2 and deltaY = 2
        Check the report are not split over the last 11 reports
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE} slot with deltaY = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=SMOOTH_THRESHOLD_DISABLE, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"""Sent deltaY = {SMOOTH_AVG_BUFF_SIZE*(SMOOTH_THRESHOLD_ENABLE-SMOOTH_THRESHOLD_DISABLE)+1}""")
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(
            dx=0,
            dy=SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE - SMOOTH_THRESHOLD_DISABLE) + 1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, _, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE +
                      (SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE - SMOOTH_THRESHOLD_DISABLE) + 1) +
                      SMOOTH_THRESHOLD_DISABLE * (SMOOTH_AVG_BUFF_SIZE + 1)),
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=0, obtained=split_counter,
            msg=f"The split report counter {split_counter} shall be 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of data = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _90_PERCENT * 10 ** 3,
                                "The report rate average is lower than the specification")

        self.testCaseChecked("FUN_HID_USB_BOOST_0011")
    # end def test_not_enable_sumY_below_enable_threshold

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_not_enable_sumXY_below_enable_threshold(self):
        """
        Goal: Verify that smoothing algo enable threshold is configured to 3 as an average of deltaX or deltaY values
        over the last 10 reports

        Scenario:
         - 10 reports with deltaY = 2 and deltaY = 2
         - 1 report with a deltaX = 11 and deltaY = 11 => sumX = sumY = 29 < enabling criteria (i.e. 30)
         - 11 reports with deltaX = 2 and deltaY = 2
        Check the report are not split over the last 11 reports
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX & Y = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Load {SMOOTH_AVG_BUFF_SIZE} slot with deltaX & Y = {SMOOTH_THRESHOLD_DISABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"""Sent deltaX & Y = {SMOOTH_AVG_BUFF_SIZE*(SMOOTH_THRESHOLD_ENABLE-SMOOTH_THRESHOLD_DISABLE)+1}""")
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(
            dx=SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE - SMOOTH_THRESHOLD_DISABLE) + 1,
            dy=SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE - SMOOTH_THRESHOLD_DISABLE) + 1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter = self._process_packets(packets)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(MINIMUM * SMOOTH_AVG_BUFF_SIZE +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE +
                      (SMOOTH_AVG_BUFF_SIZE * (SMOOTH_THRESHOLD_ENABLE - SMOOTH_THRESHOLD_DISABLE) + 1) +
                      SMOOTH_THRESHOLD_DISABLE * (SMOOTH_AVG_BUFF_SIZE + 1)),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")
        self.assertEqual(
            expected=beagle_accumulated_x,
            obtained=beagle_accumulated_y,
            msg="The cumulative displacement value on deltaY does not match the injected value.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=0, obtained=split_counter,
            msg=f"The split report counter {split_counter} shall be 0")

        average = round(mean(beagle_deltas[-SMOOTH_AVG_BUFF_SIZE:]), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of data = {average}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(average, XYDisplacementPerformanceBase.REPORT_RATE_0_25MS * _90_PERCENT * 10 ** 3,
                                "The report rate average is lower than the specification")

        self.testCaseChecked("FUN_HID_USB_BOOST_0012")
    # end def test_not_enable_sumXY_below_enable_threshold

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_sum_abs_X_and_Y_equal_1(self):
        """
        Goal: When the USB boost algo is enabled and the HID report contains deltaX=1 or -1 and deltaY=1 or -1,
              the algo shall split displacement values by putting the X value in the first report
              and Y value in the second

        Scenario:
         - 1 report with a deltaX = 30 to match the enabling criteria in one shot
         - 2 reports with deltaX = 1 and deltaY = 1
         - 2 reports with deltaX = -1 and deltaY = -1
         - 2 reports with deltaX = -1 and deltaY = 1
         - 2 reports with deltaX = 1 and deltaY = -1
        Check the reports are split and comply with the rule
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE, dy=0)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = 1 and deltaY = 1')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=1, dy=1, repetition=1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = -1 and deltaY = -1')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-1, dy=-1, repetition=1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = -1 and deltaY = 1')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=-1, dy=1, repetition=1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = 1 and deltaY = -1')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=1, dy=-1, repetition=1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        enable_algo = False
        sum_x = 0
        for packet in packets:
            delta_x = to_signed_int(packet.x, little_endian=True)
            sum_x += delta_x
            if not enable_algo and sum_x >= SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE:
                enable_algo = True
            elif enable_algo:
                # Check packet content
                delta_y = to_signed_int(packet.y, little_endian=True)
                sum_xy = abs(delta_x) + abs(delta_y)

                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Validate the sum of delta X & Y in each report')
                # ----------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=1, obtained=sum_xy, msg=f"The sum of delta X + Y {sum_xy} shall be 1")
            # end if
        # end for

        self.testCaseChecked("FUN_HID_USB_BOOST_0020")
    # end def test_sum_abs_X_and_Y_equal_1

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_split_x(self):
        """
        Goal: When the USB boost algo is enabled and the HID report contains deltaX > 1,
              the algo shall allocate half of the value in the first report and the other half in the second report.
              If the value is odd, the first reported value is one greater than the second reported value.

        Scenario:
         - 1 report with a deltaX = 30 to match the enabling criteria in one shot
         - 1 report with an incremental deltaX value from 2 to 0x1FF
        Check the reports are split and comply with the rule
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE, dy=0)
        self.motion_emulator.commit_actions()

        delta_x_test_list = list(range(2, 0x1FF))
        for x in delta_x_test_list:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Sent deltaX = {x}')
            # --------------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=x, dy=0, skip=SKIP_COUNTER*4)
            self.motion_emulator.commit_actions()
        # end for
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        enable_algo = False
        sum_x = 0
        previous_x = 0
        for packet in packets:
            delta_x = to_signed_int(packet.x, little_endian=True)
            sum_x += delta_x
            if not enable_algo and sum_x >= SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE:
                enable_algo = True
            elif enable_algo:
                if delta_x + previous_x >= delta_x_test_list[0]:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, f'Verify the sum of 2 consecutive delta X values match the input')
                    # --------------------------------------------------------------------------------------------------
                    self.assertEqual(expected=delta_x_test_list[0], obtained=delta_x + previous_x,
                                     msg=f"The sum of 2 consecutive delta X values {delta_x + previous_x} does not "
                                         f"match the input {delta_x_test_list[0]}")
                    delta_x_test_list = delta_x_test_list[1:]
                    previous_x = 0
                else:
                    previous_x = delta_x
                # end if
            # end if
        # end for

        self.testCaseChecked("FUN_HID_USB_BOOST_0021")
    # end def test_split_x

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_split_y(self):
        """
        Goal: When the USB boost algo is enabled and the HID report contains deltaX > 1,
              the algo shall allocate half of the value in the first report and the other half in the second report.
              If the value is odd, the second reported value is one greater than the first reported value.

        Scenario:
         - 1 report with a deltaX = 30 to match the enabling criteria in one shot
         - 1 report with an incremental deltaX value from 2 to 0x1FF
        Check the reports are split and comply with the rule
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaY = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=MINIMUM, dy=0, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaY = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE)
        self.motion_emulator.commit_actions()

        delta_y_test_list = list(range(2, 0x1FF))
        for y in delta_y_test_list:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Sent deltaY = {y}')
            # --------------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=0, dy=y, skip=SKIP_COUNTER*4)
            self.motion_emulator.commit_actions()
        # end for
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        enable_algo = False
        sum_y = 0
        previous_y = 0
        for packet in packets:
            delta_y = to_signed_int(packet.y, little_endian=True)
            sum_y += delta_y
            if not enable_algo and sum_y >= SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE:
                enable_algo = True
            elif enable_algo:
                if delta_y + previous_y >= delta_y_test_list[0]:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, f'Verify the sum of 2 consecutive delta Y values match the input')
                    # --------------------------------------------------------------------------------------------------
                    self.assertEqual(expected=delta_y_test_list[0], obtained=delta_y + previous_y,
                                     msg=f"The sum of 2 consecutive delta Y values {delta_y + previous_y} does not "
                                         f"match the input {delta_y_test_list[0]}")
                    delta_y_test_list = delta_y_test_list[1:]
                    previous_y = 0
                else:
                    previous_y = delta_y
                # end if
            # end if
        # end for

        self.testCaseChecked("FUN_HID_USB_BOOST_0022")
    # end def test_split_y

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_split_x_y(self):
        """
        Goal: When the USB boost algo is enabled and the HID report contains deltaX & deltaY > 1,
              the algo shall allocate half of the value in the first report and the other half in the second report.
              If the deltaX value is odd, the first reported value is one greater than the second reported value.
              If the deltaY value is odd, the second reported value is one greater than the first reported value.

        Scenario:
         - 1 report with a deltaX = 30 to match the enabling criteria in one shot
         - 1 report with an incremental deltaX & deltaY values from 2 to 0x1FF
        Check the reports are split and comply with the rule
        """
        self.force_report_rate_and_start_usb_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
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

        delta_xy_test_list = list(range(2, 0x1FF))
        for delta in delta_xy_test_list:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Sent deltaX = {delta} & deltaY = {delta}')
            # --------------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=delta, dy=delta, skip=SKIP_COUNTER*4)
            self.motion_emulator.commit_actions()
        # end for
        self.motion_emulator.prepare_sequence()

        packets = self._get_usb_packets()
        enable_algo = False
        sum_x = 0
        previous_x = 0
        previous_y = 0
        for packet in packets:
            delta_x = to_signed_int(packet.x, little_endian=True)
            delta_y = to_signed_int(packet.y, little_endian=True)
            sum_x += delta_x
            if not enable_algo and sum_x >= SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE:
                enable_algo = True
            elif enable_algo:
                if delta_x + previous_x >= delta_xy_test_list[0] or delta_y + previous_y >= delta_xy_test_list[0]:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, f'Verify the sum of 2 consecutive delta X values match the input')
                    # --------------------------------------------------------------------------------------------------
                    self.assertEqual(expected=delta_xy_test_list[0], obtained=delta_x + previous_x,
                                     msg=f"The sum of 2 consecutive delta X values {delta_x + previous_x} does not "
                                         f"match the input {delta_xy_test_list[0]}")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, f'Verify the sum of 2 consecutive delta Y values match the input')
                    # --------------------------------------------------------------------------------------------------
                    self.assertEqual(expected=delta_xy_test_list[0], obtained=delta_y + previous_y,
                                     msg=f"The sum of 2 consecutive delta Y values {delta_y + previous_y} does not "
                                         f"match the input {delta_xy_test_list[0]}")
                    delta_xy_test_list = delta_xy_test_list[1:]
                    previous_x = 0
                    previous_y = 0
                else:
                    previous_x = delta_x
                    previous_y = delta_y
                # end if
            # end if
        # end for

        self.testCaseChecked("FUN_HID_USB_BOOST_0023")
    # end def test_split_x_y

    @features('RcvUSBBoost')
    @level('Functionality')
    @services('OpticalSensor')
    def test_disable_sumX_equal_to_disable_threshold(self):
        """
        Goal: Verify the smoothing algo disable threshold shall be lower than 2 as an average over the last 10 reports

        Scenario:
         - 1 report with a deltaX = 30 to match the enabling criteria in one shot
         - 11 reports with deltaX = 2 and deltaY = 0
         - 1 report with deltaX = 1 and deltaY = 0 => sumX = 19 < disabling criteria (i.e. 20)
         - 10 reports with deltaX = 2 and deltaY = 2
        Check the reports are Not split
        """
        self.force_report_rate_and_start_usb_capture()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Start the test sequence with {SMOOTH_AVG_BUFF_SIZE} deltaX = 0 '
                                         'to reset the xy_buff_prev_values firmware internal buffer')
        # ----------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, dy=MINIMUM, repetition=SMOOTH_AVG_BUFF_SIZE-1)
        self.motion_emulator.commit_actions()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Sent deltaX = {SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE}')
        # ----------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE, dy=0)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=0,
                                       repetition=SMOOTH_AVG_BUFF_SIZE)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE-1, dy=0)
        self.motion_emulator.commit_actions()
        self.motion_emulator.xy_motion(dx=SMOOTH_THRESHOLD_DISABLE, dy=SMOOTH_THRESHOLD_DISABLE,
                                       repetition=SMOOTH_AVG_BUFF_SIZE - 1, skip=SKIP_COUNTER)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()
        packets = self._get_usb_packets()

        beagle_deltas, beagle_accumulated_x, _, split_counter = self._process_packets(packets)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value')
        # ----------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=(SMOOTH_AVG_BUFF_SIZE * SMOOTH_THRESHOLD_ENABLE +
                      SMOOTH_THRESHOLD_DISABLE * (SMOOTH_AVG_BUFF_SIZE + 1) +
                      SMOOTH_THRESHOLD_DISABLE-1 +
                      SMOOTH_THRESHOLD_DISABLE * SMOOTH_AVG_BUFF_SIZE),
            obtained=beagle_accumulated_x,
            msg="The cumulative displacement value obtained in the HID reports does not match the injected value.")

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the split report counter')
        # ----------------------------------------------------------------------------------------------------------
        self.assertLessEqual(
            a=split_counter, b=0,
            msg=f"The split report counter {split_counter} shall be 0")

        average = round(mean(beagle_deltas), 1)
        LogHelper.log_info(self, f"Arithmetic mean (average) of data = {average}")
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # ----------------------------------------------------------------------------------------------------------
        self.assertGreater(average, XYDisplacementPerformanceBase.REPORT_RATE_0_125MS * _102_PERCENT * 10 ** 3,
                           "The report rate average is lower than expected")

        self.testCaseChecked("FUN_HID_USB_BOOST_0030")
    # end def test_disable_sumX_equal_to_disable_threshold
# end class SharedSmoothingAlgoFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
