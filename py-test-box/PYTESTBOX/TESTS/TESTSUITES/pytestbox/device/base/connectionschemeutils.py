#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.device.base.connectionschemeutils
    :brief:  Helpers for BLE Pro Connection Scheme feature
    :author: Christophe Roquebert
    :date: 2020/08/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from warnings import warn

from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.tools.hexlist import HexList
from pyraspi.services.kosmos.kosmosledspy import KosmosLedSpy
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_MILLI_SEC
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleProConnectionSchemeTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers on device BLE Pro connection scheme feature
    """

    class NvsHelper:
        """
        Non Volatile Memory Helper class
        """

        @classmethod
        def invalidate_connect_id_chunks(cls, test_case):
            """
            Invalidate all Connect Id chunks in NVS to emulate a return to OOB state.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            # Dump Device NVS
            test_case.memory_manager.read_nvs()
            # Extract Connect Id chunks
            invalidated_chunk_count = test_case.memory_manager.invalidate_chunks(['NVS_CONNECT_ID',
                                                                                  'NVS_BTLDR_CONNECT_ID'])
            if invalidated_chunk_count > 0:
                test_case.memory_manager.load_nvs()
            # end if
        # end def invalidate_connect_id_chunks

        @classmethod
        def unpair_host(cls, test_case, host_index, oob=False):
            """
            Invalidate all pairing chunks related to the first slot to emulate an unpaired use case.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param host_index: Host index to activate
            :type host_index: ``int``
            :param oob: Force oob state on all host indexes
            :type oob: ``bool``
            """
            if test_case.device_memory_manager is not None:
                # Dump Device NVS
                test_case.device_memory_manager.read_nvs()
                # Extract connect chunks
                bootloader_connect_id_chunk = \
                    test_case.device_memory_manager.get_active_chunk_by_name('NVS_BTLDR_CONNECT_ID')
                connect_id_chunk = test_case.device_memory_manager.get_active_chunk_by_name('NVS_CONNECT_ID')
                # Update host index values
                bootloader_connect_id_chunk.host_idx = host_index
                connect_id_chunk.data.host_index = host_index
                if oob:
                    # Force an OOB state to all supported host indexes
                    connect_id_chunk.data.scheme_host_0 = ConnectIdChunkData.STATUS.OOB
                    if hasattr(connect_id_chunk.data, 'scheme_host_1'):
                        connect_id_chunk.data.scheme_host_1 = ConnectIdChunkData.STATUS.OOB
                    # end if
                    if hasattr(connect_id_chunk.data, 'scheme_host_2'):
                        connect_id_chunk.data.scheme_host_2 = ConnectIdChunkData.STATUS.OOB
                    # end if
                    connect_id_chunk.data.pairing_src_0 = ConnectIdChunkData.PairingSrc.NONE
                    if hasattr(connect_id_chunk.data, 'pairing_src_1'):
                        connect_id_chunk.data.pairing_src_1 = ConnectIdChunkData.PairingSrc.NONE
                    # end if
                    if hasattr(connect_id_chunk.data, 'pairing_src_2'):
                        connect_id_chunk.data.pairing_src_2 = ConnectIdChunkData.PairingSrc.NONE
                    # end if
                else:
                    # Force the given host to OOB state
                    if hasattr(connect_id_chunk.data, f'scheme_host_{host_index}'):
                        connect_id_chunk.data.setValue(
                            connect_id_chunk.data.getFidFromName(f'scheme_host_{host_index}'),
                            ConnectIdChunkData.STATUS.OOB)
                    # end if
                # end if
                # Create 2 new chunks with the new configuration
                test_case.device_memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_BTLDR_CONNECT_ID', data=HexList(
                    bootloader_connect_id_chunk))
                test_case.device_memory_manager.nvs_parser.add_new_chunk(
                    chunk_id='NVS_CONNECT_ID', data=HexList(connect_id_chunk))
                # Update the device memory
                test_case.device_memory_manager.load_nvs()
            # end if
        # end def unpair_host
    # end class NvsHelper

    class LedSpyHelper:
        """
        LEDs spy module Helper class
        """
        THIRTY_TWO_MILLI = 32
        THREE_MINUTES = 180000
        FIVE_SECONDS = 5000
        THREE_SECONDS = 3000
        ONE_SECOND = 1000
        HUNDRED_MILLISECOND = 100

        class POSITION:
            """
            Timeline cursor position. We shall select ``FIRST`` to start from the beginning, ``NEXT`` to take the
            next transition on the timeline or ``ANY`` to find the first transition with a matching scheme type.
            """
            FIRST = 0
            NEXT = 1
            ANY = 2
        # end class POSITION

        @classmethod
        def start_monitoring(cls, test_case, led_identifiers):
            """
            Start the connectivity status LEDs monitoring period.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_identifiers: List of LED to start monitoring
            :type led_identifiers: ``list[pylibrary.emulator.ledid.LED_ID]``
            """
            test_case.led_timeline = None
            if test_case.led_spy is not None:
                # enable LED monitoring on the given list of LED
                test_case.led_spy.start(led_identifiers)
            elif test_case.led_spy_over_i2c is not None:
                # enable I2C monitoring
                test_case.led_spy_over_i2c.start(led_identifiers=led_identifiers)
            # end if
        # end def start_monitoring

        @classmethod
        def start_monitoring_when_device_is_off(cls, test_case, led_identifiers, off_on_time=1):
            """
            Define the sequence between LEDs monitoring start and DUT power on according to the services available.

            If a power slider is present, start the connectivity LEDs monitoring when device is off then power on
            the device. Else start the connectivity LEDs monitoring then reset the device with debugger

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_identifiers: List of LED to start monitoring
            :type led_identifiers: ``list[pylibrary.emulator.ledid.LED_ID]``
            :param off_on_time: duration between power off and power on (second) - OPTIONAL
            :type off_on_time: ``float``
            """
            if test_case.power_slider_emulator is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f'Power off the device and wait {off_on_time}s')
                # ------------------------------------------------------------------------------------------------------
                test_case.kosmos.sequencer.offline_mode = True
                test_case.power_slider_emulator.power_off()
                test_case.kosmos.pes.delay(off_on_time)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Start LEDs monitoring and Power on the device')
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(test_case=test_case,
                                                                              led_identifiers=led_identifiers)
                test_case.power_slider_emulator.power_on()
                test_case.kosmos.sequencer.offline_mode = False
                test_case.kosmos.sequencer.play_sequence()
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, 'No power slider, LEDs monitoring starts when device is still powered on')
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Start LEDs monitoring')
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(test_case=test_case,
                                                                              led_identifiers=led_identifiers)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Power off / on the device')
                # ------------------------------------------------------------------------------------------------------
                test_case.memory_manager.debugger.reset(soft_reset=False)
            # end if
        # end def start_monitoring_when_device_is_off

        @classmethod
        def stop_monitoring(cls, test_case, led_identifiers=None, build_timeline=True):
            """
            End the connectivity status LEDs monitoring period.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_identifiers: List of LED to stop monitoring - OPTIONAL
            :type led_identifiers: ``list[pylibrary.emulator.ledid.LED_ID]``
            :param build_timeline: Flag indicating post-processing of the data received from the LED spy - OPTIONAL
            :type build_timeline: ``bool``
            """
            if test_case.led_spy is not None:
                # stop LED monitoring on the given list of LED
                test_case.led_spy.stop(led_identifiers)
                if build_timeline:
                    # Build the LEDs timeline from PWM signals
                    test_case.led_timeline = test_case.led_spy.get_timeline()
                # end if
            elif test_case.led_spy_over_i2c is not None:
                # stop I2C monitoring
                test_case.led_spy_over_i2c.stop()
                if build_timeline:
                    # Build the LEDs timeline from I2C frames
                    test_case.led_timeline = test_case.led_spy_over_i2c.get_timeline()
                # end if
            # end if
        # end def stop_monitoring

        @classmethod
        def check_led_state(cls, test_case, led_id, state=SchemeType.OFF):
            """
            Check the current status of the connectivity status LED on the given host index matches the given state.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param state: expected LED blinking speed - OPTIONAL
            :type state: ``SchemeType``
            """
            if test_case.led_spy is not None:
                # Flush LED fifo into SW buffer
                test_case.led_spy.flush_led_data()

                test_case.led_timeline = test_case.led_spy.get_timeline()
            elif test_case.led_spy_over_i2c is not None:
                # Flush LED fifo into SW buffer
                test_case.led_spy_over_i2c.download()

                test_case.led_timeline = test_case.led_spy_over_i2c.get_timeline()
            # end if

            if test_case.led_timeline is not None and \
                    test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.BLE_PRO_CS.F_ConnectivityLEDsCheck:
                # Retrieve the last entry related to the given led id
                channel_id = test_case.led_spy.get_channel_id(led_id) if test_case.led_spy is not None else \
                    test_case.led_spy_over_i2c.get_channel_id(led_id)
                channel = test_case.led_timeline.get_channel(channel_id=channel_id)

                test_case.assertEqual(
                    expected=state, obtained=channel.get_scheme().type,
                    msg=f'Connectivity Status LED shall be in the given state (i.e. {str(state)}) '
                        f'in LED timeline: {str(test_case.led_timeline)}'
                )
            # end if
        # end def check_led_state

        @classmethod
        def check_fast_blinking_time(cls, test_case, led_id, exact_duration=THREE_MINUTES, minimum_duration=None,
                                     position=POSITION.NEXT, reset=False):
            """
            Verify the connectivity status LED on the given host index is fast blinking for the given duration.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param exact_duration: fast blink state exact duration in ms to enforce (default is 3 minutes) - OPTIONAL
            :type exact_duration: ``int``
            :param minimum_duration: fast blink state minimum duration in ms to verify (exclusive with exact_duration)
            :type minimum_duration: ``int``
            :param position: Option defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None and \
                    test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.BLE_PRO_CS.F_ConnectivityLEDsCheck:
                if minimum_duration is not None:
                    checked_duration = minimum_duration
                    check_upper_limit = False
                else:
                    checked_duration = exact_duration
                    check_upper_limit = True
                # end if

                if reset:
                    test_case.led_timeline.reset()
                # end if

                if position == cls.POSITION.FIRST:
                    fast_blinking_start_time = 0
                else:
                    # Get next scheme transition on given LED id
                    fast_blinking_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                    if fast_blinking_transition is not None and position == cls.POSITION.ANY:
                        while fast_blinking_transition.destination != SchemeType.FAST_BLINKING:
                            fast_blinking_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                        # end while
                    # end if
                    test_case.assertNotNone(fast_blinking_transition,
                                            f'Next transition on channel {str(led_id)} not found (fast blinking '
                                            f'expected) in LED timeline: {str(test_case.led_timeline)}')
                    fast_blinking_start_time = fast_blinking_transition.timing
                # end if
                # Check fast blink scheme on given led id
                test_case.assertTrue(
                    expr=cls.is_blinking_fast(test_case=test_case, led_id=led_id, start_time=fast_blinking_start_time,
                                              duration=checked_duration * TICKS_PER_MILLI_SEC,
                                              check_upper_limit=check_upper_limit),
                    msg=f'Connectivity Status LED shall be in fast blinking state for at least {checked_duration} ms '
                        f'in LED timeline: {str(test_case.led_timeline)}'
                )
            # end if
        # end def check_fast_blinking_time

        @classmethod
        def check_slow_blinking_time(cls, test_case, led_id, exact_duration=FIVE_SECONDS, minimum_duration=None,
                                     position=POSITION.NEXT, reset=False):
            """
            Verify the connectivity status LED on the given host index is slow blinking for the given duration.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param exact_duration: slow blinking state exact duration to enforce in ms (default is 5 seconds) - OPTIONAL
            :type exact_duration: ``int``
            :param minimum_duration: slow blinking state minimum duration to verify in ms
                                     (exclusive with exact_duration) - OPTIONAL
            :type minimum_duration: ``int``
            :param position: Option defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None and \
                    test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.BLE_PRO_CS.F_ConnectivityLEDsCheck:
                if minimum_duration is not None:
                    checked_duration = minimum_duration
                    check_upper_limit = False
                else:
                    checked_duration = exact_duration
                    check_upper_limit = True
                # end if

                if reset:
                    test_case.led_timeline.reset()
                # end if

                if position == cls.POSITION.FIRST:
                    slow_blinking_start_time = 0
                else:
                    # Get next scheme transition on given LED id
                    slow_blinking_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                    if slow_blinking_transition is not None and position == cls.POSITION.ANY:
                        while slow_blinking_transition.destination != SchemeType.SLOW_BLINKING:
                            slow_blinking_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                        # end while
                    # end if
                    test_case.assertNotNone(slow_blinking_transition,
                                            f'Next transition on channel {str(led_id)} not found (Slow blinking '
                                            f'expected) in LED timeline: {str(test_case.led_timeline)}')
                    slow_blinking_start_time = slow_blinking_transition.timing
                # end if
                # Check slow blink scheme on given led id
                test_case.assertTrue(
                    expr=cls.is_blinking_slow(test_case=test_case, led_id=led_id, start_time=slow_blinking_start_time,
                                              duration=checked_duration * TICKS_PER_MILLI_SEC,
                                              check_upper_limit=check_upper_limit),
                    msg=f'Connectivity Status LED shall be in slow blinking state for at least {checked_duration} ms '
                        f'in LED timeline: {str(test_case.led_timeline)}'
                )
            # end if
        # end def check_slow_blinking_time

        @classmethod
        def check_steady_time(cls, test_case, led_id, exact_duration=FIVE_SECONDS, minimum_duration=None,
                              position=POSITION.NEXT, reset=False):
            """
            Verify the connectivity status LED on the given host index is steady for the given duration.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param exact_duration: steady state exact duration to enforce in ms (default is 5 seconds) - OPTIONAL
            :type exact_duration: ``int``
            :param minimum_duration: steady state minimum duration to verify in ms
                                     (exclusive with exact_duration) - OPTIONAL
            :type minimum_duration: ``int``
            :param position: Option defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None and \
                    test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.BLE_PRO_CS.F_ConnectivityLEDsCheck:
                if minimum_duration is not None:
                    checked_duration = minimum_duration
                    check_upper_limit = False
                else:
                    checked_duration = exact_duration
                    check_upper_limit = True
                # end if

                if reset:
                    test_case.led_timeline.reset()
                # end if

                if position == cls.POSITION.FIRST:
                    steady_start_time = 0
                else:
                    # Get next scheme transition on given LED id
                    steady_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                    if steady_transition is not None and position == cls.POSITION.ANY:
                        while steady_transition.destination != SchemeType.STEADY:
                            steady_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                        # end while
                    # end if
                    test_case.assertNotNone(steady_transition,
                                            f'Next transition on channel {str(led_id)} not found (Steady expected) '
                                            f'in LED timeline: {str(test_case.led_timeline)}')
                    steady_start_time = steady_transition.timing
                # end if
                # Check steady period on given led id
                test_case.assertTrue(
                    expr=cls.is_turned_on(test_case=test_case, led_id=led_id, start_time=steady_start_time,
                                          duration=checked_duration * TICKS_PER_MILLI_SEC,
                                          check_upper_limit=check_upper_limit),
                    msg=f'Connectivity Status LED '
                        f'{led_id!r} shall be on and steady for at least {checked_duration} ms '
                        f'in LED timeline: {str(test_case.led_timeline)}'
                )
            # end if
        # end def check_steady_time

        @classmethod
        def check_off_time(cls, test_case, led_id, minimum_duration=THIRTY_TWO_MILLI, position=POSITION.NEXT,
                           reset=False):
            """
            Verify the connectivity status LED on the given host index is off for the given duration.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param minimum_duration: off state minimum duration to enforce in ms (default is 32 ms) - OPTIONAL
            :type minimum_duration: ``int``
            :param position: Option defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None and \
                    test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.BLE_PRO_CS.F_ConnectivityLEDsCheck:
                checked_duration = minimum_duration

                if reset:
                    test_case.led_timeline.reset()
                # end if

                if position == cls.POSITION.FIRST:
                    off_start_time = 0
                else:
                    # Get next scheme transition on given LED id
                    off_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                    if off_transition is not None and position == cls.POSITION.ANY:
                        while off_transition.destination != SchemeType.OFF:
                            off_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                        # end while
                    # end if
                    test_case.assertNotNone(off_transition,
                                            f'Next transition on channel {str(led_id)} not found (off expected) '
                                            f'in LED timeline: {str(test_case.led_timeline)}')
                    off_start_time = off_transition.timing
                # end if
                # Check off period on given led id
                test_case.assertTrue(
                    expr=cls.is_turned_off(test_case=test_case, led_id=led_id, start_time=off_start_time,
                                           duration=checked_duration * TICKS_PER_MILLI_SEC),
                    msg=f'Connectivity Status LED shall be off for at least {checked_duration} ms '
                        f'in LED timeline: {str(test_case.led_timeline)}'
                )
            # end if
        # end def check_off_time

        @classmethod
        def get_next_transition(cls, test_case, led_id=None):
            """
            Retrieve the next transition to occur in the timeline.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: LED unique identifier for which a transition is required.
                           None to request the first transition from the iterator.
            :type led_id: ``pylibrary.emulator.ledid.LED_ID`` or ``None``

            :return: The next transition matching the given led id
            :rtype: ``pyraspi.services.kosmos.leds.leddataparser.Transition``
            """
            channel_id = test_case.led_spy.get_channel_id(led_id) if test_case.led_spy is not None else \
                test_case.led_spy_over_i2c.get_channel_id(led_id)
            return test_case.led_timeline.get_next_transition(channel_id=channel_id)
        # end def get_next_transition

        @classmethod
        def is_blinking_fast(cls, test_case, led_id, start_time, duration, check_upper_limit=False):
            """
            Verify the PWM period and duty cycle on a gpio associated to a given led id match the fast blink scheme
            characteristics.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param start_time: the time at which the fast blinking period is supposed to begin
                               (The reference time t0 is the time of the beginning of the monitoring.)
            :type start_time: ``float``
            :param duration: fast blinking duration in ms to verify
            :type duration: ``int``
            :param check_upper_limit: Flag to enable the verification of the upper boundary - OPTIONAL
            :type check_upper_limit: ``bool``
            """
            status = True
            channel_id = test_case.led_spy.get_channel_id(led_id) if test_case.led_spy is not None else \
                test_case.led_spy_over_i2c.get_channel_id(led_id)

            channel = test_case.led_timeline.get_channel(channel_id)
            next_scheme = channel.get_next_scheme()
            while start_time != next_scheme.start_time:
                next_scheme = channel.get_next_scheme()
            # end while
            if next_scheme.type != SchemeType.FAST_BLINKING:
                warn(f'Wrong scheme type: {next_scheme.type} != {SchemeType.FAST_BLINKING}')
                status = False
            # end if
            if duration is not None and not next_scheme.effect_duration > duration * KosmosLedSpy.LOWER_BOUNDARY:
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} < '
                     f'{duration * KosmosLedSpy.LOWER_BOUNDARY}')
                status = False
            # end if
            if (duration is not None and check_upper_limit and
                    not next_scheme.effect_duration < duration * KosmosLedSpy.UPPER_BOUNDARY):
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} > '
                     f'{duration * KosmosLedSpy.UPPER_BOUNDARY}')
                status = False
            # end if

            return status

        # end def is_blinking_fast

        @classmethod
        def is_blinking_slow(cls, test_case, led_id, start_time, duration, check_upper_limit=False):
            """
            Verify the PWM period and duty cycle on a gpio associated to a given led id match the slow blink scheme
            characteristics.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param start_time: the time at which the slow blinking period is supposed to begin
                               (The reference time t0 is the time of the beginning of the monitoring.)
            :type start_time: ``float``
            :param duration: slow blinking duration in ms to verify
            :type duration: ``int``
            :param check_upper_limit: Flag to enable the verification of the upper boundary - OPTIONAL
            :type check_upper_limit: ``bool``
            """
            status = True
            channel_id = test_case.led_spy.get_channel_id(led_id) if test_case.led_spy is not None else \
                test_case.led_spy_over_i2c.get_channel_id(led_id)

            channel = test_case.led_timeline.get_channel(channel_id)
            next_scheme = channel.get_next_scheme()
            while start_time != next_scheme.start_time:
                next_scheme = channel.get_next_scheme()
            # end while
            if next_scheme.type != SchemeType.SLOW_BLINKING:
                warn(f'Wrong scheme type: {next_scheme.type} != {SchemeType.SLOW_BLINKING}')
                status = False
            # end if
            if duration is not None and not next_scheme.effect_duration > duration * KosmosLedSpy.LOWER_BOUNDARY:
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} < '
                     f'{duration * KosmosLedSpy.LOWER_BOUNDARY}')
                status = False
            # end if
            if (duration is not None and check_upper_limit and
                    not next_scheme.effect_duration < duration * KosmosLedSpy.UPPER_BOUNDARY):
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} > '
                     f'{duration * KosmosLedSpy.UPPER_BOUNDARY}')
                status = False
            # end if

            return status

        # end def is_blinking_slow

        @classmethod
        def is_turned_on(cls, test_case, led_id, start_time, duration, check_upper_limit=False):
            """
            Verify the PWM period and duty cycle on a gpio associated to a given led id match the steady scheme
            characteristics.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID``
            :param start_time: the time at which the steady period is supposed to begin
                               (The reference time t0 is the time of the beginning of the monitoring.)
            :type start_time: ``float``
            :param duration: steady duration in ms to verify
            :type duration: ``int``
            :param check_upper_limit: Flag to enable the verification of the upper boundary - OPTIONAL
            :type check_upper_limit: ``bool``
            """
            status = True
            channel_id = test_case.led_spy.get_channel_id(led_id) if test_case.led_spy is not None else \
                test_case.led_spy_over_i2c.get_channel_id(led_id)

            channel = test_case.led_timeline.get_channel(channel_id)
            next_scheme = channel.get_next_scheme()
            while start_time != next_scheme.start_time:
                next_scheme = channel.get_next_scheme()
            # end while
            if next_scheme.type != SchemeType.STEADY:
                warn(f'Wrong scheme type: {next_scheme.type} != {SchemeType.STEADY}')
                status = False
            # end if
            if duration is not None and not next_scheme.effect_duration > duration * KosmosLedSpy.LOWER_BOUNDARY:
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} < '
                     f'{duration * KosmosLedSpy.LOWER_BOUNDARY}')
                status = False
            # end if
            if (duration is not None and check_upper_limit and
                    not next_scheme.effect_duration < duration * KosmosLedSpy.UPPER_BOUNDARY):
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} > '
                     f'{duration * KosmosLedSpy.UPPER_BOUNDARY}')
                status = False
            # end if

            return status

        # end def is_turned_on

        @classmethod
        def is_turned_off(cls, test_case, led_id, start_time, duration, check_upper_limit=False):
            """
            Verify the PWM period and duty cycle on a gpio associated to a given led id match the off scheme
            characteristics.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``pylibrary.emulator.ledid.LED_ID`` or ``int``
            :param start_time: the time at which the off period is supposed to begin
                               (The reference time t0 is the time of the beginning of the monitoring.)
            :type start_time: ``float``
            :param duration: off duration in ms to verify
            :type duration: ``int``
            :param check_upper_limit: Flag to enable the verification of the upper boundary - OPTIONAL
            :type check_upper_limit: ``bool``
            """
            status = True
            channel_id = test_case.led_spy.get_channel_id(led_id) if test_case.led_spy is not None else \
                test_case.led_spy_over_i2c.get_channel_id(led_id)

            channel = test_case.led_timeline.get_channel(channel_id)
            next_scheme = channel.get_next_scheme()
            while start_time != next_scheme.start_time:
                next_scheme = channel.get_next_scheme()
            # end while
            if next_scheme.type != SchemeType.OFF:
                warn(f'Wrong scheme type: {next_scheme.type} != {SchemeType.OFF}')
                status = False
            # end if
            if duration is not None and not next_scheme.effect_duration > duration * KosmosLedSpy.LOWER_BOUNDARY:
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} < '
                     f'{duration * KosmosLedSpy.LOWER_BOUNDARY}')
                status = False
            # end if
            if (duration is not None and check_upper_limit and
                    not next_scheme.effect_duration < duration * KosmosLedSpy.UPPER_BOUNDARY):
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} > '
                     f'{duration * KosmosLedSpy.UPPER_BOUNDARY}')
                status = False
            # end if

            return status
        # end def is_turned_off
    # end class LedSpyHelper

# end class BleProConnectionSchemeTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
