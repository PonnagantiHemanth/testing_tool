#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.advertising
:brief: Validates BLE advertising test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/06/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from copy import deepcopy
from time import sleep
from time import time

import matplotlib.pyplot as plt
import numpy as np
from math import inf
from matplotlib import patches
from matplotlib.colors import TABLEAU_COLORS

from pychannel.blechannel import BleChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.logiconstants import BleAdvertisingInterval
from pychannel.logiconstants import BleAdvertisingSeries
from pychannel.logiconstants import LogitechBleConstants
from pyharness.core import TestException
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleproprepairingutils import BleProPrePairingTestUtils
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import EXTRA_SCAN_TIME
from pytestbox.device.base.bleprotocolutils import MAX_ADVERTISING_INTERVAL_DIRECTED_HDC
from pytestbox.device.base.bleprotocolutils import MS_TO_S_DIVIDER
from pytestbox.device.base.bleprotocolutils import SCAN_DURATION_FOR_INTERVAL_CHECKING
from pytestbox.device.base.bleprotocolutils import SCAN_TRIGGER_TIME
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.bleprosafeprepairedreceiverutils import BleProSafePrePairedReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytransport.ble.bleadvertisingparser import BleAdvertisingParser
from pytransport.ble.bleadvertisingparser import BleAdvertisingPlotter
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.blecontext import BleContextDevice
from pytransport.ble.bleinterfaceclasses import BleGapAddress
from pytransport.transportcontext import TransportContextException
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
MAKE_GRAPH = False  # Flag to generate graphs
DEBUG_GRAPH = False # Flag to indicate if the graph need extra information for test case debugging
SEND_DEBUG_PLOTS = True  # Flag to send any plot made during a test to pycharm

SERIES_TIMING_TOLERANCE = 5
WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE = 5
ERROR_RATE_INTERVAL = 1 # in percents


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class SeriesSequenceStatistics():
    """
    Class to store data about a series' windows for the sequence tests
    """
    timestamps: np.array
    intervals: np.array
    filtered_intervals: np.array
    wrong_intervals: np.array
    on_time: np.array
    off_time: np.array
    start_time: np.array
    end_time: np.array

    def __init__(self, series):
        """
        :param series: the corresponding series
        :type series: ``BleAdvertisingSeries``
        """
        self.series = series

        self.timestamps = np.array([])
        self.intervals = np.array([])
        self.filtered_intervals = np.array([])
        self.wrong_intervals = np.array([])
        self.on_time = np.array([])
        self.off_time = np.array([])
        self.start_time = np.array([])
        self.end_time = np.array([])
    # end def __init__

    def add_statistics(self, test_case, batch_timestamps, batch_intervals, batch_duration, batch_start, batch_end):
        """
        Adds a batch of statistics to the statistic object, calculate on and off time and filter the timestamps

        :param test_case: current test case object
        :type test_case: ``DeviceBaseTestCase``
        :param batch_timestamps: timestamps of a batch
        :type batch_timestamps:  ``list(int)``
        :param batch_intervals: intervals of a batch
        :type batch_intervals: ``list(int)``
        :param batch_duration: duration of a batch in seconds
        :type batch_duration: ``float``
        :param batch_start: start time of a batch in seconds
        :type batch_start: ``float``
        :param batch_end: end time of a batch in seconds
        :type batch_end: ``float``
        """
        if len(self.end_time) > 0:
            off_time = batch_start - self.end_time[-1]
            self.off_time = np.append(self.off_time, off_time)
        # end if

        interval = self.series.value.interval
        if interval == BleAdvertisingInterval.HIGH_DUTY_CYCLE:
            filtered_intervals, wrong_interval = BleProtocolTestUtils.filter_hdc_intervals(test_case, batch_intervals)
        else:
            filtered_intervals, wrong_interval = BleProtocolTestUtils.filter_ldc_advertising(
                test_case, batch_intervals, interval.value)
        # end if

        self.timestamps = np.append(self.timestamps, batch_timestamps)
        self.intervals = np.append(self.intervals, batch_intervals)
        self.filtered_intervals = np.append(self.filtered_intervals, filtered_intervals)
        self.wrong_intervals = np.append(self.wrong_intervals, wrong_interval)
        self.on_time = np.append(self.on_time, batch_duration)
        self.start_time = np.append(self.start_time, batch_start)
        self.end_time = np.append(self.end_time, batch_end)
    # end def add_statistics


    def overlapping_subset(self, overlapped):
        """
        Return the subset of elemeents overlapping a given statistics in time

        :param overlapped: the statistics overlapped by this statistic
        :type overlapped: ``SeriesSequenceStatistics``
        :return: subset lists of start time, end time and on time that overlap the current series
        :rtype: ``tuple(list,list,list)``
        """
        overlapped_start = min(overlapped.start_time[0], overlapped.series.value.start)
        overlapped_end = max(overlapped.end_time[-1], overlapped.series.value.stop)

        start_on_time = self.start_time < overlapped_end
        end_on_time = self.end_time > overlapped_start

        args_overlapped = np.argwhere(np.logical_and(start_on_time, end_on_time))

        return self.start_time[args_overlapped], self.end_time[args_overlapped], self.on_time[args_overlapped]
    # end def overlapping_subset
# end class SeriesSequenceStatistics

