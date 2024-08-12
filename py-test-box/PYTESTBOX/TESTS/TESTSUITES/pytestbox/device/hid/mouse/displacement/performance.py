#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.displacement.performance
:brief: Hid mouse XY displacement performance test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/03/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import F_OK
from os import access
from os import makedirs
from os.path import join
from statistics import mean
from statistics import stdev
from time import sleep
from uuid import uuid4

from matplotlib import pyplot as plt

from pychannel.usbchannel import UsbChannel
from pyharness.core import TYPE_FAILURE
from pyharness.core import TestException
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hid import HidMouseNvidiaExtension
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ReportRateInfoEvent
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.tool.beagle.beagle480 import Beagle480
from pyraspi.tool.beagle.beagle480 import BeagleChannel
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA0
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA1
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils
from pytestbox.device.hid.base.hidreportutils import to_signed_int
from pytestbox.device.hid.mouse.displacement.xydisplacement import XYDisplacementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Christophe Roquebert"

# Plot the reporting rate graph using matplot lib
ENABLE_GRAPH = False

# Method 1 using a Beagle USB 480 analyser to compute results
# average report rate value shall be in range -2%/+2%
_98_PERCENT = 98 / 100
_102_PERCENT = 102 / 100
# average report rate value shall be in range -5%/+5%
_95_PERCENT = 95 / 100
_105_PERCENT = 105 / 100

# Method 2 using LogiUSB layer to compute results
# average report rate value shall be in range -10%/+10%
_90_PERCENT = 90 / 100
_110_PERCENT = 110 / 100

