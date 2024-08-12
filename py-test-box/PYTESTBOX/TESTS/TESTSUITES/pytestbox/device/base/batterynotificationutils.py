#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.batterynotificationutils
:brief: Helper for Battery Notification feature
:author: Gautham S B <gsb@logitech.com>
:date: 2024/02/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from warnings import warn

from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.kosmos.kosmosledspy import KosmosLedSpy
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pyraspi.services.kosmos.leds.leddataparser import TICKS_PER_MILLI_SEC
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BatteryNotificationUtils(DeviceBaseTestUtils):
    """
    Provide helpers for Battery Notification feature
    """

    class LedSpyHelper(BleProConnectionSchemeTestUtils.LedSpyHelper):
        """
        LEDs spy module helper class
        """
        THIRTY_TWO_MILLI = 32
        THREE_MINUTES_IN_MS = 180000
        FIVE_SECONDS_IN_MS = 5000

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
        def check_steady_time(cls, test_case, led_id, exact_duration=FIVE_SECONDS_IN_MS, minimum_duration=None,
                              maximum_duration=None, position=POSITION.NEXT, reset=False):
            """
            Verify the LED is steady ON for the given duration.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param led_id: The unique LED identifier to monitor
            :type led_id: ``LED_ID``
            :param exact_duration: The steady state exact duration to enforce in ms (default is 5 seconds)
                                   (exclusive with minimum and maximum duration) - OPTIONAL
            :type exact_duration: ``int``
            :param minimum_duration: The steady state minimum duration to verify in ms
                                     (exclusive with exact_duration) - OPTIONAL
            :type minimum_duration: ``int``
            :param maximum_duration: The steady state maximum duration to verify in ms
                                     (exclusive with exact_duration) - OPTIONAL
            :type maximum_duration: ``int``
            :param position: The option for defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BatteryNotificationUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``

            :raise ``AssertionError``: Assert steady state time duration that raises an exception
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None:
                if minimum_duration is not None:
                    checked_duration = minimum_duration
                elif maximum_duration is not None:
                    checked_duration = maximum_duration
                else:
                    checked_duration = exact_duration
                # end if

                if reset:
                    test_case.led_timeline.reset()
                # end if

                if position == cls.POSITION.FIRST:
                    steady_start_time = 0
                else:
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

                err_msg = None
                if minimum_duration or exact_duration is not None:
                    err_msg = (f'{str(led_id)} shall be on and steady for at least {checked_duration} ms '
                               f'in LED timeline: {str(test_case.led_timeline)}')
                elif maximum_duration is not None:
                    err_msg = (f'{str(led_id)} shall be on for not longer than {checked_duration} ms '
                               f'in LED timeline: {str(test_case.led_timeline)}')
                # end if

                # Check steady period on given led id
                test_case.assertTrue(
                    expr=cls.is_turned_on(test_case=test_case, led_id=led_id, start_time=steady_start_time,
                                          exact_duration=exact_duration, minimum_duration=minimum_duration,
                                          maximum_duration=maximum_duration), msg=err_msg)
            # end if
        # end def check_steady_time

        @classmethod
        def check_off_time(cls, test_case, led_id, minimum_duration=FIVE_SECONDS_IN_MS, position=POSITION.FIRST,
                           reset=False):
            """
            Verify the LED is off for the given duration.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``LED_ID``
            :param minimum_duration: off state minimum duration to enforce in ms (default is 32 ms) - OPTIONAL
            :type minimum_duration: ``int``
            :param position: Option defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BatteryNotificationUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``

            :raise ``AssertionError``: Assert off time duration that raise an exception
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None:
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
                    msg=f'{str(led_id)} LED shall be off for at least {checked_duration} ms '
                        f'in LED timeline: {str(test_case.led_timeline)}'
                )
            # end if
        # end def check_off_time

        @classmethod
        def check_slow_blinking_time(cls, test_case, led_id, exact_duration=FIVE_SECONDS_IN_MS, minimum_duration=None,
                                     position=POSITION.NEXT, reset=False):
            """
            Verify the LED is slow blinking for the given duration.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param led_id: The unique LED identifier to monitor
            :type led_id: ``LED_ID``
            :param exact_duration: The slow blinking state exact duration to enforce in ms
                                   (default is 5 seconds) - OPTIONAL
            :type exact_duration: ``int``
            :param minimum_duration: The slow blinking state minimum duration to verify in ms
                                     (exclusive with exact_duration) - OPTIONAL
            :type minimum_duration: ``int``
            :param position: Option defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BatteryNotificationUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``

            :raise ``AssertionError``: Assert slow blinking time duration that raises an exception
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None:
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
                    msg=f'{str(led_id)} shall be in slow blinking state for at least {checked_duration} ms '
                        f'in LED timeline: {str(test_case.led_timeline)}')
            # end if
        # end def check_slow_blinking_time

        @classmethod
        def check_pulsing_time(cls, test_case, led_id, exact_duration=THREE_MINUTES_IN_MS, minimum_duration=None,
                               position=POSITION.FIRST, reset=False):
            """
            Verify the LED is pulsing for the given duration

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param led_id: The unique LED identifier to monitor
            :type led_id: ``LED_ID``
            :param exact_duration: The pulsing state exact duration to enforce in ms (default is 3 minutes) - OPTIONAL
            :type exact_duration: ``int``
            :param minimum_duration: The pulsing state minimum duration to verify in ms
                                     (exclusive with exact_duration) - OPTIONAL
            :type minimum_duration: ``int``
            :param position: Option defining how to find the right transition in the timeline - OPTIONAL
            :type position: ``BatteryNotificationUtils.LedSpyHelper.POSITION``
            :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
            :type reset: ``bool``

            :raise ``AssertionError``: Assert pulsing time duration that raise an exception
            """
            if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
                return
            # end if

            if test_case.led_timeline is not None:
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

                if position == position.FIRST:
                    pulsing_state_start_time = 0
                else:
                    # Get next scheme transition on given LED id
                    pulsing_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                    if pulsing_transition is not None and position == cls.POSITION.ANY:
                        while pulsing_transition.destination != SchemeType.PULSING:
                            pulsing_transition = cls.get_next_transition(test_case=test_case, led_id=led_id)
                        # end while
                    # end if
                    test_case.assertNotNone(pulsing_transition,
                                            f'Next transition on channel {str(led_id)} not found (Pulsing'
                                            f'expected) in LED timeline: {str(test_case.led_timeline)}')
                    pulsing_state_start_time = pulsing_transition.timing
                # end if

                # Check pulsing scheme on given led id
                test_case.assertTrue(expr=cls.is_pulsing(test_case=test_case, led_id=led_id,
                                                         start_time=pulsing_state_start_time,
                                                         duration=checked_duration * TICKS_PER_MILLI_SEC,
                                                         check_upper_limit=check_upper_limit),
                                     msg=f'{str(led_id)} shall be in pulsing state for at least {checked_duration} ms '
                                         f'in LED timeline: {str(test_case.led_timeline)}')
            # end if
        # end def check_pulsing_time

        @classmethod
        def is_pulsing(cls, test_case, led_id, start_time, duration, check_upper_limit=False):
            """
            Verify the PWM period and duty cycle on a gpio associated to a given led id match the pulsing scheme
            characteristics

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param led_id: The unique LED identifier to monitor
            :type led_id: ``LED_ID``
            :param start_time: The time at which the pulsing period is supposed to begin
                               (The reference time t0 is the time of the beginning of the monitoring)
            :type start_time: ``float``
            :param duration: The pulsing duration in ms to verify
            :type duration: ``int``
            :param check_upper_limit: The flag to enable the verification of the upper boundary - OPTIONAL
            :type check_upper_limit: ``bool``

            :return: Status as true if the LED is pulsing on for the expected duration, false otherwise
            :rtype: ``bool``
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
                warn(f'Wrong scheme type: {next_scheme.type} != {SchemeType.PULSING}')
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

        # end def is_pulsing

        @classmethod
        def is_turned_on(cls, test_case, led_id, start_time, exact_duration, minimum_duration=None,
                         maximum_duration=None):
            """
            Verify the PWM period and duty cycle on a gpio associated to a given led id match the steady scheme
            characteristics.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param led_id: unique LED identifier to monitor
            :type led_id: ``LED_ID``
            :param start_time: The time at which the steady period is supposed to begin
                               (The reference time t0 is the time of the beginning of the monitoring.)
            :type start_time: ``float``
            :param exact_duration: The exact steady duration in ms to verify
            :type exact_duration: ``int``
            :param minimum_duration: The exact minimum steady duration in ms to verify
            :type minimum_duration: ``int``
            :param maximum_duration: The exact maximum steady duration in ms to verify
            :type maximum_duration: ``int``

            :return: Status as true if the LED is turned on for the expected duration, false otherwise
            :rtype: ``bool``
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

            if maximum_duration == minimum_duration is None:
                maximum_duration = minimum_duration = exact_duration
            # end if

            maximum_duration = maximum_duration * TICKS_PER_MILLI_SEC if maximum_duration is not None else None
            minimum_duration = minimum_duration * TICKS_PER_MILLI_SEC if minimum_duration is not None else None

            if (minimum_duration is not None and next_scheme.effect_duration < minimum_duration *
                    KosmosLedSpy.LOWER_BOUNDARY):
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} < '
                     f'{minimum_duration * KosmosLedSpy.LOWER_BOUNDARY}')
                status = False
            # end if

            if (maximum_duration is not None and next_scheme.effect_duration > maximum_duration *
                    KosmosLedSpy.UPPER_BOUNDARY):
                warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} > '
                     f'{maximum_duration * KosmosLedSpy.LOWER_BOUNDARY}')
                status = False
            # end if

            return status
        # end def is_turned_on
    # end class LedSpyHelper
# end class BatteryNotificationUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
