#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytransport.ble.bleadvertisingparser
:brief: Parser for advertising data
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/11/28
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import itertools
from enum import IntEnum

import math
import numpy as np
from matplotlib import pyplot as plt

from pychannel.logiconstants import BleAdvertisingInterval
from pychannel.logiconstants import BleAdvertisingSeries
from pychannel.logiconstants import BleAdvertisingSeriesStartTimeCategory
from pychannel.logiconstants import BleAdvertisingSeriesWindows
from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
TIME_ASSUMED_ONE_WINDOW = int(100 * TIMESTAMP_UNIT_DIVIDER_MAP['ms'])
THRESHOLD_LEVEL = 0.80
SIZE_ZONE_OF_INTEREST_LEFT = 12
SIZE_ZONE_OF_INTEREST_RIGHT = 6
CROSSING_STABILITY_LENGTH = 10
STABILITY_MAX_THRESHOLD = .8 * CROSSING_STABILITY_LENGTH
HIGH_DUTY_CYCLE_VALUE_FOR_PARSING = 3.75
N = 10

# flag to turn on generation of plot, no saving or displaying is done at this level
DEBUG_PLOTS = False


class TimingsTupleIndex(IntEnum):
    """
    Index for tuple of values returned by the method ``build_data``
    """
    SERIES = 0
    START = 1
    STOP = 2
