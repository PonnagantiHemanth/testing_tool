#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytransport.ble.test.bleadvertisingparsertest
:brief: Validates function of Ble Advertising Parser
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/11/28
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import random

import math
import matplotlib.pyplot as plt
import numpy as np

from pychannel.logiconstants import BleAdvertisingInterval
from pychannel.logiconstants import BleAdvertisingSeries
from pyharness.core import TestCase
from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP
from pytransport.ble.bleadvertisingparser import BleAdvertisingParser
from pytransport.ble.bleadvertisingparser import BleAdvertisingPlotter
from pytransport.ble.bleadvertisingparser import TimingsTupleIndex

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
SEED_RANGE = 42
EXPECTED_SERIES_SET_TO_CHECK = [
    [BleAdvertisingSeries.A, BleAdvertisingSeries.B, BleAdvertisingSeries.C],
    [BleAdvertisingSeries.A, BleAdvertisingSeries.B, BleAdvertisingSeries.C, BleAdvertisingSeries.D],
    [BleAdvertisingSeries.E, BleAdvertisingSeries.F],
    [BleAdvertisingSeries.E, BleAdvertisingSeries.F, BleAdvertisingSeries.D],
    [BleAdvertisingSeries.I, BleAdvertisingSeries.J, BleAdvertisingSeries.K],
]


MAKE_GRAPHS = False


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PacketDrop:
    """
    Generator of packet drop simulating a clumping of missing data, by increasing probability a packet is lost based on
    if previous was lost, in a quadratic curve
    """
    def __init__(self, peak_proba=0.5, peak_number=4, proba_at_start=0.05):
        """
        :param peak_proba: peak of probability of a given packet will be lost - OPTIONAL
        :type peak_proba: ``float``
        :param peak_number: number of consecutive missing packets where the peak probability happens - OPTIONAL
        :type peak_number: ``int``
        :param proba_at_start: probability the initial packet is lost - OPTIONAL
        :type proba_at_start: ``float``
        """
        self.peak_proba = peak_proba
        self.peak_number = peak_number
        self.proba_at_start = proba_at_start
        self.a = -(self.proba_at_start - self.peak_proba) / (self.peak_number ** 2)
        self.consecutive_drop = 0
    # end def __init__

    def proba(self):
        """
        calculate the probability for the current number of consecutive drop
        :return: probability
        :rtype: ``float``
        """
        return -self.a * (self.consecutive_drop - self.peak_number) ** 2 + self.peak_proba
    # end def proba

    def is_next_dropped(self):
        """
        return if the packet should be dropped based on previous results
        :return: flag indicating dropped packet
        :rtype: ``bool``
        """
        dropped = random.uniform(0, 1) < self.proba()

        if dropped:
            self.consecutive_drop += 1
        else:
            self.consecutive_drop = 0
        # end if
        return dropped
    # end def is_next_dropped
# end class PacketDrop