class AdvertisingTestCase(DeviceBaseTestCase):
    """
    BLE advertising Test Cases common class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.device_prepairing_ble_address = None
        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        self.memory_manager.backup_nvs_parser = deepcopy(self.memory_manager.nvs_parser)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        if SEND_DEBUG_PLOTS:
            plt.show()
        # end if
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(test_case=self)
                if isinstance(self.backup_dut_channel, BleChannel):
                    ChannelUtils.wait_usb_ble_channel_connection_state(
                        test_case=self, channel=self.backup_dut_channel, connection_state=False)
                # end if
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self, channel=self.backup_dut_channel)
                ChannelUtils.clean_messages(
                    test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                    class_type=WirelessDeviceStatusBroadcastEvent, channel=self.backup_dut_channel)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_channel != self.backup_dut_channel:
                ChannelUtils.close_channel(test_case=self)
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def trigger(self):
        """
        Method to put the device in the expected mode while the scanning starts, ensure the first data is captured
        """
        BleProtocolTestUtils.enter_pairing_mode_ble(self)
    # end def trigger

    def check_device_not_advertising(self, scan_duration):
        """
        Scan for enough time to get multiple potential advertising packet and verify that the device is NOT advertising.

        :param scan_duration: The scan duration in seconds to check that the device is not advertising
        :type scan_duration: ``int`` or ``float``
        """
        try:
            BleProtocolTestUtils.scan_for_current_device(
                test_case=self, scan_timeout=scan_duration, send_scan_request=False,
                force_scan_for_all_timeout=True)
        except TransportContextException as e:
            self.assertEqual(expected=TransportContextException.Cause.DEVICE_NOT_FOUND, obtained=e.get_cause(),
                             msg="Right exception but wrong cause")
        # end try
    # end def check_device_not_advertising

    def _prerequisite_for_prepairing(self):
        """
        Method for prepairing prerequisite in child classes
        """
        # Do nothing in this class
        pass
    # end def _prerequisite_for_prepairing

    def _scan(self, ble_addresses, scan_time, send_scan_request=False, force_scan_for_all_timeout=False):
        """
        scans for a device returning as it's found either the current advertising one or the one with the given address

        :param ble_addresses: if given filters for those given addresses, if omitted scan for the current device
        :type ble_addresses: ``list[BleAddress]`` or ``None``
        :param scan_time: The scan timeout in seconds
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag to indicate that a scan response is requested for each advertising packet - OPTIONAL
        :type send_scan_request: ``bool``
        :param force_scan_for_all_timeout: Flag to indicate to scan for the whole timeout, even if the device is found
                                    before the end - OPTIONAL
        :type force_scan_for_all_timeout: ``bool``

        :return: the found ble devices
        :rtype: ``list[BleContextDevice]``
        """

        self.assertLess(scan_time, 60 * 60, msg=f"scan time must be less than an hour to avoid timeout"
                                                f"(scan time {scan_time / 60}min)")

        if ble_addresses is None:
            try:
                address_current_device = BleProtocolTestUtils.get_current_device_ble_gap_address(test_case=self)
            except TestException:
                DeviceBaseTestUtils.NvsHelper.force_last_gap_address(test_case=self)
                address_current_device = BleProtocolTestUtils.get_current_device_ble_gap_address(test_case=self)
            # end try
            ble_addresses = [address_current_device]
        # end if
        BleProtocolTestUtils.start_scan_for_devices(
            test_case=self, ble_addresses=ble_addresses, scan_timeout=scan_time + SCAN_TRIGGER_TIME,
            send_scan_request=send_scan_request, force_scan_for_all_timeout=force_scan_for_all_timeout)
        self.trigger()
        ble_devices = BleProtocolTestUtils.get_scanning_result(self, scan_time + SCAN_TRIGGER_TIME)

        return ble_devices
    # end def _scan

    def _test_advertising_type(self, expected_type, scanning_timeout, ble_addresses=None):
        """
        Test the advertising type of the device.

        :param expected_type: Expected type of advertising
        :type expected_type: ``BleAdvertisingPduType``
        :param scanning_timeout: Timeout for the scanning part to find the current device
        :type scanning_timeout: ``int`` or ``float``
        :param ble_addresses: The list of bluetooth addresses to consider. If ``None``, the current advertising
                              address will be used - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f"Scan until current device is found (max {scanning_timeout + SCAN_TRIGGER_TIME}s)")
        # ---------------------------------------------------------------------------
        current_device = self._scan(ble_addresses=ble_addresses, scan_time=scanning_timeout)[0]

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the advertising is {expected_type.name}")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=current_device.advertising_type,
                         expected=expected_type,
                         msg=f"Advertising should be {expected_type.name}")
    # end def _test_advertising_type

    def _test_advertising_duration(self, expected_duration, accepted_error, ble_addresses=None,
                                   verify_reconnection=True):
        """
        Test the advertising duration of the device.

        :param expected_duration: Expected duration of advertising in seconds
        :type expected_duration: ``int`` or ``float``
        :param accepted_error: Accepted error in seconds
        :type accepted_error: ``int`` or ``float``
        :param ble_addresses: The list of bluetooth addresses to consider. If ``None``, the current advertising
                              address will be used - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        :param verify_reconnection: Flag indicating to verify the disconnection and reconnection at the end - OPTIONAL
        :type verify_reconnection: ``bool``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f"Scan for the entire advertising window plus {EXTRA_SCAN_TIME + SCAN_TRIGGER_TIME}s "
                                 f"({expected_duration + EXTRA_SCAN_TIME + SCAN_TRIGGER_TIME}s)")
        # ---------------------------------------------------------------------------

        current_devices = self._scan(ble_addresses, expected_duration + EXTRA_SCAN_TIME,
                                     force_scan_for_all_timeout=True)
        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the advertising duration is {expected_duration}s")
        # ---------------------------------------------------------------------------
        timestamps = []
        for current_device in current_devices:
            timestamps.extend([advertising_data.get_timestamps() for advertising_data in current_device.advertising_data])
        # end for

        start = min([timestamp[0] for timestamp in timestamps])
        stop = max([timestamp[-1] for timestamp in timestamps])

        duration = (stop - start) / TIMESTAMP_UNIT_DIVIDER_MAP['s']
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"duration is {duration}")
        # --------------------------------------------------------------------------------------------------------------
        self.assertAlmostEqual(first=duration,
                               second=expected_duration,
                               delta=accepted_error,
                               msg=f"Wrong advertising duration: {duration}")

        if verify_reconnection:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check that the device is back on the first known host")
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
        # end if
    # end def _test_advertising_duration

    def _make_statistics(self, timestamps):
        """
        extract first timestamp to be used as second 0 and generate plot of advertising intervals
        from a set of timestamps indexed by data source if asked

        :param timestamps: Timestamps indexed by data source
        :type timestamps: ``list[list[int]]``
        """
        concatenated_timestamps = BleAdvertisingParser.concatenate_timestamps(
            advertising_data_timestamps=timestamps)
        self.first_timestamp = concatenated_timestamps[0]
        if MAKE_GRAPH:
            test_title = self.id().split('.')[-1]
            timestamps_starting_from_zero = []
            num_graph = 2 if DEBUG_GRAPH else 1
            self.fig_timestamps, self.ax_timestamps = BleAdvertisingPlotter.make_figure(
                title=f"Timestamps by sources for {test_title}", shape=(num_graph, 1))
            BleAdvertisingPlotter.plot_advertising_data_into_timestamp_diagram(
                timestamps, self.ax_timestamps[0], title="Raw advertising data", zero_point=self.first_timestamp)


            self.fig_intervals, self.ax_intervals = BleAdvertisingPlotter.make_figure(
                title=f"Advertising Intervals for {test_title}", shape=(num_graph, 1))

            concatenated_interval = np.ediff1d(concatenated_timestamps)
            self.intervals_numbers = BleAdvertisingPlotter.plot_advertising_intervals(concatenated_interval,
                                                                                      self.ax_intervals[0],
                                                                                      "Raw advertising intervals")
        # end if
        duration = (concatenated_timestamps[-1]-self.first_timestamp)/TIMESTAMP_UNIT_DIVIDER_MAP["s"]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"captured duration = {duration}s")
        LogHelper.log_info(self, f"Timestamps:\n{timestamps}")
        # --------------------------------------------------------------------------------------------------------------
    # end def _make_statistics

    def _plot_add_batches(self, batches_data_id, batches_intervals, batches_timestamps, expected_series):
        """
        Append data from batches to the graphs made with ``_make_statistics``

        :param batches_data_id: list of data source indexes for each batch
        :type batches_data_id: ``np.ndarray``
        :param batches_intervals: list of batches of intervals
        :type batches_intervals: ``np.ndarray``
        :param batches_timestamps: list of batches of timestamps
        :type batches_timestamps: ``np.ndarray``
        :param expected_series: expected series
        :type expected_series: ``tuple[BleAdvertisingSeries]``
        """
        if MAKE_GRAPH:
            BleAdvertisingPlotter.plot_add_ticks_at_intervals(expected_series, self.ax_intervals[0])

            if DEBUG_GRAPH:
                BleAdvertisingPlotter.plot_add_batch_timestamps(batches_timestamps, batches_data_id,
                                                                self.ax_timestamps[1],"Data split in batches",
                                                                self.first_timestamp)
                BleAdvertisingPlotter.plot_add_batch_intervals(batches_intervals, self.intervals_numbers,
                                                               self.ax_intervals[1], "Data split in batches")
            # end if
        # end if
    # end def _plot_add_batches

    def _test_advertising_interval(self, expected_series, ble_addresses=None, check_all=False, max_scan_time=None):
        """
        Test the advertising interval of the device. It works for undirected, directed using Low Duty Cycle (LDC)
        and directed using High Duty Cycle (HDC) advertising.

        :param expected_series: List of expected series definition
        :type expected_series: ``list[BleAdvertisingSeries]``
        :param ble_addresses: The list of bluetooth addresses to consider. If ``None``, the current advertising
                              address will be used - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        :param check_all: Flag indicating to check all interval value and not just the average - OPTIONAL
        :type check_all: ``bool``
        :param max_scan_time: Maximum time to scan, if omited scan for the whole advertising duration - OPTIONAL
        :type max_scan_time: ``int`` or ``float`` or ``None``
        """

        duration = BleProtocolTestUtils.get_scan_time(expected_series, max_scan_time) + EXTRA_SCAN_TIME
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"scanning for {duration + SCAN_TRIGGER_TIME}s")
        # --------------------------------------------------------------------------------------------------------------
        devices = self._scan(ble_addresses=ble_addresses, scan_time=duration, force_scan_for_all_timeout=True)

        timestamps = []
        for device in devices:
            timestamps.extend(BleAdvertisingParser.get_all_advertising_timestamps(device))
        # end for
        self._make_statistics(timestamps)
        batches_tuples = BleAdvertisingParser.split_advertisement_data_in_batches(
            timestamps, expected_series)
        batches_timestamps, batches_intervals, batches_data_id, batches_discarded = batches_tuples

        self._plot_add_batches(batches_data_id, batches_intervals, batches_timestamps, expected_series)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"batches split discarded the following data {batches_discarded}")
        # --------------------------------------------------------------------------------------------------------------

        possible_intervals = set(s.value.interval for s in expected_series)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Possible intervals {possible_intervals}.")
        # --------------------------------------------------------------------------------------------------------------

        filtered_values_for_each_interval = {interval: [] for interval in possible_intervals}
        wrong_interval_for_each_interval = {interval: [] for interval in possible_intervals}

        for i, (batch_timestamp,batch_intervals) in enumerate(zip(batches_timestamps,batches_intervals)):
            stop = (batch_timestamp[-1] - self.first_timestamp) / TIMESTAMP_UNIT_DIVIDER_MAP["s"]
            start = (batch_timestamp[0] - self.first_timestamp) / TIMESTAMP_UNIT_DIVIDER_MAP["s"]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Analysing interval for batch {i}, going from {start} to {stop} ")
            # ----------------------------------------------------------------------------------------------------------

            # calculate a rough interval value with the median of the data. If less than 50% loss it will be close
            rough_intervals = np.median(batch_intervals) / TIMESTAMP_UNIT_DIVIDER_MAP["ms"]

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Rough interval is {rough_intervals}")
            # ----------------------------------------------------------------------------------------------------------
            most_likely_interval = -inf
            # get the biggest interval bellow the rough interval
            for interval in possible_intervals:
                if most_likely_interval < interval <= rough_intervals:
                    most_likely_interval = interval
                # end if
            # end for

            self.assertNotEqual(unexpected=-inf, obtained=most_likely_interval,
                                msg=f"Rough interval {rough_intervals} too low compared "
                                    f"to any expected interval {possible_intervals}")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Using interval {most_likely_interval} for detailed check")
            # ----------------------------------------------------------------------------------------------------------

            if most_likely_interval == BleAdvertisingInterval.HIGH_DUTY_CYCLE:
                filtered_values, wrong_interval = BleProtocolTestUtils.filter_hdc_intervals(test_case=self,
                                                                                            intervals=batch_intervals)
            else:
                filtered_values, wrong_interval = BleProtocolTestUtils.filter_ldc_advertising(
                    test_case=self, intervals=batch_intervals,
                    expected_interval_ms=most_likely_interval)
            # end if
            filtered_values_for_each_interval[most_likely_interval].extend(filtered_values)
            wrong_interval_for_each_interval[most_likely_interval].extend(wrong_interval)
        # end for

        for interval in possible_intervals:
            filtered_values = filtered_values_for_each_interval[interval]
            wrong_interval = wrong_interval_for_each_interval[interval]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check there is at least one interval with the expected value: {interval}")
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(len(filtered_values), 0, f"No intervals detected for the expected interval {interval}")
            if interval == BleAdvertisingInterval.HIGH_DUTY_CYCLE:
                BleProtocolTestUtils.check_advertising_interval_directed_hdc(
                    test_case=self, filtered_values=filtered_values, wrong_interval=wrong_interval, check_all=check_all)
            else:
                BleProtocolTestUtils.check_advertising_interval_undirected_or_directed_ldc(
                    test_case=self, expected_interval_ms=interval, filtered_values=filtered_values,
                    wrong_interval=wrong_interval, check_all=check_all)
            # end if
        # end for
    # end def _test_advertising_interval

    def _test_advertising_sequence(self, expected_series, time, pairing, prepairing):
        """
        Detail check of the sequences of series, scan for the whole duration,
        then using packet content and median interval, group packets in their respective series
        then verifies their position in time

        """
        no_overlap = []
        overlapped = []
        for i, series in enumerate(expected_series):
            higher_priority_series = expected_series[i + 1:]
            overlapping_series = []
            on_time, repetition = series.value.window.value if series.value.window.value is not None else (0, 0)
            for upper_series in higher_priority_series:
                upper_on_time, upper_repetition = upper_series.value.window.value if (upper_series.value.window.value
                                                                                      is not None) else (0, 0)

                start_after = upper_series.value.start.value > series.value.stop.value
                end_before = upper_series.value.stop.value < series.value.start.value
                not_aligned = repetition != upper_repetition

                if not (start_after or end_before) and not_aligned:
                    overlapping_series.append(upper_series)
                # end if

            # end for
            if len(overlapping_series) > 0:
                overlapped.append((series, overlapping_series))
            else:
                no_overlap.append(series)
            # end if
        # end for

        if prepairing:
            address_current_device = BleProtocolTestUtils.increment_address(self)
            ble_addresses = [self.device_prepairing_ble_address, address_current_device]
        else:
            try:
                address_current_device = BleProtocolTestUtils.get_current_device_ble_gap_address(test_case=self)
            except TestException:
                DeviceBaseTestUtils.NvsHelper.force_last_gap_address(test_case=self)
                address_current_device = BleProtocolTestUtils.get_current_device_ble_gap_address(test_case=self)
            # end try
            ble_addresses = [address_current_device]
        # end if

        if pairing:
            current_devices = BleProtocolTestUtils.scan_for_devices_with_entering_pairing_mode_during_scan(
                test_case=self, ble_addresses=ble_addresses,
                scan_timeout=time + EXTRA_SCAN_TIME, send_scan_request=False, force_scan_for_all_timeout=True)
        else:
            current_devices = BleProtocolTestUtils.scan_for_devices(
                test_case=self, ble_addresses=ble_addresses, scan_timeout=time+ EXTRA_SCAN_TIME,
                send_scan_request=False, force_scan_for_all_timeout=True)
        # end if

        pairing_device = None
        prepairing_device = None
        if prepairing:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check both advertising type are found "
                                      "(they will be seen as different devices)")
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=len(current_devices), expected=2,
                             msg=f"Did not find all devices, found: {current_devices}")

            for device in current_devices:
                if device.address == address_current_device:
                    pairing_device = device
                    # ---------------------------------------------------------------------------
                    LogHelper.log_info(self, f"Found pairing device with address {address_current_device}")
                    # ---------------------------------------------------------------------------
                elif device.address == self.device_prepairing_ble_address:
                    prepairing_device = device
                    # ---------------------------------------------------------------------------
                    LogHelper.log_info(self, f"Found prepairing device with address "
                                             f"{self.device_prepairing_ble_address}")
                    # ---------------------------------------------------------------------------
                else:
                    assert False, (f"FATAL ERROR: unknown device found with address"
                                   f" {device.address}, this should not happen")
                # end if
            # end for
        else:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check advertising device is found ")
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=len(current_devices), expected=1,
                             msg=f"Did not find the device, or found more, found: {current_devices}")
            pairing_device = current_devices[0]
        # end if
        # put all the timestamps in a list
        timestamps = []
        pairing_device_data_id = list(range(len(pairing_device.advertising_data)))
        timestamps.extend(BleAdvertisingParser.get_all_advertising_timestamps(pairing_device))
        if prepairing_device is not None:
            start = pairing_device_data_id[-1] + 1
            prepairing_device_data_ids = list(range(start, start + len(prepairing_device.advertising_data)))
            timestamps.extend(BleAdvertisingParser.get_all_advertising_timestamps(prepairing_device))
        else:
            prepairing_device_data_ids = []
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Extract series information from advertising data")
        # --------------------------------------------------------------------------------------------------------------

        self._make_statistics(timestamps)
        batches_timestamps, batches_intervals, batches_data_id, batches_discarded = \
            BleAdvertisingParser.split_advertisement_data_in_batches(timestamps, expected_series)
        first_timestamp = batches_timestamps[0][0]
        self._plot_add_batches(batches_data_id, batches_intervals, batches_timestamps, expected_series)

        # make data structures to isolate interesting data for each series

        statistics_for_series = {series: SeriesSequenceStatistics(series) for series in expected_series}

        series_sequence = []

        unique_packets = BleAdvertisingParser.get_packet_shared_data(expected_series)
        packets_expected_data = []
        for series_set in unique_packets:
            data = BleProtocolTestUtils.build_expected_advertising_data(self, series_set[0].value.packet)
            packets_expected_data.append(data)
        # end for
        for i, (batch_timestamp, batch_intervals, batch_data_id, batch_discarded) in \
                enumerate(zip(batches_timestamps, batches_intervals, batches_data_id, batches_discarded)):
            batch_start = (batch_timestamp[0] - first_timestamp) / TIMESTAMP_UNIT_DIVIDER_MAP["s"]
            batch_end = (batch_timestamp[-1] - first_timestamp) / TIMESTAMP_UNIT_DIVIDER_MAP["s"]

            batch_duration = batch_end - batch_start

            # get the current series from the data
            current_series = None
            if batch_data_id in prepairing_device_data_ids:
                # only advertising series from prepairing
                current_series = BleAdvertisingSeries.D
            else:
                advertising_data = pairing_device.advertising_data[batch_data_id].records

                self.assertIn(member=advertising_data, container=packets_expected_data,
                              msg=f"packet of unexpected series found {packets_expected_data}")

                index = packets_expected_data.index(advertising_data)

                possible_series = unique_packets[index]
                if len(possible_series) == 1:
                    current_series = possible_series[0]
                else:

                    if len(possible_series) > 1:
                        if len(batch_intervals) > 1:
                            rough_interval = np.median(batch_intervals[1:]) / TIMESTAMP_UNIT_DIVIDER_MAP['ms']
                            # ------------------------------------------------------------------------------------------
                            LogHelper.log_info(self, "multiple series can possibly be represented by this batch"
                                               f"use median of interval {rough_interval} to determine the correct one")
                            # ------------------------------------------------------------------------------------------
                            most_likely_interval = -inf
                            # get the biggest interval bellow the rough interval
                            for series in possible_series:
                                interval = series.value.interval.value
                                if most_likely_interval < interval <= rough_interval:
                                    most_likely_interval = interval
                                    current_series = series
                                # end if
                            # end for

                            self.assertNotEqual(unexpected=-inf, obtained=most_likely_interval,
                                                msg=f"Rough interval {rough_interval} too low compared "
                                                    f"to any expected interval of the series : "
                                                    f"{','.join([s.name for s in possible_series])}")
                        else:
                            # ------------------------------------------------------------------------------------------
                            LogHelper.log_info(self, "Multiple series can possibly be represented by this batch"
                                                     "but it is too short for use of median interval, so the previous"
                                                     "matching series is used")
                            # ------------------------------------------------------------------------------------------
                            for series in reversed(series_sequence):
                                if series in possible_series:
                                    current_series = series
                                    break
                                # end if
                            # end for
                        # end if
                    else:
                        current_series = possible_series[0]
                    # end if
                # end if
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"current series is of this batch is {current_series.name}")
            # ----------------------------------------------------------------------------------------------------------
            statistics_for_series[current_series].add_statistics(self, batch_timestamp, batch_intervals, batch_duration,
                                                                 batch_start, batch_end)

            series_sequence.append(current_series)
        # end for

        if MAKE_GRAPH:
            index = {series: i for i, series in enumerate(expected_series)}
            test_title = self.id().split('.')[-1]
            fig, ax = BleAdvertisingPlotter.make_figure(f"Series sequence of for {test_title}")
            colors = list(TABLEAU_COLORS.keys())

            length = 0
            for series, statistics in statistics_for_series.items():
                i = index[series]
                for start, end in zip(statistics.start_time, statistics.end_time):
                    rect = patches.Rectangle((start, i), end - start, 1, color=colors[i])
                    ax[0].add_patch(rect)
                    length = max(end, length)
                # end for
            # end for
            label_name= [s.name for s in expected_series]

            ax[0].set_yticks(np.arange(stop=len(expected_series)+0.5, start=0.5), labels=label_name)
            ax[0].set_yticks(np.arange(stop=len(expected_series)+1, start=0), minor=True)
            ax[0].set_xticks(np.arange(stop=length,step=5), minor=False )
            ax[0].set_xticks(np.arange(stop=length,step=1), minor=True)
            ax[0].grid(True, axis="both")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "[Test loop] on each series who are not overlapped with another")
        # --------------------------------------------------------------------------------------------------------------
        for series in no_overlap:
            statistics = statistics_for_series[series]
            self._check_non_overlapped(series, statistics)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop on each series who are not overlapped with another")
        LogHelper.log_info(self, "Test loop on each series who are overlapped with another")
        # --------------------------------------------------------------------------------------------------------------

        for series, overlapping in overlapped:
            statistics = statistics_for_series[series]
            assert len(overlapping) == 1, "Multiple overlapping series not supported"
            overlapping_statistics = statistics_for_series[overlapping[0]]
            self._check_overlapped(series, statistics, overlapping_statistics)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop on each series who are overlapped with another")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_advertising_sequence

    def _check_non_overlapped(self, series, statistics):
        """
        Check the timing of a series which is not overlapped by another series

        :param series: series to check
        :type series: ``BleAdvertisingSeries``
        :param statistics: statistics of a series
        :type statistics: ``SeriesSequenceStatistics``
        """
        name = series.name
        expected_on_time, repetition_duration = series.value.window.value if series.value.window.value is not None \
            else (None, None)
        expected_off_time = repetition_duration - expected_on_time if repetition_duration is not None else None
        interval_ms = series.value.interval.value \
            if series.value.interval is not BleAdvertisingInterval.HIGH_DUTY_CYCLE else 3.5
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check series {name} has the right intervals")
        # ----------------------------------------------------------------------------------------------------------
        error_rate = len(statistics.wrong_intervals) / len(statistics.intervals)
        self.assertLess(error_rate, ERROR_RATE_INTERVAL / 100.0,
                        msg=f"Series {name} should not have more than {ERROR_RATE_INTERVAL}% of wrong intervals")
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check series {name} start at the right time")
        # ----------------------------------------------------------------------------------------------------------
        first_start = statistics.start_time[0]
        start = series.value.start
        self.assertGreaterEqual(first_start, start * (1 - SERIES_TIMING_TOLERANCE / 100.0),
                                msg=f"The advertising for series {name} started too early ("
                                    f"expect start after {start}-{SERIES_TIMING_TOLERANCE}%)")
        self.assertLessEqual(first_start, start * (1 + SERIES_TIMING_TOLERANCE / 100.0),
                             msg=f"The advertising for series {name} started too late "
                                 f"(expect start before {start}+{SERIES_TIMING_TOLERANCE}%)")
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check series {name} stops at the right time")
        # ----------------------------------------------------------------------------------------------------------
        stop = series.value.stop.value
        last_end = statistics.end_time[-1]
        window_tolerance = WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE * interval_ms / 1e3
        self.assertGreaterEqual(last_end, stop * (1 - SERIES_TIMING_TOLERANCE / 100.0) - window_tolerance,
                                msg=f"The advertising for series {name} stopped too early "
                                    f"(expect start after {stop:d}-{SERIES_TIMING_TOLERANCE}% )"
                                    f"- {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms")
        self.assertLessEqual(last_end, stop * (1 + SERIES_TIMING_TOLERANCE / 100.0) + window_tolerance,
                             msg=f"The advertising for series {name} stopped too late "
                                 f"(expect start before {stop:d}+{SERIES_TIMING_TOLERANCE}% "
                                 f"+ {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms)")
        if expected_on_time is not None:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check series {name} has the windows on for the right length")
            # ------------------------------------------------------------------------------------------------------
            for i, measured_on_time in enumerate(statistics.on_time):
                self.assertGreaterEqual(measured_on_time, expected_on_time * (1 - SERIES_TIMING_TOLERANCE / 100.0)
                                        - window_tolerance,
                                        msg=f"The advertising window N°{i} of series {name} was on too shortly "
                                            f"(expected duration {expected_on_time}-{SERIES_TIMING_TOLERANCE}%)"
                                            f"- {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms")
                self.assertLessEqual(measured_on_time, expected_on_time * (1 + SERIES_TIMING_TOLERANCE / 100.0)
                                     + window_tolerance,
                                     msg=f"The advertising window N°{i} of series {name} was on too long "
                                         f"(expected duration {expected_on_time}+{SERIES_TIMING_TOLERANCE}%)"
                                         f"+ {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms)")
            # end for
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check series {name} has  the windows off for the right time")
            # ------------------------------------------------------------------------------------------------------
            for i, measured_on_time in enumerate(statistics.off_time):
                self.assertGreaterEqual(measured_on_time, expected_off_time * (1 - SERIES_TIMING_TOLERANCE / 100.0)
                                        - window_tolerance,
                                        msg=f"The advertising window N°{i} of series {name} was off too shortly "
                                            f"(expected duration {expected_on_time}-{SERIES_TIMING_TOLERANCE}%)")
                self.assertLessEqual(measured_on_time, expected_off_time * (1 + SERIES_TIMING_TOLERANCE / 100.0)
                                     + window_tolerance,
                                     msg=f"The advertising window N°{i} of series {name} was off too long "
                                         f"(expected duration {expected_on_time}+{SERIES_TIMING_TOLERANCE}%)")
            # end for
        else:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the advertising happens during the whole duration")
            # ------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1, obtained=len(statistics.on_time))
        # end if
    # end def _check_non_overlapped

    def _check_overlapped(self, series, statistics, overlapping_statistics):
        """
        Check the timing of a series which is not overlapped by another series

        :param series: series to check
        :type series: ``BleAdvertisingSeries``
        :param statistics: statistics of a series
        :type statistics: ``SeriesSequenceStatistics``
        :param overlapping_statistics: statistic of the series overlapping
        :type overlapping_statistics: ``SeriesSequenceStatistics``
        """
        name = series.name
        expected_on_time, repetition_duration = series.value.window.value if series.value.window.value is not None \
            else (None, None)
        expected_off_time = repetition_duration - expected_on_time if repetition_duration is not None else None
        interval_ms = series.value.interval.value \
            if series.value.interval is not BleAdvertisingInterval.HIGH_DUTY_CYCLE else 3.5

        overlapped_start, overlapped_stop, overlapped_on_time = overlapping_statistics.overlapping_subset(statistics)


        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Checking series {name} has the right intervals")
        # ----------------------------------------------------------------------------------------------------------
        error_rate = len(statistics.wrong_intervals) / len(statistics.intervals)
        self.assertLess(error_rate, ERROR_RATE_INTERVAL / 100.0,
                        msg=f"Series {name} should not have more than {ERROR_RATE_INTERVAL}% of wrong intervals")
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Checking series {name} start at the right time")
        # ----------------------------------------------------------------------------------------------------------
        window_tolerance = WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE * interval_ms / 1e3
        before_stat_count = np.count_nonzero(overlapping_statistics.start_time <= series.value.start* (
                1 + SERIES_TIMING_TOLERANCE / 100.0))
        overlapped_time_at_start = overlapping_statistics.end_time[before_stat_count-1] if before_stat_count > 0 else 0.
        first_start = statistics.start_time[0]
        if before_stat_count == 1:
            expected_start = series.value.start + overlapped_time_at_start
        else:
            expected_start = max(series.value.start, overlapped_time_at_start)
        # end if
        self.assertGreaterEqual(first_start, expected_start * (1 - SERIES_TIMING_TOLERANCE / 100.0) - window_tolerance,
                                msg=f"The advertising for series {name} started too early ("
                                    f"expect start after {expected_start}-{SERIES_TIMING_TOLERANCE}%)"
                                    f"- {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms")
        self.assertLessEqual(first_start, expected_start * (1 + SERIES_TIMING_TOLERANCE / 100.0) + window_tolerance,
                             msg=f"The advertising for series {name} started too late "
                                 f"(expect start before {expected_start}+{SERIES_TIMING_TOLERANCE}%)"
                                 f"+ {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms")
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Checking series {name} stops at the right time")
        # ----------------------------------------------------------------------------------------------------------
        stop = series.value.stop.value

        if series != BleAdvertisingSeries.A:
            last_end = statistics.end_time[-1]

            self.assertGreaterEqual(last_end, stop * (1 - SERIES_TIMING_TOLERANCE / 100.0) - window_tolerance,
                                    msg=f"The advertising for series {name} stopped too early "
                                        f"(expect start after {stop:d}-{SERIES_TIMING_TOLERANCE}% )"
                                        f"- {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms")
            self.assertLessEqual(last_end, stop * (1 + SERIES_TIMING_TOLERANCE / 100.0) + window_tolerance,
                                 msg=f"The advertising for series {name} stopped too late "
                                     f"(expect start before {stop:d}+{SERIES_TIMING_TOLERANCE}% "
                                     f"+ {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms)")
        else:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "ignore length of series A to correct for https://jira.logitech.io/browse/BT-572")
            # --------------------------------------------------------------------------------------------------------------
        # end if
        if expected_on_time is not None:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check series {name} has the windows are on for the right time")
            # ------------------------------------------------------------------------------------------------------
            for i, measured_on_time in enumerate(statistics.on_time):
                self.assertLessEqual(measured_on_time, expected_on_time * (1 + SERIES_TIMING_TOLERANCE / 100.0)
                                     + window_tolerance,
                                     msg=f"The advertising window N°{i} of series {name} was on too long "
                                         f"(expected duration {expected_on_time:d}+{SERIES_TIMING_TOLERANCE}%)"
                                         f"+ {WINDOW_TIMING_LOSS_LAST_PACKETS_TOLERANCE}*{interval_ms}ms)")
            # end for
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check series {name} has  the windows are off for the right time")
            # ------------------------------------------------------------------------------------------------------
            for i, measured_off_time in enumerate(statistics.off_time):
                arg_corresponding_overlapped = np.argwhere(overlapped_start >= statistics.end_time[i])
                if len(arg_corresponding_overlapped) > 0:
                    overlapped_on_time_corresponding = overlapped_on_time[arg_corresponding_overlapped[0][0]][0]
                    expected_off_time_local = expected_off_time  +overlapped_on_time_corresponding
                else:
                    expected_off_time_local = expected_off_time
                # end if
                self.assertLessEqual(measured_off_time, expected_off_time_local * (1 + SERIES_TIMING_TOLERANCE / 100.0)
                                     + window_tolerance,
                                     msg=f"The advertising window N°{i} of series {name} was off too long "
                                         f"(expected duration {expected_on_time:d}+{SERIES_TIMING_TOLERANCE}%)")

            # end for
        else:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the advertising happens during the whole duration")
            # ------------------------------------------------------------------------------------------------------
            for i, measured_off_time in enumerate(statistics.off_time):
                arg_corresponding_overlapped = np.argwhere(overlapped_start>= statistics.end_time[i])
                if len(arg_corresponding_overlapped) > 0:
                    overlapped_on_time_corresponding = overlapped_on_time[arg_corresponding_overlapped[0][0]][0]
                    self.assertGreater(a=measured_off_time,
                                       b=overlapped_on_time_corresponding,
                                       msg="")
                    self.assertLess(a=measured_off_time,
                                    b=overlapped_on_time_corresponding + window_tolerance,
                                    msg="The advertising window N°{i} of series {name} was off too long "
                                        f"(expected duration {expected_on_time:d}+{SERIES_TIMING_TOLERANCE}%)")

                else:
                    self.fail(f"The advertising for series {name} is off when no overlapping series asks for it")
                # end if
            # end for
        # end if
    # end def _check_overlapped

    def _connect_and_check_no_advertising(self, current_device, advertising_interval):
        """
        Connect to a device and check that it is not advertising after that.

        :param current_device: Current device for the test
        :type current_device: ``BleContextDevice``
        :param advertising_interval: Interval value in milliseconds to use to calculate the duration of the scan to
                                     get a minimum of advertising packets (if any)
        :type advertising_interval: ``int``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to the device")
        # ---------------------------------------------------------------------------
        BleProtocolTestUtils.connect_device(test_case=self, ble_context_device=current_device, confirm_connect=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Scan for a duration wide enough to get "
                                 f"{SCAN_DURATION_FOR_INTERVAL_CHECKING} potential advertising packets")
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the device is not advertising anymore")
        # ---------------------------------------------------------------------------
        scan_duration = advertising_interval / MS_TO_S_DIVIDER * SCAN_DURATION_FOR_INTERVAL_CHECKING
        self.check_device_not_advertising(scan_duration=scan_duration)
    # end def _connect_and_check_no_advertising

    def common_advertising_packet_content_pairing_mode_application(self):
        """
        Check the advertising packet content when the device is in application mode and unpaired.
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self)
        duration = BleProtocolTestUtils.get_scan_time_one_window_each_series(expected_series)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Ble Pairing mode and scan until one window of each series is expected to"
                                 f"have been found ({duration})")
        # ---------------------------------------------------------------------------
        current_device = BleProtocolTestUtils.scan_for_current_device_with_entering_pairing_mode_during_scan(
            test_case=self, scan_timeout=duration, send_scan_request=False, force_scan_for_all_timeout=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the advertising packets content")
        # ---------------------------------------------------------------------------
        expected_series_sharing_packets = BleAdvertisingParser.get_packet_shared_data(expected_series)
        for i, series_sharing_packet in enumerate(expected_series_sharing_packets):
            BleProtocolTestUtils.check_advertising_content(test_case=self,
                                                           advertising_packet=current_device.advertising_data[i],
                                                           expected_series=series_sharing_packet[0])
        # end for
    # end def common_advertising_packet_content_pairing_mode_application

    def common_scan_response_content_pairing_mode_application(self, expected_series):
        """
        Check the scan response content when the device is in application mode and unpaired.
        :param expected_series: expected series
        :type expected_series: ``list[BleAdvertisingSeries]``
        """
        duration = BleProtocolTestUtils.get_scan_time_one_window_each_series(expected_series)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Ble Pairing mode and scan until one window of each series is expected to"
                                 f"have been found ({duration}) with scan response")
        # ---------------------------------------------------------------------------
        current_device = BleProtocolTestUtils.scan_for_current_device_with_entering_pairing_mode_during_scan(
            test_case=self, scan_timeout=duration, send_scan_request=True, force_scan_for_all_timeout=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the scan responses content")
        # ---------------------------------------------------------------------------
        expected_series_sharing_packets = BleAdvertisingParser.get_scan_response_shared_data(expected_series)
        for i, series_sharing_packet in enumerate(expected_series_sharing_packets):
            BleProtocolTestUtils.check_scan_response_content(
                test_case=self, scan_response=current_device.scan_response[i],
                expected_series=series_sharing_packet[0])
        # end for
    # end def common_scan_response_content_pairing_mode_application

    def common_business_pairing_mode_application(self):
        """
        Check the business cases when the device is in application mode and unpaired.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Ble Pairing mode and scan until current "
                                 "device is found (max 2s) with scan request")
        # ---------------------------------------------------------------------------
        current_device = BleProtocolTestUtils.scan_for_current_device_with_entering_pairing_mode_during_scan(
            test_case=self, scan_timeout=2, send_scan_request=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the advertising is connectable undirected")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=current_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg="Advertising should be connectable undirected")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the first advertising packet content")
        # ---------------------------------------------------------------------------
        BleProtocolTestUtils.check_advertising_content(test_case=self,
                                                       advertising_packet=current_device.advertising_data[0])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the scan response is present")
        # ---------------------------------------------------------------------------
        self.assertNotNone(obtained=current_device.scan_response, msg="The scan response should be present")
        self.assertNotEqual(unexpected=0, obtained=len(current_device.scan_response),
                            msg="The scan response should be present")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the first scan response content")
        # ---------------------------------------------------------------------------
        BleProtocolTestUtils.check_scan_response_content(
            test_case=self, scan_response=current_device.scan_response[0])

        advertising_interval = max(self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_SecondAdvertisingIntervalMs,
                                   self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_SecondAdvertisingIntervalMs)
        self._connect_and_check_no_advertising(
            current_device=current_device, advertising_interval=advertising_interval)
    # end def common_business_pairing_mode_application

    def common_business_paired_mode(self):
        """
        Check the business cases when the device is in paired mode.
        """
        # ---------------------------------------------------------------------------
        scan_time = 2
        LogHelper.log_step(self, f"Scan until current device is found (max {scan_time + SCAN_TRIGGER_TIME}s) with scan request")
        # ---------------------------------------------------------------------------
        current_device = self._scan(ble_addresses=[self.current_channel.get_device_ble_address()], scan_time=scan_time,
                                    send_scan_request=False)[0]

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the advertising is directed")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=current_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
                         msg="Advertising should be directed")

        self._connect_and_check_no_advertising(current_device=self.current_channel.get_ble_context_device(),
                                               advertising_interval=MAX_ADVERTISING_INTERVAL_DIRECTED_HDC)
    # end def common_business_paired_mode