# end class TimingsTupleIndex


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BleAdvertisingParser:
    """
    Parsing functions to treat advertising data
    """

    @staticmethod
    def moving_average(data, n=3):
        """
        Calculate a moving average of a list of data

        :param data: Data to average
        :type data: ``np.ndarray`` or ``iterable``
        :param n: Size of the average window
        :type n: ``int``

        :return: the rolling average, a shape n-1 shorter than the input
        :rtype: ``np.ndarray``
        """
        ret = np.cumsum(data, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n
    # end def moving_average

    @staticmethod
    def split_advertisement_data_in_batches(data, expected_series=None):
        """
        Split advertising data in batches representing received windows. the split is based on their data
        type and advertising interval. Expected series can be set to hint the parser on how to deal with the data

        :param data: Advertising data to split
        :type data: ``list``
        :param expected_series: expected
        :type expected_series: ``list[BleAdvertisingSeries]``

        :return: tuple of four list that correspond the following data related to each batch:
            timestamps
            intervals
            data indexes
            list of discarded timestamps at the end of the batch
        :rtype: ``tuple``
        """
        indexes = np.zeros(len(data), dtype=int)
        indexes_limit = np.array([len(x) for x in data])
        batches_timestamps = []
        batches_intervals = []
        batches_data_id = []
        batches_discarded = []
        if expected_series is None:
            expected_series = [series for series in BleAdvertisingSeries]
        # end if
        possible_transition = BleAdvertisingParser.get_possible_transition_in_series_set(expected_series)
        last_timestamp_appended = None

        def append_batch(_start, _stop, _current_data_id, _last_timestamp_appended):
            """
            Add a batch separated by data to the list. If the batch is sufficiently long it will be checked for
             interval time transition
            Internal helper function

            :param _start: start index of the slice
            :type _start: ``int``
            :param _stop: stop index of the slice
            :type _stop: ``int``
            :param _last_timestamp_appended: timestamp of the last value added to the lists, used to calculate first
                interval of a new batch - Optional
            :type _last_timestamp_appended: ``int`` or ``None``
            :param _current_data_id: current index of the data considered - Optional
            :type _current_data_id: ``int`` or None

            :return: last timestamp appended to the lists
            :rtype: ``int``
            """
            data_slice = np.array(data[_current_data_id][_start:_stop])

            last_timestamp = data_slice[-1]
            while len(data_slice) > 0:
                intervals_of_slice = np.ediff1d(data_slice)

                if _last_timestamp_appended is not None:
                    intervals = np.append([data_slice[0] - _last_timestamp_appended], intervals_of_slice)
                else:
                    intervals = intervals_of_slice
                # end if

                if last_timestamp - data_slice[0] < TIME_ASSUMED_ONE_WINDOW:
                    batches_timestamps.append(data_slice)
                    batches_intervals.append(intervals)
                    batches_data_id.append(_current_data_id)
                    batches_discarded.append([])
                    return last_timestamp
                # end if
                data_slice = split_batch(intervals, data_slice, _current_data_id)

            # end while
            return last_timestamp
        # end def append_batch

        def split_batch(intervals, timestamps, _current_data_id):
            """
            split a single batch in two based on the most likely initial transition happening in the interval times
            Internal helper function

            :param timestamps: list of timestamps to consider
            :type timestamps: ``list[int]``
            :param intervals: intervals to consider
            :type intervals: ``np.ndarray``
            :param _current_data_id: current index of the data considered
            :type _current_data_id: ``int``

            :return: data after the split
            :rtype: ``list``
            """
            moving_averaged = BleAdvertisingParser.moving_average(intervals, N)
            ax = None
            splits = []
            splits_crossing = []

            if DEBUG_PLOTS:
                fig, ax = BleAdvertisingPlotter.make_figure("split_batch Debug plot",
                                                            shape=(len(possible_transition), 1))
                moving_averaged_ms = moving_averaged / TIMESTAMP_UNIT_DIVIDER_MAP["ms"]
                for i, transition in enumerate(possible_transition):
                    intervals_number = BleAdvertisingPlotter.plot_advertising_intervals(
                        intervals, axis=ax[i], title=f"possible transition {transition}")
                    ax[i].step(intervals_number[N-1:], moving_averaged_ms)
                # end for
            # end if
            for i_transition, transition in enumerate(possible_transition):
                decoded = [t if t != BleAdvertisingInterval.HIGH_DUTY_CYCLE else HIGH_DUTY_CYCLE_VALUE_FOR_PARSING
                           for t in transition]

                initial = decoded[0] * TIMESTAMP_UNIT_DIVIDER_MAP['ms']
                final = decoded[1] * TIMESTAMP_UNIT_DIVIDER_MAP['ms']
                order_of_transition = initial < final
                threshold_level = THRESHOLD_LEVEL if order_of_transition else 1 - THRESHOLD_LEVEL

                # for some cases the threshold level need to be changed
                if transition[0] == BleAdvertisingInterval.HIGH_DUTY_CYCLE:
                    threshold_level = 0.50
                elif transition[1] == BleAdvertisingInterval.HIGH_DUTY_CYCLE:
                    threshold_level = 0.75
                # end if

                threshold = (abs(final-initial) * threshold_level) + min(initial, final)

                averaged_threshold = np.array(moving_averaged > threshold)
                threshold_crossings = np.diff(averaged_threshold)
                threshold_crossing_indexes = np.argwhere(threshold_crossings)[:, 0]

                while len(threshold_crossing_indexes) > 0:
                    analyzed_crossing = threshold_crossing_indexes[0]
                    # is crossing in the right direction
                    if averaged_threshold[analyzed_crossing] == order_of_transition:
                        # wrong direction, discard crossing
                        threshold_crossing_indexes = np.delete(threshold_crossing_indexes, 0)
                        continue
                    # end if
                    # Test whether crossing is long enough
                    stability_zone = averaged_threshold[analyzed_crossing+1:
                                                        analyzed_crossing+1+CROSSING_STABILITY_LENGTH]
                    stability_count = np.count_nonzero(stability_zone == order_of_transition)
                    number_after_crossing = len(moving_averaged) - 1 - analyzed_crossing
                    if stability_count >= min(STABILITY_MAX_THRESHOLD, float(number_after_crossing)):
                        break
                    # end if
                    threshold_crossing_indexes = np.delete(threshold_crossing_indexes, 0)
                # end while

                threshold_crossing_indexes_back_to_initial = threshold_crossing_indexes + N - 1

                if DEBUG_PLOTS:
                    ax[i_transition].axhline(threshold / TIMESTAMP_UNIT_DIVIDER_MAP["ms"], c='r')
                # end if

                if len(threshold_crossing_indexes) == 0:
                    # no crossing for this value
                    continue
                # end if
                crossing_index = int(threshold_crossing_indexes_back_to_initial[0])

                if DEBUG_PLOTS:
                    ax[i_transition].axvline(crossing_index, c='r')
                # end if

                start_interest = max(crossing_index - SIZE_ZONE_OF_INTEREST_LEFT, 0)
                zone_of_interest = intervals[start_interest:crossing_index+SIZE_ZONE_OF_INTEREST_RIGHT]

                divided_initial = zone_of_interest / initial
                divided_final = zone_of_interest / final
                round_initial = np.round(divided_initial)
                round_final = np.round(divided_final)
                closeness_initial = np.abs(divided_initial - round_initial)
                closeness_final = np.abs(divided_final - round_final)

                closer_initial = closeness_initial < closeness_final
                delta_closeness = np.abs(closeness_initial-closeness_final)
                too_close_closeness = delta_closeness < 0.2

                too_far = np.logical_and(closer_initial > 0.5, closeness_final > 0.5)
                # a value much bellow both expected at transition is an outlier generated
                # by the firmware that we can't deal with
                too_low = np.logical_and(round_initial == 0, round_final == 0)
                # if above the value of both at transition can lead to wrong classification
                too_big = np.logical_and(round_initial >= 2, round_final >= 2)
                ambiguous = np.logical_or(too_close_closeness,
                                          np.logical_or(too_far, np.logical_or(too_low, too_big)))

                # for each value that are continuously in the rough size of the biggest value at the start
                continuous_sure_end = 0
                continuous_sure_start = 0
                if order_of_transition:
                    threshold = round(final/initial)
                    override_thresholded = np.array(divided_initial < threshold)
                    for val in override_thresholded:
                        if not val:
                            continuous_sure_start += 1
                        else:
                            break
                        # end if
                    # end for

                    for val in reversed(override_thresholded):
                        if val:
                            continuous_sure_end += 1
                        else:
                            break
                        # end if
                    # end for
                else:
                    threshold = round(initial/final)
                    override_thesholded = np.array(divided_final > threshold)
                    for val in override_thesholded:
                        if val:
                            continuous_sure_start += 1
                        else:
                            break
                        # end if
                    # end for
                    for val in reversed(override_thesholded):
                        if not val:
                            continuous_sure_end += 1
                        else:
                            break
                        # end if
                    # end for
                # end if
                mask_override = np.pad(np.repeat(True, len(zone_of_interest) - continuous_sure_end),
                                       (0, continuous_sure_end), constant_values=False)
                closer_initial_override_masked_end = np.logical_and(closer_initial, mask_override)

                mask_override = np.pad(np.repeat(True, continuous_sure_start),
                                       (0, len(zone_of_interest) - continuous_sure_start), constant_values=False)

                closer_initial_override_masked = np.logical_or(closer_initial_override_masked_end, mask_override)

                closer_initial_masked = np.logical_xor(closer_initial_override_masked, ambiguous)

                index_crossing = np.argwhere(np.diff(closer_initial_masked))[:, 0]
                index_where_closer = index_crossing[np.where(closer_initial_masked[index_crossing])]
                index_where_further = index_crossing[
                    np.where(np.logical_not(closer_initial_masked[index_crossing]))]
                index_where_ambiguous = np.argwhere(np.diff(ambiguous))[:, 0]

                # protect index errors when never ambiguous
                if len(index_where_ambiguous) > 0:
                    last_before_ambiguous = index_where_ambiguous[0] - 1
                    last_ambiguous = index_where_ambiguous[-1] + 1
                else:
                    last_before_ambiguous = math.inf
                    last_ambiguous = -math.inf
                # end if
                # if it is true closer at start of the window
                if len(index_where_closer) == 0 or len(index_crossing) == 0:
                    low = 0
                elif index_crossing[0] == index_where_closer[0]:
                    low = min(int(index_where_closer[0]), last_before_ambiguous)
                else:
                    low = 0
                # end if
                if len(index_where_closer) > 0:
                    last_closer_plus_1 = index_where_closer[-1] + 1
                else:
                    last_closer_plus_1 = -math.inf
                # end if
                if len(index_where_further) == 0 or len(index_crossing) == 0:
                    high = max(low + 1, last_closer_plus_1, last_ambiguous)
                elif index_crossing[-1] == index_where_further[-1]:
                    high = SIZE_ZONE_OF_INTEREST_LEFT+SIZE_ZONE_OF_INTEREST_RIGHT
                else:
                    high = max(low + 1, last_closer_plus_1, last_ambiguous)
                # end if

                if round_initial[low] > 3:
                    low -= 1
                # end if

                split_at_low = start_interest + low
                split_at_high = start_interest + high

                if DEBUG_PLOTS:
                    fig_zone, ax_zone = BleAdvertisingPlotter.make_figure(
                        f"Zoom Zone of interest Debug Plot {transition} {crossing_index}", (6, 1), sharey="none")
                    zone_numbers = BleAdvertisingPlotter.plot_advertising_intervals(zone_of_interest, ax_zone[0],
                                                                                    "interest")
                    ax_zone[1].set_title("closeness values")
                    ax_zone[1].step(zone_numbers, closeness_initial, label="closeness_initial", where='mid')
                    ax_zone[1].step(zone_numbers, closeness_final, label="closeness_final", where='mid')

                    ax_zone[2].step(zone_numbers, closer_initial, where='mid', label="closer_initial")
                    ax_zone[3].step(zone_numbers, too_close_closeness, where='mid', label="too_close_closeness")
                    ax_zone[3].step(zone_numbers, too_far, where='mid', label="too_far")
                    ax_zone[3].step(zone_numbers, too_low, where='mid', label="too_low")
                    ax_zone[3].step(zone_numbers, too_big, where='mid', label="too_big")
                    ax_zone[3].legend()
                    ax_zone[4].step(zone_numbers, mask_override, where='mid', label="mask_override")
                    ax_zone[5].step(zone_numbers, closer_initial_masked, where='mid', label="closer_initial_masked")

                    ax_zone[0].axvline(low, c='g')
                    ax_zone[0].axvline(high, c='r', linestyle="dotted")

                    for a in ax_zone:
                        a.legend()
                    # end for
                # end if
                splits.append((split_at_low, split_at_high))
                splits_crossing.append(crossing_index)
                # end if
            # end for

            if len(splits) == 0:
                batches_timestamps.append(timestamps)
                batches_intervals.append(intervals)
                batches_data_id.append(_current_data_id)
                batches_discarded.append(np.array([]))
                return []
            else:

                index_best_guess_split = np.argmin(splits_crossing)

                (low, high) = splits[index_best_guess_split]
                batches_timestamps.append(timestamps[0:low + 2])
                batches_intervals.append(intervals[0:low + 1])
                batches_data_id.append(_current_data_id)
                batches_discarded.append(timestamps[low+2:high+1])
                start_next_slice = high + 1
                # return the rest of the segment
                return timestamps[start_next_slice:]
            # end if
        # end def split_batch

        if len(data) > 1:
            while np.any(indexes < indexes_limit):
                current_timestamp_of_each_data = np.array([data[i][index] if index < indexes_limit[i] else math.inf
                                                           for i, index in enumerate(indexes)])
                current_data_id = np.argmin(current_timestamp_of_each_data)
                next_timestamp = np.min(np.delete(current_timestamp_of_each_data, current_data_id))

                first_id_after_switch = np.searchsorted(data[current_data_id], next_timestamp)
                current_index = indexes[current_data_id]
                last_timestamp_appended = append_batch(current_index, first_id_after_switch, current_data_id,
                                                       last_timestamp_appended)

                indexes[current_data_id] = first_id_after_switch
            # end while
        else:
            # append whole as a batch, surely to split
            append_batch(0, len(data[0]), 0, last_timestamp_appended)
        # end if
        return batches_timestamps, batches_intervals, batches_data_id, batches_discarded
    # end def split_advertisement_data_in_batches

    @staticmethod
    def get_possible_transition_in_series_set(series):
        """
        parse a set of series to find the possible
        :param series:
        :type series:
        :return:
        :rtype:
        """
        shared_packets = BleAdvertisingParser.get_packet_shared_data(series)

        possible_transition = set()
        for shared in shared_packets:
            if len(shared) <= 1:
                continue
            # end if
            for a, b in itertools.permutations(shared, r=2):
                if a.value.start <= b.value.start and a.value.interval != b.value.interval:
                    possible_transition.add((a.value.interval, b.value.interval))
                # end if
            # end for
        # end for
        return possible_transition
    # end def get_possible_transition_in_series_set

    @staticmethod
    def get_packet_shared_data(expected_series):
        """
        Return a list of each unique advertising packets for the given series

        :return: list of lists grouping the expected packet together
        :rtype: ``list``
        """
        unique_packet = []
        for series in expected_series:
            found = False
            for entry in unique_packet:
                if entry[0].value.packet == series.value.packet:
                    found = True
                    entry.append(series)
                    break
                # end if
            # end for
            if not found:
                unique_packet.append([series])
            # end if
        # end for
        return unique_packet
    # end def get_packet_shared_data

    @staticmethod
    def get_scan_response_shared_data(expected_series):
        """
        Return a list of each unique scan response packets for the given series

        :return: list of lists grouping the expected packet together
        :rtype: ``list``
        """
        unique_scan_response = []
        for series in expected_series:
            found = False
            for entry in unique_scan_response:
                if entry[0].value.scan_response == series.value.scan_response:
                    found = True
                    entry.append(series)
                    break
                # end if
            # end for
            if not found:
                unique_scan_response.append([series])
            # end if
        # end for
        return unique_scan_response
    # end def get_scan_response_shared_data

    @staticmethod
    def get_next_transition(series, absolute_time):
        """
        get the next transition in the given series for the given time

        :param series: the given series
        :type series: ``BleAdvertisingSeries``
        :param absolute_time: the given time - in seconds
        :type absolute_time: ``int`` or ``float``

        :return: A tuple of the following values:
                - Flag indicating if series would be advertising before the given transition
                - time of the next transition in seconds
                - the given series this transition is linked to
        :rtype: ``tuple[bool, float, BleAdvertisingSeries]``
        """

        series_val = series.value
        if absolute_time < series_val.start.value:
            return False, series_val.start.value, series
        elif absolute_time >= series_val.stop.value:
            return False, None, series
        elif series_val.window == BleAdvertisingSeriesWindows.WHOLE_PERIOD:
            return True, series_val.stop.value, series
        # end if

        relative_time = absolute_time - series_val.start.value
        window = series_val.window.value[0]
        duration = series_val.window.value[1]

        # use math.floor instead of // as the floor division gives inconsistant results
        # with 18.84 // 6.28 = 2.0 and not 3 as expected
        iteration = math.floor(relative_time / duration)
        active_iteration_end = series_val.start.value + window + iteration * duration
        if absolute_time < active_iteration_end:
            # active until the end of active period iteration
            return True, min(active_iteration_end, series_val.stop.value), series
        else:
            next_iteration = series_val.start.value + duration * (iteration + 1)
            if next_iteration == absolute_time:
                next_iteration = series_val.start.value + duration * (iteration + 2)
            # end if
            # inactive until the start of next iteration
            return False, min(next_iteration, series_val.stop.value), series
        # end if
    # end def get_next_transition

    @staticmethod
    def get_expected_series_timing(expected_series):
        """
        build a set of each expected transition timing for a set of expected series in reverse order of priority

        :param expected_series: The series the DUT will send, if none specified,
            use the first series of the pairing advertising of the current DUT
        :type expected_series: tuple(``BleAdvertisingSeriesDefinition``)

        :return: list of all transitions from one window to another
        :rtype: ``list``
        """

        priority_dict = {series: i for i, series in enumerate(expected_series)}
        current_state = [e.value.start == BleAdvertisingSeriesStartTimeCategory.START for e in expected_series]

        next_transitions = [BleAdvertisingParser.get_next_transition(series, 0) for series in expected_series]
        start_time = 0
        transitions = []

        while len(next_transitions) > 0:
            next_transitions.sort(key=lambda transition: transition[1])

            (transition_state, next_time, series) = next_transitions[0]
            indexes_to_recaculate = []
            for i_transitions in next_transitions:
                (i_transition_state, i_next_time, i_series) = i_transitions
                index = priority_dict[i_series]
                if i_next_time == next_time:
                    indexes_to_recaculate.append(index)
                # end if
                current_state[index] = i_transition_state
            # end for
            for i, state in reversed(list(enumerate(current_state))):
                if state:
                    transitions.append((expected_series[i], start_time, next_time))
                    break
                # end if
            # end for
            start_time = next_time
            # generate the next transitions
            del_count = 0
            for i, index in enumerate(indexes_to_recaculate):
                new_transition = BleAdvertisingParser.get_next_transition(expected_series[index], next_time)

                if new_transition[1] is not None:
                    next_transitions[i-del_count] = new_transition
                else:
                    current_state[index] = False
                    next_transitions.pop(0)  # remove this series, it is over
                    del_count += 1
                # end if
            # end for
        # end while
        return transitions  # end def get_expected_series_timing
    # end def get_expected_series_timing

    @staticmethod
    def concatenate_timestamps(advertising_data_timestamps):
        """
        Concatenate advertising data timestamps into a singular list of timestamps
        :param advertising_data_timestamps: advertising data timestamps
        :type advertising_data_timestamps: ``list``
        :return:  the concatenated list
        :rtype: ``list``
        """
        timestamps = np.array([])
        for i, adv_data in enumerate(advertising_data_timestamps):
            timestamps = np.append(timestamps, np.array([adv_data]))
        # end for
        timestamps.sort()
        return timestamps
    # end def concatenate_timestamps

    @staticmethod
    def get_all_advertising_timestamps(context_device):
        """
        Extract all the timestamps of advertising in a ble context device into a format compatible with the parser

        :param context_device: the device
        :type context_device: ``BleContextDevice``

        :return: list of lists of timestamps
        :rtype:  ``list[list[int]]``
        """
        result = []
        for data in context_device.advertising_data:
            result.append(data.get_timestamps())
        # end for
        return result
    # end def get_all_advertising_timestamps
# end class BleAdvertisingParser


class BleAdvertisingPlotter:
    """
    Methods to plot advertising data
    """
    @staticmethod
    def make_figure(title, shape=(1, 1), sharey="all"):
        """
        Create a standardized figure
        :param title: title of the figure to create
        :type title: ``str``
        :param shape: number of subplots in row and column
        :type shape: ``tuple[int, int]``
        :param sharey: sharey axis parameter, see matplotlib ``plt.subplots`` args for details - Optional
        :type sharey: ``Union[Literal["none", "all", "row", "col"]]``

        :return: figure and list of axis for each subplot
        :rtype: ``tuple``
        """
        fig, ax = plt.subplots(shape[0], shape[1], sharex="all", sharey=sharey)
        fig.set_figheight(10)
        fig.set_figwidth(35)
        fig.set_dpi(200)
        fig.suptitle(title)
        if shape == (1, 1):
            ax = [ax]
        # end if
        return fig, ax

    # end def make_figure

    @staticmethod
    def plot_advertising_data_into_timestamp_diagram(timestamps, axis, title=None, zero_point=0):
        """
        Add advertising data to a diagram of timestamp dot at each reception, x-axis is time, y-axis is data source
        :param timestamps: advertising timestamps indexed by data source
        :type timestamps: ``list``
        :param axis: axis of the subplot to add the data too
        :type axis: ``plt.Axes``
        :param title: Title of the subplot - OPTIONAL
        :type title: ``str`` or ``None``
        :param zero_point: Timestamp to use as zero point - OPTIONAL
        :type zero_point: ``int``
        """
        axis.grid(True, axis='both')
        axis.set_ylabel('Data source')
        axis.set_xlabel('Time')
        axis.set_yticks(np.arange(len(timestamps)))
        if title is not None:
            axis.set_title(title)
        # end if
        for i, data in enumerate(timestamps):
            data_in_seconds = (np.array(data) - zero_point)/TIMESTAMP_UNIT_DIVIDER_MAP["s"]
            BleAdvertisingPlotter.plot_advertising_add_timestamps_to_axis(data_in_seconds, val=i, axis=axis)
        # end for

        time_ticks = np.arange(start=0, stop=200, step=5)
        minor_ticks = np.arange(start=0, stop=200, step=1)
        axis.set_xticks(time_ticks)
        axis.set_xticks(minor_ticks, minor=True)
        axis.grid(True, axis='both', which='both')
    # end def plot_advertising_data_into_timestamp_diagram

    @staticmethod
    def plot_advertising_add_timestamps_to_axis(timestamps, val, axis):
        """
        add the timestamps to a subplot  one dot for each timestamp at the y value ``val``
        :param timestamps: list of timestamps
        :type timestamps: ``list``
        :param val: value of y-axis to use
        :type val: ``int``
        :param axis: axis of the subplot to add the data too
        :type axis: `plt.Axes``
        """
        x_val = np.full(len(timestamps), val)
        axis.scatter(timestamps, x_val)
    # end def plot_advertising_add_timestamps_to_axis

    @staticmethod
    def plot_add_batch_timestamps(batches_timestamps, batches_indexes, axis, title, zero_point=0):
        """
        Add advertising data to a diagram of timestamp dot at each reception, x-axis is time, y-axis is data source
        displaying the different batches.

        :param batches_timestamps: list of batches of timestamps
        :type batches_timestamps: ``np.ndarray``
        :param batches_indexes: list of data source indexes for each batch
        :type batches_indexes: ``np.ndarray``
        :param axis: axis of the subplot to add the data too
        :type axis: `plt.Axes``
        :param title: Title of the subplot - OPTIONAL
        :type title: ``str`` or ``None``
        :param zero_point: Timestamp to use as zero point - OPTIONAL
        :type zero_point: ``int``
        """
        axis.grid(True, axis='both')
        axis.set_ylabel('Data source')
        axis.set_xlabel('Time')
        if title is not None:
            axis.set_title(title)
        # end if
        for batches_timestamps, batches_index in zip(batches_timestamps, batches_indexes):
            timestamps = (batches_timestamps - zero_point) / TIMESTAMP_UNIT_DIVIDER_MAP["s"]
            BleAdvertisingPlotter.plot_advertising_add_timestamps_to_axis(timestamps, batches_index, axis)
        # end for
    # end def plot_add_batch_timestamps

    @staticmethod
    def plot_advertising_intervals(intervals, axis, title=None):
        """
        Plot intervals in a step plot

        :param intervals: Intervals to plot
        :type intervals: ``np.ndarray``
        :param axis: axis of the subplot to add the data too
        :type axis: `plt.Axes``
        :param title: Title of the subplot to optionally add. - Optional
        :type title: ``str`` or ``None``

        :return: list of interval numbers of the x-axis to add to the subplot
        :rtype: ``np.ndarray``
        """
        intervals_numbers = np.arange(len(intervals))

        axis.step(intervals_numbers, intervals / TIMESTAMP_UNIT_DIVIDER_MAP["ms"], 'x:', where='mid')
        axis.margins(x=0)
        axis.set_ylabel('Time [ms]')
        axis.set_xlabel('Interval number')
        axis.grid(True, axis='y')
        if title is not None:
            axis.set_title(title)
        # end if
        return intervals_numbers
    # end def plot_advertising_intervals

    @staticmethod
    def plot_add_ticks_at_intervals(series_set, axis):
        """
        create tick line at expected values for interval for a given set of series, and their multiple

        :param series_set: list of series definition to use
        :type series_set: ``list[BleAdvertisingSeries]``
        :param axis: axis of the subplot to change the ticks of
        :type axis: `plt.Axes``
        """
        intervals_bases = set()
        for s in series_set:
            intervals_bases.add(s.value.interval if s.value.interval > BleAdvertisingInterval.HIGH_DUTY_CYCLE else 1)
        # end for
        multiples = np.arange(8)
        a = np.array([multiples * intervals_base for intervals_base in intervals_bases])
        ticks = np.sort(np.unique(a.flatten()))
        axis.set_yticks(ticks=ticks)
    # end def plot_add_ticks_at_intervals

    @staticmethod
    def plot_add_batch_intervals(batches_intervals, intervals_numbers, axis, title=None):
        """
        Plot intervals in a step plot, for a batches of interval

        :param batches_intervals: list of lists of intervals
        :type batches_intervals: ``np.ndarray``
        :param intervals_numbers: list of interval numbers of the x-axis to add to the subplot
        :type intervals_numbers: ``np.ndarray``
        :param axis: axis of the subplot to add the data too
        :type axis: `plt.Axes``
        :param title: Title of the subplot to optionally add. - Optional
        :type title: ``str`` or ``None``
        """
        current_number = 0
        axis.grid(True, axis='y')
        axis.set_ylabel('Time [ms]')
        axis.set_xlabel('Interval number')
        if title is not None:
            axis.set_title(title)
        # end if
        for batch_intervals in batches_intervals:
            axis.step(intervals_numbers[current_number:current_number + len(batch_intervals)],
                      batch_intervals / TIMESTAMP_UNIT_DIVIDER_MAP["ms"], 'x:', where='mid')
            current_number += len(batch_intervals)
        # end for
    # end def plot_add_batch_intervals
# end class BleAdvertisingPlotter

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