# Choose a deltaX = 2 to ensure that the "smoothing algo" is not enabled on the receiver side
MOVE_BY_2 = 2
# 80000 continuous XY displacements at 8kHz during 10 seconds
EIGHTY_THOUSAND_DISPLACEMENTS = 80000


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class XYDisplacementPerformanceBase(XYDisplacementTestCase):
    """
    Provide generic methods for the performance testing
    """
    # While 2D sensor polling is done at 1kHz, compute the accumulation value when HID report are created at a slower
    # pace
    REPORT_RATE_8MS = 8
    REPORT_RATE_4MS = 4
    REPORT_RATE_2MS = 2
    REPORT_RATE_1MS = 1
    REPORT_RATE_0_5MS = .5
    REPORT_RATE_0_25MS = .25
    REPORT_RATE_0_125MS = .125

    # tuple(number of polling slot to skip, expected report rate)
    REPORT_RATE = [
        (1, REPORT_RATE_0_25MS),
        (3, REPORT_RATE_0_5MS),
        (7, REPORT_RATE_1MS),
        (15, REPORT_RATE_2MS),
        (31, REPORT_RATE_4MS),
    ]

    CONNECTION_TYPE = None

    def setUp(self):
        """
        Handle test prerequisites
        """
        self.beagle480 = None
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Clean WirelessDeviceStatusBroadcastEvent messages")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=WirelessDeviceStatusBroadcastEvent)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Clean Battery Status messages")
        # --------------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.beagle480 is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Close beagle device")
                # ------------------------------------------------------------------------------------------------------
                self.beagle480.close()
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # post_requisite_reload_nvs flag need not be set to True,
                # if the set_report_Rate is performed in host_mode and switched back to onboard_mode
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False

                ChannelUtils.get_only(
                    test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, check_first_message=False,
                    class_type=WirelessDeviceStatusBroadcastEvent, allow_no_message=True)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean Battery Status messages")
                # ------------------------------------------------------------------------------------------------------
                self.cleanup_battery_event_from_queue()

                ChannelUtils.clean_messages(
                    test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                    class_type=(WirelessDeviceStatusBroadcastEvent, ReportRateInfoEvent))
            # end if
        # end with
        super().tearDown()
    # end def tearDown
    
    @staticmethod
    def _get_delta_times(packets):
        """
        Compute the list of delta time between 2 consecutive HID reports

        :param packets: List of HID reports returned by the USB analyser
        :type packets: ``List[TimestampedBitFieldContainerMixin]``

        :return: tuple of delta times and timestamps
        :rtype: ``Tuple[float, int]``
        """
        beagle_deltas = []
        beagle_timestamps = []
        beagle_previous_timestamp = None
        beagle_initial_timestamp = packets[0].timestamp
        for packet in packets:
            if beagle_previous_timestamp is not None:
                delta = (packet.timestamp - beagle_previous_timestamp) / 10 ** 3
                beagle_deltas.append(delta)
                beagle_timestamps.append((packet.timestamp - beagle_initial_timestamp) / 10 ** 6)
            # end if
            beagle_previous_timestamp = packet.timestamp
        # end for
        return beagle_deltas, beagle_timestamps
    # end def _get_delta_times

    def _plot_graph(self, timestamps, deltas):
        """
        Create a graph to highlight the reporting rate over time

        :param timestamps: list of HID report timestamps
        :type timestamps: ``list[int]``
        :param deltas: list of delta time between 2 consecutive HID reports
        :type deltas: ``list[int]``
        """
        # Creation of beagle trace directory
        beagle_trace_dir = join(self.getContext().getOutputDir(),
                                self.getContext().getCurrentTarget(), 'beagle')
        if not access(beagle_trace_dir, F_OK):
            makedirs(beagle_trace_dir)
        # end if
        file_name = f"{self.id()}{uuid4()}.png"
        plot_path = join(beagle_trace_dir, file_name)

        fig, ax = plt.subplots(1, 1, sharex="all", sharey="all")
        fig.set_figheight(20)
        fig.set_figwidth(50)
        fig.set_dpi(200)
        fig.suptitle('Reporting rate')
        ax.plot(timestamps, deltas)
        ax.margins(x=0)
        ax.set_ylabel('Reporting time [us]')
        ax.set_xlabel('Timeline [ms]')
        plt.savefig(plot_path)
    # end def _plot_graph
    
    def _report_rate_with_button(self, key_id):
        """
        Validate the DUT can report continuous XY displacement and keystrokes at 8kHz during 1 second

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID``
        """
        self.post_requisite_reload_nvs = True

        ExtendedAdjustableReportRateTestUtils.set_report_rate(
            self, connection_type=self.CONNECTION_TYPE, 
            report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pause the polling tasks processing the received reports")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.mute()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Start the USB capture using the Beagle 480 USB analyzer")
        # --------------------------------------------------------------------------------------------------------------
        self.beagle480 = Beagle480(test_case=self, channel_type=BeagleChannel.WIRELESS)
        self.beagle480.start_capture()

        # Verify the impact of a keystroke on a hybrid switch (i.e. left button) and a galvanic (i.e. middle button)
        self.kosmos.sequencer.offline_mode = True
        initial_motion_count = 3000
        x_motion = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate {initial_motion_count} motion with delta X = {x_motion}")
        # --------------------------------------------------------------------------------------------------------------
        motion_count = initial_motion_count
        repetition_max = 256
        while motion_count > repetition_max:
            self.motion_emulator.xy_motion(dx=x_motion, dy=0, repetition=repetition_max - 1)
            self.motion_emulator.commit_actions()
            motion_count -= repetition_max
        # end while
        self.motion_emulator.xy_motion(dx=x_motion, dy=0, repetition=motion_count - 1)
        self.motion_emulator.commit_actions()
        # Start Sensor Emulator model update
        self.kosmos.dt.pes.execute(action=self.motion_emulator.module.action_event.START)
        # Add a 100us delay before pressing the first key
        self.kosmos.pes.delay(delay_ns=100000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press on the {key_id!r} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id, duration=.04, delay=.04, repeat=4)
        # Wait until Sensor Emulator finishes its sequence
        # Warning: FIFO_UNDERRUN is not a state and the user shall ensure the keystroke sequence is not too long
        self.kosmos.dt.pes.wait(action=self.motion_emulator.module.resume_event.FIFO_UNDERRUN)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        # Add a 5s delay to let the Beagle process all the HID reports
        sleep(5)

        self.beagle480.parse()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Filter USB packets to keep HID Mouse report only")
        # --------------------------------------------------------------------------------------------------------------
        self.beagle480.filter(pid_filtering_list=[BG_USB_PID_DATA0, BG_USB_PID_DATA1],
                              report_filtering_list=[HidMouseNvidiaExtension])
        packets = self.beagle480.get_filtered_packets()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Compute the list of delta time between 2 consecutive HID reports")
        # --------------------------------------------------------------------------------------------------------------
        beagle_deltas, beagle_timestamps = self._get_delta_times(packets)
        minimum, maximum, average = self.get_statistics(timings=beagle_deltas)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, self.REPORT_RATE_0_125MS * _95_PERCENT * 10 ** 3,
                           "At least one of the timings is lower than the specification for the reporting rate")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, self.REPORT_RATE_0_125MS * _105_PERCENT * 10 ** 3,
                        "At least one of the timings is greater than the specification for the reporting rate")

        if ENABLE_GRAPH:
            self._plot_graph(beagle_timestamps, beagle_deltas)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with X displacement field set")
        # --------------------------------------------------------------------------------------------------------------
        beagle_accumulated_x = 0
        for packet in packets:
            beagle_accumulated_x += to_signed_int(packet.x[:], little_endian=True)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value retrieved from HID reports')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            x_motion * initial_motion_count, beagle_accumulated_x,
            "The cumulative displacement value obtained in the HID reports does not match the injected value.")

        self.beagle480.close()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Resume the polling tasks processing the received reports")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.unmute()
    # end def _report_rate_with_button

    def _report_rate_stability(self, report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_1KHZ,
                               report_rate_margin=_102_PERCENT):
        """
        Configure the DUT at a given report rate then play continuous XY displacement

        :param report_rate: Report Rate
        :type report_rate: ``int`` or ``HexList``
        """

        ExtendedAdjustableReportRateTestUtils.set_report_rate(
            self, connection_type=self.CONNECTION_TYPE,
            report_rate=report_rate)

        if self.CONNECTION_TYPE == ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS:
            channel = self.current_channel.receiver_channel
        else:
            channel = self.current_channel
        # end if

        # Empty hid_message_queue
        ChannelUtils.clean_messages(
            test_case=self, channel=channel, queue_name=HIDDispatcher.QueueName.HID,
            class_type=HID_REPORTS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pause the polling tasks processing the received reports")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.mute()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Start the USB capture using the Beagle 480 USB analyzer")
        # --------------------------------------------------------------------------------------------------------------
        self.beagle480 = Beagle480(test_case=self, channel_type=BeagleChannel.WIRELESS)
        self.beagle480.start_capture(immediate=False)

        initial_motion_count = EIGHTY_THOUSAND_DISPLACEMENTS
        x_motion = MOVE_BY_2
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate {initial_motion_count} motion with delta X = {x_motion}")
        # ----------------------------------------------------------------------------------------------------------
        motion_count = initial_motion_count
        repetition_max = 256
        while motion_count > repetition_max:
            self.motion_emulator.xy_motion(dx=x_motion, dy=0, repetition=repetition_max - 1)
            self.motion_emulator.commit_actions()
            motion_count -= repetition_max
        # end while
        self.motion_emulator.xy_motion(dx=x_motion, dy=0, repetition=motion_count - 1)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence(timeout=100)
        # Add a 15s delay to let the Beagle process all the HID reports
        sleep(15)

        self.beagle480.print_buffer_usage()

        self.beagle480.parse()
        self.beagle480.close()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Filter USB packets to keep HID Mouse report only")
        # --------------------------------------------------------------------------------------------------------------
        self.beagle480.filter(pid_filtering_list=[BG_USB_PID_DATA0, BG_USB_PID_DATA1],
                              report_filtering_list=[HidMouseNvidiaExtension])
        packets = self.beagle480.get_filtered_packets()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Resume the polling tasks processing the received reports")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.unmute()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Compute the list of delta time between 2 consecutive HID reports")
        # --------------------------------------------------------------------------------------------------------------
        beagle_deltas, beagle_timestamps = self._get_delta_times(packets)
        if ENABLE_GRAPH:
            self._plot_graph(beagle_timestamps, beagle_deltas)
        # end if
        minimum, maximum, average = self.get_statistics(timings=beagle_deltas)

        expected_report_rate = (
            self.REPORT_RATE_0_125MS if report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ else
            self.REPORT_RATE_0_25MS if report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ else
            self.REPORT_RATE_0_5MS if report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_2KHZ else
            self.REPORT_RATE_1MS)
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # ----------------------------------------------------------------------------------------------------------
        self.assertGreater(average, expected_report_rate * _98_PERCENT * 10 ** 3,
                           "The timings average is lower than the specification for the reporting rate")

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # ----------------------------------------------------------------------------------------------------------
        self.assertLess(average, expected_report_rate * report_rate_margin * 10 ** 3,
                        "The timings average is greater than the specification for the reporting rate")

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the HID Mouse report with X displacement field set")
        # ----------------------------------------------------------------------------------------------------------
        beagle_accumulated_x = 0
        hid_report_count = 0
        for packet in packets:
            hid_report_count += 1
            beagle_accumulated_x += to_signed_int(packet.x, little_endian=True)
        # end for

        if hid_report_count > initial_motion_count:
            LogHelper.log_info(
                self, f'{hid_report_count} HID packets received while {initial_motion_count} were expected')
        # end if

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value retrieved from HID reports')
        # ----------------------------------------------------------------------------------------------------------
        self.assertEqual(
            x_motion * initial_motion_count, beagle_accumulated_x,
            "The cumulative displacement value obtained in the HID reports does not match the injected value.")
    # end def _report_rate_stability

    def _report_rate_with_skip(self, skip_index):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
        NB: the test scenario comprises the following five sequences:
          - 1 report with deltaX = 2 followed by one full of 0
          - 1 report with deltaX = 3 followed by three full of 0
          - 1 report with deltaX = 4 followed by seven full of 0
          - 1 report with deltaX = 5 followed by fifteen full of 0
          - 1 report with deltaX = 6 followed by thirty-one full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis

        :param skip_index: index in the REPORT_RATE mapping
        :type skip_index: ``int``

        :raise ``TestException``: If not enough reports were received from the USB analyser
        """
        self.post_requisite_reload_nvs = True
        
        ExtendedAdjustableReportRateTestUtils.set_report_rate(
            self, connection_type=self.CONNECTION_TYPE,
            report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Start the USB capture using the Beagle 480 USB analyzer")
        # --------------------------------------------------------------------------------------------------------------
        self.beagle480 = Beagle480(test_case=self, channel_type=BeagleChannel.WIRELESS)
        self.beagle480.start_capture()

        x_motion = 1
        skip, expected_report_rate = self.REPORT_RATE[skip_index]
        
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pause the polling tasks processing the received reports")
        # ----------------------------------------------------------------------------------------------------------
        self.current_channel.mute()

        initial_motion_count = 1500
        x_motion += 1
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate {initial_motion_count} motions with delta X = {x_motion} "
                                 f"and skip = {skip}")
        # ----------------------------------------------------------------------------------------------------------
        # Start and finish the test sequence with a double deltaX value to ease the debugging
        self.motion_emulator.xy_motion(dx=x_motion * 2, dy=0, skip=skip)
        self.motion_emulator.commit_actions()
        motion_count = initial_motion_count - 4
        repetition_max = 256
        while motion_count > repetition_max:
            self.motion_emulator.xy_motion(dx=x_motion, dy=0, repetition=repetition_max - 1, skip=skip)
            self.motion_emulator.commit_actions()
            motion_count -= repetition_max
        # end while
        self.motion_emulator.xy_motion(dx=x_motion, dy=0, repetition=motion_count - 1, skip=skip)
        self.motion_emulator.commit_actions()
        # Complete the test sequence with a double deltaX value
        self.motion_emulator.xy_motion(dx=x_motion * 2, dy=0)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()
        # Add a 2s delay to let the Beagle process all the HID reports
        sleep(2)

        self.beagle480.parse()
        self.beagle480.close()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Filter USB packets to keep HID Mouse report only")
        # ----------------------------------------------------------------------------------------------------------
        self.beagle480.filter(pid_filtering_list=[BG_USB_PID_DATA0, BG_USB_PID_DATA1],
                              report_filtering_list=[HidMouseNvidiaExtension])
        packets = self.beagle480.get_filtered_packets()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Resume the polling tasks processing the received reports")
        # ----------------------------------------------------------------------------------------------------------
        self.current_channel.unmute()

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Compute the list of delta time between 2 consecutive HID reports")
        # ----------------------------------------------------------------------------------------------------------
        beagle_deltas, beagle_timestamps = self._get_delta_times(packets)
        if len(beagle_deltas) < 2:
            self.beagle480.empty_queue()
            raise TestException(TYPE_FAILURE, f'Not enough samples (i.e. {len(beagle_deltas)}) were received'
                                              'from the Beagle 480 USB Analyser')
        # end if
        minimum, maximum, average = self.get_statistics(timings=beagle_deltas)
        beagle_accumulated_x = 0
        for packet in packets:
            beagle_accumulated_x += to_signed_int(packet.x[:], little_endian=True)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(average, expected_report_rate * _98_PERCENT * 10 ** 3,
                           f"The timings average with delta X = {x_motion} and skip = {skip} is lower than "
                           "the expected reporting rate")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(average, expected_report_rate * _102_PERCENT * 10 ** 3,
                        f"The timings average with delta X = {x_motion} and skip = {skip} is greater than "
                        "the expected reporting rate")

        if ENABLE_GRAPH:
            self._plot_graph(beagle_timestamps, beagle_deltas)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the cumulative displacement value retrieved from HID reports')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            x_motion * initial_motion_count, beagle_accumulated_x,
            f"The cumulative displacement value obtained with delta X = {x_motion} and skip = {skip} does not"
            f" match the injected value. FYI: accumulation value from Beagle capture = {beagle_accumulated_x}')")
    # end def _report_rate_with_skip

    def get_statistics(self, timings):
        """
        Compute the minimum, maximum and average of the received timing values.

        :param timings: list of timing values
        :type timings: ``list[int]``

        :return: minimum, maximum and average timing values in nanoseconds
        :rtype: ``float``, ``float``, ``float``
        """
        average = round(mean(timings), 1)
        maximum = round(max(timings), 1)
        minimum = round(min(timings), 1)
        std_deviation = round(stdev(timings), 1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Data set = {timings}")
        LogHelper.log_info(self, f"Arithmetic mean (average) of data = {average}")
        LogHelper.log_info(self, f"Maximum = {maximum} and minimum = {minimum}")
        LogHelper.log_info(self, f"Delta on max = {(maximum - average) * 100 / average} "
                                 f"and delta on min = {(average - minimum) * 100 / average}")
        LogHelper.log_info(self, f"Sample standard deviation of data = {std_deviation}")

        LogHelper.log_metrics(self,
                              key=f'The report rate : ',
                              value=f'average={average}us, minimum={minimum}us, maximum={maximum}us, '
                                    f'"Delta on max={(maximum - average) * 100 / average}us, '
                                    f'Delta on min = {(average - minimum) * 100 / average}us, '
                                    f'standard deviation={std_deviation}us')
        # --------------------------------------------------------------------------------------------------------------
        return minimum, maximum, average
    # end def get_statistics
# end class XYDisplacementPerformanceBase


class XYDisplacementReportRatePerformanceTestCase(XYDisplacementPerformanceBase):
    """
    Validate ``ReportRate`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        
        # Use the connection type of the current channel
        self.CONNECTION_TYPE = ExtendedAdjustableReportRate.ConnectionType.WIRED \
            if isinstance(self.current_channel, UsbChannel) \
            else ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS
    # end def setUp
    
    @features('Mice')
    @features("Feature8060")
    @features("Feature8100")
    @level("Timing")
    @services('OpticalSensor')
    def test_set_report_rate(self):
        """
        Validate ``SetReportRate`` business test case
        """
        self.post_requisite_reload_nvs = True
        host_mode = OnboardProfiles.Mode.HOST_MODE

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8100 index")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_8100, _, _ = OnboardProfilesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8060 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8060_index, self.feature_8060, _, _ = ReportRateTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {host_mode} (host mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=host_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no error returned")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=self, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over reportRate in reportRateList ")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in ReportRateTestUtils.get_default_report_rate_list(self):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with reportRate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            response = ReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate no error returned")
            # ----------------------------------------------------------------------------------------------------------
            ReportRateTestUtils.MessageChecker.check_fields(
                test_case=self, message=response,
                expected_cls=self.feature_8060.set_report_rate_response_cls, check_map={})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            response = ReportRateTestUtils.HIDppHelper.get_report_rate(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate GetReportRate.reportRate shall be equal to {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ReportRateTestUtils.GetReportRateResponseChecker.check_report_rate(
                test_case=self, response=response, expected=report_rate)

            # Empty hid_message_queue
            ChannelUtils.clean_messages(
                test_case=self, channel=self.current_channel.receiver_channel, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a continuous XY displacement")
            # ----------------------------------------------------------------------------------------------------------
            motion_count = 100
            self.motion_emulator.xy_motion(dx=1, dy=0, repetition=motion_count - 1)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with left button and X displacement fields set")
            # ----------------------------------------------------------------------------------------------------------
            delta = []
            previous_timestamp = None
            for _ in range(motion_count//report_rate):
                # Retrieve the first HID report
                hid_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                if previous_timestamp is not None:
                    delta.append(hid_packet.timestamp - previous_timestamp)
                # end if
                previous_timestamp = hid_packet.timestamp
            # end for

            minimum, maximum, average = self.get_statistics(timings=delta)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(average, report_rate * .99 * 10**6,
                               "At least one of the timings is lower than the specification for the reporting rate")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(average, report_rate * 1.01 * 10**6,
                            "At least one of the timings is greater than the specification for the reporting rate")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("PER_HID_MOTION_0010", _AUTHOR)
    # end def test_set_report_rate

    @features('Mice')
    @features("Feature8061")
    @features("Feature8100")
    @level("Business")
    @services('OpticalSensor')
    def test_set_adjustable_report_rate(self):
        """
        Validate ``SetReportRate`` business test case
        """
        self.post_requisite_reload_nvs = True
        host_mode = OnboardProfiles.Mode.HOST_MODE
        supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8100 index")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_8100, _, _ = OnboardProfilesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {host_mode} (host mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=host_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no error returned")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=self, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over reportRate in reportRateList ")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in supported_report_rate_list:
            self.force_report_rate(report_rate=report_rate)

            # Empty hid_message_queue
            ChannelUtils.clean_messages(
                test_case=self, channel=self.current_channel.receiver_channel, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)

            motion_count = 200
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Emulate {motion_count} motion with delta X = 1")
            # ----------------------------------------------------------------------------------------------------------
            x_motion = 1
            self.motion_emulator.xy_motion(dx=x_motion, dy=0, repetition=motion_count - 1)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with X displacement field set")
            # ----------------------------------------------------------------------------------------------------------
            delta = []
            accumulated_x = 0
            previous_timestamp = None
            accumulation_factor = (
                self.REPORT_RATE_8MS if report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_125HZ else
                self.REPORT_RATE_4MS if report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_250HZ else
                self.REPORT_RATE_2MS if report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_500HZ else
                1)
            while accumulated_x < x_motion * motion_count:
                # Retrieve the first HID report
                hid_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                   allow_no_message=True)
                if hid_packet is None:
                    break
                # end if
                delta_x = to_signed_int(hid_packet.getValue(hid_packet.getFidFromName('x')))
                if previous_timestamp is not None and delta_x == accumulation_factor:
                    # keep delta time if accumulation does not occur
                    delta.append(hid_packet.timestamp - previous_timestamp)
                # end if

                accumulated_x += delta_x
                previous_timestamp = hid_packet.timestamp
            # end while

            minimum, maximum, average = self.get_statistics(timings=delta)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate the cumulative displacement value obtained with {len(delta)} '
                                      'HID reports')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(
                x_motion * motion_count, accumulated_x,
                "The cumulative displacement value obtained in the HID reports does not match the injected value.")

            reporting_rate = (
                self.REPORT_RATE_0_125MS if
                report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ else self.REPORT_RATE_0_25MS if
                report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ else self.REPORT_RATE_0_5MS
                if report_rate == ExtendedAdjustableReportRate.ReportRateList.POS.RATE_2KHZ else accumulation_factor)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the lower limit for the average report rate')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(average, reporting_rate * _90_PERCENT * 10 ** 3,
                               "At least one of the timings is lower than the specification for the reporting rate")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the upper limit for the average report rate')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(average, reporting_rate * _110_PERCENT * 10**6,
                            "At least one of the timings is greater than the specification for the reporting rate")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("PER_HID_MOTION_0011", _AUTHOR)
    # end def test_set_adjustable_report_rate
# end class XYDisplacementReportRatePerformanceTestCase


class XYDisplacementReportRatePerformanceLSXTestCase(XYDisplacementPerformanceBase):
    CONNECTION_TYPE = ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 8kHz.
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ)

        self.testCaseChecked("PER_HID_MOTION_0012", _AUTHOR)
    # end def test_8kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @features('Feature8090')
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_stability_hybrid_switch_mode(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 8kHz
        when the hybrid switch is configured in another power mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the hybrid switch mode configuration")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.flip_hybrid_switch_mode(test_case=self)

        self._report_rate_stability(
            report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ,
            report_rate_margin=_105_PERCENT if self.device_debugger.MCU_NAME.startswith('NRF52') else _102_PERCENT)

        self.testCaseChecked("PER_HID_MOTION_0016", _AUTHOR)
    # end def test_8kHz_report_rate_stability_hybrid_switch_mode

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._4_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_4kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 4kHz
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ)

        self.testCaseChecked("PER_HID_MOTION_0013", _AUTHOR)
    # end def test_4kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._4_KHz)
    @features('Feature8090')
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_4kHz_report_rate_stability_hybrid_switch_mode(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 4kHz
        when the hybrid switch is configured in another power mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the hybrid switch mode configuration")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.flip_hybrid_switch_mode(test_case=self)

        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ)

        self.testCaseChecked("PER_HID_MOTION_0017", _AUTHOR)
    # end def test_4kHz_report_rate_stability_hybrid_switch_mode

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._2_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_2kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 2kHz
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_2KHZ)

        self.testCaseChecked("PER_HID_MOTION_0014", _AUTHOR)
    # end def test_2kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._1_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_1kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 1kHz
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_1KHZ)

        self.testCaseChecked("PER_HID_MOTION_0015", _AUTHOR)
    # end def test_1kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_1_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by one full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=0)

        self.testCaseChecked("PER_HID_MOTION_0020#1", _AUTHOR)
    # end def test_8kHz_report_rate_with_1_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_3_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by three full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=1)

        self.testCaseChecked("PER_HID_MOTION_0020#2", _AUTHOR)
    # end def test_8kHz_report_rate_with_3_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_7_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by seven full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=2)

        self.testCaseChecked("PER_HID_MOTION_0020#3", _AUTHOR)
    # end def test_8kHz_report_rate_with_7_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_15_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by fifteen full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=3)

        self.testCaseChecked("PER_HID_MOTION_0020#4", _AUTHOR)
    # end def test_8kHz_report_rate_with_15_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_31_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by thirty-one full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=4)

        self.testCaseChecked("PER_HID_MOTION_0020#5", _AUTHOR)
    # end def test_8kHz_report_rate_with_31_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_hybrid_button(self):
        """
        Validate the DUT can report continuous XY displacement and 4 keystrokes on a hybrid button at 8kHz
        """
        self._report_rate_with_button(key_id=KEY_ID.LEFT_BUTTON)

        self.testCaseChecked("PER_HID_MOTION_0021#1", _AUTHOR)
    # end def test_8kHz_report_rate_hybrid_button

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_galvanic_button(self):
        """
        Validate the DUT can report continuous XY displacement and 4 keystrokes on a galvanic button at 8kHz
        """
        self._report_rate_with_button(key_id=KEY_ID.MIDDLE_BUTTON)

        self.testCaseChecked("PER_HID_MOTION_0021#2", _AUTHOR)
    # end def test_8kHz_report_rate_galvanic_button
# end class XYDisplacementReportRatePerformanceLSXTestCase


class XYDisplacementReportRatePerformanceUSBTestCase(XYDisplacementPerformanceBase):
    CONNECTION_TYPE = ExtendedAdjustableReportRate.ConnectionType.WIRED

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 8kHz.
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ)

        self.testCaseChecked("PER_HID_MOTION_0022", _AUTHOR)

    # end def test_8kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @features('Feature8090')
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_stability_hybrid_switch_mode(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 8kHz
        when the hybrid switch is configured in another power mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the hybrid switch mode configuration")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.flip_hybrid_switch_mode(test_case=self)

        self._report_rate_stability(
            report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ,
            report_rate_margin=_105_PERCENT if self.device_debugger.MCU_NAME.startswith('NRF52') else _102_PERCENT)

        self.testCaseChecked("PER_HID_MOTION_0023", _AUTHOR)

    # end def test_8kHz_report_rate_stability_hybrid_switch_mode

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._4_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_4kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 4kHz
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ)

        self.testCaseChecked("PER_HID_MOTION_0024", _AUTHOR)

    # end def test_4kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._4_KHz)
    @features('Feature8090')
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_4kHz_report_rate_stability_hybrid_switch_mode(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 4kHz
        when the hybrid switch is configured in another power mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the hybrid switch mode configuration")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.flip_hybrid_switch_mode(test_case=self)

        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ)

        self.testCaseChecked("PER_HID_MOTION_0025", _AUTHOR)

    # end def test_4kHz_report_rate_stability_hybrid_switch_mode

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._2_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_2kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 2kHz
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_2KHZ)

        self.testCaseChecked("PER_HID_MOTION_0026", _AUTHOR)

    # end def test_2kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._1_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_1kHz_report_rate_stability(self):
        """
        Validate the DUT can report 80000 continuous XY displacements at 1kHz
        """
        self._report_rate_stability(report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_1KHZ)

        self.testCaseChecked("PER_HID_MOTION_0027", _AUTHOR)

    # end def test_1kHz_report_rate_stability

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_1_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by one full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=0)

        self.testCaseChecked("PER_HID_MOTION_0028#1", _AUTHOR)

    # end def test_8kHz_report_rate_with_1_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_3_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by three full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=1)

        self.testCaseChecked("PER_HID_MOTION_0028#2", _AUTHOR)

    # end def test_8kHz_report_rate_with_3_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_7_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by seven full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=2)

        self.testCaseChecked("PER_HID_MOTION_0028#3", _AUTHOR)

    # end def test_8kHz_report_rate_with_7_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_15_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by fifteen full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=3)

        self.testCaseChecked("PER_HID_MOTION_0028#4", _AUTHOR)

    # end def test_8kHz_report_rate_with_15_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_with_31_skip(self):
        """
        Validate the DUT can report semi-continuous 1500 XY displacements at 8kHz
          - 1 report with deltaX = 2 followed by thirty-one full of 0
          Note that the deltaX values will be doubled in the first and the last reports to ease a failure analysis
        """
        self._report_rate_with_skip(skip_index=4)

        self.testCaseChecked("PER_HID_MOTION_0028#5", _AUTHOR)

    # end def test_8kHz_report_rate_with_31_skip

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_hybrid_button(self):
        """
        Validate the DUT can report continuous XY displacement and 4 keystrokes on a hybrid button at 8kHz
        """
        self._report_rate_with_button(key_id=KEY_ID.LEFT_BUTTON)

        self.testCaseChecked("PER_HID_MOTION_0029#1", _AUTHOR)

    # end def test_8kHz_report_rate_hybrid_button

    @features('Mice')
    @features("Feature8061SupportedReportRate", ExtendedAdjustableReportRate.ConnectionType.WIRED,
              ExtendedAdjustableReportRate.RATE._8_KHz)
    @level("Performance")
    @services('OpticalSensor')
    @services('USBAnalyser')
    def test_8kHz_report_rate_galvanic_button(self):
        """
        Validate the DUT can report continuous XY displacement and 4 keystrokes on a galvanic button at 8kHz
        """
        self._report_rate_with_button(key_id=KEY_ID.MIDDLE_BUTTON)

        self.testCaseChecked("PER_HID_MOTION_0029#2", _AUTHOR)
    # end def test_8kHz_report_rate_galvanic_button
# end class XYDisplacementReportRatePerformanceUSBTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