# end class AdvertisingTestCase


class AdvertisingPairingModeTestCase(AdvertisingTestCase):
    """
    BLE advertising Test Cases common class for pairing mode
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.last_ble_address = None

        super().setUp()

        self._prerequisite_for_prepairing()

        self.post_requisite_reload_nvs = True
    # end def setUp

    def _prerequisite_for_prepairing(self):
        """
        Method for prepairing prerequisite in child classes
        """
        # Do nothing in this class
        pass
    # end def _prerequisite_for_prepairing
# end class AdvertisingPairingModeTestCase


class AdvertisingPairingModeUsedPrepairingDataTestCase(AdvertisingPairingModeTestCase):
    """
    BLE advertising Test Cases common class for pairing mode with used prepairing data present
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.clean_receiver_pairing_data = False

        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.clean_receiver_pairing_data:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Cleanup all pairing slots in the receiver except the first one")
                # ------------------------------------------------------
                DevicePairingTestUtils.unpair_all(test_case=self)
                self.clean_receiver_pairing_data = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def _prerequisite_for_prepairing(self):
        # See ``AdvertisingPairingModeTestCase._prerequisite_for_prepairing``
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Add prepairing information in the device and in the receiver and make them connect')
        # ---------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Cleanup all pairing slots in the receiver except the first one')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(test_case=self)

        feature_index_1816, feature_1816, ltk_key, irk_remote_key, irk_local_key, csrk_remote_key, csrk_local_key = \
            BleProPrePairingTestUtils.get_1816_and_generate_keys_prepairing(test_case=self)

        rcv_prepairing_slot = 2

        self.clean_receiver_pairing_data = True
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            test_case=self, feature_1816=feature_1816, feature_index_1816=feature_index_1816,
            rcv_pre_pairing_slot=rcv_prepairing_slot, ltk_key=ltk_key, irk_local_key=irk_local_key,
            irk_remote_key=irk_remote_key, csrk_local_key=csrk_local_key, csrk_remote_key=csrk_remote_key)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enter pairing mode')
        # ---------------------------------------------------------------------------
        # Todo use current host instead of forcing to 1
        # force host to 1 to have the same behaviour on keyboards and on mice
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Wait for device to be connected')
        # ---------------------------------------------------------------------------
        new_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                                           port_index=ChannelUtils.get_port_index(test_case=self),
                                           device_index=rcv_prepairing_slot))
        ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self, channel=new_channel)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=new_channel)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Verify an HID report can be received')
        # ---------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.memory_manager.read_nvs(backup=False)
    # end def _prerequisite_for_prepairing
