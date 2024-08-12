#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.base.ledspyhelper
:brief: Helper for LedSpy service
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from warnings import warn

from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.kosmos.kosmosledspy import KosmosLedSpy
from pyraspi.services.kosmos.leds.leddataparser import SchemeType, TICKS_PER_MILLI_SEC
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LedSpyHelper:
    """
    LEDs spy module helper class
    """
    ONE_SECOND = 1000
    TWO_SECONDS = 2000
    FIVE_SECONDS = 5000

    class POSITION:
        """
        Timeline cursor position. We shall select ``FIRST`` to start from the beginning, ``NEXT`` to take the
        next transition on the timeline, ``ANY`` to find the first transition with a matching scheme type or
        ``FROM_LAST`` to consider schemes in reverse order starting from the last one to the first.
        """
        FIRST = 0
        NEXT = 1
        ANY = 2
        FROM_LAST = 3
    # end class POSITION

    @classmethod
    def start_monitoring(cls, test_case, led_identifiers):
        """
        Start the LEDs monitoring period.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param led_identifiers: The LED(s) to start monitoring
        :type led_identifiers: ``list[LED_ID] or LED_ID``
        """
        if not isinstance(led_identifiers, list):
            led_identifiers = [led_identifiers]
        # end if
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
    def start_monitoring_when_device_is_off(cls, test_case, led_identifiers, off_on_time=ONE_SECOND//1000):
        """
        Define the sequence between LEDs monitoring start and DUT power on according to the services available.

        If a power slider is present, start the LEDs monitoring when device is off then power on the device.
        Else start the LEDs monitoring then reset the device with debugger.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param led_identifiers: The LED(s) to start monitoring
        :type led_identifiers: ``list[LED_ID] or LED_ID``
        :param off_on_time: The duration between power off and power on in seconds
                            (Default value is 1 second) - OPTIONAL
        :type off_on_time: ``float``
        """
        if not isinstance(led_identifiers, list):
            led_identifiers = [led_identifiers]
        # end if
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
            cls.start_monitoring(test_case=test_case, led_identifiers=led_identifiers)
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
            cls.start_monitoring(test_case=test_case, led_identifiers=led_identifiers)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Power off / on the device')
            # ------------------------------------------------------------------------------------------------------
            test_case.memory_manager.debugger.reset(soft_reset=False)
        # end if
    # end def start_monitoring_when_device_is_off

    @classmethod
    def stop_monitoring(cls, test_case, led_identifiers, build_timeline=True):
        """
        End the LEDs monitoring period.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param led_identifiers: The LED(s) to stop monitoring
        :type led_identifiers: ``list[LED_ID] or LED_ID``
        :param build_timeline: Flag indicating post-processing of the data received from the LED spy - OPTIONAL
        :type build_timeline: ``bool``
        """
        if not isinstance(led_identifiers, list):
            led_identifiers = [led_identifiers]
        # end if
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
    def check_effect_duration(cls, test_case, led_id, effect, exact_duration=None, minimum_duration=None,
                              maximum_duration=None, position=POSITION.NEXT, reset=False):
        """
        Verify the LED shows the specified effect for a given duration.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param led_id: The unique LED identifier to monitor
        :type led_id: ``LED_ID``
        :param effect: The effect to verify
        :type effect: ``SchemeType``
        :param exact_duration: The exact duration to enforce in ms
                               (exclusive of minimum and maximum duration) - OPTIONAL
        :type exact_duration: ``int``
        :param minimum_duration: The minimum duration to verify in ms
                                 (exclusive of exact_duration) - OPTIONAL
        :type minimum_duration: ``int``
        :param maximum_duration: The maximum duration to verify in ms
                                 (exclusive of exact_duration) - OPTIONAL
        :type maximum_duration: ``int``
        :param position: The option for defining how to find the right transition in the timeline
                         (default position is next) - OPTIONAL
        :type position: ``LedSpyHelper.POSITION``
        :param reset: Flag indicating if you want to restart parsing the timeline from the beginning - OPTIONAL
        :type reset: ``bool``

        :raise ``AssertionError``: Assert steady state time duration that raises an exception
        """
        from_last = False
        clear_last_iterator = True

        if minimum_duration or maximum_duration is not None:
            exact_duration = None
        # end if

        if test_case.led_spy is None and test_case.led_spy_over_i2c is None:
            raise AssertionError('No LED spy service available')
        # end if

        if test_case.led_timeline is not None:
            if reset:
                test_case.led_timeline.reset()
            # end if

            if position == cls.POSITION.FIRST:
                start_time = 0
            else:
                if position == cls.POSITION.FROM_LAST:
                    from_last = True
                    clear_last_iterator = False
                # end if

                channel_id = test_case.led_spy.get_channel_id(led_id) if test_case.led_spy is not None else \
                    test_case.led_spy_over_i2c.get_channel_id(led_id)
                transition = test_case.led_timeline.get_next_transition(
                    channel_id=channel_id, from_last=from_last, clear_from_last_iterator=clear_last_iterator)

                if transition is not None and position in [cls.POSITION.ANY, cls.POSITION.FROM_LAST]:
                    while transition.destination != effect:
                        transition = test_case.led_timeline.get_next_transition(
                            channel_id=channel_id, from_last=from_last,
                            clear_from_last_iterator=clear_last_iterator)
                    # end while
                # end if

                test_case.assertNotNone(transition,
                                        f'{effect.name} transition for {led_id.name} not found '
                                        f'in LED timeline: {str(test_case.led_timeline)}')
                start_time = transition.timing
            # end if

            if from_last:
                test_case.led_timeline.reset()
            # end if

            err_msg = ''

            if minimum_duration is not None:
                err_msg += f'{led_id.name} shall be in {effect.name} state for at least {minimum_duration} ms '
            # end if

            if maximum_duration is not None:
                if minimum_duration is not None:
                    err_msg += ' and '
                # end if
                err_msg += (f'{led_id.name} shall be in {effect.name} state for not longer than '
                            f'{maximum_duration} ms ')
            # end if

            if exact_duration is not None:
                err_msg += f'{led_id.name} shall be in {effect.name} state for exactly {exact_duration} ms '
            # end if

            err_msg += f'in LED timeline: {str(test_case.led_timeline)}'

            test_case.assertTrue(
                expr=cls.is_effect_duration_valid(test_case=test_case, led_id=led_id, effect=effect,
                                                  start_time=start_time, exact_duration=exact_duration,
                                                  minimum_duration=minimum_duration, maximum_duration=maximum_duration
                                                  ), msg=err_msg)
        # end if
    # end def check_effect_duration

    @classmethod
    def is_effect_duration_valid(cls, test_case, led_id, effect, start_time, exact_duration=None, minimum_duration=None,
                                 maximum_duration=None):
        """
        Verify the PWM period and duty cycle on a gpio associated to a given led id match the specified effect
        characteristics.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param led_id: The unique LED identifier
        :type led_id: ``LED_ID``
        :param effect: The effect to verify
        :type effect: ``SchemeType``
        :param start_time: The time at which the effect period is supposed to begin
                           (The reference time t0 is the time of the beginning of the monitoring.)
        :type start_time: ``float``
        :param exact_duration: The exact effect duration in ms to verify
                               (exclusive of minimum and maximum duration) - OPTIONAL
        :type exact_duration: ``int``
        :param minimum_duration: The minimum effect duration in ms to verify
                                 (exclusive of exact_duration) - OPTIONAL
        :type minimum_duration: ``int``
        :param maximum_duration: The maximum effect duration in ms to verify
                                 (exclusive of exact_duration) - OPTIONAL
        :type maximum_duration: ``int``

        :return: Status (True if the LED is turned ON for the expected duration, False otherwise)
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

        if next_scheme.type != effect:
            warn(f'Wrong scheme type: {next_scheme.type} != {effect}')
            status = False
        # end if

        if exact_duration is not None:
            maximum_duration = minimum_duration = exact_duration
        # end if

        maximum_duration = maximum_duration * TICKS_PER_MILLI_SEC if maximum_duration is not None else None
        minimum_duration = minimum_duration * TICKS_PER_MILLI_SEC if minimum_duration is not None else None

        if (minimum_duration is not None and next_scheme.effect_duration < minimum_duration *
                KosmosLedSpy.LOWER_BOUNDARY):
            warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} > '
                 f'{minimum_duration * KosmosLedSpy.LOWER_BOUNDARY}')
            status = False
        # end if

        if (maximum_duration is not None and next_scheme.effect_duration > maximum_duration *
                KosmosLedSpy.UPPER_BOUNDARY):
            warn(f'Scheme duration does not complied with requirement: {next_scheme.effect_duration} < '
                 f'{maximum_duration * KosmosLedSpy.LOWER_BOUNDARY}')
            status = False
        # end if

        return status
    # end def is_effect_duration_valid
# end class LedSpyHelper

# ----------------------------------------------------------------------------------------------------------------------
# End of File
# ----------------------------------------------------------------------------------------------------------------------
