#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.timings.main_loop
:brief: Validate Main Loop processing time
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/11/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from sys import stdout
from time import sleep

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.rftest import RFTestModel
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformationResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.rttprofiler import Parser
from pylibrary.tools.rttprofiler import Profiler
from pylibrary.tools.rttprofiler import ProfilerExecutor
from pylibrary.tools.rttprofiler import RelativeMeasure
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.rftestutils import RFTestTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
# Results verification: minimum and maximum frequency values shall be in range -5%/+5%
_95_PERCENT = 95 / 100
_105_PERCENT = 105 / 100
# Results verification: average frequency value shall be in range -1%/+1%
_99_PERCENT = 99 / 100
_101_PERCENT = 101 / 100
# Statistics computation: Tolerance on start and end timings
END_TIME_TOLERANCE = 90 / 100
START_TIME_TOLERANCE = 110 / 100
# Capture: duration extension on sleep mode
CAPTURE_MARGIN = 2  # seconds

RTT_BUFFER_CHUNK_COUNT = 42
END_OF_STATUP_TAG = 444
MAIN_LOOP_START_TAG = 393
MAIN_LOOP_END_TAG = 787
# RTOS, 2kHz
# Fast tick frequency (TSTAG_FAST_TICK[N] - TSTAG_FAST_TICK[N-1])
FAST_TICK_START_TAG = 100
# Rx instant relatively to fast tick (TSTAG_RX[N] - TSTAG_FAST_TICK[N])
RX_START_TAG = 101
# Tx instant relatively to fast tick (TSTAG_TX[N] - TSTAG_FAST_TICK[N])
TX_START_TAG = 102

MAIN_LOOP_FREQUENCY = RelativeMeasure(MAIN_LOOP_START_TAG, MAIN_LOOP_START_TAG)
MAIN_LOOP_DURATION = RelativeMeasure(MAIN_LOOP_START_TAG, MAIN_LOOP_END_TAG)
FAST_TICK_FREQUENCY = RelativeMeasure(FAST_TICK_START_TAG, FAST_TICK_START_TAG)
RX_STARTING_TIME = RelativeMeasure(FAST_TICK_START_TAG, RX_START_TAG)
RX_FREQUENCY = RelativeMeasure(RX_START_TAG, RX_START_TAG)
TX_STARTING_TIME = RelativeMeasure(FAST_TICK_START_TAG, TX_START_TAG)

VERBOSE = False


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class INDEX:
    RUN = 0
    WALK = 1
    SLEEP = 2
    DEEP_SLEEP = 3
# end class INDEX


class TimingsTestCase(BaseTestCase):
    """
    Validate Core Timings TestCases
    """
    MODES = ['run', 'walk', 'sleep']
    MAIN_LOOP_MAX_DURATION = 1.2  # ms
    MAIN_LOOP_FREQUENCY = [4.2, 4.2, 81]  # run, walk, sleep in ms
    MAIN_LOOP_FREQUENCY_LS2 = [1.05, 1.05, 8.4]  # run, walk, sleep in ms
    """ On BLE PRO:
    The timer is driven by a 32.768 kHz clock with a pre-scaller of 33. 
    So each tick period is 33/32.768 = 1.007 ms (instead of 1 ms). 
    Therefore, the nominal value for the run mode loop is 4 * 33/32.768 = 4.028 ms. 
    And we add 5% margin to the maximum expected value => 4.23ms
    In addition, the nominal value in sleep mode loop for a Mouse with Rambo or EPM roller is 80 * 33/32.768 = 80.57ms. 
    So, a better test criteria would be 80.6 ms +/- 4 ms. """
    MAIN_LOOP_FREQUENCY_BLE_MSE_ROLLER = [4.23, 4.23, 84.6]  # run, walk, sleep in ms
    """ Likewise, the nominal value in sleep mode loop for all other products is 500 * 33/32.768 = 503.54 ms. 
    So, a better test criteria would be 503.54 ms +/- 25 ms. """
    MAIN_LOOP_FREQUENCY_BLE = [4.23, 4.23, 528.6]  # run, walk, sleep in ms

    # 2kHz Test Plan - 1.Timings - core
    MAIN_LOOP_FREQUENCY_LS2_2KHZ = [0.505, 0.505, 8.4]  # run, walk, sleep in ms
    MAIN_LOOP_FREQUENCY_LS2_1KHZ = [1.05, 1.05, 8.4]  # run, walk, sleep in ms
    # cf https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
    # Check Rx instant
    RX_INSTANT_2KHZ = [0.200, 0.200, 0.200]  # 200 us
    RX_INSTANT_1KHZ = [0.625, 0.625, 0.625]  # 625 us
    # Check Tx instant
    TX_INSTANT_2KHZ = [0.325, 0.325, 0.325]  # 325 us
    TX_INSTANT_1KHZ = [0.750, 0.750, 0.750]  # 750 us

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_unpluging_usb_cable = False
        self.post_requisite_onboard_mode = False
        self.feature_8061 = None

        super().setUp()

        self.parser = Parser()
        self.profiler = Profiler(END_OF_STATUP_TAG, RTT_BUFFER_CHUNK_COUNT)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Empty message queues')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queues(test_case=self)
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_unpluging_usb_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Unplug the USB cable to force the device back at 2kHz')
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_usb_channel(test_case=self)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_onboard_mode:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Force back the device in 2kHz mode')
                # ------------------------------------------------------------------------------------------------------
                ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(
                    test_case=self, report_rate=ExtendedAdjustableReportRate.RATE._2_KHz)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Configure the device in OnBoard mode')
                # ------------------------------------------------------------------------------------------------------
                OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(
                    test_case=self, onboard_mode=OnboardProfiles.Mode.ONBOARD_MODE)
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def _get_all_capture(self, capture_time, is_reset=True):
        """
        Create a complete capture of a given duration after an optional device reset

        :param capture_time: Recording time
        :type capture_time: ``float`` or ``str``
        :param is_reset: Flag indicating that the device will reset before starting the capture - OPTIONAL
        :type is_reset: ``bool``
        """
        profiler_exec = ProfilerExecutor(self.debugger.get_jlink(), self.parser, self.profiler)
        if is_reset:
            self.debugger._j_link.reset(halt=False)
        # end if
        profiler_exec.start_capture(self.debugger.get_rtt_address())
        sleep(capture_time)
        profiler_exec.stop_capture()
    # end def _get_all_capture

    def _log_statistics(self, tags, statistics):
        """
        Log the timing statistics into result files and optionally send them in the console output

        :param tags: tuple of start and end tags
        :type tags: ``RelativeMeasure[int, int]``
        :param statistics: Statistics with average, minimum and maximum values for each tag
        :type statistics: ``Statistics``
        """
        message = f"tag pair:{tags}, min:{statistics.min:.3f}, max:{statistics.max:.3f}, ave:{statistics.average:.3f}"
        if VERBOSE:
            stdout.write(f"{message}\n")
        # end if
        self.logTrace(msg=message)
    # end def _log_statistics