# end class AdvertisingPairingModeUsedPrepairingDataTestCase


class AdvertisingPairingModeUnusedPrepairingDataTestCase(AdvertisingPairingModeTestCase):
    """
    BLE advertising Test Cases common class for pairing mode with used prepairing data present
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.device_prepairing_ble_address = None

        super().setUp()
    # end def setUp

    def _prerequisite_for_prepairing(self):
        # See ``AdvertisingPairingModeTestCase._prerequisite_for_prepairing``
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Add prepairing information in the device')
        # ---------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Cleanup all pairing slots in the receiver except the first one')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(test_case=self)

        feature_index_1816, feature_1816, ltk_key, irk_remote_key, irk_local_key, csrk_remote_key, csrk_local_key = \
            BleProPrePairingTestUtils.get_1816_and_generate_keys_prepairing(test_case=self)

        # The receiver address should be the one of the central of the BLE context to be able to catch the prepairing
        # directed advertising from the device
        receiver_address = HexList(BleProtocolTestUtils.get_ble_context_central_address(test_case=self).address)
        # The address in the interface is in big endian while in the prepairing sequence it is in little endian, so we
        # need to reverse the one gotten from the interface
        receiver_address.reverse()

        DeviceTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True,
                                                      device_index=self.original_device_index)

        device_prepairing_ble_address = BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=feature_1816, pre_pairing_index=feature_index_1816,
            long_term_key=ltk_key, remote_identity_resolving_key=irk_remote_key,
            local_identity_resolving_key=irk_local_key, remote_connection_signature_resolving_key=csrk_remote_key,
            local_connection_signature_resolving_key=csrk_local_key, receiver_address=receiver_address)

        # Same reason as previously, we need to inverse endianness to match with the interface big endian format
        device_prepairing_ble_address.reverse()
        self.device_prepairing_ble_address = BleGapAddress(address_type=LogitechBleConstants.ADDRESS_TYPE,
                                                           address=str(device_prepairing_ble_address))
    # end def _prerequisite_for_prepairing
# end class AdvertisingPairingModeUnusedPrepairingDataTestCase


class AdvertisingApplicationReconnectionModeTestCase(AdvertisingTestCase):
    """
    BLE advertising Test Cases common class for application reconnection mode
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.time_lost_user_action = 0

        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disconnect from device")
        # ------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ChannelUtils.disconnect_ble_channel(test_case=self)
        # Add a small delay to let the device realize the disconnection and enter deep sleep
        sleep(.1)
    # end def setUp

    def trigger(self):
        # see ``AdvertisingTestCase.trigger``
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a user action to wake up the device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
    # end def trigger
# end class AdvertisingApplicationReconnectionModeTestCase


class AdvertisingBootloaderReconnectionModeTestCase(AdvertisingTestCase):
    """
    BLE advertising Test Cases common class for bootloader reconnection mode
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_restart_in_main_application = False

        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_restart_in_main_application:
                # ---------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Restart in Main Application mode")
                # ---------------------------------------------------------------------------
                self.debugger.set_application_bit()
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=self, ble_service_changed_required=True)
                self.post_requisite_restart_in_main_application = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def trigger(self):
        # see ``AdvertisingTestCase.trigger``
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Put device in bootloader")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=False)
        self.post_requisite_restart_in_main_application = True
        self.debugger.stop()
        ChannelUtils.wait_usb_ble_channel_connection_state(
            test_case=self, channel=self.current_channel, connection_state=False)
        self.debugger.run()
    # end def trigger
# end class AdvertisingBootloaderReconnectionModeTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
