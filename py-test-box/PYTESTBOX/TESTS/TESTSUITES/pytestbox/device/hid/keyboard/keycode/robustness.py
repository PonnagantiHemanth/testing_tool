#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.keycode.robustness
:brief: Hid Keyboard keycode robustness test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.keycode.keycode import KeyCodeTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyCodeRobustnessTestCase(KeyCodeTestCase):
    """
    Validate Keyboard KeyCode robustness TestCases
    """
    DICTATION_FULL_SEQUENCE_HID_REPORT_COUNT = 4
    DICTATION_ABORTED_SEQUENCE_HID_REPORT_COUNT = 2
    ANOTHER_KEY_HID_REPORT_COUNT = 2

    @features('Keyboard')
    @features('KeyCode')
    @level('Robustness')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.DICTATION,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @bugtracker('Dictation_Abort_Handling')
    def test_mac_os_dictation_aborted_by_other_key(self):
        """
        User presses the dictation key, then the user presses any other key before the dictation keycodes are all sent,
        FW aborts dictation in this case.

        JIRA: https://jira.logitech.io/browse/NRF52-469
        """
        # Force the switch in mac os mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keypress on {str(KEY_ID.DICTATION)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(
            key_ids=[KEY_ID.DICTATION], delay=2 * KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 0.95e-3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on {str(KEY_ID.KEYBOARD_A)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_A, duration=0.04)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a key release on {str(KEY_ID.DICTATION)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.DICTATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the expected number of HID reports received')
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(KeyCodeRobustnessTestCase.DICTATION_ABORTED_SEQUENCE_HID_REPORT_COUNT +
                       KeyCodeRobustnessTestCase.ANOTHER_KEY_HID_REPORT_COUNT):
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        ChannelUtils.check_queue_empty(test_case=self, channel=self.current_channel.receiver_channel,
                                       queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("ROB_MEMB_0001")
    # end def test_mac_os_dictation_aborted_by_other_key

    @features('Keyboard')
    @features('KeyCode')
    @level('Robustness')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.DICTATION,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_mac_os_dictation_not_aborted_by_other_key(self):
        """
        User presses the dictation key, then the user presses any other key after the second dictation make is sent,
        FW just completed the dictation sequence in this case.
        """
        # Force the switch in mac os mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keypress on {str(KEY_ID.DICTATION)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(
            key_ids=[KEY_ID.DICTATION], delay=2 * KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 1.05e-3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on {str(KEY_ID.KEYBOARD_A)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_A, duration=0.04)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a key release on {str(KEY_ID.DICTATION)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.DICTATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the expected number of HID reports received')
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(KeyCodeRobustnessTestCase.DICTATION_FULL_SEQUENCE_HID_REPORT_COUNT +
                       KeyCodeRobustnessTestCase.ANOTHER_KEY_HID_REPORT_COUNT):
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        ChannelUtils.check_queue_empty(test_case=self, channel=self.current_channel.receiver_channel,
                                       queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("ROB_MEMB_0002")
    # end def test_mac_os_dictation_not_aborted_by_other_key

    @features('Keyboard')
    @features('KeyCode')
    @level('Robustness')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.DICTATION,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_mac_os_dictation_aborted_by_dictation_key(self):
        """
        User presses the dictation key, then the user presses the dictation key again
        before the dictation keycodes are all sent,
        FW aborts dictation in this case.
        """
        self.kosmos.sequencer.offline_mode = True

        # Force the switch in mac os mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION, delay=1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate two keystrokes on {str(KEY_ID.DICTATION)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(
            key_id=KEY_ID.DICTATION, duration=KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 0.95e-3,
            delay=KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 0.95e-3, repeat=2)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the expected number of HID reports received')
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(KeyCodeRobustnessTestCase.DICTATION_ABORTED_SEQUENCE_HID_REPORT_COUNT):
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        ChannelUtils.check_queue_empty(test_case=self, channel=self.current_channel.receiver_channel,
                                       queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("ROB_MEMB_0003")
    # end def test_mac_os_dictation_aborted_by_dictation_key

    @features('Keyboard')
    @features('KeyCode')
    @level('Robustness')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.DICTATION,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_mac_os_dictation_not_aborted_by_dictation_key(self):
        """
        User presses the dictation key, then the user presses the dictation key again after the second dictation
         make is sent, FW just completed both dictation sequences in this case.
        """
        # Force the switch in mac os mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate two keystrokes on {str(KEY_ID.DICTATION)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(
            key_id=KEY_ID.DICTATION, duration=KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 1.05e-3,
            delay=KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 1.05e-3, repeat=2)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the expected number of HID reports received')
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(KeyCodeRobustnessTestCase.DICTATION_FULL_SEQUENCE_HID_REPORT_COUNT * 2):
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        ChannelUtils.check_queue_empty(test_case=self, channel=self.current_channel.receiver_channel,
                                       queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("ROB_MEMB_0004")
    # end def test_mac_os_dictation_not_aborted_by_dictation_key
# end class KeyCodeRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