# en class TimingsTestCase(BaseTestCase):


class MainLoopTestCase(TimingsTestCase):
    """
    Validate MainLoop timings TestCases
    """

    @features('Timings')
    @level('Functionality')
    @services('Debugger')
    def test_processing_time(self):
        """
        Validate the main loop processing time
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Start the RTT Profiler thread')
        # --------------------------------------------------------------------------------------------------------------
        profiler_exec = ProfilerExecutor(self.debugger.get_jlink(), self.parser, self.profiler)
        profiler_exec.start_capture(self.debugger.get_rtt_address())
        sleep(3)
        profiler_exec.stop_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate main loop maximum duration')
        # --------------------------------------------------------------------------------------------------------------
        statistics = self.profiler.get_statistics((MAIN_LOOP_DURATION,))[MAIN_LOOP_DURATION]
        self.logTrace(msg=f"tag pair:{MAIN_LOOP_DURATION}, min:{statistics.min}, max:{statistics.max}, "
                          f"ave:{statistics.average}")
        self.assertGreater(a=self.MAIN_LOOP_MAX_DURATION,
                           b=statistics.max,
                           msg=f"Main loop duration exceed the expected value")

        self.testCaseChecked("FUN_TIME_0001")
    # end def test_processing_time

    @features('Timings')
    @level('Functionality')
    @services('Debugger')
    def test_frequency(self):
        """
        Validate the main loop frequency
        It is the time spent between two consecutive main loop execution (cf tag 'TSTAG_START_MLOOP').
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        if self.f.PRODUCT.F_IsGaming and self.f.PRODUCT.TIMINGS.F_2kHzSupport:
            expected_values = self.MAIN_LOOP_FREQUENCY_LS2_2KHZ
        elif self.f.PRODUCT.F_IsGaming:
            expected_values = self.MAIN_LOOP_FREQUENCY_LS2
        elif self.config_manager.current_protocol in (LogitechProtocol.BLE, LogitechProtocol.BLE_PRO):
            if self.f.PRODUCT.F_IsMice:
                expected_values = self.MAIN_LOOP_FREQUENCY_BLE_MSE_ROLLER
            else:
                expected_values = self.MAIN_LOOP_FREQUENCY_BLE
            # end if
        else:
            expected_values = self.MAIN_LOOP_FREQUENCY
        # end if

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):

            results = self.profiler.get_statistics(
                (MAIN_LOOP_FREQUENCY,), start=int(delay) * START_TIME_TOLERANCE,
                end=int(next_delay) * END_TIME_TOLERANCE)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate main loop average frequency for mode = {mode}')
            # ----------------------------------------------------------------------------------------------------------
            statistics = results[MAIN_LOOP_FREQUENCY]
            self._log_statistics(tags=MAIN_LOOP_FREQUENCY, statistics=statistics)
            self.assertGreater(a=max_frequency,
                               b=statistics.average,
                               msg=f"Main loop frequency exceed the expected value in mode = {mode}")
            # end for
        # end for
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0002")
    # end def test_frequency

    @features('Timings')
    @features('Feature1830powerMode', 1)
    @level('Functionality')
    @services('Debugger')
    def test_frequency_dead_mode(self):
        """
        Validate the main loop is never executed after switching in dead mode state
        (cf tag 'TSTAG_START_MLOOP').
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetPowerMode with powerModeNumber = 1 (DEAD_MODE)')
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Start the RTT Profiler thread')
        # --------------------------------------------------------------------------------------------------------------
        profiler_exec = ProfilerExecutor(self.debugger.get_jlink(), self.parser, self.profiler)
        profiler_exec.start_capture(self.debugger.get_rtt_address())
        sleep(.1)
        # Clean up the RTT buffer from data pushed before entering the Dead mode
        self.profiler.clear_data()
        # Retrieve RTT data during 1 second
        sleep(1)
        profiler_exec.stop_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate main loop is not executed anymore')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEquals(expected=0,
                          obtained=len(self.profiler._in_records),
                          msg="Main loop still processed after receiving switch to 'Dead mode' request, records: "
                              f"{self.profiler._in_records}")

        self.testCaseChecked("FUN_TIME_0003")
    # end def test_frequency_dead_mode

    @features('Timings')
    @level('Functionality')
    @services('Debugger')
    def test_startup_time(self):
        """
        Validate the device startup time after a soft reset
        """
        self._test_startup_time(soft_reset=True, acceptance_criteria=self.f.PRODUCT.TIMINGS.F_StartupTime)
        self.testCaseChecked("FUN_TIME_0004#1")
    # end def test_startup_time

    @features('Timings')
    @level('Functionality')
    @services('Debugger')
    def test_startup_time_hard_reset(self):
        """
        Validate the device startup time after a hardware reset
        """
        self._test_startup_time(
            soft_reset=False,
            acceptance_criteria=self.config_manager.get_feature(self.config_manager.ID.STARTUP_TIME_COLD_BOOT))
        self.testCaseChecked("FUN_TIME_0004#2")
    # end def test_startup_time_hard_reset

    def _test_startup_time(self, acceptance_criteria, soft_reset=True):
        """
        Validate the device startup time
        It is the time spent between the reset and the entry in the main loop (cf tag 'TSTAG_END_INIT_SEQUENCE').

        :param acceptance_criteria: Maximum accepted start up time in ms
        :type acceptance_criteria: ``int``
        :param soft_reset: flag to select between a soft reset and an emulated power on reset - OPTIONAL
        :type soft_reset: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the device after starting the RTT Profiler thread')
        # --------------------------------------------------------------------------------------------------------------
        profiler_exec = ProfilerExecutor(self.debugger.get_jlink(), self.parser, self.profiler)
        self.debugger._j_link.reset(halt=True)
        profiler_exec.start_capture(self.debugger.get_rtt_address())
        self.device_debugger.reset(soft_reset=soft_reset)
        sleep(acceptance_criteria / 1000 + 0.2)
        profiler_exec.stop_capture()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate firmware startup time')
        # --------------------------------------------------------------------------------------------------------------
        startup_time = self.profiler.get_startup_time_msec()
        self.assertNotNone(startup_time, "Startup tag not found in processed data")
        self.logTrace(msg=f"Start-up time: {startup_time}")
        self.assertGreater(a=float(acceptance_criteria),
                           b=startup_time,
                           msg=f"Startup time is greater than expected: {startup_time} > {acceptance_criteria} ms")
    # end def _test_startup_time
