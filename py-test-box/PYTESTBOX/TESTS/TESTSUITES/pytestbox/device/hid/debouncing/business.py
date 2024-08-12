#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.debouncing.business
:brief: Hid debouncing business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.debouncing.debouncing import DebouncingTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DebouncingBusinessTestCase(DebouncingTestCase):
    """
    Validates Debouncing business TestCases
    """
    DOUBLE_KEYSTROKE = 2

    @features('Debounce')
    @level('Business')
    @services('ButtonPressed')
    def test_0percent_make(self):
        """
        Check the timing defined in the FW specification below which a make shall never occur (0% Make)
        """
        self.kosmos.sequencer.offline_mode = True
        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]

        make_detection_level = self.f.PRODUCT.DEBOUNCE.F_0PercentMakeDebounceUs
        make_duration_min = make_detection_level - self.TEST_DURATION if make_detection_level > self.TEST_DURATION \
            else self.STEP

        for make_duration in range(make_duration_min, make_detection_level, self.STEP):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke with duration of the make = {make_duration}us on the key '
                                     f'id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=make_duration / 10**6)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report has been received')
        # ---------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, channel=self.channel_to_use,
                                       queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_DEBC_0001")
    # end def test_0percent_make

    @features('Debounce')
    @level('Business')
    @services('ButtonPressed')
    def test_100percent_make(self):
        """
        Check the timing defined in the FW specification above which a make shall always occur (100% Make)
        """
        self.kosmos.sequencer.offline_mode = True
        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]

        make_detection_level = self.f.PRODUCT.DEBOUNCE.F_100PercentMakeDebounceUs
        make_duration_max = make_detection_level + self.TEST_DURATION
        key_count = 0

        for make_duration in reversed(range(make_detection_level, make_duration_max,
                                            self.STEP)):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke with duration of the make = {make_duration}us on the key '
                                     f'id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=make_duration / 10**6)
            key_count += 1
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        for _ in range(key_count):
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check a make has been detected and generate an HID report on the key id = '
                                      f'{str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the release also generate an HID report on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_DEBC_0002")
    # end def test_100percent_make

    @features('Debounce')
    @level('Business')
    @services('KeyMatrix')
    def test_0percent_break(self):
        """
        Check the timing defined in the FW specification below which a break shall never be detected (0% Break)
        """
        self.kosmos.sequencer.offline_mode = True
        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]

        break_detection_level = self.f.PRODUCT.DEBOUNCE.F_0PercentBreakDebounceUs
        break_duration_min = break_detection_level - self.TEST_DURATION if break_detection_level > self.TEST_DURATION \
            else self.STEP

        for break_duration in range(break_duration_min, break_detection_level, self.STEP):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke with duration of the break = {break_duration}us '
                                     f'on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, delay=break_duration / 10**6)
        # end for
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check a report has been received for the first make on the key id = {str(key_id)}')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check a report has been received for the last break on the key id = {str(key_id)}')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no other HID report has been received')
        # ---------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, channel=self.channel_to_use,
                                       queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_DEBC_0003")
    # end def test_0percent_break

    @features('Debounce')
    @level('Business')
    @services('ButtonPressed')
    def test_100percent_break(self):
        """
        Check the timing defined in the FW specification above which a break shall always occur (100% Break)
        """
        self.kosmos.sequencer.offline_mode = True
        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]

        break_detection_level = self.f.PRODUCT.DEBOUNCE.F_100PercentBreakDebounceUs
        break_duration_max = break_detection_level + self.TEST_DURATION
        key_count = 0

        for break_duration in reversed(range(break_detection_level, break_duration_max, self.STEP)):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on {str(key_id)} with duration of the break = '
                                     f'{break_duration}us on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, delay=break_duration / 10**6)
            key_count += 1
        # end for
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION)
        key_count += 1

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        for _ in range(key_count):
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check a make has been detected and generate an HID report on the key id = '
                                      f'{str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the release also generate an HID report on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_DEBC_0004")
    # end def test_100percent_break

    @features('Debounce')
    @level('Business')
    @services('ButtonPressed')
    def test_single_make_blind_window(self):
        """
        Check the make blind window value defined in the FW specification below which 2 keystrokes shall not be
        detected.
        """
        second_make_time = (self.f.PRODUCT.DEBOUNCE.F_0PercentMakeDebounceUs +
                            self.f.PRODUCT.DEBOUNCE.F_MakeBlindWindowUs +
                            self.f.PRODUCT.DEBOUNCE.F_0PercentBreakDebounceUs)
        second_make_start = second_make_time - self.TEST_DURATION

        key_count = self.TEST_DURATION // self.STEP
        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=key_count, group_size=1, random=False,
                                               excluded_keys=HidData.get_not_single_action_keys())

        loop_size = 0
        for duration in range(second_make_start, second_make_time, self.STEP):
            (key_id,) = keys[loop_size]
            loop_size += 1

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a first keystroke with the sum of make and break duration = '
                                     f'{duration}us on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=(duration / 2) / 10**6,
                                                   delay=(duration / 2) / 10**6)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a second keystroke where the make occurs during the make blind window '
                                     f'on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION,
                                                   delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify that only one make and break events are reported per key')
        # ---------------------------------------------------------------------------
        for loop_index in range(loop_size):
            (key_id,) = keys[loop_index]
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check a make has been detected and generate an HID report '
                                      f'on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the release also generate an HID report on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_DEBC_0005")
    # end def test_single_make_blind_window

    @features('Debounce')
    @level('Business')
    @services('ButtonPressed')
    def test_double_make_blind_window(self):
        """
        Check the make blind window value defined in the FW specification above which 2 keystrokes shall always be
        detected.
        """
        second_make_time = (self.f.PRODUCT.DEBOUNCE.F_100PercentMakeDebounceUs +
                            self.f.PRODUCT.DEBOUNCE.F_MakeBlindWindowUs +
                            self.f.PRODUCT.DEBOUNCE.F_100PercentBreakDebounceUs)
        second_make_max = second_make_time + self.TEST_DURATION

        key_count = self.TEST_DURATION // self.STEP
        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=key_count, group_size=1, random=False,
                                               excluded_keys=HidData.get_not_single_action_keys())

        loop_size = 0

        for duration in reversed(range(second_make_time, second_make_max, self.STEP)):
            (key_id,) = keys[loop_size]
            loop_size += 1

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a first keystroke with the sum of make and break '
                                     f'duration = {duration}us on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=(duration / 2) / 10**6,
                                                   delay=(duration / 2) / 10**6)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a second keystroke where the make occurs after the '
                                     f'make blind window on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION,
                                                   delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify that two make and break events are reported per key')
        # ---------------------------------------------------------------------------
        for loop_index in range(loop_size):
            (key_id,) = keys[loop_index]
            for index in range(self.DOUBLE_KEYSTROKE):
                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check make number {index+1} has been detected on the '
                                          f'key id = {str(key_id)}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check break number {index+1} has been detected on '
                                          f'the key id = {str(key_id)}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
            # end for
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_DEBC_0006")
    # end def test_double_make_blind_window

    @features('Debounce')
    @level('Business')
    @services('ButtonPressed')
    def test_single_break_blind_window(self):
        """
        Check the break blind window value defined in the FW specification below which 2 keystrokes shall not be
        detected.
        """
        second_break_time = (self.f.PRODUCT.DEBOUNCE.F_0PercentBreakDebounceUs +
                             self.f.PRODUCT.DEBOUNCE.F_BreakBlindWindowUs +
                             self.f.PRODUCT.DEBOUNCE.F_0PercentMakeDebounceUs)
        second_break_start = second_break_time-self.TEST_DURATION

        key_count = self.TEST_DURATION // self.STEP
        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=key_count, group_size=1, random=False,
                                               excluded_keys=HidData.get_not_single_action_keys())

        loop_size = 0
        for duration in range(second_break_start, second_break_time, self.STEP):
            (key_id,) = keys[loop_size]
            loop_size += 1

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a first keystroke with the break '
                                     f'duration = {duration / 2}us on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION,
                                                   delay=(duration / 2) / 10**6)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a second keystroke with the make '
                                     f'duration = {duration / 2}us on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=(duration / 2) / 10**6,
                                                   delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify that only one make and break events are reported per key')
        # ---------------------------------------------------------------------------
        for loop_index in range(loop_size):
            (key_id,) = keys[loop_index]
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the make of the first keystroke on the key id = '
                                      f'{str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check only one break is detected and generate an HID '
                                      f'report on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_DEBC_0007")
    # end def test_single_break_blind_window

    @features('Debounce')
    @level('Business')
    @services('ButtonPressed')
    def test_double_break_blind_window(self):
        """
        Check the break blind window value defined in the FW specification above which 2 keystrokes shall always be
        detected.
        """
        second_break_time = (self.f.PRODUCT.DEBOUNCE.F_100PercentBreakDebounceUs +
                             self.f.PRODUCT.DEBOUNCE.F_BreakBlindWindowUs +
                             self.f.PRODUCT.DEBOUNCE.F_100PercentMakeDebounceUs)
        second_break_max = second_break_time + self.TEST_DURATION

        key_count = self.TEST_DURATION // self.STEP
        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=key_count, group_size=1, random=False,
                                               excluded_keys=HidData.get_not_single_action_keys())

        loop_size = 0
        for duration in reversed(range(second_break_time, second_break_max, self.STEP)):
            (key_id,) = keys[loop_size]
            loop_size += 1

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a first keystroke with the break '
                                     f'duration = {duration / 2}us on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION,
                                                   delay=(duration / 2) / 10**6)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a second keystroke with the make '
                                     f'duration = {duration / 2}us on the key id = {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=(duration / 2) / 10**6,
                                                   delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify that only one make and break events are reported per key')
        # ---------------------------------------------------------------------------
        for loop_index in range(loop_size):
            (key_id,) = keys[loop_index]
            for index in range(self.DOUBLE_KEYSTROKE):
                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check make number {index+1} has been detected on the '
                                          f'key id = {str(key_id)}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check break number {index+1} has been detected on '
                                          f'the key id = {str(key_id)}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_DEBC_0008")
    # end def test_double_break_blind_window

# end class DebouncingBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
