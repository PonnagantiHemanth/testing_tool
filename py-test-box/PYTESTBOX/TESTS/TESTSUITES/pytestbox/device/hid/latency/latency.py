#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.latency.latency
:brief: Hid Button Latency test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/07/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue
from os import F_OK
from os import access
from os import makedirs
from os.path import join
from random import choice
from random import randint
from random import uniform
from time import sleep

from math import ceil
from math import floor
from matplotlib import pyplot as plt
from numpy import array
from numpy import max as max_array
from numpy import mean as mean_array
from numpy import min as min_array
from numpy import percentile
from numpy import std as std_array

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbChannel
from pyhid.hid import HID_REPORTS
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ReportRateInfoEvent
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.tools.hexlist import HexList
from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.tool.beagle.beagle480 import Beagle480
from pyraspi.tool.beagle.beagle480 import BeagleChannel
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytransport.transportmessage import TransportMessage

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
Event = HidReportTestUtils.Event
EventId = HidReportTestUtils.EventId


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LatencyTestCase(BaseTestCase):
    """
    Validate Button Latency requirement
    """
    MOUSE_BUTTON_GROUP_SIZE = 2
    KEYBOARD_KEY_GROUP_SIZE = 30
    REPETITION = 100
    REPETITION_IN_SLEEP_MODE = 20
    # Conversion of MicroBlaze tick into micro seconds
    TICK_CONVERSION = 10**6 / FPGA_CURRENT_CLOCK_FREQ
    # Conversion of MicroBlaze frequency into seconds
    FPGA_CLOCK_PERIOD_S = 1 / FPGA_CURRENT_CLOCK_FREQ
    # Plot the reporting rate graph using matplot lib
    ENABLE_GRAPH = False
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._1_KHz

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        self.post_requisite_reset_motion_emulator = False
        self.post_requisite_turn_on_all_generic_usb_ports = False

        if self.ENABLE_GRAPH:
            # Creation of plot directory
            plot_dir = join(self.getContext().getOutputDir(), self.getContext().getCurrentTarget(),
                            'plot')
            if not access(plot_dir, F_OK):
                makedirs(plot_dir)
            # end if
            self._plot_path = join(plot_dir, f"{self.id()}.png")
        else:
            self._plot_path = None
        # end if

        self.trigger_gpio_in_polling_callbacks(enabled=True)

        # Empty hid_message_queue
        channel_to_use = self.current_channel.receiver_channel \
            if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel
        ChannelUtils.clean_messages(
            test_case=self, channel=channel_to_use, queue_name=HIDDispatcher.QueueName.HID, class_type=HID_REPORTS)

        # Flag indicating whether the test uses beagle analyser to trig on HID report
        self.use_beagle_analyser = False
        self.beagle480 = None
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Clean ReportRateInfoEvent messages")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=ReportRateInfoEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Clean HID messages")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                    class_type=HID_REPORTS)

        with self.manage_kosmos_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        with self.manage_kosmos_post_requisite():
            if self.post_requisite_reset_motion_emulator:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reset motion emulator')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.reset()
                self.post_requisite_reset_motion_emulator = False
            # end if
        # end with

        with self.manage_kosmos_post_requisite():
            # Reset timer module
            # noinspection PyUnresolvedReferences
            self.kosmos.timers.reset_module()
        # end with

        with self.manage_post_requisite():
            # Unsubscribe callback
            self.trigger_gpio_in_polling_callbacks(enabled=False)
        # end with

        with self.manage_post_requisite():
            if self.beagle480 is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Close beagle device")
                # ------------------------------------------------------------------------------------------------------
                self.beagle480.close()
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_turn_on_all_generic_usb_ports:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Turn on all generic USB ports (1, 2, 3, 4, 7)")
                # ------------------------------------------------------------------------------------------------------
                DeviceBaseTestUtils.UsbHubHelper.turn_on_all_generic_usb_ports(test_case=self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # post_requisite_reload_nvs flag need not be set to True,
                # if the set_report_Rate is performed in host_mode and switched back to onboard_mode
                # if hybrid switch power mode has been changed
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean WirelessDeviceStatusBroadcastEvent messages")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                            class_type=WirelessDeviceStatusBroadcastEvent)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean Battery Status messages")
                # ------------------------------------------------------------------------------------------------------
                self.cleanup_battery_event_from_queue()
            # end if
        # end with
        super().tearDown()
    # end def tearDown

    def set_mode_status_power_mode(self, power_mode):
        """
        Set hybrid switch power mode

        :param power_mode: Hybrid switch power mode
        :type power_mode: ``pyhid.hidpp.features.gaming.modestatus.ModeStatus.ModeStatus1.PowerMode``
        """
        config = self.f.PRODUCT.FEATURES.GAMING.MODE_STATUS
        if HexList(config.F_ModeStatus1).testBit(ModeStatus.ModeStatus1.POS.POWER_MODE) == power_mode:
            # Check if power_mode is the default mode
            return
        elif config.F_Enabled:
            # Check if feature 0x8090 (mode status) is enabled
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Change the hybrid switch mode configuration")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            ModeStatusTestUtils.flip_hybrid_switch_mode(test_case=self)
        else:
            raise ValueError(f"Unable to set power mode to {power_mode}, please ensure the setting is correct.")
        # end if
    # end def set_mode_status_power_mode

    def get_group_size(self, test_case):
        """
        Get the key/button group size for latency measurement

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Thr group size
        :rtype: ``int``
        """
        return self.MOUSE_BUTTON_GROUP_SIZE if test_case.f.PRODUCT.F_IsMice else self.KEYBOARD_KEY_GROUP_SIZE
    # end def get_group_size

    def get_latency_keys(self, get_hybrid_switch=False):
        """
        Get the key/button group size for latency measurement

        :param get_hybrid_switch: Flag indicating whether we get only hybrid or galvanic switches - OPTIONAL
        :type get_hybrid_switch: ``bool``

        :return: The latency keys/buttons use for the test
        :rtype: ``list``
        """
        if self.f.PRODUCT.F_IsMice:
            if get_hybrid_switch:
                excluded_keys = []
                for key in self.button_stimuli_emulator.get_key_id_list():
                    if key not in self.button_stimuli_emulator.get_hybrid_key_id_list():
                        excluded_keys.append(key)
                    # end if
                # end for
            else:
                excluded_keys = [key for key in self.button_stimuli_emulator.get_hybrid_key_id_list()]
            # end if
            keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.MOUSE_BUTTON_GROUP_SIZE, group_size=1,
                                                   random=False, excluded_keys=excluded_keys)
        else:
            excluded_keys = HidData.get_not_single_action_keys()
            keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.KEYBOARD_KEY_GROUP_SIZE, group_size=1,
                                                   random=False, excluded_keys=excluded_keys)
        # end if
        return keys
    # end def get_latency_keys

    # noinspection PyUnusedLocal
    def polling_callback(self, transport_message):
        """
        Callback function called when an HID report is received on Mouse & Keyboard EndPoint. The parameter
        ``transport_message`` is unused but is kept in the signature as it is what is expected of a transport callback
        (see ``TransportContextDevice``).

        :param transport_message: received interrupt data - UNUSED
        :type transport_message: ``TransportMessage``
        """
        # Toggle Go signal to generate the timestamp
        self.kosmos.fpga.pulse_global_go_line()
    # end def polling_callback

    def trigger_gpio_in_polling_callbacks(self, enabled=False):
        """
        Configure the task executor to poll the requested EPs

        :param enabled: Flag to enable the gpio triggering on Keyboard & Mouse EndPoints - OPTIONAL
        :type enabled: ``bool``
        """
        if enabled:
            # Update callback on Keyboard & Mouse Interfaces
            self.current_channel.update_callback(
                targeted_report_types=[LogitechReportType.KEYBOARD, LogitechReportType.MOUSE],
                callback=self.polling_callback)
        else:
            # Remove callback on Keyboard & Mouse Interfaces
            self.current_channel.update_callback(
                targeted_report_types=[LogitechReportType.KEYBOARD, LogitechReportType.MOUSE], callback=None)
        # end if
    # end def trigger_gpio_in_polling_callbacks

    def check_hid_input(
            self, count, ble_notification_queue=None, make_timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            break_timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT):
        """
        Check if the number of notifications received in a queue is correct

        :param count: the amount of notification to expect
        :type count: ``int``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        :param make_timeout: The waiting time before receiving the make report - OPTIONAL
        :type make_timeout: ``int``
        :param break_timeout: The waiting time before receiving the break report - OPTIONAL
        :type break_timeout: ``int``
        """
        if ble_notification_queue is None:
            for _ in range(count):
                # Retrieve the HID make report
                ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=make_timeout)
                # Retrieve the HID release report
                ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=break_timeout)
            # end for
        else:
            for _ in range(count):
                # Retrieve the HID make report
                # noinspection PyUnresolvedReferences
                ble_notification_queue.get(timeout=make_timeout)
                # Retrieve the HID release report
                # noinspection PyUnresolvedReferences
                ble_notification_queue.get(timeout=break_timeout)
            # end for
        # end if
    # end def check_hid_input

    def get_statistics(self, timings, high_bound=None):
        """
        Compute the average, minimum, maximum, 95 percentile and 99 percentile of the received timing values.

        :param timings: list of timing values
        :type timings: ``list[int]``
        :param high_bound: Highest acceptable value in micro seconds - OPTIONAL
        :type high_bound: ``int``

        :return: average, minimum, maximum, 95 percentile and 99 percentile timing values in micro seconds
        :rtype: ``float``, ``float``, ``float``, ``float``, ``float``
        """
        assert len(timings), "timings list is empty"
        timings = array(timings) * LatencyTestCase.TICK_CONVERSION
        average = mean_array(timings)
        minimum = min_array(timings)
        maximum = max_array(timings)
        _95_percentile = percentile(timings, q=95)
        _99_percentile = percentile(timings, q=99)
        above_high_bound_counter = sum(timings > high_bound) if high_bound is not None else 0
        # --------------------------------------------------------------------------------------------------------------
        if above_high_bound_counter > 0:
            LogHelper.log_info(
                self, f'{above_high_bound_counter} out of range measurement over {len(timings)} tries')
        # end if
        # --------------------------------------------------------------------------------------------------------------
        return average, minimum, maximum, _95_percentile, _99_percentile
    # end def get_statistics

    def plot_switch_latency(self, timings, title):
        """
        Save on a plot the switch latency

        :param timings: list of switch latency values
        :type timings: ``list[int]``
        :param title: Name of the plot
        :type title: ``str``
        """
        timings = array(timings)
        timings = timings * LatencyTestCase.TICK_CONVERSION / 1000
        average = mean_array(timings)
        standard_deviation = std_array(timings)

        fig, axs = plt.subplots(2, 1, layout='constrained', figsize=(10, 10))
        fig.suptitle(title, fontsize=12)

        axs[0].plot(timings, '+')
        axs[0].set_xlabel('sample')
        axs[0].set_ylabel('latency (ms)')
        axs[0].set_title('Latency')

        num_bins = 100
        _, _, _ = axs[1].hist(timings, bins=num_bins, density=True, stacked=True)
        axs[1].set_xlabel('Latency (ms)')
        axs[1].set_ylabel('Probability density')
        axs[1].set_title(f'Histogram of latency: average={average:0.2f}, std={standard_deviation:0.2f}')

        if self._plot_path is not None:
            plt.savefig(fname=self._plot_path)
        # end if
        plt.show()
    # end def plot_switch_latency

    def plot_motion_latency(self, min_timings, max_timings, title):
        """
        Save on a plot the motion latency

        :param min_timings: list of minimum motion latency values
        :type min_timings: ``list[int]``
        :param max_timings: list of maximum motion latency values
        :type max_timings: ``list[int]``
        :param title: Name of the plot
        :type title: ``str``
        """
        min_timings = array(min_timings)
        min_timings = min_timings * LatencyTestCase.TICK_CONVERSION / 1000
        max_timings = array(max_timings)
        max_timings = max_timings * LatencyTestCase.TICK_CONVERSION / 1000

        fig, axs = plt.subplots(3, 2, layout='constrained', figsize=(10, 10))
        fig.suptitle(title, fontsize=12)

        axs[0][0].plot(min_timings, '+')
        axs[0][0].set_xlabel('sample')
        axs[0][0].set_ylabel('latency (ms)')
        axs[0][0].set_title('Minimum Motion Latency')

        num_bins = 100
        min_average = mean_array(min_timings)
        min_standard_deviation = std_array(min_timings)
        axs[0][1].hist(min_timings, bins=num_bins, density=True, stacked=True)
        axs[0][1].set_xlabel('Latency (ms)')
        axs[0][1].set_ylabel('Probability density')
        axs[0][1].set_title(f'Histogram: average={min_average:0.2f}, std={min_standard_deviation:0.2f}')

        axs[1][0].plot(max_timings, '+')
        axs[1][0].set_xlabel('sample')
        axs[1][0].set_ylabel('latency (ms)')
        axs[1][0].set_title('Maximum Motion Latency')

        max_average = mean_array(max_timings)
        max_standard_deviation = std_array(max_timings)
        axs[1][1].hist(max_timings, bins=num_bins, density=True, stacked=True)
        axs[1][1].set_xlabel('Latency (ms)')
        axs[1][1].set_ylabel('Probability density')
        axs[1][1].set_title(f'Histogram: average={max_average:0.2f}, std={max_standard_deviation:0.2f}')

        axs[2][0].plot(max_timings - min_timings, '+')
        axs[2][0].set_xlabel('sample')
        axs[2][0].set_ylabel('delta (ms)')
        axs[2][0].set_title('Sensor polling delta time')

        average = mean_array(max_timings - min_timings)
        standard_deviation = std_array(max_timings - min_timings)
        axs[2][1].hist(max_timings - min_timings, bins=num_bins, density=True, stacked=True)
        axs[2][1].set_xlabel('Delta (ms)')
        axs[2][1].set_ylabel('Probability density')
        axs[2][1].set_title(f'Histogram: average={average:0.3f}, std={standard_deviation:0.5f}')

        if self._plot_path is not None:
            plt.savefig(fname=self._plot_path)
        # end if
        plt.show()
    # end def plot_motion_latency

    def validate_switch_latency(self, timings, on_press=True, sleep_mode=False, deep_sleep_mode=False, lift_mode=False):
        """
        Validate the motion latency measurements of the device

        :param timings: list of motion latency values
        :type timings: ``list[int]``
        :param on_press: Flag indicating that the user action is pressing a button - OPTIONAL
        :type on_press: ``bool``
        :param sleep_mode: Flag indicating if the device is in sleep mode (exclusive with deep_sleep_mode)
                           - OPTIONAL
        :type sleep_mode: ``bool``
        :param deep_sleep_mode: Flag indicating if the device is in deep sleep mode (exclusive with sleep_mode)
                               - OPTIONAL
        :type deep_sleep_mode: ``bool``
        :param lift_mode: Flag indicating if the device is in lift mode - OPTIONAL
        :type lift_mode: ``bool``

        :raise ``ValueError``: If the protocol on current channel is not supported or if the report rate is not
                               supported
        """
        average, minimum, maximum, _95_percentile, _99_percentile = self.get_statistics(timings=timings)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_metrics(self,
                              key=f'The switch latency time : ',
                              value=f'average={average}us, minimum={minimum}us, maximum={maximum}us, '
                                    f'95_percentile={_95_percentile}us, 99_percentile={_99_percentile}us')
        # --------------------------------------------------------------------------------------------------------------
        if deep_sleep_mode:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for switch latency in Deep Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_MinSwitchLatencyDeepSleepMode,
                "At least one of the switch latency measurement is lower than the specification in Deep Sleep")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the average marker for switch latency in Deep Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                average,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyDeepSleepMode,
                "The switch latency average is greater than the specification in Deep Sleep mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the 95 percentile marker for switch latency in Deep Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                _95_percentile,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyDeepSleepMode,
                "In Deep Sleep mode, Less than 95% of the measurements have a switch latency time of "
                f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyDeepSleepMode}us or less")
        elif sleep_mode:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for switch latency in Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_MinSwitchLatencySleepMode,
                "At least one of the switch latency measurement is lower than the specification in Sleep mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the average marker for switch latency in Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                average,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencySleepMode,
                "The switch latency average is greater than the specification in Sleep mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the 95 percentile marker for switch latency in Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                _95_percentile,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencySleepMode,
                "In Deep Sleep mode, Less than 95% of the measurements have a switch latency time of "
                f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencySleepMode}us or less")
        elif lift_mode:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for switch latency in lift mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_MinSwitchLatencyLiftMode,
                "At least one of the switch latency measurement is lower than the specification in Lift mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the average marker for switch latency in Lift mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                average,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyLiftMode,
                "The switch latency average is greater than the specification in Lift mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the 95 percentile marker for switch latency in Lift mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                _95_percentile,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyLiftMode,
                "In Lift mode, Less than 95% of the measurements have a switch latency time of "
                f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyLiftMode}us or less")
        elif self.current_channel.protocol == LogitechProtocol.LS2_CA_CRC24:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for switch latency on LS2')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_MinSwitchLatencyLs2RunMode,
                "At least one of the LS2 switch latency measurement is lower than the specification")
            if on_press:
                if self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._1_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on LS2 at 1kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressLs2RunMode1kHz,
                        "The press latency average is greater than the specification at 1kHz on LS2")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 95 percentile marker for press latency on LS2 at 1kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode1kHz,
                        "On LS2 at 1kHz, Less than 95% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode1kHz}us or less")
                elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._2_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on LS2 at 2kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressLs2RunMode2kHz,
                        "The press latency average is greater than the specification at 2kHz on LS2")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 95 percentile marker for press latency on LS2 at 2kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode2kHz,
                        "On LS2 at 2kHz, Less than 95% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode2kHz}us or less")
                elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._4_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on LS2 at 4kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressLs2RunMode4kHz,
                        "The press latency average is greater than the specification at 4kHz on LS2")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 95 percentile marker for press latency on LS2 at 4kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode4kHz,
                        "On LS2 at 4kHz, Less than 95% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode4kHz}us or less")
                elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._8_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on LS2 at 8kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressLs2RunMode8kHz,
                        "The press latency average is greater than the specification at 8kHz on LS2")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 95 percentile marker for press latency on LS2 at 8kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode8kHz,
                        "On LS2 at 8kHz, Less than 95% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyPressLs2RunMode8kHz}us or less")
                # end if
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for release latency on LS2')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyReleaseLs2RunMode,
                    "The release latency average is greater than the specification on LS2")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for release latency on LS2')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyReleaseLs2RunMode,
                    "On LS2, Less than 95% of the measurements have a release latency time of "
                    f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95SwitchLatencyReleaseLs2RunMode}us or less")
            # end if
        elif self.current_channel.protocol == LogitechProtocol.USB:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for switch latency on USB')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_MinSwitchLatencyUsb,
                "At least one of the USB switch latency measurement is lower than the specification")
            if on_press:
                if self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._1_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on USB at 1kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressUsb1kHz,
                        "The press latency average is greater than the specification at 1kHz on USB")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 99 percentile marker for press latency on USB at 1kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb1kHz,
                        "On USB at 1kHz, Less than 99% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb1kHz}us or less")
                elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._2_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on USB at 2kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressUsb2kHz,
                        "The press latency average is greater than the specification at 2kHz on USB")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 99 percentile marker for press latency on USB at 2kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb2kHz,
                        "On USB at 2kHz, Less than 99% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb2kHz}us or less")
                elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._4_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on USB at 4kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressUsb4kHz,
                        "The press latency average is greater than the specification at 4kHz on USB")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 99 percentile marker for press latency on USB at 4kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb4kHz,
                        "On USB at 4kHz, Less than 99% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb4kHz}us or less")
                elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._8_KHz:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the average marker for press latency on USB at 8kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        average,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyPressUsb8kHz,
                        "The press latency average is greater than the specification at 8kHz on USB")
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate the 99 percentile marker for press latency on USB at 8kHz')
                    # --------------------------------------------------------------------------------------------------
                    self.assertLess(
                        _95_percentile,
                        self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb8kHz,
                        "On USB at 8kHz, Less than 99% of the measurements have a press latency time of "
                        f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyPressUsb8kHz}us or less")
                # end if
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for release latency on USB')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgSwitchLatencyReleaseUsb,
                    "The release latency average is greater than the specification on USB")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for release latency on USB')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyReleaseUsb,
                    "On USB, Less than 99% of the measurements have a release latency time of "
                    f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile99SwitchLatencyReleaseUsb}us or less")
            # end if
        elif (self.current_channel.protocol == LogitechProtocol.BLE or
              self.current_channel.protocol == LogitechProtocol.BLE_PRO):
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for switch latency on BLE')
            # ------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_MinSwitchLatencyRunMode,
                "At least one of the BLE press switch latency measurement is lower than the specification")
            if on_press:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for press switch latency on BLE')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgPressLatencyRunMode,
                    "The press switch latency average is greater than the specification on BLE")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for press switch latency on BLE')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95PressLatencyRunMode,
                    "On BLE, Less than 95% of the measurements have a press switch latency time of "
                    f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95PressLatencyRunMode}us or "
                    f"less")
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for release switch latency on BLE')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_AvgReleaseLatencyRunMode,
                    "The release switch latency average is greater than the specification on BLE")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for release switch latency on BLE')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95ReleaseLatencyRunMode,
                    "On BLE, Less than 95% of the measurements have a release switch latency time of "
                    f"{self.f.PRODUCT.LATENCY.SWITCH_LATENCY.F_Percentile95ReleaseLatencyRunMode}us or "
                    f"less")
            # end if
        else:
            raise ValueError(f'Unsupported protocol: {self.current_channel.protocol!s}')
        # end if
    # end def validate_switch_latency

    def validate_motion_latency(self, timings, sleep_mode=False, deep_sleep_mode=False):
        """
        Validate the motion latency measurements of the device

        :param timings: list of motion latency values
        :type timings: ``list[int]``
        :param sleep_mode: Flag indicating if the device is in sleep mode (exclusive with deep_sleep_mode)
                           - OPTIONAL
        :type sleep_mode: ``bool``
        :param deep_sleep_mode: Flag indicating if the device is in deep sleep mode (exclusive with sleep_mode)
                               - OPTIONAL
        :type deep_sleep_mode: ``bool``

        :raise ``ValueError``: If the protocol on current channel is not supported or if the report rate is not
                               supported
        """
        average, minimum, maximum, _95_percentile, _99_percentile = self.get_statistics(timings=timings)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_metrics(self,
                              key=f'The motion latency time : ',
                              value=f'average={average}us, minimum={minimum}us, maximum={maximum}us, '
                                    f'95_percentile={_95_percentile}us, 99_percentile={_99_percentile}us')
        # --------------------------------------------------------------------------------------------------------------

        if deep_sleep_mode:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for motion latency in Deep Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_MinMotionLatencyDeepSleepMode,
                "At least one of the USB motion latency measurement is lower than the specification")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the average marker for motion latency in Deep Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                average,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyDeepSleepMode,
                "The motion latency average is greater than the specification in Deep Sleep mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the 95 percentile marker for motion latency in Deep Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                _95_percentile,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyDeepSleepMode,
                "In Deep Sleep mode, Less than 95% of the measurements have a motion latency time of "
                f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyDeepSleepMode}us or "
                f"less")
        elif sleep_mode:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for motion latency in Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_MinMotionLatencySleepMode,
                "At least one of the USB motion latency measurement is lower than the specification")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the average marker for motion latency in Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                average,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencySleepMode,
                "The motion latency average is greater than the specification in Sleep mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the 95 percentile marker for motion latency in Sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                _95_percentile,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencySleepMode,
                "In Sleep mode, Less than 95% of the measurements have a motion latency time of "
                f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencySleepMode}us or "
                f"less")
        elif self.current_channel.protocol == LogitechProtocol.LS2_CA_CRC24:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for motion latency on LS2')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_MinMotionLatencyLs2RunMode,
                "At least one of the LS2 motion latency measurement is lower than the specification")
            if self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._1_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on LS2 at 1kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyLs2RunMode1kHz,
                    "The motion latency average is greater than the specification at 1kHz on LS2")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for motion latency on LS2 at 1kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb1kHz,
                    "On LS2 at 1kHz, Less than 95% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyLs2RunMode1kHz}us "
                    f"or less")
            elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._2_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on LS2 at 2kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyLs2RunMode2kHz,
                    "The motion latency average is greater than the specification at 2kHz on LS2")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for motion latency on LS2 at 2kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyLs2RunMode2kHz,
                    "On LS2 at 2kHz, Less than 95% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyLs2RunMode2kHz}us "
                    f"or less")
            elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._4_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on LS2 at 4kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyLs2RunMode4kHz,
                    "The motion latency average is greater than the specification at 4kHz on LS2")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for motion latency on LS2 at 4kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyLs2RunMode4kHz,
                    "On LS2 at 4kHz, Less than 95% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyLs2RunMode4kHz}us"
                    f" or less")
            elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._8_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on LS2 at 8kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyLs2RunMode8kHz,
                    "The motion latency average is greater than the specification at 8kHz on LS2")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 95 percentile marker for motion latency on LS2 at 8kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _95_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyLs2RunMode8kHz,
                    "On USB at 8kHz, Less than 99% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyLs2RunMode8kHz}us"
                    f" or less")
            # end if
        elif self.current_channel.protocol == LogitechProtocol.USB:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for motion latency on USB')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_MinMotionLatencyUsb,
                "At least one of the USB motion latency measurement is lower than the specification")
            if self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._1_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on USB at 1kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyUsb1kHz,
                    "The motion latency average is greater than the specification at 1kHz on USB")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 99 percentile marker for motion latency on USB at 1kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _99_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb1kHz,
                    "On USB at 1kHz, Less than 99% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb1kHz}us or "
                    f"less")
            elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._2_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on USB at 2kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyUsb2kHz,
                    "The motion latency average is greater than the specification at 2kHz on USB")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 99 percentile marker for motion latency on USB at 2kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _99_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb2kHz,
                    "On USB at 2kHz, Less than 99% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb2kHz}us or "
                    f"less")
            elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._4_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on USB at 4kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyUsb4kHz,
                    "The motion latency average is greater than the specification at 4kHz on USB")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 99 percentile marker for motion latency on USB at 4kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _99_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb4kHz,
                    "On USB at 4kHz, Less than 99% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb4kHz}us or "
                    f"less")
            elif self.REPORT_RATE == ExtendedAdjustableReportRate.RATE._8_KHz:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the average marker for motion latency on USB at 8kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    average,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyUsb8kHz,
                    "The motion latency average is greater than the specification at 8kHz on USB")
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the 99 percentile marker for motion latency on USB at 8kHz')
                # ------------------------------------------------------------------------------------------------------
                self.assertLess(
                    _99_percentile,
                    self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb8kHz,
                    "On USB at 8kHz, Less than 99% of the measurements have a motion latency time of "
                    f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile99MotionLatencyUsb8kHz}us or "
                    f"less")
            else:
                raise ValueError(f'Unsupported report rate: {self.REPORT_RATE!s}')
            # end if
        elif (self.current_channel.protocol == LogitechProtocol.BLE or
              self.current_channel.protocol == LogitechProtocol.BLE_PRO):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the minimum marker for motion latency on BLE')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(
                minimum,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_MinMotionLatencyRunMode,
                "At least one of the USB motion latency measurement is lower than the specification")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the average marker for motion latency on BLE')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                average,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_AvgMotionLatencyRunMode,
                "The motion latency average is greater than the specification on BLE in Deep Sleep mode")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the 95 percentile marker for motion latency on BLE')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(
                _95_percentile,
                self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyRunMode,
                "On BLE, in Deep Sleep mode, Less than 95% of the measurements have a motion latency time of "
                f"{self.f.PRODUCT.LATENCY.MOTION_LATENCY.F_Percentile95MotionLatencyRunMode}us or "
                f"less")
        else:
            raise ValueError(f'Unsupported protocol: {self.current_channel.protocol!s}')
        # end if
    # end def validate_motion_latency

    def get_endpoint(self):
        """
        Get the endpoint of the DUT

        :return: Endpoint number
        :rtype: ``int``
        """
        if self.f.PRODUCT.F_IsMice:
            report_type = LogitechReportType.MOUSE
        else:
            report_type = LogitechReportType.KEYBOARD
        # end if
        channel = self.current_channel
        if isinstance(channel, ThroughReceiverChannel):
            return channel.receiver_channel.report_type_to_endpoint[report_type] & 0x7F
        elif isinstance(channel, UsbChannel):
            return channel.report_type_to_endpoint[report_type] & 0x7F
        else:
            raise TypeError(
                "Cannot get the USB device address if the channel is not the right type. It should be one "
                "of the channel types (UsbChannel, ThroughReceiverChannel), it is "
                f"{type(channel)}")
        # end if
    # end def get_endpoint

    def measure_and_validate_make_latency_in_active_mode(self, ble_notification_queue=None, check_hybrid_switch=False):
        """
        Measure and validate make latency in active mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        :param check_hybrid_switch:  Flag indicating whether we use only hybrid or galvanic switches - OPTIONAL
        :type check_hybrid_switch: ``bool``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        timings = []
        timer_id = TIMER.LOCAL
        initial_keys = self.get_latency_keys(get_hybrid_switch=check_hybrid_switch)

        keys = initial_keys.copy()
        while len(keys) < LatencyTestCase.REPETITION_IN_SLEEP_MODE:
            keys.extend(initial_keys)
        # end while
        loop_count = ceil(LatencyTestCase.REPETITION / len(keys))

        for _ in range(loop_count):
            self.kosmos.sequencer.offline_mode = True
            for (key_id,) in keys:
                # Local timer initialization
                self.kosmos.timers.restart(timers=timer_id)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keypress on the supported key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=key_id)
                if self.use_beagle_analyser:
                    # PES will then wait for the Beagle signal
                    if self.current_channel.protocol == LogitechProtocol.USB:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                    else:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                    # end if
                else:
                    # PES will then wait for the raspberry PI signal
                    self.kosmos.pes.wait_go_signal()
                # end if
                self.kosmos.timers.save(timers=timer_id)

                # add random delay between 0 and 1ms to avoid to do a key press always on the same time during MCU
                # main loop and choose a value that is multiple of fpga clock period
                random_delay_s = uniform(0, 1/1000)
                ticks = floor(random_delay_s / self.FPGA_CLOCK_PERIOD_S)
                random_delay_s = self.FPGA_CLOCK_PERIOD_S * ticks
                self.button_stimuli_emulator.multiple_keys_release(
                    key_ids=[key_id],
                    delay=ButtonStimuliInterface.DEFAULT_DELAY + random_delay_s)
            # end for

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence()

            for _ in keys:
                # Retrieve the HID reports
                self.check_hid_input(count=1, ble_notification_queue=ble_notification_queue)
            # end for

            # Wait for end of sequence execution
            self.kosmos.sequencer.wait_end_of_sequence()

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])
        # end for

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timings, title=self.short_name())
        # end if

        # Validate time marks
        self.assertGreaterEqual(len(timings), LatencyTestCase.REPETITION,
                                f'The number of test point is too low ({len(timings)} < {LatencyTestCase.REPETITION})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch press latency specification in active mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timings)
    # end def measure_and_validate_make_latency_in_active_mode

    def measure_and_validate_break_latency_in_active_mode(self, ble_notification_queue=None, check_hybrid_switch=False):
        """
        Measure and validate break latency in active mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        :param check_hybrid_switch: Flag indicating whether we use only hybrid or galvanic switches - OPTIONAL
        :type check_hybrid_switch: ``bool``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        timings = []
        timer_id = TIMER.LOCAL
        initial_keys = self.get_latency_keys(get_hybrid_switch=check_hybrid_switch)
        keys = initial_keys.copy()
        while len(keys) < LatencyTestCase.REPETITION_IN_SLEEP_MODE:
            keys.extend(initial_keys)
        # end while
        loop_count = ceil(LatencyTestCase.REPETITION / len(keys))

        for _ in range(loop_count):
            self.kosmos.sequencer.offline_mode = True
            for (key_id, ) in keys:
                # add random delay between 0 and 1ms to avoid to do a key press always on the same time during MCU
                # main loop and choose a value that is multiple of fpga clock period
                random_delay_s = uniform(0, 1 / 1000)
                ticks = floor(random_delay_s / self.FPGA_CLOCK_PERIOD_S)
                random_delay_s = self.FPGA_CLOCK_PERIOD_S * ticks
                self.button_stimuli_emulator.multiple_keys_press(
                    key_ids=[key_id],
                    delay=ButtonStimuliInterface.DEFAULT_DELAY + random_delay_s)
                # Local timer initialization
                self.kosmos.timers.restart(timers=timer_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a key release on the supported key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key_id)
                if self.use_beagle_analyser:
                    # PES will then wait for the Beagle signal
                    if self.current_channel.protocol == LogitechProtocol.USB:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                    else:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                    # end if
                else:
                    # PES will then wait for the raspberry PI signal
                    self.kosmos.pes.wait_go_signal()
                # end if
                self.kosmos.timers.save(timers=timer_id)
            # end for

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(block=False)

            for _ in keys:
                # Retrieve the HID reports
                self.check_hid_input(count=1, ble_notification_queue=ble_notification_queue)
            # end for

            # Wait for end of sequence execution
            self.kosmos.sequencer.wait_end_of_sequence()

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])
        # end for

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timings, title=self.short_name())
        # end if

        # Validate time marks
        self.assertGreaterEqual(len(timings), LatencyTestCase.REPETITION,
                                f'The number of test point is too low ({len(timings)} < {LatencyTestCase.REPETITION})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch release latency specification in active mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timings, on_press=False)
    # end def measure_and_validate_break_latency_in_active_mode

    def measure_and_validate_make_latency_in_run_mode(self, ble_notification_queue=None):
        """
        Measure and validate make latency in run mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        timings = []
        timer_id = TIMER.LOCAL
        excluded_keys = HidData.get_not_single_action_keys()
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.get_group_size(test_case=self),
                                               group_size=1, random=False, excluded_keys=excluded_keys)

        (wake_up_key_id, ) = keys.pop(0)
        loop_count = ceil(LatencyTestCase.REPETITION / len(keys))

        for _ in range(loop_count):
            self.kosmos.sequencer.offline_mode = True
            for (key_id, ) in keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Emulate a keypress to force the DUT in run mode')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=wake_up_key_id,
                                                       duration=ButtonStimuliInterface.DEFAULT_DURATION / 2,
                                                       delay=ButtonStimuliInterface.DEFAULT_DELAY / 2)

                # Local timer initialization
                self.kosmos.timers.restart(timers=timer_id)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keypress on the supported key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=key_id)

                if self.use_beagle_analyser:
                    # PES will then wait for the Beagle signal
                    if self.current_channel.protocol == LogitechProtocol.USB:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                    else:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                    # end if
                else:
                    # PES will then wait for the raspberry PI signal
                    self.kosmos.pes.wait_go_signal()
                # end if
                self.kosmos.timers.save(timers=timer_id)

                self.button_stimuli_emulator.multiple_keys_release(key_ids=[key_id],
                                                                   delay=ButtonStimuliInterface.DEFAULT_DELAY)
            # end for

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(block=False)

            for _ in keys:
                # Retrieve the HID reports
                self.check_hid_input(count=2, ble_notification_queue=ble_notification_queue)
            # end for

            # Wait for end of sequence execution
            self.kosmos.sequencer.wait_end_of_sequence(timeout=1)

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])
        # end for

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timings, title=self.short_name())
        # end if

        # Validate time marks
        self.assertGreaterEqual(len(timings), LatencyTestCase.REPETITION,
                                f'The number of test point is too low ({len(timings)} < {LatencyTestCase.REPETITION})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch press latency specification in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timings)
    # end def measure_and_validate_make_latency_in_run_mode

    def measure_and_validate_break_latency_in_run_mode(self, ble_notification_queue=None):
        """
        Measure and validate break latency in run mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        timings = []
        timer_id = TIMER.LOCAL
        excluded_keys = HidData.get_not_single_action_keys()
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.get_group_size(test_case=self),
                                               group_size=1, random=False, excluded_keys=excluded_keys)
        (wake_up_key_id, ) = keys.pop(0)
        loop_count = ceil(LatencyTestCase.REPETITION / len(keys))
        for _ in range(loop_count):
            self.kosmos.sequencer.offline_mode = True
            for (key_id, ) in keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Emulate a keypress to force the DUT in run mode')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=wake_up_key_id,
                                                       duration=ButtonStimuliInterface.DEFAULT_DURATION / 2,
                                                       delay=ButtonStimuliInterface.DEFAULT_DELAY / 2)

                self.button_stimuli_emulator.multiple_keys_press(key_ids=[key_id],
                                                                 delay=ButtonStimuliInterface.DEFAULT_DELAY)
                # Local timer initialization
                self.kosmos.timers.restart(timers=timer_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a key release on the supported key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key_id)

                if self.use_beagle_analyser:
                    # PES will then wait for the Beagle signal
                    if self.current_channel.protocol == LogitechProtocol.USB:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                    else:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                    # end if
                else:
                    # PES will then wait for the raspberry PI signal
                    self.kosmos.pes.wait_go_signal()
                # end if
                self.kosmos.timers.save(timers=timer_id)
            # end for

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(block=False)

            for _ in keys:
                # Retrieve the HID reports
                self.check_hid_input(count=2, ble_notification_queue=ble_notification_queue)
            # end for

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])
        # end for

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timings, title=self.short_name())
        # end if

        # Validate time marks
        self.assertGreaterEqual(len(timings), LatencyTestCase.REPETITION,
                                f'The number of test point is too low ({len(timings)} < {LatencyTestCase.REPETITION})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch release latency specification in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timings, on_press=False)
    # end def measure_and_validate_break_latency_in_run_mode

    def measure_and_validate_make_latency_in_sleep_mode(self, ble_notification_queue=None):
        """
        Measure and validate make latency in sleep mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        timer_id = TIMER.LOCAL
        excluded_keys = HidData.get_not_single_action_keys()
        initial_keys = KeyMatrixTestUtils.get_key_list(self, group_count=1,
                                                       group_size=1, random=False, excluded_keys=excluded_keys)
        keys = initial_keys.copy()
        while len(keys) < LatencyTestCase.REPETITION_IN_SLEEP_MODE:
            keys.extend(initial_keys)
        # end while
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep + 1)

        self.kosmos.sequencer.offline_mode = True
        count = 0
        for (key_id, ) in keys[:LatencyTestCase.REPETITION_IN_SLEEP_MODE]:
            count += 1
            # Local timer initialization
            self.kosmos.timers.restart(timers=timer_id)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keypress on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=key_id)

            if self.use_beagle_analyser:
                # PES will then wait for the Beagle signal
                if self.current_channel.protocol == LogitechProtocol.USB:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                else:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                # end if
            else:
                # PES will then wait for the raspberry PI signal
                self.kosmos.pes.wait_go_signal()
            # end if
            self.kosmos.timers.save(timers=timer_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a key release on the supported key {str(key_id)} then wait for the '
                                     'device to re-enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(
                key_ids=[key_id],
                delay=self.f.PRODUCT.DEVICE.F_MaxWaitSleep + .5 if count < LatencyTestCase.REPETITION_IN_SLEEP_MODE else ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for _ in keys[:LatencyTestCase.REPETITION_IN_SLEEP_MODE]:
            # Retrieve the HID reports
            self.check_hid_input(count=1, ble_notification_queue=ble_notification_queue,
                                 make_timeout=self.f.PRODUCT.DEVICE.F_MaxWaitSleep + 1)
        # end for

        # Wait for end of sequence execution
        self.kosmos.sequencer.wait_end_of_sequence()

        # Download time mark
        timemarks = self.kosmos.timers.download()

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timemarks[timer_id], title=self.short_name())
        # end if

        # Validate time marks
        self.assertEqual(LatencyTestCase.REPETITION_IN_SLEEP_MODE, len(timemarks[timer_id]),
                         f'The number of test point is not as expected ({len(timemarks[timer_id])} < '
                         f'{LatencyTestCase.REPETITION_IN_SLEEP_MODE})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch press latency specification in sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timemarks[timer_id])
    # end def measure_and_validate_make_latency_in_sleep_mode

    def measure_and_validate_break_latency_in_sleep_mode(self, ble_notification_queue=None):
        """
        Measure and validate break latency in sleep mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        timer_id = TIMER.LOCAL
        excluded_keys = HidData.get_not_single_action_keys()
        initial_keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.get_group_size(test_case=self),
                                                       group_size=1, random=False, excluded_keys=excluded_keys)
        keys = initial_keys.copy()
        while len(keys) < LatencyTestCase.REPETITION_IN_SLEEP_MODE:
            keys.extend(initial_keys)
        # end while

        self.kosmos.sequencer.offline_mode = True
        for (key_id, ) in keys[:LatencyTestCase.REPETITION_IN_SLEEP_MODE]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {str(key_id)} then wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=[key_id],
                                                             delay=self.f.PRODUCT.DEVICE.F_MaxWaitSleep + .5)
            # Local timer initialization
            self.kosmos.timers.restart(timers=timer_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a key release on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=key_id)

            if self.use_beagle_analyser:
                # PES will then wait for the Beagle signal
                if self.current_channel.protocol == LogitechProtocol.USB:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                else:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                # end if
            else:
                # PES will then wait for the raspberry PI signal
                self.kosmos.pes.wait_go_signal()
            # end if
            self.kosmos.timers.save(timers=timer_id)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for _ in keys[:LatencyTestCase.REPETITION_IN_SLEEP_MODE]:
            # Retrieve the HID reports
            self.check_hid_input(count=1, ble_notification_queue=ble_notification_queue,
                                 break_timeout=self.f.PRODUCT.DEVICE.F_MaxWaitSleep + 1)
        # end for

        # Wait for end of sequence execution
        self.kosmos.sequencer.wait_end_of_sequence()
        # Download time mark
        timemarks = self.kosmos.timers.download()

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timemarks[timer_id], title=self.short_name())
        # end if

        # Validate time marks
        self.assertEqual(LatencyTestCase.REPETITION_IN_SLEEP_MODE, len(timemarks[timer_id]),
                         f'The number of test point is not as expected ({len(timemarks[timer_id])} < '
                         f'{LatencyTestCase.REPETITION_IN_SLEEP_MODE})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch release latency specification in sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timemarks[timer_id], on_press=False)
    # end def measure_and_validate_break_latency_in_sleep_mode

    def measure_and_validate_make_latency_in_deep_sleep_mode(self, ble_notification_queue=None):
        """
        Measure and validate make latency in deep sleep mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        timings = []
        timer_id = TIMER.LOCAL
        excluded_keys = HidData.get_not_single_action_keys()
        initial_keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.get_group_size(test_case=self),
                                                       group_size=1, random=False, excluded_keys=excluded_keys)
        keys = initial_keys.copy()
        while len(keys) < LatencyTestCase.REPETITION_IN_SLEEP_MODE:
            keys.extend(initial_keys)
        # end while

        for (key_id, ) in keys[:LatencyTestCase.REPETITION_IN_SLEEP_MODE]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

            if ble_notification_queue is None:
                self.trigger_gpio_in_polling_callbacks(enabled=True)
            # end if

            # Empty hid_message_queue
            channel_to_use = self.current_channel.receiver_channel \
                if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel
            ChannelUtils.clean_messages(
                test_case=self, channel=channel_to_use, queue_name=HIDDispatcher.QueueName.HID, class_type=HID_REPORTS)

            self.kosmos.sequencer.offline_mode = True
            # Local timer initialization
            self.kosmos.timers.restart(timers=timer_id)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keypress on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=key_id)

            if self.use_beagle_analyser:
                # PES will then wait for the Beagle signal
                if self.current_channel.protocol == LogitechProtocol.USB:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                else:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                # end if
            else:
                # PES will then wait for the raspberry PI signal
                self.kosmos.pes.wait_go_signal()
            # end if
            self.kosmos.timers.save(timers=timer_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a key release on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=key_id)

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(block=False)

            if ble_notification_queue is not None:
                BleProtocolTestUtils.connect_and_bond_device(test_case=self,
                                                             ble_context_device=self.ble_context_device_used,
                                                             log_gatt_table=False)
                self.trigger_gpio_in_polling_callbacks(enabled=True)
            # end if

            # Retrieve the HID reports
            self.check_hid_input(count=1, ble_notification_queue=ble_notification_queue)

            # Wait for end of sequence execution
            self.kosmos.sequencer.wait_end_of_sequence()

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])

            # Start polling all EPs
            self.trigger_gpio_in_polling_callbacks(enabled=False)
        # end for

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timings, title=self.short_name())
        # end if

        # Validate time marks
        self.assertEqual(LatencyTestCase.REPETITION_IN_SLEEP_MODE, len(timings),
                         f'The number of test point is not as expected ({len(timings)} < '
                         f'{LatencyTestCase.REPETITION_IN_SLEEP_MODE})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch press latency specification in deep sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timings, deep_sleep_mode=True)
    # end def measure_and_validate_make_latency_in_deep_sleep_mode

    def measure_and_validate_make_latency_in_lift_mode(self, ble_notification_queue=None):
        """
        Measure and validate make latency in Lift mode

        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        if self.use_beagle_analyser:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint)
            self.beagle480.start_capture(immediate=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Lift mouse')
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=0, lift=True)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()
        self.post_requisite_reset_motion_emulator = True

        timings = []
        timer_id = TIMER.LOCAL
        excluded_keys = HidData.get_not_single_action_keys()
        initial_keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.get_group_size(test_case=self),
                                                       group_size=1, random=False, excluded_keys=excluded_keys)
        keys = initial_keys.copy()
        while len(keys) < LatencyTestCase.REPETITION_IN_SLEEP_MODE:
            keys.extend(initial_keys)
        # end while
        loop_count = ceil(LatencyTestCase.REPETITION / len(keys))

        test_count = 0
        for _ in range(loop_count):
            self.kosmos.sequencer.offline_mode = True
            for (key_id,) in keys:
                # Local timer initialization
                self.kosmos.timers.restart(timers=timer_id)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keypress on the supported key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=key_id)

                if self.use_beagle_analyser:
                    # PES will then wait for the Beagle signal
                    if self.current_channel.protocol == LogitechProtocol.USB:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                    else:
                        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                    # end if
                else:
                    # PES will then wait for the raspberry PI signal
                    self.kosmos.pes.wait_go_signal()
                # end if
                self.kosmos.timers.save(timers=timer_id)

                self.button_stimuli_emulator.multiple_keys_release(key_ids=[key_id],
                                                                   delay=ButtonStimuliInterface.DEFAULT_DELAY)
            # end for

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(block=False)

            for _ in keys:
                # Retrieve the HID reports
                self.check_hid_input(count=1, ble_notification_queue=ble_notification_queue)
                test_count += 1
            # end for

            # Wait for end of sequence execution
            self.kosmos.sequencer.wait_end_of_sequence()

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])
        # end for

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_switch_latency(timings=timings, title=self.short_name())
        # end if

        # Validate time marks
        self.assertGreaterEqual(len(timings), LatencyTestCase.REPETITION,
                                f'The number of test point is too low ({len(timings)} < {LatencyTestCase.REPETITION})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the switch press latency specification in Lift mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_switch_latency(timings=timings, lift_mode=True)
    # end def measure_and_validate_make_latency_in_lift_mode

    def measure_and_validate_xy_motion_in_run_mode(self, direction):
        """
        Measure and validate XY motion latency in run mode

        :param direction: X or Y motion. Possible values are X or Y
        :type direction: ``str``
        """
        assert direction in ['X', 'Y']
        if direction == 'X':
            x_motion = 1
            x_motion_before_after = 0
            y_motion = 0
            y_motion_before_after = 1
        else:
            x_motion = 0
            x_motion_before_after = 1
            y_motion = 1
            y_motion_before_after = 0
        # end if
        if self.use_beagle_analyser:
            endpoint = self.get_endpoint()
            beagle_channel = BeagleChannel.USB if self.current_channel.protocol == LogitechProtocol.USB else (
                BeagleChannel.WIRELESS)
            data_to_match = [0x00, 0x00, x_motion, 0x00, y_motion, 0x00]
            if direction == 'X':
                # We don't want to check delta Y because previous Y motion can be sent in the same report as X motion
                data_valid = [1, 1, 1, 1, 0, 0]
            else:
                # We don't want to check delta X because previous X motion can be sent in the same report as Y motion
                data_valid = [1, 1, 0, 0, 1, 1]
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure Beagle480 trigger and start the USB capture")
            # ----------------------------------------------------------------------------------------------------------
            self.beagle480 = Beagle480(test_case=self, channel_type=beagle_channel)
            self.beagle480.setup_digital_output(endpoint=endpoint, data=data_to_match, data_valid=data_valid)
            self.beagle480.start_capture(immediate=False)
        # end if

        # Min timing = elapsed time measured between the EXPECTED X/Y motion sensor polling and the detection of the
        # expected HID report
        min_timings = []
        # Max timing = elapsed time measured between the X/Y motion sensor polling who is before the EXPECTED X/Y
        # motion sensor polling and the detection of the expected HID report
        max_timings = []
        timer_id = TIMER.LOCAL
        # Some motion is performed on the other axis before the expected motion in order to stress the system
        repetition_before = randint(10, 20)
        # Some motion is performed on the other axis before the expected motion in order to stress the system
        # But this number of repetition must be enough bigger to have a latency duration smaller than the duration
        # until Sensor Emulator finishes its sequence
        repetition_after = 100
        loop_count = LatencyTestCase.REPETITION
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Move right or left on X axis by minimum motion resolution')
        # ----------------------------------------------------------------------------------------------------------
        for _ in range(loop_count):
            self.kosmos.sequencer.offline_mode = True
            if self.use_beagle_analyser:
                # Add motion before the expected one only if we use beagle analyser because in the other case we are
                # not able to differentiate HID reports
                self.motion_emulator.xy_motion(dx=x_motion_before_after, dy=y_motion_before_after,
                                               repetition=repetition_before - 1)
                self.motion_emulator.commit_actions()
            # end if
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion)
            self.motion_emulator.commit_actions()
            self.motion_emulator.xy_motion(dx=x_motion_before_after, dy=y_motion_before_after,
                                           repetition=repetition_after - 1)
            self.motion_emulator.commit_actions()
            # Start Sensor Emulator model update
            self.kosmos.pes.execute(action=self.motion_emulator.module.action_event.START)

            # Wait until Sensor Emulator finishes its sequence
            for i in range(repetition_before + 1):
                self.kosmos.pes.wait(action=self.motion_emulator.module.resume_event.UPDATE_DONE)
            # end for
            # Local timer initialization
            self.kosmos.timers.restart(timers=timer_id)
            # Wait until Sensor Emulator finishes its sequence
            self.kosmos.pes.wait(action=self.motion_emulator.module.resume_event.UPDATE_DONE)
            self.kosmos.timers.save(timers=timer_id)
            if self.use_beagle_analyser:
                # PES will then wait for the Beagle signal
                if self.current_channel.protocol == LogitechProtocol.USB:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[30])
                else:
                    self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.events.led_pin_resume_events[31])
                # end if
            else:
                # PES will then wait for the raspberry PI signal
                self.kosmos.pes.wait_go_signal()
            # end if
            self.kosmos.timers.save(timers=timer_id)

            # Wait until Sensor Emulator finishes its sequence
            self.kosmos.dt.pes.wait(action=self.motion_emulator.module.resume_event.FIFO_UNDERRUN)

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence()

            # Download time mark
            timemarks = self.kosmos.timers.download()
            max_timings.append(timemarks[timer_id][1])
            min_timings.append(timemarks[timer_id][1] - timemarks[timer_id][0])

            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for

        if self.use_beagle_analyser:
            self.beagle480.close()
        # end if

        if self.ENABLE_GRAPH:
            self.plot_motion_latency(min_timings=min_timings, max_timings=max_timings, title=self.short_name())
        # end if

        # Validate time marks
        self.assertGreaterEqual(len(min_timings), loop_count,
                                f'The number of test point is too low ({len(min_timings)} < {loop_count})')
        timings = min_timings + max_timings

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate the {direction} latency specification in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_motion_latency(timings=timings)
    # end def measure_and_validate_xy_motion_in_run_mode

    def measure_and_validate_x_motion_in_sleep_mode(self):
        """
        Measure and validate X motion latency in sleep mode
        """
        timings = []
        timer_id = TIMER.LOCAL

        loop_count = LatencyTestCase.REPETITION_IN_SLEEP_MODE
        for _ in range(loop_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep + 1)

            self.kosmos.sequencer.offline_mode = True
            # Local timer initialization
            self.kosmos.timers.restart(timers=timer_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Move right or left on X axis by minimum motion resolution')
            # ----------------------------------------------------------------------------------------------------------
            x_motion = choice(seq=[-1, 1])
            self.motion_emulator.xy_motion(dx=x_motion, dy=0)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            # PES will then wait for the raspberry PI signal
            self.kosmos.pes.wait_go_signal()
            self.kosmos.timers.save(timers=timer_id)
            # end for

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(block=False)

            # Retrieve the HID mouse report
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                  timeout=self.f.PRODUCT.DEVICE.F_MaxWaitSleep + 1)

            # Wait for end of sequence execution
            self.kosmos.sequencer.wait_end_of_sequence()

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])
        # end for

        # Validate time marks
        self.assertGreaterEqual(len(timings), loop_count,
                                f'The number of test point is too low ({len(timings)} < {loop_count})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the motion latency specification in sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_motion_latency(timings=timings)
    # end def measure_and_validate_x_motion_in_sleep_mode

    def measure_and_validate_x_motion_in_deep_sleep_mode(self):
        """
        Measure and validate X motion latency in deep sleep mode
        """
        timings = []
        timer_id = TIMER.LOCAL

        loop_count = LatencyTestCase.REPETITION_IN_SLEEP_MODE
        for _ in range(loop_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

            self.trigger_gpio_in_polling_callbacks(enabled=True)

            # Empty hid_message_queue
            ChannelUtils.clean_messages(
                test_case=self, channel=self.current_channel.receiver_channel, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)

            self.kosmos.sequencer.offline_mode = True
            # Local timer initialization
            self.kosmos.timers.restart(timers=timer_id)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Move right or left on X axis by minimum motion resolution')
            # ----------------------------------------------------------------------------------------------------------
            x_motion = choice(seq=[-1, 1])
            self.motion_emulator.xy_motion(dx=x_motion, dy=0)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            # PES will then wait for the raspberry PI signal
            self.kosmos.pes.wait_go_signal()
            self.kosmos.timers.save(timers=timer_id)

            self.kosmos.sequencer.offline_mode = False
            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(block=False)

            # Retrieve the HID mouse report
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # Wait for end of sequence execution
            self.kosmos.sequencer.wait_end_of_sequence()

            # Download time mark
            timemarks = self.kosmos.timers.download()
            timings.extend([timemarks[timer_id][index] for index in range(len(timemarks[timer_id]))])

            # Start polling all EPs
            self.trigger_gpio_in_polling_callbacks(enabled=False)
        # end for

        # Validate time marks
        self.assertEqual(LatencyTestCase.REPETITION_IN_SLEEP_MODE, len(timings),
                         f'The number of test point is not as expected ({len(timings)} < '
                         f'{LatencyTestCase.REPETITION_IN_SLEEP_MODE})')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the motion latency specification in deep sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.validate_motion_latency(timings=timings, deep_sleep_mode=True)
    # end def measure_and_validate_x_motion_in_deep_sleep_mode
# end class LatencyTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