class BleAdvertisingParserTestCase(TestCase):
    """
    Validates BleAdvertisingParser
    """

    def setUp(self):
        """
        Handle test prerequisite
        """
        self.data_to_check = []
    # end def setUp

    @staticmethod
    def build_data(seed, series, packet_drop=PacketDrop(), max_time=math.inf, start_time=0, jitter=0,
                   window_jitter=(0, 0), fix_error_interval=1., adv_delay=True):
        """
        Simulate the results of a scan of a logitech device advertising based on a set of rules

        :param seed: seed to feed the random number generator
        :type seed: ``int``
        :param series: set if series to use to generate, higher index in the list means higher priority
        :type series: ``List[BleAdvertisingSeries]``
        :param packet_drop: distribution for packed drop generation to use - Optional
        :type packet_drop: ``PacketDrop``
        :param max_time: Maximum time to simulate advertising in nanoseconds - Optional
        :type max_time: ``int``
        :param start_time: Time to start the simulation of advertising at in nanoseconds - Optional
        :type start_time: ``int``
        :param jitter: random jitter to add to each packets in nanoseconds - Optional
        :type jitter: ``int``
        :param window_jitter: jitter of the window timing in nanoseconds, tuple of min and max applied - Optional
        :type window_jitter: ``tuple[int, int]``
        :param fix_error_interval: Fix relative error each interval has,
            value multiplied to the nominal interval value - Optional
        :type fix_error_interval: ``float``
        :param adv_delay: Flag to enable simulating interval delay of bluetooth specification - Optional
        :type adv_delay: ``bool``

        :return: a tuple of the advertising data, in the format of ``BleAdvertisingData`` internal structure
            and information about where advertising data changes from one series to another, which is a tuple of index
            of the data, the corresponding index in the list for that data and the series.
        :rtype: ``tuple``
        """
        random.seed(seed)

        transitions_index = []

        unique_packets = BleAdvertisingParser.get_packet_shared_data(series)
        packet_dict = dict()
        for i, series_set in enumerate(unique_packets):
            for series_name in series_set:
                packet_dict[series_name] = i
            # end for
        # end for
        adv_data_timestamps = [[] for _ in range(len(unique_packets))]
        timings = BleAdvertisingParser.get_expected_series_timing(series)
        current_time = start_time
        latest_index = None
        started = False
        while len(timings) > 0:
            current = timings[0]
            start = current[TimingsTupleIndex.START] * TIMESTAMP_UNIT_DIVIDER_MAP["s"]
            stop = current[TimingsTupleIndex.STOP] * TIMESTAMP_UNIT_DIVIDER_MAP["s"]
            current_series = current[TimingsTupleIndex.SERIES]
            if not current_series.value.interval == BleAdvertisingInterval.HIGH_DUTY_CYCLE:
                nominal_interval = current_series.value.interval.value
                high_duty_cycle = False
            else:
                nominal_interval = 3.75
                high_duty_cycle = True
            # end if
            interval = nominal_interval * fix_error_interval * TIMESTAMP_UNIT_DIVIDER_MAP["ms"]

            if current_time < start and not started: # only wait for the first series
                current_time = start
                continue
            else:
                started = True
            # end if

            if current_time <= stop + random.randint(window_jitter[0], window_jitter[1]):

                index = packet_dict[current_series]
                delay = random.uniform(0, 10*TIMESTAMP_UNIT_DIVIDER_MAP["ms"]) if adv_delay and not high_duty_cycle else 0
                current_time += interval + random.uniform(-jitter, jitter) + delay
                if not packet_drop.is_next_dropped():  # if not dropped
                    adv_data_timestamps[index].append(current_time)
                # end if
                latest_index = (index, len(adv_data_timestamps[index]) - 1, current_series)
            else:
                timings.pop(0)
                if latest_index is not None:
                    transitions_index.append(latest_index)
                # end if
            # end if

            if current_time >= max_time:
                if latest_index is not None:
                    transitions_index.append(latest_index)
                # end if
                break
            # end if
        # end while
        return adv_data_timestamps, transitions_index
    # end def build_data

    def _common_test_set_of_data(self, filter_expected_series=False):
        """
        Helper function to test a set of data to be parsed
        :param filter_expected_series: Flag indicating if the expected series is given to the parser - Optional
        :type filter_expected_series: ``bool``
        """

        for (seed, series_set, data_timestamps, transition_indexes) in self.data_to_check:
            title = f"Data for series {', '.join([s.name for s in series_set])} seed={seed}"

            ax_interval = None
            ax_timestamps = None
            intervals_numbers = None
            if MAKE_GRAPHS:
                _, ax_timestamps = BleAdvertisingPlotter.make_figure(title, shape=(2, 1))
                BleAdvertisingPlotter.plot_advertising_data_into_timestamp_diagram(data_timestamps, ax_timestamps[0],
                                                                                   title="raw advertising data")
                concatenated_timestamps = BleAdvertisingParser.concatenate_timestamps(
                    advertising_data_timestamps=data_timestamps)
                concatenated_interval = np.ediff1d(concatenated_timestamps)
                _, ax_interval, = BleAdvertisingPlotter.make_figure(title, shape=(2, 1))
                intervals_numbers = BleAdvertisingPlotter.plot_advertising_intervals(concatenated_interval,
                                                                                     ax_interval[0],
                                                                                     "Advertising intervals")
            # end if

            batches_timestamps, batches_intervals, batches_data_id, batches_discarded = \
                BleAdvertisingParser.split_advertisement_data_in_batches(data_timestamps,
                                                                         series_set if filter_expected_series else None)

            i_of_transitions = 0
            length_of_each_data = [0 for _ in range(len(data_timestamps))]
            if MAKE_GRAPHS:
                BleAdvertisingPlotter.plot_add_batch_timestamps(batches_timestamps, batches_data_id, ax_timestamps[1],
                                                                "Data split in batches")

                BleAdvertisingPlotter.plot_add_ticks_at_intervals(series_set, ax_interval[1])
                BleAdvertisingPlotter.plot_add_batch_intervals(batches_intervals, intervals_numbers, ax_interval[1],
                                                               "Data split in batches")
                plt.show()
            # end if
            for i_batch, (batch_data_id, batch_timestamps, batch_intervals, batch_discarded) in enumerate(
                    zip(batches_data_id, batches_timestamps, batches_intervals, batches_discarded)):

                self.assertLessEqual(i_of_transitions, len(transition_indexes),
                                     f"Too many transitions found for {title}")

                index_of_packet, index_of_data, series = transition_indexes[i_of_transitions]


                self.assertEqual(expected=index_of_packet, obtained=batch_data_id,
                                 msg=f"not matching id filtered {batch_data_id}!= data construction {index_of_packet}"
                                     f"for {title}"
                                     f"(last timestamp of batch={batch_timestamps[-1]} "
                                     f"[{batch_timestamps[-1] / TIMESTAMP_UNIT_DIVIDER_MAP['s']}])")

                length_of_each_data[batch_data_id] += len(batch_timestamps)
                index_from_batch = length_of_each_data[batch_data_id] - 1

                if len(batch_discarded) == 0:
                    self.assertEqual(expected=index_of_data, obtained=index_from_batch,
                                     msg=f"Transition detected at the wrong index {index_from_batch},"
                                         f"construction expects {index_of_data} "
                                         f"when no data discarded for {title}"
                                         f"(last timestamp of batch={batch_timestamps[-1]} "
                                         f"[{batch_timestamps[-1]/TIMESTAMP_UNIT_DIVIDER_MAP['s']}]")
                else:
                    if i_batch+1 < len(batch_timestamps):
                        next_batch_timestamps = batches_timestamps[i_batch + 1]
                    else:
                        next_batch_timestamps = []
                    # end if
                    intersect = np.intersect1d(next_batch_timestamps, batch_discarded)
                    len_before = len(batch_discarded)-len(intersect)

                    self.assertGreaterEqual(a=index_from_batch, b=index_of_data - len_before,
                                            msg=f"Transition detected at index too early {index_from_batch}"
                                                f"construction expects {index_of_data} "
                                                f"And {len(batch_discarded)} timestamps where discarded"
                                                f" for {title}"
                                                f"(last timestamp of batch={batch_timestamps[-1]} "
                                                f"[{batch_timestamps[-1] / TIMESTAMP_UNIT_DIVIDER_MAP['s']}]")
                    self.assertLessEqual(a=index_from_batch, b=index_of_data,
                                         msg=f"Transition detected at index too late {index_from_batch}"
                                             f"construction expects {index_of_data} "
                                             f"And {len(batch_discarded)} timestamps where discarded"
                                             f" for {title}"
                                             f"(last timestamp of batch={batch_timestamps[-1]} "
                                             f"[{batch_timestamps[-1] / TIMESTAMP_UNIT_DIVIDER_MAP['s']}]")

                    # check that the transition isn't discarded
                    length_of_each_data[batch_data_id] += len(batch_discarded)

                    if i_of_transitions < len(transition_indexes)-1:
                        next_index_of_packet, next_index_of_data, next_series = transition_indexes[i_of_transitions+1]
                        if index_of_packet == next_index_of_packet:
                            if length_of_each_data[batch_data_id] > next_index_of_data:
                                i_of_transitions += 1
                            # end if
                        # end if
                    # end if
                # end if
                i_of_transitions += 1
                prev_discarded = batch_discarded
                prev_batch_timestamp = batch_timestamps
                prev_data_id = batch_data_id
            # end for
        # end for
    # end def _common_test_set_of_data

    def test_parse_no_flaws(self):
        """
        Tests all series set with no flaws in the generation
        """
        seed = 42
        for series_set in EXPECTED_SERIES_SET_TO_CHECK:
            data_timestamps, transition_indexes = self.build_data(
                seed, series_set, packet_drop=PacketDrop(peak_proba=0., proba_at_start=0.),
                start_time=29 * TIMESTAMP_UNIT_DIVIDER_MAP["s"], max_time=31 * TIMESTAMP_UNIT_DIVIDER_MAP["s"],
                jitter=0, window_jitter=(0, 0), fix_error_interval=1)
            self.data_to_check.append((seed, series_set, data_timestamps, transition_indexes))
        # end for

        self._common_test_set_of_data(True)
    # end def test_parse_no_flaws

    def test_parse_flaws(self):
        """
        Test all series set with a representative amount of flaws in the input signal,
        for a range of seeds to check stability in various situation
        """
        for seed in [0]:
            for series_set in [EXPECTED_SERIES_SET_TO_CHECK[2]]:
                data_timestamps, transition_indexes = self.build_data(
                    seed, series_set, packet_drop=PacketDrop(peak_proba=0.5, proba_at_start=0.2, peak_number=3),
                    max_time=180 * TIMESTAMP_UNIT_DIVIDER_MAP["s"], jitter=2 * TIMESTAMP_UNIT_DIVIDER_MAP["ms"],
                    window_jitter=(100 * TIMESTAMP_UNIT_DIVIDER_MAP["ms"], 100 * TIMESTAMP_UNIT_DIVIDER_MAP["ms"]),
                    fix_error_interval=1, adv_delay=True)
                self.data_to_check.append((seed, series_set, data_timestamps, transition_indexes))
            # end for
        # end for
        self._common_test_set_of_data(True)
    # end def test_parse_flaws
# end class BleAdvertisingParserTestCase


if __name__ == '__main__':
    from unittest import main

    main()
# end if
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
