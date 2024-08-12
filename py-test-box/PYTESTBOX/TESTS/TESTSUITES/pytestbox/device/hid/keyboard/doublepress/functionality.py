#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.doublepress.functionality
:brief: Hid Keyboard double press functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/05/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.doublepress.doublepress import DoublePressTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DoublePressFunctionalityTestCase(DoublePressTestCase):
    """
    Validate Keyboard Double Press functionality TestCases
    """

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_slow_press(self):
        """
        Check that If the ?play/pause? (PP) key is pressed slowly, the PlayPause make is sent
        when reaching the 500ms timeout
        """
        key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = (DoublePressTestCase.DOUBLE_CLICK_TIME + DoublePressTestCase.HUNDRED_MILLI) / 10**3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a slow pressed keystroke on the key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=key_press_duration)
        self.kosmos.sequencer.offline_mode = False
        # Upload the sequence to Kosmos to be played.
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard report linked to the key id={str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check no other HID reports are sent')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("FUN_DBL_CLK_0001")
    # end def test_play_pause_slow_press

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_slow_double_click(self):
        """
        Check that If the ?play/pause? (PP) key is pressed twice slowly, the PlayPause make is sent
        when reaching the 500ms timeout
        """
        key_id = KEY_ID.PLAY_PAUSE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a slow double click on the key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=2)
        self.kosmos.sequencer.offline_mode = False
        # Upload the sequence to Kosmos to be played.
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard reports linked to the key id={str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check no other HID reports are sent')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("FUN_DBL_CLK_0002")
    # end def test_play_pause_slow_double_click

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_multiple_presses(self):
        """
        Check that if Play Pause (PP) key is pressed multiple times within a maximum period of time Tdc
        ('double click'), the 'next tract' (NT) key is always sent only once
        """
        pp_key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.FIFTY_MILLI / 10**3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a triple click on the key {str(pp_key_id)} with a interval of '
                                 f'{key_press_duration}ms between makes and breaks')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.keystroke(key_id=pp_key_id, duration=key_press_duration,
                                               delay=key_press_duration, repeat=3)
        self.kosmos.sequencer.offline_mode = False
        # Upload the sequence to Kosmos to be played.
        self.kosmos.sequencer.play_sequence()

        nt_key_id = KEY_ID.NEXT_TRACK
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check single make and break reports from key id={str(nt_key_id)} are sent')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(nt_key_id, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(nt_key_id, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check no other HID reports are sent')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a quatriple click on the key {str(pp_key_id)} with a interval of '
                                 f'{key_press_duration}ms between makes and breaks')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.keystroke(key_id=pp_key_id, duration=key_press_duration,
                                               delay=key_press_duration, repeat=4)
        self.kosmos.sequencer.offline_mode = False
        # Upload the sequence to Kosmos to be played.
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check single make and break reports from key id={str(nt_key_id)} are sent')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(nt_key_id, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(nt_key_id, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check no other HID reports are sent')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_DBL_CLK_0003")
    # end def test_play_pause_multiple_presses

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_multiple_presses_and_press(self):
        """
        Check that if Play Pause (PP) key is pressed multiple times and the key is still pressed when the time Tdc
        ('double click') is reached, the 'next tract' (NT) key make and break reports are sent only once
        """
        pp_key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.HUNDRED_MILLI / 10**3
        key_release_duration = DoublePressTestCase.FIFTY_MILLI / 10**3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a quadruple click on the key {str(pp_key_id)} with '
                                 f'{key_press_duration}ms duration for make and {key_release_duration}ms for break')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.keystroke(key_id=pp_key_id, duration=key_press_duration,
                                               delay=key_release_duration, repeat=4)
        self.kosmos.sequencer.offline_mode = False
        # Upload the sequence to Kosmos to be played.
        self.kosmos.sequencer.play_sequence()

        nt_key_id = KEY_ID.NEXT_TRACK
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check single make and break reports from key id={str(nt_key_id)} are sent')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(nt_key_id, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(nt_key_id, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check no other HID reports are sent')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_DBL_CLK_0003")
    # end def test_play_pause_multiple_presses_and_press

# end class DoublePressFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
