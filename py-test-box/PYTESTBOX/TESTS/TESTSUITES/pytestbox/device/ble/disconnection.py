#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.disconnection
:brief: Validate BLE disconnection test cases
:author:  Sylvana Ieri <sieri@logitech.com>
:date: 2023/12/14
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import perf_counter_ns
from time import sleep

import numpy as np
from matplotlib import pyplot as plt

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import HidData
from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP
from pyraspi.services.kosmos.module.pestimer import TIMER
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.latency.latency import LatencyTestCase
from pytransport.ble.blecontext import BleContextCallbackEvents

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
MAX_DISCONNECTION_TIME = 100  # in ms

ITERATIONS = 3  # number of iterations to test

MAKE_GRAPH = False  # Flag to activate graphing the results of measure

_AUTHOR = "Sylvana Ieri"

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


# noinspection PyUnusedLocal
def do_nothing(*args):
    """
    Callback function doing nothing for placeholder

    :param args: placeholder arguments not used
    :type args: ``int``
    """
    pass
# end def do_nothing


# noinspection PyUnusedLocal
def delay_1s(*args):
    """
    Callback function simply delaying by 1 second

    :param args: placeholder arguments not used
    :type args: ``int``
    """
    sleep(1)
# end def delay_1s


class DisconnectionShutdownTestCases(DeviceBaseTestCase):

    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def tearDown(self):
        """
        Handle test post-requisites.
        """

        with self.manage_post_requisite():
            ble_context = BleProtocolTestUtils.get_ble_context(self)
            ble_context.clear_ble_event_callback()
        # end with

        with self.manage_kosmos_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        with self.manage_post_requisite():
            self.power_slider_emulator.power_on()
            # add 50ms delay to let the DUT restart
            sleep(.05)
        # end with

        with self.manage_post_requisite():
            # Reset timer module
            self.kosmos.timers.reset_module()
        # end with

        super().tearDown()
    # end def tearDown

    def _generic_disconnection_timing_test(self, scenario_string, delay=delay_1s, just_before_timer=do_nothing,
                                           reset=do_nothing):
        """
        Generic test for disconnection timing with power slider

        :param scenario_string: string describing the scenario being tested
        :type scenario_string: ``str``
        :param delay: method to delay after reconnection, takes an index as argument
        :type delay: ``callable``
        :param just_before_timer: method to call just before the timer is reset, takes an index as argument
        :type just_before_timer: ``callable``
        :param reset: method to call to reset the test in between iterations
        :type reset: ``callable``
        """
        self.callback_time = 0
        self.timestamps = 0
        test_loop_counter = ITERATIONS

        timer_id = TIMER.LOCAL
        delta_time = []
        timemarks = []

        # Get the kosmos instance here. Otherwise, the callback will be called from another thread and access to
        # the kosmos property create a new context, which will create issues on resource freeing
        kosmos = self.kosmos

        def callback(**kwargs):
            """
            Internal callback stopping the kosmos timer. If a timestamp is attached to the event also save it and
            timing data to compensate for treatment time

            :param kwargs: keyword arguments
            :type kwargs: ``dict``
            """
            kosmos.fpga.pulse_global_go_line()
            self.callback_time = perf_counter_ns()
            self.timestamps = kwargs['timestamps'] if "timestamps" in kwargs.keys() else None
        # end def callback

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Register callback on disconnection complete")
        # --------------------------------------------------------------------------------------------------------------
        ble_context = BleProtocolTestUtils.get_ble_context(self)
        ble_context.register_ble_event_callback(BleContextCallbackEvents.DISCONNECTION_COMPLETE, callback)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "turn the DUT off to have consistent time between connection and power off in "
                                 " each iterations")
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_off()
        self.current_channel.wait_device_connection_state(connected=False, timeout=3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop on each iterations")
        # --------------------------------------------------------------------------------------------------------------
        for i in range(test_loop_counter+1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Turn DUT back on")
            # ----------------------------------------------------------------------------------------------------------
            self.power_slider_emulator.power_on()
            reset(i)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Prepare shutdown sequence with timer")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True

            just_before_timer(i)
            self.kosmos.timers.restart(timers=timer_id)
            self.power_slider_emulator.power_off()
            self.kosmos.pes.wait_go_signal()
            self.kosmos.timers.save(timers=timer_id)
            self.kosmos.sequencer.offline_mode = False

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reconnect to DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.current_channel.wait_device_connection_state(connected=True, timeout=3)
            delay(i)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Play sequence")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait for disconnection")
            # ----------------------------------------------------------------------------------------------------------
            self.current_channel.wait_device_connection_state(connected=False, timeout=3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Download the timers")
            # ----------------------------------------------------------------------------------------------------------
            timemark = self.kosmos.timers.download()[timer_id]
            if self.timestamps is not None:
                delta = (self.callback_time - self.timestamps) / TIMESTAMP_UNIT_DIVIDER_MAP["us"]
                delta_time.append(delta)
            else:
                delta_time.append(0)
            # end if
            if len(timemark) == 0:
                # Force to call to the callback to unblock the pes wait_go_signal instruction
                kosmos.fpga.pulse_global_go_line()
                # Empty timestamp buffer
                self.kosmos.timers.download()
                self.fail(msg="'Disconnection complete' BLE event not received")
            # end if
            timemarks.append(timemark[0])
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Calculate the statistics of disconnection time")
        # --------------------------------------------------------------------------------------------------------------
        time_us = np.array(timemarks) * LatencyTestCase.TICK_CONVERSION
        corrected_time_ms = (time_us - delta_time) / 1e3
        average = np.average(corrected_time_ms)
        median = np.median(corrected_time_ms)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Average = {average}")
        LogHelper.log_info(self, f"median = {median}")
        # --------------------------------------------------------------------------------------------------------------

        if MAKE_GRAPH:
            self._plot_disconnection_time_distribution(
                test_loop_counter, corrected_time_ms, average, median, scenario_string)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check the average disconnection time {scenario_string} is less than {MAX_DISCONNECTION_TIME}ms")
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(a=average, b=MAX_DISCONNECTION_TIME,
                        msg=f"The average disconnection time ({average:.2f}ms) is more than the accepted "
                            f"time of {MAX_DISCONNECTION_TIME}ms")
    # end def _generic_disconnection_timing_test

    @features('BLEProtocol')
    @features('NoIsPlatform')
    @level('Business')
    @services('BleContext')
    @services('PowerSwitch')
    def test_slider_off_disconnection_time(self):
        """
        Verify that the average disconnection time is lower than the accepted time in the case where the disconnection
        doesn't happen immediately after connection.
        """
        self._generic_disconnection_timing_test(scenario_string="with a delay of 1s after reconnecting")

        self.testCaseChecked("BUS_BLE_DISC_0001", _AUTHOR)
    # end def test_slider_off_disconnection_time

    @features('BLEProtocol')
    @features('NoIsPlatform')
    @level('Business')
    @services('BleContext')
    @services('PowerSwitch')
    def test_slider_off_disconnection_time_no_delay(self):
        """
        Verify that the average disconnection time is lower than the accepted time in the case where the disconnection
        happens soon after connection
        """
        self._generic_disconnection_timing_test(scenario_string="with no delay after reconnecting", delay=do_nothing)

        self.testCaseChecked("BUS_BLE_DISC_0002", _AUTHOR)
    # end def test_slider_off_disconnection_time_no_delay

    @features('BLEProtocol')
    @features('NoIsPlatform')
    @level('Business')
    @services('KeyMatrix')
    @services('BleContext')
    @services('PowerSwitch')
    def test_slider_off_disconnection_time_key_press(self):
        """
        Verify that the average disconnection time is lower than the accepted time in the case where the disconnection
        happens as a key get pressed
        """
        self.callback_time = 0
        self.timestamps = None
        test_loop_counter = ITERATIONS

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Build a set of keys for {test_loop_counter} cycles")
        # --------------------------------------------------------------------------------------------------------------

        excluded_keys = HidData.get_not_single_action_keys()
        initial_keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False,
                                                       excluded_keys=excluded_keys)
        keys = initial_keys.copy()
        while len(keys) < test_loop_counter:
            keys.extend(initial_keys)
        # end while

        def _press_key(index):
            """
            Internal function to press a key in the list

            :param index: index of the key to press
            :type index: ``int``
            """
            self.button_stimuli_emulator.key_press(keys[index][0])
        # end def _press_key

        # noinspection PyUnusedLocal
        def _release_keys(i):
            """
            Internal function to release all keys

            :param i: index, not used
            :type i: ``int``
            """
            self.button_stimuli_emulator.release_all()
        # end def _release_keys

        self._generic_disconnection_timing_test(
            scenario_string="with a delay of 1s after reconnection and a keypress just before the switch",
            just_before_timer=_press_key, reset=_release_keys)

        self.testCaseChecked("BUS_BLE_DISC_0003", _AUTHOR)
    # end def test_slider_off_disconnection_time_key_press

    @staticmethod
    def _plot_disconnection_time_distribution(n_iter, disconnection_time_ms, average, median, title):
        """
        Plot the distribution of disconnection times for a given number of iterations

        :param n_iter: the number of iterations
        :type n_iter: ``int``
        :param disconnection_time_ms: list of times in milliseconds
        :type disconnection_time_ms: ``float``
        :param average: Average disconnection time in milliseconds
        :type average: ``float``
        :param median: Median disconnection time in milliseconds
        :type median: ``float``
        :param title: Scenario title, inserted in figure title
        :type title: ``str``
        """
        fig, ax = plt.subplots()
        fig.set_figwidth(15)
        fig.set_figwidth(15)
        fig.set_dpi(200)
        ax.hist(disconnection_time_ms, bins=10)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Count")
        ax.set_title(
            f"Distribution of disconnection time {title} over {n_iter} iteration\n"
            f" average={average:.2f}ms | median={median:.2f}ms")
        plt.show()
    # end def _plot_disconnection_time_distribution
# end class DisconnectionShutdownTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
