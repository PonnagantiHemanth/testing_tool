#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.doublepress.business
:brief: Hid Keyboard double press business test suite
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
class DoublePressBusinessTestCase(DoublePressTestCase):
    """
    Validate Keyboard Double Press business TestCases
    """

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business', 'SmokeTests')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_pressed_once(self):
        """
        Check that If the ?play/pause? (PP) key is pressed once, the key is sent normally

        cf https://docs.google.com/document/d/1Yebz9EikFP38I6lRIUav_JWwU4SgoWPzxfCzQGAj1SQ/edit#bookmark=id.c7ioidyhqlbh
        """
        key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.HUNDRED_MILLI / 10**3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a single keystroke on the key {str(key_id)} during {key_press_duration}')
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

        self.testCaseChecked("BUS_DBL_CLK_0001")
    # end def test_play_pause_pressed_once

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_double_click(self):
        """
        Check that if Play Pause (PP) key is pressed twice within a maximum period of time Tdc ('double click'),
        the 'next tract' (NT) key is sent instead
        """
        key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = DoublePressTestCase.HUNDRED_MILLI / 10**3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a double click on the key {str(key_id)} with a interval of '
                                 f'{key_press_duration}ms between makes and breaks')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=key_press_duration,
                                               delay=key_press_duration, repeat=2)
        self.kosmos.sequencer.offline_mode = False
        # Upload the sequence to Kosmos to be played.
        self.kosmos.sequencer.play_sequence()

        key_id = KEY_ID.NEXT_TRACK
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard report linked to the key id={str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check no other HID reports are sent')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_DBL_CLK_0002")
    # end def test_play_pause_double_click

    @features('Keyboard')
    @features('PlayPauseDoublePress')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.PLAY_PAUSE,))
    @services('SingleKeystroke')
    def test_play_pause_5_make_4_break_within_tdc(self):
        """
        Check that if Play Pause (PP) key is pressed 5 times and released 4 times within a maximum period of time
        Tdc ('double click'), the 'next tract' (NT) make report is sent but the break report is sent once the
        key is released
        """
        key_id = KEY_ID.PLAY_PAUSE
        key_press_duration = (DoublePressTestCase.FIFTY_MILLI + DoublePressTestCase.THIRTY_MILLI) / 10 ** 3
        key_press_delay = DoublePressTestCase.THIRTY_MILLI / 10 ** 3

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Empty Queue before keystrokes')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate four clicks on the key {str(key_id)} with a interval of '
                                 f'{key_press_duration}ms between makes and breaks')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.keystroke(key_id=key_id,
                                               duration=key_press_duration,
                                               delay=key_press_delay,
                                               repeat=4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Key Press on the key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key_id)
        self.kosmos.sequencer.offline_mode = False
        # Upload the sequence to Kosmos to be played.
        self.kosmos.sequencer.play_sequence()

        key_id = KEY_ID.NEXT_TRACK
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard make report linked to the key id={str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard break report not received until 5th break is made')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Key Release on the key {str(KEY_ID.PLAY_PAUSE)}')
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.PLAY_PAUSE)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check Break is received after the 5th Break')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        self.testCaseChecked("BUS_DBL_CLK_0003")
    # end def test_play_pause_5_make_4_break_within_tdc

# end class DoublePressBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
