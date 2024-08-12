#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.doublepress.timings
:brief: Hid Keyboard double press timings test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/05/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HidConsumer
from pyhid.hid import HidKeyboard
from pyhid.hid import HidKeyboardBitmap
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.keyboard.doublepress.doublepress import DoublePressTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DoublePressTimingsTestCase(DoublePressTestCase):
    """
    Validate Keyboard Double Press timings TestCases
    """

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_RETURN_ENTER))
    @services('SimultaneousKeystrokes')
    def test_play_pause_pressed_once(self):
        """
        Check the HID intervals when the ?play/pause? (PP) key is pressed once.
        """
        key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.HUNDRED_MILLI / 10**3

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a second keystroke on the key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)
        # Set a long delay after the keystroke to prevent the "enter" key release to occur before the end of the
        # 500ms double press timeout
        # noinspection DuplicatedCode
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=key_press_duration,
                                               delay=DoublePressTestCase.DOUBLE_CLICK_TIME/10**3)
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID report timings')
        # --------------------------------------------------------------------------------------------------------------
        enter_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                  class_type=(HidKeyboard, HidKeyboardBitmap),
                                                  check_first_message=False)
        pp_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=HidConsumer)
        press_make_delta = (pp_make_packet.timestamp - enter_make_packet.timestamp) / 10**6
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the press / make interval')
        # ----------------------------------------------------------------------------------------------------------
        self.assertGreater(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')
        self.assertLess(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')

        pp_break_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                class_type=HidConsumer)
        make_break_delta = (pp_break_packet.timestamp - pp_make_packet.timestamp) / 10**6
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate make and break reports are sent in a burst')
        # ----------------------------------------------------------------------------------------------------------
        self.assertLess(make_break_delta, DoublePressTestCase.MAKE_BREAK_DELAY * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.MAKE_BREAK_DELAY} value')

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Get {KEY_ID.KEYBOARD_RETURN_ENTER} key release')
        # ----------------------------------------------------------------------------------------------------------
        ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                              class_type=(HidKeyboard, HidKeyboardBitmap))

        self.testCaseChecked("TIM_DBL_CLK_0001")
    # end def test_play_pause_pressed_once

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_double_click(self):
        """
       Check the HID intervals when Play Pause (PP) key is pressed twice within a maximum period of time Tdc
       ('double click')
        """
        key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.HUNDRED_MILLI / 10**3
        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a double click on the key {str(key_id)} with a interval of '
                                 f'{key_press_duration}ms between makes and breaks')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=key_press_duration,
                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # Set a long delay after the second keystroke to prevent the "enter" key release to occur before the end of the
        # 500ms double press timeout
        # noinspection DuplicatedCode
        self.button_stimuli_emulator.keystroke(
            key_id=key_id, duration=key_press_duration, delay=DoublePressTestCase.DOUBLE_CLICK_TIME/10**3)
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID report timings')
        # --------------------------------------------------------------------------------------------------------------
        enter_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                  class_type=(HidKeyboard, HidKeyboardBitmap),
                                                  check_first_message=False)
        nt_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=HidConsumer)
        press_make_delta = (nt_make_packet.timestamp - enter_make_packet.timestamp) / 10**6
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the press / make interval')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')
        self.assertLess(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')

        nt_break_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                class_type=HidConsumer)
        make_break_delta = (nt_break_packet.timestamp - nt_make_packet.timestamp) / 10**6
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate make and break reports are sent in a burst')
        # ----------------------------------------------------------------------------------------------------------
        self.assertLess(make_break_delta, DoublePressTestCase.MAKE_BREAK_DELAY * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.MAKE_BREAK_DELAY} value')

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Get {KEY_ID.KEYBOARD_RETURN_ENTER} key release')
        # ----------------------------------------------------------------------------------------------------------
        ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                              class_type=(HidKeyboard, HidKeyboardBitmap))

        self.testCaseChecked("TIM_DBL_CLK_0002")
    # end def test_play_pause_double_click

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_RETURN_ENTER))
    @services('SimultaneousKeystrokes')
    def test_play_pause_slow_press(self):
        """
        Check the HID intervals when the 'play/pause' (PP) key is pressed slowly.
        """
        key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = (DoublePressTestCase.DOUBLE_CLICK_TIME + DoublePressTestCase.HUNDRED_MILLI) / 10**3

        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on the key {str(key_id)} with a interval of '
                                 f'{key_press_duration}ms between makes and breaks')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)
        self.button_stimuli_emulator.keystroke(
            key_id=key_id, duration=key_press_duration, delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # noinspection DuplicatedCode
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID reports intervals')
        # --------------------------------------------------------------------------------------------------------------
        enter_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                  class_type=(HidKeyboard, HidKeyboardBitmap),
                                                  check_first_message=False)
        pp_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=HidConsumer)
        press_make_delta = (pp_make_packet.timestamp - enter_make_packet.timestamp) / 10 ** 6

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the press / make interval')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')
        self.assertLess(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')

        pp_break_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                class_type=HidConsumer)
        make_break_delta = (pp_break_packet.timestamp - pp_make_packet.timestamp) / 10 ** 6
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the make / break interval')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(make_break_delta, DoublePressTestCase.HUNDRED_MILLI * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.HUNDRED_MILLI}ms value')
        self.assertLess(make_break_delta, DoublePressTestCase.HUNDRED_MILLI * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.HUNDRED_MILLI}ms value')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Get {KEY_ID.KEYBOARD_RETURN_ENTER} key release')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                              class_type=(HidKeyboard, HidKeyboardBitmap))

        self.testCaseChecked("TIM_DBL_CLK_0003")
    # end def test_play_pause_slow_press

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_RETURN_ENTER))
    @services('SimultaneousKeystrokes')
    def test_play_pause_slow_double_click(self):
        """
        Check the HID intervals when the 'play/pause' (PP) key is pressed twice slowly.
        """
        key_id = KEY_ID.PLAY_PAUSE
        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a slow double click on the key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)
        self.button_stimuli_emulator.keystroke(
            key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION, repeat=2,
            delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # noinspection DuplicatedCode
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID report timings')
        # --------------------------------------------------------------------------------------------------------------
        enter_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                  class_type=(HidKeyboard, HidKeyboardBitmap),
                                                  check_first_message=False)
        pp_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=HidConsumer)
        press_make_delta = (pp_make_packet.timestamp - enter_make_packet.timestamp) / 10 ** 6
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the press / make interval')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')
        self.assertLess(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')

        pp_break_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                class_type=HidConsumer)
        make_break_delta = (pp_break_packet.timestamp - pp_make_packet.timestamp) / 10 ** 6
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the make / break interval')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(make_break_delta, DoublePressTestCase.HUNDRED_MILLI * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.HUNDRED_MILLI}ms value')
        self.assertLess(make_break_delta, DoublePressTestCase.HUNDRED_MILLI * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.HUNDRED_MILLI}ms value')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Get {KEY_ID.KEYBOARD_RETURN_ENTER} key release')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                              class_type=(HidKeyboard, HidKeyboardBitmap))

        self.testCaseChecked("TIM_DBL_CLK_0004")
    # end def test_play_pause_slow_double_click

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_RETURN_ENTER))
    @services('SimultaneousKeystrokes')
    def test_play_pause_multiple_presses(self):
        """
        Check the HID reports intervals when the Play Pause (PP) key is pressed multiple times within a maximum
        period of time Tdc ('double click').
        Check the 'next tract' (NT) key is sent only once
        """
        pp_key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.FIFTY_MILLI / 10**3
        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a triple click on the key {str(pp_key_id)} with a interval of '
                                 f'{key_press_duration}ms between makes and breaks')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)
        self.button_stimuli_emulator.keystroke(key_id=pp_key_id, duration=key_press_duration,
                                               delay=key_press_duration, repeat=2)
        # Set a long delay after the third keystroke to prevent the "enter" key release to occur before the end of the
        # 500ms double press timeout
        # noinspection DuplicatedCode
        self.button_stimuli_emulator.keystroke(key_id=pp_key_id, duration=key_press_duration,
                                               delay=DoublePressTestCase.DOUBLE_CLICK_TIME/10**3)
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID report timings')
        # --------------------------------------------------------------------------------------------------------------
        enter_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                  class_type=(HidKeyboard, HidKeyboardBitmap),
                                                  check_first_message=False)
        nt_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=HidConsumer)
        press_make_delta = (nt_make_packet.timestamp - enter_make_packet.timestamp) / 10 ** 6
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the press / make interval')
        # ----------------------------------------------------------------------------------------------------------
        self.assertGreater(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')
        self.assertLess(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')

        nt_break_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                class_type=HidConsumer)
        make_break_delta = (nt_break_packet.timestamp - nt_make_packet.timestamp) / 10 ** 6
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate make and break reports are sent in a burst')
        # ----------------------------------------------------------------------------------------------------------
        self.assertLess(make_break_delta, DoublePressTestCase.MAKE_BREAK_DELAY * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.MAKE_BREAK_DELAY} value')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Get {KEY_ID.KEYBOARD_RETURN_ENTER} key release')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                              class_type=(HidKeyboard, HidKeyboardBitmap))

        self.testCaseChecked("TIM_DBL_CLK_0005")
    # end def test_play_pause_multiple_presses

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE, KEY_ID.KEYBOARD_RETURN_ENTER))
    @services('SimultaneousKeystrokes')
    def test_play_pause_multiple_presses_and_press(self):
        """
        Check the HID reports intervals when the Play Pause (PP) key is pressed multiple times within a maximum
        period of time Tdc ('double click').
        Check the 'next tract' (NT) key is sent only once
        """
        pp_key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.HUNDRED_MILLI / 10**3
        key_release_duration = DoublePressTestCase.FIFTY_MILLI / 10**3
        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate four clicks on the key {str(pp_key_id)} with {key_press_duration}ms '
                                 f'duration for make and {key_release_duration}ms for break')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)
        self.button_stimuli_emulator.keystroke(key_id=pp_key_id, duration=key_press_duration,
                                               delay=key_release_duration, repeat=4)
        # noinspection DuplicatedCode
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.KEYBOARD_RETURN_ENTER)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID report timings')
        # --------------------------------------------------------------------------------------------------------------
        enter_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                  class_type=(HidKeyboard, HidKeyboardBitmap),
                                                  check_first_message=False)
        nt_make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=HidConsumer)
        press_make_delta = (nt_make_packet.timestamp - enter_make_packet.timestamp) / 10 ** 6
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the press / make interval')
        # ----------------------------------------------------------------------------------------------------------
        self.assertGreater(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')
        self.assertLess(press_make_delta, DoublePressTestCase.DOUBLE_CLICK_TIME * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.DOUBLE_CLICK_TIME}ms value')

        nt_break_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                class_type=HidConsumer)
        make_break_delta = (nt_break_packet.timestamp - nt_make_packet.timestamp) / 10 ** 6
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the make / break interval')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(make_break_delta, DoublePressTestCase.FIFTY_MILLI * 0.9,
                           f'The delta is lower than 90% of the {DoublePressTestCase.FIFTY_MILLI}ms value')
        self.assertLess(make_break_delta, DoublePressTestCase.FIFTY_MILLI * 1.1,
                        f'The delta is greater than 110% of the {DoublePressTestCase.FIFTY_MILLI}ms value')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Get {KEY_ID.KEYBOARD_RETURN_ENTER} key release')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                              class_type=(HidKeyboard, HidKeyboardBitmap))

        self.testCaseChecked("TIM_DBL_CLK_0006")
    # end def test_play_pause_multiple_presses_and_press
# end class DoublePressTimingsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
