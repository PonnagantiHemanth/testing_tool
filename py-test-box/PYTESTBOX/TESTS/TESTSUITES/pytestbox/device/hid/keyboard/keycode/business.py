#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.keycode.business
:brief: Hid Keyboard keycode business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.keycode.keycode import KeyCodeTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyCodeBusinessTestCase(KeyCodeTestCase):
    """
    Validate Keyboard KeyCode business TestCases
    """

    @features('Keyboard')
    @features('KeyCode')
    @level('Business', 'SmokeTests')
    @services('SingleKeystroke')
    def test_first_5_keys(self):
        """
        Check the first 5 supported keys starting from row 0 returned the correct key code
        """
        self._test_key_code(group_count=self.NUMBER_OF_KEYS)

        self.testCaseChecked("BUS_MEMB_0001")
    # end def test_some_available_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_some_key_pairs(self):
        """
        Check some combination of 2 keys pressed simultaneously
        """
        self.kosmos.sequencer.offline_mode = True
        pair_of_keys_list = KeyMatrixTestUtils.get_key_list(self, group_count=self.NUMBER_OF_KEYS, group_size=2)

        for key_pair in pair_of_keys_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate pressing the key pair {str(key_pair[0])} & {str(key_pair[1])}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_pair, delay=.2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate releasing the key pair {str(key_pair[0])} & {str(key_pair[1])}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_pair, delay=.2)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_pair in pair_of_keys_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report on key pair {str(key_pair[0])} & '
                                      f'{str(key_pair[1])}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_pair)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_pair[index], MAKE))
            # end for
            for index in range(len(key_pair)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_pair[index], BREAK))
            # end for
        # end for

        self.testCaseChecked("BUS_MEMB_0002")
    # end def test_two_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Business')
    @services('KeyMatrix')
    def test_some_key_triplets(self):
        """
        Check some combination of 3 keys pressed simultaneously
        """
        self.kosmos.sequencer.offline_mode = True
        key_triplets = KeyMatrixTestUtils.get_key_list(self, group_count=self.NUMBER_OF_KEYS, group_size=3)

        for key_triplet in key_triplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate pressing the key triplet {str(key_triplet[0])} & '
                                     f'{str(key_triplet[1])} & {str(key_triplet[2])}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_triplet, delay=.2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate releasing the key triplet {str(key_triplet[0])} & '
                                     f'{str(key_triplet[1])} & {str(key_triplet[2])}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_triplet, delay=.2)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_triplet in key_triplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report on key triplet {str(key_triplet[0])} & '
                                      f'{str(key_triplet[1])} & {str(key_triplet[2])}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_triplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_triplet[index], MAKE))
            # end for
            for index in range(len(key_triplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_triplet[index], BREAK))
            # end for
        # end for

        self.testCaseChecked("BUS_MEMB_0003")
    # end def test_some_key_triplets

    @features('Keyboard')
    @features('KeyCode')
    @level('Business')
    @services('KeyMatrix')
    def test_some_key_quadruplets(self):
        """
        Check some combination of 4 keys pressed simultaneously
        """
        self.kosmos.sequencer.offline_mode = True
        key_quadruplets = KeyMatrixTestUtils.get_key_list(self, group_count=self.NUMBER_OF_KEYS, group_size=4)

        for key_quadruplet in key_quadruplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key presses on the quadruplet {str(key_quadruplet[0])} & '
                                     f'{str(key_quadruplet[1])} & {str(key_quadruplet[2])} & {str(key_quadruplet[3])}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_quadruplet, delay=.2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key releases on the quadruplet {str(key_quadruplet[0])} & '
                                     f'{str(key_quadruplet[1])} & {str(key_quadruplet[2])} & {str(key_quadruplet[3])}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_quadruplet, delay=.2)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_quadruplet in key_quadruplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the HID reports on the quadruplet {str(key_quadruplet[0])} & '
                                      f'{str(key_quadruplet[1])} & {str(key_quadruplet[2])} & {str(key_quadruplet[3])}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], MAKE))
            # end for
            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], BREAK))
            # end for
        # end for

        self.testCaseChecked("BUS_MEMB_0004")
    # end def test_some_key_quadruplets

    @features('Keyboard')
    @features('KeyCode')
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_fn_key(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code
        """
        self._test_fn_key()

        self.testCaseChecked("BUS_MEMB_0005")
    # end def test_fn_key

    @features('Keyboard')
    @features('KeyCode')
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_LOCK,))
    def test_fn_lock_key(self):
        """
        Emulate a keystrocke on the Fn_lock key then check that F-Keys returned the right key code.
        """
        self._test_fn_lock_key()

        self.testCaseChecked("BUS_MEMB_0005")
    # end def test_fn_lock_key

    @features('Keyboard')
    @features('KeyCode')
    @level('Business')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_caps_lock(self):
        """
        Check some random keys are working properly when caps lock key is on.
        """
        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=self.NUMBER_OF_KEYS, group_size=1)

        for (key_id, ) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=.2, repeat=1, delay=.2)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for (key_id, ) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id, MAKE))

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        self.testCaseChecked("BUS_MEMB_0006")
    # end def test_caps_lock
# end class KeyCodeBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