# end class MainLoopTestCase


class MainLoop2kHzTestCase(TimingsTestCase):
    """
    Validate MainLoop 2kHz timings TestCases
    """

    @features('2kHzTimings')
    @level('Functionality')
    @services('Debugger')
    def test_rx_starting_time(self):
        """
        Validate RX instant at 2kHz
        It is the time spent between the 'TSTAG_FAST_TICK' tag and the 'TSTAG_RX' tag.

        cf 2kHz Test Plan section 1.2 - Check Rx instant = 200us
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        expected_values = self.RX_INSTANT_2KHZ

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):
            results = self.profiler.get_statistics(
                (RX_STARTING_TIME,), start=int(delay) * START_TIME_TOLERANCE, end=int(next_delay) * END_TIME_TOLERANCE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate RX instant at 2kHz for mode = {mode}')
            # ----------------------------------------------------------------------------------------------------------
            statistics = results[RX_STARTING_TIME]
            self._log_statistics(tags=RX_STARTING_TIME, statistics=statistics)
            # Minimum and Maximum values shall be in range -5%/+5%
            self.assertLess(a=max_frequency * _95_PERCENT,
                            b=statistics.min,
                            msg=f"minimum RX instant at 2kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _105_PERCENT,
                               b=statistics.max,
                               msg=f"maximum RX instant at 2kHz exceed the expected value in mode = {mode}")
            # Average value shall be in range -1%/+1%
            self.assertLess(a=max_frequency * _99_PERCENT,
                            b=statistics.average,
                            msg=f"average RX instant at 2kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _101_PERCENT,
                               b=statistics.average,
                               msg=f"average RX instant at 2kHz exceed the expected value in mode = {mode}")
        # end for
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0010")
    # end def test_rx_starting_time

    @features('2kHzTimings')
    @features('Feature8061')
    @level('Functionality')
    @services('Debugger')
    def test_rx_starting_time_at_1kHz(self):
        """
        Validate RX instant at 1kHz
        It is the time spent between the 'TSTAG_FAST_TICK' tag and the 'TSTAG_RX' tag.

        cf 2kHz Test Plan section 1.5 - Check Rx instant = 625us
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Configure the device at 1kHz')
        # --------------------------------------------------------------------------------------------------------------
        self._set_report_rate()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        expected_values = self.RX_INSTANT_1KHZ

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN, is_reset=False)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):
            results = self.profiler.get_statistics(
                (RX_STARTING_TIME,), start=int(delay) * START_TIME_TOLERANCE, end=int(next_delay) * END_TIME_TOLERANCE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate RX instant at 1kHz for mode = {mode}')
            # ----------------------------------------------------------------------------------------------------------
            statistics = results[RX_STARTING_TIME]
            self._log_statistics(tags=RX_STARTING_TIME, statistics=statistics)
            # Minimum and Maximum values shall be in range -5%/+5%
            self.assertLess(a=max_frequency * _95_PERCENT,
                            b=statistics.min,
                            msg=f"minimum RX instant at 1kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _105_PERCENT,
                               b=statistics.max,
                               msg=f"maximum RX instant at 1kHz exceed the expected value in mode = {mode}")
            # Average value shall be in range -1%/+1%
            self.assertLess(a=max_frequency * _99_PERCENT,
                            b=statistics.average,
                            msg=f"average RX instant at 1kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _101_PERCENT,
                               b=statistics.average,
                               msg=f"average RX instant at 1kHz exceed the expected value in mode = {mode}")
        # end for
        self.profiler.clear_data()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_TIME_0011")
    # end def test_rx_starting_time_at_1kHz

    @features('2kHzTimings')
    @level('Functionality')
    @services('Debugger')
    def test_tx_starting_time(self):
        """
        Validate TX instant at 2kHz
        It is the time spent between the 'TSTAG_FAST_TICK' tag and the 'TSTAG_TX' tag.

        cf 2kHz Test Plan section 1.3 - Check Tx instant = 325us
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        expected_values = self.TX_INSTANT_2KHZ

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):
            results = self.profiler.get_statistics(
                (TX_STARTING_TIME,), start=int(delay) * START_TIME_TOLERANCE, end=int(next_delay) * END_TIME_TOLERANCE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate TX instant at 2kHz for mode = {mode}')
            # ----------------------------------------------------------------------------------------------------------
            statistics = results[TX_STARTING_TIME]
            self._log_statistics(tags=TX_STARTING_TIME, statistics=statistics)
            # Minimum and Maximum values shall be in range -5%/+5%
            self.assertLess(a=max_frequency * _95_PERCENT,
                            b=statistics.min,
                            msg=f"minimum TX instant at 2kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _105_PERCENT,
                               b=statistics.max,
                               msg=f"maximum TX instant at 2kHz exceed the expected value in mode = {mode}")
            # Average value shall be in range -1%/+1%
            self.assertLess(a=max_frequency * _99_PERCENT,
                            b=statistics.average,
                            msg=f"average TX instant at 2kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _101_PERCENT,
                               b=statistics.average,
                               msg=f"average TX instant at 2kHz exceed the expected value in mode = {mode}")
        # end for
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0012")
    # end def test_tx_starting_time

    @features('2kHzTimings')
    @features('Feature8061')
    @level('Functionality')
    @services('Debugger')
    def test_tx_starting_time_at_1kHz(self):
        """
        Validate TX instant at 1kHz
        It is the time spent between the 'TSTAG_FAST_TICK' tag and the 'TSTAG_TX' tag.

        cf 2kHz Test Plan section 1.6 - Check Tx instant = 750us
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Configure the device at 1kHz')
        # --------------------------------------------------------------------------------------------------------------
        self._set_report_rate()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        expected_values = self.TX_INSTANT_1KHZ

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN, is_reset=False)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):
            results = self.profiler.get_statistics(
                (TX_STARTING_TIME,), start=int(delay) * START_TIME_TOLERANCE, end=int(next_delay) * END_TIME_TOLERANCE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate TX instant at 1kHz for mode = {mode}')
            # ----------------------------------------------------------------------------------------------------------
            statistics = results[TX_STARTING_TIME]
            self._log_statistics(tags=TX_STARTING_TIME, statistics=statistics)
            # Minimum and Maximum values shall be in range -5%/+5%
            self.assertLess(a=max_frequency * _95_PERCENT,
                            b=statistics.min,
                            msg=f"minimum TX instant at 1kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _105_PERCENT,
                               b=statistics.max,
                               msg=f"maximum TX instant at 1kHz exceed the expected value in mode = {mode}")
            # Average value shall be in range -1%/+1%
            self.assertLess(a=max_frequency * _99_PERCENT,
                            b=statistics.average,
                            msg=f"average TX instant at 1kHz is lower than the minimum expected value in mode = {mode}")
            self.assertGreater(a=max_frequency * _101_PERCENT,
                               b=statistics.average,
                               msg=f"average TX instant at 1kHz exceed the expected value in mode = {mode}")
        # end for
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0013")
    # end def test_tx_starting_time_at_1kHz

    @features('2kHzTimings')
    @features('Feature8061')
    @level('Functionality')
    @services('Debugger')
    def test_fast_trick_frequency_at_2khz(self):
        """
        Validate fast trick frequency shall be 2kHz by default

        cf 2kHz Test Plan section 1.1 - Check rtos delivers 500us - fast tick
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the device is configured by default to 2kHz')
        # --------------------------------------------------------------------------------------------------------------
        report_rate = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(test_case=self,
                                                                                        connection_type=1)
        self.assertEquals(ExtendedAdjustableReportRate.RATE._2_KHz, to_int(report_rate.report_rate),
                          msg='The DUT shall be configured at a 2kHz report rate by default')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        expected_values = self.MAIN_LOOP_FREQUENCY_LS2_2KHZ

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):
            results = self.profiler.get_statistics(
                (FAST_TICK_FREQUENCY,), start=int(delay) * START_TIME_TOLERANCE,
                end=int(next_delay) * END_TIME_TOLERANCE)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate fast trick max frequency for mode = {mode}')
            # ----------------------------------------------------------------------------------------------------------
            statistics = results[FAST_TICK_FREQUENCY]
            self._log_statistics(tags=FAST_TICK_FREQUENCY, statistics=statistics)
            self.assertGreater(a=max_frequency,
                               b=statistics.max,
                               msg=f"Main loop frequency exceed the expected value in mode = {mode}")
        # end for
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0014")
    # end def test_fast_trick_frequency_at_2khz

    @features('2kHzTimings')
    @features('Feature8061')
    @level('Functionality')
    @services('Debugger')
    def test_fast_trick_frequency_at_1khz(self):
        """
        Validate fast trick frequency when the user requests 1kHz report rate
        Then validate fast trick frequency when the user requests 2kHz report rate

        cf 2kHz Test Plan section 1.4 Check rtos delivers 1ms - fast tick
        and 2kHz Test Plan section 4.2 Any other rate, fast tick must be 1ms
        then 2kHz Test Plan section 4.1 - 2kHz requested, fast tick must be 500us
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Configure the device at 1kHz')
        # --------------------------------------------------------------------------------------------------------------
        self._set_report_rate()

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # ---------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        expected_values = self.MAIN_LOOP_FREQUENCY_LS2_1KHZ

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN, is_reset=False)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):
            results = self.profiler.get_statistics(
                (FAST_TICK_FREQUENCY,), start=int(delay) * START_TIME_TOLERANCE,
                end=int(next_delay) * END_TIME_TOLERANCE)
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate fast trick max frequency for mode = {mode}')
            # ---------------------------------------------------------------------------
            statistics = results[FAST_TICK_FREQUENCY]
            self._log_statistics(tags=FAST_TICK_FREQUENCY, statistics=statistics)
            self.assertGreater(a=max_frequency,
                               b=statistics.max,
                               msg=f"Main loop frequency exceed the expected value in mode = {mode}")
        # end for
        self.profiler.clear_data()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Configure back the device at 2kHz')
        # --------------------------------------------------------------------------------------------------------------
        self._set_report_rate(rate=ExtendedAdjustableReportRate.RATE._2_KHz)

        self._get_all_capture(int(pm_delay_list[INDEX.RUN]), is_reset=False)
        results = self.profiler.get_statistics((MAIN_LOOP_FREQUENCY,))
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate main loop max frequency at 2kHz')
        # ----------------------------------------------------------------------------------------------------------
        statistics = results[MAIN_LOOP_FREQUENCY]
        self._log_statistics(tags=MAIN_LOOP_FREQUENCY, statistics=statistics)
        self.assertGreater(a=self.MAIN_LOOP_FREQUENCY_LS2_2KHZ[0],
                           b=statistics.max,
                           msg=f"Main loop frequency exceed the expected value at 2kHz")
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0015")
    # end def test_fast_trick_frequency_at_1khz

    @features('2kHzTimings')
    @features('Feature8061')
    @level('Functionality')
    @services('Debugger')
    def test_fast_trick_frequency_at_500hz(self):
        """
        Validate fast trick frequency when the user requests 500Hz report rate

        cf 2kHz Test Plan section 4.2 Any other rate, fast tick must be 1ms
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Configure the device at 500Hz')
        # --------------------------------------------------------------------------------------------------------------
        self._set_report_rate(rate=ExtendedAdjustableReportRate.RATE._500_Hz)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        pm_delay_list = self.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay
        expected_values = self.MAIN_LOOP_FREQUENCY_LS2_1KHZ

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get a complete capture covering all the supported modes")
        # ----------------------------------------------------------------------------------------------------------
        self._get_all_capture(int(pm_delay_list[INDEX.SLEEP]) + CAPTURE_MARGIN, is_reset=False)

        for mode, delay, next_delay, max_frequency in zip(self.MODES, pm_delay_list[:-1], pm_delay_list[1:],
                                                          expected_values):
            results = self.profiler.get_statistics(
                (FAST_TICK_FREQUENCY,), start=int(delay) * START_TIME_TOLERANCE,
                end=int(next_delay) * END_TIME_TOLERANCE)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate fast trick max frequency for mode = {mode}')
            # ----------------------------------------------------------------------------------------------------------
            statistics = results[FAST_TICK_FREQUENCY]
            self._log_statistics(tags=FAST_TICK_FREQUENCY, statistics=statistics)
            self.assertGreater(a=max_frequency,
                               b=statistics.max,
                               msg=f"Main loop frequency exceed the expected value in mode = {mode}")
        # end for
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0016")
    # end def test_fast_trick_frequency_at_500hz

    def _check_supported_report_rate(self, rate=ExtendedAdjustableReportRate.RATE._1_KHz):
        """
        Check if the device supports the required configuration

        :param rate: Report rate requested value
        :type rate: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Get the report rates supported by the device')
        # --------------------------------------------------------------------------------------------------------------
        device_capabilities = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_device_capabilities(
            test_case=self, connection_type=1)
        ExtendedAdjustableReportRateTestUtils.GetDeviceCapabilitiesResponseChecker.check_fields(
            test_case=self, message=device_capabilities,
            expected_cls=self.feature_8061.get_device_capabilities_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Get the actual report rate list')
        # --------------------------------------------------------------------------------------------------------------
        actual_report_rate_list = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_actual_report_rate_list(
            test_case=self)
        ExtendedAdjustableReportRateTestUtils.GetActualReportRateListResponseChecker.check_fields(
            test_case=self, message=actual_report_rate_list,
            expected_cls=self.feature_8061.get_actual_report_rate_list_response_cls)

        if rate == ExtendedAdjustableReportRate.RATE._2_KHz:
            self.assertTrue(device_capabilities.report_rate_list.rate_2khz == 1, msg='2kHz not supported by the DUT')
            self.assertTrue(actual_report_rate_list.report_rate_list.rate_2khz == 1,
                            msg='2kHz not listed by the DUT')
        elif rate == ExtendedAdjustableReportRate.RATE._1_KHz:
            self.assertTrue(device_capabilities.report_rate_list.rate_1khz == 1, msg='1kHz not supported by the DUT')
            self.assertTrue(actual_report_rate_list.report_rate_list.rate_1khz == 1,
                            msg='1kHz not listed by the DUT')
        elif rate == ExtendedAdjustableReportRate.RATE._500_Hz:
            self.assertTrue(device_capabilities.report_rate_list.rate_500hz == 1, msg='500Hz not supported by the DUT')
            self.assertTrue(actual_report_rate_list.report_rate_list.rate_500hz == 1,
                            msg='500Hz not listed by the DUT')
        # end if
    # end def _check_supported_report_rate

    def _configure_report_rate(self, rate=ExtendedAdjustableReportRate.RATE._1_KHz):
        """
        Set the device to Host mode then set the given report rate value

        :param rate: Report rate requested value
        :type rate: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Configure the device in Host mode')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_onboard_mode = True
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(
            test_case=self, onboard_mode=OnboardProfiles.Mode.HOST_MODE)
        response = OnboardProfilesTestUtils.HIDppHelper.get_onboard_mode(test_case=self)
        self.assertTrue(to_int(response.onboard_mode) == OnboardProfiles.Mode.HOST_MODE,
                        msg='The DUT shall be configured in Host Mode')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Force the device to report rate value = {rate}')
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=rate)

        report_rate = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
            test_case=self, connection_type=1)
        check_map = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker.get_default_check_map(
            test_case=self)
        check_map["report_rate"] = (
            ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker.check_report_rate, rate)
        ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker.check_fields(
            test_case=self, message=report_rate, expected_cls=self.feature_8061.get_report_rate_response_cls,
            check_map=check_map)
    # end def _configure_report_rate

    def _set_report_rate(self, rate=ExtendedAdjustableReportRate.RATE._1_KHz):
        """
        Check if the device supports the required configuration, set it to Host mode then set the report
        rate to the given value

        :param rate: Report rate requested value
        :type rate: ``int``
        """
        _, self.feature_8061, _, _ = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_parameters(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Check the device supports the required configuration')
        # --------------------------------------------------------------------------------------------------------------
        self._check_supported_report_rate(rate=rate)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Configure the given report rate')
        # --------------------------------------------------------------------------------------------------------------
        self._configure_report_rate(rate=rate)
    # end def _configure_report_rate_to_1kHz
# end class MainLoop2kHzTestCase


class MainLoop2kHzUSBTestCase(TimingsTestCase):
    """
    Validate MainLoop 2kHz USB transition timings TestCases
    """
    # TODO - enable following line when available
    # PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

    @features('2kHzTimings')
    @features("USB")
    @level('Functionality')
    @services('Debugger')
    def test_no_fast_trick_usb_plugged(self):
        """
        Validate fast trick module is not called at 1kHz

        cf 2kHz Test Plan section 4.2 Any other rate, fast tick must be 1ms
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Plug in the USB cable to force the USB protocol')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unpluging_usb_cable = True
        ProtocolManagerUtils.switch_to_usb_channel(test_case=self)

        self._get_all_capture(capture_time=3, is_reset=False)
        results = self.profiler.get_statistics((FAST_TICK_FREQUENCY,))
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate fast trick max frequency when USB cable is plugged')
        # ----------------------------------------------------------------------------------------------------------
        statistics = results[FAST_TICK_FREQUENCY]
        self._log_statistics(tags=FAST_TICK_FREQUENCY, statistics=statistics)
        self.assertEqual(expected=0.0, obtained=statistics.max,
                         msg=f"Main loop frequency exceed the expected value when USB cable is plugged")

        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0030")
    # end def test_no_fast_trick_usb_plugged

    @features('2kHzTimings')
    @features("USB")
    @level('Functionality')
    @services('Debugger')
    def test_main_loop_frequency_usb_plugged(self):
        """
        Validate main loop frequency when USB cable is plugged
        It is the time spent between the 2 consecutives 'TSTAG_RX' tags.

        cf 2kHz Test Plan section 5.1 Protocol transitions 2kHz --> USB
        https://docs.google.com/spreadsheets/d/1JHoC_RGqQRpmbDldE11JczIsLT5UZK0XPrW3JD9eCCU/edit#gid=0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Plug in the USB cable to force the USB protocol')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unpluging_usb_cable = True
        self.device.turn_on_usb_charging_cable()

        self._get_all_capture(capture_time=3, is_reset=False)
        results = self.profiler.get_statistics((RX_FREQUENCY,))
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate main loop frequency when USB cable is plugged')
        # ----------------------------------------------------------------------------------------------------------
        statistics = results[RX_FREQUENCY]
        self._log_statistics(tags=RX_FREQUENCY, statistics=statistics)
        self.assertGreater(a=self.MAIN_LOOP_FREQUENCY_LS2_1KHZ[0],
                           b=statistics.max,
                           msg=f"Main loop frequency exceed the expected value when USB cable is plugged")
        self.profiler.clear_data()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Unplug the USB cable to force the LS2 protocol')
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_off_usb_charging_cable()

        self._get_all_capture(capture_time=3, is_reset=False)
        results = self.profiler.get_statistics((MAIN_LOOP_FREQUENCY,))
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate main loop frequency when USB cable is unplugged')
        # ----------------------------------------------------------------------------------------------------------
        statistics = results[MAIN_LOOP_FREQUENCY]
        self._log_statistics(tags=MAIN_LOOP_FREQUENCY, statistics=statistics)
        self.assertGreater(a=self.MAIN_LOOP_FREQUENCY_LS2_1KHZ[0],
                           b=statistics.max,
                           msg=f"Main loop frequency exceed the expected value when USB cable is plugged")
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0031")
    # end def test_main_loop_frequency_usb_plugged
# end class MainLoop2kHzUSBTestCase


class MainLoop2kHzRFTestTestCase(TimingsTestCase):
    """
    Validate main loop 2kHz timings test cases in conjonction with RF processing
    """

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Reset the DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.hardware_reset()
        # end with

        super().tearDown()
    # end def tearDown

    @features('2kHzTimings')
    @features('Feature1890')
    @level('Functionality')
    @services('Debugger')
    def test_frequency_with_rf_test(self):
        """
        Validate the main loop frequency when RF Test is on going
        It is the time spent between two consecutive main loop execution (cf tag 'TSTAG_START_MLOOP').
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Enable RF transmision using 0x1890 feature')
        # --------------------------------------------------------------------------------------------------------------
        self._call_rf_test_function(index=RFTestModel.INDEX.RF_SEND_PERIODIC_MSG, seconds=3)

        self._get_all_capture(capture_time=3, is_reset=False)
        results = self.profiler.get_statistics((MAIN_LOOP_FREQUENCY,))
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate main loop max frequency when RF Test is on going')
        # ----------------------------------------------------------------------------------------------------------
        statistics = results[MAIN_LOOP_FREQUENCY]
        self._log_statistics(tags=MAIN_LOOP_FREQUENCY, statistics=statistics)
        self.assertGreater(a=self.MAIN_LOOP_FREQUENCY_LS2_2KHZ[0],
                           b=statistics.max,
                           msg=f"Main loop frequency exceed the expected value when RF Test is on going")
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0020")
    # end def test_frequency_with_rf_test

    @features('2kHzTimings')
    @features('Feature1890')
    @level('Functionality')
    @services('Debugger')
    def test_rx_starting_time_with_rf_test(self):
        """
        Validate RX instant at 2kHz when RF Test is on going
        It is the time spent between the 'TSTAG_FAST_TICK' tag and the 'TSTAG_RX' tag.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Enable RF transmision using 0x1890 feature')
        # --------------------------------------------------------------------------------------------------------------
        self._call_rf_test_function(index=RFTestModel.INDEX.RF_TX_CW, seconds=3)

        self._get_all_capture(capture_time=3, is_reset=False)
        results = self.profiler.get_statistics((RX_STARTING_TIME,))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate RX instant at 2kHz when RF Test is on going')
        # --------------------------------------------------------------------------------------------------------------
        statistics = results[RX_STARTING_TIME]
        self._log_statistics(tags=RX_STARTING_TIME, statistics=statistics)
        # Minimum and Maximum values shall be in range -5%/+5%
        self.assertLess(
            a=self.RX_INSTANT_2KHZ[0] * _95_PERCENT, b=statistics.min,
            msg=f"minimum RX instant at 2kHz is lower than the minimum expected value when RF Test is on going")
        self.assertGreater(
            a=self.RX_INSTANT_2KHZ[0] * _105_PERCENT, b=statistics.max,
            msg=f"maximum RX instant at 2kHz exceed the expected value in mode when RF Test is on going")
        # Average value shall be in range -1%/+1%
        self.assertLess(
            a=self.RX_INSTANT_2KHZ[0] * _99_PERCENT, b=statistics.average,
            msg=f"average RX instant at 2kHz is lower than the minimum expected value when RF Test is on going")
        self.assertGreater(
            a=self.RX_INSTANT_2KHZ[0] * _101_PERCENT, b=statistics.average,
            msg=f"average RX instant at 2kHz exceed the expected value when RF Test is on going")
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0021")
    # end def test_rx_starting_time_with_rf_test

    @features('2kHzTimings')
    @features('Feature1890')
    @level('Functionality')
    @services('Debugger')
    def test_tx_starting_time_with_rf_test(self):
        """
        Validate RX instant at 2kHz when RF Test is on going
        It is the time spent between the 'TSTAG_FAST_TICK' tag and the 'TSTAG_TX' tag.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Enable RF transmision using 0x1890 feature')
        # --------------------------------------------------------------------------------------------------------------
        self._call_rf_test_function(index=RFTestModel.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK, seconds=3)

        self._get_all_capture(capture_time=3, is_reset=False)
        results = self.profiler.get_statistics((TX_STARTING_TIME,))

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate RX instant at 2kHz when RF Test is on going')
        # ----------------------------------------------------------------------------------------------------------
        statistics = results[TX_STARTING_TIME]
        self._log_statistics(tags=TX_STARTING_TIME, statistics=statistics)
        # Minimum and Maximum values shall be in range -5%/+5%
        self.assertLess(
            a=self.TX_INSTANT_2KHZ[0] * _95_PERCENT, b=statistics.min,
            msg=f"minimum TX instant at 2kHz is lower than the minimum expected value when RF Test is on going")
        self.assertGreater(
            a=self.TX_INSTANT_2KHZ[0] * _105_PERCENT, b=statistics.max,
            msg=f"maximum TX instant at 2kHz exceed the expected value in mode when RF Test is on going")
        # Average value shall be in range -1%/+1%
        self.assertLess(
            a=self.TX_INSTANT_2KHZ[0] * _99_PERCENT, b=statistics.average,
            msg=f"average TX instant at 2kHz is lower than the minimum expected value when RF Test is on going")
        self.assertGreater(
            a=self.TX_INSTANT_2KHZ[0] * _101_PERCENT, b=statistics.average,
            msg=f"average TX instant at 2kHz exceed the expected value when RF Test is on going")
        self.profiler.clear_data()

        self.testCaseChecked("FUN_TIME_0022")
    # end def test_tx_starting_time_with_rf_test

    def _call_rf_test_function(self, index, seconds):
        """
        Call the function of the 0x1890 RF Test HID++ feature matching the given feature index

        :param index: RF Test function index in [0, 1, 5]
        :type index: ``int``
        :param seconds: timeout in seconds
        :type seconds: ``int``
        """
        assert index in [RFTestModel.INDEX.RF_SEND_PERIODIC_MSG, RFTestModel.INDEX.RF_TX_CW,
                         RFTestModel.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK], f'function index {index} not supported'
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Retrieve the receiver Equad address")
        # --------------------------------------------------------------------------------------------------------------
        device_index = ChannelUtils.get_device_index(test_case=self)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.current_channel.receiver_channel)
        equad_info_request = GetTransceiverEQuadInformation()
        equad_info_response = ChannelUtils.send(
            test_case=self,
            report=equad_info_request,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetTransceiverEQuadInformationResponse)
        equad_address = equad_info_response.base_address + HexList(device_index)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        if index == RFTestModel.INDEX.RF_SEND_PERIODIC_MSG:
            nbmsg = seconds * 1000
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send 0x1890 RF Test RFSendPeriodicMsg request")
            # ----------------------------------------------------------------------------------------------------------
            # Device sends periodic message
            RFTestTestUtils.HIDppHelper.rf_send_periodic_msg(test_case=self, address=equad_address,
                                                             channel=equad_info_response.rf_channel_index, period=1,
                                                             nbmsg=nbmsg, radio_mode=2, send_only=True)
        elif index == RFTestModel.INDEX.RF_TX_CW:
            # Convert seconds in 10 milliseconds
            timeout = seconds * 100
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send 0x1890 RF Test RFTxCW request")
            # ----------------------------------------------------------------------------------------------------------
            # Device configures its transmitter to send a true continuous wave for 3 second
            RFTestTestUtils.HIDppHelper.rf_tx_cw(test_case=self, channel=equad_info_response.rf_channel_index,
                                                 timeout=timeout, send_only=True)
        elif index == RFTestModel.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK:
            nbmsg = seconds * 1000
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send 0x1890 RF Test RFSendPeriodicMsgNoAck request")
            # ----------------------------------------------------------------------------------------------------------
            # Device sends periodic message
            RFTestTestUtils.HIDppHelper.rf_send_periodic_msg_no_ack(
                test_case=self, address=equad_address, channel=equad_info_response.rf_channel_index, period=1,
                nbmsg=nbmsg, radio_mode=2, send_only=True)
        # end if
    # end def _call_rf_test_function
# end class MainLoop2kHzRFTestTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
